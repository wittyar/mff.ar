#!/usr/bin/env python3
"""Los términos del juego en español mandan sobre las traducciones propias (#32).

El juego en español tiene giros feos, pero son los que usa el juego, así que la app los usa (Ezequiel, 5 de octubre
de 2026). Las fuentes son las capturas del juego en español (fuentes/juego-es/, transcriptas a mano de las capturas
de Ezequiel): el glosario de habilidades (glosario.json), las fichas de los C.T.P. (ctps.json) y la ficha del héroe
(ficha.json). La tabla scripts/contenido/terminos_es.json dice qué stat, qué etiqueta de skill y qué efecto del catálogo
llevan qué término, y de qué captura sale.

validar() devuelve lo que no cierra:
- cada término del glosario (contenido/glosario.json) lleva como nombre en español el del juego;
- cada stat, etiqueta y efecto de la tabla lleva en guia.json, traducciones/etiquetas.json y catalogo.json lo que dice
  la tabla, y la tabla dice lo que dicen las capturas (el término, sin mayúsculas, en el texto transcripto).

Lo corre build.py; solo, `python scripts/terminos_es.py` (no necesita work/). Solo biblioteca estándar."""
import json, os, sys

_DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(_DIR)
CAPTURAS = os.path.join(RAIZ, 'fuentes', 'juego-es')


def cargar(*partes):
    with open(os.path.join(*partes), encoding='utf-8') as f:
        return json.load(f)


def textos_captura():
    """Todo lo transcripto de cada captura, en minúsculas: {'glosario': ..., 'ctps': ..., 'ficha': ...}."""
    def plano(x):
        if isinstance(x, str):
            return x
        if isinstance(x, dict):
            return ' '.join(plano(v) for v in x.values())
        if isinstance(x, list):
            return ' '.join(plano(v) for v in x)
        return ''
    return {k: plano(cargar(CAPTURAS, f'{k}.json')).lower() for k in ('glosario', 'ctps', 'ficha')}


def validar():
    mal = []
    tabla = cargar(_DIR, 'contenido', 'terminos_es.json')
    capt = textos_captura()
    juego = {x['id']: x for x in cargar(CAPTURAS, 'glosario.json')['terminos']}
    for x in cargar(_DIR, 'contenido', 'glosario.json')['terminos']:
        j = juego.get(x['id'])
        if j is None:
            mal.append(f"glosario: {x['id']} no está en fuentes/juego-es/glosario.json")
        elif x['es'] != j['nombre']:
            mal.append(f"glosario: {x['id']} se llama «{x['es']}» y en el juego «{j['nombre']}»")
    for seccion, actual in (('stats', {k: v['es'] for k, v in cargar(_DIR, 'contenido', 'guia.json')['stats'].items()}),
                            ('etiquetas', cargar(_DIR, 'traducciones', 'etiquetas.json')),
                            ('efectos', {e['id']: e['es'] for e in cargar(_DIR, 'contenido', 'catalogo.json')['efectos']})):
        for clave, (es, fuente) in tabla[seccion].items():
            if isinstance(fuente, list):
                # Compuesto de términos del juego: cada uno, en alguna captura.
                mal += [f'terminos_es: {seccion} {clave}: «{p}» no está en ninguna captura' for p in fuente
                        if not any(p in c for c in capt.values())]
            elif fuente not in capt:
                mal.append(f'terminos_es: {seccion} {clave}: fuente desconocida {fuente!r}')
            else:
                # El término tiene que estar en la captura (sin la parte entre paréntesis, que explica la app, ni la flecha
                # de las etiquetas).
                nucleo = es.split(' (')[0].replace(' ↑', '').lower()
                if nucleo not in capt[fuente]:
                    mal.append(f'terminos_es: {seccion} {clave}: «{nucleo}» no está en la captura {fuente}')
            if clave not in actual:
                mal.append(f'terminos_es: {seccion} {clave}: no existe')
            elif actual[clave] != es:
                mal.append(f'terminos_es: {seccion} {clave} dice «{actual[clave]}» y el juego, «{es}»')
    return mal


if __name__ == '__main__':
    problemas = validar()
    for p in problemas:
        print(p)
    sys.exit(1 if problemas else 0)
