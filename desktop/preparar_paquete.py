#!/usr/bin/env python3
"""Arma la carpeta que se le pasa a otra persona, con Python adentro.

Uso: python desktop/preparar_paquete.py [--sin-imagenes]

Deja dist/TA-GUIANAEL-MFF/ con la app, el pipeline, el lanzador y un Python
embebido de python.org (un ZIP sin instalador: no pide admin, no toca el PATH ni el
registro). Quien lo recibe descomprime y hace doble clic en MFF.bat, sin instalar nada.

Se elige el embebido y no un .exe de PyInstaller a proposito: un ejecutable sin firmar
dispara el aviso de SmartScreen y es un falso positivo habitual de varios antivirus.
"""
import hashlib, io, os, shutil, sys, urllib.request, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RAIZ, 'dist', 'TA-GUIANAEL-MFF')
PY_VER = '3.12.8'
PY_URL = f'https://www.python.org/ftp/python/{PY_VER}/python-{PY_VER}-embed-amd64.zip'
CACHE = os.path.join(RAIZ, 'work', f'python-{PY_VER}-embed-amd64.zip')

APP = ['index.html', 'app.js', 'styles.css', 'data.js', 'MFF.bat', 'README.md']
CARPETAS = ['scripts', 'desktop']

def bajar_python():
    if os.path.exists(CACHE):
        print(f'  python embebido: ya estaba en cache ({os.path.getsize(CACHE)//1024//1024} MB)')
        return open(CACHE, 'rb').read()
    print(f'  bajando {PY_URL}')
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    datos = urllib.request.urlopen(PY_URL, timeout=180).read()
    open(CACHE, 'wb').write(datos)
    return datos

def main():
    sin_imagenes = '--sin-imagenes' in sys.argv
    if os.path.exists(DEST):
        shutil.rmtree(DEST)
    os.makedirs(DEST)

    print('Armando el paquete en', DEST)
    for f in APP:
        origen = os.path.join(RAIZ, f)
        if not os.path.exists(origen):
            raise SystemExit(f'ERROR: falta {f} en el repo')
        shutil.copy2(origen, DEST)
    for c in CARPETAS:
        shutil.copytree(os.path.join(RAIZ, c), os.path.join(DEST, c),
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    print(f'  app y pipeline: {len(APP)} archivos + {len(CARPETAS)} carpetas')

    imgs = os.path.join(RAIZ, 'images')
    if sin_imagenes:
        print('  imagenes: omitidas (--sin-imagenes); se bajan con el boton de Ajustes')
    elif os.path.isdir(imgs):
        shutil.copytree(imgs, os.path.join(DEST, 'images'))
        n = sum(len(f) for _, _, f in os.walk(os.path.join(DEST, 'images')))
        print(f'  imagenes: {n} archivos')
    else:
        print('  AVISO: no hay carpeta images/; el paquete sale sin retratos')

    datos = bajar_python()
    sha = hashlib.sha256(datos).hexdigest()
    with zipfile.ZipFile(io.BytesIO(datos)) as z:
        if not any(n.endswith('python.exe') for n in z.namelist()):
            raise SystemExit('ERROR: el ZIP bajado no parece el Python embebido de Windows')
        z.extractall(os.path.join(DEST, 'python'))
    print(f'  python {PY_VER} embebido (sha256 {sha[:16]}…)')

    total = sum(os.path.getsize(os.path.join(r, f))
                for r, _, fs in os.walk(DEST) for f in fs)
    print(f'\nListo: {DEST}')
    print(f'  {total/1024/1024:.1f} MB en {sum(len(f) for _,_,f in os.walk(DEST))} archivos')
    print('  Comprimi esa carpeta y pasala. Quien la reciba: descomprimir y doble clic en MFF.bat.')

if __name__ == '__main__':
    main()
