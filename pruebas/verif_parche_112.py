"""La 1.0.11 publicada (el parche de la release de GitHub, con sus datos de formato 2) se actualiza
a la 1.0.12 armada acá por el camino real, con datos publicados de formato 3.

Antes del parche: la 1.0.11 sigue andando con sus datos, avisa que los datos nuevos son para una
versión más nueva y no los baja; su ficha no tiene la pestaña Análisis.
Después: la 1.0.12 arranca, ve que sus datos locales son de otro formato, baja los nuevos sola y
recarga; la pestaña Análisis, los roles por uniforme y «← Nombre» andan."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo
from playwright.sync_api import sync_playwright
RAIZ = RAIZ
S = PRUEBAS
ok = Chequeo()
base = f'{S}/release-v1.0.11/parche.zip'
latest_nuevo = json.load(open(f'{RAIZ}/dist/latest.json', encoding='utf-8'))
assert latest_nuevo['version'] == '1.0.12' and latest_nuevo['formato_datos'] == 3
parche = open(f'{RAIZ}/dist/mff-parche-1.0.12.zip', 'rb').read()


def git_show(rev, ruta):
    return subprocess.run(['git', '-C', RAIZ, 'show', f'{rev}:{ruta}'], capture_output=True, check=True).stdout


# GitHub simulado: los datos nuevos (formato 3) y la versión nueva con su parche.
PUB = tempfile.mkdtemp(prefix='mff-gh-')
m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
assert m['formato'] == 3
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

# La 1.0.11 instalada: su programa (el parche publicado) y sus datos de formato 2 (los de 663a213).
P = tempfile.mkdtemp(prefix='mff-prog-')
zipfile.ZipFile(base).extractall(P)
VIEJOS = {'data.js': git_show('663a213', 'data.js'), 'datos.json': git_show('663a213', 'datos.json'),
          'docs/AUDITORIA.md': git_show('663a213', 'docs/AUDITORIA.md')}
assert json.loads(VIEJOS['datos.json'])['formato'] == 2
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

# Un uniforme con roles propios (de los datos nuevos).
nuevos = json.loads(open(os.path.join(RAIZ, 'data.js'), encoding='utf-8').read()
                    .split('window.MFF_SEED_CHARACTERS = ', 1)[1].split(';\n', 1)[0])
pj, uni = next((c, u) for c in nuevos for u in c['uniforms'] if 'r' in u and set(u['r']) != set(c['r']))
print('caso de roles:', pj['name'], '/', uni.get('name'), pj['r'], '->', uni['r'])

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
        ok('1.0.11 instalada, con sus datos de formato 2', e0['version'] == '1.0.11' and pg.evaluate('window.MFF_VERSION.formato') == 2,
           (e0['version'], pg.evaluate('window.MFF_VERSION.formato')))
        pg.wait_for_selector('.aviso-app', timeout=30000)
        avisos = pg.locator('.aviso-app').all_inner_texts()
        ok('1.0.11: avisa que los datos nuevos son para una versión más nueva', any('versión más nueva' in a for a in avisos), avisos)
        ok('1.0.11: no bajó los datos de formato 3', json.load(open(os.path.join(D, 'datos.json')))['formato'] == 2)
        ficha(pg, 'abomination')
        ok('1.0.11: la ficha no tiene la pestaña Análisis', pg.locator('[data-a="fichaTab"][data-v="analisis"]').count() == 0)
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        pg.wait_for_selector('[data-a="actualizarApp"]', timeout=30000)
        pg.evaluate("window.__marca = 'antes del parche'")
        pg.click('[data-a="actualizarApp"]')
        # El parche reinicia la app; la 1.0.12 ve datos de otro formato, los baja y recarga.
        try:
            pg.wait_for_function("window.__marca === undefined && window.MFF_VERSION && window.MFF_VERSION.formato === 3"
                                 " && document.querySelector('.ccard')", timeout=180000)
        except Exception:
            pg.screenshot(path=S + '/parche112_trabado.png')
            print('--- texto de la página:', pg.evaluate("document.body.innerText.slice(0, 600)"))
            print('--- lanzador:', ''.join(SALIDA)[-3000:])
            raise
        pg.wait_for_timeout(1000)
        e1 = estado(pg)
        rec = pg.evaluate("""() => ['app.js', 'styles.css'].map(n => { const e = performance.getEntriesByType('resource')
                               .find(x => new URL(x.name).pathname === '/' + n);
                               return e ? [new URL(e.name).pathname + new URL(e.name).search, e.transferSize] : [n, 'sin entrada']; })""")
        ok('parche aplicado: 1.0.12, con app.js y styles.css nuevos', e1['version'] == '1.0.12'
           and all(isinstance(t, int) and t > 0 and 'v=1.0.12' in n for n, t in rec), (e1['version'], rec))
        dl = json.load(open(os.path.join(D, 'datos.json')))
        ok('1.0.12: bajó sola los datos de formato 3 y son los publicados',
           dl['formato'] == 3 and dl['archivos']['data.js']['sha256'] == m['archivos']['data.js']['sha256'])
        ok('1.0.12: sin el aviso de datos incompatibles', not any('versión más nueva' in a for a in pg.locator('.aviso-app').all_inner_texts()))
        ficha(pg, 'abomination')
        pg.click('[data-a="fichaTab"][data-v="analisis"]'); pg.wait_for_timeout(200)
        n_filas = pg.locator('#fcuerpo .anfila').count()
        roles = [r.strip().upper() for r in pg.locator('#fcuerpo .anres .tag').all_inner_texts()]
        ok('1.0.12: pestaña Análisis de Abomination, con sus roles', n_filas > 10 and roles == ['CONTROL', 'SOPORTE', 'DAÑO'], (n_filas, roles))
        ficha(pg, pj['id'], uni['id'])
        pg.click('[data-a="fichaTab"][data-v="resumen"]'); pg.wait_for_timeout(200)
        tags = [x.strip().upper() for x in pg.locator('.fid .row').first.locator('.tag.ghost').all_inner_texts()]
        ok(f"1.0.12: {pj['name']} — {uni['name']} muestra los roles del uniforme", tags == [r.upper() for r in uni['r']], (tags, uni['r']))
        # «← Nombre»: de Abomination a otro personaje desde sus combinaciones, y de vuelta
        ficha(pg, 'abomination')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=60000)
        otro = pg.locator('#combos .combo').first.locator('[data-a="open"]').nth(1)
        otro.click(); pg.wait_for_timeout(300)
        boton = pg.locator('[data-a="atras"]')
        ok('1.0.12: la ficha a la que se pasó muestra «← Abomination»', boton.count() == 1 and boton.inner_text().strip() == '← Abomination',
           boton.all_inner_texts())
        boton.click(); pg.wait_for_selector('#combos .combo', timeout=60000)
        ok('1.0.12: «← Abomination» vuelve a sus combinaciones', pg.evaluate("history.state.charId") == 'abomination'
           and pg.evaluate("history.state.fichaTab") == 'equipos')
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    try: os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError): pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
