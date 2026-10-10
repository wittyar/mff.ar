"""Flechas de la ficha: anterior y siguiente del listado del roster con sus filtros y su orden,
la posición, los extremos, las teclas ← y →, la pestaña que se conserva, "fuera del listado"
y el celular."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
ok = Chequeo()
FUERA = """() => [...document.querySelectorAll('.fcab *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > innerWidth + 0.5; })
  .map(e => (e.getAttribute('data-a') || e.className || e.tagName) + ' → ' + Math.round(e.getBoundingClientRect().right)).slice(0, 3)"""
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        # listado filtrado: clase Combate
        pg.click('[data-a="toggleFilters"]'); pg.wait_for_timeout(200)
        pg.click('[data-a="filter"][data-cat="c"][data-v="Combate"]'); pg.wait_for_timeout(300)
        pg.click('[data-a="toggleFilters"]'); pg.wait_for_timeout(200)
        lista = pg.evaluate("[...document.querySelectorAll('.ccard')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base'))")
        total = int(pg.locator('.toolbar, body').first.inner_text().split(' de ')[0].split()[-1]) if False else None
        pg.locator('.ccard').nth(1).click(); pg.wait_for_selector('.fcab')
        actual = lambda: pg.evaluate("document.querySelector('.fcab h1').textContent + '|' + document.querySelector('select[data-a=\"uniformSel\"]').value")
        pos = pg.locator('.fnav .muted').inner_text()
        ok('posición: 2 de N', pos.startswith('2 de '), pos)
        n = int(pos.split(' de ')[1].replace('.', ''))
        def esperado(k):
            cid, uid = k.split('::')
            return pg.evaluate(f"(MFF_SEED_CHARACTERS.find(c => c.id === '{cid}') || {{}}).name") + '|' + uid
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(150)
        pg.locator('.fnav [data-a="fichaVecina"]').last.click(); pg.wait_for_timeout(250)
        ok('› pasa al tercero del listado, con su uniforme', actual() == esperado(lista[2]) and pg.locator('.fnav .muted').inner_text().startswith('3 de'), (actual(), lista[2]))
        ok('se queda en la pestaña elegida', pg.locator('.ftab.on').inner_text() == 'Skills')
        pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(250); pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(250)
        ok('← dos veces: el primero, y ‹ queda deshabilitada', actual() == esperado(lista[0]) and pg.locator('.fnav button').first.is_disabled(), actual())
        pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(250)
        ok('→: el segundo', actual() == esperado(lista[1]))
        # escribir en un campo no navega
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos select', timeout=60000)
        pg.focus('select[data-a="eqOrden"]'); pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(250)
        orden = pg.locator('select[data-a="eqOrden"]').input_value()
        ok('con el foco en un selector, ← y → no cambian de personaje', actual() == esperado(lista[1]), f'orden: {orden}')
        # → en el selector cambió el orden (a PvP): se vuelve a «puntos para él», que tiene lista con
        # cualquier personaje (desde la 1.0.15, PvP no arma combinaciones a quien no tiene función ahí).
        pg.select_option('select[data-a="eqOrden"]', 'foco'); pg.wait_for_timeout(250)
        # el último del listado
        pg.evaluate("document.activeElement.blur()")
        ultimo = n - 1
        # ir al último desde el roster (última página)
        pg.click('[data-a="back"]'); pg.wait_for_selector('.ccard')
        paginas = pg.locator('[data-a="page"]').all()
        if paginas: pg.locator('[data-a="page"]').nth(len(paginas) - 2).click(); pg.wait_for_timeout(250)
        pg.locator('.ccard').last.click(); pg.wait_for_selector('.fcab')
        ok('el último: N de N y › deshabilitada', pg.locator('.fnav .muted').inner_text() == f'{n} de {n}'.replace(',', '.') or pg.locator('.fnav .muted').inner_text().startswith(f'{n} de'),
           pg.locator('.fnav .muted').inner_text())
        ok('› deshabilitada en el último', pg.locator('.fnav button').last.is_disabled())
        # fuera del listado: un personaje de otra clase (desde la búsqueda de Comparar no hace falta: se cambia el filtro)
        pg.click('[data-a="back"]'); pg.wait_for_selector('.ccard')
        if not pg.locator('[data-a="filter"][data-cat="c"][data-v="Combate"]').count(): pg.click('[data-a="toggleFilters"]'); pg.wait_for_timeout(200)
        pg.click('[data-a="filter"][data-cat="c"][data-v="Combate"]'); pg.wait_for_timeout(200)   # saca el filtro
        pg.click('[data-a="toggleFilters"]'); pg.wait_for_timeout(200)
        pg.fill('#q', 'Wong'); pg.wait_for_timeout(250); pg.click('.ccard[data-cid="wong"][data-uid=""]'); pg.wait_for_selector('.fcab')
        ok('sin filtros, Wong tiene posición', 'de' in pg.locator('.fnav .muted').inner_text(), pg.locator('.fnav .muted').inner_text())
        pg.click('[data-a="back"]'); pg.wait_for_selector('#q'); pg.fill('#q', 'Annihilus'); pg.wait_for_timeout(250)
        pg.click('.ccard[data-cid="annihilus"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
        # el líder va primero (4 de octubre de 2026): el primer retrato que no es Annihilus
        pg.locator('#combos .combo').first.locator('.eqfoto:not([data-cid="annihilus"])').first.click(); pg.wait_for_selector('.fcab'); pg.wait_for_timeout(200)
        ok('abierto desde un retrato que no está en el listado (búsqueda «Annihilus»): fuera del listado, flechas deshabilitadas',
           pg.locator('.fnav .muted').inner_text() == 'fuera del listado' and all(x.is_disabled() for x in pg.locator('.fnav button').all()))
        ok('sin errores de página', not errores, errores[:3])
        b.close()
        # celular
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.locator('.ccard').nth(3).click(); pg.wait_for_selector('.fcab')
        ok('celular: flechas a la vista y nada se sale de la pantalla', pg.locator('.fnav').is_visible() and not pg.evaluate(FUERA), pg.evaluate(FUERA))
        alto = pg.evaluate("Math.round(document.querySelector('.fcab').getBoundingClientRect().height)")
        ok('celular: la cabecera fija no crece de más', alto <= 190, alto)
        pg.screenshot(path=f'{SALIDA}/flechas_390.png')
        ok('sin errores de página (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
