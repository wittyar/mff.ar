"""Ficha en pestañas: cabecera fija (foto, nombre, uniforme), Resumen · Skills · Análisis ·
Armado · Equipos · Progreso · Más, reglas generales plegadas, enlaces internos, y alturas por pestaña."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

SH = SALIDA
ok = Chequeo()
C = datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS']
pj = {c['name']: c for c in C}
def uid_de(n, u): return next(x['id'] for x in pj[n]['uniforms'] if x['name'] == u)

def abrir(pg, nombre, uid=''):
    pg.evaluate("window.scrollTo(0,0)")
    if pg.locator('[data-a="back"]').count(): pg.click('[data-a="back"]')
    pg.fill('#q', nombre); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{pj[nombre]["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid: pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(200)

def pestana(pg, k): pg.click(f'[data-a="fichaTab"][data-v="{k}"]'); pg.wait_for_timeout(200)

D = carpeta_datos()
srv, url = levantar(D, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')

        # 1. abre en Resumen
        abrir(pg, 'Wong')
        on = pg.locator('.ftab.on').inner_text()
        # 1.0.27 (#24): primero dónde rinde, qué le da al equipo y qué necesita; después quién es
        ok('1 abre en Resumen, con la respuesta arriba', on == 'Resumen' and pg.locator('.fid .statgrid').count() == 1
           and pg.locator('.resumen3 > .bloque h4').all_inner_texts() == ['DÓNDE RINDE', 'QUÉ LE DA AL EQUIPO', 'QUÉ NECESITA']
           and pg.locator('.skill').count() == 0, (on, pg.locator('.resumen3 > .bloque h4').all_inner_texts()))
        ok('1 cabecera: foto, nombre y selector', pg.locator('.fcab h1').text_content() == 'Wong'
           and pg.locator('.fcab-face img').count() == 1 and pg.locator('select[data-a="uniformSel"] option').count() == 4)

        # 2. el selector cambia de uniforme (foto, costo, habilidades)
        ds2 = uid_de('Wong', "Marvel Studios' Doctor Strange 2")
        pg.select_option('select[data-a="uniformSel"]', ds2); pg.wait_for_timeout(250)
        foto = pg.locator('.fcab-face img').get_attribute('src')
        costo = pg.evaluate("[...document.querySelectorAll('.fid .stat')].map(x => x.innerText.replace(/\\s+/g,' ')).find(t => /costo/i.test(t)) || ''")
        hab = pg.locator('.fid .row', has_text='Habilidades').first.inner_text()
        ok('2 uniforme elegido: foto, costo y habilidades del uniforme', 'wong2' in foto and '1750' in costo and 'MAGIA' in hab.upper(),
           (foto, costo, hab.replace('\n', ' ')))
        ok('2 el selector queda en el uniforme', pg.locator('select[data-a="uniformSel"]').input_value() == ds2)

        # 3. Skills
        pestana(pg, 'skills')
        n_sk = pg.locator('.skill').count()
        ok('3 Skills: cargas, buffs clave, rotaciones y las 11 skills', n_sk == 11 and pg.locator('.chargebar').count() == 1
           and pg.locator('.keybuffs').count() == 1 and pg.locator('.rots, .section h3:has-text("Rotaciones")').count() >= 1, n_sk)
        pg.locator('.skill', has_text='Avance místico').locator('button.tag.objetivo').click()
        ok('3 el objetivo de grupo sigue abriendo la lista', pg.locator('.modal.ancho').count() == 1)
        pg.keyboard.press('Escape')

        # 4. pegada: al bajar, la cabecera queda arriba; al cambiar de pestaña, el contenido arranca de arriba
        pg.evaluate("window.scrollTo({top: 2500, behavior: 'instant'})"); pg.wait_for_timeout(150)
        top_cab = pg.evaluate("document.querySelector('.fcab').getBoundingClientRect().top")
        nav = pg.evaluate("document.querySelector('nav.topnav').offsetHeight")
        ok('4 cabecera fija bajo la barra', abs(top_cab - nav) <= 1, (top_cab, nav))
        pestana(pg, 'armado')
        pos = pg.evaluate("""() => { const c = document.querySelector('.fcab').getBoundingClientRect();
                                      return [Math.round(c.bottom), Math.round(document.getElementById('fcuerpo').getBoundingClientRect().top)]; }""")
        ok('4 al cambiar de pestaña, el contenido arranca justo debajo de la cabecera', 0 <= pos[1] - pos[0] <= 20, pos)

        # 5. Armado: C.T.P. y artefacto a la vista, reglas generales plegadas
        reglas = pg.locator('#fcuerpo details.reglas').filter(has_text='ISO-8')
        iso_visible = pg.locator('details.reglas h4:has-text("ISO-8")').is_visible()
        ok('5 Armado: C.T.P. y artefacto, reglas plegadas', pg.locator('.bloque h4:has-text("C.T.P.")').first.is_visible()
           and reglas.count() >= 1 and not iso_visible)
        reglas.first.locator(':scope > summary').click()
        ok('5 las reglas se abren con un clic', pg.locator('details.reglas h4:has-text("ISO-8")').is_visible())

        # 6. Tu progreso, dentro de Armado (1.0.27): hoja de ruta y topes; marcar un paso queda en la capa
        ok('6 Armado: tu progreso, con la hoja de ruta y los topes', pg.locator('.bloque h4:has-text("Hoja de ruta")').count() == 1
           and pg.locator('.bloque h4:has-text("Topes de stats")').count() == 1)
        pg.locator('[data-a="ruta"]').first.click(); pg.wait_for_timeout(600)
        capa = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))
        ok('6 marcar un paso de la hoja de ruta se guarda', capa.get('ruta', {}).get(pj['Wong']['id']), capa.get('ruta'))

        # 7. Fuentes (antes Más): verificación, historial y retrato propio
        pestana(pg, 'fuentes')
        ok('7 Fuentes: verificación y retrato propio (los equipos pasaron a su pestaña)', pg.locator('#verif').count() == 1
           and pg.locator('[data-a="upload"]').count() == 1 and 'Equipos donde aparece' not in pg.locator('#fcuerpo').inner_text())

        # 8. "⚠ N diferencias" lleva a Más
        abrir(pg, 'Ikaris'); pestana(pg, 'resumen')
        pg.click('[data-a="irVerif"]'); pg.wait_for_timeout(200)
        ok('8 el aviso de diferencias lleva a Fuentes, a la verificación', pg.locator('.ftab.on').inner_text() == 'Fuentes'
           and pg.locator('#verif').is_visible())

        # 9. Marcar atributos lleva a Skills con los marcadores
        pestana(pg, 'resumen'); pg.click('[data-a="marcarModo"]'); pg.wait_for_timeout(200)
        ok('9 Marcar atributos abre Skills con los marcadores', pg.locator('.ftab.on').inner_text() == 'Skills'
           and pg.locator('.marcador').count() > 0, pg.locator('.marcador').count())
        pg.click('[data-a="marcarModo"]')

        # 10. rotaciones de otro uniforme: el botón cambia el uniforme del selector
        abrir(pg, 'Hulk'); pestana(pg, 'skills')
        bt = pg.locator('.section [data-a="uniform"]').first
        destino = bt.get_attribute('data-uid'); bt.click(); pg.wait_for_timeout(200)
        ok('10 "rotaciones de otro uniforme" cambia el uniforme del selector',
           pg.locator('select[data-a="uniformSel"]').input_value() == destino and pg.locator('.ftab.on').inner_text() == 'Skills', destino)

        # 11. alturas por pestaña (compu)
        abrir(pg, 'Wong', ds2)
        alturas = {}
        for k in ('resumen', 'skills', 'armado', 'equipos', 'fuentes'):
            pestana(pg, k); alturas[k] = pg.evaluate("document.documentElement.scrollHeight")
        print('   alturas en compu (px):', alturas)
        pestana(pg, 'resumen'); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{SH}/ficha_nueva_resumen_1300.png')
        pestana(pg, 'skills'); pg.evaluate("window.scrollTo({top: 1400, behavior: 'instant'})"); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{SH}/ficha_nueva_skills_1300.png')
        pestana(pg, 'armado'); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
        pg.screenshot(path=f'{SH}/ficha_nueva_armado_1300.png')

        # 12. inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        tabs = [x.inner_text() for x in pg.locator('.ftab').all()]
        ok('12 pestañas en inglés', tabs == ['Overview', 'Skills', 'Build', 'Teams', 'Sources'], tabs)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('sin errores de página (compu)', not errores, errores[:3])
        b.close()

        # 13. celular
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        abrir(pg, 'Wong', ds2)
        cab = pg.evaluate("Math.round(document.querySelector('.fcab').getBoundingClientRect().height)")
        ancho = pg.evaluate("document.documentElement.scrollWidth")
        tabs_vis = pg.evaluate("[...document.querySelectorAll('.ftab')].every(t => { const r = t.getBoundingClientRect(); return r.right <= 390 && r.left >= 0; })")
        ok('13 celular: cabecera compacta, pestañas a la vista y sin desborde', cab <= 190 and ancho <= 390 and tabs_vis, (cab, ancho, tabs_vis))
        alt_cel = {}
        for k in ('resumen', 'skills', 'armado', 'equipos', 'fuentes'):
            pestana(pg, k); alt_cel[k] = pg.evaluate("document.documentElement.scrollHeight")
        print('   alturas en celular (px):', alt_cel)
        pestana(pg, 'skills'); pg.evaluate("window.scrollTo({top: 1800, behavior: 'instant'})"); pg.wait_for_timeout(300)
        top_cab = pg.evaluate("document.querySelector('.fcab').getBoundingClientRect().top")
        ok('13 celular: la cabecera queda fija al bajar', abs(top_cab - pg.evaluate("document.querySelector('nav.topnav').offsetHeight")) <= 1, top_cab)
        pg.screenshot(path=f'{SH}/ficha_nueva_skills_390.png')
        pestana(pg, 'resumen'); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{SH}/ficha_nueva_resumen_390.png')
        ok('sin errores de página (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
