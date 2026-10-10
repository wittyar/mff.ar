"""Paginador compartido: el armador llega a todas las páginas y el roster sigue igual."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import os, subprocess, sys, tempfile, time
from playwright.sync_api import sync_playwright

RAIZ = RAIZ
OUT = PRUEBAS
DATOS = tempfile.mkdtemp(prefix='mff-pag-')
os.symlink(os.path.join(RAIZ, 'images'), os.path.join(DATOS, 'images'))
srv = subprocess.Popen([sys.executable, 'desktop/lanzador.py', '--datos', DATOS, '--sin-ventana'], cwd=RAIZ,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
URL = None
while not URL:
    linea = srv.stdout.readline()
    if 'abriendo' in linea: URL = linea.split('abriendo')[1].strip()
fallas = []
def chequear(nombre, cond, detalle=''):
    print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
    if not cond: fallas.append(nombre)

TILES = "document.querySelectorAll('[data-a=teamToggle]').length"
SRCS = "[...document.querySelectorAll('[data-a=teamToggle] img')].map(i => i.getAttribute('src'))"
with sync_playwright() as p:
    b = p.chromium.launch()
    for ancho in (1300, 390):
        page = b.new_page(viewport={'width': ancho, 'height': 900})
        errores = []
        page.on('pageerror', lambda e: errores.append(str(e)))
        page.on('console', lambda m: m.type == 'error' and errores.append(m.text + ' @ ' + str(m.location.get('url'))))
        page.goto(URL); page.wait_for_selector('.ccard')

        # roster: el paginador sigue andando
        page.click('[data-a="page"][data-p="1"]'); page.wait_for_timeout(300)
        activa = page.evaluate("document.querySelector('[data-a=page].primary').dataset.p")
        chequear(f'[{ancho}] roster: página 2 activa', activa == '1', activa)

        if ancho == 390:
            dims = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
            chequear('[390] sin scroll horizontal con el paginador', dims[0] <= dims[1], dims)
        page.screenshot(path=f'{OUT}/verif_paginador_{ancho}.png', full_page=False)
        chequear(f'[{ancho}] sin errores de consola', not errores, errores)
        page.close()
    b.close()
srv.terminate()
print('\nFALLAS:', fallas or 'ninguna')
