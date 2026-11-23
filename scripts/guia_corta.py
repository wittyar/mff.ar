#!/usr/bin/env python3
"""La Guía de la app (1.0.59; Ezequiel, 23 de noviembre de 2026, aprobó «Guía corta de progreso y rutina dentro de la app,
enlazada a las secciones que ya existen, en vez de un texto de un millón de caracteres»), para MFF_GUIA_CORTA.

Sale de scripts/contenido/guia_corta.json: temas, cada uno con bloques de puntos, y cada punto con sus partes (k: dato,
criterio, mg, dif, app, orden, topes) y sus enlaces (ir). validar() devuelve lo que no cierra:
- cada tema, bloque y punto con id único, y es y en con texto (un punto de un modo toma el nombre del modo);
- cada fuente que se ve en la Guía (las de las partes y las de guia.json › orden_build y topes) con su nombre corto, en
  fuentes_cortas (es y en) o en guia.json (corto); y en fuentes_cortas, ninguna que no se use;
- cada parte de un tipo conocido; dato, criterio, mg y dif con fuentes, todas registradas en contenido/guia.json; mg con
  una fuente de mffguide.fyi; criterio con de quién (thanosvibs o app); app sin fuente (dice qué hace la app); orden y
  topes, sin texto (los pone la app de guia.json, orden_build y topes);
- cada enlace a algo que existe: un modo de contenido/modos.json, una pestaña de Objetos, de Mi cuenta o de la ficha
  (OBJ_TABS, CUENTA_TABS y FICHA_TABS de app.js), el planificador de Jefe mundial o de Batalla de alianza, un término del
  glosario (gl-<id>, contenido/glosario.json) o un efecto del catálogo (ef-<id>, contenido/catalogo.json), una vista
  (Tier lists o Roster), un tramo del recorrido (las claves k de RECORRIDO en app.js, o * para el completo) y, con pjs,
  el personaje de ejemplo de una ficha.

armar(pjs) valida (corta el build con la lista) y devuelve MFF_GUIA_CORTA: los temas y los nombres cortos tal cual, sin la nota.
Solo, `python scripts/guia_corta.py` valida sin work/ (sin los personajes de ejemplo, y lo dice). Solo biblioteca estándar."""
import json, os, re, sys

_DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(_DIR)
TIPOS = {'dato', 'criterio', 'mg', 'dif', 'app', 'orden', 'topes'}
CON_FUENTE = {'dato', 'criterio', 'mg', 'dif'}
CRITERIO_DE = {'thanosvibs', 'app'}
PLAN = {'wb', 'ab'}
VISTAS = {'tierlist', 'roster'}


def cargar(*partes):
    with open(os.path.join(*partes), encoding='utf-8') as f:
        return json.load(f)


def constantes_app():
    """Las pestañas y los tramos del recorrido que define app.js: {'OBJ_TABS': [...], ..., 'RECORRIDO': [...]}."""
    with open(os.path.join(RAIZ, 'app.js'), encoding='utf-8') as f:
        app = f.read()
    out = {}
    for c in ('OBJ_TABS', 'CUENTA_TABS', 'FICHA_TABS'):
        m = re.search(r'const ' + c + r" = \[([^\]]*)\]", app)
        if not m:
            raise SystemExit(f'guia_corta: app.js no define {c}')
        out[c] = re.findall(r"'(\w+)'", m.group(1))
    m = re.search(r'const RECORRIDO = \[(.*?)\n\];', app, re.S)
    if not m:
        raise SystemExit('guia_corta: app.js no define RECORRIDO')
    out['RECORRIDO'] = re.findall(r"^  \{ k: '(\w+)'", m.group(1), re.M)
    return out


def validar(G, guia, modos, glosario, catalogo, app, pjs=None):
    mal = []
    fuentes = guia['fuentes']
    ids_modo = {m['id'] for m in modos['modos']}
    glos = {'gl-' + x['id'] for x in glosario['terminos']} | {'ef-' + e['id'] for e in catalogo['efectos']}
    destinos = {
        'modo': lambda d: d.get('id') in ids_modo,
        'objetos': lambda d: d.get('tab') in app['OBJ_TABS'],
        'cuenta': lambda d: d.get('tab') in app['CUENTA_TABS'],
        'plan': lambda d: d.get('modo') in PLAN,
        'ficha': lambda d: d.get('tab') in app['FICHA_TABS'] and (pjs is None or d.get('pj') in pjs) and bool(d.get('pj')),
        'glosario': lambda d: d.get('id') in glos,
        'vista': lambda d: d.get('v') in VISTAS,
        'recorrido': lambda d: d.get('area') == '*' or d.get('area') in app['RECORRIDO'],
    }
    vistos = set()
    usadas = set()

    def unico(clave, donde):
        if clave in vistos:
            mal.append(f'{donde}: id repetido')
        vistos.add(clave)

    def textos(x, donde):
        for l in ('es', 'en'):
            if not (isinstance(x.get(l), str) and x[l].strip()):
                mal.append(f'{donde}: sin texto en {l}')

    if not G.get('temas'):
        mal.append('sin temas')
    for tm in G.get('temas', []):
        dt = f"tema {tm.get('id')}"
        unico(('t', tm.get('id')), dt)
        textos(tm, dt)
        if not tm.get('bloques'):
            mal.append(f'{dt}: sin bloques')
        for bl in tm.get('bloques', []):
            db = f"{dt} › {bl.get('id')}"
            unico(('b', bl.get('id')), db)
            textos(bl, db)
            if not bl.get('items'):
                mal.append(f'{db}: sin puntos')
            for it in bl.get('items', []):
                di = f"{db} › {it.get('id')}"
                unico(('i', it.get('id')), di)
                if 'modo' in it:
                    if it['modo'] not in ids_modo:
                        mal.append(f"{di}: modo desconocido {it['modo']!r} (contenido/modos.json)")
                    if 'es' in it or 'en' in it:
                        mal.append(f'{di}: el punto de un modo lleva el nombre del modo, no uno propio')
                else:
                    textos(it, di)
                if not it.get('partes'):
                    mal.append(f'{di}: sin partes')
                for n, p in enumerate(it.get('partes', [])):
                    dp = f'{di} › parte {n}'
                    k = p.get('k')
                    if k not in TIPOS:
                        mal.append(f'{dp}: tipo desconocido {k!r}')
                        continue
                    if k in ('orden', 'topes'):
                        usadas.update(guia['orden_build' if k == 'orden' else 'topes']['fuente'])
                        if set(p) - {'k'}:
                            mal.append(f'{dp}: {k} no lleva texto ni fuentes (los pone guia.json)')
                        continue
                    textos(p, dp)
                    fs = p.get('fuente')
                    usadas.update(fs or [])
                    if k in CON_FUENTE:
                        if not fs:
                            mal.append(f'{dp}: {k} sin fuente')
                        for f in fs or []:
                            if f not in fuentes:
                                mal.append(f'{dp}: fuente sin registrar en contenido/guia.json: {f!r}')
                        if k == 'mg' and not any(f.startswith('mffguide') for f in fs or []):
                            mal.append(f'{dp}: mg sin una fuente de mffguide.fyi')
                    elif fs:
                        mal.append(f'{dp}: app no lleva fuente (dice qué hace la app)')
                    if k == 'criterio' and p.get('de') not in CRITERIO_DE:
                        mal.append(f"{dp}: criterio de quién: {p.get('de')!r} (thanosvibs o app)")
                    if k != 'criterio' and 'de' in p:
                        mal.append(f'{dp}: solo un criterio dice de quién es')
                for d in it.get('ir', []):
                    a = d.get('a')
                    if a not in destinos:
                        mal.append(f'{di}: enlace de un tipo desconocido {a!r}')
                    elif not destinos[a](d):
                        mal.append(f'{di}: el enlace {json.dumps(d, ensure_ascii=False)} no lleva a nada que exista')
    cortas = G.get('fuentes_cortas', {})
    for f in sorted(usadas):
        if f in fuentes and not fuentes[f].get('corto'):
            if f not in cortas:
                mal.append(f'fuente sin nombre corto (fuentes_cortas): {f!r}')
            else:
                textos(cortas[f], f'fuentes_cortas › {f}')
    for f in sorted(set(cortas) - usadas):
        mal.append(f'fuentes_cortas: {f!r} no se usa en la Guía')
    for f in sorted(set(cortas) & {f for f in fuentes if fuentes[f].get('corto')}):
        mal.append(f'fuentes_cortas: {f!r} ya tiene nombre corto en guia.json')
    return mal


def armar(pjs):
    C = os.path.join(_DIR, 'contenido')
    G = cargar(C, 'guia_corta.json')
    mal = validar(G, cargar(C, 'guia.json'), cargar(C, 'modos.json'), cargar(C, 'glosario.json'), cargar(C, 'catalogo.json'),
                  constantes_app(), set(pjs))
    if mal:
        raise SystemExit('contenido/guia_corta.json no cierra:\n  ' + '\n  '.join(mal))
    return {'fuentes_cortas': G['fuentes_cortas'], 'temas': G['temas']}


if __name__ == '__main__':
    C = os.path.join(_DIR, 'contenido')
    G = cargar(C, 'guia_corta.json')
    problemas = validar(G, cargar(C, 'guia.json'), cargar(C, 'modos.json'), cargar(C, 'glosario.json'), cargar(C, 'catalogo.json'),
                        constantes_app())
    print('sin work/: no se comprueba que existan los personajes de ejemplo de las fichas')
    for p in problemas:
        print(p)
    sys.exit(1 if problemas else 0)
