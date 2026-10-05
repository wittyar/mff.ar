#!/usr/bin/env python3
"""Strikers: los personajes que pueden aparecer a pegar junto a uno, con una probabilidad, cuando
él ataca o cuando lo atacan. Según Ezequiel, el striker tiene que estar en el mismo equipo.

thanosvibs no los publica. La wiki de Future Fight, sí: en la página de cada personaje, la pestaña
Striker trae una fila por striker con su ícono, su nombre y «12% chance to appear when attacking.»
(o «when attacked.»). La lista de Kingpin coincide con la del juego (capturas de Ezequiel, octubre de
2026). Un tercio de las páginas no tiene la pestaña, casi todas de personajes recientes: esos no
tienen strikers en la app, y la auditoría los lista.

Los íconos se pasan a personajes como en los bonos de equipo (scripts/bonos.py). Lo que no se puede
leer (un ícono que no es de ningún personaje, una fila sin probabilidad) no se adivina: esa fila no
cuenta y la auditoría lo dice. Una probabilidad de más de 100% (Daken: Doctor Octopus, 219%) es un dato
imposible de la wiki: no se corrige ni se topea, va tal cual (la app la marca) y la auditoría la lista.

Lo usa fuentes.py: los strikers van a la app (MFF_STRIKERS) y lo que no cierra, a docs/AUDITORIA.md."""
import re
from bonos import ICONOS, _ICONO, _norm

# Fin de la pestaña: la siguiente («|-|»), el cierre de las pestañas o la sección siguiente.
_FIN = re.compile(r'\n\|-\||</tabber>|\n==[^=]|\{\{CharacterNav')
# «12% chance to appear when attacking.»; la wiki tiene erratas en el número («18tf%», «20 chance»).
# «attackin» y «attackeing» son erratas de «attacking»; «when attack.» no dice cuál de los dos es.
_PROB = re.compile(r'(\d+(?:\.\d+)?)[a-z]*\s*%?\s*chance to appear when (attacked|attacking|attackin|attackeing)\b', re.I)
CUANDO = {'attacked': 'atacado', 'attacking': 'ataca', 'attackin': 'ataca', 'attackeing': 'ataca'}


def seccion(wt):
    """La pestaña Striker de una página, sin su título; None si no tiene."""
    i = wt.find('Striker=')
    if i < 0:
        return None
    m = _FIN.search(wt, i + len('Striker='))
    return wt[i + len('Striker='):m.start() if m else len(wt)]


def strikers(paginas, nombres):
    """Los strikers de cada personaje y lo que no cierra.

    paginas: los wikitexts de los personajes ({'name': nombre en thanosvibs, 'wt'}); nombres: los
    nombres de los personajes en thanosvibs. Devuelve {'strikers': {personaje: [[striker, %,
    'ataca'|'atacado'], ...]}, 'auditoria': {...}}, en el orden de la página."""
    nombres = set(nombres)
    por_norm = {_norm(n): n for n in nombres}

    def personaje(icono):
        n = ICONOS.get(icono) or por_norm.get(_norm(icono))
        return n if n in nombres else None

    out, sin_pestana, ilegibles, repetidos, imposibles = {}, [], [], [], []
    for d in paginas:
        sec = seccion(d['wt'])
        if sec is None:
            sin_pestana.append(d['name'])
            continue
        filas = []
        for linea in sec.split('\n'):
            iconos = [m.group(1) for m in _ICONO.finditer(linea)]
            if not iconos:
                continue
            quien, m = personaje(iconos[0]), _PROB.search(linea)
            if quien is None or m is None or quien == d['name']:
                motivo = ('ícono sin personaje: ' + iconos[0] if quien is None else
                          'no se lee la probabilidad o cuándo aparece' if m is None else 'es él mismo')
                ilegibles.append({'pagina': d['name'], 'fila': re.sub(r'<br\s*/?>', '', linea).strip()[:120], 'motivo': motivo})
                continue
            if any(f[0] == quien for f in filas):
                repetidos.append({'pagina': d['name'], 'striker': quien})
                continue
            filas.append([quien, float(m.group(1)), CUANDO[m.group(2).lower()]])
            if filas[-1][1] > 100:
                imposibles.append({'pagina': d['name'], 'striker': quien, 'p': filas[-1][1], 'cuando': filas[-1][2]})
        out[d['name']] = filas
    return {'strikers': out, 'auditoria': {'paginas': len(out), 'sin_pestana': sorted(sin_pestana),
                                           'ilegibles': ilegibles, 'repetidos': repetidos, 'imposibles': imposibles,
                                           'filas': sum(len(f) for f in out.values())}}
