"""De dónde sale cada imagen de la app: una sola regla para todo el proyecto.

La usan fetch_all.py, que las baja en la máquina que corre el pipeline, y build.py, que
publica en datos.json la lista de imágenes con su origen para que la app instalada baje
las que le falten.

    images/<retrato>.png        -> thanosvibs /images/portraits/<retrato>.png
    images/icons/<slug>.png     -> thanosvibs /images/attributes/<slug>.png
    images/items/<nombre>.png   -> thanosvibs /images/items/<nombre>.png
"""
TV = 'https://thanosvibs.money'
CARPETAS = {'icons': 'attributes', 'items': 'items'}


def origen(ruta):
    """Ruta local ('images/...png') -> URL de la imagen en thanosvibs."""
    partes = ruta.split('/')
    if partes[0] != 'images' or not partes[-1].endswith('.png'):
        raise ValueError(f'ruta de imagen inesperada: {ruta}')
    if len(partes) == 2:
        return f'{TV}/images/portraits/{partes[1]}'
    if len(partes) == 3 and partes[1] in CARPETAS:
        return f'{TV}/images/{CARPETAS[partes[1]]}/{partes[2]}'
    raise ValueError(f'ruta de imagen sin origen conocido: {ruta}')
