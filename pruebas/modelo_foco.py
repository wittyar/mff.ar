"""Sinergia con foco en un integrante (lo que le dan, lo que da él, el liderazgo del líder del equipo si lo
involucra, ventaja de clase solo en pares con él) y búsqueda con vínculo. Modelo aparte para decidir."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import auditoria_equipos as A
from analisis_haz import ADV, LE_GANA, RANGO, TODAS, VAR

def efectos_foco(vs, f=0, lider='solo'):
    """Lo que cuenta para él (f): los soportes que lo involucran y el liderazgo del líder del equipo si lo involucra
    (el líder no depende del foco: A.lider_sin_contexto, o el índice que se pase, el de un contexto)."""
    cuenta = lambda i, bs: f is None or i == f or f in bs
    li = A.lider_sin_contexto(vs) if lider == 'solo' else lider
    ef = []
    for i, a in enumerate(vs):
        for k, x, p, alc in A.SOPS[a['key']]:
            if k in A.LIDER: continue
            # a quiénes se les aplica algo (una habilidad, una sola vez: A.se_aplica)
            bs = [j for j, b in enumerate(vs) if j != i and b['key'] in alc and A.se_aplica(vs, li, i, k, x, j)]
            if bs and cuenta(i, bs): ef.append((i, bs, p))
    # un bono cuenta si él está en el bono o le sirve a él
    return ef + A.efectos_lider(vs, li, cuenta) + A.efectos_bonos(vs, lambda ints, rec: f is None or f in ints or f in rec)

def score_foco(vs, f=0, lider='solo'):
    if len(vs) < 2: return 0
    s = sum(p for _, _, p in efectos_foco(vs, f, lider))
    roles = {r for v in vs for r in v['r']}
    if len([r for r in A.ROLES if r in roles]) >= 2: s += 1
    if len({v['c'] for v in vs}) == len(vs): s += 1
    for i, a in enumerate(vs):
        for j, b in enumerate(vs):
            am = LE_GANA.get(b['c'])
            if i != j and am and ADV[a['c']].get(am) and (f is None or f in (i, j)): s += 1
    return s

def stk_foco(vs, f=0):
    """Cuántos strikers del equipo lo involucran (uno es striker del otro): no suman, desempatan (4 de octubre de 2026)."""
    return sum(1 for i, a in enumerate(vs) for j, b in enumerate(vs) if i != j and (f is None or f in (i, j))
               and b['cid'] in A.STRIKERS_DE.get(a['cid'], ()))

def sueltos_foco(vs, f=0, lider='solo'):
    ef = efectos_foco(vs, f, lider)
    return [j for j in range(len(vs)) if j != f and not any((g == f and j in bs) or (g == j and f in bs) for g, bs, _ in ef)]

def haz_foco(v, tam, ancho=10):
    pool = [x for x in TODAS if x['cid'] != v['cid']]
    h, niveles = [[v]], {}
    for n in range(2, tam + 1):
        mejores = {}
        for eq in h:
            for x in pool:
                if any(y['cid'] == x['cid'] for y in eq): continue
                vs = eq + [x]
                if sueltos_foco(vs): continue
                firma = '|'.join(sorted(y['cid'] for y in vs))
                o = (vs, score_foco(vs), sum(RANGO[y['key']] for y in vs))
                p = mejores.get(firma)
                if p is None or (o[1] > p[1] or (o[1] == p[1] and o[2] < p[2])): mejores[firma] = o
        h = [o[0] for o in sorted(mejores.values(), key=lambda o: (-o[1], o[2]))[:ancho]]
        niveles[n] = h
    return niveles

def desperdicio(vs, f=0):
    """Soportes de cada compañero que no le llegan a él (cuántos de cuántos)."""
    out = []
    for j, x in enumerate(vs):
        if j == f: continue
        sops = [(k, alc) for k, sp, p, alc in A.SOPS[x['key']] if k not in A.LIDER]
        out.append((x['name'], sum(1 for k, alc in sops if vs[f]['key'] not in alc), len(sops)))
    return out

if __name__ == '__main__':
    import random
    from harness import datos_js
    C = datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS']
    for nombre in sys.argv[1:] or ['Apocalypse', 'Annihilus']:
        c = next(c for c in C if c['name'] == nombre); v = VAR[f"{c['id']}::base"]
        nv = haz_foco(v, 6)
        print(f'\n== {nombre} ({v["f"]})')
        for tam in (3, 6):
            for vs in nv[tam][:3]:
                print(f'  [{tam}] foco {score_foco(vs)} / equipo {A.score(vs)} :', ' + '.join(x['name'] + (' (u)' if x['uid'] else '') for x in vs[1:]),
                      '| no le llegan:', [(n, f'{w}/{t}') for n, w, t in desperdicio(vs) if w])
