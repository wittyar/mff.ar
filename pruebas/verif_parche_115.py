"""La 1.0.14 publicada (el parche de la release de GitHub, con datos de formato 5) se actualiza a la
1.0.15 armada acá por el camino real. Los datos no cambian de formato.

Antes del parche: la 1.0.14 anda con sus datos, ofrece la versión nueva y no avisa nada de los
datos; le arma a Thor base su lista de PvP.
Después: la 1.0.15 arranca con app.js y styles.css nuevos y los mismos datos, sin bajarlos; a Thor
base el orden PvP le muestra el aviso de que no tiene función, y a Knull — Ancient History le arma la
lista con la nota de las reglas, que ya cuenta las defensas."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo
from playwright.sync_api import sync_playwright
RAIZ = RAIZ
S = PRUEBAS
ok = Chequeo()
base = f'{S}/release-v1.0.14/parche.zip'
v_nueva = json.load(open(f'{RAIZ}/version.json', encoding='utf-8'))
assert v_nueva['version'] == '1.0.15' and v_nueva['formato_datos'] == 5
parche = open(f'{RAIZ}/dist/mff-parche-1.0.15.zip', 'rb').read()
# latest.json como lo arma construir.py manifiesto (sin el instalador, que se arma en Windows).
latest_nuevo = {'version': v_nueva['version'], 'python': v_nueva['python'], 'notas': v_nueva['notas'],
                'formato_datos': v_nueva['formato_datos'], 'instalador': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1}}


def git_show(rev, ruta):
    return subprocess.run(['git', '-C', RAIZ, 'show', f'{rev}:{ruta}'], capture_output=True, check=True).stdout


# GitHub simulado: los datos (formato 5, los mismos) y la versión nueva con su parche.
PUB = tempfile.mkdtemp(prefix='mff-gh-')
m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
assert m['formato'] == 5
m['imagenes'] = [[r, u] for r, u in m['imagenes'] if os.path.exists(os.path.join(RAIZ, r))]
json.dump(m, open(os.path.join(PUB, 'datos.json'), 'w', encoding='utf-8'))
for rel in m['archivos']:
    os.makedirs(os.path.dirname(os.path.join(PUB, rel)) or PUB, exist_ok=True)
    shutil.copy(os.path.join(RAIZ, rel), os.path.join(PUB, rel))
open(os.path.join(PUB, 'parche.zip'), 'wb').write(parche)


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=PUB, **k)
    def log_message(self, *a): pass


srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_port}/'
latest = dict(latest_nuevo, parche={'url': BASE + 'parche.zip', 'bytes': len(parche), 'sha256': hashlib.sha256(parche).hexdigest()})
json.dump(latest, open(os.path.join(PUB, 'latest.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# La 1.0.14 instalada: su programa (el parche publicado) y sus datos de formato 5 (los de 00daad6, v1.0.14).
P = tempfile.mkdtemp(prefix='mff-prog-')
zipfile.ZipFile(base).extractall(P)
VIEJOS = {'data.js': git_show('00daad6', 'data.js'), 'datos.json': git_show('00daad6', 'datos.json'),
          'docs/AUDITORIA.md': git_show('00daad6', 'docs/AUDITORIA.md')}
assert json.loads(VIEJOS['datos.json'])['formato'] == 5
for rel, b in VIEJOS.items():
    os.makedirs(os.path.dirname(os.path.join(P, rel)) or P, exist_ok=True)
    open(os.path.join(P, rel), 'wb').write(b)
antes = time.time() - 5 * 3600
for r, _, fs in os.walk(P):
    for f in fs: os.utime(os.path.join(r, f), (antes, antes))
D = tempfile.mkdtemp(prefix='mff-dat-')
for rel, b in VIEJOS.items():
    os.makedirs(os.path.dirname(os.path.join(D, rel)) or D, exist_ok=True)
    open(os.path.join(D, rel), 'wb').write(b)
os.symlink(os.path.join(RAIZ, 'images'), os.path.join(D, 'images'))

p = subprocess.Popen([sys.executable, os.path.join(P, 'desktop', 'lanzador.py'), '--datos', D, '--sin-ventana',
                      '--origen-datos', BASE, '--origen-app', BASE + 'latest.json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
while True:
    l = p.stdout.readline()
    if not l: raise SystemExit('no arrancó')
    if 'abriendo' in l: url = l.split('abriendo')[1].strip(); break
SALIDA = []
# La salida del lanzador se sigue leyendo: si nadie la lee, el caño se llena y el proceso se traba.
threading.Thread(target=lambda: [SALIDA.append(x) for x in p.stdout], daemon=True).start()


def ficha(pg, cid, uid=''):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.evaluate("""([cid, uid]) => { const el = document.createElement('button'); el.dataset.a = 'open';
        el.dataset.cid = cid; el.dataset.uid = uid; document.body.appendChild(el); el.click(); el.remove(); }""", [cid, uid])
    pg.wait_for_selector('.fcab')


def estado(pg):
    return pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json())")


try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e))); pg.on('dialog', lambda d: d.accept())
        pg.goto(url); pg.wait_for_selector('.ccard')
        e0 = estado(pg)
        ok('1.0.14 instalada, con datos de formato 5', e0['version'] == '1.0.14' and pg.evaluate('window.MFF_VERSION.formato') == 5,
           (e0['version'], pg.evaluate('window.MFF_VERSION.formato')))
        pg.wait_for_selector('[data-a="actualizarApp"]', timeout=30000)
        ok('1.0.14: ofrece la 1.0.15 y no avisa nada de los datos', not any('versión más nueva' in a for a in pg.locator('.aviso-app').all_inner_texts()))
        ficha(pg, 'thor')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_selector('#combos .cxpts', timeout=60000)
        ok('1.0.14: Thor base tiene lista de PvP', pg.locator('#combos .combo').count() > 0)
        pg.select_option('select[data-a="eqOrden"]', 'foco'); pg.wait_for_timeout(300)
        datos_antes = os.stat(os.path.join(D, 'data.js')).st_mtime
        pg.evaluate("window.__marca = 'antes del parche'")
        pg.click('[data-a="actualizarApp"]')
        # El parche reinicia la app; la 1.0.15 ve datos del mismo formato y no baja nada.
        try:
            pg.wait_for_function("window.__marca === undefined && window.MFF_VERSION && document.querySelector('.ccard')", timeout=180000)
        except Exception:
            pg.screenshot(path=S + '/parche115_trabado.png')
            print('--- texto de la página:', pg.evaluate("document.body.innerText.slice(0, 600)"))
            print('--- lanzador:', ''.join(SALIDA)[-3000:])
            raise
        pg.wait_for_timeout(1500)
        e1 = estado(pg)
        rec = pg.evaluate("""() => ['app.js', 'styles.css'].map(n => { const e = performance.getEntriesByType('resource')
                               .find(x => new URL(x.name).pathname === '/' + n);
                               return e ? [new URL(e.name).pathname + new URL(e.name).search, e.transferSize] : [n, 'sin entrada']; })""")
        ok('parche aplicado: 1.0.15, con app.js y styles.css nuevos', e1['version'] == '1.0.15'
           and all(isinstance(t, int) and t > 0 and 'v=1.0.15' in n for n, t in rec), (e1['version'], rec))
        ok('1.0.15: los mismos datos, sin bajarlos', pg.evaluate('window.MFF_VERSION.formato') == 5
           and os.stat(os.path.join(D, 'data.js')).st_mtime == datos_antes)
        ok('1.0.15: sin avisos de datos', not any('versión más nueva' in a for a in pg.locator('.aviso-app').all_inner_texts()))
        ficha(pg, 'thor')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos select[data-a="eqOrden"]', timeout=60000)
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_selector('#combos .cxnota', timeout=60000)
        nota = pg.locator('#combos .cxnota').text_content()
        ok('1.0.15: Thor base, en PvP el aviso y ninguna combinación',
           'no tiene función en PvP' in nota and pg.locator('#combos .combo').count() == 0, nota)
        ficha(pg, 'knull', 'knull-10100241')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos select[data-a="eqOrden"]', timeout=60000)
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_selector('#combos .cxpts', timeout=60000)
        ok('1.0.15: Knull — Ancient History, lista de PvP con la nota que cuenta las defensas',
           'pts PvP' in pg.locator('#combos .combo').first.text_content() and 'todas las defensas' in pg.locator('#combos .cxnota').text_content())
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    try: os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError): pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
