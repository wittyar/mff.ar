"""Histórico de los personajes (Ezequiel, 5 de octubre de 2026: «una pestaña de histórico... cada cambio con el link a su
nota»; primero solo los personajes). Datos de formato 10 (MFF_HISTORICO, scripts/historico.py), contra un modelo escrito
acá con MFF_HISTORICO y MFF_SEED_CHARACTERS:
1. Datos: cada hecho nombra una variante (o un personaje, en balance) del roster, una versión de MFF_HISTORICO.versiones
   (o ninguna, con su fecha) y una nota de MFF_HISTORICO.notas (o ninguna); los tipos son los seis; cada llegada de
   thanosvibs está una vez; Red Skull — The Crimson Fall y Sister Grimm — Princess Tsukimi llegan en la 12.2.5 con la
   nota del 21 de septiembre (1896518) y el texto que los nombra.
2. La pestaña (#24: cada versión plegada, la primera abierta, con cuántos hechos de cada tipo; las notas una vez, arriba;
   una fila por personaje con sus hechos): el botón «Histórico» en la barra; título, nota, los filtros; sin filtros, los grupos del modelo (versiones
   con algo y notas sin versión, de la más nueva a la más vieja), de a 20, con «Más versiones»; cada grupo con la versión,
   el nombre y la fecha de thanosvibs y los links a sus notas; cada hecho con su tipo, a quién (el botón abre su ficha) y
   el link a la nota o el aviso de que la nota no lo nombra; el texto en inglés, plegado.
3. Filtros: por personaje (Red Skull: lo del modelo, y la 12.2.5 primera, con el uniforme y el Tier-4) y por tipo (solo
   ese tipo); los dos juntos; «Nada con estos filtros» cuando no hay nada.
4. La ficha (pestaña Más): el bloque «Historial» con los grupos del personaje del modelo y el botón que abre el
   Histórico filtrado por él. Gorr: su llegada (personaje) con su nota.
5. Los links van al foro oficial (forum.netmarble.com/futurefight_en/view/<tablero>/<id>, el 2196 de notas o el 2213 de avisos), en otra pestaña.
6. Inglés, celular sin desbordes, capturas y sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D0 = datos_js('MFF_HISTORICO', 'MFF_SEED_CHARACTERS', 'MFF_MODOS')
H, CH = D0['MFF_HISTORICO'], {c['id']: c for c in D0['MFF_SEED_CHARACTERS']}
SH = SALIDA
os.makedirs(SH, exist_ok=True)
TIPOS = ['personaje', 'uniforme', 't3', 'tp', 't4', 'balance', 'modo']
MODOS = {m['id']: m for m in D0['MFF_MODOS']}
VERS = {v[0]: v for v in H['versiones']}

# 1. Datos.
mal = []
for x in H['hechos']:
    k, t, v, n, txt = x[:5]
    cid, _, uid = k.partition('::')
    if t == 'modo':   # 1.0.34 (#4): la clave es «modo:<id de MFF_MODOS>»
        if not k.startswith('modo:') or k[5:] not in MODOS: mal.append(('clave de modo', x[:4]))
    elif cid not in CH or (uid and uid != 'base' and not any(u['id'] == uid for u in CH[cid]['uniforms'])): mal.append(('clave', x[:4]))
    if t not in TIPOS: mal.append(('tipo', x[:4]))
    if t != 'modo' and (t == 'balance') == ('::' in k): mal.append(('clave de balance', x[:4]))
    if v is not None and v not in VERS: mal.append(('versión', x[:4]))
    if v is None and (len(x) < 6 or t not in ('balance', 'modo')): mal.append(('sin versión', x[:4]))
    if t == 'modo' and (n is None or not txt): mal.append(('modo sin nota', x[:4]))
    if n is not None and str(n) not in H['notas']: mal.append(('nota', x[:4]))
    if n is None and txt: mal.append(('texto sin nota', x[:4]))
ok('1 cada hecho: variante del roster, tipo, versión y nota que existen', not mal, mal[:4])
# #24: la nota va una vez, en la cabecera de la versión; un hecho con versión tiene que citar una de las notas de su versión.
fuera = [x[:4] for x in H['hechos'] if x[2] is not None and x[3] is not None and x[3] not in VERS[x[2]][3]]
ok('1 la nota de cada hecho es una de las de su versión', not fuera, fuera[:4])
llegadas = [(x[0], x[1]) for x in H['hechos'] if x[1] not in ('balance', 'modo')]
modos_con = {x[0][5:] for x in H['hechos'] if x[1] == 'modo'}
ok('1 modos: los hechos de modo nombran modos de MFF_MODOS, y casi todos tienen alguno', modos_con <= set(MODOS) and len(modos_con) >= len(MODOS) - 2,
   sorted(set(MODOS) - modos_con))
wb = [x for x in H['hechos'] if x[0] == 'modo:world-boss']
ok('1 Jefe mundial: con sus notas, el título de la sección que lo nombra primero', len(wb) >= 10 and all('world boss' in x[4][0].lower() for x in wb), len(wb))
ok('1 cada llegada de thanosvibs, una vez', len(llegadas) == len(set(llegadas)), len(llegadas) - len(set(llegadas)))
for key, nombre in (('red-skull::red-skull-10300015', 'Red Skull'), ('sister-grimm::sister-grimm-10300053', 'Sister Grimm')):
    u = next(x for x in H['hechos'] if x[0] == key and x[1] == 'uniforme')
    ok(f'1 {key}: uniforme de la 12.2.5 con la nota del 21 de septiembre y el texto que lo nombra',
       u[2] == '12.2.5' and u[3] == 1896518 and any(nombre in l for l in u[4]), u)


def grupos(filtro):
    """Los grupos del modelo: (orden, clave) — versión o nota sin versión — con sus hechos, del más nuevo al más viejo."""
    por_v, sin_v = {}, {}
    for x in H['hechos']:
        if not filtro(x): continue
        (por_v.setdefault(x[2], []) if x[2] is not None else sin_v.setdefault(x[3], [])).append(x)
    out = [(v[2], 'v:' + v[0], por_v[v[0]]) for v in H['versiones'] if v[0] in por_v]
    out += [(H['notas'][str(n)][1], 'n:' + str(n), hs) for n, hs in sin_v.items()]
    out.sort(key=lambda g: g[0], reverse=True)    # sort estable, como el de la app
    return out


LEER = r"""() => [...document.querySelectorAll('.hiversion')].map(g => ({
  cab: g.querySelector('.hicab').textContent.replace(/\s+/g, ' ').trim(),
  abierta: g.open,
  cuenta: [...g.querySelectorAll('.hicab .hicuenta .tag')].map(x => x.textContent.trim()),
  links: [...g.querySelectorAll(':scope > .hinotas > a')].map(a => a.getAttribute('href')),
  target: [...g.querySelectorAll(':scope > .hinotas > a')].map(a => a.target),
  filas: [...g.querySelectorAll('.hifila')].map(f => ({
    quien: f.querySelector('.hiquien [data-a="open"]') ? [f.querySelector('.hiquien [data-a="open"]').dataset.cid, f.querySelector('.hiquien [data-a="open"]').dataset.uid]
         : f.querySelector('.hiquien [data-a="verModo"]') ? ['modo:' + f.querySelector('.hiquien [data-a="verModo"]').dataset.id, ''] : null,
    hechos: [...f.querySelectorAll('.hihecho')].map(li => ({
      tipo: li.querySelector('.tag').textContent.trim(),
      nota: li.querySelector('.hinota a') ? li.querySelector('.hinota a').getAttribute('href') : null,
      sin: !!li.querySelector(':scope > .muted:not(.hitexto1)'),
      lineas: li.querySelectorAll('.hitexto li').length + (li.querySelector('summary') ? 1 : 0) + li.querySelectorAll('.hitexto1').length,
      lang: li.querySelector('.hitexto, .hitexto1') ? li.querySelector('.hitexto, .hitexto1').getAttribute('lang') : null })) })) }))"""
ROT = {'es': {'personaje': 'Personaje nuevo', 'uniforme': 'Uniforme', 't3': 'Tier-3', 'tp': 'Potencial Trascendido', 't4': 'Tier-4',
              'balance': 'Skills y balance', 'modo': 'Modo de juego'},
       'en': {'personaje': 'New character', 'uniforme': 'Uniform', 't3': 'Tier-3', 'tp': 'Potential Transcendence', 't4': 'Tier-4',
              'balance': 'Skills and balance', 'modo': 'Game mode'}}
ORD = {t: i for i, t in enumerate(TIPOS)}


def esperado(gs, lang):
    """#24: cada versión plegada (la primera abierta), con cuántos hechos de cada tipo en la cabecera, sus notas una vez y
    una fila por variante (o personaje, en balance) con sus hechos, en el orden de los tipos; la nota de un hecho solo si la
    versión tiene más de una."""
    out = []
    for i, (_, clave, hs) in enumerate(gs):
        hs = sorted(hs, key=lambda x: ORD[x[1]])
        ids = list(VERS[clave[2:]][3]) if clave.startswith('v:') else [int(clave[2:])]
        varias = len(ids) > 1
        filas = {}
        for x in hs: filas.setdefault(x[0], []).append(x)
        out.append(dict(clave=clave, abierta=i == 0, links=[H['notas'][str(n)][2] for n in ids], target=['_blank'] * len(ids),
          cuenta=[f'{ROT[lang][k]} {n}' for k in TIPOS for n in [sum(1 for x in hs if x[1] == k)] if n],
          filas=[dict(quien=[k.split('::')[0], '' if '::' not in k or k.endswith('::base') else k.split('::')[1]], hechos=[dict(
            tipo=ROT[lang][x[1]], nota=H['notas'][str(x[3])][2] if x[3] is not None and varias else None, sin=x[3] is None and x[1] not in ('balance', 'modo'),
            lineas=len(x[4]), lang='en' if x[4] else None) for x in fx]) for k, fx in filas.items()]))
    return out


def comparar(app, esp):
    """[(grupo, app, modelo)] de los que difieren (sin la cabecera, que se mira aparte)."""
    dif = []
    for i, (a, e) in enumerate(zip(app, esp)):
        if any(a[k] != e[k] for k in ('abierta', 'cuenta', 'links', 'target', 'filas')):
            dif.append((i, e['clave'], a, e))
    if len(app) != len(esp): dif.append(('cantidad', len(app), len(esp)))
    return dif


D = carpeta_datos()
srv, url = levantar(D, origen_local())
errores = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.goto(url); pg.wait_for_selector('.ccard')

        # 2. La pestaña, sin filtros.
        boton = pg.locator('nav.topnav [data-a="goHistorico"]')
        ok('2 «Histórico» en la barra', boton.count() == 1 and boton.inner_text() == 'Histórico', boton.count())
        boton.click(); pg.wait_for_selector('.hiversion')
        h1 = lambda: pg.evaluate("document.querySelector('main h1').firstChild.textContent.trim()")
        ok('2 título, nota (en el «?») y filtros', h1() == 'Histórico'
           and 'foro oficial' in pg.locator('.page-head h1 details.ayuda').text_content() and pg.locator('select[data-a="hiPj"]').count() == 1
           and pg.locator('[data-a="hiTipo"]').count() == 8 and pg.locator('select[data-a="hiPj"] optgroup').count() == 2)
        todos = grupos(lambda x: True)
        app = pg.evaluate(LEER)
        dif = comparar(app, esperado(todos[:20], 'es'))
        ok(f'2 sin filtros: los 20 primeros de los {len(todos)} grupos del modelo, con sus hechos y links', not dif, dif[:1])
        v0 = VERS[todos[0][1][2:]]
        ok('2 la cabecera: versión, nombre y fecha de thanosvibs', app[0]['cab'].startswith(f'{v0[0]} · {v0[1]} · {v0[2]}'), (app[0]['cab'][:120], v0))
        cuenta = pg.locator('.page-head + .row + p.muted').inner_text()
        ok('2 la cuenta de grupos', cuenta == f'{len(todos)} versiones con algo', cuenta)
        ok('2 sin la fecha de nuevo en cada hecho: la nota va una vez por versión', pg.locator('.hiversion').first.locator('.hinotas').count() == 1)
        pg.click('[data-a="hiMas"]'); pg.wait_for_timeout(200)
        app = pg.evaluate(LEER)
        ok('2 «Más versiones»: 40', len(app) == 40 and not comparar(app, esperado(todos[:40], 'es')), len(app))
        pg.screenshot(path=f'{SH}/historico_1300.png')
        ok('5 los links van al foro oficial, en otra pestaña', all(re.fullmatch(r'https://forum\.netmarble\.com/futurefight_en/view/(2196|2213)/\d+', l)
                                                                  for g in app for l in g['links'] + [h_['nota'] for f in g['filas'] for h_ in f['hechos'] if h_['nota']])
           and all(x == '_blank' for g in app for x in g['target']))

        # 3. Filtros.
        pg.select_option('select[data-a="hiPj"]', 'red-skull'); pg.wait_for_timeout(200)
        rs = grupos(lambda x: x[0].split('::')[0] == 'red-skull')
        app = pg.evaluate(LEER)
        ok('3 Red Skull: lo del modelo', not comparar(app, esperado(rs[:20], 'es')), comparar(app, esperado(rs[:20], 'es'))[:1])
        ok('3 Red Skull: la 12.2.5 primero, con The Crimson Fall (uniforme) y el Tier-4, con la nota del 21 de septiembre',
           app[0]['cab'].startswith('12.2.5') and [h_['tipo'] for f in app[0]['filas'] for h_ in f['hechos']] == ['Uniforme', 'Tier-4']
           and any(l.endswith('/1896518') for l in app[0]['links']), app[0])
        pg.click('[data-a="hiTipo"][data-v="balance"]'); pg.wait_for_timeout(200)
        rsb = grupos(lambda x: x[0].split('::')[0] == 'red-skull' and x[1] == 'balance')
        app = pg.evaluate(LEER)
        ok('3 Red Skull y «Skills y balance»: lo del modelo, o «Nada con estos filtros»',
           (not comparar(app, esperado(rsb[:20], 'es'))) and (bool(rsb) or 'Nada con estos filtros.' in pg.locator('main').inner_text()), len(rsb))
        pg.select_option('select[data-a="hiPj"]', ''); pg.click('[data-a="hiTipo"][data-v="t4"]'); pg.wait_for_timeout(200)
        t4 = grupos(lambda x: x[1] == 't4')
        app = pg.evaluate(LEER)
        ok('3 solo Tier-4: lo del modelo, y ningún otro tipo', not comparar(app, esperado(t4[:20], 'es'))
           and all(h_['tipo'] == 'Tier-4' for g in app for f in g['filas'] for h_ in f['hechos']), len(app))
        sin = next(c for c in CH if not any(x[0].split('::')[0] == c and x[1] == 'tp' for x in H['hechos']))
        pg.select_option('select[data-a="hiPj"]', sin); pg.click('[data-a="hiTipo"][data-v="tp"]'); pg.wait_for_timeout(200)
        ok(f'3 {sin} sin Potencial Trascendido: «Nada con estos filtros.»', pg.locator('.hiversion').count() == 0
           and 'Nada con estos filtros.' in pg.locator('main').inner_text())
        pg.click('[data-a="hiTipo"][data-v="todos"]'); pg.select_option('select[data-a="hiPj"]', '')

        # 7. Los modos de juego (1.0.34, #4): el filtro por modo, el botón que lleva a Modos y el «Historial» de cada modo.
        pg.select_option('select[data-a="hiPj"]', 'modo:world-boss'); pg.wait_for_timeout(200)
        wbg = grupos(lambda x: x[0] == 'modo:world-boss')
        app = pg.evaluate(LEER)
        ok('7 Jefe mundial: lo del modelo', not comparar(app, esperado(wbg[:20], 'es')), comparar(app, esperado(wbg[:20], 'es'))[:1])
        ok('7 Jefe mundial: cada hecho es «Modo de juego», con la sección en inglés', app and all(h_['tipo'] == 'Modo de juego' and h_['lang'] == 'en'
           for g in app for f in g['filas'] for h_ in f['hechos']), app[:1])
        pg.select_option('select[data-a="hiPj"]', ''); pg.click('[data-a="hiTipo"][data-v="modo"]'); pg.wait_for_timeout(200)
        mg = grupos(lambda x: x[1] == 'modo')
        ok('7 solo «Modo de juego»: lo del modelo', not comparar(pg.evaluate(LEER), esperado(mg[:20], 'es')), comparar(pg.evaluate(LEER), esperado(mg[:20], 'es'))[:1])
        quien = pg.locator('.hiquien [data-a="verModo"]').first
        mid = quien.get_attribute('data-id'); quien.click(); pg.wait_for_selector(f'#modo-{mid}.on')
        ok('7 el nombre de un modo abre Modos con ese modo abierto y a la vista', pg.evaluate(f"document.getElementById('modo-{mid}').getBoundingClientRect().top") < 400)
        mh = grupos(lambda x: x[0] == 'modo:' + mid)
        app = pg.evaluate(LEER.replace("document.querySelectorAll('.hiversion')", f"document.querySelectorAll('#modo-{mid} .hiversion')"))
        ok(f'7 Modos, {mid}: «Historial» con las {min(5, len(mh))} versiones más recientes del modelo, sin repetir el modo en cada fila',
           not comparar(app, [dict(e, filas=[dict(f, quien=None) for f in e['filas']]) for e in esperado(mh[:5], 'es')]), comparar(app, esperado(mh[:5], 'es'))[:1])
        pg.locator(f'#modo-{mid}').screenshot(path=f'{SH}/historial_modo.png')
        pg.click(f'#modo-{mid} [data-a="goHistorico"]'); pg.wait_for_selector('.hiversion')
        ok('7 «Ver todo en el Histórico»: la pestaña filtrada por el modo', pg.locator('select[data-a="hiPj"]').input_value() == 'modo:' + mid
           and not comparar(pg.evaluate(LEER), esperado(mh[:20], 'es')))
        pg.click('[data-a="hiTipo"][data-v="todos"]'); pg.select_option('select[data-a="hiPj"]', '')

        # 4. La ficha de Gorr, pestaña Más.
        pg.evaluate("document.querySelector('nav.topnav [data-a=\"back\"]').click()"); pg.wait_for_selector('#q')
        pg.fill('#q', 'Gorr'); pg.wait_for_timeout(250)
        pg.click('.ccard[data-cid="gorr"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="fuentes"]'); pg.wait_for_selector('#historial')
        go = grupos(lambda x: x[0].split('::')[0] == 'gorr')
        app = pg.evaluate(LEER.replace("document.querySelectorAll('.hiversion')", "document.querySelectorAll('#historial .hiversion')"))
        ok('4 ficha de Gorr: «Historial» con lo del modelo', pg.locator('#historial h3').text_content() == 'Historial'
           and not comparar(app, esperado(go, 'es')), comparar(app, esperado(go, 'es'))[:1])
        ok('4 Gorr: su llegada como personaje, con su nota', any(h_['tipo'] == 'Personaje nuevo' and g['links'] and not h_['sin']
                                                                for g in app for f in g['filas'] for h_ in f['hechos']), app[-1:])
        pg.locator('#historial').screenshot(path=f'{SH}/historial_gorr.png')
        pg.click('#historial [data-a="goHistorico"]'); pg.wait_for_selector('.hiversion')
        ok('4 «Ver en el Histórico»: la pestaña filtrada por Gorr', pg.locator('select[data-a="hiPj"]').input_value() == 'gorr'
           and not comparar(pg.evaluate(LEER), esperado(go[:20], 'es')))
        # Un hecho abre la ficha de su variante.
        pg.locator('.hiquien [data-a="open"]').first.click(); pg.wait_for_selector('.fcab')
        ok('2 el nombre de un hecho abre su ficha', 'Gorr' in pg.locator('.fcab').text_content())
        ok('sin errores de página ni de consola (castellano)', not errores, errores[:3])

        # 6. Inglés.
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.click('nav.topnav [data-a="goHistorico"]'); pg.wait_for_selector('.hiversion')
        app = pg.evaluate(LEER)
        ok('6 inglés: título, botón y lo del modelo (desde la barra, sin filtro de personaje)', h1() == 'History'
           and pg.locator('nav.topnav [data-a="goHistorico"]').inner_text() == 'History' and not comparar(app, esperado(todos[:20], 'en')))
        tx = pg.locator('main').inner_text()
        ok('6 inglés: sin restos en castellano', all(w not in tx for w in ('Personaje nuevo', 'Histórico', 'versiones con algo', 'Todos')), tx[:200])
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        b.close()

        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.evaluate("document.querySelector('nav.topnav [data-a=\"goHistorico\"]').click()"); pg.wait_for_selector('.hiversion')
        pg.evaluate("document.querySelectorAll('.hiversion').forEach((d, i) => { if (i < 3) d.open = true; })")
        for d in pg.locator('.hihecho details').all()[:8]: d.locator('summary').click()
        r = pg.evaluate("""() => ({ doc: document.documentElement.scrollWidth,
          fuera: [...document.querySelectorAll('.hiversion *')].filter(el => { if (!el.checkVisibility()) return false; const r = el.getBoundingClientRect(); return r.width && r.right > innerWidth + 0.5; })
            .map(el => el.className || el.tagName).slice(0, 5) })""")
        ok('6 celular: sin desbordes, con textos abiertos', r['doc'] <= 390 and not r['fuera'], r)
        pg.screenshot(path=f'{SH}/historico_390.png')
        ok('sin errores de página ni de consola (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
