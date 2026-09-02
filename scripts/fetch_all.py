#!/usr/bin/env python3
"""Baja todo lo necesario desde thanosvibs.money y la wiki de Future Fight.
Uso: python scripts/fetch_all.py [--no-images]
Deja: work/characters.json, work/gen_versions.json, work/wikitext/*.json,
      images/*.png e images/icons/*.png (salvo --no-images)."""
import json, re, os, sys, time, unicodedata, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {'User-Agent': 'Mozilla/5.0 (mff-comparador; uso personal)'}
TV = 'https://thanosvibs.money'
WIKI = 'https://future-fight.fandom.com'
NO_IMAGES = '--no-images' in sys.argv
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

# 2) tier list general (por titulo, no por id hardcodeado)
projects = get_json(TV + '/api/tierlists/projects')
gen = next(p for p in projects if 'General Tier List' in p['title'])
vers = get_json(TV + f"/api/tierlists/projects/{urllib.parse.quote(gen['id'])}/versions")
json.dump(vers, open('work/gen_versions.json', 'w'))
print('tier list:', gen['title'], '| version de juego:', vers[0]['gameVersion'])

# 3) resolucion de titulos de wiki (lotes + busqueda de rescate + overrides)
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

# 4) wikitexts
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

# 5) imagenes
if not NO_IMAGES:
    ports = sorted({r['portrait'] for r in chars} | {r['base_portrait'] for r in chars})
    def getp(p):
        fn = f'images/{p}.png'
        if os.path.exists(fn): return
        try: open(fn, 'wb').write(get(f'{TV}/images/portraits/{p}.png'))
        except Exception as e: print('AVISO retrato fallo:', p, e)
    with ThreadPoolExecutor(6) as ex: list(ex.map(getp, ports))
    print('retratos:', len([f for f in os.listdir('images') if f.endswith('.png')]))
    # iconos: tipos + razas + generos + bandos + habilidades (slug del nombre en ingles)
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
        except Exception: pass
    with ThreadPoolExecutor(6) as ex: list(ex.map(geti, slugs))
    print('iconos:', len(os.listdir('images/icons')))
