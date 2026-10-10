"""La 1.0.8 publicada (parche de la release) se actualiza a la 1.0.9 armada acá por el camino
real, con los datos actuales. Después: la sinergia nueva (Abomination — Infected Bioweapon sin
Satana; Human Torch con Satana de líder y su daño de fuego)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo
from playwright.sync_api import sync_playwright
RAIZ = RAIZ
S = PRUEBAS
ok = Chequeo()
base = f'{S}/release-v1.0.8/mff-parche-1.0.8.zip'
latest_pub = json.load(open(f'{S}/armado/latest-1.0.9.json', encoding='utf-8'))
parche = open(f'{RAIZ}/dist/mff-parche-1.0.9.zip', 'rb').read()
PUB = tempfile.mkdtemp(prefix='mff-gh-')
m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
m['imagenes'] = [[r, u] for r, u in m['imagenes'] if os.path.exists(os.path.join(RAIZ, r))]
json.dump(m, open(os.path.join(PUB, 'datos.json'), 'w', encoding='utf-8'))
open(os.path.join(PUB, 'parche.zip'), 'wb').write(parche)
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=PUB, **k)
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_port}/'
latest = dict(latest_pub, parche={'url': BASE + 'parche.zip', 'bytes': len(parche), 'sha256': hashlib.sha256(parche).hexdigest()})
json.dump(latest, open(os.path.join(PUB, 'latest.json'), 'w', encoding='utf-8'), ensure_ascii=False)
P = tempfile.mkdtemp(prefix='mff-prog-')
zipfile.ZipFile(base).extractall(P)
for f in ('data.js', 'datos.json'): shutil.copy(os.path.join(RAIZ, f), os.path.join(P, f))
os.makedirs(os.path.join(P, 'docs')); shutil.copy(os.path.join(RAIZ, 'docs/AUDITORIA.md'), os.path.join(P, 'docs'))
antes = time.time() - 5 * 3600
for r, _, fs in os.walk(P):
    for f in fs: os.utime(os.path.join(r, f), (antes, antes))
D = tempfile.mkdtemp(prefix='mff-dat-')
for f in ('data.js', 'datos.json'): shutil.copy(os.path.join(RAIZ, f), D)
shutil.copytree(os.path.join(RAIZ, 'docs'), os.path.join(D, 'docs'))
os.symlink(os.path.join(RAIZ, 'images'), os.path.join(D, 'images'))
p = subprocess.Popen([sys.executable, os.path.join(P, 'desktop', 'lanzador.py'), '--datos', D, '--sin-ventana',
                      '--origen-datos', BASE, '--origen-app', BASE + 'latest.json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
while True:
    l = p.stdout.readline()
    if not l: raise SystemExit('no arrancó')
    if 'abriendo' in l: url = l.split('abriendo')[1].strip(); break
def abrir(pg, nombre, cid, uid=''):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(300); pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid: pg.select_option('select[data-a="uniformSel"]', uid)
    pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e))); pg.on('dialog', lambda d: d.accept())
        pg.goto(url); pg.wait_for_selector('.ccard')
        v0 = pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json()).then(e => e.version)")
        abrir(pg, 'Abomination', 'abomination', 'abomination-10100228')
        pg.select_option('select[data-a="eqCon"]', 'satana'); pg.wait_for_timeout(200)
        antes_satana = pg.locator('#combos .combo').count()
        ok('1.0.8 (antes del parche): con Abomination — Infected Bioweapon todavía hay combinaciones con Satana', v0 == '1.0.8' and antes_satana > 0, (v0, antes_satana))
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        pg.wait_for_selector('[data-a="actualizarApp"]', timeout=30000)
        pg.evaluate("window.__marca = 'antes del parche'")
        pg.click('[data-a="actualizarApp"]')
        pg.wait_for_function("window.__marca === undefined && document.querySelector('nav.topnav')", timeout=90000)
        pg.wait_for_timeout(1000)
        ver = pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json()).then(e => e.version)")
        rec = pg.evaluate("""() => ['app.js', 'styles.css'].map(n => { const e = performance.getEntriesByType('resource')
                               .find(x => new URL(x.name).pathname === '/' + n);
                               return e ? [new URL(e.name).pathname + new URL(e.name).search, e.transferSize] : [n, 'sin entrada']; })""")
        ok('parche aplicado: 1.0.9, con app.js y styles.css nuevos', ver == '1.0.9' and all(isinstance(t, int) and t > 0 and 'v=1.0.9' in n for n, t in rec), (ver, rec))
        abrir(pg, 'Abomination', 'abomination', 'abomination-10100228')
        pg.select_option('select[data-a="eqCon"]', 'satana'); pg.wait_for_timeout(200)
        ok('1.0.9: con Abomination — Infected Bioweapon, ninguna combinación con Satana', pg.locator('#combos .combo').count() == 0)
        abrir(pg, 'Human Torch', 'human-torch')
        pg.select_option('select[data-a="eqCon"]', 'satana'); pg.wait_for_timeout(200)
        c = pg.locator('#combos .combo').first
        c.locator('summary').first.click(); pg.wait_for_timeout(100)
        tx = c.inner_text()
        ok('1.0.9: Human Torch con Satana de líder y su daño de fuego', 'Líder: Satana' in tx and 'Daño de fuego +70%' in tx, tx[:200])
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    try: os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError): pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
