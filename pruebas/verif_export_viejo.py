"""La versión vieja (e6f7999) corriendo desde un worktree sin work/ ni images/: con una capa en
localStorage (origen 127.0.0.1:8731), Ajustes → Exportar mi capa baja el JSON con esa capa."""
import json
from playwright.sync_api import sync_playwright
URL = 'http://127.0.0.1:8731/index.html'
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(); errores = []
    pg.on('pageerror', lambda e: errores.append(str(e)))
    pg.goto(URL); pg.wait_for_selector('.ccard', timeout=30000)
    # una capa como la que tendría guardada: se escribe con la propia app (equipo nuevo)
    pg.click('[data-a="goTeams"]'); pg.click('[data-a="teamOpen"]')
    pg.fill('[data-a="teamName"]', 'Equipo de prueba ★')
    for i in range(2): pg.locator('[data-a="teamToggle"]').nth(i).click()
    pg.click('[data-a="teamSave"]')
    guardada = json.loads(pg.evaluate("localStorage.getItem('mff_user_v1')"))
    pg.reload(); pg.wait_for_selector('.ccard', timeout=30000)
    pg.click('[data-a="goSettings"]')
    with pg.expect_download() as d:
        pg.click('[data-a="exportUser"]')
    ruta = d.value.path(); nombre = d.value.suggested_filename
    capa = json.load(open(ruta, encoding='utf-8'))
    print('archivo:', nombre)
    print('equipos exportados:', [t['name'] for t in capa.get('teams', [])])
    print('igual a lo guardado en localStorage:', capa == guardada)
    print('errores de página:', errores or 'ninguno')
    b.close()
