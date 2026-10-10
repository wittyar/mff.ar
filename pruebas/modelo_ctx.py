"""Modelo aparte del puntaje de contexto (1.0.15 + líder único, reglas de Ezequiel), escrito acá sin
mirar app.js. Sin función en el contexto (ninguna fila de sus tier lists, o solo «Not for wbl»), el foco
no tiene lista en ese contexto.
- Roles: las filas de las tier lists del contexto (roles_listas.json y las ubicaciones de data.js). Sin
  DPS, el trío no entra.
- En PvP, anti-mermas para los tres, del liderazgo del candidato a líder o del soporte de alguno (uno que
  se activa con una condición vale igual). Sin candidato que cumpla, no entra.
- Liderazgo (Ezequiel, 2 de octubre de 2026: «único + condicional a la mitad»; 4 de octubre: la tabla de
  valor, MFF_VALOR): por cada stat de la fila del contexto y cada integrante al que le llega y le sirve, su
  peso si le llega por un liderazgo permanente y la parte del condicional si solo le llega por uno que se
  activa con una condición (el slot trae ac, como «When Debuffed»). Cada stat cuenta una vez por
  integrante, con el mayor peso; los porcentajes no cuentan.
- Líder: el candidato que más suma; a igual puntaje, el de menor puesto en el contexto (la suma de su
  puesto en cada lista del contexto: la mejor fila; sin ubicar, una más abajo que la última) y después la
  clave menor. No depende del orden del trío: es el mismo en las listas de los tres.
- DPS (su peso por nivel de fila), soportes que le llegan a otro y le sirven y bonos activos (el peso de
  cada uno, de la tabla). Los strikers del trío no suman (Ezequiel, 4 de octubre de 2026): a igual
  puntaje, desempatan.
- El requisito (en PvP, anti-mermas para los tres) y los stats anti-mermas también salen de la tabla. Cuentan
  el liderazgo del candidato, los soportes de cualquiera (también el propio) y los anti-mermas propios de sus
  skills, salvo los que tienen probabilidad (Ezequiel, 4 de octubre de 2026).
La tabla (pesos, requisito, anti-mermas) se lee de los datos; la cuenta se hace acá aparte.
evaluar(vs, ctx, antes=True) es la regla de la 1.0.15 (2 por stat e integrante, con los stats de entonces,
sin mirar la activación; 2 por nivel de DPS y 1 por soporte, bono y striker; a igual puntaje, el primero
del trío): solo para los «antes» de los casos de referencia."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import datos_js
import auditoria_equipos as A
from analisis_haz import VAR, TODAS, aplica, SOP

_D = datos_js('MFF_SEED_TIER_ASSIGNMENTS', 'MFF_STRIKERS', 'MFF_SEED_TIERLISTS', 'MFF_VALOR')
ASIG, STK, VALOR = _D['MFF_SEED_TIER_ASSIGNMENTS'], _D['MFF_STRIKERS'], _D['MFF_VALOR']
FILAS_LISTA = {l['id']: [r['id'] for r in l['rows']] for l in _D['MFF_SEED_TIERLISTS']}
ROLES = json.load(open(f'{RAIZ}/scripts/contenido/roles_listas.json', encoding='utf-8'))
TABLA = {c: {lid: {f['fila']: (f['rol'], f['nivel']) for f in fs} for lid, fs in ROLES[c].items()} for c in ('pvp', 'pve')}
ANTI = set(VALOR['anti_mermas'])
FILA = VALOR['contextos']
VALE = {c: {x['stat']: x['peso'] for x in FILA[c]['liderazgo']} for c in FILA}
# La 1.0.15, para los «antes» de los casos de referencia: 2 por stat, con los stats de entonces.
VALE_1015 = {'pvp': {'All Basic Attacks', 'All Basic Attacks (Stackable)', 'All Basic Defenses', 'HP', 'Ignore Dodge'},
             'pve': {'All Basic Attacks', 'All Basic Attacks (Stackable)', 'Physical Attack', 'Energy Attack', 'Fire Damage',
                     'Fire Damage by % Fire Resist', 'Cold Damage', 'Lightning Damage', 'Poison Damage', 'Mind Damage',
                     'All Element Damage', 'Basic Damage Dealt to Boss Types'}}
LID = ('leader', 'leader2')
NOLID = ('passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact')
STK_DE = {c: {x[0] for x in fs} for c, fs in STK.items()}

def funcion(key, ctx):
    """¿Tiene función en el contexto? Alguna fila de sus tier lists que no lo deje fuera («Not for wbl»)."""
    return any(tabla[fid][0] != 'fuera' for lid, tabla in TABLA[ctx].items() for fid in ASIG.get(lid, {}).get(key, []))

_ROL = {}
def dps_de(key, ctx):
    if (key, ctx) not in _ROL:
        n = 0
        for lid, tabla in TABLA[ctx].items():
            for fid in ASIG.get(lid, {}).get(key, []):
                rol, nivel = tabla[fid]
                if rol == 'dps': n = max(n, nivel)
        _ROL[(key, ctx)] = n
    return _ROL[(key, ctx)]

def puesto(lid, key):
    filas = FILAS_LISTA[lid]
    idx = sorted(filas.index(r) for r in ASIG.get(lid, {}).get(key, []) if r in filas)
    return idx[0] if idx else len(filas)

def puesto_ctx(key, ctx):
    """Su puesto en el contexto: la suma de su puesto en cada lista del contexto (desempata al líder)."""
    return sum(puesto(lid, key) for lid in TABLA[ctx])

def _sirve1(s, b): return A.sirve_fx({'s': s}, A.PERFIL[b['p']])
def _anti(x): return any(f['s'] in ANTI for f in x['fx'])

def puntos_lider(vs, li, ctx, antes=False):
    """Puntos del liderazgo de vs[li] en el trío vs: cada stat que vale, una vez por integrante al que le llega, le sirve
    y se le aplica, con el peso mayor (el suyo si es permanente, la parte del condicional si se activa con una condición)."""
    sp = SOP.get(vs[li]['p']) or {}
    peso = {}
    for k in LID:
        x = sp.get(k)
        if not x: continue
        for f in x['fx']:
            if antes:
                if f['s'] not in VALE_1015[ctx]: continue
                w = 2
            else:
                if f['s'] not in VALE[ctx]: continue
                w = VALE[ctx][f['s']] * (FILA[ctx]['condicional'] if x.get('ac') else 1)
            for j, m in enumerate(vs):
                # una habilidad (lo que no se acumula; la tabla de hoy no pesa ninguna) suma si es la que se le aplica (5 de
                # octubre de 2026: A.primera, con él de líder)
                if aplica(x, m) and _sirve1(f['s'], m) and (antes or A.acumula(f) or A.primera(vs, li, j, f['s']) == (li, k)):
                    peso[f['s'], j] = max(peso.get((f['s'], j), 0), w)
    return sum(peso.values())

def candidatos(vs, ctx, antes=False):
    """[(índice, puntos del liderazgo)] de los que pueden liderar el trío (en PvP, con anti-mermas para los tres)."""
    sp = [SOP.get(x['p']) or {} for x in vs]
    # Sin el liderazgo: un soporte de alguno (también el propio) o sus propias skills (sin probabilidad; desde el 4 de
    # octubre de 2026; con antes=True, la 1.0.15, solo los soportes).
    cubre = [any(_anti(s[k]) and aplica(s[k], m) for s in sp for k in NOLID if s.get(k)) or (not antes and bool(A.anti_propio(m)[0]))
             for m in vs]
    out = []
    for i in range(len(vs)):
        requisito = 'anti_mermas' if antes and ctx == 'pvp' else None if antes else FILA[ctx]['requisito']
        if requisito == 'anti_mermas' and not all(cubre[j] or any(_anti(sp[i][k]) and aplica(sp[i][k], m) for k in LID if sp[i].get(k))
                                                  for j, m in enumerate(vs)):
            continue
        out.append((i, puntos_lider(vs, i, ctx, antes)))
    return out

def evaluar(vs, ctx, antes=False):
    """(puntaje, índice del líder, (liderazgo, dps, sinergia, strikers)) o None si el trío no entra. Los strikers
    no van en el puntaje (desde el 4 de octubre de 2026; con antes=True, la 1.0.15, sí): desempatan."""
    dps = [dps_de(x['key'], ctx) for x in vs]
    if not any(dps): return None
    cs = candidatos(vs, ctx, antes)
    if not cs: return None
    if antes: li, plid = max(cs, key=lambda c: c[1])   # el primero entre empates
    else: li, plid = min(cs, key=lambda c: (-c[1], puesto_ctx(vs[c[0]]['key'], ctx), vs[c[0]]['key']))
    sp = [SOP.get(x['p']) or {} for x in vs]
    # cada soporte con el que a otro le llega algo que se le aplica y le sirve (una habilidad, una sola vez: desde el 5 de
    # octubre de 2026, A.se_aplica; con antes=True, la 1.0.15, sin eso)
    n_sop = sum(1 for a, s in enumerate(sp) for k in NOLID if s.get(k)
                and any(j != a and aplica(s[k], m) and A.sirve(s[k], m) and (antes or A.se_aplica(vs, li, a, k, s[k], j)) for j, m in enumerate(vs)))
    n_bono = len(A.bonos_activos(vs))
    stk = sum(1 for a in vs for b in vs if a is not b and b['cid'] in STK_DE.get(a['cid'], ()))
    if antes:
        partes = (plid, 2 * sum(dps), n_sop + n_bono, stk)
        return sum(partes), li, partes
    F = FILA[ctx]
    partes = (plid, F['dps'] * sum(dps), F['soporte'] * n_sop + F['bono'] * n_bono, stk)
    return sum(partes[:3]), li, partes
