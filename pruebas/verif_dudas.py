"""La información dudosa entre el coreano, el inglés y el español (#32, 1.0.33, MFF_DUDAS) y los nombres de los C.T.P. en
español (#43): el «≠» en el glosario (términos y efectos), en el «Cómo funciona» de las skills, en las skills, en las
stats de Armado, en los C.T.P. y en las notas del histórico; en español y en inglés; el celular sin desborde; sin errores
de página ni de consola. Datos de formato 11 (MFF_DATOS)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
RAIZ = RAIZ
SP = PRUEBAS
ok = Chequeo()
D = json.load(open(f'{RAIZ}/scripts/contenido/dudas.json', encoding='utf-8'))['dudas']
CTP_ES = {c['id']: c for c in json.load(open(f'{RAIZ}/fuentes/juego-es/ctps.json', encoding='utf-8'))['ctps']}
por = {}
for d in D:
    por.setdefault((d['sobre']['tipo'], d['sobre']['id']), []).append(d)
print('dudas:', len(D), 'sobre', len(por), 'cosas')

FUERA = """(w) => { const out = [];
  for (const el of document.querySelectorAll('main *')) { if (!el.checkVisibility()) continue; const r = el.getBoundingClientRect();
    if (r.width && r.right > w + 1) out.push(el.className || el.tagName); }
  return { doc: document.documentElement.scrollWidth, fuera: [...new Set(out)].slice(0, 8) }; }"""

def abrir(pg, nombre, uid=''):
    pg.evaluate("window.scrollTo(0,0)")
    if pg.locator('[data-a="back"]').count(): pg.click('[data-a="back"]')
    if not pg.locator('#q').count(): pg.locator('nav [data-a="back"], [data-a="back"]').first.click(); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{nombre.lower()}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid: pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(200)


srv, url = levantar(carpeta_datos(), origen_local())
errores, consola = [], []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: consola.append(m.text) if m.type == 'error' else None)
        pg.goto(url); pg.wait_for_selector('.ccard')
        ok('datos de formato 11 o más nuevo, con MFF_DUDAS', pg.evaluate('window.MFF_VERSION.formato') >= 11 and pg.evaluate('!!window.MFF_DUDAS'))
        n_datos = pg.evaluate('Object.values(window.MFF_DUDAS).reduce((n, o) => n + Object.values(o).reduce((m, l) => m + l.length, 0), 0)')
        ok('todas las dudas llegan a los datos', n_datos == len(D), (n_datos, len(D)))
        ok('cada C.T.P. trae sus nombres en español', pg.evaluate('MFF_CTPS.every(c => c.es && c.es.base && c.es.poderoso && c.es.brillante)'))

        # ---- Glosario: términos y efectos ----
        pg.click('[data-a="goGlosario"]'); pg.wait_for_selector('.glitem')
        gl = {i for (t, i) in por if t == 'glosario'}
        marcados = set(pg.evaluate("[...document.querySelectorAll('details.glitem')].filter(d => d.querySelector('summary .dudatag')).map(d => d.id.slice(3))"))
        ok('glosario: llevan la marca los términos con duda, y solo esos', marcados == gl, sorted(marcados ^ gl))
        w = pg.locator('#gl-wall')
        ok('Muro: la marca a la vista, la caja plegada', w.locator('summary .dudatag').inner_text().strip().lower() == '≠ dudoso' and not w.locator('.dudacaja').is_visible())
        w.locator('summary').click()
        caja = w.locator('.dudacaja').inner_text()
        ok('Muro abierto: la nota y lo que dice cada idioma', 'Barrera' in caja and '방벽' in caja and 'Coreano (original):' in caja, caja[:200])
        ok('Muro: la fuente', w.locator('.dudacaja .fuente').count() >= 1)
        pg.click('[data-a="glTab"][data-v="app"]'); pg.wait_for_selector('.glef')
        ef = {i for (t, i) in por if t == 'efecto'}
        marc_ef = set(pg.evaluate("[...document.querySelectorAll('details.glef')].filter(d => d.querySelector('summary .dudatag')).map(d => d.id.slice(3))"))
        ok('efectos: llevan la marca los que tienen duda, y solo esos', marc_ef == ef, sorted(marc_ef ^ ef))
        pg.evaluate("document.getElementById('ef-golpes_encadenados').open = true")
        ok('impacto en cadena: la caja dice los dos nombres del español', 'daño infligido por cadena' in pg.locator('#ef-golpes_encadenados .dudacaja').inner_text())

        # ---- Ficha de Gorr (The God Butcher): skills, «Cómo funciona», C.T.P. ----
        abrir(pg, 'Gorr', 'gorr-10100253')
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(400)
        sk = {i.split('|')[1] for (t, i) in por if t == 'skill' and i.startswith('gorr2|')}
        n = pg.locator('#fcuerpo details.duda').count()
        ok('skills de Gorr (uniforme): un «≠» por skill con duda', n == len(sk), (n, len(sk)))
        dd = pg.locator('#fcuerpo details.duda').first
        dd.locator('summary').click()
        tx = dd.locator('.ayudatx').inner_text()
        ok('el «≠» abre la nota y lo que dice cada idioma', 'Inglés:' in tx and 'Español del juego:' in tx, tx[:200])
        ok('la nota usa el vocabulario del juego', 'debuff' not in tx.split('Inglés:')[0].lower(), tx[:200])
        dd.locator('summary').click()
        pg.select_option('select[data-a="uniformSel"]', 'base'); pg.wait_for_timeout(200)
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(300)
        ok('Gorr base: sin «≠» en las skills (las dudas son del uniforme)', pg.locator('#fcuerpo details.duda').count() == 0, pg.locator('#fcuerpo details.duda').count())
        # Armado: las stats con duda y los C.T.P. con su nombre en español
        pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(400)
        nombres = pg.evaluate("[...document.querySelectorAll('#fcuerpo details.ctp > summary b')].map(b => b.textContent)")
        ok('C.T.P. en la ficha: con el nombre del juego en español', nombres and all(n.startswith('C.T.P. de ') for n in nombres), nombres)
        cortos = pg.evaluate("[...document.querySelectorAll('#fcuerpo')].map(e => e.innerText)")[0]
        ok('sin «C.T.P. of» en español', 'C.T.P. of' not in cortos)
        st = pg.locator('#fcuerpo details.duda')
        ok('Armado: hay stats con «≠»', st.count() >= 1, st.count())

        # Modos: los C.T.P. de cada grupo, con su nombre y su marca
        def ctps_modos():
            pg.click('[data-a="goModos"]'); pg.wait_for_timeout(300)
            vistos = {}
            for i in range(pg.locator('[data-a="modoAbrir"]').count()):
                pg.locator('[data-a="modoAbrir"]').nth(i).click(); pg.wait_for_timeout(150)
                for d in pg.evaluate("[...document.querySelectorAll('details.ctp')].map(d => ({n: d.querySelector('summary b').textContent, m: !!d.querySelector('summary .dudatag'), c: (d.querySelector('.dudacaja') || {}).textContent || '', s: d.querySelector('summary').textContent}))"):
                    vistos[d['n']] = d
                if pg.locator('[data-a="modoAbrir"]').nth(i).count(): pg.locator('[data-a="modoAbrir"]').nth(i).click(); pg.wait_for_timeout(100)
            return vistos
        vm = ctps_modos()
        ok('Modos: los C.T.P. con el nombre del juego en español', vm and all(n.startswith('C.T.P. de ') for n in vm), list(vm)[:5])
        j = vm.get('C.T.P. de justiciero')
        ok('C.T.P. de justiciero: con la marca y la caja', j and j['m'] and 'todo tipo de daño' in j['c'], j)
        ins = vm.get('C.T.P. de percepción')
        ok('C.T.P. sin duda: sin marca', ins and not ins['m'], ins)
        con = {CTP_ES[i]['base'] for (t, i) in por if t == 'ctp'}
        ok('llevan la marca los C.T.P. con duda, y solo esos', {n for n, d in vm.items() if d['m']} == con & set(vm), sorted({n for n, d in vm.items() if d['m']} ^ (con & set(vm))))

        # ---- Histórico: las notas con duda (Silk, 1.8.0) ----
        pg.click('[data-a="goHistorico"]'); pg.wait_for_selector('.hiversion')
        pg.select_option('select[data-a="hiPj"]', 'silk'); pg.wait_for_timeout(300)
        for _ in range(10):
            if pg.locator('a[href$="/173001"]').count() or not pg.locator('[data-a="hiMas"]').count(): break
            pg.click('[data-a="hiMas"]'); pg.wait_for_timeout(200)
        pg.evaluate("document.querySelectorAll('details.hiversion').forEach(d => d.open = true)")
        nota = pg.locator('.hinotas', has=pg.locator('a[href$="/173001"]'))
        ok('nota 1.8.0: el «≠» junto al link', nota.locator('details.duda').count() == 1, nota.count())
        if nota.count():
            nota.locator('details.duda summary').click()
            ok('nota 1.8.0: la nota en español', 'Military Resistance' in nota.locator('.ayudatx').inner_text())
        n_duda = pg.locator('.hinotas details.duda').count()
        ok('las otras notas de Silk sin «≠»', n_duda == 1, n_duda)

        # ---- en inglés ----
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ve = ctps_modos()
        j = ve.get('C.T.P. of Judgment')
        ok('inglés: C.T.P. of Judgment, con la marca en inglés', j and '≠ doubtful' in j['s'], list(ve)[:4])
        ok('inglés: la nota en inglés', j and 'The Spanish game says' in j['c'], j)
        pg.click('[data-a="goGlosario"]'); pg.wait_for_selector('.glitem')
        pg.click('[data-a="glTab"][data-v="juego"]'); pg.wait_for_selector('#gl-wall')
        pg.locator('#gl-wall summary').click()
        ok('inglés: Muro con la nota en inglés', 'Korean (original):' in pg.locator('#gl-wall .dudacaja').inner_text())
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)

        # ---- celular ----
        m = b.new_page(viewport={'width': 390, 'height': 800})
        m.on('pageerror', lambda e: errores.append(str(e)))
        m.goto(url); m.wait_for_selector('.ccard')
        abrir(m, 'Gorr', 'gorr-10100253')
        m.click('[data-a="fichaTab"][data-v="skills"]'); m.wait_for_timeout(300)
        m.locator('#fcuerpo details.duda summary').first.click()
        r = m.evaluate(FUERA, 390)
        ok('celular: el «≠» abierto no desborda', r['doc'] <= 390 and not r['fuera'], r)
        m.screenshot(path=f'{SP}/dudas_390.png')
        abrir(pg, 'Gorr', 'gorr-10100253')
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(300)
        pg.locator('#fcuerpo details.duda summary').first.click()
        pg.screenshot(path=f'{SP}/dudas_1300.png')
        b.close()
finally:
    srv.terminate()
ok('sin errores de página', not errores, errores[:3])
ok('sin errores de consola', not consola, consola[:3])
ok.fin()
