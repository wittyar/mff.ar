"""Auditoría de 'Equipos nuevos con él': ¿cuántas sugerencias meten compañeros sin ningún
vínculo de soporte con el personaje? Vínculo = en ese equipo, el compañero le da algo (un
soporte, o el liderazgo si es el líder que cuenta la sinergia) o recibe algo de él.

Modelo aparte de app.js (misma regla de sinergia, escrita acá con los efectos aplicados).
Uso: auditoria_equipos.py [actual|vinculado] [n_variantes|todas]"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import multiprocessing as mp, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analisis_haz import VAR, TODAS, RANGO, SOP, ADV, LE_GANA, aplica, score as score_viejo

NOLIDER = ['passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact']
LIDER = ['leader', 'leader2']
ROLES = ('Tanque', 'Control', 'Daño', 'Soporte')

# 1.0.9: un soporte o liderazgo le sirve a b si alguno de sus efectos le sirve. Los que suben
# un ataque o un daño elemental, solo si b pega con eso en sus skills activas (con lo que dice
# cada etapa de daño: de qué ataque sale y su tipo y elemento). Escrito acá aparte de app.js.
from harness import datos_js as _dj
_D = _dj('MFF_SKILLS', 'MFF_TABLAS')
_SK, _DESC = _D['MFF_SKILLS'], _D['MFF_TABLAS']['desc']
def perfil(p):
    src, tipo, elem = set(), set(), set()
    for sk in _SK.get(p, []):
        if not sk['sl'].startswith('Active'): continue
        for st in sk.get('st') or []:
            for f in st.get('fx') or []:
                d = _DESC[f['p']] if isinstance(f.get('p'), int) and 0 <= f['p'] < len(_DESC) else None
                if d is None or 'pi' not in d or not f.get('v') or d['pi'] >= len(f['v']) or not f['v'][d['pi']]: continue
                partes = d['elem'].split(' ')
                src.add(d['src']); tipo.add(partes[0])
                if len(partes) > 1: elem.add(partes[1])
    return src, tipo, elem
# El cuarto: res, los elementos cuya resistencia le sube el daño (1.0.14, del build: artefacto y Striker).
_PERF = _dj('MFF_PERFIL')['MFF_PERFIL']
PERFIL = {a['p']: perfil(a['p']) + (set(_PERF[a['p']]['res']) if a['p'] in _PERF else set(),) for a in TODAS}
# Desde la segunda parte del carril de consistencia (formato 7), la regla de cada stat está en el catálogo
# (MFF_CATALOGO.soporte: todos, nadie, escala:, elemento:, tipo:, resistencia:, con * para cualquiera); acá se
# evalúa aparte, con el perfil calculado arriba. Un stat que el catálogo no tiene cuenta para todos (la app lo dice).
REGLA = {s: x['sirve'] for s, x in _dj('MFF_CATALOGO')['MFF_CATALOGO']['soporte'].items()}
def sirve_fx(f, pf):
    src, tipo, elem, res = pf
    r = REGLA.get(f['s'], 'todos')
    if r == 'todos': return True
    if r == 'nadie': return False
    mira, valor = r.split(':', 1)
    de = {'escala': src, 'elemento': elem, 'tipo': tipo, 'resistencia': res}[mira]
    return bool(de) if valor == '*' else valor in de
def sirve(x, b): return any(sirve_fx(f, PERFIL[b['p']]) for f in x['fx'])

# Anti-mermas propios (4 de octubre de 2026): lo que sus pasivas (no las activas ni la Striker) le dan a él mismo
# (el análisis, destino 'e'), con los efectos de los stats de anti-mermas de la tabla de valor según el catálogo.
# Con probabilidad (la activación empieza con «#%» y el número es menor que 100), no cuenta. Escrito acá aparte.
import re as _re
_DA = _dj('MFF_ANALISIS', 'MFF_VALOR', 'MFF_CATALOGO')
_IDS = [e['id'] for e in _DA['MFF_CATALOGO']['efectos']]
ANTI_STATS = list(_DA['MFF_VALOR']['anti_mermas'])
EFECTOS_ANTI = {e for s in ANTI_STATS for e in _DA['MFF_CATALOGO']['soporte'][s]['efectos']}
_ACT = _D['MFF_TABLAS']['act']
STAT_DE_EFECTO = {}
for _s in ANTI_STATS:
    for _e in _DA['MFF_CATALOGO']['soporte'][_s]['efectos']: STAT_DE_EFECTO.setdefault(_e, _s)
def _anti_propio(p):
    """([que cuentan], [con probabilidad]), cada uno {sl, ac, av, s, p}: la skill, la activación de la etapa (índice en
    MFF_TABLAS.act y sus números), el stat de anti-mermas y la probabilidad. Uno por etapa, en el orden del análisis."""
    cuenta, prob, vistas = [], [], set()
    for ie, d, _, fuentes in (_DA['MFF_ANALISIS'].get(p) or {}).get('fx', []):
        if d != 'e' or _IDS[ie] not in EFECTOS_ANTI: continue
        for si, ti, _ in fuentes:
            sk = _SK[p][si]
            if sk['sl'].startswith('Active') or sk['sl'] == 'Striker Skill' or (si, ti) in vistas: continue
            vistas.add((si, ti))
            st = sk['st'][ti]
            act = _ACT[st['ac']]['en'] if st.get('ac') is not None else ''
            pr = (st.get('av') or [None])[0] if _re.match(r'\{?#\}?%', act) else None
            x = dict(sl=sk['sl'], ac=st.get('ac'), av=st.get('av'), s=STAT_DE_EFECTO[_IDS[ie]], p=pr)
            (prob if pr is not None and pr < 100 else cuenta).append(x)
    return cuenta, prob
def activacion(x, lang):
    """La activación de un anti-mermas propio en el idioma (como txt('act', ...) de la app: cada # con su número)."""
    if x['ac'] is None: return None
    f = _ACT[x['ac']]
    patron = f['en'] if lang == 'en' or f.get('es') is None else f['es']
    nums = iter(x['av'] or [])
    return _re.sub('#', lambda m: str(next(nums, '#')), patron)
ANTI_PROPIO = {a['p']: _anti_propio(a['p']) for a in TODAS}
def anti_propio(v): return ANTI_PROPIO.get(v['p'], ([], []))

# 1.0.12: bonos de equipo (MFF_BONOS). Activo con todos sus integrantes en el equipo; suma 1 si le
# sirve a alguien (algún stat de alguna de sus versiones, con la misma regla que los soportes); sus
# integrantes quedan vinculados entre sí, y a los que solo lo reciben no los vincula.
BONOS_DE = {}
for _b in _dj('MFF_BONOS')['MFF_BONOS']:
    _x = {'m': frozenset(_b['m']), 'primero': _b['m'][0], 'fx': [{'s': s} for v in _b['v'] for s, _ in v]}
    for _c in _b['m']:
        BONOS_DE.setdefault(_c, []).append(_x)
def bonos_activos(vs):
    """[(índices de sus integrantes, índices de a quiénes les sirve)] de cada bono activo que le sirve a alguien."""
    cids = {v['cid'] for v in vs}
    out = []
    for v in vs:
        for b in BONOS_DE.get(v['cid'], ()):
            if b['primero'] != v['cid'] or not b['m'] <= cids: continue
            rec = [j for j, x in enumerate(vs) if any(sirve_fx(f, PERFIL[x['p']]) for f in b['fx'])]
            if rec: out.append(([j for j, x in enumerate(vs) if x['cid'] in b['m']], rec))
    return out
def comparten_bono(a, b): return any(b['cid'] in x['m'] for x in BONOS_DE.get(a['cid'], ()))
def efectos_bonos(vs, cuenta=lambda ints, rec: True):
    """Los bonos como efectos: cada integrante a los otros; el primero lleva el punto."""
    ef = []
    for ints, rec in bonos_activos(vs):
        if not cuenta(ints, rec): continue
        for k, i in enumerate(ints): ef.append((i, [j for j in ints if j != i], 1 if k == 0 else 0))
    return ef

# Strikers (MFF_STRIKERS): de cada personaje, los que pueden aparecer con él. No suman: desempatan (4 de octubre de 2026).
STRIKERS_DE = {c: {x[0] for x in fs} for c, fs in _dj('MFF_STRIKERS')['MFF_STRIKERS'].items()}

# alcance precalculado: (variante que da, tipo) -> claves de las variantes a las que llega y les sirve
SOPS = {}
for a in TODAS:
    sp = SOP.get(a['p']) or {}
    SOPS[a['key']] = [(k, sp[k], 3 if sp[k].get('sig') else 2,
                       frozenset(b['key'] for b in TODAS if aplica(sp[k], b) and sirve(sp[k], b))) for k in NOLIDER + LIDER if sp.get(k)]

# Efectos iguales (Ezequiel, 5 de octubre de 2026: «El juego no permite el solapado de habilidades iguales... el
# antimermas de apocalipsis y el de deadpool solo va a funcionar uno»; y después: «el daño contra facciones si se suma. EL
# ataque se suma... Las habilidades especificas, inmunidad a romper guardia, por ejemplo no se solapan»). Si se suma lo dice
# el catálogo (MFF_CATALOGO.soporte, acumula: formato 8; un stat que no tiene se suma). Una habilidad (lo que no se acumula)
# que a un integrante le llega de dos o más fuentes se le aplica una sola vez: la de mayor valor (el número de la línea; sin
# número, ninguna gana por valor) y, a igual valor, la primera en este orden: lo propio (sus anti-mermas de las skills que
# cuentan, y sus soportes que le llegan), el liderazgo del líder y los soportes de los demás, el líder primero y los otros
# por su clave. Un soporte o un liderazgo suma, y vincula, solo si a otro le llega algo que se le aplica y le sirve. Escrito
# acá aparte de app.js.
ACUMULA = {s: x['acumula'] for s, x in _DA['MFF_CATALOGO']['soporte'].items()}
def acumula(f): return ACUMULA.get(f['s'], True)
NO_ACUM = {id(x): any(not acumula(f) for f in x['fx']) for sp in SOP.values() for x in sp.values() if isinstance(x, dict) and 'fx' in x}
def _valor(x, s):
    ns = [f['v'] for f in x['fx'] if f['s'] == s and type(f.get('v')) in (int, float)]
    return max(ns) if ns else None
def _lineas(sp, ks, b, s):
    """Las líneas de sp, en los slots ks y en ese orden, que le llegan a b y traen s: [(slot, valor)]."""
    return [(k, _valor(sp[k], s)) for k in ks if sp.get(k) and aplica(sp[k], b) and any(f['s'] == s for f in sp[k]['fx'])]
def primera(vs, li, j, s):
    """La fuente cuya línea del stat s (que no se acumula) se le aplica a vs[j]: (índice, slot), (j, 'propio') si es de sus
    skills, o None si no le llega. La de mayor valor; a igual valor (o sin valor), la primera en el orden."""
    b, cands = vs[j], []
    if any(x['s'] == s for x in anti_propio(b)[0]): cands.append(((j, 'propio'), None))
    cands += [((j, k), v) for k, v in _lineas(SOP.get(b['p']) or {}, NOLIDER, b, s)]
    if li is not None: cands += [((li, k), v) for k, v in _lineas(SOP.get(vs[li]['p']) or {}, LIDER, b, s)]
    for i in ([li] if li is not None else []) + sorted((i for i in range(len(vs)) if i != li), key=lambda i: vs[i]['key']):
        if i != j: cands += [((i, k), v) for k, v in _lineas(SOP.get(vs[i]['p']) or {}, NOLIDER, b, s)]
    mejor = None
    for c, v in cands:
        if mejor is None or (v is not None and mejor[1] is not None and v > mejor[1]): mejor = (c, v)
    return mejor[0] if mejor else None
def se_aplica(vs, li, i, k, x, j):
    """¿A vs[j], al que x (el slot k de vs[i]) le llega y le sirve, se le aplica algo de x? Lo que se acumula, siempre; lo
    que no, si x es la fuente que se le aplica de ese stat."""
    if not NO_ACUM[id(x)]: return True
    pf = PERFIL[vs[j]['p']]
    return any(sirve_fx(f, pf) and (acumula(f) or primera(vs, li, j, f['s']) == (i, k)) for f in x['fx'])


def lider_sin_contexto(vs):
    """Índice del líder sin contexto (Ezequiel, 4 de octubre de 2026: la regla de la 1.0.16 para todo): el que más
    suma con su liderazgo (cada slot que le llega y le sirve a otro: 3 si es Notable, 2 si no); a igual puntaje, el
    mejor ubicado en la General de thanosvibs (RANGO: la primera lista, la de referencia por defecto) y después la
    clave. No depende del orden ni del foco. None si ningún liderazgo suma."""
    mejor = None
    for i, a in enumerate(vs):
        pts = sum(p for k, x, p, alc in SOPS[a['key']] if k in LIDER
                  and any(j != i and b['key'] in alc and se_aplica(vs, i, i, k, x, j) for j, b in enumerate(vs)))
        if pts and (mejor is None or (-pts, RANGO[a['key']], a['key']) < mejor[0]):
            mejor = ((-pts, RANGO[a['key']], a['key']), i)
    return None if mejor is None else mejor[1]

def efectos_lider(vs, li, cuenta=lambda i, bs: True):
    """Los liderazgos del líder (índice li) que le llegan y le sirven a otro, como efectos."""
    if li is None: return []
    out = []
    for k, x, p, alc in SOPS[vs[li]['key']]:
        if k not in LIDER: continue
        bs = [j for j, b in enumerate(vs) if j != li and b['key'] in alc and se_aplica(vs, li, li, k, x, j)]
        if bs and cuenta(li, bs): out.append((li, bs, p))
    return out

def efectos(vs, lider='solo'):
    """Efectos que cuenta la sinergia: (quien da, [a quiénes se les aplica], puntos). Soportes de todos y el
    liderazgo del líder del equipo (lider_sin_contexto, o el índice que se pase: el de un contexto)."""
    li = lider_sin_contexto(vs) if lider == 'solo' else lider
    ef = []
    for i, a in enumerate(vs):
        for k, x, p, alc in SOPS[a['key']]:
            if k in LIDER: continue
            bs = [j for j, b in enumerate(vs) if j != i and b['key'] in alc and se_aplica(vs, li, i, k, x, j)]
            if bs: ef.append((i, bs, p))
    return ef + efectos_lider(vs, li) + efectos_bonos(vs)

def score(vs, lider='solo'):
    if len(vs) < 2: return 0
    s = sum(p for _, _, p in efectos(vs, lider))
    roles = {r for v in vs for r in v['r']}
    if len([r for r in ROLES if r in roles]) >= 2: s += 1
    if len({v['c'] for v in vs}) == len(vs): s += 1
    for a in vs:
        for b in vs:
            am = LE_GANA.get(b['c'])
            if a is not b and am and ADV[a['c']].get(am): s += 1
    return s

def sueltos(vs, i=0):
    """Compañeros de vs[i] sin vínculo de soporte con él en ese equipo."""
    ef = efectos(vs)
    return [j for j in range(len(vs)) if j != i and not any((g == i and j in bs) or (g == j and i in bs) for g, bs, _ in ef)]

def haz(v, tam, ancho=10, vinculado=False):
    """Niveles de la búsqueda: {tamaño: los `ancho` mejores}. vinculado: solo equipos donde
    todos los compañeros tienen vínculo con v."""
    pool = [x for x in TODAS if x['cid'] != v['cid']]
    h, niveles = [[v]], {}
    for n in range(2, tam + 1):
        mejores = {}
        for eq in h:
            for x in pool:
                if any(y['cid'] == x['cid'] for y in eq): continue
                vs = eq + [x]
                if vinculado and sueltos(vs): continue
                firma = '|'.join(sorted(y['cid'] for y in vs))
                o = (vs, score(vs), sum(RANGO[y['key']] for y in vs))
                p = mejores.get(firma)
                if p is None or (o[1] > p[1] or (o[1] == p[1] and o[2] < p[2])): mejores[firma] = o
        h = [o[0] for o in sorted(mejores.values(), key=lambda o: (-o[1], o[2]))[:ancho]]
        niveles[n] = h
    return niveles

def auditar(args):
    k, vinculado = args
    nv = haz(VAR[k], 6, vinculado=vinculado)
    out = {}
    for tam in (3, 5, 6):
        sug = nv[tam][:3]
        out[tam] = [(score(vs), [vs[j]['key'] for j in sueltos(vs)], [x['key'] for x in vs]) for vs in sug]
    return k, out

if __name__ == '__main__':
    # (hasta la 1.0.8 se comparaba con el puntaje de analisis_haz.py; desde la 1.0.9 los
    # efectos cuentan solo si le sirven a quien los recibe, y ese modelo viejo no lo sabe)
    modo = sys.argv[1] if len(sys.argv) > 1 else 'actual'
    cuantas = sys.argv[2] if len(sys.argv) > 2 else 'todas'
    claves = sorted(VAR) if cuantas == 'todas' else random.Random(7).sample(sorted(VAR), int(cuantas))
    with mp.Pool(2) as p:
        res = p.map(auditar, [(k, modo == 'vinculado') for k in claves], chunksize=8)
    import json
    json.dump({k: v for k, v in res}, open(f'{SALIDA}/auditoria_{modo}.json', 'w'))
    for tam in (3, 5, 6):
        sug = [(k, s) for k, r in res for s in r[tam]]
        malas = [(k, s) for k, s in sug if s[1]]
        vars_malas = {k for k, _ in malas}
        cortas = sum(1 for k, r in res if len(r[tam]) < 3)
        print(f'equipos de {tam}: {len(malas)}/{len(sug)} sugerencias con algún compañero sin vínculo '
              f'({len(vars_malas)}/{len(res)} variantes); variantes con menos de 3 sugerencias: {cortas}')
