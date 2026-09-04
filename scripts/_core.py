import glob, json, os, re, unicodedata
d = json.load(open('work/characters.json'))
wiki = json.load(open('work/wiki_parsed.json'))
ver = json.load(open('work/gen_versions.json'))[0]
# Cada lista de thanosvibs define sus propias filas rotuladas ("Meta", "T4 / s",
# "strikers"...). No son rangos S-D: aplastarlas a S-D renombraba un striker top
# como "D". Se importan con sus filas tal cual y el orden de la fuente.
TL_FILES = sorted(glob.glob('work/tierlists/*.json'))
TYPE = {'Combat':'Combate','Blast':'Detonación','Speed':'Velocidad','Universal':'Universal'}
ALLIES = {'Alien':'Alienígena','Creature':'Criatura','Human':'Humano','Inhuman':'Inhumano','Mutant':'Mutante','Other':'Otro'}
GENDER = {'Male':'Masculino','Female':'Femenino','Neutral':'Neutro'}
SIDE = {'Super Hero':'Superhéroe','Super Villain':'Supervillano','Neutral':'Neutral'}
ORIGIN = {'MCU':'MCU','Comic':'Cómic','Animation':'Animación','TV':'TV','Sony':'Sony','Collab':'Colaboración','Original':'Original MFF'}
INSTINCT = {'Justice':'Justicia','Order':'Orden','Destruction':'Destrucción','Cruelty':'Crueldad'}
ABIL = {
 'Agent':'Agente','Agility':'Agilidad','Annihilators':'Aniquiladores','Black Order':'Orden Negra',
 'Chaos Magic':'Magia del Caos','Chill':'Congelación','Cold Blooded':'Sangre Fría','Command':'Mando',
 'Cosmic Cube':'Cubo Cósmico','Dark Avengers':'Vengadores Oscuros','Defenders':'Defensores','Durability':'Durabilidad',
 'Energy Projection':'Proyección de Energía','Eternals':'Eternos','Fantastic Four':'Los 4 Fantásticos',
 'Fast Movement':'Movimiento Rápido','Flame':'Llama','Gamma Radiation':'Radiación Gamma',
 'Guardians of the Galaxy':'Guardianes de la Galaxia','Healing':'Curación','Heightened Senses':'Sentidos Agudizados',
 'Hellfire':'Fuego Infernal','Infinity Warps':'Infinity Warps','Leadership':'Liderazgo','Machine':'Máquina',
 'Magic':'Magia','Mind':'Mente','Mind Resist':'Resistencia Mental','Olympus':'Olimpo','Phoenix Force':'Fuerza Fénix',
 'Poison':'Veneno','Power Cosmic':'Poder Cósmico','Pure Evil':'Maldad Pura','Shock':'Electrochoque',
 'Sinister Six':'Los Seis Siniestros','Spider-Sense':'Sentido Arácnido','Strong':'Fuerza','Symbiote':'Simbionte',
 'Thunderbolts':'Thunderbolts','Time Freezing Immunity':'Inmunidad a Detención del Tiempo',
 'Warriors of the Sky':'Guerreros del Cielo','Weapons Master':'Maestro de Armas','Young Avengers':'Jóvenes Vengadores','Zombie':'Zombi'}
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
SLOT_SORT = {'Liderazgo':0,'Pasiva':1,'Activa 1':2,'Activa 2':3,'Activa 3':4,'Activa 4':5,'Activa 5':6,'Definitiva':9}
def sort_sk(sks): return sorted(sks, key=lambda s: SLOT_SORT.get(s['slot'], 7))
CONTROL_TAGS = {'Aturdir','Inmovilizar','Silencio','Miedo','Ralentizar'}
def derive_roles(skills):
    tags = set(t for s in skills for t in s['tags'])
    roles = []
    if len(tags & CONTROL_TAGS) >= 2: roles.append('Control')
    if 'Curación' in tags or 'Limpia Debuffs' in tags: roles.append('Soporte')
    if 'Provocar' in tags: roles.append('Tanque')
    roles.append('Daño')
    return roles
nuevas = sorted({a for r in d for a in r['ability']} - set(ABIL))
if nuevas:
    raise SystemExit(f'habilidades sin traducir en ABIL: {nuevas} — agregalas a scripts/_core.py')
byid = {}
for x in d: byid.setdefault(x['id'], []).append(x)
characters, images, uindex, seen = [], {}, {}, set()
for numid, rows in sorted(byid.items(), key=lambda kv: int(kv[0])):
    base = next(r for r in rows if r['uniformed']=='False')
    cid = slug(base['character'])
    if cid in seen: cid = f"{cid}-{numid}"
    seen.add(cid)
    w = wiki.get(base['character'], {'instinct':'','base':[],'per_uni':{}})
    ins = INSTINCT.get(w['instinct'], 'Desconocido')
    base_skills = list(w['base'])
    per_uni = list(w['per_uni'].items())
    used = set()
    uniforms = []
    for i, r in enumerate([r for r in rows if r['uniformed']=='True']):
        uid = f"{cid}-{r.get('uniform_id') or 'u'+str(i)}"
        uname = r['uniform']
        if r['character'] != base['character']: uname = f"{uname} ({r['character']})"
        usk, nu = [], norm(r['uniform'])
        for j,(wk, v) in enumerate(per_uni):
            k = norm(wk)
            if j not in used and k and (k in nu or nu in k):
                usk = sort_sk(v); used.add(j); break
        u = {'id': uid, 'name': uname, 'tier': tier_of(r), 'year': '',
             'cost': r.get('uniform_cost',''), 'striker': r['striker_skill'],
             'wba': ABIL[r['world_boss_ability']], 'trans': r['skill6'] == 'Transcended',
             'new': r['new'] == 'True', 'skills': usk}
        # El uniforme puede cambiar tipo, bando o habilidades respecto de la base.
        if TYPE[r['type']] != TYPE[base['type']]: u['c'] = TYPE[r['type']]
        if SIDE[r['side']] != SIDE[base['side']]: u['f'] = SIDE[r['side']]
        if r['ability'] != base['ability']: u['ab'] = [ABIL[a] for a in r['ability']]
        uniforms.append(u)
        images['portrait-'+uid] = 'images/' + r['portrait'] + '.png'
        uindex[(numid, r.get('uniform_id'))] = (cid, uid)
    leftovers = [j for j in range(len(per_uni)) if j not in used]
    # En las paginas donde las activas viven por uniforme, la base no trae ninguna y el
    # primer grupo sin cruzar es el traje base: ese se mergea. Si la base ya trae activas,
    # el grupo es de un uniforme que no supimos cruzar y mergearlo inventaria atribucion.
    if leftovers and not any(sk['slot'].startswith('Activa') for sk in base_skills):
        base_skills += per_uni[leftovers[0]][1]
        leftovers = leftovers[1:]
    for j in leftovers:
        print(f"AVISO: {base['character']}: skills de '{per_uni[j][0]}' sin uniforme que cruce"
              f" ({len(per_uni[j][1])} skills, quedan fuera del snapshot)")
    base_skills = sort_sk(base_skills)
    all_sk = base_skills + [s for u in uniforms for s in u['skills']]
    characters.append({
        'id': cid, 'name': base['character'], 'c': TYPE[base['type']], 'f': SIDE[base['side']],
        'r': derive_roles(all_sk) if all_sk else [], 'ins': ins, 'race': ALLIES[base['allies']],
        'gender': GENDER[base['gender']], 't': tier_of(base), 'modes': [],
        'abilities': [ABIL[a] for a in base['ability']], 'origin': ORIGIN[base['original']],
        'tuc': base.get('tuc', []), 'stats': base.get('stats', {}),
        'striker': base['striker_skill'], 'wba': ABIL[base['world_boss_ability']],
        'trans': base['skill6'] == 'Transcended', 'new': base['new'] == 'True',
        'baseSkills': base_skills, 'uniforms': uniforms})
    images['portrait-'+cid] = 'images/' + base['base_portrait'] + '.png'
    uindex[(numid, None)] = (cid, None)
tierlists, assign = [], {}
for fn in TL_FILES:
    tl = json.load(open(fn))
    v, slug = tl['version'], tl['slug']
    # Las filas "Landing" son el area de descarte del editor de thanosvibs, no un nivel.
    rows = [{'id': t['id'], 'label': t['label'].strip()} for t in v.get('tiers', [])
            if not t['id'].startswith('tier-landing')]
    valid = {r['id'] for r in rows}
    a = {}
    for cellkey, items in v['cellContents'].items():
        row = cellkey.split(':', 1)[1]
        if row not in valid: continue
        for it in items:
            pair = uindex.get((it['id'], it.get('uniform_id') if it['uniformed']=='True' else None))
            if not pair: continue
            cid, uid = pair
            key = f"{cid}::{uid}" if uid else f"{cid}::base"
            # La fuente a veces coloca la misma entrada en dos filas: se avisa y gana
            # la primera, en vez de pisarla en silencio.
            if key in a and a[key] != row:
                print(f"AVISO {slug}: {it.get('character')} / {it.get('uniform')} aparece"
                      f" en '{a[key]}' y en '{row}'; queda en la primera")
                continue
            a[key] = row
    tierlists.append({'id': slug, 'order': tl.get('order', 99), 'name': tl['name_es'], 'source': tl['title'],
                      'author': v.get('author', ''), 'gameVersion': v.get('gameVersion', ''),
                      'rows': rows})
    assign[slug] = a
    print(f"tier list {slug}: {len(rows)} filas, {len(a)} asignaciones"
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
tierlists.sort(key=lambda t: t['order'])   # el orden de fetch_all manda: la general primero
json.dump({'characters':characters,'images':images,'assign':assign,'tierlists':tierlists},
          open('work/build2.json','w'), ensure_ascii=False)
print('chars:', len(characters), '| imágenes:', len(images),
      '| listas:', len(tierlists), '| asignaciones:', sum(len(a) for a in assign.values()))
