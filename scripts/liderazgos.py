#!/usr/bin/env python3
"""Los liderazgos que Leads & Supports no publica, armados con la Leader Skill de la API de skills (Ezequiel, 4
de octubre de 2026: «¿Tomamos los liderazgos que Leads & Supports no publica de la Leader Skill de la API?»,
«si, tomalos de ahí»).

derivar() es una función pura y la única ruta. La usan fuentes.py, en el build (los slots derivados van a
MFF_SOPORTES con "src": "api", y lo demás a la sección 12 de docs/AUDITORIA.md), y completitud.py, sobre data.js
(los slots que no se pudieron derivar son el faltante «Liderazgo sin completar» de docs/COMPLETITUD.md).

1. Partes. La Leader Skill de la API tiene una etapa: un objetivo, una activación y sus efectos. Se parte en los
   slots de liderazgo de Leads & Supports (leader y leader2) con estas reglas, que la verificación contrasta:
   - El objetivo da la restricción: un grupo de aliados, la suya (scripts/dominio.py, OBJETIVO_GRUPO, que viaja
     en MFF_TABLAS.tgt); «All Allies», ninguna; «Self», el personaje. «All Allies for the first effect, Self for
     the second effect» da dos partes: el primer efecto, para todos; el segundo, para él. «X\\nActivates when: Y
     enters» es X, con una condición por efecto (cuántos Y hay en el equipo): la lleva porque el texto de la API
     la trae, y su texto se aprende.
   - «Give Power» («Acquires the following effect for $TIME sec.») y lo que sigue van en una parte aparte, al
     final: es lo que Leads & Supports publica como segundo liderazgo. La API no dice qué otorga ni por cuánto
     tiempo, así que esa parte no se deriva, salvo que A_MANO diga qué otorga según el juego (abajo).
   - La activación de la etapa y la recarga de la skill van en cada parte.
   La primera parte va a leader y la segunda a leader2.
2. Correspondencia. Se aprende de las variantes que tienen las dos cosas: cada parte con el slot de Leads &
   Supports del mismo lugar y, dentro, los efectos en orden. Un efecto de la API da un stat de Leads & Supports
   por cada número de su texto (salvo el de un marcador, como $HEROSUBTYPE1), con ese número de valor (con o sin
   signo), o uno sin valor si no trae números, y la duración si la publican los dos. De ahí sale qué stats da cada efecto de la API (por su etiqueta, su texto y
   el valor de su marcador), qué texto de Leads & Supports tiene cada activación y qué condición lleva cada efecto
   de un objetivo «Activates when» (de las variantes en que Leads & Supports la publica: si no la publica, es una
   diferencia que lista la verificación, no otra condición). Si dos variantes dicen distinto para lo mismo, no se
   usa: es una contradicción y se lista.
   Lo que Leads & Supports no publica en ningún liderazgo va a mano en scripts/contenido/liderazgos_api.json
   (validar()): un efecto de la API da un stat del catálogo con el número de su texto, y una activación de la API va
   con su texto. Y lo que otorga el «Give Power» de una Leader Skill, si lo dice el juego (otorga: Ezequiel, 5 de
   octubre de 2026): sus efectos (stats del catálogo), su activación (un texto de la API, que pasa como las demás) y
   su recarga, con la fuente y lo que dice el juego; la restricción es la del objetivo de la API, y el slot lleva la
   fuente (otorga). Lo que publica Leads & Supports manda: si dice otra cosa, el build para; si dice lo mismo, lo de
   a mano sobra (aviso).
3. Derivación. Para cada variante sin liderazgo de Leads & Supports, cada parte de su Leader Skill da un slot si
   todo cierra: el objetivo con restricción conocida, la activación y cada efecto con su correspondencia y sus
   valores publicados (sin $TIME ni un marcador sin resolver). Si algo no cierra, ese slot no se deriva y se dice
   por qué: todo o nada por slot. Lo derivado lleva "src": "api" y el nombre de la skill (n); no lleva «Notable»
   (sig), que es una marca de thanosvibs que la API no tiene. La activación es el texto de Leads & Supports, o el
   de la API si va a mano.
4. Verificación. Lo mismo sobre las variantes con liderazgo de Leads & Supports: cada slot derivado contra el de
   Leads & Supports, en stats, valores, duración, condición, restricción, activación y recarga.
"""
import collections, re
from modelo import _mapeo

LIDERAZGOS = ('leader', 'leader2')
A_MANO = 'scripts/contenido/liderazgos_api.json'
TODOS, EL = 'All Allies', 'Self'
PRIMERO_Y_EL = 'All Allies for the first effect, Self for the second effect'
# La fuente mete la condición de entrada dentro del objetivo, con un «\n» literal (una barra y una n).
AL_ENTRAR = re.compile(r'^(.+)\\nActivates when: (.+) enters$')
OTORGA = 'Give Power'
# Lo que el texto de un efecto nombra y la API puede no publicar: el marcador y el campo que lo trae.
SIN_PUBLICAR = (('$TIME', 'd'), ('$TICK', 't'))
# El marcador de una facción, un tipo, una raza o una habilidad: en el patrón, su número es otro '#'.
MARCADOR = re.compile(r'\$HERO(?:SUBTYPE|CLASS)#')

# Por qué un slot no se deriva. {d} es el detalle de cada caso.
MOTIVOS = {
    'sin_skill': 'la API de skills no trae su Leader Skill',
    'etapas': 'la Leader Skill tiene {d} etapas',
    'vacia': 'la Leader Skill no trae efectos',
    'objetivo': 'la API no dice a quiénes llega («{d}»)',
    'partes': 'la Leader Skill da {d} partes y Leads & Supports tiene dos slots de liderazgo',
    'otorga': 'otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME)',
    'valor': 'la API no publica un valor: {d}',
    'efecto': f'un efecto sin stat (no se aprende de Leads & Supports ni está en {A_MANO}): {{d}}',
    'contradiccion': 'Leads & Supports publica distinto, en otras variantes, {d}',
    'activacion': f'una activación sin correspondencia (no se aprende de Leads & Supports ni está en {A_MANO}): «{{d}}»',
    'condicion': 'la condición de cada efecto de este objetivo no tiene correspondencia con Leads & Supports: «{d}»',
}


# Lo mismo, corto, para contar.
ROTULOS = {
    'sin_skill': 'sin Leader Skill', 'etapas': 'más de una etapa', 'vacia': 'sin efectos', 'objetivo': 'objetivo sin nombre',
    'partes': 'más de dos partes', 'otorga': '«Give Power»', 'valor': 'valor sin publicar',
    'efecto': 'efecto sin stat', 'contradiccion': 'contradicción de Leads & Supports',
    'activacion': 'activación sin correspondencia', 'condicion': 'condición sin correspondencia',
}


def motivo_txt(m, d):
    return MOTIVOS[m].format(d=d)


def _num(x):
    return int(x) if float(x).is_integer() else x


def _texto(patron, nums):
    """Un patrón de la API (descripción o activación) con sus números en lugar de cada '#'."""
    vals = list(nums or [])
    return re.sub('#', lambda m: str(_num(vals.pop(0))) if vals else '#', patron)


def _g(x):
    return f'{x:g}'


def fx_txt(g):
    """Un efecto de un liderazgo, para los informes: «All Basic Attacks +30%», «Remove All Debuffs (12 s)»."""
    v = g.get('v')
    t = g['s'] + (f" {'+' if v > 0 else '−'}{_g(abs(v))}%" if isinstance(v, (int, float)) else '')
    entre = [x for x in (f"{_g(g['d'])} s" if g.get('d') is not None else '', g.get('c') or '') if x]
    return t + (f" ({', '.join(entre)})" if entre else '')


def r_txt(r):
    return f'{r[0]}: {r[1]}' if r else 'ninguna'


def slot_txt(x):
    """Un slot de liderazgo, en una línea: sus efectos y, si los tiene, a quiénes llega, la activación y la recarga."""
    extra = [f"para {r_txt(x['r'])}" if x.get('r') else '', x.get('ac') or '',
             f"recarga {_g(x['cd'])} s" if x.get('cd') else '']
    extra = [e for e in extra if e]
    return ', '.join(fx_txt(g) for g in _fx_ls(x)) + (f" — {', '.join(extra)}" if extra else '')


def efecto_txt(f, T):
    """Un efecto de la API, para los informes: «Increases all Basic Attacks by 30%» (ALL BASIC ATTACKS INCREASE)."""
    return f"«{_texto(T['desc'][f['p']]['en'], f.get('v'))}» ({T['ab'][f['a']]['en']})"


def clave(f, T):
    """Un efecto de la API como se aprende su correspondencia: su etiqueta, su texto (con '#' en cada número) y el
    valor de su marcador ($HEROSUBTYPE1), si lo trae."""
    return (T['ab'][f['a']]['en'], T['desc'][f['p']]['en'], f.get('g'))


def _valores(f, T):
    """Los números del texto de un efecto que son valores, [(lugar en f['v'], número)]: todos menos el del marcador
    ($HEROSUBTYPE1), que es parte de su nombre."""
    trozos = T['desc'][f['p']]['en'].split('#')
    return [(k, n) for k, n in enumerate(f.get('v') or []) if not trozos[k].endswith(('$HEROSUBTYPE', '$HEROCLASS'))]


def sin_publicar(f, T):
    """Lo que el texto de un efecto nombra y la API no publica: $TIME sin duración, $TICK sin intervalo o un
    marcador sin valor ($HEROSUBTYPE1)."""
    patron = T['desc'][f['p']]['en']
    faltan = [m for m, campo in SIN_PUBLICAR if m in patron and f.get(campo) is None]
    if MARCADOR.search(patron) and not f.get('g'):
        faltan.append(re.search(r'\$HERO(?:SUBTYPE|CLASS)\d*', _texto(patron, f.get('v'))).group(0))
    return faltan


def _restriccion(objetivo, T, nombre):
    """(True, restricción) de un objetivo, o (False, None) si no se sabe a quiénes llega."""
    if objetivo == TODOS:
        return True, None
    if objetivo == EL:
        return True, ['Character', nombre]
    fila = next((f for f in T['tgt'] if f['en'] == objetivo), None)
    if fila is not None and 'r' in fila:
        return True, list(fila['r'])
    return False, None


def partes(sk, T, nombre):
    """La Leader Skill en las partes que van a cada slot de liderazgo, en orden: ([{'efectos': [(i, efecto)], 'r',
    'ac', 'act', 'av', 'cd', 'otorga', 'al_entrar'}], None), o (None, (motivo, detalle)) si no se puede partir. i es
    el lugar del efecto en la etapa; ac, el texto de la activación, que es la fila act de T['act'] con los números
    av; al_entrar, el objetivo «Activates when», si lo es."""
    if len(sk['st']) != 1:
        return None, ('etapas', str(len(sk['st'])))
    st = sk['st'][0]
    if not st['fx']:
        return None, ('vacia', '')
    tg = T['tgt'][st['tg']]['en'] if st.get('tg') is not None else ''
    fx = list(enumerate(st['fx']))
    if tg == PRIMERO_Y_EL:
        if len(fx) != 2:
            return None, ('objetivo', f'{tg}, con {len(fx)} efectos')
        grupos, al_entrar = [(fx[:1], None), (fx[1:], ['Character', nombre])], None
    else:
        m = AL_ENTRAR.match(tg)
        ok, r = _restriccion(m.group(1) if m else tg, T, nombre)
        if not ok:
            return None, ('objetivo', tg or 'sin objetivo')
        grupos, al_entrar = [(fx, r)], (tg if m else None)
    antes, otorgan = [], []
    for efs, r in grupos:
        i = next((j for j, (_, f) in enumerate(efs) if T['ab'][f['a']]['en'] == OTORGA), len(efs))
        if efs[:i]:
            antes.append({'efectos': efs[:i], 'r': r, 'otorga': False})
        if efs[i:]:
            otorgan.append({'efectos': efs[i:], 'r': r, 'otorga': True})
    ps = antes + otorgan
    if len(ps) > len(LIDERAZGOS):
        return None, ('partes', str(len(ps)))
    ac = _texto(T['act'][st['ac']]['en'], st.get('av')) if st.get('ac') is not None else None
    for x in ps:
        x.update(ac=ac, act=st.get('ac'), av=st.get('av'), cd=sk['cd'] or None, al_entrar=al_entrar)
    return ps, None


def _fx_ls(x):
    """Los efectos de un slot de Leads & Supports con su duración: la propia o la del slot (como los lee la app)."""
    return [dict(g, d=x['d']) if 'd' not in g and 'd' in x else g for g in x['fx']]


def _alinear(efectos, fx, T):
    """Los efectos de una parte con los de su slot de Leads & Supports, en orden: [(i, efecto, [efectos de Leads &
    Supports])], o None si no cierran. Un efecto con valores da uno de Leads & Supports por valor, con ese número
    (con o sin signo); uno sin valores, uno sin valor. La duración la publican los dos o ninguno."""
    out, j = [], 0
    for i, f in efectos:
        vals = [n for _, n in _valores(f, T)]
        gs = fx[j:j + max(len(vals), 1)]
        if len(gs) < max(len(vals), 1):
            return None
        if vals:
            if any(not isinstance(g.get('v'), (int, float)) or abs(g['v']) != n for g, n in zip(gs, vals)):
                return None
        elif 'v' in gs[0]:
            return None
        if any(('d' in g) != ('d' in f) for g in gs):
            return None
        out.append((i, f, gs))
        j += len(gs)
    return out if j == len(fx) else None


def _plantilla(f, gs, T):
    """Lo que da un efecto de la API según Leads & Supports: por stat, de qué número de su texto sale su valor (el
    lugar en f['v']) y con qué signo. La duración es la del efecto, si la publica (_alinear pide que la publiquen
    los dos)."""
    vals = _valores(f, T)
    return tuple((g['s'], (vals[k][0], -1 if g['v'] < 0 else 1) if vals else None) for k, g in enumerate(gs))


def _aprender(P, sop, T):
    """Las observaciones de cada correspondencia en las variantes con liderazgo de Leads & Supports:
    {'efectos': {clave: [(retrato, slot, plantilla)]}, 'activaciones': {texto de la API: [(retrato, slot, texto de
    Leads & Supports)]}, 'condiciones': {objetivo: [(retrato, slot, condición de cada efecto)]}}."""
    obs = {k: collections.defaultdict(list) for k in ('efectos', 'activaciones', 'condiciones')}
    for p in sorted(P):
        ps, _ = P[p]
        e = sop.get(p) or {}
        if ps is None:
            continue
        for x, k in zip(ps, LIDERAZGOS):
            if k not in e or x['otorga']:
                continue
            al = _alinear(x['efectos'], _fx_ls(e[k]), T)
            if al is None:
                continue
            for _, f, gs in al:
                obs['efectos'][clave(f, T)].append((p, k, _plantilla(f, gs, T)))
            if x['ac'] is not None:
                obs['activaciones'][x['ac']].append((p, k, e[k].get('ac')))
            # La condición la trae el texto de la API («Activates when»); de Leads & Supports sale su texto, de las
            # variantes en que la publica en todos los efectos (Drax — Classic y Annihilation no la publican: la
            # verificación lo lista como diferencia).
            if x['al_entrar']:
                cs = [{g.get('c') for g in gs} for _, _, gs in al]
                if all(len(c) == 1 and None not in c for c in cs):
                    obs['condiciones'][x['al_entrar']].append((p, k, tuple(c.pop() for c in cs)))
    return obs


def _tabla(obs):
    """De las observaciones: {clave: valor} con las que coinciden todas, y las contradicciones: {clave: {valor:
    [retratos]}}."""
    tabla, contra = {}, {}
    for k, xs in obs.items():
        vals = {}
        for p, _, v in xs:
            vals.setdefault(v, []).append(p)
        if len(vals) == 1:
            tabla[k] = next(iter(vals))
        else:
            contra[k] = vals
    return tabla, contra


def validar(manual, T, cat):
    """Lista de problemas de las correspondencias a mano (A_MANO; vacía si está bien): cada efecto, con su etiqueta y
    su texto como los publica la API y un solo número (el valor), da un stat del catálogo (soporte) que el catálogo
    clasifica con los mismos efectos que a él; cada activación es un texto de la API; nada se repite. T: las tablas
    de la API (MFF_TABLAS); cat: el catálogo de efectos (contenido/catalogo.json)."""
    if set(manual) != {'nota', 'efectos', 'activaciones', 'otorga'}:
        return ['lleva nota, efectos, activaciones y otorga']
    mal = [] if isinstance(manual['nota'], str) and manual['nota'] else ['la nota es un texto']
    etiquetas, textos, activaciones = ({f['en'] for f in T[k]} for k in ('ab', 'desc', 'act'))
    vistos = set()
    for e in manual['efectos']:
        if set(e) != {'ab', 'desc', 'stat'}:
            mal.append(f'efecto {e}: lleva ab, desc y stat')
            continue
        d = f"efecto «{e['desc']}» ({e['ab']})"
        if (e['ab'], e['desc']) in vistos:
            mal.append(f'{d}: repetido')
        vistos.add((e['ab'], e['desc']))
        if e['ab'] not in etiquetas:
            mal.append(f'{d}: la API no tiene esa etiqueta')
        if e['desc'] not in textos:
            mal.append(f'{d}: la API no tiene ese texto')
        if e['desc'].count('#') != 1 or MARCADOR.search(e['desc']):
            mal.append(f'{d}: el texto tiene que traer un solo número, el valor, y ningún marcador')
        m = _mapeo(cat, e['ab'], e['desc'])
        if e['stat'] not in cat['soporte']:
            mal.append(f"{d}: «{e['stat']}» no es un stat del catálogo (soporte)")
        elif m is None:
            mal.append(f'{d}: el catálogo no lo clasifica')
        elif m['efectos'] != cat['soporte'][e['stat']]['efectos']:
            mal.append(f"{d}: el catálogo lo clasifica como {m['efectos']} y a «{e['stat']}», como "
                       f"{cat['soporte'][e['stat']]['efectos']}")
    mal += [f'activación «{a}»: la API no tiene ese texto' for a in manual['activaciones'] if a not in activaciones]
    mal += [f'activación «{a}»: repetida' for a, n in collections.Counter(manual['activaciones']).items() if n > 1]
    for o in manual['otorga']:
        d = f"el «Give Power» de {o.get('p')}"
        if not {'p', 'skill', 'fx', 'fuente', 'juego'} <= set(o) <= {'p', 'skill', 'ac', 'cd', 'fx', 'fuente', 'juego'}:
            mal.append(f'{d}: lleva p, skill, fx, fuente y juego, y puede llevar ac y cd')
            continue
        if not all(isinstance(o[k], str) and o[k] for k in ('p', 'skill', 'juego')):
            mal.append(f'{d}: p, skill y juego son textos')
        if not (isinstance(o['fuente'], list) and o['fuente'] and all(isinstance(k, str) for k in o['fuente'])):
            mal.append(f'{d}: fuente es una lista de fuentes (contenido/guia.json)')
        if 'ac' in o and (o['ac'] not in activaciones or '#' in o['ac']):
            mal.append(f"{d}: la activación «{o['ac']}» tiene que ser un texto de la API sin números")
        if 'cd' in o and not (isinstance(o['cd'], (int, float)) and o['cd'] > 0):
            mal.append(f'{d}: la recarga es un número de segundos')
        if not (isinstance(o['fx'], list) and o['fx']):
            mal.append(f'{d}: fx es la lista de lo que otorga')
            continue
        for g in o['fx']:
            if not (isinstance(g, dict) and 's' in g and set(g) <= {'s', 'v', 'd'}
                    and all(isinstance(g[k], (int, float)) for k in ('v', 'd') if k in g)):
                mal.append(f'{d}: cada efecto lleva su stat (s) y puede llevar valor (v) y duración (d): {g}')
            elif g['s'] not in cat['soporte']:
                mal.append(f"{d}: «{g['s']}» no es un stat del catálogo (soporte)")
    mal += [f'el «Give Power» de {p}: repetido' for p, n in collections.Counter(o.get('p') for o in manual['otorga']).items()
            if n > 1]
    return mal


def _a_mano(manual, C, P, T, skill_de):
    """Las correspondencias a mano (A_MANO, ya validadas) al lado de las aprendidas C: ({'efectos': {clave:
    plantilla}, 'activaciones': {texto de la API}, 'otorga': {retrato: lo que otorga su «Give Power»}}, {'efectos':
    [[etiqueta, texto, stat, variantes]], 'activaciones': [[texto, variantes]], 'otorga': [[retrato, skill, fuente,
    juego]], 'avisos': [...]}), con las variantes que lo tienen en la Leader Skill. Un efecto da su stat con el número
    de su texto (el único). Lo que publica Leads & Supports manda: si da otra cosa para un efecto de acá, o se
    contradice, el build para; si da lo mismo, lo de acá sobra (aviso), como lo que ninguna Leader Skill tiene. Lo que
    otorga un «Give Power» vale para el retrato cuya Leader Skill tiene ese nombre y una parte «Give Power»; si no, sobra
    (aviso). skill_de: el nombre de la Leader Skill de cada retrato."""
    tabla, contra = C['efectos']
    efectos = {(e['ab'], e['desc'], None): ((e['stat'], (0, 1)),) for e in manual['efectos']}
    usan_fx, usan_ac = collections.defaultdict(set), collections.defaultdict(set)
    for p, (ps, _) in P.items():
        for x in ps or []:
            for _, f in x['efectos']:
                usan_fx[clave(f, T)].add(p)
            if x['act'] is not None:
                usan_ac[T['act'][x['act']]['en']].add((p, x['ac']))
    mal, avisos = [], []
    for k, pl in efectos.items():
        d = f'el efecto «{k[1]}» ({k[0]})'
        if k in contra:
            mal.append(f'{d}: Leads & Supports lo publica, distinto en distintas variantes')
        elif k in tabla and tabla[k] != pl:
            mal.append(f"{d}: Leads & Supports da {', '.join(s for s, _ in tabla[k])}, no {pl[0][0]}")
        elif k in tabla:
            avisos.append(f'{d}: Leads & Supports lo publica igual, sobra')
        elif not usan_fx[k]:
            avisos.append(f'{d}: ninguna Leader Skill lo tiene, sobra')
    for a in manual['activaciones']:
        if not usan_ac[a]:
            avisos.append(f'la activación «{a}»: ninguna Leader Skill la tiene, sobra')
        elif all(t in C['activaciones'][0] for _, t in usan_ac[a]):
            avisos.append(f'la activación «{a}»: Leads & Supports publica todas las de ese texto, sobra')
    if mal:
        raise SystemExit(f'{A_MANO} no coincide con Leads & Supports:\n  ' + '\n  '.join(mal))
    otorga = {}
    for o in manual['otorga']:
        d = f"el «Give Power» de {o['p']} ({o['skill']})"
        ps = P[o['p']][0] if o['p'] in P else None
        if o['p'] not in P:
            avisos.append(f'{d}: no es un retrato de los datos, sobra')
        elif skill_de.get(o['p']) != o['skill']:
            avisos.append(f"{d}: su Leader Skill se llama «{skill_de.get(o['p'])}», sobra")
        elif not any(x['otorga'] for x in ps or []):
            avisos.append(f'{d}: su Leader Skill no tiene una parte «Give Power» que se pueda derivar, sobra')
        else:
            otorga[o['p']] = o
    informe = {'efectos': [[k[0], k[1], pl[0][0], len(usan_fx[k])] for k, pl in efectos.items()],
               'activaciones': [[a, len({p for p, _ in usan_ac[a]})] for a in manual['activaciones']],
               'otorga': [[o['p'], o['skill'], o['fuente'], o['juego']] for o in otorga.values()],
               'avisos': avisos}
    return {'efectos': efectos, 'activaciones': set(manual['activaciones']), 'otorga': otorga}, informe


def _activacion(texto, patron, C, M):
    """(La activación de un slot derivado, None) o (None, (motivo, detalle)): el texto de Leads & Supports que se
    aprende para el de la API (texto, con sus números) o, si va a mano (patron, el texto de la API con '#'), el de la
    API."""
    tabla, contra = C['activaciones']
    if texto in tabla:
        return tabla[texto], None
    if texto in contra:
        return None, ('contradiccion', f'la activación «{texto}»')
    if patron in M['activaciones']:
        return texto, None
    return None, ('activacion', texto)


def _otorgado(x, nombre_skill, R, C, M):
    """El slot de una parte «Give Power» cuyo contenido dice el juego (R, de A_MANO): la restricción, la del objetivo de
    la API; los efectos, la activación y la recarga, los de R; y la fuente, en otorga. O (None, [(motivo, detalle)])."""
    ac = None
    if 'ac' in R:
        ac, mal = _activacion(R['ac'], R['ac'], C, M)
        if mal:
            return None, [mal]
    out = {'n': nombre_skill} if nombre_skill else {}
    if x['r'] is not None:
        out['r'] = x['r']
    if ac is not None:
        out['ac'] = ac
    if R.get('cd'):
        out['cd'] = R['cd']
    out['fx'] = [dict(g) for g in R['fx']]
    out['src'] = 'api'
    out['otorga'] = list(R['fuente'])
    return out, None


def _slot(x, nombre_skill, T, C, M, R=None):
    """El slot de una parte, con las correspondencias aprendidas C y las de a mano M, o (None, [(motivo, detalle)]):
    todo o nada. R: lo que otorga el «Give Power» de la parte, si lo dice el juego (A_MANO)."""
    if x['otorga']:
        return _otorgado(x, nombre_skill, R, C, M) if R is not None else (None, [('otorga', '')])
    tabla = {k: C[k][0] for k in C}
    contra = {k: C[k][1] for k in C}
    mal = []
    ac = None
    if x['ac'] is not None:
        # El texto de Leads & Supports; si va a mano, el de la API.
        ac, m = _activacion(x['ac'], T['act'][x['act']]['en'], C, M)
        if m:
            mal.append(m)
    cond = None
    if x['al_entrar']:
        cond = tabla['condiciones'].get(x['al_entrar'])
        if cond is None:
            mal.append(('contradiccion', f"la condición de cada efecto de «{x['al_entrar']}»")
                       if x['al_entrar'] in contra['condiciones'] else ('condicion', x['al_entrar']))
    fx = []
    for i, f in x['efectos']:
        faltan = sin_publicar(f, T)
        if faltan:
            mal.append(('valor', f"{', '.join(faltan)} en {efecto_txt(f, T)}"))
            continue
        k = clave(f, T)
        if k in contra['efectos']:
            mal.append(('contradiccion', f'el efecto {efecto_txt(f, T)}'))
            continue
        # La aprendida o la de a mano: no se pisan (_a_mano).
        plantilla = tabla['efectos'].get(k, M['efectos'].get(k))
        if plantilla is None:
            mal.append(('efecto', efecto_txt(f, T)))
            continue
        for s, val in plantilla:
            g = {'s': s}
            if val is not None:
                g['v'] = _num(f['v'][val[0]] * val[1])
            if 'd' in f:
                g['d'] = f['d']
            if cond is not None and i < len(cond) and cond[i] is not None:
                g['c'] = cond[i]
            fx.append(g)
    if mal:
        return None, mal
    out = {'n': nombre_skill} if nombre_skill else {}
    if x['r'] is not None:
        out['r'] = x['r']
    if ac is not None:
        out['ac'] = ac
    if x['cd']:
        out['cd'] = x['cd']
    out['fx'] = fx
    out['src'] = 'api'
    return out, None


def _comparar(der, ls):
    """En qué difiere un slot derivado del de Leads & Supports (lo derivado / Leads & Supports)."""
    def efs(x):
        return [(g['s'], g.get('v'), g.get('d'), g.get('c')) for g in _fx_ls(x)]
    dif = []
    if der.get('r') != ls.get('r'):
        dif.append(f"restricción: {r_txt(der.get('r'))} / {r_txt(ls.get('r'))}")
    if der.get('ac') != ls.get('ac'):
        dif.append(f"activación: {der.get('ac') or 'ninguna'} / {ls.get('ac') or 'ninguna'}")
    if der.get('cd') != ls.get('cd'):
        dif.append(f"recarga: {_g(der['cd']) + ' s' if der.get('cd') else 'ninguna'} / "
                   f"{_g(ls['cd']) + ' s' if ls.get('cd') else 'ninguna'}")
    if efs(der) != efs(ls):
        dif.append(f"efectos: {', '.join(fx_txt(g) for g in _fx_ls(der))} / {', '.join(fx_txt(g) for g in _fx_ls(ls))}")
    return dif


def derivar(sop, skills, T, nombres, manual):
    """Los liderazgos de la Leader Skill de la API para las variantes sin liderazgo de Leads & Supports.

    sop: los soportes de Leads & Supports tal como los publica (fuentes.soportes(), o MFF_SOPORTES sin lo
    derivado); skills y T: las skills de la API y sus tablas (MFF_SKILLS y MFF_TABLAS); nombres: el personaje de
    cada retrato (para la restricción «Self»), con todas las variantes; manual: las correspondencias a mano (A_MANO,
    validadas con validar()). Para con SystemExit si Leads & Supports dice otra cosa que lo de a mano.

    Devuelve {'derivados': {retrato: {slot: liderazgo}}, 'sin_derivar': [{'p', 'slot', 'motivos'}] (de las
    variantes sin liderazgo de Leads & Supports), 'verificacion': [{'p', 'slot', 'estado', 'dif' o 'motivos'}] (de
    las que lo tienen: 'igual', 'distinto', 'sin_derivar', 'solo_ls' si Leads & Supports publica un slot que la
    Leader Skill no da aparte, o 'solo_api' al revés), 'correspondencia' y 'contradicciones' (lo aprendido, para el
    informe), 'a_mano' (lo de a mano que se usa y sus avisos) y 'textos' (la traducción de cada activación de lo
    derivado que va con el texto de la API, de T['act'], o None si no la tiene)}."""
    P, skill_de = {}, {}
    for p, nombre in nombres.items():
        sk = next((s for s in skills.get(p, []) if s['sl'] == 'Leader Skill'), None)
        P[p] = (None, ('sin_skill', '')) if sk is None else partes(sk, T, nombre)
        skill_de[p] = T['name'][sk['n']]['en'] if sk is not None and sk['n'] is not None else None
    obs = _aprender(P, sop, T)
    C = {k: _tabla(v) for k, v in obs.items()}
    M, a_mano = _a_mano(manual, C, P, T, skill_de)
    derivados, sin_derivar, verificacion, textos, mal_ls = {}, [], [], {}, []
    for p in sorted(P):
        ps, problema = P[p]
        e = sop.get(p) or {}
        con_ls = any(k in e for k in LIDERAZGOS)
        nombre_skill = skill_de[p]
        for i, k in enumerate(LIDERAZGOS):
            if ps is None:
                if not con_ls and i == 0:
                    sin_derivar.append({'p': p, 'slot': k, 'motivos': [list(problema)]})
                elif con_ls and k in e:
                    verificacion.append({'p': p, 'slot': k, 'estado': 'sin_derivar', 'motivos': [list(problema)]})
                continue
            if i >= len(ps):
                if con_ls and k in e:
                    verificacion.append({'p': p, 'slot': k, 'estado': 'solo_ls'})
                continue
            R = M['otorga'].get(p) if ps[i]['otorga'] else None
            der, mal = _slot(ps[i], nombre_skill, T, C, M, R)
            if R is not None and con_ls:
                # Leads & Supports publica el liderazgo de la variante: manda.
                if k in e and der is not None and _comparar(der, e[k]):
                    mal_ls.append(f"el «Give Power» de {p}: Leads & Supports publica {slot_txt(e[k])}, no {slot_txt(der)}")
                else:
                    a_mano['avisos'].append(f'el «Give Power» de {p}: Leads & Supports publica el liderazgo de la variante, '
                                            'sobra')
            if not con_ls:
                if der is None:
                    sin_derivar.append({'p': p, 'slot': k, 'motivos': [list(x) for x in mal]})
                else:
                    derivados.setdefault(p, {})[k] = der
                    if 'ac' in der:
                        texto = R['ac'] if R is not None else ps[i]['ac']
                        if texto not in C['activaciones'][0]:     # a mano: el texto de la API, con su traducción
                            fila = (next(f for f in T['act'] if f['en'] == R['ac']) if R is not None
                                    else T['act'][ps[i]['act']])
                            es = fila.get('es')
                            textos[der['ac']] = _texto(es, None if R is not None else ps[i]['av']) if es else None
            elif k not in e:
                verificacion.append({'p': p, 'slot': k, 'estado': 'solo_api'} if der is not None else
                                    {'p': p, 'slot': k, 'estado': 'solo_api', 'motivos': [list(x) for x in mal]})
            elif der is None:
                verificacion.append({'p': p, 'slot': k, 'estado': 'sin_derivar', 'motivos': [list(x) for x in mal]})
            else:
                dif = _comparar(der, e[k])
                verificacion.append({'p': p, 'slot': k, 'estado': 'distinto', 'dif': dif} if dif else
                                    {'p': p, 'slot': k, 'estado': 'igual'})
    if mal_ls:
        raise SystemExit(f'{A_MANO} no coincide con Leads & Supports:\n  ' + '\n  '.join(mal_ls))
    def variantes(k, c):
        return len({p for p, _, _ in obs[k][c]})
    correspondencia = {
        'efectos': [[list(c), [list(x) for x in v], variantes('efectos', c)]
                    for c, v in sorted(C['efectos'][0].items(), key=lambda kv: str(kv[0]))],
        'activaciones': [[c, v, variantes('activaciones', c)] for c, v in sorted(C['activaciones'][0].items())],
        'condiciones': [[c, list(v), variantes('condiciones', c)] for c, v in sorted(C['condiciones'][0].items())],
    }
    contradicciones = {
        'efectos': [[list(c), [[[list(x) for x in v], ps] for v, ps in vals.items()]] for c, vals in sorted(C['efectos'][1].items(), key=lambda kv: str(kv[0]))],
        'activaciones': [[c, [[v, ps] for v, ps in vals.items()]] for c, vals in sorted(C['activaciones'][1].items())],
        'condiciones': [[c, [[list(v), ps] for v, ps in vals.items()]] for c, vals in sorted(C['condiciones'][1].items())],
    }
    return {'derivados': derivados, 'sin_derivar': sin_derivar, 'verificacion': verificacion,
            'correspondencia': correspondencia, 'contradicciones': contradicciones, 'a_mano': a_mano,
            'textos': dict(sorted(textos.items()))}
