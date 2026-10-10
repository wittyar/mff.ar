"""«Qué hace con sus skills» (#33 con #7, 1.0.36, datos de formato 14): el bloque del Resumen y la lectura de cada skill,
contra un modelo escrito acá con MFF_ANALISIS, MFF_SKILLS y MFF_CATALOGO (valor y pvp): lo que lo distingue (raro: lo
tiene el 15% o menos; alto: su número es tanto o más que el del 90% de los que lo tienen, con 20 o más para comparar), las
filas de cada destino, el tiempo activo (duración ÷ recarga), lo que vale en PvP, el daño de cada skill, lo que el
catálogo lee solo en PvE, la lectura de la A2, en inglés, el celular sin desborde y sin errores. Datos: MFF_DATOS."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, DATOS
from playwright.sync_api import sync_playwright
ok = Chequeo()
SP = PRUEBAS
s = open(f'{DATOS}/data.js', encoding='utf-8').read()


def load(n):
    i = s.find(f'window.{n} = ') + len(f'window.{n} = '); j = s.find(';\n', i); return json.loads(s[i:j])


A, S, T, CAT = load('MFF_ANALISIS'), load('MFF_SKILLS'), load('MFF_TABLAS'), load('MFF_CATALOGO')
EF = CAT['efectos']
PAS = {'Leader Skill', 'Passive', 'Tier-2 Passive', 'Uniform Passive'}
P = 'abomination1'


def valor(f, e):
    i = CAT['valor'][str(f['p'])][e]
    if i is None: return None
    pat = T['desc'][f['p']]['en']; pos = [k for k, ch in enumerate(pat) if ch == '#'][i]
    return (f['v'][i], pat[pos + 1:pos + 2] == '%')


# rareza en el roster
tienen, vals = {}, {}
for p, an in A.items():
    vista = {}
    for ie, d, o, fu in an['fx']:
        k = f"{d}|{EF[ie]['id']}"
        for si, ti, fi in fu:
            x = valor(S[p][si]['st'][ti]['fx'][fi], EF[ie]['id'])
            if x and (vista.get(k) is None or x[0] > vista[k][0]): vista[k] = x
            vista.setdefault(k, None)
    for k, x in vista.items():
        tienen[k] = tienen.get(k, 0) + 1
        if x: vals.setdefault(k, []).append(x)
N = len(A)

filas = {}
for ie, d, o, fu in A[P]['fx']:
    e = EF[ie]['id']; r = filas.setdefault(f'{d}|{e}', {'d': d, 'e': e, 'f': []})
    for si, ti, fi in fu:
        sk = S[P][si]; f = sk['st'][ti]['fx'][fi]; dur = f.get('d')
        uso = min(1, dur / sk['cd']) if sk['sl'] not in PAS and sk.get('cd') and dur is not None and e != 'curacion' else None
        r['f'].append((sk['sl'], valor(f, e), dur, uso))
for k, r in filas.items():
    vs = [x[1] for x in r['f'] if x[1]]
    r['val'] = max(vs, key=lambda x: x[0]) if vs else None
    us = [x[3] for x in r['f'] if x[3] is not None]
    r['uso'] = max(us) if us else None
    r['tienen'] = round(100 * tienen[k] / N)
    pc = None
    if r['val']:
        comp = [x for x in vals.get(k, []) if x[1] == r['val'][1]]
        if len(comp) >= 20: pc = math.floor(100 * sum(1 for x in comp if x[0] <= r['val'][0]) / len(comp))
    r['pc'] = pc; r['alto'] = pc is not None and pc >= 90; r['raro'] = r['tienen'] <= 15
    r['pvp'] = (r['d'] in 'ei' and r['e'] in CAT['pvp']['prioridad']) or (r['d'] == 'q' and r['e'] in CAT['pvp']['soporte'])
dist = sorted([r for r in filas.values() if r['alto'] or r['raro']], key=lambda r: (-(r['pc'] if r['alto'] else 0), r['tienen']))[:6]
nombre = {e['id']: e['es'] for e in EF}
print('distingue (modelo):', [(nombre[r['e']], r['pc'], r['tienen']) for r in dist])

FUERA = """(w) => { const out = [];
  for (const el of document.querySelectorAll('main *')) { if (!el.checkVisibility()) continue; const r = el.getBoundingClientRect();
    if (r.width && r.right > w + 1) out.push(el.className || el.tagName); }
  return { doc: document.documentElement.scrollWidth, fuera: [...new Set(out)].slice(0, 8) }; }"""
srv, url = levantar(carpeta_datos(), origen_local())
errores, consola = [], []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: consola.append(m.text) if m.type == 'error' else None)
        pg.goto(url); pg.wait_for_selector('.ccard')
        ok('datos de formato 14, con MFF_CATALOGO.pvp', pg.evaluate('MFF_VERSION.formato') >= 14 and pg.evaluate('!!MFF_CATALOGO.pvp'))
        pg.fill('#q', 'Abomination'); pg.wait_for_timeout(300)
        pg.click('.ccard[data-cid="abomination"][data-uid="abomination-10100228"]'); pg.wait_for_selector('#analisis')
        chips = pg.evaluate("[...document.querySelectorAll('#analisis .qhdchip')].map(c => ({ m: c.querySelector('.qhmarca').textContent, n: c.querySelector('.annom').textContent }))")
        esperado = [{'m': f"TANTO O MÁS QUE EL {r['pc']}%" if r['alto'] else f"LO TIENE EL {r['tienen']}%", 'n': nombre[r['e']]} for r in dist]
        ok('lo que lo distingue: lo raro y lo alto, en el orden del modelo', chips == esperado, (chips, esperado))
        for d in 'qre':
            n = pg.locator(f'#analisis .qhpanel:has(.cpedot.{d}) .qhfila').count()
            m = sum(1 for r in filas.values() if r['d'] == d)
            ok(f'panel {d}: una fila por efecto (las de más de 6, plegadas)', n == m, (n, m))
        txt = pg.locator('#analisis').inner_text()
        ok('superarmadura: 71% del tiempo (10 s cada 14 s)', '71% del tiempo (10 s cada 14 s)' in txt)
        ok('el liderazgo: siempre activo, a los aliados zombis', 'Siempre activo · Aliados zombis' in txt)
        pvp = pg.evaluate("[...document.querySelectorAll('#analisis .qhfila')].filter(f => f.querySelector('.qhmarca.pvp')).map(f => f.querySelector('.annom').textContent)")
        ok('PvP: marcados los de la lista de Ezequiel, y solo esos', sorted(pvp) == sorted(nombre[r['e']] for r in filas.values() if r['pvp']), pvp)
        dn = pg.evaluate("[...document.querySelectorAll('#analisis .qhdanof')].map(f => f.querySelector('.cpev').textContent)")
        ok('daño por skill: A1 215% · 11%, DEF 455% · 23%', dn[0] == '215% · 11%' and dn[-1] == '455% · 23%', dn)
        pve = pg.locator('#analisis .qhmodos').inner_text()
        ok('solo en PvE: lo que no tiene lectura de PvP (quemadura, parálisis, silencio), sin la fractura', 'Quemadura' in pve and 'Silencio' in pve and 'Fractura' not in pve, pve[:300])
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(400)
        a2 = pg.locator('.skill', has=pg.locator('.slotbadge', has_text='Activa 2')).locator('.sklect').inner_text()
        ok('Skills, A2: daño 395% · 20% del total, la barrera alta y su tiempo activo', '395%' in a2 and '20% del total' in a2 and 'Barrera' in a2 and '44%' in a2, a2)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.click('[data-a="fichaTab"][data-v="resumen"]'); pg.wait_for_timeout(300)
        ok('inglés: el título y las marcas', 'what its skills do' in pg.locator('#analisis').inner_text().lower() and 'AT LEAST' in pg.locator('#analisis').inner_text())
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        pg.set_viewport_size({'width': 390, 'height': 800}); pg.wait_for_timeout(400)
        r = pg.evaluate(FUERA, 390)
        ok('celular: sin desborde', r['doc'] <= 390 and not r['fuera'], r)
        pg.screenshot(path=f'{SP}/que_hace_390.png', full_page=True)
        b.close()
finally:
    srv.terminate()
ok('sin errores de página', not errores, errores[:3])
ok('sin errores de consola', not consola, consola[:3])
ok.fin()
