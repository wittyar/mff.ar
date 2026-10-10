"""Casos para ajustar los pesos del puntaje de contexto: para cada personaje foco y cada contexto,
todos los tríos que entran (los que muestra la pestaña Equipos con el orden PvP o PvE), con las
cuentas de cada parte (sin pesar) y los desempates del orden. Usa el código de la app (enContexto,
consultaCon), no un modelo aparte."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar
from playwright.sync_api import sync_playwright
SP = PRUEBAS
FOCOS = sys.argv[1].split(',')
SALIDA = sys.argv[2]
# Opcional: JS que se corre antes (para probar una regla distinta) y los contextos a recorrer.
PREVIO = sys.argv[3] if len(sys.argv) > 3 else ''
CTXS = sys.argv[4].split(',') if len(sys.argv) > 4 else ['pvp', 'pve']

JS = r"""([focos, ctxs]) => {
  const porKey = new Map(allVariants().map(x => [x.key, x]));
  const out = { peso: Object.assign({}, PESO), focos: {} };
  for (const k of focos) {
    const v = porKey.get(k); if (!v) { out.focos[k] = null; continue; }
    CONSULTA = null; const q = consultaCon(v);
    const pool = q.pool.map(x => x.key);
    const res = { pool, ctx: {} };
    for (const c of ctxs) {
      const ls = (c === 'pvp' ? LISTAS_PVP : LISTAS_PVE).map(listById);
      const pos = q.pool.map(x => ls.reduce((s, l) => s + puesto(l, x.key), 0));
      const ref = q.pool.map(x => rankIndex(x.key));
      const dpsCtx = q.pool.map(x => rolEn(x, c).dps > 0);
      const filas = [], vs = [v, null, null];
      for (let i = 0; i < q.n; i++) {
        if (!((q.F[i] & 1 || dpsCtx[q.A[i]]) && (q.F[i] & 2 || dpsCtx[q.B[i]]))) continue;
        vs[1] = q.pool[q.A[i]]; vs[2] = q.pool[q.B[i]];
        const e = enContexto(vs, c);
        if (!e) continue;
        const p = e.partes;
        filas.push([q.A[i], q.B[i], p.lider / PESO.lider, p.dps / PESO.dps, p.sinergia / PESO.sinergia, p.striker / PESO.striker,
                    pos[q.A[i]] + pos[q.B[i]], ref[q.A[i]] + ref[q.B[i]], vs.indexOf(e.lider), i]);
      }
      res.ctx[c] = filas;
    }
    out.focos[k] = res;
  }
  CONSULTA = null;
  // Nombres y roles de cada variante, para leer los casos.
  out.vars = Object.fromEntries(allVariants().map(x => [x.key, [fullLabel(x), x.cid, rolEn(x, 'pvp').dps, rolEn(x, 'pve').dps, rolEn(x, 'pvp').soporte, rolEn(x, 'pve').soporte]]));
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
        if PREVIO: print('previo:', pg.evaluate('(js) => window.__ev(js)', PREVIO), flush=True)
        import time
        R = {'focos': {}}
        for f in FOCOS:
            t0 = time.time()
            r = pg.evaluate('([js, f, c]) => window.__ev(js)([f, c])', [JS, [f], CTXS])
            R['focos'].update(r['focos']); R['peso'] = r['peso']; R['vars'] = r['vars']
            print(f, round(time.time() - t0, 1), 's', flush=True)
        b.close()
finally:
    srv.terminate(); srv.wait()
json.dump(R, open(SALIDA, 'w'))
for k, r in R['focos'].items():
    print(k, None if r is None else {c: len(f) for c, f in r['ctx'].items()})
