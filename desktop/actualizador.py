"""Actualizaciones de TA GUIANAEL MFF.

Datos del juego: salen de GitHub ya armados por el workflow semanal, en la carpeta de cada
formato (datos/<formato>/): la app baja los del suyo, así que una versión vieja sigue teniendo
datos que puede leer cuando sube el formato (#1). datos.json dice qué hay publicado (formato,
versión, sha256 y tamaño de cada archivo); se bajan los archivos, se verifican contra ese
manifiesto y recién ahí reemplazan a los anteriores.
Lo último que se escribe es datos.json: si algo corta a mitad de camino, lo local sigue
siendo la versión anterior completa.

Imágenes: datos.json trae la lista de retratos e íconos con su URL de origen
(thanosvibs). Se bajan las que falten; las que la fuente no publica (404) se informan
aparte de las que fallaron por otra cosa.

Versión de la app: cada release de GitHub publica latest.json (versión, notas, versión
de Python, parche con su sha256 e instalador). Si la versión nueva usa el mismo Python,
el parche (un zip con los archivos del programa) reemplaza esos archivos y la app se
reinicia; si cambia Python, hace falta el instalador completo.

Solo biblioteca estándar: corre con el Python embebido del instalador.
"""
import hashlib, io, json, os, re, shutil, threading, urllib.error, urllib.request, zipfile
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

def publicados(origen, formato_app):
    """La carpeta de los datos del formato de la app y su manifiesto, crudo y leído. Corta si todavía no hay datos
    publicados de ese formato o si el manifiesto dice otro."""
    base = f'{origen}datos/{formato_app}/'
    try:
        crudo = bajar(base + 'datos.json', 15)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise RuntimeError(f'todavía no hay datos publicados de formato {formato_app} ({e.url})') from e
        raise
    m = json.loads(crudo)
    if m['formato'] != formato_app:
        raise RuntimeError(f'{base}datos.json dice formato {m["formato"]} y está en la carpeta del {formato_app}')
    return base, crudo, m


def novedades_datos(origen, carpeta, formato_app):
    """Compara el datos.json publicado para el formato de la app con el local. 'hay': el data.js publicado es otro."""
    _, _, remoto = publicados(origen, formato_app)
    local = leer_json(os.path.join(carpeta, 'datos.json'))
    sha_local = local['archivos']['data.js']['sha256'] if local else None
    return {'hay': remoto['archivos']['data.js']['sha256'] != sha_local,
            'remoto': resumen(remoto), 'local': resumen(local)}


def actualizar_datos(origen, carpeta, formato_app, tarea):
    base, crudo, m = publicados(origen, formato_app)
    archivos = m['archivos']
    for rel in archivos:
        if not ARCHIVO_DE_DATOS.match(rel):
            raise RuntimeError(f'el manifiesto pide un archivo que la app no usa: {rel}')
    tarea.avance(0, sum(a['bytes'] for a in archivos.values()))
    listos, hecho = [], 0
    try:
        for rel, info in archivos.items():
            contenido = bajar(base + rel, 60, lambda h, b=hecho: tarea.avance(b + h))
            if len(contenido) != info['bytes'] or hashlib.sha256(contenido).hexdigest() != info['sha256']:
                raise RuntimeError(f'{rel} llegó distinto de lo que anuncia datos.json (GitHub puede estar '
                                   'terminando de publicar una actualización): no se usa. Probá de nuevo en unos minutos.')
            destino = os.path.join(carpeta, *rel.split('/'))
            listos.append((_escribir(destino, contenido), destino))
            hecho += info['bytes']
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


# ---- versión de la app ----

# Lo único que un parche puede reemplazar: los archivos del programa (PROGRAMA en construir.py).
DEL_PROGRAMA = re.compile(r'^(?:index\.html|app\.js|styles\.css|version\.json|desktop/[\w-]+\.py|desktop/mff\.ico)$')


def version_tupla(v):
    return tuple(int(x) for x in v.split('.'))


def novedades_app(url, version):
    """Compara latest.json de la última release con la versión instalada. 'aplicable': la
    nueva usa el mismo Python, así que alcanza con el parche."""
    ult = json.loads(bajar(url, 15))
    return {'hay': version_tupla(ult['version']) > version_tupla(version['version']),
            'version': ult['version'], 'notas': ult.get('notas', ''),
            'aplicable': ult['python'] == version['python'], 'instalador': ult['instalador']['url']}


def actualizar_app(url, raiz, respaldo, version, tarea):
    """Baja el parche de la última release, lo verifica y reemplaza los archivos del
    programa. Antes de pisar nada copia los actuales a `respaldo`; si un reemplazo falla,
    los vuelve a poner. version.json va último: hasta ahí el programa sigue siendo el
    anterior."""
    ult = json.loads(bajar(url, 15))
    if version_tupla(ult['version']) <= version_tupla(version['version']):
        raise RuntimeError(f'la última versión publicada ({ult["version"]}) no es más nueva que la instalada')
    if ult['python'] != version['python']:
        raise RuntimeError(f'la versión {ult["version"]} necesita el instalador completo (cambia Python)')
    parche = ult['parche']
    tarea.avance(0, parche['bytes'])
    contenido = bajar(parche['url'], 120, tarea.avance)
    if len(contenido) != parche['bytes'] or hashlib.sha256(contenido).hexdigest() != parche['sha256']:
        raise RuntimeError('el parche llegó distinto de lo que anuncia la release: no se usa')
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        nombres = [n for n in z.namelist() if not n.endswith('/')]
        ajenos = [n for n in nombres if not DEL_PROGRAMA.match(n)]
        if ajenos:
            raise RuntimeError(f'el parche trae archivos que no son del programa: {", ".join(ajenos[:3])}')
        if 'version.json' not in nombres or json.loads(z.read('version.json'))['version'] != ult['version']:
            raise RuntimeError('el parche no es de la versión que anuncia la release')
        nombres.sort(key=lambda n: n == 'version.json')
        nuevos = []
        try:
            for n in nombres:
                destino = os.path.join(raiz, *n.split('/'))
                nuevos.append((_escribir(destino, z.read(n)), destino, n))
        except Exception:
            for tmp, _, _ in nuevos:
                os.remove(tmp)
            raise
    if os.path.isdir(respaldo):
        shutil.rmtree(respaldo)
    hechos = []
    try:
        for tmp, destino, n in nuevos:
            if os.path.exists(destino):
                copia = os.path.join(respaldo, *n.split('/'))
                os.makedirs(os.path.dirname(copia), exist_ok=True)
                shutil.copy2(destino, copia)
            os.replace(tmp, destino)
            hechos.append((destino, n))
    except Exception:
        for destino, n in hechos:
            copia = os.path.join(respaldo, *n.split('/'))
            if os.path.exists(copia):
                shutil.copy2(copia, destino)
            else:
                os.remove(destino)
        for tmp, _, _ in nuevos:
            if os.path.exists(tmp):
                os.remove(tmp)
        raise
    return {'version': ult['version']}
