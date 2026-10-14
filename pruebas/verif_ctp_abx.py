"""C.T.P. de Alliance Battle (#25): la guía de armado no los da por personaje sino en su leyenda («ABX: Rage», «Judgement+
can replace Rage»). Alliance Battle tiene su contexto propio (ctp «abx» en modos.json): Modos muestra Rage y, reforjado,
Judgement en su lugar (no los de PvE), y también arriba de sus equipos por día; un equipo guardado con el modo Alliance
Battle muestra lo mismo."""
import json, os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_GUIA_ARMADO', 'MFF_CTPS')
LEY = D['MFF_GUIA_ARMADO']['leyenda']['abx']
CTPS = {c['id']: c for c in D['MFF_CTPS']}
ES = lambda i: CTPS[i]['es']['base'].replace('C.T.P. de ', '')  # como ctpNomCorto, sin mayúscula
ok('la leyenda de la guía: Rage y Judgement reforjado', LEY['c'] == 'rage' and LEY['alt'] == {'c': 'judgement', 'r': True}, LEY)
por_nombre = {c['name']: c for c in D['MFF_SEED_CHARACTERS']}
EQ = ['abomination::base', 'hulk::base', 'red-hulk::base']

DATOS = carpeta_datos()
json.dump({'teams': [{'id': 'eq-ab', 'name': 'Equipo AB', 'members': EQ, 'reason': '', 'modeId': 'alliance-battle',
                      'lider': EQ[0]}]}, open(os.path.join(DATOS, 'capa.json'), 'w', encoding='utf-8'))
srv, url = levantar(DATOS, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')

        # 1. Modos → Alliance Battle
        pg.click('nav.topnav [data-a="goModos"]'); pg.wait_for_selector('.modo')
        pg.click('.modohead[data-id="alliance-battle"]'); pg.wait_for_timeout(300)
        m = pg.locator('#modo-alliance-battle')
        abx = m.locator('.ctpabx')
        txt = ' '.join(abx.all_inner_texts()).lower()
        ok('1 Modos: Rage y Judgement reforjado, arriba de los equipos y en el bloque de C.T.P.', abx.count() == 2
           and all(ES('rage').lower() in x.lower() and ES('judgement').lower() in x.lower() for x in abx.all_inner_texts()), txt[:200])
        ok('1 Modos: no muestra los C.T.P. de PvE', 'Destruction' not in m.inner_text() and ES('competition').lower() not in m.inner_text().lower())
        pg.screenshot(path=f'{SALIDA}/ctp_abx_modos.png')

        # 2. el equipo guardado con el modo Alliance Battle
        pg.click('nav.topnav [data-a="goTeams"]'); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{SALIDA}/ctp_abx_equipos.png')
        card = pg.locator('main .card', has_text='Equipo AB').filter(has=pg.locator('.ga-eq'))
        ok('2 el equipo guardado está', card.count() == 1, pg.locator('main').inner_text()[:300])
        card.locator('.ga-eq summary').click(); pg.wait_for_timeout(150)
        ok('2 el equipo de Alliance Battle: la regla de la guía, no las columnas de PvE', card.locator('.ctpabx').count() == 1
           and 'Alliance Battle' in card.locator('.ga-eq summary').inner_text(), card.locator('.ga-eq').inner_text()[:200])

        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
