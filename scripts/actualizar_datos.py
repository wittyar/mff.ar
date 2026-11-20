#!/usr/bin/env python3
"""Actualiza los datos publicados desde la PC de Ezequiel, sin GitHub Actions (Ezequiel, 20 de noviembre de 2026).

  python scripts/actualizar_datos.py        (en Windows, también ActualizarDatos.bat)

Hace lo mismo que el workflow «Actualizar datos MFF» (.github/workflows/actualizar.yml): baja las fuentes, corre el
build y, si cambió algo, commitea «Datos actualizados AAAA-MM-DD» (fecha UTC, como el workflow) en main con la
identidad git de quien lo corre y lo empuja. Los pasos y las rutas del commit son los del workflow, copiados: si
cambian ahí, cambian acá (CLAUDE.md, «Datos»).

Antes de empezar: git en el PATH, Python 3.12 o más, la rama main, sin cambios en archivos seguidos ni archivos nuevos
donde escribe el build (irían al commit), y main igual a origin/main después de `git pull --ff-only`. Los archivos sin
seguir de otras partes (el bundle de la entrega, por ejemplo) no se tocan: se listan en un aviso. Si algo no está,
corta diciendo qué. Si un paso falla, corta sin commitear: lo que alcanzó a escribir queda en el árbol para mirarlo.
Todo lo que muestra queda también en work/actualizar_datos.log.
"""
import datetime, os, shutil, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_MINIMO = (3, 12)          # el del workflow; los scripts no usan nada fuera de la biblioteca estándar
PASOS = [
    ['scripts/fetch_all.py', '--no-portraits'],
    ['scripts/parse_instinto.py'],
    ['scripts/foro.py'],
    ['scripts/cafe.py'],
    ['scripts/build.py'],
]
RUTAS = ['data.js', 'datos.json', 'datos', 'mff-thanosvibs-import.json', 'docs/AUDITORIA.md', 'docs/CATALOGO.md',
         'docs/COMPLETITUD.md', 'docs/HISTORICO.md', 'docs/NOTAS_COREANO.md', 'fuentes/guia-armado', 'fuentes/foro',
         'fuentes/cafe']
# Los scripts leen y escriben UTF-8 (en Windows, sin esto, Python usa cp1252) y su salida se lee en UTF-8.
ENTORNO = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONUNBUFFERED='1')
VOLVER = 'Para dejar el árbol como estaba: git reset --hard HEAD y git clean -fd -- ' + ' '.join(RUTAS)
LOG = None


def decir(texto):
    sys.stdout.write(texto + '\n')
    sys.stdout.flush()
    LOG.write(texto + '\n')
    LOG.flush()


def cortar(texto):
    decir('CORTA: ' + texto)
    sys.exit(1)


def correr(args):
    """Corre un comando desde la raíz del repo, mostrando y anotando su salida; devuelve su código."""
    decir('> ' + ' '.join(args))
    p = subprocess.Popen(args, cwd=RAIZ, env=ENTORNO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for linea in p.stdout:
        decir(linea.decode('utf-8', errors='replace').rstrip('\r\n'))
    return p.wait()


def git(*args):
    """Un git de consulta: su salida, o corta con su error."""
    r = subprocess.run(['git', '-C', RAIZ, *args], capture_output=True)
    if r.returncode:
        cortar(f'git {" ".join(args)}: {r.stderr.decode("utf-8", errors="replace").strip()}')
    return r.stdout.decode('utf-8', errors='replace').rstrip()


def estado():
    """git status como [(XY, ruta)], con los archivos sin seguir uno por uno."""
    r = subprocess.run(['git', '-C', RAIZ, 'status', '--porcelain', '-z', '--untracked-files=all'], capture_output=True)
    if r.returncode:
        cortar(f'git status: {r.stderr.decode("utf-8", errors="replace").strip()}')
    partes = r.stdout.decode('utf-8', errors='replace').split('\0')
    lineas, i = [], 0
    while i < len(partes):
        if partes[i]:
            lineas.append((partes[i][:2], partes[i][3:]))
            if partes[i][0] in 'RC':        # un renombre trae después la ruta de origen
                i += 1
        i += 1
    return lineas


def en_rutas(ruta):
    return any(ruta == r or ruta.startswith(r + '/') for r in RUTAS)


def main():
    if sys.version_info < PYTHON_MINIMO:
        cortar(f'hace falta Python {".".join(map(str, PYTHON_MINIMO))} o más (este es {sys.version.split()[0]}): '
               'instalalo de https://www.python.org/downloads/')
    if not shutil.which('git'):
        cortar('no está git en el PATH: instalá Git para Windows (https://git-scm.com/download/win)')
    if git('rev-parse', '--abbrev-ref', 'HEAD') != 'main':
        cortar('la rama no es main: git switch main')
    antes = estado()
    cambios = [f'{xy} {r}' for xy, r in antes if xy != '??']
    if cambios:
        cortar('hay cambios sin commitear (git status):\n' + '\n'.join(cambios))
    sueltos = [r for xy, r in antes if xy == '??']
    if any(en_rutas(r) for r in sueltos):
        cortar('hay archivos sin seguir donde escribe el build (irían al commit de datos):\n'
               + '\n'.join(r for r in sueltos if en_rutas(r)))
    if sueltos:
        decir('AVISO: archivos sin seguir fuera de los datos (no se tocan ni se commitean): ' + ', '.join(sueltos))
    if git('rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}') != 'origin/main':
        cortar('main no sigue a origin/main: git branch -u origin/main')
    if correr(['git', 'pull', '--ff-only']):
        cortar('git pull --ff-only no pudo traer origin/main: main y origin/main se separaron')
    adelante = git('rev-list', '--oneline', 'origin/main..HEAD')
    if adelante:
        cortar('main tiene commits que origin/main no tiene (empujalos o sacalos antes):\n' + adelante)

    for paso in PASOS:
        codigo = correr([sys.executable, *paso])
        if codigo:
            cortar(f'{paso[0]} terminó con el código {codigo}: no se commitea nada. {VOLVER}.')

    if correr(['git', 'add', '--', *RUTAS]):
        cortar(f'git add falló: no se commitea nada. {VOLVER}.')
    fuera = [f'{xy} {r}' for xy, r in estado() if (xy[1] != ' ' and xy != '??') or (xy == '??' and r not in sueltos)]
    if fuera:
        cortar('el build cambió archivos que el commit de datos no lleva: no se commitea nada.\n'
               + '\n'.join(fuera) + f'\n{VOLVER}.')
    if subprocess.run(['git', '-C', RAIZ, 'diff', '--cached', '--quiet']).returncode == 0:
        decir('Sin cambios: no hay nada que commitear.')
        return
    mensaje = 'Datos actualizados ' + datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    if correr(['git', 'commit', '-m', mensaje]):
        cortar(f'git commit falló: los cambios quedan en el índice, sin commitear. {VOLVER}.')
    if correr(['git', 'push']):
        cortar(f'git push falló: el commit «{mensaje}» quedó hecho y sin empujar. Cuando se pueda: git push.')
    decir(f'Listo: «{mensaje}» empujado a origin/main.')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    os.makedirs(os.path.join(RAIZ, 'work'), exist_ok=True)
    with open(os.path.join(RAIZ, 'work', 'actualizar_datos.log'), 'a', encoding='utf-8') as LOG:
        decir(f'\n=== {datetime.datetime.now().isoformat(timespec="seconds")} scripts/actualizar_datos.py ===')
        main()
