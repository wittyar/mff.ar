"""Capa del usuario en capa.json (a través del servidor).

1  primer uso: sin capa.json arranca vacía; un cambio crea capa.json
2  persiste entre reinicios del servidor (idioma y un equipo)
3  respaldo diario: la segunda escritura del día deja respaldos/capa-HOY.json
4  capa.json ilegible: pantalla de error y el archivo queda intacto
5  file://: pantalla que explica cómo abrirla
6  servidor caído al guardar: aviso + reintento que guarda al volver el servidor
7  importar una capa vieja (asignación como texto) la normaliza y la guarda
"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import datetime, json, os, shutil, subprocess, sys, tempfile, time
from playwright.sync_api import sync_playwright

RAIZ = RAIZ
fallas = []
def chequear(nombre, cond, detalle=''):
    print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
    if not cond: fallas.append(nombre)

# Los datos y el servidor, los del harness (MFF_DATOS y el origen local de los datos publicados): desde la 1.0.30 la app
# baja los de su formato, y con los datos del repo de otro formato que version.json no arranca en el roster.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness
carpeta_datos = harness.carpeta_datos
def levantar(datos): return harness.levantar(datos, harness.origen_local())

def bajar(srv):
    srv.terminate(); srv.wait()

def capa(d):
    return json.load(open(os.path.join(d, 'capa.json'), encoding='utf-8'))

with sync_playwright() as p:
    b = p.chromium.launch()
    D = carpeta_datos()
    srv, url = levantar(D)
    ctx = b.new_context(viewport={'width': 1300, 'height': 900})
    page = ctx.new_page()
    errores = []
    page.on('pageerror', lambda e: errores.append(str(e)))
    page.goto(url); page.wait_for_selector('.ccard')
    chequear('1 primer uso: arranca sin capa.json', not os.path.exists(os.path.join(D, 'capa.json')))
    page.click('[data-a="lang"]'); page.wait_for_timeout(500)
    chequear('1 un cambio crea capa.json', os.path.exists(os.path.join(D, 'capa.json')) and capa(D)['prefs']['lang'] == 'en',
             capa(D)['prefs']['lang'] if os.path.exists(os.path.join(D, 'capa.json')) else 'sin archivo')
    # un equipo
    page.locator('.ccard').first.click(); page.wait_for_selector('.plista')
    dos = page.evaluate("(() => { const ks = [...document.querySelectorAll('.plista [data-a=\"mesaPoner\"]')].map(x => x.dataset.key), out = [];"
                        " for (const k of ks) if (!out.some(o => o.split('::')[0] === k.split('::')[0])) out.push(k); return out.slice(0, 2); })()")
    for k in dos:
        page.click(f'.plista [data-a="mesaPoner"][data-key="{k}"]'); page.wait_for_timeout(150)
    page.fill('[data-a="mesaNombre"]', 'Prueba capa')
    page.click('[data-a="mesaGuardar"]'); page.wait_for_timeout(500)
    chequear('2 el equipo quedó en capa.json', [t['name'] for t in capa(D)['teams']] == ['Prueba capa'], capa(D)['teams'][:1])
    chequear('3 respaldo del día', os.path.exists(os.path.join(D, 'respaldos', f'capa-{datetime.date.today().isoformat()}.json')),
             os.listdir(os.path.join(D, 'respaldos')) if os.path.isdir(os.path.join(D, 'respaldos')) else 'sin carpeta')
    bajar(srv)
    srv, url = levantar(D)
    page.goto(url); page.wait_for_selector('.ccard')
    idioma = page.evaluate("document.querySelector('.langbtn .on').textContent")
    page.click('[data-a="goTeams"]'); page.wait_for_timeout(300)
    equipos = page.evaluate("[...document.querySelectorAll('.card > div[style*=\"font-weight:600\"]')].map(e => e.textContent.trim())")
    chequear('2 tras reiniciar el servidor: idioma y equipo', idioma == 'EN' and 'Prueba capa' in equipos, (idioma, equipos))

    # 6: el servidor no puede escribir la capa (capa.json.tmp ocupado por una carpeta)
    os.mkdir(os.path.join(D, 'capa.json.tmp'))
    page.click('[data-a="lang"]'); page.wait_for_timeout(800)
    avisos = page.evaluate("document.querySelector('#avisos').innerText")
    chequear('6 un guardado fallido avisa con el motivo', ('No se guardó' in avisos or 'not saved' in avisos) and 'capa' in avisos, avisos[:200])
    chequear('6 el archivo conserva lo anterior', capa(D)['prefs']['lang'] == 'en', capa(D)['prefs']['lang'])
    os.rmdir(os.path.join(D, 'capa.json.tmp'))
    page.click('[data-a="reintentarGuardado"]'); page.wait_for_timeout(800)
    chequear('6 reintentar guarda el cambio', capa(D)['prefs']['lang'] == 'es', capa(D)['prefs']['lang'])
    chequear('6 el aviso de guardado se va', 'No se guardó' not in page.evaluate("document.querySelector('#avisos').innerText"))

    # 7: importar una capa vieja
    vieja = {'lists': [], 'assign': {'tv-general': {'thanos::base': 'tier-a'}}, 'teams': [], 'prefs': {'lang': 'es'}}
    ruta_vieja = os.path.join(D, 'vieja.json'); json.dump(vieja, open(ruta_vieja, 'w'))
    page.click('[data-a="goSettings"]'); page.wait_for_timeout(300)
    page.set_input_files('[data-a="importUser"]', ruta_vieja); page.wait_for_timeout(800)
    chequear('7 importar normaliza (texto -> lista) y guarda', capa(D)['assign'] == {'tv-general': {'thanos::base': ['tier-a']}}, capa(D)['assign'])
    chequear('sin errores de página', not errores, errores)
    ctx.close()

    # 4: capa ilegible
    bajar(srv)
    open(os.path.join(D, 'capa.json'), 'w').write('{"teams": [ roto')
    antes = open(os.path.join(D, 'capa.json')).read()
    srv, url = levantar(D)
    page = b.new_page(); page.goto(url); page.wait_for_selector('.fatal')
    texto = page.evaluate("document.querySelector('.fatal').innerText")
    chequear('4 capa ilegible: pantalla de error', 'no se pudo cargar tu capa' in texto.lower() and 'capa.json' in texto, texto[:200])
    page.wait_for_timeout(500)
    chequear('4 capa ilegible: el archivo queda intacto', open(os.path.join(D, 'capa.json')).read() == antes)
    page.close()
    bajar(srv)

    # 5: file://
    page = b.new_page(); page.goto(f'file://{RAIZ}/index.html'); page.wait_for_selector('.fatal')
    chequear('5 file://: explica cómo abrirla', 'acceso directo' in page.evaluate("document.querySelector('.fatal').innerText").lower())
    page.screenshot(path=f'{SALIDA}/fatal_file.png')
    b.close()
    shutil.rmtree(D)

print('\nFALLAS:', fallas or 'ninguna')
