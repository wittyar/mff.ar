import json, os, re, sys, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traducir

# El parser NO traduce: decide la estructura de cada skill (qué línea le pega a quién)
# y guarda el inglés de la wiki tal cual. La traducción vive en traducir.py, para que
# data.js pueda llevar los dos idiomas y la app alternar entre ellos.

SKIP = re.compile(r"^[}{|]+$|Cooldown Time|Required (Hero )?Rank|Mastery Needed|Tier-\d Advancement|Applies to the following Uniforms|^\s*$|^\[\[File:|^<|^\{\{|^\}\}|^\{\||^\|\}|^class=|^style=|^[-–—_=]{2,}$|^:+$", re.I)

# Los íconos de la wiki ([[File:x.png|left|frameless|60x60px]]) no aportan nada al
# efecto y, si se dejan, ocupan lugar en el presupuesto de 14 líneas de parse_body.
FILE_LINK = re.compile(r'\[\[\s*(?:File|Image|Archivo)\s*:[^\[\]]*\]\]', re.I)
# Restos de sintaxis de imagen sueltos: aparecen cuando el corchete de cierre falta.
# Solo se aplica a la línea completa, para no borrar palabras de un efecto real.
IMG_ONLY = re.compile(r'^(?:\s*(?:left|right|center|thumb|thumbnail|frame|frameless|border|baseline|top|middle|bottom'
                      r'|\d+x\d+px|\d+px|link=\S*|alt=\S*)\s*\|?)+', re.I)
# Se sacan TODAS las etiquetas HTML, no solo <br> y <font>: un <span style="color:#0f0">
# metía un '#' literal en el texto, que colisiona con el '#' que traducir.py usa como
# marcador de número. Sin etiquetas, el marcador es inequívoco.
WIKI_MARKUP = re.compile(r"'''|''|</?[a-zA-Z][^>]*/?>|\{\{[Ss]tar\}\}|\{\{MStar\}\}")

def clean_line(l):
    l = l.strip()
    l = re.sub(r'^\|+\s*', '', l)      # fmt1: las filas de tabla empiezan con |
    l = WIKI_MARKUP.sub('', l)
    l = FILE_LINK.sub(' ', l)          # el ícono entero, antes del enlace genérico
    l = re.sub(r'\[\[([^\[\]]+)\]\]', lambda m: m.group(1).split('|')[-1], l)
    l = IMG_ONLY.sub('', l)            # atributos huérfanos de un File: sin cerrar
    l = re.sub(r'\s{2,}', ' ', l)
    return l.strip(' *·|\t')

def classify_target(raw):
    t = raw.strip().lower().rstrip('.')
    if t in ('self',): return 'self', None
    if t in ('enemy','enemies','all enemies','all: enemies','eenmy','target','targets'): return 'enemy', None
    if t in ('allies','all allies','team','all team','all team members','team members',
             'all allies and self','self and allies'): return 'allies', None
    if t == 'villains in team': return 'allies', 'villains in team'
    if t == 'heroes in team': return 'allies', 'heroes in team'
    return None, raw.strip()

APPLY_RE = re.compile(r"^Appl(?:y|ies) to\s*:?\s*(.+)", re.I)
META_RE = re.compile(r"^Activ?i?ation Rate\s*:?|^How to Apply\s*:?", re.I)
DMGPCT_RE = re.compile(r"^\d+% (?:Energy|Physical) Damage", re.I)
# Líneas que describen la geometría del golpe: van al bloque general aunque haya un
# objetivo activo, porque describen la skill y no un efecto sobre alguien.
GEO_RE = re.compile(r'\bRanged\b|\bMelee\b|\b\d+ Hits?\b|\bPushback\b|Draw in enemies|\bAOE\b'
                    r'|Teleport (?:to|away from) target|\d+ way shot|\bSplit\b', re.I)

def parse_body(body, nombre=''):
    """Cuerpo de wikitext -> {bucket: [líneas en inglés]}. Sin traducir."""
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
                add('general', 'Applies to: ' + note)
            continue
        gen = bool(META_RE.match(l) or DMGPCT_RE.match(l) or GEO_RE.search(l))
        add('general' if (gen or scope is None) else scope, l)
    # La primera fila del cuerpo suele repetir el nombre de la skill (1.426 de 3.008):
    # es el encabezado de la tabla de la wiki, no un efecto. La tarjeta ya muestra el
    # nombre, así que se descarta en vez de quedar como una línea a traducir.
    if fx['general'] and nombre and fx['general'][0].strip().lower() == nombre.strip().lower():
        fx['general'].pop(0)
    return {k:v for k,v in fx.items() if v}

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
    fx = parse_body(body, name)
    fx_es = traducir.traducir_fx(fx)
    return {'slot':slot,'n':name,'nEs':traducir.traducir_skill(name),
            'd':traducir.aplanar(fx, traducir.ETIQ_EN),'fx':fx,'fxEs':fx_es,
            'dmg':dmg,'ii':bool(II_RE.search(body)),
            'tags':effects_to_tags(body),'cd':int(cdm.group(1)) if cdm else None,
            'perm':slot in ('Pasiva','Liderazgo'),'iframe':slot=='Definitiva','gb':False,'sgb':False}

# La fila del nombre de la skill viene en tres plantillas distintas segun la pagina:
#   | class="header2" |Nombre   -> cuerpo en la fila siguiente
#   |<center>NOMBRE-EN-NEGRITA  -> cuerpo en la fila siguiente
#   |NOMBRE-EN-NEGRITA + cuerpo -> nombre y cuerpo en la misma fila
NAME_H2 = re.compile(r'\|\s*class="header2"\s*\|(.+)')
NAME_BOLD = re.compile(r"\|\s*(?:<center>\s*)?'''(.+)")

def parse_fmt1(sec, dmg_hint):
    # Cada seccion usa una sola de las tres plantillas de fila-nombre:
    #   class="header2"          -> el nombre es esa fila; las negritas son cuerpo resaltado
    #   negrita en fila propia   -> el nombre ocupa su fila; toda fila multilinea es cuerpo
    #   negrita + cuerpo debajo  -> el nombre es la primera linea de la fila
    entries = [e.strip() for e in re.split(r'\n\|-\n', sec)]
    if 'class="header2"' in sec:
        name_re, solo = NAME_H2, False
    else:
        name_re = NAME_BOLD
        solo = any('\n' not in e and NAME_BOLD.match(e) for e in entries)
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
    for e in entries:
        hm = re.match(r'!\s*(.+)', e)
        if hm:
            flush()
            h = hm.group(1).strip()
            slot_ctx = 'Liderazgo' if 'Leader' in h else ('Pasiva' if 'Passive' in h else 'Activa')
            continue
        head, _, rest = e.partition('\n')
        nm = None if (solo and rest) else name_re.match(head)
        if nm:
            flush()
            cur_name = re.sub(r"'''|''|</?center>", '', nm.group(1)).strip()
            cur_body = [rest] if rest else []
            continue
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

# La seccion de skills es una pestana del tabber ("Skills =", "Skills (Uniforme)=")
# o un encabezado normal ("==Skill==" / "==Skills=="). La primera seccion es la base;
# las siguientes, rotuladas con el nombre de un uniforme, son skills propias de ese uniforme.
SEC_RE = re.compile(r'(?:^|\n)(?:[ \t]*Skills?[ \t]*(?:\(([^)\n]*)\))?[ \t]*=[ \t]*\n|==[ \t]*Skills?[ \t]*==[ \t]*\n)')
SEC_END = re.compile(r'\n\|-\||\n==[^=]')
# discrimina fmt1 (tabla con filas de encabezado) de fmt2 (subsecciones ====Leadership====)
TABLE_HDR = re.compile(r"(?:^|\n)!\s*'*\s*(?:Leader|Passive|Active|Ultimate)", re.I)

def skill_sections(wt):
    """[(etiqueta|None, texto)] de cada seccion de skills con tabla estilo fmt1."""
    out = []
    for m in SEC_RE.finditer(wt):
        rest = wt[m.end():]
        e = SEC_END.search(rest)
        sec = rest[:e.start()] if e else rest
        if TABLE_HDR.search(sec): out.append((m.group(1), sec))
    return out

results = {}
for fn in glob.glob('work/wikitext/*.json'):
    dd = json.load(open(fn)); name, wt = dd['name'], dd['wt']
    im = re.search(r'\|\s*instinct\s*=\s*(?:\[\[:Category:\w+\|)?([A-Za-z]+)', wt)
    am = re.search(r'\|\s*atk[ _]type\s*=\s*(?:\[\[:Category:\w+\|)?([A-Za-z]+)', wt)
    inst = im.group(1) if im else ''
    atk = am.group(1) if am else ''
    hint = 'Energía' if atk=='Energy' else ('Físico' if atk=='Physical' else None)
    sections = skill_sections(wt)
    if sections:
        base, per_uni = [], {}
        for label, sec in sections:
            sks = parse_fmt1(sec, hint)
            if not sks: continue
            if not base: base = sks
            elif label: per_uni[label] = sks
        results[name] = {'instinct':inst,'atk':atk,'base':base,'per_uni':per_uni}
    elif re.search(r'==\s*Skills\s*==', wt):
        b, pu = parse_fmt2(wt, hint)
        results[name] = {'instinct':inst,'atk':atk,'base':b,'per_uni':pu}
    else:
        results[name] = {'instinct':inst,'atk':atk,'base':[],'per_uni':{}}

json.dump(results, open('work/wiki_parsed.json','w'), ensure_ascii=False)
todas = [s for r in results.values() for grp in [r['base']]+list(r['per_uni'].values()) for s in grp]
lineas = [(l, es) for s in todas for k in s['fx'] for l, es in zip(s['fx'][k], s['fxEs'][k])]
sin = sorted({l for l, es in lineas if es is None})
nombres_sin = sorted({s['n'] for s in todas if s['nEs'] is None})
json.dump(sin, open('work/sin_traducir.json','w'), ensure_ascii=False, indent=1)
json.dump(nombres_sin, open('work/skills_sin_traducir.json','w'), ensure_ascii=False, indent=1)
distintas = {l for l, _ in lineas}
print('skills:', len(todas), '| líneas de efecto:', len(lineas), f'({len(distintas)} distintas)')
print(f"traducidas: {len(lineas)-sum(1 for _, es in lineas if es is None)}/{len(lineas)}"
      f" líneas — sin traducir {len(sin)} distintas (work/sin_traducir.json)")
distintos_n = {s['n'] for s in todas}
print(f"nombres de skill: {len(distintos_n)-len(nombres_sin)}/{len(distintos_n)} distintos con traducción"
      f" ({len(nombres_sin)} sin ella, work/skills_sin_traducir.json)")
