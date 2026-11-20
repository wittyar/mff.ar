#!/usr/bin/env python3
"""Arma lo que publica cada versión de TA GUIANAEL MFF. La release se arma en la sesión de Claude
(Linux, con Wine) y la sube Ezequiel desde su PC; GitHub Actions no se usa (Ezequiel, 20 de
noviembre de 2026).

  python desktop/construir.py release vX.Y.Z      todo, en la sesión de Claude: verifica, programa,
                                                  instalador (Inno Setup bajo Wine) y manifiesto
  python desktop/construir.py subir vX.Y.Z COMMIT  en la PC de Ezequiel: verifica dist/ contra latest.json
                                                  y crea la release con gh, con la etiqueta en COMMIT
  python desktop/construir.py programa            dist/programa/ y el parche
  python desktop/construir.py manifiesto vX.Y.Z   dist/latest.json y dist/notas.md
  python desktop/construir.py formato DATOS.json   corta si los datos no son del formato de version.json
  python desktop/construir.py formato_datos        el formato de datos de version.json
  python desktop/construir.py version              la versión de version.json

dist/programa/ es lo que instala el instalador (desktop/instalador.iss): los archivos del
programa, los datos iniciales (se copian a la carpeta de datos en el primer arranque) y
el Python embebido de python.org, verificado contra su sha256.

El parche (dist/mff-parche-X.Y.Z.zip) lleva solo los archivos del programa: es lo que la
app instalada baja y aplica sola cuando sale una versión con el mismo Python.
latest.json es lo que la app consulta para saber si hay versión nueva.

Los archivos de texto del programa van como están en git (LF). Hasta la 1.0.57 la release salía de
Actions en Windows, donde git los entregaba con CRLF: el contenido es el mismo.
"""
import glob, hashlib, io, json, os, shutil, subprocess, sys, urllib.request, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(RAIZ, 'dist')
REPO = 'wittyar/mff.ar'

# El programa: lo que instala el instalador y lo que puede traer un parche (tiene que
# coincidir con DEL_PROGRAMA de actualizador.py).
PROGRAMA = ['index.html', 'app.js', 'styles.css', 'version.json', 'desktop/mff.ico',
            'desktop/lanzador.py', 'desktop/servidor.py', 'desktop/actualizador.py',
            'desktop/rescate.py']
# Datos del primer arranque: después se actualizan solos desde GitHub.
DATOS_INICIALES = ['data.js', 'datos.json', 'docs/AUDITORIA.md']
# Python embebido de python.org por versión, con su sha256 (se agrega al cambiar
# "python" en version.json; sin la huella, no se arma).
PYTHON_SHA256 = {
    '3.14.7': 'd297e5ff019966817ad8502465176139f2d3d840fa4ed84b13bed399a6ab1f15',
}
# Inno Setup, de su release oficial y verificado contra su sha256 antes de ejecutarlo (los mismos que usaba
# publicar.yml).
INNO_VERSION = '6.7.3'
INNO_URL = 'https://github.com/jrsoftware/issrc/releases/download/is-6_7_3/innosetup-6.7.3.exe'
INNO_SHA256 = '9c73c3bae7ed48d44112a0f48e66742c00090bdb5bef71d9d3c056c66e97b732'
# Wine de Ubuntu 24.04 (9.0): wine64 y wine32:i386, porque el instalador de Inno Setup es de 32 bits. El prefijo es
# el de pruebas/verif_wine.py, que prueba el programa instalado ahí.
WINE = '/usr/lib/wine/wine64'
PREFIJO_WINE = '/tmp/wine64pfx'
ISCC = r'C:\InnoSetup\ISCC.exe'


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


def formato(publicados):
    """La versión sale solo con los datos que pide (version.json, formato_datos): los del commit etiquetado (datos.json,
    que van en el instalador como datos del primer arranque) y los publicados, el datos.json de la carpeta de su formato
    en main (datos/<formato>/datos.json, de donde los baja la app; `publicados`, una copia). Si no, la app nueva queda esperando datos que no hay (la 1.0.17: la etiqueta salió antes que los datos) o
    trabada (la 1.0.22: la etiqueta fue sobre el commit de la versión, con datos de formato 8, y main ya publicaba los de
    formato 10)."""
    pide = version()['formato_datos']
    with open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8') as f:
        del_commit = json.load(f)['formato']
    with open(publicados, encoding='utf-8') as f:
        de_main = json.load(f)['formato']
    if del_commit != pide:
        raise SystemExit(f'los datos de este commit son de formato {del_commit} y version.json pide el {pide}: la release '
                         f'se arma sobre el commit «Datos actualizados» de formato {pide}')
    if de_main != pide:
        raise SystemExit(f'los datos publicados (main) son de formato {de_main} y version.json pide el {pide}: esta versión '
                         'no podría usarlos; se publica la versión que los lee')
    print(f'datos: formato {pide}, el del commit y el publicado')


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


def git(*args):
    r = subprocess.run(['git', '-C', RAIZ, *args], capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode:
        raise SystemExit(f'git {" ".join(args)}: {r.stderr.strip()}')
    return r.stdout.strip()


def antecesor(a, b):
    """Si el commit a está en la historia de b."""
    return subprocess.run(['git', '-C', RAIZ, 'merge-base', '--is-ancestor', a, b]).returncode == 0


def entorno_wine():
    """Wine 9.0 se cae al arrancar («free(): invalid pointer») si está definida TMPDIR: se corre sin ella."""
    env = {k: v for k, v in os.environ.items() if k != 'TMPDIR'}
    env.update(WINEPREFIX=PREFIJO_WINE, WINEDEBUG='-all')
    return env


def inno_setup():
    """Deja Inno Setup en el prefijo de Wine: si no está, baja el instalador oficial a work/, lo verifica y lo instala. El
    instalador abre su ventana aunque vaya en silencio: corre en una pantalla virtual (xvfb-run)."""
    for prog, paquete in ((WINE, 'wine64 y wine32:i386 (antes, dpkg --add-architecture i386)'), ('xvfb-run', 'xvfb')):
        if not shutil.which(prog):
            raise SystemExit(f'falta {prog}: instalá {paquete} con apt-get')
    if os.path.exists(os.path.join(PREFIJO_WINE, 'drive_c', 'InnoSetup', 'ISCC.exe')):
        return
    cache = os.path.join(RAIZ, 'work', os.path.basename(INNO_URL))
    if not os.path.exists(cache):
        print('  bajando', INNO_URL)
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        datos = urllib.request.urlopen(INNO_URL, timeout=180).read()
        with open(cache, 'wb') as f:
            f.write(datos)
    if huella(cache)['sha256'] != INNO_SHA256:
        raise SystemExit(f'el instalador de Inno Setup no coincide con su sha256: {cache}. No se ejecuta.')
    subprocess.run(['xvfb-run', '-a', WINE, cache, '/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', '/CURRENTUSER',
                    r'/DIR=C:\InnoSetup'], env=entorno_wine(), check=True)
    if not os.path.exists(os.path.join(PREFIJO_WINE, 'drive_c', 'InnoSetup', 'ISCC.exe')):
        raise SystemExit(f'Inno Setup no quedó instalado en {PREFIJO_WINE}')


def instalador():
    """dist/TA-GUIANAEL-MFF-X.Y.Z.exe: desktop/instalador.iss compilado con ISCC bajo Wine, sobre dist/programa/."""
    v = version()['version']
    inno_setup()
    r = subprocess.run([WINE, ISCC, f'/DAppVersion={v}', r'desktop\instalador.iss'], cwd=RAIZ, env=entorno_wine(),
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    salida = [l for l in r.stdout.splitlines() + r.stderr.splitlines() if l.strip() and not l.strip().startswith('Compressing:')]
    if r.returncode:
        raise SystemExit('ISCC falló:\n' + '\n'.join(salida[-30:]))
    if f'Compiler engine version: Inno Setup {INNO_VERSION}' not in r.stdout:
        raise SystemExit(f'el ISCC de {PREFIJO_WINE} no es Inno Setup {INNO_VERSION}: borrá C:\\InnoSetup del prefijo y '
                         'volvé a correr')
    exe = os.path.join(DIST, f'TA-GUIANAEL-MFF-{v}.exe')
    if not os.path.exists(exe):
        raise SystemExit(f'ISCC terminó sin dejar {os.path.relpath(exe, RAIZ)}')
    print(f'instalador: {os.path.basename(exe)} ({os.path.getsize(exe) / 1048576:.1f} MB), Inno Setup {INNO_VERSION} bajo Wine')


def release(etiqueta):
    """Lo que publicaba publicar.yml, en la sesión de Claude: las mismas verificaciones, el programa y el parche, el
    instalador y latest.json. Se arma sobre la punta de main, limpia, con origin/main adentro: es lo que Ezequiel empuja
    antes de subir la release, así que los datos publicados de su formato (datos/<formato>/ de main) van a ser los de
    este commit."""
    v = version()
    if etiqueta != 'v' + v['version']:
        raise SystemExit(f'la etiqueta {etiqueta} no coincide con version.json ({v["version"]})')
    if git('status', '--porcelain'):
        raise SystemExit('hay cambios sin commitear: la release se arma sobre un commit')
    if git('rev-parse', '--abbrev-ref', 'HEAD') != 'main':
        raise SystemExit('la release se arma sobre main')
    git('fetch', 'origin', 'main')
    if not antecesor('origin/main', 'HEAD'):
        raise SystemExit('origin/main tiene commits que este main no tiene: main tiene que poder empujarse sin merge')
    formato(os.path.join(RAIZ, 'datos', str(v['formato_datos']), 'datos.json'))
    programa()
    instalador()
    manifiesto(etiqueta)
    commit = git('rev-parse', 'HEAD')
    print(f'\nrelease {etiqueta} armada sobre {commit}:')
    for f in (f'TA-GUIANAEL-MFF-{v["version"]}.exe', f'mff-parche-{v["version"]}.zip', 'latest.json', 'notas.md'):
        h = huella(os.path.join(DIST, f))
        print(f'  dist/{f}  {h["bytes"]} bytes  sha256 {h["sha256"]}')
    print(f'\nla sube Ezequiel, con esos archivos en dist\\ y main empujado:\n'
          f'  python desktop\\construir.py subir {etiqueta} {commit}')


def subir(etiqueta, commit):
    """En la PC de Ezequiel, con lo que armó `release` en dist/: verifica el instalador y el parche contra latest.json,
    que el commit esté en origin/main y sea de esa versión, y crea la release con gh (la etiqueta va sobre el commit).
    Crear la etiqueta vX.Y.Z en GitHub dispara publicar.yml mientras ese workflow siga activo."""
    with open(os.path.join(DIST, 'latest.json'), encoding='utf-8') as f:
        latest = json.load(f)
    ver = latest['version']
    if etiqueta != 'v' + ver:
        raise SystemExit(f'la etiqueta {etiqueta} no coincide con dist/latest.json ({ver})')
    archivos = {'instalador': f'TA-GUIANAEL-MFF-{ver}.exe', 'parche': f'mff-parche-{ver}.zip'}
    for clave, nombre in archivos.items():
        ruta = os.path.join(DIST, nombre)
        if not os.path.exists(ruta):
            raise SystemExit(f'falta dist/{nombre}')
        if huella(ruta) != {k: latest[clave][k] for k in ('sha256', 'bytes')}:
            raise SystemExit(f'dist/{nombre} no es el que anuncia dist/latest.json: no se sube nada')
    if not os.path.exists(os.path.join(DIST, 'notas.md')):
        raise SystemExit('falta dist/notas.md')
    if not shutil.which('gh'):
        raise SystemExit('falta gh (GitHub CLI)')
    commit = git('rev-parse', '--verify', commit + '^{commit}')
    git('fetch', 'origin', 'main')
    if not antecesor(commit, 'origin/main'):
        raise SystemExit(f'{commit} no está en origin/main: primero se empuja main (paso «1. Código»)')
    if json.loads(git('show', f'{commit}:version.json'))['version'] != ver:
        raise SystemExit(f'version.json de {commit} no es la {ver}')
    subprocess.run(['gh', 'release', 'create', etiqueta, os.path.join(DIST, archivos['instalador']),
                    os.path.join(DIST, archivos['parche']), os.path.join(DIST, 'latest.json'), '--repo', REPO,
                    '--target', commit, '--title', f'TA GUIANAEL MFF {ver}', '--notes-file', os.path.join(DIST, 'notas.md')],
                   check=True)


if __name__ == '__main__':
    orden = sys.argv[1:2]
    if orden == ['release'] and len(sys.argv) == 3:
        release(sys.argv[2])
    elif orden == ['subir'] and len(sys.argv) == 4:
        subir(sys.argv[2], sys.argv[3])
    elif orden == ['programa']:
        programa()
    elif orden == ['manifiesto'] and len(sys.argv) == 3:
        manifiesto(sys.argv[2])
    elif orden == ['formato'] and len(sys.argv) == 3:
        formato(sys.argv[2])
    elif orden == ['version']:
        print(version()['version'])
    elif orden == ['formato_datos']:
        print(version()['formato_datos'])
    else:
        raise SystemExit(__doc__)
