"""La 1.0.9 publicada (parche de la release) se actualiza a la 1.0.10 armada acá por el camino
real, con los datos nuevos (marcadores completados). Antes: la app vieja con los datos nuevos no
se rompe. Después: los marcadores con su valor, el índice y la cobertura."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo
from playwright.sync_api import sync_playwright
RAIZ = RAIZ
S = PRUEBAS
ok = Chequeo()
base = f'{S}/release-v1.0.9/mff-parche-1.0.9.zip'
latest_pub = json.load(open(f'{S}/armado/latest-1.0.10.json', encoding='utf-8'))
parche = open(f'{RAIZ}/dist/mff-parche-1.0.10.zip', 'rb').read()
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
def abrir(pg, nombre, cid, uid='', tab='skills'):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(300); pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid: pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(150)
    pg.click(f'[data-a="fichaTab"][data-v="{tab}"]'); pg.wait_for_timeout(200)
def pasiva_uniforme(pg):
    sk = pg.locator('.skill', has=pg.locator('.slotbadge', has_text='Pasiva de uniforme')).first
    return sk.locator('.tpl-ok').count(), sk.locator('.tpl').count(), sk.inner_text()
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e))); pg.on('dialog', lambda d: d.accept())
        pg.goto(url); pg.wait_for_selector('.ccard')
        v0 = pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json()).then(e => e.version)")
        abrir(pg, 'Ebony Maw', 'ebony-maw', 'ebony-maw-10200077')
        n_ok, n_pend, tx = pasiva_uniforme(pg)
        ok('1.0.9 (antes del parche) con los datos nuevos: la pasiva de uniforme de Ebony Maw sigue "sin especificar", sin romperse',
           v0 == '1.0.9' and n_ok == 0 and n_pend == 2, (v0, n_ok, n_pend, tx[:160]))
        abrir(pg, 'Ebony Maw', 'ebony-maw', 'ebony-maw-10200077', 'resumen')
        ok('1.0.9: todavía sin el índice', pg.locator('.lesirve').count() == 0 and pg.locator('.sopcats').count() == 0)
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
        ok('parche aplicado: 1.0.10, con app.js y styles.css nuevos', ver == '1.0.10' and all(isinstance(t, int) and t > 0 and 'v=1.0.10' in n for n, t in rec), (ver, rec))
        abrir(pg, 'Ebony Maw', 'ebony-maw', 'ebony-maw-10200077')
        n_ok, n_pend, tx = pasiva_uniforme(pg)
        ok('1.0.10: la pasiva de uniforme de Ebony Maw dice Universal, marcado de la wiki', n_ok == 2 and n_pend == 0 and 'Universal' in tx, (n_ok, n_pend, tx[:160]))
        abrir(pg, 'Ebony Maw', 'ebony-maw', 'ebony-maw-10200077', 'resumen')
        ok('1.0.10: Resumen con «Le sirve» y las categorías', pg.locator('.lesirve').count() == 1 and pg.locator('.sopcats').count() >= 1)
        pg.click('[data-a="paraVer"][data-tipo="lid"]'); pg.wait_for_timeout(300)
        ok('1.0.10: «Líderes que se lo dan» abre el roster filtrado', pg.locator('[data-a="paraQuitar"]').count() == 1 and int(pg.locator('.count b').inner_text()) > 0,
           pg.locator('.count b').inner_text())
        pg.click('[data-a="clearFilters"]'); pg.wait_for_timeout(100)
        abrir(pg, 'Abomination', 'abomination', '', 'equipos'); pg.wait_for_selector('#combos .combo', timeout=60000)
        ok('1.0.10: combinaciones con su cobertura', pg.locator('#combos .combo .cobertura').count() == pg.locator('#combos .combo').count() > 0)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    try: os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError): pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
