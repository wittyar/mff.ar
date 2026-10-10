"""La guía de armado en la ficha (Resumen, Skills y Armado) contra la planilla leída aparte:
este modelo lee el CSV de la copia en uso con su propio código (no usa guia_armado.py) y
calcula lo que tiene que mostrarse. Se eligen filas hasta cubrir todos los valores
distintos de cada columna que se muestra. También: inglés, celular y datos sin la guía."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import csv, json, os, re, shutil, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js, RAIZ
from playwright.sync_api import sync_playwright

ok = Chequeo()
CARP = f'{RAIZ}/fuentes/guia-armado'
raw = list(csv.reader(open(f'{CARP}/champ-building.csv', encoding='utf-8', newline='')))
ie = next(i for i, f in enumerate(raw) if f and f[0] == 'PK')
enc = raw[ie]
col = lambda f, n: f[enc.index(n)].strip()
filas = [f for f in raw[ie + 1:] if f[0].strip()]
TR = json.load(open(f'{RAIZ}/scripts/traducciones/armado.json', encoding='utf-8'))
TV = json.load(open(f'{RAIZ}/work/characters.json'))
def k(s): return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())
retrato = {(k(r['character']), k(r['uniform'])): r['portrait'] for r in TV}
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_CTPS', 'MFF_GUIA')
var_de = {}
for c in D['MFF_SEED_CHARACTERS']:
    var_de[c['p']] = (c['id'], '', c['name'])
    for u in c['uniforms']: var_de[u['p']] = (c['id'], u['id'], c['name'])
CTP_NOMBRE = {c['id']: c['name'] for c in D['MFF_CTPS']}
tl = list(csv.reader(open(f'{CARP}/tier-list.csv', encoding='utf-8', newline='')))
ley_txt = next(c for f in tl[:5] for c in f if '🤝 =' in c).split('\n')[0]
EMO = {a: b.strip() for a, b in (p.split(' = ') for p in re.split(r'\s{2,}', ley_txt.strip()))}
ISO_SETS = {'offensive': ['Power of Angry Hulk', 'Overdrive', "Hawk's Eye"], 'shield': ['Drastic Density Enhancement', 'Binary Power'],
            'defensive': ['Protect the Captain', 'Tenacious Symbiote', 'Spider Sense']}
ADQ = {'SLS': 'Shadowland Selectors', 'SS': 'Dimension Mission Support Shop', 'EQ': 'Epic Quest', 'HQ': 'Heroic Quest'}
OB_OK = {'proc': 'Proc', 'invincible': 'Invincible', 'gbi': 'GBI', 'mini-rage': 'Mini-Rage', 'fire': 'Fire', 'lightning': 'Lightning',
         'mind': 'Mind', 'cold': 'Cold', 'poison': 'Poison', 'hp': 'HP'}
ROL = {'Best CTP': 'Mejor', '2nd Best CTP': '2.º mejor', 'Meta CTP (PVE)': 'Meta PvE', 'Off-Meta CTP (PVE)': 'Fuera del meta PvE',
       'Meta CTP (PVP)': 'Meta PvP', 'Off-Meta CTP (PVP)': 'Fuera del meta PvP'}
ROL_EN = {'Best CTP': 'Best', '2nd Best CTP': '2nd best', 'Meta CTP (PVE)': 'PvE meta', 'Off-Meta CTP (PVE)': 'PvE off-meta',
          'Meta CTP (PVP)': 'PvP meta', 'Off-Meta CTP (PVP)': 'PvP off-meta'}
v_ = lambda x: '' if x in ('', '-') else x

def esperado(f, lang='es'):
    tr = (lambda x: TR.get(x, x)) if lang == 'es' else (lambda x: x)
    p = retrato[(k(col(f, 'Best Uni Character Name')), k(col(f, 'Best Uniform')))]
    cid, uid, nombre = var_de[p]
    bl = v_(col(f, 'Tier List Bling')).replace('️', '')
    emos = sorted((bl.index(e.replace('️', '')), e) for e in EMO if e.replace('️', '') in bl)
    resto = bl
    for _, e in emos: resto = resto.replace(e.replace('️', ''), '')
    resto = re.sub(r'\s', '', resto)
    ctps = []
    for c in ROL:
        x = v_(col(f, c))
        if not x: continue
        clave = (x.rstrip('+'), x.endswith('+'))
        g = next((g for g in ctps if g[0] == clave), None)
        if not g: ctps.append(g := [clave, []])
        g[1].append((ROL if lang == 'es' else ROL_EN)[c])
    iso = v_(col(f, 'Best ISO-8 Set')).lower()
    iso_tok = [t for t in ['dont waste gold', 'offensive', 'defensive', 'shield'] if t in iso]
    iso_tok.sort(key=iso.index)
    iso_x = re.sub(r'[,\s]+', ' ', re.sub('dont waste gold|offensive|defensive|shield', ' ', iso)).strip()
    obs = [x.strip() for x in v_(col(f, 'Obelisk (SL/AC)')).split(',') if x.strip()]
    art = v_(col(f, 'Needs Artifact?'))
    m = re.fullmatch(r'([YXO])(?: \((PVP|PVE)\))?', art)
    leg = {'Y': 'Must have for character to function', 'X': 'Nice to have', 'O': 'Optional / Not needed'}
    art_txt = (tr(leg[m.group(1)]) + (' (' + {'PVP': 'PvP', 'PVE': 'PvE'}[m.group(2)] + ')' if m.group(2) else '')) if m else (tr(art) if art in ('N', 'Optional', 'Support') else art)
    return {
        'pk': f[0], 'nombre': nombre, 'cid': cid, 'uid': uid,
        'rank': v_(col(f, 'Tier List Rank')), 'emojis': [e + ' ' + tr(EMO[e]) for _, e in emos], 'bl_x': resto,
        'adq': [x + (' · ' + ADQ[x] if x in ADQ else '') for x in re.split(r'\s*[,;/]\s*', v_(col(f, 'Acquisition'))) if v_(x)],
        'nota': tr(v_(col(f, 'Notes'))),
        'rot': [v for v in (v_(col(f, 'Proc Rotation')), v_(col(f, 'Best CTP Rotation')), v_(col(f, 'Proc/Frenzy Skill')))],
        'ctp': [(('C.T.P. of ' + CTP_NOMBRE[n.lower()]) if n.lower() in CTP_NOMBRE else n, r, roles) for (n, r), roles in ctps],
        'iso': [(tr(t), ISO_SETS.get(t, [])) for t in iso_tok], 'iso_x': iso_x,
        'ob': [tr(OB_OK[x.lower()]) for x in obs if x.lower() in OB_OK], 'ob_x': [x for x in obs if x.lower() not in OB_OK],
        'art': art_txt,
    }

# Filas: hasta cubrir cada valor distinto de lo que se muestra, más casos puntuales.
cubrir = ['Tier List Rank', 'Tier List Bling', 'Acquisition', 'Best ISO-8 Set', 'Obelisk (SL/AC)', 'Needs Artifact?', 'Notes',
          'Best CTP', '2nd Best CTP', 'Meta CTP (PVE)', 'Off-Meta CTP (PVE)', 'Meta CTP (PVP)', 'Off-Meta CTP (PVP)']
vistos, elegidas = set(), []
for f in filas:
    nuevos = {(c, col(f, c)) for c in cubrir} - vistos
    if nuevos: elegidas.append(f); vistos |= nuevos
for pk in ('HULKCHO', 'AGENTVEN', 'ABOM'):       # renombrado por uniforme, base vs uniforme, rotación
    f = next(x for x in filas if x[0] == pk)
    if f not in elegidas: elegidas.append(f)
print('filas elegidas:', len(elegidas))

def texto(loc): return loc.evaluate('e => e.textContent.replace(/\\s+/g, " ").trim()')
def bloque_resumen(pg): return pg.locator('.usogrid .bloque', has=pg.locator('h4', has_text=re.compile('Cynicalex')))

def abrir(pg, cid, uid=''):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', ''); pg.wait_for_timeout(50)
    nombre = next(c['name'] for c in D['MFF_SEED_CHARACTERS'] if c['id'] == cid)
    pg.fill('#q', nombre); pg.wait_for_timeout(200)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid: pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(100)

def leer_ficha(pg):
    out = {}
    pg.click('[data-a="fichaTab"][data-v="resumen"]'); pg.wait_for_timeout(120)
    b = bloque_resumen(pg)
    mp = b.locator('.ga-mejor .minipj')
    out['best'] = (mp.get_attribute('data-cid'), mp.get_attribute('data-uid') or '')
    out['este'] = b.locator('.ga-mejor', has_text='el que estás viendo').count() == 1
    out['rank'] = texto(b.locator('.ga-tier .tag.ghost')) if b.locator('.ga-tier .tag.ghost').count() else ''
    out['emojis'] = [texto(x) for x in b.locator('.ga-tier .tag.dim').all()]
    out['bl_x'] = texto(b.locator('.ga-tier .sinint')) if b.locator('.ga-tier .sinint').count() else ''
    out['adq'] = [texto(x) for x in b.locator('.ga-adq .tag').all()]
    out['nota'] = texto(b.locator('.ga-nota')) if b.locator('.ga-nota').count() else ''
    out['version'] = texto(b.locator('.fuentes .tag'))
    pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(120)
    out['rot'] = [texto(pg.locator(f'.ga-rot .rot[data-k="{k}"] .rotd')) if pg.locator(f'.ga-rot .rot[data-k="{k}"]').count() else ''
                  for k in ('ga_rot', 'ga_rotc', 'ga_proc')]
    out['rot_none'] = pg.locator('.section', has_text='La guía de armado no le da rotación.').count() > 0
    pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(150)
    out['ctp'] = []
    for d in pg.locator('.ga-ctp > *').all():
        nom = texto(d.locator('b').first) if d.locator('b').count() else texto(d.locator('.sinint'))
        out['ctp'].append((nom, d.locator('.ctproles .tag.solid').count() == 1,
                           [texto(x) for x in d.locator('.ctproles .tag.ghost').all()]))
    out['iso'] = [(texto(x.locator('b')), [x2.evaluate('e => e.firstChild.textContent') for x2 in x.locator('.isoset').all()])
                  for x in pg.locator('.isocat').all()]
    out['iso_x'] = texto(pg.locator('.ga-iso-x')) if pg.locator('.ga-iso-x').count() else ''
    out['ob'] = [texto(x) for x in pg.locator('.ga-ob .tag').all()]
    out['ob_x'] = [texto(x) for x in pg.locator('.ga-ob .sinint').all()]
    out['art'] = texto(pg.locator('.ga-art b, .ga-art .sinint').first) if pg.locator('.ga-art').count() else ''
    return out

def comparar(nombre, e, f):
    campos = ['rank', 'emojis', 'bl_x', 'adq', 'nota', 'rot', 'ctp', 'iso', 'iso_x', 'ob', 'ob_x', 'art']
    malos = [c for c in campos if e[c] != f[c]]
    ok(f'{nombre} ({e["pk"]})', (e['cid'], e['uid']) == f['best'] and not malos and f['version'] == 'V12.2.0',
       {c: (e[c], f[c]) for c in malos} or f['best'])

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        for f in elegidas:
            e = esperado(f)
            abrir(pg, e['cid'])
            got = leer_ficha(pg)
            comparar(e['nombre'], e, got)
        # el mejor uniforme abierto: «el que estás viendo» y sin rótulo de otra variante
        e = esperado(next(x for x in filas if x[0] == 'AGENTVEN'))
        abrir(pg, e['cid'], e['uid']); got = leer_ficha(pg)
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(100)
        ok('con el mejor uniforme abierto: lo dice y no rotula otra variante', got['este'] and pg.locator('.ga-rot .varx').count() == 0)
        abrir(pg, e['cid'])
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(100)
        ok('con la base abierta: la rotación dice de qué uniforme es', texto(pg.locator('.ga-rot .varx').first) == 'Guardians of the Galaxy')
        # tocar el mejor uniforme lo abre, en la misma pestaña
        pg.click('[data-a="fichaTab"][data-v="resumen"]'); pg.wait_for_timeout(100)
        bloque_resumen(pg).locator('.ga-mejor .minipj').click(); pg.wait_for_timeout(200)
        ok('tocar el mejor uniforme abre la ficha con ese uniforme', pg.locator('select[data-a="uniformSel"]').input_value() == e['uid'])
        # inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        con_nota = next(x for x in elegidas if v_(col(x, 'Notes')) and col(x, 'Notes') in TR and TR[col(x, 'Notes')] != col(x, 'Notes'))
        e = esperado(con_nota, 'en'); abrir(pg, e['cid'])
        got = leer_ficha(pg)
        comparar('inglés: ' + e['nombre'], e, got)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('sin errores de página', not errores, errores[:3])
        b.close()

        # celular: nada se sale de la pantalla en las tres pestañas
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        # Lo que está dentro de un contenedor con scroll horizontal propio (las tablas de etapas
        # de las skills) no cuenta: se desplaza adentro, la página no.
        FUERA = """() => { const conScroll = (e) => { for (let x = e.parentElement; x; x = x.parentElement) if (getComputedStyle(x).overflowX !== 'visible') return true; return false; };
          return [...document.querySelectorAll('.fcuerpo *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > innerWidth + 0.5 && !e.closest('details:not([open])') && !conScroll(e); })
          .map(e => (e.className || e.tagName) + ' → ' + Math.round(e.getBoundingClientRect().right)).slice(0, 4).concat(document.scrollingElement.scrollWidth > innerWidth ? ['página: ' + document.scrollingElement.scrollWidth] : []); }"""
        for pk in ('AGENTVEN', 'ABOM', next(x[0] for x in filas if 'Inv' in [t.strip() for t in col(x, 'Obelisk (SL/AC)').split(',')])):
            e = esperado(next(x for x in filas if x[0] == pk)); abrir(pg, e['cid'])
            for tab in ('resumen', 'skills', 'armado'):
                pg.click(f'[data-a="fichaTab"][data-v="{tab}"]'); pg.wait_for_timeout(150)
                fuera = pg.evaluate(FUERA)
                ok(f'celular {e["nombre"]} / {tab}: nada se sale', not fuera, fuera)
        ok('sin errores de página (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()

# datos sin la guía (de antes de 1.0.8): la ficha lo dice y no se rompe
d = carpeta_datos()
js = open(os.path.join(d, 'data.js'), encoding='utf-8').read()
js2 = re.sub(r'\nwindow\.MFF_GUIA_ARMADO = .*?;\n', '\n', js, count=1)
assert js2 != js
open(os.path.join(d, 'data.js'), 'w', encoding='utf-8').write(js2)
srv, url = levantar(d, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        abrir(pg, esperado(next(x for x in filas if x[0] == 'AGENTVEN'))['cid'])
        aviso = 'Los datos cargados no traen la guía de armado'
        r = aviso in texto(bloque_resumen(pg))
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(100); s_ = aviso in texto(pg.locator('#fcuerpo'))
        pg.click('[data-a="fichaTab"][data-v="armado"]'); pg.wait_for_timeout(100); a_ = texto(pg.locator('#fcuerpo')).count(aviso)
        ok('datos sin la guía: lo dicen Resumen, Skills y Armado (C.T.P. e ISO-8), sin errores', r and s_ and a_ == 2 and not errores, (r, s_, a_, errores[:2]))
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
