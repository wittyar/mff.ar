#!/usr/bin/env python3
"""Arranca TA GUIANAEL MFF: el servidor local y la ventana de la app.

Instalada, el acceso directo corre `pythonw lanzador.py`: sin consola, con los datos en
%LOCALAPPDATA%\\TA GUIANAEL MFF. Desde el repo, MFF.bat hace lo mismo con el Python del
sistema, así que las dos usan los mismos datos y la misma capa.

- Una sola instancia por carpeta de datos (candado del sistema sobre instancia.lock, que
  se libera solo aunque el proceso muera). Si ya hay una abierta, se le abre otra ventana
  y este proceso termina.
- La ventana es Microsoft Edge en modo app (--app), con un perfil propio dentro de la
  carpeta de datos: no toca el Edge ni el Chrome de todos los días.
- El servidor se apaga solo cuando ninguna ventana late durante --espera-latido segundos.
  No hay una consola que cerrar por separado.
- Un error al arrancar se muestra en un cuadro de diálogo y queda en registro.txt.

- Tras aplicar un parche de versión (o volver al programa anterior), el proceso se relanza a
  sí mismo en el mismo puerto (--reinicio) y sin abrir otra ventana: la que está abierta se
  reconecta y recarga.
- Pantalla de rescate (#2): si la página no avisa que arrancó en --espera-arranque segundos
  (sin contar lo que tarde en bajar datos o un parche) o avisa un error, se abre una ventana
  con /rescate, una página del servidor que no depende de app.js ni de data.js.

Opciones para probar fuera de Windows: --datos CARPETA, --sin-ventana (ninguna ventana, tampoco
la de rescate: su dirección va a la salida), --puerto N, --espera-arranque S,
--espera-latido S, --origen-datos URL (la base de los datos publicados: los de cada formato, en
datos/<formato>/; por defecto, main en GitHub),
--origen-app URL (el latest.json de la última release).
"""
import argparse, json, logging, os, shutil, subprocess, sys, threading, time, traceback, urllib.request, webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
# El Python embebido del instalador no suma la carpeta del script al path (a propósito,
# bpo-34841): servidor.py y actualizador.py hay que encontrarlos a mano. Se importan
# dentro de main(), después de armar el registro: si fallan (programa incompleto), el
# error tiene que llegar al cuadro de diálogo, no perderse en una consola que no existe.
sys.path.insert(0, AQUI)

APP = 'TA GUIANAEL MFF'
RAIZ = os.path.dirname(AQUI)
ORIGEN_DATOS = 'https://raw.githubusercontent.com/wittyar/mff.ar/main/'
ORIGEN_APP = 'https://github.com/wittyar/mff.ar/releases/latest/download/latest.json'


def carpeta_datos_por_defecto():
    if sys.platform == 'win32':
        return os.path.join(os.environ['LOCALAPPDATA'], APP)
    return os.path.join(os.path.expanduser('~'), '.local', 'share', APP)


def configurar_registro(datos):
    ruta = os.path.join(datos, 'registro.txt')
    if os.path.exists(ruta) and os.path.getsize(ruta) > 1024 * 1024:
        os.replace(ruta, os.path.join(datos, 'registro.anterior.txt'))
    manejadores = [logging.FileHandler(ruta, encoding='utf-8')]
    if sys.stderr is not None:        # con pythonw no hay consola
        manejadores.append(logging.StreamHandler(sys.stderr))
    logging.basicConfig(level=logging.INFO, handlers=manejadores,
                        format='%(asctime)s %(levelname)s %(message)s')
    # Con pythonw, sys.stderr es None y los errores de los hilos se perderían.
    threading.excepthook = lambda a: logging.error('error en un hilo: %s', ''.join(
        traceback.format_exception(a.exc_type, a.exc_value, a.exc_traceback)))


def avisar(titulo, texto):
    """Error visible: cuadro de diálogo en Windows (no hay consola), stderr en el resto."""
    logging.error('%s: %s', titulo, texto)
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, texto, titulo, 0x10)
    elif sys.stderr is not None:
        print(f'{titulo}: {texto}', file=sys.stderr)


def tomar_candado(datos):
    """Archivo abierto con un candado exclusivo del sistema. None si otro proceso lo tiene.
    El sistema lo suelta cuando el proceso termina, aunque sea por un cuelgue."""
    f = open(os.path.join(datos, 'instancia.lock'), 'a+')
    try:
        if sys.platform == 'win32':
            import msvcrt
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        f.close()
        return None
    return f


def instancia_abierta(datos, espera=15):
    """Estado de la instancia que tiene el candado. Si recién está arrancando, se le da
    unos segundos para que escriba instancia.json y conteste."""
    limite = time.monotonic() + espera
    while True:
        try:
            with open(os.path.join(datos, 'instancia.json'), encoding='utf-8') as f:
                puerto = json.load(f)['puerto']
            req = urllib.request.Request(f'http://127.0.0.1:{puerto}/api/estado', headers={'X-MFF': '1'})
            estado = json.loads(urllib.request.urlopen(req, timeout=3).read())
            estado['puerto'] = puerto
            return estado
        except Exception as e:
            if time.monotonic() > limite:
                raise RuntimeError(f'hay otra instancia de la app con el candado, pero no contesta ({e}). '
                                   'Cerrala desde el Administrador de tareas (proceso pythonw) y volvé a abrirla.')
            time.sleep(0.5)


def sembrar_datos(datos):
    """Primer arranque: la carpeta de datos todavía no tiene data.js, así que se copian los
    datos que trae el programa (el instalador y el repo los traen), con su datos.json.
    Después se actualizan solos desde GitHub."""
    if os.path.exists(os.path.join(datos, 'data.js')):
        return
    for f in ('data.js', 'datos.json'):
        origen = os.path.join(RAIZ, f)
        if not os.path.exists(origen):
            raise RuntimeError(f'el programa no trae los datos iniciales: falta {origen}')
        shutil.copy2(origen, os.path.join(datos, f))
    docs = os.path.join(RAIZ, 'docs')
    if os.path.isdir(docs):
        shutil.copytree(docs, os.path.join(datos, 'docs'), dirs_exist_ok=True)
    logging.info('primer arranque: datos copiados desde %s', RAIZ)


def abrir_ventana(url, datos):
    if sys.platform == 'win32':
        perfil = os.path.join(datos, 'ventana')
        # ShellExecute encuentra msedge.exe por App Paths, esté donde esté instalado.
        try:
            os.startfile('msedge.exe', 'open', f'--app={url} --user-data-dir="{perfil}" '
                                               '--no-first-run --no-default-browser-check')
        except OSError as e:
            raise RuntimeError(f'no se pudo abrir Microsoft Edge, que la app usa como ventana ({e}). '
                               'Si no está instalado, se baja de microsoft.com/edge.')
    else:
        webbrowser.open(url)


def main():
    ap = argparse.ArgumentParser(description=f'Arranca {APP}')
    ap.add_argument('--datos', help='carpeta de datos (por defecto, la de la app instalada)')
    ap.add_argument('--sin-ventana', action='store_true',
                    help='no abrir ventanas (tampoco la de rescate: su dirección va a la salida)')
    ap.add_argument('--reinicio', action='store_true',
                    help='relanzado tras un parche: no abre la ventana principal (la abierta se reconecta)')
    ap.add_argument('--espera-arranque', type=int, default=60,
                    help='segundos para que la página avise que arrancó antes de abrir la pantalla de rescate')
    ap.add_argument('--puerto', type=int, default=0, help='puerto fijo (0: lo elige el sistema)')
    ap.add_argument('--espera-latido', type=int, default=180,
                    help='segundos sin latidos de ninguna ventana antes de apagarse')
    ap.add_argument('--origen-datos', default=ORIGEN_DATOS,
                    help='URL base de los datos publicados (los de cada formato, en datos/<formato>/)')
    ap.add_argument('--origen-app', default=ORIGEN_APP, help='URL del latest.json de la última release')
    args = ap.parse_args()
    datos = os.path.abspath(args.datos or carpeta_datos_por_defecto())
    os.makedirs(datos, exist_ok=True)
    configurar_registro(datos)
    import servidor

    candado = tomar_candado(datos)
    if candado is None:
        otra = instancia_abierta(datos)
        if os.path.normcase(otra.get('raiz', '')) != os.path.normcase(RAIZ):
            raise RuntimeError(f'ya está abierta la app desde otra carpeta ({otra.get("raiz")}). '
                               'Cerrala antes de abrir esta.')
        url = f'http://127.0.0.1:{otra["puerto"]}/index.html'
        logging.info('ya había una instancia abierta: nueva ventana en %s', url)
        print(f'  abriendo {url}', flush=True)
        if not args.sin_ventana:
            abrir_ventana(url, datos)
        return 0

    sembrar_datos(datos)
    srv = servidor.crear(datos, args.puerto, args.espera_latido, args.origen_datos, args.origen_app, args.espera_arranque)
    puerto = srv.server_port
    url = f'http://127.0.0.1:{puerto}/index.html'
    ruta_instancia = os.path.join(datos, 'instancia.json')
    with open(ruta_instancia, 'w', encoding='utf-8') as f:
        json.dump({'pid': os.getpid(), 'puerto': puerto, 'raiz': RAIZ}, f)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    logging.info('%s: programa en %s, datos en %s', APP, RAIZ, datos)
    print(APP, flush=True)
    print(f'  datos: {datos}', flush=True)
    print(f'  abriendo {url}', flush=True)
    if not args.sin_ventana and not args.reinicio:
        abrir_ventana(url, datos)

    while not servidor.debe_cerrar() and not servidor.REINICIAR.is_set():
        motivo = servidor.motivo_rescate()
        if motivo:
            rescate = f'http://127.0.0.1:{puerto}/rescate'
            logging.info('se abre la pantalla de rescate (%s)', motivo['tipo'])
            print(f'  rescate {rescate}', flush=True)
            if not args.sin_ventana:
                abrir_ventana(rescate, datos)
        time.sleep(1)
    reiniciar = servidor.REINICIAR.is_set()
    if reiniciar:
        logging.info('cambió el programa (un parche o la vuelta al anterior): se reinicia en el puerto %s', puerto)
    else:
        logging.info('ninguna ventana late hace %s s: se apaga', args.espera_latido)
    if servidor.TAREAS['imagenes'].estado()['corriendo']:
        logging.info('se corta la descarga de imágenes: las que falten se bajan la próxima vez')
    servidor.cancelar_tareas()
    srv.shutdown()
    srv.server_close()
    os.remove(ruta_instancia)
    candado.close()
    if reiniciar:
        relanzar(args, datos, puerto)
    return 0


def relanzar(args, datos, puerto):
    """Otro proceso con el programa ya parchado (o el anterior), en el mismo puerto y sin ventana nueva; la de
    rescate sí puede abrirse, salvo con --sin-ventana."""
    cmd = [sys.executable, os.path.abspath(__file__), '--datos', datos, '--puerto', str(puerto),
           '--sin-ventana' if args.sin_ventana else '--reinicio', '--espera-latido', str(args.espera_latido),
           '--espera-arranque', str(args.espera_arranque), '--origen-datos', args.origen_datos,
           '--origen-app', args.origen_app]
    if sys.platform == 'win32':
        subprocess.Popen(cmd, close_fds=True,
                         creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        subprocess.Popen(cmd, close_fds=True, start_new_session=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        logging.error('%s', traceback.format_exc())
        avisar(f'No se pudo abrir {APP}', str(e))
        sys.exit(1)
