"""Objetos (1.0.56; Ezequiel, 18 de noviembre de 2026: «Arma un modulo para CTPs, donde este el detalle. Bendiciones de
Odin, Javis, Emblemas, Sets de Iso e ISOs»). Lo que se espera sale de data.js (MFF_CTPS, MFF_OBJETOS, MFF_GUIA_ARMADO), no
de app.js:
  1. La barra: «Objetos» en el grupo del juego, en lugar de «Cromos»; la sub-barra con C.T.P., ISO-8, Bendiciones de Odín,
     Emblemas, J.A.R.V.I.S. y Cromos, cada una con cuántos tiene.
  2. C.T.P.: están todos; el grupo; el grado (los valores de Rage normal y brillante, la reforja solo en poderoso y
     brillante); de dónde se consigue; a cuántos y a quiénes se lo pone la guía de armado; el propio, marcado; la búsqueda.
  3. ISO-8: las 8 piedras y los 26 sets; «Da» y las piezas; el detalle (piezas, lo que da con su valor, la activación);
     el nombre del juego en español de Fuerza del Hulk cabreado; lo dudoso de Healing Factor, marcado.
  4. Bendiciones de Odín: están todas; «Da» y el color; el detalle con valor, bono y total.
  5. Emblemas: están todos; colección, rareza, tipo y «Da»; el detalle con los 60 niveles y dónde rige (enlace a Modos);
     «De lujo», marcado dudoso.
  6. J.A.R.V.I.S.: los 27 chips por tipo; el filtro; que no hay valores, dicho; los modos en que rige.
  7. Enlaces: desde la ficha (Armado) un C.T.P. y un set de ISO-8 abren su detalle en Objetos, y «Atrás» vuelve a la ficha;
     desde Modos, un set de ISO-8.
  8. El historial: la pestaña de Objetos se recuerda al volver con «Atrás».
  9. En inglés; en el celular, ninguna pestaña desborda el ancho. Sin errores de página ni 404."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, SALIDA  # noqa: E401
import re
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_CTPS', 'MFF_OBJETOS', 'MFF_GUIA_ARMADO')
CTPS, O, GA = D['MFF_CTPS'], D['MFF_OBJETOS'], D['MFF_GUIA_ARMADO']
B, E, S, J = O['odin']['bendiciones'], O['emblemas']['emblemas'], O['iso']['sets'], O['jarvis']['chips']
TABS = [('ctp', 'C.T.P.', len(CTPS)), ('iso', 'ISO-8', len(S)), ('odin', 'Bendiciones de Odín', len(B)),
        ('emblemas', 'Emblemas', len(E)), ('jarvis', 'J.A.R.V.I.S.', len(J))]
num = lambda x: (f'{x:.2f}'.rstrip('0').rstrip('.')).replace('.', ',')   # como numTxt en español
armado = lambda c: sorted(p for p, e in GA['pj'].items() if any(x['c'] == c for x in e.get('ctp') or []))
VISTOS = "[...document.querySelectorAll('main details.objitem')].map(x => x.id).sort()"

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); errores, recursos = [], []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('response', lambda r: r.status == 404 and recursos.append(r.url))
        pg.goto(url); pg.wait_for_selector('.ccard')
        vistos = lambda: sorted(pg.evaluate(VISTOS))
        def tab(k): pg.click(f'.cutabs [data-a="objTab"][data-v="{k}"]'); pg.wait_for_timeout(300)
        def chip(k, v): pg.click(f'main [data-a="obFiltro"][data-k="{k}"][data-v="{v}"]'); pg.wait_for_timeout(250)
        def da(k, v): pg.select_option(f'main select[data-a="obFiltro"][data-k="{k}"]', v); pg.wait_for_timeout(250)
        def abrir(id_): pg.click(f'#{id_} > summary'); pg.wait_for_timeout(200); return pg.locator(f'#{id_} .glcuerpo').inner_text()

        # 1. la barra y la sub-barra
        juego = pg.locator('nav.topnav .navgrupo:not(.cuenta) .navlink').all_inner_texts()
        ok('1 «Objetos» en el grupo del juego, en lugar de «Cromos»', 'Objetos' in juego and 'Cromos' not in juego, juego)
        pg.click('[data-a="goObjetos"]'); pg.wait_for_selector('.cucab.juego')
        tabs = pg.locator('.cucab.juego .cutab').all_inner_texts()
        espera = [f'{n} {k}' for _, n, k in TABS] + [f"Cromos {len(datos_js('MFF_CROMOS')['MFF_CROMOS']['cromos'])}"]
        ok('1 la sub-barra: las seis pestañas en orden, con cuántos tiene cada una', [re.sub(r'\s+', ' ', x) for x in tabs] == espera, tabs)
        ok('1 abre en C.T.P.', pg.locator('.cutab.on').inner_text().startswith('C.T.P.'))

        # 2. C.T.P.
        ok('2 están todos los C.T.P.', vistos() == sorted('ctp-' + c['id'] for c in CTPS), len(vistos()))
        chip('ctpGrupo', 'pvp')
        ok('2 el grupo PvP', vistos() == sorted('ctp-' + c['id'] for c in CTPS if c['grupo'] == 'pvp'), vistos())
        chip('ctpGrupo', '')
        rage = next(c for c in CTPS if c['id'] == 'rage')
        fija = next(o for o in rage['op'] if o['k'] == 'fija')
        tx = abrir('ctp-rage')
        ok('2 Rage brillante: la opción bloqueada con sus valores de brillante', all(v in tx for v in fija['v']['brillante']) and 'Brillante' in tx, tx[:300])
        esp = next(o for o in rage['op'] if o['k'] == 'esp')
        ok('2 Rage brillante: la reforja con sus valores', 'Rabioso' in tx and esp['v']['brillante'][0] in tx, tx)
        ok('2 de dónde se consigue el brillante', 'Superéxito al reforjar un C.T.P.' in tx, tx[-400:])
        pjs = armado('rage')
        ok('2 a cuántos se lo pone la guía de armado', f'se lo pone a {len(pjs)} personajes' in tx
           and pg.locator('#ctp-rage .objpjs .minipj').count() == len(pjs), (len(pjs), pg.locator('#ctp-rage .objpjs .minipj').count()))
        chip('ctpGrado', 'normal')
        ok('2 cambiar el grado no cierra lo abierto', pg.locator('#ctp-rage').get_attribute('open') is not None)
        tx = pg.locator('#ctp-rage .glcuerpo').inner_text()
        ok('2 en normal, los valores de normal y sin reforja', all(v in tx for v in fija['v']['normal'])
           and pg.locator('#ctp-rage .ctpop').count() == len(fija['o']) and 'solo en poderoso y brillante' in tx, tx[-500:])
        chip('ctpGrado', 'brillante')
        prop = next(c for c in CTPS if c.get('pr'))
        ok('2 el propio (Ascenso), marcado y sin ícono', pg.locator(f'#ctp-{prop["id"]} .propio').count() == 1
           and pg.locator(f'#ctp-{prop["id"]} summary img').count() == 0, prop['id'])
        pg.fill('#q', 'furia'); pg.wait_for_timeout(300)
        ok('2 la búsqueda, también por el nombre del juego en español (furia: Rage)', vistos() == ['ctp-rage'], vistos())
        pg.fill('#q', ''); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{SALIDA}/objetos_ctp_1400.png')

        # 3. ISO-8
        tab('iso')
        ok('3 las 8 piedras y los 26 sets', pg.locator('.objpiedra').count() == 8 and vistos() == sorted('iso-' + s['id'] for s in S)
           and len(S) == 26, (pg.locator('.objpiedra').count(), len(vistos())))
        da('isoStat', 'cd')
        ok('3 «Da»: reducir duración de recarga', vistos() == sorted('iso-' + s['id'] for s in S if any(x['s'] == 'cd' for x in s['st'])), vistos())
        da('isoStat', ''); chip('isoPiezas', '3')
        ok('3 los de 3 piezas', vistos() == sorted('iso-' + s['id'] for s in S if len(s['piezas']) == 3), len(vistos()))
        chip('isoPiezas', '')
        hulk = next(s for s in S if s['n'] == 'Power of Angry Hulk')
        ok('3 Power of Angry Hulk con su nombre del juego en español', pg.locator(f'#iso-{hulk["id"]} summary').inner_text().startswith('Fuerza del Hulk cabreado'))
        tx = abrir('iso-' + hulk['id'])
        ok('3 el detalle: piezas, lo que da con su valor y la activación', '8 piezas' in tx.lower() and all(f'{num(x["v"])}%' in tx for x in hulk['st'])
           and hulk['act'][1]['es'] in tx and pg.locator(f'#iso-{hulk["id"]} summary .piedras i').count() == 8, tx[:400])
        ok('3 lo que dicen la guía de principiantes y la de armado', 'propone para PvE' in tx and 'Ofensivo' in tx, tx[-300:])
        hf = next(s for s in S if s['n'] == 'Healing Factor')
        ok('3 Healing Factor: lo dudoso de la wiki, marcado', pg.locator(f'#iso-{hf["id"]} summary .dudatag').count() == 1)

        # 4. Bendiciones de Odín
        tab('odin')
        ok('4 están todas', vistos() == sorted('odin-' + x['id'] for x in B) and len(B) == 17, len(vistos()))
        da('odinStat', 'igdef')
        ok('4 «Da»: ignorar defensa', vistos() == sorted('odin-' + x['id'] for x in B if any(s['s'] == 'igdef' for s in x['st'])), vistos())
        da('odinStat', ''); chip('odinColor', 'red')
        ok('4 el color rojo', vistos() == sorted('odin-' + x['id'] for x in B if x['color'] == 'red'), vistos())
        chip('odinColor', '')
        amp = next(x for x in B if x['n'] == 'Amplify')
        abrir('odin-' + amp['id'])
        filas = pg.locator(f'#odin-{amp["id"]} tbody tr').all_inner_texts()
        ok('4 el detalle: valor, bono y total de cada stat', len(filas) == 2 and all(num(v) in f for st, f in zip(amp['st'], filas) for v in st['v']), filas)
        ok('4 de dónde cae', 'Cae en: Jefe mundial definitivo: Ebony Maw' in pg.locator(f'#odin-{amp["id"]}').inner_text())

        # 5. Emblemas
        tab('emblemas')
        ok('5 están todos', vistos() == sorted('emblema-' + x['id'] for x in E) and len(E) == 63, len(vistos()))
        chip('emCol', 'IRON MAN')
        ok('5 colección Iron Man', vistos() == sorted('emblema-' + x['id'] for x in E if x['col'] == 'IRON MAN'), len(vistos()))
        chip('emCol', 'sin')
        ok('5 sin colección', vistos() == sorted('emblema-' + x['id'] for x in E if not x['col']), vistos())
        chip('emCol', ''); chip('emRar', 'Mythic')
        ok('5 rareza mítica', vistos() == sorted('emblema-' + x['id'] for x in E if x['r'] == 'Mythic'), vistos())
        chip('emRar', ''); chip('emTipo', 'libre')
        ok('5 los que rigen en todo', vistos() == sorted('emblema-' + x['id'] for x in E if x['libre']), vistos())
        chip('emTipo', ''); da('emStat', 'inst_atk')
        ok('5 «Da»: ATQ de instinto', vistos() == sorted('emblema-' + x['id'] for x in E if x['s'] == 'inst_atk'), vistos())
        da('emStat', '')
        mj = next(x for x in E if x['n'] == 'Mary Jane Watson')
        tx = abrir('emblema-' + mj['id'])
        celdas = pg.locator(f'#emblema-{mj["id"]} .emniv span').count()
        ok('5 el detalle: los 60 niveles, del 1 al 60', celdas == 60 and f'{num(mj["v"][0])}% en el nivel 1' in tx and f'{num(mj["v"][59])}% en el nivel 60' in tx, (celdas, tx[:200]))
        ok('5 dónde rige: el modo de su colección, con enlace a Modos', pg.locator(f'#emblema-{mj["id"]} [data-a="verModo"][data-id="timeline-battle"]').count() == 1)
        lujo = next(x for x in E if x['r'] == 'Advanced')
        ok('5 «De lujo» (Advanced), marcado dudoso', 'DE LUJO' in pg.locator(f'#emblema-{lujo["id"]} summary').inner_text().upper()
           and pg.locator(f'#emblema-{lujo["id"]} summary .dudatag').count() == 1)
        pg.click(f'#emblema-{mj["id"]} [data-a="verModo"]'); pg.wait_for_timeout(400)
        ok('5 el enlace lleva a Modos, con el modo abierto', pg.locator('nav .navlink.on').inner_text() == 'Modos')
        pg.go_back(); pg.wait_for_timeout(400)
        ok('8 «Atrás» desde Modos vuelve a Objetos › Emblemas', pg.locator('.cutab.on').inner_text().startswith('Emblemas'))

        # 6. J.A.R.V.I.S.
        tab('jarvis')
        ok('6 los 27 chips, en tres tipos', vistos() == sorted('jarvis-' + x['id'] for x in J) and len(J) == 27
           and pg.locator('main .section h3').count() == 3, len(vistos()))
        chip('jvCat', 'especial')
        ok('6 el filtro por tipo', vistos() == sorted('jarvis-' + x['id'] for x in J if x['cat'] == 'especial'), len(vistos()))
        chip('jvCat', '')
        ok('6 dice que no hay valores', 'Sin valores' in pg.locator('main .objaviso').inner_text())
        pg.click('main .objnotas > summary'); pg.wait_for_timeout(200)
        ok('6 los modos en que rige, con enlace', pg.locator('main .objnotas [data-a="verModo"]').count() == len(O['jarvis']['modos']['ids']))

        # 7. enlaces desde la ficha y Modos
        pg.click('nav.topnav [data-a="back"]'); pg.wait_for_selector('.ccard')
        pg.fill('.toolbar .search input', 'Thor'); pg.wait_for_timeout(400); pg.locator('.ccard').first.click(); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(400)
        quien = pg.locator('.fcab h1').inner_text()
        l = pg.locator('main [data-a="verObj"][data-tab="ctp"]').first; destino = l.get_attribute('data-id')
        l.click(); pg.wait_for_timeout(400)
        ok('7 un C.T.P. de la ficha abre su detalle en Objetos', pg.locator('.cutab.on').inner_text().startswith('C.T.P.')
           and pg.locator(f'#{destino}').get_attribute('open') is not None and 'resaltada' in pg.locator(f'#{destino}').get_attribute('class'), destino)
        pg.go_back(); pg.wait_for_timeout(400)
        ok('7 «Atrás» vuelve a la ficha, en Armado', pg.locator('.fcab h1').inner_text() == quien and pg.locator('.ftab.on').inner_text() == 'Armado')
        l = pg.locator('main [data-a="verObj"][data-tab="iso"]').first; destino = l.get_attribute('data-id')
        l.click(); pg.wait_for_timeout(400)
        ok('7 un set de ISO-8 de la ficha abre su detalle', pg.locator('.cutab.on').inner_text().startswith('ISO-8')
           and pg.locator(f'#{destino}').get_attribute('open') is not None, destino)
        pg.click('nav.topnav [data-a="goModos"]'); pg.wait_for_timeout(400)
        l = pg.locator('main [data-a="verObj"][data-tab="iso"]').first; destino = l.get_attribute('data-id')
        l.click(); pg.wait_for_timeout(400)
        ok('7 desde Modos, un set de ISO-8', pg.locator(f'#{destino}').get_attribute('open') is not None, destino)

        # 8. el historial: la pestaña se recuerda
        tab('odin'); pg.click('nav.topnav [data-a="goGlosario"]'); pg.wait_for_timeout(300); pg.go_back(); pg.wait_for_timeout(400)
        ok('8 «Atrás» desde el Glosario vuelve a Objetos › Bendiciones de Odín', pg.locator('.cutab.on').inner_text().startswith('Bendiciones'))

        # 9. inglés y celular
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('9 en inglés', pg.locator('nav .navlink.on').inner_text() == 'Items' and pg.locator('main h1').inner_text().startswith("Odin's Blessings")
           and "Odin's Blessing: Amplify" in pg.locator('main').inner_text())
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(300)
        for k, _, _ in TABS + [('cromos', '', 0)]:
            tab(k)
            if k != 'cromos':
                pg.locator('main details.objitem > summary').first.click(); pg.wait_for_timeout(200)
            anchos = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
            ok(f'9 celular: {k} no desborda el ancho', anchos[0] <= anchos[1], anchos)
            pg.screenshot(path=f'{SALIDA}/objetos_{k}_390.png')
        ok('sin errores de página', not errores, errores[:3])
        ok('sin imágenes que den 404', not recursos, recursos[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
