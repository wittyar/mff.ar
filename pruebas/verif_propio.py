"""Contenido propio (fuentes/propio/, scripts/propio.py; Ezequiel, 13 de octubre de 2026): lo que se carga de las notas del
juego antes de que thanosvibs lo publique. Agatha Harkness (personaje nuevo), los uniformes Wiccan — Young Avengers y
Morgan Le Fay — Classic, sus Tier-4 y el artefacto de Morgan cambiado: en el roster, en la ficha (retrato propio, marca
«propio», skills con su marca, el artefacto sin puntaje) y en la comparativa por potenciador. Lo que se espera sale de
fuentes/propio/, no de app.js."""
import json, os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
PROP = os.path.join(RAIZ, 'fuentes', 'propio')
FILAS = {r['portrait']: r for r in json.load(open(os.path.join(PROP, 'personajes.json'), encoding='utf-8'))['filas']}
SK = {p: json.load(open(os.path.join(PROP, 'skills', p + '.json'), encoding='utf-8')) for p in ('agathaharkness', 'wiccan1')}
D = datos_js('MFF_SEED_CHARACTERS')
por_nombre = {c['name']: c for c in D['MFF_SEED_CHARACTERS']}

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')

        # 1. Agatha en el roster, con su retrato propio
        ag = por_nombre.get('Agatha Harkness')
        ok('1 Agatha Harkness está en los datos', ag is not None and ag['p'] == 'agathaharkness')
        pg.fill('#q', 'Agatha'); pg.wait_for_timeout(300)
        carta = pg.locator(f'.ccard[data-cid="{ag["id"]}"][data-uid=""]')
        src = carta.locator('img').first.get_attribute('src') if carta.locator('img').count() else ''
        ok('1 en el roster, con el retrato de fuentes/propio', carta.count() == 1 and 'images/propio/agathaharkness.png' in (src or ''), src)
        nat = pg.evaluate("(s) => new Promise(r => { const i = new Image(); i.onload = () => r(i.naturalWidth); i.onerror = () => r(0); i.src = s; })", src)
        ok('1 el retrato carga', nat == 256, nat)

        # 2. su ficha: marca propio, sus 10 skills con la marca, el artefacto sin puntaje
        carta.click(); pg.wait_for_selector('.fcab')
        ok('2 la cabecera dice «propio»', pg.locator('.fcab .propio').count() == 1)
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(200)
        n_sk = pg.locator('.skill:not(#sk-artefacto)').count(); n_pr = pg.locator('.skill:not(#sk-artefacto) .propio').count()
        ok(f'2 las {len(SK["agathaharkness"]["slots"])} skills de la nota, cada una marcada', n_sk == len(SK['agathaharkness']['slots']) == n_pr, (n_sk, n_pr))
        txt = pg.locator('.skill', has_text='Witch Duel').first.inner_text() if pg.locator('.skill', has_text='Witch Duel').count() else ''
        ok('2 la Activa 5 con el texto de la nota (resistencia mental −20%, hasta −80%)', '20' in txt and '80' in txt, txt[:200])
        art = pg.locator('#sk-artefacto')
        ok('2 el artefacto nuevo, marcado y sin puntaje de thanosvibs', art.count() == 1 and 'Vishanti' in art.inner_text()
           and art.locator('.propio').count() == 1 and 'sin puntaje' in art.inner_text().lower(), art.inner_text()[:300] if art.count() else '')
        pg.screenshot(path=f'{SALIDA}/propio_agatha_1300.png')

        # 3. Wiccan: el uniforme nuevo y la Tier-4 en todos sus retratos
        wi = por_nombre['Wiccan']
        ok('3 Wiccan es T4 y trae Young Avengers', wi['t'] == 'T4' and any(u['p'] == 'wiccan1' for u in wi['uniforms']))
        pg.click('[data-a="back"]'); pg.fill('#q', 'Wiccan'); pg.wait_for_timeout(300)
        pg.click(f'.ccard[data-cid="{wi["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        uid = next(u['id'] for u in wi['uniforms'] if u['p'] == 'wiccan1')
        pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(300)
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(200)
        nombres = pg.evaluate("[...document.querySelectorAll('.skill .nm')].map(x => x.textContent)")
        ok('3 Young Avengers: las skills de la nota y el striker de Tier-4', any('Staff Smash' in n for n in nombres)
           and any("Demiurge's Potential" in n for n in nombres), nombres)
        pg.select_option('select[data-a="uniformSel"]', 'base'); pg.wait_for_timeout(300)
        nombres = pg.evaluate("[...document.querySelectorAll('.skill .nm')].map(x => x.textContent)")
        ok('3 la base también trae el striker de Tier-4', any("Demiurge's Potential" in n for n in nombres), nombres)

        # 4. la comparativa por potenciador con Agatha
        pg.click('[data-a="back"]'); pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(200)
        for n in ('Agatha Harkness', 'Wiccan'):
            pg.fill('#q', n); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{por_nombre[n]["id"]}"][data-uid=""]'); pg.wait_for_timeout(150)
        pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_timeout(500)
        pg.click('[data-a="cmpVista"][data-v="pot"]'); pg.wait_for_timeout(500)
        fila = pg.locator('.cpb .cpefila[data-e="ignorar_evasion"] .cpecel').first
        ok('4 Agatha en la comparativa: ignorar esquiva de su artefacto y de su definitiva', fila.locator('.slotbadge.art').count() == 1
           and fila.locator('.cpbfu').count() >= 2, fila.inner_text()[:200])
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
