"""Mi cuenta, aparte de lo del juego (1.0.52, Ezequiel, 12 de noviembre de 2026: «Separa el armado de mi propia cuenta de lo
demás del juego»). Con una capa armada acá (un equipo, la hoja de ruta de un personaje, atributos marcados, un personaje
creado a mano y una lista propia):
  1. La barra: el grupo del juego y el de Mi cuenta; «Equipos» y «+ Personaje» ya no están en ella; en la ficha y en la
     comparativa sigue marcado «Roster».
  2. Mi cuenta: el resumen (una tarjeta por apartado, con lo que hay) y la sub-barra, que sigue en Equipos y en el editor;
     cada tarjeta lleva a su apartado.
  3. Tu progreso, Personajes propios, Atributos marcados y Mi capa muestran lo de la capa; «Ver en su ficha» abre la ficha
     en su pestaña «Mi cuenta» y «Atrás» vuelve al apartado.
  4. Ajustes ya no tiene la capa (exportar, importar, borrar): lleva a Mi capa.
  5. La pestaña «Mi cuenta» de la ficha: tus equipos, tu progreso, los atributos marcados y tus cambios a sus datos.
  6. Un personaje creado a mano: su ficha abre en todas las pestañas (antes de la 1.0.52 no abría) y se compara con uno del
     juego en todos los métodos.
  7. Tier lists propias, desde Mi cuenta: abre las tier lists para editar, en la lista propia.
  8. En inglés. Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js, ir_a_equipos
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED', 'MFF_SEED_CHARACTERS', 'MFF_GUIA')
SEED, PJ = D['MFF_SEED'], {c['id']: c for c in D['MFF_SEED_CHARACTERS']}
PASOS = D['MFF_GUIA']['progresion']['pasos']
WONG, THOR = PJ['wong'], PJ['thor']
MIO = dict(id='mio-prueba', name='Personaje de prueba', c=SEED['CLASSES'][0], f=SEED['FACTIONS'][0], r=[], t='T2',
           ins=SEED['INSTINCTS'][0], race=SEED['RACES'][0], gender=SEED['GENDERS'][0], origin='Original MFF',
           abilities=[], tuc=[], stats={}, striker=4, wba='', trans=False, new=False, uniforms=[])
CAPA = {
    'teams': [{'id': 'eq-1', 'name': 'Equipo de la cuenta', 'modeId': '', 'reason': '', 'members': ['wong::base', 'thor::base', 'hulk::base'], 'lider': 'wong::base'}],
    'ruta': {'wong': PASOS[2]['id']},
    'marcas': {WONG['p'] + '::Active 1': {'gb': True}},
    'charNew': [MIO],
    'lists': [{'id': 'mia-1', 'name': 'Mi lista', 'kind': 'personajes', 'rows': [{'id': 'f-1', 'label': 'S'}, {'id': 'f-2', 'label': 'A'}]}],
    'assign': {'mia-1': {'wong::base': ['f-1']}},
}
DIR = carpeta_datos()
json.dump(CAPA, open(os.path.join(DIR, 'capa.json'), 'w', encoding='utf-8'), ensure_ascii=False)
srv, url = levantar(DIR, origen_local())


def clic(pg, a, **d):
    """Un clic en una acción de la app (un botón suelto con su data-a), para lo que no tiene un botón a mano."""
    pg.evaluate("""([a, d]) => { const el = document.createElement('button'); el.dataset.a = a; Object.assign(el.dataset, d);
        document.body.appendChild(el); el.click(); el.remove(); }""", [a, d])
    pg.wait_for_timeout(250)


try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' and '404' not in m.text else None)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(500)
        marcado = lambda: pg.locator('nav.topnav .navlink.on').all_inner_texts()
        # La sub-barra: [[apartado, cuántos]] y el apartado marcado (sin su cuenta).
        SUB = "[...document.querySelectorAll('.cutabs .cutab')].map(b => [b.firstChild.textContent.trim(), b.querySelector('.cun') ? b.querySelector('.cun').textContent : null, b.classList.contains('on')])"
        sub = lambda: next((x[0] for x in pg.evaluate(SUB) if x[2]), None)

        # 1. la barra
        juego = pg.locator('nav.topnav .navgrupo:not(.cuenta) .navlink').all_inner_texts()
        ok('1 barra: el grupo del juego (Roster, Tier lists, Modos, Glosario, Histórico)', juego == ['Roster', 'Tier lists', 'Modos', 'Glosario', 'Histórico'], juego)
        ok('1 barra: el grupo de Mi cuenta, con el botón de la mesa; sin «Equipos» ni «+ Personaje»',
           pg.locator('nav.topnav .navgrupo.cuenta .navlink').all_inner_texts() == ['Mi cuenta']
           and pg.locator('nav.topnav .navgrupo.cuenta [data-a="mesaToggle"]').count() == 1
           and pg.locator('nav.topnav [data-a="goTeams"], nav.topnav [data-a="goEditor"]').count() == 0)
        ok('1 roster: marcado «Roster» y sin nada de la cuenta en la pantalla', marcado() == ['Roster'] and pg.locator('.cucab, aside.mesa').count() == 0, marcado())
        clic(pg, 'open', cid='wong'); pg.wait_for_selector('.fcab')
        ok('1 ficha: sigue marcado «Roster»', marcado() == ['Roster'], marcado())

        # 2. Mi cuenta: el resumen y la sub-barra
        pg.click('nav.topnav [data-a="goCuenta"]'); pg.wait_for_selector('.cuhub')
        tabs = [x[0] for x in pg.evaluate(SUB)]
        ok('2 Mi cuenta: marcada en la barra, con su sub-barra', marcado() == ['Mi cuenta'] and sub() == 'Resumen'
           and tabs == ['Resumen', 'Equipos', 'Progreso', 'Personajes propios', 'Atributos marcados', 'Mi capa'], (marcado(), tabs))
        cuentas = {x[0]: x[1] for x in pg.evaluate(SUB) if x[1]}
        ok('2 la sub-barra dice cuánto hay en cada apartado', cuentas == {'Equipos': '1', 'Progreso': '1', 'Personajes propios': '1', 'Atributos marcados': '1'}, cuentas)
        tiles = pg.locator('.cuhub .cutile')
        valores = [tiles.nth(i).locator('.v').inner_text() if tiles.nth(i).locator('.v').count() else None for i in range(tiles.count())]
        ok('2 el resumen: una tarjeta por apartado, con lo que hay (equipos, progreso, propios, marcas, listas) y la capa',
           tiles.count() == 6 and valores == ['1', '1', '1', '1', '1', None], valores)
        destinos = []
        for i, espera in enumerate(('Equipos', 'Progreso', 'Personajes propios', 'Atributos marcados', None, 'Mi capa')):
            pg.click('nav.topnav [data-a="goCuenta"]'); pg.wait_for_selector('.cuhub')
            pg.locator('.cuhub .cutile').nth(i).click(); pg.wait_for_timeout(300)
            destinos.append((espera, sub(), marcado()))
        ok('2 cada tarjeta lleva a su apartado (la de las listas, a Tier lists)',
           all(s == e and m == ['Mi cuenta'] for e, s, m in destinos if e) and destinos[4][1:] == (None, ['Tier lists']), destinos)

        # 7. Tier lists propias desde Mi cuenta: para editar, en la propia
        pg.click('nav.topnav [data-a="goCuenta"]'); pg.locator('.cuhub .cutile').nth(4).click(); pg.wait_for_timeout(300)
        ok('7 «Tier lists propias»: abre las tier lists editando, en la lista propia', pg.locator('.tledit').count() == 1
           and pg.locator('.tlbar .chip.on').inner_text() == 'Mi lista' and pg.locator('.tlchip[draggable="true"]').count() == 1
           and pg.locator('[data-a="tlEditar"]').get_attribute('aria-pressed') == 'true', pg.locator('.tlbar .chip.on').all_inner_texts())
        pg.click('[data-a="tlEditar"]'); pg.wait_for_timeout(200)

        # 3. los apartados
        ir_a_equipos(pg); pg.wait_for_timeout(300)
        ok('3 Equipos: es de Mi cuenta (sub-barra y barra) y tiene la mesa y el equipo de la capa', sub() == 'Equipos' and marcado() == ['Mi cuenta']
           and pg.locator('aside.mesa .mslot').count() == 3 and pg.locator('.card', has_text='Equipo de la cuenta').count() == 1)
        pg.click('.cutabs [data-a="cuentaTab"][data-v="progreso"]'); pg.wait_for_timeout(300)
        fila = pg.locator('.cutabla tbody tr')
        ok('3 Tu progreso: Wong, en el paso 3 de la hoja de ruta', fila.count() == 1 and 'Wong' in fila.inner_text()
           and f'Paso 3 de {len(PASOS)}' in fila.inner_text() and PASOS[2]['es'] in fila.inner_text(), fila.all_inner_texts())
        fila.locator('[data-a="abrirEn"]').click(); pg.wait_for_selector('.fcab')
        ok('3 «Ver en su ficha»: la ficha de Wong en su pestaña «Mi cuenta»', pg.locator('.fcab h1').inner_text() == 'Wong'
           and pg.locator('.ftab.mia.on').count() == 1 and marcado() == ['Roster'])

        # 5. la pestaña «Mi cuenta» de la ficha
        titulos = pg.locator('#fcuerpo > .section > h3').all_inner_texts()
        ok('5 ficha › Mi cuenta: tus equipos, tu progreso, los atributos que marcaste y tus cambios a sus datos',
           [x.split('\n')[0].strip().lower() for x in titulos] == ['en tus equipos', 'tu progreso', 'atributos que marcaste', 'tus cambios a sus datos'], titulos)
        ok('5 su equipo, su paso de la ruta marcado y el atributo que se le marcó', pg.locator('#fcuerpo .card', has_text='Equipo de la cuenta').count() == 1
           and pg.locator('ol.ruta li.hecho').count() == 3 and 'rotura de guardia' in pg.locator('#fcuerpo > .section').nth(2).inner_text().lower(),
           pg.locator('#fcuerpo > .section').nth(2).inner_text())
        ok('5 «Editar» y «Marcar atributos» están acá, y «Poner en la mesa» también', pg.locator('#fcuerpo [data-a="edit"]').count() == 1
           and pg.locator('#fcuerpo [data-a="marcarModo"]').count() == 1 and pg.locator('#fcuerpo [data-a="mesaPoner"]').count() == 1)
        atras = pg.locator('[data-a="atras"]')
        ok('3 la ficha tiene «←» al apartado del que se vino', atras.count() == 1 and 'Mi cuenta' in atras.inner_text(), atras.all_inner_texts())
        atras.click(); pg.wait_for_selector('.cutabla')
        ok('3 «Atrás» vuelve a Mi cuenta › Progreso', sub() == 'Progreso' and marcado() == ['Mi cuenta'], (sub(), marcado()))

        pg.click('.cutabs [data-a="cuentaTab"][data-v="propios"]'); pg.wait_for_timeout(300)
        ok('3 Personajes propios: el creado a mano, con «Editar», y «+ Personaje»', 'Personaje de prueba' in pg.locator('.cutabla').inner_text()
           and 'creado' in pg.locator('.cutabla').inner_text().lower() and pg.locator('main [data-a="goEditor"]').count() == 1, pg.locator('.cutabla').inner_text())
        pg.click('main [data-a="goEditor"]'); pg.wait_for_timeout(300)
        ok('3 «+ Personaje»: el editor, dentro de Mi cuenta › Personajes propios; «← Anterior» es el paso de antes', sub() == 'Personajes propios'
           and marcado() == ['Mi cuenta'] and pg.locator('[data-a="edPrev"]').inner_text() == '← Anterior', (sub(), pg.locator('[data-a="edPrev"]').all_inner_texts()))
        pg.click('.cutabs [data-a="cuentaTab"][data-v="marcas"]'); pg.wait_for_timeout(300)
        ok('3 Atributos marcados: Wong, Activa 1, Rotura de guardia', all(x in pg.locator('.cutabla').inner_text().lower() for x in ('wong', 'activa 1', 'rotura de guardia')),
           pg.locator('.cutabla').inner_text())
        pg.click('.cutabs [data-a="cuentaTab"][data-v="capa"]'); pg.wait_for_timeout(300)
        stats = dict(zip(pg.locator('.statgrid .stat .k').all_inner_texts(), pg.locator('.statgrid .stat .v').all_inner_texts()))
        ok('3 Mi capa: lo que hay y exportar, importar y borrar', pg.locator('[data-a="exportUser"]').count() == 1 and pg.locator('[data-a="importUser"]').count() == 1
           and pg.locator('[data-a="resetUser"]').count() == 1 and list(stats.values())[:4] == ['1', '1', '1', '0'], stats)   # la ubicación en la lista propia no es un cambio sobre una importada
        with pg.expect_download() as dl:
            pg.click('[data-a="exportUser"]')
        exportada = json.load(open(dl.value.path(), encoding='utf-8'))
        ok('3 Mi capa: «Exportar» baja la capa (el equipo, la ruta y el personaje propio)', [x['name'] for x in exportada['teams']] == ['Equipo de la cuenta']
           and exportada['ruta'] == CAPA['ruta'] and [c['id'] for c in exportada['charNew']] == ['mio-prueba'], list(exportada))

        # 4. Ajustes
        pg.click('nav.topnav [data-a="goSettings"]'); pg.wait_for_selector('#seccion-actualizaciones')
        ok('4 Ajustes: sin exportar, importar ni borrar la capa; lleva a Mi capa', pg.locator('[data-a="exportUser"], [data-a="importUser"], [data-a="resetUser"]').count() == 0
           and pg.locator('main [data-a="cuentaTab"][data-v="capa"]').count() == 1 and pg.locator('main [data-a="exportCsv"]').count() == 1)
        pg.click('main [data-a="cuentaTab"][data-v="capa"]'); pg.wait_for_timeout(300)
        ok('4 el botón de Ajustes abre Mi cuenta › Mi capa', sub() == 'Mi capa' and marcado() == ['Mi cuenta'])

        # 6. el personaje creado a mano
        clic(pg, 'open', cid='mio-prueba'); pg.wait_for_timeout(500)
        ok('6 la ficha del personaje creado a mano abre', pg.locator('.fcab h1').count() == 1 and pg.locator('.fcab h1').inner_text() == 'Personaje de prueba', errores[-2:])
        vistas = {}
        for tb in ('resumen', 'skills', 'armado', 'equipos', 'fuentes', 'cuenta'):
            n = len(errores); pg.click(f'[data-a="fichaTab"][data-v="{tb}"]'); pg.wait_for_timeout(400)
            vistas[tb] = pg.locator('.ftab.on').get_attribute('data-v') == tb and len(errores) == n and pg.locator('#fcuerpo').inner_text().strip() != ''
        ok('6 y en todas sus pestañas, sin errores', all(vistas.values()), vistas)
        ok('6 su pestaña «Mi cuenta» dice que lo creaste', 'creaste' in pg.locator('#fcuerpo > .section').last.inner_text().lower(), pg.locator('#fcuerpo > .section').last.inner_text())
        clic(pg, 'back'); clic(pg, 'pick', cid='mio-prueba', uid=''); clic(pg, 'pick', cid='thor', uid='')
        pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_timeout(400)
        ok('6 comparado con Thor: abre la comparativa, «Roster» marcado', pg.locator('.cmet').count() == 1 and marcado() == ['Roster'], marcado())
        metodos = {}
        for m in ('kit', 'efecto', 'pot', 'pvp', 'listas', 'ficha'):
            n = len(errores); pg.click(f'[data-a="cmpVista"][data-v="{m}"]'); pg.wait_for_timeout(300)
            metodos[m] = len(errores) == n and pg.locator(f'.cmetb.on[data-v="{m}"]').count() == 1
        ok('6 y los seis métodos, sin errores', all(metodos.values()), metodos)
        pg.click('[data-a="cmpVista"][data-v="ficha"]'); pg.wait_for_timeout(200)
        cargas = pg.evaluate("[...document.querySelectorAll('table.cmpt tbody tr')].filter(tr => ['Ult', 'Striker'].includes(tr.querySelector('th').textContent)).map(tr => tr.querySelector('td').textContent)")
        ok('6 sin datos de carga, la ficha de la comparativa dice «—» en la de ult y en la de striker, no 0%', cargas.count('—') == 2 and '0%' not in cargas, cargas)

        # 8. inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.click('nav.topnav [data-a="goCuenta"]'); pg.wait_for_selector('.cuhub')
        tabs_en = [x[0] for x in pg.evaluate(SUB)]
        ok('8 inglés: la barra y la sub-barra', pg.locator('nav.topnav .navgrupo.cuenta .navlink').inner_text() == 'My account'
           and tabs_en == ['Overview', 'Teams', 'Progress', 'Own characters', 'Marked attributes', 'My layer'], tabs_en)
        resto = [x for x in ('Progreso', 'Personajes propios', 'Mi capa', 'Equipos', 'Tier lists propias') if x in pg.locator('main').inner_text()]
        ok('8 inglés: el resumen sin restos en castellano', not resto, resto)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)

        ok('sin errores de página ni de consola', not errores, errores[:4])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
