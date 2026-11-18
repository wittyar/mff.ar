"""Mi cuenta › Cromos (1.0.53, #35; Ezequiel, 17 de noviembre de 2026: «en lo que respecta la cuenta personal poder anotar
los cromos que tengo en sus dos sets»). Los dos mazos del juego, de 5 lugares; un cromo va una vez por mazo. Lo que se
espera sale de MFF_CROMOS (data.js) y de la capa guardada (/api/capa), no de app.js:
  1. Vacío: los dos mazos sin cromos, para poner uno; la sub-barra y el resumen de Mi cuenta lo cuentan.
  2. Poner cromos en los dos mazos (desde acá y desde la sección Cromos; el mismo cromo en los dos), anotar la opción de
     algunos grados (también una activación) y sacar uno.
  3. Qué cubre cada mazo: por stat, cuántos cromos lo dan fijo y cuántos en una opción anotada; las activaciones anotadas.
  4. Se guarda en la capa (mazos con {id, op}) y vuelve al recargar.
  5. Exportar «Mi capa» los trae; importar una capa los reemplaza; una capa de antes (sin cromos) entra con los mazos
     vacíos; una con un cromo repetido en un mazo no entra y lo dice; un cromo que ya no está en los datos queda con aviso.
  6. En el celular, sin desbordar. Sin errores de página."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, SALIDA  # noqa: E401
import json, tempfile
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
C = datos_js('MFF_CROMOS')['MFF_CROMOS']
POR = {c['id']: c for c in C['cromos']}
WK3 = next(c for c in C['cromos'] if c['n'] == 'WAR OF KINGS (2009) #3')
OTRO = next(c for c in C['cromos'] if c['t'] == 'Premium' and not c.get('pr'))
TERCERO = next(c for c in C['cromos'] if c['t'] == 'Support')
clave = lambda o: o['s'] + '@' + o['act'] if o.get('act') else o['s']
ACT4 = next(o for o in WK3['grados']['4'] if o.get('act'))
OP3 = WK3['grados']['3'][0]
OP6 = OTRO['grados']['6'][2]


def cobertura(mazo):
    """{stat: [fijos, anotados]} y las activaciones anotadas, de un mazo de la capa."""
    por, acts = {}, []
    for x in mazo:
        c = POR.get(x['id'])
        if not c:
            continue
        for f in c['fijas']:
            por.setdefault(f['s'], [0, 0])[0] += 1
        for g, k in x['op'].items():
            o = next((y for y in c['grados'].get(g, []) if clave(y) == k), None)
            if o and o.get('act'):
                acts.append(o)
            elif o:
                por.setdefault(o['s'], [0, 0])[1] += 1
    return por, acts


srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1400, 'height': 900}, accept_downloads=True)
        pg = ctx.new_page(); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        alertas = []
        pg.on('dialog', lambda d: (alertas.append(d.message), d.accept()))
        pg.goto(url); pg.wait_for_selector('.ccard')
        capa = lambda: (pg.wait_for_timeout(300), pg.evaluate("fetch('/api/capa', { headers: { 'X-MFF': '1' } }).then(r => r.json())")['capa'])[1]
        def ir():
            pg.click('nav.topnav [data-a="goCuenta"]'); pg.wait_for_selector('.cuhub')
            pg.click('.cutabs [data-a="cuentaTab"][data-v="cromos"]'); pg.wait_for_timeout(300)

        # 1. vacío
        ir()
        ok('1 los dos mazos, vacíos, para poner un cromo', pg.locator('select[data-a="crPoner"]').count() == 2
           and pg.locator('select[data-a="crOp"]').count() == 0 and pg.locator('h3', has_text='Mazo 1').count() == 1
           and pg.locator('h3', has_text='Mazo 2').count() == 1)

        # 2. poner, anotar, sacar
        pg.select_option('select[data-a="crPoner"][data-m="0"]', WK3['id']); pg.wait_for_timeout(300)
        pg.select_option('select[data-a="crPoner"][data-m="0"]', OTRO['id']); pg.wait_for_timeout(300)
        pg.select_option('select[data-a="crPoner"][data-m="0"]', TERCERO['id']); pg.wait_for_timeout(300)
        ok('2 el mismo cromo no se ofrece dos veces en un mazo', pg.locator(f'select[data-a="crPoner"][data-m="0"] option[value="{WK3["id"]}"]').count() == 0)
        pg.click('[data-a="goObjetos"]'); pg.click('.cutabs [data-a="objTab"][data-v="cromos"]'); pg.wait_for_selector('.crcard')
        pg.click(f'#cromo-{WK3["id"]} [data-a="crMazo"][data-m="1"]'); pg.wait_for_timeout(250)
        ok('2 desde Cromos, el mismo cromo también en el mazo 2', [pg.locator(f'#cromo-{WK3["id"]} [data-a="crMazo"][data-m="{m}"]').get_attribute('aria-pressed') for m in (0, 1)] == ['true', 'true'])
        ir()
        sel = lambda m, l, g: f'select[data-a="crOp"][data-m="{m}"][data-l="{l}"][data-g="{g}"]'
        pg.select_option(sel(0, 0, '3'), clave(OP3)); pg.wait_for_timeout(200)
        pg.select_option(sel(0, 0, '4'), clave(ACT4)); pg.wait_for_timeout(200)
        pg.select_option(sel(0, 1, '6'), clave(OP6)); pg.wait_for_timeout(200)
        ok('2 los Premium no tienen 3★', pg.locator(sel(0, 1, '3')).count() == 0 and pg.locator(sel(0, 1, '4')).count() == 1)
        ok('2 lo anotado queda elegido', [pg.locator(sel(0, 0, '3')).input_value(), pg.locator(sel(0, 0, '4')).input_value(),
                                          pg.locator(sel(0, 1, '6')).input_value(), pg.locator(sel(0, 0, '5')).input_value()]
           == [clave(OP3), clave(ACT4), clave(OP6), ''])
        pg.click('[data-a="crQuitar"][data-m="0"][data-l="2"]'); pg.wait_for_timeout(300)
        ok('2 sacar uno', [x['id'] for x in capa()['cromos']['mazos'][0]] == [WK3['id'], OTRO['id']])

        # 3. qué cubre
        esperado, acts = cobertura(capa()['cromos']['mazos'][0])
        filas = pg.evaluate("""[...document.querySelectorAll('.crcobertura')][0].querySelectorAll('tbody tr').length""")
        tabla = pg.evaluate("""Object.fromEntries([...[...document.querySelectorAll('.crcobertura')][0].querySelectorAll('tbody tr')]
          .map(tr => [tr.cells[0].textContent, [tr.cells[1].textContent.trim(), tr.cells[2].textContent.trim()]]))""")
        nombres = {k: v['es'] for k, v in C['stats'].items()}
        espera_tabla = {nombres[k]: [str(f) if f else '—', str(a) if a else '—'] for k, (f, a) in esperado.items()}
        ok('3 el mazo 1: por stat, cuántos lo dan fijo y cuántos anotado', tabla == espera_tabla and filas == len(esperado), (tabla, espera_tabla))
        li = pg.locator('.crcobertura').first.locator('li').all_inner_texts()
        ok('3 la activación anotada, con su cromo y su grado', len(li) == len(acts) == 1 and nombres[ACT4['s']] in li[0]
           and WK3['n'] in li[0] and '4★' in li[0], li)
        ok('3 sin sumar porcentajes', '%' not in pg.locator('.crcobertura').first.inner_text())
        pg.click('nav.topnav [data-a="goCuenta"]'); pg.wait_for_selector('.cuhub')
        tile = pg.locator('.cuhub .cutile', has_text='Cromos en tus mazos')
        ok('1 el resumen de Mi cuenta cuenta los cromos y los mazos', tile.locator('.v').inner_text() == '3'
           and 'Mazo 1: 2 de 5' in tile.inner_text() and 'mazo 2: 1 de 5' in tile.inner_text(), tile.inner_text())
        sub = pg.locator('.cutabs [data-v="cromos"] .cun').inner_text()
        ok('1 la sub-barra también', sub == '3', sub)

        # 4. la capa y al recargar
        c = capa()['cromos']
        ok('4 en la capa: los dos mazos con {id, op}', c == {'mazos': [[{'id': WK3['id'], 'op': {'3': clave(OP3), '4': clave(ACT4)}},
                                                                         {'id': OTRO['id'], 'op': {'6': clave(OP6)}}],
                                                                        [{'id': WK3['id'], 'op': {}}]]}, c)
        pg.reload(); pg.wait_for_selector('.ccard'); ir()
        ok('4 al recargar, siguen', pg.locator(sel(0, 0, '4')).input_value() == clave(ACT4) and pg.locator('select[data-a="crOp"][data-m="1"]').count() == 4)

        # 5. exportar e importar
        pg.click('.cutabs [data-a="cuentaTab"][data-v="capa"]'); pg.wait_for_timeout(300)
        ok('5 Mi capa cuenta los cromos', '3' in pg.locator('.stat', has_text='Cromos en los mazos').inner_text())
        with pg.expect_download() as dl:
            pg.click('[data-a="exportUser"]')
        exp = json.load(open(dl.value.path(), encoding='utf-8'))
        ok('5 exportar trae los mazos', exp.get('cromos') == c, exp.get('cromos'))
        d = tempfile.mkdtemp(prefix='mffcr-')
        def importar(x):
            f = os.path.join(d, 'capa.json'); json.dump(x, open(f, 'w', encoding='utf-8'))
            pg.set_input_files('input[data-a="importUser"]', f); pg.wait_for_timeout(600)
        otra = dict(exp); otra['cromos'] = {'mazos': [[{'id': TERCERO['id'], 'op': {}}], []]}
        importar(otra)
        ok('5 importar una capa reemplaza los mazos', capa()['cromos'] == otra['cromos'], capa()['cromos'])
        vieja = {k: v for k, v in exp.items() if k != 'cromos'}
        importar(vieja)
        ok('5 una capa de antes, sin cromos, entra con los mazos vacíos', capa()['cromos'] == {'mazos': [[], []]} and not alertas, (capa()['cromos'], alertas))
        rota = dict(exp); rota['cromos'] = {'mazos': [[{'id': WK3['id'], 'op': {}}, {'id': WK3['id'], 'op': {}}], []]}
        importar(rota)
        ok('5 una con un cromo dos veces en un mazo no entra y lo dice', alertas and 'dos veces' in alertas[-1] and capa()['cromos'] == {'mazos': [[], []]}, alertas)
        perdido = dict(exp); perdido['cromos'] = {'mazos': [[{'id': 'no-existe', 'op': {}}, {'id': WK3['id'], 'op': {'5': 'no-esta'}}], []]}
        importar(perdido)
        pg.click('.cutabs [data-a="cuentaTab"][data-v="cromos"]'); pg.wait_for_timeout(300)
        avisos = pg.locator('main .aviso').all_inner_texts()
        ok('5 un cromo y una opción que ya no están en los datos, con aviso', any('no-existe' in a for a in avisos) and any('5★' in a for a in avisos), avisos)
        pg.click('[data-a="crQuitar"][data-m="0"][data-l="0"]'); pg.wait_for_timeout(300)
        ok('5 y el que no está se puede sacar', [x['id'] for x in capa()['cromos']['mazos'][0]] == [WK3['id']])
        pg.screenshot(path=f'{SALIDA}/cuenta_cromos_1400.png', full_page=True)

        # 6. celular
        pg.click('.cutabs [data-a="cuentaTab"][data-v="capa"]'); pg.wait_for_timeout(300)
        importar(exp); pg.click('.cutabs [data-a="cuentaTab"][data-v="cromos"]'); pg.wait_for_timeout(300)
        pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(400)
        anchos = pg.evaluate("[document.querySelector('main').scrollWidth, document.querySelector('main').clientWidth]")
        ok('6 celular: los mazos no se salen del ancho', anchos[0] <= anchos[1], anchos)
        pg.screenshot(path=f'{SALIDA}/cuenta_cromos_390.png', full_page=True)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
