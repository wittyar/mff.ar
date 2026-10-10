"""Recorrida por las vistas principales sin errores de página (regresión general)."""
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
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.goto(url); pg.wait_for_selector('.ccard')
        for accion, espera in (('goTier', '.tlrow, .tl, table'), ('goModos', 'main'), ('goTeams', 'main'),
                               ('goSettings', '#seccion-actualizaciones')):
            pg.click(f'[data-a="{accion}"]'); pg.wait_for_timeout(500)
            ok(f'vista {accion}', pg.locator('main').inner_text().strip() != '')
        pg.click('[data-a="back"]') if pg.locator('[data-a="back"]').count() else None
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.locator('.ccard').nth(3).click(); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(150)
        ok('ficha abre con skills', pg.locator('.skill').count() > 3, pg.locator('.skill').count())
        pg.click('[data-a="view"][data-v="tabla"]') if pg.locator('[data-a="view"][data-v="tabla"]').count() else None
        ok('sin errores de página ni de consola', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
