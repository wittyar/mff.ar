"""El «Give Power» que ninguna fuente publica (carril Q, segunda parte, punto 4; 5 de octubre de 2026).

- Los datos: las variantes cuya Leader Skill trae un «Give Power» sin lo que otorga (la entrada «otorga» del análisis
  que sale de la Leader Skill) son las que da un modelo escrito acá desde las skills: un «Give Power» sin nada detrás
  en su etapa (o con lo de detrás para otro objetivo, en una etapa con un objetivo para cada efecto) ni en las etapas
  siguientes. Son 21: los 19 pares con Leads & Supports y Mephisto — Master of Hell y Sentry — Thunderbolts*, que
  tienen el liderazgo derivado. Kang the Conqueror entra (antes el análisis tomaba su «Give Power» como envoltorio
  de la suba de ataque para él).
- La app: en «Lo que le da al equipo» (Resumen), el aviso de que la Leader Skill da un poder que ninguna fuente
  publica, en las 21 menos Mephisto — Master of Hell, cuyo «Give Power» lo dice el juego (carril de cierre: el liderazgo
  derivado lo trae, con la fuente del juego), y en ninguna otra de una muestra; en español y en inglés, y en el celular
  sin pasarse de ancho.
  En los pares no dice nada más (no se deduce de Leads & Supports): el texto es el mismo.

  MFF_DATOS=CARPETA python3 verif_otorga.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
X = datos_js('MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_TABLAS', 'MFF_ANALISIS', 'MFF_CATALOGO', 'MFF_SOPORTES')
CH, SK, TB, AN, CAT, SO = (X[k] for k in ('MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_TABLAS', 'MFF_ANALISIS', 'MFF_CATALOGO',
                                          'MFF_SOPORTES'))
OTORGA = next(i for i, e in enumerate(CAT['efectos']) if e['id'] == 'otorga')
ES = 'Su Leader Skill da un poder que ninguna fuente publica («Give Power»: la API no dice qué otorga ni por cuánto tiempo).'
EN = 'Its Leader Skill grants a power no source publishes ("Give Power": the API does not say what it grants or for how long).'

# ---- datos ----
de_datos = {p for p, a in AN.items() for ie, _, _, fs in a['fx'] if ie == OTORGA and any(SK[p][si]['sl'] == 'Leader Skill' for si, _, _ in fs)}


def vacio(etapas, ti, fi):
    st = etapas[ti]
    por_efecto = st.get('tg') is not None and TB['tgt'][st['tg']]['en'].startswith('All Allies for the first effect')
    return (not st['fx'][fi + 1:] or por_efecto) and not any(x['fx'] for x in etapas[ti + 1:])


modelo = {p for p, sks in SK.items() for sk in sks if sk['sl'] == 'Leader Skill' for ti, st in enumerate(sk['st'])
          for fi, f in enumerate(st['fx']) if TB['ab'][f['a']]['en'] == 'Give Power' and vacio(sk['st'], ti, fi)}
ok('1 datos: las variantes con el «Give Power» vacío en la Leader Skill son las del modelo', de_datos == modelo,
   sorted(de_datos ^ modelo))
con_ls = {p for p in de_datos if any(k in SO.get(p, {}) and SO[p][k].get('src') != 'api' for k in ('leader', 'leader2'))}
ok('1 son 21: 19 con Leads & Supports y Mephisto — Master of Hell y Sentry — Thunderbolts* con el derivado',
   len(de_datos) == 21 and len(con_ls) == 19 and de_datos - con_ls == {'mephisto1', 'sentry2'}, sorted(de_datos - con_ls))
ok('1 Kang the Conqueror entra (sus dos variantes)', {'kang', 'kang1'} <= de_datos)
# Carril de cierre (5 de octubre de 2026): el «Give Power» de Mephisto — Master of Hell lo dice el juego, y su liderazgo
# derivado lo trae con esa fuente (otorga). Ahí no va el aviso.
resueltos = {p for p in de_datos if any(SO.get(p, {}).get(k, {}).get('otorga') for k in ('leader', 'leader2'))}
ok('1 el de Mephisto — Master of Hell lo resuelve el juego (liderazgo con otorga)', resueltos == {'mephisto1'}
   and SO['mephisto1']['leader2'].get('otorga') == ['juego-ficha-ko'], sorted(resueltos))
avisan = de_datos - resueltos

# ---- la app ----
donde = {}
for c in CH:
    donde[c['p']] = (c, '')
    for u in c['uniforms']:
        donde[u['p']] = (c, u['id'])
random.seed(5)
sin = sorted(set(random.sample(sorted(set(donde) - de_datos), 12)) | {'thanos', 'sentinel2'})


def abrir(pg, p):
    c, uid = donde[p]
    if pg.locator('[data-a="back"]').count():
        pg.click('[data-a="back"]')
    pg.fill('#q', c['name']); pg.wait_for_timeout(200)
    pg.click(f'.ccard[data-cid="{c["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid:
        pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(150)
    pg.wait_for_selector('details.usodet', state='attached'); pg.evaluate("document.querySelector('details.usodet').open = true")
    return pg.locator('details.usodet .usotorga')


D = carpeta_datos()
srv, url = levantar(D, origen_local())
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append(m.text) if m.type == 'error' else None)
        pg.goto(url); pg.wait_for_selector('.ccard')
        mal = []
        for p in sorted(avisan):
            av = abrir(pg, p)
            txt = av.inner_text() if av.count() == 1 else None
            # El aviso va antes de los liderazgos, en «Qué le da al equipo» (arriba) y en su detalle plegado (1.0.27).
            dentro = pg.evaluate("""() => { const a = document.querySelector('details.usodet .usotorga');
              const s = a && a.closest('details').querySelector('.sops');
              const r = document.querySelector('.resumen3 .usotorga'), d = r && r.closest('.bloque').querySelector('.rsda');
              return !!(a && s && (a.compareDocumentPosition(s) & Node.DOCUMENT_POSITION_FOLLOWING)
                        && r && r.textContent === a.textContent && d && (r.compareDocumentPosition(d) & Node.DOCUMENT_POSITION_FOLLOWING)); }""")
            if txt != '⚠ ' + ES or not dentro:
                mal.append((p, txt, dentro))
        ok(f'2 el aviso, en las {len(avisan)}, antes de sus liderazgos', not mal and len(avisan) == 20, mal[:3])
        mal = [p for p in sin if abrir(pg, p).count()]
        ok(f'2 en ninguna otra (muestra de {len(sin)})', not mal, mal)
        # Mephisto — Master of Hell: sin aviso; el segundo liderazgo, con su fuente del juego.
        av = abrir(pg, 'mephisto1')
        uso = pg.locator('details.usodet')
        sops = uso.locator('.sop')
        segundo = sops.nth(1).inner_text() if sops.count() > 1 else ''
        titulo = sops.nth(1).locator('.srcapi').get_attribute('title') if sops.count() > 1 and sops.nth(1).locator('.srcapi').count() else ''
        fuentes = uso.locator('.fuentes').first.inner_text() if uso.locator('.fuentes').count() else ''
        ok('2 Mephisto — Master of Hell: sin aviso, y el «Give Power» del juego con su fuente', av.count() == 0 and sops.count() == 2
           and 'según la skill del juego' in segundo.lower() and 'ficha del juego' in (titulo or '') and '영웅 정보' in fuentes,
           (av.count(), sops.count(), segundo[:160], titulo, fuentes[:200]))
        # Un par: lo que publica Leads & Supports se muestra igual, sin nada deducido.
        abrir(pg, 'thanos5')
        sops = pg.locator('details.usodet .sop').count()
        ok('3 Thanos (par): el aviso y sus slots de Leads & Supports, sin más', sops >= 2 and pg.locator('details.usodet .usotorga').count() == 1, sops)
        # En inglés.
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        av = abrir(pg, 'kang')
        ok('4 en inglés', av.count() == 1 and av.inner_text() == '⚠ ' + EN, av.inner_text() if av.count() else None)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        # En el celular.
        m = b.new_page(viewport={'width': 390, 'height': 844}); m.on('pageerror', lambda e: errores.append(str(e)))
        m.goto(url); m.wait_for_selector('.ccard')
        av = abrir(m, 'sentry2')
        ancho = m.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
        caja = av.bounding_box() if av.count() else None
        ok('5 en el celular: se ve entero y la página no se pasa de ancho', caja is not None and caja['x'] >= 0
           and caja['x'] + caja['width'] <= 390 and ancho[0] <= ancho[1], (caja, ancho))
        m.screenshot(path=f'{SALIDA}/otorga_390.png')
        ok('6 sin errores de página ni de consola', not errores, errores[:3])
        b.close()
finally:
    srv.terminate()
ok.fin()
