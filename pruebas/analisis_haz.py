"""¿Cuánto se acerca la búsqueda en haz (la de la pestaña Equipos) al óptimo exhaustivo en
equipos de 3? Misma búsqueda que ampliarHaz de app.js (orden del roster, desempate por puesto
en la lista de referencia por defecto, un equipo por conjunto de personajes), escrita aparte,
con la sinergia recalculada acá. Muestra: Wong (Doctor Strange 2) y variantes al azar."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import itertools, multiprocessing as mp, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import datos_js

D0 = datos_js('MFF_SEED_CHARACTERS', 'MFF_SOPORTES', 'MFF_SEED', 'MFF_SEED_TIERLISTS', 'MFF_SEED_TIER_ASSIGNMENTS')
C, SOP, ADV = D0['MFF_SEED_CHARACTERS'], D0['MFF_SOPORTES'], D0['MFF_SEED']['VENTAJA_TIPO']
REF = D0['MFF_SEED_TIERLISTS'][0]
FILAS = [r['id'] for r in REF['rows']]
ASIG = D0['MFF_SEED_TIER_ASSIGNMENTS'][REF['id']]

VAR = {}
for c in C:
    VAR[f"{c['id']}::base"] = dict(key=f"{c['id']}::base", cid=c['id'], name=c['name'], uid=None, c=c['c'], f=c['f'],
                                    race=c['race'], ab=c['abilities'], r=c['r'], p=c['p'])
    for u in c['uniforms']:
        VAR[f"{c['id']}::{u['id']}"] = dict(key=f"{c['id']}::{u['id']}", cid=c['id'], name=c['name'], uid=u['id'],
                                             c=u.get('c', c['c']), f=u.get('f', c['f']), race=u.get('race', c['race']),
                                             ab=u.get('ab', c['abilities']), r=u.get('r', c['r']), p=u['p'])
TODAS = list(VAR.values())
def rango(k):
    idx = sorted(FILAS.index(r) for r in ASIG.get(k, []) if r in FILAS)
    return idx[0] if idx else 999
RANGO = {k: rango(k) for k in VAR}
def aplica(x, b):
    if not x.get('r'): return True
    cat, val = x['r']
    return {'Ability': val in b['ab'], 'Type': b['c'] == val, 'Allies': b['race'] == val, 'Side': b['f'] == val, 'Character': b['name'] == val}[cat]
NOLIDER = ['passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact']
# 1.0.11: a qué clases le gana cada una ('normal' o 'menor', la de Universal); la amenaza de una
# clase es la que le gana con ventaja normal.
LE_GANA = {d: c for c, sobre in ADV.items() for d, f in sobre.items() if f == 'normal'}
def score(vs):
    if len(vs) < 2: return 0
    s = 0
    for i, a in enumerate(vs):
        sp = SOP.get(a['p']) or {}
        for k in NOLIDER:
            if sp.get(k) and any(aplica(sp[k], b) for j, b in enumerate(vs) if j != i):
                s += 3 if sp[k].get('sig') else 2
    mejor = 0
    for i, a in enumerate(vs):
        sp = SOP.get(a['p']) or {}
        mejor = max(mejor, sum((3 if sp[k].get('sig') else 2) for k in ('leader', 'leader2')
                               if sp.get(k) and any(aplica(sp[k], b) for j, b in enumerate(vs) if j != i)))
    s += mejor
    roles = {r for v in vs for r in v['r']}
    if len([r for r in ('Tanque', 'Control', 'Daño', 'Soporte') if r in roles]) >= 2: s += 1
    if len({v['c'] for v in vs}) == len(vs): s += 1
    for i, a in enumerate(vs):
        for j, b in enumerate(vs):
            am = LE_GANA.get(b['c'])
            if i != j and am and ADV[a['c']].get(am): s += 1
    return s

def haz(v, tam, ancho):
    pool = [x for x in TODAS if x['cid'] != v['cid']]
    h = [[v]]
    for _ in range(1, tam):
        mejores = {}
        for eq in h:
            for x in pool:
                if any(y['cid'] == x['cid'] for y in eq): continue
                vs = eq + [x]; firma = '|'.join(sorted(y['cid'] for y in vs))
                o = (vs, score(vs), sum(RANGO[y['key']] for y in vs))
                p = mejores.get(firma)
                if p is None or (o[1] > p[1] or (o[1] == p[1] and o[2] < p[2])): mejores[firma] = o
        h = [o[0] for o in sorted(mejores.values(), key=lambda o: (-o[1], o[2]))[:ancho]]
    return h

def estudiar(k):
    v = VAR[k]
    pool = [x for x in TODAS if x['cid'] != v['cid']]
    opt = max(score([v, a, b]) for a, b in itertools.combinations(pool, 2) if a['cid'] != b['cid'])
    return k, opt, {a: score(haz(v, 3, a)[0]) for a in (5, 10, 20)}

if __name__ == '__main__':
    wong2 = next(k for k, x in VAR.items() if x['name'] == 'Wong' and x['uid'] and 'wong-10200092' in k)
    random.seed(7)
    muestra = [wong2] + random.sample(sorted(VAR), 23)
    with mp.Pool(2) as p:
        res = p.map(estudiar, muestra)
    llega = {a: 0 for a in (5, 10, 20)}
    for k, opt, b in res:
        for a in b: llega[a] += b[a] == opt
        print(f"{VAR[k]['name'][:28]:28} {('— ' + k.split('::')[1]) if VAR[k]['uid'] else '(base)':28} óptimo {opt:3}  haz5 {b[5]:3}  haz10 {b[10]:3}  haz20 {b[20]:3}")
    print({f'llega al óptimo con ANCHO={a}': f'{n}/{len(res)}' for a, n in llega.items()})
