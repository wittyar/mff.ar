"""La Guía (1.0.59; Ezequiel, 23 de noviembre de 2026, aprobó «Guía corta de progreso y rutina dentro de la app, enlazada
a las secciones que ya existen, en vez de un texto de un millón de caracteres»). Lo que se espera sale de data.js
(MFF_GUIA_CORTA, MFF_GUIA, MFF_MODOS, MFF_SEED_CHARACTERS, MFF_CATALOGO), no de app.js:
  1. La barra: «Guía» al final del grupo del juego; en 1400 y en 1280 la barra no desborda.
  2. Los temas: la sub-barra con los tres en orden; cada uno con sus bloques y sus puntos (el de un modo, con el nombre del
     modo), en orden.
  3. Cada afirmación con su fuente a la vista: cada parte con su marca (Dato, Criterio de quién, mffguide · sin confirmar,
     ≠ no coinciden, En la app) y una ficha por fuente, con el nombre completo de la fuente al pasar el mouse; las de
     la app, sin fuente; el orden de armado y los topes de la guía de thanosvibs, con los suyos.
  4. Cada enlace lleva adonde dice (el modo abierto y a la vista, la pestaña de Objetos o de Mi cuenta, el planificador
     en su modo, la ficha en su pestaña, la entrada del glosario abierta, la vista, el tramo del recorrido) y «Atrás»
     vuelve a la Guía, en el mismo tema y a la misma altura; desde la ficha, también su botón «← Guía».
  5. En inglés: los temas, los bloques y cada parte, con el texto en inglés.
  6. En el celular: ningún tema desborda el ancho y los enlaces se tocan.
  7. Las capturas (escritorio y celular: el índice, un tema abierto, un punto con su enlace y sus fuentes) y cuántas
     palabras tiene la Guía en español. Sin errores de página ni 404."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import SALIDA  # noqa: E401
import re
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_GUIA_CORTA', 'MFF_GUIA', 'MFF_MODOS', 'MFF_SEED_CHARACTERS', 'MFF_CATALOGO')
G, GU, MODOS = D['MFF_GUIA_CORTA'], D['MFF_GUIA'], {m['id']: m for m in D['MFF_MODOS']}
PJ = {c['id']: c['name'] for c in D['MFF_SEED_CHARACTERS']}
EF = {'ef-' + e['id']: e for e in D['MFF_CATALOGO']['efectos']}
CAPTURAS = os.environ.get('MFF_CAPTURAS', os.path.join(SALIDA, 'guia'))
os.makedirs(CAPTURAS, exist_ok=True)
MARCA = {'dato': 'DATO', 'mg': 'MFFGUIDE · SIN CONFIRMAR', 'dif': '≠ NO COINCIDEN', 'app': 'EN LA APP'}
OBJ = {'ctp': 'C.T.P.', 'iso': 'ISO-8', 'odin': 'Bendiciones de Odín', 'emblemas': 'Emblemas', 'jarvis': 'J.A.R.V.I.S.', 'cromos': 'Cromos'}
CU = {'roster': 'Tu roster', 'plan': 'Planificador', 'cromos': 'Cromos', 'equipos': 'Equipos'}
AREA = {'comparativa': 'Comparativa', 'mesa': 'Mesa'}
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
titulo = lambda it, lang='es': (MODOS[it['modo']]['nombre_es' if lang == 'es' else 'nombre'] if 'modo' in it else it[lang])


def marca(p):
    return 'CRITERIO DE THANOSVIBS' if p['k'] == 'criterio' and p['de'] == 'thanosvibs' else \
           'CRITERIO DE LA APP' if p['k'] == 'criterio' else MARCA[p['k']]


def fuentes_de(p):
    return GU['orden_build']['fuente'] if p['k'] == 'orden' else GU['topes']['fuente'] if p['k'] == 'topes' else p.get('fuente', [])


srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); errores, recursos = [], []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('response', lambda r: r.status == 404 and recursos.append(r.url))
        pg.goto(url); pg.wait_for_selector('.ccard')
        # Que termine la bajada de retratos e íconos: su aviso de arriba cambia el alto de la página (y la altura a la que vuelve «Atrás»).
        pg.wait_for_function("!document.querySelector('#avisos').innerText.includes('Bajando')", timeout=120000)

        # 1. la barra
        juego = pg.locator('nav.topnav .navgrupo:not(.cuenta) .navlink').all_inner_texts()
        ok('1 «Guía» al final del grupo del juego', juego[-1] == 'Guía' and len(juego) == 7, juego)
        for w in (1400, 1280):
            pg.set_viewport_size({'width': w, 'height': 900}); pg.wait_for_timeout(200)
            n = pg.evaluate("(() => { const n = document.querySelector('nav.topnav'); return [n.scrollWidth, n.clientWidth]; })()")
            ok(f'1 en {w} la barra no desborda', n[0] <= n[1], n)
        pg.set_viewport_size({'width': 1400, 'height': 900})
        pg.click('nav.topnav [data-a="goGuia"]'); pg.wait_for_selector('.guia')
        ok('1 «Guía» queda marcada', pg.locator('nav.topnav .navlink.on').all_inner_texts() == ['Guía'])

        # 2 y 3. temas, bloques, puntos, partes y fuentes
        tabs = pg.locator('.cucab.juego .cutab').all_inner_texts()
        ok('2 la sub-barra: los tres temas en orden', [norm(x) for x in tabs] == [t['es'] for t in G['temas']], tabs)
        palabras = 0
        for tm in G['temas']:
            pg.click(f'.cutabs [data-a="guiaTab"][data-v="{tm["id"]}"]'); pg.wait_for_timeout(250)
            palabras += len(pg.locator('main').inner_text().split())
            ok(f'2 {tm["id"]}: el título y la pestaña marcada', pg.locator('main h1').inner_text() == tm['es']
               and norm(pg.locator('.cutab.on').inner_text()) == tm['es'])
            ok(f'2 {tm["id"]}: sus bloques en orden', pg.locator('main .guiabloque > h3').all_inner_texts() == [x['es'] for x in tm['bloques']]
               or [x.upper() for x in pg.locator('main .guiabloque > h3').all_inner_texts()] == [x['es'].upper() for x in tm['bloques']])
            items = [it for bl in tm['bloques'] for it in bl['items']]
            ok(f'2 {tm["id"]}: sus puntos en orden, con su título', pg.locator('main .guiaitem .guiatit').all_inner_texts() == [titulo(it) for it in items],
               pg.locator('main .guiaitem .guiatit').all_inner_texts())
            mal = []
            for it in items:
                el = pg.locator(f'#gu-{it["id"]}')
                partes = el.locator('.guiap')
                if partes.count() != len(it['partes']):
                    mal.append(f'{it["id"]}: {partes.count()} partes'); continue
                for i, pt in enumerate(it['partes']):
                    x = partes.nth(i)
                    tag = x.locator('.tag').first.inner_text()
                    espera = 'CRITERIO DE THANOSVIBS' if pt['k'] == 'orden' else 'DATO' if pt['k'] == 'topes' else marca(pt)
                    if tag != espera:
                        mal.append(f'{it["id"]}/{i}: marca {tag!r}, se espera {espera!r}')
                    fs = fuentes_de(pt)
                    tits = x.locator('.fuente').evaluate_all('els => els.map(e => e.title)')
                    if tits != [GU['fuentes'][f]['nombre'] for f in fs]:
                        mal.append(f'{it["id"]}/{i}: fuentes {tits} en vez de {fs}')
                    if pt['k'] in ('dato', 'criterio', 'mg', 'dif') and not fs:
                        mal.append(f'{it["id"]}/{i}: una afirmación sin fuente')
                    if pt['k'] not in ('orden', 'topes') and pt['es'] not in norm(x.inner_text()):
                        mal.append(f'{it["id"]}/{i}: sin su texto')
                    if pt['k'] == 'orden' and x.locator('li').all_inner_texts() != [s['es'] for s in GU['orden_build']['pasos']]:
                        mal.append(f'{it["id"]}: el orden de armado no es el de la guía')
                    if pt['k'] == 'topes' and x.locator('li').count() != len([y for y in GU['topes']['items'] if y['tope'] is not None]) + 1:
                        mal.append(f'{it["id"]}: los topes no son los de la guía')
                ir = ([{'a': 'modo', 'id': it['modo']}] if 'modo' in it else []) + it.get('ir', [])
                if el.locator('.guiair [data-a="guiaIr"]').count() != len(ir):
                    mal.append(f'{it["id"]}: {el.locator(".guiair [data-a=guiaIr]").count()} enlaces, se esperan {len(ir)}')
            ok(f'3 {tm["id"]}: cada parte con su marca, su texto y sus fuentes (nombre completo al pasar el mouse)', not mal, mal)
            pg.screenshot(path=os.path.join(CAPTURAS, f'guia_1400_{tm["id"]}.png'), full_page=True)
        print(f'Palabras de la Guía en español (los tres temas, con títulos, marcas, fuentes y enlaces): {palabras}')

        # 4. los enlaces y «Atrás»
        def destino_ok(d):
            if d['a'] == 'modo':
                m = pg.locator(f'#modo-{d["id"]}')
                top = m.evaluate('e => e.getBoundingClientRect().top')
                nav = pg.evaluate("document.querySelector('nav.topnav').offsetHeight")
                return pg.locator('nav.topnav .navlink.on').inner_text() == 'Modos' and 'on' in m.get_attribute('class') and nav <= top < 600, (nav, top)
            if d['a'] == 'objetos':
                return norm(pg.locator('.cucab.juego .cutab.on').inner_text()).startswith(OBJ[d['tab']]), pg.locator('.cutab.on').inner_text()
            if d['a'] == 'cuenta':
                return norm(pg.locator('.cucab .cutab.on').inner_text()).startswith(CU[d['tab']]), pg.locator('.cutab.on').inner_text()
            if d['a'] == 'plan':
                return (norm(pg.locator('.cucab .cutab.on').inner_text()).startswith('Planificador')
                        and pg.locator(f'.plmodo [data-v="{d["modo"]}"]').get_attribute('class') == 'on'), d['modo']
            if d['a'] == 'ficha':
                return PJ[d['pj']] in pg.locator('.fcab-id').inner_text() and pg.locator('.ftab.on').inner_text() == 'Armado', d['pj']
            if d['a'] == 'glosario':
                pg.wait_for_timeout(700)
                e = pg.locator(f'#{d["id"]}')
                return e.evaluate('e => e.open') and EF[d['id']]['es'] in e.locator('summary').inner_text(), d['id']
            if d['a'] == 'vista':
                return pg.locator('nav.topnav .navlink.on').inner_text() == 'Tier lists', d['v']
            if d['a'] == 'recorrido':
                t = pg.locator('#rc-tarjeta')
                if d['area'] == '*':
                    return t.count() == 1 and 'Paso 1 de ' in t.inner_text() and 'LA BARRA DE ARRIBA' in t.locator('.rcarea').inner_text().upper(), t.inner_text()[:60]
                return t.count() == 1 and AREA[d['area']].upper() in t.locator('.rcarea').inner_text().upper(), t.inner_text()[:60]
        vistos = 0
        for tm in G['temas']:
            for it in [it for bl in tm['bloques'] for it in bl['items']]:
                ir = ([{'a': 'modo', 'id': it['modo']}] if 'modo' in it else []) + it.get('ir', [])
                for j, d in enumerate(ir):
                    pg.click(f'.cutabs [data-a="guiaTab"][data-v="{tm["id"]}"]'); pg.wait_for_timeout(150)
                    boton = pg.locator(f'#gu-{it["id"]} .guiair [data-a="guiaIr"]').nth(j)
                    boton.scroll_into_view_if_needed(); y = pg.evaluate('scrollY')
                    texto = boton.inner_text()
                    boton.click(); pg.wait_for_timeout(450)
                    cond, det = destino_ok(d)
                    ok(f'4 {tm["id"]}/{it["id"]}: «{texto}» lleva adonde dice', cond, det)
                    if d['a'] == 'recorrido':
                        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
                        ok(f'4 {it["id"]}: al salir del recorrido, de vuelta en la Guía', pg.locator('.guia').count() == 1
                           and norm(pg.locator('.cutab.on').inner_text()) == tm['es'])
                    else:
                        if d['a'] == 'ficha' and vistos == 0:
                            atras = pg.locator('main [data-a="atras"]')
                            ok('4 la ficha ofrece «← Guía»', atras.count() == 1 and 'Guía' in atras.inner_text(), atras.all_inner_texts())
                            vistos += 1
                        pg.go_back(); pg.wait_for_timeout(450)
                        y2 = pg.evaluate('scrollY')
                        ok(f'4 {it["id"]}: «Atrás» vuelve a la Guía, al mismo tema y a la misma altura', pg.locator('.guia').count() == 1
                           and norm(pg.locator('.cutab.on').inner_text()) == tm['es'] and abs(y2 - y) < 3, (y, y2))
        pg.screenshot(path=os.path.join(CAPTURAS, 'guia_1400_vuelta.png'))
        # un punto con su enlace y sus fuentes, con el nombre completo de una fuente al pasar el mouse
        pg.click('.cutabs [data-a="guiaTab"][data-v="rutina"]'); pg.wait_for_timeout(200)
        el = pg.locator('#gu-wb'); el.scroll_into_view_if_needed()
        el.screenshot(path=os.path.join(CAPTURAS, 'guia_1400_enlace_fuente.png'))

        # 5. inglés
        pg.click('nav.topnav [data-a="lang"]'); pg.wait_for_timeout(300)
        ok('5 en inglés: los temas', [norm(x) for x in pg.locator('.cucab.juego .cutab').all_inner_texts()] == [t['en'] for t in G['temas']])
        mal = []
        for tm in G['temas']:
            pg.click(f'.cutabs [data-a="guiaTab"][data-v="{tm["id"]}"]'); pg.wait_for_timeout(200)
            for it in [it for bl in tm['bloques'] for it in bl['items']]:
                el = pg.locator(f'#gu-{it["id"]}')
                if el.locator('.guiatit').inner_text() != titulo(it, 'en'):
                    mal.append(f'{it["id"]}: título')
                for i, pt in enumerate(it['partes']):
                    if pt['k'] not in ('orden', 'topes') and pt['en'] not in norm(el.locator('.guiap').nth(i).inner_text()):
                        mal.append(f'{it["id"]}/{i}')
        ok('5 en inglés: cada título y cada parte', not mal, mal)
        pg.screenshot(path=os.path.join(CAPTURAS, 'guia_1400_en.png'), full_page=True)
        pg.click('nav.topnav [data-a="lang"]'); pg.wait_for_timeout(300)

        # 6. celular
        c = b.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        c.on('pageerror', lambda e: errores.append(str(e)))
        c.goto(url); c.wait_for_selector('.ccard')
        c.locator('nav.topnav [data-a="goGuia"]').scroll_into_view_if_needed(); c.tap('nav.topnav [data-a="goGuia"]'); c.wait_for_selector('.guia')
        c.screenshot(path=os.path.join(CAPTURAS, 'guia_390_indice.png'))
        for tm in G['temas']:
            c.tap(f'.cutabs [data-a="guiaTab"][data-v="{tm["id"]}"]'); c.wait_for_timeout(250)
            w = c.evaluate('document.documentElement.scrollWidth')
            ok(f'6 celular, {tm["id"]}: no desborda el ancho', w <= 390, w)
            c.screenshot(path=os.path.join(CAPTURAS, f'guia_390_{tm["id"]}.png'), full_page=True)
        c.tap('.cutabs [data-a="guiaTab"][data-v="rutina"]'); c.wait_for_timeout(200)
        el = c.locator('#gu-wb'); el.scroll_into_view_if_needed(); el.screenshot(path=os.path.join(CAPTURAS, 'guia_390_enlace_fuente.png'))
        el.locator('[data-a="guiaIr"]').nth(1).tap(); c.wait_for_timeout(400)
        ok('6 celular: el enlace se toca y lleva al planificador', norm(c.locator('.cucab .cutab.on').inner_text()).startswith('Planificador'))
        c.go_back(); c.wait_for_timeout(400)
        ok('6 celular: «Atrás» vuelve a la Guía', c.locator('.guia').count() == 1)

        ok('7 sin errores de página', not errores, errores)
        ok('7 sin 404', not recursos, recursos[:5])
        b.close()
finally:
    srv.terminate()
ok.fin()
