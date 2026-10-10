"""Pantalla de rescate (#2, 1.0.31): una página del servidor (/rescate), sin app.js ni data.js, que el lanzador abre si
la página no avisa a tiempo que arrancó o avisa un error. Con una copia del programa como quedaría instalado (sin .git) y
un GitHub local (latest.json y datos/<formato>/):
1. arranque normal: la página avisa que arrancó y no hay rescate;
2. app.js roto: pasado --espera-arranque, el lanzador saca la dirección de /rescate; la pantalla dice por qué, lo
   instalado (versión, formato, datos), que no hay programa anterior, el final de registro.txt, el instalador de la última
   versión y, con una versión nueva con el mismo Python, «Actualizar a la …» (con un parche que no existe: el error a la
   vista); late (el servidor no se apaga con la pantalla abierta); «Volver a bajar los datos» baja los publicados;
3. un error al arrancar (iniciarDatos): el aviso llega enseguida, sin esperar el plazo, con el error;
4. «Volver a la …»: con programa-anterior/ (lo que guardó el último parche) y el programa actual roto, vuelve al anterior,
   se reinicia en el mismo puerto, la pantalla pasa a la app y la app arranca con la versión anterior; el respaldo se
   borra;
5. desde el repo (.git): dice que el programa se cambia con git, sin «Volver» ni «Actualizar»; abierta a mano, «se abrió
   a mano»;
6. inglés (capa en inglés), celular sin desborde y sin errores de página ni de consola;
7. datos locales de otro formato sin los de su formato publicados: la pantalla de datos avisa el error y el rescate
   abre enseguida."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import functools, hashlib, http.server, json, os, shutil, subprocess, sys, tempfile, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import RAIZ, DATOS, Chequeo
from playwright.sync_api import sync_playwright

ok = Chequeo()
V = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))
F = V['formato_datos']
SH = SALIDA
os.makedirs(SH, exist_ok=True)

# ---- GitHub local ----
PUB = tempfile.mkdtemp(prefix='mff-rescate-pub-')
class Silencioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv_pub = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Silencioso, directory=PUB))
threading.Thread(target=srv_pub.serve_forever, daemon=True).start()
BASE = f'http://127.0.0.1:{srv_pub.server_port}/'


def manifiesto(juego=None):
    m = json.load(open(os.path.join(DATOS, 'datos.json'), encoding='utf-8'))
    m['imagenes'] = [[r, u] for r, u in m['imagenes'] if os.path.exists(os.path.join(DATOS, r))]
    if juego: m['juego'] = juego
    return m


def publicar(juego, latest):
    """datos/<F>/ con el data.js de DATOS (otro «juego» en datos.json: la app lo verifica por sha256, no por versión) y
    un latest.json."""
    d = os.path.join(PUB, 'datos', str(F))
    os.makedirs(os.path.join(d, 'docs'), exist_ok=True)
    shutil.copy(os.path.join(DATOS, 'data.js'), d)
    shutil.copy(os.path.join(DATOS, 'docs', 'AUDITORIA.md'), os.path.join(d, 'docs'))
    json.dump(manifiesto(juego), open(os.path.join(d, 'datos.json'), 'w', encoding='utf-8'))
    json.dump(dict({'version': V['version'], 'python': V['python'], 'notas': '', 'formato_datos': F,
                    'parche': {'url': BASE + 'no-existe.zip', 'sha256': '0' * 64, 'bytes': 1},
                    'instalador': {'url': BASE + 'instalador.exe', 'sha256': '0' * 64, 'bytes': 1}}, **latest),
              open(os.path.join(PUB, 'latest.json'), 'w'))


def programa(version=None, romper=None, git=False):
    d = tempfile.mkdtemp(prefix='mff-prog-')
    for f in ('index.html', 'app.js', 'styles.css', 'version.json'):
        shutil.copy(os.path.join(RAIZ, f), d)
    for f in ('data.js', 'datos.json'):
        shutil.copy(os.path.join(DATOS, f), d)
    shutil.copytree(os.path.join(RAIZ, 'desktop'), os.path.join(d, 'desktop'), ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(os.path.join(DATOS, 'docs'), os.path.join(d, 'docs'))
    if version:
        json.dump(dict(V, version=version), open(os.path.join(d, 'version.json'), 'w'))
    if romper == 'sintaxis':
        open(os.path.join(d, 'app.js'), 'a', encoding='utf-8').write('\n)(roto\n')
    if git:
        os.mkdir(os.path.join(d, '.git'))
    return d


def datos(lang='es', romper_valor=False):
    d = tempfile.mkdtemp(prefix='mff-dat-')
    os.symlink(os.path.join(DATOS, 'images'), os.path.join(d, 'images'))
    shutil.copy(os.path.join(DATOS, 'data.js'), d)
    shutil.copytree(os.path.join(DATOS, 'docs'), os.path.join(d, 'docs'))
    json.dump(manifiesto(), open(os.path.join(d, 'datos.json'), 'w', encoding='utf-8'))
    if romper_valor:   # iniciarDatos corta: la tabla de valor no tiene la fila pvp
        open(os.path.join(d, 'data.js'), 'a', encoding='utf-8').write('\nwindow.MFF_VALOR.contextos = {};\n')
    if lang == 'en':
        json.dump({'prefs': {'lang': 'en'}}, open(os.path.join(d, 'capa.json'), 'w'))
    return d


class Lanzador:
    """El lanzador con --sin-ventana: lee su salida en un hilo («abriendo …», «rescate …»)."""
    def __init__(self, prog, dat, espera_arranque, espera_latido=900):
        self.p = subprocess.Popen([sys.executable, os.path.join(prog, 'desktop', 'lanzador.py'), '--datos', dat, '--sin-ventana',
                                   '--espera-arranque', str(espera_arranque), '--espera-latido', str(espera_latido),
                                   '--origen-datos', BASE, '--origen-app', BASE + 'latest.json'],
                                  cwd=prog, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        self.lineas, self.rescate, self.url = [], None, None
        threading.Thread(target=self._leer, daemon=True).start()
        limite = time.monotonic() + 30
        while not self.url:
            if time.monotonic() > limite: raise SystemExit('no arrancó: ' + ''.join(self.lineas))
            time.sleep(0.1)

    def _leer(self):
        for l in self.p.stdout:
            self.lineas.append(l)
            if 'abriendo' in l and not self.url: self.url = l.split('abriendo')[1].strip()
            if l.strip().startswith('rescate '): self.rescate = (l.split(None, 1)[1].strip(), time.monotonic())

    def esperar_rescate(self, s):
        limite = time.monotonic() + s
        while not self.rescate and time.monotonic() < limite: time.sleep(0.2)
        return self.rescate

    def cerrar(self):
        self.p.terminate(); self.p.wait()


errores = []
def pagina(b, ancho=1100, lang=None):
    pg = b.new_page(viewport={'width': ancho, 'height': 900})
    pg.on('pageerror', lambda e: errores.append(str(e)))
    pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
    pg.on('dialog', lambda d: d.accept())
    return pg


def leer(pg):
    pg.wait_for_function("document.querySelector('#publicada') && !/consultando|checking/.test(document.querySelector('#publicada').textContent)")
    return pg.evaluate("""() => { const vis = (s) => { const e = document.querySelector(s); return !!e && !e.closest('[hidden]'); };
      return { h1: document.querySelector('h1').textContent, motivo: document.querySelector('#motivo').textContent,
        version: document.querySelector('#version').textContent, formato: document.querySelector('#formato').textContent,
        datos: document.querySelector('#datos').textContent, anterior: document.querySelector('#anterior').textContent,
        publicada: document.querySelector('#publicada').textContent, registro: document.querySelector('#registro').textContent,
        actualizar: vis('#actualizar') ? document.querySelector('#actualizar button').textContent : null,
        instalador: vis('#instalador') ? [document.querySelector('#instalador a').textContent, document.querySelector('#instalador a').href] : null,
        volver: vis('#volver') ? document.querySelector('#volver button').textContent : null,
        repo: vis('#repo'), aldia: vis('#aldia'), app_js: !!document.querySelector('script[src*="app.js"]') }; }""")


with sync_playwright() as pw:
    b = pw.chromium.launch()

    # 1. arranque normal
    publicar('12.2.6', {})
    L = Lanzador(programa(), datos(), 6)
    pg = pagina(b); pg.goto(L.url); pg.wait_for_selector('.ccard')
    time.sleep(8)
    ok('1 arranque normal: sin rescate', L.rescate is None, L.lineas[-3:])
    pg.close(); L.cerrar()

    # 2. app.js roto
    publicar('12.2.7', {'version': '9.9.10'})
    D = datos()
    L = Lanzador(programa(romper='sintaxis'), D, 6, espera_latido=20)
    t0 = time.monotonic()
    pg = pagina(b); pg.goto(L.url)
    r = L.esperar_rescate(20)
    ok('2 app.js roto: el lanzador saca /rescate pasado el plazo', r and r[0].endswith('/rescate') and 5 <= r[1] - t0 <= 12, (r, r and r[1] - t0))
    errores.clear()   # los de la página rota se esperan
    pg.goto(r[0])
    x = leer(pg)
    ok('2 la pantalla: título, por qué (6 segundos) y sin app.js', x['h1'] == 'Pantalla de rescate'
       and x['motivo'] == 'La app no avisó que arrancó en 6 segundos.' and not x['app_js'], x)
    ok('2 lo instalado: versión, formato, datos, sin programa anterior', x['version'] == V['version'] and x['formato'] == str(F)
       and x['datos'].startswith(manifiesto()['juego'] + ' · ') and x['anterior'].startswith('no hay'), x)
    ok('2 el final de registro.txt', 'no avisó que arrancó' in x['registro'], x['registro'][-300:])
    ok('2 la última versión, el instalador y «Actualizar a la 9.9.10»', x['publicada'] == '9.9.10'
       and x['instalador'] == ['Bajar el instalador de la 9.9.10', BASE + 'instalador.exe'] and x['actualizar'] == 'Actualizar a la 9.9.10'
       and x['volver'] is None and not x['repo'], x)
    pg.screenshot(path=f'{SH}/rescate_1100.png', full_page=True)
    pg.click('#actualizar button')
    pg.wait_for_function("document.querySelector('#aviso').classList.contains('err')", timeout=20000)
    ok('2 «Actualizar» con un parche que no está: el error a la vista', 'no-existe.zip' in pg.locator('#aviso').inner_text(), pg.locator('#aviso').inner_text())
    time.sleep(26)
    ok('2 la pantalla late: el servidor sigue después de --espera-latido', L.p.poll() is None and pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.ok)"))
    pg.click('#datosbajar button')
    pg.wait_for_function("/Datos bajados/.test(document.querySelector('#aviso').textContent)", timeout=30000)
    ok('2 «Volver a bajar los datos»: baja los publicados', json.load(open(os.path.join(D, 'datos.json')))['juego'] == '12.2.7')
    pg.set_viewport_size({'width': 360, 'height': 800})
    ancho = pg.evaluate("[document.documentElement.scrollWidth, innerWidth]")
    ok('6 celular: sin desborde', ancho[0] <= ancho[1], ancho)
    pg.screenshot(path=f'{SH}/rescate_360.png', full_page=True)
    pg.close(); L.cerrar()

    # 3. error al arrancar
    publicar('12.2.7', {})
    L = Lanzador(programa(), datos(romper_valor=True), 60)
    t0 = time.monotonic()
    pg = pagina(b); pg.goto(L.url)
    r = L.esperar_rescate(20)
    ok('3 error al arrancar: rescate enseguida', r and r[1] - t0 < 15, r and r[1] - t0)
    ok('3 la página muestra el error', 'La app no pudo arrancar' in pg.locator('.fatal h1').inner_text())
    errores.clear()
    pg.goto(r[0]); x = leer(pg)
    ok('3 la pantalla dice el error', x['motivo'].startswith('La app avisó este error al arrancar:\nLa app no pudo arrancar: ')
       and 'MFF_VALOR' in x['motivo'] and x['aldia'], x)
    pg.close(); L.cerrar()

    # 4. volver al programa anterior
    P = programa(version='9.9.9', romper='sintaxis')
    D = datos()
    anterior = os.path.join(D, 'programa-anterior')
    os.makedirs(os.path.join(anterior, 'desktop'))
    for f in ('app.js', 'version.json'):
        shutil.copy(os.path.join(RAIZ, f), anterior)
    shutil.copy(os.path.join(RAIZ, 'desktop', 'servidor.py'), os.path.join(anterior, 'desktop'))
    publicar('12.2.7', {'version': '9.9.9'})
    L = Lanzador(P, D, 5)
    r = L.esperar_rescate(20)
    errores.clear()
    pg = pagina(b); pg.goto(r[0]); x = leer(pg)
    ok('4 con programa anterior: «Volver a la …»', x['anterior'] == V['version'] and x['volver'] == f"Volver a la {V['version']}"
       and x['actualizar'] is None and x['aldia'], x)
    pg.click('#volver button')
    pg.wait_for_url('**/index.html', timeout=40000)
    pg.wait_for_selector('.ccard', timeout=40000)
    est = pg.evaluate("fetch('/api/estado', {headers: {'X-MFF': '1'}}).then(r => r.json())")
    ok('4 se reinicia con la versión anterior, la app arranca', est['version'] == V['version'] and pg.url.startswith(L.url.rsplit('/', 1)[0]), est['version'])
    ok('4 el programa anterior en su lugar y el respaldo borrado', open(os.path.join(P, 'app.js'), 'rb').read() == open(os.path.join(RAIZ, 'app.js'), 'rb').read()
       and not os.path.exists(anterior))
    pg.close(); L.p.wait(5) if L.p.poll() is None else None
    subprocess.run(['pkill', '-f', P], check=False)

    # 5. desde el repo, abierta a mano
    L = Lanzador(programa(git=True), datos(), 60)
    pg = pagina(b); pg.goto(L.url); pg.wait_for_selector('.ccard')
    pg.goto(L.url.replace('/index.html', '/rescate')); x = leer(pg)
    ok('5 desde el repo: el programa con git, sin «Volver» ni «Actualizar»; abierta a mano', x['repo'] and x['volver'] is None
       and x['actualizar'] is None and x['motivo'].startswith('Se abrió a mano'), x)
    pg.close(); L.cerrar()

    # 7. datos locales de otro formato y ninguno publicado del suyo: la pantalla de datos avisa el error enseguida
    shutil.rmtree(os.path.join(PUB, 'datos'))
    D = datos()
    js = open(os.path.join(D, 'data.js'), encoding='utf-8').read()
    open(os.path.join(D, 'data.js'), 'w', encoding='utf-8').write(js.replace(f'"formato": {F}}}', f'"formato": {F - 1}}}', 1))
    L = Lanzador(programa(), D, 60)
    t0 = time.monotonic()
    pg = pagina(b); pg.goto(L.url)
    r = L.esperar_rescate(20)
    errores.clear()
    ok('7 datos de otro formato sin los del suyo publicados: rescate enseguida', r and r[1] - t0 < 15, r and r[1] - t0)
    pg.goto(r[0]); x = leer(pg)
    ok('7 la pantalla dice el error de la pantalla de datos', f'todavía no hay datos publicados de formato {F}' in x['motivo'], x['motivo'])
    pg.close(); L.cerrar()

    # 6. inglés
    L = Lanzador(programa(romper='sintaxis'), datos('en'), 5)
    r = L.esperar_rescate(20)
    errores.clear()
    pg = pagina(b); pg.goto(r[0]); x = leer(pg)
    ok('6 inglés', x['h1'] == 'Rescue screen' and x['motivo'] == 'The app did not report that it started within 5 seconds.'
       and x['instalador'][0].startswith('Download the') and x['datos'].endswith(f' · format {F}'), x)
    pg.close(); L.cerrar()
    b.close()
ok('sin errores de página ni de consola (en la pantalla de rescate)', not errores, errores[:3])
srv_pub.shutdown()
ok.fin()
