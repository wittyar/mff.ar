#!/usr/bin/env python3
"""Servidor local de TA GUIANAEL MFF.

Por que hace falta: la API de thanosvibs no manda Access-Control-Allow-Origin, asi
que el navegador bloquea sus llamadas desde la pagina. La sincronizacion tiene que
correr fuera del sandbox, y este proceso es ese afuera: sirve la app en 127.0.0.1 y
expone los botones de Ajustes como endpoints que ejecutan el pipeline de siempre.

Solo biblioteca estandar, para que corra con el Python embebido que viaja en la carpeta.
"""
import json, os, re, socket, subprocess, sys, threading, urllib.request, webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from version_juego import ultima
PY = sys.executable
PUERTO_PREFERIDO = 8731
UA = {'User-Agent': 'Mozilla/5.0 (mff-comparador; uso personal)'}

# Cada boton de Ajustes es una secuencia de comandos. build.py se corre despues de
# cualquier cambio de datos porque es el que regenera data.js.
TAREAS = {
    'datos':     [[PY, 'scripts/fetch_all.py', '--datos'],
                  [PY, 'scripts/parse_instinto.py'],
                  [PY, 'scripts/build.py']],
    'tierlists': [[PY, 'scripts/fetch_all.py', '--tierlists'],
                  [PY, 'scripts/build.py']],
    'imagenes':  [[PY, 'scripts/fetch_all.py', '--imagenes']],
}

class Trabajo:
    """Una sincronizacion en curso. Solo puede haber una a la vez."""
    def __init__(self):
        self.lock = threading.Lock()
        self.que = None
        self.lineas = []
        self.error = None
        self.terminado = False
        self.corriendo = False

    def estado(self):
        with self.lock:
            return {'corriendo': self.corriendo, 'que': self.que, 'lineas': self.lineas[-200:],
                    'error': self.error, 'terminado': self.terminado}

    def arrancar(self, que):
        with self.lock:
            if self.corriendo:
                return False
            self.que, self.lineas, self.error, self.terminado, self.corriendo = que, [], None, False, True
        threading.Thread(target=self._correr, args=(que,), daemon=True).start()
        return True

    def _log(self, txt):
        with self.lock:
            self.lineas.append(txt)

    def _correr(self, que):
        try:
            for cmd in TAREAS[que]:
                self._log('$ ' + ' '.join(os.path.basename(c) for c in cmd))
                p = subprocess.Popen(cmd, cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     text=True, encoding='utf-8', errors='replace', bufsize=1)
                for linea in p.stdout:
                    self._log(linea.rstrip())
                if p.wait() != 0:
                    raise RuntimeError(f'{os.path.basename(cmd[1])} termino con codigo {p.returncode}')
            self._log('Listo.')
        except Exception as e:
            with self.lock:
                self.error = str(e)
            self._log('ERROR: ' + str(e))
        finally:
            with self.lock:
                self.corriendo, self.terminado = False, True

TRABAJO = Trabajo()
REMOTA = {'juego': None, 'error': None}

# 'tierlists' regenera data.js, y para eso el build necesita los insumos que deja la
# sincronizacion de datos. En un paquete recien descomprimido no estan.
INSUMOS = ('work/characters.json', 'work/instintos.json', 'work/uniforms.json', 'work/updates.json',
           'work/ctps.json', 'work/artifacts.json', 'work/abxl.json', 'work/supports.json',
           'work/rotations.json', 'work/guia/changelog.json', 'work/guia/parte1.txt', 'work/guia/parte2.txt')
def pipeline_listo():
    if any(not os.path.exists(os.path.join(RAIZ, f)) for f in INSUMOS):
        return False
    d = os.path.join(RAIZ, 'work', 'skills_api')
    return os.path.isdir(d) and bool(os.listdir(d))

def version_local():
    """Lee window.MFF_VERSION del data.js que hay en disco."""
    try:
        with open(os.path.join(RAIZ, 'data.js'), encoding='utf-8') as f:
            cabecera = f.read(4000)
        m = re.search(r'window\.MFF_VERSION\s*=\s*(\{.*?\});', cabecera, re.S)
        return json.loads(m.group(1)) if m else {}
    except Exception:
        return {}

def consultar_version_remota():
    """La version de juego que publica thanosvibs, para avisar si hay una mas nueva.
    Sale de /api/updates con la misma regla que usa build.py (version_juego.py)."""
    try:
        req = urllib.request.Request('https://thanosvibs.money/api/updates', headers=UA)
        REMOTA['juego'] = ultima(json.loads(urllib.request.urlopen(req, timeout=25).read()))[1]
    except Exception as e:
        REMOTA['error'] = str(e)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=RAIZ, **kw)

    def log_message(self, *a):
        pass  # la consola es para el progreso de la sincronizacion, no para cada GET

    # --- proteccion minima: solo se aceptan llamadas de la propia app ---
    def _propio(self):
        # Una pagina de otro sitio no puede mandar esta cabecera sin un preflight,
        # y este servidor no responde CORS, asi que el preflight falla.
        if self.headers.get('X-MFF') != '1':
            return False
        origen = self.headers.get('Origin')
        return not origen or origen.startswith('http://127.0.0.1:') or origen.startswith('http://localhost:')

    def _json(self, datos, codigo=200):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode('utf-8')
        self.send_response(codigo)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(cuerpo)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(cuerpo)

    def end_headers(self):
        # data.js cambia con cada sincronizacion: no puede quedar cacheado.
        if self.path.startswith('/data.js'):
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/api/'):
            if not self._propio():
                return self._json({'error': 'origen no permitido'}, 403)
            if self.path.startswith('/api/estado'):
                return self._json({'app': 'mff-escritorio', 'local': version_local(), 'remota': REMOTA,
                                   'listo': pipeline_listo(), 'trabajo': TRABAJO.estado()})
            if self.path.startswith('/api/progreso'):
                return self._json(TRABAJO.estado())
            return self._json({'error': 'no existe'}, 404)
        return super().do_GET()

    def do_POST(self):
        if not self.path.startswith('/api/'):
            return self._json({'error': 'no existe'}, 404)
        if not self._propio():
            return self._json({'error': 'origen no permitido'}, 403)
        m = re.match(r'/api/sync/(datos|tierlists|imagenes)', self.path)
        if not m:
            return self._json({'error': 'no existe'}, 404)
        que = m.group(1)
        if que == 'tierlists' and not pipeline_listo():
            return self._json({'error': 'sin-datos'}, 409)
        if not TRABAJO.arrancar(que):
            return self._json({'error': 'ya hay una sincronizacion en curso'}, 409)
        return self._json(TRABAJO.estado())

def puerto_libre(preferido):
    for p in [preferido] + list(range(preferido + 1, preferido + 20)):
        with socket.socket() as s:
            try:
                s.bind(('127.0.0.1', p)); return p
            except OSError:
                continue
    return 0  # que elija el sistema

def main():
    faltan = [f for f in ('index.html', 'app.js', 'styles.css', 'data.js') if not os.path.exists(os.path.join(RAIZ, f))]
    if faltan:
        print('ERROR: faltan archivos de la app en', RAIZ, '->', ', '.join(faltan))
        input('Enter para cerrar...')
        return 1
    threading.Thread(target=consultar_version_remota, daemon=True).start()
    puerto = puerto_libre(PUERTO_PREFERIDO)
    servidor = ThreadingHTTPServer(('127.0.0.1', puerto), Handler)
    url = f'http://127.0.0.1:{servidor.server_port}/index.html'
    v = version_local()
    print('TA GUIANAEL MFF')
    print(f'  datos locales: juego {v.get("juego", "?")} (snapshot {v.get("generado", "?")})')
    print(f'  abriendo {url}')
    print('  cerra esta ventana para apagar la app.')
    if '--no-abrir' not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print('\nApagando.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
