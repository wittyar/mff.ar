"""Tier lists de lectura hasta que se elige «Editar listas» (1.0.52, de la revisión de la navegación: 293 «✕» y el
formulario de crear lista estaban siempre a la vista, sobre listas que casi siempre solo se leen).
  1. Sin editar: ni «✕», ni arrastre, ni «sin ubicar», ni el formulario de crear, ni «Duplicar»; tocar una entrada abre su
     ficha (el personaje y el uniforme de esa entrada).
  2. «Editar listas»: aparece todo eso, con la barra que lo dice; tocar una entrada abre el selector de filas.
  3. Quitar una entrada de una importada: queda «Deshacer mis cambios (1)» y en la capa; al dejar de editar, la lista dice
     que tiene un cambio tuyo.
  4. Crear una lista propia: queda elegida y se sigue editando (renombrar, editar filas, eliminar); sin editar, esos
     controles no están.
  5. Elegir para comparar es del roster: al pasar a Tier lists se deja de elegir y tocar una entrada abre su ficha.
  6. En inglés. Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_TIERLISTS', 'MFF_SEED_TIER_ASSIGNMENTS')
LISTA = D['MFF_SEED_TIERLISTS'][0]
ASIG = D['MFF_SEED_TIER_ASSIGNMENTS'][LISTA['id']]
LUGARES = sum(len(v) for v in ASIG.values())
DIR = carpeta_datos()
capa = lambda: json.load(open(os.path.join(DIR, 'capa.json'), encoding='utf-8'))
srv, url = levantar(DIR, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' and '404' not in m.text else None)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(500)
        pg.click('nav.topnav [data-a="goTier"]'); pg.wait_for_selector('.tlchip')
        cuenta = lambda sel: pg.locator(sel).count()

        # 1. de lectura
        ok('1 abre en la primera lista, de lectura: todas sus entradas y el botón «Editar listas»', cuenta('.tierrow .tlchip') == LUGARES
           and pg.locator('[data-a="tlEditar"]').inner_text() == 'Editar listas' and pg.locator('[data-a="tlEditar"]').get_attribute('aria-pressed') == 'false',
           (cuenta('.tierrow .tlchip'), LUGARES))
        ok('1 sin «✕», arrastre, «sin ubicar», formulario de crear ni «Duplicar»',
           cuenta('[data-a="unassign"]') + cuenta('.tlchip[draggable]') + cuenta('[data-a="togglePool"]') + cuenta('[data-a="addList"]') + cuenta('[data-a="newListName"]')
           + cuenta('[data-a="dupList"]') + cuenta('[data-a="tlAbrir"]') + cuenta('.tierrow[data-a="drop"]') == 0)
        chip = pg.locator('.tierrow button.tlchip').nth(3)
        key = chip.get_attribute('data-key'); cid, uid = key.split('::')
        chip.click(); pg.wait_for_selector('.fcab')
        ok('1 tocar una entrada abre su ficha, en ese uniforme', pg.locator('select[data-a="uniformSel"]').input_value() == uid
           and pg.locator('.plista .plit.on [data-a="fichaVecina"]').get_attribute('data-cid') == cid, (key, pg.locator('select[data-a="uniformSel"]').input_value()))
        ok('1 y la ficha tiene cómo volver a la lista', pg.locator('[data-a="atras"]').count() == 1 and 'Tier lists' in pg.locator('[data-a="atras"]').inner_text())
        pg.click('[data-a="atras"]'); pg.wait_for_selector('.tlchip')

        # 2. editando
        pg.click('[data-a="tlEditar"]'); pg.wait_for_timeout(250)
        ok('2 «Editar listas»: la barra lo dice y el botón pasa a «Listo»', cuenta('.tledit') == 1 and pg.locator('[data-a="tlEditar"]').inner_text() == 'Listo'
           and pg.locator('[data-a="tlEditar"]').get_attribute('aria-pressed') == 'true', pg.locator('.tledit').all_inner_texts())
        ok('2 con «✕» en cada entrada, arrastre, «sin ubicar», crear y «Duplicar»', cuenta('[data-a="unassign"]') == LUGARES and cuenta('.tlchip[draggable]') == LUGARES
           and cuenta('[data-a="togglePool"]') == 1 and cuenta('[data-a="addList"]') == 1 and cuenta('[data-a="dupList"]') == 1 and cuenta('.tierrow[data-a="drop"]') == len(LISTA['rows']),
           (cuenta('[data-a="unassign"]'), LUGARES))
        pg.locator('.tierrow .tlchip').nth(3).click(); pg.wait_for_timeout(200)
        ok('2 tocar una entrada abre el selector de filas', cuenta('.modal .filasel') == 1 and cuenta('.fcab') == 0)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)

        # 3. quitar una entrada
        x = pg.locator('.tierrow .tlchip').first
        quitada, fila = x.get_attribute('data-key'), x.get_attribute('data-from')
        x.locator('[data-a="unassign"]').click(); pg.wait_for_timeout(600)
        ok('3 quitar una entrada: sale de la fila, «Deshacer mis cambios (1)» y queda en la capa', cuenta(f'.tlchip[data-key="{quitada}"][data-from="{fila}"]') == 0
           and pg.locator('[data-a="resetList"]').inner_text().endswith('(1)') and quitada in capa()['assign'][LISTA['id']], capa().get('assign'))
        pg.click('[data-a="tlEditar"]'); pg.wait_for_timeout(250)
        ok('3 de lectura otra vez: la lista dice que tiene un cambio tuyo, sin el botón de deshacer', '1 cambios tuyos' in pg.inner_text('.tlsource').lower()
           and cuenta('[data-a="resetList"]') == 0 and cuenta('[data-a="unassign"]') == 0, pg.inner_text('.tlsource'))

        # 4. una lista propia
        pg.click('[data-a="tlEditar"]'); pg.wait_for_timeout(200)
        pg.fill('[data-a="newListName"]', 'Lista de prueba'); pg.click('[data-a="addList"]'); pg.wait_for_timeout(500)
        ok('4 crear una lista: queda elegida y se sigue editando, con renombrar, editar filas y eliminar', pg.locator('.tlbar .chip.on').inner_text() == 'Lista de prueba'
           and cuenta('.tledit') == 1 and cuenta('[data-a="listName"]') == 1 and cuenta('[data-a="editRows"]') == 1 and cuenta('[data-a="removeList"]') == 1
           and [l['name'] for l in capa()['lists']] == ['Lista de prueba'])
        pg.click('[data-a="tlEditar"]'); pg.wait_for_timeout(250)
        ok('4 sin editar: la lista propia tampoco muestra esos controles', cuenta('[data-a="listName"]') + cuenta('[data-a="editRows"]') + cuenta('[data-a="removeList"]') == 0
           and 'lista propia' in pg.inner_text('.tlsource').lower())

        # 5. eligiendo para comparar
        pg.locator('.tlbar .chip').first.click(); pg.wait_for_timeout(250)
        pg.evaluate("document.querySelector('nav.topnav .navlink').click()"); pg.wait_for_selector('.ccard')
        pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(150)
        pg.click('nav.topnav [data-a="goTier"]'); pg.wait_for_selector('.tlchip')
        chip = pg.locator('.tierrow button.tlchip').nth(5); key = chip.get_attribute('data-key')
        chip.click(); pg.wait_for_timeout(250)
        ok('5 se venía eligiendo para comparar: en Tier lists ya no, y tocar una entrada abre su ficha sin sumarla',
           cuenta('.fcab') == 1 and pg.locator('select[data-a="uniformSel"]').input_value() == key.split('::')[1] and cuenta('aside.mesa .mscmp') == 0)
        pg.evaluate("document.querySelector('nav.topnav .navlink').click()"); pg.wait_for_selector('.ccard')
        ok('5 y en el roster, «Comparar» quedó apagado', 'primary' not in pg.get_attribute('[data-a="pickMode"]', 'class'))

        # 6. inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.click('nav.topnav [data-a="goTier"]'); pg.wait_for_selector('.tlchip')
        ok('6 inglés: «Edit lists» y la marca de tus cambios', pg.locator('[data-a="tlEditar"]').inner_text() == 'Edit lists' and '1 changes of yours' in pg.inner_text('.tlsource').lower(),
           pg.inner_text('.tlsource'))
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)

        ok('sin errores de página ni de consola', not errores, errores[:4])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
