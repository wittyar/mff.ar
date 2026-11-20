"""La app instalada (instalador compilado con Inno Setup, Python embebido de Windows) corriendo
bajo Wine, manejada desde Chromium. Prueba lo que en Linux no se ve: rutas con espacios,
LOCALAPPDATA como carpeta de datos por defecto, candado con msvcrt, codificación de Windows,
el Python embebido sin la carpeta del script en el path, y el apagado por falta de latidos.
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import datetime, http.server, json, os, shutil, subprocess, threading, time
from harness import abrir_mesa
from playwright.sync_api import sync_playwright

PFX = '/tmp/wine64pfx'
PROG_WIN = r'C:\users\root\AppData\Local\Programs\TA GUIANAEL MFF'
DATOS = os.path.join(PFX, 'drive_c/users/root/AppData/Local/TA GUIANAEL MFF')
RAIZ = RAIZ
fallas = []
def chequear(n, c, d=''):
    print(('OK   ' if c else 'FALLA'), n, '|', d)
    if not c: fallas.append(n)

# origen falso por http (el Python de Windows bajo Wine no confía en el CA del proxy)
PUB = '/tmp/mff-wine-pub'
shutil.rmtree(PUB, ignore_errors=True); os.makedirs(PUB)
m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
m['imagenes'] = [[r, u] for r, u in m['imagenes'] if os.path.exists(os.path.join(RAIZ, r))]
json.dump(m, open(os.path.join(PUB, 'datos.json'), 'w'))
# Desde la 1.0.30 la app consulta los de su formato, en datos/<formato>/ (#1).
os.makedirs(os.path.join(PUB, 'datos', str(m['formato'])))
json.dump(m, open(os.path.join(PUB, 'datos', str(m['formato']), 'datos.json'), 'w'))
v = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))
json.dump({'version': v['version'], 'python': v['python'], 'notas': '', 'formato_datos': v['formato_datos'],
           'parche': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1}, 'instalador': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1}},
          open(os.path.join(PUB, 'latest.json'), 'w'))
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=PUB, **k)
    def log_message(self, *a): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_port}/'

# carpeta de datos limpia, con las imágenes del repo (y un datos.json sin faltantes después de sembrar)
shutil.rmtree(DATOS, ignore_errors=True)
os.makedirs(DATOS)
os.symlink(os.path.join(RAIZ, 'images'), os.path.join(DATOS, 'images'))
# Wine 9 no implementa CopyFile2 (lo usa shutil.copy2 en Python 3.12+; Windows lo tiene desde
# 8): la siembra de datos se hace acá para poder probar el resto.
shutil.copy(os.path.join(RAIZ, 'data.js'), DATOS)
os.makedirs(os.path.join(DATOS, 'docs')); shutil.copy(os.path.join(RAIZ, 'docs', 'AUDITORIA.md'), os.path.join(DATOS, 'docs'))
json.dump(m, open(os.path.join(DATOS, 'datos.json'), 'w'))
# Con una capa guardada (vacía): sin capa, la app abre la bienvenida del recorrido encima de todo (1.0.54).
open(os.path.join(DATOS, 'capa.json'), 'w').write('{}')
# Y con su respaldo del día ya hecho: el de la primera escritura del día es un shutil.copy2 (CopyFile2, como arriba).
os.makedirs(os.path.join(DATOS, 'respaldos'))
open(os.path.join(DATOS, 'respaldos', f'capa-{datetime.date.today().isoformat()}.json'), 'w').write('{}')

# Wine 9.0 (Ubuntu 24.04) se cae al arrancar si está definida TMPDIR (como en desktop/construir.py).
env = dict({k: x for k, x in os.environ.items() if k != 'TMPDIR'}, WINEDEBUG='-all', WINEPREFIX=PFX)
cmd = ['/usr/lib/wine/wine64', PROG_WIN + r'\python\python.exe', PROG_WIN + r'\desktop\lanzador.py',
       '--sin-ventana', '--espera-latido', '12', '--origen-datos', BASE, '--origen-app', BASE + 'latest.json']
p = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors='replace')
url, salida = None, []
fin = time.time() + 90
while time.time() < fin:
    l = p.stdout.readline()
    if not l: break
    salida.append(l.rstrip())
    if 'abriendo' in l:
        url = l.split('abriendo')[1].strip(); break
chequear('arranca con el Python embebido de Windows', url is not None, salida[-3:])
chequear('carpeta de datos por defecto: LOCALAPPDATA', os.path.exists(os.path.join(DATOS, 'instancia.json')))

with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
    pg.on('pageerror', lambda e: errores.append(str(e)))
    pg.goto(url); pg.wait_for_selector('.ccard', timeout=60000)
    chequear('la página carga servida desde Windows', pg.locator('.ccard').count() > 0)
    # un cambio con caracteres fuera de cp1252 en la capa
    # (desde la 1.0.25 los equipos se arman en la mesa: dos personajes de la lista de la ficha y guardar)
    abrir_mesa(pg); pg.locator('main [data-a="open"]').first.click(); pg.wait_for_selector('.plista')
    dos = pg.evaluate("""() => { const ks = [...document.querySelectorAll('.plista [data-a="mesaPoner"]')].map(x => x.dataset.key);
        return [ks[0], ks.find(k => k.split('::')[0] !== ks[0].split('::')[0])]; }""")
    for k in dos: pg.click(f'.plista [data-a="mesaPoner"][data-key="{k}"]'); pg.wait_for_timeout(200)
    pg.fill('[data-a="mesaNombre"]', 'Equipo ★ ↑ ñandú')
    pg.click('[data-a="mesaGuardar"]'); pg.wait_for_timeout(1500)
    capa = json.load(open(os.path.join(DATOS, 'capa.json'), encoding='utf-8'))
    chequear('capa.json en UTF-8 con ★ y ↑', [t['name'] for t in capa['teams']] == ['Equipo ★ ↑ ñandú'], capa['teams'][:1])
    pg.click('[data-a="goSettings"]'); pg.wait_for_timeout(1500)
    sec = pg.evaluate("document.querySelector('#seccion-actualizaciones').innerText")
    chequear('Ajustes: versión, al día y carpeta de datos de Windows', v['version'] in sec and 'estás al día' in sec.lower()
             and 'AppData\\Local\\TA GUIANAEL MFF' in sec, [l for l in sec.splitlines() if 'Carpeta' in l or 'AL DÍA' in l])
    # segunda instancia: reusa (candado con msvcrt)
    p2 = subprocess.run(cmd, env=env, capture_output=True, text=True, errors='replace', timeout=90)
    chequear('segunda instancia reusa la abierta (msvcrt)', url in p2.stdout and p2.returncode == 0, p2.stdout.strip()[-120:])
    chequear('sin errores de página', not errores, errores[:3])
    pg.close(); b.close()
t0 = time.time()
try: p.wait(timeout=40)
except subprocess.TimeoutExpired: pass
chequear('se apaga solo sin ventanas', p.returncode == 0 and not os.path.exists(os.path.join(DATOS, 'instancia.json')), f'{time.time() - t0:.1f} s')
reg = open(os.path.join(DATOS, 'registro.txt'), encoding='utf-8').read()
chequear('registro.txt en la carpeta de datos', 'se apaga' in reg, reg.strip().splitlines()[-1][:120])
srv.shutdown()
print('\nFALLAS:', fallas or 'ninguna')
