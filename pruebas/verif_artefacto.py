"""La pasiva del artefacto exclusivo (Ezequiel, 10 de octubre de 2026): en Skills como una skill más, sin sacarla de
Armado, y en el filtro del roster «Su artefacto da» con las categorías del índice. Los personajes que tiene que dejar
el filtro se cuentan acá, con los stats del artefacto (los de `fx`) y las categorías escritas aparte de app.js."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_ARTEFACTOS')
C, A = D['MFF_SEED_CHARACTERS'], D['MFF_ARTEFACTOS']
por_nombre = {c['name']: c for c in C}
ART = {a['p']: a for a in A}
# Las categorías del índice que puede dar un artefacto, con sus stats (CATEGORIAS de app.js, más las anti-mermas
# de la tabla de valor).
CATS = {'atk': {'All Basic Attacks', 'All Basic Attacks (Stackable)'}, 'evasion': {'Ignore Dodge'}, 'vida': {'HP'},
        'mermas': {'Remove All Debuffs', 'Debuff Immunity'}, 'hielo': {'Cold Damage'}}


def esperado(cats):
    stats = set().union(*(CATS[c] for c in cats))
    return {c['id'] for c in C if c['p'] in ART and stats & {f['s'] for f in ART[c['p']]['fx']}}


def resultados(pg):
    """Todas las entradas del roster filtrado (vista tabla, todas las páginas) con su línea del índice."""
    out = {}
    while True:
        for tr in pg.locator('tr[data-a="open"]').all():
            k = tr.get_attribute('data-cid') + '::' + (tr.get_attribute('data-uid') or 'base')
            out[k] = tr.locator('.indlinea').inner_text() if tr.locator('.indlinea').count() else ''
        sig = pg.locator('[data-a="page"]', has_text='→')
        if not sig.count() or sig.is_disabled(): break
        sig.click(); pg.wait_for_timeout(80)
    return out


srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')

        # 1. Agent Venom: la pasiva del artefacto en Skills y en Armado
        av = por_nombre['Agent Venom']
        pg.fill('#q', 'Agent Venom'); pg.wait_for_timeout(300)
        pg.click(f'.ccard[data-cid="{av["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(150)
        sk = pg.locator('#sk-artefacto')
        ok('1 Skills: la pasiva del artefacto', sk.count() == 1 and ART[av['p']]['name'] in sk.inner_text(),
           sk.inner_text()[:120] if sk.count() else 'no está')
        pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(150)
        ok('1 Armado la sigue mostrando', pg.locator('#artefacto .artl').count() > 0)
        pg.screenshot(path=f'{SALIDA}/artefacto_ficha_1300.png')
        sin = next(c for c in C if c['p'] not in ART)
        pg.click('[data-a="back"]'); pg.fill('#q', sin['name']); pg.wait_for_timeout(300)
        pg.click(f'.ccard[data-cid="{sin["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(150)
        ok(f'1 sin artefacto ({sin["name"]}), sin el bloque en Skills', pg.locator('#sk-artefacto').count() == 0)

        # 2. el filtro del roster
        pg.click('[data-a="back"]'); pg.fill('#q', ''); pg.wait_for_timeout(200)
        if pg.locator('[data-a="clearFilters"]').count(): pg.locator('[data-a="clearFilters"]').first.click()
        if not pg.locator('.filterpanel').count(): pg.click('[data-a="toggleFilters"]')
        pg.click('[data-a="view"][data-v="table"]'); pg.wait_for_timeout(150)
        for cats in (['evasion'], ['evasion', 'atk'], ['mermas']):
            for c in cats:
                if not pg.locator(f'[data-a="filter"][data-cat="art"][data-v="{c}"].on').count():
                    pg.click(f'[data-a="filter"][data-cat="art"][data-v="{c}"]'); pg.wait_for_timeout(100)
            r = resultados(pg); got = {k.split('::')[0] for k in r}
            esp = esperado(cats)
            ok(f'2 su artefacto da {cats}: {len(esp)} personajes', got == esp and esp,
               {'faltan': sorted(esp - got)[:4], 'sobran': sorted(got - esp)[:4]})
            malas = [(k, x) for k, x in r.items() if not x.startswith('Artefacto:')]
            ok(f'2 {cats}: cada fila dice qué da su artefacto', not malas, malas[:3])
            pg.locator('[data-a="clearFilters"]').first.click(); pg.wait_for_timeout(100)
            if not pg.locator('.filterpanel').count(): pg.click('[data-a="toggleFilters"]'); pg.wait_for_timeout(100)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
