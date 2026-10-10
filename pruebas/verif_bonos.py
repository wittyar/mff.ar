"""Bonos de equipo (1.0.12): MFF_BONOS, el bloque de la ficha y la sinergia, contra la wiki leída
aparte (work/wikitext) y el modelo escrito aparte (auditoria_equipos.py / modelo_foco.py).
- datos: integrantes válidos, Afflicted Lovers y Krakoan Order como en la captura del juego, los
  empates con sus dos versiones, la recarga en negativo, los del juego con su fuente
- ficha: el bloque plegado con todos sus bonos (Cyclops), un empate (Ancient One), uno del juego
  (Galactus) y un personaje sin bonos
- sinergia: comparar Cyclops + Jean Grey (la razón del bono y el puntaje del modelo); un equipo de la
  capa con Galactus, Thanos y Annihilus; las combinaciones de Galactus contra el modelo (los
  integrantes de un bono quedan vinculados)
- inglés y celular.
Carril J: el bono del trío se lee de «Además», en el «Por qué» de la tarjeta (antes, de sus renglones de texto).
Carril modal (5 de octubre de 2026): de los puntos de la ventana del «Por qué» de la tarjeta («Bonos de equipo»).
Carril de consistencia: los bonos y la comparativa escriben los números como el «Por qué» (coma decimal y «−»)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright
import auditoria_equipos as A
import modelo_foco as F

ok = Chequeo()
D0 = datos_js('MFF_BONOS', 'MFF_SEED_CHARACTERS', 'MFF_GUIA')
BON, C, FUENTES = D0['MFF_BONOS'], D0['MFF_SEED_CHARACTERS'], D0['MFF_GUIA']['fuentes']
IDS = {c['id'] for c in C}
NOM = {c['id']: c['name'] for c in C}
def bono(*cids): return next(b for b in BON if sorted(b['m']) == sorted(cids))

# ---- datos ----
malos = [b for b in BON if not 2 <= len(set(b['m'])) == len(b['m']) <= 3 or set(b['m']) - IDS or not b['v'] or not all(b['v'])
         or set(b['f']) - set(FUENTES)]
ok('cada bono: 2 o 3 personajes distintos del roster, stats y fuentes definidas', not malos, malos[:2])
conjuntos = [frozenset(b['m']) for b in BON]
ok('un bono por conjunto de integrantes', len(set(conjuntos)) == len(conjuntos))
al = bono('cyclops', 'jean-grey')
ok('Afflicted Lovers: Cyclops y Jean Grey, ataques +5,2% y vida +5% (el juego: 5,24% y 4,97%)',
   al['n'] == 'Afflicted Lovers' and al['v'] == [[['All Basic Attacks', 5.2], ['HP', 5.0]]] and al['f'] == ['wiki-bonos'], al)
ko = bono('cyclops', 'jean-grey', 'polaris')
ok('Krakoan Order: de tres, con la recarga en negativo', ko['n'] == 'Krakoan Order' and ['Skill Cooldown', -4.8] in ko['v'][0], ko)
bs = bono('ancient-one', 'baron-mordo')
ok('Bad Student: las dos páginas no coinciden y van las dos versiones', bs['n'] == 'Bad Student' and len(bs['v']) == 2, bs)
ga = bono('galactus', 'thanos', 'annihilus')
ok('Galactus Abducted: del juego, con sus dos decimales', ga['f'] == ['juego-bonos'] and
   ga['v'] == [[['All Basic Attacks', 5.35], ['Critical Rate', 4.78], ['Attack Speed', 4.78]]], ga)
ok('ningún stat de recarga o de duración de control en positivo',
   not [b for b in BON for v in b['v'] for s, x in v if s in ('Skill Cooldown', 'Crowd Control Time') and x > 0])
sin_bonos = next(c for c in C if not any(c['id'] in b['m'] for b in BON))
de_cyclops = [b for b in BON if 'cyclops' in b['m']]

# ---- modelo: combinaciones de Galactus (como verif_combos.py) ----
def consulta(v):
    pool = [x for x in A.TODAS if x['cid'] != v['cid']]
    puede = [any(v['key'] in alc for *_, alc in A.SOPS[x['key']]) or any(x['key'] in alc for *_, alc in A.SOPS[v['key']])
             or A.comparten_bono(v, x) for x in pool]
    filas = []
    for i in range(len(pool)):
        if not puede[i]: continue
        for j in range(i + 1, len(pool)):
            if not puede[j] or pool[i]['cid'] == pool[j]['cid']: continue
            vs = [v, pool[i], pool[j]]
            if not F.sueltos_foco(vs): filas.append((i, j, F.score_foco(vs), F.stk_foco(vs)))
    return pool, filas
def vista(pool, filas, con=''):
    ref = [A.RANGO[x['key']] for x in pool]
    orden = sorted(range(len(filas)), key=lambda n: (-filas[n][2], -filas[n][3], ref[filas[n][0]] + ref[filas[n][1]], n))    # los strikers desempatan
    vistos, out = set(), []
    for n in orden:
        i, j, p, _ = filas[n]; a, b = pool[i], pool[j]
        if con and con not in (a['cid'], b['cid']): continue
        par = tuple(sorted((a['cid'], b['cid'])))
        if par in vistos: continue
        vistos.add(par); out.append((a, b, p))
    return out
gal = A.VAR['galactus::base']
t0 = time.time(); pool, filas = consulta(gal); fv = vista(pool, filas)
print(f'modelo: {len(fv)} combinaciones de Galactus ({time.time() - t0:.1f} s)')
con_thanos = vista(pool, filas, con='thanos')
ok('modelo: Galactus con Thanos y Annihilus (Galactus Abducted los vincula)', any({a['cid'], b['cid']} == {'thanos', 'annihilus'} for a, b, _ in con_thanos))

D = carpeta_datos()
EQUIPO = {'id': 'eq-b', 'name': 'Devoradores', 'modeId': '', 'reason': '', 'members': ['galactus::base', 'thanos::base', 'annihilus::base']}
json.dump({'teams': [EQUIPO]}, open(os.path.join(D, 'capa.json'), 'w', encoding='utf-8'), ensure_ascii=False)
srv, url = levantar(D, origen_local())
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        def inicio():
            pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        def ficha(cid, tab='equipos'):
            inicio(); pg.fill('#q', NOM[cid]); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
            pg.click(f'[data-a="fichaTab"][data-v="{tab}"]'); pg.wait_for_selector('#bonos')
        def tarjeta(nombre):
            return pg.locator('#bonos .card.bono', has=pg.locator('b', has_text=nombre)).first

        # 1. ficha de Cyclops: todos sus bonos, plegados
        ficha('cyclops')
        resumen = pg.locator('#bonos details.reglas > summary').inner_text()
        ok('Cyclops: el bloque está plegado y dice cuántos bonos tiene', f'Ver sus {len(de_cyclops)} bonos' in resumen
           and not pg.locator('#bonos details.reglas').get_attribute('open') is not None and not pg.locator('#bonos .card.bono').first.is_visible(), resumen)
        pg.click('#bonos details.reglas > summary'); pg.wait_for_timeout(150)
        ok('Cyclops: una tarjeta por bono', pg.locator('#bonos .card.bono').count() == len(de_cyclops), pg.locator('#bonos .card.bono').count())
        t = tarjeta('Afflicted Lovers')
        ok('Afflicted Lovers: con Jean Grey (se abre su ficha) y sus stats', t.locator('[data-a="open"][data-cid="jean-grey"]').count() == 1
           and t.locator('[data-a="open"]').count() == 1 and 'Todos los ataques básicos +5,2% · PG +5%' in t.inner_text()
           and 'Future Fight Wiki — Team Bonus' in t.inner_text(), t.inner_text().replace('\n', ' | '))
        t = tarjeta('Krakoan Order')
        ok('Krakoan Order: con los otros dos y la recarga que baja', t.locator('[data-a="open"]').count() == 2
           and 'Recarga de skills (Skill Cooldown) −4,8%' in t.inner_text(), t.inner_text().replace('\n', ' | '))
        primeros = pg.locator('#bonos .card.bono').evaluate_all("cs => cs.map(c => c.querySelectorAll('[data-a=open]').length)")
        ok('primero los de tres', primeros == sorted(primeros, reverse=True), primeros[:12])

        # 2. un empate de la wiki
        ficha('ancient-one'); pg.click('#bonos details.reglas > summary'); pg.wait_for_timeout(150)
        t = tarjeta('Bad Student')
        ok('Bad Student: avisa que la wiki no coincide y muestra las dos versiones', t.locator('.bonoaviso').count() == 1
           and t.locator('.bonostats').count() == 2, t.inner_text().replace('\n', ' | '))

        # 3. del juego
        ficha('galactus'); pg.click('#bonos details.reglas > summary'); pg.wait_for_timeout(150)
        t = tarjeta('Galactus Abducted')
        ok('Galactus Abducted: los valores del juego y su fuente', 'Todos los ataques básicos +5,35% · Probabilidad de crítico +4,78% · Velocidad atq. +4,78%' in t.inner_text()
           and 'MARVEL Future Fight — Team Bonus' in t.inner_text(), t.inner_text().replace('\n', ' | '))
        # combinaciones de Galactus contra el modelo
        pg.wait_for_selector('#combos .combo', timeout=90000)
        cuenta = int(re.sub(r'\D', '', pg.locator('#combos .row > span.muted').first.inner_text().split('·')[0]))
        ok('Galactus: la cantidad de combinaciones es la del modelo', cuenta == len(fv), (cuenta, len(fv)))
        pg.select_option('select[data-a="eqCon"]', 'thanos'); pg.wait_for_timeout(250)
        def pagina():
            return [([f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in c.locator('.eqfoto').all()],
                     int(c.locator('.eqpts > b').inner_text())) for c in pg.locator('#combos .combo').all()]
        def en_orden(vs):
            """Como se pintan: el líder del equipo primero (4 de octubre de 2026)."""
            li = A.lider_sin_contexto(vs)
            return [x['key'] for x in ([vs[li]] + [x for n, x in enumerate(vs) if n != li] if li is not None else vs)]
        ok('Galactus con Thanos: la primera página es la del modelo',
           pagina() == [(en_orden([gal, a, b_]), p) for a, b_, p in con_thanos[:20]], pagina()[:3])
        k = next(i for i, (a, b_, _) in enumerate(con_thanos) if {a['cid'], b_['cid']} == {'thanos', 'annihilus'})
        for _ in range(k // 20):
            pg.locator('[data-a="eqPagina"]').last.click(); pg.wait_for_timeout(200)
        trio = pg.locator('#combos .combo', has=pg.locator('.eqfoto[data-cid="annihilus"]')).first
        trio.locator('[data-a="pqAbrir"]').click(); pg.wait_for_selector('#pqdlg[open]')
        lineas = pg.evaluate("() => [...document.querySelectorAll('#pqdlg .pqm-parte ul.pqm-lista > li')].map(li => [[...li.childNodes]"
                             ".filter(n => n.nodeName !== 'UL').map(n => n.textContent).join('').replace(/\\s+/g, ' ').trim(),"
                             " [...li.querySelectorAll(':scope > ul > li')].map(x => x.textContent.replace(/\\s+/g, ' ').trim())])")
        pg.keyboard.press('Escape'); pg.wait_for_selector('#pqdlg', state='hidden')
        ok(f'Galactus con Thanos: el trío con Annihilus (fila {k + 1}) dice el bono, en los puntos de la ventana del «Por qué»',
           any(l.startswith('Bono de equipo «Galactus Abducted» (Galactus + Thanos + Annihilus) →') and
               fx == ['Todos los ataques básicos +5,35%', 'Probabilidad de crítico +4,78%', 'Velocidad atq. +4,78%'] for l, fx in lineas), lineas)
        pg.select_option('select[data-a="eqCon"]', ''); pg.wait_for_timeout(100)

        # 4. sin bonos
        ficha(sin_bonos['id'])
        ok(f"{sin_bonos['name']}: sin bonos conocidos, sin tarjetas", pg.locator('#bonos .card.bono').count() == 0
           and 'No tiene bonos de equipo conocidos' in pg.locator('#bonos').inner_text())

        # 5. comparar Cyclops y Jean Grey
        inicio(); pg.fill('#q', 'Cyclops'); pg.wait_for_timeout(250)
        pg.click('.ccard[data-cid="cyclops"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="pickThis"]'); pg.wait_for_selector('#q')
        pg.fill('#q', 'Jean Grey'); pg.wait_for_timeout(250)
        pg.click('.ccard[data-cid="jean-grey"][data-uid=""]'); pg.wait_for_timeout(150)
        pg.click('[data-a="goCompare"]'); pg.wait_for_timeout(300)
        card = pg.locator('.card', has=pg.locator('h3', has_text='Sinergia estimada'))
        lineas = card.locator('li').all_inner_texts()
        pts = int(card.locator('span.muted').first.inner_text().split()[0])
        esperado = A.score([A.VAR['cyclops::base'], A.VAR['jean-grey::base']])
        ok('comparar Cyclops + Jean Grey: la razón del bono y el puntaje del modelo',
           'Bono de equipo «Afflicted Lovers» (Cyclops + Jean Grey) → Cyclops, Jean Grey: Todos los ataques básicos +5,2% · PG +5%' in lineas
           and pts == esperado, (pts, esperado, lineas))
        ok('la nota de la sinergia nombra los bonos', 'Cada bono de equipo con todos sus integrantes' in card.inner_text())
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(200)
        lineas_en = pg.locator('.card', has=pg.locator('h3', has_text='Estimated synergy')).locator('li').all_inner_texts()
        ok('en inglés', any(l.startswith('Team bonus «Afflicted Lovers» (Cyclops + Jean Grey) →') for l in lineas_en), lineas_en)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(200)
        inicio(); pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(150)

        # 6. un equipo de la capa
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        tx = pg.locator('.card', has_text='Devoradores').first.inner_text()
        esperado = A.score([A.VAR[k] for k in EQUIPO['members']])
        ok('equipo Devoradores: la sinergia del modelo (con Galactus Abducted)', f'{esperado} pts de sinergia' in tx, (esperado, tx.replace('\n', ' | ')))
        ok('sin errores de página', not errores, errores[:3])
        b.close()

        # 7. celular
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        ficha('cyclops'); pg.click('#bonos details.reglas > summary'); pg.wait_for_timeout(200)
        ancho = pg.evaluate('document.documentElement.scrollWidth')
        ok('celular: el bloque abierto no se sale de la pantalla', ancho <= 390, ancho)
        pg.locator('#bonos').screenshot(path=f'{SALIDA}/bonos_390.png')
        ok('sin errores de página (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
