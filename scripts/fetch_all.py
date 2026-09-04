#!/usr/bin/env python3
"""Baja todo lo necesario desde thanosvibs.money y la wiki de Future Fight.
Uso: python scripts/fetch_all.py [--no-portraits]
Deja: work/characters.json, work/gen_versions.json, work/wikitext/*.json,
      images/icons/*.png (siempre: son insumo del build) e images/*.png
      (los retratos, salvo --no-portraits)."""
import json, re, os, sys, time, unicodedata, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {'User-Agent': 'Mozilla/5.0 (mff-comparador; uso personal)'}
TV = 'https://thanosvibs.money'
WIKI = 'https://future-fight.fandom.com'
NO_PORTRAITS = '--no-portraits' in sys.argv
os.makedirs('work/wikitext', exist_ok=True)
os.makedirs('images/icons', exist_ok=True)

def get(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

def get_json(url):
    return json.loads(get(url))

def wiki_api(params):
    return get_json(WIKI + '/api.php?' + urllib.parse.urlencode(params))

# 1) personajes
chars = get_json(TV + '/api/characters')
json.dump(chars, open('work/characters.json', 'w'))
print('characters:', len(chars), 'filas')

# 2) tier lists (por titulo, no por id hardcodeado). La general va aparte por
# compatibilidad con work/gen_versions.json; las demas quedan en work/tierlists/.
# Son listas de autor: cada una trae sus propias filas rotuladas, que se respetan
# tal cual (ver _core.py). Si alguna cambia de titulo, el fetch avisa y sigue.
# (slug, título en thanosvibs, nombre ES en la app, nombre EN en la app)
TIERLISTS = [
    ('tv-general',  'THANO$VIB$ General Tier List',   'General',               'General'),
    ('tv-alianza',  'Alliance Battle',                'Batalla de Alianza',    'Alliance Battle'),
    ('tv-arena',    'Team Battle Arena',              'Arena de Equipos',      'Team Battle Arena'),
    ('tv-wbl',      'World Boss Legend (+)',          'World Boss Legend (+)', 'World Boss Legend (+)'),
    ('tv-soportes', 'THANO$VIB$ Supports Tier List',  'Soportes',              'Supports'),
]
projects = get_json(TV + '/api/tierlists/projects')
by_title = {p['title']: p['id'] for p in projects}
os.makedirs('work/tierlists', exist_ok=True)
for i, (slug, title, es, en) in enumerate(TIERLISTS):
    pid = by_title.get(title)
    if not pid:
        print('AVISO: tier list sin encontrar (cambio de titulo?):', title)
        continue
    vers = get_json(TV + f'/api/tierlists/projects/{urllib.parse.quote(pid)}/versions')
    v0 = vers[0]
    json.dump({'slug': slug, 'title': title, 'name_es': es, 'name_en': en, 'order': i, 'version': v0},
              open(f'work/tierlists/{slug}.json', 'w'))
    if slug == 'tv-general':
        json.dump(vers, open('work/gen_versions.json', 'w'))
    print('tier list:', title, '| juego', v0['gameVersion'], '| autor', v0.get('author'),
          '| filas', len(v0.get('tiers', [])))

# 3) skills: la API de thanosvibs es la fuente. Una llamada por retrato, porque cada
# uniforme tiene su propio set (incluidas Uniform Passive y Striker Skill).
os.makedirs('work/skills_api', exist_ok=True)
ports_sk = sorted({r['portrait'] for r in chars} | {r['base_portrait'] for r in chars})
fallos_sk = []
def get_skills(p):
    fn = f'work/skills_api/{p}.json'
    if os.path.exists(fn): return
    for intento in range(3):
        try:
            open(fn, 'wb').write(get(f'{TV}/api/characters/{urllib.parse.quote(p)}/skills'))
            return
        except Exception as e:
            if intento == 2: fallos_sk.append(p)
            time.sleep(1.5)
with ThreadPoolExecutor(5) as ex: list(ex.map(get_skills, ports_sk))
print('skills:', len(os.listdir('work/skills_api')), 'retratos', ('| AVISO fallaron: ' + str(fallos_sk)) if fallos_sk else '')

# 3b) costos y materiales de cada uniforme
json.dump(get_json(TV + '/api/uniforms'), open('work/uniforms.json', 'w'))
print('uniformes:', len(json.load(open('work/uniforms.json'))), 'con costos y materiales')

# 4) resolucion de titulos de wiki. La wiki ya NO aporta skills: se usa solo para el
# instinto, que thanosvibs no publica en ninguna de sus APIs.

OVERRIDES = {'Kraven The Hunter': 'Kraven the Hunter', 'Morgan le Fay': 'Morgan Le Fay',
             'Falcon (Joaquin Torres)': 'Falcon (Joaqu\u00edn Torres)'}
names = sorted({r['character'] for r in chars if r['uniformed'] == 'False'})
resolved = dict(OVERRIDES)
pending = [n for n in names if n not in resolved]
for i in range(0, len(pending), 50):
    batch = pending[i:i+50]
    q = wiki_api({'action':'query','titles':'|'.join(batch),'redirects':'1','format':'json'})['query']
    norm = {n['from']: n['to'] for n in q.get('normalized', [])}
    redir = {r['from']: r['to'] for r in q.get('redirects', [])}
    ok = {p['title'] for p in q['pages'].values() if 'missing' not in p}
    for n in batch:
        t = redir.get(norm.get(n, n), norm.get(n, n))
        if t in ok: resolved[n] = t
    time.sleep(0.3)
missing = [n for n in names if n not in resolved]
for n in missing:
    hits = wiki_api({'action':'query','list':'search','srsearch':n,'srlimit':1,'format':'json'})['query']['search']
    if hits: resolved[n] = hits[0]['title']
    time.sleep(0.2)
still = [n for n in names if n not in resolved]
if still: print('AVISO: sin pagina de wiki:', still)
json.dump(resolved, open('work/wiki_titles.json', 'w'))

# 4b) wikitexts (solo por el instinto)
def wslug(s): return re.sub(r'[^A-Za-z0-9]+', '_', s)
for name, title in resolved.items():
    fn = f'work/wikitext/{wslug(name)}.json'
    try:
        d = wiki_api({'action':'parse','page':title,'prop':'wikitext','format':'json'})
        json.dump({'name': name, 'title': title, 'wt': d['parse']['wikitext']['*']}, open(fn, 'w'))
    except Exception as e:
        print('AVISO wikitext fallo:', name, e)
    time.sleep(0.1)
print('wikitexts:', len(os.listdir('work/wikitext')))

# 5) retratos: arte de terceros, gitignoreado y ajeno al build; se omiten en CI
if not NO_PORTRAITS:
    ports = sorted({r['portrait'] for r in chars} | {r['base_portrait'] for r in chars})
    def getp(p):
        fn = f'images/{p}.png'
        if os.path.exists(fn): return
        try: open(fn, 'wb').write(get(f'{TV}/images/portraits/{p}.png'))
        except Exception as e: print('AVISO retrato fallo:', p, e)
    with ThreadPoolExecutor(6) as ex: list(ex.map(getp, ports))
    print('retratos:', len([f for f in os.listdir('images') if f.endswith('.png')]))

# 6) iconos: tipos + razas + generos + bandos + habilidades (slug del nombre en ingles).
# _core.py arma el mapa de iconos leyendo images/icons/, asi que son insumo del build y
# se bajan siempre: sin ellos data.js saldria sin iconos.
fixed = ['combat','blast','speed','universal','human','mutant','inhuman','alien','creature','other',
         'male','female','neutral','hero','villain']
abil = sorted({a for r in chars for a in r['ability']})
slugs = fixed + [re.sub(r'[^a-z0-9]', '', a.lower()) for a in abil]
def geti(s):
    fn = f'images/icons/{s}.png'
    if os.path.exists(fn): return
    try:
        data = get(f'{TV}/images/attributes/{s}.png')
        if data[:4] == b'\x89PNG': open(fn, 'wb').write(data)
    except Exception as e: print('AVISO icono fallo:', s, e)
with ThreadPoolExecutor(6) as ex: list(ex.map(geti, slugs))
print('iconos:', len(os.listdir('images/icons')))
