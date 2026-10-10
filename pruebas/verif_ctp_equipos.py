"""C.T.P. recomendado en cada tarjeta de equipo (pedido de Ezequiel, 3 de octubre de 2026: «el detalle de los
CTPs recomendados en cada caso según el modo de juego»; regla del 4 de octubre: una sola respuesta, con su fuente; del 5
de octubre: las dos fuentes, la guía de armado y la Ideal CTP List, una al lado de la otra), contra un modelo escrito acá
con MFF_GUIA_ARMADO, la Ideal CTP List, MFF_CTPS y MFF_MODOS:
- por integrante, las dos columnas del contexto en la guía de armado: orden PvP o modo del juego de tipo pvp,
  'pvp' y 'pvp_alt'; PvE, 'pve' y 'pve_alt'; sin contexto (puntos para él, una tier list, equipo sin modo, modo
  propio, favorito marcado sin contexto), 'mejor' y 'segundo'. Una columna que la guía no da dice «—» (nunca
  otra columna); si no da ninguna de las dos (o no tiene su fila), «—» en las dos, con el motivo en el title. Y, en
  otra columna, las filas de la Ideal CTP List en las que está (esta variante o, si no, otra del personaje), con «Not
  worth» dicho; si no está, «—» con el motivo;
- las dos fuentes abajo, siempre (la guía con su versión y sus notas, y la Ideal CTP List);
- si la recomendación de una fuente es de otro uniforme, el uniforme va en su celda, con la nota;
- con las columnas en el rótulo: plegado en la tarjeta en tus equipos y favoritos; en las combinaciones y «cómo
  entraría», en la ventana del «Por qué» de la tarjeta (carril modal, 5 de octubre de 2026), que se abre con su botón;
- combinaciones (Adam Warlock — Guardians of the Galaxy 3: pvp Greed+ y pvp_alt Energy+; el mismo trío en
  PvE y en puntos para él), Equipos de tu cuenta (PvP, PvE guardado con el armador, sin modo, modo propio,
  Otherworld Battle de 5), los de la ficha, «cómo entraría» (Black Cat — Winter Criminal) y Favoritos (con el
  contexto en que se marcaron);
- Jeff the Land Shark (su fila de la guía está vacía): «—» de la guía y Liberation de la Ideal CTP List, en la ficha y
  en una tarjeta; Gorr — The God Butcher: Authority de la guía y Conquest de la Ideal CTP List, las dos a la vista;
- solo las tarjetas visibles (una por combinación de la página), en castellano y en inglés, sin errores de
  página ni de consola, y en el celular sin desbordes con el bloque abierto (en la tarjeta o en la ventana)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D0 = datos_js('MFF_SEED_CHARACTERS', 'MFF_GUIA_ARMADO', 'MFF_CTPS', 'MFF_MODOS', 'MFF_SEED', 'MFF_GUIA', 'MFF_SEED_TIERLISTS',
             'MFF_SEED_TIER_ASSIGNMENTS')
CH = {c['id']: c for c in D0['MFF_SEED_CHARACTERS']}
G, CTP = D0['MFF_GUIA_ARMADO'], {c['id']: c['name'] for c in D0['MFF_CTPS']}
# En español, el nombre corto del juego (1.0.33, #43): el del base sin «C.T.P. de», con mayúscula.
_corto = lambda n: (lambda x: x[0].upper() + x[1:])(n.replace('C.T.P. de ', ''))
CTP_LANG = {'en': CTP, 'es': {c['id']: _corto(c['es']['base']) for c in D0['MFF_CTPS']}}
TIPO = {m['id']: m['ctp'] for m in D0['MFF_MODOS']}
FUENTE = D0['MFF_GUIA']['fuentes']['cyn-armado']['nombre']
SEED = D0['MFF_SEED']
COLS = {'pvp': ('pvp', 'pvp_alt'), 'pve': ('pve', 'pve_alt'), None: ('mejor', 'segundo')}
ROT = {'es': {'mejor': 'Mejor', 'segundo': '2.º mejor', 'pve': 'Meta PvE', 'pve_alt': 'Fuera del meta PvE',
              'pvp': 'Meta PvP', 'pvp_alt': 'Fuera del meta PvP'},
       'en': {'mejor': 'Best', 'segundo': '2nd best', 'pve': 'PvE meta', 'pve_alt': 'PvE off-meta',
              'pvp': 'PvP meta', 'pvp_alt': 'PvP off-meta'}}
TXT = {'es': dict(rotulo='C.T.P. recomendados: {a} · {b} · Ideal CTP List', ideal='Ideal CTP List',
                  sin_col='La guía de armado no le da uno en esta columna.',
                  sin_armado='La guía de armado no le da uno en este contexto.',
                  sin_ideal='La Ideal CTP List no lo tiene (ni a otro uniforme del personaje).',
                  not_worth='Ninguno: no vale la pena («Not worth»)', ref='Reforjado', base='Base',
                  nota='Con un uniforme al lado del nombre, la recomendación es para ese (el que tiene la fuente), no para el que lleva en este equipo.'),
       'en': dict(rotulo='Recommended C.T.P.: {a} · {b} · Ideal CTP List', ideal='Ideal CTP List',
                  sin_col='The building guide gives none in this column.',
                  sin_armado='The building guide gives none in this context.',
                  sin_ideal='The Ideal CTP List does not have it (nor another uniform of the character).',
                  not_worth='None: not worth it («Not worth»)', ref='Reforged', base='Base',
                  nota='A uniform next to the name means the recommendation is for that one (the one the source has), not the one used in this team.')}
IDEAL = D0['MFF_GUIA']['ctp_ranking']['lista_ideal']
LI = next(l for l in D0['MFF_SEED_TIERLISTS'] if l['id'] == IDEAL['id'])
ORDEN_IDEAL = [r['id'] for r in LI['rows']]
ROTULO_IDEAL = {r['id']: r['label'] for r in LI['rows']}
ASIG_IDEAL = D0['MFF_SEED_TIER_ASSIGNMENTS'][IDEAL['id']]
FUENTE_IDEAL = [D0['MFF_GUIA']['fuentes'][k]['nombre'] for k in IDEAL['fuente']] + [IDEAL['nombre']]
SP = SALIDA
os.makedirs(SP, exist_ok=True)

# Un personaje propio (no tiene fila en la guía) y un modo propio (sin tipo).
MIO = dict(id='mio-ctp', name='Personaje propio', c=SEED['CLASSES'][0], f=SEED['FACTIONS'][0], r=[], t='T2',
           ins=SEED['INSTINCTS'][0], race=SEED['RACES'][0], gender=SEED['GENDERS'][0], origin='Original MFF',
           abilities=[], tuc=[], stats={}, striker=4, wba='', trans=False, new=False, uniforms=[])
CH[MIO['id']] = MIO
AW_BASE, AW_GG3 = 'adam-warlock::base', 'adam-warlock::adam-warlock-10200152'
EQUIPOS = [
    {'id': 'eq-1', 'name': 'Arena AW', 'modeId': 'team-battle-arena', 'reason': '',
     'members': [AW_BASE, 'stryfe::stryfe-10200168', 'thanos::thanos-10700075']},
    {'id': 'eq-2', 'name': 'Otro mundo', 'modeId': 'otherworld-battle', 'reason': '',
     'members': [AW_GG3, 'knull::knull-10100241', 'thanos::thanos-10700075', 'hulk::hulk-10900002', 'doctor-strange::doctor-strange-10600028']},
    {'id': 'eq-3', 'name': 'Sin modo', 'modeId': '', 'reason': '', 'members': ['mio-ctp::base', 'wong::wong-10300092', 'clea::base']},
    {'id': 'eq-4', 'name': 'Modo propio', 'modeId': 'mio-modo', 'reason': '', 'members': ['hulk::base', 'galactus::base', 'knull::base']},
]
JEFE = ('Jefe', 'world-boss', [AW_GG3, 'doctor-strange::base', 'wong::base'])    # se guarda con el armador
FAVORITO = ['black-cat::black-cat-10400009', 'thanos::thanos-10700075', 'stryfe::stryfe-10200168']
JEFF = 'jeff-the-land-shark::base'
FAVORITO_PVP = [JEFF, 'thanos::thanos-10700075', 'stryfe::stryfe-10200168']    # marcado en el orden PvP
BLACK_CAT_WC = 'black-cat::black-cat-10300009'


def ctx_equipo(mode_id):
    """Tipo de modo de un equipo guardado: el de MODOS en los del juego; sin modo o propio, None."""
    return TIPO.get(mode_id) if mode_id else None


def variantes(cid):
    """Las variantes del personaje, base primero: [(clave, retrato, nombre del uniforme o None)]."""
    c = CH[cid]
    return [(f'{cid}::base', c.get('p'), None)] + [(f"{cid}::{u['id']}", u.get('p'), u['name']) for u in c['uniforms']]


def fila_guia(cid):
    """La fila de la guía del personaje: (clave de la variante, nombre del uniforme o None si es la base, fila)."""
    return next(((k, sub, G['pj'][p]) for k, p, sub in variantes(cid) if p in G['pj']), None)


def ideal_de(key):
    """Las filas de la Ideal CTP List de la variante o, si no está, de otra del personaje: (clave, uniforme, rótulos)."""
    cid = key.split('::')[0]
    vs = variantes(cid)
    for k, _, sub in [x for x in vs if x[0] == key] + [x for x in vs if x[0] != key]:
        fs = sorted(ASIG_IDEAL.get(k) or [], key=ORDEN_IDEAL.index)
        if fs:
            return k, sub, [ROTULO_IDEAL[f] for f in fs]
    return None


def item_ideal(rotulo, lang):
    slug = re.sub(r'[^a-z0-9]', '', rotulo.lower())
    if slug in CTP:
        return dict(ctp=CTP_LANG[lang][slug], ico=True)
    return dict(txt=TXT[lang]['not_worth']) if slug == 'notworth' else dict(sinint=rotulo)


def esperado_fila(key, ctx, lang):
    """La fila de un integrante: su nombre y las celdas (las dos de la guía y la de la Ideal CTP List), cada una con la
    fuente (f) y el uniforme del que sale si no es el suyo (uni: en la primera de la guía y en la de la lista)."""
    cid = key.split('::')[0]
    T, f = TXT[lang], fila_guia(cid)
    uni = lambda k, sub: None if k == key else (sub or T['base'])
    celdas = []
    entradas = [next((x for x in f[2].get('ctp', []) if x['k'] == k), None) for k in COLS[ctx]] if f else [None, None]
    if any(entradas):
        for n, x in enumerate(entradas):
            if x is None:
                c = dict(dash=True, titulo=T['sin_col'])
            elif 'c' in x:
                c = dict(ctp=CTP_LANG[lang][x['c']], ref=T['ref'] if x['r'] else None, ico=True)
            else:
                c = dict(sinint=x['x'])
            celdas.append(dict(f='armado', uni=uni(f[0], f[1]) if n == 0 else None, **c))
    else:
        celdas.append(dict(f='armado', uni=None, sin=T['sin_armado'], colspan=2))
    i = ideal_de(key)
    if i:
        ik, isub, rotulos = i
        celdas.append(dict(f='ideal', uni=uni(ik, isub), ideal=[item_ideal(r, lang) for r in rotulos]))
    else:
        celdas.append(dict(f='ideal', uni=None, sin=T['sin_ideal']))
    return dict(nombre=CH[cid]['name'], celdas=celdas)


def esperado(keys, ctx, lang):
    cols = COLS[ctx]
    filas = [esperado_fila(k, ctx, lang) for k in keys]
    return dict(rotulo=TXT[lang]['rotulo'].format(a=ROT[lang][cols[0]], b=ROT[lang][cols[1]]),
                cols=['', ROT[lang][cols[0]], ROT[lang][cols[1]], TXT[lang]['ideal']], filas=filas,
                nota=[TXT[lang]['nota']] if any(c['uni'] for f in filas for c in f['celdas']) else [],
                notas=len(G['leyenda']['ctp']), fuente=[FUENTE, G['version']] + FUENTE_IDEAL)


# d: el bloque plegado de una tarjeta (details.ga-eq) o la sección de la ventana del «Por qué» (section.ga-eq, con el rótulo
# en su h3): adentro tienen lo mismo.
LEER = r"""(d) => ({
  abierto: d.tagName === 'DETAILS' && d.open,
  rotulo: d.querySelector(':scope > summary, :scope > h3').textContent.trim(),
  cols: [...d.querySelectorAll(':scope > table thead th')].map(th => th.textContent.trim()),
  filas: [...d.querySelectorAll(':scope > table tbody tr')].map(tr => {
    const ctp = (c) => { const r = c.querySelector('.tag.solid');
      return { ctp: c.querySelector(':scope > span:not(.tag)').textContent, ref: r ? r.textContent : null, ico: !!c.querySelector('img.ctpico') }; };
    return { nombre: tr.querySelector('th').textContent.trim(),
             celdas: [...tr.querySelectorAll('td')].map(td => {
               const tag = td.querySelector('.varx'), base = { f: td.dataset.f, uni: tag ? tag.textContent : null };
               const sin = td.querySelector('.ctpsin');
               if (sin) return td.colSpan === 2 ? { ...base, sin: sin.getAttribute('title'), colspan: 2 } : { ...base, sin: sin.getAttribute('title') };
               if (td.dataset.f === 'ideal') return { ...base, ideal: [...td.children].filter(x => !x.classList.contains('varx')).map(x => x.classList.contains('sinint') ? { sinint: x.textContent }
                 : x.classList.contains('row') ? (({ ctp: c, ico }) => ({ ctp: c, ico }))(ctp(x)) : { txt: x.textContent }) };
               const si = td.querySelector('.sinint'), c = td.querySelector('.row');
               if (si) return { ...base, sinint: si.textContent };
               if (c) return { ...base, ...ctp(c) };
               const m = td.querySelector('.muted');
               return { ...base, dash: td.textContent.replace(tag ? tag.textContent : '', '').trim() === '—', titulo: (m && m.getAttribute('title')) || null };
             }) };
  }),
  nota: [...d.querySelectorAll(':scope > p.muted')].map(p => p.textContent.trim()),
  notas: d.querySelectorAll(':scope > details li').length,
  fuente: [...d.querySelectorAll(':scope > .fuentes > *')].map(x => x.textContent.trim()),
})"""


def abrir_ventana(pg, tarjeta):
    """Abre la ventana del «Por qué» de una tarjeta con su botón: la sección de los C.T.P."""
    tarjeta.locator('[data-a="pqAbrir"]').click()
    pg.wait_for_selector('#pqdlg[open] section.ga-eq')
    return pg.locator('#pqdlg section.ga-eq')


def cerrar_ventana(pg):
    pg.keyboard.press('Escape'); pg.wait_for_selector('#pqdlg', state='hidden')


def leer(tarjeta):
    """El bloque de C.T.P. de una tarjeta (tiene que haber uno solo): plegado en ella (tus equipos y favoritos) o en la
    ventana de su «Por qué» (combinaciones y «cómo entraría»), que se abre y se cierra."""
    bloques, boton = tarjeta.locator('details.ga-eq'), tarjeta.locator('[data-a="pqAbrir"]')
    if bloques.count() + boton.count() != 1:
        return dict(error=f'{bloques.count()} bloques de C.T.P. y {boton.count()} botones del «Por qué»')
    if bloques.count():
        return bloques.first.evaluate(LEER)
    sec = abrir_ventana(tarjeta.page, tarjeta)
    r = sec.evaluate(LEER) if sec.count() == 1 else dict(error=f'{sec.count()} bloques de C.T.P. en la ventana')
    cerrar_ventana(tarjeta.page)
    return r


def sin_abierto(x): return {k: v for k, v in x.items() if k != 'abierto'}


def fila_de(r, nombre):
    """La fila de un integrante por su nombre (el líder va primero: el orden de las filas es el de los retratos)."""
    return next(f for f in r['filas'] if f['nombre'] == nombre)


def claves(tarjeta):
    return [f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in tarjeta.locator('.eqfoto').all()]


def comparar_tarjetas(tarjetas, ctx, lang):
    """Cada tarjeta contra el modelo: [(claves, diferencia)] de las que no coinciden y cuántas son."""
    malas = []
    for c in tarjetas:
        ks, r = claves(c), leer(c)
        e = esperado(ks, ctx, lang)
        if sin_abierto(r) != e or r['abierto']:
            malas.append((ks, r, e))
    return malas


def resumen(malas):
    if not malas: return 'todas coinciden'
    ks, r, e = malas[0]
    return dict(n=len(malas), claves=ks, app=r, modelo=e)


def ficha(pg, nombre, cid, uid=None):
    pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid: pg.select_option('select[data-a="uniformSel"]', uid)
    pg.click('[data-a="fichaTab"][data-v="equipos"]')
    pg.wait_for_selector('#combos .combo, #combos .cxnota', timeout=60000)


def orden(pg, o):
    pg.select_option('select[data-a="eqOrden"]', o)
    pg.wait_for_selector('#combos .combo', timeout=60000); pg.wait_for_timeout(150)


def buscar_trio(pg, cids):
    """La tarjeta del trío (el personaje de la ficha y los dos de cids) en el orden elegido: filtra «Con» el
    primero y recorre las páginas. None si no está."""
    pg.select_option('select[data-a="eqCon"]', cids[0]); pg.wait_for_timeout(200)
    while True:
        for c in pg.locator('#combos .combo').all():
            if {k.split('::')[0] for k in claves(c)} == set(cids) | {AW_GG3.split('::')[0]}:    # el líder va primero, sea quien sea
                return c
        sig = pg.locator('#combos [data-a="eqPagina"]')     # el último botón del paginador es «→»
        if not sig.count() or sig.last.is_disabled():
            return None
        sig.last.click(); pg.wait_for_timeout(250)


GANCHO = '\nwindow.__ev = s => eval(s);\narrancar();\n})();'
TRIOS = r"""() => { const q = CONSULTA, out = {}, antes = ui.eqOrden;
  for (const o of ['pvp', 'pve', 'foco']) { ui.eqOrden = o; q.vista = null;
    out[o] = vistaConsulta(q).filas.map(i => [q.pool[q.A[i]].cid, q.pool[q.B[i]].cid].sort().join('|')); }
  ui.eqOrden = antes; q.vista = null; return out; }"""

D = carpeta_datos()
json.dump({'teams': EQUIPOS, 'charNew': [MIO], 'modes': [{'id': 'mio-modo', 'name': 'Mi modo', 'teamSize': 3}],
           'favoritos': [{'id': 'fav-1', 'members': FAVORITO}, {'id': 'fav-2', 'members': FAVORITO_PVP, 'ctx': 'pvp'}]}, open(os.path.join(D, 'capa.json'), 'w', encoding='utf-8'), ensure_ascii=False)
srv, url = levantar(D, origen_local())
errores = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        def gancho(route):
            r = route.fetch(); cuerpo = r.text()
            route.fulfill(response=r, body=cuerpo.replace('\narrancar();\n})();', GANCHO))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard')

        # 1. Adam Warlock — Guardians of the Galaxy 3 (el uniforme de su fila), orden PvP.
        ficha(pg, 'Adam Warlock', 'adam-warlock', AW_GG3.split('::')[1]); orden(pg, 'pvp')
        combos = pg.locator('#combos .combo').all()
        ok('1 PvP: las tarjetas de la página no traen los C.T.P.: van en la ventana del «Por qué» (un botón por tarjeta)',
           len(combos) == 20 and pg.locator('#combos .ga-eq').count() == 0 and pg.locator('#combos [data-a="pqAbrir"]').count() == 20, len(combos))
        malas = comparar_tarjetas(combos, 'pvp', 'es')
        ok('1 PvP: las 20 tarjetas, cada integrante con lo suyo según el modelo (pvp y pvp_alt)', not malas, resumen(malas))
        aw = [fila_de(leer(c), 'Adam Warlock') for c in combos]
        ok('1 PvP: Adam Warlock, Greed reforjado (meta) y Energy reforjado (fuera del meta), sin otro uniforme',
           all(f['celdas'][:2] == [dict(f='armado', uni=None, ctp='Codicia', ref='Reforjado', ico=True),
                                   dict(f='armado', uni=None, ctp='Energía', ref='Reforjado', ico=True)] for f in aw), aw[0])
        primera = combos[0]
        ok('1 PvP: la tarjeta no tiene plegados: el «Por qué» (con los C.T.P.) es el botón que abre la ventana',
           primera.locator('summary').count() == 0 and primera.locator('[data-a="pqAbrir"]').inner_text() == 'Por qué y C.T.P.')
        sec = abrir_ventana(pg, primera)
        ok('1 PvP: se abre con un clic y muestra la tabla y la fuente',
           sec.locator('table').is_visible() and FUENTE in sec.locator('.fuentes a.fuente').all_inner_texts())
        rot = sec.locator('h3').first.text_content().strip()
        ok('1 PvP: el rótulo dice las columnas', rot == 'C.T.P. recomendados: Meta PvP · Fuera del meta PvP · Ideal CTP List', rot)
        sec.scroll_into_view_if_needed(); pg.wait_for_timeout(100)
        pg.locator('#pqdlg').screenshot(path=f'{SP}/ctp_combo_pvp.png')
        cerrar_ventana(pg)

        # 2. El mismo trío en PvE y en puntos para él.
        trios = pg.evaluate('(js) => window.__ev(js)()', TRIOS)
        en_todos = [t for t in trios['pvp'] if t in set(trios['pve']) and t in set(trios['foco'])]
        ok('2 hay tríos que están en las tres listas', bool(en_todos), {k: len(v) for k, v in trios.items()})
        cids = en_todos[0].split('|')
        vistos = {}
        for o, ctx, cols in (('pvp', 'pvp', ('Codicia', 'Energía')), ('pve', 'pve', ('Energía', 'Codicia')), ('foco', None, ('Energía', None))):
            orden(pg, o)
            c = buscar_trio(pg, cids)
            if c is None:
                ok(f'2 {o}: el trío {cids}', False, 'no está'); continue
            r, ks = leer(c), claves(c)
            vistos[o] = ks
            e = esperado(ks, ctx, 'es')
            ok(f'2 {o}: el trío Adam Warlock + {cids} según el modelo ({" y ".join(COLS[ctx])})', sin_abierto(r) == e, (ks, r if sin_abierto(r) != e else ''))
            adam = fila_de(r, 'Adam Warlock')['celdas']
            ok(f'2 {o}: Adam Warlock, {cols[0]} y {cols[1] or "«—» (la guía no le da segundo: no se completa con otra)"}',
               [x.get('ctp') or ('—' if x.get('dash') else None) for x in adam[:2]] == [cols[0], cols[1] or '—'], adam)
            pg.select_option('select[data-a="eqCon"]', ''); pg.wait_for_timeout(150)
        ok('2 el trío es el mismo en los tres órdenes (personajes)', len({tuple(sorted(k.split('::')[0] for k in ks)) for ks in vistos.values()}) == 1, vistos)

        # 3. Una tier list: sin modo, mejor y segundo.
        orden(pg, 'lista:tv-soportes')
        malas = comparar_tarjetas(pg.locator('#combos .combo').all(), None, 'es')
        ok('3 orden por una tier list: mejor y segundo, según el modelo', not malas, resumen(malas))

        # 4. Un integrante sin fila (quitada en memoria: un personaje nuevo que la guía todavía no tiene).
        orden(pg, 'pvp')
        c0 = pg.locator('#combos .combo').first
        ks = claves(c0)
        quitado = next(k for k in ks if not k.startswith('adam-warlock::')).split('::')[0]    # un compañero
        p_fila = next(p for p in [CH[quitado]['p']] + [u['p'] for u in CH[quitado]['uniforms']] if p in G['pj'])
        pg.evaluate('(p) => { window.__fila = window.MFF_GUIA_ARMADO.pj[p]; delete window.MFF_GUIA_ARMADO.pj[p]; }', p_fila)
        orden(pg, 'foco'); orden(pg, 'pvp')
        c0 = pg.locator('#combos .combo').first
        f = leer(c0)['filas'][ks.index(next(k for k in ks if k.startswith(quitado + '::')))]
        fila_py = G['pj'].pop(p_fila)
        e4 = esperado_fila(next(k for k in ks if k.startswith(quitado + '::')), 'pvp', 'es')
        G['pj'][p_fila] = fila_py
        ok(f'4 sin fila en la guía ({CH[quitado]["name"]}): «—» de la guía con el motivo, y la Ideal CTP List igual',
           claves(c0) == ks and f == e4 and f['celdas'][0].get('sin') == TXT['es']['sin_armado'], (f, e4))
        pg.evaluate('(p) => { window.MFF_GUIA_ARMADO.pj[p] = window.__fila; }', p_fila)
        # Un valor que la app no interpreta ({k, x}, puesto en memoria en la fila de Adam Warlock): va tal cual, marcado.
        pg.evaluate('''() => { const e = window.MFF_GUIA_ARMADO.pj.adamwarlock2; window.__ctp = e.ctp;
          e.ctp = e.ctp.map(x => x.k === 'pvp' ? { k: 'pvp', x: 'Greed+ / Rage' } : x); }''')
        orden(pg, 'foco'); orden(pg, 'pvp')
        f = fila_de(leer(pg.locator('#combos .combo').first), 'Adam Warlock')
        sec = abrir_ventana(pg, pg.locator('#combos .combo').first)
        titulo = sec.locator('.sinint').first.get_attribute('title'); cerrar_ventana(pg)
        ok('4 un valor que la app no interpreta: tal cual, marcado, y la otra columna igual',
           f['celdas'][:2] == [dict(f='armado', uni=None, sinint='Greed+ / Rage'), dict(f='armado', uni=None, ctp='Energía', ref='Reforjado', ico=True)]
           and titulo == 'La app no interpreta este valor de la guía: va tal cual.', (f, titulo))
        pg.evaluate('() => { window.MFF_GUIA_ARMADO.pj.adamwarlock2.ctp = window.__ctp; }')

        # 5. Con otro uniforme: Adam Warlock base (la guía es la de Guardians of the Galaxy 3). En PvP no
        #    tiene función (no hay lista): puntos para él.
        ficha(pg, 'Adam Warlock', 'adam-warlock'); orden(pg, 'foco')
        combos = pg.locator('#combos .combo').all()
        malas = comparar_tarjetas(combos, None, 'es')
        r = leer(combos[0])
        ok('5 Adam Warlock base: el uniforme de la guía en su celda y la nota, en todas las tarjetas', not malas
           and fila_de(r, 'Adam Warlock')['celdas'][0]['uni'] == "Marvel Studios' Guardians of the Galaxy 3" and r['nota'] == [TXT['es']['nota']],
           resumen(malas) if malas else fila_de(r, 'Adam Warlock'))

        # 6. Tus equipos en la ficha (Adam Warlock está en Arena AW y en Otro mundo).
        mios = pg.locator('#fcuerpo > .section').nth(0).locator('.card').all()
        nombres = [c.locator('div').first.inner_text() for c in mios]
        bien = []
        for c, n in zip(mios, nombres):
            tt = next(x for x in EQUIPOS if x['name'] == n)
            bien.append(sorted(claves(c)) == sorted(tt['members']) and sin_abierto(leer(c)) == esperado(claves(c), ctx_equipo(tt['modeId']), 'es'))
        ok('6 ficha, en tus equipos: cada tarjeta con el modo de su equipo', nombres == ['Arena AW', 'Otro mundo'] and all(bien), (nombres, bien))

        # 7. Equipos de tu cuenta: uno de PvE guardado con el armador (como verif_escuadras).
        pg.click('[data-a="mesaVaciar"]') if not pg.locator('[data-a="mesaVaciar"]').is_disabled() else None
        pg.fill('[data-a="mesaNombre"]', JEFE[0])
        pg.select_option('select[data-a="mesaModo"]', JEFE[1]); pg.wait_for_timeout(150)
        for k in JEFE[2]:
            pg.evaluate("k => { const b = document.createElement('button'); b.dataset.a = 'mesaPoner'; b.dataset.key = k; document.body.appendChild(b); b.click(); b.remove(); }", k)
            pg.wait_for_timeout(120)
        pg.click('[data-a="mesaGuardar"]'); pg.wait_for_timeout(600)
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        capa = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))
        ok('7 el armador guarda «Jefe» (World Boss, PvE)', capa['teams'][0]['name'] == JEFE[0] and capa['teams'][0]['modeId'] == JEFE[1]
           and capa['teams'][0]['members'] == sorted(JEFE[2]), capa['teams'][0])    # en orden canónico
        sec = pg.locator('.section', has=pg.locator('h3', has_text='Equipos de tu cuenta'))
        tarjetas = sec.locator('.grid > .card').all()
        tipos = {}
        for c, tt in zip(tarjetas, capa['teams']):
            ctx = ctx_equipo(tt['modeId'])
            r, e = leer(c), esperado(claves(c), ctx, 'es')    # en el orden de los retratos: el líder primero
            tipos[tt['name']] = (ctx, len(r.get('filas', [])))
            ok(f"7 «{tt['name']}» ({tt['modeId'] or 'sin modo'}): {' y '.join(COLS[ctx])} por integrante, según el modelo",
               sin_abierto(r) == e and not r['abierto'], '' if sin_abierto(r) == e else (r, e))
        ok('7 los tipos: Arena y Otherworld PvP, Jefe PvE, sin modo y modo propio con mejor y segundo; Otherworld con 5',
           tipos == {'Jefe': ('pve', 3), 'Arena AW': ('pvp', 3), 'Otro mundo': ('pvp', 5), 'Sin modo': (None, 3), 'Modo propio': (None, 3)}, tipos)
        sinf = fila_de(leer(sec.locator('.grid > .card', has_text='Sin modo').first), 'Personaje propio')
        ok('7 el personaje propio (ni en la guía ni en la Ideal CTP List): «—» en las dos, con el motivo de cada una',
           sinf == dict(nombre='Personaje propio', celdas=[dict(f='armado', uni=None, sin=TXT['es']['sin_armado'], colspan=2),
                                                         dict(f='ideal', uni=None, sin=TXT['es']['sin_ideal'])]), sinf)
        favs = pg.locator('.section', has=pg.locator('h3', has_text='Favoritos')).locator('.eqsug').all()
        malas = comparar_tarjetas(favs[:1], None, 'es') + comparar_tarjetas(favs[1:], 'pvp', 'es')
        ok('7 Favoritos: el de antes (sin contexto), mejor y segundo; el marcado en PvP, las columnas de PvP', len(favs) == 2 and not malas, resumen(malas))
        jf = next(f for f in leer(favs[1])['filas'] if f['nombre'] == 'Jeff the Land Shark')
        ok('7 Jeff the Land Shark (su fila de la guía está vacía): «—» de la guía y Liberation de la Ideal CTP List',
           jf['celdas'] == [dict(f='armado', uni=None, sin=TXT['es']['sin_armado'], colspan=2), dict(f='ideal', uni=None, ideal=[dict(ctp='Liberación', ico=True)])]
           and 'marcado en PvP' in favs[1].text_content(), jf)
        otro = sec.locator('.grid > .card', has_text='Otro mundo').first
        otro.locator('details.ga-eq > summary').click(); pg.wait_for_timeout(150)
        otro.screenshot(path=f'{SP}/ctp_otherworld.png')

        # 8. Cómo entraría Black Cat — Winter Criminal en tus equipos: el modo de cada uno.
        ficha(pg, 'Black Cat', 'black-cat', BLACK_CAT_WC.split('::')[1])
        sugs = pg.locator('#fcuerpo > .section').nth(1).locator('.eqsug').all()
        modo = {tt['name']: tt['modeId'] for tt in capa['teams']}
        res = {}
        for c in sugs:
            n = c.locator('b').first.inner_text()
            ks, r = claves(c), leer(c)
            res[n] = sin_abierto(r) == esperado(ks, ctx_equipo(modo[n]), 'es') and BLACK_CAT_WC in ks
        ok('8 cómo entraría: las cinco tarjetas con el modo de su equipo, según el modelo', len(res) == 5 and all(res.values()), res)
        bc = next(f for c in sugs for f in leer(c)['filas'] if f['nombre'] == 'Black Cat')
        ok('8 Black Cat — Winter Criminal: la guía es para Queen in Black', bc['celdas'][0]['uni'] == 'Queen in Black', bc)

        # 8b. La ficha de Jeff the Land Shark (Armado): lo mismo que sus tarjetas, en cada contexto, con la fuente.
        pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
        pg.fill('#q', 'Jeff'); pg.wait_for_timeout(250)
        pg.click('.ccard[data-cid="jeff-the-land-shark"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_selector('ul.ctprec')
        LINEAS = """() => [...document.querySelectorAll('ul.ctprec > li')].map(li => [li.querySelector(':scope > b').textContent,
          ...['armado', 'ideal'].map(f => { const r = li.querySelector('.ctp-' + f); return [
            r.querySelector('.ctpsin') ? 'SIN' : [...r.querySelectorAll(':scope > span.row > span:not(.tag):not(.muted), :scope > span.row:not(.ctpfuente) > span:not(.tag):not(.muted)')].map(x => x.textContent),
            [...r.querySelectorAll('.ctpfuente a.fuente')].map(a => a.textContent)]; })])"""
        lineas = pg.evaluate(LINEAS)
        ok('8b ficha de Jeff, Armado: sin contexto, en PvP y en PvE, «la guía no le da» y Liberation de la Ideal CTP List, cada una con el enlace a su fuente',
           lineas == [[c, ['SIN', [FUENTE]], [['Liberación'], [FUENTE_IDEAL[0]]]] for c in ('Sin contexto', 'PvP', 'PvE')], lineas)
        # Gorr — The God Butcher: la guía dice Authority y la Ideal CTP List, otro (Conquest el 5 de octubre): se ven los dos.
        gorr_ideal = [item_ideal(x, 'es').get('ctp') for x in ideal_de('gorr::base')[2]]
        pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
        pg.fill('#q', 'Gorr'); pg.wait_for_timeout(250)
        pg.click('.ccard[data-cid="gorr"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_selector('ul.ctprec')
        txt = [li.inner_text() for li in pg.locator('ul.ctprec > li').all()]
        ok(f'8b ficha de Gorr: Authority (guía de armado) y {gorr_ideal} (Ideal CTP List) a la vista, con sus fuentes; en PvE la guía no le da',
           len(txt) == 3 and 'Autoridad' not in gorr_ideal and all('Autoridad' in x and FUENTE in x for x in txt[:2])
           and all(all(c in x for c in gorr_ideal) and FUENTE_IDEAL[0] in x for x in txt) and TXT['es']['sin_armado'] in txt[2], txt)
        pg.locator('ul.ctprec').screenshot(path=f'{SP}/ctp_ficha_gorr.png')
        ok('sin errores de página ni de consola (castellano)', not errores, errores[:3])

        # 9. En inglés.
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        sec = pg.locator('.section', has=pg.locator('h3', has_text="Your account's teams"))
        bien = {}
        for c, tt in zip(sec.locator('.grid > .card').all(), capa['teams']):
            bien[tt['name']] = sin_abierto(leer(c)) == esperado(claves(c), ctx_equipo(tt['modeId']), 'en')
        ok('9 inglés: Equipos de tu cuenta según el modelo', len(bien) == 5 and all(bien.values()), bien)
        arena = leer(sec.locator('.grid > .card', has_text='Arena AW').first)
        ok('9 inglés: rótulo, reforjado y la nota', arena['rotulo'] == "Recommended C.T.P.: PvP meta · PvP off-meta · Ideal CTP List"
           and arena['nota'] == [TXT['en']['nota']] and any(x.get('ref') == 'Reforged' for f in arena['filas'] for x in f['celdas']), arena)
        ficha(pg, 'Adam Warlock', 'adam-warlock', AW_GG3.split('::')[1]); orden(pg, 'pve')
        malas = comparar_tarjetas(pg.locator('#combos .combo').all(), 'pve', 'en')
        ok('9 inglés: combinaciones en PvE según el modelo', not malas, resumen(malas))
        sec = abrir_ventana(pg, pg.locator('#combos .combo').first)
        tx = sec.text_content() + pg.locator('#combos').inner_text(); cerrar_ventana(pg)
        ok('9 inglés: sin restos en castellano en el bloque (en la ventana) ni en las tarjetas', all(x not in tx for x in ('recomendados', 'no le da', 'no lo tiene')))
        ok('sin errores de página ni de consola (inglés)', not errores, errores[:3])
        b.close()

        # 10. Celular: el bloque abierto no se sale de la tarjeta ni de la ventana.
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)    # la capa quedó en inglés: de vuelta al castellano
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        for s in pg.locator('details.ga-eq > summary').all(): s.click()
        pg.wait_for_timeout(200)
        desborde = """() => { const out = []; for (const d of document.querySelectorAll('details.ga-eq')) { const lim = d.closest('.card').getBoundingClientRect().right;
          for (const el of d.querySelectorAll('*')) { const r = el.getBoundingClientRect(); if (r.width && r.right > lim + 0.5) out.push(el.className || el.tagName); } }
          return { doc: document.documentElement.scrollWidth, fuera: [...new Set(out)].slice(0, 5) }; }"""
        r = pg.evaluate(desborde)
        ok('10 celular, Equipos: todos los bloques abiertos, sin desborde', pg.locator('details.ga-eq[open]').count() == 7 and r['doc'] <= 390 and not r['fuera'], r)
        pg.locator('.card', has_text='Otro mundo').first.scroll_into_view_if_needed()
        pg.screenshot(path=f'{SP}/ctp_equipos_390.png')
        ficha(pg, 'Adam Warlock', 'adam-warlock'); orden(pg, 'foco')
        sec = abrir_ventana(pg, pg.locator('#combos .combo').first)
        sec.scroll_into_view_if_needed(); pg.wait_for_timeout(200)
        r = pg.evaluate("""() => { const s = document.querySelector('#pqdlg section.ga-eq'), out = [];
          const lim = document.querySelector('#pqdlg .pqm-cuerpo').getBoundingClientRect().right;
          for (const el of s.querySelectorAll('*')) { const r = el.getBoundingClientRect(); if (r.width && r.right > lim + 0.5) out.push(el.className || el.tagName); }
          return { doc: document.documentElement.scrollWidth, fuera: [...new Set(out)].slice(0, 5) }; }""")
        ok('10 celular, combinaciones: los C.T.P. en la ventana, sin desborde', r['doc'] <= 390 and not r['fuera'], r)
        pg.screenshot(path=f'{SP}/ctp_combo_390.png')
        cerrar_ventana(pg)
        ok('sin errores de página ni de consola (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
