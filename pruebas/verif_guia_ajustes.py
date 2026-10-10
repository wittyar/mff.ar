"""Ajustes: estado de la guía de armado en sus tres casos (compatible, la planilla de la última
revisión no se pudo usar, datos sin la guía) y que la ficha siga mostrando la copia en uso
cuando hubo rechazo."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright

ok = Chequeo()
def texto(loc): return loc.evaluate('e => e.textContent.replace(/\\s+/g, " ").trim()')
def visto(loc): return loc.evaluate('e => e.innerText.replace(/\\s+/g, " ").trim().toLowerCase()')
RX = re.compile(r'\nwindow\.MFF_GUIA_ARMADO = (.*?);\n')

def carpeta(cambio):
    d = carpeta_datos()
    ruta = os.path.join(d, 'data.js')
    js = open(ruta, encoding='utf-8').read()
    m = RX.search(js)
    G = json.loads(m.group(1))
    nuevo = cambio(G)
    js = js[:m.start()] + ('\n' if nuevo is None else '\nwindow.MFF_GUIA_ARMADO = ' + json.dumps(nuevo, ensure_ascii=False) + ';\n') + js[m.end():]
    open(ruta, 'w', encoding='utf-8').write(js)
    return d

def ajustes(pg):
    pg.click('[data-a="goSettings"]'); pg.wait_for_timeout(250)
    return pg.locator('.section', has=pg.locator('h3', has_text=re.compile('Cynicalex')))

def con_rechazo(G):
    G['estado']['comprobada'] = '2026-10-12'
    G['estado']['rechazo'] = {'version': 'V13.0.0', 'motivos': ['faltan columnas: «Best CTP»', 'la leyenda cambió; ya no dice «CTP+ = Reforged required»']}
    return G

casos = [('compatible', lambda G: G), ('rechazada', con_rechazo), ('sin guía', lambda G: None)]
with sync_playwright() as p:
    for nombre, cambio in casos:
        srv, url = levantar(carpeta(cambio), origen_local())
        try:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
            pg.on('pageerror', lambda e: errores.append(str(e)))
            pg.goto(url); pg.wait_for_selector('.ccard')
            sec = ajustes(pg)
            tx = texto(sec) if sec.count() else ''
            tv = visto(sec) if sec.count() else ''
            fuentes = texto(pg.locator('.section', has=pg.locator('h3', has_text='Fuentes')))
            if nombre == 'compatible':
                ok('compatible: versión, fecha, revisión, personajes', all(x.lower() in tv for x in ['Versión en uso V12.2.0 tomada el 2026-10-01',
                   'Última revisión 2026-10-01 compatible', 'Personajes 290']) and sec.locator('.ga-rechazo').count() == 0, tv[:300])
                sec.locator('summary', has_text='no interpreta').click(); pg.wait_for_timeout(100)
                items = [texto(x) for x in sec.locator('details li').all()]
                ok('compatible: los 3 valores sin interpretar, por columna', items == ['Best ISO-8 Set: defensive, shield, veteran soldier',
                   'Obelisk (SL/AC): Lightning, Inv', 'Tier List Bling: ()'], items)
                ok('compatible: sin filas sin personaje', 'sin personaje' not in tx)
                ok('Fuentes: nombra la planilla con su enlace', pg.locator('a[href^="https://docs.google.com/spreadsheets/d/1H0Hcl9oVZV9gA266xkJAqPv5bD1qwqhC5NeVbLj_-FE"]').count() >= 1
                   and 'Cynicalex Mega Guides' in fuentes, fuentes[-200:])
                pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
                tx_en = visto(ajustes(pg))
                ok('compatible, en inglés', all(x.lower() in tx_en for x in ['Version in use V12.2.0 taken on 2026-10-01', 'Last check 2026-10-01 compatible']), tx_en[:300])
                pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
            elif nombre == 'rechazada':
                av = texto(sec.locator('.ga-rechazo')) if sec.locator('.ga-rechazo').count() else ''
                ok('rechazada: aviso con fecha, la versión que se sigue usando y los motivos',
                   av.startswith('⚠ El 2026-10-12 la planilla (V13.0.0) no se pudo usar: se sigue con la V12.2.0, tomada el 2026-10-01. Motivos:')
                   and 'faltan columnas: «Best CTP»' in av and '«CTP+ = Reforged required»' in av, av)
                ok('rechazada: la revisión dice que no se pudo usar', 'última revisión 2026-10-12 no se pudo usar' in tv, tv[:300])
                # la ficha sigue con la copia en uso
                pg.click('nav.topnav button'); pg.wait_for_selector('#q'); pg.fill('#q', 'Abomination'); pg.wait_for_timeout(250)
                pg.locator('.ccard').first.click(); pg.wait_for_selector('.fcab')
                bl = pg.locator('.usogrid .bloque', has=pg.locator('h4', has_text=re.compile('Cynicalex')))
                ok('rechazada: la ficha sigue mostrando la versión en uso', 'Lead/Support Gods' in texto(bl) and 'V12.2.0' in texto(bl))
            else:
                ok('sin guía: Ajustes lo dice', 'Los datos cargados no traen la guía de armado' in tx, tx)
                ok('sin guía: Fuentes sigue andando', 'Cynicalex Mega Guides' in fuentes)
            ok(f'{nombre}: sin errores de página', not errores, errores[:3])
            b.close()
        finally:
            srv.terminate(); srv.wait()
    # celular, con rechazo: nada se sale
    srv, url = levantar(carpeta(con_rechazo), origen_local())
    try:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.goto(url); pg.wait_for_selector('.ccard'); sec = ajustes(pg)
        sec.locator('summary', has_text='no interpreta').click(); pg.wait_for_timeout(100)
        fuera = pg.evaluate("""() => [...document.querySelectorAll('#guia-armado *')].filter(e => { const r = e.getBoundingClientRect();
          return r.width && r.right > innerWidth + 0.5; }).map(e => e.className || e.tagName).slice(0, 4)""")
        ok('celular: la sección de Ajustes no se sale de la pantalla', not fuera, fuera)
        sec.screenshot(path=f'{SALIDA}/ga_ajustes_390.png')
        b.close()
    finally:
        srv.terminate(); srv.wait()
ok.fin()
