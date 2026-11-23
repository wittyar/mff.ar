#!/usr/bin/env python3
"""Los cromos de cómic (#35; Ezequiel, 17 de noviembre de 2026: «Arma un modulo sobre cromos donde pongas todos los cromos
con sus caractaristicas»), para MFF_CROMOS.

Salen de work/cards.json (thanosvibs, /api/cards, con lo propio de fuentes/propio/cromos.json encima: propio.py), que trae
cada cromo como {id, name, type, img, stat1, …, stat6}: stat1 y stat2 son las opciones fijas; stat3 a stat6, las cinco
opciones posibles de cada grado (3★ a 6★), salvo en los Premium, donde stat3 es una tercera fija y los grados son 4★ a
6★. Una opción «<stat> Proc (<cuándo>)» es una activación.

Los valores, las colecciones, de dónde sale cada uno y su nombre del juego en español salen de las tablas del juego según
mffguide.fyi (fuentes/mffguide/cromos.json; Ezequiel, 23 de noviembre de 2026: «Dale con todo»), una sola tabla para todos:
las fijas por calidad (1 a 7) de un cromo 6★, el valor de cada casilla (3 a 6) y el efecto propio (probabilidad, cuánto,
cuántos segundos y recarga). Un cromo se empareja con el de la guía por su nombre (sin mirar mayúsculas) o por
contenido/cromos.json (mffguide.nombres). thanosvibs sigue mandando donde ya hay dato: lo que la guía dice distinto (las
opciones de una casilla, el stat o el cuándo de la activación) va en dif del cromo y en la auditoría, y sin los datos de la
guía que no le corresponden (la activación). Los cromos que la guía tiene y thanosvibs no, entran con los datos de la guía
(mg). Los de War of Kings (propios, de la nota del 17 de noviembre de 2026) tienen que coincidir con la guía en todo lo que
dice la nota (opciones, valores a la máxima calidad, activación y colección): si no, corta el build; la nota queda como
fuente de sus valores y de su colección.

Cómo se lee cada texto, cada cuándo y cada tipo: scripts/contenido/cromos.json; lo que no está ahí corta el build. Los
nombres de los stats: los de guia.json (stats) y, los que no están ahí, los de cromos.json (nombres); j, cómo lo escribe el
juego en el cromo (la guía).

cruce(cards) empareja con la guía y dice qué difiere (también para la auditoría); armar(cards, guia_stats) devuelve
(MFF_CROMOS, imágenes):
  stats {clave: {es, en, j?: {es, en}}}, cuando {id: {es, en}}, tipos [{id, es, en}],
  valores {calidad [7 valores, fijas de un 6★ por calidad 1 a 7], casilla {'3'..'6': %}, act {prob, dur, rec}, f (fuentes)},
  obtencion {código: {es, en}},
  cromos [{id, n (nombre de thanosvibs o, si no lo publica, el de la guía en inglés), es (nombre del juego en español, o
           null), t (tipo o null), td (true si la fuente lo publica como dudoso), p (premium: tres fijas y grados 4★ a 6★),
           img (clave de la imagen o null), fijas [{s, cal?: true (según la calidad), v?: % fijo}], grados {'3'..'6': [{s} |
           {s, act}]}, vf (fuentes de los valores, o null si no hay), act ({prob, v, dur, txt {es, en}, cu {es, en}}: el
           efecto propio con el texto del juego), col (id de la colección o null), obt ({o, cl, te, sp, mc}: código de
           obtención, clase normal/limitado/exclusivo, cristales de la Tienda de envío, Selector premium, misión de creación),
           dif ([{k: 'casilla'|'act'|'fijas'|'premium', g?, tv, mg}]: lo que la guía dice distinto), mg (true: solo en la
           guía), pr (fuentes, si es propio), sc (sin confirmar), nota ({es, en}, de la fuente propia)}],
  colecciones [{id, n {es, en}, cromos (ids), premio {s, v}, f (fuentes)}]
Solo biblioteca estándar."""
import json, os, re

_DIR = os.path.dirname(os.path.abspath(__file__))
PROC = re.compile(r'^(.+) Proc \((when [a-z]+)\)$')
NOTA = ['foro-1897819', 'cafe-3190031']   # la nota de War of Kings, la de los cromos propios


def cargar(*partes):
    with open(os.path.join(*partes), encoding='utf-8') as f:
        return json.load(f)


def _llano(n):
    return re.sub(r'\s+', ' ', n).strip().upper()


def guia():
    """La fuente de mffguide y cómo se lee (contenido/cromos.json, mffguide)."""
    return cargar(_DIR, '..', 'fuentes', 'mffguide', 'cromos.json'), cargar(_DIR, 'contenido', 'cromos.json')


def cruce(cards):
    """Empareja los cromos de work/cards.json con los de la guía y compara. Devuelve {pares {nombre: cromo de la guía},
    solo_guia [cromos de la guía], sin_guia [nombres], dif {nombre: [diferencias]}, mal [lo que no cierra]}."""
    M, C = guia()
    L = C['mffguide']
    mal = []
    gpor = {_llano(g['en']): g for g in M['cromos']}

    def stat_g(i, donde):
        k = L['stats'].get(str(i))
        if k is None:
            mal.append(f'{donde}: el stat {i} de la guía no está en contenido/cromos.json (mffguide.stats)')
        return k

    def stat_tv(texto, donde):
        m = PROC.match(texto)
        if m:
            c = C['cuando'].get(m.group(2))
            return ('act', C['stats'].get(m.group(1).upper()), c and c['id'])
        k = C['stats'].get(texto.upper())
        if k is None:
            mal.append(f'{donde}: el stat «{texto}» no está en contenido/cromos.json')
        return k

    pares, sin_guia, dif = {}, [], {}
    for c in cards:
        g = gpor.get(_llano(L['nombres'].get(c['name'], c['name'])))
        if g is None:
            if c['name'] in L['nombres']:
                mal.append(f"contenido/cromos.json (mffguide.nombres): {c['name']} → {L['nombres'][c['name']]}, que la guía no tiene")
            sin_guia.append(c['name'])
            continue
        if any(x is g for x in pares.values()):
            mal.append(f"el cromo de la guía {g['en']} empareja con dos cromos")
        pares[c['name']] = g
        donde = f"cromo {c['name']}"
        d = []
        prem = es_premium(c, C)
        if prem != g['premium']:
            d.append({'k': 'premium', 'tv': prem, 'mg': g['premium']})
        nf = 3 if prem else 2
        tv_f = [stat_tv(c['stat' + str(i)], donde) for i in range(1, nf + 1)]
        mg_f = [stat_g(s, donde) for s, _ in g['fijas']]
        if tv_f != mg_f:
            d.append({'k': 'fijas', 'tv': tv_f, 'mg': mg_f})
        for k, ops in g['casillas'].items():
            tv_o = [stat_tv(t, donde) for t in c.get('stat' + k) or []]
            tv_s = sorted(o for o in tv_o if not isinstance(o, tuple) and o)
            mg_s = sorted(stat_g(s, donde) or '' for s in ops if s != 'efecto')
            if tv_s != mg_s or sum(isinstance(o, tuple) for o in tv_o) != ops.count('efecto'):
                d.append({'k': 'casilla', 'g': k, 'tv': [o if not isinstance(o, tuple) else 'act' for o in tv_o],
                          'mg': [stat_g(s, donde) if s != 'efecto' else 'act' for s in ops]})
        tv_a = [o for k in ('3', '4', '5', '6') for o in [stat_tv(t, donde) for t in (c.get('stat' + k) if isinstance(c.get('stat' + k), list) else [])]
                if isinstance(o, tuple)]
        mg_a = efecto(g, L, mal, donde)
        if [a[1:] for a in tv_a] != [(mg_a['s'], mg_a['cuando'])]:
            d.append({'k': 'act', 'tv': [list(a[1:]) for a in tv_a], 'mg': [mg_a['s'], mg_a['cuando']]})
        if d:
            dif[c['name']] = d
    usados = {id(g) for g in pares.values()}
    solo_guia = [g for g in M['cromos'] if id(g) not in usados]
    return {'pares': pares, 'solo_guia': solo_guia, 'sin_guia': sin_guia, 'dif': dif, 'mal': mal}


def es_premium(c, C):
    """Premium: tres fijas y grados 4★ a 6★. thanosvibs lo dice en el tipo; uno propio sin tipo, por su forma."""
    t = C['dudosos'].get(c['type'], c['type'])
    return t == 'Premium' if t is not None else not isinstance(c['stat3'], list)


def efecto(g, L, mal, donde):
    """El efecto propio de un cromo de la guía: stat y cuándo (por sus textos en inglés), probabilidad, cuánto y segundos."""
    e = g['efecto']
    s = next((k for t, k in L['efectos'] if t in e['en']), None)
    cu = L['cuando'].get(e['cuando_en'])
    v = re.search(r'(\d+(?:\.\d+)?)%', e['en'])
    dur = re.search(r'\((\d+) s\)', e['en'])
    prob = re.search(r'^(\d+)%', e['cuando_en'])
    if s is None or cu is None or not (v and dur and prob):
        mal.append(f'{donde}: el efecto propio «{e["en"]}» / «{e["cuando_en"]}» no se lee con contenido/cromos.json (mffguide)')
        return {'s': s, 'cuando': cu}
    return {'s': s, 'cuando': cu, 'prob': float(prob.group(1)), 'v': float(v.group(1)), 'dur': float(dur.group(1)),
            'txt': {'es': e['es'], 'en': e['en']}, 'cu': {'es': e['cuando_es'], 'en': e['cuando_en']}}


def _num(x):
    return int(x) if float(x).is_integer() else x


def armar(cards, guia_stats):
    M, C = guia()
    L = C['mffguide']
    P = cargar(_DIR, '..', 'fuentes', 'propio', 'cromos.json')
    propios = {p['name']: p for p in P['cromos']}
    X = cruce(cards)
    mal = list(X['mal'])
    V = M['valores']
    tope = V['fijas_6e_por_calidad'][-1]

    def stat(texto, donde):
        k = C['stats'].get(texto.upper())
        if k is None:
            mal.append(f'{donde}: el stat «{texto}» no está en contenido/cromos.json')
        return k

    def opcion(texto, donde):
        m = PROC.match(texto)
        if not m:
            return {'s': stat(texto, donde)}
        cuando = C['cuando'].get(m.group(2))
        if cuando is None:
            mal.append(f'{donde}: la activación «{texto}» no dice cuándo como contenido/cromos.json')
            return {'s': None}
        return {'s': stat(m.group(1), donde), 'act': cuando['id']}

    def de_guia(x, g, donde, fuentes):
        """Lo que la guía agrega a un cromo: nombre en español, valores, efecto propio, colección y obtención."""
        x['es'] = g['es']
        x['vf'] = fuentes
        sin_dif = {d['k'] for d in x['dif']}
        if 'fijas' not in sin_dif:
            for f, (_, v) in zip(x['fijas'], g['fijas']):
                if v == tope:
                    f['cal'] = True
                else:
                    f['v'] = _num(v)
        a = efecto(g, L, mal, donde)
        if 'act' not in sin_dif and 'prob' in a:
            x['act'] = {k: _num(a[k]) if isinstance(a[k], float) else a[k] for k in ('prob', 'v', 'dur', 'txt', 'cu')}
        x['col'] = None if g['coleccion'] is None else f"col{g['coleccion']}"
        x['obt'] = {'o': str(g['obtencion']), 'cl': g['clase'], 'te': g['tienda_envio'], 'sp': g['selector_premium'],
                    'mc': g['mision_creacion']}

    tipos = {x['id'] for x in C['tipos']}
    cromos, imagenes, por_guia = [], {}, {}
    for c in cards:
        donde = f"cromo {c['name']}"
        t = C['dudosos'].get(c['type'], c['type'])
        if t is not None and t not in tipos:
            mal.append(f'{donde}: tipo «{c["type"]}» desconocido')
        premium = es_premium(c, C)
        fijas = [c['stat1'], c['stat2']] + ([c['stat3']] if premium else [])
        grados = ('4', '5', '6') if premium else ('3', '4', '5', '6')
        if any(not isinstance(x, str) for x in fijas) or any(not isinstance(c['stat' + g], list) or len(c['stat' + g]) != 5 for g in grados):
            mal.append(f'{donde}: no tiene la forma de un cromo {"Premium" if premium else "no Premium"} (fijas y cinco opciones por grado)')
            continue
        x = {'id': str(c['id']), 'n': c['name'], 'es': None, 't': t, 'td': t != c['type'], 'p': premium,
             'img': ('cromo-' + str(c['id'])) if c['img'] else None,
             'fijas': [{'s': stat(s, donde)} for s in fijas],
             'grados': {g: [opcion(o, donde) for o in c['stat' + g]] for g in grados},
             'vf': None, 'col': None, 'obt': None, 'dif': X['dif'].get(c['name'], [])}
        if c['img']:
            imagenes['cromo-' + str(c['id'])] = f"images/cards/{c['img']}.png"
        g = X['pares'].get(c['name'])
        fuentes = ['mffguide']
        if '_propio' in c:
            # Lo propio: sus fuentes y lo que no confirman. Lo que dice la nota tiene que ser lo de la guía.
            prop = propios[c['name']]
            x['pr'], x['sc'] = prop['fuente'], prop.get('sin_confirmar', [])
            if 'nota' in prop:
                x['nota'] = prop['nota']
            if g is None:
                mal.append(f'{donde}: es propio y la guía no lo tiene: sus valores no tienen con qué confirmarse')
            else:
                if x['dif']:
                    mal.append(f'{donde}: la nota y la guía no dicen lo mismo: {x["dif"]}')
                val = c['valores']
                a = efecto(g, L, mal, donde)
                nota = ([v for _, v in g['fijas']],
                        {k: V['azar'][k] for k in grados}, (a.get('prob'), a.get('v'), a.get('dur')))
                suya = (val['fijas'], {k: val[k] for k in grados},
                        (val['activacion']['prob'], val['activacion']['v'], val['activacion']['dur']))
                if nota != suya:
                    mal.append(f'{donde}: los valores de la nota {suya} no son los de la guía {nota}')
                fuentes = ['mffguide'] + prop['fuente']
        if g is not None:
            de_guia(x, g, donde, fuentes)
            por_guia[g['id_juego']] = x['id']
        if x['dif']:
            print(f"AVISO: cromo {c['name']}: mffguide dice otra cosa (manda thanosvibs): {x['dif']}")
        cromos.append(x)
    for n in X['sin_guia']:
        print(f'AVISO: cromo {n}: mffguide no lo tiene (sin valores, colección ni obtención)')

    # Los que la guía tiene y thanosvibs no: entran con lo de la guía.
    firma = lambda x: (tuple(f['s'] for f in x['fijas']), tuple((g, tuple(sorted(str(o) for o in os_))) for g, os_ in sorted(x['grados'].items())))
    sin_guia = {firma(x): x['n'] for x in cromos if x['n'] in X['sin_guia']}
    for g in X['solo_guia']:
        donde = f"cromo {g['en']} (mffguide)"
        a = efecto(g, L, mal, donde)
        st = lambda i: L['stats'].get(str(i)) or mal.append(f'{donde}: el stat {i} no está en mffguide.stats')
        x = {'id': f"mg{g['id_juego']}", 'n': g['en'], 'es': None, 't': None, 'td': False, 'p': g['premium'], 'img': None,
             'fijas': [{'s': st(s)} for s, _ in g['fijas']],
             'grados': {k: [{'s': a['s'], 'act': a['cuando']} if s == 'efecto' else {'s': st(s)} for s in ops]
                        for k, ops in g['casillas'].items()},
             'vf': None, 'col': None, 'obt': None, 'dif': [], 'mg': True}
        if set(x['grados']) != ({'4', '5', '6'} if g['premium'] else {'3', '4', '5', '6'}):
            mal.append(f'{donde}: sus casillas no son las de un cromo {"premium" if g["premium"] else "no premium"}')
        if firma(x) in sin_guia:
            mal.append(f'{donde} es {sin_guia[firma(x)]} de thanosvibs con otro nombre: va en contenido/cromos.json (mffguide.nombres)')
        de_guia(x, g, donde, ['mffguide'])
        por_guia[g['id_juego']] = x['id']
        cromos.append(x)
    ids = [x['id'] for x in cromos]
    if len(set(ids)) != len(ids):
        mal.append('dos cromos con el mismo id: ' + ', '.join(sorted({i for i in ids if ids.count(i) > 1})))

    # Las colecciones, de la guía; la de War of Kings, también de la nota (tiene que decir lo mismo).
    colecciones = []
    for col in M['colecciones']:
        miembros = [por_guia[g['id_juego']] for g in M['cromos'] if g['coleccion'] == col['n']]
        x = {'id': f"col{col['n']}", 'n': {'es': col['es'], 'en': col['en']}, 'cromos': miembros,
             'premio': {'s': L['stats'].get(str(col['stat'])), 'v': _num(col['v'])}, 'f': ['mffguide']}
        if x['premio']['s'] is None:
            mal.append(f"colección {col['en']}: el stat {col['stat']} no está en mffguide.stats")
        colecciones.append(x)
    por_nombre = {x['n']: x['id'] for x in cromos}
    for pc in P['colecciones']:
        x = next((y for y in colecciones if _llano(y['n']['en']) == _llano(pc['nombre'])), None)
        suya = (sorted(por_nombre.get(n, n) for n in pc['cromos']), stat(pc['premio']['stat'], f"colección {pc['nombre']}"), pc['premio']['v'])
        if x is None or (sorted(x['cromos']), x['premio']['s'], x['premio']['v']) != suya:
            mal.append(f"colección {pc['nombre']} (propia): la guía no dice lo mismo ({x and (x['cromos'], x['premio'])} / {suya})")
        else:
            x['f'] = ['mffguide'] + pc['fuente']

    usados = {k for k in C['stats'].values()} | {o['s'] for x in cromos for g in x['grados'].values() for o in g} \
        | {f['s'] for x in cromos for f in x['fijas']} | {x['premio']['s'] for x in colecciones}
    usados.discard(None)
    juego = {L['stats'][i]: v for i, v in M['stats'].items() if i in L['stats']}
    faltan_stats = sorted(set(M['stats']) - set(L['stats']))
    if faltan_stats:
        mal.append(f'stats de la guía sin clave en contenido/cromos.json (mffguide.stats): {faltan_stats}')
    nombres = {}
    for k in sorted(usados):
        n = guia_stats.get(k) or C['nombres'].get(k)
        if n is None:
            mal.append(f'el stat {k} no tiene nombre en guia.json ni en contenido/cromos.json')
        else:
            nombres[k] = {'es': n['es'], 'en': n['en']}
            if k in juego:
                nombres[k]['j'] = juego[k]
    sobran = sorted(set(C['nombres']) - usados) + sorted(set(C['nombres']) & set(guia_stats))
    if sobran:
        mal.append(f'contenido/cromos.json: nombres que no se usan o que ya están en guia.json: {sobran}')
    if mal:
        raise SystemExit('Los cromos no cierran con scripts/contenido/cromos.json:\n- ' + '\n- '.join(mal))
    return ({'stats': nombres, 'cuando': {v['id']: {'es': v['es'], 'en': v['en']} for v in C['cuando'].values()},
             'tipos': C['tipos'],
             'valores': {'calidad': [_num(v) for v in V['fijas_6e_por_calidad']], 'casilla': {k: _num(v) for k, v in V['azar'].items()},
                         'act': {'prob': V['efecto']['prob'], 'dur': V['efecto']['dura_s'], 'rec': V['efecto']['enfria_s']},
                         'f': ['mffguide']},
             'obtencion': M['obtencion'],
             'cromos': cromos, 'colecciones': colecciones}, imagenes)
