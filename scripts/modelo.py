#!/usr/bin/env python3
"""Modelo del juego (docs/MODELO.md): lo que se deduce de cada variante (un personaje con un
uniforme) a partir de sus datos, en un solo lugar. La app y los scripts lo leen de acá en vez
de calcularlo cada uno por su lado.

Etapa 1, perfil de combate: con qué pega cada retrato, según el daño de sus skills activas
(las cinco y la de Tier-3 o Trascendido; la Striker no, que no la usa él):
- esc: de qué ataque sale el % de daño (ataque físico, de energía o la vida), con su parte
  del total en %, de mayor a menor. Según la guía de thanosvibs (parte 3), un personaje
  escala con un solo ataque, que es el que se construye; el tipo de daño de cada skill no lo
  cambia (una skill puede hacer daño de energía sobre el ataque físico).
- tip: los tipos de daño de sus skills, físico y/o de energía (importa contra los reflejos y
  en las etapas que solo reciben uno).
- ele: los elementos de su daño (fuego, frío, rayo, veneno, mente). Un buff de un elemento
  solo le sirve a quien hace daño de ese elemento (guía, parte 3).
- res: los elementos cuya resistencia le sube el daño, de su artefacto o de su Striker
  (segun_resistencia). Un liderazgo o un soporte de resistencias solo le sirve a quien la tiene.

Etapa 2, lo que hace cada variante con sus skills (analisis): cada efecto de cada skill,
clasificado con el catálogo (scripts/contenido/catalogo.json), con a quién le llega (a él, al
equipo y a qué aliados, al rival o a sus invocaciones), desde qué skills, con qué condición y,
si es para él, si le sirve. De ahí salen también sus roles (roles), que no existen en el juego:
qué le aporta al equipo.

Lo usa _core.py para data.js (MFF_PERFIL y MFF_ANALISIS, por retrato, y los roles de cada
personaje y uniforme)."""
import json, math, re


def perfil(skills, desc):
    """{'esc': [[ataque, %], ...], 'tip': [...], 'ele': [...]} de un set de skills de la API
    (formato de work/skills_parsed.json); desc es la tabla de patrones de efecto, que trae en
    cada patrón de daño la posición del % (pi), el ataque del que sale (src) y el tipo con su
    elemento (elem, "Energy Fire")."""
    escala, tipos, elementos = {}, set(), set()
    for sk in skills:
        if not sk['sl'].startswith('Active'):
            continue
        for st in sk.get('st') or []:
            for f in st.get('fx') or []:
                d = desc[f['p']] if f.get('p') is not None else None
                v = f.get('v')
                if d is None or 'pi' not in d or not v or d['pi'] >= len(v) or not v[d['pi']]:
                    continue
                escala[d['src']] = escala.get(d['src'], 0) + v[d['pi']]
                tipo, *elem = d['elem'].split(' ')
                tipos.add(tipo)
                if elem:
                    elementos.add(elem[0])
    total = sum(escala.values())
    return {'esc': [[src, math.floor(n * 100 / total + 0.5)] for src, n in sorted(escala.items(), key=lambda x: -x[1])],
            'tip': sorted(tipos), 'ele': sorted(elementos)}


# Daño según la resistencia: el artefacto exclusivo lo escribe «Increases Cold Damage by [P1]% of
# Cold Resist» (thanosvibs, /api/artifacts).
_SEGUN_RESISTENCIA = re.compile(r'Increases (Fire|Cold|Lightning|Poison|Mind) Damage by \[P\d+\]% of \1 Resist')


def segun_resistencia(skills, ab, ele, artefacto):
    """Elementos cuya resistencia le sube el daño (res del perfil). Según Ezequiel, los liderazgos y
    soportes de resistencias solo le sirven a quien tiene esa mejora. Sale de dos lugares:
    - su artefacto exclusivo (artefacto: sus líneas de texto, o None), lo que dice que es para él
      («Applies to: Self»). El de Robbie Reyes es para los aliados con la habilidad Llama: depende de
      que él esté en el equipo, así que no entra en el perfil de nadie;
    - la Element Conversion de su Striker (Ghost Rider, Hades): la fuente trae el elemento como un
      código sin resolver («Increases 1 damage by 10% of 1 Resistance»), así que vale el de su daño
      (ele). ab es la tabla de etiquetas de efecto."""
    res = set()
    para_el = False
    for linea in artefacto or []:
        linea = re.sub(r'^(&emsp;)+', '', linea)       # la sangría de la fuente
        if linea.startswith('Applies to:'):
            para_el = linea == 'Applies to: Self'
            continue
        m = _SEGUN_RESISTENCIA.search(linea)
        if m and para_el:
            res.add(m.group(1))
    if any(ab[f['a']]['en'] == 'ELEMENT CONVERSION' for sk in skills if sk['sl'] == 'Striker Skill'
           for st in sk.get('st') or [] for f in st.get('fx') or []):
        res.update(ele)
    return sorted(res)


# ---- Etapa 2: lo que hace cada variante con sus skills ----------------------------------
# Destino de un efecto: a él, al equipo, al rival o a sus invocaciones.
EL, EQUIPO, RIVAL, INVOCACION = 'e', 'q', 'r', 'i'
_ORDEN_DESTINO = {EL: 0, EQUIPO: 1, RIVAL: 2, INVOCACION: 3}


def _mapeo(cat, etiqueta, patron):
    """Cómo clasifica el catálogo un efecto (etiqueta y patrón de su texto), o None si no lo
    clasifica (scripts/catalogo.py lo avisa y la auditoría lo lista)."""
    m = cat['skills'].get(etiqueta)
    if m is None:
        return None
    return m['por_patron'].get(patron) if 'por_patron' in m else m


def _destino(para, etapa, j, tgt):
    """A quién le llega el efecto j de una etapa, y a qué aliados (el objetivo de la etapa,
    índice en la tabla de objetivos) si es al equipo. Lo que se le aplica al rival va al rival
    aunque la etapa tenga objetivo: es lo que otorga «Give Power» (sus golpes aplican
    sangrado). Sin objetivo, lo propio es para él; las de liderazgo siempre lo traen."""
    if para == 'rival':
        return RIVAL, None
    if 'tg' not in etapa:
        return EL, None
    texto = tgt[etapa['tg']]['en']
    # Dos objetivos de la fuente traen la condición de activación pegada como "\\n".
    if texto == 'Self' or texto.startswith('Self\\n'):
        return EL, None
    if texto == 'Summoned Character':
        return INVOCACION, None
    if texto.startswith('All Allies for the first effect'):
        return (EQUIPO, _indice(tgt, 'All Allies')) if j == 0 else (EL, None)
    return EQUIPO, etapa['tg']


def _indice(tgt, texto):
    return next(i for i, x in enumerate(tgt) if x['en'] == texto)


def le_sirve(regla, perfil, efectos, skills):
    """¿Le sirve a la variante un efecto con esta regla del catálogo (sirve)? efectos: los ids
    de catálogo de todo lo que hace, con su destino; skills: sus skills."""
    if regla in ('todos', 'propio'):
        return True
    tipo, _, valor = regla.partition(':')
    if tipo == 'escala':
        return valor in {src for src, _ in perfil['esc']}
    if tipo == 'elemento':
        return bool(perfil['ele']) if valor == '*' else valor in perfil['ele']
    if tipo == 'tipo':
        return valor in perfil['tip']
    if regla == 'aplica_debuffs':
        return any(d == RIVAL and g in ('control', 'debilitar', 'continuo') for _, d, g in efectos)
    if regla == 'invoca':
        return any(e == 'invocar' for e, _, _ in efectos)
    # La definitiva de Tier-3 se carga con la barra (la fuente la publica sin recarga); la de
    # los Trascendidos tiene recarga de verdad.
    if regla == 'definitiva':
        return any(sk['sl'] == 'Active Ult' and not sk['cd'] for sk in skills)
    if regla == 'striker':
        return any(sk['sl'] == 'Striker Skill' for sk in skills)
    raise SystemExit(f'regla de «le sirve» del catálogo que el modelo no sabe evaluar: {regla!r} (scripts/modelo.py)')


def analisis(skills, tablas, cat, perfil):
    """Lo que hace una variante con sus skills, efecto por efecto.

    fx: [efecto, destino, objetivo, fuentes], en el orden del catálogo y por destino. efecto:
      índice en cat['efectos']; destino: 'e' (él), 'q' (equipo), 'r' (rival), 'i' (sus
      invocaciones); objetivo: si es al equipo, el índice del objetivo en la tabla de objetivos
      (qué aliados), si no None; fuentes: [skill, etapa, efecto] de cada aparición, índices en
      sus skills. Las fuentes de una entrada comparten la condición del catálogo (contra quién,
      cómo varía o cuánto dura).
    ns: índices de fx de lo que es para él pero no le sirve (un buff de fuego sin daño de fuego).
    sc: fuentes de lo que el catálogo no clasifica (thanosvibs agregó una etiqueta).
    El daño de los golpes no va: es el perfil de combate. «Give Power» es un envoltorio (lo que
    otorga viene después, en la misma etapa o en las que siguen); va solo si no le sigue nada,
    porque entonces la fuente no dice qué otorga."""
    ab, desc, tgt = tablas['ab'], tablas['desc'], tablas['tgt']
    idx = {e['id']: i for i, e in enumerate(cat['efectos'])}
    grupo = {e['id']: e['grupo'] for e in cat['efectos']}
    entradas, sin_clasificar = {}, []
    for si, sk in enumerate(skills):
        etapas = sk.get('st') or []
        for ti, etapa in enumerate(etapas):
            fx = etapa.get('fx') or []
            for fi, f in enumerate(fx):
                m = _mapeo(cat, ab[f['a']]['en'], desc[f['p']]['en'])
                if m is None:
                    sin_clasificar.append([si, ti, fi])
                    continue
                d, objetivo = _destino(m['para'], etapa, fi, tgt)
                cond = json.dumps(m.get('condicion'), sort_keys=True)
                for e in m['efectos']:
                    if e == 'golpe':
                        continue
                    if e == 'otorga' and (fx[fi + 1:] or any(x.get('fx') for x in etapas[ti + 1:])):
                        continue
                    entradas.setdefault((e, d, objetivo, cond), []).append([si, ti, fi])
    claves = sorted(entradas, key=lambda k: (_ORDEN_DESTINO[k[1]], idx[k[0]], k[2] if k[2] is not None else -1, k[3]))
    fx = [[idx[e], d, objetivo, entradas[(e, d, objetivo, cond)]] for e, d, objetivo, cond in claves]
    efectos = [(e, d, grupo[e]) for e, d, _, _ in claves]
    ns = [i for i, (e, d, objetivo, cond) in enumerate(claves)
          if d == EL and not le_sirve(cat['efectos'][idx[e]]['sirve'], perfil, efectos, skills)]
    out = {'fx': fx}
    if ns:
        out['ns'] = ns
    if sin_clasificar:
        out['sc'] = sin_clasificar
    return out


# Roles: no existen en el juego. Dicen qué le aporta la variante al equipo (Ezequiel, 2 de
# octubre de 2026): Soporte, le da algo a sus aliados fuera del liderazgo; Tanque, provoca o le
# baja al equipo el daño que recibe; Control, le aplica al rival tres o más controles
# distintos; Daño, todos.
ROLES = ('Control', 'Soporte', 'Tanque', 'Daño')
CONTROLES_PARA_ROL = 3


def roles(an, skills, cat):
    ids = [e['id'] for e in cat['efectos']]
    grupo = {e['id']: e['grupo'] for e in cat['efectos']}
    r = []
    controles = {ids[e] for e, d, _, _ in an['fx'] if d == RIVAL and grupo[ids[e]] == 'control' and ids[e] != 'provocar'}
    if len(controles) >= CONTROLES_PARA_ROL:
        r.append('Control')
    if any(d == EQUIPO and any(skills[si]['sl'] != 'Leader Skill' for si, _, _ in fuentes) for _, d, _, fuentes in an['fx']):
        r.append('Soporte')
    if any(ids[e] == 'provocar' or (d == EQUIPO and grupo[ids[e]] == 'reduccion') for e, d, _, _ in an['fx']):
        r.append('Tanque')
    r.append('Daño')
    return r
