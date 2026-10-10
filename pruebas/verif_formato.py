"""Datos locales que la app no puede leer: de un formato anterior (el 1 de la 1.0.10, el 2 de la
1.0.11, el 3 de la 1.0.12, el 4 de la 1.0.13, el 5 de la 1.0.14 a la 1.0.16) o sin data.js. La app no
tiene que romperse al cargar: va a pantallaDatos(), baja los publicados (del formato que pide
version.json), recarga y muestra el roster, sin errores de página.

Además, el hueco entre el push de una versión con formato nuevo y el workflow de datos: con datos
locales de formato 5 y publicados solo los de formato 5 (en la raíz y en datos/5/, sin la carpeta del
formato de la app), la app se queda en pantallaDatos con el motivo a la vista y no toca los datos locales.
Desde la 1.0.30 la app baja los de la carpeta de su formato, datos/<formato>/ (#1).

Los publicados salen de harness.DATOS (el repo, o MFF_DATOS mientras el data.js del repo sea de un
formato anterior: armar_datos_prueba.py)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import http.server, json, os, shutil, subprocess, sys, tempfile, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import levantar, Chequeo, RAIZ, DATOS
from playwright.sync_api import sync_playwright
ok = Chequeo()
v = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))
FORMATO = v['formato_datos']
DEL_5 = '45abe69'   # la 1.0.16: datos de formato 5, los mismos que publicaron la 1.0.14 y la 1.0.15


def git_show(rev, rel):
    return subprocess.run(['git', '-C', RAIZ, 'show', f'{rev}:{rel}'], capture_output=True, check=True).stdout


def publicar(leer):
    """Un GitHub local con datos.json y sus archivos (leer(rel) da los bytes) y un latest.json de la
    misma versión (no ofrece parche). datos.json sin imágenes: la prueba no baja nada."""
    pub = tempfile.mkdtemp(prefix='mffpub-')
    m = json.loads(leer('datos.json'))
    m['imagenes'] = []
    for base in (pub, os.path.join(pub, 'datos', str(m['formato']))):   # la raíz y la carpeta de su formato
        os.makedirs(base, exist_ok=True)
        json.dump(m, open(os.path.join(base, 'datos.json'), 'w', encoding='utf-8'))
        for rel in m['archivos']:
            os.makedirs(os.path.dirname(os.path.join(base, rel)) or base, exist_ok=True)
            open(os.path.join(base, rel), 'wb').write(leer(rel))
    json.dump({'version': v['version'], 'python': v['python'], 'notas': '', 'formato_datos': FORMATO,
               'parche': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1}, 'instalador': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1}},
              open(os.path.join(pub, 'latest.json'), 'w'))

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=pub, **k)
        def log_message(self, *a): pass
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return m, srv, f'http://127.0.0.1:{srv.server_port}/'


m, srv_pub, ORIGEN = publicar(lambda rel: open(os.path.join(DATOS, rel), 'rb').read())
assert m['formato'] == FORMATO, (m['formato'], FORMATO)


def carpeta(rev):
    """Carpeta de datos con los de una versión publicada (rev), o sin datos (rev None)."""
    d = tempfile.mkdtemp(prefix='mffdatos-')
    if rev:
        viejo = json.loads(git_show(rev, 'datos.json'))
        for rel in ['datos.json', *viejo['archivos']]:
            os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
            open(os.path.join(d, rel), 'wb').write(git_show(rev, rel))
    os.symlink(os.path.join(DATOS, 'images'), os.path.join(d, 'images'))
    return d


for nombre, rev, formato_viejo in (('datos de formato 1 (1.0.10)', '093cde8', 1), ('datos de formato 2 (1.0.11)', '663a213', 2),
                                   ('datos de formato 3 (1.0.12)', 'a51ea31', 3),
                                   ('datos de formato 4 (1.0.13)', 'ab9a8e0', 4),
                                   ('datos de formato 5 (1.0.14 a 1.0.16)', DEL_5, 5),
                                   ('sin data.js', None, None)):
    d = carpeta(rev)
    if rev:
        assert json.load(open(os.path.join(d, 'datos.json'), encoding='utf-8'))['formato'] == formato_viejo != FORMATO
    srv, url = levantar(d, ORIGEN)
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
            pg.on('pageerror', lambda e: errores.append(str(e)))
            pg.goto(url)
            pg.wait_for_function(f"window.MFF_VERSION && window.MFF_VERSION.formato === {FORMATO} && document.querySelector('.ccard')", timeout=120000)
            local = json.load(open(os.path.join(d, 'datos.json'), encoding='utf-8'))
            n = pg.locator('.ccard').count()
            ok(f'{nombre}: baja los publicados (formato {FORMATO}) y muestra el roster',
               local['formato'] == FORMATO and local['archivos']['data.js']['sha256'] == m['archivos']['data.js']['sha256'] and n > 0,
               (local['formato'], local['archivos']['data.js']['sha256'][:8], m['archivos']['data.js']['sha256'][:8], n))
            ok(f'{nombre}: sin errores de página', not errores, errores[:3])
            b.close()
    finally:
        srv.terminate(); srv.wait()
srv_pub.shutdown()

# El hueco: la app nueva con datos de formato 5, y GitHub todavía publica los de formato 5.
m5, srv_pub5, ORIGEN5 = publicar(lambda rel: git_show(DEL_5, rel))
assert m5['formato'] == 5 != FORMATO
d = carpeta(DEL_5)
antes = {f: open(os.path.join(d, f), 'rb').read() for f in ('data.js', 'datos.json')}
srv, url = levantar(d, ORIGEN5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url)
        # Desde la 1.0.30 la app pide los de su formato (datos/<formato>/): no están, y lo dice.
        motivo = f'No se pudieron bajar los datos nuevos: todavía no hay datos publicados de formato {FORMATO}'
        pg.wait_for_function("document.querySelector('.fatal p') && document.querySelector('.fatal p').textContent.includes(%s)"
                             % json.dumps(motivo), timeout=60000)
        titulo = pg.locator('.fatal h1').inner_text()
        ok('publicados de formato 5: la app queda en la pantalla de datos con el motivo',
           titulo.upper() == 'ACTUALIZANDO LOS DATOS DEL JUEGO' and pg.locator('.ccard').count() == 0, (titulo, pg.locator('.fatal p').inner_text()))
        ok('publicados de formato 5: los datos locales no cambian',
           all(open(os.path.join(d, f), 'rb').read() == b_ for f, b_ in antes.items()) and not [f for f in os.listdir(d) if f.endswith('.nuevo')])
        ok('publicados de formato 5: sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
    srv_pub5.shutdown()
ok.fin()
