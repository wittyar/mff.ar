"""Género por uniforme: los 11 uniformes que cambian el género muestran el suyo en la ficha;
la base y un uniforme que no lo cambia, el de la base. También en inglés."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright
ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_VOCAB_EN')
casos = []
for c in D['MFF_SEED_CHARACTERS']:
    for u in c['uniforms']:
        if 'gender' in u:
            casos.append((c, u['id'], u['gender']))
    if any('gender' in u for u in c['uniforms']):
        casos.append((c, '', c['gender']))
        otro = next((u for u in c['uniforms'] if 'gender' not in u), None)
        if otro: casos.append((c, otro['id'], c['gender']))
print('casos:', len(casos))
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        def genero(c, uid):
            pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
            pg.fill('#q', c['name']); pg.wait_for_timeout(150)
            pg.click(f'.ccard[data-cid="{c["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
            if uid: pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(100)
            return pg.locator('.statgrid .stat', has=pg.locator('.k', has_text='Género' if not ingles else 'Gender')).locator('.v').text_content().strip()
        ingles = False
        malos = [(c['name'], uid, g, genero(c, uid)) for c, uid, g in casos]
        malos = [m for m in malos if m[2] != m[3]]
        ok('ficha: el género de cada uniforme (y de la base)', not malos, malos[:4])
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(250); ingles = True
        c, uid, g = casos[0]
        en = genero(c, uid)
        ok('inglés', en == D['MFF_VOCAB_EN'][g], (en, g))
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
