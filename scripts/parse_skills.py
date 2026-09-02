import json, re, glob

STAT = {
 'All Attack':'ATQ total','Physical Attack':'ATQ físico','Energy Attack':'ATQ de energía',
 'All Defense':'DEF total','Physical Defense':'DEF física','Energy Defense':'DEF de energía',
 'All Speeds':'todas las velocidades','Attack Speed':'vel. de ataque','Movement Speed':'vel. de movimiento',
 'Dodge Rate':'evasión','Guaranteed Dodge Rate':'evasión garantizada','Critical Rate':'prob. de crítico',
 'Critical Damage':'daño crítico','Max HP':'vida máx.','MAX HP':'vida máx.','HP':'vida',
 'Skill Cooldown':'recarga de skills','Recovery Rate':'tasa de recuperación','Defense Penetration':'perforación de DEF',
 'Ignore Defense':'ignorar DEF','All Basic Attacks':'ataques básicos','Crowd Control Time':'duración de control',
 'Debuff Duration':'duración de debuffs','Lightning Damage':'daño eléctrico','Fire Damage':'daño de fuego',
 'Additional Pierce Damage':'daño perforante adicional','Damage Rate':'tasa de daño','damage':'daño',
}
ELEM = {'Fire':'Fuego','Shock':'Electro','Chill':'Hielo','Poison':'Veneno','Lightning':'Rayo'}
def stat_es(s):
    s = s.strip()
    for k in sorted(STAT, key=len, reverse=True):
        if k.lower() == s.lower(): return STAT[k]
    return s
def secs(x): return x.replace('Sec.','s').replace('Sec','s').replace(' ','')
def hits(n): return f"{n} golpe" + ('' if n=='1' else 's')

RULES = [
 (re.compile(r"^(\d+)% (Energy|Physical) Damage(?:, Add \w+ Damage (\d+))?", re.I),
  lambda m: f"{m.group(1)}% daño {'de Energía' if m.group(2).lower()=='energy' else 'Físico'}" + (f" (+{m.group(3)})" if m.group(3) else '')),
 (re.compile(r"^Appl(?:y|ies) to\s*:?\s*(.+)", re.I),
  lambda m: '→ ' + {'self':'sí mismo','enemy':'enemigo','enemies':'enemigos','all allies':'todos los aliados','allies':'aliados','villains in team':'villanos del equipo','heroes in team':'héroes del equipo','all enemies':'todos los enemigos'}.get(m.group(1).strip().lower().rstrip('.'), m.group(1).strip())),
 (re.compile(r"^Activ?i?ation Rate\s*:?\s*(.+)", re.I), lambda m: 'Se activa: ' + m.group(1).strip()),
 (re.compile(r"^How to Apply\s*:?\s*(.+)", re.I), lambda m: 'Aplicación: ' + m.group(1).strip()),
 (re.compile(r"^Stun \(([\d.]+ ?Sec\.?)\)", re.I), lambda m: f"Aturde {secs(m.group(1))}"),
 (re.compile(r"^Bind \(([\d.]+ ?Sec\.?)\)", re.I), lambda m: f"Inmoviliza {secs(m.group(1))}"),
 (re.compile(r"^Fear \(([\d.]+ ?Sec\.?)\)", re.I), lambda m: f"Miedo {secs(m.group(1))}"),
 (re.compile(r"^Silence \(([\d.]+ ?Sec\.?)\)", re.I), lambda m: f"Silencia {secs(m.group(1))}"),
 (re.compile(r"^Provoke \(([\d.]+ ?Sec\.?)\)", re.I), lambda m: f"Provoca {secs(m.group(1))}"),
 (re.compile(r"^Incapacitation ?\(?([^)]*)\)? ?\(([\d.]+ ?Sec\.?)\)", re.I), lambda m: f"Incapacita {secs(m.group(2))}" + (' (quita buffs activos)' if 'buff' in m.group(1).lower() else '')),
 (re.compile(r"^Immune to all damages? \(([\d.]+ ?Sec\.?)\)", re.I), lambda m: f"Inmune a todo daño {secs(m.group(1))}"),
 (re.compile(r"^Invincible \(([\d.]+ ?Sec\.?)\)", re.I), lambda m: f"Invencible {secs(m.group(1))}"),
 (re.compile(r"^(?:MAX HP Recovery|Recovery of MAX HP)\s*\+?(\d+)%(?: \(([\d.]+ ?Sec\.?)\))?", re.I),
  lambda m: f"Recupera {m.group(1)}% de vida máx." + (f" ({secs(m.group(2))})" if m.group(2) else '')),
 (re.compile(r"^(\d+)% recovery of MA?X HP(?: \(([\d.]+ ?Sec\.?)\))?", re.I),
  lambda m: f"Recupera {m.group(1)}% de vida máx." + (f" ({secs(m.group(2))})" if m.group(2) else '')),
 (re.compile(r"^It deals (\d+)% (\w+) damage every ([\d.]+) Sec\.? \(([\d.]+ ?Sec\.?)\)", re.I),
  lambda m: f"DoT: {m.group(1)}% {ELEM.get(m.group(2), m.group(2))} c/{m.group(3)}s ({secs(m.group(4))})"),
 (re.compile(r"^Increases? damage by (\d+)% for (\d+) attack", re.I), lambda m: f"+{m.group(1)}% daño por {m.group(2)} ataque(s)"),
 (re.compile(r"^\+?(\d+)% increase of (.+?)\.?$", re.I), lambda m: f"+{m.group(1)}% {stat_es(m.group(2))}"),
 (re.compile(r"^Increases? (.+?) by \+?([\d.]+)%?\.? ?(?:\(([\d.]+ ?Sec\.?)\))?", re.I),
  lambda m: f"+{m.group(2)}% {stat_es(m.group(1))}" + (f" ({secs(m.group(3))})" if m.group(3) else '')),
 (re.compile(r"^Decreases? (.+?) by \-?([\d.]+)%?\.? ?(?:\(([\d.]+ ?Sec\.?)\))?", re.I),
  lambda m: f"-{m.group(2)}% {stat_es(m.group(1))}" + (f" ({secs(m.group(3))})" if m.group(3) else '')),
 (re.compile(r"^(.+?) \+([\d.]+)%$"), lambda m: f"+{m.group(2)}% {stat_es(m.group(1))}"),
 (re.compile(r"^(\d+)% chance to penetrate with .*?(?:INVINCIBLE|IMMUNE)[^.]*\.? ?(?:\(([\d.]+ ?Sec\.?)\))?", re.I),
  lambda m: f"{m.group(1)}% de perforar escudos/barreras/invencibilidad" + (f" ({secs(m.group(2))})" if m.group(2) else '')),
 (re.compile(r"^Ig?nores? target'?s? Dodge Rate by (\d+)%", re.I),
  lambda m: f"Ignora {m.group(1)}% de la evasión del objetivo"),
 (re.compile(r"^Remo[vb]es? all Debuffs?", re.I), lambda m: "Limpia todos los debuffs"),
 (re.compile(r"^Guaranteed Critical", re.I), lambda m: "Crítico garantizado"),
]
GEO = [ (r'\bRanged\b','A distancia'), (r'\bMelee\b','Cuerpo a cuerpo'), (r'(\d+) Hits?\b', lambda m: hits(m.group(1))),
        (r'\bPushback\b','empuje'), (r'Draw in enemies','atrae enemigos'), (r'Large AOE','área grande'),
        (r'Small AOE','área chica'), (r'\bAOE\b','área'), (r'Teleport to target','teletransporte al objetivo'),
        (r'Teleport away from target','teletransporte lejos del objetivo'), (r'(\d+) way shot', r'disparo en \1 direcciones'),
        (r'\bSplit\b','dividido') ]
SKIP = re.compile(r"^[}{|]+$|Cooldown Time|Required (Hero )?Rank|Mastery Needed|Tier-\d Advancement|Applies to the following Uniforms|^\s*$|^\[\[File:|^<|^\{\{|^\}\}", re.I)

def clean_line(l):
    l = l.strip()
    l = re.sub(r'^\|+\s*', '', l)      # fmt1: filas de tabla empiezan con |
    l = re.sub(r"'''|''|<br ?/?>|</?font[^>]*>|\{\{[Ss]tar\}\}|\{\{MStar\}\}", '', l)
    l = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', l)
    return l.strip(' *·\t')

def classify_target(raw):
    t = raw.strip().lower().rstrip('.')
    if t in ('self',): return 'self', None
    if t in ('enemy','enemies','all enemies'): return 'enemy', None
    if t in ('allies','all allies','team'): return 'allies', None
    if t == 'villains in team': return 'allies', 'solo villanos del equipo'
    if t == 'heroes in team': return 'allies', 'solo héroes del equipo'
    return None, raw.strip()

GEO_WORDS = re.compile(r'golpe|área|distancia|Cuerpo a cuerpo|teletransporte|disparo|empuje|atrae', re.I)
APPLY_RE = re.compile(r"^Appl(?:y|ies) to\s*:?\s*(.+)", re.I)
META_RE = re.compile(r"^Activ?i?ation Rate\s*:?|^How to Apply\s*:?", re.I)
DMGPCT_RE = re.compile(r"^\d+% (?:Energy|Physical) Damage", re.I)

def translate_body(body):
    fx = {'general':[], 'self':[], 'enemy':[], 'allies':[]}
    scope = None
    seen = set()
    count = 0
    def add(bucket, t):
        nonlocal count
        if t and t not in seen:
            seen.add(t); fx[bucket].append(t); count += 1
    for raw in re.split(r'\n|<br ?/?>', body):
        if count >= 14: break
        l = clean_line(raw)
        if not l or SKIP.search(l): continue
        am = APPLY_RE.match(l)
        if am:
            tgt, note = classify_target(am.group(1))
            if tgt:
                scope = tgt
                if note: add(tgt, '(' + note + ')')
            else:
                scope = None
                add('general', '→ ' + note)
            continue
        t, kind = None, 'fx'
        if META_RE.match(l) or DMGPCT_RE.match(l): kind = 'gen'
        for rx, fn in RULES:
            m = rx.match(l)
            if m: t = fn(m); break
        if t is None:
            t = l
            for rx, rep in GEO: t = re.sub(rx, rep, t)
            if GEO_WORDS.search(t): kind = 'gen'
        if kind == 'gen' or scope is None: add('general', t)
        else: add(scope, t)
    fx = {k:v for k,v in fx.items() if v}
    flat_parts = []
    if 'general' in fx: flat_parts += fx['general']
    for k, lbl in (('self','A sí mismo'),('enemy','Al oponente'),('allies','Al equipo')):
        if k in fx: flat_parts.append(lbl + ': ' + ' / '.join(fx[k]))
    return ' · '.join(flat_parts), fx

II_RE = re.compile(r'penetrate with .{0,80}(INVINCIBLE|ALL DAMAGE IMMUNE)|Ignores? Invincib', re.I|re.S)
CD_RE = re.compile(r'Cooldown Time\s*:?\s*(\d+)\s*second', re.I)
DMG_LINE = re.compile(r"(\d+)% (Energy|Physical) Damage")
TAG_RULES = [
 (r'\bStun', 'Aturdir'), (r'\bBind\b', 'Inmovilizar'), (r'\bFear\b', 'Miedo'),
 (r'\bSilence', 'Silencio'), (r'\bProvoke|\bTaunt', 'Provocar'),
 (r'All Speeds? by \-|Decrease[sd]? .{0,20}Speed|\bSlow\b', 'Ralentizar'),
 (r'\bBleed', 'Sangrado'), (r'damage every \d|\bBurn\b|Poison damage', 'DoT'),
 (r'HP Recovery|Recovery of MA?X HP|\bHeals?\b|\bRecovers\b', 'Curación'),
 (r'\bShield|\bBarrier', 'Escudo'),
 (r'\bInvincible|Immune to all damage', 'Invencibilidad'),
 (r'penetrate with .{0,60}(INVINCIBLE|ALL DAMAGE IMMUNE)', 'Perfora Inmunidad'),
 (r"Ig?nores? target'?s? Dodge", 'Ignora Evasión'),
 (r'Ignore Defense|Defense Penetration|Pierce', 'Perfora DEF'),
 (r'Remo[vb]es? (all )?Debuff', 'Limpia Debuffs'),
 (r'Guaranteed Critical|Critical (Rate|Damage) ?(↑|\+|increase)', 'Buff Crítico'),
 (r'(All |Physical |Energy )?Attack ?(↑|\+\d|by \+|increase)', 'Buff ATQ'),
 (r'(All )?Defense ?(↑|\+\d|by \+|increase)', 'Buff DEF'),
 (r'(All )?Speeds? ?(↑|\+\d|by \+|increase)|Attack Speed ?↑', 'Buff VEL'),
 (r'Dodge Rate increase|Evasion ?(↑|\+)', 'Buff Evasión'),
 (r'\bPushback', 'Empuje'), (r'Knock ?down', 'Derribo'),
]
def effects_to_tags(text):
    tags = []
    for rx, tag in TAG_RULES:
        if re.search(rx, text, re.I) and tag not in tags: tags.append(tag)
    return tags

def mk_skill(slot, name, body, dmg_hint):
    dmg = 'Ninguno'
    mm = re.search(r'\((Energy|Physical) Attack\)', name)
    if mm:
        dmg = 'Energía' if mm.group(1)=='Energy' else 'Físico'
        name = re.sub(r'\s*\((Energy|Physical) Attack\)','',name).strip()
    elif slot.startswith('Activa') or slot=='Definitiva':
        m2 = DMG_LINE.search(body)
        if m2: dmg = 'Energía' if m2.group(2)=='Energy' else 'Físico'
        elif dmg_hint: dmg = dmg_hint
    cdm = CD_RE.search(body)
    d, fx = translate_body(body)
    return {'slot':slot,'n':name,'d':d,'fx':fx,'dmg':dmg,'ii':bool(II_RE.search(body)),
            'tags':effects_to_tags(body),'cd':int(cdm.group(1)) if cdm else None,
            'perm':slot in ('Pasiva','Liderazgo'),'iframe':slot=='Definitiva','gb':False,'sgb':False}

def parse_fmt1(sec, dmg_hint):
    skills, slot_ctx, active_n = [], None, 0
    cur_name, cur_body = None, []
    def flush():
        nonlocal cur_name, cur_body, active_n
        if not cur_name: return
        body = '\n'.join(cur_body)
        if slot_ctx=='Liderazgo': slot='Liderazgo'
        elif slot_ctx=='Pasiva': slot='Pasiva'
        else:
            if re.search(r'Tier-3 Advancement|Tier-4', body): slot='Definitiva'
            else: active_n+=1; slot=f'Activa {active_n}'
        skills.append(mk_skill(slot, cur_name, body, dmg_hint))
        cur_name, cur_body = None, []
    for e in re.split(r'\n\|-\n', sec):
        e = e.strip()
        hm = re.match(r'!\s*(.+)', e)
        if hm:
            flush()
            h = hm.group(1).strip()
            slot_ctx = 'Liderazgo' if 'Leader' in h else ('Pasiva' if 'Passive' in h else 'Activa')
            continue
        nm = re.match(r'\|\s*class="header2"\s*\|(.+)', e)
        if nm:
            flush(); cur_name = re.sub(r"'''|''",'',nm.group(1)).strip(); continue
        if cur_name is not None: cur_body.append(e)
    flush()
    return skills

def split_blocks(text):
    out = []
    for p in re.split(r"(?=''' ?[^'\n][^\n]*?''')", text):
        m = re.match(r"'''(.+?)'''", p)
        if m: out.append((m.group(1).strip(), p))
    return out

def parse_fmt2(wt, dmg_hint):
    base, per_uni = [], {}
    def section(pattern, until=r'\n====|\n==[^=]'):
        m = re.search(pattern, wt)
        if not m: return ''
        rest = wt[m.end():]
        e = re.search(until, rest)
        return rest[:e.start()] if e else rest
    for name, body in split_blocks(section(r'====\s*Leadership\s*===='))[:1]:
        base.append(mk_skill('Liderazgo', name, body, dmg_hint))
    seen = set()
    for name, body in split_blocks(section(r"====\s*Passive Skills?\s*====")):
        key = re.sub(r'\s*v\d+$','',name)
        if key in seen: continue
        seen.add(key)
        base.append(mk_skill('Pasiva', key, body, dmg_hint))
    for name, body in split_blocks(section(r"====\s*''?(?:Ultimate|Awakened) Skill''?\s*===="))[:1]:
        base.append(mk_skill('Definitiva', name, body, dmg_hint))
    for m in re.finditer(r'\n==\[\[File:[^\]]+\]\]"([^"]+)" Uniform==', wt):
        rest = wt[m.end():]
        e = re.search(r'\n==[^=]', rest)
        usec = rest[:e.start()] if e else rest
        am = re.search(r'===\s*Active Skills?\s*===', usec)
        if not am: continue
        atext = usec[am.end():]
        e2 = re.search(r'\n===[^=]', atext)
        if e2: atext = atext[:e2.start()]
        sks, n = [], 0
        for name, body in split_blocks(atext):
            name = re.sub(r'\s*v\d+$','',name)
            if re.search(r'Tier-3 Advancement|Tier-4', body): slot='Definitiva'
            else: n+=1; slot=f'Activa {n}'
            sks.append(mk_skill(slot, name, body, dmg_hint))
        if sks: per_uni[m.group(1)] = sks
    return base, per_uni

results = {}
for fn in glob.glob('work/wikitext/*.json'):
    dd = json.load(open(fn)); name, wt = dd['name'], dd['wt']
    im = re.search(r'\|\s*instinct\s*=\s*(?:\[\[:Category:\w+\|)?([A-Za-z]+)', wt)
    am = re.search(r'\|\s*atk[ _]type\s*=\s*(?:\[\[:Category:\w+\|)?([A-Za-z]+)', wt)
    inst = im.group(1) if im else ''
    atk = am.group(1) if am else ''
    hint = 'Energía' if atk=='Energy' else ('Físico' if atk=='Physical' else None)
    m = re.search(r'(?:^|\n)\s*Skills\s*=\s*\n', wt)
    if m:
        rest = wt[m.end():]; end = rest.find('\n|-|')
        results[name] = {'instinct':inst,'atk':atk,'base':parse_fmt1(rest[:end] if end!=-1 else rest, hint),'per_uni':{}}
    elif re.search(r'==\s*Skills\s*==', wt):
        b, pu = parse_fmt2(wt, hint)
        results[name] = {'instinct':inst,'atk':atk,'base':b,'per_uni':pu}
    else:
        results[name] = {'instinct':inst,'atk':atk,'base':[],'per_uni':{}}

json.dump(results, open('work/wiki_parsed.json','w'), ensure_ascii=False)
th = results['Thanos']['base']
for s in [th[1], th[2], th[-1]]:
    print(f"[{s['slot']}] {s['n']} :: {s['d'][:230]}")
tot = sum(len(r['base'])+sum(len(v) for v in r['per_uni'].values()) for r in results.values())
con_d = sum(1 for r in results.values() for grp in [r['base']]+list(r['per_uni'].values()) for s in grp if s['d'])
print('skills totales:', tot, '| con descripción:', con_d)
