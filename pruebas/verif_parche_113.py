"""La 1.0.12 publicada (el parche de la release de GitHub, con sus datos de formato 3) se actualiza
a la 1.0.13 armada acá por el camino real, con datos publicados de formato 4.

Antes del parche: la 1.0.12 sigue andando con sus datos, avisa que los datos nuevos son para una
versión más nueva y no los baja; no tiene la solapa Glosario.
Después: la 1.0.13 arranca, ve que sus datos locales son de otro formato, baja los nuevos sola y
recarga; la solapa Glosario anda con los datos bajados."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo
from playwright.sync_api import sync_playwright
RAIZ = RAIZ
S = PRUEBAS
ok = Chequeo()
base = f'{S}/release-v1.0.12/parche.zip'
v_nueva = json.load(open(f'{RAIZ}/version.json', encoding='utf-8'))
assert v_nueva['version'] == '1.0.13' and v_nueva['formato_datos'] == 4
parche = open(f'{RAIZ}/dist/mff-parche-1.0.13.zip', 'rb').read()
# latest.json como lo arma construir.py manifiesto (sin el instalador, que se arma en Windows).
latest_nuevo = {'version': v_nueva['version'], 'python': v_nueva['python'], 'notas': v_nueva['notas'],
                'formato_datos': v_nueva['formato_datos'], 'instalador': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1}}


def git_show(rev, ruta):
    return subprocess.run(['git', '-C', RAIZ, 'show', f'{rev}:{ruta}'], capture_output=True, check=True).stdout


# GitHub simulado: los datos nuevos (formato 4) y la versión nueva con su parche.
PUB = tempfile.mkdtemp(prefix='mff-gh-')
m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
assert m['formato'] == 4
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

# La 1.0.12 instalada: su programa (el parche publicado) y sus datos de formato 3 (los de a51ea31).
P = tempfile.mkdtemp(prefix='mff-prog-')
zipfile.ZipFile(base).extractall(P)
VIEJOS = {'data.js': git_show('a51ea31', 'data.js'), 'datos.json': git_show('a51ea31', 'datos.json'),
          'docs/AUDITORIA.md': git_show('a51ea31', 'docs/AUDITORIA.md')}
assert json.loads(VIEJOS['datos.json'])['formato'] == 3
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
        ok('1.0.12 instalada, con sus datos de formato 3', e0['version'] == '1.0.12' and pg.evaluate('window.MFF_VERSION.formato') == 3,
           (e0['version'], pg.evaluate('window.MFF_VERSION.formato')))
        pg.wait_for_selector('.aviso-app', timeout=30000)
        avisos = pg.locator('.aviso-app').all_inner_texts()
        ok('1.0.12: avisa que los datos nuevos son para una versión más nueva', any('versión más nueva' in a for a in avisos), avisos)
        ok('1.0.12: no bajó los datos de formato 4', json.load(open(os.path.join(D, 'datos.json')))['formato'] == 3)
        ok('1.0.12: no tiene la solapa Glosario', pg.locator('[data-a="goGlosario"]').count() == 0)
        pg.wait_for_selector('[data-a="actualizarApp"]', timeout=30000)
        pg.evaluate("window.__marca = 'antes del parche'")
        pg.click('[data-a="actualizarApp"]')
        # El parche reinicia la app; la 1.0.13 ve datos de otro formato, los baja y recarga.
        try:
            pg.wait_for_function("window.__marca === undefined && window.MFF_VERSION && window.MFF_VERSION.formato === 4"
                                 " && document.querySelector('.ccard')", timeout=180000)
        except Exception:
            pg.screenshot(path=S + '/parche113_trabado.png')
            print('--- texto de la página:', pg.evaluate("document.body.innerText.slice(0, 600)"))
            print('--- lanzador:', ''.join(SALIDA)[-3000:])
            raise
        pg.wait_for_timeout(1000)
        e1 = estado(pg)
        rec = pg.evaluate("""() => ['app.js', 'styles.css'].map(n => { const e = performance.getEntriesByType('resource')
                               .find(x => new URL(x.name).pathname === '/' + n);
                               return e ? [new URL(e.name).pathname + new URL(e.name).search, e.transferSize] : [n, 'sin entrada']; })""")
        ok('parche aplicado: 1.0.13, con app.js y styles.css nuevos', e1['version'] == '1.0.13'
           and all(isinstance(t, int) and t > 0 and 'v=1.0.13' in n for n, t in rec), (e1['version'], rec))
        dl = json.load(open(os.path.join(D, 'datos.json')))
        ok('1.0.13: bajó sola los datos de formato 4 y son los publicados',
           dl['formato'] == 4 and dl['archivos']['data.js']['sha256'] == m['archivos']['data.js']['sha256'])
        ok('1.0.13: sin el aviso de datos incompatibles', not any('versión más nueva' in a for a in pg.locator('.aviso-app').all_inner_texts()))
        pg.click('[data-a="goGlosario"]'); pg.wait_for_selector('.glterm')
        ok('1.0.13: solapa Glosario con los datos bajados', pg.locator('.glterm').count() == 44 and pg.locator('.glef').count() == 126,
           (pg.locator('.glterm').count(), pg.locator('.glef').count()))
        ficha(pg, 'abomination')
        pg.click('[data-a="fichaTab"][data-v="analisis"]'); pg.wait_for_timeout(200)
        ok('1.0.13: la pestaña Análisis sigue andando', pg.locator('#fcuerpo .anfila').count() > 10)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    try: os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError): pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
