"""«Atrás»: de la ficha de un personaje se pasa a otro desde sus combinaciones, y se vuelve al
primero tal como estaba (pestaña Equipos, la misma página, la misma posición). También con el
volver del navegador (Alt+← o el botón del mouse), y «← Roster» vuelve al roster donde estaba."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
ok = Chequeo()
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        estado = lambda: pg.evaluate("({ view: history.state.view, charId: history.state.charId, tab: history.state.fichaTab, pag: history.state.eqPagina, n: history.state.n })")

        # roster: segunda página, bajando un poco; se abre una ficha y «← Roster» vuelve ahí
        pg.click('[data-a="page"][data-p="1"]'); pg.wait_for_timeout(1200)   # el cambio de página sube con animación
        pg.evaluate("window.scrollTo({ top: 600, behavior: 'instant' })"); pg.wait_for_timeout(200)
        y_roster = pg.evaluate("scrollY")
        # se toca una tarjeta que está a la vista, sin que el clic mueva la página
        y_roster = pg.evaluate("""() => { const c = [...document.querySelectorAll('.ccard')]
            .find(x => { const r = x.getBoundingClientRect(); return r.top > 120 && r.bottom < innerHeight; });
            const y = scrollY; c.click(); return y; }""")
        pg.wait_for_selector('.fcab')
        ok('desde el roster, la ficha no muestra un «Atrás» aparte (lo hace «← Roster»)', pg.locator('[data-a="atras"]').count() == 0)
        pg.click('main [data-a="back"]'); pg.wait_for_selector('.ccard')
        pg.wait_for_timeout(300)
        pagina = pg.locator('button.primary[data-a="page"]').first.inner_text().strip()
        ok('«← Roster» vuelve a la misma página del roster y a la misma altura',
           pagina == '2' and abs(pg.evaluate("scrollY") - y_roster) < 5, (pagina, pg.evaluate("scrollY"), y_roster))

        # Abomination, pestaña Equipos, página 2 de las combinaciones
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        pg.fill('#q', 'Abomination'); pg.wait_for_timeout(300)
        pg.click('.ccard[data-cid="abomination"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
        pg.click('#combos [data-a="eqPagina"][data-p="1"]'); pg.wait_for_timeout(300)
        combo = pg.locator('#combos .combo').nth(3)
        combo.scroll_into_view_if_needed(); pg.wait_for_timeout(150)
        y_abo = pg.evaluate("scrollY")
        # el líder va primero (4 de octubre de 2026): el primer retrato que no es él
        otro = combo.locator('[data-a="open"]:not([data-cid="abomination"])').first
        otro_cid = otro.get_attribute('data-cid')
        otro.click(); pg.wait_for_selector(f'.fcab'); pg.wait_for_timeout(300)
        e1 = estado()
        ok('se pasó a otro personaje desde una combinación', e1['view'] == 'detail' and e1['charId'] == otro_cid and e1['charId'] != 'abomination', e1)
        boton = pg.locator('[data-a="atras"]')
        ok('su ficha muestra «← Abomination»', boton.count() == 1 and boton.inner_text().strip() == '← Abomination', boton.all_inner_texts())
        ok('el título dice a qué vuelve (personaje y pestaña)', 'Abomination' in (boton.get_attribute('title') or '') and 'Equipos' in (boton.get_attribute('title') or ''),
           boton.get_attribute('title'))
        boton.click()
        pg.wait_for_selector('#combos .combo', timeout=60000); pg.wait_for_timeout(500)
        e2 = estado()
        ok('«Atrás» vuelve a Abomination, en Equipos y en la página 2', e2['charId'] == 'abomination' and e2['tab'] == 'equipos' and e2['pag'] == 1, e2)
        ok('y a la misma altura', abs(pg.evaluate("scrollY") - y_abo) < 5, (pg.evaluate("scrollY"), y_abo))
        # adelante y otra vez atrás con el navegador (Alt+← o el botón del mouse)
        pg.go_forward(); pg.wait_for_timeout(500)
        ok('adelante: vuelve al otro personaje', estado()['charId'] == otro_cid, estado())
        pg.go_back(); pg.wait_for_selector('#combos .combo', timeout=60000); pg.wait_for_timeout(500)
        ok('el volver del navegador hace lo mismo', estado()['charId'] == 'abomination' and estado()['pag'] == 1, estado())
        # cambiar de uniforme o de pestaña no suma pasos: «Atrás» sigue llevando al lugar anterior
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(200)
        n_antes = estado()['n']
        pg.click('[data-a="fichaTab"][data-v="resumen"]'); pg.wait_for_timeout(200)
        ok('cambiar de pestaña no abre otra entrada', estado()['n'] == n_antes, (estado()['n'], n_antes))
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
