"""Parche de versión: aviso, confirmación, aplicación verificada y reinicio en el mismo puerto.

1  versión nueva con el mismo Python: aviso con Actualizar y novedades
2  Actualizar: confirma, aplica, se relanza en el mismo puerto y la ventana recarga con la nueva
3  parche con sha que no coincide: error, el programa no cambia
4  parche con un archivo que no es del programa: error, no cambia
5  versión nueva con otro Python: pide el instalador completo (enlace)
6  corriendo desde el repo (.git): dice que se actualiza con git pull, sin botón
7  sin release publicada (404): el error aparece junto a la búsqueda, la app anda

El programa sale de RAIZ; los datos (data.js, datos.json, docs/, images/), de harness.DATOS.
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, http.server, io, json, os, shutil, signal, subprocess, sys, tempfile, threading, time, zipfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import RAIZ, DATOS
from playwright.sync_api import sync_playwright

fallas = []
def chequear(nombre, cond, detalle=''):
    print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
    if not cond: fallas.append(nombre)

PUB = tempfile.mkdtemp(prefix='mff-rel-')        # lo que sirve el "GitHub" falso
class Origen(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=PUB, **k)
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Origen)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_port}/'

def manifiesto_repo():
    m = json.load(open(os.path.join(DATOS, 'datos.json'), encoding='utf-8'))
    m['imagenes'] = [[r, u] for r, u in m['imagenes'] if os.path.exists(os.path.join(DATOS, r))]
    return m
json.dump(manifiesto_repo(), open(os.path.join(PUB, 'datos.json'), 'w', encoding='utf-8'))
# Desde la 1.0.30 la app consulta los de su formato, en datos/<formato>/ (#1).
os.makedirs(os.path.join(PUB, 'datos', str(manifiesto_repo()['formato'])))
json.dump(manifiesto_repo(), open(os.path.join(PUB, 'datos', str(manifiesto_repo()['formato']), 'datos.json'), 'w', encoding='utf-8'))

VERSION = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))
def publicar_release(version, python=None, romper_sha=False, extra=None):
    """latest.json + parche con app.js marcado y servidor.py que reporta la versión nueva."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        v = dict(VERSION, version=version, notas=f'Cambios de la {version}.', python=python or VERSION['python'])
        z.writestr('version.json', json.dumps(v))
        z.writestr('app.js', open(os.path.join(RAIZ, 'app.js'), encoding='utf-8').read() + f'\n// parche {version}\n')
        for f in ('index.html', 'styles.css'):
            z.write(os.path.join(RAIZ, f), f)
        for f in os.listdir(os.path.join(RAIZ, 'desktop')):
            if f.endswith('.py'):
                z.write(os.path.join(RAIZ, 'desktop', f), 'desktop/' + f)
        for nombre, contenido in (extra or {}).items():
            z.writestr(nombre, contenido)
    datos = buf.getvalue()
    open(os.path.join(PUB, f'parche-{version}.zip'), 'wb').write(datos)
    latest = {'version': version, 'notas': f'Cambios de la {version}.', 'python': python or VERSION['python'],
              'formato_datos': VERSION['formato_datos'],
              'parche': {'url': BASE + f'parche-{version}.zip', 'bytes': len(datos),
                         'sha256': '0' * 64 if romper_sha else hashlib.sha256(datos).hexdigest()},
              'instalador': {'url': BASE + f'instalador-{version}.exe', 'bytes': 1, 'sha256': '0' * 64}}
    json.dump(latest, open(os.path.join(PUB, 'latest.json'), 'w', encoding='utf-8'))

def programa(con_git=False):
    """Copia del programa como quedaría instalado (sin .git), con sus datos iniciales."""
    d = tempfile.mkdtemp(prefix='mff-prog-')
    for f in ('index.html', 'app.js', 'styles.css', 'version.json'):
        shutil.copy(os.path.join(RAIZ, f), d)
    for f in ('data.js', 'datos.json'):
        shutil.copy(os.path.join(DATOS, f), d)
    shutil.copytree(os.path.join(RAIZ, 'desktop'), os.path.join(d, 'desktop'), ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(os.path.join(DATOS, 'docs'), os.path.join(d, 'docs'))
    if con_git: os.mkdir(os.path.join(d, '.git'))
    return d

def datos():
    d = tempfile.mkdtemp(prefix='mff-dat-')
    os.symlink(os.path.join(DATOS, 'images'), os.path.join(d, 'images'))
    shutil.copy(os.path.join(DATOS, 'data.js'), d)
    json.dump(manifiesto_repo(), open(os.path.join(d, 'datos.json'), 'w', encoding='utf-8'))
    return d

def lanzar(prog, dat, origen_app=None):
    p = subprocess.Popen([sys.executable, os.path.join(prog, 'desktop', 'lanzador.py'), '--datos', dat, '--sin-ventana',
                          '--origen-datos', BASE, '--origen-app', origen_app or BASE + 'latest.json'],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    while True:
        l = p.stdout.readline()
        if not l: raise SystemExit('no arrancó: ' + str(p.poll()))
        if 'abriendo' in l: return p, l.split('abriendo')[1].strip()

def apagar(p, dat):
    try:
        pid = json.load(open(os.path.join(dat, 'instancia.json')))['pid']
        os.kill(pid, signal.SIGTERM)
    except (OSError, ValueError, KeyError):
        pass
    if p.poll() is None: p.terminate(); p.wait()

def avisos(pg): return pg.evaluate("(document.querySelector('#avisos') || {}).innerText || ''")
def esperar(pg, texto, n=80):
    for _ in range(n):
        if texto in avisos(pg): return True
        pg.wait_for_timeout(150)
    return False

with sync_playwright() as pw:
    b = pw.chromium.launch()
    errores = []
    def pagina():
        pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('dialog', lambda d: d.accept())
        return pg

    # 1 y 2
    publicar_release('1.1.0')
    P, D = programa(), datos()
    p, url = lanzar(P, D)
    pg = pagina(); pg.goto(url); pg.wait_for_selector('.ccard')
    chequear('1 aviso de versión nueva con botón', esperar(pg, 'Versión 1.1.0 disponible') and pg.locator('[data-a="actualizarApp"]').count() == 1,
             avisos(pg)[:120])
    pid_viejo = p.pid
    pg.click('[data-a="actualizarApp"]')
    visto_reinicio = esperar(pg, 'Reiniciando', 100)
    pg.wait_for_function("window.location && document.querySelector('.ccard')", timeout=30000)
    for _ in range(100):
        v = pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json()).then(e => e.version).catch(() => null)")
        if v == '1.1.0': break
        pg.wait_for_timeout(300)
    pg.wait_for_selector('.ccard', timeout=30000); pg.wait_for_timeout(1500)
    app_js = pg.evaluate("fetch('/app.js').then(r => r.text())")
    nueva_pid = json.load(open(os.path.join(D, 'instancia.json')))['pid']
    chequear('2 aplica, se relanza en el mismo puerto y recarga', visto_reinicio and v == '1.1.0' and app_js.rstrip().endswith('// parche 1.1.0')
             and nueva_pid != pid_viejo and p.poll() == 0 and pg.url.startswith(url.rsplit('/', 1)[0]),
             f'reinicio visto {visto_reinicio}, versión {v}, pid {pid_viejo}->{nueva_pid}, viejo terminó {p.poll()}')
    chequear('2 respaldo del programa anterior', os.path.exists(os.path.join(D, 'programa-anterior', 'app.js'))
             and not open(os.path.join(D, 'programa-anterior', 'app.js'), encoding='utf-8').read().rstrip().endswith('// parche 1.1.0'))
    chequear('2 ya no ofrece la misma versión', esperar(pg, '', 1) and 'Versión 1.1.0 disponible' not in avisos(pg), avisos(pg)[:100])
    pg.close(); apagar(p, D)

    # 3: sha que no coincide
    publicar_release('1.2.0', romper_sha=True)
    P, D = programa(), datos()
    antes = open(os.path.join(P, 'app.js'), encoding='utf-8').read()
    p, url = lanzar(P, D)
    pg = pagina(); pg.goto(url); pg.wait_for_selector('.ccard'); esperar(pg, 'Versión 1.2.0')
    pg.click('[data-a="actualizarApp"]')
    chequear('3 sha distinto: error y el programa no cambia', esperar(pg, 'No se pudo actualizar la app')
             and 'llegó distinto' in avisos(pg) and open(os.path.join(P, 'app.js'), encoding='utf-8').read() == antes
             and not [f for f in os.listdir(P) if f.endswith('.nuevo')], avisos(pg)[:140])
    pg.close(); apagar(p, D)

    # 4: archivo ajeno en el parche
    publicar_release('1.2.1', extra={'scripts/malo.py': 'print(1)'})
    P, D = programa(), datos()
    p, url = lanzar(P, D)
    pg = pagina(); pg.goto(url); pg.wait_for_selector('.ccard'); esperar(pg, 'Versión 1.2.1')
    pg.click('[data-a="actualizarApp"]')
    chequear('4 archivo ajeno: error y no escribe', esperar(pg, 'No se pudo actualizar la app') and 'no son del programa' in avisos(pg)
             and not os.path.exists(os.path.join(P, 'scripts', 'malo.py')) and json.load(open(os.path.join(P, 'version.json')))['version'] == VERSION['version'],
             avisos(pg)[:140])
    pg.close(); apagar(p, D)

    # 5: otro Python
    publicar_release('2.0.0', python='3.15.1')
    P, D = programa(), datos()
    p, url = lanzar(P, D)
    pg = pagina(); pg.goto(url); pg.wait_for_selector('.ccard')
    ok = esperar(pg, 'Versión 2.0.0')
    enlace = pg.evaluate("(document.querySelector('#avisos a.btn') || {}).href")
    chequear('5 otro Python: pide el instalador', ok and 'instalador completo' in avisos(pg) and enlace == BASE + 'instalador-2.0.0.exe'
             and pg.locator('[data-a="actualizarApp"]').count() == 0, (avisos(pg)[:120], enlace))
    pg.close(); apagar(p, D)

    # 6: desde el repo
    publicar_release('1.3.0')
    P, D = programa(con_git=True), datos()
    p, url = lanzar(P, D)
    pg = pagina(); pg.goto(url); pg.wait_for_selector('.ccard')
    chequear('6 desde el repo: git pull, sin botón', esperar(pg, 'git pull') and pg.locator('[data-a="actualizarApp"]').count() == 0, avisos(pg)[:120])
    pg.close(); apagar(p, D)

    # 7: sin release publicada
    P, D = programa(), datos()
    p, url = lanzar(P, D, origen_app=BASE + 'no-hay/latest.json')
    pg = pagina(); pg.goto(url); pg.wait_for_selector('.ccard')
    chequear('7 sin release: error visible, la app anda', esperar(pg, 'No se pudo buscar actualizaciones') and '404' in avisos(pg)
             and pg.locator('.ccard').count() > 0, avisos(pg)[:140])
    pg.close(); apagar(p, D)
    chequear('sin errores de página', not errores, errores[:3])
    b.close()
srv.shutdown()
print('\nFALLAS:', fallas or 'ninguna')
