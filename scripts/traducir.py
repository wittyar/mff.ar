#!/usr/bin/env python3
"""Tablas de traducción de las skills (inglés -> español), que usa skills_api.py.

Cómo funciona
-------------
Una descripción de efecto se normaliza reemplazando cada número por '#'. Ese patrón
se busca en traducciones/efectos.json, que mapea patrón inglés -> patrón español con
los mismos '#'. La app reinyecta los números en orden al mostrarlo.

    "Physical Damage 152% of Physical Attack."
      -> patrón  "Physical Damage #% of Physical Attack."
      -> español "Daño físico #% del ataque físico."
      -> en la app "Daño físico 152% del ataque físico."

Así una traducción cubre todas las variantes numéricas, incluidas las de futuras
versiones del juego. Si un patrón no está, no hay traducción: la app muestra el
inglés marcado y el build lo lista. Nunca se usa una traducción aproximada.
"""
import json, os, re

_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'traducciones')
NUM = re.compile(r'\d+(?:\.\d+)?')


def _cargar(nombre):
    # Las tablas están en el repo: si falta una, es un error, no "todo sin traducir".
    with open(os.path.join(_DIR, nombre), encoding='utf-8') as f:
        return json.load(f)


EFECTOS      = _cargar('efectos.json')      # patrón de descripción inglés -> español
SKILLS       = _cargar('skills.json')       # nombre de skill inglés -> español
ETIQUETAS    = _cargar('etiquetas.json')    # etiqueta de efecto ("STUN") -> español
ELEMENTOS    = _cargar('elementos.json')    # elemento de daño ("Energy Fire") -> español
OBJETIVOS    = _cargar('objetivos.json')    # objetivo de la etapa -> español
ACTIVACIONES = _cargar('activaciones.json') # activación de la etapa (patrón) -> español


def patron(linea):
    """Clave de búsqueda: la línea con cada número reemplazado por '#'."""
    return NUM.sub('#', linea)


def traducir_skill(nombre):
    """Nombre de skill en español, o None si no está en la tabla."""
    return SKILLS.get(nombre)


def traducir_etiqueta(v):  return ETIQUETAS.get(v)
def traducir_elemento(v):  return ELEMENTOS.get(v)
def traducir_objetivo(v):  return OBJETIVOS.get(v)
