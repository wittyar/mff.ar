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
  la tabla, y la tabla dice lo que dicen las capturas (el término, sin mayúsculas, en el texto transcripto);
- el vocabulario (sección vocabulario de la tabla, #44 y #45): cada término del juego está en la captura que cita, y
  ningún texto en español usa la traducción propia que reemplazó (propias: expresiones regulares sobre el texto en
  minúsculas), salvo los de excepto. Los textos: las traducciones de scripts/traducciones/ (salvo skills.json, los
  nombres de las skills, que siguen siendo propios), los "es" del contenido curado (scripts/contenido/) y las cadenas
  es:'…' de app.js. Lo que va entre comillas es una cita (lo que dice el inglés, por ejemplo) y no cuenta.

Lo corre build.py; solo, `python scripts/terminos_es.py` (no necesita work/). Solo biblioteca estándar."""
import glob, json, os, re, sys

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
    return mal + validar_vocabulario(tabla['vocabulario'])


# Dónde está cada fuente del vocabulario (fuentes/juego-es/<archivo>.json). ficha.json no lleva captura por línea: es la
# captura 210 (y los rótulos de los C.T.P., 3 a 49).
ARCHIVOS = {'skills': ['ficha_heroe'], 'ctps': ['ctps_fichas', 'ctps'], 'ficha': ['ficha'], 'glosario': ['glosario'],
            'objetos': ['objetos']}


def lineas_captura(x, cap, out):
    """[(captura, texto en minúsculas)] de todo lo transcripto; la captura, la del objeto más cercano que la dice."""
    if isinstance(x, dict):
        c = x.get('captura', cap)
        for v in x.values():
            lineas_captura(v, c, out)
    elif isinstance(x, list):
        for v in x:
            lineas_captura(v, cap, out)
    elif isinstance(x, str):
        out.append((cap, x.lower()))
    return out


def validar_vocabulario(voc):
    mal = []
    textos = {a: lineas_captura(cargar(CAPTURAS, f'{a}.json'), None, []) for xs in ARCHIVOS.values() for a in xs}
    for x in voc:
        es = x['es'].lower()
        if x['fuente'] not in ARCHIVOS:
            mal.append(f"terminos_es: vocabulario {x['en']}: fuente desconocida {x['fuente']!r}")
        elif not any(es in t and (c == x['captura'] or (c is None and x['fuente'] == 'ficha'))
                     for a in ARCHIVOS[x['fuente']] for c, t in textos[a]):
            mal.append(f"terminos_es: vocabulario {x['en']}: «{x['es']}» no está en la captura {x['captura']} ({x['fuente']})")
    trad = textos_es()
    for x in voc:
        for e in x['excepto']:
            if not any(v == e for _, _, v in trad):
                mal.append(f"terminos_es: vocabulario {x['en']}: la excepción {e!r} no es ninguna traducción")
        for r in x['propias']:
            mal += [f"{f}: «{k}» dice «{v}»: el juego dice «{x['es']}» ({r})" for f, k, v in trad
                    if re.search(r, sin_citas(v)) and v not in x['excepto']]
    return mal


def sin_citas(v):
    """El texto en minúsculas sin lo que va entre comillas (las citas)."""
    return re.sub(r'«[^»]*»|"[^"]*"|“[^”]*”', '', v).lower()


def textos_es():
    """[(archivo, dónde, texto)] de todo lo que la app muestra en español con palabras propias."""
    out = [(f'traducciones/{os.path.basename(p)}', k, v) for p in sorted(glob.glob(os.path.join(_DIR, 'traducciones', '*.json')))
           if not p.endswith('skills.json') for k, v in cargar(p).items()]
    def es(o, donde, f):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == 'es' and isinstance(v, str):
                    out.append((f, donde, v))
                else:
                    es(v, f'{donde}/{k}', f)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                es(v, f'{donde}/{i}', f)
    for p in sorted(glob.glob(os.path.join(_DIR, 'contenido', '*.json'))):
        if not p.endswith('terminos_es.json'):
            es(cargar(p), '', f'contenido/{os.path.basename(p)}')
    with open(os.path.join(RAIZ, 'app.js'), encoding='utf-8') as f:
        app = f.read()
    out += [('app.js', m.group(1), m.group(2).replace("\\'", "'"))
            for m in re.finditer(r"(\w+):\s*\{\s*es:\s*'((?:[^'\\]|\\.)*)'", app)]
    return out


if __name__ == '__main__':
    problemas = validar()
    for p in problemas:
        print(p)
    sys.exit(1 if problemas else 0)
