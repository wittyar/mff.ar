"""Mi cuenta › Planificador (1.0.59; Ezequiel, 23 de noviembre de 2026, «Dale con todo» a «Planificador de Jefe mundial y
Batalla de alianza con tu roster: qué equipo armar con lo que tenés para la restricción del día»). El modelo, escrito aparte
de app.js con los datos (MFF_SEED_CHARACTERS, MFF_JEFE_MUNDIAL, MFF_ABX, la hoja de ruta de MFF_GUIA, la lista de cada modo y
sus roles, MFF_SOPORTES, MFF_CATALOGO, MFF_PERFIL), dice quiénes de un roster armado acá tienen que salir en cada grupo, en
qué orden y quiénes le dan algo al que pega:
  1. Sin roster: muestra qué pide y dice qué hacer (marcar tu roster), con el botón que lleva ahí.
  2. Jefe mundial, Leyenda, Knull, fases 20 a 24 (Superhéroes masculinos): la restricción y lo que piden los 3 que juegan y
     los aliados, con su fuente; los grupos (pueden jugar, solo aliados, les falta categoría y cuánto o que no llegan, con
     otro uniforme) y cuántos del juego la cumplen y no tenés, como el modelo; el orden por rol en la lista, por fila y por
     nombre; la lista con autor, versión y fecha y el aviso de lista vieja.
  3. El que pega: quiénes de los que pueden jugar le dan algo (liderazgo o soporte que le llega y le sirve), como el modelo.
  4. «Ya lo usé» lo saca y «Devolver» lo trae; cambiar el jefe no los devuelve.
  5. «Poner en la mesa»: la mesa con el modo, el líder sumado primero y el que pega, en lugar de lo que había (y lo dice).
  6. Batalla de alianza, el día y el modo en que más del roster pueden jugar: la restricción, sin categoría; los grupos y el
     orden con la lista del modo.
  7. Definitivo: sin restricción por fase y con la nota de la guía del juego.
  8. Desde Modos (Jefe mundial): «Planificar con tu roster» abre el planificador y «Atrás» vuelve a Modos.
  9. En el celular, sin desbordar; en inglés, con su texto. Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import SALIDA  # noqa: E401
import json, re
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED', 'MFF_SEED_CHARACTERS', 'MFF_JEFE_MUNDIAL', 'MFF_ABX', 'MFF_GUIA', 'MFF_SEED_TIERLISTS',
             'MFF_SEED_TIER_ASSIGNMENTS', 'MFF_ROLES_LISTAS', 'MFF_SOPORTES', 'MFF_CATALOGO', 'MFF_PERFIL', 'MFF_VERSION')
SEED, JM, ABX = D['MFF_SEED'], D['MFF_JEFE_MUNDIAL'], D['MFF_ABX']
PJ = {c['id']: c for c in D['MFF_SEED_CHARACTERS']}
PASOS = [p['id'] for p in D['MFF_GUIA']['progresion']['pasos']]
LISTAS = {l['id']: l for l in D['MFF_SEED_TIERLISTS']}


# ---- el modelo ----
def variante(c, uid=None):
    u = next((x for x in c['uniforms'] if x['id'] == uid), None) if uid else None
    if not u:
        return dict(cid=c['id'], uid=None, key=c['id'] + '::base', name=c['name'], sub='', c=c['c'], f=c['f'], gender=c['gender'],
                    race=c['race'], ab=c.get('abilities') or [], t=c['t'], trans=c['trans'], p=c['p'])
    return dict(cid=c['id'], uid=u['id'], key=c['id'] + '::' + u['id'], name=c['name'], sub=u['name'], c=u.get('c') or c['c'],
                f=u.get('f') or c['f'], gender=u.get('gender') or c['gender'], race=u.get('race') or c['race'],
                ab=u.get('ab') or c.get('abilities') or [], t=u.get('tier') or c['t'], trans=u.get('trans'), p=u['p'])
def versiones(c): return [variante(c)] + [variante(c, u['id']) for u in c['uniforms']]
def cumple1(v, x):
    for k, campo in (('CLASSES', 'c'), ('FACTIONS', 'f'), ('GENDERS', 'gender'), ('RACES', 'race')):
        if x in SEED[k]: return v[campo] == x
    if x in SEED['SKILL_TAGS']: return x in v['ab']
    raise SystemExit('valor de restricción desconocido: ' + x)
def cumple(v, restr): return all(cumple1(v, x) for x in restr)
def pasos_de(v):
    corte = {'T2': 't3', 'T3': 't4'}.get(v['t'])
    return PASOS[:PASOS.index(corte)] if corte else PASOS
def llega(paso_tuyo, pide): return PASOS.index(paso_tuyo) >= PASOS.index(pide)
def grupos(ruta, uniforme, restr, principal, aliados, usados=()):
    g = {'si': [], 'aliados': [], 'falta': [], 'otro': []}; no_tenes = 0
    for c in PJ.values():
        if c['id'] not in ruta:
            no_tenes += any(cumple(v, restr) for v in versiones(c)); continue
        v = variante(c, uniforme.get(c['id']))
        if not cumple(v, restr):
            if any(cumple(y, restr) for y in versiones(c) if y['key'] != v['key']): g['otro'].append(v['key'])
            continue
        if c['id'] in usados: continue
        if llega(ruta[c['id']], principal): g['si'].append(v)
        elif aliados and llega(ruta[c['id']], aliados): g['aliados'].append(v)
        else: g['falta'].append(v['key'])
    return g, no_tenes
def full(v): return v['name'] + (' — ' + v['sub'] if v['uid'] else '')
def filas_rol(lid, v):
    roles = D['MFF_ROLES_LISTAS']['pve'][lid]
    return [roles[f] for f in D['MFF_SEED_TIER_ASSIGNMENTS'].get(lid, {}).get(v['key'], [])]
def orden_rol(lid, v):
    k = lambda r: 3 - r[1] if r[0] == 'dps' else 3 if r[0] == 'lider' else 6 - r[1] if r[0] == 'soporte' else 6 if r[0] == 'striker' else 7
    fs = filas_rol(lid, v)
    return min(map(k, fs)) if fs else 8
def puesto(lid, v):
    rows = [r['id'] for r in LISTAS[lid]['rows']]; fs = D['MFF_SEED_TIER_ASSIGNMENTS'].get(lid, {}).get(v['key'], [])
    return min(rows.index(f) for f in fs) if fs else len(rows)
def ordenar(vs, key): return [v['key'] for v in sorted(vs, key=lambda v: (key(v), full(v).lower()))]
PIDE = {s: x['sirve'] for s, x in D['MFF_CATALOGO']['soporte'].items() if x['sirve'] != 'todos'}
MIRA = {'escala': 'esc', 'elemento': 'ele', 'tipo': 'tip', 'resistencia': 'res'}
def sirve(f, v):
    r = PIDE.get(f['s'])
    if not r: return True
    if r == 'nadie': return False
    que, val = r.split(':')
    pf = D['MFF_PERFIL'].get(v['p'], {'esc': [], 'tip': [], 'ele': [], 'res': []})
    de = {e[0] for e in pf['esc']} if que == 'escala' else set(pf[MIRA[que]])
    return val in de if val != '*' else bool(de)
SLOTS = ('leader', 'leader2', 'passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact')
R = {'Ability': 'ab', 'Type': 'c', 'Allies': 'race', 'Side': 'f'}
def aplica(x, v):
    if not x.get('r'): return True
    cat, val = x['r']
    if cat == 'Character': return v['name'] == val
    return val in v['ab'] if cat == 'Ability' else v[R[cat]] == val
def le_dan(p, si):
    out = []
    for v in si:
        if v['cid'] == p['cid']: continue
        so = D['MFF_SOPORTES'].get(v['p'], {})
        xs = [so[k] for k in SLOTS if so.get(k)]
        if any(aplica(x, p) and (not any(f['s'] in PIDE for f in x['fx']) or any(sirve(f, p) for f in x['fx'])) for x in xs):
            out.append(v['key'])
    return sorted(out)


# ---- el roster de la prueba (Knull, fases 20 a 24: Superhéroe y Masculino) ----
KNULL = next(j for j in JM['jefes'] if j['id'] == 'knull')
RANGO = KNULL['r'][3]; RESTR = RANGO[2]
LEY = next(d for d in JM['dificultades'] if d['id'] == 'leyenda')
assert RANGO[:2] == [20, 24] and RESTR == ['Superhéroe', 'Masculino'] and LEY['principal']['paso'] == 't3' and LEY['aliados']['paso'] == 't2'
asig = D['MFF_SEED_TIER_ASSIGNMENTS']['tv-wbl']
ruta, uniforme, usados_cids = {}, {}, set()
# Uniformes que están en la lista de Jefe mundial, que cumplen y con roles distintos: pueden jugar (Tier-3).
roles_vistos = set()
for key in sorted(asig):
    cid, uid = key.split('::')
    c = PJ.get(cid)
    if not c or uid == 'base' or cid in ruta: continue
    v = variante(c, uid); o = orden_rol('tv-wbl', v)
    if v['t'] != 'T2' and cumple(v, RESTR) and o not in roles_vistos and len(roles_vistos) < 4:
        roles_vistos.add(o); ruta[cid] = 't3'; uniforme[cid] = uid
def elegir(cond):
    return next(c for c in sorted(PJ.values(), key=lambda c: c['id']) if c['id'] not in ruta and cond(c))
base_si = elegir(lambda c: cumple(variante(c), RESTR) and c['t'] == 'T4' and not any(asig.get(c['id'] + '::base', [])))
ruta[base_si['id']] = 't4'                                                     # cumple, sin la base en la lista: va al final
ruta[elegir(lambda c: cumple(variante(c), RESTR) and c['t'] != 'T2')['id']] = 't2'          # solo aliado
ruta[elegir(lambda c: cumple(variante(c), RESTR) and c['t'] != 'T2')['id']] = 'n70'         # solo aliado, con un paso intermedio
FALTA = elegir(lambda c: cumple(variante(c), RESTR) and c['t'] != 'T2'); ruta[FALTA['id']] = 't1'   # les falta categoría
T2 = elegir(lambda c: cumple(variante(c), RESTR) and c['t'] == 'T2'); ruta[T2['id']] = 'desbloqueo'  # T2: no llega a jugar
OTRO = elegir(lambda c: not cumple(variante(c), RESTR) and any(cumple(v, RESTR) for v in versiones(c)) and c['t'] != 'T2')
ruta[OTRO['id']] = 't4'                                                        # la cumpliría con otro uniforme
NADA = elegir(lambda c: not any(cumple(v, RESTR) for v in versiones(c))); ruta[NADA['id']] = 't4'   # no la cumple con nada
CAPA = {'ruta': ruta, 'uniforme': uniforme, 'mesa': {'members': ['wolverine::base'], 'modeId': '', 'abxDia': 1, 'abxDif': '', 'name': ''}}
G, NO_TENES = grupos(ruta, uniforme, RESTR, 't3', 't2')
assert len(G['si']) >= 4 and G['aliados'] and G['falta'] and G['otro'], G

GRUPOS_JS = """[...document.querySelectorAll('.plgrupo')].map(g => [g.querySelector('h4').firstChild.textContent.trim(),
  [...g.querySelectorAll('.plfila .minipj, .plusado .minipj')].map(m => m.dataset.cid + '::' + (m.dataset.uid || 'base')),
  [...g.querySelectorAll('.plfila')].map(f => f.innerText)])"""
grupos_app = lambda pg: {t: (ks, txt) for t, ks, txt in pg.evaluate(GRUPOS_JS)}

DIR = carpeta_datos()
srv, url = levantar(DIR, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' and '404' not in m.text else None)
        pg.goto(url); pg.wait_for_selector('.ccard')
        capa = lambda: pg.evaluate("fetch('/api/capa', { headers: { 'X-MFF': '1' } }).then(r => r.json())")['capa']
        def plan():
            pg.click('nav.topnav [data-a="goCuenta"]'); pg.wait_for_selector('.cuhub')
            pg.click('.cutabs [data-a="cuentaTab"][data-v="plan"]'); pg.wait_for_selector('.plpasos')
        def caso_knull():
            pg.select_option('select[data-a="planDif"]', 'leyenda'); pg.wait_for_timeout(200)
            pg.select_option('select[data-a="planJefe"]', 'knull'); pg.wait_for_timeout(200)
            pg.select_option('select[data-a="planFase"]', '3'); pg.wait_for_timeout(300)

        # 1. sin roster
        plan(); caso_knull()
        p2 = pg.locator('.plpaso').nth(1)
        ok('1 sin roster: dice qué hacer y lleva a Tu roster', 'Todavía no marcaste tu roster' in p2.inner_text()
           and p2.locator('[data-a="cuentaTab"][data-v="roster"]').count() == 1 and 'superhéroe' in pg.locator('.plpaso').nth(0).inner_text().lower(), p2.inner_text()[:200])
        ok('1 sin roster: el contador de los del juego que la cumplen', f'Del juego, {sum(any(cumple(v, RESTR) for v in versiones(c)) for c in PJ.values())} personajes' in p2.inner_text(), p2.inner_text()[:300])
        ok('1 el texto fijo a la vista', pg.locator('.plaviso').inner_text() == 'Es una consulta sobre tu roster y las listas de la comunidad, no un equipo probado.')
        p2.locator('[data-a="cuentaTab"][data-v="roster"]').click(); pg.wait_for_selector('.roslista')
        ok('1 el botón lleva a Tu roster', pg.locator('.cutab.on').inner_text().startswith('Tu roster'))

        # Con el roster de la prueba.
        json.dump(CAPA, open(os.path.join(DIR, 'capa.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        pg.reload(); pg.wait_for_selector('.ccard'); plan(); caso_knull()

        # 2. Jefe mundial
        p1 = pg.locator('.plpaso').nth(0).inner_text()
        ok('2 qué pide: la restricción, los 3 que juegan, los aliados y la fuente', all(x.lower() in p1.lower() for x in ('Superhéroe', 'Masculino', LEY['principal']['es'], LEY['aliados']['es'], 'mffguide.fyi')), p1)
        ga = grupos_app(pg)
        tit = {'si': 'Pueden jugar (cumplen y llegan a lo que piden los 3 que juegan)', 'aliados': 'Solo como aliados',
               'falta': 'La cumplen y les falta categoría', 'otro': 'La cumplirían con otro uniforme'}
        ok('2 pueden jugar, como el modelo, en el orden por rol en la lista', ga.get(tit['si'], [[]])[0] == ordenar(G['si'], lambda v: orden_rol('tv-wbl', v)),
           (ga.get(tit['si'], [[]])[0], ordenar(G['si'], lambda v: orden_rol('tv-wbl', v))))
        ok('2 solo como aliados, como el modelo', sorted(ga.get(tit['aliados'], [[]])[0]) == sorted(v['key'] for v in G['aliados']), ga.get(tit['aliados']))
        ok('2 les falta categoría, como el modelo', sorted(ga.get(tit['falta'], [[]])[0]) == sorted(G['falta']), ga.get(tit['falta']))
        ok('2 con otro uniforme, como el modelo', sorted(ga.get(tit['otro'], [[]])[0]) == sorted(G['otro']), ga.get(tit['otro']))
        ok('2 el que no la cumple con nada no sale', not any(k.startswith(NADA['id'] + '::') for t in ga for k in ga[t][0]))
        falta = dict(zip(ga[tit['falta']][0], ga[tit['falta']][1]))
        t3 = 'TP' if FALTA['trans'] else 'T3'
        ok('2 cuánto falta: de aliado T2 y para jugar T3 (TP si trasciende); un T2 no llega', 'de aliado pide T2' in falta[FALTA['id'] + '::base']
           and f'para jugar pide {t3}' in falta[FALTA['id'] + '::base'] and 'pide T3 y no llega: su máximo es T2' in falta[T2['id'] + '::base'], falta)
        ok('2 cuántos del juego la cumplen y no tenés', f'Del juego, {NO_TENES} personajes' in pg.locator('.plpaso').nth(1).inner_text(), NO_TENES)
        ok('2 el paso intermedio se ve («Nv. 70»)', any('nv. 70' in x.lower() for x in ga[tit['aliados']][1]), ga[tit['aliados']][1])
        l = LISTAS['tv-wbl']; cab = pg.locator('.pllistacab').inner_text()
        ok('3 la lista del modo con autor, versión y fecha, y el aviso de versión vieja', all(x in cab for x in (l['author'], l['gameVersion'], l['published']))
           and pg.locator('.plpaso').nth(2).locator('.aviso', has_text=l['gameVersion']).count() == 1, cab)
        ok('3 el criterio del orden se dice', 'Primero los que la lista pone para pegar' in pg.locator('.plpaso').nth(2).inner_text())
        filas_si = dict(zip(ga[tit['si']][0], ga[tit['si']][1]))
        ok('3 el rol y la fila de cada uno; el que no está en la lista lo dice', 'no está en la lista' in filas_si[base_si['id'] + '::base']
           and all(any(r['label'].lower() in filas_si[v['key']].lower() for r in l['rows'] if r['id'] in asig.get(v['key'], [])) for v in G['si'] if asig.get(v['key'])), filas_si)
        pg.click('[data-a="planOrden"][data-v="fila"]'); pg.wait_for_timeout(300)
        ok('3 por fila de la lista', grupos_app(pg)[tit['si']][0] == ordenar(G['si'], lambda v: puesto('tv-wbl', v)))
        pg.click('[data-a="planOrden"][data-v="nombre"]'); pg.wait_for_timeout(300)
        ok('3 por nombre', grupos_app(pg)[tit['si']][0] == ordenar(G['si'], lambda v: 0))
        pg.click('[data-a="planOrden"][data-v="rol"]'); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{SALIDA}/plan_wb_1400.png', full_page=True)

        # 3. el que pega
        PEGA = next(v for v in G['si'] if le_dan(v, G['si'])) if any(le_dan(v, G['si']) for v in G['si']) else G['si'][0]
        pg.click(f'[data-a="planPega"][data-key="{PEGA["key"]}"]'); pg.wait_for_timeout(300)
        dan = sorted(pg.evaluate("[...document.querySelectorAll('.plda > .plpj .minipj')].map(m => m.dataset.cid + '::' + (m.dataset.uid || 'base'))"))
        ok('3 quiénes le dan algo al que pega, como el modelo', dan == le_dan(PEGA, G['si']), (dan, le_dan(PEGA, G['si'])))
        ok('3 sin «el mejor»: el texto dice que no se suma ni se ordena por cuánto da', 'No se suma ni se ordena por cuánto da' in pg.locator('.plpaso').nth(3).inner_text())
        pg.screenshot(path=f'{SALIDA}/plan_wb_pega_1400.png', full_page=True)

        # 5. a la mesa
        lider = None
        if dan:
            lider = dan[0]; pg.click(f'[data-a="planCon"][data-key="{lider}"]'); pg.wait_for_timeout(200)
        pg.click('[data-a="planMesa"]'); pg.wait_for_timeout(500)
        m = capa()['mesa']
        tiene_lid = lider and any(pg.locator(f'.plda:has(.minipj[data-cid="{lider.split("::")[0]}"]) .plda-g', has_text='Si lo llevás de líder').count() for _ in [0])
        ok('5 la mesa: el modo, el que pega y el sumado (el líder primero si le da su liderazgo), en lugar de lo que había',
           m['modeId'] == 'world-boss' and set(m['members']) == {PEGA['key']} | ({lider} if lider else set())
           and (m['members'][0] == (lider if tiene_lid else PEGA['key'])) and 'en lugar de los 1 que había' in pg.locator('aside.mesa').inner_text(), (m, lider))

        # 4. ya lo usé
        usado = G['si'][-1]
        pg.click(f'.plfila:has(.minipj[data-cid="{usado["cid"]}"]) [data-a="planUsado"]'); pg.wait_for_timeout(300)
        ga = grupos_app(pg)
        ok('4 «Ya lo usé» lo saca de los que pueden jugar y lo lista aparte', usado['key'] not in ga[tit['si']][0] and usado['key'] in ga['Ya usados'][0], list(ga))
        pg.select_option('select[data-a="planFase"]', '4'); pg.wait_for_timeout(300)
        ok('4 cambiar de fases no lo devuelve (aunque no cumpla la nueva restricción)', usado['key'] in grupos_app(pg).get('Ya usados', [[]])[0])
        pg.select_option('select[data-a="planFase"]', '3'); pg.wait_for_timeout(300)
        pg.click(f'[data-a="planDevolver"][data-cid="{usado["cid"]}"]'); pg.wait_for_timeout(300)
        ok('4 «Devolver» lo trae', usado['key'] in grupos_app(pg)[tit['si']][0])

        # 6. Batalla de alianza
        pg.click('[data-a="planModoJuego"][data-v="ab"]'); pg.wait_for_timeout(300)
        # El día y el modo en que más de tu roster pueden jugar (según el modelo), con alguna restricción.
        r = max((x for x in ABX['restricciones'] if x['r']), key=lambda x: (len(grupos(ruta, uniforme, x['r'], 'desbloqueo', None)[0]['si']), -x['d']))
        pg.select_option('select[data-a="planDia"]', str(r['d'])); pg.wait_for_timeout(200)
        pg.select_option('select[data-a="planModo"]', r['m']); pg.wait_for_timeout(300)
        GA, NA = grupos(ruta, uniforme, r['r'], 'desbloqueo', None)
        ga = grupos_app(pg); p1 = pg.locator('.plpaso').nth(0).inner_text()
        ok('6 el día con su restricción (y la de cada modo en la lista de días), sin categoría', 'No pide' in p1 and all(x.lower() in p1.lower() for x in r['r'])
           and r['m'] + ': ' in pg.locator(f'select[data-a="planDia"] option[value="{r["d"]}"]').inner_text() and len(GA['si']) >= 2, (r, p1))
        ok('6 pueden jugar, como el modelo, en el orden por rol en la lista del modo',
           ga.get('Pueden jugar (cumplen la restricción)', [[]])[0] == ordenar(GA['si'], lambda v: orden_rol('tv-alianza', v)), (ga, [v['key'] for v in GA['si']]))
        ok('6 con otro uniforme, como el modelo', sorted(ga.get(tit['otro'], [[]])[0]) == sorted(GA['otro']))
        ok('6 la lista de Batalla de alianza', LISTAS['tv-alianza']['author'] in pg.locator('.pllistacab').inner_text())
        pg.screenshot(path=f'{SALIDA}/plan_ab_1400.png', full_page=True)

        # 7. Definitivo
        pg.click('[data-a="planModoJuego"][data-v="wb"]'); pg.wait_for_timeout(200)
        pg.select_option('select[data-a="planDif"]', 'definitivo'); pg.wait_for_timeout(300)
        p1 = pg.locator('.plpaso').nth(0).inner_text()
        ok('7 Definitivo: sin fases, sin restricción y la nota de la guía del juego', pg.locator('select[data-a="planFase"]').count() == 0
           and 'sin restricción' in p1 and 'es ideal para personajes de Tier-2' in p1, p1)

        # 8. desde Modos y «Atrás»
        pg.click('nav.topnav [data-a="goModos"]'); pg.wait_for_selector('.modos')
        pg.click('#modo-world-boss .modohead'); pg.wait_for_timeout(300)
        pg.click('#modo-world-boss [data-a="irPlan"]'); pg.wait_for_selector('.plpasos')
        ok('8 «Planificar con tu roster» abre el planificador en Jefe mundial', pg.locator('[data-a="planModoJuego"][data-v="wb"].on').count() == 1)
        pg.go_back(); pg.wait_for_timeout(500)
        ok('8 «Atrás» vuelve a Modos', pg.locator('.modos').count() == 1 and pg.locator('nav.topnav .navlink.on').inner_text() == 'Modos')
        pg.click('#modo-alliance-battle .modohead'); pg.wait_for_timeout(300)
        pg.click('#modo-alliance-battle [data-a="irPlan"]'); pg.wait_for_selector('.plpasos')
        ok('8 desde Batalla de alianza, en Batalla de alianza', pg.locator('[data-a="planModoJuego"][data-v="ab"].on').count() == 1)

        # 9. celular e inglés
        pg.click('[data-a="planModoJuego"][data-v="wb"]'); pg.wait_for_timeout(200); caso_knull()
        pg.click(f'[data-a="planPega"][data-key="{PEGA["key"]}"]'); pg.wait_for_timeout(300)
        pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(400)
        anchos = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
        ok('9 celular: no se sale del ancho', anchos[0] <= anchos[1], anchos)
        pg.screenshot(path=f'{SALIDA}/plan_wb_390.png', full_page=True)
        pg.set_viewport_size({'width': 1400, 'height': 900})
        pg.click('nav.topnav [data-a="lang"]'); pg.wait_for_timeout(400)
        ok('9 en inglés', pg.locator('.plaviso').inner_text() == 'It is a query over your roster and the community lists, not a tested team.'
           and 'super hero' in pg.locator('.plpaso').nth(0).inner_text().lower().replace('superhero', 'super hero'), pg.locator('.plpaso').nth(0).inner_text()[:200])
        pg.click('nav.topnav [data-a="lang"]'); pg.wait_for_timeout(300)
        ok('sin errores de página ni de consola', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
