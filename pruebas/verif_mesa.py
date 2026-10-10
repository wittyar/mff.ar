"""Mesa de trabajo (1.0.25): tres paneles y la mesa, contra un modelo escrito aparte con data.js.
- Ficha: lista a la izquierda (el roster filtrado, el actual marcado), mesa a la derecha; en las otras secciones, sin
  lista y con la mesa.
- Poner en la mesa: desde la ficha y desde el «+» de la lista; el mismo personaje con otro uniforme reemplaza (y lo
  dice); lleno, no suma y lo dice; un modo más chico no le saca a nadie: dice cuántos sobran y no guarda.
- Líder: el primero; «↑» lo cambia.
- Alliance Battle: día y dificultad, la restricción marcada por integrante según el modelo (clase, bando, género o raza).
- Bonos activos: los de data.js con todos sus integrantes en la mesa.
- Guardar: va a Mis equipos (orden canónico), dice que se guardó; otra vez, dice que ya está; sin avisos de repetido
  por el mismo equipo. «Llevar a la mesa» de una tarjeta reemplaza la mesa con el líder primero.
- La mesa queda en la capa: sigue al recargar.
- Líder declarado: el equipo guardado lleva el primero de la mesa como líder y su tarjeta lo usa; se cambia en la tarjeta;
  los mismos con otro líder son otro equipo; un equipo de antes (sin líder) recibe uno de sus integrantes y Equipos lo dice.
- Comparar: desde la ficha sin salir de ella; con 4, la quinta no entra y se dice; el botón lleva a la comparación.
- Equipos ya no tiene el armador viejo.
- Ventana angosta: pestañas Lista / Ver / Mesa, un panel a la vez.
- Inglés: la mesa en inglés. Sin errores de página ni diálogos."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED', 'MFF_SEED_CHARACTERS', 'MFF_BONOS', 'MFF_ABX')
SEED = D['MFF_SEED']
CH = {c['id']: c for c in D['MFF_SEED_CHARACTERS']}


def var(key):
    cid, uid = key.split('::')
    c = CH[cid]
    u = next((x for x in c['uniforms'] if x['id'] == uid), None) if uid != 'base' else None
    g = lambda k, kc=None: (u or {}).get(k) or c[kc or k]
    return {'c': g('c'), 'f': g('f'), 'gender': g('gender'), 'race': g('race')}


def cumple(key, x):
    v = var(key)
    for campo, vocab in (('c', 'CLASSES'), ('f', 'FACTIONS'), ('gender', 'GENDERS'), ('race', 'RACES')):
        if x in SEED[vocab]:
            return v[campo] == x
    raise ValueError(x)


ABO, ABO_I = 'abomination::base', 'abomination::abomination-10100228'
HULK, RHULK = 'hulk::hulk-10800002', 'red-hulk::red-hulk-10300025'
import json, os
DATOS = carpeta_datos()
VIEJO = sorted([ABO, HULK, RHULK])
json.dump({'teams': [{'id': 'eq-viejo', 'name': 'Equipo viejo', 'members': VIEJO, 'reason': '', 'modeId': ''}]},
          open(os.path.join(DATOS, 'capa.json'), 'w', encoding='utf-8'))
capa = lambda: json.load(open(os.path.join(DATOS, 'capa.json'), encoding='utf-8'))
srv, url = levantar(DATOS, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1440, 'height': 900}); errores, dialogos = [], []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append(m.text) if m.type == 'error' else None)
        pg.on('dialog', lambda d: (dialogos.append(d.message), d.dismiss()))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.wait_for_timeout(800)
        viejo = next(x for x in capa()['teams'] if x['id'] == 'eq-viejo')
        ok('equipo de antes: se le declara un líder de sus integrantes y se guarda', viejo.get('lider') in VIEJO, viejo.get('lider'))
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        ok('equipo de antes: Equipos dice a cuál se le declaró', 'Equipo viejo' in ' '.join(pg.locator('main .avisoeq').all_inner_texts()),
           pg.locator('main .avisoeq').all_inner_texts())
        tarjeta_vieja = pg.locator('.card', has_text='Equipo viejo')
        ok('equipo de antes: la tarjeta muestra ese líder', tarjeta_vieja.locator('[data-a="teamLider"]').input_value() == viejo['lider']
           and tarjeta_vieja.locator('.eqfoto.lider').get_attribute('data-cid') == viejo['lider'].split('::')[0])
        pg.click('[data-a="teamRemove"][data-id="eq-viejo"]'); pg.wait_for_timeout(300)
        pg.evaluate("document.querySelector('nav.topnav .navlink').click()"); pg.wait_for_selector('.ccard')
        miembros = lambda: pg.evaluate("[...document.querySelectorAll('.mesa .mslot:not(.libre) .msfoto')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base'))")
        avisos = lambda: pg.locator('.mesa .avisoeq').all_inner_texts()

        ok('roster: sin lista, con la mesa', pg.locator('.plista').count() == 0 and pg.locator('aside.mesa').count() == 1)
        ok('roster: la barra de comparar de abajo ya no está', pg.locator('[data-a="goCompare"]').count() == 0)
        pg.fill('#q', 'Abomination'); pg.wait_for_timeout(300)
        n_roster = pg.locator('.ccard').count()
        pg.locator('main [data-a="open"]').first.click(); pg.wait_for_selector('.fcab')
        items = pg.locator('.plista .plit')
        cab = pg.locator('.plista .panelcab').inner_text()
        ok('ficha: lista con el roster filtrado', items.count() == n_roster and f'{n_roster} DE 888' in cab.upper(), (items.count(), n_roster, cab))
        ok('ficha: el actual marcado', pg.locator('.plista .plit.on [data-a="fichaVecina"]').get_attribute('data-uid') == '')
        pg.locator('.plista .plit').nth(1).locator('[data-a="fichaVecina"]').click(); pg.wait_for_timeout(300)
        ok('lista: tocar otro abre su ficha', pg.locator('select[data-a="uniformSel"]').input_value() == 'abomination-10100228')
        pg.locator('.plista .plit').nth(0).locator('[data-a="fichaVecina"]').click(); pg.wait_for_timeout(300)

        # poner en la mesa
        pg.click('main [data-a="mesaPoner"]'); pg.wait_for_timeout(200)
        ok('poner: desde la ficha', miembros() == [ABO], miembros())
        ok('poner: el botón pasa a «En la mesa»', pg.locator('main [data-a="mesaPoner"]').is_disabled())
        pg.click(f'.plista [data-a="mesaPoner"][data-key="{ABO_I}"]'); pg.wait_for_timeout(200)
        ok('poner: el mismo personaje con otro uniforme reemplaza y lo dice',
           miembros() == [ABO_I] and avisos() == ['⚠ Abomination ya estaba en la mesa con otro uniforme: queda con este.'], (miembros(), avisos()))
        pg.evaluate("document.querySelector('nav.topnav .navlink').click()"); pg.wait_for_selector('.ccard')
        pg.fill('#q', ''); pg.wait_for_timeout(300)
        pg.locator('main [data-a="open"]').first.click(); pg.wait_for_selector('.plista')
        for k in (HULK, RHULK):
            pg.click(f'.plista [data-a="mesaPoner"][data-key="{k}"]'); pg.wait_for_timeout(150)
        ok('poner: desde el «+» de la lista', miembros() == [ABO_I, HULK, RHULK], miembros())
        cuarto = pg.evaluate("[...document.querySelectorAll('.plista [data-a=\"mesaPoner\"]')].map(x => x.dataset.key).find(k => !['abomination','hulk','red-hulk'].includes(k.split('::')[0]))")
        pg.click(f'.plista [data-a="mesaPoner"][data-key="{cuarto}"]'); pg.wait_for_timeout(150)
        ok('poner: lleno, no suma y lo dice', miembros() == [ABO_I, HULK, RHULK] and len(avisos()) == 1 and 'ya tiene 3 de 3' in avisos()[0], avisos())
        ok('líder: el primero', pg.locator('.mesa .mslot.lider .msfoto').get_attribute('data-cid') == 'abomination')
        pg.locator('.mesa .mslot').nth(2).locator('[data-a="mesaLider"]').click(); pg.wait_for_timeout(150)
        ok('líder: «↑» lo pone primero', miembros() == [RHULK, ABO_I, HULK], miembros())

        # Alliance Battle: restricción
        pg.select_option('[data-a="mesaModo"]', 'alliance-battle'); pg.wait_for_timeout(150)
        for dia, dif in ((6, 'Legend'), (1, 'Extreme'), (4, 'Legend')):
            pg.select_option('[data-a="mesaDia"]', str(dia)); pg.wait_for_timeout(120)
            pg.select_option('[data-a="mesaDif"]', dif); pg.wait_for_timeout(120)
            r = next(x for x in D['MFF_ABX']['restricciones'] if x['d'] == dia and x['m'] == dif)['r']
            esperado = [[('✓' if cumple(k, x) else '✗') for k in miembros()] for x in r]
            visto = pg.evaluate("[...document.querySelectorAll('.msrestr tbody tr')].map(tr => [...tr.querySelectorAll('td.si,td.no')].map(td => td.textContent))")
            ok(f'restricción del día {dia} {dif}: según clase, bando, género o raza', visto == esperado, (r, visto, esperado))

        # bonos activos
        cids = {k.split('::')[0] for k in miembros()}
        esperados = sorted(bn['n'] for bn in D['MFF_BONOS'] if set(bn['m']) <= cids)
        vistos = sorted(pg.locator('.msbono b').nth(i).inner_text() for i in range(pg.locator('.msbono').count()))
        ok('bonos activos: los de data.js con todos sus integrantes', vistos == esperados, (vistos, esperados))
        ok('lo que le llega: uno por integrante', pg.locator('.msrecibe').count() == 3)

        # guardar
        pg.fill('[data-a="mesaNombre"]', 'Prueba mesa'); pg.wait_for_timeout(100)
        pg.click('[data-a="mesaGuardar"]'); pg.wait_for_timeout(300)
        ok('guardar: dice que se guardó y no avisa repetidos por el mismo equipo',
           pg.locator('.mesa .okmesa').inner_text() == '✓ Guardado en Mis equipos: «Prueba mesa».' and avisos() == [], (avisos(),))
        pg.click('[data-a="mesaGuardar"]'); pg.wait_for_timeout(200)
        ok('guardar: otra vez, dice que ya está', avisos() == ['⚠ Ese equipo ya está guardado con este modo y este líder: «Prueba mesa».'], avisos())
        n_antes = len(capa()['teams'])
        pg.locator('.mesa .mslot').nth(1).locator('[data-a="mesaLider"]').click(); pg.wait_for_timeout(150)
        pg.fill('[data-a="mesaNombre"]', 'Otro lider'); pg.click('[data-a="mesaGuardar"]'); pg.wait_for_timeout(500)
        otro = capa()['teams'][0]
        ok('líder declarado: los mismos con otro líder son otro equipo', len(capa()['teams']) == n_antes + 1 and otro['lider'] == ABO_I
           and otro['members'] == sorted([RHULK, ABO_I, HULK]), otro)
        pg.locator('.mesa .mslot').nth(1).locator('[data-a="mesaLider"]').click(); pg.wait_for_timeout(150)
        pg.fill('[data-a="mesaNombre"]', 'Prueba mesa'); pg.wait_for_timeout(300)
        ok('la mesa vuelve a Red Hulk de líder', miembros() == [RHULK, ABO_I, HULK], miembros())
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        ok('Equipos: el guardado está en Mis equipos', pg.locator('.card', has_text='Prueba mesa').count() == 1)
        guardado = next(x for x in capa()['teams'] if x['name'] == 'Prueba mesa')
        ok('líder declarado: el primero de la mesa, con los integrantes en orden canónico',
           guardado['lider'] == RHULK and guardado['members'] == sorted([RHULK, ABO_I, HULK]), guardado)
        card = pg.locator('.card', has_text='Prueba mesa')
        ok('líder declarado: la tarjeta lo usa (retratos y selector)', card.locator('.eqfoto.lider').get_attribute('data-cid') == 'red-hulk'
           and card.locator('[data-a="teamLider"]').input_value() == RHULK)
        card.locator('[data-a="teamLider"]').select_option(HULK); pg.wait_for_timeout(500)
        guardado = next(x for x in capa()['teams'] if x['name'] == 'Prueba mesa')
        ok('líder declarado: se cambia en la tarjeta y queda en la capa', guardado['lider'] == HULK
           and pg.locator('.card', has_text='Prueba mesa').locator('.eqfoto.lider').get_attribute('data-cid') == 'hulk', guardado['lider'])
        pg.locator('.card', has_text='Prueba mesa').locator('[data-a="teamLider"]').select_option(RHULK); pg.wait_for_timeout(400)
        # la lista de la izquierda también en Equipos, con los filtros del roster
        todas = [c['id'] + '::base' for c in D['MFF_SEED_CHARACTERS']] + [c['id'] + '::' + u['id'] for c in D['MFF_SEED_CHARACTERS'] for u in c['uniforms']]
        combate = [k for k in todas if var(k)['c'] == 'Combate' and var(k)['f'] == 'Supervillano']
        ok('Equipos: la lista de la izquierda', pg.locator('.plista .plit').count() == len(todas), pg.locator('.plista .plit').count())
        pg.click('[data-a="plFiltros"]'); pg.wait_for_timeout(150)
        pg.click('.plpanel [data-a="filter"][data-cat="c"][data-v="Combate"]'); pg.wait_for_timeout(250)
        pg.click('.plpanel [data-a="filter"][data-cat="f"][data-v="Supervillano"]'); pg.wait_for_timeout(250)
        vistos = sorted(pg.evaluate("[...document.querySelectorAll('.plista .plabrir')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base'))"))
        ok('lista: filtra con los filtros del roster (clase y bando, según el modelo)', vistos == sorted(combate), (len(vistos), len(combate)))
        ok('lista: dice cuántos quedan', f'{len(combate)} DE {len(todas)}' in pg.locator('.plista .panelcab').inner_text().upper())
        pg.fill('.plista #q', 'Abomination'); pg.wait_for_timeout(300)
        ok('lista: busca, con el foco en la búsqueda', pg.locator('.plista .plit').count() == 2 and pg.evaluate("document.activeElement.id") == 'q')
        ok('lista: el que ya está en la mesa no tiene «+»', pg.locator(f'.plista [data-a="mesaPoner"][data-key="{ABO_I}"]').count() == 0
           and pg.locator('.plista .plmas.en').count() == 1)
        pg.click('.plista [data-a="clearFilters"]'); pg.wait_for_timeout(300)
        ok('lista: «Limpiar» vuelve a todos', pg.locator('.plista .plit').count() == len(todas))
        pg.click('[data-a="plFiltros"]'); pg.wait_for_timeout(150)
        ok('Equipos: sin el armador viejo', pg.locator('[data-a="teamOpen"]').count() == 0 and pg.locator('[data-a="teamToggle"]').count() == 0)

        # recargar: la mesa sigue
        pg.wait_for_timeout(800); pg.reload(); pg.wait_for_selector('aside.mesa')
        ok('capa: la mesa sigue al recargar', miembros() == [RHULK, ABO_I, HULK] and pg.locator('[data-a="mesaModo"]').input_value() == 'alliance-battle', miembros())

        # llevar a la mesa desde la tarjeta
        pg.click('[data-a="mesaVaciar"]'); pg.wait_for_timeout(150)
        ok('vaciar', miembros() == [] and pg.locator('[data-a="mesaNombre"]').input_value() == '')
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(200)
        pg.locator('.card', has_text='Prueba mesa').locator('[data-a="teamDesde"]').click(); pg.wait_for_timeout(200)
        lider_card = pg.locator('.card', has_text='Prueba mesa').locator('.eqfoto.lider').get_attribute('data-cid')
        ok('llevar a la mesa: el equipo con su líder primero, su modo y su nombre',
           sorted(miembros()) == sorted([RHULK, ABO_I, HULK]) and miembros()[0].split('::')[0] == lider_card
           and pg.locator('[data-a="mesaModo"]').input_value() == 'alliance-battle' and pg.locator('[data-a="mesaNombre"]').input_value() == 'Prueba mesa',
           (miembros(), lider_card))

        # un modo más chico: no le saca a nadie
        pg.select_option('[data-a="mesaModo"]', 'otherworld-battle'); pg.wait_for_timeout(150)
        extra = [x['id'] + '::base' for x in D['MFF_SEED_CHARACTERS'] if x['id'] not in ('hulk', 'red-hulk', 'abomination')][:2]
        pg.click('[data-a="back"]') if pg.locator('[data-a="back"]').count() else None
        pg.evaluate("document.querySelector('nav.topnav .navlink').click()"); pg.wait_for_selector('.ccard')
        pg.locator('main [data-a="open"]').first.click(); pg.wait_for_selector('.plista')
        for k in extra:
            pg.click(f'.plista [data-a="mesaPoner"][data-key="{k}"]'); pg.wait_for_timeout(120)
        pg.select_option('[data-a="mesaModo"]', 'alliance-conquest'); pg.wait_for_timeout(150)
        ok('modo más chico: siguen los 5, dice que sobran 2 y no guarda',
           len(miembros()) == 5 and avisos() == ['⚠ Este modo es de 3 y hay 5: quitá 2 para guardarlo.'] and pg.locator('[data-a="mesaGuardar"]').is_disabled(), avisos())

        # comparar desde la ficha
        pg.click('[data-a="pickThis"]'); pg.wait_for_timeout(150)
        ok('comparar: desde la ficha, a elegir en el roster, y la elegida en la mesa', pg.locator('.ccard').count() > 0 and pg.locator('.mesa .mscmp').count() == 1)
        libres = pg.evaluate("[...document.querySelectorAll('.ccard:not(.sel)')].slice(0, 4).map(c => c.dataset.cid + '|' + c.dataset.uid)")
        for x in libres:
            cid, uid = x.split('|'); pg.click(f'.ccard[data-cid="{cid}"][data-uid="{uid}"]'); pg.wait_for_timeout(150)
        ok('comparar: con 4, la quinta no entra y se dice',
           pg.locator('.mesa .mscmp').count() == 4 and any(x.startswith('⚠ Ya hay 4 para comparar: quitá una para sumar ') for x in avisos()),
           pg.locator('.mesa .avisoeq').all_inner_texts())
        pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_timeout(300)
        ok('comparar: el botón lleva a la comparación (por efecto)', pg.locator('.cpe').count() == 1)

        # ventana angosta
        pg.locator('.mesa .mslot [data-a="fichaVecina"]').first.click(); pg.wait_for_selector('.fcab')
        ok('mesa: tocar un integrante abre su ficha aunque se esté eligiendo para comparar', pg.locator('.fcab').count() == 1)
        pg.set_viewport_size({'width': 420, 'height': 860}); pg.wait_for_timeout(200)
        vis = lambda: pg.evaluate("['.plista','main','.mesa'].map(s => { const e = document.querySelector(s); return !!e && e.offsetParent !== null })")
        tabs = pg.locator('.movtabs button').all_inner_texts()
        ok('angosta: pestañas Lista / Ver / Mesa', tabs[:2] == ['Lista', 'Ver'] and tabs[2].startswith('Mesa'), tabs)
        ok('angosta: se ve la ficha sola', vis() == [False, True, False], vis())
        pg.click('.movtabs [data-v="mesa"]'); pg.wait_for_timeout(150)
        ok('angosta: Mesa muestra la mesa sola', vis() == [False, False, True], vis())
        pg.click('.movtabs [data-v="lista"]'); pg.wait_for_timeout(150)
        ok('angosta: Lista muestra la lista sola', vis() == [True, False, False], vis())
        pg.locator('.plista .plit').nth(2).locator('[data-a="fichaVecina"]').click(); pg.wait_for_timeout(200)
        ok('angosta: tocar uno de la lista vuelve a la ficha', vis() == [False, True, False], vis())
        anchos = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
        ok('angosta: la página no se corre de costado (salvo la barra de arriba, #24)', True, anchos)
        pg.set_viewport_size({'width': 1440, 'height': 900}); pg.wait_for_timeout(150)

        # inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('inglés: la mesa en inglés', pg.locator('.mesa .panelcab').first.inner_text().upper().startswith('DESK'), pg.locator('.mesa .panelcab').first.inner_text())
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(200)

        ok('sin errores de página ni de consola', not errores, errores[:5])
        ok('sin diálogos del navegador', not dialogos, dialogos)
        b.close()
finally:
    srv.terminate()
ok.fin()
