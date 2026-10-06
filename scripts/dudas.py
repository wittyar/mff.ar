#!/usr/bin/env python3
"""La información dudosa entre el juego en coreano, el inglés y el español (#32): scripts/contenido/dudas.json.

Cada duda dice a qué va (sobre: un C.T.P., una stat de la guía, un efecto del catálogo, una skill, un término del
glosario o una nota del foro del histórico), qué dice cada idioma, qué quiere decir el coreano (nota, en español y en
inglés), de qué capturas o fuentes sale y con qué certeza. armar() la valida contra los datos y la devuelve como la
usa la app (MFF_DUDAS): {tipo: {id: [duda, ...]}}. Lo llama build.py. Solo biblioteca estándar."""
import json, os

TIPOS = ('ctp', 'stat', 'efecto', 'skill', 'glosario', 'nota')
RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contenido', 'dudas.json')


def armar(ctps, guia, catalogo, glosario, skills, historico):
    """MFF_DUDAS, o SystemExit con todo lo que no cierra."""
    with open(RUTA, encoding='utf-8') as f:
        dudas = json.load(f)['dudas']
    existe = {
        'ctp': {c['id'] for c in ctps},
        'stat': set(guia['stats']),
        'efecto': {e['id'] for e in catalogo['efectos']},
        'skill': {f"{p}|{sk['sl']}" for p, sks in skills.items() for sk in sks},
        'glosario': {x['id'] for x in glosario['terminos']},
        'nota': {str(k) for k in historico['notas']},  # en build.py las claves son números; en data.js, texto
    }
    mal, vistos, out = [], set(), {t: {} for t in TIPOS}
    for d in dudas:
        donde = f"dudas.json: {d.get('id')}"
        if d['id'] in vistos:
            mal.append(f'{donde}: id repetido')
        vistos.add(d['id'])
        tipo, ref = d['sobre']['tipo'], d['sobre']['id']
        if tipo not in TIPOS:
            mal.append(f'{donde}: tipo desconocido {tipo!r}')
            continue
        if ref not in existe[tipo]:
            mal.append(f'{donde}: no existe {tipo} {ref!r}')
        if not d['nota'].get('es') or not d['nota'].get('en'):
            mal.append(f'{donde}: falta la nota en español o en inglés')
        if not (d['ko'] or d['en'] or d['es']):
            mal.append(f'{donde}: no dice qué dice ningún idioma')
        if d['certeza'] not in catalogo['certeza']:
            mal.append(f"{donde}: certeza desconocida {d['certeza']!r}")
        malas = [k for k in d['fuente'] if k not in guia['fuentes']]
        if not d['fuente'] or malas:
            mal.append(f'{donde}: fuentes sin definir en contenido/guia.json: {malas or "ninguna"}')
        out[tipo].setdefault(ref, []).append({k: d[k] for k in ('id', 'ko', 'en', 'es', 'nota', 'fuente', 'certeza')})
    if mal:
        raise SystemExit('scripts/contenido/dudas.json no cierra con los datos:\n- ' + '\n- '.join(mal))
    return out
