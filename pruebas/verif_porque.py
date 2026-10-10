"""«Por qué» de las tarjetas de equipo y detalle de PvP y PvE, legibles (carril J, 3 de octubre de 2026; en una ventana desde
el carril modal, 5 de octubre de 2026). Ezequiel: «los bloques de texto que armaste son ilegibles», y el 4 de octubre: «Esto
se tiene que poder ver más prolijo y legible... El desglose, podés ponerlo en un modal, con los retratos para cada
personaje». La tarjeta tiene el botón «Por qué y C.T.P.»; la ventana, una pestaña por integrante con lo que recibe (un
renglón por beneficio: efecto, total y de dónde sale cada parte, con el enlace a cada skill) y lo que aporta, y arriba de
dónde salen los puntos. Contra un modelo escrito acá (recibe() con aplica/sirve_fx de auditoria_equipos.py, las partes de la
sinergia con A.SOPS, sin mirar app.js):
1. Adam Warlock — GotG3 + Black Cat — Queen in Black + Jeff the Land Shark, puntos para él: lo que recibe Adam (la pestaña
   que abre la ventana), renglón por renglón (el total exacto del pedido, con la condición de «Elimina todas las mermas» y lo
   que llega sin artefactos en el renglón mixto; de dónde sale cada parte: Black Cat, liderazgo y Tier-2; Jeff, Pasiva 4★ y
   su secundaria; los dos artefactos), la leyenda del * una sola vez, lo que aporta él y las partes de los puntos para él.
2. Cada enlace lleva a la skill correcta (la secundaria de Jeff es su Activa 5, Jeff's Cuddle Buddy) o al artefacto, en la
   ficha de ese compañero con su uniforme, resaltada y a la vista, y «Atrás» vuelve a la lista en la misma página, a la misma
   altura y con la ventana abierta en la misma pestaña.
3. Detalle de PvP de Adam + Wasp — Quantumania + Doctor Voodoo — Savage Avengers (más allá de la primera página del orden
   PvP), en la ventana: una parte por renglón con sus viñetas, nombres cortos, «a todos» y los números del modelo de
   contexto; el enlace al liderazgo de Wasp y «Atrás» (y el volver del navegador) a esa página. Los strikers, como desempate.
4. Condicionales: Silver Surfer — Void Knight + Yondu + Invisible Woman (lidera ella: empatan en puntos y está mejor en la
   General; el líder es uno solo desde la lista de cualquiera, 4 de octubre de 2026), cada condicional con su condición y un
   valor de texto; Silver Surfer + Yondu + Sleeper (lidera él): lo permanente y lo condicional del mismo stat en renglones
   aparte; el enlace a su propio liderazgo abre otra entrada del historial y «Atrás» vuelve a la lista.
5. «Cómo entraría»: Jeff en Black Cat — QiB + Doctor Voodoo — SA + Thor (entra por Thor): lo que recibe, lo que aporta, lo
   que se gana (la ventaja) y lo que se pierde; un enlace y «Atrás».
6. Inglés; celular (390 px) sin desbordes; sin errores de página ni de consola.
Carril de consistencia: cada efecto con la recarga de su activación y «dura N s» (el mismo texto que el Resumen, la
comparativa, los bonos y el detalle de PvP y PvE); en el detalle, «Soportes y bonos de equipo +N» dice de quién es cada
soporte (con «*» si es un artefacto) y cada bono.
Capturas en carril-modal/shots: porque_1300.png, porque_390.png, detalle_pvp_1300.png."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright
import auditoria_equipos as A
import modelo_ctx as M
from analisis_haz import VAR, SOP, ADV, LE_GANA, aplica

ok = Chequeo()
CAPT = SALIDA
os.makedirs(CAPT, exist_ok=True)
D0 = datos_js('MFF_SEED_CHARACTERS', 'MFF_TXT', 'MFF_STRIKERS', 'MFF_ARTEFACTOS', 'MFF_SKILLS', 'MFF_TABLAS', 'MFF_BONOS')
C, TXT, STK, ARTES = D0['MFF_SEED_CHARACTERS'], D0['MFF_TXT'], D0['MFF_STRIKERS'], D0['MFF_ARTEFACTOS']
SKILLS, NOMBRES = D0['MFF_SKILLS'], D0['MFF_TABLAS']['name']
SUB = {(c['id'], u['id']): u['name'] for c in C for u in c['uniforms']}
BASE_P = {c['id']: c['p'] for c in C}
def full(v): return v['name'] + (' — ' + SUB[(v['cid'], v['uid'])] if v['uid'] else '')

ADAM, BC, JEFF = VAR['adam-warlock::adam-warlock-10200152'], VAR['black-cat::black-cat-10400009'], VAR['jeff-the-land-shark::base']
WASP, DV, THOR = VAR['wasp::wasp-10300051'], VAR['doctor-voodoo::doctor-voodoo-10200204'], VAR['thor::base']
SS, YONDU, IW = VAR['silver-surfer::silver-surfer-10200199'], VAR['yondu::yondu-10300046'], VAR['invisible-woman::invisible-woman-10400180']
EQUIPO = {'id': 'eq-porque', 'name': 'Prueba del porqué', 'modeId': '', 'reason': '', 'members': [BC['key'], DV['key'], THOR['key']]}

# ---- el modelo (la regla de la app escrita de nuevo) ----
TIPOS = ['leader', 'leader2', 'passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact']
LID = ('leader', 'leader2')
ROT = {'es': dict(leader='Liderazgo', leader2='Liderazgo (secundario)', passive='Pasiva 4★', passive2='Pasiva 4★ (secundaria)',
                  t2='Pasiva de Tier-2', t22='Pasiva de Tier-2 (secundaria)', uniform='Efecto de uniforme',
                  uniform2='Efecto de uniforme (secundario)', artifact='Skill exclusiva del artefacto'),
       'en': dict(leader='Leadership', leader2='Leadership (Secondary)', passive='4★ Passive', passive2='4★ Passive (Secondary)',
                  t2='Tier-2 Passive', t22='Tier-2 Passive (Secondary)', uniform='Uniform Effect', uniform2='Uniform Effect (Secondary)',
                  artifact='Artifact Exclusive Skill')}
L = {'es': dict(inst='del instinto total', req='requiere', cap='acumula hasta', cd='recarga', dura='dura', sin_art='sin artefactos: {x}',
                at6='a 6★', recibe='Lo que recibe {x}', aporta='Lo que aporta {x}', todos='a todos', si_art='si lleva su artefacto',
                ley='* Solo si el compañero que lo da lleva su artefacto.', ademas='Además', pierde='Se pierde',
                gana='Se gana, además de lo de {x}', nada='Nada de lo suyo les llega y les sirve a los demás.',
                lider='Liderazgo de {x}', sop='Soportes', bonos='Bonos de equipo', otras='Roles, clases y ventaja de clase'),
     'en': dict(inst='of total Instinct', req='requires', cap='stacks up to', cd='cooldown', dura='lasts', sin_art='without artifacts: {x}',
                at6='at 6★', recibe='What {x} gets', aporta='What {x} gives', todos='everyone', si_art='if it has its artifact',
                ley='* Only if the teammate who gives it has its artifact.', ademas='Also', pierde='Lost',
                gana="Also gained, besides what {x} brings", nada='Nothing of its own reaches and helps the others.',
                lider="{x}'s leadership", sop='Supports', bonos='Team bonuses', otras='Roles, classes and class advantage')}
def tr(en, lang): return TXT.get(en, en) if lang == 'es' else en
# Topes (carril filtro2, segunda parte): de la guía (MFF_GUIA.topes, con su fuente) y qué stat tiene cuál, del catálogo
# (MFF_CATALOGO.soporte, tope). Debajo del efecto, en lo que recibe: «Tope de la guía: 75%.» con la fuente y, si lo que suman
# los buffs pasa lo que queda hasta el tope (con condición, con lo que le llega siempre), el aviso.
_DT = datos_js('MFF_GUIA', 'MFF_CATALOGO')
TOPE_DE = {s: x.get('tope', []) for s, x in _DT['MFF_CATALOGO']['soporte'].items()}
TOPES = {k: (it['tope'], it.get('base') or 0) for it in _DT['MFF_GUIA']['topes']['items'] if it['tope'] is not None for k in it['stats']}
NOM_TOPE = _DT['MFF_GUIA']['stats']
FUENTE_TOPE = _DT['MFF_GUIA']['fuentes'][_DT['MFF_GUIA']['topes']['fuente'][0]]['nombre']
T_TOPE = {'es': dict(tope='Tope de la guía: {t}.', base='{n}% (desde {b}%)', pasa='Pasa el tope: los potenciadores suman {x}% y hasta el tope quedan {r}%; lo de más no suma.',
                     pasa_c='Con lo que le llega siempre, pasa el tope: los potenciadores suman {x}% y hasta el tope quedan {r}%; lo de más no suma.'),
          'en': dict(tope='Guide cap: {t}.', base='{n}% (from {b}%)', pasa='Over the cap: the buffs add up to {x}% and only {r}% is left to the cap; the rest adds nothing.',
                     pasa_c='With what it always gets, it goes over the cap: the buffs add up to {x}% and only {r}% is left to the cap; the rest adds nothing.')}
def tope_txt(s, total, cond, siempre, lang):
    ks = TOPE_DE.get(s) or []
    if not ks: return ''
    T = T_TOPE[lang]
    uno = lambda k: (NOM_TOPE[k][lang] + ' ' if len(ks) > 1 else '') + (T['base'].format(n=num(TOPES[k][0], lang), b=num(TOPES[k][1], lang)) if TOPES[k][1] else num(TOPES[k][0], lang) + '%')
    txt = ' ' + T['tope'].format(t=', '.join(uno(k) for k in ks)) + ' ' + FUENTE_TOPE
    suma = None if total is None else abs(total + (siempre if cond else 0))
    queda = min(TOPES[k][0] - TOPES[k][1] for k in ks)
    if suma is not None and suma > queda:
        txt += ' ' + (T['pasa_c'] if cond and siempre else T['pasa']).format(x=num(suma, lang), r=num(queda, lang))
    return txt
def num(n, lang):
    s = f'{round(n, 2):g}'
    return s.replace('.', ',') if lang == 'es' else s
def pct(n, lang): r = round(n, 2); return ('+' if r > 0 else '−' if r < 0 else '') + num(abs(r), lang) + '%'
def valor(v, i, lang):
    out = []
    if isinstance(v, str): out.append(tr(v, lang))
    elif v is not None: out.append(pct(v, lang))
    if i is not None: out.append(pct(i, lang) + ' ' + L[lang]['inst'])
    return ' '.join(out)
def condicion(x, f, lang):
    p = []
    if x.get('ac'): s = tr(x['ac'], lang); p.append(s[:1].lower() + s[1:])
    if x.get('cd'): p.append(L[lang]['cd'] + ' ' + num(x['cd'], lang) + ' s')
    if x.get('req'): p.append(L[lang]['req'] + ' ' + tr(x['req'], lang))
    if f.get('c'): p.append(tr(f['c'], lang))
    d = f['d'] if f.get('d') is not None else x.get('d')
    if d is not None: p.append(L[lang]['dura'] + ' ' + num(d, lang) + ' s')
    if f.get('tope') is not None: p.append(L[lang]['cap'] + ' ' + num(f['tope'], lang) + '%')
    return ', '.join(p)
def efecto(x, f, lang):
    val, cond = valor(f.get('v'), f.get('i'), lang), condicion(x, f, lang)
    return tr(f['s'], lang) + (' ' + val if val else '') + (f' ({cond})' if cond else '')
def sirve(f, b): return A.sirve_fx(f, A.PERFIL[b['p']])
def recibe(dest, a, es_lider, lang='es'):
    """Lo que le llega a dest de a y le sirve: (slot, soporte, efectos). Desde el 4 de octubre de 2026, también los soportes
    propios y sus anti-mermas propios sin probabilidad ('propio'). Desde el 5 de octubre, en el orden en que se aplican: de él
    mismo, sus anti-mermas propios, sus soportes y su liderazgo; de otro, su liderazgo y sus soportes."""
    sp, out = SOP.get(a['p']) or {}, []
    if a is dest:
        for y in A.anti_propio(a)[0]:
            out.append(('propio', {'ac': A.activacion(y, lang), 'sl': y['sl']}, [{'s': y['s']}]))
    sop = [k for k in TIPOS if k not in LID]
    for k in (sop + (list(LID) if es_lider else [])) if a is dest else ((list(LID) if es_lider else []) + sop):
        x = sp.get(k)
        if not x or not aplica(x, dest): continue
        fx = [f for f in x['fx'] if sirve(f, dest)]
        if fx: out.append((k, x, fx))
    return out
# Efectos iguales (Ezequiel, 5 de octubre de 2026): una habilidad (lo que no se acumula, según el catálogo) que a uno le llega de
# dos fuentes se le aplica una vez, la de mayor valor y, a igual valor, la primera (A.primera: lo propio, el liderazgo del líder,
# los soportes con el líder primero y los demás por clave). Lo que no se suma va con «no se suma: ya lo tiene …» (lo que recibe)
# o «X ya lo tiene …» (a quién le llega), y no entra en el total.
REP = {'es': dict(no='no se suma: ya lo tiene {de}', quien='{y} ya lo tiene {de}', nada='no suma', propio='propio ({s})',
                  su_lid='de su liderazgo', lid='del liderazgo de {x}', sop='de {x} ({s})', y=' y '),
       'en': dict(no='not added: it already has it {de}', quien='{y} already has it {de}', nada='adds nothing', propio='as its own ({s})',
                  su_lid='from its own leadership', lid="from {x}'s leadership", sop='from {x} ({s})', y=' and ')}
def orden_equipo(vs, lider): return ([lider] if lider else []) + sorted([x for x in vs if x is not lider], key=lambda x: x['key'])
def ix(vs, x): return next(i for i, y in enumerate(vs) if y is x)
def ya_de(vs, j, s, fuente, nom, lang):
    """De quién ya tiene vs[j] el stat s: fuente, (índice de quien da, slot) de A.primera."""
    i, k = fuente
    if k == 'propio':
        sl = next(x['sl'] for x in A.anti_propio(vs[j])[0] if x['s'] == s)
        return REP[lang]['propio'].format(s=SLOT_ES.get(sl, sl) if lang == 'es' else sl)
    if i == j: return REP[lang]['su_lid'] if k in LID else REP[lang]['propio'].format(s=ROT[lang][k])
    return REP[lang]['lid'].format(x=nom(vs[i])) if k in LID else REP[lang]['sop'].format(x=nom(vs[i]), s=ROT[lang][k])
def no_suma(vs, li, i, k, f, j, n=0):
    """Si el efecto f (del slot k de vs[i]; n: el lugar de un propio de las skills entre los del mismo stat) no se le suma a
    vs[j], la fuente que ya se lo da; si no, None."""
    if A.acumula(f): return None
    p = A.primera(vs, li, j, f['s'])
    return None if p == (i, k) and n == 0 else p
def ya_lo_tienen(vs, no, nom, lang):
    """« (X ya lo tiene …; Y ya lo tiene …)» de [(j, [(stat, fuente)])], o vacío."""
    if not no: return ''
    def de(j, fs):
        vistas, out = set(), []
        for st, p in fs:
            t = ya_de(vs, j, st, p, nom, lang)
            if t not in vistas: vistas.add(t); out.append(t)
        return REP[lang]['y'].join(out)
    return ' (' + '; '.join(REP[lang]['quien'].format(y=nom(vs[j]), de=de(j, fs)) for j, fs in no) + ')'
def reparto(vs, li, i, k, x, alc):
    """A quiénes (menos vs[i]) les llega x y les sirve (alc: sus claves): (a los que se les aplica algo, [(j, [(stat, fuente)])]
    a los que les llega algo que ya tienen)."""
    si, no = [], []
    for j, b in enumerate(vs):
        if j == i or b['key'] not in alc: continue
        if A.se_aplica(vs, li, i, k, x, j): si.append(j)
        fs = [(f['s'], p) for f in x['fx'] if sirve(f, b) and (p := no_suma(vs, li, i, k, f, j))]
        if fs: no.append((j, fs))
    return si, no
def origenes(foco, vs, lider, lang='es'):
    pjs, arts = [], []
    for a in [foco] + [x for x in orden_equipo(vs, lider) if x is not foco]:
        rs = recibe(foco, a, a is lider, lang)
        if [r for r in rs if r[0] != 'artifact']: pjs.append((a, False, [r for r in rs if r[0] != 'artifact']))
        if [r for r in rs if r[0] == 'artifact']: arts.append((a, True, [r for r in rs if r[0] == 'artifact']))
    return pjs + arts
SLOT_ES = {'Leader Skill': 'Liderazgo', 'Passive': 'Pasiva', 'Tier-2 Passive': 'Pasiva T2', 'Uniform Passive': 'Pasiva de uniforme'}
def artefacto(a): return next(y for y in ARTES if y['p'] == BASE_P[a['cid']])['name']
def rotulo(a, k, x, lang):
    """El texto del enlace a la skill o al artefacto (enlaceSkill): el slot, o el artefacto con su nivel de estrellas."""
    if k == 'artifact': return f"{artefacto(a)} ({L[lang]['at6']})"
    if k == 'propio': return SLOT_ES.get(x['sl'], x['sl']) if lang == 'es' else x['sl']
    return ROT[lang][k]
def nombre_en(vs): return lambda x: full(x) if any(y is not x and y['name'] == x['name'] for y in vs) else x['name']
def filas(foco, vs, lider, lang):
    """Lo que recibe, como la tabla de la ventana: por stat y condición (lo permanente primero), [efecto (con la condición),
    total (sin topes; «*» si algo solo llega con un artefacto y, si también llega algo sin él, cuánto), [de dónde sale cada
    parte: «quién: skill o artefacto valor», con «*» si es un artefacto]]."""
    nom, lineas = nombre_en(vs), {}
    j, li = ix(vs, foco), (ix(vs, lider) if lider else None)
    for a, art, skills in origenes(foco, vs, lider, lang):
        vistos = {}
        for k, x, fx in skills:
            for f in fx:
                n = vistos.get(f['s'], 0) if k == 'propio' else 0
                if k == 'propio': vistos[f['s']] = n + 1
                p = no_suma(vs, li, ix(vs, a), k, f, j, n)
                cond, txt = condicion(x, f, lang), f['v'] if isinstance(f.get('v'), str) else None
                l = lineas.setdefault((f['s'], cond, txt), dict(s=f['s'], cond=cond, txt=txt, v=[None, None], i=[None, None], sin=False, de=[], rep=True))
                ja = 1 if art else 0
                if not p:   # en el total, solo lo que se le aplica
                    if isinstance(f.get('v'), (int, float)): l['v'][ja] = (l['v'][ja] or 0) + f['v']
                    if f.get('i') is not None: l['i'][ja] = (l['i'][ja] or 0) + f['i']
                    if not art: l['sin'] = True
                    l['rep'] = False
                val = valor(f.get('v'), f.get('i'), lang)
                l['de'].append(f"{nom(a)}: {rotulo(a, k, x, lang)}" + (' ' + val if val else '') + ('*' if art else '')
                               + (' (' + REP[lang]['no'].format(de=ya_de(vs, j, f['s'], p, nom, lang)) + ')' if p else ''))
    out = []
    tot = lambda p: None if p == [None, None] else (p[0] or 0) + (p[1] or 0)
    siempre = {l['s']: tot(l['v']) or 0 for l in lineas.values() if not l['cond']}
    for l in sorted(lineas.values(), key=lambda l: bool(l['cond'])):
        art = not l['rep'] and (l['v'][1] is not None or l['i'][1] is not None or (not l['sin'] and l['v'][0] is None and l['i'][0] is None))
        total = ('' if l['rep'] else valor(l['txt'] if l['txt'] is not None else tot(l['v']), tot(l['i']), lang)) + ('*' if art else '')
        if art and (l['v'][0] is not None or l['i'][0] is not None): total += ' (' + L[lang]['sin_art'].format(x=valor(l['v'][0], l['i'][0], lang)) + ')'
        out.append([tr(l['s'], lang) + (f" ({l['cond']})" if l['cond'] else '') + tope_txt(l['s'], tot(l['v']), bool(l['cond']), siempre.get(l['s'], 0), lang), total, l['de']])
    return out
SKILL_DE = dict(leader='Leader Skill', leader2='Leader Skill', passive='Passive', passive2='Passive', t2='Tier-2 Passive',
                t22='Tier-2 Passive', uniform='Uniform Passive', uniform2='Uniform Passive')
def destino(a, k, x):
    """A dónde lleva el enlace: (cid, uid, pestaña, ancla, lo que se ve resaltado). Un liderazgo, a la Leader Skill;
    un soporte, a la skill con el nombre que le da Leads & Supports o, si no hay, a la de su tipo; el artefacto, al
    bloque del artefacto en Armado."""
    if k == 'artifact':
        return a['cid'], a['uid'] or 'base', 'armado', 'artefacto', artefacto(a)
    sks = SKILLS[a['p']]
    sk = (next((s for s in sks if NOMBRES[s['n']]['en'] == x.get('n')), None) if k not in LID and x.get('n') else None) \
        or next(s for s in sks if s['sl'] == SKILL_DE[k])
    return a['cid'], a['uid'] or 'base', 'skills', 'sk-' + ''.join(ch for ch in sk['sl'].lower() if ch.isalnum()), NOMBRES[sk['n']]['en']
def destinos(foco, vs, lider):
    """Los destinos distintos de los enlaces de lo que recibe, en el orden en que aparecen en la tabla."""
    vistos, out = set(), []
    lineas = {}
    for a, art, skills in origenes(foco, vs, lider):
        for k, x, fx in skills:
            for f in fx:
                lineas.setdefault((f['s'], condicion(x, f, 'es'), f['v'] if isinstance(f.get('v'), str) else None), []).append((a, k, x))
    for clave in sorted(lineas, key=lambda c: bool(c[1])):
        for a, k, x in lineas[clave]:
            d = destino(a, k, x)
            if d not in vistos: vistos.add(d); out.append(d)
    return out
def da(foco, vs, lider, lang):
    """Lo que aporta el foco a los demás, como en su pestaña: por slot, [el enlace (con «si lleva su artefacto») y a quiénes
    si es a los mismos, [efectos (con a quiénes, si no)]]."""
    nom, gs = nombre_en(vs), {}
    i, li = ix(vs, foco), (ix(vs, lider) if lider else None)
    for b in vs:
        if b is foco: continue
        for k, x, fx in recibe(b, foco, foco is lider):
            g = gs.setdefault(k, (x, {}))
            for f in fx:
                e = g[1].setdefault(id(f), (f, [], []))
                p = no_suma(vs, li, i, k, f, ix(vs, b))
                if p: e[2].append((ix(vs, b), [(f['s'], p)]))
                else: e[1].append(b)
    out = []
    for k in [k for k in TIPOS if k in gs]:
        x, efs = gs[k]
        efs = sorted(efs.values(), key=lambda e: x['fx'].index(e[0]))
        a = lambda ms, no: re.sub(r'\s+', ' ', ' → ' + (L[lang]['todos'] if len(ms) == len(vs) else ', '.join(nom(m) for m in ms)) + ya_lo_tienen(vs, no, nom, lang))
        quienes = lambda e: ([m['key'] for m in e[1]], [(j, fs) for j, fs in e[2]])
        iguales = all(quienes(e) == quienes(efs[0]) for e in efs)
        cab = rotulo(foco, k, x, lang) + (f" ({L[lang]['si_art']})" if k == 'artifact' else '') + (a(efs[0][1], efs[0][2]) if iguales else '')
        out.append([cab, [efecto(x, f, lang) + ('' if iguales else a(ms, no)) for f, ms, no in efs]])
    return out
def ventajas(vs, nom, con=None):
    out = []
    for a in vs:
        for b in vs:
            am = LE_GANA.get(b['c']); fu = am and ADV[a['c']].get(am)
            if a is not b and fu and (con is None or con in (a, b)):
                out.append(f"{nom(a)} ({a['c']}) cubre la debilidad de {nom(b)} ({b['c']}) contra {am}" + (' (ventaja menor).' if fu == 'menor' else '.'))
    return out
def strikers(foco, vs, nom):
    cuando = {'ataca': '{p}% al atacar', 'atacado': '{p}% al ser atacado'}
    return [f"{nom(b)} de {nom(a)} ({cuando[c].format(p=p)})" for a in vs for x, p, c in STK.get(a['cid'], [])
            for b in vs if b is not a and b['cid'] == x and (foco is None or foco in (a, b))]
def partes_sinergia(vs, f, li, lang='es'):
    """De dónde salen los puntos para él (vs[f]) sin contexto, como en la ventana: [rótulo con lo que suma, [viñetas]]. El
    liderazgo del líder (vs[li]) y los soportes que lo involucran (A.SOPS: 3 si es Notable, 2 si no), los bonos (no los
    tiene ningún trío de esta prueba: si alguno los tiene, para), las lecturas propias y los strikers con él."""
    nom = nombre_en(vs)
    a_ = lambda bs: L[lang]['todos'] if len(bs) == len(vs) else ', '.join(nom(vs[j]) for j in bs)
    cuenta = lambda i, bs: i == f or f in bs
    if A.bonos_activos(vs): raise SystemExit('el modelo no escribe bonos de equipo: elegí otro trío')
    lid, sop, art = [], [], False
    # cada slot con a quiénes se les aplica algo (si) y a quiénes les llega algo que ya tienen (no), si lo involucra a él; lo que
    # suma (0 si no se le aplica a nadie: «no suma») y el texto desde la flecha
    def linea(i, k, x, p, alc):
        si, no = reparto(vs, li, i, k, x, alc)
        if (not si and not no) or not (cuenta(i, si) or f in [j for j, _ in no]): return None
        pts = p if si and cuenta(i, si) else 0
        return pts, re.sub(r'\s+', ' ', f" → {a_(si)}{ya_lo_tienen(vs, no, nom, lang)} ") + (f'(+{p})' if pts else '· ' + REP[lang]['nada'])
    for k, x, p, alc in (A.SOPS[vs[li]['key']] if li is not None else []):
        if k not in LID: continue
        r = linea(li, k, x, p, alc)
        if r: lid.append((r[0], f'{ROT[lang][k]}{r[1]}'))
    for i, a in enumerate(vs):
        for k, x, p, alc in A.SOPS[a['key']]:
            if k in LID: continue
            r = linea(i, k, x, p, alc)
            if not r: continue
            sop.append((TIPOS.index(k), i, f"{nom(a)}: {rotulo(a, k, x, lang)}{'*' if k == 'artifact' else ''}{r[1]}", r[0]))
            art = art or (k == 'artifact' and r[0] > 0)
    sop.sort(key=lambda s: (s[1], s[0]))
    roles = [r for r in A.ROLES if any(r in v['r'] for v in vs)]
    otras = (['Roles cubiertos (derivados de las skills): ' + ' + '.join(roles) + '. (+1)'] if len(roles) >= 2 else []) \
        + (['Clases distintas: no comparten la misma debilidad. (+1)'] if len({v['c'] for v in vs}) == len(vs) else []) \
        + [x + ' (+1)' for x in ventajas(vs, nom, vs[f])]
    out = []
    if lid: out.append([L[lang]['lider'].format(x=nom(vs[li])) + f" +{sum(p for p, _ in lid)}", [t for _, t in lid]])
    if sop: out.append([L[lang]['sop'] + f" +{sum(s[3] for s in sop)}" + ('*' if art else ''), [s[2] for s in sop]])
    if otras: out.append([L[lang]['otras'] + f' +{len(otras)}', otras])
    st = strikers(vs[f], vs, nom)
    if st: out.append([f"Desempate: {len(st)} striker{'s' if len(st) > 1 else ''}", st])
    return out
def sinergia_ctx(vs, li, lang='es'):
    """La parte «Soportes y bonos de equipo» del puntaje de contexto (enContexto): cada soporte que le llega a otro
    integrante y le sirve, con a quiénes (el artefacto, con su «*»), y cada bono activo que le sirve a alguien, en el
    orden del trío. Devuelve (rótulo con «*» si sumó un artefacto, viñetas)."""
    nom, out, art = nombre_en(vs), [], False
    a_ = lambda ms: L[lang]['todos'] if len(ms) == len(vs) else ', '.join(nom(m) for m in ms)
    for a in vs:
        sp = SOP.get(a['p']) or {}
        for k in TIPOS:
            x = sp.get(k)
            if not x or k in LID: continue
            alc = {b['key'] for b in vs if aplica(x, b) and any(sirve(f, b) for f in x['fx'])}
            si, no = reparto(vs, li, ix(vs, a), k, x, alc)
            if not si and not no: continue
            ms = [vs[j] for j in si]
            if k == 'artifact':
                art = True
                rot = f"{artefacto(a)} ({L[lang]['at6']})*"
            else:
                rot = ROT[lang][k]
            out.append(re.sub(r'\s+', ' ', f"{nom(a)}: {rot} → {a_(ms)}{ya_lo_tienen(vs, no, nom, lang)}") + ('' if si else ' · ' + REP[lang]['nada']))
    cids = {v['cid'] for v in vs}
    for a in vs:
        for b in D0['MFF_BONOS']:
            if b['m'][0] != a['cid'] or not set(b['m']) <= cids: continue
            ms = [x for x in vs if any(sirve({'s': s}, x) for v in b['v'] for s, _ in v)]
            if ms:
                nombre = f"«{b['n']}»" if b.get('n') else 'sin nombre en la wiki'
                out.append(f"Bono de equipo {nombre} ({' + '.join(x['name'] for x in vs if x['cid'] in b['m'])}) → {a_(ms)}")
    return ('Soportes y bonos de equipo +{}' + ('*' if art else '')), out

# ---- lo que se lee de la página ----
LEER = r"""() => {
  const pl = (el) => el ? el.textContent.replace(/\s+/g, ' ').trim() : null, d = document.getElementById('pqdlg');
  const cab = (li) => [...li.childNodes].filter(n => n.nodeName !== 'UL').map(n => n.textContent).join('').replace(/\s+/g, ' ').trim();
  const lista = (ul) => ul ? [...ul.querySelectorAll(':scope > li')].map(li => [cab(li), [...li.querySelectorAll(':scope > ul > li')].map(pl)]) : null;
  const sec = (k) => [...d.querySelectorAll('.pqm-sec')].find(s => pl(s.querySelector(':scope > h3')) === k);
  const panel = d && d.open && d.querySelector('[role="tabpanel"]:not([hidden])');
  if (!panel) return { abierto: false };
  return {
    abierto: d.open, tab: d.querySelector('[role="tab"][aria-selected="true"]').dataset.key,
    titulo: pl(panel.querySelector(':scope > h4')), titulos: [...panel.querySelectorAll(':scope > h4')].map(pl),
    suma: [...panel.querySelectorAll('.pqm-fila:not(.pqm-th)')].map(f => [pl(f.querySelector('.pqm-ef')), pl(f.querySelector('.pqm-tot')),
      [...f.querySelectorAll('.pqm-de1')].map(pl)]),
    leyendas: [...d.querySelectorAll('[role="tabpanel"] .pqley')].filter(p => !p.closest('[hidden]')).map(pl),
    aporta: lista(panel.querySelector(':scope > ul.pqm-lista')),
    nada: [...panel.querySelectorAll(':scope > p.muted')].filter(p => !p.classList.contains('pqley') && !p.classList.contains('pqprob')).map(pl),
    partes: [...d.querySelectorAll('.pqm-parte')].map(p => [pl(p.querySelector(':scope > .pqm-parteh')), [...p.querySelectorAll(':scope > ul > li')].map(cab)]),
    secciones: [...d.querySelectorAll('.pqm-sec > h3')].map(pl),
    ademas: (s => s ? lista(s.querySelector(':scope > ul')) : null)(sec(window.__L.ademas)),
    gana: (s => s ? lista(s.querySelector(':scope > ul')) : null)(sec(window.__L.gana)),
    pierde: (s => s ? lista(s.querySelector(':scope > ul')) : null)(sec(window.__L.pierde)),
  };
}"""
def leer(pg, foco=None, lang='es'):
    pg.evaluate('(l) => { window.__L = l; }', {**L[lang], 'gana': L[lang]['gana'].format(x=foco['name'] if foco else '')})
    return pg.evaluate(LEER)
def trio_card(pg, *cids):
    c = pg.locator('#combos .combo')
    for x in cids: c = c.filter(has=pg.locator(f'.eqfoto[data-cid="{x}"]'))
    return c.first
def buscar_trio(pg, *cids):
    """La tarjeta del trío, en la página en que esté: desde la primera, con «→»."""
    while not trio_card(pg, *cids).count():
        sig = pg.locator('#combos [data-a="eqPagina"]').last
        if sig.is_disabled(): break
        sig.click(); pg.wait_for_timeout(200)
    return trio_card(pg, *cids)
def abrir(pg, card):
    b = card.locator('[data-a="pqAbrir"]'); b.scroll_into_view_if_needed(); b.click()
    pg.wait_for_selector('#pqdlg[open]'); pg.wait_for_timeout(80)
def cerrar(pg):
    if pg.evaluate("!!document.querySelector('#pqdlg[open]')"): pg.keyboard.press('Escape'); pg.wait_for_timeout(80)
def estado(pg): return pg.evaluate('({ ...history.state })')
def cuerpo_y(pg): return pg.evaluate("document.querySelector('#pqdlg .pqm-cuerpo').scrollTop")
FUERA = """(sel) => { const out = []; for (const el of document.querySelectorAll(sel + ' *')) { const r = el.getBoundingClientRect();
  if (r.width && r.right > innerWidth + 0.5) out.push((el.className || el.tagName) + ' ' + Math.round(r.right)); }
  return { doc: document.documentElement.scrollWidth, fuera: [...new Set(out)].slice(0, 5) }; }"""
def captura(pg, ruta):
    pg.locator('#pqdlg').screenshot(path=ruta)

def ficha(pg, nombre, cid, uid=None, tab='equipos'):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid: pg.select_option('select[data-a="uniformSel"]', uid)
    pg.click(f'[data-a="fichaTab"][data-v="{tab}"]')
    if tab == 'equipos': pg.wait_for_selector('#combos .combo', timeout=90000)

def enlace_a(pg, esperado):
    """El primer enlace de la pestaña abierta que lleva a ese destino (ficha, uniforme, pestaña, ancla)."""
    cid, uid, tab, ancla, _ = esperado
    return pg.locator(f'#pqdlg [role="tabpanel"]:not([hidden]) .pqm-de [data-a="irSkill"][data-cid="{cid}"][data-uid="{"" if uid == "base" else uid}"]'
                      f'[data-tab="{tab}"][data-ancla="{ancla}"]').first

def seguir(pg, enlace, esperado, nombre, tarjeta):
    """Toca un enlace de la ventana: ficha, uniforme, pestaña, ancla resaltada y a la vista; «Atrás» vuelve a la lista igual
    (la tarjeta, en el mismo lugar de la pantalla: las fuentes web que llegan tarde pueden mover scrollY y Chrome deja lo que
    se ve donde estaba), con la ventana abierta en la misma pestaña y a la misma altura."""
    enlace.scroll_into_view_if_needed(); pg.wait_for_timeout(50)
    antes = estado(pg); y = pg.evaluate('scrollY'); yd = cuerpo_y(pg); tab = leer(pg)['tab']; arriba = tarjeta().bounding_box()['y']
    enlace.click(); pg.wait_for_selector('.fcab'); pg.wait_for_timeout(150)
    e = estado(pg)
    cid, uid, tabf, ancla, que = esperado
    r = pg.evaluate("""(a) => { const el = document.querySelector('.resaltada'); if (!el) return null;
      const r = el.getBoundingClientRect(), arriba = document.querySelector('.fcab').getBoundingClientRect().bottom;
      return { id: el.id, n: document.querySelectorAll('.resaltada').length, txt: el.textContent, top: r.top, arriba, alto: innerHeight,
               uni: document.querySelector('select[data-a="uniformSel"]').value }; }""", ancla)
    ok(f'{nombre}: abre la ficha de {cid} ({uid}) en {tabf} y cierra la ventana', e['charId'] == cid and e['uniformId'] == uid and e['fichaTab'] == tabf
       and e['n'] == antes['n'] + 1 and r and r['uni'] == uid and not leer(pg)['abierto'], (e['charId'], e['uniformId'], e['fichaTab'], e['n'], antes['n'], r and r['uni']))
    ok(f'{nombre}: resalta {ancla} ({que}) y lo deja a la vista debajo de la cabecera',
       r and r['id'] == ancla and r['n'] == 1 and que in r['txt'] and r['arriba'] - 2 <= r['top'] < r['alto'], r and {k: r[k] for k in ('id', 'top', 'arriba', 'alto')})
    atras = pg.locator('[data-a="atras"]')
    ok(f'{nombre}: hay «Atrás» a la ficha de antes', atras.count() == 1, atras.all_inner_texts())
    atras.click(); pg.wait_for_selector('#pqdlg[open]', timeout=90000); pg.wait_for_timeout(300)
    d = estado(pg)
    ok(f'{nombre}: «Atrás» vuelve a la lista (misma ficha, pestaña, orden, página y altura) con la ventana abierta en la misma pestaña y altura',
       (d['charId'], d['uniformId'], d['fichaTab'], d['eqPagina']) == (antes['charId'], antes['uniformId'], antes['fichaTab'], antes['eqPagina'])
       and abs(tarjeta().bounding_box()['y'] - arriba) < 5 and leer(pg)['tab'] == tab and abs(cuerpo_y(pg) - yd) < 3
       and tarjeta().locator('[data-a="pqAbrir"]').count() == 1,
       (d['charId'], d['fichaTab'], d['eqPagina'], antes['eqPagina'], round(tarjeta().bounding_box()['y']), round(arriba),
        round(pg.evaluate('scrollY')), round(y), leer(pg)['tab'], tab, cuerpo_y(pg), yd))

D = carpeta_datos()
json.dump({'teams': [EQUIPO]}, open(os.path.join(D, 'capa.json'), 'w', encoding='utf-8'), ensure_ascii=False)
srv, url = levantar(D, origen_local())
errores = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(60000)

        # 1. El trío del pedido, en puntos para él.
        ficha(pg, 'Adam Warlock', 'adam-warlock', ADAM['uid'])
        tarjeta1 = lambda: trio_card(pg, 'black-cat', 'jeff-the-land-shark')
        card = tarjeta1()
        lider = card.locator('.combolider').inner_text(); boton = card.locator('[data-a="pqAbrir"]').inner_text()
        abrir(pg, card)
        R = leer(pg)
        PEDIDO = [['Todos los ataques básicos', '+65%'], ['Ignorar esquiva', '+35%'], ['Efecto de todas las mermas', '+40%'],
                  ['Daño básico a villanos', '+75% +0,7% del instinto total* (sin artefactos: +45%)'], ['Daño básico recibido de villanos', '−40%'],
                  ['Ignora la reducción de daño de enemigos que no son jefes', '+10%'], ['Daño básico a héroes', '+10% +0,2% del instinto total*'],
                  ['Daño básico a jefes', '+20% +0,1% del instinto total*'], ['PG', '+20% +0,4% del instinto total*'],
                  ['Elimina todas las mermas (al estar mermado, recarga 20 s, dura 12 s)', '']]
        vs = [ADAM, BC, JEFF]
        ok('1 la tarjeta: líder Black Cat — Queen in Black y el botón «Por qué y C.T.P.»',
           lider == 'Líder: Black Cat — Queen in Black' and boton == 'Por qué y C.T.P.', (lider, boton))
        ok('1 la ventana abre en él: «Lo que recibe Adam Warlock» y «Lo que aporta Adam Warlock»', R['tab'] == ADAM['key']
           and R['titulos'] == ['Lo que recibe Adam Warlock', 'Lo que aporta Adam Warlock'], (R['tab'], R['titulos']))
        ok('1 lo que recibe: el efecto y el total exactos del pedido', [x[:2] for x in R['suma']] == PEDIDO, [x[:2] for x in R['suma']])
        ok('1 lo que recibe es lo del modelo, con de dónde sale cada parte', R['suma'] == filas(ADAM, vs, BC, 'es'), filas(ADAM, vs, BC, 'es'))
        ok('1 la leyenda del *, una sola vez', R['leyendas'] == ['* Solo si el compañero que lo da lleva su artefacto.'], R['leyendas'])
        DE = [['Black Cat: Liderazgo +65%'], ['Black Cat: Liderazgo +35%'], ['Black Cat: Pasiva de Tier-2 +40%'],
              ['Jeff the Land Shark: Pasiva 4★ +45%', 'Black Cat: Persona of Desire (a 6★) +10% +0,2% del instinto total*',
               'Jeff the Land Shark: Baby Land Shark (a 6★) +20% +0,5% del instinto total*'],
              ['Jeff the Land Shark: Pasiva 4★ −40%'], ['Jeff the Land Shark: Pasiva 4★ +10%'],
              ['Black Cat: Persona of Desire (a 6★) +10% +0,2% del instinto total*'], ['Black Cat: Persona of Desire (a 6★) +20% +0,1% del instinto total*'],
              ['Jeff the Land Shark: Baby Land Shark (a 6★) +20% +0,4% del instinto total*'], ['Jeff the Land Shark: Pasiva 4★ (secundaria)']]
        ok('1 de dónde: Black Cat (liderazgo y Tier-2), Jeff (Pasiva 4★ y su secundaria) y sus artefactos, con lo de cada uno',
           [x[2] for x in R['suma']] == DE, [x[2] for x in R['suma']])
        ok('1 lo que aporta él: nada, y lo dice', da(ADAM, vs, BC, 'es') == [] and R['aporta'] is None
           and 'Nada de lo suyo les llega y les sirve a los demás.' in R['nada'], (R['aporta'], R['nada']))
        ok('1 de dónde salen los puntos para él: liderazgo, soportes y lecturas propias, con lo que suma cada uno (el modelo)',
           R['partes'] == partes_sinergia([ADAM, BC, JEFF], 0, 1), (R['partes'], partes_sinergia([ADAM, BC, JEFF], 0, 1)))
        ok('1 las lecturas propias: roles y la ventaja de clase con él',
           next(x for x in R['partes'] if x[0].startswith('Roles'))[1] == ['Roles cubiertos (derivados de las skills): Tanque + Control + Daño + Soporte. (+1)',
                                                                           'Black Cat (Universal) cubre la debilidad de Adam Warlock (Detonación) contra Velocidad (ventaja menor). (+1)'],
           R['partes'])
        largos = pg.evaluate("""() => [...document.querySelectorAll('#pqdlg .pqm-tabla, #pqdlg .pqm-partes, #pqdlg [role="tabpanel"] > ul')]
          .flatMap(x => [...x.querySelectorAll('li, .pqm-fila')]).map(li => [...li.childNodes].filter(n => n.nodeName !== 'UL').map(n => n.textContent).join(''))
          .filter(t => t.includes(' · ') || t.includes('Queen in Black') || t.includes('Guardians of the Galaxy'))""")
        ok('1 en la tabla, las partes y las listas, nada de cadenas con «·» ni nombres completos (van en el title)', not largos, largos)
        titulos = pg.evaluate("() => [...document.querySelectorAll('#pqdlg .pqm-de1 span[title]')].map(s => [s.textContent, s.title])")
        ok('1 el nombre completo, en el title', ['Black Cat', 'Black Cat — Queen in Black'] in titulos and ['Jeff the Land Shark', 'Jeff the Land Shark'] in titulos, titulos)
        captura(pg, f'{CAPT}/porque_1300.png')

        # 2. Los enlaces de lo que recibe y «Atrás».
        ESPERA = destinos(ADAM, vs, BC)
        enlaces = pg.locator('#pqdlg [role="tabpanel"]:not([hidden]) .pqm-de [data-a="irSkill"]')
        textos = [enlaces.nth(i).inner_text() for i in range(enlaces.count())]
        ok('2 un enlace por parte, en el orden de la tabla; seis destinos (la secundaria de Jeff va a su Activa 5, Jeff\'s Cuddle Buddy)',
           len(ESPERA) == 6 and destino(JEFF, 'passive2', SOP[JEFF['p']]['passive2'])[3:] == ('sk-active5', "Jeff's Cuddle Buddy")
           and textos == ['Liderazgo', 'Liderazgo', 'Pasiva de Tier-2', 'Pasiva 4★', 'Persona of Desire', 'Baby Land Shark', 'Pasiva 4★', 'Pasiva 4★',
                          'Persona of Desire', 'Persona of Desire', 'Baby Land Shark', 'Pasiva 4★ (secundaria)'],
           (textos, ESPERA))
        for i, esperado in enumerate(ESPERA):
            seguir(pg, enlace_a(pg, esperado), esperado, f'2 enlace {i + 1}', tarjeta1)
        # Y si en la ficha del compañero se miran sus combinaciones, la lista de Adam se recalcula al volver: la posición y la
        # ventana se aplican cuando termina.
        enlace = enlace_a(pg, ESPERA[0])
        enlace.scroll_into_view_if_needed(); pg.wait_for_timeout(50)
        y, antes, yd, arriba = pg.evaluate('scrollY'), estado(pg), cuerpo_y(pg), tarjeta1().bounding_box()['y']
        enlace.click(); pg.wait_for_selector('.fcab')
        pg.click('[data-a="fichaTab"][data-v="equipos"]'); pg.wait_for_selector('#combos .combo', timeout=90000)
        otra = pg.evaluate("() => document.querySelector('#combos .combo [data-a=\"open\"]').dataset.cid")   # la lista de Black Cat
        pg.click('[data-a="atras"]')
        pg.wait_for_function("() => history.state.charId === 'adam-warlock' && document.querySelector('#combos .combo') && document.querySelector('#pqdlg[open]')",
                             timeout=90000)
        pg.wait_for_timeout(500)
        ok('2 «Atrás» después de mirar las combinaciones de Black Cat: la lista de Adam, recalculada, en su página y con la tarjeta en su lugar, con la ventana',
           otra == 'black-cat' and estado(pg)['eqPagina'] == antes['eqPagina'] and abs(tarjeta1().bounding_box()['y'] - arriba) < 5 and leer(pg)['abierto']
           and abs(cuerpo_y(pg) - yd) < 3, (otra, estado(pg)['eqPagina'], round(tarjeta1().bounding_box()['y']), round(arriba),
                                            round(pg.evaluate('scrollY')), round(y), cuerpo_y(pg), yd))
        cerrar(pg)

        # 3. PvP: Adam + Wasp — Quantumania + Doctor Voodoo — Savage Avengers.
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_timeout(300); pg.wait_for_selector('#combos .combo')
        # la página del trío (desde que los strikers solo desempatan, ya no es la 4): se recorre con «→»
        while not trio_card(pg, 'wasp', 'doctor-voodoo').count():
            sig = pg.locator('#combos [data-a="eqPagina"]').last
            if sig.is_disabled(): break
            sig.click(); pg.wait_for_timeout(250)
        tarjeta3 = lambda: trio_card(pg, 'wasp', 'doctor-voodoo')
        card = tarjeta3()
        PAG = estado(pg)['eqPagina']
        ok(f'3 PvP: el trío está en la página {PAG + 1}, no en la primera', card.count() == 1 and PAG >= 1, PAG)
        lider = card.locator('.combolider').inner_text()
        abrir(pg, card)
        R = leer(pg)
        m = M.evaluar([ADAM, WASP, DV], 'pvp')
        # Con la tabla de valor (4 de octubre de 2026): ataques 2 y defensas 1,5 por integrante.
        ok('3 PvP: el modelo de contexto da líder Wasp y 10,5 + 4 + 3 (y 2 strikers, que desempatan)', m[1] == 1 and m[2] == (10.5, 4, 3, 2) and m[0] == 17.5, m)
        sin_rot, sin_vi = sinergia_ctx([ADAM, WASP, DV], m[1])
        num_es = lambda x: (f'{x:.2f}'.rstrip('0').rstrip('.')).replace('.', ',')
        DET = [['Anti-mermas', ['Wasp (soporte) → a todos']],
               [f'Liderazgo de Wasp +{num_es(m[2][0])}', ['Todos los ataques básicos +30% → a todos (+6)', 'Todas las defensas básicas +20% → a todos (+4,5)']],
               [f'DPS +{num_es(m[2][1])}', ['Adam Warlock (Arena de Equipos: Niche)']],
               [sin_rot.format(num_es(m[2][2])), sin_vi],
               [f'Desempate: {m[2][3]} strikers', ['Adam Warlock de Wasp (22% al atacar)', 'Doctor Voodoo de Wasp (16% al ser atacado)']]]
        ok('3 PvP: una parte por renglón, viñetas, nombres cortos, «a todos» y los números del modelo', R['partes'] == DET, R['partes'])
        ok('3 PvP: los soportes y bonos de equipo dicen qué es cada uno (uno por punto)', len(sin_vi) == m[2][2] and sin_vi, sin_vi)
        tit = pg.evaluate("() => [...document.querySelectorAll('#pqdlg .pqm-partes span[title]')].map(s => s.title)")
        ok('3 PvP: los nombres completos, en el title', 'Wasp — Ant-Man and the Wasp: Quantumania' in tit and
           'Doctor Voodoo — Savage Avengers' in tit, tit)
        ok('3 PvP: el líder de la tarjeta y su liderazgo en lo que recibe Adam', lider == 'Líder: Wasp — Ant-Man and the Wasp: Quantumania'
           and R['suma'] == filas(ADAM, [ADAM, WASP, DV], WASP, 'es') and R['suma'][0][:2] == ['Todos los ataques básicos', '+30%'], R['suma'])
        captura(pg, f'{CAPT}/detalle_pvp_1300.png')
        esperado = destino(WASP, 'leader', SOP[WASP['p']]['leader'])
        ok('3 PvP: el primer enlace de lo que recibe Adam es el liderazgo de Wasp', pg.locator('#pqdlg [role="tabpanel"]:not([hidden]) .pqm-de [data-a="irSkill"]').first
           .evaluate('b => [b.textContent, b.dataset.cid, b.dataset.ancla]') == ['Liderazgo', 'wasp', 'sk-leaderskill'])
        seguir(pg, enlace_a(pg, esperado), esperado, '3 PvP, liderazgo de Wasp', tarjeta3)
        enlace = enlace_a(pg, esperado)
        enlace.scroll_into_view_if_needed(); pg.wait_for_timeout(50); y = pg.evaluate('scrollY'); arriba = tarjeta3().bounding_box()['y']
        enlace.click(); pg.wait_for_timeout(300)
        pg.go_back(); pg.wait_for_selector('#pqdlg[open]', timeout=90000); pg.wait_for_timeout(400)
        ok(f'3 PvP: el volver del navegador también vuelve a la página {PAG + 1}, con la tarjeta en su lugar y con la ventana',
           estado(pg)['eqPagina'] == PAG and estado(pg)['fichaTab'] == 'equipos' and abs(tarjeta3().bounding_box()['y'] - arriba) < 5 and leer(pg)['abierto'],
           (estado(pg)['eqPagina'], round(tarjeta3().bounding_box()['y']), round(arriba), round(pg.evaluate('scrollY')), round(y)))
        cerrar(pg)
        pg.select_option('select[data-a="eqOrden"]', 'foco'); pg.wait_for_timeout(200)

        # 4. Condicionales. 4a: Silver Surfer — Void Knight + Yondu + Invisible Woman (First Steps). Silver Surfer e
        #    Invisible Woman suman lo mismo con su liderazgo y lidera ella, mejor ubicada en la General: el líder del
        #    equipo es uno, desde la lista de cualquiera (Ezequiel, 4 de octubre de 2026; antes lideraba él en su
        #    lista). Cada condicional con su condición y un valor de texto (Barrera, 1 golpe).
        ficha(pg, 'Silver Surfer', 'silver-surfer', SS['uid'])
        card = trio_card(pg, 'yondu', 'invisible-woman')
        lider = card.locator('.combolider').inner_text()
        abrir(pg, card)
        R = leer(pg)
        vs = [SS, YONDU, IW]
        COND = ['Barrera (al recibir un golpe, recarga 5 s, dura 2 s)', 'Elimina todas las mermas (al estar mermado, recarga 20 s, dura 12 s)',
                'Inmunidad a mermas (al estar mermado, recarga 20 s, dura 12 s)']
        ok('4a el líder es Invisible Woman (empata en puntos con él y está mejor en la General)', lider == 'Líder: ' + full(IW), lider)
        ok('4a lo que recibe es lo del modelo con ella de líder, sin topes, lo permanente primero', R['suma'] == filas(SS, vs, IW, 'es')
           and all('(' not in R['suma'][i][0] for i in range(3)), R['suma'])
        ok('4a cada condicional con su condición; un valor de texto (1 golpe)', all(x in [f[0] for f in R['suma']] for x in COND)
           and next(f for f in R['suma'] if f[0] == COND[0])[1] == '1 golpe', R['suma'])
        ok('4a de dónde: primero ella (líder), con su liderazgo', R['suma'][0][2][0].startswith('Invisible Woman: Liderazgo'), R['suma'][0])
        ok('4a lo que aporta él (el modelo)', (R['aporta'] or []) == da(SS, vs, IW, 'es'), (R['aporta'], da(SS, vs, IW, 'es')))
        ok('4a las partes de los puntos para él (el modelo)', R['partes'] == partes_sinergia(vs, 0, 2), (R['partes'], partes_sinergia(vs, 0, 2)))
        cerrar(pg)
        # 4b. Silver Surfer + Yondu + Sleeper: lidera él. Lo permanente (todos los ataques de Yondu) y lo condicional
        #    (los de su liderazgo, al estar mermado) del mismo stat, en renglones aparte.
        SLEEPER = VAR['sleeper::base']
        tarjeta4 = lambda: trio_card(pg, 'yondu', 'sleeper')
        card = buscar_trio(pg, 'yondu', 'sleeper')
        lider = card.locator('.combolider').inner_text()
        abrir(pg, card)
        R = leer(pg)
        vs = [SS, YONDU, SLEEPER]
        COND = [['Todos los ataques básicos', '+35%'], ['Todos los ataques básicos (al estar mermado, recarga 20 s, dura 12 s)', '+30%'],
                ['Todas las defensas básicas (al estar mermado, recarga 20 s, dura 12 s)', '+30%'],
                ['Elimina todas las mermas (al estar mermado, recarga 20 s, dura 12 s)', '']]
        ok('4b el líder es él', lider == 'Líder: Silver Surfer — Void Knight', lider)
        ok('4b lo que recibe es lo del modelo, sin topes, lo permanente primero', R['suma'] == filas(SS, vs, SS, 'es')
           and '(' not in R['suma'][0][0], R['suma'])
        ok('4b lo permanente y lo condicional del mismo stat, aparte; cada condicional con su condición',
           all(x in [f[:2] for f in R['suma']] for x in COND) and [f[:2] for f in R['suma']].index(COND[0]) < [f[:2] for f in R['suma']].index(COND[1]), R['suma'])
        # Desde el 5 de octubre de 2026 (efectos sin valor, una vez), su anti-mermas no se le suma a Sleeper, que lo tiene propio (su
        # Pasiva 4★ secundaria): los efectos de su liderazgo no van a los mismos y cada uno dice a quiénes.
        ok('4b lo que aporta él: su liderazgo (el modelo); el anti-mermas, a Yondu, porque Sleeper ya lo tiene propio, y lo demás a los dos',
           (R['aporta'] or []) == da(SS, vs, SS, 'es') and R['aporta'][0][0] == 'Liderazgo'
           and R['aporta'][0][1][0].endswith('→ Yondu (Sleeper ya lo tiene propio (Pasiva 4★ (secundaria)))')
           and all(x.endswith('→ Yondu, Sleeper') for x in R['aporta'][0][1][1:]), R['aporta'])
        esperado = destino(SS, 'leader', SOP[SS['p']]['leader'])
        seguir(pg, enlace_a(pg, esperado), esperado, '4b su propio liderazgo (otra entrada del historial)', tarjeta4)
        cerrar(pg)

        # 5. «Cómo entraría»: Jeff en Black Cat + Doctor Voodoo + Thor.
        ficha(pg, 'Jeff the Land Shark', 'jeff-the-land-shark')
        tarjeta5 = lambda: pg.locator('.card.eqsug', has_text=EQUIPO['name']).first
        card = tarjeta5()
        ok('5 la tarjeta: entra por Thor y mejora (14 → 23)', 'en lugar de Thor' in card.inner_text() and card.locator('.eqpts b').inner_text() == '23'
           and card.locator('.eqdelta').inner_text() == '+9', card.inner_text().replace('\n', ' | ')[:200])
        abrir(pg, card)
        R = leer(pg, JEFF)
        nuevo = [BC, DV, JEFF]
        ok('5 lo que recibe Jeff es lo del modelo, con Black Cat de líder', R['suma'] == filas(JEFF, nuevo, BC, 'es')
           and R['titulo'] == 'Lo que recibe Jeff the Land Shark' and R['tab'] == JEFF['key'], R['suma'])
        nom = nombre_en(nuevo)
        ok('5 lo que aporta él (el modelo)', R['aporta'] == da(JEFF, nuevo, BC, 'es'), (R['aporta'], da(JEFF, nuevo, BC, 'es')))
        ok('5 lo que se gana, fuera de lo suyo: la ventaja', R['gana'] == [[x, []] for x in ventajas(nuevo, nom, JEFF)], R['gana'])
        viejo = [BC, DV, THOR]
        lv = viejo[A.lider_sin_contexto(viejo)]    # el líder del equipo de antes (la misma regla)
        perdido = [[f"{x[0][0]}: {ROT['es'][x[1]]}" + (f" ({L['es']['si_art']})" if x[1] == 'artifact' else '') + ' → Thor', x[2]]
                   for x in [((a['name'],), k, [efecto(sx, f, 'es') for f in fx]) for a in (BC, DV) for k, sx, fx in recibe(THOR, a, False)]
                   + [((lv['name'],), k, [efecto(sx, f, 'es') for f in fx]) for k, sx, fx in recibe(THOR, lv, True) if k in LID]]
        ok('5 lo que se pierde: lo que le llegaba a Thor, con el mismo criterio', R['pierde'] == perdido and R['secciones'][-2] == 'Se pierde', R['pierde'])
        esperado = destino(DV, 't2', SOP[DV['p']]['t2'])
        seguir(pg, enlace_a(pg, esperado), esperado, '5 la Tier-2 de Doctor Voodoo', tarjeta5)
        cerrar(pg)

        # 6. Inglés.
        ficha(pg, 'Adam Warlock', 'adam-warlock', ADAM['uid'])
        pg.click('[data-a="lang"]'); pg.wait_for_selector('#combos .combo', timeout=90000)
        card = trio_card(pg, 'black-cat', 'jeff-the-land-shark')
        boton = card.locator('[data-a="pqAbrir"]').inner_text()
        abrir(pg, card)
        R, vs = leer(pg, None, 'en'), [ADAM, BC, JEFF]
        ok('6 inglés: el botón, los títulos y lo que recibe, del modelo', boton == 'Why and C.T.P.' and R['titulos'] == ['What Adam Warlock gets', 'What Adam Warlock gives']
           and R['suma'] == filas(ADAM, vs, BC, 'en') and R['leyendas'] == [L['en']['ley']], (boton, R['titulos'], R['suma'][:2]))
        ok('6 inglés: «Basic Damage Dealt to Villains +75% +0.7% of total Instinct* (without artifacts: +45%)» y la condición',
           ['Basic Damage Dealt to Villains', '+75% +0.7% of total Instinct* (without artifacts: +45%)'] in [f[:2] for f in R['suma']]
           and ['Remove All Debuffs (when Debuffed, cooldown 20 s, lasts 12 s)', ''] in [f[:2] for f in R['suma']], R['suma'])
        tx = pg.locator('#pqdlg').inner_text()
        resto = [x for x in ('Lo que recibe', 'De dónde', 'Además', 'Liderazgo', 'Artefacto de', 'a todos', 'instinto', 'al recibir', 'Soportes') if x in tx]
        ok('6 inglés: sin restos en castellano en la ventana', not resto, resto)
        cerrar(pg)
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_timeout(300); pg.wait_for_selector('#combos .combo')
        abrir(pg, pg.locator('#combos .combo').first)
        det = leer(pg, None, 'en')['partes']
        sd = json.dumps(det, ensure_ascii=False)
        ok('6 inglés: el detalle de PvP', det[0][0] == 'Debuff removal' and any("'s leadership +" in x[0] for x in det)
           and not any(w in sd for w in ('a todos', 'Liderazgo', '(soporte)', '(liderazgo)')), det)
        cerrar(pg)
        pg.select_option('select[data-a="eqOrden"]', 'foco'); pg.wait_for_selector('#combos .combo')
        pg.click('[data-a="lang"]'); pg.wait_for_selector('#combos .combo', timeout=90000)
        ok('sin errores de página ni de consola', not errores, errores[:3])
        b.close()

        # 7. Celular.
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(60000)
        ficha(pg, 'Adam Warlock', 'adam-warlock', ADAM['uid'])
        abrir(pg, trio_card(pg, 'black-cat', 'jeff-the-land-shark'))
        r = pg.evaluate(FUERA, '#pqdlg')
        ok('7 celular: la ventana del trío, con lo que recibe, no se sale', r['doc'] <= 390 and not r['fuera'], r)
        pg.screenshot(path=f'{CAPT}/porque_390.png')
        cerrar(pg)
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_timeout(300); pg.wait_for_selector('#combos .combo')
        abrir(pg, pg.locator('#combos .combo').first)
        r = pg.evaluate(FUERA, '#pqdlg')
        ok('7 celular: la ventana de PvP (el detalle y lo que recibe) no se sale', r['doc'] <= 390 and not r['fuera'], r)
        cerrar(pg)
        ficha(pg, 'Jeff the Land Shark', 'jeff-the-land-shark')
        abrir(pg, pg.locator('.card.eqsug').first)
        r = pg.evaluate(FUERA, '#pqdlg')
        ok('7 celular: la ventana de «Cómo entraría» no se sale', r['doc'] <= 390 and not r['fuera'], r)
        ok('sin errores de página ni de consola (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
