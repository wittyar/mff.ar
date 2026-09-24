#!/usr/bin/env python3
"""Baja todo lo necesario desde thanosvibs.money y la wiki de Future Fight.

Uso:
  python scripts/fetch_all.py                 # todo
  python scripts/fetch_all.py --datos         # personajes, skills, uniformes, instintos, iconos
  python scripts/fetch_all.py --tierlists     # solo las tier lists (todas las públicas)
  python scripts/fetch_all.py --imagenes      # solo los retratos que falten
  python scripts/fetch_all.py --no-portraits  # todo menos los retratos (lo que usa el CI)

Las partes se pueden pedir sueltas para que cada boton de Ajustes actualice solo lo suyo.
Deja: work/characters.json, work/updates.json, work/tierlists/*.json,
      work/skills_api/*.json, work/uniforms.json, work/ctps.json, work/artifacts.json,
      work/wikitext/*.json, images/icons/*.png (insumo del build), images/*.png (los
      retratos) e images/items/*.png (íconos de C.T.P.s y artefactos)."""
import glob, json, re, os, sys, time, unicodedata, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = {'User-Agent': 'Mozilla/5.0 (mff-comparador; uso personal)'}
TV = 'https://thanosvibs.money'
WIKI = 'https://future-fight.fandom.com'
_flags = {a for a in sys.argv[1:] if a.startswith('--')}
_sueltos = _flags & {'--datos', '--tierlists', '--imagenes'}
# Sin flags de parte, se hace todo. Con alguno, solo esas partes.
HACER_DATOS     = not _sueltos or '--datos' in _flags
HACER_TIERLISTS = not _sueltos or '--tierlists' in _flags
HACER_IMAGENES  = (not _sueltos or '--imagenes' in _flags) and '--no-portraits' not in _flags
os.makedirs('work/wikitext', exist_ok=True)
os.makedirs('images/icons', exist_ok=True)

def get(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()

def get_json(url):
    return json.loads(get(url))

def wiki_api(params):
    return get_json(WIKI + '/api.php?' + urllib.parse.urlencode(params))

# Los personajes son insumo de casi todo lo demas, asi que se bajan siempre.
# 1) personajes
chars = get_json(TV + '/api/characters')
json.dump(chars, open('work/characters.json', 'w'))
print('characters:', len(chars), 'filas')


if HACER_TIERLISTS:
    # 2) tier lists: todas las listas publicadas en thanosvibs, en work/tierlists/.
    # Son listas de autor: cada una trae sus propias filas rotuladas, que se respetan
    # tal cual (ver _core.py). Las cinco principales (la general, soportes y las tres de
    # modo) conservan el slug que ya tenían, porque la capa del usuario guarda sus
    # cambios por slug, y se reconocen por id de proyecto y no por título: hay dos listas
    # que se llaman parecido ("THANO$VIB$ Supports Tier List" y "Supports"). Las demás
    # van con 'tv-' + id de proyecto.
    # id de proyecto -> (slug, nombre ES en la app, nombre EN en la app)
    PRINCIPALES = {
        'proj-1787128586625-aucll': ('tv-general',  'General',               'General'),
        'proj-1787505061964-ema1t': ('tv-alianza',  'Batalla de Alianza',    'Alliance Battle'),
        'proj-1787507393380-56kpn': ('tv-arena',    'Arena de Equipos',      'Team Battle Arena'),
        'proj-1787515240347-mnkz6': ('tv-wbl',      'World Boss Legend (+)', 'World Boss Legend (+)'),
        'proj-1787128676713-qt4q4': ('tv-soportes', 'Soportes',              'Supports'),
    }
    projects = get_json(TV + '/api/tierlists/projects')
    faltan = [slug for pid, (slug, _, _) in PRINCIPALES.items() if pid not in {p['id'] for p in projects}]
    if faltan:
        print('AVISO: listas principales que thanosvibs ya no publica:', faltan)
    # Se reescribe la carpeta entera: una lista que el autor despublicó no puede seguir
    # entrando al build desde un archivo viejo.
    os.makedirs('work/tierlists', exist_ok=True)
    for viejo in glob.glob('work/tierlists/*.json'):
        os.remove(viejo)
    orden_principal = list(PRINCIPALES)
    for p in projects:
        vers = get_json(TV + f"/api/tierlists/projects/{urllib.parse.quote(p['id'])}/versions")
        v0 = vers[0]
        if p['id'] in PRINCIPALES:
            slug, es, en = PRINCIPALES[p['id']]
            orden, grupo = orden_principal.index(p['id']), 'principal'
        else:
            slug, es, en = 'tv-' + p['id'], p['title'], p['title']
            orden, grupo = 100, 'comunidad'
        json.dump({'slug': slug, 'title': p['title'], 'name_es': es, 'name_en': en, 'order': orden,
                   'group': grupo, 'project': p, 'version': v0},
                  open(f'work/tierlists/{slug}.json', 'w'))
        print('tier list:', p['title'], '| juego', v0['gameVersion'], '| autor', v0.get('author'),
              '| filas', len(v0.get('tiers', [])))
    print('tier lists:', len(projects), 'publicadas')


if HACER_DATOS:
    # 3) skills: la API de thanosvibs es la fuente. Una llamada por retrato, porque cada
    # uniforme tiene su propio set (incluidas Uniform Passive y Striker Skill).
    os.makedirs('work/skills_api', exist_ok=True)
    ports_sk = sorted({r['portrait'] for r in chars} | {r['base_portrait'] for r in chars})
    fallos_sk = []
    # Se bajan siempre, aunque ya haya copia: un rebalanceo cambia skills de retratos que
    # ya existían, y saltear los archivos presentes dejaba esos cambios afuera para siempre.
    def get_skills(p):
        fn = f'work/skills_api/{p}.json'
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

    # 3c) actualizaciones del juego: de acá sale la versión del snapshot (version_juego.py)
    json.dump(get_json(TV + '/api/updates'), open('work/updates.json', 'w'))
    print('actualizaciones:', len(json.load(open('work/updates.json'))), 'versiones mayores')

    # 3d) C.T.P.s y artefactos (los transforma scripts/fuentes.py)
    json.dump(get_json(TV + '/api/ctps'), open('work/ctps.json', 'w'))
    json.dump(get_json(TV + '/api/artifacts'), open('work/artifacts.json', 'w'))
    print('ctps:', len(json.load(open('work/ctps.json'))), '| artefactos:', len(json.load(open('work/artifacts.json'))))


if HACER_DATOS:
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
if HACER_IMAGENES:
    ports = sorted({r['portrait'] for r in chars} | {r['base_portrait'] for r in chars})
    def getp(p):
        fn = f'images/{p}.png'
        if os.path.exists(fn): return
        try: open(fn, 'wb').write(get(f'{TV}/images/portraits/{p}.png'))
        except Exception as e: print('AVISO retrato fallo:', p, e)
    with ThreadPoolExecutor(6) as ex: list(ex.map(getp, ports))
    print('retratos:', len([f for f in os.listdir('images') if f.endswith('.png')]))

    # Íconos de C.T.P.s y de artefactos: arte de terceros como los retratos. Salen de los
    # insumos que baja --datos, así que se omiten si todavía no se bajaron.
    os.makedirs('images/items', exist_ok=True)
    items = []
    if os.path.exists('work/ctps.json'):
        items += ['ctp_' + re.sub(r'[^a-z0-9]', '', c['name'].lower()) for c in json.load(open('work/ctps.json'))]
    if os.path.exists('work/artifacts.json'):
        items += ['artifact_' + a['portrait'] for a in json.load(open('work/artifacts.json'))]
    def geti_item(n):
        fn = f'images/items/{n}.png'
        if os.path.exists(fn): return
        try:
            data = get(f'{TV}/images/items/{n}.png')
            if data[:4] == b'\x89PNG': open(fn, 'wb').write(data)
            else: print('AVISO ícono de ítem no es PNG:', n)
        except Exception as e: print('AVISO ícono de ítem fallo:', n, e)
    with ThreadPoolExecutor(6) as ex: list(ex.map(geti_item, items))
    print('íconos de ítems:', len(os.listdir('images/items')))


if HACER_DATOS:
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
