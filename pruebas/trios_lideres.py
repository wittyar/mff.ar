"""Los tríos de la lista de un contexto de una variante, con su líder (para ver qué cambia con los liderazgos de la
API). MFF_DATOS dice qué datos. python3 trios_lideres.py CLAVE CTX SALIDA.json"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar
from playwright.sync_api import sync_playwright
JS = r"""([clave, ctx]) => {
  const v = allVariants().find(x => x.key === clave);
  ui.eqOrden = ctx; CONSULTA = null; const q = consultaCon(v); q.vista = null;
  const filas = vistaConsulta(q).filas, out = {};
  for (const i of filas) {
    const vs = [q.v, q.pool[q.A[i]], q.pool[q.B[i]]], e = enContexto(vs, ctx);
    out[[vs[1].key, vs[2].key].sort().join(' + ')] = { lider: e.lider.key, score: e.score };
  }
  ui.eqOrden = 'foco'; CONSULTA = null;
  return out;
}"""
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        def gancho(route):
            r = route.fetch(); cuerpo = r.text()
            route.fulfill(response=r, body=cuerpo.replace('\narrancar();\n})();', '\nwindow.__ev = s => eval(s);\narrancar();\n})();'))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)
        r = pg.evaluate('([js, a]) => window.__ev(js)(a)', [JS, sys.argv[1:3]])
        b.close()
finally:
    srv.terminate(); srv.wait()
json.dump(r, open(sys.argv[3], 'w'), ensure_ascii=False)
print(len(r), 'tríos')
