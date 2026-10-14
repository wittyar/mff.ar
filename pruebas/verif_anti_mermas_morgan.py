"""El anti-mermas del efecto de uniforme de Morgan le Fay (Ezequiel, 14 de octubre de 2026: «en los 2 uniformes de morgana
no estás incluyendo el anti mermas... y pusiste cualquier cosa»). Los dos uniformes, Fallen Soul y Classic, dicen en el
juego: a los aliados Universales, todos los ataques y el daño a jefes, siempre; y al estar mermado, elimina todas las mermas
(10 s), con recarga de 18 s.
- Fallen Soul: la API publicaba un «Obtiene el siguiente efecto» sin el anti-mermas; va lo del juego (skills_juego.json,
  la ficha de la nota del 18 de octubre de 2022), marcado «según el juego».
- Classic: la recarga de 18 s es del anti-mermas, no de los ataques (liderazgos.partes_soporte).
- «Qué hace»: lo que se activa (al estar mermado, al morir) no es «Siempre activo»: dice cuándo y su recarga."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
M = next(c for c in datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS'] if c['name'] == 'Morgan le Fay')
UNI = {u['name']: u['id'] for u in M['uniforms']}

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.fill('#q', 'Morgan'); pg.wait_for_timeout(300)
        pg.click(f'.ccard[data-cid="{M["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        for nombre in ('Fallen Soul', 'Classic'):
            pg.select_option('select[data-a="uniformSel"]', UNI[nombre]); pg.wait_for_timeout(400)
            pg.click('[data-a="fichaTab"][data-v="resumen"]'); pg.wait_for_timeout(300)
            main = pg.locator('main').inner_text()
            ok(f'{nombre}: «Qué le da al equipo» con el anti-mermas, al estar mermado, recarga 18 s, dura 10 s',
               'Elimina todas las mermas (al estar mermado, recarga 18 s, dura 10 s)' in main)
            ok(f'{nombre}: los ataques que da siempre, sin recarga', '(recarga 18 s)' not in main.split('EFECTO DE UNIFORME')[1].split('EFECTO DE UNIFORME (SECUNDARIO)')[0],
               main.split('EFECTO DE UNIFORME')[1][:160])
            fila = pg.locator('.qhfila', has_text='Le saca todas las mermas').first
            txt = fila.inner_text() if fila.count() else ''
            ok(f'{nombre}: «Qué hace»: el anti-mermas se activa al estar mermado (no «Siempre activo»)',
               'al estar mermado' in txt and 'recarga 18 s' in txt and 'Siempre activo' not in txt, txt.replace('\n', ' '))
            pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(300)
            uni = pg.locator('.skill', has_text='PASIVA DE UNIFORME').first.inner_text()
            ok(f'{nombre}: la skill de uniforme con el anti-mermas y sin «Obtiene el siguiente efecto»',
               'Elimina todas las mermas' in uni and 'Obtiene el siguiente efecto' not in uni, uni.replace('\n', ' ')[:300])
        pg.select_option('select[data-a="uniformSel"]', UNI['Fallen Soul']); pg.wait_for_timeout(300)
        ok('Fallen Soul: la skill de uniforme dice «según el juego»',
           pg.locator('.skill', has_text='PASIVA DE UNIFORME').first.locator('.skjuego').count() == 1)
        pg.screenshot(path=f'{SALIDA}/anti_mermas_morgan.png')
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
