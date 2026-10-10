"""Modos: lo que suma la guía del juego (World Boss con sus 6 dificultades, Team Battle Arena con 5
equipos, Story Ultimate en Nv. 70...) se ve en su modo, con la guía del juego como fuente sin enlace."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright
ok = Chequeo()
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        pg.click('[data-a="goModos"]'); pg.wait_for_timeout(400)
        CASOS = [('world-boss', 'Legend+', 'Mythic (Tier-4'), ('alliance-battle', 'Infinite Challenge', '1.000.000'),
                 ('alliance-conquest', 'las batallas son automáticas', None), ('zombie-survival', 'cambian cada semana', None),
                 ('team-battle-arena', 'hasta 5 equipos de 3', None), ('story-ultimate', 'de Nv. 70 o más', None),
                 ('giant-boss-raid', 'Entran hasta 3 jugadores', None), ('dimension-rift', 'Es cooperativo', None)]
        def abrir(i):
            pg.click(f'[data-a="modoAbrir"][data-id="{i}"]'); pg.wait_for_timeout(150)
            return pg.locator('.modo.on')
        for i, a, b2 in CASOS:
            card = abrir(i)
            texto = card.inner_text()
            ok(f'{i}: se ve «{a}»' + (f' y «{b2}»' if b2 else ''), a in texto and (b2 is None or b2 in texto), texto[:200])
            # Desde el carril ko-u (5 de octubre de 2026), algunos modos citan también la guía en coreano (juego-guia-ko),
            # cuyo nombre dice «la guía dentro del juego, en coreano», y Alliance Battle la cita en dos bloques: la inglesa,
            # al menos una vez, y ninguna con enlace.
            ok(f'{i}: la guía del juego como fuente, sin enlace', card.locator('span.fuente', has_text='guía dentro del juego (contenidos').count() >= 1
               and card.locator('a.fuente', has_text='guía dentro del juego').count() == 0)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        texto = abrir('team-battle-arena').inner_text()
        ok('en inglés también', 'up to 5 teams of 3' in texto, texto[:200])
        ok('sin errores de página', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
