"""La 1.0.18 instalada se actualiza a la 1.0.19 por el camino del parche. Los datos no cambian de
formato (6): la app nueva arranca con los mismos datos, sin bajar nada.

Sin red: el programa de la 1.0.18 sale de git (6a8a9d3, el último commit de la 1.0.18 que se
entregó; los archivos de PROGRAMA son los de su commit de versión, 75a5804) y el parche de la 1.0.19
se arma acá con los archivos de PROGRAMA de desktop/construir.py, como `construir.py programa` (sin
el Python embebido, que va solo en el instalador). Los datos publicados son los de harness.DATOS, los
mismos que tiene la 1.0.18.

Antes del parche: la 1.0.18 ofrece la 1.0.19 y no avisa nada de los datos; sus skills no abren
«Cómo funciona». Después: la 1.0.19 arranca con app.js y styles.css nuevos y los mismos datos, y
la Tier-2 de Doctor Voodoo — Savage Avengers abre su «Cómo funciona» con las cinco secciones."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, io, json, os, signal, subprocess, sys, tarfile, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import Chequeo, RAIZ, DATOS
from playwright.sync_api import sync_playwright
S = PRUEBAS
VIEJA = '6a8a9d3'
ok = Chequeo()
v_nueva = json.load(open(f'{RAIZ}/version.json', encoding='utf-8'))
assert v_nueva['version'] == '1.0.19' and v_nueva['formato_datos'] == 6
sys.path.insert(0, f'{RAIZ}/desktop')
from construir import PROGRAMA
buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
    for rel in PROGRAMA:
        z.write(os.path.join(RAIZ, *rel.split('/')), rel)
parche = buf.getvalue()
# latest.json como lo arma construir.py manifiesto (sin el instalador, que se arma en Windows).
latest_nuevo = {'version': v_nueva['version'], 'python': v_nueva['python'], 'notas': v_nueva['notas'],
                'formato_datos': v_nueva['formato_datos'], 'instalador': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1}}


def git_show(rev, ruta):
    return subprocess.run(['git', '-C', RAIZ, 'show', f'{rev}:{ruta}'], capture_output=True, check=True).stdout


# GitHub simulado: los mismos datos (formato 6) y la versión nueva con su parche.
PUB = tempfile.mkdtemp(prefix='mff-gh-')
m = json.load(open(os.path.join(DATOS, 'datos.json'), encoding='utf-8'))
assert m['formato'] == 6
m['imagenes'] = [[r, u] for r, u in m['imagenes'] if os.path.exists(os.path.join(DATOS, r))]
json.dump(m, open(os.path.join(PUB, 'datos.json'), 'w', encoding='utf-8'))
for rel in m['archivos']:
    os.makedirs(os.path.dirname(os.path.join(PUB, rel)) or PUB, exist_ok=True)
    open(os.path.join(PUB, rel), 'wb').write(open(os.path.join(DATOS, rel), 'rb').read())
open(os.path.join(PUB, 'parche.zip'), 'wb').write(parche)


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=PUB, **k)
    def log_message(self, *a): pass


srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_port}/'
latest = dict(latest_nuevo, parche={'url': BASE + 'parche.zip', 'bytes': len(parche), 'sha256': hashlib.sha256(parche).hexdigest()})
json.dump(latest, open(os.path.join(PUB, 'latest.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# La 1.0.18 instalada: su programa (de git) y sus datos de formato 6 (los de ese commit).
P = tempfile.mkdtemp(prefix='mff-prog-')
tar = subprocess.run(['git', '-C', RAIZ, 'archive', VIEJA, *PROGRAMA], capture_output=True, check=True).stdout
tarfile.open(fileobj=io.BytesIO(tar)).extractall(P, filter='data')
assert json.load(open(os.path.join(P, 'version.json'), encoding='utf-8'))['version'] == '1.0.18'
VIEJOS = {rel: git_show(VIEJA, rel) for rel in ('data.js', 'datos.json', 'docs/AUDITORIA.md')}
assert json.loads(VIEJOS['datos.json'])['formato'] == 6
assert json.loads(VIEJOS['datos.json'])['archivos']['data.js']['sha256'] == m['archivos']['data.js']['sha256'], 'los datos publicados no son los de la 1.0.18'
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
os.symlink(os.path.join(DATOS, 'images'), os.path.join(D, 'images'))

p = subprocess.Popen([sys.executable, os.path.join(P, 'desktop', 'lanzador.py'), '--datos', D, '--sin-ventana',
                      '--origen-datos', BASE, '--origen-app', BASE + 'latest.json'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
while True:
    l = p.stdout.readline()
    if not l: raise SystemExit('no arrancó')
    if 'abriendo' in l: url = l.split('abriendo')[1].strip(); break
SALIDA = []
# La salida del lanzador se sigue leyendo: si nadie la lee, el caño se llena y el proceso se traba.
threading.Thread(target=lambda: [SALIDA.append(x) for x in p.stdout], daemon=True).start()


def ficha_skills(pg, cid, uid=''):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.evaluate("""([cid, uid]) => { const el = document.createElement('button'); el.dataset.a = 'open';
        el.dataset.cid = cid; el.dataset.uid = uid; document.body.appendChild(el); el.click(); el.remove(); }""", [cid, uid])
    pg.wait_for_selector('.fcab')
    pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_selector('.skill')


def tooltip(pg):
    """Toca la cabecera de la Tier-2 (Voodoo Shield) y devuelve [botón «?» presente, secciones del popover]."""
    return pg.evaluate("""() => { const sk = [...document.querySelectorAll('.skill')].find(e => e.querySelector('.top').textContent.includes('Voodoo Shield'));
        const b = sk.querySelector('.sktit'); if (!b) return [false, []];
        b.click(); const pop = document.getElementById('skpop');
        const secs = pop ? [...pop.querySelectorAll('.tipsec h4')].map(h => h.textContent) : [];
        if (pop) pop.querySelector('[data-a="tipCerrar"]').click();
        return [true, secs]; }""")


def estado(pg):
    return pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json())")


try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e))); pg.on('dialog', lambda d: d.accept())
        pg.goto(url); pg.wait_for_selector('.ccard')
        e0 = estado(pg)
        ok('1.0.18 instalada, con datos de formato 6', e0['version'] == '1.0.18' and pg.evaluate('window.MFF_VERSION.formato') == 6,
           (e0['version'], pg.evaluate('window.MFF_VERSION.formato')))
        pg.wait_for_selector('[data-a="actualizarApp"]', timeout=30000)
        avisos = pg.locator('.aviso-app').all_inner_texts()
        ok('1.0.18: ofrece la 1.0.19 sin avisar nada de los datos',
           any('1.0.19' in a for a in avisos) and not any('versión más nueva de la app' in a for a in avisos), avisos)
        cid, uid = pg.evaluate("""() => { const c = window.MFF_SEED_CHARACTERS.find(x => x.name === 'Doctor Voodoo');
            const u = c.uniforms.find(x => /Savage Avengers/.test(x.name)); return [c.id, u.id]; }""")
        ficha_skills(pg, cid, uid)
        antes_ = tooltip(pg)
        ok('1.0.18: las skills no abren «Cómo funciona»', antes_ == [False, []], antes_)
        pg.evaluate("window.__marca = 'antes del parche'")
        pg.click('[data-a="actualizarApp"]')
        # El parche reinicia la app; la 1.0.19 arranca con los mismos datos.
        try:
            pg.wait_for_function("window.__marca === undefined && window.MFF_VERSION && window.MFF_VERSION.formato === 6"
                                 " && document.querySelector('.ccard')", timeout=180000)
        except Exception:
            pg.screenshot(path=S + '/parche119_trabado.png')
            print('--- texto de la página:', pg.evaluate("document.body.innerText.slice(0, 600)"))
            print('--- lanzador:', ''.join(SALIDA)[-3000:])
            raise
        pg.wait_for_timeout(1000)
        e1 = estado(pg)
        rec = pg.evaluate("""() => ['app.js', 'styles.css'].map(n => { const e = performance.getEntriesByType('resource')
                               .find(x => new URL(x.name).pathname === '/' + n);
                               return e ? [new URL(e.name).pathname + new URL(e.name).search, e.transferSize] : [n, 'sin entrada']; })""")
        ok('parche aplicado: 1.0.19, con app.js y styles.css nuevos', e1['version'] == '1.0.19'
           and all(isinstance(t, int) and t > 0 and 'v=1.0.19' in n for n, t in rec), (e1['version'], rec))
        dl = json.load(open(os.path.join(D, 'datos.json')))
        ok('1.0.19: los mismos datos de formato 6', dl['formato'] == 6 and dl['archivos']['data.js']['sha256'] == m['archivos']['data.js']['sha256'])
        ok('1.0.19: sin el aviso de datos incompatibles', not any('versión más nueva' in a for a in pg.locator('.aviso-app').all_inner_texts()))
        ficha_skills(pg, cid, uid)
        despues = tooltip(pg)
        ok('1.0.19: la Tier-2 de Doctor Voodoo — Savage Avengers abre «Cómo funciona» con las cinco secciones',
           despues == [True, ['Cómo funciona', 'Cuándo, cuánto, a quién', 'Texto del juego', 'Certeza y fuentes', 'Diferencias con el coreano']], despues)
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    try: os.kill(json.load(open(os.path.join(D, 'instancia.json')))['pid'], signal.SIGTERM)
    except (OSError, ValueError, KeyError): pass
    if p.poll() is None: p.terminate(); p.wait()
    srv.shutdown()
ok.fin()
