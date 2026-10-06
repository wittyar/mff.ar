#!/usr/bin/env python3
"""Copia los datos publicados en la raíz (datos.json y los archivos que lista) a datos/<formato>/.

La app instalada baja los datos de la carpeta de su formato (desktop/actualizador.py): cuando sube el formato,
la carpeta del anterior queda como estaba y las versiones de la app que lo usan siguen teniendo datos que pueden
leer, y ven adentro el aviso de la versión nueva (#1). La raíz se sigue publicando: la leen las versiones
instaladas hasta la 1.0.29.

Lo corre build.py después de escribir datos.json; solo, copia lo que ya está en la raíz. Verifica cada archivo
contra el sha256 y el tamaño de datos.json: si no coinciden, corta sin tocar la carpeta."""
import hashlib, json, os, shutil, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def copiar():
    with open(os.path.join(RAIZ, 'datos.json'), 'rb') as f:
        crudo = f.read()
    m = json.loads(crudo)
    contenidos = {}
    for rel, info in m['archivos'].items():
        with open(os.path.join(RAIZ, *rel.split('/')), 'rb') as f:
            contenidos[rel] = f.read()
        if len(contenidos[rel]) != info['bytes'] or hashlib.sha256(contenidos[rel]).hexdigest() != info['sha256']:
            raise SystemExit(f'{rel} no es el que anuncia datos.json: no se copia a datos/{m["formato"]}/')
    destino = os.path.join(RAIZ, 'datos', str(m['formato']))
    # La carpeta se rehace entera: un archivo que el manifiesto ya no lista no queda publicado.
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    for rel, contenido in list(contenidos.items()) + [('datos.json', crudo)]:
        ruta = os.path.join(destino, *rel.split('/'))
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, 'wb') as f:
            f.write(contenido)
    print(f'datos/{m["formato"]}/: datos.json y {len(contenidos)} archivos')


if __name__ == '__main__':
    if len(sys.argv) != 1:
        raise SystemExit(__doc__)
    copiar()
