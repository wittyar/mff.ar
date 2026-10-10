"""Objetivo de grupo tocable: en la ficha (cabecera de la skill y objetivo por etapa) y en
comparar, "→ Aliados de magia" abre una ventana con los personajes que lo cumplen, por
uniforme puesto. Se contrasta contra una cuenta hecha acá, aparte de la app."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

SHOTS = SALIDA
os.makedirs(SHOTS, exist_ok=True)
ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_TABLAS')
C, TGT = D['MFF_SEED_CHARACTERS'], D['MFF_TABLAS']['tgt']
por_nombre = {c['name']: c for c in C}


def esperado(r):
    """(cid, uid) de cada retrato que debería mostrar la ventana, calculado sin la app."""
    cat, val = r
    def cumple(v):
        return {'Ability': val in v['ab'], 'Type': v['c'] == val, 'Side': v['f'] == val, 'Allies': v['race'] == val}[cat]
    out = set()
    for c in C:
        base = {'c': c['c'], 'f': c['f'], 'race': c['race'], 'ab': c['abilities'], 'uid': ''}
        us = [{'c': u.get('c', c['c']), 'f': u.get('f', c['f']), 'race': u.get('race', c['race']),
               'ab': u.get('ab', c['abilities']), 'uid': u['id']} for u in c['uniforms']]
        if cumple(base):
            out.add((c['id'], ''))
        else:
            out |= {(c['id'], u['uid']) for u in us if cumple(u)}
    return out


def uid_de(nombre, uniforme):
    return next(u['id'] for u in por_nombre[nombre]['uniforms'] if u['name'] == uniforme)


def ir_a(pg, nombre, uid=''):
    pg.evaluate("() => window.scrollTo(0, 0)")
    if pg.locator('[data-a="back"]').count():
        pg.click('[data-a="back"]')
    pg.fill('#q', nombre); pg.wait_for_timeout(300)
    pg.click(f'.ccard[data-cid="{por_nombre[nombre]["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid:
        pg.select_option('select[data-a="uniformSel"]', uid)
    pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(150)


def ventana(pg):
    m = pg.locator('.modal.ancho')
    if not m.count():
        return None
    return {'titulo': m.locator('.altitulo').inner_text(),
            'cabecera': m.locator('.altitulo + div').inner_text(),
            'nota': m.locator('p.muted').first.inner_text() if m.locator('p.muted').count() else '',
            'tiles': {(t.get_attribute('data-cid'), t.get_attribute('data-uid')) for t in m.locator('.altile').all()},
            'notas': [(t.get_attribute('data-cid'), t.get_attribute('data-uid'),
                       t.locator('.alnota').inner_text() if t.locator('.alnota').count() else '')
                      for t in m.locator('.altile').all()]}


srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')

        # A. Wong con Doctor Strange 2: la pasiva Avance místico apunta a Aliados de magia
        w2 = uid_de('Wong', "Marvel Studios' Doctor Strange 2")
        ir_a(pg, 'Wong', w2)
        tarjeta = pg.locator('.skill', has_text='Avance místico')
        if not tarjeta.count():
            tarjeta = pg.locator('div', has=pg.locator('.nm', has_text='Avance místico')).last
        boton = tarjeta.locator('button.tag.objetivo[data-a="verAliados"]').first
        ok('A la cabecera de Avance místico es un botón', boton.count() == 1 and 'Aliados de magia'.upper() in boton.inner_text().upper(),
           boton.inner_text() if boton.count() else 'sin botón')
        boton.click(); v = ventana(pg)
        r_magia = next(t['r'] for t in TGT if t['en'] == 'Magic Allies')
        esp = esperado(r_magia)
        ok('A abre la ventana con el objetivo', v and v['titulo'] == 'Aliados de magia', v and v['titulo'])
        ok('A criterio y cuenta', v and 'Aplica a: habilidad' in v['cabecera'] and 'Magia' in v['cabecera']
           and f"{len({c for c, _ in esp})} personajes" in v['cabecera'], v and v['cabecera'])
        ok('A retratos = cuenta independiente', v and v['tiles'] == esp,
           v and f"de más: {sorted(v['tiles'] - esp)[:4]} | faltan: {sorted(esp - v['tiles'])[:4]}")
        wong = por_nombre['Wong']['id']
        tiles_wong = sorted(u for c, u in (v['tiles'] if v else []) if c == wong)
        ok('A Wong aparece con sus dos uniformes que tienen Magia', len(tiles_wong) == 2 and w2 in tiles_wong,
           [n for c, u, n in v['notas'] if c == wong] if v else None)
        ok('A aviso de que cuenta el uniforme puesto', v and 'uniforme que lleva puesto' in v['nota'], v and v['nota'])
        pg.screenshot(path=f'{SHOTS}/aliados_magia_1300.png')

        # B. cerrar: clic adentro no cierra, Esc sí, fondo sí; un retrato abre su ficha
        pg.click('.modal.ancho .altitulo'); ok('B clic adentro no cierra', ventana(pg) is not None)
        pg.keyboard.press('Escape'); ok('B Esc cierra', ventana(pg) is None)
        boton.click(); pg.mouse.click(5, 450); ok('B clic en el fondo cierra', ventana(pg) is None)
        boton.click()
        ds = por_nombre['Doctor Strange']['id']
        pg.click(f'.modal.ancho .altile[data-cid="{ds}"]'); pg.wait_for_timeout(300)
        ok('B un retrato abre la ficha y cierra la ventana', ventana(pg) is None
           and pg.locator('.fcab h1').text_content() == 'Doctor Strange', pg.locator('.fcab h1').text_content())

        # C. los objetivos que no son grupo quedan como texto; los botones son todos grupos
        grupos = {t['es'].upper() for t in TGT if t.get('r')}
        spans = [x.inner_text().replace('→', '').strip().upper() for x in pg.locator('span.tag.objetivo').all()]
        botones = [x.inner_text().replace('→', '').strip().upper() for x in pg.locator('button.tag.objetivo').all()]
        ok('C sin grupo: etiqueta sin botón', spans and not any(s in grupos for s in spans), spans[:4])
        ok('C con grupo: botón', all(x in grupos for x in botones), botones[:4])

        # D. objetivo de clase (líder de Ancient One: Detonación), con uniformes que cambian de clase
        ir_a(pg, 'Ancient One')
        pg.locator('button.tag.objetivo', has_text='Detonación').first.click(); v = ventana(pg)
        esp = esperado(['Type', 'Detonación'])
        ok('D clase Detonación: retratos = cuenta independiente', v and v['tiles'] == esp,
           v and f"{len(v['tiles'])} vs {len(esp)}")
        excepciones = [n for c, u, n in (v['notas'] if v else []) if n.startswith('Salvo con')]
        ok('D los que cambian de clase con un uniforme dicen con cuál no', bool(excepciones), excepciones[:2])
        pg.keyboard.press('Escape')

        # E. objetivo por etapa: Jessica Jones (Jewel), pasiva de uniforme -> Aliados de Defenders
        ir_a(pg, 'Jessica Jones', uid_de('Jessica Jones', 'Jewel'))
        link = pg.locator('button.objlink', has_text='Aliados de Defenders').first
        ok('E objetivo de etapa: enlace', link.count() == 1)
        link.click(); v = ventana(pg)
        esp = esperado(['Ability', 'Defensores'])
        ok('E abre Aliados de Defenders con sus personajes', v and v['titulo'] == 'Aliados de Defenders' and v['tiles'] == esp,
           v and (v['titulo'], len(v['tiles']), len(esp)))
        pg.keyboard.press('Escape')

        # F. comparar: la fila "Beneficia a" también abre la ventana
        ir_a(pg, 'Wong', w2)
        pg.click('[data-a="pickThis"]'); pg.wait_for_selector('.ccard')
        pg.fill('#q', 'Doctor Strange'); pg.wait_for_timeout(300)
        pg.click(f'.ccard[data-cid="{ds}"][data-uid=""]')
        pg.click('[data-a="goCompare"]'); pg.wait_for_timeout(300)
        pg.click('[data-a="cmpVista"][data-v="ficha"]'); pg.wait_for_timeout(300)   # desde la 1.0.35 abre por efecto
        bt = pg.locator('button.tag.objetivo[data-a="verAliados"]', has_text='Aliados de magia').first
        ok('F comparar: el objetivo es un botón', bt.count() == 1)
        bt.click(); v = ventana(pg)
        ok('F comparar: abre la ventana', v and v['titulo'] == 'Aliados de magia', v and v['titulo'])
        pg.keyboard.press('Escape')

        # G. en inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.locator('button.tag.objetivo[data-a="verAliados"]', has_text='Magic Allies').first.click(); v = ventana(pg)
        ok('G inglés: título, criterio y cuenta', v and v['titulo'] == 'Magic Allies' and 'Applies to: ability' in v['cabecera']
           and 'Magic' in v['cabecera'] and 'characters' in v['cabecera'], v and v['cabecera'])
        pg.keyboard.press('Escape'); pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('sin errores de página', not errores, errores[:3])
        b.close()

        # H. celular
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        ir_a(pg, 'Wong', w2)
        pg.locator('button.tag.objetivo[data-a="verAliados"]', has_text='magia').first.click()
        cols = pg.evaluate("getComputedStyle(document.querySelector('.algrid')).gridTemplateColumns.split(' ').length")
        ancho = pg.evaluate("[document.documentElement.scrollWidth, document.querySelector('.modal.ancho').getBoundingClientRect().right]")
        ok('H celular: 3 columnas y sin desborde', cols == 3 and ancho[0] <= 390 and ancho[1] <= 390, (cols, ancho))
        pg.screenshot(path=f'{SHOTS}/aliados_magia_390.png')
        ok('sin errores de página (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
