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
  POST /api/arranque          la página avisa que arrancó ({"ok": true}) o por qué no ({"error": "..."})
  GET  /api/rescate           lo que muestra la pantalla de rescate: por qué se abrió, el programa anterior
                              guardado y el final de registro.txt
  POST /api/rescate/volver    vuelve al programa anterior (programa-anterior/) y pide reiniciar

Pantalla de rescate (#2): GET /rescate es una página propia, hecha acá (rescate.py), sin app.js ni data.js. La
abre el lanzador si la página no avisa que arrancó a tiempo o avisa un error (motivo_rescate); desde ella se
actualiza la app, se baja el instalador, se vuelve al programa anterior o se vuelven a bajar los datos.

No se corre solo: lo arranca desktop/lanzador.py (crear), que también abre la ventana
y lo apaga cuando ninguna ventana late durante un rato.

Solo biblioteca estándar: corre con el Python embebido del instalador.
"""
import datetime, glob, json, logging, os, re, shutil, threading, time, urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import actualizador, rescate

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

# ---- arranque y rescate (#2) ----
ESPERA_ARRANQUE = 60                  # segundos para que la página avise que arrancó; la fija crear()
ARRANQUE = {'ok': False, 'error': None}
_plazo_arranque = None
RESCATE = None                        # por qué se abrió la pantalla de rescate, cuando se abrió

def avisar_arranque(cuerpo):
    """Lo que avisa la página: que arrancó, o el error que cortó el arranque."""
    if cuerpo == {'ok': True}:
        ARRANQUE['ok'] = True
    elif set(cuerpo) == {'error'} and isinstance(cuerpo['error'], str) and cuerpo['error']:
        ARRANQUE['error'] = cuerpo['error'][:2000]
        logging.error('la página no pudo arrancar: %s', ARRANQUE['error'])
    else:
        raise ValueError('el aviso de arranque es {"ok": true} o {"error": "..."}')

def motivo_rescate():
    """None mientras no haga falta la pantalla de rescate. Hace falta si la página avisó un error, o si pasaron
    ESPERA_ARRANQUE segundos sin que avisara que arrancó; mientras se bajan datos o un parche, el plazo se corre (el
    primer arranque de una versión con otro formato baja los datos antes de mostrar nada)."""
    global _plazo_arranque, RESCATE
    if ARRANQUE['ok'] or RESCATE:
        return None
    if ARRANQUE['error']:
        RESCATE = {'tipo': 'error', 'detalle': ARRANQUE['error']}
        return RESCATE
    ahora = time.monotonic()
    if any(TAREAS[n].estado()['corriendo'] for n in NO_SE_CORTAN):
        _plazo_arranque = ahora + ESPERA_ARRANQUE
        return None
    if ahora > _plazo_arranque:
        RESCATE = {'tipo': 'tiempo', 'segundos': ESPERA_ARRANQUE}
        logging.error('la página no avisó que arrancó en %s s', ESPERA_ARRANQUE)
        return RESCATE
    return None

def _respaldo():
    return os.path.join(DATOS, 'programa-anterior')

def estado_rescate():
    registro = os.path.join(DATOS, 'registro.txt')
    with open(registro, encoding='utf-8', errors='replace') as f:
        final = f.readlines()[-40:]
    return {'motivo': RESCATE, 'programa_anterior': actualizador.programa_anterior(_respaldo()),
            'registro': ''.join(final)}

def volver_al_anterior():
    if DESDE_REPO:
        raise RuntimeError('la app corre desde el repo: el programa se cambia con git')
    resultado = actualizador.volver_al_anterior(RAIZ, _respaldo())
    logging.info('se volvió al programa anterior (%s)', resultado['version'])
    threading.Timer(2.0, REINICIAR.set).start()
    return resultado

def cancelar_tareas():
    """Antes de apagar: las tareas que se pueden cortar dejan de tomar trabajo nuevo."""
    for t in TAREAS.values():
        t.cancelar.set()

# Lo único que se sirve: los archivos del programa (y su ícono) y, de la carpeta de datos,
# data.js, los informes de docs/ y las imágenes. Cualquier otra ruta es 404.
PROGRAMA = {'/': 'index.html', '/index.html': 'index.html', '/app.js': 'app.js', '/styles.css': 'styles.css',
            '/favicon.ico': 'desktop/mff.ico'}
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
    resultado = actualizador.actualizar_app(ORIGEN_APP, RAIZ, _respaldo(), VERSION, t)
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
        # Todo lo que se sirve (programa, datos, informe, retratos) puede cambiar con un
        # parche o una actualización de datos mientras la ventana sigue en el mismo puerto.
        # Sin esta cabecera el navegador reusa su copia sin preguntar (caché heurística:
        # hasta un 10% de la edad del archivo) y, tras un parche, la ventana seguía con el
        # app.js viejo. Con no-cache pregunta siempre; lo que no cambió vuelve como 304.
        if not self.path.startswith('/api/'):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def _index(self):
        """index.html con la versión en las direcciones de app.js y styles.css. Las copias
        que guardó el navegador de la 1.0.0 y la 1.0.1, que no mandaban Cache-Control,
        todavía le valen un rato: con otra dirección no las usa."""
        html = open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
        for f in ('app.js', 'styles.css'):
            if html.count(f'"{f}"') != 1:
                logging.error('index.html no referencia "%s" una sola vez', f)
                return self.send_error(500, f'index.html no referencia "{f}" una sola vez')
            html = html.replace(f'"{f}"', f'"{f}?v={VERSION["version"]}"')
        self._html(html)

    def _html(self, html):
        cuerpo = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

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
            ruta = urllib.parse.urlsplit(self.path).path
            if ruta in ('/', '/index.html'):
                return self._index()
            if ruta == '/rescate':
                return self._html(rescate.pagina(idioma()))
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
        if self.path == '/api/rescate':
            return self._json(estado_rescate())
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
        if self.path == '/api/arranque':
            largo = int(self.headers.get('Content-Length') or 0)
            if not 0 < largo <= 8192:
                return self._json({'error': f'tamaño inválido ({largo} bytes)'}, 413)
            try:
                avisar_arranque(json.loads(self.rfile.read(largo).decode('utf-8')))
            except ValueError as e:
                return self._json({'error': str(e)}, 400)
            return self._json({'ok': True})
        if self.path == '/api/rescate/volver':
            try:
                return self._json(volver_al_anterior())
            except Exception as e:
                logging.error('no se pudo volver al programa anterior: %s', e)
                return self._json({'error': actualizador.explicar(e)}, 500)
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

def idioma():
    """El idioma de la capa ('es' si todavía no hay o no se puede leer: la pantalla de rescate tiene que abrir igual)."""
    codigo, cuerpo = leer_capa()
    capa = cuerpo.get('capa') if codigo == 200 else None
    return 'en' if capa and (capa.get('prefs') or {}).get('lang') == 'en' else 'es'

def crear(datos, puerto, espera, origen_datos, origen_app, espera_arranque):
    """Servidor atado a 127.0.0.1. puerto 0 deja que el sistema elija uno libre: la capa no
    depende del origen, así que el puerto puede cambiar entre arranques. Con un puerto
    fijo (el reinicio tras un parche retoma el de la ventana abierta) se reintenta unos
    segundos: el proceso anterior puede estar terminando de soltarlo."""
    global DATOS, ESPERA, _ARRANQUE, ORIGEN_DATOS, ORIGEN_APP, ESPERA_ARRANQUE, _plazo_arranque
    DATOS, ESPERA, _ARRANQUE = os.path.abspath(datos), espera, time.monotonic()
    ESPERA_ARRANQUE, _plazo_arranque = espera_arranque, _ARRANQUE + espera_arranque
    ORIGEN_DATOS, ORIGEN_APP = origen_datos, origen_app
    limite = time.monotonic() + 20
    while True:
        try:
            return ThreadingHTTPServer(('127.0.0.1', puerto), Handler)
        except OSError:
            if not puerto or time.monotonic() > limite:
                raise
            time.sleep(0.5)
