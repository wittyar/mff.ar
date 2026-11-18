#!/usr/bin/env python3
"""Objetos (1.0.56; Ezequiel, 18 de noviembre de 2026: «Arma un modulo para CTPs, donde este el detalle. Bendiciones de Odin,
Javis, Emblemas, Sets de Iso e ISOs»), para MFF_OBJETOS. El detalle de los C.T.P. va en MFF_CTPS (fuentes.ctps).

De dónde sale cada parte:
- Bendiciones de Odín: thanosvibs, /api/odins-blessings (work/odins.json): cada una con sus dos stats, color, forma y de
  dónde cae; los valores, por stat: [valor, bono de amplificación, total], como los muestra su página.
- Emblemas: thanosvibs, /api/emblems (work/emblems.json), con /api/emblems/static (en qué modo rige cada colección; su
  página lo lee de ahí) y /api/emblems/levels (estrellas y lo que cuesta cada nivel). flags: el tipo (Offensive o
  Defensive), «nores» (rige en todo el contenido) y cómo se consigue (las claves de static.farming).
- Sets de ISO-8: la tabla «ISO SET BONUS» de la página ISO-8 de la wiki (work/wiki_iso.json); thanosvibs no tiene API de
  ISO-8. Las piedras (color, nombre y stats) son las de la guía (contenido/guia.json, iso.piedras): la app las toma de ahí.
  Los sets que nombra la guía tienen que cerrar con la wiki pieza por pieza y stat por stat, y los de la leyenda de la guía
  de armado (guia_armado.LEY_ISO_SET) tienen que estar: la app lleva de su nombre a su detalle.
- J.A.R.V.I.S.: fuentes/objetos/jarvis.json (la nota oficial que lo introdujo, la del 14 de octubre de 2026 y la guía del
  juego; thanosvibs no lo publica).

Cómo se lee cada texto de las fuentes: scripts/contenido/objetos.json; uno que no está ahí corta el build, como un color de
ISO-8 sin piedra o una fuente citada que no está en guia.json.

armar(...) devuelve (MFF_OBJETOS, imágenes):
  stats {clave: {es, en}} (los nombres de todos los stats que se usan),
  odin {bendiciones [{id, n, color, forma, st [{s, v [valor, bono, total], u ('%' o '')}], drop ({es, en} o null), img}],
        colores, formas, notas},
  emblemas {rarezas [{id, es, en, color, duda?}], rarezas_fuente, tipos, obtencion, sin_restriccion,
            colecciones [{n, modo (id de modos.json)}],
            emblemas [{id, n, img, r, col (o null), s, tipo, libre, obt [claves], v [60 valores, del nivel 1 al 60]}],
            niveles [[estrellas, datos, kits, oro] del nivel 1 al 60], notas},
  iso {sets [{id, n, es, captura, piezas [piedras], st [{s, v, d?}], act [{es, en}]}], piedras_es, piedras_es_fuente, notas},
  jarvis (fuentes/objetos/jarvis.json: categorias, chips con id, ex_opciones, modos, notas, imagen_lista).
Solo biblioteca estándar."""
import json, os, re
from guia_armado import LEY_ISO_SET

_DIR = os.path.dirname(os.path.abspath(__file__))
_NUM = re.compile(r'^(.*?)\s*\+?(\d+(?:\.\d+)?)%$')


def cargar(*partes):
    with open(os.path.join(*partes), encoding='utf-8') as f:
        return json.load(f)


def tabla_sets_iso(wt):
    """Las filas de la tabla «ISO SET BONUS» de la wiki: [nombre, piezas, colores, stats, activación], como texto."""
    i = wt.index('== ISO SET BONUS ==')
    tabla = wt[i:wt.index('|}', i)]
    filas = []
    for f in tabla.split('\n|-\n')[1:]:
        celdas = [re.sub(r'^\s*colspan="\d+"\s*\|', '', c).strip() for c in re.split(r'\n\|', '\n' + f)[1:]]
        filas.append(celdas)
    return filas


def armar(odins, emblems, emb_static, emb_levels, wiki_iso, guia, cromos_nombres, modos):
    C = cargar(_DIR, 'contenido', 'objetos.json')
    J = cargar(_DIR, '..', 'fuentes', 'objetos', 'jarvis.json')
    fuentes, ids_modos = set(guia['fuentes']), {m['id'] for m in modos}
    mal, usados, imagenes = [], set(), {}

    def notas(lista, donde):
        for n in lista:
            for f in n['f']:
                if f not in fuentes:
                    mal.append(f'{donde}: la fuente {f} no está en contenido/guia.json')
        return lista

    # Bendiciones de Odín.
    O = C['odin']
    for st in odins['stats']:
        if st not in O['stats']:
            mal.append(f'Odín: el stat «{st}» no está en contenido/objetos.json')

    def valores(st):
        vals = odins['stats'][st]
        u = {'%' if isinstance(x, str) and x.endswith('%') else '' for x in vals}
        if len(vals) != 3 or len(u) != 1:
            mal.append(f'Odín: los valores de «{st}» no son [valor, bono, total] con la misma unidad: {vals}')
            return [], ''
        u = u.pop()
        return [float(x[:-1]) if u else x for x in vals], u

    bendiciones = []
    for b in odins['blessings']:
        donde = f"bendición de Odín {b['name']}"
        st = []
        for s in (b['stat1'], b['stat2']):
            if s not in odins['stats'] or s not in O['stats']:
                mal.append(f'{donde}: el stat «{s}» no tiene valores o no está en contenido/objetos.json')
                continue
            v, u = valores(s)
            st.append({'s': O['stats'][s], 'v': v, 'u': u})
            usados.add(O['stats'][s])
        for campo, tabla in (('colour', 'colores'), ('shape', 'formas'), ('drop', 'drop')):
            if b[campo] not in O[tabla]:
                mal.append(f'{donde}: «{b[campo]}» ({campo}) no está en contenido/objetos.json (odin.{tabla})')
        img = 'odin-' + str(b['id'])
        imagenes[img] = f"images/items/uru_{b['name'].lower()}.png"
        bendiciones.append({'id': str(b['id']), 'n': b['name'], 'color': b['colour'], 'forma': b['shape'], 'st': st,
                            'drop': O['drop'].get(b['drop']), 'img': img})

    # Emblemas.
    E = C['emblemas']
    rarezas = [r['id'] for r in E['rarezas']]
    niveles = sorted(emb_levels, key=lambda x: x['level'])
    if [x['level'] for x in niveles] != list(range(1, 61)):
        mal.append('emblemas: /api/emblems/levels no trae los niveles 1 a 60')
    colecciones, emblemas = [], []
    for e in emblems:
        donde = f"emblema {e['name']} ({e['id']})"
        if e['rarity'] not in rarezas:
            mal.append(f"{donde}: rareza «{e['rarity']}» desconocida")
        if e['buff'] not in E['buffs']:
            mal.append(f"{donde}: lo que da, «{e['buff']}», no está en contenido/objetos.json")
            continue
        col = None if e['collection'] == 'None' else e['collection']
        if col and col not in [c['n'] for c in colecciones]:
            modo = emb_static['modes'].get(col)
            if E['modos'].get(modo) not in ids_modos:
                mal.append(f'{donde}: la colección {col} rige en «{modo}», que no está en contenido/objetos.json o en modos.json')
            colecciones.append({'n': col, 'modo': E['modos'].get(modo)})
        tipos = [f for f in e['flags'] if f in E['tipos']]
        obt = [f for f in e['flags'] if f in E['obtencion']]
        otros = set(e['flags']) - set(tipos) - set(obt) - {'nores'}
        if len(tipos) != 1 or otros:
            mal.append(f"{donde}: flags que no se entienden: {e['flags']}")
        if len(e['levels']) != 60 or not all(isinstance(x, (int, float)) for x in e['levels']):
            mal.append(f'{donde}: no trae los 60 valores de nivel')
        img = 'emblema-' + str(e['id'])
        imagenes[img] = f"images/emblemas/{e['icon']}.png"
        usados.add(E['buffs'][e['buff']])
        emblemas.append({'id': str(e['id']), 'n': e['name'], 'img': img, 'r': e['rarity'], 'col': col, 's': E['buffs'][e['buff']],
                         'tipo': tipos[0] if tipos else None, 'libre': 'nores' in e['flags'], 'obt': obt, 'v': e['levels']})
    sobran = sorted(set(E['buffs']) - {e['buff'] for e in emblems})
    if sobran:
        mal.append(f'contenido/objetos.json: emblemas.buffs que ningún emblema da: {sobran}')

    # Sets de ISO-8.
    I = C['iso']
    piedras = set(guia['iso']['piedras'])
    if set(I['colores'].values()) != piedras or not set(I['piedras_es']) <= piedras:
        mal.append('contenido/objetos.json: los colores de ISO-8 no son las piedras de guia.json (iso.piedras)')
    sets = []
    for nombre, piezas, colores, efecto, act in tabla_sets_iso(wiki_iso['wt']):
        donde = f'set de ISO-8 {nombre}'
        cols = [c.strip() for c in colores.split(',')]
        m = re.fullmatch(r'(\d+) ISO-8', piezas)
        if not m or int(m.group(1)) != len(cols):
            mal.append(f'{donde}: «{piezas}» no son sus {len(cols)} piezas')
        for c in cols:
            if c not in I['colores']:
                mal.append(f'{donde}: el color «{c}» no está en contenido/objetos.json')
        st = []
        for ln in filter(None, (x.replace('\xa0', ' ').strip() for x in efecto.split('\n'))):
            mm = _NUM.match(ln)
            if not mm or mm.group(1) not in I['stats']:
                mal.append(f'{donde}: el stat «{ln}» no está en contenido/objetos.json')
                continue
            x = {'s': I['stats'][mm.group(1)], 'v': float(mm.group(2))}
            if mm.group(1) in I['dudas']:
                x['d'] = I['dudas'][mm.group(1)]
            usados.add(x['s'])
            st.append(x)
        acts = []
        for ln in filter(None, (x.replace('\xa0', ' ').strip().lstrip('*').strip() for x in act.split('\n'))):
            if ln not in I['activaciones']:
                mal.append(f'{donde}: la activación «{ln}» no está en contenido/objetos.json')
                continue
            acts.append({'es': I['activaciones'][ln], 'en': re.sub(r'\[\[|\]\]', '', ln)})
        es = I['sets_es'].get(nombre)
        sets.append({'id': re.sub(r'[^a-z0-9]', '', nombre.lower()), 'n': nombre, 'es': es['es'] if es else None,
                     'captura': es['captura'] if es else None, 'piezas': [I['colores'].get(c) for c in cols], 'st': st, 'act': acts})
    por_nombre = {s['n'].replace('-', ' ').lower(): s for s in sets}
    for g in guia['iso']['sets_pve'] + guia['iso']['sets_pvp']:
        s = por_nombre.get(g['nombre'].replace('-', ' ').lower())
        if not s:
            mal.append(f"guia.json nombra el set de ISO-8 {g['nombre']}, que la wiki no tiene")
        elif sorted(s['piezas']) != sorted(g['piedras']) or {x['s'] for x in s['st']} != set(g['stats']):
            mal.append(f"el set de ISO-8 {g['nombre']}: guia.json y la wiki no dicen las mismas piezas o stats")
    # La app lleva al detalle de cada set que nombran la guía y la guía de armado (isoSetLink): tienen que estar.
    for n in [x for _, x in LEY_ISO_SET]:
        if n.replace('-', ' ').lower() not in por_nombre:
            mal.append(f'la leyenda de la guía de armado nombra el set de ISO-8 {n}, que la wiki no tiene')
    for k in set(I['sets_es']) - {s['n'] for s in sets}:
        mal.append(f'contenido/objetos.json: iso.sets_es nombra el set {k}, que la wiki no tiene')

    # J.A.R.V.I.S.
    cats = {c['id'] for c in J['categorias']}
    for i, ch in enumerate(J['chips']):
        if ch['cat'] not in cats:
            mal.append(f"J.A.R.V.I.S.: el chip {ch['n']} es de una categoría desconocida ({ch['cat']})")
        ch['id'] = f"{ch['cat']}-{re.sub(r'[^a-z0-9]', '', ch['n'].lower())}"
    if len({ch['id'] for ch in J['chips']}) != len(J['chips']):
        mal.append('J.A.R.V.I.S.: dos chips con la misma categoría y nombre')
    usados.update(J['ex_opciones']['stats'])
    for k in J['modos']['ids']:
        if k not in ids_modos:
            mal.append(f'J.A.R.V.I.S.: el modo {k} no está en modos.json')
    for f in J['chips_fuente'] + J['ex_opciones']['fuente'] + J['modos']['fuente'] + I['piedras_es_fuente']['f'] + E['rarezas_fuente']:
        if f not in fuentes:
            mal.append(f'objetos: la fuente {f} no está en contenido/guia.json')

    # Los nombres de los stats: guia.json, los de los cromos y, los que no están en ninguno, los de objetos.json.
    nombres = {}
    for k in sorted(usados):
        n = guia['stats'].get(k) or cromos_nombres.get(k) or C['nombres'].get(k)
        if n is None:
            mal.append(f'el stat {k} no tiene nombre en guia.json, cromos.json ni objetos.json')
        else:
            nombres[k] = {'es': n['es'], 'en': n['en']}
    sobran = sorted(set(C['nombres']) - usados) + sorted(set(C['nombres']) & (set(guia['stats']) | set(cromos_nombres)))
    if sobran:
        mal.append(f'contenido/objetos.json: nombres que no se usan o que ya están en guia.json o cromos.json: {sobran}')

    salida = {
        'stats': nombres,
        'odin': {'bendiciones': bendiciones, 'colores': O['colores'], 'formas': O['formas'], 'notas': notas(O['notas'], 'odin')},
        'emblemas': {'rarezas': E['rarezas'], 'rarezas_fuente': E['rarezas_fuente'], 'tipos': E['tipos'], 'obtencion': E['obtencion'],
                     'sin_restriccion': E['sin_restriccion'], 'colecciones': colecciones, 'emblemas': emblemas,
                     'niveles': [[x['stars'], x['data_cost'], x['kits_cost'], x['gold_cost']] for x in niveles],
                     'notas': notas(E['notas'], 'emblemas')},
        'iso': {'sets': sets, 'piedras_es': I['piedras_es'], 'piedras_es_fuente': I['piedras_es_fuente'], 'notas': notas(I['notas'], 'iso')},
        'jarvis': {k: J[k] for k in ('categorias', 'chips', 'chips_fuente', 'ex_opciones', 'modos', 'imagen_lista')}
                  | {'notas': notas(J['notas'], 'jarvis')},
    }
    if mal:
        raise SystemExit('Objetos no cierra con scripts/contenido/objetos.json:\n- ' + '\n- '.join(mal))
    return salida, imagenes
