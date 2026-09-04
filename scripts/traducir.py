#!/usr/bin/env python3
"""Capa de traducción al español. Separada del parser a propósito: parse_skills.py
decide estructura (a quién le pega cada efecto) y guarda el inglés crudo de la wiki;
acá se traduce, sin inventar.

Cómo funciona
-------------
Una línea de efecto se normaliza reemplazando cada número por '#'. Ese patrón se
busca en traducciones/efectos.json, que mapea patrón inglés -> patrón español con
los mismos '#'. Al aplicar, los números originales se reinyectan en orden.

    "Physical Damage 152% of Physical Attack."
      -> patrón  "Physical Damage #% of Physical Attack."
      -> español "Daño físico #% del ataque físico."
      -> salida  "Daño físico 152% del ataque físico."

Así una traducción cubre todas las variantes numéricas, incluidas las que aparezcan
en futuras versiones del juego. Si un patrón no está, la función devuelve None: la
app muestra el inglés marcado. Nunca se devuelve una traducción aproximada.
"""
import json, os, re

_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'traducciones')
NUM = re.compile(r'\d+(?:\.\d+)?')

def _cargar(nombre):
    ruta = os.path.join(_DIR, nombre)
    if not os.path.exists(ruta):
        return {}
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)

EFECTOS = _cargar('efectos.json')   # patrón inglés -> patrón español
SKILLS  = _cargar('skills.json')    # nombre de skill inglés -> español

def patron(linea):
    """Clave de búsqueda: la línea con cada número reemplazado por '#'."""
    return NUM.sub('#', linea)

def traducir_linea(linea):
    """Español, o None si no hay traducción cargada para ese patrón."""
    es = EFECTOS.get(patron(linea))
    if es is None:
        return None
    numeros = NUM.findall(linea)
    if es.count('#') != len(numeros):
        # El patrón español perdió o inventó un número: es un error de la tabla, no
        # un texto sin traducir. Se avisa fuerte en vez de emitir una cifra equivocada.
        raise ValueError(f'placeholders desparejos en efectos.json\n  en: {patron(linea)!r}\n  es: {es!r}')
    it = iter(numeros)
    return re.sub(r'#', lambda _: next(it), es)

def traducir_fx(fx):
    """{bucket: [líneas]} -> {bucket: [línea traducida o None]}, misma longitud."""
    return {k: [traducir_linea(l) for l in v] for k, v in fx.items()}

def traducir_skill(nombre):
    """Nombre de skill en español, o None si no está en la tabla."""
    return SKILLS.get(nombre)

def aplanar(fx, etiquetas):
    """Arma el string plano 'd' a partir de un fx ya en un solo idioma."""
    partes = list(fx.get('general', []))
    for k, lbl in etiquetas:
        if fx.get(k):
            partes.append(lbl + ': ' + ' / '.join(fx[k]))
    return ' · '.join(partes)

ETIQ_ES = (('self', 'A sí mismo'), ('enemy', 'Al oponente'), ('allies', 'Al equipo'))
ETIQ_EN = (('self', 'Self'), ('enemy', 'Enemy'), ('allies', 'Allies'))
