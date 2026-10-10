"""La 1.0.10 publicada (el parche de la release de GitHub, con sus datos de formato 1) se actualiza
a la 1.0.11 armada acá por el camino real, con datos publicados de formato 2.

Antes del parche: la 1.0.10 sigue andando con sus datos, avisa que los datos nuevos son para una
versión más nueva y no los baja; el uniforme que cambia el género todavía muestra el de la base.
Después: la 1.0.11 arranca, ve que sus datos locales son de otro formato, baja los nuevos sola y
recarga; el género del uniforme, el perfil calculado y la ventaja de Universal están."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo
from playwright.sync_api import sync_playwright
RAIZ = RAIZ
S = PRUEBAS
ok = Chequeo()
base = f'{S}/release-v1.0.10/mff-parche-1.0.10.zip'
latest_nuevo = json.load(open(f'{RAIZ}/dist/latest.json', encoding='utf-8'))
parche = open(f'{RAIZ}/dist/mff-parche-1.0.11.zip', 'rb').read()


def git_show(rev, ruta):
    return subprocess.run(['git', '-C', RAIZ, 'show', f'{rev}:{ruta}'], capture_output=True, check=True).stdout


# GitHub simulado: los datos nuevos (formato 2) y la versión nueva con su parche.
PUB = tempfile.mkdtemp(prefix='mff-gh-')
m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
assert m['formato'] == 2
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

# La 1.0.10 instalada: su programa (el parche publicado) y sus datos de formato 1 (los de 093cde8).
P = tempfile.mkdtemp(prefix='mff-prog-')
zipfile.ZipFile(base).extractall(P)
VIEJOS = {'data.js': git_show('093cde8', 'data.js'), 'datos.json': git_show('093cde8', 'datos.json'),
          'docs/AUDITORIA.md': git_show('093cde8', 'docs/AUDITORIA.md')}
assert json.loads(VIEJOS['datos.json'])['formato'] == 1
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

# Un uniforme que cambia el género (de los datos nuevos).
nuevos = json.loads(open(os.path.join(RAIZ, 'data.js'), encoding='utf-8').read()
                    .split('window.MFF_SEED_CHARACTERS = ', 1)[1].split(';\n', 1)[0])
caso = next((c, u) for c in nuevos for u in c['uniforms'] if 'gender' in u)
pj, uni = caso
print('caso de género:', pj['name'], '/', uni.get('name'), pj['gender'], '->', uni['gender'])

p = subprocess.Popen([sys.executable, os.path.join(P, 'desktop', 'lanzador.py'), '--datos', D, '--sin-ventana',
                      '--origen-datos', BASE, '--origen-app', BASE + 'latest.json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
while True:
    l = p.stdout.readline()
    if not l: raise SystemExit('no arrancó')
    if 'abriendo' in l: url = l.split('abriendo')[1].strip(); break
SALIDA = []
# La salida del lanzador se sigue leyendo: si nadie la lee, el caño se llena y el proceso se traba.
threading.Thread(target=lambda: [SALIDA.append(x) for x in p.stdout], daemon=True).start()


def genero(pg):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', pj['name']); pg.wait_for_timeout(300)
    pg.click(f'.ccard[data-cid="{pj["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    pg.select_option('select[data-a="uniformSel"]', uni['id']); pg.wait_for_timeout(200)
    return pg.locator('.statgrid .stat', has=pg.locator('.k', has_text='Género')).locator('.v').text_content().strip()


def estado(pg):
    return pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json())")


try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e))); pg.on('dialog', lambda d: d.accept())
        pg.goto(url); pg.wait_for_selector('.ccard')
        e0 = estado(pg)
        ok('1.0.10 instalada, con sus datos de formato 1', e0['version'] == '1.0.10' and pg.evaluate('window.MFF_VERSION.formato') == 1,
           (e0['version'], pg.evaluate('window.MFF_VERSION.formato')))
        pg.wait_for_selector('.aviso-app', timeout=30000)
        avisos = pg.locator('.aviso-app').all_inner_texts()
        ok('1.0.10: avisa que los datos nuevos son para una versión más nueva', any('versión más nueva' in a for a in avisos), avisos)
        g0 = genero(pg)
        ok(f"1.0.10: {pj['name']} con su uniforme todavía muestra el género de la base", g0 == pj['gender'], g0)
        ok('1.0.10: no bajó los datos de formato 2', json.load(open(os.path.join(D, 'datos.json')))['formato'] == 1)
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        pg.wait_for_selector('[data-a="actualizarApp"]', timeout=30000)
        pg.evaluate("window.__marca = 'antes del parche'")
        pg.click('[data-a="actualizarApp"]')
        # El parche reinicia la app; la 1.0.11 ve datos de otro formato, los baja y recarga.
        try:
            pg.wait_for_function("window.__marca === undefined && window.MFF_VERSION && window.MFF_VERSION.formato === 2"
                                 " && document.querySelector('.ccard')", timeout=180000)
        except Exception:
            pg.screenshot(path=S + '/parche111_trabado.png')
            print('--- texto de la página:', pg.evaluate("document.body.innerText.slice(0, 600)"))
            print('--- lanzador:', ''.join(SALIDA)[-3000:])
            raise
        pg.wait_for_timeout(1000)
        e1 = estado(pg)
        rec = pg.evaluate("""() => ['app.js', 'styles.css'].map(n => { const e = performance.getEntriesByType('resource')
                               .find(x => new URL(x.name).pathname === '/' + n);
                               return e ? [new URL(e.name).pathname + new URL(e.name).search, e.transferSize] : [n, 'sin entrada']; })""")
        ok('parche aplicado: 1.0.11, con app.js y styles.css nuevos', e1['version'] == '1.0.11'
           and all(isinstance(t, int) and t > 0 and 'v=1.0.11' in n for n, t in rec), (e1['version'], rec))
        dl = json.load(open(os.path.join(D, 'datos.json')))
        ok('1.0.11: bajó sola los datos de formato 2 y son los publicados',
           dl['formato'] == 2 and dl['archivos']['data.js']['sha256'] == m['archivos']['data.js']['sha256'])
        ok('1.0.11: sin el aviso de datos incompatibles', not any('versión más nueva' in a for a in pg.locator('.aviso-app').all_inner_texts()))
        g1 = genero(pg)
        ok(f"1.0.11: {pj['name']} con su uniforme muestra su género ({uni['gender']})", g1 == uni['gender'], g1)
        ok('1.0.11: perfil de combate calculado en los datos', pg.evaluate("Object.keys(window.MFF_PERFIL || {}).length") > 800)
        ok('1.0.11: Universal le gana a las otras tres (ventaja menor)',
           pg.evaluate("JSON.stringify(window.MFF_SEED.VENTAJA_TIPO.Universal)") == json.dumps({'Combate': 'menor', 'Velocidad': 'menor', 'Detonación': 'menor'}, ensure_ascii=False, separators=(',', ':')))
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        pg.fill('#q', 'Abomination'); pg.wait_for_timeout(300)
        pg.click('.ccard[data-cid="abomination"][data-uid=""]'); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
        ok('1.0.11: combinaciones con su cobertura', pg.locator('#combos .combo .cobertura').count() == pg.locator('#combos .combo').count() > 0)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    try: os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError): pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
