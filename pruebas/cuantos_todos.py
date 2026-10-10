"""Combinaciones que muestra la pestaña Equipos para cada personaje (su variante base), sin filtros:
consultaCon + vistaConsulta de la app, servida con un gancho de eval (el archivo no se toca)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar
from playwright.sync_api import sync_playwright
JS = r"""() => CHARS.map(ch => { const v = variant(ch.id, null); CONSULTA = null;
  const q = consultaCon(v), vista = vistaConsulta(q); const r = [ch.id, vista.filas.length]; CONSULTA = null; return r; })"""
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        def gancho(route):
            r = route.fetch(); cuerpo = r.text()
            assert cuerpo.count('\narrancar();\n})();') == 1
            route.fulfill(response=r, body=cuerpo.replace('\narrancar();\n})();', '\nwindow.__ev = s => eval(s);\narrancar();\n})();'))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.set_default_timeout(0)
        r = pg.evaluate('(js) => window.__ev(js)()', JS)
        b.close()
finally:
    srv.terminate(); srv.wait()
json.dump(r, open(f'{SALIDA}/cuantos_todos.json', 'w'))
xs = sorted(n for _, n in r)
print('personajes', len(xs), 'mediana', statistics.median(xs), 'min', xs[0], 'p10', xs[len(xs)//10], 'p25', xs[len(xs)//4],
      'p75', xs[len(xs)*3//4], 'p90', xs[len(xs)*9//10], 'max', xs[-1])
for lo, hi in ((0, 1000), (1000, 3000), (3000, 6000), (6000, 10000), (10000, 20000), (20000, 30000), (30000, 50000)):
    print(f'{lo}-{hi}:', sum(lo <= n < hi for n in xs))
print('menos:', sorted(r, key=lambda x: x[1])[:8]); print('más:', sorted(r, key=lambda x: -x[1])[:8])
