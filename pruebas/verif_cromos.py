"""La sección Cromos (1.0.53, #35; desde la 1.0.56, la pestaña Cromos de Objetos; Ezequiel, 17 de noviembre de 2026: «Arma un modulo sobre cromos donde pongas todos los
cromos con sus caractaristicas»). Lo que se espera sale de MFF_CROMOS (data.js), no de app.js:
  1. Objetos (en el grupo del juego de la barra) la tiene como pestaña; están todos los cromos, cada uno con sus fijas y las cinco opciones de cada
     grado (3★ a 6★; los Premium, 4★ a 6★).
  2. «Da este stat»: fijo, posible en un grado (también como activación) o cualquiera, con lo que lo da resaltado y el
     resumen de cuántos; el tipo; la activación (con o cuándo); la búsqueda por nombre.
  3. Los valores (1.0.59, las tablas del juego según mffguide.fyi): las fijas según la calidad elegida (1 a 7) o fijas
     (la tercera de un Premium, la perforación de Doctor Strange), el valor de cada grado, el efecto propio con el texto del
     juego y su recarga, la colección, de dónde sale y la fuente de todo eso. Los propios (War of Kings, de la nota del 17
     de noviembre de 2026): marca «propio», sin imagen, que el #1 no acumula, y la nota también como fuente. Los que solo
     tiene mffguide: marca «mffguide», sin imagen. Lo que mffguide dice distinto de thanosvibs, con «≠». El nombre del juego
     en español (y se busca por él). Los filtros de premium y de colección.
  7. Las colecciones (la vista «Colecciones»): todas, con lo que dan y sus cromos; un cromo lleva a su tarjeta y «Ver la
     colección», a la colección.
  4. Lo dudoso de la fuente («Rare?»): Raro, con la marca; entra en el filtro de Raro.
  5. En qué mazo tuyo está: ponerlo y sacarlo, con el color de Mi cuenta; un mazo lleno no toma un sexto y lo dice.
  6. «Atrás» vuelve a Objetos › Cromos; en inglés; en el celular, sin desbordar. Sin errores de página."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
C = datos_js('MFF_CROMOS')['MFF_CROMOS']
CR = C['cromos']
grados = lambda c: [g for g in ('3', '4', '5', '6') if g in c['grados']]
opciones = lambda c: [o for g in grados(c) for o in c['grados'][g]]
def da(c, k, modo):
    fija, posible = any(f['s'] == k for f in c['fijas']), any(o['s'] == k for o in opciones(c))
    return fija if modo == 'fija' else posible if modo == 'posible' else fija or posible
ids = lambda f: sorted(c['id'] for c in CR if f(c))
VISTOS = "[...document.querySelectorAll('.crcard')].map(x => x.id.slice(6)).sort()"

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        vistos = lambda: sorted(pg.evaluate(VISTOS))

        # 1. la sección, con todos
        ok('1 la barra: «Objetos» en el grupo del juego', pg.locator('nav.topnav .navgrupo:not(.cuenta) [data-a="goObjetos"]').count() == 1)
        pg.click('[data-a="goObjetos"]'); pg.click('.cutabs [data-a="objTab"][data-v="cromos"]'); pg.wait_for_selector('.crcard')
        ok('1 están todos los cromos', vistos() == ids(lambda c: True), (len(vistos()), len(CR)))
        filas = pg.evaluate("Object.fromEntries([...document.querySelectorAll('.crcard')].map(x => [x.id.slice(6), [...x.querySelectorAll('.crfila')].map(f => f.querySelectorAll('.crop').length)]))")
        espera = {c['id']: [len(c['fijas'])] + [5] * len(grados(c)) for c in CR}
        ok('1 cada uno con sus fijas y las cinco opciones de cada grado', filas == espera,
           [k for k in espera if filas.get(k) != espera[k]][:5])
        premium = [c for c in CR if c['t'] == 'Premium']
        ok('1 los Premium: tres fijas y de 4★ a 6★', premium and all(len(c['fijas']) == 3 and grados(c) == ['4', '5', '6'] for c in premium))
        n_act = pg.locator('.crop.act').count()
        ok('1 las activaciones, marcadas', n_act == sum(1 for c in CR for o in opciones(c) if o.get('act')), n_act)

        # 2. filtros
        for modo in ('cualquiera', 'fija', 'posible'):
            pg.select_option('select[data-a="crStat"]', 'eatk'); pg.wait_for_timeout(200)
            pg.click(f'[data-a="crModo"][data-v="{modo}"]'); pg.wait_for_timeout(250)
            ok(f'2 «Da este stat» ataque de energía, {modo}', vistos() == ids(lambda c: da(c, 'eatk', modo)), len(vistos()))
        res = pg.locator('.crresumen').first.inner_text()
        ok('2 el resumen: cuántos lo dan fijo y cuántos en un grado', f"{len(ids(lambda c: da(c, 'eatk', 'fija')))} lo dan fijo" in res
           and f"{len(ids(lambda c: da(c, 'eatk', 'posible')))} lo pueden dar" in res, res)
        hits = pg.evaluate("[...document.querySelectorAll('.crop.hit')].length")
        ok('2 lo que lo da (fijo o en un grado), resaltado', hits == sum(1 for c in CR if da(c, 'eatk', 'posible')
                                                                  for o in c['fijas'] + opciones(c) if o['s'] == 'eatk'), hits)
        pg.select_option('select[data-a="crStat"]', ''); pg.wait_for_timeout(200)
        pg.click('[data-a="crTipo"][data-v="Premium"]'); pg.wait_for_timeout(200)
        ok('2 tipo Premium', vistos() == ids(lambda c: c['t'] == 'Premium'), len(vistos()))
        pg.click('[data-a="crTipo"][data-v="sin"]'); pg.wait_for_timeout(200)
        ok('2 sin tipo publicado: los de la nota que no lo dicen y los de mffguide', vistos() == ids(lambda c: c['t'] is None) and len(vistos()) == 11, vistos())
        pg.click('[data-a="crTipo"][data-v=""]'); pg.wait_for_timeout(200)
        for act in ('con', 'golpe', 'critico'):
            pg.click(f'[data-a="crAct"][data-v="{act}"]'); pg.wait_for_timeout(200)
            ok(f'2 activación {act}', vistos() == ids(lambda c: any(o.get('act') and (act == 'con' or o['act'] == act) for o in opciones(c))), len(vistos()))
        pg.click('[data-a="crAct"][data-v=""]'); pg.wait_for_timeout(200)
        pg.fill('#q', 'war of kings'); pg.wait_for_timeout(300)
        ok('2 la búsqueda por nombre: los cinco de War of Kings', vistos() == ids(lambda c: 'WAR OF KINGS' in c['n']) and len(vistos()) == 5, vistos())
        pg.fill('#q', 'guerra de reyes'); pg.wait_for_timeout(300)
        ok('2 y por su nombre del juego en español', vistos() == ids(lambda c: 'WAR OF KINGS' in c['n']), vistos())
        pg.fill('#q', ''); pg.wait_for_timeout(300)
        for v, f in (('si', lambda c: c['p']), ('no', lambda c: not c['p'])):
            pg.click(f'[data-a="crPrem"][data-v="{v}"]'); pg.wait_for_timeout(200)
            ok(f'2 premium {v}', vistos() == ids(f), len(vistos()))
        ok('2 los premium son 23 (mffguide)', len(ids(lambda c: c['p'])) == 23)
        pg.click('[data-a="crPrem"][data-v=""]'); pg.wait_for_timeout(200)
        col0 = C['colecciones'][0]
        pg.select_option('select[data-a="crCol"]', col0['id']); pg.wait_for_timeout(250)
        ok('2 colección', vistos() == sorted(col0['cromos']) == ids(lambda c: c.get('col') == col0['id']), vistos())
        pg.select_option('select[data-a="crCol"]', 'sin'); pg.wait_for_timeout(250)
        ok('2 sin colección', vistos() == ids(lambda c: not c.get('col')) and len(vistos()) == 6, len(vistos()))
        pg.select_option('select[data-a="crCol"]', ''); pg.wait_for_timeout(250)
        pg.fill('#q', 'war of kings'); pg.wait_for_timeout(300)

        # 3. los valores (mffguide) y los propios
        V = C['valores']
        assert V['calidad'] == [7.5, 8, 8.5, 9, 9.5, 10, 11] and V['casilla'] == {'3': 5.1, '4': 5.4, '5': 5.7, '6': 6}
        ok('3 todos con valores de mffguide', all(c['vf'] and 'mffguide' in c['vf'] for c in CR), [c['n'] for c in CR if not c['vf']][:3])
        wk1 = next(c for c in CR if c['n'] == 'WAR OF KINGS (2009) #1')
        card = pg.locator(f'#cromo-{wk1["id"]}'); tx = card.inner_text()
        ok('3 War of Kings #1: propio, Premium, sin imagen, su nombre del juego en español', card.locator('.propio').count() == 1
           and 'PREMIUM' in tx.upper() and card.locator('.crimg img').count() == 0 and 'GUERRA DE REYES (2009) N.º 1' in tx, tx[:120])
        fijas = lambda: [x.strip() for x in card.locator('.crfila').first.locator('.crop b').all_inner_texts()]
        ok('3 calidad 7: fijas 11%, 11% y la tercera 5,1%', fijas() == ['11%', '11%', '5,1%'], fijas())
        pg.click('[data-a="crCal"][data-v="2"]'); pg.wait_for_timeout(250)
        ok('3 calidad 2: 8%, 8% y la tercera sigue en 5,1%', fijas() == ['8%', '8%', '5,1%'], fijas())
        pg.click('[data-a="crCal"][data-v="7"]'); pg.wait_for_timeout(250)
        tx = card.inner_text()
        ok('3 el valor de cada grado: 4★ 5,4%, 5★ 5,7%, 6★ 6%',
           [x.strip() for x in card.locator('.crg b').all_inner_texts()] == ['5,4%', '5,7%', '6%'], card.locator('.crg b').all_inner_texts())
        ok('3 el efecto propio, con el texto del juego y su recarga', '30% de aumento en el ataque de energía. (15 s) cuando atacas con una probabilidad de 5 %' in tx
           and 'vuelve a activarse a los 45 s' in tx, tx)
        ok('3 que no acumula su activación y la colección', 'no se acumula' in tx and 'Colección GUERRA DE REYES (5 cromos)' in tx and '+3%' in tx, tx[-400:])
        fu = card.locator('.crfuente .fuente').all_inner_texts()
        ok('3 la fuente de sus valores: mffguide y la nota', fu == ['mffguide.fyi', 'nota del foro, 17/11/2026', 'nota del café, 18/11/2026'], fu)
        card.locator('details.crobt > summary').click(); pg.wait_for_timeout(150)
        ok('3 de dónde sale', 'cofre de cromos de la tienda' in card.locator('details.crobt').inner_text())
        ds = next(c for c in CR if any(f.get('v') == 1.5 for f in c['fijas']))
        pg.fill('#q', ds['n']); pg.wait_for_timeout(300)
        pg.click('[data-a="crCal"][data-v="1"]'); pg.wait_for_timeout(250)
        ok('3 la perforación de Doctor Strange no cambia con la calidad', '1,5%' in pg.locator(f'#cromo-{ds["id"]} .crfila').first.inner_text()
           and '7,5%' in pg.locator(f'#cromo-{ds["id"]} .crfila').first.inner_text(), ds['n'])
        pg.click('[data-a="crCal"][data-v="7"]'); pg.wait_for_timeout(250)
        mg = [c for c in CR if c.get('mg')]
        ok('3 los siete que solo tiene mffguide, entre ellos FANTASTIC FOUR (1961) #49', len(mg) == 7 and any(c['n'] == 'FANTASTIC FOUR (1961) #49' for c in mg))
        pg.fill('#q', 'FANTASTIC FOUR (1961) #49'); pg.wait_for_timeout(300)
        ff = next(c for c in mg if c['n'] == 'FANTASTIC FOUR (1961) #49'); fc = pg.locator(f'#cromo-{ff["id"]}')
        ok('3 un cromo de mffguide: su marca, sin imagen, Premium y sus valores', fc.locator('.propio', has_text='mffguide').count() == 1
           and fc.locator('.crimg img').count() == 0 and 'PREMIUM' in fc.inner_text().upper() and '11%' in fc.inner_text(), fc.inner_text()[:200])
        dif = [c for c in CR if c['dif']]
        pg.fill('#q', ''); pg.wait_for_timeout(300)
        ok('3 lo que mffguide dice distinto, con «≠»', len(dif) == 4 and pg.locator('.crdif').count() == sum(len(c['dif']) for c in dif)
           and all(pg.locator(f'#cromo-{c["id"]} .crdif').count() == len(c['dif']) for c in dif), [c['n'] for c in dif])
        armor = next(c for c in dif if c['n'] == 'ARMOR WARS #1')
        ok('3 la activación que difiere, sin el texto de mffguide', 'act' not in armor and 'VELOCIDAD MOVIMIENTO' in pg.locator(f'#cromo-{armor["id"]} .crdif').inner_text())

        # 4. lo dudoso
        dud = [c['id'] for c in CR if c['td']]
        ok('4 los «Rare?» de la fuente, con su marca', dud and pg.locator('.crcab .dudatag').count() == len(dud)
           and all(pg.locator(f'#cromo-{i} .crcab .dudatag').count() == 1 for i in dud), len(dud))
        pg.click('[data-a="crTipo"][data-v="Rare"]'); pg.wait_for_timeout(200)
        ok('4 entran en Raro', set(dud) <= set(vistos()) and vistos() == ids(lambda c: c['t'] == 'Rare'), len(vistos()))
        pg.click('[data-a="crTipo"][data-v=""]'); pg.wait_for_timeout(200)

        # 5. los mazos
        primeros = pg.evaluate(VISTOS.replace('.sort()', '.slice(0, 6)'))
        pg.click(f'#cromo-{primeros[0]} [data-a="crMazo"][data-m="1"]'); pg.wait_for_timeout(200)
        b2 = pg.locator(f'#cromo-{primeros[0]} [data-a="crMazo"][data-m="1"]')
        color = b2.evaluate("e => getComputedStyle(e).color"); cuenta = pg.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--cuenta')")
        ok('5 ponerlo en el mazo 2: marcado, con el color de Mi cuenta', b2.get_attribute('aria-pressed') == 'true' and color == 'rgb(95, 212, 196)'
           and cuenta.strip() == '#5fd4c4', (color, cuenta))
        pg.click(f'#cromo-{primeros[0]} [data-a="crMazo"][data-m="1"]'); pg.wait_for_timeout(200)
        ok('5 sacarlo', pg.locator(f'#cromo-{primeros[0]} [data-a="crMazo"][data-m="1"]').get_attribute('aria-pressed') == 'false')
        for i in primeros[:5]:
            pg.click(f'#cromo-{i} [data-a="crMazo"][data-m="0"]'); pg.wait_for_timeout(120)
        pg.click(f'#cromo-{primeros[5]} [data-a="crMazo"][data-m="0"]'); pg.wait_for_timeout(200)
        ok('5 un mazo lleno no toma un sexto y lo dice', pg.locator(f'#cromo-{primeros[5]} [data-a="crMazo"][data-m="0"]').get_attribute('aria-pressed') == 'false'
           and 'ya tiene 5 cromos' in pg.locator('main').inner_text(), pg.locator('.aviso').all_inner_texts())
        ok('5 los cinco, en el mazo 1', all(pg.locator(f'#cromo-{i} [data-a="crMazo"][data-m="0"]').get_attribute('aria-pressed') == 'true' for i in primeros[:5]))
        pg.screenshot(path=f'{SALIDA}/cromos_1400.png')

        # 7. las colecciones
        pg.click('[data-a="crVista"][data-v="col"]'); pg.wait_for_timeout(300)
        items = pg.locator('details.objitem')
        ok('7 las 35 colecciones', items.count() == len(C['colecciones']) == 35, items.count())
        wk = next(x for x in C['colecciones'] if x['n']['en'] == 'WAR OF KINGS')
        it = pg.locator(f'#{wk["id"]}'); it.locator('summary').click(); pg.wait_for_timeout(200)
        ok('7 lo que da y sus cromos', 'ÍNDICE DE RECUPERACIÓN' in it.inner_text() and '+3%' in it.inner_text()
           and it.locator('.crmini').count() == 5, it.inner_text()[:200])
        it.locator('.crmini').first.click(); pg.wait_for_timeout(400)
        ok('7 un cromo lleva a su tarjeta', pg.locator(f'#cromo-{wk["cromos"][0]}.resaltada').count() == 1)
        pg.click(f'#cromo-{wk["cromos"][0]} [data-a="crVerCol"]'); pg.wait_for_timeout(400)
        ok('7 «Ver la colección» la abre', pg.locator(f'#{wk["id"]}[open]').count() == 1)
        pg.click('[data-a="crVista"][data-v="cromos"]'); pg.wait_for_timeout(300)

        # 6. Atrás, inglés, celular
        pg.click('[data-a="goGlosario"]'); pg.wait_for_timeout(300); pg.go_back(); pg.wait_for_timeout(400)
        ok('6 «Atrás» desde el Glosario vuelve a Objetos › Cromos', pg.locator('.crcard').count() > 0
           and pg.locator('nav.topnav .navlink.on').inner_text() == 'Objetos' and pg.locator('.cutab.on').inner_text().startswith('Cromos'))
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('6 en inglés', pg.locator('main h1').inner_text().startswith('Comic cards')
           and 'Deck 1' in pg.locator('.crcard').first.inner_text(), pg.locator('main h1').inner_text())
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(400)
        anchos = pg.evaluate("""[document.querySelector('main').scrollWidth, document.querySelector('main').clientWidth,
          Math.max(...[...document.querySelectorAll('.crcard')].map(x => x.getBoundingClientRect().right))]""")
        ok('6 celular: la sección no se sale del ancho', anchos[0] <= anchos[1] and anchos[2] <= 390, anchos)
        pg.screenshot(path=f'{SALIDA}/cromos_390.png')
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
