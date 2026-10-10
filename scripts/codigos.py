#!/usr/bin/env python3
"""Los números que la API publica en el texto de algunos efectos en lugar de un nombre: el id de una habilidad
(«Increases damage dealt to targets with 206 effect»), un elemento («Increases 1 damage by...») o las ranuras de las
activas («Sets the Cooldown time of 1234 skill»). CODIGOS dice, de cada patrón, en qué lugar de sus números va un código.

nombres() da el nombre de cada código de un efecto, en inglés y en español, en este orden:
1. Un id de habilidad de la API (abilityId, que la misma API trae en cada efecto con su etiqueta): la etiqueta.
2. scripts/contenido/codigos.json: el nombre que dan las fichas de las notas de los foros oficiales, con su fuente.
Si algún código del efecto queda sin nombre, ninguno se nombra: el efecto se muestra como lo publica la API y
docs/COMPLETITUD.md lo lista («Código en lugar de un nombre»). Solo biblioteca estándar."""
import json, os

CODIGOS = {
    'Increases damage dealt to targets with # effect by #%': (0,),
    '#s increase to the duration of #.': (1,),
    'Increases # damage by #% of # Resistance (up to #%)': (0, 2),
    'Accumulates #% of pure # damage when attacking (Max #%)': (1,),
    'Removes # from target (Includes all debuffs)': (0,),
    'Removes the effect # from #.': (0, 1),
    'Decreases # effect used by the Character by #%.': (0,),
    'Decreases damage received from reflected effects by #%.Effect: #': (1,),
    'Sets the Cooldown time of # skill to # sec': (0,),
}
RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'contenido', 'codigos.json')


def a_mano():
    """{(patrón, código): (inglés, español)} de codigos.json, validado contra CODIGOS."""
    out, mal = {}, []
    for e in json.load(open(RUTA, encoding='utf-8'))['codigos']:
        if set(e) != {'patron', 'codigo', 'en', 'es', 'fuente'}:
            mal.append(f'{e}: lleva patron, codigo, en, es y fuente')
            continue
        if e['patron'] not in CODIGOS:
            mal.append(f"{e['patron']!r}: no es un patrón con códigos (CODIGOS)")
        k = (e['patron'], e['codigo'])
        if k in out:
            mal.append(f'{k}: repetido')
        out[k] = (e['en'], e['es'])
    if mal:
        raise SystemExit('scripts/contenido/codigos.json tiene errores:\n  ' + '\n  '.join(mal))
    return out


def nombres(patron, valores, etiqueta_de, manual):
    """[[lugar, inglés, español, origen]] de los códigos de un efecto ('a': la etiqueta de la API; 'm': codigos.json),
    o None si el patrón no tiene códigos o alguno queda sin nombre. etiqueta_de: {abilityId: (inglés, español)}."""
    if patron not in CODIGOS:
        return None
    out = []
    for i in CODIGOS[patron]:
        c = valores[i]
        if (patron, c) in manual:
            out.append([i, *manual[(patron, c)], 'm'])
        elif c in etiqueta_de and len(str(c)) == 3:
            out.append([i, *etiqueta_de[c], 'a'])
        else:
            return None
    return out
