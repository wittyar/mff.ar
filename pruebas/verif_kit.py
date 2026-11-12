"""El kit de un vistazo (1.0.52, Ezequiel, 12 de noviembre de 2026: «una mejor visual de las habilidades... formas de comparar
en un mismo personaje entre uniformes»): la tabla de arriba de la pestaña Skills, contra un modelo armado acá desde data.js
(sin app.js).
  1. En una muestra de variantes (una de cada 12, más las que se nombran): una fila por skill, con su daño (la suma de sus
     golpes), su parte del total y sus efectos repartidos por a quién le llegan (él y sus invocaciones, el equipo, el rival)
     según MFF_ANALISIS; el total; lo que el catálogo no clasifica.
  2. «Comparar con» otra versión del personaje: la skill nueva, lo que suma («+»), lo que cambia («≠», con lo de antes) y lo
     que pierde (tachado), y cuánto cambia el daño, contra el modelo; se apaga al pasar a otro personaje.
  3. El nombre de una fila lleva a la skill del detalle (resaltada); un efecto abre su «Cómo funciona» en ese efecto.
  4. El detalle: la etiqueta de cada efecto lleva el color de su destino.
  5. En inglés y en el celular (sin desborde). Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_ANALISIS', 'MFF_CATALOGO', 'MFF_TABLAS')
C, S, A, CAT, T = D['MFF_SEED_CHARACTERS'], D['MFF_SKILLS'], D['MFF_ANALISIS'], D['MFF_CATALOGO'], D['MFF_TABLAS']
EF = [e['id'] for e in CAT['efectos']]
PJ = {c['id']: c for c in C}
VARS = [(c['id'], '', c['p']) for c in C] + [(c['id'], u['id'], u['p']) for c in C for u in c['uniforms']]


# ---- el modelo ----
def dano_skill(sk):
    n = 0
    for st in sk.get('st', []):
        for f in st.get('fx', []):
            pi = T['desc'][f['p']].get('pi')
            if pi is not None and f.get('v'): n += f['v'][pi]
    return n


def valor(f, e):
    i = CAT['valor'][str(f['p'])][e]
    return None if i is None else f['v'][i]


def kit(p):
    """Por skill: su daño y sus efectos {(destino, efecto, aliados): (mayor número, mayor duración)}; los que no clasifica."""
    out = []
    for si, sk in enumerate(S[p]):
        ef = {}
        for ie, d, obj, fu in A[p]['fx']:
            mias = [x for x in fu if x[0] == si]
            if not mias or EF[ie] == 'golpe': continue
            k = (d, EF[ie], obj if d == 'q' else None)
            vals, duras = ef.get(k, ([], []))
            for _, ti, fi in mias:
                f = sk['st'][ti]['fx'][fi]
                if valor(f, EF[ie]) is not None: vals.append(valor(f, EF[ie]))
                if f.get('d') is not None: duras.append(f['d'])
            ef[k] = (vals, duras)
        out.append(dict(sl=sk['sl'], dano=dano_skill(sk), sc=sum(1 for x in A[p].get('sc', []) if x[0] == si),
                        ef={k: (max(v) if v else None, max(d) if d else None) for k, (v, d) in ef.items()}))
    return out


def columnas(k):
    cuenta = lambda ds: sum(1 for (d, _, _) in k['ef'] if d in ds)
    return [cuenta('ei'), cuenta('q'), cuenta('r')]


def diferencia(a, ref):
    """Lo que cambia de un kit contra otro, por slot: nueva, o cuántos efectos suma, cambia y pierde, y el daño."""
    de = {k['sl']: k for k in ref}
    out = {}
    for k in a:
        r = de.get(k['sl'])
        if not r: out[k['sl']] = 'nueva'; continue
        out[k['sl']] = dict(nuevo=sum(1 for x in k['ef'] if x not in r['ef']), cambia=sum(1 for x, v in k['ef'].items() if x in r['ef'] and r['ef'][x] != v),
                            perdido=sum(1 for x in r['ef'] if x not in k['ef']), dano=round(k['dano'] - r['dano'], 2))
    return out, [k['sl'] for k in ref if k['sl'] not in {x['sl'] for x in a}]


num = lambda s: float(s.replace('%', '').replace('.', '').replace(',', '.'))
LEER = """() => ({
  total: document.querySelector('#kit .kittotal').textContent,
  filas: [...document.querySelectorAll('#kit .kittabla .kitfila:not(.cab):not(.perdida)')].map(f => ({
    nueva: f.classList.contains('nueva'),
    dano: f.querySelector('.kitc.dano .knum b') ? f.querySelector('.kitc.dano .knum b').textContent : null,
    parte: f.querySelector('.kitc.dano .knum small') ? f.querySelector('.kitc.dano .knum small').textContent : null,
    delta: f.querySelector('.kitc.dano .kdelta') ? f.querySelector('.kitc.dano .kdelta').textContent : null,
    cols: [...f.querySelectorAll('.kitc.fx')].map(c => [...c.querySelectorAll('button.kfx')].map(x => x.classList[1])),
    marcas: ['nuevo', 'cambia', 'perdido'].map(m => f.querySelectorAll('.kfx.' + m).length),
    sc: f.querySelector('.kfx.sc') ? f.querySelector('.kfx.sc').textContent : null })),
  perdidas: document.querySelectorAll('#kit .kitfila.perdida').length })"""


def abrir(pg, cid, uid):
    pg.evaluate("""([cid, uid]) => { const el = document.createElement('button'); el.dataset.a = 'open'; el.dataset.cid = cid; if (uid) el.dataset.uid = uid;
        document.body.appendChild(el); el.click(); el.remove(); }""", [cid, uid])
    pg.wait_for_selector('.fcab')
    if pg.locator('.ftab.on').get_attribute('data-v') != 'skills': pg.click('[data-a="fichaTab"][data-v="skills"]')
    pg.wait_for_selector('#kit')


def revisar(r, p):
    """Las filas del kit que muestra la app contra el modelo: lista de diferencias."""
    m, mal = kit(p), []
    total = sum(k['dano'] for k in m)
    if len(r['filas']) != len(m): return [('filas', len(r['filas']), len(m))]
    if abs(num(r['total'].split(':')[1].split('%')[0]) - total) > 0.01: mal.append(('total', r['total'], total))
    for f, k in zip(r['filas'], m):
        if (num(f['dano']) if f['dano'] else 0) != round(k['dano'], 2): mal.append((k['sl'], 'daño', f['dano'], k['dano']))
        if k['dano'] and not f['parte'].startswith(f"{round(100 * k['dano'] / total)}% "): mal.append((k['sl'], 'parte', f['parte'], round(100 * k['dano'] / total)))
        if [len(c) for c in f['cols']] != columnas(k): mal.append((k['sl'], 'efectos por destino', [len(c) for c in f['cols']], columnas(k)))
        if any(x not in ds for c, ds in zip(f['cols'], ('ei', 'q', 'r')) for x in c): mal.append((k['sl'], 'un efecto en la columna de otro destino', f['cols']))
        if bool(f['sc']) != bool(k['sc']) or (k['sc'] and not f['sc'].startswith(str(k['sc']) + ' ')): mal.append((k['sl'], 'sin clasificar', f['sc'], k['sc']))
    return mal


srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' and '404' not in m.text else None)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(500)

        # 1. la tabla contra el modelo
        muestra = VARS[::12] + [v for v in VARS if v[0] in ('dormammu', 'hulk', 'wong', 'jeff-the-land-shark', 'black-cat', 'sentry')]
        malas = {}
        for cid, uid, pp in muestra:
            abrir(pg, cid, uid)
            mal = revisar(pg.evaluate(LEER), pp)
            if mal: malas[f'{cid}::{uid or "base"}'] = mal[:3]
        ok(f'1 el kit de {len(muestra)} variantes: filas, daño, parte del total, efectos por destino y sin clasificar, como el modelo', not malas, dict(list(malas.items())[:3]))
        abrir(pg, 'dormammu', '')
        r = pg.evaluate(LEER); m = kit(PJ['dormammu']['p'])
        mayor = max(m, key=lambda k: k['dano'])
        ancho = pg.evaluate("[...document.querySelectorAll('#kit .kbarra i')].map(i => i.style.width)")
        ok('1 Dormammu: la barra de la skill que más pega va entera y las demás en proporción', '100%' in ancho and len(ancho) == sum(1 for k in m if k['dano']), ancho)
        ok('1 Dormammu: la leyenda de los destinos y el total', 'Para él' in pg.inner_text('#kit .kitley') and 'Contra el rival' in pg.inner_text('#kit .kitley')
           and r['total'].startswith('Daño total:'), (pg.inner_text('#kit .kitley'), r['total'], mayor['sl']))

        # 2. comparar con otra versión
        con_uniformes = [c for c in C if c['uniforms']][::9][:14] + [PJ['dormammu'], PJ['hulk']]
        malas = {}
        for c in con_uniformes:
            u = c['uniforms'][-1]
            abrir(pg, c['id'], u['id'])
            pg.select_option('#kit [data-a="kitCon"]', 'base'); pg.wait_for_timeout(150)
            r = pg.evaluate(LEER)
            esperado, sobran = diferencia(kit(u['p']), kit(c['p']))
            mal = []
            for f, k in zip(r['filas'], kit(u['p'])):
                e = esperado[k['sl']]
                if e == 'nueva':
                    if not f['nueva'] or f['marcas'] != [0, 0, 0]: mal.append((k['sl'], 'nueva', f['nueva'], f['marcas']))
                    continue
                if f['nueva'] or f['marcas'] != [e['nuevo'], e['cambia'], e['perdido']]: mal.append((k['sl'], f['marcas'], e))
                visto = 0 if not f['delta'] else num(f['delta'].split()[1]) * (1 if '▲' in f['delta'] else -1)
                if visto != e['dano']: mal.append((k['sl'], 'daño', f['delta'], e['dano']))
            if r['perdidas'] != len(sobran): mal.append(('skills que solo tiene la otra', r['perdidas'], sobran))
            if mal: malas[c['id']] = mal[:3]
        ok(f'2 «Comparar con» la base, en {len(con_uniformes)} uniformes: nueva, suma, cambia, pierde y el daño, como el modelo', not malas, dict(list(malas.items())[:3]))
        abrir(pg, 'dormammu', PJ['dormammu']['uniforms'][-1]['id'])
        pg.select_option('#kit [data-a="kitCon"]', 'base'); pg.wait_for_timeout(150)
        pg.select_option('select[data-a="uniformSel"]', PJ['dormammu']['uniforms'][0]['id']); pg.wait_for_timeout(250)
        ok('2 la comparación sigue al cambiar de uniforme dentro del personaje, con su nota', pg.locator('#kit [data-a="kitCon"]').input_value() == 'base'
           and 'Contra Base' in pg.inner_text('#kit .kitdif') and pg.locator('#kit .kfx.nuevo, #kit .kfx.perdido, #kit .kitfila.nueva').count() > 0, pg.inner_text('#kit .kitdif'))
        antes = pg.locator('#kit .kfx.cambia .kantes').first.inner_text() if pg.locator('#kit .kfx.cambia').count() else 'antes'
        ok('2 lo que cambia dice lo de antes', antes.startswith('antes'), antes)
        abrir(pg, 'hulk', PJ['hulk']['uniforms'][-1]['id'])
        ok('2 al pasar a otro personaje, se apaga', pg.locator('#kit [data-a="kitCon"]').input_value() == '' and pg.locator('#kit .kitdif').count() == 0)
        abrir(pg, 'wong', '')
        solo = next(c for c in C if not c['uniforms'])
        abrir(pg, solo['id'], '')
        ok(f'2 {solo["name"]} (sin uniformes): sin «Comparar con»', pg.locator('#kit [data-a="kitCon"]').count() == 0)

        # 3. del kit al detalle y al «Cómo funciona»
        abrir(pg, 'dormammu', '')
        fila = pg.locator('#kit .kitfila:not(.cab)').nth(len(m) - 2)        # la definitiva
        fila.locator('[data-a="kitIr"]').click(); pg.wait_for_timeout(200)
        r = pg.evaluate("""() => { const el = document.querySelector('.resaltada'); const c = document.querySelector('.fcab').getBoundingClientRect().bottom;
          return el && { id: el.id, n: document.querySelectorAll('.resaltada').length, top: el.getBoundingClientRect().top, cab: c, alto: innerHeight }; }""")
        ok('3 el nombre de una fila lleva a esa skill del detalle, resaltada y a la vista', r and r['n'] == 1 and r['id'].startswith('sk-') and r['cab'] - 2 <= r['top'] < r['alto'], r)
        pg.evaluate("window.scrollTo(0, 0)")
        chip = fila.locator('button.kfx').first
        st, fx, nombre = chip.get_attribute('data-st'), chip.get_attribute('data-fx'), chip.locator('b').inner_text()
        chip.click(); pg.wait_for_selector('#skpop')
        ok('3 un efecto abre el «Cómo funciona» de su skill, en ese efecto', pg.locator('#skpop .tipef.foco').count() >= 1
           and nombre.lower() in pg.locator('#skpop .tipef.foco').first.inner_text().lower(), (nombre, st, fx, pg.locator('#skpop .tipef.foco').all_inner_texts()[:1]))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        ok('3 se cierra con Escape', pg.locator('#skpop').count() == 0)

        # 4. el detalle: la etiqueta de cada efecto, con el color de su destino
        colores = pg.evaluate("""() => { const o = {}; for (const x of document.querySelectorAll('.skill .fxtag')) { const c = [...x.classList].find(k => k.startsWith('d-')) || 'sin'; o[c] = (o[c] || 0) + 1; } return o; }""")
        lider = pg.evaluate("[...document.querySelector('.skill').querySelectorAll('.fxtag')].map(x => x.className)")
        ok('4 el detalle: las etiquetas llevan su destino (el liderazgo, para el equipo)', colores.get('d-e', 0) > 0 and colores.get('d-r', 0) > 0
           and all('d-q' in x for x in lider) and colores.get('sin', 0) == 0, (colores, lider))

        # 5. inglés y celular
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        tx = pg.inner_text('#kit')
        ok('5 inglés: el kit en inglés', 'THE KIT AT A GLANCE' in tx.upper() and 'Total damage' in tx and 'Compare with' in tx
           and not [x for x in ('Daño total', 'Para él', 'Comparar con', 'barra de ult', 'constante') if x in tx], tx[:120])
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(300)
        fuera = pg.evaluate("""() => { const lim = document.getElementById('fcuerpo').getBoundingClientRect().right;
          return { doc: document.documentElement.scrollWidth, fuera: [...document.querySelectorAll('#kit *')].filter(e => e.getBoundingClientRect().width && e.getBoundingClientRect().right > lim + 0.5).map(e => e.className).slice(0, 4) }; }""")
        ok('5 celular: el kit no se sale de la columna', fuera['doc'] <= 390 and not fuera['fuera'], fuera)
        pg.screenshot(path=f'{SALIDA}/kit_390.png')
        pg.set_viewport_size({'width': 1440, 'height': 900}); pg.wait_for_timeout(200)
        pg.screenshot(path=f'{SALIDA}/kit_1440.png')

        ok('sin errores de página ni de consola', not errores, errores[:4])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
