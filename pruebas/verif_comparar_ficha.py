"""Comparar desde la ficha (1.0.50, Ezequiel, 28 de octubre de 2026): «+ Comparar esta versión» lleva al roster con las
versiones de ese personaje primero, en el orden elegido, y lo dice arriba de la lista; si no tiene otras versiones, la
lista queda como está. Contra un modelo armado acá desde data.js (sin app.js):
  1. Dormammu (base): las primeras tarjetas son todas sus versiones, en orden de lanzamiento, el aviso, y después el
     resto del roster en su orden; la cuenta no cambia.
  2. Un personaje sin uniformes: ni aviso ni otro orden.
  3. Salir de «Comparar»: el orden de siempre, sin aviso.
Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_HISTORICO')
PJ = {c['id']: c for c in D['MFF_SEED_CHARACTERS']}
FECHA = {v[0]: v[2] for v in D['MFF_HISTORICO']['versiones']}
LLEGA = {x[0]: FECHA[x[2]] for x in D['MFF_HISTORICO']['hechos'] if x[1] in ('personaje', 'uniforme')}
SOLO = next(c['id'] for c in PJ.values() if not c['uniforms'])
ok('modelo: Dormammu tiene más de una versión', len(PJ['dormammu']['uniforms']) >= 1)

def claves(c): return [f'{c["id"]}::base'] + [f'{c["id"]}::{u["id"]}' for u in c['uniforms']]
def tarjetas(pg): return pg.evaluate("[...document.querySelectorAll('.ccard')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base'))")
def abrir(pg, cid):
    pg.evaluate("""(cid) => { const el = document.createElement('button'); el.dataset.a = 'open'; el.dataset.cid = cid;
        document.body.appendChild(el); el.click(); el.remove(); }""", cid)
    pg.wait_for_selector('.fcab')

errores = []
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1366, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' else None)
        pg.goto(url); pg.wait_for_selector('.ccard')
        antes = tarjetas(pg); cuenta = pg.inner_text('.count')

        # 1. Dormammu
        abrir(pg, 'dormammu'); pg.click('[data-a="pickThis"]'); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(200)
        suyas = claves(PJ['dormammu'])
        ahora = tarjetas(pg)
        fechas = [LLEGA[k] for k in ahora[:len(suyas)]]
        ok('Dormammu: primero todas sus versiones, de la más nueva a la más vieja',
           sorted(ahora[:len(suyas)]) == sorted(suyas) and fechas == sorted(fechas, reverse=True), (ahora[:len(suyas)], fechas))
        resto = [k for k in antes if not k.startswith('dormammu::')]
        ok('Dormammu: después, el resto del roster en el orden de siempre', ahora[len(suyas):] == resto[:len(ahora) - len(suyas)],
           (ahora[len(suyas):len(suyas) + 3], resto[:3]))
        aviso = pg.locator('.pickprimero')
        ok('Dormammu: lo dice arriba de la lista', aviso.count() == 1 and 'Dormammu' in aviso.inner_text(), aviso.all_inner_texts())
        ok('Dormammu: la cuenta no cambia (no es un filtro)', pg.inner_text('.count').split()[-1] == cuenta.split()[-1], (pg.inner_text('.count'), cuenta))
        ok('Dormammu: la versión de la ficha ya está elegida', pg.locator('.ccard[data-cid="dormammu"][data-uid=""] .pick.on').count() == 1)

        # 3. salir de «Comparar»
        pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(200)
        ok('fuera de «Comparar»: el orden de siempre, sin aviso', tarjetas(pg) == antes and pg.locator('.pickprimero').count() == 0)

        # 2. un personaje sin uniformes
        abrir(pg, SOLO); pg.click('[data-a="pickThis"]'); pg.wait_for_selector('.ccard'); pg.wait_for_timeout(200)
        ok(f'{PJ[SOLO]["name"]} (sin uniformes): ni aviso ni otro orden', tarjetas(pg) == antes and pg.locator('.pickprimero').count() == 0)
        ok('sin errores de página ni de consola', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
