"""La comparativa: los métodos y skill por skill (1.0.52, Ezequiel, 12 de noviembre de 2026: «formas de comparar en un mismo
personaje entre uniformes... y si intento comparar entre otros personajes, que me proponga metodologías de comparación»).
Contra un modelo armado acá desde data.js (sin app.js).
  1. «Comparar sus versiones», desde la ficha: hasta 4 versiones (la de la ficha, de referencia, y las más nuevas), en
     «Qué cambia entre versiones», que es el método sugerido; el daño total de cada una y cuánto cambia; «Solo lo que
     cambia» junta al pie las skills iguales en todas; «Usar de referencia»; sin la sinergia (un personaje no va dos veces
     en un equipo). Sin uniformes, no hay botón.
  2. El desplegable de la columna cambia esa columna por otra versión del personaje.
  3. El método sugerido según lo elegido y el rol que les dan las listas (MFF_ROLES_LISTAS): los que pegan y los que las
     listas no ubican, efecto por efecto; soportes, lo que le dan al equipo; un soporte y uno que pega, lo mismo, y lo dice
     con sus nombres. Una comparación nueva abre en el sugerido aunque antes se haya elegido otro.
  4. «Para PvP»: solo las filas de lo que más pesa en PvP (MFF_CATALOGO.pvp).
  5. «En las listas»: una fila por lista en la que está alguno, con la fila de cada uno, y el rol en PvE y en PvP.
  6. En inglés. Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_ANALISIS', 'MFF_CATALOGO', 'MFF_TABLAS', 'MFF_ROLES_LISTAS', 'MFF_SEED_TIER_ASSIGNMENTS',
             'MFF_SEED_TIERLISTS', 'MFF_HISTORICO')
C, S, A, CAT, T = D['MFF_SEED_CHARACTERS'], D['MFF_SKILLS'], D['MFF_ANALISIS'], D['MFF_CATALOGO'], D['MFF_TABLAS']
ROLES, ASIG, LISTAS = D['MFF_ROLES_LISTAS'], D['MFF_SEED_TIER_ASSIGNMENTS'], D['MFF_SEED_TIERLISTS']
EF = [e['id'] for e in CAT['efectos']]
PJ = {c['id']: c for c in C}
RETRATO = {f"{c['id']}::base": c['p'] for c in C} | {f"{c['id']}::{u['id']}": u['p'] for c in C for u in c['uniforms']}
FECHA = {v[0]: v[2] for v in D['MFF_HISTORICO']['versiones']}
LLEGA = {x[0]: FECHA[x[2]] for x in D['MFF_HISTORICO']['hechos'] if x[1] in ('personaje', 'uniforme')}
SLOTS = ['Leader Skill', 'Passive', 'Tier-2 Passive', 'Uniform Passive', 'Active 1', 'Active 2', 'Active 3', 'Active 4', 'Active 5', 'Active Ult', 'Striker Skill']


# ---- el modelo ----
def dano_skill(sk):
    return sum(f['v'][T['desc'][f['p']]['pi']] for st in sk.get('st', []) for f in st.get('fx', []) if T['desc'][f['p']].get('pi') is not None and f.get('v'))


def kit(p):
    out = {}
    for si, sk in enumerate(S[p]):
        ef = {}
        for ie, d, obj, fu in A[p]['fx']:
            mias = [x for x in fu if x[0] == si]
            if not mias or EF[ie] == 'golpe': continue
            vals, duras = ef.setdefault((d, EF[ie], obj if d == 'q' else None), ([], []))
            for _, ti, fi in mias:
                f = sk['st'][ti]['fx'][fi]; i = CAT['valor'][str(f['p'])][EF[ie]]
                if i is not None: vals.append(f['v'][i])
                if f.get('d') is not None: duras.append(f['d'])
        out[sk['sl']] = (round(dano_skill(sk), 2), {k: (max(v) if v else None, max(d) if d else None) for k, (v, d) in ef.items()})
    return out


def rol(key):
    """(pega, soporte) según las filas de las listas de rol en las que está."""
    filas = [ROLES[ctx][lid][f] for ctx in ROLES for lid in ROLES[ctx] for f in ASIG.get(lid, {}).get(key, [])]
    return any(r == 'dps' and n > 0 for r, n in filas), any(r == 'soporte' and n > 0 for r, n in filas)


def sugerido(keys):
    if len({k.split('::')[0] for k in keys}) == 1: return 'kit'
    rs = [rol(k) for k in keys]
    if all(s for _, s in rs): return 'pot'
    if any(s and not p for p, s in rs) and any(p and not s for p, s in rs): return 'pot'
    return 'efecto'


def pesa_en_pvp(clave):
    d, e = clave.split('|')
    return e in CAT['pvp']['prioridad'] if d in 'ei' else d == 'q' and e in CAT['pvp']['soporte']


CON_ROL = {k: rol(k) for k in RETRATO}
PEGAN = [k for k, (p, s) in CON_ROL.items() if p and not s]
SOPORTES = [k for k, (p, s) in CON_ROL.items() if s and not p]
SIN_ROL = [k for k, (p, s) in CON_ROL.items() if not p and not s]
distintos = lambda ks, n=2: [k for i, k in enumerate(ks) if k.split('::')[0] not in {x.split('::')[0] for x in ks[:i]}][:n]
num = lambda s: float(s.replace('%', '').replace('.', '').replace(',', '.'))
srv, url = levantar(carpeta_datos(), origen_local())


def clic(pg, a, **d):
    pg.evaluate("""([a, d]) => { const el = document.createElement('button'); el.dataset.a = a; Object.assign(el.dataset, d);
        document.body.appendChild(el); el.click(); el.remove(); }""", [a, d])
    pg.wait_for_timeout(200)


def comparar(pg, keys):
    """Deja elegidas esas variantes (y nada más) y abre la comparativa desde la bandeja del roster."""
    clic(pg, 'back')
    while pg.locator('.mesa [data-a="unpick"]').count():
        pg.locator('.mesa [data-a="unpick"]').first.click(); pg.wait_for_timeout(100)
    for k in keys:
        cid, uid = k.split('::'); clic(pg, 'pick', cid=cid, uid='' if uid == 'base' else uid)
    pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_selector('.cmet')


columnas = lambda pg: pg.evaluate("[...document.querySelectorAll('.cpecab [data-a=\"unpick\"]')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base'))")
metodo = lambda pg: pg.locator('.cmetb.on').get_attribute('data-v')
sugerida = lambda pg: pg.locator('.cmetb.sug').get_attribute('data-v')

try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' and '404' not in m.text else None)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(500)

        # 1. «Comparar sus versiones»
        dor = PJ['dormammu']; versiones = ['dormammu::base'] + [f"dormammu::{u['id']}" for u in dor['uniforms']]
        clic(pg, 'open', cid='dormammu'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="cmpVersiones"]'); pg.wait_for_selector('.cmet')
        cols = columnas(pg)
        nuevas = sorted(versiones[1:], key=lambda k: LLEGA[k], reverse=True)[:3]
        ok('1 «Comparar sus versiones»: la de la ficha primero y sus otras versiones, de la más nueva a la más vieja', cols == ['dormammu::base'] + nuevas, cols)
        ok('1 abre en «Qué cambia entre versiones», que es el sugerido, y dice por qué', metodo(pg) == 'kit' and sugerida(pg) == 'kit'
           and pg.locator('.cmetb.on b').inner_text() == 'Qué cambia entre versiones' and 'versiones de Dormammu' in pg.inner_text('.cmetrazon'), pg.inner_text('.cmetrazon'))
        ok('1 los seis métodos, a la vista', pg.locator('.cmetb').count() == 6
           and [x.get_attribute('data-v') for x in pg.locator('.cmetb').all()] == ['kit', 'efecto', 'pot', 'pvp', 'listas', 'ficha'])
        kits = [kit(RETRATO[k]) for k in cols]
        totales = [round(sum(d for d, _ in k.values()), 2) for k in kits]
        vistos = [num(x) for x in pg.locator('.cktotal .cpecel .knum b').all_inner_texts()]
        deltas = pg.evaluate("[...document.querySelectorAll('.cktotal .cpecel')].map(c => c.querySelector('.kdelta') ? c.querySelector('.kdelta').textContent : '')")
        d_esp = [round(t - totales[0], 2) for t in totales]
        d_vis = [0 if not x else num(x.split()[1]) * (1 if '▲' in x else -1) for x in deltas]
        ok('1 el daño total de cada versión y cuánto cambia contra la de referencia (la primera)', vistos == totales and d_vis == d_esp
           and pg.locator('.cpefila.ckref .cpecel').first.locator('.ckesref').count() == 1, (vistos, totales, d_vis, d_esp))
        slots = [sl for sl in SLOTS if any(sl in k for k in kits)]
        quietas = [sl for sl in slots if all(sl in k for k in kits) and all(k[sl] == kits[0][sl] for k in kits)]
        filas = pg.evaluate("[...document.querySelectorAll('.ckfila')].map(f => f.dataset.sl)")
        ok('1 «Solo lo que cambia»: una fila por skill que cambia en alguna, y las iguales en todas, juntas al pie',
           pg.locator('[data-a="cmpCambios"]').is_checked() and filas == [sl for sl in slots if sl not in quietas]
           and pg.locator('.ckquietas .slotbadge').count() == len(quietas), (filas, quietas))
        iguales = pg.locator('.ckfila .ckigual').count()
        esperadas = sum(1 for sl in slots if sl not in quietas for k in kits[1:] if sl in k and sl in kits[0] and k[sl] == kits[0][sl])
        ok('1 la skill que una versión tiene igual que la referencia lo dice, sin repetir sus efectos', iguales == esperadas, (iguales, esperadas))
        pg.click('[data-a="cmpCambios"]'); pg.wait_for_timeout(200)
        ok('1 sin «Solo lo que cambia»: todas las skills', pg.evaluate("[...document.querySelectorAll('.ckfila')].map(f => f.dataset.sl)") == slots
           and pg.locator('.ckquietas').count() == 0 and pg.locator('.ckigual').count() == 0)
        pg.click('[data-a="cmpCambios"]'); pg.wait_for_timeout(200)
        pg.locator('.cpefila.ckref [data-a="cmpRef"]').first.click(); pg.wait_for_timeout(200)
        deltas = pg.evaluate("[...document.querySelectorAll('.cktotal .cpecel')].map(c => c.querySelector('.kdelta') ? c.querySelector('.kdelta').textContent : '')")
        d_vis = [0 if not x else num(x.split()[1]) * (1 if '▲' in x else -1) for x in deltas]
        ok('1 «Usar de referencia»: la referencia pasa a esa columna y los cambios se miden contra ella',
           pg.locator('.cpefila.ckref .cpecel').nth(1).locator('.ckesref').count() == 1 and d_vis == [round(t - totales[1], 2) for t in totales], d_vis)
        ok('1 versiones de un mismo personaje: sin la sinergia estimada', pg.locator('main h3', has_text='Sinergia estimada').count() == 0)
        pg.locator('.ckfila .cmpsk').first.click(); pg.wait_for_selector('#skpop')
        ok('1 el nombre de una skill abre su «Cómo funciona»', pg.locator('#skpop .tipsec').count() == 5)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        solo = next(c for c in C if not c['uniforms'])
        clic(pg, 'open', cid=solo['id']); pg.wait_for_selector('.fcab')
        ok(f'1 {solo["name"]} (sin uniformes): sin «Comparar sus versiones»', pg.locator('[data-a="cmpVersiones"]').count() == 0)

        # 2. el desplegable de la columna
        hulk = PJ['hulk']; todas = ['hulk::base'] + [f"hulk::{u['id']}" for u in hulk['uniforms']]
        clic(pg, 'open', cid='hulk'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="cmpVersiones"]'); pg.wait_for_selector('.cmet')
        cols = columnas(pg)
        ok(f'2 Hulk tiene {len(todas)} versiones: van 4, cada columna con su desplegable', len(todas) > 4 and len(cols) == 4 and pg.locator('.cpecab select.cpever').count() == 4, cols)
        libre = next(k for k in todas if k not in cols)
        opciones = pg.locator('.cpecab select.cpever').nth(1).evaluate("s => [...s.options].map(o => o.value)")
        ok('2 el desplegable ofrece la versión de la columna y las que no están en otra', sorted(opciones) == sorted([k.split('::')[1] for k in todas if k == cols[1] or k not in cols]), opciones)
        pg.locator('.cpecab select.cpever').nth(1).select_option(libre.split('::')[1]); pg.wait_for_timeout(250)
        ok('2 elegir otra cambia esa columna y deja las demás', columnas(pg) == [cols[0], libre, cols[2], cols[3]] and metodo(pg) == 'kit', columnas(pg))

        # 3. el método sugerido
        casos = [('los que pegan', distintos(PEGAN), 'efecto'), ('soportes', distintos(SOPORTES), 'pot'),
                 ('un soporte y uno que pega', distintos([SOPORTES[0]] + PEGAN), 'pot'), ('los que las listas no ubican', distintos(SIN_ROL), 'efecto')]
        for nombre, keys, esperado in casos:
            comparar(pg, keys)
            ok(f'3 {nombre} ({", ".join(keys)}): abre en «{esperado}», el sugerido del modelo', sugerido(keys) == esperado and metodo(pg) == esperado and sugerida(pg) == esperado,
               (metodo(pg), sugerida(pg), pg.inner_text('.cmetrazon')[:90]))
            if nombre == 'un soporte y uno que pega':
                a, bb = (PJ[k.split('::')[0]]['name'] for k in keys)
                ok('3 un soporte y uno que pega: lo dice con sus nombres', f'{a} da soporte y {bb} pega' in pg.inner_text('.cmetrazon'), pg.inner_text('.cmetrazon'))
        par = distintos(PEGAN)
        comparar(pg, par)
        ok('3 entre personajes distintos, la sinergia estimada sigue', pg.locator('main h3', has_text='Sinergia estimada').count() == 1)
        pg.click('[data-a="cmpVista"][data-v="ficha"]'); pg.wait_for_timeout(200)
        ok('3 se puede elegir otro método', metodo(pg) == 'ficha' and sugerida(pg) == 'efecto' and pg.locator('table.cmpt').count() == 1)
        clic(pg, 'back'); pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_selector('.cmet')
        ok('3 una comparación nueva abre otra vez en el sugerido', metodo(pg) == 'efecto')

        # 4. «Para PvP»
        pg.click('[data-a="cmpIguales"]'); pg.click('[data-a="cmpSolos"]'); pg.wait_for_timeout(250)
        todas_filas = pg.evaluate("[...document.querySelectorAll('.cpefila[data-clave]')].map(f => f.dataset.clave)")
        pg.click('[data-a="cmpVista"][data-v="pvp"]'); pg.wait_for_timeout(250)
        de_pvp = pg.evaluate("[...document.querySelectorAll('.cpefila[data-clave]')].map(f => f.dataset.clave)")
        ok('4 «Para PvP»: de las filas de «Efecto por efecto», solo las de lo que más pesa en PvP', de_pvp == [c for c in todas_filas if pesa_en_pvp(c)] and 0 < len(de_pvp) < len(todas_filas),
           (len(de_pvp), len(todas_filas)))
        pg.click('[data-a="cmpIguales"]'); pg.click('[data-a="cmpSolos"]'); pg.wait_for_timeout(200)

        # 5. «En las listas»
        pg.click('[data-a="cmpVista"][data-v="listas"]'); pg.wait_for_timeout(250)
        rotulo = {l['id']: {r['id']: r['label'] for r in l['rows']} for l in LISTAS}
        esperado = [[l['name']] + [sorted(rotulo[l['id']][f] for f in ASIG.get(l['id'], {}).get(k, [])) for k in par]
                    for l in LISTAS if any(ASIG.get(l['id'], {}).get(k) for k in par)]
        visto = pg.evaluate("""[...document.querySelectorAll('.cli .cpefila')].filter(f => f.querySelector('.cplista')).map(f =>
          [f.querySelector('.cplista').textContent].concat([...f.querySelectorAll(':scope > .cpecel')].map(c => [...c.querySelectorAll('.tag')].map(x => x.textContent).sort())))""")
        ok('5 «En las listas»: una fila por lista en la que está alguno, con la fila de cada uno', sorted(visto) == sorted(esperado) and len(visto) > 0, (len(visto), len(esperado)))
        roles = pg.evaluate("[...document.querySelectorAll('.cli .cpesec')][0].innerText")
        ok('5 el rol según las listas, en PvE y en PvP', 'PvE' in roles and 'PvP' in roles and 'pega (nivel' in roles, roles.replace('\n', ' | ')[:160])
        lista0 = pg.locator('.cli .cplista').first.inner_text()
        pg.locator('.cli .cplista').first.click(); pg.wait_for_timeout(250)
        ok('5 el nombre de una lista la abre en Tier lists', pg.locator('.tlbar .chip.on').inner_text() == lista0, lista0)

        # 6. inglés
        comparar(pg, par)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        tx = pg.inner_text('.cmet')
        ok('6 inglés: los métodos y el porqué', 'HOW TO COMPARE THEM' in tx.upper() and 'Effect by effect' in tx and 'For PvP' in tx and 'In the lists' in tx
           and not [x for x in ('Sugerida', 'Efecto por efecto', 'Las listas') if x in tx], tx[:160].replace('\n', ' | '))
        pg.click('[data-a="cmpVista"][data-v="kit"]'); pg.wait_for_timeout(250)
        tx = pg.inner_text('.ck')
        ok('6 inglés: skill por skill', 'Total damage' in tx and not [x for x in ('Daño total', 'Efectos', 'Para él') if x in tx], tx[:120].replace('\n', ' | '))
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{SALIDA}/cmp_metodos_1440.png')

        ok('sin errores de página ni de consola', not errores, errores[:4])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
