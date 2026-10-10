"""La 1.0.16 (45abe69, datos de formato 5) frente a los datos nuevos (formato 6, los de harness.DATOS),
con GitHub ya publicando la 1.0.17 y los datos de formato 6:

A con sus datos de formato 5: sigue andando, avisa que los datos nuevos son para una versión más nueva
  de la app y no los baja.
B con los datos de formato 6 en su carpeta (la carpeta de datos es la misma para la app instalada y
  para MFF.bat desde el repo): no los muestra (con ellos, un marcador de Leads & Supports saldría como
  dato de la wiki); queda en la pantalla de datos con el motivo, que pide actualizar la app.

El programa de la 1.0.16 sale de git (git archive, solo lectura) a una carpeta temporal."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import io, json, os, shutil, subprocess, sys, tarfile, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import origen_local, Chequeo, RAIZ, DATOS
from playwright.sync_api import sync_playwright
VIEJA = '45abe69'
ok = Chequeo()
FORMATO = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))['formato_datos']
assert json.load(open(os.path.join(DATOS, 'datos.json'), encoding='utf-8'))['formato'] == FORMATO


def git_show(rel):
    return subprocess.run(['git', '-C', RAIZ, 'show', f'{VIEJA}:{rel}'], capture_output=True, check=True).stdout


origen = origen_local()   # publica los datos de DATOS y un latest.json de la versión del repo
PROG = tempfile.mkdtemp(prefix='mff-1016-')
tar = subprocess.run(['git', '-C', RAIZ, 'archive', VIEJA, 'index.html', 'app.js', 'styles.css', 'version.json', 'desktop'],
                     capture_output=True, check=True).stdout
tarfile.open(fileobj=io.BytesIO(tar)).extractall(PROG, filter='data')
v_vieja = json.load(open(os.path.join(PROG, 'version.json'), encoding='utf-8'))
assert v_vieja['version'] == '1.0.16' and v_vieja['formato_datos'] == 5 != FORMATO, v_vieja
harness.RAIZ = PROG   # levantar() corre el lanzador de la 1.0.16


def carpeta(datos):
    d = tempfile.mkdtemp(prefix='mffdatos-')
    for rel, b in datos.items():
        os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
        open(os.path.join(d, rel), 'wb').write(b)
    os.symlink(os.path.join(DATOS, 'images'), os.path.join(d, 'images'))
    return d


propios = {rel: git_show(rel) for rel in ('data.js', 'datos.json', 'docs/AUDITORIA.md')}
nuevos = {rel: open(os.path.join(DATOS, rel), 'rb').read() for rel in ('data.js', 'datos.json', 'docs/AUDITORIA.md')}
with sync_playwright() as p:
    b = p.chromium.launch()
    # A: sus datos de formato 5
    d = carpeta(propios)
    srv, url = harness.levantar(d, origen)
    try:
        pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.wait_for_selector('.aviso-app', timeout=30000)
        avisos = pg.locator('.aviso-app').all_inner_texts()
        ok('A 1.0.16 con sus datos: anda con el formato 5', pg.evaluate('window.MFF_VERSION.formato') == 5)
        ok('A avisa que los datos nuevos son para una versión más nueva de la app', any('versión más nueva de la app' in a for a in avisos), avisos)
        pg.wait_for_timeout(1500)
        ok('A no baja los datos de formato 6', open(os.path.join(d, 'datos.json'), 'rb').read() == propios['datos.json'])
        ok('A sin errores de página', not errores, errores[:3])
        pg.close()
    finally:
        srv.terminate(); srv.wait()
    # B: datos de formato 6 en su carpeta
    d = carpeta(nuevos)
    srv, url = harness.levantar(d, origen)
    try:
        pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url)
        motivo = f'los datos publicados son de formato {FORMATO} y esta versión de la app usa el 5: actualizá la app.'
        pg.wait_for_function("document.querySelector('.fatal p') && document.querySelector('.fatal p').textContent.includes(%s)"
                             % json.dumps(motivo), timeout=60000)
        ok('B 1.0.16 con datos de formato 6: no los muestra y queda en la pantalla de datos pidiendo actualizar la app',
           pg.locator('.ccard').count() == 0 and pg.locator('.fatal h1').inner_text().upper() == 'ACTUALIZANDO LOS DATOS DEL JUEGO',
           (pg.locator('.fatal p').inner_text(), 'botón de parche:', pg.locator('[data-a="actualizarApp"]').count()))
        ok('B no toca los datos de la carpeta', all(open(os.path.join(d, rel), 'rb').read() == x for rel, x in nuevos.items()))
        ok('B sin errores de página', not errores, errores[:3])
        pg.close()
    finally:
        srv.terminate(); srv.wait()
    b.close()
shutil.rmtree(PROG)
ok.fin()
