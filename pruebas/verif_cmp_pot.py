"""Comparativa por potenciador (Ezequiel, 11 de octubre de 2026): una fila por potenciador con lo que tiene cada uno de
sus skills, su liderazgo, su soporte y su artefacto; el tooltip de cada fuente; la suma por grupo de a quiénes llega (lo
que se acumula se suma, lo que no cuenta la mayor); y al pie, a quiénes del roster les llega. Las filas, las fuentes y la
suma para él se cuentan acá, con los datos y sin app.js."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_ANALISIS', 'MFF_CATALOGO', 'MFF_SKILLS', 'MFF_TABLAS', 'MFF_ARTEFACTOS')
C, AN, CAT, SK, TB = D['MFF_SEED_CHARACTERS'], D['MFF_ANALISIS'], D['MFF_CATALOGO'], D['MFF_SKILLS'], D['MFF_TABLAS']
ART = {a['p']: a for a in D['MFF_ARTEFACTOS']}
E = CAT['efectos']
por_nombre = {c['name']: c for c in C}
PJ = ['Magneto', 'Shang-Chi', 'Agent Venom', 'Jean Grey']
EST = '6'


def valor(f, ef):
    """El número del efecto ef en el efecto de skill f, como valorFx: (n, pct) o None."""
    i = CAT['valor'][str(f['p'])][ef]
    if i is None:
        return None
    patron, pos = TB['desc'][f['p']]['en'], -1
    for _ in range(i + 1):
        pos = patron.index('#', pos + 1)
    return (f['v'][i], patron[pos + 1:pos + 2] == '%')


def cumple(r, c):
    cat, val = r
    return {'Ability': val in c['abilities'], 'Type': c['c'] == val, 'Side': c['f'] == val, 'Allies': c['race'] == val,
            'Character': c['name'] == val}[cat]


def modelo(c):
    """{efecto: [fuentes (dest, valor o None, sumable)]} del personaje c sin uniforme."""
    p, out = c['p'], {}
    vistas = set()
    for ie, d, obj, fuentes in AN[p]['fx']:
        e = E[ie]
        if d == 'r' or e['grupo'] == 'golpe' or e['id'] == 'otorga':
            continue
        dest = 'propio' if d == 'e' else 'inv' if d == 'i' else '|'.join(TB['tgt'][obj]['r']) if TB['tgt'][obj].get('r') else 'todos'
        for si, ti, fi in fuentes:
            sk = SK[p][si]; f = sk['st'][ti]['fx'][fi]
            clave = (e['id'], sk['sl'], f['p'], tuple(map(str, f.get('v', []))), f.get('d'), dest)
            if clave in vistas:
                continue
            vistas.add(clave)
            v = valor(f, e['id'])
            out.setdefault(e['id'], []).append((dest, v, v is not None))
    a = ART.get(p)
    if a:
        dest = 'propio' if a['a'] == 'propio' else '|'.join(a['a']) if a['a'] else 'todos'
        for f in a['fx']:
            efs = CAT['soporte'][f['s']]['efectos']; ln = a['lineas'][f['l']]['t']
            n = a['valores'][EST][f['p'] - 1] if f['p'] is not None and len(a['valores'][EST]) >= f['p'] else None
            v = (float(n), f'[P{f["p"]}]%' in ln) if n is not None else None
            for ef in efs:
                out.setdefault(ef, []).append((dest, v, v is not None and len(efs) == 1))
    return out


def num(n, pct):
    r = round(n * 100) / 100
    s = (f'{r:.2f}'.rstrip('0').rstrip('.') if r != int(r) else str(int(r))).replace('.', ',')
    return s + ('%' if pct else '')


def suma_el(c, fs, acumula):
    """El texto de la suma para él (como sumaPot), o None si no hay al menos dos fuentes con número."""
    nums = [x for x in fs if x[2]]
    if len(nums) < 2:
        return None
    llegan = [x for x in nums if x[0] in ('propio', 'todos') or (x[0] != 'inv' and cumple(x[0].split('|'), c))]
    if not llegan:
        return None
    por = {}
    for _, (n, pct), _ in llegan:
        por[pct] = por.get(pct, 0) + n if acumula else max(por.get(pct, float('-inf')), n)
    return ' · '.join(num(n, pct) for pct, n in por.items())


srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(200)
        for n in PJ:
            pg.fill('#q', n); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{por_nombre[n]["id"]}"][data-uid=""]'); pg.wait_for_timeout(150)
        pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_timeout(500)
        pg.click('[data-a="cmpVista"][data-v="pot"]'); pg.wait_for_timeout(500)
        ok('la vista «Por potenciador»', pg.locator('.cpb').count() == 1)

        # 1. filas y fuentes
        M = [modelo(por_nombre[n]) for n in PJ]
        esp = set().union(*M)
        got = pg.evaluate("""() => [...document.querySelectorAll('.cpb .cpefila')].map(f => [f.dataset.e,
            [...f.querySelectorAll(':scope > .cpecel')].map(c => [c.querySelectorAll('.cpbfu').length,
              [...c.querySelectorAll('.cpbsuma > span')].map(s => s.textContent.trim())])])""")
        filas = {e: cel for e, cel in got}
        ok(f'1 una fila por potenciador de los cuatro ({len(esp)})', set(filas) == esp and len(filas) == len(got),
           {'faltan': sorted(esp - set(filas)), 'sobran': sorted(set(filas) - esp)})
        malas = [(e, k, len(M[k].get(e, [])), filas[e][k][0]) for e in esp & set(filas) for k in range(len(PJ))
                 if len(M[k].get(e, [])) != filas[e][k][0]]
        ok('1 cuántas fuentes tiene cada uno en cada fila', not malas, malas[:5])

        # 2. la suma para él
        acum = {e['id']: e.get('acumula') for e in E}
        malas, vistas = [], 0
        for e in esp & set(filas):
            for k, n in enumerate(PJ):
                s = suma_el(por_nombre[n], M[k].get(e, []), acum[e])
                el = next((x for x in filas[e][k][1] if x.startswith('Él:')), None)
                if s is not None:
                    vistas += 1
                if (s is None) != (el is None) or (s is not None and el != f'Él: {s}'):
                    malas.append((e, n, s, el))
        ok(f'2 la suma para él ({vistas} celdas con suma)', not malas and vistas > 0, malas[:5])
        ok('2 Magneto, todos los ataques: su liderazgo a los mutantes le llega (15 + 40 + 45)',
           'Él: 100%' in filas['ataques_todos'][0][1], filas['ataques_todos'][0][1])

        # 3. tooltip: de dónde sale
        fu = pg.locator('.cpb .cpefila[data-e="ataques_todos"] .cpecel').first.locator('.cpbfu', has=pg.locator('.slotbadge.lead')).first
        fu.hover(); pg.wait_for_timeout(150)
        tip = fu.locator('.cpbtip')
        ok('3 el tooltip del liderazgo dice de dónde sale, a quién llega y que cuenta si lidera',
           tip.is_visible() and 'Liderazgo' in tip.inner_text() and 'Aliados mutantes' in tip.inner_text() and 'lidera' in tip.inner_text(),
           tip.inner_text() if tip.count() else 'sin tooltip')
        pg.screenshot(path=f'{SALIDA}/cmp_pot_1440.png')

        # 4. pie: a quiénes del roster; el grupo abre la lista
        boton = pg.locator('.cpb .cpefila[data-e="dano_contra"] .cpbpie [data-a="verGrupo"]').first
        n_sim = sum(1 for c in C if any(cumple(['Ability', 'Simbionte'], {'abilities': u.get('ab', c['abilities']), 'c': u.get('c', c['c']),
                    'f': u.get('f', c['f']), 'race': u.get('race', c['race']), 'name': c['name']}) for u in [{}] + c['uniforms']))
        ok('4 el pie del artefacto de Agent Venom: aliados simbiontes, con cuántos', boton.count() == 1
           and f'{n_sim} personajes' in boton.inner_text().lower(), (n_sim, boton.inner_text() if boton.count() else 'sin botón'))
        boton.click(); pg.wait_for_timeout(200)
        cids = pg.evaluate("[...new Set([...document.querySelectorAll('.modal.ancho .altile')].map(t => t.dataset.cid))].length")
        ok('4 abre la lista de esos personajes (uno o más retratos por personaje)', cids == n_sim, cids)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)

        # 5. las estrellas del artefacto cambian el número
        celda = pg.locator('.cpb .cpefila[data-e="ignorar_evasion"] .cpecel').nth(1)
        antes = celda.locator('.cpbfu').first.locator('.cpev').inner_text()
        pg.click('.cpbest [data-a="artEst"][data-v="3"]'); pg.wait_for_timeout(300)
        despues = pg.locator('.cpb .cpefila[data-e="ignorar_evasion"] .cpecel').nth(1).locator('.cpbfu').first.locator('.cpev').inner_text()
        a = ART[por_nombre['Shang-Chi']['p']]; f = next(x for x in a['fx'] if x['s'] == 'Ignore Dodge')
        ok('5 Shang-Chi, ignorar esquiva: el número del artefacto según las estrellas',
           (antes, despues) == (a['valores']['6'][f['p'] - 1] + '%', a['valores']['3'][f['p'] - 1] + '%'), (antes, despues))

        # 6. celular: sin desborde
        pg.set_viewport_size({'width': 390, 'height': 800}); pg.wait_for_timeout(300)
        ancho = pg.evaluate('document.documentElement.scrollWidth')
        ok('6 celular: sin desborde horizontal', ancho <= 390, ancho)
        pg.screenshot(path=f'{SALIDA}/cmp_pot_390.png', full_page=False)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
