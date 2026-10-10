"""¿Cuántas combinaciones de 3 muestra la pestaña Equipos y por qué? Corre la consulta de la app
(consultaCon / vistaConsulta) para una muestra, y para todos los personajes cuenta con cuántos
tiene vínculo y de qué tipo: solo efectos sin restricción (le llegan a cualquiera), alguno
restringido (por habilidad, tipo, bando, aliados o personaje) o un bono de equipo.

app.js corre dentro de una función: para leer sus variables se sirve con un gancho de eval
(solo en esta prueba; el archivo no se toca)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar
from playwright.sync_api import sync_playwright
MUESTRA = ['galactus', 'kingpin', 'cyclops', 'spider-man', 'captain-america', 'thor', 'man-thing', 'annihilus', 'black-widow', 'hulk']

JS = r"""(muestra) => {
  const porCid = {}; allVariants().forEach(x => (porCid[x.cid] = porCid[x.cid] || []).push(x));
  const nChars = CHARS.length;
  // Por qué se vinculan dos variantes, en un sentido: de le da algo a a.
  function razones (de, a, out) {
    const s = SOPORTES[de.p];
    if (s) for (const [k] of TIPOS_SOPORTE) if (s[k] && aplicaA(s[k], a) && leSirve(s[k], a)) out.add(s[k].r ? 'restringido' : 'cualquiera');
    const bonos = BONOS_DE[de.cid]; if (bonos && bonos.some(bb => bb.m.includes(a.cid))) out.add('bono');
  }
  // Para cada personaje (su variante base y sus uniformes, como la consulta): con cuántos otros
  // personajes tiene algún vínculo posible, y de qué tipo.
  const clase = {};
  const resumen = CHARS.map(ch => {
    const vs = porCid[ch.id]; const cuenta = { gen: 0, esp: 0, nadie: 0 };
    for (const o of CHARS) { if (o.id === ch.id) continue;
      const rz = new Set();
      for (const v of vs) for (const x of porCid[o.id]) { razones(x, v, rz); razones(v, x, rz); }
      const k = !rz.size ? 'nadie' : (rz.has('restringido') || rz.has('bono')) ? 'esp' : 'gen';
      cuenta[k]++; clase[ch.id + '>' + o.id] = k;
    }
    return { cid: ch.id, ...cuenta };
  });
  // Los que le dan algo sin restricción a casi todos: a cuántos personajes les llega y sirve.
  const dadores = CHARS.map(ch => {
    let n = 0;
    for (const o of CHARS) { if (o.id === ch.id) continue; const rz = new Set();
      for (const v of porCid[ch.id]) for (const x of porCid[o.id]) razones(v, x, rz);
      if (rz.has('cualquiera')) n++; }
    return [ch.id, n];
  }).sort((a, b) => b[1] - a[1]);
  const filas = [];
  for (const cid of muestra) {
    const v = variant(cid, null); if (!v) { filas.push({ cid, falta: true }); continue; }
    const t0 = performance.now(); CONSULTA = null;
    const q = consultaCon(v); const vista = vistaConsulta(q);
    const pts = vista.filas.map(i => q.P[i]).sort((a, b) => b - a);
    const socios = new Set(); let soloGen = 0, unGen = 0;
    for (const i of vista.filas) {
      const a = q.pool[q.A[i]].cid, b = q.pool[q.B[i]].cid; socios.add(a); socios.add(b);
      const ka = clase[cid + '>' + a], kb = clase[cid + '>' + b];
      if (ka === 'gen' && kb === 'gen') soloGen++; else if (ka === 'gen' || kb === 'gen') unGen++;
    }
    const hist = {}; pts.forEach(p => hist[p] = (hist[p] || 0) + 1);
    filas.push({ cid, n: vista.filas.length, ocultos: vista.ocultos, variantes_pares: q.n, socios: socios.size,
                 soloGen, unGen, max: pts[0], p50: pts[Math.floor(pts.length / 2)], p10: pts[Math.floor(pts.length * 0.1)],
                 hist, ms: Math.round(performance.now() - t0) });
  }
  return { nChars, nVariantes: allVariants().length, resumen, dadores: dadores.slice(0, 25), filas };
}"""

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
        r = pg.evaluate('([js, m]) => window.__ev(js)(m)', [JS, MUESTRA])
        b.close()
finally:
    srv.terminate(); srv.wait()

N = r['nChars']
print('personajes:', N, '| variantes:', r['nVariantes'], '| pares de personajes posibles por personaje:', (N - 1) * (N - 2) // 2)
for f in r['filas']:
    print({k: v for k, v in f.items() if k != 'hist'})
    print('   puntos→filas:', dict(sorted(((int(k), v) for k, v in f['hist'].items()), reverse=True)))
res = r['resumen']
for k in ('gen', 'esp', 'nadie'):
    xs = sorted(x[k] for x in res)
    print(k, 'mediana', statistics.median(xs), 'min', xs[0], 'max', xs[-1])
vinc = sorted(x['gen'] + x['esp'] for x in res)
print('vinculados (personajes): mediana', statistics.median(vinc), 'p10', vinc[len(vinc) // 10], 'p90', vinc[len(vinc) * 9 // 10])
print('dadores sin restricción (a cuántos personajes les llega y sirve):', r['dadores'])
json.dump(r, open(f'{SALIDA}/cuantos_equipos.json', 'w'))
for cid in MUESTRA:
    print(cid, next((x for x in res if x['cid'] == cid), None))
