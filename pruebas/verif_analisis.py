"""Etapa 2 del modelo: el análisis de cada variante (MFF_ANALISIS) y la pestaña Análisis.
- Los datos: cada retrato con skills tiene su análisis; cada fuente apunta a un efecto que
  existe y que el catálogo clasifica así; «Give Power» solo cuando no le sigue nada (lo que le sigue en una etapa con
  un objetivo para cada efecto no cuenta: el de Kang the Conqueror es una entrada).
- La pestaña: una fila por entrada, sin errores, en una muestra de variantes y en casos puntuales
  (Ebony Maw con su uniforme contra Universales, Phil Coulson con algo que no le sirve, el «Give
  Power» vacío del liderazgo de Deadpool, los roles por uniforme), en inglés y en el celular."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, DATOS
from playwright.sync_api import sync_playwright
ok = Chequeo()
js = open(f'{DATOS}/data.js', encoding='utf-8').read()
def var(n):
    return json.loads(re.search(r'window\.' + n + r' = (.*?);\n', js, re.S).group(1))
AN, SK, CAT, TB, CH = var('MFF_ANALISIS'), var('MFF_SKILLS'), var('MFF_CATALOGO'), var('MFF_TABLAS'), var('MFF_SEED_CHARACTERS')

# ---- datos ----
ok('cada retrato con skills tiene su análisis', set(AN) == set(SK), sorted(set(SK) ^ set(AN))[:5])
malas, otorga_con_algo = [], []
OTORGA = next(i for i, e in enumerate(CAT['efectos']) if e['id'] == 'otorga')
for p, a in AN.items():
    for x in a['fx']:
        e, d, objetivo, fuentes = x
        if d not in 'eqri' or (d == 'q') != (objetivo is not None):
            malas.append((p, x)); continue
        for si, ti, fi in fuentes:
            f = SK[p][si]['st'][ti]['fx'][fi]
            m = CAT['skills'][TB['ab'][f['a']]['en']]
            m = m['por_patron'][TB['desc'][f['p']]['en']] if 'por_patron' in m else m
            if CAT['efectos'][e]['id'] not in m['efectos']:
                malas.append((p, x))
            if e == OTORGA:
                # Lo que le sigue en una etapa con un objetivo para cada efecto va a otro objetivo: no es lo que
                # otorga (carril Q, segunda parte: Kang the Conqueror).
                etapas = SK[p][si]['st']
                tg = etapas[ti].get('tg')
                por_efecto = tg is not None and TB['tgt'][tg]['en'].startswith('All Allies for the first effect')
                if (etapas[ti]['fx'][fi + 1:] and not por_efecto) or any(s.get('fx') for s in etapas[ti + 1:]):
                    otorga_con_algo.append((p, si))
    for i in a.get('ns', []):
        if a['fx'][i][1] != 'e': malas.append((p, 'ns', i))
ok('cada fuente apunta a un efecto que existe y que el catálogo clasifica así', not malas, malas[:3])
ok('«Give Power» va solo cuando no le sigue nada', not otorga_con_algo, otorga_con_algo[:3])
kang = [x for x in AN['kang']['fx'] if x[0] == OTORGA]
ok('el «Give Power» de Kang the Conqueror (para todos; la suba que le sigue es para él) es una entrada, al equipo',
   len(kang) == 1 and kang[0][1] == 'q', kang)
ok('nada sin clasificar en estos datos', not any(a.get('sc') for a in AN.values()))
uni_con_roles = [(c, u) for c in CH for u in c['uniforms'] if 'r' in u]
ok('hay uniformes con roles propios', len(uni_con_roles) > 100, len(uni_con_roles))

# ---- la pestaña: desde la 1.0.27 no hay pestaña Análisis (#33: se rehace); el análisis lo usan el «Cómo funciona»
# (verif_tooltip_skill, verif_tooltip_todas) y el «Pega con» del Resumen (verif_ficha).
ok.fin()
