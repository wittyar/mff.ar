"""A qué skill de la ficha se le atribuye un soporte de Leads & Supports (skillDeSoporte, #25): por el nombre que le da
Leads & Supports solo si esa skill da lo que da el soporte. Jeff the Land Shark: su «Pasiva 4★ (secundaria)» (Jeff's Cuddle
Buddy) es su Activa 5, que la da. Polaris — Uncanny X-Men: Leads & Supports llama «Magnetic Pulse» (el nombre de su Activa
1) a su Tier-2; la Activa 1 no la da, así que va en la Tier-2. Se mira en el «Cómo funciona» de cada skill (sus liderazgos
y soportes, .tipls)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_SKILLS')
por_nombre = {c['name']: c for c in D['MFF_SEED_CHARACTERS']}


def indice(p, sl):
    return next(i for i, s in enumerate(D['MFF_SKILLS'][p]) if s['sl'] == sl)


def soportes_de(pg, si):
    """Los nombres de los soportes que el «Cómo funciona» de la skill si muestra (vacío si no tiene)."""
    pg.click(f'#skt-{si}'); pg.wait_for_selector('#skpop')
    pop = pg.locator('#skpop')
    out = pop.locator('.tipls .sop').all_text_contents() if pop.locator('.tipls').count() else []
    pg.click('[data-a="tipCerrar"]'); pg.wait_for_timeout(150)
    return out


def abrir(pg, nombre, p):
    c = por_nombre[nombre]
    pg.evaluate("() => window.scrollTo(0, 0)")
    if pg.locator('[data-a="back"]').count():
        pg.click('[data-a="back"]')
    pg.fill('#q', nombre); pg.wait_for_timeout(300)
    pg.click(f'.ccard[data-cid="{c["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if p != c['p']:
        pg.select_option('select[data-a="uniformSel"]', next(u['id'] for u in c['uniforms'] if u['p'] == p)); pg.wait_for_timeout(250)
    pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(200)


srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')

        abrir(pg, 'Polaris', 'polaris1')
        t2, a1 = soportes_de(pg, indice('polaris1', 'Tier-2 Passive')), soportes_de(pg, indice('polaris1', 'Active 1'))
        ok('Polaris — Uncanny X-Men: el soporte de Tier-2 va en su Tier-2', any('Magnetic Pulse' in x for x in t2), t2)
        ok('Polaris — Uncanny X-Men: y no en su Activa 1 (que se llama como ese soporte en Leads & Supports)', not a1, a1)

        abrir(pg, 'Jeff the Land Shark', 'jeffthelandshark')
        a5 = soportes_de(pg, indice('jeffthelandshark', 'Active 5'))
        ok("Jeff the Land Shark: Jeff's Cuddle Buddy (su soporte secundario) sigue en su Activa 5", any("Jeff's Cuddle Buddy" in x for x in a5), a5)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
