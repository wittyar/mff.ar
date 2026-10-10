"""Prueba de scripts/liderazgos.py (derivar), sin work/ (carril Q, 5 de octubre de 2026). Reemplaza a
liderazgos_heredados/, que probaba completar_liderazgos (la regla anterior, que ya no existe).

A. Sobre los datos de formato 7 (ORIGEN, por defecto carril-consistencia/datos7), con Leads & Supports tal como lo
   publica: el MFF_SOPORTES de data.js sin los liderazgos que copiaba la regla anterior (los «Completados» de su
   docs/AUDITORIA.md).
   1. Es pura: no cambia lo que recibe y da lo mismo dos veces.
   2. Lo que copiaba la regla anterior (knull1, shangchi2, moongirl1, ghost2, sentinel2) sale igual derivado en stats,
      valores, duración, condición, restricción, activación y recarga. Lo único distinto es «Notable» (sig).
   3. Nada silencioso: cada parte de la Leader Skill de cada variante sin liderazgo de Leads & Supports está derivada o
      listada con su motivo; a las que lo tienen no se les deriva nada, y cada slot suyo tiene su verificación.
   4. Forma: cada slot derivado lleva "src": "api", el nombre de su Leader Skill y efectos con un stat del catálogo
      (MFF_CATALOGO.soporte); su activación y sus condiciones tienen traducción (MFF_TXT).
   5. La verificación: cuántos slots dan igual y en qué difieren los demás.
B. Casos modificados a propósito, en copias en memoria: una contradicción de Leads & Supports, una activación sin
   correspondencia, un objetivo sin nombre, $TIME sin duración, $HEROSUBTYPE1 sin valor y un «Give Power» con lo que
   otorga detrás.
C. fuentes.nombres_pj con el work/characters.json reducido de liderazgos_heredados/fixture, y el camino del build
   sobre los datos crudos de ese fixture (skills_api.py, fuentes.soportes(), derivar()).
D. Las correspondencias a mano (scripts/contenido/liderazgos_api.json; carril Q, segunda parte): validar() con el
   contenido del repo y con uno roto a propósito; Leads & Supports manda (distinto: para; igual o sin uso: aviso); la
   activación a mano va con el texto de la API y su traducción, y el efecto, con el stat, el número y la duración; lo
   que queda sin derivar es «Give Power» o un efecto sin stat; sin lo de a mano, lo de antes.

  python3 prueba.py [ORIGEN]"""
import copy, json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = RAIZ
S = SALIDA
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import fuentes, liderazgos as L  # noqa: E402

ORIGEN = sys.argv[1] if len(sys.argv) > 1 else f'{S}/carril-consistencia/datos7'
fallas = []


def chequeo(nombre, cond, detalle=''):
    print(('OK   ' if cond else 'FALLA'), nombre, '|', detalle)
    if not cond:
        fallas.append(nombre)


def cargar(ruta):
    texto = open(ruta, encoding='utf-8').read()
    dec, out = json.JSONDecoder(), {}
    for m in re.finditer(r'^window\.(MFF_[A-Z_]+) = ', texto, re.M):
        out[m.group(1)], _ = dec.raw_decode(texto, m.end())
    return out


D = cargar(os.path.join(ORIGEN, 'data.js'))
SK, T, CH = D['MFF_SKILLS'], D['MFF_TABLAS'], D['MFF_SEED_CHARACTERS']
NOMBRES = {ch['p']: ch['name'] for ch in CH} | {u['p']: ch['name'] for ch in CH for u in ch['uniforms']}
aud = open(os.path.join(ORIGEN, 'docs', 'AUDITORIA.md'), encoding='utf-8').read()
COPIADOS = re.findall(r'\(`([^`]+)`\) ← ', aud.split('### Completados')[1].split('\n### ')[0])
LS = {p: e for p, e in D['MFF_SOPORTES'].items() if p not in COPIADOS}
MANUAL = json.load(open(os.path.join(REPO, 'scripts', 'contenido', 'liderazgos_api.json'), encoding='utf-8'))
CAT = json.load(open(os.path.join(REPO, 'scripts', 'contenido', 'catalogo.json'), encoding='utf-8'))


def leader_skill(skills, p):
    return next(s for s in skills[p] if s['sl'] == 'Leader Skill')


def motivos_de(R, p):
    return [m for x in R['sin_derivar'] if x['p'] == p for m, _ in x['motivos']]


print('======== A. Datos de formato 7:', ORIGEN)
print('copiados por la regla anterior:', COPIADOS)
chequeo('A0 los copiados son los cinco de la prueba de la regla anterior',
        sorted(COPIADOS) == ['ghost2', 'knull1', 'moongirl1', 'sentinel2', 'shangchi2'], COPIADOS)
entrada = copy.deepcopy((LS, SK, T, NOMBRES, MANUAL))
R = L.derivar(LS, SK, T, NOMBRES, MANUAL)
chequeo('A1 no cambia lo que recibe', entrada == (LS, SK, T, NOMBRES, MANUAL))
chequeo('A1 da lo mismo dos veces', json.dumps(R, sort_keys=True, default=sorted) == json.dumps(L.derivar(LS, SK, T, NOMBRES, MANUAL), sort_keys=True, default=sorted))

campos = ('r', 'ac', 'cd')
for p in COPIADOS:
    der, viejo = R['derivados'].get(p, {}), D['MFF_SOPORTES'][p]
    iguales = set(der) == set(viejo) and all(
        all(der[k].get(c) == viejo[k].get(c) for c in campos) and L._comparar(der[k], viejo[k]) == [] for k in der)
    dif = sorted({c for k in viejo for c in viejo[k] if c not in ('fx',) + campos and der.get(k, {}).get(c) != viejo[k][c]})
    chequeo(f'A2 {p}: derivado igual a lo copiado', iguales, f'derivado {json.dumps(der, ensure_ascii=False)}; difiere solo en {dif}')
    chequeo(f'A2 {p}: lo único distinto es «Notable» o nada', set(dif) <= {'sig'}, dif)

con_ls = {p for p, e in LS.items() if any(k in e for k in L.LIDERAZGOS)}
sin_ls = set(NOMBRES) - con_ls
chequeo('A3 a las que tienen liderazgo de Leads & Supports no se les deriva nada', not (set(R['derivados']) & con_ls))
listados = {(x['p'], x['slot']) for x in R['sin_derivar']}
silenciosos = []
for p in sorted(sin_ls):
    ps, problema = L.partes(leader_skill(SK, p), T, NOMBRES[p])
    esperados = {L.LIDERAZGOS[0]} if ps is None else set(L.LIDERAZGOS[:len(ps)])
    tiene = set(R['derivados'].get(p, {})) | {k for q, k in listados if q == p}
    if tiene != esperados or set(R['derivados'].get(p, {})) & {k for q, k in listados if q == p}:
        silenciosos.append(p)
chequeo('A3 cada parte de cada variante sin Leads & Supports está derivada o listada', not silenciosos, silenciosos[:5])
verificados = {(x['p'], x['slot']) for x in R['verificacion']}
sin_verif = [(p, k) for p in sorted(con_ls) for k in L.LIDERAZGOS if k in LS[p] and (p, k) not in verificados]
chequeo('A3 cada slot de liderazgo de Leads & Supports tiene su verificación', not sin_verif, sin_verif[:5])

stats = set(D['MFF_CATALOGO']['soporte'])
mal = []
for p, x in R['derivados'].items():
    nombre = T['name'][leader_skill(SK, p)['n']]['en']
    for k, s in x.items():
        if s.get('src') != 'api' or s.get('n') != nombre or not s['fx'] or 'sig' in s:
            mal.append((p, k, 'forma'))
        mal += [(p, k, g['s']) for g in s['fx'] if g['s'] not in stats]
        mal += [(p, k, t) for t in [s.get('ac')] + [g.get('c') for g in s['fx']] if t and t not in D['MFF_TXT'] and not R['textos'].get(t)]
chequeo('A4 forma de lo derivado (src, nombre, sin Notable, stats del catálogo, textos traducidos)', not mal, mal[:5])

V = R['verificacion']
cuenta = {e: sum(1 for x in V if x['estado'] == e) for e in ('igual', 'distinto', 'sin_derivar', 'solo_ls', 'solo_api')}
print('   verificación:', cuenta, '| derivados', len(R['derivados']), 'variantes,',
      sum(len(x) for x in R['derivados'].values()), 'slots | sin derivar', len(R['sin_derivar']), 'slots')
chequeo('A5 cada distinto dice en qué difiere y cada sin derivar, por qué',
        all(x.get('dif') for x in V if x['estado'] == 'distinto') and all(x.get('motivos') for x in V if x['estado'] == 'sin_derivar')
        and all(x.get('motivos') for x in R['sin_derivar']))
chequeo('A5 la mayoría de los slots de Leads & Supports da igual derivado', cuenta['igual'] > 0.8 * len(V),
        f"{cuenta['igual']} de {len(V)}")
for x in V:
    if x['estado'] == 'distinto':
        print('   distinto:', x['p'], x['slot'], '; '.join(x['dif']))

print('\n======== B. Casos modificados a propósito (copias en memoria)')
# B1. Leads & Supports contradice un efecto: el «All Basic Attacks» de thanos, publicado como «All Basic Defenses».
ls = copy.deepcopy(LS)
ls['thanos']['leader']['fx'][0]['s'] = 'All Basic Defenses'
R1 = L.derivar(ls, SK, T, NOMBRES, MANUAL)
clave = ['ALL BASIC ATTACKS INCREASE', 'Increases all Basic Attacks by #%', None]
contra = [c for c, _ in R1['contradicciones']['efectos']]
chequeo('B1 la contradicción se lista', clave in contra, contra)
# Las partes con ese efecto, de las variantes sin Leads & Supports: [(retrato, slot)].
usan = [(p, L.LIDERAZGOS[i]) for p in sorted(sin_ls) for i, x in enumerate(L.partes(leader_skill(SK, p), T, NOMBRES[p])[0] or [])
        if any(L.clave(f, T) == tuple(clave) for _, f in x['efectos'])]
listadas = {(x['p'], x['slot']) for x in R1['sin_derivar'] if 'contradiccion' in [m for m, _ in x['motivos']]}
chequeo('B1 ningún slot con ese efecto se deriva: va listado como contradicción', usan and all(
    u in listadas and u[1] not in R1['derivados'].get(u[0], {}) for u in usan), f'{len(usan)} slots lo usan: {usan}')
# B2. Una activación sin correspondencia: carnage2 (al recibir un debuff) con «when attacking», que no está en
# Leads & Supports ni a mano.
sk = copy.deepcopy(SK)
st = leader_skill(sk, 'carnage2')['st'][0]
st['ac'], st['av'] = next(i for i, f in enumerate(T['act']) if f['en'] == 'when attacking'), []
R2 = L.derivar(LS, sk, T, NOMBRES, MANUAL)
chequeo('B2 activación sin correspondencia: no se deriva', 'carnage2' not in R2['derivados'] and motivos_de(R2, 'carnage2') == ['activacion'],
        motivos_de(R2, 'carnage2'))
chequeo('B2 lo demás no cambia', {p: x for p, x in R2['derivados'].items()} == {p: x for p, x in R['derivados'].items() if p != 'carnage2'})
# B3. Un objetivo sin nombre: athena (derivada) con «Target ID: 88».
sk = copy.deepcopy(SK)
leader_skill(sk, 'athena')['st'][0]['tg'] = next(i for i, f in enumerate(T['tgt']) if f['en'] == 'Target ID: 88')
R3 = L.derivar(LS, sk, T, NOMBRES, MANUAL)
chequeo('B3 objetivo sin nombre: no se deriva', 'athena' not in R3['derivados'] and motivos_de(R3, 'athena') == ['objetivo'],
        motivos_de(R3, 'athena'))
# B4. $TIME sin duración y $HEROSUBTYPE1 sin valor, sumados a la Leader Skill de athena.
sk = copy.deepcopy(SK)
fx = leader_skill(sk, 'athena')['st'][0]['fx']
ab = next(i for i, f in enumerate(T['ab']) if f['en'] == "INCREASES BASIC DAMAGE BASED ON CHARACTER'S GENDER")
fx.append({'a': ab, 'p': next(i for i, f in enumerate(T['desc']) if f['en'] == 'Increases basic damage dealt to $HEROSUBTYPE# types by #%.'),
           'v': [1, 48]})
fx.append({'a': fx[0]['a'], 'p': next(i for i, f in enumerate(T['desc']) if f['en'].startswith('HP does not drop below # for $TIME')),
           'v': [1]})
R4 = L.derivar(LS, sk, T, NOMBRES, MANUAL)
det = [d for x in R4['sin_derivar'] if x['p'] == 'athena' for m, d in x['motivos'] if m == 'valor']
chequeo('B4 $HEROSUBTYPE1 y $TIME sin publicar: no se deriva y se dice cuál', 'athena' not in R4['derivados']
        and any('$HEROSUBTYPE1' in d for d in det) and any('$TIME' in d for d in det), det)
# B5. «Give Power» con lo que otorga detrás: athena da sus defensas y otorga ataques por 10 s.
sk = copy.deepcopy(SK)
fx = leader_skill(sk, 'athena')['st'][0]['fx']
gp = next(f for p in SK for s in SK[p] if s['sl'] == 'Leader Skill' for st in s['st'] for f in st['fx'] if T['ab'][f['a']]['en'] == 'Give Power')
aba = leader_skill(SK, 'knull')['st'][0]['fx'][0]
fx += [dict(gp, d=10), copy.deepcopy(aba)]
R5 = L.derivar(LS, sk, T, NOMBRES, MANUAL)
chequeo('B5 la parte del «Give Power» no se deriva y la primera sí',
        list(R5['derivados'].get('athena', {})) == ['leader'] and R5['derivados']['athena']['leader'] == R['derivados']['athena']['leader']
        and [(x['slot'], [m for m, _ in x['motivos']]) for x in R5['sin_derivar'] if x['p'] == 'athena'] == [('leader2', ['otorga'])],
        json.dumps([x for x in R5['sin_derivar'] if x['p'] == 'athena'], ensure_ascii=False))

# B6. Un objetivo «Activates when» que ningún liderazgo de Leads & Supports muestra: no se deriva («condicion»).
T6 = copy.deepcopy(T)
T6['tgt'].append({'en': 'All Allies\\nActivates when: Speed Type Ally enters', 'es': 'x'})
sk = copy.deepcopy(SK)
leader_skill(sk, 'athena')['st'][0]['tg'] = len(T6['tgt']) - 1
R6 = L.derivar(LS, sk, T6, NOMBRES, MANUAL)
chequeo('B6 condición sin correspondencia: no se deriva', 'athena' not in R6['derivados'] and motivos_de(R6, 'athena') == ['condicion'],
        motivos_de(R6, 'athena'))
# B7. Drax y Nebula (carril Q, segunda parte): la condición va porque el texto de la API la trae («Activates when»); su
# texto sale de Drax y Drax — All-New, All-Different, y que Drax — Classic y Annihilation no la tengan en Leads &
# Supports es una diferencia de la verificación, no una contradicción.
cond = ['when 1 Combat', 'when 2 Combats', 'when 3 Combats']
chequeo('B7 Nebula se deriva con la condición de cada efecto', all(
    [g.get('c') for g in R['derivados'].get(p, {}).get('leader', {}).get('fx', [])] == cond for p in ('nebula', 'nebula1', 'nebula4', 'nebula5', 'nebula6')),
    R['derivados'].get('nebula'))
V = {(x['p'], x['slot']): x for x in R['verificacion']}
chequeo('B7 Drax: iguales los que la publican, distintos (la condición) los que no',
        [V[(p, 'leader')]['estado'] for p in ('drax', 'drax1', 'drax2', 'drax3')] == ['igual', 'igual', 'distinto', 'distinto']
        and 'when 1 Combat' in V[('drax2', 'leader')]['dif'][0] and not R['contradicciones']['condiciones'],
        [V[(p, 'leader')] for p in ('drax2',)])

print('\n======== D. Correspondencias a mano (scripts/contenido/liderazgos_api.json)')
chequeo('D1 el contenido del repo valida contra MFF_TABLAS y el catálogo', L.validar(MANUAL, T, CAT) == [], L.validar(MANUAL, T, CAT))
malo = copy.deepcopy(MANUAL)
malo['efectos'] += [
    {'ab': 'POISON RESIST ↑', 'desc': 'Increases Poison Resist by #%.', 'stat': 'Poison Resist'},          # stat que no existe
    {'ab': 'FLAME RESIST ↑', 'desc': 'Increases Flame Resist by #%', 'stat': 'Fire Resist'},               # texto que no es el de la API
    {'ab': 'FLAME RESIST ↑', 'desc': 'Increases Flame Resist by #%.', 'stat': 'Fire Resist'},              # repetido
    {'ab': 'ENERGY SHIELD', 'desc': 'Creates an energy Shield equal to #% of Max HP', 'stat': 'Physical Defense'},  # otra clasificación
    {'ab': 'HP STEAL', 'desc': 'Recovers HP equal to #% of damage dealt to a target<br>Cannot recover more than #% HP each time damage is dealt.', 'stat': 'Heal'},  # dos números
    {'ab': 'PHYSICAL DEFENSE ↑', 'desc': '#% increase of Physical Defense.'},                              # sin stat
]
malo['activaciones'] += ['when tagging', 'when tagging an ally']
problemas = L.validar(malo, T, CAT)
for p_ in problemas:
    print('   ', p_)
esperados = ["«Poison Resist» no es un stat del catálogo", 'la API no tiene ese texto', 'repetido', "y a «Physical Defense», como", "y a «Heal», como",
             'un solo número', 'lleva ab, desc y stat', '«when tagging»: repetida', '«when tagging an ally»: la API no tiene ese texto']
chequeo('D2 validar dice cada problema', all(any(e in p_ for p_ in problemas) for e in esperados) and len(problemas) == len(esperados),
        [e for e in esperados if not any(e in p_ for p_ in problemas)])
chequeo('D2 validar: una clave de más o de menos', L.validar({'efectos': [], 'activaciones': []}, T, CAT) == ['lleva nota, efectos, activaciones y otorga'])
# D3. Lo que publica Leads & Supports manda: distinto, el build para; igual o sin uso, aviso.
m = copy.deepcopy(MANUAL)
m['efectos'].append({'ab': 'ALL BASIC ATTACKS INCREASE', 'desc': 'Increases all Basic Attacks by #%', 'stat': 'All Basic Defenses'})
try:
    L.derivar(LS, SK, T, NOMBRES, m)
    paro = None
except SystemExit as e:
    paro = str(e)
chequeo('D3 Leads & Supports dice otra cosa: el build para y dice qué', paro is not None and 'Increases all Basic Attacks by #%' in paro
        and 'All Basic Attacks' in paro, paro)
m = copy.deepcopy(MANUAL)
m['efectos'].append({'ab': 'ALL BASIC ATTACKS INCREASE', 'desc': 'Increases all Basic Attacks by #%', 'stat': 'All Basic Attacks'})
m['activaciones'] += ['when debuffed', '#% rate when debuffed']
RM = L.derivar(LS, SK, T, NOMBRES, m)
av = RM['a_mano']['avisos']
chequeo('D3 lo que Leads & Supports publica igual, o que ninguna Leader Skill tiene, sobra (aviso) y no cambia nada',
        len(av) == 3 and any('Increases all Basic Attacks' in a and 'sobra' in a for a in av)
        and any('«when debuffed»: Leads & Supports publica todas' in a for a in av)
        and any('«#% rate when debuffed»: ninguna Leader Skill' in a for a in av) and RM['derivados'] == R['derivados'], av)
chequeo('D3 el contenido del repo no tiene avisos', R['a_mano']['avisos'] == [], R['a_mano']['avisos'])
# D4. La activación a mano va con el texto de la API y su traducción de la API; la aprendida, con la de Leads & Supports.
der = R['derivados']
chequeo('D4 activación a mano: el texto de la API', der['colossus']['leader'].get('ac') == '25% rate when hit'
        and der['warwolf']['leader'].get('ac') == 'When enemies are below 30% HP,' and der['rescue']['leader'].get('ac') == 'when HP is below 30%',
        {p: der[p]['leader'].get('ac') for p in ('colossus', 'warwolf', 'rescue')})
chequeo('D4 su traducción es la de la API, con sus números', R['textos'].get('25% rate when hit') == '25% al recibir un golpe'
        and R['textos'].get('when tagging') == 'al cambiar de personaje' and set(R['textos']) == {
            x.get('ac') for e in der.values() for x in e.values() if x.get('ac') not in ('When Debuffed', 'When HP is below 99%', None)},
        R['textos'])
chequeo('D4 la aprendida sigue con el texto de Leads & Supports', der['sentinel2']['leader'].get('ac') == 'When Debuffed'
        and 'When Debuffed' not in R['textos'])
# D5. Los efectos a mano: el stat con el número del texto y la duración del efecto, si la publica.
chequeo('D5 efecto a mano: stat, valor y duración', der['killmonger']['leader']['fx'] == [{'s': 'Physical Defense', 'v': 50}]
        and der['vision']['leader']['fx'] == [{'s': 'Super Armor, All Basic Defenses', 'v': 30, 'd': 10}]
        and der['gamora']['leader']['fx'] == [{'s': 'Attack Speed', 'v': 13.5}],
        {p: der[p]['leader']['fx'] for p in ('killmonger', 'vision', 'gamora')})
# D6. Lo que queda sin derivar: «Give Power» o un efecto sin stat en el catálogo.
sin_stat = {'COLD IMMUNITY', 'BLEED', 'ENERGY SHIELD', 'HP STEAL', 'PHYSICAL SHIELD', 'ALL DAMAGE IMMUNE', 'PARALYZE', 'POISON RESIST ↑', 'RESIST'}
quedan = [(x['p'], m_, d) for x in R['sin_derivar'] for m_, d in x['motivos']]
chequeo('D6 sin derivar: solo «Give Power» y efectos sin stat', all(m_ == 'otorga' or (m_ == 'efecto' and re.search(r'\(([^()]+)\)$', d).group(1) in sin_stat)
                                                                     for _, m_, d in quedan), [q for q in quedan if q[1] not in ('otorga', 'efecto')][:5])
print('   derivados', len(der), 'variantes,', sum(len(x) for x in der.values()), 'slots | sin derivar', len(R['sin_derivar']), 'slots')
# D7. Sin lo de a mano se deriva lo mismo que antes de cargarlo (la parte aprendida no cambia).
R0 = L.derivar(LS, SK, T, NOMBRES, {'nota': 'x', 'efectos': [], 'activaciones': [], 'otorga': []})
chequeo('D7 sin lo de a mano: solo lo aprendido', all(der[p][k] == y for p, x in R0['derivados'].items() for k, y in x.items())
        and len(R0['derivados']) == 333 and sum(len(x) for x in R0['derivados'].values()) == 350,
        (len(R0['derivados']), sum(len(x) for x in R0['derivados'].values())))

# D8. Lo que otorga un «Give Power» según el juego (carril de cierre, 5 de octubre de 2026): Mephisto — Master of Hell.
print('\n======== D8. «Give Power» que dice el juego (otorga)')
esperado = {'n': 'Lord of Hell', 'r': ['Side', 'Supervillano'], 'ac': 'When Debuffed', 'cd': 20,
            'fx': [{'s': 'Remove All Debuffs', 'd': 12}], 'src': 'api', 'otorga': ['juego-ficha-ko']}
chequeo('D8 Mephisto — Master of Hell: el segundo slot, como lo dice el juego y con su fuente',
        der.get('mephisto1', {}).get('leader2') == esperado, der.get('mephisto1'))
base = LS['mephisto']['leader2']
chequeo('D8 es, valor por valor, el segundo liderazgo que Leads & Supports publica para la base (hallazgo)',
        all(esperado[k] == base[k] for k in ('r', 'ac', 'cd', 'fx')), base)
chequeo('D8 sin derivar por «Give Power» queda solo Sentry — Thunderbolts*',
        sorted(x['p'] for x in R['sin_derivar'] if any(m_ == 'otorga' for m_, _ in x['motivos'])) == ['sentry2'])
chequeo('D8 la verificación de los 19 pares no cambia (sin derivar por «Give Power»)',
        sum(1 for x in R['verificacion'] if x['estado'] == 'sin_derivar' and any(m_ == 'otorga' for m_, _ in x['motivos'])) == 19)
chequeo('D8 el informe lo lista con su fuente', [o[:3] for o in R['a_mano']['otorga']] == [['mephisto1', 'Lord of Hell', ['juego-ficha-ko']]],
        R['a_mano']['otorga'])
roto = copy.deepcopy(MANUAL)
roto['otorga'] += [{'p': 'sentry2', 'skill': 'Shining Hero', 'ac': '#% rate when hit', 'cd': -1, 'fx': [{'s': 'Inventado'}],
                    'fuente': 'juego-ficha-ko', 'juego': 'x'},
                   {'p': 'sentry2', 'skill': 'Shining Hero', 'fx': []},
                   copy.deepcopy(MANUAL['otorga'][0])]
pr = L.validar(roto, T, CAT)
for p_ in pr:
    print('   ', p_)
chequeo('D8 validar dice cada problema', len(pr) == 7 and any('sin números' in x for x in pr) and any('recarga' in x for x in pr)
        and any('Inventado' in x for x in pr) and any('fuente es una lista' in x for x in pr) and any('lleva p, skill' in x for x in pr)
        and any('repetido' in x for x in pr), pr)
# Sobra: otra Leader Skill, o una sin «Give Power»: aviso, y nada cambia.
sobra = copy.deepcopy(MANUAL)
sobra['otorga'] += [dict(MANUAL['otorga'][0], p='sentry2'), dict(MANUAL['otorga'][0], p='mephisto', skill='Soul Contract')]
RS = L.derivar(LS, SK, T, NOMBRES, sobra)
chequeo('D8 sobra (otra Leader Skill, o sin «Give Power»): aviso y nada cambia',
        RS['derivados'] == R['derivados'] and len(RS['a_mano']['avisos']) == 2 and all('sobra' in a for a in RS['a_mano']['avisos']),
        RS['a_mano']['avisos'])
# Leads & Supports manda: para un par, lo mismo que publica sobra; otra cosa para el build.
igual = copy.deepcopy(MANUAL)
igual['otorga'].append({'p': 'deadpool8', 'skill': "Marvel's Savior", 'ac': 'when debuffed', 'cd': 25,
                        'fx': [{'s': 'Remove All Debuffs', 'd': 10}], 'fuente': ['juego-ficha-ko'], 'juego': 'x'})
RI = L.derivar(LS, SK, T, NOMBRES, igual)
chequeo('D8 un par que Leads & Supports publica igual: aviso, sobra', RI['derivados'] == R['derivados']
        and any('deadpool8' in a and 'sobra' in a for a in RI['a_mano']['avisos']), RI['a_mano']['avisos'])
distinto = copy.deepcopy(igual)
distinto['otorga'][-1]['cd'] = 20
try:
    L.derivar(LS, SK, T, NOMBRES, distinto)
    chequeo('D8 un par que Leads & Supports publica distinto: el build para', False)
except SystemExit as e:
    chequeo('D8 un par que Leads & Supports publica distinto: el build para', 'deadpool8' in str(e), str(e)[:200])
# Activación a mano: va con el texto de la API y su traducción.
mano = copy.deepcopy(MANUAL)
mano['otorga'] = [dict(MANUAL['otorga'][0], p='sentry2', skill='Shining Hero', ac='when tagging')]
RM2 = L.derivar(LS, SK, T, NOMBRES, mano)
s2 = RM2['derivados'].get('sentry2', {}).get('leader2', {})
chequeo('D8 activación a mano: el texto y la traducción de la API', s2.get('ac') == 'when tagging'
        and RM2['textos'].get('when tagging') == 'al cambiar de personaje' and s2.get('r') is None, (s2, RM2['textos'].get('when tagging')))

print('\n======== C. fuentes.nombres_pj (work/characters.json reducido del fixture)')
chars = json.load(open(os.path.join(AQUI, '..', 'liderazgos_heredados', 'fixture', 'work', 'characters.json'), encoding='utf-8'))
n = fuentes.nombres_pj(chars)
chequeo('C1 cada retrato con el personaje de su base', len(n) == len(chars) and all(
    n[r['portrait']] == next(b['character'] for b in chars if b['portrait'] == r['base_portrait']) for r in chars),
    {p: n[p] for p in list(n)[:4]})

# C2. El camino del build sobre datos crudos: el fixture de liderazgos_heredados (la API de skills de 29 retratos y
# /api/supports de 6, bajados el 2 de octubre; los demás soportes, de data.js) con skills_api.py, fuentes.soportes(),
# fuentes.nombres_pj() y derivar(), como en fuentes.main(). Con menos pares se aprende menos, pero lo que deriva para
# los cinco que copiaba la regla anterior tiene que ser lo mismo que con todos los datos.
FIX = os.path.join(AQUI, '..', 'liderazgos_heredados', 'fixture')
r = subprocess.run([sys.executable, os.path.join(REPO, 'scripts', 'skills_api.py')], cwd=FIX, capture_output=True, text=True)
chequeo('C2 skills_api.py corre sobre el fixture', r.returncode == 0, (r.stdout + r.stderr).strip()[-300:])
crudo = json.load(open(os.path.join(FIX, 'work', 'skills_parsed.json'), encoding='utf-8'))
aqui = os.getcwd(); os.chdir(FIX)
retratos = {r['portrait'] for r in chars} | {r['base_portrait'] for r in chars}
sop = fuentes.soportes(retratos, {r['character'] for r in chars})[0]
os.chdir(aqui)
sop.update(json.load(open(os.path.join(FIX, 'soportes_de_datajs.json'), encoding='utf-8')))
RF = L.derivar(sop, crudo['skills'], crudo['tablas'], fuentes.nombres_pj(chars), MANUAL)
iguales = {p: RF['derivados'].get(p) == R['derivados'].get(p) for p in COPIADOS}
chequeo('C2 lo derivado de los datos crudos es lo mismo que con data.js', all(iguales.values()),
        {p: RF['derivados'].get(p) for p, ok_ in iguales.items() if not ok_})
print('   del fixture: aprendidos', len(RF['correspondencia']['efectos']), 'efectos; derivados', sorted(RF['derivados']),
      '| sin derivar', [(x['p'], [m for m, _ in x['motivos']]) for x in RF['sin_derivar']])

print('\nFALLAS:', fallas or 'ninguna')
