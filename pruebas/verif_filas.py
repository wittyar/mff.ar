"""filasDe sin copiar la lista entera: mismo resultado que antes, más rápido.

1  equivalencia (node): la función vieja (assignOf(listId)[key] || []) y la nueva sobre las
   listas reales de data.js y una capa del usuario con filas propias, quitadas (REMOVED),
   entradas nuevas y listas propias; todas las listas y todas las claves (más una que no existe)
2  la app vieja (HEAD) y la nueva, lado a lado: orden del roster por puesto en la lista de
   referencia (tarjetas y tabla), orden del armador de equipos, quitar una entrada de una
   lista importada (desaparece, "Deshacer (1)", la tarjeta cambia su puesto); y los tiempos."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, shutil, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import origen_local, Chequeo
from playwright.sync_api import sync_playwright

S = PRUEBAS
NUEVO, VIEJO = RAIZ, f'{S}/wt-head'
ok = Chequeo()

# 1 --------------------------------------------------------------------------------------
js = r"""
const vm = require('vm'), fs = require('fs');
const c = { window: {} }; vm.createContext(c);
vm.runInContext(fs.readFileSync('%s/data.js', 'utf8'), c);
const ASSIGN_SEED = c.window.MFF_SEED_TIER_ASSIGNMENTS || {};
const REMOVED = null;
const listas = Object.keys(ASSIGN_SEED);
// capa del usuario: en cada lista importada, una entrada movida, una quitada y una nueva; y una lista propia
const U = { assign: {} };
listas.forEach((id, i) => { const ks = Object.keys(ASSIGN_SEED[id]);
  U.assign[id] = { [ks[0]]: ['A', 'B'], [ks[1]]: REMOVED, ['nuevo::' + i]: ['C'] }; });
U.assign['propia'] = { 'x::base': ['S'], 'y::base': REMOVED };
function assignOf (listId) {
  const out = Object.assign({}, ASSIGN_SEED[listId] || {});
  const mine = U.assign[listId] || {};
  for (const k in mine) { if (mine[k] === REMOVED) delete out[k]; else out[k] = mine[k]; }
  return out;
}
const viejo = (listId, key) => assignOf(listId)[key] || [];
function nuevo (listId, key) {
  const mia = (U.assign[listId] || {})[key];
  if (mia === REMOVED) return [];
  return mia || (ASSIGN_SEED[listId] || {})[key] || [];
}
let n = 0, dif = [];
listas.concat(['propia', 'no-existe']).forEach(id => {
  const claves = new Set(Object.keys(ASSIGN_SEED[id] || {}).concat(Object.keys(U.assign[id] || {}), ['no::existe']));
  claves.forEach(k => { n++; if (JSON.stringify(viejo(id, k)) !== JSON.stringify(nuevo(id, k))) dif.push([id, k]); });
});
process.stdout.write(JSON.stringify({ listas: listas.length, n, dif: dif.slice(0, 5), ndif: dif.length }));
""" % NUEVO
r = json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)
ok('equivalencia: vieja y nueva dan lo mismo en todas las listas y claves', r['ndif'] == 0 and r['n'] > 1000,
   f"{r['listas']} listas importadas, {r['n']} consultas, {r['ndif']} diferencias {r['dif']}")

# 2 --------------------------------------------------------------------------------------
def recorrer(raiz):
    harness.RAIZ = raiz
    d = tempfile.mkdtemp(prefix='mffdatos-')
    for f in ('data.js', 'datos.json'): shutil.copy(os.path.join(NUEVO, f), d)
    shutil.copytree(os.path.join(NUEVO, 'docs'), os.path.join(d, 'docs')); os.symlink(os.path.join(NUEVO, 'images'), os.path.join(d, 'images'))
    srv, url = harness.levantar(d, origen_local())
    obs, tiempos = {}, {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
            pg.on('pageerror', lambda e: errores.append(str(e))); pg.on('dialog', lambda x: x.accept())
            pg.goto(url); pg.wait_for_selector('.ccard')
            claves = lambda sel: pg.evaluate(f"[...document.querySelectorAll('{sel}')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base'))")
            t0 = time.time(); pg.select_option('select[data-a="sort"]', 'rank'); pg.wait_for_timeout(50); tiempos['ordenar por puesto'] = time.time() - t0
            obs['roster por puesto'] = claves('.ccard')
            pg.click('[data-a="view"][data-v="table"]'); pg.wait_for_timeout(200)
            obs['tabla por puesto'] = pg.evaluate("[...document.querySelectorAll('table.dt tbody tr')].map(x => x.innerText.split('\\n')[0])")
            pg.click('[data-a="view"][data-v="grid"]'); pg.wait_for_timeout(200)
            pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(200)
            t0 = time.time(); pg.click('[data-a="teamOpen"]'); pg.wait_for_selector('[data-a="teamToggle"]'); tiempos['abrir el armador'] = time.time() - t0
            obs['armador'] = pg.evaluate("[...document.querySelectorAll('[data-a=\"teamToggle\"]')].map(x => x.dataset.key)")
            t0 = time.time(); pg.fill('[data-a="teamSearch"]', 'man'); pg.wait_for_timeout(50); tiempos['buscar en el armador'] = time.time() - t0
            obs['armador "man"'] = pg.evaluate("[...document.querySelectorAll('[data-a=\"teamToggle\"]')].map(x => x.dataset.key)")
            # quitar una entrada de la lista importada de referencia
            pg.click('[data-a="goTier"]'); pg.wait_for_selector('.tlchip')
            x = pg.locator('.tlchip:has([data-a="unassign"])').first
            key, fila = x.get_attribute('data-key'), x.get_attribute('data-from')
            antes = pg.locator(f'.tlchip[data-key="{key}"]').count()
            x.locator('[data-a="unassign"]').click(); pg.wait_for_timeout(300)
            obs['quitada'] = (key, fila, antes, pg.locator(f'.tlchip[data-key="{key}"][data-from="{fila}"]').count(),
                              pg.locator('[data-a="resetList"]').inner_text().strip())
            cid, uid = key.split('::')
            nombre = pg.evaluate(f"(MFF_SEED_CHARACTERS.find(c => c.id === {json.dumps(cid)}) || {{}}).name")
            pg.click('[data-a="back"]') if pg.locator('[data-a="back"]').count() else None
            pg.evaluate("document.querySelector('nav.topnav button, nav.topnav a').click()")
            pg.wait_for_selector('#q'); pg.fill('#q', nombre); pg.wait_for_timeout(300)
            obs['tarjeta después de quitarla'] = pg.locator(f'.ccard[data-cid="{cid}"]').first.inner_text()
            obs['errores'] = errores
            b.close()
    finally:
        srv.terminate(); srv.wait()
    return obs, tiempos

vie, tv = recorrer(VIEJO)
nue, tn = recorrer(NUEVO)
for k in vie:
    if k == 'errores': continue
    ok(f'mismo resultado que la app vieja: {k}', vie[k] == nue[k] and vie[k],
       (str(nue[k])[:140] + ('…' if len(str(nue[k])) > 140 else '')))
q = nue['quitada']
ok('quitar una entrada importada: desaparece de esa fila y queda "Deshacer (1)"', q[3] == 0 and '(1)' in q[4], q)
ok('sin errores de página', not vie['errores'] and not nue['errores'], (vie['errores'][:2], nue['errores'][:2]))
for k in tv: print(f'   {k}: {tv[k] * 1000:.0f} ms antes -> {tn[k] * 1000:.0f} ms ahora')
ok.fin()
