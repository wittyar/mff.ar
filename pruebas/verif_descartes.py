"""Descartar combinaciones: se ocultan en las listas de los tres personajes, con cualquier
uniforme; «Ver descartados» las muestra para restaurarlas; en Equipos, la lista de todos.
Cantidades y páginas contra la consulta escrita aparte (la de verif_combos.py)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright
import auditoria_equipos as A
import modelo_foco as F

ok = Chequeo()
C = datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS']
def cid(n): return next(c['id'] for c in C if c['name'] == n)

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

def vista(v, pool, filas, descartes=(), solo_descartados=False, con=''):
    ref = [A.RANGO[x['key']] for x in pool]
    orden = sorted(range(len(filas)), key=lambda n: (-filas[n][2], -filas[n][3], ref[filas[n][0]] + ref[filas[n][1]], n))    # los strikers desempatan
    trios = {tuple(sorted(d)) for d in descartes}
    vistos, out = set(), []
    for n in orden:
        i, j, p, _ = filas[n]; a, b = pool[i], pool[j]
        if con and con not in (a['cid'], b['cid']): continue
        par = tuple(sorted((a['cid'], b['cid'])))
        if par in vistos: continue
        vistos.add(par)
        if (tuple(sorted((v['cid'], a['cid'], b['cid']))) in trios) == solo_descartados: out.append((a, b, p))
    return out

def claves_pagina(pg):
    return [[f"{x.get_attribute('data-cid')}::{x.get_attribute('data-uid') or 'base'}" for x in c.locator('.eqfoto').all()]
            for c in pg.locator('#combos .combo').all()]
def esperadas(v, filas_v):
    """Las claves de cada tarjeta de la primera página, como se pintan: el líder del equipo primero (4 de octubre de 2026)."""
    out = []
    for a, b, _ in filas_v[:20]:
        vs = [v, a, b]; li = A.lider_sin_contexto(vs)
        out.append([x['key'] for x in ([vs[li]] + [x for k, x in enumerate(vs) if k != li] if li is not None else vs)])
    return out
def cuenta(pg): return pg.locator('#combos .row > span.muted').first.inner_text()

def abrir(pg, nombre, uni=''):
    pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid(nombre)}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uni: pg.select_option('select[data-a="uniformSel"]', uni)
    pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)

D = carpeta_datos()
srv, url = levantar(D, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')

        # 1. Annihilus: descartar la primera
        va = A.VAR['annihilus::base']; pool, filas = consulta(va)
        abrir(pg, 'Annihilus')
        primera = claves_pagina(pg)[0]
        trio = sorted(k.split('::')[0] for k in primera)
        pg.locator('#combos .combo').first.locator('[data-a="descartar"]').click(); pg.wait_for_timeout(400)
        capa = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))
        esp = vista(va, pool, filas, [trio])
        ok('1 descartar: se guarda el trío de personajes', capa.get('descartados') == [trio], capa.get('descartados'))
        ok('1 sale de la lista y la cuenta lo dice', claves_pagina(pg) == esperadas(va, esp) and
           cuenta(pg).startswith(f"{len(esp):,}".replace(',', '.') + ' combinaciones') and '· 1 descartado' in cuenta(pg), cuenta(pg))
        ok('1 aparece «Ver descartados (1)»', pg.locator('[data-a="eqVerDescartados"]').inner_text() == 'Ver descartados (1)')

        # 2. en otro de los tres, con otro uniforme: tampoco está
        otro = next(k for k in primera if k.split('::')[0] != 'annihilus')
        c_otro = otro.split('::')[0]; tercero = next(c for c in trio if c not in ('annihilus', c_otro))
        nombre_otro = next(c['name'] for c in C if c['id'] == c_otro)
        unis = [u['id'] for c in C if c['id'] == c_otro for u in c['uniforms']]
        uni = next((u for u in unis if f'{c_otro}::{u}' != otro), '')
        vo = A.VAR[f'{c_otro}::{uni}' if uni else f'{c_otro}::base']
        abrir(pg, nombre_otro, uni)
        pg.select_option('select[data-a="eqCon"]', 'annihilus'); pg.wait_for_timeout(200)
        po, fo = consulta(vo)
        con_desc = vista(vo, po, fo, [trio], con='annihilus')
        ok(f'2 {nombre_otro} con otro uniforme, «Con Annihilus»: el trío no está, y la página coincide',
           claves_pagina(pg) == esperadas(vo, con_desc) and not any(tercero in [k.split('::')[0] for k in fila] for fila in claves_pagina(pg)),
           (vo['key'], cuenta(pg)))

        # 3. ver descartados: está; restaurarlo
        pg.click('[data-a="eqVerDescartados"]'); pg.wait_for_timeout(200)
        vistos = claves_pagina(pg)
        # Con este uniforme: el foco está en la tarjeta, no siempre primero (va primero el líder del trío; con los liderazgos
        # de la API, en este trío lidera Yondu).
        ok('3 «Ver descartados»: solo el trío descartado, con este uniforme', len(vistos) == 1 and sorted(k.split('::')[0] for k in vistos[0]) == trio
           and vo['key'] in vistos[0], vistos)
        pg.locator('#combos [data-a="restaurar"]').click(); pg.wait_for_timeout(400)
        capa = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))
        ok('3 restaurar: sale de la capa; la vista de descartados queda vacía y ofrece volver',
           capa['descartados'] == [] and 'No hay descartados' in pg.locator('#combos').inner_text() and pg.locator('[data-a="eqVerDescartados"]').inner_text() == 'Volver a la lista')
        pg.click('[data-a="eqVerDescartados"]'); pg.wait_for_timeout(200)
        ok('3 de vuelta en la lista, el trío otra vez', claves_pagina(pg) == esperadas(vo, vista(vo, po, fo, [], con='annihilus'))
           and pg.locator('[data-a="eqVerDescartados"]').count() == 0)

        # 4. dos descartes y la lista de Equipos
        abrir(pg, 'Annihilus')
        t1 = sorted(k.split('::')[0] for k in claves_pagina(pg)[0]); pg.locator('#combos .combo').first.locator('[data-a="descartar"]').click(); pg.wait_for_timeout(300)
        t2 = sorted(k.split('::')[0] for k in claves_pagina(pg)[0]); pg.locator('#combos .combo').first.locator('[data-a="descartar"]').click(); pg.wait_for_timeout(300)
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        sec = pg.locator('.section', has_text='Descartados (2)')
        ok('4 Equipos: «Descartados (2)», plegado', sec.count() == 1 and not sec.locator('.combo').first.is_visible())
        sec.locator('summary').click(); pg.wait_for_timeout(150)
        filas_eq = [sorted(x.get_attribute('data-cid') for x in c.locator('.eqfoto').all()) for c in sec.locator('.combo').all()]
        ok('4 los dos tríos, el último primero', filas_eq == [t2, t1], filas_eq)
        sec.locator('.combo').nth(1).locator('[data-a="restaurar"]').click(); pg.wait_for_timeout(400)
        capa = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))
        ok('4 restaurar desde Equipos', capa['descartados'] == [t2], capa['descartados'])
        abrir(pg, 'Annihilus')
        ok('4 en Annihilus queda oculto solo el que sigue descartado', claves_pagina(pg) == esperadas(va, vista(va, pool, filas, [t2])) and '· 1 descartado' in cuenta(pg), cuenta(pg))

        # 5. inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        tx = pg.locator('#combos').inner_text()
        ok('5 inglés', 'Discard' in tx and 'Show discarded (1)' in tx and '1 discarded' in tx, tx[600:900].replace('\n', ' | '))
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
