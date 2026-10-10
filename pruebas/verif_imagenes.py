"""Retratos e íconos que faltan: se bajan solos al abrir.

1  carpeta sin imágenes: arranca la descarga sola, con avance a la vista
2  al terminar, las que no publica la fuente (404) no son error; Ajustes las cuenta
3  los retratos visibles aparecen sin redibujar (se re-piden los rotos)
4  una imagen que falla por otra cosa (500): aviso con reintento; al reintentar se completa
5  lo que llega y no es PNG no se guarda
6  datos.json con una ruta de imagen inválida: aviso, la app arranca igual
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import http.server, json, os, shutil, subprocess, sys, tempfile, threading
from playwright.sync_api import sync_playwright

RAIZ = RAIZ
fallas = []
def chequear(nombre, cond, detalle=''):
    print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
    if not cond: fallas.append(nombre)

MAPA = {'portraits': '', 'items': 'items/', 'attributes': 'icons/'}
ROTAS = set()          # rutas de origen que responden 500
LENTAS = set()         # con algo adentro, cada imagen tarda medio segundo
NO_PNG = set()         # rutas de origen que responden algo que no es PNG
class Origen(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        ruta = self.path.split('?')[0]
        # Desde la 1.0.30 la app baja los de su formato, de datos/<formato>/ (#1).
        pre = f"/datos/{m['formato']}"
        if ruta.startswith(pre + '/') and ruta[len(pre):] in ('/datos.json', '/data.js', '/docs/AUDITORIA.md'):
            archivo = os.path.join(ORIGEN_DATOS, ruta[len(pre) + 1:])
        elif ruta.startswith('/images/'):
            _, _, carpeta, nombre = ruta.split('/', 3)
            if ruta in ROTAS: return self.send_error(500)
            if LENTAS: __import__('time').sleep(0.5)
            if ruta in NO_PNG:
                self.send_response(200); self.end_headers(); return self.wfile.write(b'<html>no</html>')
            archivo = os.path.join(RAIZ, 'images', MAPA.get(carpeta, '??/') + nombre)
        else:
            return self.send_error(404)
        if not os.path.exists(archivo): return self.send_error(404)
        cuerpo = open(archivo, 'rb').read()
        self.send_response(200); self.send_header('Content-Length', str(len(cuerpo))); self.end_headers()
        self.wfile.write(cuerpo)

srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Origen)
threading.Thread(target=srv.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv.server_port}'

# datos.json con las URLs de las imágenes apuntando al origen falso
ORIGEN_DATOS = tempfile.mkdtemp(prefix='mff-od-')
m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
m['imagenes'] = [[r, u.replace('https://thanosvibs.money', BASE)] for r, u in m['imagenes']]
json.dump(m, open(os.path.join(ORIGEN_DATOS, 'datos.json'), 'w', encoding='utf-8'))
shutil.copy(os.path.join(RAIZ, 'data.js'), ORIGEN_DATOS)
os.makedirs(os.path.join(ORIGEN_DATOS, 'docs'))
shutil.copy(os.path.join(RAIZ, 'docs', 'AUDITORIA.md'), os.path.join(ORIGEN_DATOS, 'docs'))

def carpeta():
    d = tempfile.mkdtemp(prefix='mff-img-')
    for f in ('data.js',):
        shutil.copy(os.path.join(RAIZ, f), d)
    shutil.copy(os.path.join(ORIGEN_DATOS, 'datos.json'), d)
    os.makedirs(os.path.join(d, 'docs')); shutil.copy(os.path.join(RAIZ, 'docs', 'AUDITORIA.md'), os.path.join(d, 'docs'))
    return d

def lanzar(d):
    p = subprocess.Popen([sys.executable, 'desktop/lanzador.py', '--datos', d, '--sin-ventana', '--origen-datos', BASE + '/'],
                         cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    while True:
        l = p.stdout.readline()
        if not l: raise SystemExit('no arrancó')
        if 'abriendo' in l: return p, l.split('abriendo')[1].strip()

def avisos(pg): return pg.evaluate("(document.querySelector('#avisos') || {}).innerText || ''")
def esperar_fin(pg, n=200):
    visto = False
    for _ in range(n):
        a = avisos(pg)
        if 'Bajando retratos' in a: visto = True
        elif visto or pg.evaluate("!document.querySelector('#avisos .barra')"):
            if 'Bajando retratos' not in a: break
        pg.wait_for_timeout(150)
    return visto

esperados = len(m['imagenes'])
en_repo = sum(1 for r, _ in m['imagenes'] if os.path.exists(os.path.join(RAIZ, r)))
with sync_playwright() as pw:
    b = pw.chromium.launch()
    errores = []
    D = carpeta(); p, url = lanzar(D)
    page = b.new_page(viewport={'width': 1300, 'height': 900})
    page.on('pageerror', lambda e: errores.append(str(e)))
    page.goto(url); page.wait_for_selector('.ccard')
    visto = esperar_fin(page)
    page.wait_for_timeout(1500)
    en_disco = sum(1 for r, _ in m['imagenes'] if os.path.exists(os.path.join(D, r)))
    chequear('1 arranca sola y muestra el avance', visto)
    chequear('2 bajó todas las publicadas; los 404 no son error', en_disco == en_repo and 'Faltan imágenes' not in avisos(page),
             f'{en_disco} en disco, {en_repo} publicadas, {esperados} en la lista')
    rotas_visibles = page.evaluate("[...document.querySelectorAll('.ccard img')].filter(i => i.getBoundingClientRect().top < innerHeight && i.complete && i.naturalWidth === 0).length")
    chequear('3 los retratos visibles aparecen sin redibujar', rotas_visibles == 0, rotas_visibles)
    page.click('[data-a="goSettings"]'); page.wait_for_timeout(300)
    sec = page.evaluate("document.querySelector('#seccion-actualizaciones').innerText")
    chequear('2 Ajustes cuenta las no publicadas', f'faltan {esperados - en_repo} de {esperados}' in sec and 'no están publicados' in sec,
             [l for l in sec.splitlines() if 'Retratos' in l or 'RETRATOS' in l])
    page.close(); p.terminate(); p.wait()

    # 4 y 5: una rota (500) y una que no es PNG
    D2 = carpeta()
    publicadas = [(r, u) for r, u in m['imagenes'] if os.path.exists(os.path.join(RAIZ, r))]
    rota, no_png = publicadas[0], publicadas[1]
    ROTAS.add(rota[1].replace(BASE, '')); NO_PNG.add(no_png[1].replace(BASE, ''))
    p, url = lanzar(D2)
    page = b.new_page(viewport={'width': 1300, 'height': 900}); page.goto(url); page.wait_for_selector('.ccard')
    esperar_fin(page); page.wait_for_timeout(1000)
    a = avisos(page)
    chequear('4 una imagen con error 500: aviso con reintento', 'Faltan imágenes' in a and '2 imágenes no se pudieron bajar' in a, a[:160])
    chequear('5 lo que no es PNG no se guarda', not os.path.exists(os.path.join(D2, no_png[0])))
    ROTAS.clear(); NO_PNG.clear()
    page.click('[data-a="reintentarImagenes"]'); page.wait_for_timeout(2500)
    chequear('4 reintentar completa las que faltaban', os.path.exists(os.path.join(D2, rota[0])) and os.path.exists(os.path.join(D2, no_png[0]))
             and 'Faltan imágenes' not in avisos(page), avisos(page)[:120])
    page.close(); p.terminate(); p.wait()

    # 6: ruta inválida en la lista
    D3 = carpeta()
    m3 = json.load(open(os.path.join(D3, 'datos.json'), encoding='utf-8'))
    m3['imagenes'].append(['images/../../fuera.png', BASE + '/images/portraits/x.png'])
    json.dump(m3, open(os.path.join(D3, 'datos.json'), 'w', encoding='utf-8'))
    json.dump(m3, open(os.path.join(ORIGEN_DATOS, 'datos.json'), 'w', encoding='utf-8'))  # que no se "actualice" solo
    p, url = lanzar(D3)
    page = b.new_page(viewport={'width': 1300, 'height': 900}); page.goto(url); page.wait_for_selector('.ccard'); page.wait_for_timeout(800)
    a = avisos(page)
    chequear('6 lista inválida: aviso y la app arranca', 'imagen inválida' in a and page.locator('.ccard').count() > 0, a[:140])
    page.close(); p.terminate(); p.wait()
    # 7: cerrar la ventana con la descarga de imágenes a mitad de camino no deja la app andando
    LENTAS.add(True)
    D4 = carpeta()
    json.dump(m, open(os.path.join(D4, 'datos.json'), 'w', encoding='utf-8'))
    json.dump(m, open(os.path.join(ORIGEN_DATOS, 'datos.json'), 'w', encoding='utf-8'))
    p = subprocess.Popen([sys.executable, 'desktop/lanzador.py', '--datos', D4, '--sin-ventana', '--origen-datos', BASE + '/',
                          '--espera-latido', '4'], cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    while True:
        l = p.stdout.readline()
        if 'abriendo' in l: url = l.split('abriendo')[1].strip(); break
    page = b.new_page(); page.goto(url); page.wait_for_selector('.ccard'); page.wait_for_timeout(1500)
    corriendo = 'Bajando retratos' in avisos(page)
    page.close()
    import time as _t; t0 = _t.time()
    try: p.wait(timeout=25)
    except subprocess.TimeoutExpired: pass
    bajadas = sum(1 for r, _ in m['imagenes'] if os.path.exists(os.path.join(D4, r)))
    reg = open(os.path.join(D4, 'registro.txt'), encoding='utf-8').read()
    chequear('7 cerrar a mitad de la descarga de imágenes: se apaga igual', corriendo and p.returncode == 0
             and bajadas < en_repo and 'se corta la descarga de imágenes' in reg, f'{_t.time() - t0:.1f} s, {bajadas} bajadas')
    LENTAS.clear()
    chequear('sin errores de página', not errores, errores[:3])
    b.close()
srv.shutdown()
print('\nFALLAS:', fallas or 'ninguna')
