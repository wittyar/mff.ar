#!/usr/bin/env python3
"""Los cromos de cómic (#35; Ezequiel, 17 de noviembre de 2026: «Arma un modulo sobre cromos donde pongas todos los cromos
con sus caractaristicas»), para MFF_CROMOS.

Salen de work/cards.json (thanosvibs, /api/cards, con lo propio de fuentes/propio/cromos.json encima: propio.py), que trae
cada cromo como {id, name, type, img, stat1, …, stat6}: stat1 y stat2 son las opciones fijas; stat3 a stat6, las cinco
opciones posibles de cada grado (3★ a 6★), salvo en los Premium, donde stat3 es una tercera fija y los grados son 4★ a
6★. Una opción «<stat> Proc (<cuándo>)» es una activación. thanosvibs no publica cuánto da cada opción: solo los cromos
propios traen valores (los de la nota, a la máxima calidad y grado).

Cómo se lee cada texto, cada cuándo y cada tipo: scripts/contenido/cromos.json; lo que no está ahí corta el build. Los
nombres de los stats: los de guia.json (stats) y, los que no están ahí, los de cromos.json (nombres).

armar(cards, guia_stats) devuelve (MFF_CROMOS, imágenes):
  stats {clave: {es, en}}, cuando {id: {es, en}}, tipos [{id, es, en}],
  cromos [{id, n (nombre), t (tipo o null), td (true si la fuente lo publica como dudoso), img (clave de la imagen o null),
           fijas [{s, v?}], grados {'3'..'6': [{s} | {s, act}]}, v ({grado: % de cada opción}, solo los propios),
           act ({prob, v, dur} de la activación, solo los propios), pr (fuentes, si es propio), sc (sin confirmar), nota ({es, en}, de la fuente propia)}],
  colecciones [{id, n, cromos (ids), grado, premio {s, v}, pr}]
Solo biblioteca estándar."""
import json, os, re

_DIR = os.path.dirname(os.path.abspath(__file__))
PROC = re.compile(r'^(.+) Proc \((when [a-z]+)\)$')


def cargar(*partes):
    with open(os.path.join(*partes), encoding='utf-8') as f:
        return json.load(f)


def armar(cards, guia_stats):
    C = cargar(_DIR, 'contenido', 'cromos.json')
    P = cargar(_DIR, '..', 'fuentes', 'propio', 'cromos.json')
    propios = {p['name']: p for p in P['cromos']}
    mal = []

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

    tipos = {x['id'] for x in C['tipos']}
    cromos, imagenes = [], {}
    for c in cards:
        donde = f"cromo {c['name']}"
        t = C['dudosos'].get(c['type'], c['type'])
        if t is not None and t not in tipos:
            mal.append(f'{donde}: tipo «{c["type"]}» desconocido')
        premium = t == 'Premium'
        fijas = [c['stat1'], c['stat2']] + ([c['stat3']] if premium else [])
        grados = ('4', '5', '6') if premium else ('3', '4', '5', '6')
        if any(not isinstance(x, str) for x in fijas) or any(not isinstance(c['stat' + g], list) or len(c['stat' + g]) != 5 for g in grados):
            mal.append(f'{donde}: no tiene la forma de un cromo {"Premium" if premium else "no Premium"} (fijas y cinco opciones por grado)')
            continue
        x = {'id': str(c['id']), 'n': c['name'], 't': t, 'td': t != c['type'],
             'img': ('cromo-' + str(c['id'])) if c['img'] else None,
             'fijas': [{'s': stat(s, donde)} for s in fijas],
             'grados': {g: [opcion(o, donde) for o in c['stat' + g]] for g in grados}}
        if c['img']:
            imagenes['cromo-' + str(c['id'])] = f"images/cards/{c['img']}.png"
        if '_propio' in c:
            # Lo propio: sus fuentes y lo que no confirman; los valores, de la nota.
            prop = propios[c['name']]
            x['pr'], x['sc'] = prop['fuente'], prop.get('sin_confirmar', [])
            val = c['valores']
            if len(val['fijas']) != len(fijas) or set(val) - {'fijas', 'activacion'} != set(grados):
                mal.append(f'{donde}: los valores no son los de sus fijas y sus grados')
                continue
            for f, v in zip(x['fijas'], val['fijas']):
                f['v'] = v
            x['v'] = {g: val[g] for g in grados}
            hay_act = any('act' in o for g in grados for o in x['grados'][g])
            if hay_act != ('activacion' in val):
                mal.append(f'{donde}: la activación y sus valores no van juntos')
            if 'activacion' in val:
                x['act'] = val['activacion']
            if 'nota' in prop:
                x['nota'] = prop['nota']
        cromos.append(x)
    ids = [x['id'] for x in cromos]
    if len(set(ids)) != len(ids):
        mal.append('dos cromos con el mismo id: ' + ', '.join(sorted({i for i in ids if ids.count(i) > 1})))

    # Las colecciones de lo propio (los cromos, por nombre).
    por_nombre = {x['n']: x['id'] for x in cromos}
    colecciones = []
    for col in P['colecciones']:
        faltan = [n for n in col['cromos'] if n not in por_nombre]
        if faltan:
            mal.append(f"colección {col['nombre']}: cromos que no están: {faltan}")
        colecciones.append({'id': col['id'], 'n': col['nombre'], 'cromos': [por_nombre.get(n) for n in col['cromos']],
                            'grado': col['grado'], 'premio': {'s': stat(col['premio']['stat'], f"colección {col['nombre']}"),
                                                              'v': col['premio']['v']}, 'pr': col['fuente']})

    usados = {k for k in C['stats'].values()}
    nombres = {}
    for k in sorted(usados):
        n = guia_stats.get(k) or C['nombres'].get(k)
        if n is None:
            mal.append(f'el stat {k} no tiene nombre en guia.json ni en contenido/cromos.json')
        else:
            nombres[k] = {'es': n['es'], 'en': n['en']}
    sobran = sorted(set(C['nombres']) - usados) + sorted(set(C['nombres']) & set(guia_stats))
    if sobran:
        mal.append(f'contenido/cromos.json: nombres que no se usan o que ya están en guia.json: {sobran}')
    if mal:
        raise SystemExit('Los cromos no cierran con scripts/contenido/cromos.json:\n- ' + '\n- '.join(mal))
    return ({'stats': nombres, 'cuando': {v['id']: {'es': v['es'], 'en': v['en']} for v in C['cuando'].values()},
             'tipos': C['tipos'], 'cromos': cromos, 'colecciones': colecciones}, imagenes)
