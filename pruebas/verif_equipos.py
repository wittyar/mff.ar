"""(1.0.6: las combinaciones de 3 se prueban en verif_combos.py.) Pestaña Equipos de la ficha, contrastada con una sinergia recalculada acá en Python (misma
regla que synergy() de app.js, escrita aparte, con los efectos aplicados: auditoria_equipos.py):
- en tus equipos: los que lo tienen; en los demás, el mejor cambio (quién sale, antes y después)
  entre los lugares donde queda vinculado con alguien; los que no, en su línea
- equipos nuevos: puntaje para él (sinergia con foco: modelo_foco.py) y el del equipo, todos los
  compañeros con vínculo de soporte con él, uno por personaje, la misma búsqueda que la escrita
  aparte, y el óptimo exhaustivo de 3 (con vínculo)
- Annihilus (villano sin soportes): nada de Nick Fury; Apocalypse: nada de Phil Coulson
- el botón abre el armador con el equipo cargado; sin equipos; celular con 7 pestañas."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import itertools, json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
FUERA = """() => { const lim = document.getElementById('fcuerpo').getBoundingClientRect().right;
  return [...document.querySelectorAll('#fcuerpo *')].filter(e => e.getBoundingClientRect().right > lim + 0.5)
    .map(e => (e.getAttribute('data-a') || e.className || e.tagName) + ' → ' + Math.round(e.getBoundingClientRect().right)).slice(0, 4); }"""
D0 = datos_js('MFF_SEED_CHARACTERS', 'MFF_SOPORTES', 'MFF_SEED', 'MFF_MODOS')
C, SOP, ADV = D0['MFF_SEED_CHARACTERS'], D0['MFF_SOPORTES'], D0['MFF_SEED']['VENTAJA_TIPO']
TAM = {m['id']: m['equipo']['tam'] for m in D0['MFF_MODOS'] if m.get('equipo') and m['equipo'].get('tam')}
NOMBRE_MODO = {m['id']: m['nombre'] for m in D0['MFF_MODOS']}

VAR = {}
for c in C:
    VAR[f"{c['id']}::base"] = dict(key=f"{c['id']}::base", cid=c['id'], name=c['name'], sub='Base', uid=None, c=c['c'], f=c['f'],
                                    race=c['race'], ab=c['abilities'], r=c['r'], p=c['p'])
    for u in c['uniforms']:
        VAR[f"{c['id']}::{u['id']}"] = dict(key=f"{c['id']}::{u['id']}", cid=c['id'], name=c['name'], sub=u['name'], uid=u['id'],
                                             c=u.get('c', c['c']), f=u.get('f', c['f']), race=u.get('race', c['race']),
                                             ab=u.get('ab', c['abilities']), r=u.get('r', c['r']), p=u['p'])
def full(v): return v['name'] + (' — ' + v['sub'] if v['uid'] else '')
def aplica(x, b):
    if not x.get('r'): return True
    cat, val = x['r']
    return {'Ability': val in b['ab'], 'Type': b['c'] == val, 'Allies': b['race'] == val, 'Side': b['f'] == val, 'Character': b['name'] == val}[cat]
NOLIDER = ['passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact']
def score(vs):
    if len(vs) < 2: return 0
    s = 0
    for i, a in enumerate(vs):
        sp = SOP.get(a['p']) or {}
        for k in NOLIDER:
            if sp.get(k) and any(aplica(sp[k], b) for j, b in enumerate(vs) if j != i):
                s += 3 if sp[k].get('sig') else 2
    mejor = 0
    for i, a in enumerate(vs):
        sp = SOP.get(a['p']) or {}
        pts = sum((3 if sp[k].get('sig') else 2) for k in ('leader', 'leader2')
                  if sp.get(k) and any(aplica(sp[k], b) for j, b in enumerate(vs) if j != i))
        mejor = max(mejor, pts)
    s += mejor
    roles = {r for v in vs for r in v['r']}
    if len([r for r in ('Tanque', 'Control', 'Daño', 'Soporte') if r in roles]) >= 2: s += 1
    if len({v['c'] for v in vs}) == len(vs): s += 1
    le_gana = lambda c: next((k for k, x in ADV.items() if x.get(c) == 'normal'), None)
    for i, a in enumerate(vs):
        for j, b in enumerate(vs):
            am = le_gana(b['c'])
            if i != j and am and ADV[a['c']].get(am): s += 1
    return s

def cid(nombre): return next(c['id'] for c in C if c['name'] == nombre)
def uid(nombre, uni): return next(u['id'] for c in C if c['name'] == nombre for u in c['uniforms'] if u['name'] == uni)
WONG2 = f"{cid('Wong')}::{uid('Wong', 'Marvel Studios' + chr(39) + ' Doctor Strange 2')}"
EQUIPOS = [
    {'id': 'eq-1', 'name': 'Magia AB', 'modeId': 'alliance-battle', 'reason': '',
     'members': [f"{cid('Doctor Strange')}::base", f"{cid('Clea')}::base", WONG2]},
    {'id': 'eq-2', 'name': 'Arena', 'modeId': 'team-battle-arena', 'reason': '',
     'members': [f"{cid('Captain America')}::base", f"{cid('Iron Man')}::base", f"{cid('Thor')}::base"]},
    {'id': 'eq-3', 'name': 'Dúo', 'modeId': '', 'reason': '', 'members': [f"{cid('Hulk')}::base", f"{cid('She-Hulk')}::base"]},
    {'id': 'eq-4', 'name': 'Conquista', 'modeId': 'alliance-conquest', 'reason': '',
     'members': [f"{cid(n)}::base" for n in ('Spider-Man', 'Black Widow', 'Hawkeye', 'Vision', 'Scarlet Witch', 'Captain Marvel')]},
]
import auditoria_equipos as A
import modelo_foco as F
def como_entra(v, tt):
    """Mejor lugar entre los que lo dejan vinculado con alguien del equipo (None si no hay)."""
    vs = [A.VAR[k] for k in sorted(tt['members'])]; va = A.VAR[v['key']]    # la capa los guarda en orden canónico
    ops = [(x, vs[:i] + [va] + vs[i + 1:], i) for i, x in enumerate(vs)]
    if len(vs) < TAM.get(tt['modeId'], 3): ops.append((None, vs + [va], len(vs)))
    validas = [o for o in ops if len(A.sueltos(o[1], o[2])) < len(o[1]) - 1]
    if not validas: return None
    # el de más puntos; a igual puntaje, el de más strikers (desempatan); después el primero, como el sort estable de la app
    best = max(validas, key=lambda o: (A.score(o[1]), F.stk_foco(o[1], None)))
    return dict(antes=A.score(vs), despues=A.score(best[1]), sale=VAR[best[0]['key']] if best[0] else None,
                delta=A.score(best[1]) - A.score(vs))

D = carpeta_datos()
json.dump({'teams': EQUIPOS}, open(os.path.join(D, 'capa.json'), 'w', encoding='utf-8'), ensure_ascii=False)
srv, url = levantar(D, origen_local())
v = VAR[WONG2]
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.fill('#q', 'Wong'); pg.wait_for_timeout(250)
        pg.click(f'.ccard[data-cid="{v["cid"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.select_option('select[data-a="uniformSel"]', v['uid'])
        t0 = time.time(); pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('.eqsug'); dt = time.time() - t0
        ok('pestaña Equipos: aparece y calcula', True, f'{dt * 1000:.0f} ms desde el clic')

        secciones = pg.locator('#fcuerpo > .section')
        mios = secciones.nth(0)
        ok('en tus equipos: el que lo tiene', mios.locator('.card').count() == 1 and 'Magia AB' in mios.inner_text(), mios.locator('.card').count())

        # cómo entraría en los otros: contra el cálculo aparte
        otros = [tt for tt in EQUIPOS if not any(k.split('::')[0] == v['cid'] for k in tt['members'])]
        esp_todos = {tt['name']: como_entra(v, tt) for tt in otros}
        esp = {n: e for n, e in esp_todos.items() if e}
        sin_vinculo = [n for n, e in esp_todos.items() if not e]
        tarjetas = secciones.nth(1).locator('.eqsug')
        vistas = {}
        for i in range(tarjetas.count()):
            tx = tarjetas.nth(i).inner_text()
            nom = tarjetas.nth(i).locator('b').first.inner_text()
            desp = int(tarjetas.nth(i).locator('.eqpts b').inner_text())
            delta = int(tarjetas.nth(i).locator('.eqdelta').inner_text().replace('+', ''))
            antes = int(re.search(r'antes (-?\d+)', tx).group(1))
            m = re.search(r'en lugar de (.+)', tx)
            vistas[nom] = dict(antes=antes, despues=desp, delta=delta, sale=m.group(1).strip() if m else None)
        coinciden = all(vistas[n]['antes'] == e['antes'] and vistas[n]['despues'] == e['despues'] and vistas[n]['delta'] == e['delta']
                        and vistas[n]['sale'] == (full(e['sale']) if e['sale'] else None) for n, e in esp.items() if e['delta'] > 0)
        ok('cómo entraría: mismos equipos, quién sale y puntajes que el cálculo aparte',
           set(vistas) == {n for n, e in esp.items() if e['delta'] > 0} and coinciden,
           {n: (e['antes'], e['despues'], full(e['sale']) if e['sale'] else 'suma') for n, e in esp.items()})
        no_mejoran = [n for n, e in esp.items() if e['delta'] <= 0]
        tx1 = secciones.nth(1).inner_text()
        ok('los que no mejoran quedan en una línea', all(n in tx1 for n in no_mejoran), no_mejoran)
        linea = next((l for l in tx1.split('\n') if l.startswith('Sin vínculo con nadie')), '')
        ok('los que no tienen vínculo con nadie del equipo, en la suya', all(n in linea for n in sin_vinculo) and bool(linea) == bool(sin_vinculo),
           (sin_vinculo, linea))

        # botón: lleva el equipo a la mesa (1.0.25), con el líder primero
        card = secciones.nth(1).locator('.eqsug').first
        esperado = [f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in card.locator('.eqfoto').all()]
        card.locator('[data-a="teamDesde"]').click(); pg.wait_for_timeout(300)
        nombre = pg.locator('[data-a="mesaNombre"]').input_value()
        marcados = pg.evaluate("[...document.querySelectorAll('.mesa .mslot:not(.libre) .msfoto')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base'))")
        ok('Llevar a la mesa: el nombre y los integrantes, el líder primero, sin salir de la ficha', 'con Wong' in nombre and
           marcados == esperado and pg.locator('.fcab').count() == 1, (nombre, esperado, marcados))
        pg.click('[data-a="mesaGuardar"]'); pg.wait_for_timeout(600)
        guardado = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))['teams'][0]
        ok('guardarlo crea un equipo nuevo con esos integrantes, en orden canónico', guardado['members'] == sorted(esperado) and guardado['name'] == nombre,
           (guardado['name'], guardado['members']))
        # El mismo equipo otra vez (desde la misma tarjeta, con los integrantes en otro orden): no se repite y se dice.
        cuantos = len(json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))['teams'])
        pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
        pg.fill('#q', 'Wong'); pg.wait_for_timeout(250)
        pg.click(f'.ccard[data-cid="{v["cid"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.select_option('select[data-a="uniformSel"]', v['uid'])
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('.eqsug')
        otra = pg.locator('#fcuerpo > .section').nth(1).locator('.eqsug').first
        ok('la misma tarjeta de antes', sorted(f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in otra.locator('.eqfoto').all())
           == sorted(esperado))
        otra.locator('[data-a="teamDesde"]').click(); pg.wait_for_timeout(300)
        pg.click('[data-a="mesaGuardar"]'); pg.wait_for_timeout(600)
        aviso = pg.locator('.mesa .avisoeq').all_inner_texts()
        ok('guardar el mismo equipo otra vez: no se repite y se dice cuál es',
           len(json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))['teams']) == cuantos
           and aviso == [f'⚠ Ese equipo ya está guardado con este modo y este líder: «{nombre}».'], aviso)

        ok('sin errores de página', not errores, errores[:3])
        b.close()

        # celular con equipos: nada se sale de la columna (nombres de uniforme largos incluidos)
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        fuera = {}
        for nombre, uni in (('Wong', v['uid']), ('Falcon', None)):
            c = next(c for c in C if c['name'] == nombre)
            u = uni or max(c['uniforms'], key=lambda x: len(x['name']))['id']
            pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
            pg.fill('#q', nombre); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{c["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
            pg.select_option('select[data-a="uniformSel"]', u)
            pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('.eqsug')
            fuera[nombre] = pg.evaluate(FUERA)
        ok('celular con equipos: nada se sale de la columna', not any(fuera.values()), fuera)
        b.close()

        # sin equipos + celular
        D2 = carpeta_datos()
        srv2, url2 = levantar(D2, origen_local())
        try:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
            pg.on('pageerror', lambda e: errores.append(str(e)))
            pg.goto(url2); pg.wait_for_selector('.ccard')
            pg.fill('#q', 'Wong'); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{v["cid"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
            vis = pg.evaluate("[...document.querySelectorAll('.ftab')].every(t => { const r = t.getBoundingClientRect(); return r.right <= 390 && r.left >= 0; })")
            ok('celular: las 5 pestañas a la vista', vis and pg.locator('.ftab').count() == 5)
            pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#fcuerpo .section')
            tx = pg.locator('#fcuerpo').inner_text()
            pg.wait_for_selector('#combos .combo', timeout=60000)
            ok('sin equipos: lo explica y muestra las combinaciones', 'Todavía no armaste equipos' in tx and pg.locator('#combos .combo').count() == 20,
               pg.locator('#combos .combo').count())
            ancho = pg.evaluate("document.documentElement.scrollWidth")
            ok('celular: sin desborde', ancho <= 390 and not pg.evaluate(FUERA), (ancho, pg.evaluate(FUERA)))
            pg.screenshot(path=f'{SALIDA}/equipos_390.png', full_page=True)
            ok('sin errores de página (celular)', not errores, errores[:3])
            b.close()
        finally:
            srv2.terminate(); srv2.wait()
finally:
    srv.terminate(); srv.wait()
ok.fin()
