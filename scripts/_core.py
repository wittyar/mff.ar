import json, re, unicodedata
d = json.load(open('work/characters.json'))
wiki = json.load(open('work/wiki_parsed.json'))
ver = json.load(open('work/gen_versions.json'))[0]
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
             'cost': r.get('uniform_cost',''), 'skills': usk}
        if TYPE[r['type']] != TYPE[base['type']]: u['c'] = TYPE[r['type']]
        uniforms.append(u)
        images['portrait-'+uid] = 'images/' + r['portrait'] + '.png'
        uindex[(numid, r.get('uniform_id'))] = (cid, uid)
    leftovers = [j for j in range(len(per_uni)) if j not in used]
    if leftovers: base_skills += per_uni[leftovers[0]][1]
    base_skills = sort_sk(base_skills)
    all_sk = base_skills + [s for u in uniforms for s in u['skills']]
    characters.append({
        'id': cid, 'name': base['character'], 'c': TYPE[base['type']], 'f': SIDE[base['side']],
        'r': derive_roles(all_sk) if all_sk else [], 'ins': ins, 'race': ALLIES[base['allies']],
        'gender': GENDER[base['gender']], 't': tier_of(base), 'modes': [],
        'abilities': [ABIL[a] for a in base['ability']], 'origin': ORIGIN[base['original']],
        'tuc': base.get('tuc', []), 'stats': base.get('stats', {}),
        'baseSkills': base_skills, 'uniforms': uniforms})
    images['portrait-'+cid] = 'images/' + base['base_portrait'] + '.png'
    uindex[(numid, None)] = (cid, None)
RANK = {'tier-s':'S','tier-a':'A','tier-b':'B','tier-c':'C','tier-d':'D',
        'tier-1786666916600':'D','tier-1786667217191':'D','tier-1786666818513':'D'}
assign = {}
for cellkey, items in ver['cellContents'].items():
    rank = RANK.get(cellkey.split(':',1)[1])
    if not rank: continue
    for it in items:
        pair = uindex.get((it['id'], it.get('uniform_id') if it['uniformed']=='True' else None))
        if not pair: continue
        cid, uid = pair
        assign[(f"{cid}::{uid}" if uid else f"{cid}::base")] = rank
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
json.dump({'characters':characters,'images':images,'assign':assign}, open('work/build2.json','w'), ensure_ascii=False)
print('chars:', len(characters), '| imágenes:', len(images), '| tiers:', len(assign))
