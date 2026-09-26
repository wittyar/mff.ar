#!/usr/bin/env python3
"""Servidor local de TA GUIANAEL MFF.

Por que hace falta: la API de thanosvibs no manda Access-Control-Allow-Origin, asi
que el navegador bloquea sus llamadas desde la pagina. La sincronizacion tiene que
correr fuera del sandbox, y este proceso es ese afuera: sirve la app en 127.0.0.1 y
expone los botones de Ajustes como endpoints que ejecutan el pipeline de siempre.

Programa y datos van en carpetas distintas. De la carpeta del programa (la del repo)
salen index.html, app.js y styles.css; de la carpeta de datos (--datos), data.js,
docs/ e images/, y ahi escribe el pipeline. Fuera de esas rutas no se sirve nada.

La capa del usuario (listas, equipos, rutas, topes, ediciones) vive en capa.json, en
la carpeta de datos: la pagina la pide con GET /api/capa y la guarda con PUT. Antes
de la primera escritura de cada dia se copia la anterior a respaldos/ (quedan 7).

Uso: python desktop/servidor.py --datos CARPETA

Solo biblioteca estandar, para que corra con el Python embebido que viaja en la carpeta.
"""
import argparse, datetime, glob, json, os, re, shutil, socket, subprocess, sys, threading, urllib.parse, urllib.request, webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = None                          # carpeta de datos; la fija main() con --datos
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from version_juego import ultima
PY = sys.executable
PUERTO_PREFERIDO = 8731
UA = {'User-Agent': 'Mozilla/5.0 (mff-comparador; uso personal)'}

# Lo unico que se sirve: los tres archivos del programa y, de la carpeta de datos,
# data.js, los informes de docs/ y las imagenes. Cualquier otra ruta es 404.
PROGRAMA = {'/': 'index.html', '/index.html': 'index.html', '/app.js': 'app.js', '/styles.css': 'styles.css'}
DE_DATOS = re.compile(r'^/(?:data\.js|docs/[\w-]+\.md|images/(?:[\w-]+/)?[\w-]+\.png)$')

def _script(nombre):
    return os.path.join(RAIZ, 'scripts', nombre)

# Cada boton de Ajustes es una secuencia de comandos. build.py se corre despues de
# cualquier cambio de datos porque es el que regenera data.js. Corren con la carpeta
# de datos como directorio de trabajo: ahi dejan work/, images/, docs/ y data.js.
TAREAS = {
    'datos':     [[PY, _script('fetch_all.py'), '--datos'],
                  [PY, _script('parse_instinto.py')],
                  [PY, _script('build.py')]],
    'tierlists': [[PY, _script('fetch_all.py'), '--tierlists'],
                  [PY, _script('build.py')]],
    'imagenes':  [[PY, _script('fetch_all.py'), '--imagenes']],
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
                p = subprocess.Popen(cmd, cwd=DATOS, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
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
           'work/rotations.json', 'work/wiki_artifact.json', 'work/guia/changelog.json',
           'work/guia/parte1.txt', 'work/guia/parte2.txt')
def pipeline_listo():
    if any(not os.path.exists(os.path.join(DATOS, f)) for f in INSUMOS):
        return False
    d = os.path.join(DATOS, 'work', 'skills_api')
    return os.path.isdir(d) and bool(os.listdir(d))

def version_local():
    """Lee window.MFF_VERSION del data.js que hay en disco."""
    try:
        with open(os.path.join(DATOS, 'data.js'), encoding='utf-8') as f:
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

# ---- capa del usuario ----
CAPA_MAX = 64 * 1024 * 1024        # las imagenes subidas viajan como data URL dentro de la capa
RESPALDOS = 7
_capa_lock = threading.Lock()

def _ruta_capa():
    return os.path.join(DATOS, 'capa.json')

def leer_capa():
    """(codigo, cuerpo): {'capa': null} si todavia no hay capa (primer uso); 500 si el
    archivo no es un objeto JSON valido. En ese caso la pagina no arranca: guardar
    encima la pisaria."""
    ruta = _ruta_capa()
    if not os.path.exists(ruta):
        return 200, {'capa': None}
    try:
        with open(ruta, encoding='utf-8') as f:
            capa = json.load(f)
        if not isinstance(capa, dict):
            raise ValueError('no es un objeto JSON')
        return 200, {'capa': capa}
    except Exception as e:
        return 500, {'error': f'no se pudo leer {ruta}: {e}'}

def guardar_capa(capa):
    """Escribe capa.json de forma atomica (archivo temporal + reemplazo). Antes de la
    primera escritura del dia copia la capa vigente a respaldos/capa-AAAA-MM-DD.json."""
    ruta = _ruta_capa()
    with _capa_lock:
        if os.path.exists(ruta):
            carpeta = os.path.join(DATOS, 'respaldos')
            os.makedirs(carpeta, exist_ok=True)
            hoy = os.path.join(carpeta, f'capa-{datetime.date.today().isoformat()}.json')
            if not os.path.exists(hoy):
                shutil.copy2(ruta, hoy)
                for viejo in sorted(glob.glob(os.path.join(carpeta, 'capa-*.json')))[:-RESPALDOS]:
                    os.remove(viejo)
        tmp = ruta + '.tmp'
        with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(capa, f, ensure_ascii=False)
        os.replace(tmp, ruta)

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        ruta = urllib.parse.unquote(path.split('?', 1)[0].split('#', 1)[0])
        if ruta in PROGRAMA:
            return os.path.join(RAIZ, PROGRAMA[ruta])
        if DE_DATOS.match(ruta):
            return os.path.join(DATOS, *ruta[1:].split('/'))
        return os.path.join(DATOS, 'no-existe')  # send_head responde 404

    def log_message(self, *a):
        pass  # la consola es para el progreso de la sincronizacion, no para cada GET

    # --- proteccion minima: solo se aceptan llamadas de la propia app ---
    def _host_valido(self):
        # Una pagina de otro sitio puede hacer que su dominio apunte a 127.0.0.1 (DNS
        # rebinding) y hablarle a este servidor como si fuera su propio origen, con
        # cabeceras incluidas. El Host delata el nombre que uso: solo se acepta el nuestro.
        puerto = self.server.server_port
        return self.headers.get('Host') in (f'127.0.0.1:{puerto}', f'localhost:{puerto}')

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
        if not self._host_valido():
            return self.send_error(403)
        if self.path.startswith('/api/'):
            if not self._propio():
                return self._json({'error': 'origen no permitido'}, 403)
            if self.path.startswith('/api/estado'):
                return self._json({'app': 'mff-escritorio', 'local': version_local(), 'remota': REMOTA,
                                   'listo': pipeline_listo(), 'trabajo': TRABAJO.estado()})
            if self.path.startswith('/api/progreso'):
                return self._json(TRABAJO.estado())
            if self.path == '/api/capa':
                codigo, cuerpo = leer_capa()
                return self._json(cuerpo, codigo)
            return self._json({'error': 'no existe'}, 404)
        return super().do_GET()

    def do_PUT(self):
        if not self._host_valido():
            return self.send_error(403)
        if self.path != '/api/capa':
            return self._json({'error': 'no existe'}, 404)
        if not self._propio():
            return self._json({'error': 'origen no permitido'}, 403)
        largo = int(self.headers.get('Content-Length') or 0)
        if not 0 < largo <= CAPA_MAX:
            return self._json({'error': f'tamaño de capa invalido ({largo} bytes; maximo {CAPA_MAX})'}, 413)
        try:
            capa = json.loads(self.rfile.read(largo).decode('utf-8'))
        except Exception as e:
            return self._json({'error': f'la capa no es JSON valido: {e}'}, 400)
        if not isinstance(capa, dict):
            return self._json({'error': 'la capa tiene que ser un objeto JSON'}, 400)
        try:
            guardar_capa(capa)
        except OSError as e:
            return self._json({'error': f'no se pudo escribir la capa: {e}'}, 500)
        return self._json({'ok': True})

    def do_POST(self):
        if not self._host_valido():
            return self.send_error(403)
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
    global DATOS
    ap = argparse.ArgumentParser(description='Servidor local de TA GUIANAEL MFF')
    ap.add_argument('--datos', required=True, help='carpeta de datos (data.js, docs/, images/, work/)')
    ap.add_argument('--no-abrir', action='store_true', help='no abrir el navegador')
    args = ap.parse_args()
    DATOS = os.path.abspath(args.datos)
    faltan = [os.path.join(RAIZ, f) for f in ('index.html', 'app.js', 'styles.css')
              if not os.path.exists(os.path.join(RAIZ, f))]
    faltan += [os.path.join(DATOS, f) for f in ('data.js',) if not os.path.exists(os.path.join(DATOS, f))]
    if faltan:
        print('ERROR: faltan archivos de la app ->', ', '.join(faltan))
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
    if not args.no_abrir:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print('\nApagando.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
