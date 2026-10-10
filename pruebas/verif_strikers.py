"""1.0.14: los strikers en la pestaña Equipos de la ficha. Kingpin: sus 50 strikers (los de la wiki,
validados contra el juego) y de quiénes es striker; Galactus: la wiki no tiene los suyos. Contra
MFF_STRIKERS leído aparte (node). Celular sin desborde y sin errores de página.
Carril de consistencia: una probabilidad de más de 100% (Daken: Doctor Octopus, 219%) va tal cual, sin topear,
marcada como dato imposible de la fuente; las demás, sin marca."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright
ok = Chequeo()
SP = PRUEBAS
ST = datos_js('MFF_STRIKERS')['MFF_STRIKERS']
de = {}
for cid, filas in ST.items():
    for x, p, c in filas: de.setdefault(x, []).append((cid, p, c))
def abrir(pg, cid, nombre):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#strikers')
srv, url = levantar(carpeta_datos(), origen_local())
errores = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1300, 'height': 900}); pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        # 1.0.27 (#24): una sola tabla, una fila por personaje con los dos sentidos
        def filas_modelo(cid):
            suyos, d = {x: (p_, c) for x, p_, c in ST.get(cid, [])}, {x: (p_, c) for x, p_, c in de.get(cid, [])}
            txt = lambda v: f"{v[0]:g}% al {'atacar' if v[1] == 'ataca' else 'ser atacado'}"
            out = {}
            for x in set(suyos) | set(d):
                out[x] = (txt(suyos[x]) if x in suyos else ('no' if cid in ST else 'sin dato'),
                          txt(d[x]) if x in d else ('no' if x in ST else 'sin dato'))
            return suyos, d, out
        def filas_app(sec):
            return pg.evaluate("""() => [...document.querySelectorAll('#strikers .sktabla tbody tr')].map(tr => [tr.querySelector('[data-cid]').dataset.cid,
                ...[...tr.querySelectorAll('td')].slice(1).map(td => td.textContent.replace(' ⚠', '').trim())])""")
        abrir(pg, 'kingpin', 'Kingpin')
        sec = pg.locator('#strikers')
        suyos, d, modelo = filas_modelo('kingpin')
        resumen = sec.locator('details.reglas > summary').inner_text()
        ok('Kingpin: el resumen dice cuántos con él, cuántos lo ayudan y a cuántos ayuda',
           resumen == f'Strikers: {len(modelo)} con él ({len(suyos)} lo ayudan, él ayuda a {len(d)})', resumen)
        sec.locator('details.reglas > summary').click()
        app = filas_app(sec)
        ok('Kingpin: cada fila con los dos sentidos, según MFF_STRIKERS', {f[0]: (f[1], f[2]) for f in app} == modelo and len(app) == len(modelo), app[:3])
        mx = lambda f: max([v[0] for v in (suyos.get(f), d.get(f)) if v] or [0])
        ok('Kingpin: de mayor a menor probabilidad (la mayor de los dos sentidos)', [mx(f[0]) for f in app] == sorted([mx(f[0]) for f in app], reverse=True))
        ok('Kingpin: Black Cat 17% al atacar', any(f[1] == '17% al atacar' for f in app if f[0] == 'black-cat'))
        ok('la fuente es la pestaña Striker de la wiki', 'pestaña Striker' in sec.locator('.fuentes').text_content())
        sec.locator('.sktabla [data-a="open"]').first.click(); pg.wait_for_timeout(300)
        ok('el nombre abre la ficha del striker', pg.evaluate('history.state.charId') == app[0][0], pg.evaluate('history.state.charId'))
        imposibles = [(c, x, p_, q) for c, fs in ST.items() for x, p_, q in fs if p_ > 100]
        ok('datos: las dos probabilidades imposibles de hoy', sorted((c, x, p_) for c, x, p_, _ in imposibles)
           == [('daken', 'doctor-octopus', 219), ('molecule-man', 'morgan-le-fay', 120)], imposibles)
        abrir(pg, 'daken', 'Daken')
        sec = pg.locator('#strikers'); sec.locator('details.reglas > summary').click()
        marca = sec.locator('.sktabla tr', has=pg.locator('[data-cid="doctor-octopus"]')).locator('.imposible')
        ok('Daken: Doctor Octopus 219% tal cual, marcado como dato imposible de la fuente', marca.count() == 1
           and marca.text_content() == '219% al ser atacado ⚠' and 'Dato imposible de la fuente' in marca.get_attribute('title'),
           marca.count() and (marca.text_content(), marca.get_attribute('title')[:60]))
        ok('Daken: las demás, sin marca', sec.locator('.imposible').count() == 1, sec.locator('.imposible').count())
        abrir(pg, 'galactus', 'Galactus')
        tx = pg.locator('#strikers').text_content()
        ok('Galactus: la wiki no tiene sus strikers y no es striker de nadie', 'La wiki no tiene sus strikers.' in tx and 'No es striker de nadie en la wiki.' in tx, tx[:200])
        pg.click('[data-a="lang"]'); pg.wait_for_selector('#strikers')
        ok('inglés', 'The wiki does not list its strikers.' in pg.locator('#strikers').text_content())
        pg.click('[data-a="lang"]')
        pg.close()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        abrir(pg, 'kingpin', 'Kingpin')
        pg.locator('#strikers details.reglas > summary').click()
        r = pg.evaluate("""() => { const out = []; for (const el of document.querySelectorAll('#strikers *')) { const r = el.getBoundingClientRect();
            if (r.width && r.right > 391) out.push(el.className || el.tagName); } return { doc: document.documentElement.scrollWidth, fuera: out.slice(0, 5) }; }""")
        ok('celular: sin desborde', r['doc'] <= 390 and not r['fuera'], r)
        pg.locator('#strikers').scroll_into_view_if_needed(); pg.screenshot(path=f'{SP}/strikers_390.png')
        b.close()
finally:
    srv.terminate(); srv.wait()
ok('sin errores de página', not errores, errores[:3])
ok.fin()
