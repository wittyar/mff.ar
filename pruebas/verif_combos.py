"""Combinaciones de 3 de la pestaña Equipos (consulta sobre los datos), contrastadas con la
misma consulta escrita aparte en Python (modelo_foco.py / auditoria_equipos.py):
- todas las parejas con los dos compañeros vinculados con él, una por trío, puntos para él y
  del equipo (con «*» si cuentan un artefacto), líder; cantidad y primera página, en orden por puntos,
  PvP, PvE y una tier list; el puesto de cada uno en la lista, con «+N» si está en más de una fila
- filtros «Con» y «Sin», páginas (y el salto a la lista)
- ★ favoritos: se guardan en la capa, aparecen en Equipos y se arman para la cuenta
- armador: aviso de personaje repetido en otro equipo del mismo modo (no en otro modo)
- cómo entraría en tus otros equipos: igual que antes (sinergia del equipo y vínculo)
- celular sin desbordes."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright
import auditoria_equipos as A
import modelo_foco as F

ok = Chequeo()
D0 = datos_js('MFF_SEED_CHARACTERS', 'MFF_SEED_TIERLISTS', 'MFF_SEED_TIER_ASSIGNMENTS', 'MFF_MODOS')
C, TL, ASIG = D0['MFF_SEED_CHARACTERS'], {l['id']: l for l in D0['MFF_SEED_TIERLISTS']}, D0['MFF_SEED_TIER_ASSIGNMENTS']
TAM = {m['id']: m['equipo']['tam'] for m in D0['MFF_MODOS'] if m.get('equipo') and m['equipo'].get('tam')}
FUERA = """() => { const lim = document.getElementById('fcuerpo').getBoundingClientRect().right;
  return [...document.querySelectorAll('#fcuerpo *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > lim + 0.5; })
    .map(e => (e.getAttribute('data-a') || e.className || e.tagName) + ' → ' + Math.round(e.getBoundingClientRect().right)).slice(0, 4); }"""

def cid(n): return next(c['id'] for c in C if c['name'] == n)
def uid(n, u): return next(x['id'] for c in C if c['name'] == n for x in c['uniforms'] if x['name'] == u)
def full(v): return v['name'] + (' — ' + next(u['name'] for c in C if c['id'] == v['cid'] for u in c['uniforms'] if u['id'] == v['uid']) if v['uid'] else '')
def puesto(lid, key):
    filas = [r['id'] for r in (TL[lid].get('rows') or [])]
    idx = sorted(filas.index(r) for r in ASIG.get(lid, {}).get(key, []) if r in filas)
    return idx[0] if idx else len(filas)
def puesto_txt(lid, key):
    """Lo que dice la tarjeta de su lugar en la lista: la mejor fila y «+N» si está en más (como el roster), o «—»."""
    filas = TL[lid].get('rows') or []
    idx = sorted(i for i, r in enumerate(filas) if r['id'] in ASIG.get(lid, {}).get(key, []))
    return filas[idx[0]]['label'] + (f' +{len(idx) - 1}' if len(idx) > 1 else '') if idx else '—'

def lider(vs):
    """El líder del equipo (Ezequiel, 4 de octubre de 2026): el mismo desde la lista de cualquiera y en cualquier
    orden (auditoria_equipos.lider_sin_contexto)."""
    i = A.lider_sin_contexto(vs)
    return None if i is None else vs[i]

def con_lider(vs, l):
    """Como se pintan: el líder primero (a la izquierda) y los demás en su orden."""
    return [l] + [x for x in vs if x is not l] if l else vs

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
            if F.sueltos_foco(vs): continue
            filas.append((i, j, F.score_foco(vs), F.stk_foco(vs)))
    return pool, filas

def vista(pool, filas, listas=(), excluir=(), con=''):
    pos = [sum(puesto(l, x['key']) for l in listas) for x in pool]
    ref = [A.RANGO[x['key']] for x in pool]
    orden = sorted(range(len(filas)), key=lambda n: (pos[filas[n][0]] + pos[filas[n][1]], -filas[n][2], -filas[n][3], ref[filas[n][0]] + ref[filas[n][1]], n))    # los strikers desempatan
    vistos, out = set(), []
    for n in orden:
        i, j, p, _ = filas[n]; a, b = pool[i], pool[j]
        if a['cid'] in excluir or b['cid'] in excluir or (con and con not in (a['cid'], b['cid'])): continue
        trio = tuple(sorted((a['cid'], b['cid'])))
        if trio in vistos: continue
        vistos.add(trio); out.append((a, b, p))
    return out

def leer_pagina(pg):
    out = []
    for c in pg.locator('#combos .combo').all():
        keys = [f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in c.locator('.eqfoto').all()]
        pts = int(c.locator('.eqpts > b').inner_text())
        tx = c.locator('.eqpts').inner_text()
        ast = re.match(r'\d+(\*?) ', tx).group(1) == '*'
        m = re.search(r'(\d+)(\*?) del equipo', tx)
        lid = c.locator('.combolider').inner_text()
        out.append((keys, pts, ast, int(m.group(1)), m.group(2) == '*', lid))
    return out

def art(vs, f):
    """¿Los puntos cuentan el soporte de un artefacto (llevan «*»)? Uno que le llega a otro integrante y le sirve;
    con foco (f), si lo da él o le llega a él."""
    for i, a in enumerate(vs):
        for k, x, p, alc in A.SOPS[a['key']]:
            bs = [j for j, b in enumerate(vs) if j != i and b['key'] in alc]
            if k == 'artifact' and bs and (f is None or i == f or f in bs): return True
    return False

def esperado_pagina(v, filas_v, pagina=0):
    out = []
    for a, b, p in filas_v[pagina * 20:(pagina + 1) * 20]:
        vs = [v, a, b]; l = lider(vs)
        out.append(([x['key'] for x in con_lider(vs, l)], p, art(vs, 0), A.score(vs), art(vs, None), f'Líder: {full(l)}' if l else 'Ningún liderazgo le suma'))
    return out

def abrir(pg, nombre, u=None):
    pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid(nombre)}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if u: pg.select_option('select[data-a="uniformSel"]', u)
    # lo que va mostrando la lista, en orden (la página se traba mientras calcula: no se puede mirar en el medio)
    pg.evaluate("""() => { window.__combos = []; new MutationObserver(() => { const c = document.getElementById('combos');
      const tx = c ? (c.querySelector('.combo') ? 'lista' : c.innerText) : ''; if (tx && window.__combos[window.__combos.length - 1] !== tx) window.__combos.push(tx); })
      .observe(document.body, { childList: true, subtree: true }); }""")
    t0 = time.time(); pg.click('[data-a="fichaTab"][data-v="equipos"]')
    pg.wait_for_selector('#combos .combo', timeout=60000)
    return time.time() - t0, pg.evaluate('window.__combos')

WONG2 = f"{cid('Wong')}::{uid('Wong', 'Marvel Studios' + chr(39) + ' Doctor Strange 2')}"
AC = 'alliance-conquest'
EQUIPOS = [
    {'id': 'eq-1', 'name': 'Magia AB', 'modeId': 'alliance-battle', 'reason': '', 'members': [f"{cid('Doctor Strange')}::base", f"{cid('Clea')}::base", WONG2]},
    {'id': 'eq-2', 'name': 'Arena', 'modeId': 'team-battle-arena', 'reason': '', 'members': [f"{cid(n)}::base" for n in ('Captain America', 'Iron Man', 'Thor')]},
    {'id': 'eq-3', 'name': 'Conquista 1', 'modeId': AC, 'reason': '', 'members': [f"{cid(n)}::base" for n in ('Enchantress', 'Black Cat', 'Yondu')]},
]
D = carpeta_datos()
json.dump({'teams': EQUIPOS}, open(os.path.join(D, 'capa.json'), 'w', encoding='utf-8'), ensure_ascii=False)
srv, url = levantar(D, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')

        # 1. Annihilus: la consulta entera contra la escrita aparte
        v = A.VAR['annihilus::base']
        t0 = time.time(); pool, filas = consulta(v); tpy = time.time() - t0
        dt, aviso = abrir(pg, 'Annihilus')
        ok('1 primero el aviso, después la lista', len(aviso) == 2 and 'Calculando' in aviso[0] and aviso[1] == 'lista',
           f'{dt * 1000:.0f} ms hasta la lista (Python: {tpy:.1f} s)')
        fv = vista(pool, filas)
        cuenta = int(re.sub(r'\D', '', pg.locator('#combos .row > span.muted').first.inner_text()))
        ok('1 misma cantidad de combinaciones (una por trío)', cuenta == len(fv), (cuenta, len(fv)))
        app, esp = leer_pagina(pg), esperado_pagina(v, fv)
        ok('1 primera página: mismos tríos, uniformes, puntos para él, del equipo y líder', app == esp,
           [(x[0][1:], x[1], x[2], x[3]) for x in app[:2]] if app != esp else f'{len(app)} filas')
        ok('1 nada de Nick Fury (solo da a héroes)', not any(k.startswith('nick-fury') for a, b_, _ in fv for k in (a['key'], b_['key'])))

        # 2. orden por una tier list (desde 1.0.14, PvP y PvE son contextos con su propio puntaje:
        #    los prueba verif_contexto.py)
        for orden, listas in (('lista:tv-soportes', ['tv-soportes']),):
            pg.select_option('select[data-a="eqOrden"]', orden); pg.wait_for_timeout(150)
            fo = vista(pool, filas, listas)
            app, esp = leer_pagina(pg), esperado_pagina(v, fo)
            lineas = pg.locator('#combos .combo').first.locator('.combotx div.muted').all_inner_texts()
            ok(f'2 orden {orden}: primera página igual a la escrita aparte, con los puestos a la vista', app == esp and
               all(lineas[k].startswith(TL[lid]['name'] + ':') for k, lid in enumerate(listas)),
               [(x[0][1:], x[1]) for x in app[:2]] if app != esp else lineas)
            # el puesto de cada integrante, con «+N» si está en más de una fila (como el roster)
            mal, varias = [], 0
            for c in pg.locator('#combos .combo').all():
                keys = [f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in c.locator('.eqfoto').all()]
                tx = c.locator('.combotx div.muted').all_inner_texts()
                for k, lid in enumerate(listas):
                    esp_l = TL[lid]['name'] + ': ' + ' · '.join(puesto_txt(lid, key) for key in keys)
                    varias += sum(' +' in puesto_txt(lid, key) for key in keys)
                    if tx[k] != esp_l: mal.append((tx[k], esp_l))
            ok(f'2 orden {orden}: cada puesto como en el roster, con «+N» si está en más de una fila', not mal, (mal[:2], varias))
        pg.select_option('select[data-a="eqOrden"]', 'foco'); pg.wait_for_timeout(150)

        # 3. filtros y páginas
        pg.select_option('select[data-a="eqExcluir"]', cid('Enchantress')); pg.wait_for_timeout(150)
        fx = vista(pool, filas, excluir={cid('Enchantress')})
        cuenta = int(re.sub(r'\D', '', pg.locator('#combos .row > span.muted').first.inner_text()))
        ok('3 «Sin Enchantress»: cantidad y primera página', cuenta == len(fx) and leer_pagina(pg) == esperado_pagina(v, fx), (cuenta, len(fx)))
        pg.select_option('select[data-a="eqCon"]', cid('Valkyrie')); pg.wait_for_timeout(150)
        fc = vista(pool, filas, excluir={cid('Enchantress')}, con=cid('Valkyrie'))
        app = leer_pagina(pg)
        ok('3 «Con Valkyrie»: todas la tienen', app == esperado_pagina(v, fc) and all(any(k.startswith('valkyrie') for k in x[0]) for x in app), len(fc))
        pg.select_option('select[data-a="eqCon"]', ''); pg.wait_for_timeout(100)
        pg.locator('[data-a="eqPagina"][data-p="1"]').first.click(); pg.wait_for_timeout(250)
        top = pg.evaluate("document.getElementById('combos').getBoundingClientRect().top")
        ok('3 página 2: las filas 21 a 40 y la lista arriba', leer_pagina(pg) == esperado_pagina(v, fx, 1) and 0 <= top < 400, round(top))
        pg.locator('[data-a="eqIncluir"]').first.click(); pg.wait_for_timeout(150)
        ok('3 volver a incluir', pg.locator('[data-a="eqIncluir"]').count() == 0 and leer_pagina(pg) == esperado_pagina(v, fv))

        # 4. favoritos
        fila = pg.locator('#combos .combo').nth(1)
        keys = fila.locator('[data-a="favorito"]').get_attribute('data-m').split(',')    # él primero, como en la lista
        fila.locator('[data-a="favorito"]').click(); pg.wait_for_timeout(500)
        capa = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))
        ok('4 ★ se guarda en la capa y queda marcada', [f['members'] for f in capa.get('favoritos', [])] == [keys]
           and pg.locator('#combos .combo').nth(1).locator('[data-a="favorito"]').inner_text() == '★', capa.get('favoritos'))
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        favs = pg.locator('.section', has_text='Favoritos').locator('.eqsug')
        l = lider([A.VAR[k] for k in keys])
        vsf = [A.VAR[k] for k in keys]
        ok('4 Equipos: el favorito con su líder y su sinergia (con «*» si cuenta un artefacto)', favs.count() == 1
           and (f'Líder: {full(l)}' if l else 'Ningún liderazgo suma') in favs.first.inner_text()
           and f"{A.score(vsf)}{'*' if art(vsf, None) else ''} pts de sinergia" in favs.first.inner_text(), favs.first.inner_text().replace('\n', ' | ')[:160])

        # 5. armar para la cuenta: aviso de repetido en el mismo modo
        favs.first.locator('[data-a="teamDesde"]').click(); pg.wait_for_timeout(300)
        pg.select_option('select[data-a="mesaModo"]', 'team-battle-arena'); pg.wait_for_timeout(150)
        en_tba = {k.split('::')[0] for k in EQUIPOS[1]['members']}
        ok('5 Team Battle Arena: avisa solo por los de «Arena»', pg.locator('.mesa .avisoeq').count() == sum(1 for k in keys if k.split('::')[0] in en_tba))
        pg.select_option('select[data-a="mesaModo"]', AC); pg.wait_for_timeout(150)
        en_ac = {k.split('::')[0] for k in EQUIPOS[2]['members']}
        rep = [A.VAR[k]['name'] for k in keys if k.split('::')[0] in en_ac]
        avisos = pg.locator('.mesa .avisoeq').all_inner_texts()
        ok('5 mismo modo (Alliance Conquest): avisa a cuáles ya usás en «Conquista 1»',
           len(avisos) == len(rep) and all(any(n in a_ and 'Conquista 1' in a_ for a_ in avisos) for n in rep), (rep, avisos))
        pg.locator('.section', has_text='Favoritos').locator('[data-a="favorito"]').click(); pg.wait_for_timeout(400)
        capa = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))
        ok('4 quitar la ★ desde Equipos', capa['favoritos'] == [] and pg.locator('.section', has_text='Favoritos').count() == 0)

        # 6. Wong (Doctor Strange 2): cómo entraría y la primera página
        dt2, _ = abrir(pg, 'Wong', WONG2.split('::')[1])
        tx = pg.locator('#fcuerpo > .section').nth(1).inner_text()
        # Arena (Captain America, Iron Man y Thor, las bases): sin ningún liderazgo, Wong no se vincula con nadie; con los
        # que el build deriva de la Leader Skill (carril Q: Captain America, HP +30%; Iron Man, Skill Cooldown −24%), el
        # líder le da algo, y el cambio no mejora la sinergia.
        con_lid = [n for n in ('Captain America', 'Iron Man', 'Thor') if any(k in A.SOP.get(A.VAR[f"{cid(n)}::base"]['p'], {}) for k in ('leader', 'leader2'))]
        arena = 'No mejoran con él: Arena' if con_lid else 'Sin vínculo con nadie del equipo: Arena'
        ok(f'6 cómo entraría: «{arena}» (con liderazgo en Arena: {con_lid or "nadie"}); Conquista 1 sí', arena in tx and 'Conquista 1' in tx, tx[:200].replace('\n', ' | '))
        vw = A.VAR[WONG2]; pw, fw = consulta(vw); fvw = vista(pw, fw)
        ok('6 Wong: primera página igual a la escrita aparte', leer_pagina(pg) == esperado_pagina(vw, fvw), f'{dt2 * 1000:.0f} ms')
        ok('sin errores de página', not errores, errores[:3])
        b.close()

        # 7. celular
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        abrir(pg, 'Annihilus')
        pg.select_option('select[data-a="eqExcluir"]', cid('Enchantress')); pg.wait_for_timeout(150)
        ok('7 celular: nada se sale de la columna', not pg.evaluate(FUERA) and pg.evaluate('document.documentElement.scrollWidth') <= 390, pg.evaluate(FUERA))
        pg.screenshot(path=f'{SALIDA}/combos_390.png', full_page=False)
        ok('sin errores de página (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
