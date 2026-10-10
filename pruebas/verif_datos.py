"""Datos del juego desde "GitHub" (un servidor local que hace de origen).

1  al día: no baja nada y Ajustes lo dice
2  datos nuevos: se bajan solos con avance, "Usar ahora" recarga y quedan en uso
3  hash que no coincide: error a la vista, los archivos locales no cambian
4  se publica un formato más nuevo (en su carpeta y en la raíz): la app sigue con los de su formato,
   datos/<formato>/, sin aviso (#1)
8  sin carpeta para su formato (404): aviso que lo dice
5  sin conexión: aviso ocultable
6  datos locales de otro formato: pantalla que baja los publicados y arranca
7  manifiesto que apunta fuera de lo que la app usa: error, no escribe nada

Los datos salen de harness.DATOS (el repo, o MFF_DATOS mientras el data.js del repo sea de un
formato anterior al de version.json: armar_datos_prueba.py); el formato, de version.json.
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import functools, hashlib, http.server, json, os, re, shutil, subprocess, sys, tempfile, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import RAIZ, DATOS
from playwright.sync_api import sync_playwright

fallas = []
def chequear(nombre, cond, detalle=''):
    print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
    if not cond: fallas.append(nombre)

# ---- origen falso ----
ORIGEN = tempfile.mkdtemp(prefix='mff-origen-')
class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv_origen = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Silencioso, directory=ORIGEN))
threading.Thread(target=srv_origen.serve_forever, daemon=True).start()
URL_ORIGEN = f'http://127.0.0.1:{srv_origen.server_port}/'
# La release publicada es la misma versión que la instalada: estas pruebas son de datos.
_v = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))
FORMATO = _v['formato_datos']
json.dump({'version': _v['version'], 'python': _v['python'], 'notas': '', 'formato_datos': _v['formato_datos'],
           'parche': {'url': URL_ORIGEN + 'x.zip', 'sha256': '0' * 64, 'bytes': 1},
           'instalador': {'url': URL_ORIGEN + 'x.exe', 'sha256': '0' * 64, 'bytes': 1}},
          open(os.path.join(ORIGEN, 'latest.json'), 'w'))

def manifiesto_repo():
    """datos.json de DATOS con solo las imágenes que hay en DATOS: así las pruebas de datos
    no disparan descargas de imágenes a thanosvibs."""
    m = json.load(open(os.path.join(DATOS, 'datos.json'), encoding='utf-8'))
    m['imagenes'] = [[r, u] for r, u in m['imagenes'] if os.path.exists(os.path.join(DATOS, r))]
    return m

def publicar(juego, formato=FORMATO, romper_hash=False, archivos_extra=None):
    """Arma en ORIGEN/datos/<formato>/ un data.js con otra versión y su datos.json, y lo copia a la raíz, como el
    workflow de datos (#1: la app baja de la carpeta de su formato; la raíz la leen las versiones hasta la 1.0.29)."""
    dest = os.path.join(ORIGEN, 'datos', str(formato))
    base = open(os.path.join(DATOS, 'data.js'), encoding='utf-8').read()
    nuevo = re.sub(r'window\.MFF_VERSION = \{[^}]*\};',
                   f'window.MFF_VERSION = {{"juego": "{juego}", "generado": "2026-10-05", "formato": {formato}}};', base, count=1)
    os.makedirs(os.path.join(dest, 'docs'), exist_ok=True)
    open(os.path.join(dest, 'data.js'), 'w', encoding='utf-8', newline='\n').write(nuevo)
    shutil.copy(os.path.join(DATOS, 'docs', 'AUDITORIA.md'), os.path.join(dest, 'docs', 'AUDITORIA.md'))
    def huella(rel):
        b = open(os.path.join(dest, rel), 'rb').read()
        return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    archivos = {r: huella(r) for r in ('data.js', 'docs/AUDITORIA.md')}
    if romper_hash:
        archivos['data.js']['sha256'] = '0' * 64
    archivos.update(archivos_extra or {})
    m = manifiesto_repo()
    m.update(formato=formato, juego=juego, generado='2026-10-05', archivos=archivos)
    json.dump(m, open(os.path.join(dest, 'datos.json'), 'w', encoding='utf-8'))
    raiz_igual(dest)

def raiz_igual(dest):
    for rel in ('data.js', 'datos.json', 'docs/AUDITORIA.md'):
        os.makedirs(os.path.dirname(os.path.join(ORIGEN, rel)), exist_ok=True)
        shutil.copy(os.path.join(dest, rel), os.path.join(ORIGEN, rel))

def publicar_igual():
    dest = os.path.join(ORIGEN, 'datos', str(FORMATO))
    os.makedirs(os.path.join(dest, 'docs'), exist_ok=True)
    shutil.copy(os.path.join(DATOS, 'data.js'), dest)
    shutil.copy(os.path.join(DATOS, 'docs', 'AUDITORIA.md'), os.path.join(dest, 'docs'))
    json.dump(manifiesto_repo(), open(os.path.join(dest, 'datos.json'), 'w', encoding='utf-8'))
    raiz_igual(dest)

def carpeta_datos():
    d = tempfile.mkdtemp(prefix='mff-datos-')
    os.symlink(os.path.join(DATOS, 'images'), os.path.join(d, 'images'))
    shutil.copy(os.path.join(DATOS, 'data.js'), d)
    json.dump(manifiesto_repo(), open(os.path.join(d, 'datos.json'), 'w', encoding='utf-8'))
    return d

def lanzar(datos, origen=None):
    p = subprocess.Popen([sys.executable, 'desktop/lanzador.py', '--datos', datos, '--sin-ventana',
                          '--origen-datos', origen or URL_ORIGEN, '--origen-app', URL_ORIGEN + 'latest.json'], cwd=RAIZ,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    while True:
        linea = p.stdout.readline()
        if not linea: raise SystemExit('no arrancó')
        if 'abriendo' in linea: return p, linea.split('abriendo')[1].strip()

def texto_avisos(page):
    return page.evaluate("(document.querySelector('#avisos') || {}).innerText || ''")

def juego_local(d):
    return json.load(open(os.path.join(d, 'datos.json'), encoding='utf-8'))['juego']

with sync_playwright() as pw:
    b = pw.chromium.launch()
    errores = []
    def pagina():
        pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        return pg

    # 1: al día
    publicar_igual()
    D = carpeta_datos(); p, url = lanzar(D)
    page = pagina(); page.goto(url); page.wait_for_selector('.ccard'); page.wait_for_timeout(1500)
    page.click('[data-a="goSettings"]'); page.wait_for_timeout(300)
    sec = page.evaluate("document.querySelector('#seccion-actualizaciones').innerText")
    chequear('1 al día: sin avisos y Ajustes lo dice', texto_avisos(page).strip() == '' and 'estás al día' in sec.lower(), sec[-200:].replace('\n', ' | '))
    page.close(); p.terminate(); p.wait()

    # 2: datos nuevos
    publicar('12.2.6')
    p, url = lanzar(D)
    page = pagina(); page.goto(url); page.wait_for_selector('.ccard')
    visto_bajando = False
    for _ in range(40):
        a = texto_avisos(page)
        if 'Bajando datos nuevos' in a: visto_bajando = True
        if 'actualizados' in a: break
        page.wait_for_timeout(150)
    a = texto_avisos(page)
    chequear('2 baja solo y avisa que terminó', 'Datos del juego actualizados 12.2.6' in a, (visto_bajando, a[:120]))
    chequear('2 archivos reemplazados', juego_local(D) == '12.2.6' and '"juego": "12.2.6"' in open(os.path.join(D, 'data.js'), encoding='utf-8').read(3000))
    page.click('[data-a="goSettings"]'); page.wait_for_timeout(200)
    page.click('[data-a="usarDatos"]'); page.wait_for_selector('#seccion-actualizaciones'); page.wait_for_timeout(1500)
    sec = page.evaluate("document.querySelector('#seccion-actualizaciones').innerText")
    chequear('2 "Usar ahora" recarga, vuelve a Ajustes y está al día', '12.2.6' in sec and 'estás al día' in sec.lower(), sec[-220:].replace('\n', ' | '))
    chequear('2 la página usa los datos nuevos', page.evaluate("window.MFF_VERSION.juego") == '12.2.6')
    page.close(); p.terminate(); p.wait()

    # 3: hash que no coincide
    publicar('12.2.7', romper_hash=True)
    antes = open(os.path.join(D, 'data.js'), 'rb').read()
    p, url = lanzar(D)
    page = pagina(); page.goto(url); page.wait_for_selector('.ccard')
    for _ in range(40):
        if 'No se pudieron bajar' in texto_avisos(page): break
        page.wait_for_timeout(150)
    a = texto_avisos(page)
    chequear('3 hash distinto: error a la vista', 'llegó distinto' in a, a[:160])
    chequear('3 hash distinto: nada cambió en disco', open(os.path.join(D, 'data.js'), 'rb').read() == antes and juego_local(D) == '12.2.6'
             and not [f for f in os.listdir(D) if f.endswith('.nuevo')])
    page.close(); p.terminate(); p.wait()

    # 7: manifiesto que apunta afuera
    publicar('12.2.8', archivos_extra={'../fuera.js': {'sha256': '0' * 64, 'bytes': 1}})
    p, url = lanzar(D)
    page = pagina(); page.goto(url); page.wait_for_selector('.ccard')
    for _ in range(40):
        if 'No se pudieron bajar' in texto_avisos(page): break
        page.wait_for_timeout(150)
    a = texto_avisos(page)
    chequear('7 ruta ajena en el manifiesto: error y no escribe', 'no usa' in a and juego_local(D) == '12.2.6'
             and not os.path.exists(os.path.join(os.path.dirname(D), 'fuera.js')), a[:140])
    page.close(); p.terminate(); p.wait()

    # 4: se publica un formato más nuevo; la carpeta del de la app tiene los mismos datos que ya tiene (12.2.6)
    publicar('12.2.6')
    publicar('13.0.0', formato=FORMATO + 1)
    chequear('4 la raíz publica el formato nuevo', json.load(open(os.path.join(ORIGEN, 'datos.json')))['formato'] == FORMATO + 1)
    p, url = lanzar(D)
    page = pagina(); page.goto(url); page.wait_for_selector('.ccard'); page.wait_for_timeout(1500)
    a = texto_avisos(page)
    page.click('[data-a="goSettings"]'); page.wait_for_timeout(300)
    sec = page.evaluate("document.querySelector('#seccion-actualizaciones').innerText")
    chequear('4 formato nuevo publicado: sigue con los de su formato, al día y sin aviso', a.strip() == '' and juego_local(D) == '12.2.6'
             and 'estás al día' in sec.lower(), (a[:140], sec[-160:].replace('\n', ' | ')))
    page.close(); p.terminate(); p.wait()

    # 8: sin carpeta para su formato
    shutil.rmtree(os.path.join(ORIGEN, 'datos', str(FORMATO)))
    p, url = lanzar(D)
    page = pagina(); page.goto(url); page.wait_for_selector('.ccard'); page.wait_for_timeout(1500)
    a = texto_avisos(page)
    chequear('8 sin carpeta de su formato: lo dice', f'todavía no hay datos publicados de formato {FORMATO}' in a and juego_local(D) == '12.2.6', a[:200])
    page.close(); p.terminate(); p.wait()

    # 5: sin conexión
    p, url = lanzar(D, origen='http://127.0.0.1:9/')
    page = pagina(); page.goto(url); page.wait_for_selector('.ccard'); page.wait_for_timeout(1500)
    a = texto_avisos(page)
    chequear('5 sin conexión: aviso', 'No se pudo buscar actualizaciones' in a, a[:140])
    page.click('[data-a="ocultarAviso"]'); page.wait_for_timeout(200)
    chequear('5 el aviso se oculta', texto_avisos(page).strip() == '')
    page.screenshot(path=f'{SALIDA}/datos_sin_conexion.png')
    page.close(); p.terminate(); p.wait()

    # 6: datos locales de otro formato
    publicar('12.2.9')
    local = open(os.path.join(D, 'data.js'), encoding='utf-8').read()
    otro = local.replace(f'"formato": {FORMATO}}}', f'"formato": {FORMATO - 1}}}', 1)
    assert otro != local
    open(os.path.join(D, 'data.js'), 'w', encoding='utf-8').write(otro)
    p, url = lanzar(D)
    page = pagina(); page.goto(url)
    page.wait_for_selector('.fatal')
    titulo = page.evaluate("document.querySelector('.fatal h1').innerText")
    page.wait_for_selector('.ccard', timeout=20000)
    chequear('6 otro formato local: baja los publicados y arranca', 'ACTUALIZANDO' in titulo.upper() and page.evaluate("window.MFF_VERSION.juego") == '12.2.9', titulo)
    page.close(); p.terminate(); p.wait()
    chequear('sin errores de página', not errores, errores[:3])
    b.close()
srv_origen.shutdown()
print('\nFALLAS:', fallas or 'ninguna')
