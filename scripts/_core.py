import collections, glob, json, os, re, unicodedata
d = json.load(open('work/characters.json'))
inst = json.load(open('work/instintos.json'))
SK = json.load(open('work/skills_parsed.json'))       # skills por retrato + tablas de texto
UNI = json.load(open('work/uniforms.json'))           # costos y materiales por uniforme
# Cada lista de thanosvibs define sus propias filas rotuladas ("Meta", "T4 / s",
# "strikers"...). No son rangos S-D: aplastarlas a S-D renombraba un striker top
# como "D". Se importan con sus filas tal cual y el orden de la fuente.
TL_FILES = sorted(glob.glob('work/tierlists/*.json'))
from dominio import TYPE, ALLIES, GENDER, SIDE, ORIGIN, INSTINCT, ABIL
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode()
    return re.sub(r'[^a-z0-9]+','-', s.lower()).strip('-')
def norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode().lower()
    s = re.sub(r"marvel studios'?|marvel'?s|avengers:|\bthe\b", '', s)
    return re.sub(r'[^a-z0-9]+','', s)
def tier_of(row):
    if row['tier-4'] == 'True': return 'T4'
    if row['skill6'] != 'False': return 'T3'
    return 'T2'
# Los roles no existen en el juego: se derivan. Antes salían de etiquetas que un regex
# adivinaba sobre el texto de la wiki; ahora salen de las etiquetas tipadas de la API,
# que son un vocabulario cerrado de 228 valores.
ETIQ_AB = [x['en'] for x in SK['tablas']['ab']]
def _ids(*patrones):
    rx = re.compile('|'.join(patrones), re.I)
    return {i for i, e in enumerate(ETIQ_AB) if rx.search(e)}
AB_CONTROL = _ids(r'\bstun\b', r'silence', r'snare', r'paraly', r'fracture', r'freeze', r'\bweb\b',
                  r'incapacit', r'\bfear\b', r'mind control', r'entice', r'misdirection')
AB_SOPORTE = _ids(r'hp recovery', r'removes all debuff', r'\bshield\b', r'barrier',
                  r'recovery rate', r'ultimate skill gauge recovery')
AB_TANQUE  = _ids(r'provoke', r'super armor', r'basic defenses increase', r'decreases all basic damage')
def derive_roles(sets):
    ab = {f['a'] for lista in sets for sk in lista for st in sk['st'] for f in st['fx']}
    roles = []
    if len(ab & AB_CONTROL) >= 2: roles.append('Control')
    if ab & AB_SOPORTE: roles.append('Soporte')
    if ab & AB_TANQUE: roles.append('Tanque')
    roles.append('Daño')
    return roles
nuevas = sorted({a for r in d for a in r['ability']} - set(ABIL))
if nuevas:
    raise SystemExit(f'habilidades sin traducir en ABIL: {nuevas} — agregalas a scripts/_core.py')
byid = {}
for x in d: byid.setdefault(x['id'], []).append(x)
characters, images, uindex, seen = [], {}, {}, set()
sin_skills = []
for numid, rows in sorted(byid.items(), key=lambda kv: int(kv[0])):
    base = next(r for r in rows if r['uniformed']=='False')
    cid = slug(base['character'])
    if cid in seen: cid = f"{cid}-{numid}"
    seen.add(cid)
    ins = INSTINCT.get(inst.get(base['character'], {}).get('instinct', ''), 'Desconocido')

    def skills_de(portrait, quien):
        # Cada retrato tiene su propio set en la API. Si falta, se avisa: no hay
        # fuente alternativa desde que la wiki dejo de aportar skills.
        if portrait not in SK['skills']:
            sin_skills.append(quien)
            return []
        return SK['skills'][portrait]

    base_sk = skills_de(base['base_portrait'], base['character'])
    uniforms = []
    for i, r in enumerate([r for r in rows if r['uniformed']=='True']):
        uid = f"{cid}-{r.get('uniform_id') or 'u'+str(i)}"
        uname = r['uniform']
        if r['character'] != base['character']: uname = f"{uname} ({r['character']})"
        u = {'id': uid, 'name': uname, 'tier': tier_of(r), 'p': r['portrait'],
             'cost': r.get('uniform_cost',''), 'striker': r['striker_skill'],
             'wba': ABIL[r['world_boss_ability']], 'trans': r['skill6'] == 'Transcended',
             'new': r['new'] == 'True'}
        # El uniforme puede cambiar tipo, bando o habilidades respecto de la base.
        if TYPE[r['type']] != TYPE[base['type']]: u['c'] = TYPE[r['type']]
        if SIDE[r['side']] != SIDE[base['side']]: u['f'] = SIDE[r['side']]
        if r['ability'] != base['ability']: u['ab'] = [ABIL[a] for a in r['ability']]
        # Costos, materiales y XP de mejora, de /api/uniforms.
        up = UNI.get(r['portrait'])
        if up:
            u['up'] = {k: up[k] for k in ('uniform_xp','uniform_kits','gold','totals','update','flags')
                       if up.get(k)}
            for mk in ('material1','material2'):
                if up.get(mk): u['up'][mk] = up[mk]
        skills_de(r['portrait'], f"{base['character']} / {r['uniform']}")
        uniforms.append(u)
        images['portrait-'+uid] = 'images/' + r['portrait'] + '.png'
        uindex[(numid, r.get('uniform_id'))] = (cid, uid)

    sets = [base_sk] + [SK['skills'].get(u['p'], []) for u in uniforms]
    characters.append({
        'id': cid, 'name': base['character'], 'c': TYPE[base['type']], 'f': SIDE[base['side']],
        'r': derive_roles(sets), 'ins': ins, 'race': ALLIES[base['allies']],
        'gender': GENDER[base['gender']], 't': tier_of(base), 'modes': [],
        'abilities': [ABIL[a] for a in base['ability']], 'origin': ORIGIN[base['original']],
        'tuc': base.get('tuc', []), 'stats': base.get('stats', {}),
        'striker': base['striker_skill'], 'wba': ABIL[base['world_boss_ability']],
        'trans': base['skill6'] == 'Transcended', 'new': base['new'] == 'True',
        'p': base['base_portrait'], 'uniforms': uniforms})
    images['portrait-'+cid] = 'images/' + base['base_portrait'] + '.png'
    uindex[(numid, None)] = (cid, None)
if sin_skills:
    print(f'AVISO: {len(sin_skills)} retratos sin skills en la API:', sin_skills[:5])
tierlists, assign = [], {}
for fn in TL_FILES:
    tl = json.load(open(fn))
    v, slug, proj = tl['version'], tl['slug'], tl['project']
    # Las filas "Landing" son el area de descarte del editor de thanosvibs, no un nivel.
    rows = [{'id': t['id'], 'label': t['label'].strip()} for t in v.get('tiers', [])
            if not t['id'].startswith('tier-landing')]
    valid = {r['id'] for r in rows}
    orden_filas = {r['id']: i for i, r in enumerate(rows)}
    # Una entrada puede estar en varias filas a la vez: muchas listas son por categoría
    # ("PVE High Meta" y "PVE Support") y ponen al mismo personaje en las dos a
    # propósito. Cada entrada guarda sus filas en el orden de la lista.
    a, sin_cruzar = {}, []
    for cellkey, items in v['cellContents'].items():
        row = cellkey.split(':', 1)[1]
        if row not in valid: continue
        for it in items:
            pair = uindex.get((it['id'], it.get('uniform_id') if it['uniformed']=='True' else None))
            if not pair:
                sin_cruzar.append(f"{it.get('character')} / {it.get('uniform')}")
                continue
            cid, uid = pair
            key = f"{cid}::{uid}" if uid else f"{cid}::base"
            filas = a.setdefault(key, [])
            if row not in filas:   # la misma fila en dos columnas de la fuente es una sola ubicación
                filas.append(row)
    for filas in a.values():
        filas.sort(key=orden_filas.get)
    if sin_cruzar:
        # Una entrada que no cruza con el roster (un personaje o uniforme que thanosvibs ya
        # no publica en /api/characters) no se puede ubicar: se avisa en vez de perderla.
        print(f"AVISO {slug}: {len(sin_cruzar)} entradas sin personaje en el roster: {sin_cruzar[:5]}")
    tierlists.append({'id': slug, 'order': tl['order'], 'group': tl['group'],
                      'name': tl['name_es'], 'nameEn': tl['name_en'], 'source': tl['title'],
                      'author': v.get('author', ''), 'gameVersion': v.get('gameVersion', ''),
                      'published': (v.get('publishDate') or '')[:10],
                      # Textos del autor, en su idioma: igual que los rótulos de las filas,
                      # no se traducen.
                      'description': re.sub(r'\n{3,}', '\n\n', (v.get('description') or '').strip()),
                      'notes': re.sub(r'\n{3,}', '\n\n', (v.get('updateNotes') or '').strip()),
                      'tags': v.get('tags') or [],
                      'rating': proj.get('averageRating'), 'ratings': proj.get('totalRatings'),
                      'rows': rows})
    assign[slug] = a
    print(f"tier list {slug}: {len(rows)} filas, {len(a)} entradas en {sum(len(f) for f in a.values())} ubicaciones"
          f" ({len([i for c in v['cellContents'].values() for i in c])} celdas en la fuente)")
# íconos: el mapa valor-ES -> archivo es fijo; los archivos los baja fetch_all y son
# insumo del build. Si falta alguno el build corta: un data.js sin íconos sería una
# regresión silenciosa (la app simplemente dejaría de mostrarlos).
import os as _os
ICON_ES = {**{v: re.sub(r'[^a-z0-9]','',k.lower()) for k,v in ABIL.items()},
 'Combate':'combat','Detonación':'blast','Velocidad':'speed','Universal':'universal',
 'Humano':'human','Mutante':'mutant','Inhumano':'inhuman','Alienígena':'alien','Criatura':'creature','Otro':'other',
 'Masculino':'male','Femenino':'female','Neutro':'neutral','Superhéroe':'hero','Supervillano':'villain'}
faltan = sorted({s for s in ICON_ES.values() if not _os.path.exists(f'images/icons/{s}.png')})
if faltan:
    raise SystemExit(f'faltan {len(faltan)} iconos en images/icons/ {faltan} — corre scripts/fetch_all.py')
for val, s in ICON_ES.items():
    images['icon-'+val] = f'images/icons/{s}.png'
# Vocabulario de dominio para el botón de idioma de la app: el snapshot guarda los
# valores en español, así que se emite el inverso de los mismos mapas que se usaron
# para traducirlos. Un solo lugar de verdad: si acá se agrega un valor, la app lo tiene.
VOCAB_EN = {}
for _mapa in (TYPE, ALLIES, GENDER, SIDE, ORIGIN, INSTINCT, ABIL):
    for _en, _es in _mapa.items():
        VOCAB_EN[_es] = _en
VOCAB_EN.update({
 'Desconocido':'Unknown', 'Neutral':'Neutral',
 # los tiers se escriben igual en los dos idiomas, pero se listan para que el mapa
 # sea completo y la app no tenga que adivinar qué hacer con un valor ausente
 'T2':'T2', 'T3':'T3', 'T4':'T4',
 # roles derivados por derive_roles
 'Daño':'Damage', 'Soporte':'Support', 'Control':'Control', 'Tanque':'Tank',
 # slots que arma parse_skills
 'Liderazgo':'Leadership', 'Pasiva':'Passive', 'Definitiva':'Ultimate',
 **{f'Activa {i}': f'Active {i}' for i in range(1, 12)},
 # tipos de daño
 'Físico':'Physical', 'Energía':'Energy', 'PG':'Mind', 'Ninguno':'None',
 # etiquetas de effects_to_tags
 'Aturdir':'Stun', 'Inmovilizar':'Bind', 'Miedo':'Fear', 'Silencio':'Silence',
 'Provocar':'Provoke', 'Ralentizar':'Slow', 'Sangrado':'Bleed', 'DoT':'DoT',
 'Curación':'Healing', 'Escudo':'Shield', 'Invencibilidad':'Invincibility',
 'Perfora Inmunidad':'Pierce Immunity', 'Ignora Evasión':'Ignore Dodge',
 'Perfora DEF':'Ignore Defense', 'Limpia Debuffs':'Cleanse', 'Buff Crítico':'Critical Buff',
 'Buff ATQ':'Attack Buff', 'Buff DEF':'Defense Buff', 'Buff VEL':'Speed Buff',
 'Buff Evasión':'Dodge Buff', 'Empuje':'Pushback', 'Derribo':'Knockdown',
 # claves de stats del API
 'recovery_rate':'Recovery Rate', 'fire_resist':'Fire Resist', 'cold_resist':'Cold Resist',
 'lightning_resist':'Lightning Resist', 'poison_resist':'Poison Resist', 'mind_resist':'Mind Resist',
})

# Dos listas de la comunidad con el mismo título ("Personal Tier List") se distinguen por
# su autor, que es lo único que las diferencia en el selector.
_titulos = collections.Counter(t['source'] for t in tierlists if t['group'] == 'comunidad')
for t in tierlists:
    if t['group'] == 'comunidad' and _titulos[t['source']] > 1:
        t['name'] = t['nameEn'] = f"{t['source']} ({t['author']})"
# Primero las cinco principales en su orden fijo; después las de la comunidad, de la
# publicada más recientemente a la más vieja.
tierlists.sort(key=lambda t: t['published'], reverse=True)
tierlists.sort(key=lambda t: t['order'])
json.dump({'characters':characters,'images':images,'assign':assign,'tierlists':tierlists,
           'vocab':VOCAB_EN,'skills':SK['skills'],'tablas':SK['tablas'],'buffs':SK['buffs']},
          open('work/build2.json','w'), ensure_ascii=False)
print('chars:', len(characters), '| imágenes:', len(images),
      '| listas:', len(tierlists), '| ubicaciones:', sum(len(f) for a in assign.values() for f in a.values()),
      '| sets de skills:', len(SK['skills']))
