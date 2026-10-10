"""desktop/lanzador.py: instancia única, siembra de datos, latido y apagado.

1  primer arranque con carpeta de datos vacía: copia data.js y docs/ y abre
2  con una ventana latiendo sigue vivo más allá de la espera
3  segundo arranque con la misma carpeta: reusa la instancia (mismo URL) y termina
4  otra carpeta de programa con la misma carpeta de datos: error claro
5  al cerrar la ventana se apaga solo, borra instancia.json y sale con 0
6  si nadie late nunca, se apaga solo
7  un proceso muerto de golpe (kill -9) no bloquea el próximo arranque
8  registro.txt anota arranque y apagado
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, shutil, signal, subprocess, sys, tempfile, time
from playwright.sync_api import sync_playwright

RAIZ = RAIZ
ESPERA = 6
fallas = []
def chequear(nombre, cond, detalle=''):
    print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
    if not cond: fallas.append(nombre)

def lanzar(datos, raiz=RAIZ, extra=()):
    p = subprocess.Popen([sys.executable, os.path.join(raiz, 'desktop', 'lanzador.py'), '--datos', datos,
                          '--sin-ventana', '--espera-latido', str(ESPERA), *extra],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return p

def url_de(p, timeout=20):
    fin = time.time() + timeout
    salida = []
    while time.time() < fin:
        linea = p.stdout.readline()
        if not linea: break
        salida.append(linea)
        if 'abriendo' in linea:
            return linea.split('abriendo')[1].strip(), salida
    return None, salida

D = tempfile.mkdtemp(prefix='mff-lanz-')
os.symlink(os.path.join(RAIZ, 'images'), os.path.join(D, 'images'))   # que no baje 77 MB de thanosvibs
with sync_playwright() as pw:
    b = pw.chromium.launch()
    p1 = lanzar(D)
    url, _ = url_de(p1)
    chequear('1 primer arranque abre y siembra datos', url and os.path.exists(os.path.join(D, 'data.js'))
             and os.path.exists(os.path.join(D, 'docs', 'AUDITORIA.md')), url)
    page = b.new_page(); page.goto(url); page.wait_for_selector('.ccard')
    time.sleep(ESPERA + 4)
    chequear('2 con una ventana latiendo sigue vivo', p1.poll() is None)

    p2 = lanzar(D)
    url2, salida2 = url_de(p2)
    p2.wait(timeout=10)
    chequear('3 segundo arranque reusa la instancia', url2 == url and p2.returncode == 0, (url2, p2.returncode))

    otra = tempfile.mkdtemp(prefix='mff-prog-')
    for f in ('index.html', 'app.js', 'styles.css', 'data.js', 'datos.json', 'version.json'):
        shutil.copy(os.path.join(RAIZ, f), otra)
    shutil.copytree(os.path.join(RAIZ, 'desktop'), os.path.join(otra, 'desktop'))
    shutil.copytree(os.path.join(RAIZ, 'scripts'), os.path.join(otra, 'scripts'))
    p3 = lanzar(D, raiz=otra)
    out3 = p3.communicate(timeout=20)[0]
    chequear('4 otra carpeta de programa: error claro', p3.returncode == 1 and 'desde otra carpeta' in out3, out3.strip()[-160:])

    incompleta = tempfile.mkdtemp(prefix='mff-incompleta-')
    shutil.copytree(os.path.join(otra, 'desktop'), os.path.join(incompleta, 'desktop'))
    p9 = lanzar(tempfile.mkdtemp(prefix='mff-d9-'), raiz=incompleta)
    out9 = p9.communicate(timeout=20)[0]
    chequear('9 programa incompleto: error claro', p9.returncode == 1 and 'No se pudo abrir' in out9 and 'incompleto' in out9,
             out9.strip().splitlines()[-1][:160])

    page.close()
    t0 = time.time()
    try:
        p1.wait(timeout=ESPERA + 10)
    except subprocess.TimeoutExpired:
        pass
    chequear('5 al cerrar la ventana se apaga solo', p1.returncode == 0 and not os.path.exists(os.path.join(D, 'instancia.json')),
             f'código {p1.returncode}, {time.time() - t0:.1f} s')

    p4 = lanzar(D)
    url4, _ = url_de(p4)
    t0 = time.time()
    try:
        p4.wait(timeout=ESPERA + 10)
    except subprocess.TimeoutExpired:
        pass
    chequear('6 sin ninguna ventana se apaga solo', p4.returncode == 0, f'{time.time() - t0:.1f} s')

    p5 = lanzar(D)
    url5, _ = url_de(p5)
    os.kill(p5.pid, signal.SIGKILL); p5.wait()
    p6 = lanzar(D)
    url6, salida6 = url_de(p6)
    chequear('7 tras un kill -9 arranca una instancia nueva', url6 is not None and p6.poll() is None, (url5, url6))
    p6.terminate(); p6.wait()

    reg = open(os.path.join(D, 'registro.txt'), encoding='utf-8').read()
    chequear('8 registro.txt anota arranque y apagado', 'datos en' in reg and 'se apaga' in reg, reg.count('\n'))
    b.close()
os.remove(os.path.join(D, 'images')); shutil.rmtree(D); shutil.rmtree(otra)
print('\nFALLAS:', fallas or 'ninguna')
