"""1.0.15 + líder único: combinaciones por contexto (PvP, PvE) con las reglas de Ezequiel, contra el
modelo aparte (modelo_ctx.py, sin mirar app.js). Liderazgo (Ezequiel, 2 de octubre de 2026: «único +
condicional a la mitad»): 2 por stat que vale e integrante al que le llega y le sirve, 1 si solo le
llega por un slot que se activa con una condición (ac); el líder es el que más suma y, a igual puntaje,
el de menor puesto en el contexto y después la clave: el mismo en cualquier orden del trío. En PvP, las
defensas del liderazgo cuentan; sin función en el contexto, el foco no tiene lista.
Tabla de valor (4 de octubre de 2026, MFF_VALOR): los pesos salen de los datos (el modelo los lee y hace la
cuenta aparte); en PvP, vida 2,5, todos los ataques 2, todas las defensas 1,5, ignorar evasión 1 y efecto de
los debuffs 0,5, y el condicional a la mitad (la propuesta, que se comprueba acá). El detalle dice cuánto
suma cada línea del liderazgo, y la suma da el total de su renglón.
1. 3.000 tríos al azar: entra o no, puntaje, líder y cada parte, en los dos contextos.
2. Quién tiene función en cada contexto: las 888 variantes, igual que el modelo.
3. Lista completa de Knull — Ancient History, Black Cat — Queen in Black y Valeria Richards en los
   contextos en que tienen función: cantidad y las primeras 20 (personajes, uniformes y puntaje). El
   vínculo por el liderazgo es con el líder del contexto (carril Q, segunda parte).
4. Los casos de referencia de docs/MODELO.md: puntaje y líder de cada opción igual que el modelo, el
   líder de la tabla, y la que eligió Ezequiel gana por puntaje en los cuatro (en Thor PvP empataban
   27 a 27 con la 1.0.15; ahora el liderazgo de Silver Surfer — Void Knight es condicional: 27 a 21).
5. En la ficha: Thor base no tiene lista en PvP ni en PvE (el aviso, sin combinaciones y sin
   calcular la consulta); Silver Surfer (Shalla-Bal) sí en PvP (puntaje, líder, de dónde sale cada
   punto y la nota, con el condicional a la mitad y el líder único) y no en PvE (solo «Not for
   wbl»); en el celular, sin desborde; sin errores. El detalle marca «la mitad» en un liderazgo
   condicional (Silver Surfer — Void Knight con Thor y Gorr) y no en uno permanente (Thanos). (Carril J:
   el detalle va en un renglón por parte, con viñetas; se lee así. Carril modal, 5 de octubre de 2026: va en
   la ventana del «Por qué» de la tarjeta, y se lee de ahí; en el celular, la ventana tampoco desborda.)
6. El trío del caso (Silver Surfer — Void Knight, Knull — Ancient History, Gorr — The God Butcher), en
   PvP y en PvE: el mismo líder, total y partes en las 6 permutaciones y en la lista de cada foco con
   función en el contexto, igual que el modelo.
7. Líder único: el mismo líder, puntaje y partes en las 6 permutaciones, en los 3.000 tríos al azar y en
   300 tríos por contexto con empate de puntos entre candidatos (semilla 15: un DPS del contexto y dos
   variantes al azar, en orden al azar), igual que el modelo.
8. Sintético (no pasa en los datos): el mismo stat por un slot permanente y por uno condicional cuenta
   una vez, con el peso mayor. En una página aparte, al final, la app y el modelo con el mismo
   liderazgo agregado; las 6 permutaciones de cada trío, igual que el modelo."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
import auditoria_equipos as A
import modelo_foco as F
import modelo_ctx as M
from analisis_haz import VAR, TODAS, RANGO
ok = Chequeo()
SP = PRUEBAS
LISTAS = {'pvp': list(M.ROLES['pvp']), 'pve': list(M.ROLES['pve'])}
FOCOS = ['knull::knull-10100241', 'black-cat::black-cat-10400009', 'valeria-richards::base']
# Casos de referencia (docs/MODELO.md): [contexto, foco, el que eligió Ezequiel, el otro, cómo gana, líderes (cid) de la tabla]
CASOS = [['pvp', 'galactus::base', ['thanos::thanos-10700075', 'kang-the-conqueror::kang-the-conqueror-10100259'],
          ['black-cat::black-cat-10400009', 'wasp::wasp-10300051'], 'puntaje', ['thanos', 'wasp']],
         ['pve', 'thor::base', ['phil-coulson::phil-coulson-10200061', 'invisible-woman::invisible-woman-10300180'],
          ['crystal::crystal-10300114', 'mephisto::mephisto-10100244'], 'puntaje', ['invisible-woman', 'crystal']],
         ['pvp', 'thor::base', ['wasp::wasp-10300051', 'sentry::sentry-10200235'],
          ['silver-surfer::silver-surfer-10200199', 'gorr::gorr-10100253'], 'puntaje', ['wasp', 'silver-surfer']],
         ['pvp', 'jean-grey::jean-grey-10400124', ['black-cat::black-cat-10400009', 'invisible-woman::invisible-woman-10400180'],
          ['knull::knull-10100241', 'gorr::gorr-10100253'], 'puntaje', ['black-cat', 'jean-grey']]]
TRIO = ['silver-surfer::silver-surfer-10200199', 'knull::knull-10100241', 'gorr::gorr-10100253']
# Detalle: [contexto, trío, líder (cid), ¿condicional?]
DETALLE = [['pvp', ['thor::base', 'silver-surfer::silver-surfer-10200199', 'gorr::gorr-10100253'], 'silver-surfer', True],
           ['pvp', ['galactus::base', 'thanos::thanos-10700075', 'kang-the-conqueror::kang-the-conqueror-10100259'], 'thanos', False]]

# La propuesta de la tabla de valor (Ezequiel, 4 de octubre de 2026).
PROPUESTA = {'pvp': {'requisito': 'anti_mermas', 'condicional': 0.5, 'dps': 2, 'soporte': 1, 'bono': 1, 'strikers': 'desempate',
                     'liderazgo': [['HP', 2.5], ['All Basic Attacks', 2], ['All Basic Attacks (Stackable)', 2], ['All Basic Defenses', 1.5],
                                   ['Ignore Dodge', 1], ['All Debuffs Effect', 0.5]]},
             'pve': {'requisito': None, 'condicional': 0.5, 'dps': 2, 'soporte': 1, 'bono': 1, 'strikers': 'desempate',
                     'liderazgo': [[s, 2] for s in ('All Basic Attacks', 'All Basic Attacks (Stackable)', 'Physical Attack', 'Energy Attack',
                                   'Fire Damage', 'Fire Damage by % Fire Resist', 'Cold Damage', 'Lightning Damage', 'Poison Damage',
                                   'Mind Damage', 'All Element Damage', 'Basic Damage Dealt to Boss Types')]}}
tabla = {c: {**{k: v for k, v in x.items() if k != 'liderazgo'}, 'liderazgo': [[y['stat'], y['peso']] for y in x['liderazgo']]}
         for c, x in M.VALOR['contextos'].items()}
ok('la tabla de valor de los datos es la de Ezequiel, confirmada el 5 de octubre', tabla == PROPUESTA and M.VALOR['propuesta'] is False
   and M.VALOR['anti_mermas'] == ['Remove All Debuffs', 'Debuff Immunity'], tabla)
from harness import datos_js
TXT = datos_js('MFF_TXT')['MFF_TXT']
def num_es(x): return (f'{x:.2f}'.rstrip('0').rstrip('.')).replace('.', ',')

rnd = random.Random(14)
trios = []
while len(trios) < 3000:
    a, b, c = rnd.sample(TODAS, 3)
    if len({a['cid'], b['cid'], c['cid']}) == 3: trios.append([a['key'], b['key'], c['key']])

# 7. Tríos con empate de puntos entre candidatos (ahí decide el desempate), según el modelo.
def empatados(vs, c):
    cs = M.candidatos(vs, c)
    if len(cs) < 2: return None
    top = max(p for _, p in cs); ts = [i for i, p in cs if p == top]
    if len(ts) < 2: return None
    pm = min(M.puesto_ctx(vs[i]['key'], c) for i in ts)
    return 'clave' if sum(1 for i in ts if M.puesto_ctx(vs[i]['key'], c) == pm) >= 2 else 'puesto'
rnd2 = random.Random(15)
EMPATES = {}
for c in ('pvp', 'pve'):
    dpsc, EMPATES[c] = [x for x in TODAS if M.dps_de(x['key'], c)], []
    while len(EMPATES[c]) < 300:
        vs = [rnd2.choice(dpsc)] + rnd2.sample(TODAS, 2)
        if len({x['cid'] for x in vs}) < 3: continue
        rnd2.shuffle(vs)
        if empatados(vs, c): EMPATES[c].append([x['key'] for x in vs])
MUESTRA = trios + EMPATES['pvp'] + EMPATES['pve']

JS = r"""([trios, focos, casos, trio, detalle, muestra]) => {
  const porKey = new Map(allVariants().map(x => [x.key, x]));
  const res = (vs, c) => { const e = enContexto(vs, c);
    return e ? [e.score, e.lider.key, [e.partes.lider, e.partes.dps, e.partes.sinergia, e.strikers]] : null; };
  const P = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
  const ev = trios.map(ks => { const vs = ks.map(k => porKey.get(k)); return ['pvp', 'pve'].map(c => { const e = enContexto(vs, c);
    return e ? [e.score, vs.indexOf(e.lider), [e.partes.lider, e.partes.dps, e.partes.sinergia, e.strikers]] : null; }); });
  const funcion = Object.fromEntries(allVariants().map(x => [x.key, [tieneFuncion(x, 'pvp'), tieneFuncion(x, 'pve')]]));
  const listas = {};
  for (const k of focos) { const v = porKey.get(k); CONSULTA = null; const q = consultaCon(v);
    for (const c of ['pvp', 'pve']) { if (!tieneFuncion(v, c)) { listas[k + '|' + c] = null; continue; }
      ui.eqOrden = c; q.vista = null; const vi = vistaConsulta(q);
      listas[k + '|' + c] = [vi.filas.length, vi.filas.slice(0, 20).map(i => { const vs = [v, q.pool[q.A[i]], q.pool[q.B[i]]];
        return [vs[1].key, vs[2].key, enContexto(vs, c).score]; })]; } }
  // 6. El trío del caso: las 6 permutaciones y, desde cada foco con función, su fila en la lista
  //    (la de esa pareja de personajes: [puesto, de cuántas, variantes, resultado]).
  const trioR = {};
  for (const c of ['pvp', 'pve']) {
    const perms = P.map(p => res(p.map(i => porKey.get(trio[i])), c));
    const desde = trio.map(k => { const v = porKey.get(k);
      if (!tieneFuncion(v, c)) return null;
      CONSULTA = null; const q = consultaCon(v); ui.eqOrden = c; q.vista = null; const vi = vistaConsulta(q);
      const cids = trio.filter(x => x !== k).map(x => porKey.get(x).cid).sort().join('|');
      const n = vi.filas.findIndex(i => [q.pool[q.A[i]].cid, q.pool[q.B[i]].cid].sort().join('|') === cids);
      if (n < 0) return [0, vi.filas.length, null, null];
      const a = q.pool[q.A[vi.filas[n]]], b = q.pool[q.B[vi.filas[n]]];
      return [n + 1, vi.filas.length, [a.key, b.key], res([v, a, b], c)]; });
    trioR[c] = [perms, desde];
  }
  ui.eqOrden = 'foco'; CONSULTA = null;
  const refs = casos.map(([c, f, a, b]) => [a, b].map(par => res([f, ...par].map(k => porKey.get(k)), c)));
  // El detalle de la ventana del «Por qué»: [rótulo con lo que suma, [viñetas]] por parte.
  const pl = (el) => el.textContent.replace(/\s+/g, ' ').trim();
  const det = detalle.map(([c, ks]) => { const vs = ks.map(k => porKey.get(k)), d = document.createElement('div');
    d.innerHTML = detalleContexto(enContexto(vs, c, true), vs, c);
    return [...d.querySelectorAll('.pqm-parte')].map(p => [pl(p.querySelector('.pqm-parteh')), [...p.querySelectorAll(':scope > ul.pqm-lista > li')].map(pl)]); });
  // 7. Permutaciones: [true, resultado] si las 6 dan lo mismo; si no, [false, las 6].
  const inv = muestra.map(ks => ['pvp', 'pve'].map(c => { const rs = P.map(p => JSON.stringify(res(p.map(i => porKey.get(ks[i])), c)));
    return rs.every(r => r === rs[0]) ? [true, JSON.parse(rs[0])] : [false, rs.map(r => JSON.parse(r))]; }));
  return { ev, funcion, listas, trio: trioR, refs, det, inv };
}"""

# 8. Liderazgos agregados: [variante, slot, liderazgo]. Silver Surfer — Void Knight tiene todo su
#    liderazgo condicional (ataques y defensas al estar mermado); Thanos — Annihilation, ataques y
#    defensas permanentes y Remove All Debuffs condicional.
SS, TH = 'silver-surfer::silver-surfer-10200199', 'thanos::thanos-10700075'
SINT = [[SS, 'leader2', {'fx': [{'s': 'All Basic Attacks', 'v': 10}]}],
        [SS, 'leader2', {'r': ['Side', 'Supervillano'], 'fx': [{'s': 'All Basic Attacks', 'v': 10}]}],
        [TH, 'leader2', {'ac': 'When Debuffed', 'fx': [{'s': 'Remove All Debuffs'}, {'s': 'All Basic Attacks', 'v': 5}]}]]
SINT_TRIOS = [['thor::base', SS, 'gorr::gorr-10100253'], TRIO, ['galactus::base', TH, 'kang-the-conqueror::kang-the-conqueror-10100259'],
              ['knull::knull-10100241', TH, SS], ['black-cat::black-cat-10400009', SS, 'wasp::wasp-10300051']]
PERMS = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
JS8 = r"""([sint, trios, perms]) => {
  const porKey = new Map(allVariants().map(x => [x.key, x]));
  return sint.map(([k, slot, x]) => {
    const so = SOPORTES[porKey.get(k).p], viejo = so[slot];
    so[slot] = x; _SLOTS.clear();
    const r = trios.map(ks => ['pvp', 'pve'].map(c => perms.map(q => { const vs = q.map(i => porKey.get(ks[i])); const e = enContexto(vs, c);
      return e ? [e.score, e.lider.key, [e.partes.lider, e.partes.dps, e.partes.sinergia, e.strikers]] : null; })));
    so[slot] = viejo; _SLOTS.clear();
    return r;
  });
}"""

# La lista de PvP ya pintada (sus tarjetas abren la ventana del «Por qué» de PvP).
PVP = '#combos .combo [data-a="pqAbrir"][data-pq^="c|pvp|"]'

def ficha(pg, buscar, cid):
    pg.fill('#q', buscar); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    pg.click('[data-a="fichaTab"][data-v="equipos"]')

srv, url = levantar(carpeta_datos(), origen_local())
errores = []
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        def gancho(route):
            r = route.fetch(); cuerpo = r.text()
            route.fulfill(response=r, body=cuerpo.replace('\narrancar();\n})();', '\nwindow.__ev = s => eval(s);\narrancar();\n})();'))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)
        R = pg.evaluate('([js, a]) => window.__ev(js)(a)', [JS, [trios, FOCOS, [x[:4] for x in CASOS], TRIO, [x[:2] for x in DETALLE], MUESTRA]])
        # 5. Thor base: sin lista en PvP ni en PvE, y sin calcular la consulta.
        pg.set_default_timeout(60000)
        ficha(pg, 'Thor', 'thor'); pg.wait_for_selector('#combos .combo')
        for c, rotulo in (('pvp', 'la tier list de PvP'), ('pve', 'las tier lists de PvE')):
            pg.evaluate('() => window.__ev("CONSULTA = null")')
            pg.select_option('select[data-a="eqOrden"]', c); pg.wait_for_selector('#combos .cxnota')
            pg.wait_for_timeout(300)
            nota = pg.locator('#combos .cxnota').text_content()
            n = pg.locator('#combos .combo').count()
            calculada = pg.evaluate('() => window.__ev("CONSULTA !== null")')
            ok(f'Thor base, orden {c}: el aviso, sin combinaciones y sin consulta',
               nota.startswith('Thor no figura en ' + rotulo) and n == 0 and not calculada, (nota, n, calculada))
            ok(f'Thor base, orden {c}: se puede cambiar el orden', pg.locator('#combos select[data-a="eqOrden"]').count() == 1
               and pg.locator('#combos select[data-a="eqCon"]').count() == 0)
        pg.select_option('select[data-a="eqOrden"]', 'foco'); pg.wait_for_selector('#combos .combo')
        ok('Thor base, de vuelta a puntos para él: la lista', pg.locator('#combos .combo').count() > 0)
        pg.close()

        # 5. Silver Surfer (Shalla-Bal): lista en PvP; en PvE solo «Not for wbl».
        pg = b.new_page(viewport={'width': 1300, 'height': 900}); pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(60000)
        ficha(pg, 'Shalla', 'silver-surfer-shalla-bal'); pg.wait_for_selector('#combos .combo')
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_selector(PVP)
        combo = pg.locator('#combos .combo').first
        cuenta = pg.locator('#combos .row > span.muted').first.text_content()
        ok('Shalla-Bal PvP: hay lista y su contador', cuenta.endswith('combinaciones') and int(cuenta.split()[0].replace('.', '')) > 0, cuenta)
        ok('Shalla-Bal PvP: puntos PvP', 'pts PvP' in combo.locator('.eqpts').text_content(), combo.locator('.eqpts').text_content())
        combo.locator('[data-a="pqAbrir"]').click(); pg.wait_for_selector('#pqdlg[open]')
        lineas = pg.locator('#pqdlg .pqm-parteh').all_text_contents()
        pg.keyboard.press('Escape'); pg.wait_for_selector('#pqdlg', state='hidden')
        ok('Shalla-Bal PvP: anti-mermas, liderazgo y DPS (en la ventana del «Por qué»)', any(l.startswith('Anti-mermas') for l in lineas)
           and any(l.startswith('Liderazgo de') for l in lineas) and any(re.sub(r'\s+', ' ', l).startswith('DPS +') for l in lineas), lineas)
        nota = pg.locator('#combos .cxnota').text_content()
        ok('Shalla-Bal PvP: la nota de las reglas, con cada stat de la tabla y su peso',
           'reglas de Ezequiel' in nota and all(f'{TXT.get(st, st)} {num_es(w)}' in nota for st, w in tabla['pvp']['liderazgo']), nota)
        ok('Shalla-Bal PvP: la nota dice el condicional y el líder único, y ya no que los pesos son una propuesta',
           'el 50% de eso si el liderazgo se activa con una condición' in nota and 'es el mismo en las listas de los tres' in nota
           and 'Los pesos son una propuesta' not in nota, nota)
        pg.select_option('select[data-a="eqOrden"]', 'pve'); pg.wait_for_timeout(500)
        nota = pg.locator('#combos .cxnota').text_content()
        ok('Shalla-Bal PvE: solo «Not for wbl», sin lista', 'o solo como «Not for wbl»' in nota and pg.locator('#combos .combo').count() == 0, nota)
        pg.screenshot(path=f'{SP}/ctx_1300.png')
        pg.close()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(60000)
        desborde = "() => { const out = []; for (const el of document.querySelectorAll('#combos *')) { const r = el.getBoundingClientRect(); if (r.width && r.right > 391) out.push(el.className || el.tagName); } return { doc: document.documentElement.scrollWidth, fuera: [...new Set(out)].slice(0, 5) }; }"
        ficha(pg, 'Shalla', 'silver-surfer-shalla-bal'); pg.wait_for_selector('#combos .combo')
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_selector(PVP)
        r = pg.evaluate(desborde)
        ok('celular: sin desborde con el orden PvP', r['doc'] <= 390 and not r['fuera'], r)
        pg.locator('#combos .combo').first.scroll_into_view_if_needed(); pg.screenshot(path=f'{SP}/ctx_390.png')
        pg.locator('#combos .combo').first.locator('[data-a="pqAbrir"]').click(); pg.wait_for_selector('#pqdlg[open] .pqm-parte')
        pg.locator('#pqdlg .pqm-partes').scroll_into_view_if_needed(); pg.wait_for_timeout(150)
        r = pg.evaluate(desborde.replace('#combos *', '#pqdlg *'))
        ok('celular: la ventana del «Por qué» de PvP, sin desborde', r['doc'] <= 390 and not r['fuera'], r)
        pg.screenshot(path=f'{SP}/ctx_390_ventana.png')
        pg.keyboard.press('Escape'); pg.wait_for_selector('#pqdlg', state='hidden')
        pg.select_option('select[data-a="eqOrden"]', 'pve'); pg.wait_for_selector('#combos .cxnota')
        r = pg.evaluate(desborde)
        ok('celular: sin desborde con el aviso de PvE', r['doc'] <= 390 and not r['fuera'], r)
        pg.locator('#combos .cxnota').scroll_into_view_if_needed(); pg.screenshot(path=f'{SP}/ctx_sin_funcion_390.png')
        pg.close()
        # 8. Sintético, en una página aparte (cambia SOPORTES y lo deja como estaba).
        pg = b.new_page(); pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)
        R8 = pg.evaluate('([js, a]) => window.__ev(js)(a)', [JS8, [SINT, SINT_TRIOS, PERMS]])
        b.close()
finally:
    srv.terminate(); srv.wait()

def modelo(ks, c):
    """[puntaje, clave del líder, partes] según el modelo, o None."""
    vs = [VAR[k] for k in ks]; m = M.evaluar(vs, c)
    return None if m is None else [m[0], vs[m[1]]['key'], list(m[2])]

# 1. tríos al azar
malos, entran = [], {'pvp': 0, 'pve': 0}
for ks, (ep, ev) in zip(trios, R['ev']):
    vs = [VAR[k] for k in ks]
    for c, e in (('pvp', ep), ('pve', ev)):
        m = M.evaluar(vs, c)
        esperado = None if m is None else [m[0], m[1], list(m[2])]
        if e is not None: entran[c] += 1
        if e != esperado: malos.append((ks, c, e, esperado))
ok('3.000 tríos al azar: igual que el modelo en PvP y PvE', not malos, (entran, len(malos), malos[:3]))

# 2. función por contexto
dif = [(k, f, [M.funcion(k, 'pvp'), M.funcion(k, 'pve')]) for k, f in R['funcion'].items() if f != [M.funcion(k, 'pvp'), M.funcion(k, 'pve')]]
cuantas = [sum(f[i] for f in R['funcion'].values()) for i in (0, 1)]
ok('función por contexto: las 888 variantes igual que el modelo', not dif and len(R['funcion']) == 888, (cuantas, dif[:3]))
ok('función por contexto: Thor base y Agent 13 sin función; Knull con función en los dos',
   R['funcion']['thor::base'] == [False, False] and R['funcion']['agent-13::base'] == [False, False]
   and R['funcion']['knull::knull-10100241'] == [True, True], (R['funcion']['thor::base'], R['funcion']['knull::knull-10100241']))

# 3. listas completas
def lista_modelo(fk, ctx):
    v = VAR[fk]
    if not M.funcion(fk, ctx): return None
    pool = [x for x in TODAS if x['cid'] != v['cid']]
    puede = [any(v['key'] in alc for *_, alc in A.SOPS[x['key']]) or any(x['key'] in alc for *_, alc in A.SOPS[v['key']])
             or A.comparten_bono(v, x) for x in pool]
    dps_any = [M.dps_de(x['key'], 'pvp') > 0 or M.dps_de(x['key'], 'pve') > 0 for x in pool]
    dctx = [M.dps_de(x['key'], ctx) > 0 for x in pool]
    filas = []
    for i in range(len(pool)):
        if not (puede[i] or dps_any[i]): continue
        for j in range(i + 1, len(pool)):
            if not (puede[j] or dps_any[j]) or pool[i]['cid'] == pool[j]['cid']: continue
            vs = [v, pool[i], pool[j]]
            e = M.evaluar(vs, ctx)
            if e is None: continue
            li = lj = False
            if puede[i] or puede[j]:
                # Los vínculos, con el líder del contexto (regla 2 de Ezequiel: un solo líder, el del modo, para
                # todo lo de ese modo; carril Q, segunda parte).
                sueltos = F.sueltos_foco(vs, lider=e[1])
                li, lj = puede[i] and 1 not in sueltos, puede[j] and 2 not in sueltos
            if not ((li or dctx[i]) and (lj or dctx[j])): continue
            ps = sum(M.puesto(l, pool[i]['key']) + M.puesto(l, pool[j]['key']) for l in LISTAS[ctx])
            filas.append((-e[0], -e[2][3], ps, RANGO[pool[i]['key']] + RANGO[pool[j]['key']], i, j, e[0]))    # los strikers desempatan
    filas.sort()
    vistos, out = set(), []
    for f in filas:
        par = tuple(sorted((pool[f[4]]['cid'], pool[f[5]]['cid'])))
        if par in vistos: continue
        vistos.add(par); out.append([pool[f[4]]['key'], pool[f[5]]['key'], f[6]])
    return [len(out), out[:20]]
for fk in FOCOS:
    for c in ('pvp', 'pve'):
        esperado, app = lista_modelo(fk, c), R['listas'][f'{fk}|{c}']
        ok(f'{fk} {c}: ' + ('cantidad y primeras 20 igual que el modelo' if esperado else 'sin función, sin lista'),
           esperado == app, (esperado and esperado[0], app and app[0], esperado and esperado[1][:2]))

# 4. casos de referencia: antes (1.0.15, modelo) → ahora; cómo gana la opción de Ezequiel (puntaje,
#    desempate de la lista: puestos de los dos compañeros en el contexto y después la referencia; o pierde).
def orden_lista(f, par, c):
    m = M.evaluar([VAR[k] for k in [f] + par], c)
    return (-m[0], -m[2][3], sum(M.puesto(l, k) for l in LISTAS[c] for k in par), sum(RANGO[k] for k in par))
for (c, f, a, b, como, lids), (ra, rb) in zip(CASOS, R['refs']):
    ma, mb = modelo([f] + a, c), modelo([f] + b, c)
    antes = [M.evaluar([VAR[k] for k in [f] + par], c, antes=True)[0] for par in (a, b)]
    oa, ob = orden_lista(f, a, c), orden_lista(f, b, c)
    veredicto = ('puntaje' if oa[0] < ob[0] else 'pierde') if oa[0] != ob[0] else ('desempate' if oa[1:] < ob[1:] else 'pierde')
    lider_ok = [ra[1].split('::')[0], rb[1].split('::')[0]] == lids
    ok(f'caso de referencia {f} {c}: gana {" + ".join(a)} por {como}, líderes {lids[0]} y {lids[1]}',
       ra == ma and rb == mb and veredicto == como and lider_ok,
       f'antes {antes[0]} a {antes[1]} → ahora {ra[0]} a {rb[0]}; líderes {ra[1]} / {rb[1]}; {veredicto}' + ('' if (ra, rb) == (ma, mb) else f'; modelo {ma} {mb}'))

# 5. detalle: «cuenta el 50%» solo en el liderazgo condicional; cada línea con lo que suma, y la suma da el total.
for (c, ks, lid, cond), partes in zip(DETALLE, R['det']):
    cab, vi = next(((x, v) for x, v in partes if x.startswith('Liderazgo de')), ('', []))
    pts = modelo(ks, c)[2][0]
    lineas = [float(re.search(r'\(\+([\d.,]+)\)$', x).group(1).replace('.', '').replace(',', '.')) if re.search(r'\(\+([\d.,]+)\)$', x) else None for x in vi]
    ok(f'detalle {ks[0]} PvP: liderazgo de {lid} +{num_es(pts)}' + (', condicional: «cuenta el 50%»' if cond else ', permanente: sin «cuenta el 50%»'),
       cab == f'Liderazgo de {VAR[next(k for k in ks if k.startswith(lid + "::"))]["name"]} +{num_es(pts)}' and vi and all('→' in x for x in vi)
       and any('cuenta el 50%' in x for x in vi) == cond, (cab, vi))
    ok(f'detalle {ks[0]} PvP: cada línea del liderazgo dice cuánto suma, y la suma da +{num_es(pts)}',
       None not in lineas and abs(sum(lineas) - pts) < 1e-9, (lineas, pts))

# 6. el trío del caso
for c in ('pvp', 'pve'):
    perms, desde = R['trio'][c]
    m = modelo(TRIO, c)
    ok(f'trío del caso, {c}: las 6 permutaciones igual que el modelo', all(p == m for p in perms), (m, perms))
    for k, d in zip(TRIO, desde):
        if not M.funcion(k, c):
            ok(f'trío del caso, {c}, desde {k}: sin función, sin lista', d is None, d); continue
        ok(f'trío del caso, {c}, desde {k}: en su lista, mismo líder y total', d is not None and d[0] > 0
           and sorted(d[2]) == sorted(x for x in TRIO if x != k) and d[3] == m, d)

# 7. líder único: las 6 permutaciones
rotos, distinto = [], []
for n, (ks, par) in enumerate(zip(MUESTRA, R['inv'])):
    for c, (igual, r) in zip(('pvp', 'pve'), par):
        if not igual: rotos.append((ks, c, r)); continue
        if r != modelo(ks, c): distinto.append((ks, c, r, modelo(ks, c)))
emp = {c: sum(1 for ks in EMPATES[c] if empatados([VAR[k] for k in ks], c) == 'clave') for c in EMPATES}
ok(f'líder único: 6 permutaciones iguales en {len(MUESTRA)} tríos (3.000 al azar + 300 empates por contexto, '
   f'{emp["pvp"]} y {emp["pve"]} decididos por la clave)', not rotos, (len(rotos), rotos[:3]))
ok('líder único: igual que el modelo en toda la muestra', not distinto, (len(distinto), distinto[:3]))

# 8. sintético: la misma mutación en el modelo (SOP es el de analisis_haz, que usa modelo_ctx).
from analisis_haz import SOP
for (k, slot, x), r in zip(SINT, R8):
    so = SOP[VAR[k]['p']]; viejo = so.get(slot); so[slot] = x
    malos, pts = [], []
    for ks, rc in zip(SINT_TRIOS, r):
        for c, rp in zip(('pvp', 'pve'), rc):
            esp = [modelo([ks[i] for i in q], c) for q in PERMS]
            pts.append(esp[0] and esp[0][2][0])
            if rp != esp: malos.append((ks, c, rp[0], esp[0]))
    so[slot] = viejo
    ok(f'sintético {k} {slot} {"condicional" if x.get("ac") else "permanente"} {x["fx"][-1]["s"]}'
       + (f' ({x["r"][1]})' if x.get('r') else '') + ': igual que el modelo en las 6 permutaciones', not malos,
       (len(malos), malos[:2]) if malos else f'liderazgo (pvp, pve) por trío: {pts}')
ok('sin errores de página', not errores, errores[:3])
ok.fin()
