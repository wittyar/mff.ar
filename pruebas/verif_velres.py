"""1.0.14, regla de Ezequiel: todas las velocidades no le sirven a nadie y las resistencias solo a
quien pega según su resistencia (res del perfil), en ese elemento. Contra el modelo aparte
(auditoria_equipos.py): cada liderazgo o soporte con alguno de esos stats, contra cada variante. Y en
la sinergia: con Odin de líder (Remove All Debuffs + All Resistances), Thor recibe los dos efectos y
Abomination solo el primero. Desde la 1.0.18, synergy() devuelve las razones en piezas (razones) y
razonesTxt() arma las líneas de texto.
Formato 7 (segunda parte del carril de consistencia): las reglas están en el catálogo (MFF_CATALOGO.soporte) y el
modelo las lee de ahí; acá se comprueba además que el catálogo diga las reglas de Ezequiel (y All Debuffs Effect, a
todos: 4 de octubre de 2026)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
import auditoria_equipos as A
ok = Chequeo()
DECIDIDAS = {'All Speeds': 'nadie', 'All Resistances': 'resistencia:*', 'Fire Resist': 'resistencia:Fire',
             'Cold Resist': 'resistencia:Cold', 'Lightning Resist': 'resistencia:Lightning', 'Mind Resist': 'resistencia:Mind',
             'All Debuffs Effect': 'todos'}
ok('el catálogo dice las reglas de Ezequiel', {k: A.REGLA.get(k) for k in DECIDIDAS} == DECIDIDAS,
   {k: A.REGLA.get(k) for k in DECIDIDAS})
STATS = ['All Speeds', 'All Resistances', 'Fire Resist', 'Cold Resist', 'Lightning Resist', 'Mind Resist']
JS = r"""(stats) => {
  const vars = allVariants(), out = [];
  for (const [p, s] of Object.entries(SOPORTES)) for (const [k] of TIPOS_SOPORTE) {
    const x = s[k]; if (!x || !x.fx.some(f => stats.includes(f.s))) continue;
    out.push([p, k, x.fx.map(f => f.s), vars.filter(b => leSirve(x, b)).map(b => b.key)]);
  }
  const thor = variant('thor', null), odin = variant('odin', null), abo = variant('abomination', null);
  const sy = synergy([thor, odin, abo]);
  const sinPerfil = sirve({ s: 'All Resistances' }, { p: null });
  return { out, reasons: razonesTxt(sy.razones), lider: sy.lider && sy.lider.cid, sinPerfil,
           resThor: [...perfilDano(thor).res], resAbo: [...perfilDano(abo).res] };
}"""
srv, url = levantar(carpeta_datos(), origen_local())
errores = []
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        def gancho(route):
            r = route.fetch(); cuerpo = r.text()
            assert cuerpo.count('\narrancar();\n})();') == 1
            route.fulfill(response=r, body=cuerpo.replace('\narrancar();\n})();', '\nwindow.__ev = s => eval(s);\narrancar();\n})();'))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard')
        r = pg.evaluate('([js, s]) => window.__ev(js)(s)', [JS, STATS])
        b.close()
finally:
    srv.terminate(); srv.wait()

# Modelo aparte: un soporte le sirve a b si alguno de sus efectos le sirve (sirve_fx).
por_key = {v['key']: v for v in A.TODAS}
malos, n = [], 0
for p, k, fx, servidos in r['out']:
    esperado = sorted(v['key'] for v in A.TODAS if any(A.sirve_fx({'s': s}, A.PERFIL[v['p']]) for s in fx))
    n += 1
    if sorted(servidos) != esperado:
        malos.append((p, k, fx, len(servidos), len(esperado)))
ok('cada liderazgo o soporte con velocidades o resistencias le sirve a los mismos que en el modelo', n > 10 and not malos, (n, malos[:4]))
solo_vel = [(p, k) for p, k, fx, sv in r['out'] if set(fx) == {'All Speeds'}]
ok('un liderazgo o soporte de solo todas las velocidades no le sirve a nadie',
   all(not sv for p, k, fx, sv in r['out'] if set(fx) == {'All Speeds'}), solo_vel[:5])
ok('perfil: Thor pega según su resistencia al rayo; Abomination no', r['resThor'] == ['Lightning'] and r['resAbo'] == [], (r['resThor'], r['resAbo']))
ok('un personaje sin perfil (agregado a mano) no recibe resistencias', r['sinPerfil'] is False, r['sinPerfil'])
lineas = [x for x in r['reasons'] if x.startswith('Con Odin de líder →')]
thor = [x for x in lineas if 'Thor' in x.split('→')[1].split(':')[0]]
abo = [x for x in lineas if 'Abomination' in x.split('→')[1].split(':')[0]]
ok('sinergia: con Odin de líder, Thor recibe los dos efectos', r['lider'] == 'odin' and len(thor) == 1 and thor[0].count(' · ') == 1, (r['lider'], thor))
ok('sinergia: Abomination recibe solo el que le sirve', len(abo) == 1 and ' · ' not in abo[0].split(':', 1)[1], abo)
ok('sin errores de página', not errores, errores[:3])
ok.fin()
