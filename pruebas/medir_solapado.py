"""Cuánto cambian las listas y los puntajes con la regla de los efectos iguales (carril filtro2, 5 de octubre de 2026: en la
primera parte, los efectos sin valor que no se suman; en la segunda, lo que no se acumula según el catálogo, la de mayor
valor). Dos navegadores con los mismos datos (MFF_DATOS): el app.js de antes (VIEJO, un commit: 29decf6 es el filtro del
último uniforme sobre la 1.0.20, con la sinergia de la 1.0.20; 3404ebf, la primera parte) y el del programa (RAIZ, el de
ahora). Por cada lista se compara fila por fila (la pareja de compañeros por sus claves, el puntaje y el líder):
- PvP y PvE: la lista de cada variante con función en el contexto (consultaCon + vistaConsulta, orden PvP o PvE).
- Sinergia: la lista «Puntos para él» de las 888 variantes.
- Tríos al azar (20.000 uniformes y 20.000 con dos o tres que traen algo que no se acumula, en la app de ahora): la sinergia
  del equipo y su líder sin contexto, y el puntaje y el líder de PvP y PvE.
  MFF_DATOS=CARPETA python3 medir_solapado.py SALIDA.json [VIEJO]"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import base64, json, os, random, struct, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar
from playwright.sync_api import sync_playwright

SALIDA = sys.argv[1]
VIEJO = sys.argv[2] if len(sys.argv) > 2 else '29decf6'
APP_VIEJO = subprocess.run(['git', '-C', RAIZ, 'show', VIEJO + ':app.js'], capture_output=True, text=True, check=True).stdout
FIN = '\narrancar();\n})();'
def gancho(cuerpo=None):
    def f(route):
        r = route.fetch(); src = cuerpo if cuerpo is not None else r.text()
        assert src.count(FIN) == 1
        route.fulfill(response=r, body=src.replace(FIN, '\nwindow.__ev = s => eval(s);' + FIN))
    return f

# Una lista entera: por fila, la pareja (índices en allVariants), el puntaje (×100) y el líder (índice en allVariants, -1 sin).
LISTA = r"""([k, o, ultimo]) => {
  const todas = allVariants(), idx = new Map(todas.map((x, i) => [x.key, i])), v = todas.find(x => x.key === k);
  const t0 = performance.now(), nueva = !CONSULTA || CONSULTA.clave !== k;
  const q = consultaCon(v), ctx = o === 'pvp' || o === 'pve' ? o : null, t1 = performance.now();
  Object.assign(ui, { eqOrden: o, eqExcluir: [], eqCon: '', eqCobertura: [], eqVerDescartados: false, eqPagina: 0 });
  if ('eqUltimo' in ui) ui.eqUltimo = false;
  q.vista = null;
  const filas = vistaConsulta(q).filas, out = new Int32Array(filas.length * 4), t2 = performance.now();
  filas.forEach((i, n) => {
    const a = q.pool[q.A[i]], b = q.pool[q.B[i]], vs = [v, a, b];
    let pts, lider;
    if (ctx) { const e = enContexto(vs, ctx); pts = Math.round(e.score * 100); lider = e.lider; }
    else { pts = q.P[i] * 100; lider = q.L[i] < 3 ? vs[q.L[i]] : null; }
    out[n * 4] = idx.get(a.key); out[n * 4 + 1] = idx.get(b.key); out[n * 4 + 2] = pts; out[n * 4 + 3] = lider ? idx.get(lider.key) : -1;
  });
  let s = ''; const u8 = new Uint8Array(out.buffer);
  for (let i = 0; i < u8.length; i += 32768) s += String.fromCharCode.apply(null, u8.subarray(i, i + 32768));
  // con «Solo el último uniforme» (la app nueva): cuántas quedan
  let conUltimo = null;
  if (ultimo) { ui.eqUltimo = true; q.vista = null; conUltimo = vistaConsulta(q).filas.length; ui.eqUltimo = false; q.vista = null; }
  return { b64: btoa(s), consulta: nueva ? Math.round(t1 - t0) : null, vista: Math.round(t2 - t1), ultimo: conUltimo };
}"""
FUNCION = r"""() => { const vs = allVariants(); return { todas: vs.map(v => v.key),
  pvp: vs.filter(v => tieneFuncion(v, 'pvp')).map(v => v.key), pve: vs.filter(v => tieneFuncion(v, 'pve')).map(v => v.key) }; }"""
CANDIDATAS = r"""() => allVariants().filter(v => SOPORTES[v.p] && Object.values(SOPORTES[v.p]).some(x => x && x.fx && x.fx.some(f => !seAcumula(f)))
  || antiPropio(v).cuenta.length).map(v => v.key)"""
# Lo que no se suma en unos tríos (la app nueva): por stat, cuántas veces (integrante, efecto) no se le suma en la sinergia
# del equipo (sin contexto), y en cuántos tríos hay alguno.
REPETIDOS = r"""(trios) => { const por = new Map(allVariants().map(x => [x.key, x])), out = { stats: {}, trios: 0 };
  for (const ks of trios) { const vs = ks.map(k => por.get(k)); let hay = false;
    for (const r of synergy(vs).razones) for (const [, fs] of r.no || []) for (const [f] of fs) { out.stats[f.s] = (out.stats[f.s] || 0) + 1; hay = true; }
    // y lo propio que se repite (no está en las razones: va en lo que recibe cada uno)
    for (const m of vs) for (const r of recibe(m, m, false)) for (const f of r.fx) if (!seAcumula(f) && !esLaFuente(fuenteQueSeAplica(m, f.s, vs, liderDe(vs, null)), r.de, r.k, r.x)) { out.stats[f.s + ' (propio)'] = (out.stats[f.s + ' (propio)'] || 0) + 1; hay = true; }
    if (hay) out.trios++; }
  return out; }"""
TRIOS = r"""(trios) => { const por = new Map(allVariants().map(x => [x.key, x]));
  return trios.map(ks => { const vs = ks.map(k => por.get(k)), sc = synergy(vs), l = liderDe(vs, null);
    const c = (x) => { const e = enContexto(vs, x); return e ? [Math.round(e.score * 100), e.lider.key] : null; };
    return [sc.score, l ? l.key : null, c('pvp'), c('pve')]; }); }"""

def filas(b64):
    raw = base64.b64decode(b64)
    n = len(raw) // 16
    xs = struct.unpack(f'<{n * 4}i', raw)
    return [(xs[i * 4], xs[i * 4 + 1], xs[i * 4 + 2], xs[i * 4 + 3]) for i in range(n)]

def comparar(viejo, nuevo, todas):
    """De dos listas: cuántas filas, las parejas (por personaje) que entran y salen, las que cambian de uniforme, de puntaje o de
    líder, y si el orden de las que siguen cambia."""
    clave = lambda f: tuple(sorted((f[0], f[1])))
    pj = lambda f: tuple(sorted((todas[f[0]].split('::')[0], todas[f[1]].split('::')[0])))
    V, N = {pj(f): f for f in viejo}, {pj(f): f for f in nuevo}
    comunes = [p for p in V if p in N]
    otra_fila = [p for p in comunes if clave(V[p]) != clave(N[p])]
    misma = [p for p in comunes if clave(V[p]) == clave(N[p])]
    puntaje = [p for p in misma if V[p][2] != N[p][2]]
    lider = [p for p in misma if V[p][3] != N[p][3]]
    orden_v = [p for p in (pj(f) for f in viejo) if p in N]
    orden_n = [p for p in (pj(f) for f in nuevo) if p in V]
    return dict(antes=len(viejo), ahora=len(nuevo), salen=[p for p in V if p not in N], entran=[p for p in N if p not in V],
                otra_fila=otra_fila, puntaje=puntaje, lider=lider, orden=orden_v != orden_n,
                ej_puntaje=[(p, V[p][2] / 100, N[p][2] / 100) for p in puntaje[:3]],
                igual=[tuple(f) for f in viejo] == [tuple(f) for f in nuevo])

t0 = time.time()
srv, url = levantar(carpeta_datos(), origen_local())
res = {'viejo': VIEJO, 'pvp': {}, 'pve': {}, 'foco': {}, 'trios': {}}
try:
    with sync_playwright() as p:
        pgs, errores = {}, []
        for nombre, cuerpo in (('viejo', APP_VIEJO), ('nuevo', None)):
            b = p.chromium.launch(); pg = b.new_page()
            pg.on('pageerror', lambda e, n=nombre: errores.append(f'{n}: {e}'))
            pg.route(lambda u: '/app.js' in u, gancho(cuerpo))
            pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)
            pgs[nombre] = pg
        F = pgs['nuevo'].evaluate('(js) => window.__ev(js)()', FUNCION)
        assert F == pgs['viejo'].evaluate('(js) => window.__ev(js)()', FUNCION), 'las dos apps no tienen las mismas variantes o funciones'
        todas = F['todas']
        # PvP y PvE, y la de puntos para él de las mismas variantes de paso (la consulta ya está calculada)
        hechas = 0
        for k in todas:
            for o in ['foco'] + [c for c in ('pvp', 'pve') if k in F[c]]:
                R = {n: pg.evaluate('([js, a]) => window.__ev(js)(a)', [LISTA, [k, o, n == 'nuevo']]) for n, pg in pgs.items()}
                res[o][k] = comparar(filas(R['viejo']['b64']), filas(R['nuevo']['b64']), todas)
                res[o][k]['ms'] = {n: [R[n]['consulta'], R[n]['vista']] for n in R}
                res[o][k]['ultimo'] = R['nuevo']['ultimo']
            hechas += 1
            if hechas % 50 == 0: print(f'{hechas}/{len(todas)} variantes, {time.time() - t0:.0f} s', flush=True)
        # tríos al azar
        r = random.Random(3)
        cand = pgs['nuevo'].evaluate('(js) => window.__ev(js)()', CANDIDATAS)
        for nombre, base in (('uniformes', todas), ('con_habilidad', cand)):
            trios = []
            while len(trios) < 20000:
                ks = [r.choice(base), r.choice(base), r.choice(base if nombre == 'con_habilidad' and len(trios) % 2 else todas)]
                if len({k.split('::')[0] for k in ks}) == 3: trios.append(ks)
            R = {n: pg.evaluate('([js, a]) => window.__ev(js)(a)', [TRIOS, trios]) for n, pg in pgs.items()}
            rep_ = pgs['nuevo'].evaluate('([js, a]) => window.__ev(js)(a)', [REPETIDOS, trios])
            dif = lambda i: [t for t, x, y in zip(trios, R['viejo'], R['nuevo']) if x[i] != y[i]]
            res['trios'][nombre] = dict(n=len(trios), candidatas=len(cand), sinergia=len(dif(0)), lider=len(dif(1)),
                                        pvp=len(dif(2)), pve=len(dif(3)),
                                        en_pvp=sum(1 for x in R['nuevo'] if x[2]), en_pve=sum(1 for x in R['nuevo'] if x[3]),
                                        repetidos=rep_, ej=[(t, x, y) for t, x, y in zip(trios, R['viejo'], R['nuevo']) if x != y][:4])
        res['errores'] = errores
finally:
    srv.terminate(); srv.wait()
res['segundos'] = round(time.time() - t0)
json.dump(res, open(SALIDA, 'w'), ensure_ascii=False, indent=0)

for o in ('pvp', 'pve', 'foco'):
    ls = res[o]
    cambian = {k: x for k, x in ls.items() if not x['igual']}
    print(f"{o}: {len(ls)} listas, cambian {len(cambian)}; combinaciones {sum(x['antes'] for x in ls.values())} → {sum(x['ahora'] for x in ls.values())}; "
          f"salen {sum(len(x['salen']) for x in ls.values())}, entran {sum(len(x['entran']) for x in ls.values())}, otra fila {sum(len(x['otra_fila']) for x in ls.values())}, "
          f"otro puntaje {sum(len(x['puntaje']) for x in ls.values())}, otro líder {sum(len(x['lider']) for x in ls.values())}; con otro orden {sum(1 for x in ls.values() if x['orden'])}")
    for k, x in sorted(cambian.items(), key=lambda kv: kv[1]['ahora'] - kv[1]['antes'])[:5]:
        print(f"   {k}: {x['antes']} → {x['ahora']}; salen {len(x['salen'])}, entran {len(x['entran'])}, otro puntaje {len(x['puntaje'])} {x['ej_puntaje'][:1]}")
for n, x in res['trios'].items(): print('tríos', n, {k: v for k, v in x.items() if k != 'ej'})
for o in ('foco', 'pvp', 'pve'):
    ls = res[o]
    print(f"último uniforme {o}: {sum(x['ahora'] for x in ls.values())} → {sum(x['ultimo'] for x in ls.values())} combinaciones; "
          f"listas que quedan vacías {sum(1 for x in ls.values() if x['ahora'] and not x['ultimo'])}")
for o in ('foco', 'pvp', 'pve'):
    ms = {n: [x['ms'][n] for x in res[o].values()] for n in ('viejo', 'nuevo')}
    tot = {n: (sum(c or 0 for c, _ in xs), sum(v for _, v in xs), max((c or 0) + v for c, v in xs)) for n, xs in ms.items()}
    print(f'tiempo {o} (consulta, vista, la más lenta) en ms:', tot)
print('errores', res['errores'], res['segundos'], 's')
