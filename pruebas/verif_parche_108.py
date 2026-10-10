"""La 1.0.7 publicada (su parche de la release, con los archivos fechados horas atrás) se
actualiza a la 1.0.8 con el parche armado acá, por el camino real: aviso, botón, reinicio en
la misma ventana. Dos casos de datos:
  nuevos: los de este build (con la guía y las opciones). Antes del parche, la 1.0.7 tiene que
          andar con ellos (es lo que va a pasar cuando se publiquen los datos del lunes).
  viejos: los de la 1.0.7 (d2dd98a). La 1.0.8 tiene que decir que faltan, sin romperse.
Uso: verif_parche_108.py nuevos|viejos"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo
from playwright.sync_api import sync_playwright

RAIZ = RAIZ
S = PRUEBAS
caso = sys.argv[1]
ok = Chequeo()
base = f'{S}/release-v1.0.7/mff-parche-1.0.7.zip'
latest_pub = json.load(open(f'{S}/armado/latest-1.0.8.json', encoding='utf-8'))
parche = open(f'{RAIZ}/dist/mff-parche-1.0.8.zip', 'rb').read()

# los datos del caso
DAT = tempfile.mkdtemp(prefix='mff-src-')
if caso == 'nuevos':
    for f in ('data.js', 'datos.json'): shutil.copy(os.path.join(RAIZ, f), DAT)
else:
    for f in ('data.js', 'datos.json'):
        open(os.path.join(DAT, f), 'wb').write(subprocess.run(['git', 'show', f'd2dd98a:{f}'], cwd=RAIZ, capture_output=True, check=True).stdout)

PUB = tempfile.mkdtemp(prefix='mff-gh-')
m = json.load(open(os.path.join(DAT, 'datos.json'), encoding='utf-8'))
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
for f in ('data.js', 'datos.json'): shutil.copy(os.path.join(DAT, f), os.path.join(P, f))
os.makedirs(os.path.join(P, 'docs')); shutil.copy(os.path.join(RAIZ, 'docs/AUDITORIA.md'), os.path.join(P, 'docs'))
antes = time.time() - 5 * 3600
for r, _, fs in os.walk(P):
    for f in fs: os.utime(os.path.join(r, f), (antes, antes))
D = tempfile.mkdtemp(prefix='mff-dat-')
for f in ('data.js', 'datos.json'): shutil.copy(os.path.join(DAT, f), D)
shutil.copytree(os.path.join(RAIZ, 'docs'), os.path.join(D, 'docs'))
os.symlink(os.path.join(RAIZ, 'images'), os.path.join(D, 'images'))

p = subprocess.Popen([sys.executable, os.path.join(P, 'desktop', 'lanzador.py'), '--datos', D, '--sin-ventana',
                      '--origen-datos', BASE, '--origen-app', BASE + 'latest.json'],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
while True:
    l = p.stdout.readline()
    if not l: raise SystemExit('no arrancó')
    if 'abriendo' in l: url = l.split('abriendo')[1].strip(); break

def texto(loc): return loc.evaluate('e => e.textContent.replace(/\\s+/g, " ").trim()')
def abrir(pg, nombre):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(300); pg.locator('.ccard').first.click(); pg.wait_for_selector('.fcab')
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e))); pg.on('dialog', lambda d: d.accept())
        pg.goto(url); pg.wait_for_selector('.ccard')
        v0 = pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json()).then(e => e.version)")
        # la 1.0.7 con estos datos
        abrir(pg, 'Abomination')
        for tab in ('resumen', 'skills', 'armado'):
            pg.click(f'[data-a="fichaTab"][data-v="{tab}"]'); pg.wait_for_timeout(150)
        pg.click('[data-a="goSettings"]'); pg.wait_for_timeout(200)
        ok(f'1.0.7 con los datos {caso}: anda sin errores', v0 == '1.0.7' and not errores, (v0, errores[:2]))
        pg.wait_for_selector('[data-a="actualizarApp"]', timeout=30000)
        pg.evaluate("window.__marca = 'antes del parche'")
        pg.click('[data-a="actualizarApp"]')
        try:
            pg.wait_for_function("window.__marca === undefined && document.querySelector('nav.topnav')", timeout=90000)
        except Exception:
            print('DEPURACIÓN', pg.evaluate("[String(window.__marca), location.href, document.body.innerText.slice(0, 600)]"), errores[:3])
            raise
        pg.wait_for_timeout(1000)
        ver = pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json()).then(e => e.version)")
        rec = pg.evaluate("""() => ['app.js', 'styles.css'].map(n => { const e = performance.getEntriesByType('resource')
                               .find(x => new URL(x.name).pathname === '/' + n);
                               return e ? [new URL(e.name).pathname + new URL(e.name).search, e.transferSize] : [n, 'sin entrada']; })""")
        ok('parche aplicado: 1.0.8, con app.js y styles.css nuevos (no de la caché)', ver == '1.0.8'
           and all(isinstance(t, int) and t > 0 and 'v=1.0.8' in n for n, t in rec), (ver, rec))
        abrir(pg, 'Abomination')
        ok('1.0.8: flechas en la ficha', pg.locator('.fnav [data-a="fichaVecina"]').count() >= 1)
        bl = pg.locator('.usogrid .bloque', has=pg.locator('h4', has_text='Cynicalex'))
        tb = texto(bl)
        pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(200)
        ta = texto(pg.locator('#fcuerpo'))
        pg.select_option('select[data-a="uniformSel"]', index=1); pg.wait_for_timeout(200)
        to = texto(pg.locator('.bloque', has=pg.locator('h4', has_text='Opciones de uniforme')))
        pg.click('[data-a="goSettings"]'); pg.wait_for_timeout(200)
        ts = texto(pg.locator('.section', has=pg.locator('h3', has_text='Cynicalex')))
        if caso == 'nuevos':
            ok('1.0.8 con datos nuevos: la guía en la ficha', 'Lead/Support Gods' in tb and 'V12.2.0' in tb, tb[:150])
            ok('1.0.8 con datos nuevos: ISO-8 y obelisco y opciones de uniforme', 'No gastes oro en su ISO-8' in ta and 'Mystique' in to and 'Advanced' in to, to[:120])
            ok('1.0.8 con datos nuevos: Ajustes con el estado de la guía', 'V12.2.0' in ts and 'compatible' in ts, ts[:150])
        else:
            aviso = 'Los datos cargados no traen la guía de armado'
            ok('1.0.8 con datos viejos: la ficha dice que faltan la guía y las opciones', aviso in tb and aviso in ta
               and 'Los datos cargados no traen las opciones de uniforme' in to, (tb[:80], to[:80]))
            ok('1.0.8 con datos viejos: Ajustes lo dice', aviso in ts, ts[:150])
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    reg = os.path.join(D, 'registro.txt')
    if os.path.exists(reg) and os.environ.get('VER_REGISTRO'): print('--- registro.txt\n' + open(reg, encoding='utf-8').read()[-3000:])
    try: os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError): pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
