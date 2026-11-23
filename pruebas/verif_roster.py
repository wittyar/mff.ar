"""Mi cuenta › Tu roster (1.0.59; Ezequiel, 23 de noviembre de 2026, «Dale con todo» al planificador con tu roster): a quién
tenés y en qué categoría, marcado en lote. Es la hoja de ruta de cada personaje (U.ruta, la de su ficha), y el uniforme con
que lo usás (U.uniforme). Lo que se espera sale de data.js (MFF_SEED_CHARACTERS, la hoja de ruta de MFF_GUIA) y de la capa
guardada (/api/capa), no de app.js:
  1. Vacío: un renglón por personaje del juego, «Tenés 0»; cada uno ofrece No, T1, 6★, T2 y, según hasta dónde llega en el
     juego, T3 (TP si trasciende) y T4.
  2. Marcar en lote: un toque por personaje deja su paso en la capa; el del uniforme también; tocar la categoría que ya tiene
     no pisa un paso intermedio (Nv. 70) marcado en la ficha; «No» lo saca de la capa con su uniforme. La sub-barra lo
     cuenta y la ficha (pestaña «Mi cuenta») muestra la misma hoja de ruta.
  3. Búsqueda, «Los que tenés» / «Los que no» y los filtros del roster (un personaje está si alguna versión pasa).
  4. Al recargar sigue todo.
  5. Exportar «Mi capa» trae la hoja de ruta y los uniformes; importar los reemplaza; una capa de la 1.0.58 (sin uniformes)
     entra; una con los uniformes mal formados no entra y lo dice; un uniforme que ya no está en los datos queda con aviso.
  6. En el celular, sin desbordar. Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import SALIDA  # noqa: E401
import json, re, tempfile
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_GUIA')
PJ = {c['id']: c for c in D['MFF_SEED_CHARACTERS']}
PASOS = [p['id'] for p in D['MFF_GUIA']['progresion']['pasos']]
# El modelo: qué toques ofrece cada personaje (hasta el paso de antes del Tier que no tiene) y cómo se rotulan.
TOQUES = ['desbloqueo', 't1', 't2', 't3', 't4']
def toques(c):
    corte = {'T2': 't3', 'T3': 't4'}.get(c['t'])
    hasta = PASOS.index(corte) if corte else len(PASOS)
    return [x for x in TOQUES if PASOS.index(x) < hasta]
ROT = {'desbloqueo': 'T1', 't1': '6★', 't2': 'T2', 't3': 'T3', 't4': 'T4'}
rot = lambda c, x: 'TP' if x == 't3' and c['trans'] else ROT[x]
CON_UNI = next(c for c in sorted(PJ.values(), key=lambda c: c['name']) if len(c['uniforms']) >= 2 and c['t'] == 'T4')
T2 = next(c for c in PJ.values() if c['t'] == 'T2')
TP = next(c for c in PJ.values() if c['trans'] and c['t'] == 'T3')

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1400, 'height': 900}, accept_downloads=True)
        pg = ctx.new_page(); errores, alertas = [], []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' and '404' not in m.text else None)
        pg.on('dialog', lambda d: (alertas.append(d.message), d.accept()))
        pg.goto(url); pg.wait_for_selector('.ccard')
        capa = lambda: (pg.wait_for_timeout(300), pg.evaluate("fetch('/api/capa', { headers: { 'X-MFF': '1' } }).then(r => r.json())")['capa'])[1]
        def ir():
            pg.click('nav.topnav [data-a="goCuenta"]'); pg.wait_for_selector('.cuhub')
            pg.click('.cutabs [data-a="cuentaTab"][data-v="roster"]'); pg.wait_for_selector('.roslista')
        def fila(c):
            pg.fill('#q', c['name']); pg.wait_for_timeout(250)
            return pg.locator('.rosfila').filter(has=pg.locator('.who', has_text=re.compile('^' + re.escape(c['name']) + '$'))).first
        def tocar(c, x):
            fila(c).locator(f'[data-a="rosPaso"][data-v="{x}"]').click(); pg.wait_for_timeout(250)
        FILAS = """[...document.querySelectorAll('.rosfila')].map(f => [f.querySelector('.who').textContent,
            [...f.querySelectorAll('[data-a="rosPaso"]')].map(b => [b.dataset.v, b.textContent.trim(), b.classList.contains('on')])])"""

        # 1. vacío
        ir()
        filas = pg.evaluate(FILAS)
        ok('1 un renglón por personaje del juego', len(filas) == len(PJ), (len(filas), len(PJ)))
        ok('1 «Tenés 0 de N»', f'Tenés 0 de {len(PJ)}' in pg.locator('.rosbarra').inner_text(), pg.locator('.rosbarra').inner_text())
        por_nombre = {}
        for c in PJ.values(): por_nombre.setdefault(c['name'], []).append(c)
        mal = []
        for nombre, bs in filas:
            cs = por_nombre[nombre]
            espera = [('', 'No', True)] + [(x, rot(c, x), False) for c in cs[:1] for x in toques(c)]
            if [tuple(x) for x in bs] != espera and len(cs) == 1: mal.append((nombre, bs, espera))
        ok('1 cada uno ofrece No, T1, 6★, T2 y hasta donde llega (T3 o TP, T4), con «No» marcado', not mal, mal[:3])
        ok('1 un T2 no ofrece T3 ni T4; uno que trasciende dice TP', fila(T2).locator('[data-a="rosPaso"]').all_inner_texts() == ['No', 'T1', '6★', 'T2']
           and 'TP' in fila(TP).locator('[data-a="rosPaso"]').all_inner_texts(), (T2['name'], TP['name']))

        # 2. marcar en lote
        MARCA = {'thor': 't3', 'hulk': 't2', CON_UNI['id']: 't4', T2['id']: 'desbloqueo', TP['id']: 't3'}
        for cid, x in MARCA.items(): tocar(PJ[cid], x)
        ok('2 un toque por personaje deja su paso en la capa', capa()['ruta'] == MARCA, capa()['ruta'])
        f = fila(CON_UNI)
        ok('2 el marcado queda encendido y ofrece el uniforme', f.locator('[data-a="rosPaso"].on').inner_text() == 'T4'
           and f.locator('select[data-a="rosUni"] option').count() == 1 + len(CON_UNI['uniforms']))
        uni = CON_UNI['uniforms'][1]
        f.locator('select[data-a="rosUni"]').select_option(uni['id']); pg.wait_for_timeout(300)
        ok('2 el uniforme con que lo usás va a la capa', capa()['uniforme'] == {CON_UNI['id']: uni['id']}, capa().get('uniforme'))
        ok('2 un personaje sin marcar no ofrece uniforme', fila(PJ['wolverine']).locator('select[data-a="rosUni"]').count() == 0)
        # Un paso intermedio (Nv. 70, marcado en la ficha) no se pisa con el toque de su categoría; otro toque sí lo cambia.
        pg.evaluate("""(c) => fetch('/api/capa', { headers: { 'X-MFF': '1' } }).then(r => r.json()).then(x => {
            x.capa.ruta[c] = 'n70'; return fetch('/api/capa', { method: 'PUT', headers: { 'X-MFF': '1', 'Content-Type': 'application/json' }, body: JSON.stringify(x.capa) }); })""", 'hulk')
        pg.reload(); pg.wait_for_selector('.ccard'); ir()
        f = fila(PJ['hulk'])
        ok('2 un paso intermedio se ve en su categoría y se dice', f.locator('[data-a="rosPaso"].on').inner_text() == 'T2' and 'Nv. 70' in f.inner_text(), f.inner_text())
        tocar(PJ['hulk'], 't2')
        ok('2 tocar la categoría que ya tiene no pisa el Nv. 70', capa()['ruta']['hulk'] == 'n70', capa()['ruta'])
        tocar(PJ['hulk'], 't3')
        ok('2 otro toque lo cambia', capa()['ruta']['hulk'] == 't3', capa()['ruta'])
        pg.click('.cutabs [data-a="cuentaTab"][data-v="resumen"]'); pg.wait_for_timeout(200)
        n = len(capa()['ruta'])
        ok('2 la sub-barra y el resumen lo cuentan', pg.locator('.cutab', has_text='Tu roster').locator('.cun').inner_text() == str(n)
           and pg.locator('.cutile', has_text='Personajes que tenés').locator('.v').inner_text() == str(n))
        pg.evaluate("(c) => { const el = document.createElement('button'); el.dataset.a = 'abrirEn'; el.dataset.cid = c; el.dataset.tab = 'cuenta'; document.body.appendChild(el); el.click(); el.remove(); }", 'thor')
        pg.wait_for_selector('ol.ruta')
        ok('2 la ficha (pestaña «Mi cuenta») muestra la misma hoja de ruta', pg.locator('ol.ruta li.hecho').count() == PASOS.index('t3') + 1,
           pg.locator('ol.ruta li.hecho').count())
        ir(); tocar(PJ[CON_UNI['id']], '')
        ok('2 «No» lo saca de la capa, con su uniforme', CON_UNI['id'] not in capa()['ruta'] and capa()['uniforme'] == {}, capa())
        tocar(PJ[CON_UNI['id']], 't4'); fila(CON_UNI).locator('select[data-a="rosUni"]').select_option(uni['id']); pg.wait_for_timeout(300)

        # 3. búsqueda y filtros
        pg.fill('#q', ''); pg.wait_for_timeout(250)
        pg.click('[data-a="rosTen"][data-v="si"]'); pg.wait_for_timeout(250)
        tengo = sorted(PJ[c]['name'] for c in capa()['ruta'])
        ok('3 «Los que tenés»', sorted(pg.locator('.rosfila .who').all_inner_texts()) == tengo, pg.locator('.rosfila .who').all_inner_texts())
        pg.click('[data-a="rosTen"][data-v="no"]'); pg.wait_for_timeout(250)
        ok('3 «Los que no»', pg.locator('.rosfila').count() == len(PJ) - len(tengo))
        pg.click('[data-a="rosTen"][data-v="todos"]'); pg.wait_for_timeout(250)
        pg.click('[data-a="plFiltros"]'); pg.click('.plpanel [data-a="filter"][data-cat="c"][data-v="Combate"]'); pg.wait_for_timeout(300)
        espera = sorted(c['name'] for c in PJ.values() if c['c'] == 'Combate' or any(u.get('c') == 'Combate' for u in c['uniforms']))
        vistos = sorted(pg.locator('.rosfila .who').all_inner_texts())
        ok('3 el filtro de clase del roster: alguna versión de Combate', vistos == espera, (len(vistos), len(espera)))
        pg.click('[data-a="clearFilters"]'); pg.wait_for_timeout(250); pg.click('[data-a="plFiltros"]'); pg.wait_for_timeout(200)

        # 4. al recargar
        antes = capa()
        pg.reload(); pg.wait_for_selector('.ccard'); ir()
        ok('4 al recargar, sigue todo', fila(CON_UNI).locator('[data-a="rosPaso"].on').inner_text() == 'T4'
           and fila(CON_UNI).locator('select[data-a="rosUni"]').input_value() == uni['id'] and capa()['ruta'] == antes['ruta'])

        # 5. exportar e importar
        pg.click('.cutabs [data-a="cuentaTab"][data-v="capa"]'); pg.wait_for_timeout(300)
        with pg.expect_download() as dl:
            pg.click('[data-a="exportUser"]')
        exp = json.load(open(dl.value.path(), encoding='utf-8'))
        ok('5 exportar trae la hoja de ruta y los uniformes', exp.get('ruta') == antes['ruta'] and exp.get('uniforme') == antes['uniforme'], (exp.get('ruta'), exp.get('uniforme')))
        d = tempfile.mkdtemp(prefix='mffros-')
        def importar(x):
            fa = os.path.join(d, 'capa.json'); json.dump(x, open(fa, 'w', encoding='utf-8'))
            pg.set_input_files('input[data-a="importUser"]', fa); pg.wait_for_timeout(600)
        otra = dict(exp, ruta={'wolverine': 't2'}, uniforme={})
        importar(otra)
        ok('5 importar reemplaza la hoja de ruta y los uniformes', capa()['ruta'] == {'wolverine': 't2'} and capa()['uniforme'] == {}, (capa()['ruta'], capa()['uniforme']))
        de58 = {k: v for k, v in exp.items() if k != 'uniforme'}
        importar(de58)
        ok('5 una capa de la 1.0.58 (sin uniformes) entra con su hoja de ruta', capa()['ruta'] == exp['ruta'] and capa()['uniforme'] == {} and not alertas, alertas)
        importar(dict(exp, uniforme=['x']))
        ok('5 una con los uniformes mal formados no entra y lo dice', alertas and 'uniformes' in alertas[-1] and capa()['uniforme'] == {}, alertas)
        importar(dict(exp, uniforme={CON_UNI['id']: 'no-existe'}))
        ir(); pg.fill('#q', CON_UNI['name']); pg.wait_for_timeout(250)
        ok('5 un uniforme que ya no está en los datos queda con aviso', 'ya no está en los datos' in fila(CON_UNI).inner_text(), fila(CON_UNI).inner_text())
        pg.click('.cutabs [data-a="cuentaTab"][data-v="capa"]'); pg.wait_for_timeout(300); importar(exp)
        ir(); pg.fill('#q', ''); pg.wait_for_timeout(200)
        pg.screenshot(path=f'{SALIDA}/roster_1400.png', full_page=False)

        # 6. celular
        ir(); pg.fill('#q', ''); pg.wait_for_timeout(200)
        pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(400)
        anchos = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
        ok('6 celular: no se sale del ancho', anchos[0] <= anchos[1], anchos)
        pg.screenshot(path=f'{SALIDA}/roster_390.png', full_page=False)
        ok('sin errores de página ni de consola', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
