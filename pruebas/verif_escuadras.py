"""Alliance Conquest como dos escuadras de 3: la etiqueta en Modos y el tope del armador.
Carril de consistencia: los topes avisan en vez de descartar en silencio.
- Armador: con el equipo lleno, tocar otro no lo suma (antes salía el primero sin decirlo) y lo dice; un modo
  más chico que el equipo no le saca a nadie: dice cuántos sobran y no guarda hasta que se quiten.
- Comparar: con 4 elegidas, la quinta no se suma (antes salía la más vieja) y la barra de abajo lo dice; quitando
  una, se suma y el aviso se va. Sin diálogos del navegador."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
ok = Chequeo()
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores, dialogos = [], []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('dialog', lambda d: (dialogos.append(d.message), d.dismiss()))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.click('[data-a="goModos"]'); pg.wait_for_selector('.modo')
        cab = pg.locator('.modohead', has_text='Conquista de alianza').inner_text()
        ok('Modos: Alliance Conquest dice equipo de 3, dos escuadras', '3 × 2' in cab, cab.replace('\n', ' '))
        otro = pg.locator('.modohead', has_text='Batalla de otro mundo').inner_text()
        ok('Modos: Otherworld Battle sigue en 5', ' 5' in otro and '×' not in otro, otro.replace('\n', ' '))

        # 3. comparar: la quinta no se suma y se dice
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('.ccard')
        pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(150)
        cards = pg.locator('.ccard')
        elegidas = [f"{cards.nth(i).get_attribute('data-cid')}::{cards.nth(i).get_attribute('data-uid') or 'base'}" for i in range(5)]
        c5 = cards.nth(4)
        nombre5 = (c5.locator('.of').inner_text() + ' — ' if c5.locator('.of').count() else '') + c5.locator('.nm').inner_text()
        for i in range(5): cards.nth(i).click(); pg.wait_for_timeout(120)
        sel = pg.evaluate("[...document.querySelectorAll('.ccard.sel')].map(c => c.dataset.cid + '::' + (c.dataset.uid || 'base'))")
        boton = pg.locator('[data-a="pickMode"]').inner_text()
        aviso = pg.locator('.mesa .avisoeq').all_inner_texts()
        ok('comparar: con 4 elegidas la quinta no se suma (no sale la primera)', sel == elegidas[:4] and boton == 'Comparando (4/4)', (sel, boton))
        ok('comparar: la mesa dice por qué', aviso == [f'⚠ Ya hay 4 para comparar: quitá una para sumar {nombre5}.']
           and pg.locator('[data-a="goCompare"]').is_visible(), aviso)
        cards.nth(0).click(); pg.wait_for_timeout(120)
        ok('comparar: quitando una, el aviso se va', pg.locator('.mesa .avisoeq').count() == 0 and pg.locator('.ccard.sel').count() == 3)
        cards.nth(4).click(); pg.wait_for_timeout(120)
        sel = pg.evaluate("[...document.querySelectorAll('.ccard.sel')].map(c => c.dataset.cid + '::' + (c.dataset.uid || 'base'))")
        ok('comparar: y la que no entraba ahora entra', sorted(sel) == sorted(elegidas[1:5]), sel)
        ok('sin diálogos del navegador', not dialogos, dialogos)
        ok('sin errores de página', not errores, errores[:2])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
