"""Las habilidades iguales no se solapan (carril filtro2, 5 de octubre de 2026). Ezequiel: «Apocalipsis da antimermas a
mutantes... Y deadpool da antimermas. El juego no permite el solapado de habilidades iguales... por lo que el antimermas de
apocalipsis y el de deadpool solo va a funcionar uno». Un efecto sin valor que a un integrante le llega de dos fuentes se le
aplica una vez: lo propio, después el liderazgo del líder y después el primer soporte en el orden del equipo (el líder
primero, los demás por clave); la otra fuente no suma y se ve atenuada, con de dónde ya lo tiene.
1. El trío de la captura en PvP (Deadpool — Deadpool & Wolverine, Apocalypse — X-Men '97, Wolverine — Deadpool & Wolverine),
   desde la lista de Deadpool, en la ventana: lidera Deadpool; anti-mermas, quién cubre a cada uno; «Apocalypse: Pasiva 4★ →
   Wolverine (Deadpool ya lo tiene de su liderazgo)»; en la pestaña de Deadpool, el anti-mermas de Apocalypse atenuado («no
   se suma: ya lo tiene de su liderazgo») y el suyo no; en la de Apocalypse, lo que aporta con Deadpool atenuado; los puntos
   como el modelo aparte (modelo_ctx). Capturas: shots/solapado_pvp_1300.png, solapado_deadpool_1300.png y _390.
2. El mismo trío sin contexto: lidera Apocalypse y a Deadpool se le aplica la pasiva de Apocalypse (nada atenuado).
3. Un soporte que no se le aplica a nadie no suma (PvP: Thanos — Annihilation lidera con anti-mermas para todos, y la pasiva
   de Sleeper «no suma»); el puntaje como el modelo.
4. Lo propio de las skills gana: Nick Fury — Secret Avengers (propio, de sus skills) no suma el efecto de uniforme de Angel; en
   PvP, Knull — Ancient History no suma el liderazgo de Gorr (ya lo tiene propio, de su Pasiva de Tier-2).
5. Dos soportes de otros al líder (Red Hulk — Red Hulk Avengers... con Wasp y Silver Surfer (Shalla-Bal)): el primero por clave
   se aplica; las 6 permutaciones dan lo mismo (líder, puntajes, lo atenuado).
6. Un liderazgo sin contexto que solo da lo que los demás ya tienen no suma: Molecule Man con Knull — Ancient History y Nick
   Fury — Secret Avengers.
7. Modelo aparte (auditoria_equipos, modelo_foco, modelo_ctx, con la regla escrita allá): 3.000 tríos con dos o tres que
   traen algo sin valor (sinergia del equipo, puntos para cada uno, líder, PvP y PvE).
8. Inglés y celular (390 px, la ventana sin desborde). Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
import auditoria_equipos as A, modelo_foco as F, modelo_ctx as M
from analisis_haz import VAR

ok = Chequeo()
SH = SALIDA
DP, AP, WO = 'deadpool::deadpool-10800164', 'apocalypse::apocalypse-10300141', 'wolverine::wolverine-10700125'
THANOS, SLEEPER, CARNAGE = 'thanos::thanos-10700075', 'sleeper::base', 'carnage::carnage-10200072'
FURY, ANGEL, FALCON = 'nick-fury::nick-fury-10300185', 'angel::angel-10300159', 'falcon::falcon-10200030'
VK, KNULL, GORR = 'silver-surfer::silver-surfer-10200199', 'knull::knull-10100241', 'gorr::gorr-10100253'
RH, WASP, SB = 'red-hulk::red-hulk-10300025', 'wasp::wasp-10300051', 'silver-surfer-shalla-bal::base'
MM = 'molecule-man::base'

GANCHO_FIN = '\narrancar();\n})();'
def gancho(route):
    r = route.fetch(); src = r.text()
    if GANCHO_FIN not in src: raise SystemExit('app.js no termina como se esperaba')
    route.fulfill(response=r, body=src.replace(GANCHO_FIN, '\nwindow.__ev = s => eval(s);' + GANCHO_FIN))

# Lo que dice la ventana del «Por qué» de un trío (pqHtml de pqDatos, lo mismo que pinta el botón), leído con el DOM: las
# partes de los puntos (rótulo, viñetas), y de cada integrante lo que recibe (cada parte de «De dónde», con si va atenuada)
# y lo que aporta.
VENTANA = r"""([ctx, keys]) => {
  const pl = (el) => el ? el.textContent.replace(/\s+/g, ' ').trim() : null;
  const d = document.createElement('div'), id = 'c|' + (ctx || '') + '|' + keys.join(','), datos = pqDatos(id);
  d.innerHTML = pqHtml({ id, tab: null }, datos);
  const partes = [...d.querySelectorAll('.pqm-parte')].map(p => [pl(p.querySelector('.pqm-parteh')), [...p.querySelectorAll(':scope > ul.pqm-lista > li')].map(pl)]);
  const tabs = {};
  for (const tab of d.querySelectorAll('[role="tab"]')) {
    const panel = d.querySelector('#' + tab.getAttribute('aria-controls'));
    tabs[tab.dataset.key] = {
      recibe: [...panel.querySelectorAll('.pqm-tabla > .pqm-fila:not(.pqm-th)')].map(f => ({ fila: pl(f.querySelector('.pqm-ef')), rep: f.classList.contains('rep'),
        de: [...f.querySelectorAll('.pqm-de1')].map(x => [pl(x), x.classList.contains('rep')]) })),
      aporta: [...panel.querySelectorAll(':scope > ul.pqm-lista > li')].map(pl) };
  }
  return { lider: datos.lider && datos.lider.key, e: datos.e && { score: datos.e.score, partes: datos.e.partes }, partes, tabs,
           porque: pl(d.querySelector('.pqm-porque')) };
}"""
TRIOS = r"""(trios) => trios.map(ks => {
  const vs = ks.map(k => variant(...k.split('::')));
  const ctx = (c) => { const e = enContexto(vs, c); return e && [e.score, e.lider.key, [e.partes.lider, e.partes.dps, e.partes.sinergia, e.strikers]]; };
  const l = liderDe(vs, null);
  return { eq: synergy(vs).score, foco: vs.map(f => synergy(vs, { foco: f }).score), lider: l && l.key, pvp: ctx('pvp'), pve: ctx('pve') };
})"""
FUERA = """() => { const d = document.querySelector('#pqdlg'), lim = d.getBoundingClientRect().right;
  return [...d.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > lim + 0.5; })
    .map(e => (e.className || e.tagName) + ' → ' + Math.round(e.getBoundingClientRect().right)).slice(0, 4); }"""

def parte(v, rot): return next((vi for r, vi in v['partes'] if r.startswith(rot)), None)
def modelo_ctx(keys, c):
    m = M.evaluar([VAR[k] for k in keys], c)
    return None if m is None else (m[0], [VAR[k] for k in keys][m[1]]['key'], list(m[2]))

errores = []
def vigilar(pg, nombre):
    pg.on('pageerror', lambda e: errores.append(f'{nombre}: {e}'))
    pg.on('console', lambda m: m.type == 'error' and errores.append(f'{nombre} consola: {m.text}'))
def abrir_ficha_trio(pg, foco, otros, ctx):
    """La ficha de foco, pestaña Equipos, orden ctx, en la página de la tarjeta del trío; abre su «Por qué»."""
    cid, uid = foco.split('::')
    pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', 'Deadpool'); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid != 'base': pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(150)
    pg.click('[data-a="fichaTab"][data-v="equipos"]')
    pg.wait_for_function("k => window.__ev('CONSULTA && CONSULTA.clave') === k && !window.__ev('ui.eqCalculando')", arg=foco, timeout=120000)
    pg.select_option('#combos select[data-a="eqOrden"]', ctx); pg.wait_for_timeout(300)
    n = pg.evaluate("""([a, b]) => window.__ev(`(() => { const q = CONSULTA, f = vistaConsulta(q).filas;
      const n = f.findIndex(i => [q.pool[q.A[i]].key, q.pool[q.B[i]].key].sort().join('|') === ${JSON.stringify([a, b].sort().join('|'))});
      if (n >= 0) { ui.eqPagina = Math.floor(n / POR_PAGINA); render(); } return n; })()`)""", otros)
    # La lista va con el mejor uniforme de cada pareja: si el trío está, se abre con su botón; si va con otros uniformes, como lo
    # abre el botón (abrirPq, con la tarjeta de ese trío).
    boton = pg.locator(f'#combos [data-a="pqAbrir"][data-pq*="{otros[0]}"][data-pq*="{otros[1]}"]')
    if n >= 0 and boton.count(): boton.first.click()
    else: pg.evaluate("id => window.__ev(`abrirPq({ id: ${JSON.stringify(id)}, charId: ui.charId, uid: ui.uniformId, tab: null, y: 0 })`)",
                      f'c|{ctx}|' + ','.join([foco] + otros))
    pg.wait_for_selector('#pqdlg[open]')
    return n

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1300, 'height': 900}); vigilar(pg, 'es')
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)
        ven = lambda ctx, ks: pg.evaluate('([js, a]) => window.__ev(js)(a)', [VENTANA, [ctx, ks]])

        # 1. el trío de la captura, en PvP
        pg.set_default_timeout(120000)
        v = ven('pvp', [DP, AP, WO])
        anti, sop = parte(v, 'Anti-mermas'), parte(v, 'Soportes y bonos de equipo')
        ok('1 PvP: lidera Deadpool (su liderazgo suma 10,5)', v['lider'] == DP and v['porque'].startswith('Lidera Deadpool: su liderazgo suma 10,5'), v['porque'])
        ok('1 anti-mermas, quién cubre a cada uno: Deadpool, su liderazgo; Apocalypse y Wolverine, la pasiva de Apocalypse',
           anti == ['Deadpool (liderazgo) → Deadpool', 'Apocalypse (soporte) → Apocalypse, Wolverine'], anti)
        ok('1 «Apocalypse: Pasiva 4★ → Wolverine (Deadpool ya lo tiene de su liderazgo)», y suma: a Wolverine se le aplica',
           sop and sop[0] == 'Apocalypse: Pasiva 4★ → Wolverine (Deadpool ya lo tiene de su liderazgo)' and 'no suma' not in sop[0], sop)
        rd = v['tabs'][DP]['recibe']
        rad = [f for f in rd if f['fila'].startswith('Elimina todas las mermas')]
        ok('1 Deadpool, lo que recibe: su anti-mermas (Liderazgo secundario) se aplica y el de Apocalypse va atenuado, «no se suma: ya lo tiene de su liderazgo»',
           len(rad) == 2 and rad[0]['de'] == [['Deadpool: Liderazgo (secundario)', False]] and not rad[0]['rep']
           and rad[1]['de'] == [['Apocalypse: Pasiva 4★ (no se suma: ya lo tiene de su liderazgo)', True]] and rad[1]['rep'], rad)
        ok('1 Deadpool: lo demás que recibe, sin atenuar', all(not x[1] for f in rd if not f['fila'].startswith('Elimina todas las mermas') for x in f['de']), rd)
        ok('1 Wolverine y Apocalypse: su anti-mermas (la pasiva de Apocalypse) se aplica',
           all(not x[1] for k in (AP, WO) for f in v['tabs'][k]['recibe'] for x in f['de']), [v['tabs'][k]['recibe'] for k in (AP, WO)])
        ok('1 Apocalypse, lo que aporta: «Pasiva 4★ → Wolverine (Deadpool ya lo tiene de su liderazgo)»',
           v['tabs'][AP]['aporta'][0].startswith('Pasiva 4★ → Wolverine (Deadpool ya lo tiene de su liderazgo)'), v['tabs'][AP]['aporta'])
        m = modelo_ctx([DP, AP, WO], 'pvp')
        ok(f'1 los puntos de PvP, como el modelo aparte: {m[0]} (liderazgo, DPS y soportes y bonos: {m[2][:3]})',
           v['e']['score'] == m[0] and [v['e']['partes'][k] for k in ('lider', 'dps', 'sinergia')] == m[2][:3], (v['e'], m))
        abrir_ficha_trio(pg, DP, [AP, WO], 'pvp')
        dlg = pg.locator('#pqdlg')
        os.makedirs(SH, exist_ok=True)
        pg.evaluate("document.querySelector('#pqdlg .pqm-cuerpo').scrollTop = document.querySelector('#pqdlg .pqm-sec').offsetTop - 10")
        dlg.screenshot(path=f'{SH}/solapado_pvp_1300.png')
        ok('1 en pantalla: la ventana del trío, desde la lista de PvP de Deadpool, dice lo mismo',
           'Apocalypse: Pasiva 4★ → Wolverine (Deadpool ya lo tiene de su liderazgo)' in dlg.inner_text().replace('\n', ' ')
           and dlg.locator('.pqm-de1.rep').count() == 1, dlg.inner_text()[:300])
        pg.evaluate("document.querySelector('#pqdlg .pqm-tabla').scrollIntoView({ block: 'center' })")
        dlg.screenshot(path=f'{SH}/solapado_deadpool_1300.png')
        pg.keyboard.press('Escape')

        # 2. el mismo trío sin contexto
        v = ven(None, [DP, AP, WO])
        ok('2 sin contexto: lidera Apocalypse y a Deadpool se le aplica la pasiva de Apocalypse (nada atenuado)',
           v['lider'] == AP and not any(x[1] for t in v['tabs'].values() for f in t['recibe'] for x in f['de'])
           and not any('ya lo tiene' in l for _, vi in v['partes'] for l in vi), v['partes'])

        # 3. un soporte que no suma (PvP)
        v = ven('pvp', [THANOS, SLEEPER, CARNAGE])
        sop = parte(v, 'Soportes y bonos de equipo') or []
        linea = next((l for l in sop if l.startswith('Sleeper: ') and l.endswith('no suma')), '')
        m = modelo_ctx([THANOS, SLEEPER, CARNAGE], 'pvp')
        ok('3 PvP, Thanos de líder: la pasiva secundaria de Sleeper no le suma a nadie («no suma») y dice de dónde ya lo tienen',
           v['lider'] == THANOS and linea.endswith('no suma') and 'Carnage ya lo tiene del liderazgo de Thanos' in linea, linea)
        ok(f'3 el puntaje sin ese soporte, como el modelo: {m[0]}', v['e']['score'] == m[0] and v['e']['partes']['sinergia'] == m[2][2], (v['e'], m))

        # 4. lo propio de las skills gana
        v = ven(None, [FURY, ANGEL, FALCON])
        filas = [x for f in v['tabs'][FURY]['recibe'] for x in f['de'] if x[1]]
        ok('4 Nick Fury — Secret Avengers: el efecto de uniforme de Angel va atenuado, «ya lo tiene propio (…)» (de sus skills)',
           filas and all(x[0].startswith('Angel: ') and '(no se suma: ya lo tiene propio (' in x[0] for x in filas), filas)
        v = ven('pvp', [VK, KNULL, GORR])
        filas = [x for f in v['tabs'][KNULL]['recibe'] for x in f['de'] if x[1]]
        ok('4 PvP, Knull — Ancient History: el liderazgo de Gorr no le suma el anti-mermas, «ya lo tiene propio (Pasiva T2)», y lo cubre lo propio',
           v['lider'] == GORR and len(filas) == 1 and filas[0][0].startswith('Gorr: Liderazgo')
           and filas[0][0].endswith('(no se suma: ya lo tiene propio (Pasiva T2))') and 'Knull (propio: Pasiva T2) → Knull' in parte(v, 'Anti-mermas'),
           (filas, parte(v, 'Anti-mermas')))

        # 5. dos soportes de otros al líder, en las 6 permutaciones
        perms = [[RH, WASP, SB], [RH, SB, WASP], [WASP, RH, SB], [WASP, SB, RH], [SB, RH, WASP], [SB, WASP, RH]]
        vs6 = [ven(None, ks) for ks in perms]
        rep = lambda v: sorted((k, x[0]) for k, t in v['tabs'].items() for f in t['recibe'] for x in f['de'] if x[1])
        ok('5 Red Hulk de líder: la pasiva de Silver Surfer (Shalla-Bal) se le aplica (primero por clave) y la de Tier-2 de Wasp va atenuada; '
           'a Wasp y a Silver Surfer, el del otro no se les suma (cada uno tiene el suyo propio)',
           vs6[0]['lider'] == RH and rep(vs6[0]) == [(RH, 'Wasp: Pasiva de Tier-2 (no se suma: ya lo tiene de Silver Surfer (Shalla-Bal) (Pasiva 4★))'),
                                                   (SB, 'Wasp: Pasiva de Tier-2 (no se suma: ya lo tiene propio (Pasiva 4★))'),
                                                   (WASP, 'Silver Surfer (Shalla-Bal): Pasiva 4★ (no se suma: ya lo tiene propio (Pasiva de Tier-2))')], rep(vs6[0]))
        # El «Por qué» de una combinación cuenta los puntos para el primero (el de la ficha): entre permutaciones con otro primero, lo
        # que no depende de eso (el líder, lo atenuado y los puntajes del equipo, de PvP y de PvE); con el mismo primero, también
        # las partes de los puntos (cada línea como el conjunto de sus palabras: los integrantes van en el orden del trío).
        eqs = [(e['eq'], e['lider'], e['pvp'], e['pve'], sorted(zip(ks, e['foco'])))
               for ks, e in zip(perms, pg.evaluate('([js, a]) => window.__ev(js)(a)', [TRIOS, perms]))]
        canon = lambda l: sorted(l.replace('(', ' ').replace(')', ' ').replace(';', ' ').replace(',', ' ').split())
        lineas = lambda x: sorted((r, sorted(canon(l) for l in vi)) for r, vi in x['partes'])
        ok('5 las 6 permutaciones: el mismo líder, lo mismo atenuado y los mismos puntajes del equipo, de PvP y de PvE; con Red Hulk '
           'primero en las dos, las mismas partes de los puntos',
           all(x['lider'] == vs6[0]['lider'] and rep(x) == rep(vs6[0]) for x in vs6) and all(e == eqs[0] for e in eqs)
           and lineas(vs6[0]) == lineas(vs6[1]), (eqs[0], [x['lider'] for x in vs6]))
        # 6. un liderazgo que no suma (sin contexto)
        v = ven(None, [MM, KNULL, FURY])
        lid = parte(v, 'Liderazgo de Molecule Man')
        ok('6 Molecule Man de líder: su liderazgo secundario (anti-mermas para todos) no suma: Knull y Nick Fury ya lo tienen propio',
           v['lider'] == MM and lid and any(l.endswith('no suma') and 'Knull ya lo tiene propio' in l and 'Nick Fury ya lo tiene propio' in l for l in lid), lid)

        # 7. contra los modelos aparte: tríos con dos o tres que traen algo que no se acumula
        sv = [k for k, x in VAR.items() if any(A.NO_ACUM[id(sp)] for sp in (A.SOP.get(x['p']) or {}).values() if isinstance(sp, dict) and 'fx' in sp)
              or A.anti_propio(x)[0]]
        r = random.Random(5); todos = list(VAR)
        trios = []
        while len(trios) < 3000:
            ks = [r.choice(sv), r.choice(sv), r.choice(sv if len(trios) % 2 else todos)]
            if len({VAR[k]['cid'] for k in ks}) == 3: trios.append(ks)
        pg.set_default_timeout(0)
        R = pg.evaluate('([js, a]) => window.__ev(js)(a)', [TRIOS, trios])
        pg.set_default_timeout(120000)
        mal = {'eq': [], 'foco': [], 'lider': [], 'pvp': [], 'pve': []}
        for ks, x in zip(trios, R):
            vs = [VAR[k] for k in ks]
            li = A.lider_sin_contexto(vs)
            if x['eq'] != A.score(vs): mal['eq'].append((ks, x['eq'], A.score(vs)))
            if x['foco'] != [F.score_foco(vs, f) for f in range(3)]: mal['foco'].append((ks, x['foco']))
            if x['lider'] != (None if li is None else vs[li]['key']): mal['lider'].append((ks, x['lider']))
            for c in ('pvp', 'pve'):
                mm = modelo_ctx(ks, c)
                if (x[c] and [x[c][0], x[c][1], x[c][2][:3]]) != (mm and [mm[0], mm[1], mm[2][:3]]): mal[c].append((ks, x[c], mm))
        ok(f'7 {len(trios)} tríos con algo sin valor ({len(sv)} variantes lo traen): la sinergia del equipo, los puntos para cada uno, el '
           'líder sin contexto y PvP y PvE, iguales que los modelos aparte', not any(mal.values()), {k: v[:2] for k, v in mal.items() if v})

        # 8. inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        v = ven('pvp', [DP, AP, WO])
        sop = parte(v, 'Supports and team bonuses') or []
        rad = [x for f in v['tabs'][DP]['recibe'] for x in f['de'] if x[1]]
        ok('8 inglés: «Apocalypse: 4★ Passive → Wolverine (Deadpool already has it from its own leadership)» y «not added: it already has it from its own leadership»',
           sop and sop[0] == 'Apocalypse: 4★ Passive → Wolverine (Deadpool already has it from its own leadership)'
           and rad == [['Apocalypse: 4★ Passive (not added: it already has it from its own leadership)', True]], (sop, rad))
        v = ven('pvp', [THANOS, SLEEPER, CARNAGE])
        linea = next((l for l in parte(v, 'Supports and team bonuses') or [] if l.startswith('Sleeper: ') and l.endswith('adds nothing')), '')
        ok('8 inglés: «adds nothing»', linea.endswith('adds nothing') and 'Carnage already has it from Thanos\'s leadership' in linea, linea)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        b.close()

        # celular
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True); vigilar(pg, 'celular')
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(120000)
        abrir_ficha_trio(pg, DP, [AP, WO], 'pvp')
        pg.evaluate("document.querySelector('#pqdlg .pqm-tabla').scrollIntoView({ block: 'center' })")
        ok('8 celular: la ventana, sin desborde', not pg.evaluate(FUERA), pg.evaluate(FUERA))
        pg.screenshot(path=f'{SH}/solapado_deadpool_390.png')
        b.close()
        ok('sin errores de página ni de consola (castellano, inglés y celular)', not errores, errores[:4])
finally:
    srv.terminate(); srv.wait()
ok.fin()
