"""De dónde salen los puntos de contexto de tríos puntuales, con el texto de la app (detalleContexto)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar
from playwright.sync_api import sync_playwright
TRIOS = json.loads(sys.argv[1])   # [[ctx, k1, k2, k3], ...]
JS = r"""(trios) => {
  const porKey = new Map(allVariants().map(x => [x.key, x]));
  return trios.map(([c, ...ks]) => { const vs = ks.map(k => porKey.get(k)); const e = enContexto(vs, c, true);
    if (!e) return [c, ks.map(k => fullLabel(porKey.get(k))), null];
    const roles = vs.map(x => { const r = rolEn(x, c); return [fullLabel(x), r.dps, r.soporte, r.lider, r.striker]; });
    return [c, roles, e.score, e.partes, fullLabel(e.lider), detalleContexto(e, vs, c)]; });
}"""
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page()
        def gancho(route):
            r = route.fetch(); cuerpo = r.text()
            route.fulfill(response=r, body=cuerpo.replace('\narrancar();\n})();', '\nwindow.__ev = s => eval(s);\narrancar();\n})();'))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)
        R = pg.evaluate('([js, t]) => window.__ev(js)(t)', [JS, TRIOS])
        b.close()
finally:
    srv.terminate(); srv.wait()
for r in R:
    print('\n==', r[0].upper(), '|', r[2], r[3] if len(r) > 3 else '', '| líder:', r[4] if len(r) > 4 else '')
    for x in r[1]: print('   ', x)
    if len(r) > 5:
        txt = re.sub(r'<li>', '\n    · ', r[5]); txt = re.sub(r'<[^>]+>', '', txt)
        print(txt.replace('&amp;', '&').replace('&#39;', "'").replace('&quot;', '"'))
