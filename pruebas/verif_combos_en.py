import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
ok = Chequeo()
D = carpeta_datos()
json.dump({'prefs': {'lang': 'en'}, 'favoritos': [{'id': 'f1', 'members': ['annihilus::base', 'enchantress::enchantress-10200041', 'yondu::yondu-10300046']}]},
          open(os.path.join(D, 'capa.json'), 'w', encoding='utf-8'))
srv, url = levantar(D, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.fill('#q', 'Annihilus'); pg.wait_for_timeout(300)
        pg.click('.ccard[data-cid="annihilus"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
        tx = pg.locator('#combos').inner_text()
        esperados = ['COMBINATIONS OF 3 WITH IT', 'Sort by', 'With', 'Without', 'combinations', 'Leader:', 'pts for it', 'for the team', 'Take to the desk', 'Why']
        ok('inglés: la lista', all(e.lower() in tx.lower() for e in esperados), [e for e in esperados if e.lower() not in tx.lower()])
        espanol = [w for w in ('Ordenar', 'combinaciones', 'Líder', 'para él', 'del equipo', 'Armar para') if w in tx]
        ok('inglés: sin restos en castellano en la lista', not espanol, espanol)
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        tx2 = pg.locator('main').inner_text() if pg.locator('main').count() else pg.locator('body').inner_text()
        ok('inglés: Equipos', 'FAVORITES' in tx2.upper() and "YOUR ACCOUNT'S TEAMS" in tx2.upper() and 'Leader:' in tx2, tx2[:200].replace('\n', ' | '))
        ok('sin errores de página', not errores, errores[:2])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
