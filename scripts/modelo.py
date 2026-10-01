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

Lo usa _core.py para data.js (MFF_PERFIL, por retrato)."""
import math


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
