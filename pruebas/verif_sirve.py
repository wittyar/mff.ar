"""Un liderazgo o un soporte suma solo si le sirve a quien lo recibe (1.0.9): los que suben un
ataque o un daño elemental, solo a quien pega con eso en sus skills activas. Caso reportado:
Abomination — Infected Bioweapon (daño físico) con Satana — Ascended One de líder (daño de
fuego +70%). Contra el modelo escrito aparte (auditoria_equipos.py / modelo_foco.py).
Carril J: lo que le da Satana se lee del desglose del «Por qué» (antes, de sus renglones de texto).
Carril modal (5 de octubre de 2026): de la tabla de lo que recibe él, en su pestaña de la ventana del «Por qué»."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright
import auditoria_equipos as A
import modelo_foco as F

ok = Chequeo()
C = datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS']
def full(v): return v['name'] + (' — ' + next(u['name'] for c in C if c['id'] == v['cid'] for u in c['uniforms'] if u['id'] == v['uid']) if v['uid'] else '')
def lider(vs):
    """El líder del equipo (4 de octubre de 2026): el mismo desde la lista de cualquiera y en cualquier orden."""
    i = A.lider_sin_contexto(vs)
    return None if i is None else vs[i]
def con_lider(vs, l): return [l] + [x for x in vs if x is not l] if l else vs
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
def leer_pagina(pg):
    out = []
    for c in pg.locator('#combos .combo').all():
        keys = [f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in c.locator('.eqfoto').all()]
        out.append((keys, int(c.locator('.eqpts > b').inner_text()), c.locator('.combolider').inner_text()))
    return out
def esperado(v, fv):
    """Cada tarjeta: sus claves como se pintan (el líder primero), los puntos para él y el líder."""
    return [([x['key'] for x in con_lider([v, a, b], l)], p, f'Líder: {full(l)}' if l else 'Ningún liderazgo le suma')
            for a, b, p in fv[:20] for l in [lider([v, a, b])]]
def cuenta(pg): return int(re.sub(r'\D', '', pg.locator('#combos .row > span.muted').first.inner_text().split('·')[0]) or 0)
def porque(pg, keys, foco):
    """Lo que recibe foco en la ventana del «Por qué» de esa tarjeta (la tabla de su pestaña): [(efecto, [de dónde])]."""
    c = next(c for c in pg.locator('#combos .combo').all()
             if [f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in c.locator('.eqfoto').all()] == keys)
    c.locator('[data-a="pqAbrir"]').click(); pg.wait_for_selector('#pqdlg[open]')
    filas = pg.evaluate("""(k) => { const d = document.getElementById('pqdlg'), tab = d.querySelector(`[role="tab"][data-key="${k}"]`);
      return [...d.querySelector('#' + tab.getAttribute('aria-controls')).querySelectorAll('.pqm-tabla > .pqm-fila:not(.pqm-th)')]
        .map(f => [f.querySelector('.pqm-ef').textContent.replace(/\\s+/g, ' ').trim(),
                   [...f.querySelectorAll('.pqm-de1 > span:last-child')].map(x => x.textContent.replace(/\\s+/g, ' ').trim())]); }""", foco)
    pg.keyboard.press('Escape'); pg.wait_for_selector('#pqdlg', state='hidden')
    return filas

# 0. Todos los efectos de soporte de los datos tienen su regla en el catálogo (MFF_CATALOGO.soporte, formato 7; antes,
#    PIDE y PARA_TODOS de app.js): ninguno cae en «sin clasificar». Los de los bonos de equipo que el catálogo no tiene
#    se listan (la app los cuenta para todos y lo dice; la auditoría, sección 9).
D = datos_js('MFF_SOPORTES', 'MFF_CATALOGO', 'MFF_BONOS')
SOP, REGLAS = D['MFF_SOPORTES'], D['MFF_CATALOGO']['soporte']
stats = {f['s'] for sp in SOP.values() for x in sp.values() if isinstance(x, dict) and 'fx' in x for f in x['fx']}
ok('0 todos los efectos de los datos tienen su regla en el catálogo', stats <= set(REGLAS) and all('sirve' in x for x in REGLAS.values()),
   (sorted(stats - set(REGLAS)), len(stats), len(REGLAS)))
de_bonos = {st for b in D['MFF_BONOS'] for v in b['v'] for st, _ in v}
print('stats de bonos sin regla en el catálogo (cuentan para todos):', sorted(de_bonos - set(REGLAS)))
abo = next(v for v in A.TODAS if v['p'] == 'abomination1')
t0 = time.time(); pool, filas = consulta(abo); fv = vista(pool, filas)
print(f'modelo: {len(fv)} combinaciones ({time.time() - t0:.1f} s)')
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.fill('#q', 'Abomination'); pg.wait_for_timeout(250)
        pg.click(f'.ccard[data-cid="{abo["cid"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.select_option('select[data-a="uniformSel"]', abo['uid'])
        t0 = time.time(); pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
        dt = time.time() - t0
        ok('1 Abomination — Infected Bioweapon: misma cantidad y primera página que el modelo', cuenta(pg) == len(fv) and leer_pagina(pg) == esperado(abo, fv),
           f'{len(fv)} combinaciones, {dt * 1000:.0f} ms')
        # 2. Satana no le sirve en nada y él no le da nada a ella: no hay tríos con ella
        sat = [x for x in A.TODAS if x['cid'] == 'satana']
        ok('2 modelo: ningún uniforme de Satana tiene vínculo útil con él', not any(a['cid'] == 'satana' or b_['cid'] == 'satana' for a, b_, _ in fv))
        pg.select_option('select[data-a="eqCon"]', 'satana'); pg.wait_for_timeout(200)
        ok('2 «Con Satana»: ninguna combinación', pg.locator('#combos .combo').count() == 0 and 'Ninguna combinación con estos filtros.' in pg.locator('#combos').inner_text())
        # 3. Comparar Doctor Strange (líder: ataque de energía + ignorar evasión) con Abomination —
        #    Infected Bioweapon (pega físico) e Iron Man (pega con energía): a cada uno, lo suyo. (Con Captain Marvel,
        #    desde el 4 de octubre de 2026 lidera ella: empata con él en puntos y está mejor en la General.)
        def elegir(nombre, uid=''):
            pg.fill('#q', nombre); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{A.VAR[nombre_a_clave[nombre]]["cid"]}"][data-uid="{uid}"]'); pg.wait_for_timeout(150)
        nombre_a_clave = {'Abomination': abo['key'], 'Iron Man': 'iron-man::base'}
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        pg.fill('#q', 'Doctor Strange'); pg.wait_for_timeout(250)
        pg.click('.ccard[data-cid="doctor-strange"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="pickThis"]'); pg.wait_for_selector('#q')
        elegir('Abomination', abo['uid']); elegir('Iron Man')
        pg.click('[data-a="goCompare"]'); pg.wait_for_timeout(300)
        lineas = [x.inner_text() for x in pg.locator('.card', has=pg.locator('h3', has_text='Sinergia estimada')).locator('li').all()]
        lid = [l for l in lineas if 'de líder' in l]
        ok('3 comparar: el líder es Doctor Strange y hay una línea para cada uno', len(lid) == 2 and all(l.startswith('Con Doctor Strange de líder →') for l in lid), lineas)
        l_abo = [l for l in lid if full(abo) in l]
        l_cm = [l for l in lid if 'Iron Man' in l.split('→')[1]]
        ok('3 a Abomination (pega físico) solo «Ignorar esquiva»', l_abo and 'Ignorar esquiva' in l_abo[0] and 'Ataque de energía' not in l_abo[0], l_abo)
        ok('3 a Iron Man (pega con energía) las dos', l_cm and 'Ignorar esquiva' in l_cm[0] and 'Ataque de energía' in l_cm[0], l_cm)
        # salir del modo comparar (si no, tocar una tarjeta la elige en vez de abrirla)
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(150)
        # 4. Los que sí pegan con fuego (los ejemplos del usuario): Satana les sirve de líder
        for nombre, uni in [('Human Torch', ''), ('Red Hulk', 'Symbiote of Vengeance'), ('Sun Bird', ''), ('Jean Grey', '')]:
            ch = next(c for c in C if c['name'] == nombre)
            uid = next(u['id'] for u in ch['uniforms'] if u['name'] == uni) if uni else ''
            v = A.VAR[f"{ch['id']}::{uid or 'base'}"]
            pv, fv2 = consulta(v)
            fs = vista(pv, fv2, con='satana')
            pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
            pg.fill('#q', nombre); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{ch["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
            if uid: pg.select_option('select[data-a="uniformSel"]', uid)
            pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
            pg.select_option('select[data-a="eqCon"]', 'satana'); pg.wait_for_timeout(200)
            app = leer_pagina(pg)
            lineas = porque(pg, app[0][0], v['key'])
            # lo que Satana le da a él en la primera combinación: de líder, daño de fuego; de
            # soporte (su efecto de uniforme), daño de todos los elementos
            de_satana = [(ef, d) for ef, des in lineas for d in des if d.startswith('Satana: ')
                         and (ef.startswith('Daño de fuego') and d.endswith(' +70%') or ef.startswith('Daño de todos los elementos') and d.endswith(' +35%'))]
            ok(f'4 {full(v)} (pega con fuego): con Satana hay combinaciones, igual que el modelo, y lo de Satana le suma',
               len(fs) > 0 and app == esperado(v, fs) and de_satana, (len(fs), app[0][2], de_satana))
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
