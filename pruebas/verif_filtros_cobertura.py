"""Casillas de cobertura en las combinaciones de 3 (carril H, 3 de octubre de 2026). Ezequiel: «En los filtros
de equipos, dame checkboxes, donde pueda filtrar por algún detalle, por ejemplo, si el equipo tiene Quita todos
los debuffs, da vida, todas las defensas y demás.» Una casilla por grupo de la cobertura de la tarjeta (Ataque,
Ignorar esquiva, Todas las defensas, Vida, Anti-mermas: desde el 4 de octubre de 2026, los stats de anti-mermas de la
tabla de valor, y lo propio cuenta para su dueño). Marcada, deja las combinaciones cuya tarjeta
muestra ✓ en ese grupo (también con *: solo con artefacto); varias, con Y; de cada pareja de compañeros, la mejor
combinación de uniformes que las cumple.
1. Referencia, en la página: de las filas que entran en el orden, ordenadas con el orden de vistaConsulta escrito
   acá (sin contexto: puestos, puntos para él, strikers, referencia, fila; en PvP y PvE: puntaje de contexto,
   strikers, puestos, referencia, fila), la primera de cada pareja cuya tarjeta tiene ✓ en todo lo marcado, con
   el líder de la tarjeta (liderDe(vs, null) o enContexto(vs, ctx, true)) y la cobertura() de la tarjeta (que
   verif_indice compara con su modelo aparte). Galactus, Adam Warlock (base y GotG3), Knull — Ancient History y
   Annihilus, en los cuatro órdenes (puntos para él, PvP, PvE, la tier list de soportes), sin casillas, con cada
   una, con pares, con tres y con las cinco: la lista igual a la referencia y ninguna tarjeta sin ✓.
2. Sin casillas: la primera página en pantalla y la cuenta, como la referencia, en los órdenes puntos para él, PvP
   y PvE. (Hasta el carril de consistencia se comparaba con el app.js de 323fa15; desde el 4 de octubre de 2026
   el líder, los strikers, los pesos y lo propio cambian las listas a propósito.)
3. En pantalla (Adam Warlock — GotG3, puntos para él): con cada casilla, la cuenta y las páginas 1, 2, 3 y la
   última igual a la referencia, con ✓ en ese grupo. Con «Todas las defensas», parejas que entran con otra
   combinación de uniformes que sin casillas (filtrando después de deduplicar se perderían).
4. Dos casillas (Ataque e Ignorar esquiva; Vida y Elimina todas las mermas): ✓ en las dos y la referencia; el Y
   es por tarjeta: las parejas de las dos están en las listas de cada una, y las que cumplen cada casilla con
   otra combinación de uniformes y ninguna las dos no entran (con Ataque e Ignorar esquiva, alguna). Tres (el
   ejemplo de Ezequiel): todas las páginas contadas = la cuenta.
5. «Ninguna combinación con estos filtros.» y la cuenta en 0; descartes con casillas (el descartado cuenta solo
   si cumple lo marcado).
6. Reinicio, como «Sin» (eqExcluir) y no como «Con» (eqCon, que se vacía al cambiar de personaje): las casillas
   quedan al cambiar de orden, de uniforme y de personaje; sin función en el contexto no se muestran, y al volver
   siguen marcadas.
7. Inglés: rótulos de la tarjeta, casillas marcadas, cuenta, sin restos en castellano. Sin errores de página ni
   de consola, en los dos idiomas. Celular: nada se sale.
Necesita las imágenes (sin ellas la consola da 404): en esta sesión, MFF_DATOS=carril-filtros/datos6."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, RAIZ
from playwright.sync_api import sync_playwright

ok = Chequeo()
SP = PRUEBAS
GRUPOS = ['ataque', 'evasion', 'defensas', 'vida', 'mermas']     # COBERTURA: el orden de las casillas y de la tarjeta
ES = {'ataque': 'Ataque', 'evasion': 'Ignorar esquiva', 'defensas': 'Todas las defensas', 'vida': 'PG', 'mermas': 'Anti-mermas'}
EN = {'ataque': 'Attack', 'evasion': 'Ignore Dodge', 'defensas': 'All Defenses', 'vida': 'HP', 'mermas': 'Debuff removal'}
ADAM, ADAM0 = 'adam-warlock::adam-warlock-10200152', 'adam-warlock::base'   # GotG3: el Adam con función en PvP y PvE
KNULL = 'knull::knull-10100241'
FOCOS = ['galactus::base', ADAM, ADAM0, KNULL, 'annihilus::base']
ORDENES = ['foco', 'pvp', 'pve', 'lista:tv-soportes']
TRES = ['defensas', 'vida', 'mermas']
CASILLAS = [[]] + [[g] for g in GRUPOS] + [['vida', 'mermas'], ['defensas', 'vida'], ['ataque', 'evasion'], TRES, GRUPOS]
CON_CLAVES = [[ADAM, 'foco'], [ADAM, 'pvp'], [ADAM, 'pve'], [ADAM, 'lista:tv-soportes'], [ADAM0, 'foco'], [KNULL, 'foco']]

GANCHO_FIN = '\narrancar();\n})();'
def gancho(cuerpo=None):
    def f(route):
        r = route.fetch(); src = cuerpo if cuerpo is not None else r.text()
        if GANCHO_FIN not in src: raise SystemExit('app.js no termina como se esperaba')
        route.fulfill(response=r, body=src.replace(GANCHO_FIN, '\nwindow.__ev = s => eval(s);' + GANCHO_FIN))
    return f

REF = r"""([focos, ordenes, casillas, conClaves]) => {
  const par = (a, b) => a.cid < b.cid ? a.cid + '|' + b.cid : b.cid + '|' + a.cid;
  const out = [];
  for (const k of focos) {
    const v = allVariants().find(x => x.key === k);
    CONSULTA = null;
    const q = consultaCon(v);
    for (const o of ordenes) {
      const ctx = o === 'pvp' || o === 'pve' ? o : null;
      if (ctx && !tieneFuncion(v, ctx)) continue;
      Object.assign(ui, { eqOrden: o, eqExcluir: [], eqCon: '', eqVerDescartados: false, eqPagina: 0, eqCobertura: [] });
      // las filas que entran en el orden, con la clave de vistaConsulta
      const ls = listasOrden();
      const pos = q.pool.map(x => ls.reduce((s, l) => s + puesto(l, x.key), 0)), ref = q.pool.map(x => rankIndex(x.key));
      const dpsCtx = ctx ? q.pool.map(x => rolEn(x, ctx).dps > 0) : null, filas = [];
      for (let i = 0; i < q.n; i++) {
        const ps = pos[q.A[i]] + pos[q.B[i]], rf = ref[q.A[i]] + ref[q.B[i]];
        let pts, stk;
        // Vínculos (1, el primero; 2, el segundo): por soportes y bonos (q.G) y por el liderazgo del líder del orden
        // (sin contexto, el de la sinergia; en PvP y PvE, el del contexto: carril Q, segunda parte): lidera él y le
        // llega al compañero, o lidera el compañero y le llega a él.
        const vs = [v, q.pool[q.A[i]], q.pool[q.B[i]]];
        // Por un soporte o un bono, con el líder del orden (desde el 5 de octubre de 2026 un efecto sin valor se aplica una vez, y
        // qué se le aplica a cada uno depende del líder): sin contexto, el de la consulta (q.G, con el de la sinergia); en PvP y PvE,
        // la sinergia con foco en él y el líder del contexto, siempre (sin el atajo de la app).
        const porSoporte = (lider) => { const ap = synergy(vs, { soloPuntaje: true, foco: v, lider }).aplicados; return (vinculo(v, vs[1], ap) ? 1 : 0) | (vinculo(v, vs[2], ap) ? 2 : 0); };
        const vinc = (lider) => [1, 2].reduce((f, n) => (lider === v && llegaLiderazgo(v, vs[n])) || (lider === vs[n] && llegaLiderazgo(vs[n], v)) ? f | n : f, ctx ? porSoporte(lider) : q.G[i]);
        if (!ctx) { if (vinc(liderDe(vs, null)) !== 3) continue; pts = q.P[i]; stk = q.S[i]; }
        else {
          const e = enContexto(vs, ctx); if (!e) continue;
          const f = vinc(e.lider);
          if (!((f & 1 || dpsCtx[q.A[i]]) && (f & 2 || dpsCtx[q.B[i]]))) continue;
          pts = e.score; stk = e.strikers;
        }
        filas.push([ctx ? [-pts, -stk, ps, rf, i] : [ps, -pts, -stk, rf, i], i]);
      }
      filas.sort((x, y) => { for (let n = 0; n < 5; n++) if (x[0][n] !== y[0][n]) return x[0][n] - y[0][n]; return 0; });
      // ✓ de cada grupo en la tarjeta de una fila: el líder como fila() de combinacionesHtml, su cobertura y el ✓ de
      // su coberturaHtml (algún c del grupo en cob)
      const memo = new Map(); let difCob = 0;
      const tarjeta = (i) => {
        let c = memo.get(i);
        if (!c) {
          const vs = [v, q.pool[q.A[i]], q.pool[q.B[i]]];
          const lider = ctx ? enContexto(vs, ctx, true).lider : liderDe(vs, null);
          const cob = cobertura(v, vs, lider);
          c = new Set(COBERTURA.filter(g => g.cats.some(x => x in cob)).map(g => g.k));
          memo.set(i, c);
        }
        return c;
      };
      for (const cs of casillas) {
        const esp = [], vistos = new Set();
        for (const [, i] of filas) {
          const p = par(q.pool[q.A[i]], q.pool[q.B[i]]);
          if (vistos.has(p) || !cs.every(g => tarjeta(i).has(g))) continue;
          vistos.add(p); esp.push(i);
        }
        ui.eqCobertura = cs; q.vista = null;
        const app = vistaConsulta(q).filas;
        const r = { foco: k, orden: o, casillas: cs, n: app.length, ref: esp.length,
                    igual: esp.length === app.length && esp.every((x, n) => x === app[n]),
                    sinTilde: app.filter(i => !cs.every(g => tarjeta(i).has(g))).length };
        if (conClaves.some(([f, oo]) => f === k && oo === o)) r.claves = esp.map(i => q.pool[q.A[i]].key + '|' + q.pool[q.B[i]].key);
        out.push(r);
      }
      out.push({ foco: k, orden: o, difCob, miradas: memo.size });
    }
  }
  Object.assign(ui, { eqOrden: 'foco', eqCobertura: [] }); CONSULTA = null;
  return out;
}"""
# Sin casillas: las listas enteras de la app, como claves de los tríos.
LISTA = r"""([focos, ordenes]) => {
  const out = {};
  for (const k of focos) {
    const v = allVariants().find(x => x.key === k);
    CONSULTA = null;
    const q = consultaCon(v);
    for (const o of ordenes) {
      if ((o === 'pvp' || o === 'pve') && !tieneFuncion(v, o)) continue;
      Object.assign(ui, { eqOrden: o, eqExcluir: [], eqCon: '', eqVerDescartados: false, eqPagina: 0 });
      q.vista = null;
      const vi = vistaConsulta(q);
      out[k + '|' + o] = [vi.filas.length, vi.filas.map(i => q.pool[q.A[i]].key + '|' + q.pool[q.B[i]].key).join(',')];
    }
  }
  Object.assign(ui, { eqOrden: 'foco' }); CONSULTA = null;
  return out;
}"""
TARJETAS = """() => [...document.querySelectorAll('#combos .combo')].map(c => ({
  claves: [...c.querySelectorAll('.eqfoto')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base')),
  cob: [...c.querySelectorAll('.cobertura .tag.cob')].map(t => [t.classList[t.classList.length - 1], t.textContent.trim()]),
  lider: c.querySelector('.combolider').innerText, pts: c.querySelector('.eqpts').innerText.replace(/\*/g, ''),   // los mismos números (el «*» de un artefacto es nuevo)
  texto: c.innerText }))"""
FUERA = """() => { const lim = document.getElementById('fcuerpo').getBoundingClientRect().right;
  return [...document.querySelectorAll('#fcuerpo *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > lim + 0.5; })
    .map(e => (e.getAttribute('data-a') || e.className || e.tagName) + ' → ' + Math.round(e.getBoundingClientRect().right)).slice(0, 4); }"""


def nombre_de(key): return {'adam-warlock': 'Adam Warlock', 'knull': 'Knull', 'galactus': 'Galactus', 'annihilus': 'Annihilus'}[key.split('::')[0]]
def esperar_lista(pg, key):
    pg.wait_for_function("k => window.__ev('CONSULTA && CONSULTA.clave') === k && !window.__ev('ui.eqCalculando')"
                         " && document.querySelector('#combos .eqfiltros')", arg=key, timeout=60000)
    pg.wait_for_timeout(100)
def abrir(pg, key):
    cid, uid = key.split('::')
    pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre_de(key)); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid != 'base': pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(150)
    pg.click('[data-a="fichaTab"][data-v="equipos"]')
    esperar_lista(pg, key)
def casilla(pg, g): return pg.locator(f'#combos input[data-a="eqCobertura"][data-g="{g}"]')
def tocar(pg, g): casilla(pg, g).click(); pg.wait_for_timeout(120)
def marcadas(pg): return [g for g in GRUPOS if casilla(pg, g).count() and casilla(pg, g).is_checked()]
def cuenta(pg):
    tx = pg.locator('#combos .row > span.muted').first.inner_text()
    return int(re.sub(r'\D', '', tx.split('·')[0]) or 0), tx
def ir_pagina(pg, p):
    # el «←» de la primera página también lleva data-p="0", deshabilitado; sin paginador (una página) no hay botón
    bt = pg.locator(f'#combos [data-a="eqPagina"][data-p="{p}"]:not([disabled])')
    if bt.count(): bt.first.click(); pg.wait_for_timeout(120)
def orden(pg, o): pg.select_option('#combos select[data-a="eqOrden"]', o); pg.wait_for_timeout(150)

def pareja(claves, foco):
    """Los dos compañeros del foco, ordenados: el líder va primero en la tarjeta (4 de octubre de 2026), así que el
    orden de los retratos no es el de la fila."""
    return '|'.join(sorted(k for k in claves if k != foco))
def revisar_paginas(pg, claves, gs, paginas=None, foco=None):
    """Las páginas pedidas (por defecto 1, 2, 3 y la última): los tríos de la referencia, en su lugar, con ✓ en
    los grupos gs. Devuelve [páginas miradas, tarjetas, problemas]."""
    total = max(1, -(-len(claves) // 20))
    ps = paginas if paginas is not None else sorted({0, 1, 2, total - 1} & set(range(total)))
    malos, n = [], 0
    for p in ps:
        ir_pagina(pg, p)
        ts = pg.evaluate(TARJETAS)
        esp = ['|'.join(sorted(x.split('|'))) for x in claves[p * 20:(p + 1) * 20]]
        got = [pareja(t['claves'], foco) for t in ts]
        if got != esp: malos.append((p, 'tríos', got[:2], esp[:2]))
        for t in ts:
            n += 1
            for g in gs:
                est, tx = t['cob'][GRUPOS.index(g)]
                if est not in ('si', 'art') or not tx.startswith('✓'): malos.append((p, t['claves'], g, est, tx))
    return [len(ps), n, malos]


errores = []
def vigilar(pg, nombre):
    pg.on('pageerror', lambda e: errores.append(f'{nombre}: {e}'))
    pg.on('console', lambda m: m.type == 'error' and errores.append(f'{nombre} consola: {m.text}'))

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1300, 'height': 900}); vigilar(pg, 'es')
        pg.route(lambda u: '/app.js' in u, gancho())
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)
        R = pg.evaluate('([js, a]) => window.__ev(js)(a)', [REF, [FOCOS, ORDENES, CASILLAS, CON_CLAVES]])
        L_NUEVA = pg.evaluate('([js, a]) => window.__ev(js)(a)', [LISTA, [FOCOS, ORDENES]])
        pg.set_default_timeout(60000)

        # 1. referencia
        casos = [r for r in R if 'casillas' in r]
        mal = [(r['foco'], r['orden'], r['casillas'], r['n'], r['ref'], r['sinTilde']) for r in casos if not r['igual'] or r['sinTilde']]
        ok(f'1 la lista igual a la referencia y sin tarjetas sin ✓ ({len(casos)} casos: {len(FOCOS)} focos, 4 órdenes con función, {len(CASILLAS)} juegos de casillas)',
           not mal, mal[:4])
        cob = [r for r in R if 'difCob' in r]
        print(f"1 tarjetas miradas: {sum(r['miradas'] for r in cob)} en {len(cob)} listas")
        REFS = {(r['foco'], r['orden'], '+'.join(r['casillas'])): r for r in casos}
        def ref(foco, o, gs): return REFS[(foco, o, '+'.join(g for g in GRUPOS if g in gs))]
        g3 = ref('galactus::base', 'pvp', TRES)
        ok('1 Galactus PvP con las tres de Ezequiel: muchas menos', 0 < g3['n'] < ref('galactus::base', 'pvp', [])['n'], (g3['n'], ref('galactus::base', 'pvp', [])['n']))

        # 2. sin casillas: las listas enteras (vistaConsulta) y la primera página en pantalla, como la referencia
        sin = {(r['foco'], r['orden']): r for r in casos if not r['casillas']}
        dif = [k for k, (n, cl) in L_NUEVA.items() if n != sin[tuple(k.split('|'))]['n']]
        ok(f'2 sin casillas: las {len(L_NUEVA)} listas enteras con la cuenta de la referencia', not dif, dif[:3])
        abrir(pg, ADAM)
        for o in ('foco', 'pvp', 'pve'):
            orden(pg, o)
            n = pg.evaluate(TARJETAS)
            esp = ref(ADAM, o, [])
            got, primeras = [pareja(t['claves'], ADAM) for t in n], ['|'.join(sorted(x.split('|'))) for x in esp['claves'][:20]]
            ok(f'2 sin casillas, {o}: la primera página y la cuenta como la referencia',
               len(n) == 20 and got == primeras and cuenta(pg)[0] == esp['n'] and marcadas(pg) == [], (cuenta(pg), esp['n'], got[:2], primeras[:2]))
        orden(pg, 'foco')
        fila = pg.locator('#combos input[data-a="eqCobertura"]').first.locator('xpath=../..')
        ok('2 la fila de casillas: «Solo si recibe:» y los cinco grupos con los rótulos de la tarjeta, sin marcar',
           pg.evaluate("[...document.querySelectorAll('#combos input[data-a=\"eqCobertura\"]')].map(x => x.dataset.g + '|' + x.parentElement.textContent.trim())")
           == [f'{g}|{ES[g]}' for g in GRUPOS] and fila.inner_text().startswith('Solo si recibe:') and '✓' in (fila.get_attribute('title') or ''),
           fila.inner_text().replace('\n', ' '))

        # 3. cada casilla, en pantalla
        for g in GRUPOS:
            tocar(pg, g)
            r = ref(ADAM, 'foco', [g])
            c, tx = cuenta(pg)
            ps, n, malos = revisar_paginas(pg, r['claves'], [g], foco=ADAM)
            ok(f'3 «{ES[g]}»: la cuenta ({c}) igual a la referencia, y {ps} páginas ({n} tarjetas) con ✓ en ese grupo y los tríos de la referencia',
               c == r['n'] and marcadas(pg) == [g] and ps >= 3 and not malos, (tx, r['n'], malos[:2]))
            tocar(pg, g)
        c, _ = cuenta(pg)
        ok('3 sin casillas otra vez: la lista entera', c == ref(ADAM, 'foco', [])['n'] and marcadas(pg) == [], c)
        par = lambda x: '|'.join(sorted(k.split('::')[0] for k in x.split('|')))
        base = {par(x): x for x in ref(ADAM, 'foco', [])['claves']}
        otra = [x for x in ref(ADAM, 'foco', ['defensas'])['claves'] if base[par(x)] != x]
        ok(f'3 «Todas las defensas»: {len(otra)} parejas entran con otra combinación de uniformes que sin casillas '
           '(filtrando después de deduplicar se perderían)', len(otra) > 0, otra[:2])

        # 4. dos casillas: intersección por combinación (por tarjeta); tres: la cuenta contando las páginas
        parejas = lambda cl: {par(x) for x in cl}
        for g1, g2 in (('ataque', 'evasion'), ('vida', 'mermas')):
            tocar(pg, g1); tocar(pg, g2)
            r2, r1a, r1b = ref(ADAM, 'foco', [g1, g2]), ref(ADAM, 'foco', [g1]), ref(ADAM, 'foco', [g2])
            c, tx = cuenta(pg)
            ps, n, malos = revisar_paginas(pg, r2['claves'], [g1, g2], foco=ADAM)
            ok(f'4 «{ES[g1]}» y «{ES[g2]}»: la cuenta ({c}) y {ps} páginas con ✓ en las dos, como la referencia',
               c == r2['n'] and marcadas(pg) == [g1, g2] and not malos, (tx, r2['n'], malos[:2]))
            pa, pb, p2 = parejas(r1a['claves']), parejas(r1b['claves']), parejas(r2['claves'])
            ok(f'4 intersección: las {len(p2)} parejas de las dos están en las listas de cada una; '
               f'{len((pa & pb) - p2)} cumplen cada una con otra combinación de uniformes y ninguna las dos: no entran',
               p2 <= (pa & pb) and (g1 != 'ataque' or len((pa & pb) - p2) > 0), sorted((pa & pb) - p2)[:3])
            if g1 == 'ataque': tocar(pg, g1); tocar(pg, g2)
        tocar(pg, 'defensas')
        r3 = ref(ADAM, 'foco', TRES)
        c, tx = cuenta(pg)
        total = -(-r3['n'] // 20)
        ps, n, malos = revisar_paginas(pg, r3['claves'], TRES, list(range(total)), foco=ADAM)
        ok(f'4 las tres de Ezequiel: {total} páginas, {n} tarjetas contadas = la cuenta ({c}), todas con ✓ en las tres',
           n == c == r3['n'] and not malos, (tx, r3['n'], n, malos[:2]))

        # 5. ninguna; descartes con casillas
        r5, rm = ref(ADAM, 'foco', GRUPOS), ref(ADAM, 'foco', ['mermas'])
        en5 = {k.split('::')[0] for x in r5['claves'] for k in x.split('|')}
        con = next(k.split('::')[0] for x in ref(ADAM, 'foco', [])['claves'] for k in x.split('|') if k.split('::')[0] not in en5)
        for g in GRUPOS:
            if g not in marcadas(pg): tocar(pg, g)
        pg.select_option('#combos select[data-a="eqCon"]', con); pg.wait_for_timeout(150)
        c, tx = cuenta(pg)
        ok(f'5 «Con {con}» y las cinco: «Ninguna combinación con estos filtros.» y la cuenta en 0',
           c == 0 and pg.locator('#combos .combo').count() == 0 and 'Ninguna combinación con estos filtros.' in pg.locator('#combos').inner_text(), tx)
        pg.select_option('#combos select[data-a="eqCon"]', ''); pg.wait_for_timeout(150)
        for g in GRUPOS:
            if g != 'mermas': tocar(pg, g)
        primero = pg.evaluate(TARJETAS)[0]['claves']
        pg.locator('#combos .combo').first.locator('[data-a="descartar"]').click(); pg.wait_for_timeout(400)
        c, tx = cuenta(pg)
        ok('5 descartar con «Anti-mermas»: una menos y «1 descartado»', c == rm['n'] - 1 and '1 descartado' in tx, tx)
        par_d = '|'.join(sorted(k.split('::')[0] for k in primero if k != ADAM))    # el líder va primero: el foco puede no ser el primero
        sin = next((g for g in GRUPOS if par_d not in parejas(ref(ADAM, 'foco', [g])['claves'])), None)
        if sin:
            tocar(pg, 'mermas'); tocar(pg, sin)
            c, tx = cuenta(pg)
            ok(f'5 con «{ES[sin]}», que ese trío no cumple con ningún uniforme: no cuenta como descartado',
               c == ref(ADAM, 'foco', [sin])['n'] and 'descartado' not in tx, tx)
            tocar(pg, sin); tocar(pg, 'mermas')
        else:
            ok('5 (sin un grupo que el trío descartado no cumpla: no se prueba)', True)
        pg.click('#combos [data-a="eqVerDescartados"]'); pg.wait_for_timeout(200)
        pg.locator('#combos [data-a="restaurar"]').first.click(); pg.wait_for_timeout(400)
        pg.click('#combos [data-a="eqVerDescartados"]'); pg.wait_for_timeout(200)
        c, tx = cuenta(pg)
        ok('5 restaurado: la cuenta de antes', c == rm['n'] and 'descartado' not in tx and marcadas(pg) == ['mermas'], tx)

        # 6. reinicio: orden, uniforme y personaje (como «Sin»; «Con» se vacía)
        tocar(pg, 'mermas'); tocar(pg, 'vida')
        for o in ('pvp', 'pve', 'lista:tv-soportes', 'foco'):
            orden(pg, o)
            r = ref(ADAM, o, ['vida']) if (ADAM, o, 'vida') in REFS else None
            c, tx = cuenta(pg)
            ts = pg.evaluate(TARJETAS)
            ok(f'6 cambiar el orden a {o}: «Vida» sigue marcada, cuenta de la referencia y ✓ en la primera página',
               marcadas(pg) == ['vida'] and c == r['n'] and ts and all(t['cob'][3][1].startswith('✓') for t in ts), (tx, r['n']))
        pg.select_option('select[data-a="uniformSel"]', 'base'); esperar_lista(pg, ADAM0)
        orden(pg, 'pvp')
        ok('6 Adam Warlock base en PvP (sin función): el aviso y sin casillas', pg.locator('#combos .cxnota').count() == 1
           and casilla(pg, 'vida').count() == 0 and pg.locator('#combos .combo').count() == 0)
        orden(pg, 'foco')
        c, tx = cuenta(pg)
        ok('6 de vuelta a puntos para él, en el uniforme base: «Vida» sigue marcada y filtra', marcadas(pg) == ['vida'] and c == ref(ADAM0, 'foco', ['vida'])['n'], tx)
        excluido = next(k.split('::')[0] for k in ref(ADAM0, 'foco', [])['claves'][0].split('|'))
        pg.select_option('#combos select[data-a="eqCon"]', con); pg.wait_for_timeout(150)
        pg.select_option('#combos select[data-a="eqExcluir"]', excluido); pg.wait_for_timeout(150)
        abrir(pg, KNULL)
        quedan = pg.locator('#combos [data-a="eqIncluir"]').count()
        ok('6 otro personaje (Knull — Ancient History): «Vida» y «Sin» quedan, «Con» se vacía',
           marcadas(pg) == ['vida'] and quedan == 1 and pg.locator('#combos select[data-a="eqCon"]').input_value() == '',
           (marcadas(pg), quedan, pg.locator('#combos select[data-a="eqCon"]').input_value()))
        pg.locator('#combos [data-a="eqIncluir"]').first.click(); pg.wait_for_timeout(150)
        c, tx = cuenta(pg)
        r = ref(KNULL, 'foco', ['vida'])
        ps, n, malos = revisar_paginas(pg, r['claves'], ['vida'], foco=KNULL)
        ok('6 Knull: la lista con «Vida», como la referencia', c == r['n'] and not malos, (tx, r['n'], malos[:2]))

        # 7. inglés
        pg.click('[data-a="lang"]'); esperar_lista(pg, KNULL)
        rotulos = pg.evaluate("[...document.querySelectorAll('#combos input[data-a=\"eqCobertura\"]')].map(x => x.parentElement.textContent.trim())")
        fila = pg.locator('#combos input[data-a="eqCobertura"]').first.locator('xpath=../..')
        c, tx = cuenta(pg)
        ts = pg.evaluate(TARJETAS)
        ok('7 inglés: «Only if it gets:», los rótulos de la tarjeta y «Vida» sigue marcada',
           rotulos == [EN[g] for g in GRUPOS] and fila.inner_text().startswith('Only if it gets:') and marcadas(pg) == ['vida']
           and 'everything checked' in (fila.get_attribute('title') or ''), (rotulos, fila.inner_text()[:40]))
        ok('7 inglés: la cuenta y ✓ HP en cada tarjeta', c == r['n'] and tx.endswith('combinations') and all(t['cob'][3][1].startswith('✓ HP') for t in ts), (tx, ts[0]['cob'] if ts else None))
        tocar(pg, 'mermas')
        c, tx = cuenta(pg)
        ts = pg.evaluate(TARJETAS)
        ok('7 inglés: con «Debuff removal» también, la referencia y ✓ en los dos', c == ref(KNULL, 'foco', ['vida', 'mermas'])['n']
           and all(t['cob'][4][1].startswith('✓ Debuff removal') and t['cob'][3][1].startswith('✓ HP') for t in ts), tx)
        txc = pg.locator('#combos').inner_text()
        resto = [w for w in ('Solo si recibe', 'Quita todos', 'Ignorar esquiva', 'Ordenar', 'combinaciones', 'Líder', 'para él') if w in txc]
        ok('7 inglés: sin restos en castellano en la lista', not resto, resto)
        pg.click('[data-a="lang"]'); esperar_lista(pg, KNULL)
        ok('7 de vuelta en castellano: las dos siguen marcadas', marcadas(pg) == ['vida', 'mermas'])
        b.close()

        # celular
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True); vigilar(pg, 'celular')
        pg.route(lambda u: '/app.js' in u, gancho())
        pg.goto(url); pg.wait_for_selector('.ccard')
        abrir(pg, ADAM)
        for g in TRES: tocar(pg, g)
        ok('7 celular: con las casillas marcadas, nada se sale de la columna', not pg.evaluate(FUERA) and pg.evaluate('document.documentElement.scrollWidth') <= 390,
           pg.evaluate(FUERA))
        pg.locator('#combos input[data-a="eqCobertura"]').first.scroll_into_view_if_needed()
        os.makedirs(f'{SP}/shots', exist_ok=True); pg.screenshot(path=f'{SP}/shots/filtros_cobertura_390.png')
        b.close()
        ok('sin errores de página ni de consola (castellano, inglés y celular)', not errores, errores[:4])
finally:
    srv.terminate(); srv.wait()
ok.fin()
