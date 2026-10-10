"""Baja al clon las imágenes que publica datos.json (las mismas que baja la app instalada)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
RAIZ = RAIZ
lista = json.load(open(f'{RAIZ}/datos.json', encoding='utf-8'))['imagenes']
def bajar(par):
    ruta, url = par
    dest = os.path.join(RAIZ, ruta)
    if os.path.exists(dest): return None
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        with urllib.request.urlopen(url, timeout=60) as r: datos = r.read()
        open(dest, 'wb').write(datos); return None
    except Exception as e:
        return f'{ruta}: {e}'
with ThreadPoolExecutor(16) as ex:
    errores = [e for e in ex.map(bajar, lista) if e]
print(len(lista), 'imágenes;', len(errores), 'errores'); print('\n'.join(errores[:20]))
