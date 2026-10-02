#!/usr/bin/env python3
"""Bonos de equipo (Team Bonus): llevar ciertos personajes juntos les sube stats a todos los del
equipo. El juego lo explica así en su guía: «When the Characters in your Team have a special
relationship, it will activate a Team Bonus» (docs/MODELO.md, «Lo que muestran las pantallas del
juego»).

thanosvibs no los publica. La wiki de Future Fight, sí: en la página de cada personaje, la sección
Team Bonus trae cada bono con su nombre, los íconos de sus 2 o 3 integrantes y sus stats,
redondeados a un decimal. Un mismo bono aparece en la página de cada integrante, y la wiki la edita
la comunidad: hay erratas en los stats («Cooldwon Duration») y en los nombres, flechas al revés y
páginas que dicen otros valores u otros stats. Por eso:
- Un bono es un conjunto de integrantes; el nombre no sirve para juntarlos, porque tiene erratas.
- Su nombre y sus stats son los de la mayoría de sus páginas. Si empatan, van todas las versiones
  empatadas (la app las muestra) y docs/AUDITORIA.md las lista.
- Los stats se escriben con los nombres de Leads & Supports de thanosvibs, los mismos con los que
  la sinergia de la app decide a quién le sirve cada efecto («All Attack» de la wiki es «All Basic
  Attacks», como lo llama el juego). La recarga y la duración de control siempre bajan, aunque la
  página ponga la flecha al revés: la wiki las escribe con ↓ en casi todas sus apariciones.
- Un stat que no está en STATS («Critical Defense», «Physical Damage») va como lo escribe la wiki:
  la app lo muestra sin clasificar y lo cuenta para todos, como a un efecto de soporte nuevo, y la
  auditoría lo lista.
- Lo que no se puede leer (un ícono que no es de ningún personaje, una línea de stat rota) no se
  adivina: esa página no cuenta para ese bono y la auditoría lo dice.

Lo que se ve en el juego va en scripts/contenido/bonos.json (de las capturas de la pantalla Team
Bonus) y manda sobre la wiki: los bonos de los personajes que la wiki todavía no tiene, o los que tiene
mal. La auditoría dice si la wiki decía otra cosa.

Lo usa fuentes.py: los bonos van a la app (MFF_BONOS) y lo que no cierra, a docs/AUDITORIA.md."""
import collections, re, unicodedata

# Nombre del stat en la wiki (con sus erratas) -> nombre de Leads & Supports (thanosvibs). Los que
# Leads & Supports no usa van con el nombre de la wiki.
STATS = {
    'All Basic Attacks': ('All Attack', 'All Attacks', 'All attack', 'All Basic Attack', 'All Basic Attacks',
                          'All Basic Attack Increase', 'All Basic Attacks Increase', 'All Basic Attacks Increse'),
    'Physical Attack': ('Physical Attack', 'Physical Attack Attack'),
    'Energy Attack': ('Energy Attack', 'Energy  Attack'),
    'Attack Speed': ('Attack Speed', 'Attacks Speed', 'Attack Speedd'),
    'Movement Speed': ('Movement Speed', 'Moovement Speed'),
    'All Speeds': ('All Speed',),
    'Critical Rate': ('Critical Rate', 'Critical rate', 'Criticl Rate', 'Critical Rage', 'Critical Rate Rate'),
    'Critical Damage': ('Critical Damage',),
    'Ignore Defense': ('Ignore Defense', 'Ingore Defense', 'Ignore Defence', 'Defense Penetration'),
    'HP': ('Max HP', 'Max Hp', 'Mac HP', 'MAX HP'),
    'Dodge': ('Dodge',),
    'Recovery Rate': ('Recovery Rate',),
    'All Basic Defenses': ('All Defense', 'All Defenses', 'All Defence', 'All Deense', 'All Basic Defenses',
                           'All Basic Defenses Increase'),
    'Physical Defense': ('Physical Defense', 'Physical Defence', 'Physical Defebse'),
    'Energy Defense': ('Energy Defense', 'Energy Defence'),
    'Skill Cooldown': ('Cooldown Duration', 'Cooldown Time', 'Cooldown Time Duration', 'Cooldwon Duration', 'Cooldown TIme'),
    'Crowd Control Time': ('Crowd Control Time', 'Crownd Control Time'),
    'Fire Resist': ('Fire Resist',),
    'Cold Resist': ('Cold Resist',),
    'Lightning Resist': ('Lightning Resist',),
    'Mind Resist': ('Mind Resist',),
}
_STAT = {w: s for s, ws in STATS.items() for w in ws}
BAJAN = {'Skill Cooldown', 'Crowd Control Time'}
# Íconos de la wiki cuyo nombre no es el del personaje en thanosvibs (sin espacios ni signos).
ICONOS = {'Hellstrom': 'Hellstorm', 'HulkAmadeusChoIconHulkAmadeusCho': 'Hulk (Amadeus Cho)',
          'Hulkbuster': 'Hulkbuster (Iron Man Mark 44)', 'RocketRacoon': 'Rocket Raccoon', 'Sabertooth': 'Sabretooth',
          'SharonCarter': 'Captain America (Sharon Rogers)', 'SharonRogers': 'Captain America (Sharon Rogers)',
          'Syvie': 'Sylvie', 'ThTheThingIconing': 'The Thing'}

_ICONO = re.compile(r'\[\[(?:Image|File):\s*([^|\]]+?)Icon\s*\.png\s*(?:\|\s*(\d+)px)?[^\]]*\]\]')
# Una línea de stat: «*Energy Attack ↑ +5.4%», «''Ignore Defense 4.8%''», «*Max HP ↑ +5.1».
_LINEA_STAT = re.compile(r"^[*'\s]*([A-Za-z][A-Za-z .'/()-]*?)\s*[↑↓]?\s*[+-]?(\d+(?:\.\d+)?)\s*%*[*'¨\s]*$")
# Fin de la sección: la pestaña siguiente («|-|»), el cierre de las pestañas o la sección siguiente.
_FIN = re.compile(r'\n\|-\||</tabber>|\n==[^=]|\{\{CharacterNav')
# Los íconos de la línea de integrantes van a 100 o 120 px; los de «X 2 Bonuses», a 50.
_PX_INTEGRANTES = 80


def _norm(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', s.lower())


def seccion(wt):
    """La sección Team Bonus de una página, sin su título; None si no tiene."""
    i = wt.find('Team Bonus')
    if i < 0:
        return None
    i = wt.find('\n', i)
    m = _FIN.search(wt, i)
    return wt[i:m.start() if m else len(wt)]


def _sin_formato(linea):
    """Una línea sin el formato de lista, negrita o celda de tabla («| class="header1" |Nombre»)."""
    return re.sub(r"^[|!*'\s]*(?:[a-z]+=\"[^\"]*\"\s*)*\|?\s*|['\s]+$", '', linea)


def _es_nombre(linea):
    """¿La línea puede ser el nombre de un bono? No lo es un stat, una línea de íconos, un título,
    una tabla que empieza o termina, ni el «X 2 Bonuses» del bono anterior."""
    return not (_LINEA_STAT.match(linea) or _ICONO.search(linea) or linea.startswith(('=', '{|', '|}'))
                or 'X 2 Bonus' in linea)


def entradas(sec):
    """Los bonos de una sección, como los escribe la página: [{'nombre', 'iconos', 'stats',
    'rotas'}]. nombre: None si la página no lo escribe; stats: [(stat de la wiki, valor)]; rotas:
    las líneas de stat que no se pudieron leer."""
    # Un <br /> corta la línea; si ya la cortaba un salto, no agrega una vacía.
    lineas = [l.strip() for l in re.sub(r'<br\s*/?>[ \t]*\n?', '\n', sec).split('\n')]
    out = []
    for k, linea in enumerate(lineas):
        iconos = [m.group(1) for m in _ICONO.finditer(linea) if not m.group(2) or int(m.group(2)) >= _PX_INTEGRANTES]
        if len(iconos) < 2:
            continue
        # El nombre: la línea anterior, salteando las vacías y los separadores de fila de tabla.
        j = k - 1
        while j >= 0 and _sin_formato(lineas[j]) in ('', '-'):
            j -= 1
        nombre = _sin_formato(lineas[j]) if j >= 0 and _es_nombre(lineas[j]) else None
        # Los stats: las líneas que siguen, hasta una vacía, el «X 2 Bonuses» o el fin de la fila.
        stats, rotas = [], []
        for s in [_ICONO.sub('', linea).strip()] + lineas[k + 1:]:
            if s in ('', '|'):
                if stats or rotas:
                    break
                continue
            if 'X 2 Bonus' in s or s.startswith(('!', '|-', '|}', '=', '----')) or _ICONO.search(s):
                break
            m = _LINEA_STAT.match(s)
            if m:
                stats.append((m.group(1).strip(), float(m.group(2))))
            elif re.search(r'[↑↓%]', s):
                rotas.append(s)
            else:
                break       # el nombre del bono siguiente, sin una línea vacía en el medio
        out.append({'nombre': nombre, 'iconos': iconos, 'stats': stats, 'rotas': rotas})
    return out


def _version(stats):
    """Los stats de un bono con los nombres de Leads & Supports (o el de la wiki, si no está en
    STATS) y la recarga y la duración de control en negativo."""
    return tuple((_STAT.get(s, s), -v if _STAT.get(s) in BAJAN else v) for s, v in stats)


def bonos(paginas, nombres, juego):
    """Los bonos de equipo y lo que no cierra.

    paginas: los wikitexts de los personajes ({'name': nombre en thanosvibs, 'wt'}); nombres: los
    nombres de los personajes en thanosvibs; juego: los bonos de scripts/contenido/bonos.json
    ({'nombre', 'integrantes', 'stats', 'fuente'}, con los stats como los escribe el juego).
    Devuelve {'bonos': [{'n': nombre, 'm': [integrantes], 'v': [versión, ...], 'f': [fuentes]}],
    'auditoria': {...}}. Cada versión es [[stat, valor], ...], con la recarga y la duración de
    control en negativo; hay más de una solo si las páginas de la wiki empatan. El nombre es None si
    ninguna página lo escribe, y lleva los empatados separados por « / »."""
    nombres = set(nombres)
    del_juego = {}
    for j in juego:
        clave = frozenset(j['integrantes'])
        if (len(clave) != len(j['integrantes']) or not 2 <= len(clave) <= 3 or clave - nombres
                or any(st not in _STAT for st, _ in j['stats']) or clave in del_juego):
            raise SystemExit(f"scripts/contenido/bonos.json: «{j['nombre']}» tiene integrantes que no son 2 o 3 "
                             f"personajes distintos de thanosvibs, un stat que no está en STATS (scripts/bonos.py) "
                             f"o los mismos integrantes que otro bono: {j['integrantes']}, {j['stats']}")
        del_juego[clave] = j
    por_norm = {_norm(n): n for n in nombres}

    def personaje(icono):
        n = ICONOS.get(icono) or por_norm.get(_norm(icono))
        return n if n in nombres else None

    sin_seccion, ilegibles = [], []
    desconocidos = collections.defaultdict(list)   # stat que no está en STATS -> páginas que lo escriben
    votos = collections.defaultdict(dict)          # integrantes -> {página: (nombre, versión)}
    dobles = set()                                 # (integrantes, página) con dos versiones en la página
    for d in paginas:
        sec = seccion(d['wt'])
        if sec is None:
            sin_seccion.append(d['name'])
            continue
        for e in entradas(sec):
            integrantes = [personaje(i) for i in e['iconos']]
            motivo = None
            if None in integrantes:
                motivo = 'ícono sin personaje: ' + ', '.join(i for i, x in zip(e['iconos'], integrantes) if x is None)
            elif len(set(integrantes)) != len(integrantes) or d['name'] not in integrantes:
                motivo = 'integrantes: ' + ', '.join(integrantes)
            elif e['rotas'] or not e['stats']:
                motivo = 'stat ilegible: ' + (' | '.join(e['rotas']) or 'no tiene stats')
            if motivo:
                ilegibles.append({'pagina': d['name'], 'bono': e['nombre'], 'motivo': motivo})
                continue
            for s, _ in e['stats']:
                if s not in _STAT:
                    desconocidos[s].append(d['name'])
            voto = (e['nombre'], _version(e['stats']))
            clave = frozenset(integrantes)
            if votos[clave].get(d['name'], voto) != voto:
                dobles.add((clave, d['name']))
            votos[clave][d['name']] = voto
    for clave, pagina in sorted(dobles, key=lambda x: (sorted(x[0]), x[1])):
        del votos[clave][pagina]
        ilegibles.append({'pagina': pagina, 'bono': None, 'motivo': 'trae dos veces el bono de ' + ', '.join(sorted(clave))
                          + ', distinto'})
    con_seccion = {d['name'] for d in paginas} - set(sin_seccion)
    out, empates, mayorias, nombres_empatados, falta_en_pagina, contra_wiki = [], [], [], [], [], []
    for clave in sorted({c for c in votos if votos[c]} | set(del_juego), key=lambda c: (len(c), sorted(c))):
        paginas_de, integrantes = votos.get(clave, {}), sorted(clave)
        if clave in del_juego:
            j = del_juego[clave]
            de_la_wiki = sorted({tuple(sorted(v)) for _, v in paginas_de.values()})
            contra_wiki.append({'nombre': j['nombre'], 'integrantes': integrantes,
                                'wiki': [[list(x) for x in v] for v in de_la_wiki],
                                'nombres_wiki': sorted({n for n, _ in paginas_de.values() if n})})
            out.append({'n': j['nombre'], 'm': integrantes, 'v': [[list(x) for x in _version(j['stats'])]],
                        'f': j['fuente']})
            continue
        # Dos páginas con los mismos stats en otro orden dicen lo mismo.
        por_version = collections.defaultdict(list)
        for p, (_, v) in sorted(paginas_de.items()):
            por_version[tuple(sorted(v))].append((p, v))
        ranking = sorted(por_version.values(), key=lambda ps: -len(ps))
        ganadoras = [ps for ps in ranking if len(ps) == len(ranking[0])]
        if len(ranking) > 1:
            (empates if len(ganadoras) > 1 else mayorias).append(
                {'integrantes': integrantes, 'versiones': [[ps[0][1], [p for p, _ in ps]] for ps in ranking]})
        votos_nombre = collections.Counter(n for n, _ in paginas_de.values() if n)
        tope = max(votos_nombre.values(), default=0)
        empatados = sorted(n for n, c in votos_nombre.items() if c == tope)
        if len(empatados) > 1:
            nombres_empatados.append({'integrantes': integrantes, 'nombres': empatados})
        falta_en_pagina += [{'pagina': i, 'integrantes': integrantes} for i in integrantes
                            if i in con_seccion and i not in paginas_de]
        out.append({'n': ' / '.join(empatados) or None, 'm': integrantes,
                    'v': [[list(x) for x in ps[0][1]] for ps in ganadoras], 'f': ['wiki-bonos']})
    return {'bonos': out, 'auditoria': {
        'paginas': len(con_seccion), 'sin_seccion': sorted(sin_seccion), 'ilegibles': ilegibles,
        'desconocidos': {s: sorted(ps) for s, ps in sorted(desconocidos.items())},
        'empates': empates, 'mayorias': mayorias, 'nombres_empatados': nombres_empatados,
        'falta_en_pagina': falta_en_pagina, 'juego': contra_wiki}}
