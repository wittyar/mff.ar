"""Arranque de la app del repo para las pruebas: carpeta de datos nueva con el data.js
recién construido, y un origen local que publica ese mismo datos.json y un latest.json
de la misma versión (así la app no baja nada de GitHub en medio de la prueba).

Los datos (data.js, datos.json, docs/ e images/) salen de DATOS: el repo, o la carpeta que diga
la variable de entorno MFF_DATOS (la que arma armar_datos_prueba.py mientras el data.js del repo
sea de un formato anterior al de version.json). El programa sale siempre de RAIZ."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import http.server, json, os, shutil, subprocess, sys, tempfile, threading

RAIZ = RAIZ
DATOS = os.environ.get('MFF_DATOS', RAIZ)
if DATOS != RAIZ:
    print(f'datos de las pruebas: {DATOS} (MFF_DATOS), no los del repo', flush=True)


def origen_local():
    pub = tempfile.mkdtemp(prefix='mffpub-')
    shutil.copy(os.path.join(DATOS, 'datos.json'), pub)
    # Desde la 1.0.30 la app lee los de su formato, en datos/<formato>/ (#1); la raíz, las versiones anteriores.
    f = json.load(open(os.path.join(DATOS, 'datos.json'), encoding='utf-8'))['formato']
    os.makedirs(os.path.join(pub, 'datos', str(f)))
    shutil.copy(os.path.join(DATOS, 'datos.json'), os.path.join(pub, 'datos', str(f)))
    v = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))
    json.dump({'version': v['version'], 'python': v['python'], 'notas': '', 'formato_datos': v['formato_datos'],
               'parche': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1},
               'instalador': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1}},
              open(os.path.join(pub, 'latest.json'), 'w'))

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=pub, **k)
        def log_message(self, *a): pass
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{srv.server_port}/'


def carpeta_datos():
    d = tempfile.mkdtemp(prefix='mffdatos-')
    for f in ('data.js', 'datos.json'):
        shutil.copy(os.path.join(DATOS, f), d)
    shutil.copytree(os.path.join(DATOS, 'docs'), os.path.join(d, 'docs'))
    os.symlink(os.path.join(DATOS, 'images'), os.path.join(d, 'images'))
    return d


def levantar(datos, origen):
    # --espera-latido 900: las pruebas evalúan en la página bloques de minutos (verif_consistencia), y mientras
    # tanto la página no late; con los 180 s de siempre, dos pruebas pesadas a la vez apagaban el servidor.
    srv = subprocess.Popen([sys.executable, 'desktop/lanzador.py', '--datos', datos, '--sin-ventana', '--espera-latido', '900',
                            '--origen-datos', origen, '--origen-app', origen + 'latest.json'],
                           cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for _ in range(40):
        linea = srv.stdout.readline()
        if 'abriendo' in linea:
            return srv, linea.split('abriendo')[1].strip()
    raise SystemExit('el servidor no arrancó')


class Chequeo:
    def __init__(self):
        self.fallas = []

    def __call__(self, nombre, cond, detalle=''):
        print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
        if not cond:
            self.fallas.append(nombre)

    def fin(self):
        print('\nFALLAS:', self.fallas or 'ninguna')


def datos_js(*globales):
    """Globales de data.js (vía node), para sacar ids y nombres sin depender de la app."""
    js = ("const vm=require('vm'),fs=require('fs');const c={window:{}};vm.createContext(c);"
          f"vm.runInContext(fs.readFileSync('{DATOS}/data.js','utf8'),c);"
          f"process.stdout.write(JSON.stringify({{{','.join(f'{g}:c.window.{g}' for g in globales)}}}));")
    return json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)
