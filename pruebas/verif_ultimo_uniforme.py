"""Filtro «Solo el último uniforme» en las combinaciones de 3 (carril filtro2, 5 de octubre de 2026). Ezequiel: «vamos a
agregar un filtro mas en el armado de equipos... El filtro seria. SOLO ultimo uniforme».
1. Modelo aparte, en Python, sobre MFF_SEED_CHARACTERS de data.js: de cada personaje entra su último uniforme (la versión del
   juego más alta de up.update, número por número y la letra después; a igual versión, el número de uniforme del id); sin
   uniformes, la base. Desde los datos de formato 9 (1.0.22) todos los uniformes traen versión (el build la saca de
   /api/updates): un uniforme sin versión es un error del modelo. Lo que tiene que dar con los datos del 5 de octubre:
   Deadpool & Wolverine sobre Nicepool (10.2 los dos), Red Skull — The Crimson Fall y Sister Grimm — Princess Tsukimi (12.2.5)
   como últimos de su personaje, ninguna letra que decida y 17 empates de versión que decide el número. La app (ultimoUniforme) dice lo mismo en los 290 personajes.
2. En pantalla (Deadpool — Deadpool & Wolverine, Puntos para él): «Compañeros: Solo el último uniforme», sin marcar; marcada,
   la nota (qué hace y cómo se elige el último, sin avisos de uniformes sin versión), la cuenta
   «N combinaciones (M sin «Solo el último uniforme»)» con M la de antes y, en cada página, solo compañeros en su último
   uniforme según el modelo.
3. Igual en todos los órdenes (Puntos para él, PvP, PvE y la tier list de Soportes) y para varios focos (vistaConsulta en la
   página): cada fila con los dos compañeros en su último uniforme (el modelo); cada pareja de la lista sin el filtro cuya
   fila ya era de últimos uniformes, con la misma fila; ninguna pareja que no esté sin el filtro; y la cuenta «sin» igual a
   la lista sin el filtro.
4. El personaje de la ficha va con el uniforme elegido (Nicepool y la base de Deadpool): el filtro solo toca a los compañeros.
5. Se guarda como los demás filtros de la pantalla (en la página, como las casillas de cobertura y «Sin»): sigue marcada al
   cambiar de orden, de uniforme y de personaje (Red Skull — The Crimson Fall en la ficha).
6. Inglés; celular (390 px: nada se sale). Capturas: carril-filtro2/shots/ultimo_1300.png y ultimo_390.png. Sin errores de
   página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
SH = SALIDA
DP, NICE, DPB = 'deadpool::deadpool-10800164', 'deadpool::deadpool-10700164', 'deadpool::base'
FOCOS = [DP, 'galactus::base', 'knull::knull-10100241', 'adam-warlock::adam-warlock-10200152', 'apocalypse::apocalypse-10300141']
ORDENES = ['foco', 'pvp', 'pve', 'lista:tv-soportes']

# 1. El modelo, aparte de app.js.
CH = datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS']
def version(u):
    s = u['up']['update']
    m = re.fullmatch(r'(\d+(?:\.\d+)*)([a-z]?)', s)
    assert m, ('versión ilegible', u['id'], s)
    return [int(x) for x in m.group(1).split('.')], m.group(2)
def clave_ver(u):
    n, l = version(u)
    return (n + [0] * (6 - len(n)), l, int(u['id'].rsplit('-', 1)[1]))
MODELO, EMPATES, LETRA_DECIDE = {}, 0, 0
for ch in CH:
    us = ch['uniforms']
    if not us: MODELO[ch['id']] = {ch['id'] + '::base'}; continue
    con = us
    MODELO[ch['id']] = {ch['id'] + '::' + max(con, key=clave_ver)['id']}
    for i, a in enumerate(con):
        for b in con[i + 1:]:
            (na, la), (nb, lb) = version(a), version(b)
            na, nb = na + [0] * (6 - len(na)), nb + [0] * (6 - len(nb))
            if na == nb and la == lb: EMPATES += 1
            elif na == nb: LETRA_DECIDE += 1
ULT = sorted(k for s in MODELO.values() for k in s)
ok('1 modelo: Deadpool & Wolverine sobre Nicepool (los dos de 10.2, decide el número de uniforme)', MODELO['deadpool'] == {DP}, MODELO['deadpool'])
ok('1 modelo: Red Skull — The Crimson Fall y Sister Grimm — Princess Tsukimi (12.2.5) son los últimos de su personaje',
   MODELO['red-skull'] == {'red-skull::red-skull-10300015'} and MODELO['sister-grimm'] == {'sister-grimm::sister-grimm-10300053'},
   (MODELO['red-skull'], MODELO['sister-grimm']))
ok('1 modelo: una variante por personaje (290)', len(MODELO) == 290 and all(len(v) == 1 for v in MODELO.values()), len(MODELO))
ok(f'1 modelo: ninguna letra decide (pares con el mismo número y otra letra: {LETRA_DECIDE}); {EMPATES} empates de versión decide el número',
   LETRA_DECIDE == 0 and EMPATES == 17, (LETRA_DECIDE, EMPATES))
print(f'1 modelo: {len(CH)} personajes, {sum(1 for c in CH if not c["uniforms"])} sin uniformes, {len(ULT)} variantes entran')

GANCHO_FIN = '\narrancar();\n})();'
def gancho(route):
    r = route.fetch(); src = r.text()
    if GANCHO_FIN not in src: raise SystemExit('app.js no termina como se esperaba')
    route.fulfill(response=r, body=src.replace(GANCHO_FIN, '\nwindow.__ev = s => eval(s);' + GANCHO_FIN))

APP = r"""() => Object.fromEntries(CHARS.map(ch => [ch.id, [ultimoUniforme(ch)]]))"""
# 3. Cada foco, cada orden: la vista sin y con el filtro (vistaConsulta), contra el modelo.
ORDEN = r"""([focos, ordenes, ult]) => {
  const U_ = new Set(ult), out = [], par = (a, b) => a.cid < b.cid ? a.cid + '|' + b.cid : b.cid + '|' + a.cid;
  const antes = { eqOrden: ui.eqOrden, eqUltimo: ui.eqUltimo };
  for (const k of focos) {
    const v = allVariants().find(x => x.key === k);
    CONSULTA = null; const q = consultaCon(v);
    for (const o of ordenes) {
      const ctx = o === 'pvp' || o === 'pve' ? o : null;
      if (ctx && !tieneFuncion(v, ctx)) { out.push({ foco: k, orden: o, sinFuncion: true }); continue; }
      Object.assign(ui, { eqOrden: o, eqExcluir: [], eqCon: '', eqCobertura: [], eqVerDescartados: false, eqUltimo: false }); q.vista = null;
      const sin = vistaConsulta(q).filas.slice();
      ui.eqUltimo = true; q.vista = null;
      const con = vistaConsulta(q);
      const filaDe = new Map(sin.map(i => [par(q.pool[q.A[i]], q.pool[q.B[i]]), i])), conPar = new Map(con.filas.map(i => [par(q.pool[q.A[i]], q.pool[q.B[i]]), i]));
      const noUltimo = con.filas.filter(i => !U_.has(q.pool[q.A[i]].key) || !U_.has(q.pool[q.B[i]].key)).length;
      const nueva = [...conPar.keys()].filter(p => !filaDe.has(p)).length;
      const ultimas = [...filaDe].filter(([, i]) => U_.has(q.pool[q.A[i]].key) && U_.has(q.pool[q.B[i]].key));
      const otraFila = ultimas.filter(([p, i]) => conPar.get(p) !== i).length;
      // el orden: las filas del filtro van en el orden de la lista sin filtro (de las que siguen)
      const pos = new Map(sin.map((i, n) => [i, n])), enOrden = con.filas.filter(i => pos.has(i)).every((i, n, xs) => !n || pos.get(xs[n - 1]) < pos.get(i));
      out.push({ foco: k, orden: o, sin: sin.length, con: con.filas.length, sinUltimo: con.sinUltimo, noUltimo, nueva, ultimas: ultimas.length, otraFila, enOrden,
                 foco_igual: true });
    }
  }
  Object.assign(ui, antes, { eqExcluir: [], eqCon: '', eqCobertura: [] }); CONSULTA = null;
  return out;
}"""
TARJETAS = """() => [...document.querySelectorAll('#combos .combo')].map(c => [...c.querySelectorAll('.eqfoto')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base')))"""
FUERA = """() => { const lim = document.getElementById('fcuerpo').getBoundingClientRect().right;
  return [...document.querySelectorAll('#fcuerpo *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > lim + 0.5; })
    .map(e => (e.getAttribute('data-a') || e.className || e.tagName) + ' → ' + Math.round(e.getBoundingClientRect().right)).slice(0, 4); }"""
NOMBRES = {'deadpool': 'Deadpool', 'red-skull': 'Red Skull', 'galactus': 'Galactus'}

def esperar_lista(pg, key):
    pg.wait_for_function("k => window.__ev('CONSULTA && CONSULTA.clave') === k && !window.__ev('ui.eqCalculando')"
                         " && document.querySelector('#combos .eqfiltros')", arg=key, timeout=120000)
    pg.wait_for_timeout(100)
def abrir(pg, key):
    cid, uid = key.split('::')
    pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', NOMBRES[cid]); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid != 'base': pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(150)
    pg.click('[data-a="fichaTab"][data-v="equipos"]')
    esperar_lista(pg, key)
def casilla(pg): return pg.locator('#combos input[data-a="eqUltimo"]')
def cuenta(pg):
    tx = pg.locator('#combos .row > span.muted').first.inner_text()
    nums = [int(re.sub(r'\D', '', n)) for n in re.findall(r'\d[\d.,]*', tx)]
    return nums, tx
def orden(pg, o): pg.select_option('#combos select[data-a="eqOrden"]', o); pg.wait_for_timeout(200)
def paginas(pg, total):
    """Las tarjetas de las páginas 1, 2, 3 y la última (de 20; total: la cuenta), como claves; vuelve a la primera."""
    ult = max(1, -(-total // 20)) - 1
    out = []
    for p in sorted({0, 1, 2, ult} & set(range(ult + 1))):
        bt = pg.locator(f'#combos [data-a="eqPagina"][data-p="{p}"]:not([disabled])')
        if p and bt.count(): bt.first.click(); pg.wait_for_timeout(80)
        out += pg.evaluate(TARJETAS)
    bt = pg.locator('#combos [data-a="eqPagina"][data-p="0"]:not([disabled])')
    if bt.count(): bt.last.click(); pg.wait_for_timeout(80)
    return out, ult

errores = []
def vigilar(pg, nombre):
    pg.on('pageerror', lambda e: errores.append(f'{nombre}: {e}'))
    pg.on('console', lambda m: m.type == 'error' and errores.append(f'{nombre} consola: {m.text}'))

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1300, 'height': 900}); vigilar(pg, 'es')
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)

        # 1. la app contra el modelo
        app = pg.evaluate('(js) => window.__ev(js)()', APP)
        dif = [c for c in MODELO if sorted(MODELO[c]) != app.get(c)]
        ok(f'1 la app elige el mismo último uniforme que el modelo en los {len(MODELO)} personajes', not dif and len(app) == len(MODELO), dif[:4])

        # 3. todos los órdenes, varios focos
        R = pg.evaluate('([js, a]) => window.__ev(js)(a)', [ORDEN, [FOCOS, ORDENES, ULT]])
        pg.set_default_timeout(60000)
        hechas = [r for r in R if not r.get('sinFuncion')]
        mal = [r for r in hechas if r['noUltimo'] or r['nueva'] or r['otraFila'] or r['sinUltimo'] != r['sin'] or not r['enOrden'] or r['con'] > r['sin']]
        ok(f'3 en {len(hechas)} listas ({len(FOCOS)} focos × Puntos para él, PvP, PvE y Soportes, las que tienen función): con el filtro, '
           'solo compañeros en su último uniforme, cada pareja que ya iba con los últimos con la misma fila y en el mismo orden, '
           'ninguna pareja nueva y la cuenta «sin» igual a la lista sin filtro', not mal and len(hechas) >= 16, mal[:3])
        for r in hechas: print(f"3 {r['foco']} {r['orden']}: {r['sin']} → {r['con']} ({r['ultimas']} ya iban con los últimos)")
        menos = [r for r in hechas if r['con'] < r['sin']]
        ok('3 el filtro saca combinaciones en todas las listas que las tienen', len(menos) == len([r for r in hechas if r['sin']]), [(r['foco'], r['orden']) for r in hechas if r not in menos])

        # 2. en pantalla
        abrir(pg, DP)
        n0, tx0 = cuenta(pg)
        fila = casilla(pg).locator('xpath=../..')
        ok('2 «Compañeros: Solo el último uniforme», sin marcar y sin la nota', casilla(pg).count() == 1 and not casilla(pg).is_checked()
           and fila.inner_text().replace('\n', ' ').startswith('Compañeros:') and 'Solo el último uniforme' in fila.inner_text()
           and pg.locator('#combos .ultnota').count() == 0, fila.inner_text())
        casilla(pg).check(); pg.wait_for_timeout(200)
        nota = pg.locator('#combos .ultnota').inner_text()
        ok('2 marcada: la nota dice qué hace y cómo se elige el último', all(x in nota for x in (
            'de cada compañero entra solo su uniforme más nuevo', 'si no tiene uniformes, la base', 'la base no entra',
            "Deadpool — Marvel Studios' Deadpool & Wolverine va con el uniforme elegido", 'versión del juego más alta', 'thanosvibs',
            '9.1.5a antes que 9.1.5b', 'número de uniforme más alto')), nota)
        ok('2 la nota no avisa de uniformes sin versión', 'No se sabe' not in nota and 'Red Skull' not in nota and 'Sister Grimm' not in nota, nota)
        n1, tx1 = cuenta(pg)
        ok('2 la cuenta: «N combinaciones (M sin «Solo el último uniforme»)», con M la de antes y N menos',
           len(n1) == 2 and n1[1] == n0[0] and n1[0] < n0[0] and '(' in tx1 and 'sin «Solo el último uniforme»)' in tx1, (tx0, tx1))
        ts, ult = paginas(pg, n1[0])
        malos = [t for t in ts if any(k not in ULT for k in t if not k.startswith('deadpool::'))]
        ok(f'2 las páginas 1, 2, 3 y la última ({ult + 1}; {len(ts)} tarjetas): ningún compañero fuera de su último uniforme, y él con Deadpool & Wolverine',
           len(ts) >= 61 and not malos and all(DP in t for t in ts), malos[:2])
        pg.locator('#combos .ultnota').scroll_into_view_if_needed()
        os.makedirs(SH, exist_ok=True)
        pg.evaluate("window.scrollTo(0, document.querySelector('#combos').getBoundingClientRect().top + scrollY - 70)")
        pg.screenshot(path=f'{SH}/ultimo_1300.png')

        # 5. sigue marcada al cambiar de orden, de uniforme y de personaje
        sin_funcion = {r['orden'] for r in R if r['foco'] == DP and r.get('sinFuncion')}
        for o in ('pvp', 'pve', 'lista:tv-soportes', 'foco'):
            orden(pg, o)
            if o in sin_funcion:
                ok(f'5 orden {o}: Deadpool — Deadpool & Wolverine no tiene función, así que no hay lista ni filtros', casilla(pg).count() == 0
                   and pg.locator('#combos .combo').count() == 0)
                continue
            ts = pg.evaluate(TARJETAS)
            ok(f'5 orden {o}: sigue marcada, con la nota, y la primera página solo con últimos uniformes', casilla(pg).is_checked()
               and pg.locator('#combos .ultnota').count() == 1 and all(k in ULT for t in ts for k in t if not k.startswith('deadpool::')), len(ts))
        # 4. el personaje de la ficha, con el uniforme elegido
        for uid, key in (('deadpool-10700164', NICE), ('base', DPB)):
            pg.select_option('select[data-a="uniformSel"]', uid); esperar_lista(pg, key)
            ts, _ = paginas(pg, cuenta(pg)[0][0])
            ok(f'4 con {key}: sigue marcada, él va con ese uniforme y los compañeros con su último',
               casilla(pg).is_checked() and ts and all(key in t for t in ts) and all(k in ULT for t in ts for k in t if not k.startswith('deadpool::')),
               (len(ts), ts[:1]))
        abrir(pg, 'red-skull::red-skull-10300015')
        nota = pg.locator('#combos .ultnota').inner_text()
        ok('5 otro personaje (Red Skull — The Crimson Fall): sigue marcada, con la nota y sin avisos',
           casilla(pg).is_checked() and 'Red Skull — The Crimson Fall va con el uniforme elegido' in nota and 'No se sabe' not in nota
           and 'Sister Grimm' not in nota, nota[-300:])
        casilla(pg).uncheck(); pg.wait_for_timeout(200)
        n, tx = cuenta(pg)
        ok('5 desmarcada: sin la nota y la cuenta sola', pg.locator('#combos .ultnota').count() == 0 and len(n) == 1 and 'sin «' not in tx, tx)
        casilla(pg).check(); pg.wait_for_timeout(200)

        # 6. inglés
        abrir(pg, DP)
        pg.click('[data-a="lang"]'); esperar_lista(pg, DP)
        fila = casilla(pg).locator('xpath=../..').inner_text().replace('\n', ' ')
        nota = pg.locator('#combos .ultnota').inner_text()
        n, tx = cuenta(pg)
        ok('6 inglés: «Teammates: Latest uniform only», la nota sin avisos y la cuenta', fila.startswith('Teammates:') and 'Latest uniform only' in fila
           and 'each teammate comes only with its newest uniform' in nota and 'is not known' not in nota
           and 'without «Latest uniform only»' in tx and casilla(pg).is_checked(), (fila, tx))
        resto = [w for w in ('Solo el último', 'Compañeros', 'entra solo', 'No se sabe', ' sin «') if w in pg.locator('#combos').inner_text()]
        ok('6 inglés: sin restos en castellano', not resto, resto)
        pg.click('[data-a="lang"]'); esperar_lista(pg, DP)
        b.close()

        # celular
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True); vigilar(pg, 'celular')
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard')
        abrir(pg, DP)
        casilla(pg).check(); pg.wait_for_timeout(250)
        ok('6 celular: con el filtro y la nota, nada se sale de la columna', not pg.evaluate(FUERA) and pg.evaluate('document.documentElement.scrollWidth') <= 390,
           pg.evaluate(FUERA))
        pg.evaluate("window.scrollTo(0, document.querySelector('#combos input[data-a=\"eqUltimo\"]').getBoundingClientRect().top + scrollY - 200)")
        pg.screenshot(path=f'{SH}/ultimo_390.png')
        b.close()
        ok('sin errores de página ni de consola (castellano, inglés y celular)', not errores, errores[:4])
finally:
    srv.terminate(); srv.wait()
ok.fin()
