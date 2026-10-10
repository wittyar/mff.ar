"""Carril de cierre (5 de octubre de 2026): lo que el próximo build corrige de thanosvibs con el juego, en la app.

- Datos (los de armar_datos_cierre.py): el C.T.P. judgement se llama «Judgment» y trae el nombre de thanosvibs (tv) y
  su fuente (f); la línea «Applies to: Self» de Planet Eater pasa a «Applies to: Allies with Power Cosmic Ability», con
  tv, f y su traducción en MFF_TXT; ningún otro dato lleva tv.
- La app: en Armado de Galactus, la línea del artefacto en español y en inglés, marcada con ⚠ y lo que dice thanosvibs
  en el título, y el códice de artefactos del juego entre las fuentes del artefacto; el artefacto de otro (Annihilus), sin marca. En el
  Glosario, Type Amplification lo da «Judgment (opción de reforjado)». En el celular, Armado no se pasa de ancho. Sin
  errores de página ni de consola.

  MFF_DATOS=CARPETA python3 verif_cierre.py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
X = datos_js('MFF_CTPS', 'MFF_ARTEFACTOS', 'MFF_TXT', 'MFF_SEED_CHARACTERS')
J = next(c for c in X['MFF_CTPS'] if c['id'] == 'judgement')
ok('1 datos: Judgment, con el nombre de thanosvibs y la fuente', J['name'] == 'Judgment' and J.get('tv') == 'Judgement'
   and J.get('f') == ['juego-ctp'] and not [c['id'] for c in X['MFF_CTPS'] if 'tv' in c and c['id'] != 'judgement'], J)
PE = next(a for a in X['MFF_ARTEFACTOS'] if a['p'] == 'galactus')
lin = [ln for ln in PE['lineas'] if 'tv' in ln]
NUEVA = 'Applies to: Allies with Power Cosmic Ability'
ok('1 datos: Planet Eater, la línea del juego con la de thanosvibs, la fuente y su traducción',
   len(lin) == 1 and lin[0]['t'] == NUEVA and lin[0]['tv'] == 'Applies to: Self' and lin[0]['f'] == ['juego-artefactos-ko']
   and X['MFF_TXT'].get(NUEVA) == 'Aplica a: aliados con la habilidad Poder Cósmico', lin)
otras = [(a['p'], ln['t']) for a in X['MFF_ARTEFACTOS'] for ln in a['lineas'] if 'tv' in ln and a['p'] != 'galactus']
ok('1 datos: ninguna otra línea de artefacto corregida', not otras, otras[:3])

GAL = next(c for c in X['MFF_SEED_CHARACTERS'] if c['p'] == 'galactus')
ANN = next(c for c in X['MFF_SEED_CHARACTERS'] if c['p'] == 'annihilus')


def armado(pg, c):
    if pg.locator('[data-a="back"]').count():
        pg.click('[data-a="back"]')
    pg.fill('#q', c['name']); pg.wait_for_timeout(200)
    pg.click(f'.ccard[data-cid="{c["id"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_selector('.artlineas')
    return pg.locator('.artlineas')


srv, url = levantar(carpeta_datos(), origen_local())
errores = []
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: errores.append(m.text) if m.type == 'error' else None)
        pg.goto(url); pg.wait_for_selector('.ccard')
        art = armado(pg, GAL)
        marca = art.locator('.corr')
        primera = art.locator('.artl').first.inner_text()
        fuentes = art.locator('xpath=..').locator('.fuentes').last.inner_text()
        ok('2 Galactus: la línea del juego, marcada, con lo que dice thanosvibs en el título',
           'Aplica a: aliados con la habilidad Poder Cósmico' in primera and marca.count() == 1
           and 'thanosvibs dice «Applies to: Self»' in (marca.get_attribute('title') or ''), (primera, marca.count(), marca.get_attribute('title') if marca.count() else None))
        ok('2 Galactus: las fuentes del artefacto suman el códice de artefactos del juego', 'Artifacts' in fuentes and '아티팩트 도감' in fuentes, fuentes[:200])
        art = armado(pg, ANN)
        ok('2 Annihilus: su artefacto sin marca', art.locator('.corr').count() == 0 and '아티팩트 도감' not in art.locator('xpath=..').locator('.fuentes').last.inner_text())
        pg.click('[data-a="goGlosario"]'); pg.wait_for_selector('.glitem')
        pg.locator('#gl-type_amplification > summary').click()
        ta = pg.locator('#gl-type_amplification').inner_text()
        ok('3 Glosario: Type Amplification lo da Judgment', 'Lo da: Justiciero (opción de reforja)' in ta and 'Judgement' not in ta.split('Lo da:')[1].split('\n')[0], ta[:400])
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        art = armado(pg, GAL)
        marca = art.locator('.corr')
        ok('4 en inglés: la línea y la marca', NUEVA in art.locator('.artl').first.inner_text() and marca.count() == 1
           and 'thanosvibs says "Applies to: Self"' in (marca.get_attribute('title') or ''), (art.locator('.artl').first.inner_text(), marca.get_attribute('title') if marca.count() else None, marca.count()))
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        m = b.new_page(viewport={'width': 390, 'height': 844}); m.on('pageerror', lambda e: errores.append(str(e)))
        m.goto(url); m.wait_for_selector('.ccard')
        armado(m, GAL)
        ancho = m.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
        ok('5 en el celular, Armado no se pasa de ancho', ancho[0] <= ancho[1], ancho)
        ok('6 sin errores de página ni de consola', not errores, errores[:3])
        b.close()
finally:
    srv.terminate()
ok.fin()
