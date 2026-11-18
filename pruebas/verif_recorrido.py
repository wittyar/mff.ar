"""El recorrido guiado (1.0.54, Ezequiel, 17 de noviembre de 2026: «la primera vez que lo abris y, si presionas el boton,
te aparece un tutorial de cada area de la aplicacion explicando que cosas ver y como verlas»).
  1. Primer uso (sin capa.json): la bienvenida; Tab no sale de ella. «Ahora no», Esc, tocar afuera y «Empezar el
     recorrido» la cierran, guardan la capa y no vuelve a salir, tampoco al recargar.
  2. Con una capa ya guardada (quien la usaba antes de la 1.0.54) no sale.
  3. El botón «Recorrido» arranca el tramo del área en la que se está, en cada área, con lo que se tiene abierto (en la
     ficha, el mismo personaje); su primer paso resalta su elemento.
  4. El recorrido completo (desde «Otras áreas») pasa por las 11 áreas con sus pasos, en orden, y termina; cada paso
     resalta su elemento, dentro de la ventana, y la tarjeta no lo tapa (en el celular, la hoja de abajo deja ver su
     comienzo). Escritorio (con la mesa abierta, una búsqueda y lo elegido para comparar) y celular.
  5. Al salir, la app vuelve adonde estaba: la misma sección y altura, la búsqueda, la bandeja de comparar con lo mismo y la
     capa (con la mesa) sin cambios; el historial no guarda los lugares del recorrido.
  6. Siguiente, Anterior (apagado en el primer paso), ← y →, Esc (el foco vuelve al botón) y tocar afuera.
  7. Un paso cuyo elemento no está en la pantalla (el roster sin resultados) lo dice, sin resaltar nada, y se sigue.
  8. «Atrás» del navegador con el recorrido abierto lo cierra y vuelve al lugar anterior.
  9. Convivencia: el tooltip de la ayuda no se abre debajo del recorrido; con el «Cómo funciona» abierto, tocar afuera lo
     cierra sin arrancar nada.
 10. En inglés, todos los pasos con su texto, distinto del español. Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json
from harness import origen_local, carpeta_datos, levantar, Chequeo, abrir_mesa
from playwright.sync_api import sync_playwright

ok = Chequeo()
# El modelo, escrito aparte de app.js: las áreas en el orden del recorrido completo, cuántos pasos tiene cada una y su
# nombre en la tarjeta.
AREAS = [('barra', 6, 'La barra de arriba'), ('roster', 5, 'Roster'), ('ficha', 9, 'Ficha de un personaje'),
         ('comparativa', 3, 'Comparativa'), ('tierlist', 3, 'Tier lists'), ('modos', 3, 'Modos'), ('objetos', 9, 'Objetos'),
         ('glosario', 3, 'Glosario'), ('historico', 3, 'Histórico'), ('cuenta', 8, 'Mi cuenta'), ('mesa', 3, 'Mesa')]
NOMBRE = {k: n for k, _, n in AREAS}
TOTAL = sum(n for _, n, _ in AREAS)
TARJETA = """() => { const t = document.getElementById('rc-tarjeta'), l = document.getElementById('rc-luz');
  if (!t) return null;
  const r = (x) => { const b = x.getBoundingClientRect(); return { top: b.top, left: b.left, bottom: b.bottom, right: b.right, h: b.height }; };
  const sig = t.querySelector('[data-a="recSig"]'), ant = t.querySelector('[data-a="recAnt"]');
  return { area: (t.querySelector('.rcarea') || {}).textContent, n: (t.querySelector('.rcn') || {}).textContent || '',
           tit: t.querySelector('.rctit').textContent.trim(), x: t.querySelector('p').textContent.trim(),
           falta: !!t.querySelector('.rcfalta'), card: r(t), luz: l ? r(l) : null, H: innerHeight, W: innerWidth,
           sig: sig ? sig.textContent.trim() : null, antOff: ant ? ant.disabled : null,
           centro: t.classList.contains('centro'), foco: !!document.activeElement.closest('#rc-tarjeta') }; }"""


def abierto(pg):
    return pg.locator('#rc-capa').count() > 0


def capa_txt(d):
    return open(os.path.join(d, 'capa.json'), encoding='utf-8').read()


def recorrer(pg, celular, etiqueta):
    """Recorre lo abierto hasta el final con «Siguiente» y devuelve los pasos vistos (con sus medidas)."""
    vistos = []
    for _ in range(TOTAL + 5):
        pg.wait_for_timeout(250)
        m = pg.evaluate(TARJETA)
        vistos.append(m)
        if m['sig'] in ('Terminar', 'Finish'):
            break
        pg.click('#rc-tarjeta [data-a="recSig"]')
    malos = []
    for i, m in enumerate(vistos):
        l, c = m['luz'], m['card']
        if m['falta'] or not l:
            malos.append((i + 1, m['tit'], 'sin elemento')); continue
        if l['top'] < -6 or l['bottom'] > m['H'] + 6:
            # en el celular, un elemento más alto que el lugar sobre la hoja queda con su comienzo a la vista
            if not (celular and l['top'] >= 0 and l['top'] + 60 <= c['top']):
                malos.append((i + 1, m['tit'], 'fuera de la ventana', l))
        visible = min(l['right'], m['W']) - max(l['left'], 0)
        if visible < min(40, l['right'] - l['left']):
            malos.append((i + 1, m['tit'], 'fuera a lo ancho', l))
        if c['top'] < -1 or c['bottom'] > m['H'] + 1 or c['left'] < -1 or c['right'] > m['W'] + 1:
            malos.append((i + 1, m['tit'], 'tarjeta fuera', c))
        if celular:
            if l['top'] + min(60, l['h']) > c['top']:
                malos.append((i + 1, m['tit'], 'la hoja tapa el comienzo', l, c))
        elif not (c['bottom'] <= l['top'] or c['top'] >= l['bottom'] or c['right'] <= l['left'] or c['left'] >= l['right']):
            malos.append((i + 1, m['tit'], 'la tarjeta tapa el elemento', l, c))
    ok(f'4 {etiqueta}: cada paso resalta su elemento a la vista y la tarjeta no lo tapa', not malos, malos[:4])
    return vistos


def areas_de(vistos):
    out = []
    for m in vistos:
        if not out or out[-1][0] != m['area']:
            out.append([m['area'], 0])
        out[-1][1] += 1
    return [tuple(x) for x in out]


errores, recursos, fallidas = [], [], []
def vigilar(pg):
    pg.on('pageerror', lambda e: errores.append(str(e)))
    # «Failed to load resource» no dice cuál: se cuentan aparte y cada uno tiene que ser una respuesta fallida anotada.
    pg.on('console', lambda m: m.type == 'error' and (recursos if m.text.startswith('Failed to load resource') else errores).append(m.text))
    pg.on('response', lambda r: r.status >= 400 and fallidas.append((r.status, r.request.method, r.url.split('/', 3)[3])))

with sync_playwright() as p:
    b = p.chromium.launch()

    # 1. Primer uso
    D1 = carpeta_datos(primer_uso=True)
    srv, url = levantar(D1, origen_local())
    try:
        pg = b.new_page(viewport={'width': 1400, 'height': 900}); vigilar(pg)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(300)
        m = pg.evaluate(TARJETA)
        ok('1 primer uso: la bienvenida, centrada y con el foco', m and m['tit'] == 'Esto es MFF.ar' and m['centro'] and m['foco']
           and pg.locator('#rc-tarjeta [data-a="recEmpezar"]').count() == 1 and not os.path.exists(os.path.join(D1, 'capa.json')), m)
        for _ in range(6):
            pg.keyboard.press('Tab')
        ok('1 Tab no sale de la bienvenida', pg.evaluate("!!document.activeElement.closest('#rc-tarjeta')"))
        pg.keyboard.press('Shift+Tab'); pg.keyboard.press('Shift+Tab'); pg.keyboard.press('Shift+Tab')
        ok('1 Shift+Tab tampoco', pg.evaluate("!!document.activeElement.closest('#rc-tarjeta')"))
        pg.click('#rc-tarjeta [data-a="recOmitir"]'); pg.wait_for_timeout(500)
        ok('1 «Ahora no» la cierra y guarda la capa', not abierto(pg) and os.path.exists(os.path.join(D1, 'capa.json')))
        pg.reload(); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(500)
        ok('1 tras «Ahora no» y recargar, no vuelve', not abierto(pg))

        os.remove(os.path.join(D1, 'capa.json'))
        pg.reload(); pg.wait_for_selector('#rc-tarjeta')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
        ok('1 Esc es «Ahora no»: la cierra y guarda la capa', not abierto(pg) and os.path.exists(os.path.join(D1, 'capa.json')))
        pg.reload(); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(500)
        ok('1 tras Esc y recargar, no vuelve', not abierto(pg))

        os.remove(os.path.join(D1, 'capa.json'))
        pg.reload(); pg.wait_for_selector('#rc-tarjeta')
        pg.mouse.click(20, 880); pg.wait_for_timeout(500)
        ok('1 tocar afuera es «Ahora no»: la cierra y guarda la capa', not abierto(pg) and os.path.exists(os.path.join(D1, 'capa.json')))

        os.remove(os.path.join(D1, 'capa.json'))
        pg.reload(); pg.wait_for_selector('#rc-tarjeta')
        pg.click('#rc-tarjeta [data-a="recEmpezar"]'); pg.wait_for_timeout(500)
        m = pg.evaluate(TARJETA)
        ok('1 «Empezar el recorrido» arranca el completo en su primer paso y guarda la capa',
           m and m['area'] == NOMBRE['barra'] and m['n'] == f'Paso 1 de {TOTAL}' and m['luz'] and os.path.exists(os.path.join(D1, 'capa.json')), m)
        pg.click('#rc-tarjeta [data-a="recSalir"]'); pg.wait_for_timeout(300)
        pg.reload(); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(500)
        ok('1 tras empezarlo y recargar, no vuelve', not abierto(pg))
        pg.screenshot(path=f'{SALIDA}/recorrido_tras_bienvenida.png')
        pg.close()
    finally:
        srv.terminate(); srv.wait()

    # 2 a 10, con una capa ya guardada
    D = carpeta_datos()
    srv, url = levantar(D, origen_local())
    try:
        pg = b.new_page(viewport={'width': 1400, 'height': 900}); vigilar(pg)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(500)
        ok('2 con una capa guardada no sale la bienvenida', not abierto(pg))

        # 3. El botón, en cada área
        def boton(area, n_esperado=None):
            pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(400)
            m = pg.evaluate(TARJETA)
            n = dict((k, c) for k, c, _ in AREAS)[area]
            ok(f'3 «Recorrido» en {area}: arranca su tramo', m and m['area'] == NOMBRE[area] and m['n'] == f'Paso 1 de {n}'
               and m['luz'] and not m['falta'] and m['foco'], m)
            return m
        boton('roster'); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        pg.locator('.ccard').nth(2).click(); pg.wait_for_selector('.fcab')
        quien = pg.locator('.fcab h1').inner_text()
        boton('ficha')
        ok('3 en la ficha, el tramo muestra el personaje que estaba abierto', pg.locator('.fcab h1').inner_text() == quien, (quien, pg.locator('.fcab h1').inner_text()))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        pg.click('main [data-a="back"]'); pg.wait_for_selector('.ccard')
        pg.click('.toolbar [data-a="pickMode"]')
        pg.locator('.ccard').nth(0).click(); pg.locator('.ccard').nth(1).click()
        pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_selector('.cmet')
        cmp_antes = pg.locator('.cpecab .cpepjn b').all_inner_texts()
        boton('comparativa')
        ok('3 en la comparativa, el tramo muestra los que estaban elegidos', pg.locator('.cpecab .cpepjn b').all_inner_texts() == cmp_antes, cmp_antes)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        for accion, area in (('goTier', 'tierlist'), ('goModos', 'modos'), ('goObjetos', 'objetos'), ('goGlosario', 'glosario'),
                             ('goHistorico', 'historico'), ('goCuenta', 'cuenta'), ('goSettings', 'barra')):
            pg.click(f'nav.topnav [data-a="{accion}"]'); pg.wait_for_timeout(400)
            boton(area); pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        pg.click('nav.topnav [data-a="goCuenta"]'); pg.click('.cutabs [data-a="goTeams"]'); pg.wait_for_timeout(300)
        boton('cuenta')
        pg.click('#rc-tarjeta [data-a="recOtras"]'); pg.wait_for_timeout(200)
        ok('3 «Otras áreas»: una por área (la actual marcada) y el completo',
           pg.locator('#rc-tarjeta [data-a="recArea"]').count() == len(AREAS) and pg.locator('#rc-tarjeta [data-a="recArea"].on').inner_text() == NOMBRE['cuenta']
           and pg.locator('#rc-tarjeta [data-a="recCompleto"]').count() == 1)
        pg.click('#rc-tarjeta [data-a="recArea"][data-v="mesa"]'); pg.wait_for_timeout(300)
        m = pg.evaluate(TARJETA)
        ok('3 desde «Otras áreas», el tramo de la mesa', m['area'] == NOMBRE['mesa'] and m['n'] == 'Paso 1 de 3' and m['luz'], m)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)

        # 6. Siguiente, Anterior, flechas, Esc y tocar afuera (en el roster)
        pg.click('nav.topnav [data-a="back"]'); pg.wait_for_selector('.ccard')
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        ok('6 en el primer paso «Anterior» está apagado', pg.evaluate(TARJETA)['antOff'] is True)
        pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(200)
        ok('6 → pasa al siguiente', pg.evaluate(TARJETA)['n'] == 'Paso 2 de 5')
        pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(200)
        ok('6 ← vuelve', pg.evaluate(TARJETA)['n'] == 'Paso 1 de 5')
        pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(200)
        pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(200)
        pg.click('#rc-tarjeta [data-a="recAnt"]'); pg.wait_for_timeout(200)
        ok('6 «Siguiente», «Siguiente», «Anterior»', pg.evaluate(TARJETA)['n'] == 'Paso 2 de 5')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        ok('6 Esc lo cierra y el foco vuelve a «Recorrido»', not abierto(pg) and pg.evaluate("document.activeElement.dataset.a") == 'recorrido')
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        pg.mouse.click(1390, 890); pg.wait_for_timeout(300)
        ok('6 tocar afuera lo cierra', not abierto(pg))

        # 7. Un paso sin su elemento: el roster sin resultados
        pg.fill('#q', 'zzzzqqq'); pg.wait_for_timeout(300)
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        for _ in range(3):
            pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(200)
        m = pg.evaluate(TARJETA)
        ok('7 sin personajes en la lista, «Un personaje» dice que no está, sin resaltar, al centro',
           m['tit'] == 'Un personaje' and m['falta'] and m['luz'] is None and m['centro'], m)
        pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(200)
        m = pg.evaluate(TARJETA)
        ok('7 y se sigue con el próximo', m['n'] == 'Paso 5 de 5' and m['luz'] and not m['falta'], m)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        ok('7 al salir, la búsqueda sigue', pg.input_value('#q') == 'zzzzqqq')
        pg.click('.toolbar [data-a="clearFilters"]'); pg.wait_for_timeout(300)

        # 8. «Atrás» del navegador
        pg.click('nav.topnav [data-a="goTier"]'); pg.wait_for_timeout(300)
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(200)
        pg.go_back(); pg.wait_for_timeout(500)
        ok('8 «Atrás» con el recorrido abierto lo cierra y vuelve al lugar anterior (el roster)',
           not abierto(pg) and pg.locator('.ccard').count() > 0 and 'on' in pg.get_attribute('nav.topnav [data-a="back"].navlink', 'class'))
        pg.go_forward(); pg.wait_for_timeout(400)
        ok('8 y «Adelante» vuelve a Tier lists', pg.locator('.tlbar').count() == 1 and not abierto(pg))
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        for _ in range(3):
            pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(200)
        ok('8 terminar el tramo vuelve a Tier lists', not abierto(pg) and pg.locator('.tlbar').count() == 1)
        pg.go_back(); pg.wait_for_timeout(500)
        ok('8 el historial no guardó los lugares del recorrido: «Atrás» va al roster', pg.locator('.ccard').count() > 0)

        # 9. Convivencia con el tooltip de la ayuda y con el «Cómo funciona»
        pg.fill('#q', 'Thor'); pg.wait_for_timeout(300)
        pg.locator('.ccard').first.click(); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(300)
        pg.click('.skill .sktit'); pg.wait_for_selector('#skpop')
        caja = pg.locator('nav.topnav [data-a="recorrido"]').bounding_box()
        pg.mouse.click(caja['x'] + 5, caja['y'] + 5); pg.wait_for_timeout(300)
        ok('9 con el «Cómo funciona» abierto, tocar afuera (sobre «Recorrido») solo lo cierra', pg.locator('#skpop').count() == 0 and not abierto(pg))
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        for _ in range(4):
            pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(250)
        ok('9 en el paso de la skill', pg.evaluate(TARJETA)['tit'] == 'Cada skill, en detalle')
        sk = pg.locator('.skill .sktit').first.bounding_box()
        pg.mouse.move(sk['x'] + 10, sk['y'] + 8); pg.wait_for_timeout(300)
        ok('9 pasar el mouse por una skill debajo del recorrido no abre el tooltip',
           pg.evaluate("!document.getElementById('flotay') || document.getElementById('flotay').hidden"))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(200)
        pg.click('main [data-a="back"]'); pg.wait_for_selector('.ccard')

        # 4 y 5. El completo en el escritorio, con la mesa abierta, una búsqueda, uno elegido para comparar y la página bajada
        abrir_mesa(pg); pg.wait_for_timeout(200)
        pg.click('.plista [data-a="mesaPoner"]') if pg.locator('.plista [data-a="mesaPoner"]').count() else None
        pg.locator('.ccard').first.click(); pg.wait_for_selector('.fcab')
        pg.click('main [data-a="mesaPoner"]'); pg.wait_for_timeout(300)
        pg.click('main [data-a="back"]'); pg.wait_for_selector('.ccard')
        pg.fill('#q', 'a'); pg.wait_for_timeout(300)
        pg.click('.toolbar [data-a="pickMode"]'); pg.locator('.ccard').nth(4).click(); pg.click('.toolbar [data-a="pickMode"]')
        pg.wait_for_timeout(300)
        pg.evaluate("window.scrollTo({ top: 700, behavior: 'instant' })"); pg.wait_for_timeout(200)
        antes = pg.evaluate("""() => ({ y: scrollY, q: document.getElementById('q').value, mesa: document.querySelector('nav.topnav [data-a="mesaToggle"] b').textContent,
            bandeja: [...document.querySelectorAll('.mesa .mscmp .pltx b')].map(x => x.textContent), n: history.state.n })""")
        capa0 = capa_txt(D)
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        pg.click('#rc-tarjeta [data-a="recOtras"]'); pg.click('#rc-tarjeta [data-a="recCompleto"]')
        vistos_es = recorrer(pg, False, 'escritorio')
        ok('4 escritorio: las 11 áreas, en orden, con sus pasos', areas_de(vistos_es) == [(n, c) for _, c, n in AREAS], areas_de(vistos_es))
        ok('4 «Paso n de m» cuenta el completo', [m['n'] for m in vistos_es] == [f'Paso {i} de {TOTAL}' for i in range(1, TOTAL + 1)])
        pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(500)
        despues = pg.evaluate("""() => ({ y: scrollY, q: document.getElementById('q').value, mesa: document.querySelector('nav.topnav [data-a="mesaToggle"] b').textContent,
            bandeja: [...document.querySelectorAll('.mesa .mscmp .pltx b')].map(x => x.textContent), n: history.state.n })""")
        ok('5 «Terminar» lo cierra y la app vuelve como estaba (altura, búsqueda, mesa, bandeja, historial)', not abierto(pg) and despues == antes, (antes, despues))
        ok('5 la capa no cambió', capa_txt(D) == capa0)
        ok('5 los del ejemplo de la comparativa no quedaron en la bandeja', not {'Hulk', 'Wolverine'} & set(despues['bandeja']), despues['bandeja'])

        # 10. En inglés
        pg.click('nav.topnav [data-a="lang"]'); pg.wait_for_timeout(300)
        capa1 = capa_txt(D)
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        pg.click('#rc-tarjeta [data-a="recOtras"]'); pg.click('#rc-tarjeta [data-a="recCompleto"]')
        vistos_en = []
        for _ in range(TOTAL):
            pg.wait_for_timeout(150)
            vistos_en.append(pg.evaluate(TARJETA))
            pg.click('#rc-tarjeta [data-a="recSig"]')
        pg.wait_for_timeout(300)
        ok('10 en inglés, el completo llega al final', not abierto(pg) and vistos_en[-1]['sig'] == 'Finish')
        malos = [(i + 1, e['tit']) for i, (e, s) in enumerate(zip(vistos_en, vistos_es))
                 if not e['tit'] or not e['x'] or 'undefined' in e['tit'] + e['x'] or e['tit'] + e['x'] == s['tit'] + s['x']]
        ok('10 cada paso tiene su título y su texto en inglés, distintos del español', not malos, malos)
        ok('10 la tarjeta en inglés', vistos_en[0]['n'] == f'Step 1 of {TOTAL}' and vistos_en[0]['area'] == 'The top bar', vistos_en[0])
        ok('10 la capa no cambió con el recorrido en inglés', capa_txt(D) == capa1)
        pg.click('nav.topnav [data-a="lang"]'); pg.wait_for_timeout(300)
        pg.close()

        # 4. El completo en el celular
        pg = b.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); vigilar(pg)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(300)
        capa2 = capa_txt(D)
        pg.click('nav.topnav [data-a="recorrido"]'); pg.wait_for_timeout(300)
        pg.click('#rc-tarjeta [data-a="recOtras"]'); pg.click('#rc-tarjeta [data-a="recCompleto"]')
        vistos_cel = recorrer(pg, True, 'celular')
        ok('4 celular: las 11 áreas, en orden, con sus pasos', areas_de(vistos_cel) == [(n, c) for _, c, n in AREAS], areas_de(vistos_cel))
        pg.click('#rc-tarjeta [data-a="recSig"]'); pg.wait_for_timeout(400)
        ok('5 celular: termina, en el roster, y la capa no cambió', not abierto(pg) and pg.locator('.ccard').count() > 0 and capa_txt(D) == capa2)
        pg.close()
    finally:
        srv.terminate(); srv.wait()
    # Cada recarga de una página nueva vuelve a pedir la bajada de las imágenes que faltan en la carpeta de datos de las
    # pruebas, y el servidor contesta 409 si ya se están bajando (lo mismo que verif_glosario): eso es del entorno.
    ajenas = [f for f in fallidas if f != (409, 'POST', 'api/imagenes/bajar')]
    ok('sin errores de página ni de consola (salvo el 409 de la bajada de imágenes ya en curso)',
       not errores and not ajenas and len(recursos) == len(fallidas), (errores[:5], ajenas[:5], len(recursos), len(fallidas)))
ok.fin()
