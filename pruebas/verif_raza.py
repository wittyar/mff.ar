"""La raza por uniforme: Ms. Marvel es inhumana en la base y humana con los uniformes del
MCU. La ficha y el filtro de raza usan la del uniforme."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
C = datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS']
ch = next(c for c in C if c['name'] == 'Ms. Marvel (Kamala Khan)')
uid = {u['name']: u['id'] for u in ch['uniforms']}
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.fill('#q', 'Kamala'); pg.wait_for_timeout(400)
        pg.click(f'.ccard[data-cid="{ch["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab .ftab'); pg.wait_for_selector('.statgrid')

        def raza():
            return pg.evaluate("""() => [...document.querySelectorAll('.statgrid > *')].map(x => x.innerText.replace(/\\s+/g, ' ').trim())
                                          .find(t => /^raza/i.test(t)) || ''""")
        r_base = raza()
        pg.select_option('select[data-a="uniformSel"]', uid["Marvel Studios' Ms. Marvel"]); r_mcu = raza()
        pg.select_option('select[data-a="uniformSel"]', uid["Karachi Costume"]); r_kar = raza()
        ok('ficha: base inhumana', r_base.endswith('Inhumano'), r_base)
        ok('ficha: uniforme del MCU humano', r_mcu.endswith('Humano') and 'Inhumano' not in r_mcu, r_mcu)
        ok('ficha: Karachi Costume inhumana', r_kar.endswith('Inhumano'), r_kar)
        # filtro de raza en el roster (todas las variantes)
        pg.click('[data-a="back"]'); pg.wait_for_selector('.ccard')
        if not pg.locator('[data-a="filter"][data-cat="race"]').count():
            pg.click('[data-a="toggleFilters"]')
        pg.click('[data-a="filter"][data-cat="race"][data-v="Inhumano"]'); pg.wait_for_timeout(400)
        subs = pg.evaluate(f"""() => [...document.querySelectorAll('.ccard[data-cid="{ch['id']}"]')]
                                     .map(c => c.querySelector('.nm').innerText)""")
        ok('filtro Inhumano: sin los dos uniformes del MCU', subs and "Marvel Studios' Ms. Marvel" not in subs
           and "Marvel Studios' The Marvels" not in subs and 'Karachi Costume' in subs, subs)
        ok('sin errores de página', not errores, errores[:2])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
