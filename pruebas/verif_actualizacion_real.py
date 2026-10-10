"""El camino real de la 1.0.0 instalada a la 1.0.1: programa armado con el parche publicado
de la 1.0.0 (el de GitHub) y los datos de d25bb2a; el "GitHub" falso publica lo que va a
haber después del push (datos.json y data.js nuevos) y la release 1.0.1 (el parche que
arma construir.py). La app baja los datos sola, se actualiza con el parche, se relanza, y
después "→ Aliados de magia" abre la lista."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, io, json, os, shutil, signal, subprocess, sys, tempfile, threading, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo
from playwright.sync_api import sync_playwright

RAIZ = RAIZ
S = PRUEBAS
ok = Chequeo()

# "GitHub": datos de main tras el push + release 1.0.1
PUB = tempfile.mkdtemp(prefix='mff-gh-')
m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
m['imagenes'] = [[r, u] for r, u in m['imagenes'] if os.path.exists(os.path.join(RAIZ, r))]
json.dump(m, open(os.path.join(PUB, 'datos.json'), 'w', encoding='utf-8'))
shutil.copy(os.path.join(RAIZ, 'data.js'), PUB)
os.makedirs(os.path.join(PUB, 'docs')); shutil.copy(os.path.join(RAIZ, 'docs', 'AUDITORIA.md'), os.path.join(PUB, 'docs'))
parche = open(os.path.join(RAIZ, 'dist', 'mff-parche-1.0.1.zip'), 'rb').read()
open(os.path.join(PUB, 'mff-parche-1.0.1.zip'), 'wb').write(parche)
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=PUB, **k)
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_port}/'
v = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))
json.dump({'version': v['version'], 'notas': v['notas'], 'python': v['python'], 'formato_datos': v['formato_datos'],
           'parche': {'url': BASE + 'mff-parche-1.0.1.zip', 'bytes': len(parche), 'sha256': hashlib.sha256(parche).hexdigest()},
           'instalador': {'url': BASE + 'x.exe', 'bytes': 1, 'sha256': '0' * 64}},
          open(os.path.join(PUB, 'latest.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# programa 1.0.0 como lo instaló el exe: el parche publicado + los datos iniciales de d25bb2a
P = tempfile.mkdtemp(prefix='mff-prog100-')
zipfile.ZipFile(os.path.join(S, 'release-v1.0.0', 'mff-parche-1.0.0.zip')).extractall(P)
for f in ('data.js', 'datos.json', 'docs/AUDITORIA.md'):
    os.makedirs(os.path.dirname(os.path.join(P, f)) or P, exist_ok=True)
    open(os.path.join(P, f), 'wb').write(subprocess.run(['git', 'show', f'd25bb2a:{f}'], cwd=RAIZ, capture_output=True, check=True).stdout)
ok('programa armado es la 1.0.0', json.load(open(os.path.join(P, 'version.json'), encoding='utf-8'))['version'] == '1.0.0')
D = tempfile.mkdtemp(prefix='mff-dat-')
os.symlink(os.path.join(RAIZ, 'images'), os.path.join(D, 'images'))

p = subprocess.Popen([sys.executable, os.path.join(P, 'desktop', 'lanzador.py'), '--datos', D, '--sin-ventana',
                      '--origen-datos', BASE, '--origen-app', BASE + 'latest.json'],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
while True:
    l = p.stdout.readline()
    if not l: raise SystemExit('no arrancó')
    if 'abriendo' in l: url = l.split('abriendo')[1].strip(); break

def avisos(pg): return pg.evaluate("(document.querySelector('#avisos') || {}).innerText || ''")
def esperar(pg, texto, n=120):
    for _ in range(n):
        if texto.lower() in avisos(pg).lower(): return True
        pg.wait_for_timeout(150)
    return False

try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e))); pg.on('dialog', lambda d: d.accept())
        pg.goto(url); pg.wait_for_selector('.ccard')
        ok('1.0.0: avisa la versión 1.0.1', esperar(pg, 'Versión 1.0.1 disponible'), avisos(pg)[:160].replace('\n', ' | '))
        ok('1.0.0: baja los datos nuevos solos', esperar(pg, 'datos') and json.load(open(os.path.join(D, 'datos.json'), encoding='utf-8'))['archivos']
           == m['archivos'], avisos(pg)[:160].replace('\n', ' | '))
        pg.click('[data-a="actualizarApp"]')
        for _ in range(120):
            est = pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json()).then(e => e.version).catch(() => null)")
            if est == '1.0.1': break
            pg.wait_for_timeout(300)
        pg.wait_for_selector('.ccard', timeout=30000); pg.wait_for_timeout(1500)
        ok('parche aplicado: la app corre la 1.0.1', est == '1.0.1'
           and json.load(open(os.path.join(P, 'version.json'), encoding='utf-8'))['version'] == '1.0.1', est)
        ok('respaldo del programa anterior', os.path.exists(os.path.join(D, 'programa-anterior', 'app.js')))
        pg.reload(); pg.wait_for_selector('.ccard')
        pg.fill('#q', 'Wong'); pg.wait_for_timeout(300)
        pg.locator('.ccard').first.click(); pg.wait_for_selector('.statgrid')
        wong2 = pg.locator('[data-a="uniform"]', has_text="Doctor Strange 2").first
        wong2.click()
        bt = pg.locator('button.tag.objetivo[data-a="verAliados"]', has_text='magia').first
        ok('1.0.1 + datos nuevos: "→ Aliados de magia" es un botón', bt.count() == 1)
        bt.click()
        cab = pg.locator('.modal.ancho .altitulo + div').inner_text() if pg.locator('.modal.ancho').count() else ''
        ok('abre la lista con 19 personajes', '19 personajes' in cab, cab)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    try:
        os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError):
        pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
