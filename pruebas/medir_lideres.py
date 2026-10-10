"""Lo que cambia con los liderazgos de la Leader Skill de la API (carril Q, 5 de octubre de 2026), medido con la app:
por variante, si tiene función en PvP y en PvE y cuántas combinaciones tiene su lista de ese contexto (consultaCon y
vistaConsulta de app.js, servida con un gancho de eval: el archivo no se toca); cuántas variantes tienen liderazgo y
cuántas lo tienen de la API. Los datos salen de MFF_DATOS, como en las demás pruebas.

  MFF_DATOS=CARPETA [MFF_DETALLE=clave,clave] python3 medir_lideres.py SALIDA.json

Con MFF_DETALLE, guarda además cada fila de esas listas (la pareja, el líder y el puntaje de contexto)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar
from playwright.sync_api import sync_playwright

JS = r"""(DETALLE) => {
  const vs = allVariants();
  const lid = v => LIDERAZGOS.filter(k => SOPORTES[v.p] && SOPORTES[v.p][k]).map(k => SOPORTES[v.p][k]);
  const out = { variantes: vs.length, con_liderazgo: vs.filter(v => lid(v).length).length,
                con_api: vs.filter(v => lid(v).some(esDeApi)).length, funcion: {}, listas: {}, ms: {}, retrato: {}, detalle: {} };
  for (const v of vs) out.retrato[v.key] = v.p;
  for (const ctx of ['pvp', 'pve']) {
    ui.eqOrden = ctx;
    const con = vs.filter(v => tieneFuncion(v, ctx));
    out.funcion[ctx] = con.length;
    for (const v of con) {
      const t0 = performance.now();
      CONSULTA = null; const q = consultaCon(v); q.vista = null;
      const filas = vistaConsulta(q).filas;
      out.listas[ctx + '|' + v.key] = filas.length;
      out.ms[ctx + '|' + v.key] = Math.round(performance.now() - t0);
      // El detalle de las listas pedidas: cada fila con su líder y su puntaje de contexto.
      if (DETALLE.includes(v.key)) out.detalle[ctx + '|' + v.key] = Object.fromEntries(filas.map(i => {
        const a = q.pool[q.A[i]], b = q.pool[q.B[i]], e = enContexto([v, a, b], ctx);
        return [[a.key, b.key].sort().join(' + '), { lider: e.lider.key, score: e.score }];
      }));
    }
  }
  ui.eqOrden = 'foco'; CONSULTA = null;
  return out;
}"""

# Las listas de las que se guarda el detalle (fila: líder y puntaje): MFF_DETALLE, claves separadas por comas.
DETALLE = [k for k in os.environ.get('MFF_DETALLE', '').split(',') if k]
t0 = time.time()
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))

        def gancho(route):
            r = route.fetch(); cuerpo = r.text()
            assert cuerpo.count('\narrancar();\n})();') == 1
            route.fulfill(response=r, body=cuerpo.replace('\narrancar();\n})();', '\nwindow.__ev = s => eval(s);\narrancar();\n})();'))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.set_default_timeout(0)
        r = pg.evaluate('([js, d]) => window.__ev(js)(d)', [JS, DETALLE])
        b.close()
finally:
    srv.terminate(); srv.wait()
r['errores'] = errores
json.dump(r, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
for ctx in ('pvp', 'pve'):
    ls = {k: n for k, n in r['listas'].items() if k.startswith(ctx + '|')}
    print(f"{ctx}: con función {r['funcion'][ctx]}, con lista no vacía {sum(1 for n in ls.values() if n)}, "
          f"combinaciones {sum(ls.values())}")
print('variantes', r['variantes'], 'con liderazgo', r['con_liderazgo'], 'de la API', r['con_api'], 'errores', errores,
      f'{time.time() - t0:.0f} s')
