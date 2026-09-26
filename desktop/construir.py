#!/usr/bin/env python3
"""Arma lo que publica cada versión de TA GUIANAEL MFF. Lo corre el workflow publicar.yml
al empujar una etiqueta vX.Y.Z; también anda a mano.

  python desktop/construir.py programa            dist/programa/ y el parche
  python desktop/construir.py manifiesto vX.Y.Z   dist/latest.json y dist/notas.md

dist/programa/ es lo que instala el instalador (desktop/instalador.iss): los archivos del
programa, los datos iniciales (se copian a la carpeta de datos en el primer arranque) y
el Python embebido de python.org, verificado contra su sha256.

El parche (dist/mff-parche-X.Y.Z.zip) lleva solo los archivos del programa: es lo que la
app instalada baja y aplica sola cuando sale una versión con el mismo Python.
latest.json es lo que la app consulta para saber si hay versión nueva.
"""
import glob, hashlib, io, json, os, shutil, sys, urllib.request, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(RAIZ, 'dist')
REPO = 'wittyar/mff.ar'

# El programa: lo que instala el instalador y lo que puede traer un parche (tiene que
# coincidir con DEL_PROGRAMA de actualizador.py).
PROGRAMA = ['index.html', 'app.js', 'styles.css', 'version.json', 'desktop/mff.ico',
            'desktop/lanzador.py', 'desktop/servidor.py', 'desktop/actualizador.py']
# Datos del primer arranque: después se actualizan solos desde GitHub.
DATOS_INICIALES = ['data.js', 'datos.json', 'docs/AUDITORIA.md']
# Python embebido de python.org por versión, con su sha256 (se agrega al cambiar
# "python" en version.json; sin la huella, no se arma).
PYTHON_SHA256 = {
    '3.14.7': 'd297e5ff019966817ad8502465176139f2d3d840fa4ed84b13bed399a6ab1f15',
}


def version():
    with open(os.path.join(RAIZ, 'version.json'), encoding='utf-8') as f:
        return json.load(f)


def huella(ruta):
    with open(ruta, 'rb') as f:
        contenido = f.read()
    return {'sha256': hashlib.sha256(contenido).hexdigest(), 'bytes': len(contenido)}


def python_embebido(ver):
    if ver not in PYTHON_SHA256:
        raise SystemExit(f'falta el sha256 del Python embebido {ver} en PYTHON_SHA256 (desktop/construir.py)')
    cache = os.path.join(RAIZ, 'work', f'python-{ver}-embed-amd64.zip')
    if not os.path.exists(cache):
        url = f'https://www.python.org/ftp/python/{ver}/python-{ver}-embed-amd64.zip'
        print('  bajando', url)
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        datos = urllib.request.urlopen(url, timeout=180).read()
        with open(cache, 'wb') as f:
            f.write(datos)
    with open(cache, 'rb') as f:
        datos = f.read()
    if hashlib.sha256(datos).hexdigest() != PYTHON_SHA256[ver]:
        raise SystemExit(f'el Python embebido {ver} no coincide con su sha256: {cache}')
    return datos


def programa():
    v = version()
    sueltos = sorted(os.path.relpath(p, RAIZ).replace(os.sep, '/') for p in glob.glob(os.path.join(RAIZ, 'desktop', '*.py')))
    fuera = [p for p in sueltos if p not in PROGRAMA and p != 'desktop/construir.py']
    if fuera:
        raise SystemExit(f'módulos de desktop/ que no están en PROGRAMA: {fuera}. Sumalos o sacalos.')
    destino = os.path.join(DIST, 'programa')
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    for rel in PROGRAMA + DATOS_INICIALES:
        origen = os.path.join(RAIZ, *rel.split('/'))
        if not os.path.exists(origen):
            raise SystemExit(f'falta {rel}')
        os.makedirs(os.path.dirname(os.path.join(destino, rel)), exist_ok=True)
        shutil.copy2(origen, os.path.join(destino, *rel.split('/')))
    with zipfile.ZipFile(io.BytesIO(python_embebido(v['python']))) as z:
        z.extractall(os.path.join(destino, 'python'))
    parche = os.path.join(DIST, f'mff-parche-{v["version"]}.zip')
    with zipfile.ZipFile(parche, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel in PROGRAMA:
            z.write(os.path.join(RAIZ, *rel.split('/')), rel)
    total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(destino) for f in fs)
    print(f'programa {v["version"]} (Python {v["python"]}): {total / 1048576:.1f} MB en dist/programa')
    print(f'parche: {os.path.basename(parche)} ({os.path.getsize(parche) // 1024} KB)')


def manifiesto(etiqueta):
    v = version()
    if etiqueta != 'v' + v['version']:
        raise SystemExit(f'la etiqueta {etiqueta} no coincide con version.json ({v["version"]})')
    base = f'https://github.com/{REPO}/releases/download/{etiqueta}/'
    parche = f'mff-parche-{v["version"]}.zip'
    instalador = f'TA-GUIANAEL-MFF-{v["version"]}.exe'
    for f in (parche, instalador):
        if not os.path.exists(os.path.join(DIST, f)):
            raise SystemExit(f'falta dist/{f}')
    latest = {'version': v['version'], 'notas': v['notas'], 'python': v['python'],
              'formato_datos': v['formato_datos'],
              'parche': dict(huella(os.path.join(DIST, parche)), url=base + parche),
              'instalador': dict(huella(os.path.join(DIST, instalador)), url=base + instalador)}
    with open(os.path.join(DIST, 'latest.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(latest, f, ensure_ascii=False, indent=1)
    with open(os.path.join(DIST, 'notas.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(v['notas'] + '\n\nLa app instalada se actualiza sola a esta versión: al abrirla avisa y pide '
                'confirmación. Para instalarla de cero, bajá el instalador.\n')
    print(f'latest.json {v["version"]}: parche {latest["parche"]["bytes"] // 1024} KB, '
          f'instalador {latest["instalador"]["bytes"] / 1048576:.1f} MB')


if __name__ == '__main__':
    orden = sys.argv[1:2]
    if orden == ['programa']:
        programa()
    elif orden == ['manifiesto'] and len(sys.argv) == 3:
        manifiesto(sys.argv[2])
    elif orden == ['version']:
        print(version()['version'])
    else:
        raise SystemExit(__doc__)
