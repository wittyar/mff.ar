"""Opciones de uniforme en Armado: para el uniforme abierto, los cinco uniformes que habilitan
sus opciones contra /api/uniforms de thanosvibs (work/uniforms.json), en orden Advanced →
Mythic, y el stat de cada rango de la guía de principiantes. Base: lo dice. Celular."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js, RAIZ
from playwright.sync_api import sync_playwright
ok = Chequeo()
U = json.load(open(f'{RAIZ}/work/uniforms.json'))
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_GUIA')
var_de = {}
for c in D['MFF_SEED_CHARACTERS']:
    var_de[c['p']] = (c['id'], '')
    for u in c['uniforms']: var_de[u['p']] = (c['id'], u['id'])
unis = [(c, u) for c in D['MFF_SEED_CHARACTERS'] for u in c['uniforms']]
random.seed(7); muestra = random.sample(unis, 25)
RANGOS = ['Advanced', 'Rare', 'Heroic', 'Legendary', 'Mythic']
STAT = {k: v['es'] for k, v in D['MFF_GUIA']['stats'].items()}
MEJOR = [[('el ataque del personaje' if k == 'ataque' else STAT[k]) for k in r['mejor']] for r in D['MFF_GUIA']['opciones_uniforme']['rangos']]
def texto(loc): return loc.evaluate('e => { const c = e.cloneNode(true); c.querySelectorAll("details.ayuda").forEach(d => d.remove()); return c.textContent.replace(/\\s+/g, " ").trim(); }')
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        for c, u in muestra:
            pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
            pg.fill('#q', c['name']); pg.wait_for_timeout(200)
            pg.click(f'.ccard[data-cid="{c["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
            pg.select_option('select[data-a="uniformSel"]', u['id']); pg.wait_for_timeout(100)
            pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(150)
            filas = pg.locator('.opuni .opfila').all()
            vista = [(texto(f.locator('b').first), (f.locator('.minipj').get_attribute('data-cid'), f.locator('.minipj').get_attribute('data-uid') or ''),
                      texto(f.locator('.opstat'))) for f in filas]
            esperado = [(RANGOS[i], var_de[pp], ' › '.join(MEJOR[i])) for i, pp in enumerate(U[u['p']]['options'])]
            ok(f"{c['name']} / {u['name']}", vista == esperado, vista if vista != esperado else '')
        # base
        pg.select_option('select[data-a="uniformSel"]', 'base'); pg.wait_for_timeout(150)
        ok('base: dice que no tiene opciones', 'El uniforme base no tiene opciones' in texto(pg.locator('#fcuerpo')) and pg.locator('.opuni').count() == 0)
        # tocar un uniforme de la tabla abre su ficha
        pg.select_option('select[data-a="uniformSel"]', muestra[-1][1]['id']); pg.wait_for_timeout(150)
        destino = var_de[U[muestra[-1][1]['p']]['options'][0]]
        pg.locator('.opuni .opfila').first.locator('.minipj').click(); pg.wait_for_timeout(250)
        ok('tocar el uniforme de una opción abre su ficha, en Armado', pg.locator('select[data-a="uniformSel"]').input_value() == (destino[1] or 'base')
           and pg.locator('.ftab.on').get_attribute('data-v') == 'armado', destino)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.goto(url); pg.wait_for_selector('.ccard')
        c, u = muestra[0]
        pg.fill('#q', c['name']); pg.wait_for_timeout(200)
        pg.click(f'.ccard[data-cid="{c["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.select_option('select[data-a="uniformSel"]', u['id']); pg.wait_for_timeout(100)
        pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(200)
        fuera = pg.evaluate("""() => [...document.querySelectorAll('.fcuerpo *')].filter(e => { const r = e.getBoundingClientRect();
          return r.width && r.right > innerWidth + 0.5 && !e.closest('details:not([open])'); }).map(e => e.className || e.tagName).slice(0, 4)""")
        ok('celular: Armado no se sale de la pantalla', not fuera, fuera)
        pg.locator('.bloque', has=pg.locator('.opuni')).screenshot(path=f'{SALIDA}/opuni_390.png')
        b.close()
finally:
    srv.terminate(); srv.wait()

ok.fin()
