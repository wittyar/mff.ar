"""Actualizaciones de TA GUIANAEL MFF.

Datos del juego: salen de GitHub ya armados por el workflow semanal. datos.json dice qué
hay publicado (formato, versión, sha256 y tamaño de cada archivo); se bajan los
archivos, se verifican contra ese manifiesto y recién ahí reemplazan a los anteriores.
Lo último que se escribe es datos.json: si algo corta a mitad de camino, lo local sigue
siendo la versión anterior completa.

Imágenes: datos.json trae la lista de retratos e íconos con su URL de origen
(thanosvibs). Se bajan las que falten; las que la fuente no publica (404) se informan
aparte de las que fallaron por otra cosa.

Solo biblioteca estándar: corre con el Python embebido del instalador.
"""
import hashlib, json, os, re, threading, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {'User-Agent': 'TA-GUIANAEL-MFF (app de escritorio; uso personal)'}
# Solo se escriben archivos que la app sirve: nada del manifiesto puede apuntar afuera.
ARCHIVO_DE_DATOS = re.compile(r'^(?:data\.js|docs/[\w-]+\.md)$')
IMAGEN = re.compile(r'^images/(?:[\w-]+/)?[\w-]+\.png$')
PNG = b'\x89PNG'


def explicar(e):
    """Un error de red dicho en criollo; cualquier otro, tal cual."""
    if isinstance(e, urllib.error.HTTPError):
        return f'el servidor respondió {e.code} para {e.url}'
    if isinstance(e, urllib.error.URLError):
        return f'sin conexión ({e.reason})'
    if isinstance(e, TimeoutError):
        return 'sin respuesta a tiempo (¿conexión lenta?)'
    return str(e)


class Tarea:
    """Un trabajo en segundo plano con su avance, para que la página lo muestre."""

    def __init__(self):
        self._lock = threading.Lock()
        self.cancelar = threading.Event()   # la tarea lo mira para cortar antes de tiempo
        self._estado = {'corriendo': False, 'terminado': False, 'error': None, 'hecho': 0, 'total': 0,
                        'resultado': None}

    def estado(self):
        with self._lock:
            return dict(self._estado)

    def avance(self, hecho, total=None):
        with self._lock:
            self._estado['hecho'] = hecho
            if total is not None:
                self._estado['total'] = total

    def arrancar(self, funcion):
        """Corre funcion(tarea) en un hilo. False si ya había una corriendo."""
        with self._lock:
            if self._estado['corriendo']:
                return False
            self._estado = {'corriendo': True, 'terminado': False, 'error': None, 'hecho': 0, 'total': 0,
                            'resultado': None}
            self.cancelar.clear()
        threading.Thread(target=self._correr, args=(funcion,), daemon=True).start()
        return True

    def _correr(self, funcion):
        resultado = error = None
        try:
            resultado = funcion(self)
        except Exception as e:
            error = explicar(e)
        with self._lock:
            self._estado.update(corriendo=False, terminado=True, error=error, resultado=resultado)

    def sumar(self):
        with self._lock:
            self._estado['hecho'] += 1


def bajar(url, timeout=30, progreso=None):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        partes, hecho = [], 0
        while True:
            bloque = r.read(64 * 1024)
            if not bloque:
                break
            partes.append(bloque)
            hecho += len(bloque)
            if progreso:
                progreso(hecho)
        return b''.join(partes)


def leer_json(ruta):
    """El JSON del archivo, o None si no existe."""
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


def resumen(manifiesto):
    return {k: manifiesto.get(k) for k in ('juego', 'generado', 'formato')} if manifiesto else None


def _escribir(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    tmp = ruta + '.nuevo'
    with open(tmp, 'wb') as f:
        f.write(contenido)
    return tmp


# ---- datos del juego ----

def novedades_datos(origen, carpeta, formato_app):
    """Compara el datos.json publicado con el local. 'hay': el data.js publicado es otro.
    'compatible': es del formato que entiende esta versión de la app."""
    remoto = json.loads(bajar(origen + 'datos.json', 15))
    local = leer_json(os.path.join(carpeta, 'datos.json'))
    sha_local = local['archivos']['data.js']['sha256'] if local else None
    return {'hay': remoto['archivos']['data.js']['sha256'] != sha_local,
            'compatible': remoto['formato'] == formato_app,
            'remoto': resumen(remoto), 'local': resumen(local)}


def actualizar_datos(origen, carpeta, formato_app, tarea):
    crudo = bajar(origen + 'datos.json', 15)
    m = json.loads(crudo)
    if m['formato'] != formato_app:
        raise RuntimeError(f'los datos publicados son de formato {m["formato"]} y esta versión de la app '
                           f'usa el {formato_app}: ' + ('actualizá la app.' if m['formato'] > formato_app
                                                        else 'esperá a la próxima publicación de datos.'))
    archivos = m['archivos']
    for rel in archivos:
        if not ARCHIVO_DE_DATOS.match(rel):
            raise RuntimeError(f'el manifiesto pide un archivo que la app no usa: {rel}')
    tarea.avance(0, sum(a['bytes'] for a in archivos.values()))
    listos, base = [], 0
    try:
        for rel, info in archivos.items():
            contenido = bajar(origen + rel, 60, lambda h, b=base: tarea.avance(b + h))
            if len(contenido) != info['bytes'] or hashlib.sha256(contenido).hexdigest() != info['sha256']:
                raise RuntimeError(f'{rel} llegó distinto de lo que anuncia datos.json (GitHub puede estar '
                                   'terminando de publicar una actualización): no se usa. Probá de nuevo en unos minutos.')
            destino = os.path.join(carpeta, *rel.split('/'))
            listos.append((_escribir(destino, contenido), destino))
            base += info['bytes']
    except Exception:
        for tmp, _ in listos:
            os.remove(tmp)
        raise
    for tmp, destino in listos:
        os.replace(tmp, destino)
    os.replace(_escribir(os.path.join(carpeta, 'datos.json'), crudo), os.path.join(carpeta, 'datos.json'))


# ---- imágenes ----

def imagenes_publicadas(carpeta):
    """[(ruta, url)] de datos.json local, validadas: solo rutas de images/ y URLs http(s)."""
    m = leer_json(os.path.join(carpeta, 'datos.json')) or {}
    lista = m.get('imagenes', [])
    for ruta, url in lista:
        if not IMAGEN.match(ruta) or not url.startswith(('https://', 'http://')):
            raise RuntimeError(f'datos.json trae una imagen inválida: {ruta} <- {url}')
    return lista


def imagenes_faltantes(carpeta):
    return [(r, u) for r, u in imagenes_publicadas(carpeta)
            if not os.path.exists(os.path.join(carpeta, *r.split('/')))]


def bajar_imagenes(carpeta, tarea):
    """Baja las imágenes que falten. Devuelve las que la fuente no publica (404) y las que
    fallaron por otra cosa; con alguna de esas últimas la tarea termina con error."""
    faltan = imagenes_faltantes(carpeta)
    tarea.avance(0, len(faltan))
    no_publicadas, fallidas = [], []

    def una(par):
        if tarea.cancelar.is_set():   # la app se está cerrando: el resto sigue la próxima vez
            return
        ruta, url = par
        try:
            contenido = bajar(url, 30)
            if contenido[:4] != PNG:
                raise RuntimeError('lo que llegó no es un PNG')
            destino = os.path.join(carpeta, *ruta.split('/'))
            os.replace(_escribir(destino, contenido), destino)
        except urllib.error.HTTPError as e:
            (no_publicadas if e.code == 404 else fallidas).append([ruta, explicar(e)])
        except Exception as e:
            fallidas.append([ruta, explicar(e)])
        tarea.sumar()

    with ThreadPoolExecutor(6) as ex:
        list(ex.map(una, faltan))
    resultado = {'bajadas': len(faltan) - len(no_publicadas) - len(fallidas),
                 'no_publicadas': sorted(no_publicadas), 'fallidas': sorted(fallidas)}
    if fallidas:
        raise RuntimeError(f'{len(fallidas)} imágenes no se pudieron bajar (la primera: {fallidas[0][0]}: {fallidas[0][1]})')
    return resultado
