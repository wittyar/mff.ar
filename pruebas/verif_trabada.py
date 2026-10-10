"""Datos por formato (#1, 1.0.30): la app baja los de la carpeta de su formato, datos/<formato>/, y no los de la raíz.
Caso de la 1.0.22 (5 de octubre de 2026): la raíz ya publicaba datos de un formato más nuevo y la app quedó trabada pidiendo
«actualizá la app». Con datos locales que la app no puede leer (de un formato anterior):
1. la raíz publica un formato más nuevo (con su carpeta) y la carpeta del formato de la app tiene los suyos: los baja de
   ahí, arranca y, adentro, avisa la versión nueva de la app (desde el repo, sin el botón del parche);
2. lo mismo sin versión nueva de la app: arranca, sin aviso;
3. sin la carpeta de su formato: se queda en la pantalla de datos y dice que todavía no hay datos publicados de su formato;
   los datos locales no cambian;
4. el 3 en inglés. Sin errores de página ni de consola.
Los datos salen de harness.DATOS (MFF_DATOS); los locales son los mismos con otro formato en data.js."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import http.server, json, os, shutil, sys, tempfile, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
from harness import Chequeo, RAIZ, DATOS
from playwright.sync_api import sync_playwright
V = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))
A = V['formato_datos']
ok = Chequeo()


def copiar_datos(dest, formato):
    """data.js, datos.json (sin imágenes, para no bajar nada) y docs/AUDITORIA.md de DATOS, con el formato dado."""
    os.makedirs(os.path.join(dest, 'docs'), exist_ok=True)
    m = json.load(open(os.path.join(DATOS, 'datos.json'), encoding='utf-8'))
    m['formato'] = formato; m['imagenes'] = []
    json.dump(m, open(os.path.join(dest, 'datos.json'), 'w'))
    shutil.copy(os.path.join(DATOS, 'data.js'), dest)
    shutil.copy(os.path.join(DATOS, 'docs', 'AUDITORIA.md'), os.path.join(dest, 'docs'))


def origen(con_su_carpeta, version):
    pub = tempfile.mkdtemp(prefix='mffpub-')
    copiar_datos(pub, A + 1)                                   # la raíz: lo del formato más nuevo
    copiar_datos(os.path.join(pub, 'datos', str(A + 1)), A + 1)
    if con_su_carpeta:
        copiar_datos(os.path.join(pub, 'datos', str(A)), A)
    json.dump({'version': version, 'python': V['python'], 'notas': 'Notas de prueba', 'formato_datos': A + 1,
               'parche': {'url': 'x', 'sha256': '0' * 64, 'bytes': 1},
               'instalador': {'url': 'https://example.invalid/instalador.exe', 'sha256': '0' * 64, 'bytes': 1}},
              open(os.path.join(pub, 'latest.json'), 'w'))
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=pub, **k)
        def log_message(self, *a): pass
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f'http://127.0.0.1:{srv.server_port}/'


def carpeta(lang='es'):
    """Datos locales de un formato anterior: los de DATOS con el formato de data.js y de datos.json cambiado."""
    d = tempfile.mkdtemp(prefix='mffdatos-')
    copiar_datos(d, A - 1)
    js = open(os.path.join(d, 'data.js'), encoding='utf-8').read()
    otro = js.replace(f'"formato": {A}}}', f'"formato": {A - 1}}}', 1)
    assert otro != js
    open(os.path.join(d, 'data.js'), 'w', encoding='utf-8', newline='\n').write(otro)
    os.symlink(os.path.join(DATOS, 'images'), os.path.join(d, 'images'))
    if lang == 'en':
        json.dump({'prefs': {'lang': 'en'}}, open(os.path.join(d, 'capa.json'), 'w'))
    return d


def caso(p, local, org):
    srv, url = harness.levantar(local, org)
    errores = []
    try:
        b = p.chromium.launch(); pg = b.new_page()
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.goto(url)
        pg.wait_for_function("() => { const p = document.querySelector('.fatal p'); return (p && /publicados|published/.test(p.textContent)) || document.querySelector('.ccard'); }", timeout=60000)
        pg.wait_for_timeout(1500)
        r = pg.evaluate("""() => ({ titulo: (document.querySelector('.fatal h1') || {}).textContent || null,
          texto: (document.querySelector('.fatal p') || {}).textContent || null,
          avisos: (document.querySelector('#avisos') || {}).innerText || '',
          boton: !!document.querySelector('#avisos [data-a="actualizarApp"]'),
          formato: window.MFF_VERSION && window.MFF_VERSION.formato,
          roster: !!document.querySelector('.ccard') })""")
        b.close()
        return r, errores
    finally:
        srv.terminate(); srv.wait()


with sync_playwright() as p:
    d = carpeta()
    r, e = caso(p, d, origen(True, '9.9.9'))
    local = json.load(open(os.path.join(d, 'datos.json')))
    ok('1 formato más nuevo en la raíz: baja los de su carpeta, arranca y avisa la versión nueva',
       r['roster'] and r['formato'] == A and local['formato'] == A and 'Versión 9.9.9 disponible.' in r['avisos'] and not e, (r, e))
    r, e = caso(p, carpeta(), origen(True, V['version']))
    ok('2 sin versión nueva de la app: arranca, sin avisos', r['roster'] and r['formato'] == A and not r['avisos'].strip() and not e, (r, e))
    d = carpeta()
    antes = {f: open(os.path.join(d, f), 'rb').read() for f in ('data.js', 'datos.json')}
    r, e = caso(p, d, origen(False, '9.9.9'))
    ok('3 sin la carpeta de su formato: la pantalla de datos lo dice',
       r['titulo'] == 'Actualizando los datos del juego' and not r['roster']
       and f'No se pudieron bajar los datos nuevos: todavía no hay datos publicados de formato {A}' in (r['texto'] or '') and not e, (r, e))
    ok('3 los datos locales no cambian', all(open(os.path.join(d, f), 'rb').read() == b_ for f, b_ in antes.items())
       and not [f for f in os.listdir(d) if f.endswith('.nuevo')])
    r, e = caso(p, carpeta('en'), origen(False, '9.9.9'))
    ok('4 inglés', r['titulo'] == 'Updating game data' and 'This app version uses data in another format' in (r['texto'] or '') and not e, (r, e))
ok.fin()
