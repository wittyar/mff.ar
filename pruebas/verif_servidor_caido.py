"""Verifica el aviso de servidor de escritorio cerrado.

A  servidor vivo: pool completo, sin aviso.
A2 servidor vivo y una imagen que no existe: sin aviso (es un archivo faltante, no el servidor).
B  servidor cerrado con la pestaña abierta: aviso arriba, en cualquier vista; sin bucle de consultas.
C  HTML servido por un estático cualquiera (sin /api): pantalla de error.
D  file://: pantalla que explica cómo abrirla.
M  ancho de celular con el aviso: sin scroll horizontal.
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import os, shutil, subprocess, sys, tempfile, time
from playwright.sync_api import sync_playwright

RAIZ = RAIZ
OUT = PRUEBAS

DATOS = tempfile.mkdtemp(prefix='mff-caido-')
os.symlink(os.path.join(RAIZ, 'images'), os.path.join(DATOS, 'images'))
def levantar():
    srv = subprocess.Popen([sys.executable, 'desktop/lanzador.py', '--datos', DATOS, '--sin-ventana'], cwd=RAIZ,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for _ in range(40):
        linea = srv.stdout.readline()
        if 'abriendo' in linea:
            return srv, linea.split('abriendo')[1].strip()
    raise SystemExit('el servidor no arrancó')

CONTAR = """() => {
  const imgs = [...document.querySelectorAll('.ccard img')];
  return {imgs: imgs.length, ok: imgs.filter(i => i.complete && i.naturalWidth > 0).length,
          rotas: imgs.filter(i => i.complete && i.naturalWidth === 0).length,
          aviso: (document.querySelector('.srvcaido') || {}).innerText || null};
}"""

def nuevo(b, url, ancho=1300):
    ctx = b.new_context(viewport={'width': ancho, 'height': 900})
    page = ctx.new_page()
    errores, estados = [], []
    page.on('pageerror', lambda e: errores.append(str(e)))
    page.on('console', lambda m: m.type == 'error' and errores.append('console: ' + m.text + ' @ ' + str(m.location.get('url'))))
    page.on('request', lambda r: '/api/estado' in r.url and estados.append(r.url))
    page.goto(url); page.wait_for_selector('.ccard'); page.wait_for_timeout(800)
    return ctx, page, errores, estados

def armador(page):
    # 1.0.25: el armador con su grilla de retratos pasó a la mesa; una página nueva del roster carga 36 retratos.
    page.wait_for_selector('.ccard'); page.click('[data-a="page"][data-p="1"]')
    page.wait_for_timeout(2500)
    return page.evaluate(CONTAR)

fallas = []
def chequear(nombre, cond, detalle):
    print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
    if not cond: fallas.append(nombre)

with sync_playwright() as p:
    b = p.chromium.launch()
    srv, url = levantar()

    ctx, page, err, est = nuevo(b, url)
    r = armador(page)
    chequear('A servidor vivo: los 36 retratos y sus íconos, sin aviso', r['imgs'] >= 36 and r['ok'] == r['imgs'] and not r['aviso'], r)
    page.evaluate("document.querySelector('main').insertAdjacentHTML('beforeend', '<img src=\"images/no-existe.png\">')")
    page.wait_for_timeout(1500)
    aviso = page.evaluate("!!document.querySelector('.srvcaido')")
    chequear('A2 archivo faltante con servidor vivo: sin aviso', not aviso, f'consultas /api/estado: {len(est)}')
    chequear('A/A2 sin errores de página', not [e for e in err if 'no-existe' not in e], err)
    ctx.close()

    ctx, page, err, est = nuevo(b, url)
    antes = len(est)
    srv.terminate(); srv.wait()
    r = armador(page)
    consultas = len(est) - antes
    chequear('B servidor cerrado: aviso arriba', bool(r['aviso']), r)
    chequear('B una sola consulta por la tanda de errores', consultas == 1, f'consultas tras cerrar: {consultas}')
    page.screenshot(path=f'{OUT}/verif_servidor_caido.png', clip={'x': 0, 'y': 0, 'width': 1300, 'height': 520})
    page.click('[data-a="back"]'); page.wait_for_timeout(600)
    en_roster = page.evaluate("!!document.querySelector('#avisos .srvcaido')")
    chequear('B el aviso sigue en otras vistas (roster)', en_roster, '')
    page.click('[data-a="lang"]'); page.wait_for_timeout(300)
    chequear('B aviso en inglés', 'The app program closed.' in (page.evaluate("document.querySelector('.srvcaido').innerText")), '')
    page.click('[data-a="lang"]')
    page.wait_for_timeout(1500)
    chequear('B sin bucle de consultas', len(est) - antes == 1, f'consultas totales tras cerrar: {len(est) - antes}')
    ctx.close()

    # M: celular con aviso
    srv, url = levantar()
    ctx, page, err, est = nuevo(b, url, ancho=390)
    srv.terminate(); srv.wait()
    page.wait_for_selector('.ccard'); page.click('[data-a="page"][data-p="1"]'); page.wait_for_timeout(2500)
    ancho = page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
    chequear('M celular: aviso y sin scroll horizontal', page.evaluate("!!document.querySelector('.srvcaido')") and ancho[0] <= ancho[1], ancho)
    page.screenshot(path=f'{OUT}/verif_servidor_caido_celular.png', clip={'x': 0, 'y': 0, 'width': 390, 'height': 700})
    ctx.close()

    # C: servida por un estático cualquiera (sin /api): no arranca y dice por qué
    est_srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8798', '--bind', '127.0.0.1'], cwd=RAIZ,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    page = b.new_page(); page.goto('http://127.0.0.1:8798/index.html'); page.wait_for_selector('.fatal')
    chequear('C estático: pantalla de error en vez de app a medias', page.locator('.ccard').count() == 0 and 'acceso directo' in page.evaluate("document.querySelector('.fatal').innerText").lower(),
             page.evaluate("document.querySelector('.fatal').innerText")[:120])
    page.close(); est_srv.terminate()

    # D: file://
    page = b.new_page(); page.goto(f'file://{RAIZ}/index.html'); page.wait_for_selector('.fatal')
    chequear('D file://: explica cómo abrirla', 'acceso directo' in page.evaluate("document.querySelector('.fatal').innerText").lower(), '')
    page.close()
    b.close()

print('\nFALLAS:', fallas or 'ninguna')
