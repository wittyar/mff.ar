"""Solapa Glosario, en dos pestañas (juego y app, #24) con cada entrada plegada: contenido (términos, errores, otras diferencias, efectos por grupo), enlaces
internos (también a un destino que la búsqueda dejó afuera), búsqueda en los tres idiomas y sin
resultados, el foco en la búsqueda mientras se escribe, la interfaz en inglés, el celular sin
desborde horizontal, «Atrás» y adelante, y sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
RAIZ = RAIZ
SP = PRUEBAS
ok = Chequeo()
G = json.load(open(f'{RAIZ}/scripts/contenido/glosario.json', encoding='utf-8'))
C = json.load(open(f'{RAIZ}/scripts/contenido/catalogo.json', encoding='utf-8'))
N_TERM, N_ERR = len(G['terminos']), len(G['errores'])
N_OTRAS = sum(1 for x in G['terminos'] if x.get('difiere') and not x.get('error'))
N_EF, N_GR = len(C['efectos']), len(C['grupos'])
print('esperado:', N_TERM, 'términos,', N_ERR, 'errores,', N_OTRAS, 'otras,', N_EF, 'efectos,', N_GR, 'grupos')

# Fuera de la columna: algo de <main> que se ve y pasa el borde derecho de la ventana (lo de un details cerrado no se ve).
FUERA = """(w) => { const out = [];
  for (const el of document.querySelectorAll('main *')) { if (!el.checkVisibility()) continue; const r = el.getBoundingClientRect();
    if (r.width && r.right > w + 1) out.push(el.className || el.tagName); }
  return { doc: document.documentElement.scrollWidth, fuera: [...new Set(out)].slice(0, 8) }; }"""
# El destino quedó a la vista, debajo de la barra de arriba, y marcado.
A_LA_VISTA = """(id) => { const el = document.getElementById(id); if (!el) return null; const r = el.getBoundingClientRect();
  const nav = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h'));
  return { top: Math.round(r.top), nav, foco: el.classList.contains('glfoco') }; }"""


def esperar_quieto(pg):
    """Espera que termine el desplazamiento suave."""
    pg.wait_for_function("""() => new Promise(r => { let y = scrollY, n = 0; const f = () => {
      if (scrollY === y) { if (++n > 6) return r(true); } else { y = scrollY; n = 0; } requestAnimationFrame(f); }; f(); })""")


srv, url = levantar(carpeta_datos(), origen_local())
errores, consola = [], []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        # ---- compu, en español ----
        pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: consola.append(m.text) if m.type == 'error' else None)
        pg.goto(url); pg.wait_for_selector('.ccard')
        nav = pg.locator('[data-a="goGlosario"]')
        ok('la barra tiene Glosario', nav.count() == 1 and nav.inner_text().strip() == 'Glosario', nav.count())
        nav.click(); pg.wait_for_selector('.glitem')
        titulo = lambda: pg.evaluate("document.querySelector('main h1').firstChild.textContent.trim()")
        ok('título', titulo() == 'Glosario', titulo())
        cuenta = lambda sel: pg.locator(sel).count()
        tab = lambda v: pg.locator(f'[data-a="glTab"][data-v="{v}"]')
        abrir = lambda sel: pg.evaluate("(s) => document.querySelectorAll(s).forEach(d => d.open = true)", sel)
        # #24: dos pestañas; arranca en la del juego, con los términos plegados y los errores plegados arriba
        ok('dos pestañas, arranca en la del juego', tab('juego').get_attribute('aria-selected') == 'true'
           and tab('app').get_attribute('aria-selected') == 'false')
        ok('pestaña del juego: cuenta los términos', tab('juego').inner_text().strip() == f'Glosario del juego · {N_TERM}', tab('juego').inner_text())
        ok('pestaña de la app: cuenta los efectos', tab('app').inner_text().strip() == f'Efectos de la app · {N_EF}', tab('app').inner_text())
        ok('todos los términos', cuenta('details.glitem[id^="gl-"]') == N_TERM, cuenta('details.glitem[id^="gl-"]'))
        ok('los términos, plegados', cuenta('details.glitem[open]') == 0)
        ok('los efectos no están en esta pestaña', cuenta('.glef') == 0, cuenta('.glef'))
        errs = pg.locator('details.glerrs')
        ok('errores: plegados, con cuántos son', errs.count() == 1 and errs.get_attribute('open') is None
           and f'{N_ERR} errores que se repiten y {N_OTRAS} diferencias más' in errs.locator('summary').inner_text(), errs.locator('summary').inner_text())
        ok('los errores que se repiten', cuenta('.glerr') == N_ERR, cuenta('.glerr'))
        ok('otras diferencias', cuenta('.glotra') == N_OTRAS, cuenta('.glotra'))
        ok('nav marca Glosario', 'on' in (nav.get_attribute('class') or '') or 'active' in (nav.get_attribute('class') or ''), nav.get_attribute('class'))
        ok('la nota del glosario, en el «?»', pg.locator('main h1 details.ayuda').count() == 1)
        inv = pg.locator('#gl-invincible')
        linea = inv.locator('summary').inner_text()
        ok('Invencible a la vista: nombres en los tres idiomas y la marca', 'Invencible' in linea and 'Invincible' in linea and '무적' in linea
           and 'el inglés difiere' in linea.lower(), linea[:160])
        ok('Invencible a la vista: lo que dice, en una línea', inv.locator('.glcorto').count() == 1 and inv.locator('.glcorto').inner_text().strip(), linea)
        ok('Invencible: el detalle, plegado', not inv.locator('.gldifbox').is_visible())
        inv.locator('summary').click()
        ok('Invencible abierto: aclara 피격 모션', '피격 모션' in inv.locator('.gldifbox').inner_text(), inv.locator('.gldifbox').inner_text()[:160])
        ok('Invencible: enlace al error y al catálogo',
           inv.locator('[data-v="gle-golpe"]').count() == 1 and inv.locator('[data-v="ef-invencible"]').count() == 1)
        ok('sin diferencia: Miedo no lleva la marca', pg.locator('#gl-fear .gldif').count() == 0)
        # #32: el nombre en español es el del juego (fuentes/juego-es/glosario.json), con sus erratas, y lo dice la nota.
        JUEGO = {x['id']: x['nombre'] for x in json.load(open(f'{RAIZ}/fuentes/juego-es/glosario.json', encoding='utf-8'))['terminos']}
        nombres_es = pg.evaluate("[...document.querySelectorAll('details.glitem[id^=\"gl-\"]')].map(d => [d.id.slice(3), d.querySelector('.glnom b').textContent])")
        ok('#32 cada término con el nombre del juego en español', all(JUEGO[i] == n for i, n in nombres_es) and len(nombres_es) == N_TERM,
           [(i, n, JUEGO[i]) for i, n in nombres_es if JUEGO[i] != n][:3])
        ok('#32 Contrataque, con la nota de la errata', 'Contrataque' in pg.locator('#gl-counterattack summary').inner_text()
           and '(sic)' in pg.locator('#gl-counterattack').text_content())
        abrir('details.glitem')
        # Carril de cierre (5 de octubre de 2026): «Lo da» dice de qué opción del C.T.P. sale cada efecto.
        ok('Penetration: lo da una opción de reforja de Regeneration y de Transcendence',
           'Lo da: Regeneración (opción de reforja), Transcendencia (opción de reforja)' in pg.locator('#gl-penetration').inner_text(),
           pg.locator('#gl-penetration').inner_text()[:300])
        ok('Penetration: la marca C.T.P. a la vista', 'C.T.P.' in pg.locator('#gl-penetration summary').inner_text())
        wall = pg.locator('#gl-wall')
        ok('Wall: lo da la opción bloqueada de Conquest, con su explicación', 'Lo da: Conquista (opción bloqueada)' in wall.inner_text()
           and 'sin reforjar' not in wall.inner_text()
           and any('los refinados' in (x.get_attribute('title') or '') for x in wall.locator('.glcuerpo span[title]').all()), wall.inner_text()[:300])
        ok('Pánico: con las dos capturas (la coreana llegó el 4 de octubre)', 'sin captura' not in pg.locator('#gl-panic').text_content())
        ok('Strike: el inglés difiere (lo que omite)', pg.locator('#gl-strike .gldif').count() == 1
           and 'Según el coreano, además' in pg.locator('#gl-strike .gldifbox').inner_text())
        # La captura en inglés de Enraged, Vitality y Wall llegó el 4 de octubre (con el contenido de la 1.0.19).
        ok('Enraged: con las dos capturas', 'sin captura' not in pg.locator('#gl-enraged').text_content())
        ok('fuentes en cada término', pg.locator('details.glitem[id^="gl-"] .fuentes').count() == N_TERM)
        abrir('details.glerrs')
        err = pg.locator('#gle-golpe')
        n_golpe = sum(1 for x in G['terminos'] if x.get('error') == 'golpe')
        ok('error golpe: enlaza sus términos', err.locator('[data-a="irGlos"]').count() == n_golpe, err.locator('[data-a="irGlos"]').count())

        # enlace interno: del término al error (con los errores plegados: los abre)
        pg.goto(url); pg.wait_for_selector('.ccard'); nav.click(); pg.wait_for_selector('.glitem')
        pg.locator('#gl-invincible summary').click()
        pg.locator('#gl-invincible [data-v="gle-golpe"]').click(); esperar_quieto(pg)
        r = pg.evaluate(A_LA_VISTA, 'gle-golpe')
        ok('enlace: abre los errores', pg.locator('details.glerrs').get_attribute('open') is not None)
        ok('enlace: el error queda a la vista debajo de la barra y marcado', r and r['nav'] <= r['top'] <= r['nav'] + 40 and r['foco'], r)
        ok('enlace: no cambia la dirección', '#' not in pg.url, pg.url)
        pg.wait_for_timeout(1800)
        ok('enlace: la marca se va sola', not pg.evaluate(A_LA_VISTA, 'gle-golpe')['foco'])
        # del término al efecto: cambia de pestaña y abre el efecto
        pg.locator('#gl-invincible [data-v="ef-invencible"]').click(); esperar_quieto(pg)
        r = pg.evaluate(A_LA_VISTA, 'ef-invencible')
        ok('enlace término → efecto: pasa a la pestaña de la app', tab('app').get_attribute('aria-selected') == 'true')
        ok('enlace término → efecto: abierto, a la vista', pg.locator('#ef-invencible').get_attribute('open') is not None
           and r and r['nav'] <= r['top'] <= r['nav'] + 40, r)

        # ---- pestaña de la app ----
        ok('app: todos los efectos', cuenta('.glef') == N_EF, cuenta('.glef'))
        ok('app: todos los grupos', cuenta('.glgrupo') == N_GR, cuenta('.glgrupo'))
        ok('app: el aviso de que son de la app', 'son de la app' in pg.locator('.glaviso').inner_text())
        ok('app: los términos no están en esta pestaña', cuenta('details.glitem[id^="gl-"]') == 0)
        ef = pg.locator('#ef-invencible')
        ok('efecto a la vista: el término que le corresponde', 'Invencible' in ef.locator('summary .glmarcas').text_content(), ef.locator('summary').inner_text())
        ok('efecto: vuelve al término', ef.locator('[data-v="gl-invincible"]').count() == 1)
        ok('efecto: lecturas, a quién le sirve', 'Le sirve:' in ef.inner_text(), ef.inner_text()[:200])
        con_etq = pg.locator('.glef .glet').count()
        ok('efectos con etiquetas de skills', con_etq > 60, con_etq)
        # del efecto al término: vuelve a la pestaña del juego
        pg.locator('#ef-escudo summary').click()
        dest = pg.locator('#ef-escudo [data-a="irGlos"]').first.get_attribute('data-v')
        pg.locator('#ef-escudo [data-a="irGlos"]').first.click(); esperar_quieto(pg)
        r = pg.evaluate(A_LA_VISTA, dest)
        ok('enlace efecto → término: pestaña del juego, abierto, a la vista', tab('juego').get_attribute('aria-selected') == 'true'
           and pg.locator('#' + dest).get_attribute('open') is not None and r and r['nav'] <= r['top'] <= r['nav'] + 40, (dest, r))

        # búsqueda: en coreano, con el foco en la caja mientras se escribe
        pg.evaluate('window.scrollTo(0, 0)')
        pg.locator('#q').click(); pg.keyboard.type('무적', delay=60)
        ok('búsqueda: el foco sigue en la caja', pg.evaluate("document.activeElement.id") == 'q' and pg.input_value('#q') == '무적', pg.input_value('#q'))
        ok('búsqueda 무적: un término', cuenta('details.glitem[id^="gl-"]') == 1 and pg.locator('details.glitem').get_attribute('id') == 'gl-invincible')
        ok('búsqueda 무적: sin la sección de errores', cuenta('.glerrs') == 0)
        ok('búsqueda 무적: dice cuántos hay en la otra pestaña', '1 en la otra pestaña' in pg.locator('.glbusca').inner_text(), pg.locator('.glbusca').inner_text())
        ok('búsqueda 무적: las pestañas cuentan lo que pasa', tab('juego').inner_text().endswith('· 1') and tab('app').inner_text().endswith('· 1'))
        # enlace a un destino que la búsqueda dejó afuera: vacía la búsqueda
        pg.locator('#gl-invincible summary').click()
        pg.locator('#gl-invincible [data-v="gle-golpe"]').click(); esperar_quieto(pg)
        r = pg.evaluate(A_LA_VISTA, 'gle-golpe')
        ok('enlace fuera de la búsqueda: la vacía y lleva al error', pg.input_value('#q') == '' and r and r['nav'] <= r['top'] <= r['nav'] + 40, r)
        ok('enlace fuera de la búsqueda: no deja el foco en la caja', pg.evaluate("document.activeElement.id") != 'q')
        ok('enlace fuera de la búsqueda: vuelve todo', cuenta('details.glitem[id^="gl-"]') == N_TERM and cuenta('.glerr') == N_ERR)
        # en español, sin tildes
        pg.fill('#q', 'trampa')
        nombres = pg.locator('.glnom b').all_inner_texts()
        ok('búsqueda trampa: el término Trampa', 'Trampa' in nombres, nombres)
        tab('app').click()
        ok('búsqueda trampa: el efecto que le corresponde', pg.locator('#ef-atrapar').count() == 1, cuenta('.glef'))
        ok('la búsqueda sigue al cambiar de pestaña', pg.input_value('#q') == 'trampa')
        tab('juego').click()
        pg.fill('#q', 'congelacion')
        ok('búsqueda sin tilde', pg.locator('#gl-time_freezing').count() == 1)
        # por una etiqueta de skill en inglés
        pg.fill('#q', 'Guard Break')
        ok('búsqueda en inglés: el término', pg.locator('#gl-guard_break').count() == 1)
        tab('app').click()
        ok('búsqueda en inglés: el efecto', pg.locator('#ef-romper_guardia').count() == 1)
        pg.fill('#q', 'zzzz')
        ok('sin resultados: lo dice', 'Nada coincide con la búsqueda.' in pg.locator('main').inner_text() and cuenta('.glitem') == 0)
        ok('sin resultados: las pestañas en cero', tab('juego').inner_text().endswith('· 0') and tab('app').inner_text().endswith('· 0'))
        pg.fill('#q', '')
        ok('búsqueda vacía: vuelve todo', cuenta('.glef') == N_EF)
        tab('juego').click()
        ok('búsqueda vacía: todos los términos', cuenta('details.glitem[id^="gl-"]') == N_TERM)

        # «Atrás» y adelante
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        pg.go_back(); pg.wait_for_selector('.glitem')
        ok('Atrás vuelve al glosario', titulo() == 'Glosario', titulo())
        pg.go_back(); pg.wait_for_selector('.ccard')
        ok('Atrás otra vez: el roster', pg.locator('.ccard').count() > 0)
        pg.go_forward(); pg.wait_for_selector('.glitem')
        ok('adelante: el glosario', titulo() == 'Glosario', titulo())

        # en inglés
        pg.click('[data-a="lang"]'); pg.wait_for_selector('.glitem')
        ok('inglés: título y barra', titulo() == 'Glossary' and pg.locator('[data-a="goGlosario"]').text_content().strip() == 'Glossary', titulo())
        tx = pg.locator('#gl-invincible summary').text_content().strip()
        ok('inglés: el nombre en inglés primero y la marca', tx.startswith('Invincible') and 'English differs' in tx, tx[:120])
        abrir('details.glitem')
        ok('inglés: la aclaración en inglés', 'English and Korean:' in pg.locator('#gl-invincible .gldifbox').inner_text())
        ok('inglés: pestañas', tab('juego').inner_text().strip() == f'Game glossary · {N_TERM}' and tab('app').inner_text().strip() == f'App effects · {N_EF}')
        ok('inglés: Wall, la opción fija', 'Granted by: Conquest (locked option)' in pg.locator('#gl-wall').inner_text(),
           pg.locator('#gl-wall').inner_text()[:300])
        ok('inglés: no quedan textos en español (juego)', all(s not in pg.locator('main').text_content()
           for s in ('Lo da:', 'En el catálogo:', 'el inglés difiere', 'sin captura', 'errores que se repiten')))
        tab('app').click(); abrir('details.glitem')
        ok('inglés: Helps', 'Helps:' in pg.locator('#ef-invencible').inner_text())
        ok('inglés: no quedan textos en español (app)', all(s not in pg.locator('main').text_content()
           for s in ('Le sirve:', 'son de la app', 'En las skills')))
        pg.screenshot(path=f'{SP}/glosario_1300_en.png', full_page=False)
        pg.click('[data-a="lang"]'); pg.wait_for_selector('.glitem')
        pg.screenshot(path=f'{SP}/glosario_1300_efectos.png', full_page=False)
        tab('juego').click(); pg.screenshot(path=f'{SP}/glosario_1300.png', full_page=False)
        pg.close()

        # ---- celular ----
        for ancho in (390, 360):
            pg = b.new_page(viewport={'width': ancho, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
            pg.on('pageerror', lambda e: errores.append(str(e)))
            pg.on('console', lambda m: consola.append(m.text) if m.type == 'error' else None)
            pg.goto(url); pg.wait_for_selector('.ccard')
            pg.locator('[data-a="goGlosario"]').scroll_into_view_if_needed()
            pg.locator('[data-a="goGlosario"]').tap(); pg.wait_for_selector('.glitem')
            r = pg.evaluate(FUERA, ancho)
            ok(f'celular {ancho}: sin desborde horizontal', r['doc'] <= ancho and not r['fuera'], r)
            ok(f'celular {ancho}: el foco no va a la búsqueda al entrar', pg.evaluate("document.activeElement.id") != 'q')
            pg.locator('#gl-shield summary').tap()
            pg.locator('#gl-shield [data-v="gle-golpe"]').tap(); esperar_quieto(pg)
            r2 = pg.evaluate(A_LA_VISTA, 'gle-golpe')
            ok(f'celular {ancho}: enlace a la vista debajo de la barra', r2 and r2['nav'] <= r2['top'] <= r2['nav'] + 40, r2)
            if ancho == 390:
                pg.evaluate('window.scrollTo(0, 0)'); pg.screenshot(path=f'{SP}/glosario_390.png')
                pg.locator('#gl-invincible summary').tap(); pg.locator('#gl-invincible').scroll_into_view_if_needed()
                pg.screenshot(path=f'{SP}/glosario_390_termino.png')
                pg.locator('[data-a="glTab"][data-v="app"]').tap(); r = pg.evaluate(FUERA, ancho)
                ok(f'celular {ancho}: pestaña de la app sin desborde horizontal', r['doc'] <= ancho and not r['fuera'], r)
                pg.locator('#ef-invencible summary').tap(); pg.locator('#ef-invencible').scroll_into_view_if_needed()
                pg.screenshot(path=f'{SP}/glosario_390_efecto.png')
            pg.close()
        b.close()
finally:
    srv.terminate(); srv.wait()
ok('sin errores de página', not errores, errores[:3])
ok('sin errores de consola', not consola, consola[:3])
ok.fin()
