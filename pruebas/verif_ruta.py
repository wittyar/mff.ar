"""Hoja de ruta (pestaña Progreso): el paso previo al Tier-4 pide skills en Nv. 10 y el aviso dice por qué."""
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
        for lang, paso, aviso in (('es', 'skills en Nv. 10', 'Las skills llegan hasta el Nv. 10'), ('en', 'Skill Lv.10', 'Skills go up to Lv.10')):
            if lang == 'en': pg.click('[data-a="lang"]'); pg.wait_for_timeout(200)
            pg.evaluate("""() => { const el = document.createElement('button'); el.dataset.a = 'open';
                el.dataset.cid = 'gorr'; el.dataset.uid = ''; document.body.appendChild(el); el.click(); el.remove(); }""")
            pg.wait_for_selector('.fcab')
            pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(200)
            ruta = pg.locator('ol.ruta').inner_text()
            ok(f'{lang}: el paso previo al Tier-4 dice «{paso}» y ninguno dice 12', paso in ruta and '12' not in ruta.split('Tier-4')[0], ruta[:400])
            ok(f'{lang}: el aviso del Tier-4 explica el cambio', aviso in pg.locator('ol.ruta .req.aviso').inner_text(), pg.locator('ol.ruta .req.aviso').inner_text())
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
