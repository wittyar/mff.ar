"""El caso de la captura: Abominación, pasiva T2 «Puños del Devastador del Mundo» →
«Aliados de radiación gamma» abre la lista."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright
ok = Chequeo()
C = datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS']
abo = next(c for c in C if c['name'] == 'Abomination')
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.fill('#q', 'Abomination'); pg.wait_for_timeout(300)
        pg.click(f'.ccard[data-cid="{abo["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(150)
        tarjeta = pg.locator('.skill', has_text='Puños del Devastador del Mundo').first
        bt = tarjeta.locator('button.tag.objetivo', has_text='radiación gamma')
        ok('la pasiva T2 muestra el objetivo como botón', bt.count() == 1)
        bt.click()
        cab = pg.locator('.modal.ancho .altitulo + div').inner_text()
        nombres = [x.inner_text() for x in pg.locator('.modal.ancho .alnm').all()]
        ok('lista de aliados de radiación gamma', 'Radiación Gamma' in cab and '6 personajes' in cab, (cab, nombres))
        ok('sin errores de página', not errores, errores[:2])
        pg.screenshot(path=f'{SALIDA}/abominacion_gamma.png')
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
