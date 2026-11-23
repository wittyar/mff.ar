#!/usr/bin/env python3
"""Jefe mundial para el planificador de Mi cuenta (1.0.59; Ezequiel, 23 de noviembre de 2026: «Dale con todo» a
«Planificador de Jefe mundial y Batalla de alianza con tu roster: qué equipo armar con lo que tenés para la restricción
del día»), para MFF_JEFE_MUNDIAL.

Sale de fuentes/mffguide/jefe_mundial.json: las tablas de Jefe mundial según mffguide.fyi, que dice sacarlas de los
archivos del juego v12.4.0 (hechos del juego, sin el criterio de la guía; lo que no se pudo contrastar está en su
cabecera). Las palabras de las restricciones se leen con el vocabulario de thanosvibs (dominio.RESTRICCION): una que no
esté ahí corta el build, como en las de Alliance Battle. Lo que pide cada dificultad va con el paso de la hoja de ruta
de la guía de thanosvibs (contenido/guia.json, progresion.pasos) que lo cumple; un paso que no esté ahí también corta.

armar(guia) devuelve MFF_JEFE_MUNDIAL:
  f (fuentes), repetir {es, en},
  dificultades [{id, es, en, fases, jefes (la dificultad de sus jefes), principal {paso, es, en}, aliados {paso, es, en},
                 repiten_aliados, nota? {es, en}}],
  jefes [{id, en, es, dif, consejos [{es, en}], r [[desde, hasta, [valores del dominio]]]}],
  habilidades_es {valor de la app: cómo lo escribe el juego en español según la guía} (para la auditoría).
Solo biblioteca estándar."""
import json, os

from dominio import ABIL, RESTRICCION

_DIR = os.path.dirname(os.path.abspath(__file__))
FUENTE = 'mffguide-jm'
CON_FASES = ('leyenda', 'leyenda+', 'mitico')     # las que tienen restricciones por fase


def fuente():
    with open(os.path.join(_DIR, '..', 'fuentes', 'mffguide', 'jefe_mundial.json'), encoding='utf-8') as f:
        return json.load(f)


def armar(guia):
    F = fuente()
    pasos = {p['id'] for p in guia['progresion']['pasos']}
    mal = []
    difs = F['dificultades']
    ids = [d['id'] for d in difs]
    for d in difs:
        for k in ('principal', 'aliados'):
            if d[k]['paso'] not in pasos:
                mal.append(f"{d['id']}: el paso {d[k]['paso']!r} de los {k} no está en la hoja de ruta (guia.json, progresion.pasos)")
        if d['jefes'] not in ids:
            mal.append(f"{d['id']}: jefes de una dificultad que no está: {d['jefes']!r}")
    jefes = []
    for j in F['jefes']:
        if j['dif'] not in ids:
            mal.append(f"{j['en']}: dificultad desconocida {j['dif']!r}")
        r = j['restricciones']
        if (j['dif'] in CON_FASES) != bool(r):
            mal.append(f"{j['en']} ({j['dif']}): " + ('sin restricciones por fase' if not r else 'con restricciones en una dificultad que no las tiene'))
        if r and not (r[0][0] == 1 and r[-1][1] == 99 and all(a[1] + 1 == b[0] for a, b in zip(r, r[1:]))):
            mal.append(f"{j['en']}: los rangos de fases no van de 1 a 99 sin huecos")
        for a, b, ps in r:
            for p in ps:
                if p not in RESTRICCION:
                    mal.append(f"{j['en']} {a}-{b}: palabra de restricción que no está en dominio.RESTRICCION: {p!r}")
        jefes.append({'id': j['id'], 'en': j['en'], 'es': j['es'], 'dif': j['dif'], 'consejos': j['consejos'],
                      'r': [[a, b, [RESTRICCION.get(p, p) for p in ps]] for a, b, ps in r]})
    for d in difs:
        if not any(j['dif'] == d['jefes'] for j in jefes):
            mal.append(f"{d['id']}: ningún jefe de {d['jefes']}")
    for en in F['habilidades_es']:
        if en not in ABIL:
            mal.append(f'habilidades_es: {en!r} no es una habilidad de thanosvibs (dominio.ABIL)')
    if mal:
        raise SystemExit('fuentes/mffguide/jefe_mundial.json no cierra:\n- ' + '\n- '.join(mal))
    return {'f': [FUENTE], 'repetir': F['repetir'], 'dificultades': difs, 'jefes': jefes,
            'habilidades_es': {ABIL[en]: es for en, es in F['habilidades_es'].items()}}
