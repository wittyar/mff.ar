"""dist/programa (lo que instala el instalador) arranca solo, sin scripts/ ni el repo."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import os, shutil, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright
PROG = f'{RAIZ}/dist/programa'
fallas = []
def chequear(n, c, d=''):
    print(('OK   ' if c else 'FALLA'), n, '|', d)
    if not c: fallas.append(n)
D = tempfile.mkdtemp(prefix='mff-inst-')
os.symlink(f'{RAIZ}/images', os.path.join(D, 'images'))
p = subprocess.Popen([sys.executable, os.path.join(PROG, 'desktop', 'lanzador.py'), '--datos', D, '--sin-ventana'],
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
url = None
while not url:
    l = p.stdout.readline()
    if not l: break
    if 'abriendo' in l: url = l.split('abriendo')[1].strip()
chequear('arranca desde dist/programa', url is not None)
chequear('siembra los datos iniciales', all(os.path.exists(os.path.join(D, f)) for f in ('data.js', 'datos.json', 'docs/AUDITORIA.md')))
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(); errores = []
    pg.on('pageerror', lambda e: errores.append(str(e)))
    pg.goto(url); pg.wait_for_selector('.ccard')
    ico = pg.evaluate("fetch('/favicon.ico').then(r => [r.status, r.headers.get('content-type')])")
    chequear('sirve el ícono', ico[0] == 200, ico)
    pg.click('[data-a="goSettings"]'); pg.wait_for_timeout(300)
    sec = pg.evaluate("document.querySelector('#seccion-actualizaciones').innerText")
    V = __import__('json').load(open(os.path.join(PROG, 'version.json')))['version']
    chequear(f'Ajustes muestra la versión {V} y no dice "desde el repo"', V in sec and 'desde el repo' not in sec, sec.splitlines()[3:6])
    chequear('sin errores de página', not errores, errores)
    b.close()
p.terminate(); p.wait()
print('FALLAS:', fallas or 'ninguna')
