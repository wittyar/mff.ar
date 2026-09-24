"""Versión de juego vigente según /api/updates de thanosvibs.

La versión del snapshot describe los datos del juego, así que sale de la lista de
actualizaciones y no de una tier list: antes se tomaba la versión de la lista general,
que se actualiza a su propio ritmo (el 24/9/2026 esa lista decía 12.2 con el juego ya en
12.2.5 y sus personajes adentro del snapshot).

Solo biblioteca estándar: lo importa también desktop/servidor.py, que corre con el
Python embebido.
"""
import datetime


def ultima(updates, hoy=None):
    """(fecha, versión) de la última actualización ya publicada.

    Cada entrada de /api/updates es una versión mayor con sus parches en `potes`
    (la mayor y las de mitad de mes, cada una con su fecha). Se ignoran las fechas
    futuras por si la fuente anuncia una versión antes de que salga.
    """
    hoy = hoy or datetime.date.today()
    publicadas = []
    for u in updates:
        for p in u.get('potes') or []:
            fecha = datetime.datetime.strptime(p['date'], '%B %d, %Y').date()
            if fecha <= hoy:
                publicadas.append((fecha, p['version']))
    if not publicadas:
        raise ValueError('/api/updates no trae ninguna versión publicada')
    return max(publicadas)
