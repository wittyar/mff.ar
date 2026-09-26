#!/usr/bin/env python3
"""Servidor local de TA GUIANAEL MFF.

Sirve la app en 127.0.0.1 y hace lo que la página no puede: guardar la capa del
usuario en disco y bajar actualizaciones (el navegador no puede escribir archivos, y
las fuentes no habilitan CORS).

Programa y datos van en carpetas distintas. De la carpeta del programa salen
index.html, app.js y styles.css; de la carpeta de datos, data.js, docs/ e images/.
Fuera de esas rutas no se sirve nada.

API (solo para la propia página: cabecera X-MFF y Host 127.0.0.1):
  GET  /api/estado            versión de la app y de los datos locales, tareas en curso
  GET  /api/capa              la capa del usuario ({"capa": null} si todavía no hay)
  PUT  /api/capa              la guarda; antes de la primera escritura de cada día copia
                              la anterior a respaldos/ (quedan 7)
  POST /api/latido            la ventana sigue abierta
  GET  /api/novedades         compara datos y versión de la app con lo publicado en GitHub
  POST /api/datos/actualizar  baja los datos publicados (tarea en segundo plano)
  POST /api/imagenes/bajar    baja los retratos e íconos que falten (tarea en segundo plano)
  POST /api/app/actualizar    aplica el parche de la última versión y pide reiniciar
  GET  /api/progreso          avance de las tareas

No se corre solo: lo arranca desktop/lanzador.py (crear), que también abre la ventana
y lo apaga cuando ninguna ventana late durante un rato.

Solo biblioteca estándar: corre con el Python embebido del instalador.
"""
import datetime, glob, json, os, re, shutil, threading, time, urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import actualizador

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = None                          # carpeta de datos; la fija crear()
ORIGEN_DATOS = None                   # de dónde se bajan los datos; lo fija crear()
ORIGEN_APP = None                     # latest.json de la última release; lo fija crear()
# Corriendo desde el repo, las versiones nuevas llegan con git pull: un parche encima de
# la copia de trabajo mezclaría archivos de la release con los de git.
DESDE_REPO = os.path.isdir(os.path.join(RAIZ, '.git'))
REINICIAR = threading.Event()         # lo mira el lanzador: se aplicó un parche
# version.json viaja con el programa: versión de la app y formato de datos que entiende.
try:
    with open(os.path.join(RAIZ, 'version.json'), encoding='utf-8') as _f:
        VERSION = json.load(_f)
except OSError as _e:
    raise RuntimeError(f'el programa está incompleto: no se pudo leer version.json ({_e})')
TAREAS = {'datos': actualizador.Tarea(), 'imagenes': actualizador.Tarea(), 'app': actualizador.Tarea()}

# ---- vida del servidor: se apaga cuando ninguna ventana late ----
ESPERA = 180                          # segundos sin latidos antes de apagarse; la fija crear()
_ARRANQUE = time.monotonic()
_ultimo_latido = None

def latido():
    global _ultimo_latido
    _ultimo_latido = time.monotonic()

def latido_cada():
    """Cada cuánto late la página: holgado frente a ESPERA porque el navegador espacia los
    timers de una ventana minimizada (hasta uno por minuto)."""
    return max(1, min(30, ESPERA // 6))

# Las tareas que no se cortan a mitad de camino aunque se cierre la ventana. La de
# imágenes sí: cada imagen se escribe entera o no se escribe, y las que falten se bajan
# la próxima vez (seguir bajando 77 MB con la app cerrada no lo espera nadie).
NO_SE_CORTAN = ('datos', 'app')

def debe_cerrar():
    """Nadie late hace ESPERA segundos (o nunca latió nadie desde el arranque), y no hay
    una tarea de las que no se cortan a mitad de camino."""
    if any(TAREAS[n].estado()['corriendo'] for n in NO_SE_CORTAN):
        return False
    return time.monotonic() - (_ultimo_latido or _ARRANQUE) > ESPERA

def cancelar_tareas():
    """Antes de apagar: las tareas que se pueden cortar dejan de tomar trabajo nuevo."""
    for t in TAREAS.values():
        t.cancelar.set()

# Lo único que se sirve: los tres archivos del programa y, de la carpeta de datos,
# data.js, los informes de docs/ y las imágenes. Cualquier otra ruta es 404.
PROGRAMA = {'/': 'index.html', '/index.html': 'index.html', '/app.js': 'app.js', '/styles.css': 'styles.css'}
DE_DATOS = re.compile(r'^/(?:data\.js|docs/[\w-]+\.md|images/(?:[\w-]+/)?[\w-]+\.png)$')

def estado():
    local = actualizador.leer_json(os.path.join(DATOS, 'datos.json'))
    return {'app': 'mff-escritorio', 'raiz': RAIZ, 'datos': DATOS, 'latido_cada': latido_cada(),
            'version': VERSION['version'], 'formato_datos': VERSION['formato_datos'], 'desde_repo': DESDE_REPO,
            'datos_local': actualizador.resumen(local),
            'imagenes': resumen_imagenes(),
            'tareas': {n: t.estado() for n, t in TAREAS.items()}}

def resumen_imagenes():
    """Cuántas imágenes lista datos.json y cuántas faltan en disco. Una lista inválida no
    tira abajo el estado: vuelve como error para que la página lo muestre."""
    try:
        return {'total': len(actualizador.imagenes_publicadas(DATOS)),
                'faltan': len(actualizador.imagenes_faltantes(DATOS))}
    except Exception as e:
        return {'total': 0, 'faltan': 0, 'error': str(e)}

def novedades():
    """Cada canal por separado: si uno falla (sin conexión, GitHub caído), el error va en
    su lugar y los demás siguen."""
    try:
        datos = actualizador.novedades_datos(ORIGEN_DATOS, DATOS, VERSION['formato_datos'])
    except Exception as e:
        datos = {'error': actualizador.explicar(e)}
    try:
        app = actualizador.novedades_app(ORIGEN_APP, VERSION)
    except Exception as e:
        app = {'error': actualizador.explicar(e)}
    return {'datos': datos, 'app': app}

def tarea_app(t):
    if DESDE_REPO:
        raise RuntimeError('la app corre desde el repo: las versiones nuevas llegan con git pull')
    resultado = actualizador.actualizar_app(ORIGEN_APP, RAIZ, os.path.join(DATOS, 'programa-anterior'), VERSION, t)
    # Un par de segundos para que la página vea que terminó antes de que el servidor se vaya.
    threading.Timer(2.0, REINICIAR.set).start()
    return resultado

# ---- capa del usuario ----
CAPA_MAX = 64 * 1024 * 1024        # las imágenes subidas viajan como data URL dentro de la capa
RESPALDOS = 7
_capa_lock = threading.Lock()

def _ruta_capa():
    return os.path.join(DATOS, 'capa.json')

def leer_capa():
    """(código, cuerpo): {'capa': null} si todavía no hay capa (primer uso); 500 si el
    archivo no es un objeto JSON válido. En ese caso la página no arranca: guardar
    encima la pisaría."""
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
    """Escribe capa.json de forma atómica (archivo temporal + reemplazo). Antes de la
    primera escritura del día copia la capa vigente a respaldos/capa-AAAA-MM-DD.json."""
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
        pass  # un renglón por cada retrato no aporta; lo que importa va a registro.txt

    # --- protección mínima: solo se aceptan llamadas de la propia app ---
    def _host_valido(self):
        # Una página de otro sitio puede hacer que su dominio apunte a 127.0.0.1 (DNS
        # rebinding) y hablarle a este servidor como si fuera su propio origen, con
        # cabeceras incluidas. El Host delata el nombre que usó: solo se acepta el nuestro.
        puerto = self.server.server_port
        return self.headers.get('Host') in (f'127.0.0.1:{puerto}', f'localhost:{puerto}')

    def _propio(self):
        # Una página de otro sitio no puede mandar esta cabecera sin un preflight,
        # y este servidor no responde CORS, así que el preflight falla.
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
        # data.js cambia con cada actualización: no puede quedar cacheado.
        if self.path.startswith('/data.js'):
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def _api(self):
        """Filtro común de la API. False (y ya respondido) si el pedido no es de la página."""
        if not self._propio():
            self._json({'error': 'origen no permitido'}, 403)
            return False
        return True

    def do_GET(self):
        if not self._host_valido():
            return self.send_error(403)
        if not self.path.startswith('/api/'):
            return super().do_GET()
        if not self._api():
            return
        if self.path == '/api/estado':
            return self._json(estado())
        if self.path == '/api/capa':
            codigo, cuerpo = leer_capa()
            return self._json(cuerpo, codigo)
        if self.path == '/api/novedades':
            return self._json(novedades())
        if self.path == '/api/progreso':
            return self._json({n: t.estado() for n, t in TAREAS.items()})
        return self._json({'error': 'no existe'}, 404)

    def do_PUT(self):
        if not self._host_valido():
            return self.send_error(403)
        if self.path != '/api/capa':
            return self._json({'error': 'no existe'}, 404)
        if not self._api():
            return
        largo = int(self.headers.get('Content-Length') or 0)
        if not 0 < largo <= CAPA_MAX:
            return self._json({'error': f'tamaño de capa inválido ({largo} bytes; máximo {CAPA_MAX})'}, 413)
        try:
            capa = json.loads(self.rfile.read(largo).decode('utf-8'))
        except Exception as e:
            return self._json({'error': f'la capa no es JSON válido: {e}'}, 400)
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
        if not self._api():
            return
        if self.path == '/api/latido':
            latido()
            return self._json({'ok': True})
        if self.path == '/api/datos/actualizar':
            tarea = lambda t: actualizador.actualizar_datos(ORIGEN_DATOS, DATOS, VERSION['formato_datos'], t)
            if not TAREAS['datos'].arrancar(tarea):
                return self._json({'error': 'ya se están bajando los datos'}, 409)
            return self._json(TAREAS['datos'].estado())
        if self.path == '/api/app/actualizar':
            if not TAREAS['app'].arrancar(tarea_app):
                return self._json({'error': 'ya se está actualizando la app'}, 409)
            return self._json(TAREAS['app'].estado())
        if self.path == '/api/imagenes/bajar':
            if not TAREAS['imagenes'].arrancar(lambda t: actualizador.bajar_imagenes(DATOS, t)):
                return self._json({'error': 'ya se están bajando las imágenes'}, 409)
            return self._json(TAREAS['imagenes'].estado())
        return self._json({'error': 'no existe'}, 404)

def crear(datos, puerto, espera, origen_datos, origen_app):
    """Servidor atado a 127.0.0.1. puerto 0 deja que el sistema elija uno libre: la capa no
    depende del origen, así que el puerto puede cambiar entre arranques. Con un puerto
    fijo (el reinicio tras un parche retoma el de la ventana abierta) se reintenta unos
    segundos: el proceso anterior puede estar terminando de soltarlo."""
    global DATOS, ESPERA, _ARRANQUE, ORIGEN_DATOS, ORIGEN_APP
    DATOS, ESPERA, _ARRANQUE = os.path.abspath(datos), espera, time.monotonic()
    ORIGEN_DATOS, ORIGEN_APP = origen_datos, origen_app
    limite = time.monotonic() + 20
    while True:
        try:
            return ThreadingHTTPServer(('127.0.0.1', puerto), Handler)
        except OSError:
            if not puerto or time.monotonic() > limite:
                raise
            time.sleep(0.5)
