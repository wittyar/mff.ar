"""Por qué un trío entra o no en la lista de un contexto: vínculos (por soportes y bonos, G; con el líder sin contexto
y con el del contexto, carril Q, segunda parte), DPS del contexto y enContexto. MFF_DATOS dice qué
datos. python3 trio_detalle.py FOCO OTRO1 OTRO2 CTX"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar
from playwright.sync_api import sync_playwright
JS = r"""([foco, a, b, ctx]) => {
  const V = k => allVariants().find(x => x.key === k);
  const v = V(foco); CONSULTA = null; const q = consultaCon(v);
  let i = -1; for (let j = 0; j < q.n; j++) { const x = q.pool[q.A[j]].key, y = q.pool[q.B[j]].key; if ((x === a && y === b) || (x === b && y === a)) { i = j; break; } }
  const vs = [v, V(a), V(b)], e = enContexto(vs, ctx);
  // Vínculos (1, el primero; 2, el segundo): por soportes y bonos (G), con el líder sin contexto y con el del contexto.
  return { par: i, G: i >= 0 ? q.G[i] : null, F_sin_contexto: i >= 0 ? vinculosFila(q, i, q.L[i]) : null,
           F_contexto: i >= 0 && e ? vinculosFila(q, i, [q.v, q.pool[q.A[i]], q.pool[q.B[i]]].indexOf(e.lider)) : null,
           A: i >= 0 ? q.pool[q.A[i]].key : null,
           dps: vs.map(x => [x.key, rolEn(x, ctx)]), contexto: e ? { lider: e.lider.key, score: e.score } : null,
           lider_sin: liderDe(vs, null) && liderDe(vs, null).key,
           anti: vs.map(x => [x.key, LIDERAZGOS.map(k => SOPORTES[x.p] && SOPORTES[x.p][k] ? SOPORTES[x.p][k].fx.map(f => f.s).join('+') + (esDeApi(SOPORTES[x.p][k]) ? ' (api)' : '') : null)]) };
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
        print(json.dumps(pg.evaluate('([js, a]) => window.__ev(js)(a)', [JS, sys.argv[1:5]]), ensure_ascii=False, indent=1))
        b.close()
finally:
    srv.terminate(); srv.wait()
