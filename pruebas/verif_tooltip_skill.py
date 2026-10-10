"""«Cómo funciona» de una skill (carril K): al tocar la cabecera o un renglón de una skill en la pestaña Skills
de la ficha se abre un popover anclado a lo tocado (en el celular, una hoja inferior) con cinco secciones:
cómo funciona, cuándo-cuánto-a quién, texto del juego, certeza y fuentes, y diferencias con el coreano.

Casos (cada uno contra un modelo armado acá desde data.js, sin app.js):
  1. Angela — Asgard's Assassin, pasiva de uniforme: el marcador ($HEROSUBTYPE1) resuelto por Leads & Supports.
  2. Doctor Voodoo — Savage Avengers, Tier-2: un efecto al equipo y dos para él.
  3. Silver Surfer — Void Knight, liderazgo: se activa al estar mermado (recarga y duración).
  4. Silver Surfer — Void Knight, pasiva de uniforme: Superarmadura, término del glosario que difiere del coreano.
  5. Angela — Asgard's Assassin, Activa 3: cuatro etapas, abierta desde un renglón y desde una fila de daño.
  6. Beast — Age of Apocalypse, pasiva de uniforme: sin efectos (los avisos).
Para cada uno: las cinco secciones con su contenido (o el aviso), la ubicación, el cierre con Esc (el foco
vuelve a la skill), en español y en inglés, y sin errores de página ni de consola. Con Doctor Voodoo, además:
tocar afuera, el teclado (Enter abre, el foco queda adentro con Tab y Shift+Tab, Esc lo devuelve), el mismo
disparador lo cierra, otra skill lo cambia, ← y → no cambian de personaje, abrir y cerrar no abre otra entrada
del historial ni pliega lo que estaba abierto ni mueve la página, encima de la skill crece hacia arriba, y
«Atrás» con el popover abierto. En el celular (390 px): hoja inferior sin desbordes, el fondo la cierra.
Capturas: capturas/tooltip_1300.png y capturas/tooltip_390.png (Tier-2 de Doctor Voodoo)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

CAPTURAS = SALIDA
os.makedirs(CAPTURAS, exist_ok=True)
ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_TABLAS', 'MFF_ANALISIS', 'MFF_CATALOGO', 'MFF_GLOSARIO',
             'MFF_SOPORTES', 'MFF_VOCAB_EN')
TB, CAT, GLO, AN, SK, VOC = D['MFF_TABLAS'], D['MFF_CATALOGO'], D['MFF_GLOSARIO'], D['MFF_ANALISIS'], D['MFF_SKILLS'], D['MFF_VOCAB_EN']
PJ = {c['id']: c for c in D['MFF_SEED_CHARACTERS']}
GOLPE = next(i for i, e in enumerate(CAT['efectos']) if e['id'] == 'golpe')

# Textos de la interfaz que la prueba espera (los de la tabla de idioma de app.js).
UI = {
    'es': {'secs': ['Cómo funciona', 'Cuándo, cuánto, a quién', 'Texto del juego', 'Certeza y fuentes', 'Diferencias entre idiomas (el coreano es el original)'],
           'd': {'e': 'Para él', 'q': 'Para el equipo', 'r': 'Contra el rival', 'i': 'Para sus invocaciones'},
           'ko_no': 'En coreano: los datos no traen el texto de las skills en coreano.',
           'ko_sin': 'Tampoco tiene términos del glosario del juego.', 'vacia': 'La fuente no publica efectos para esta skill.',
           'dif_sin': 'No tiene términos del glosario del juego: no hay con qué comparar.',
           'dif_nada': 'Sus términos del glosario del juego dicen lo mismo en inglés y en coreano.',
           'sin_cond': 'sin condición: la fuente no publica una activación', 'al_usar': 'al usarla',
           'sin_recarga': 'no tiene (la fuente pone 0 s)', 'dura': 'dura', 'texto': 'los publica thanosvibs (API de skills)',
           'activa': 'Se activa:', 'recarga': 'Recarga:', 'etapa': 'Etapa', 'unspec': 'sin especificar', 'errores': 'Lo que el inglés traduce mal'},
    'en': {'secs': ['How it works', 'When, how much, to whom', 'Game text', 'Certainty and sources', 'Differences between languages (Korean is the original)'],
           'd': {'e': 'For itself', 'q': 'For the team', 'r': 'Against the foe', 'i': 'For its summons'},
           'ko_no': 'In Korean: the data has no Korean text for skills.',
           'ko_sin': 'It has no game glossary terms either.', 'vacia': 'The source publishes no effects for this skill.',
           'dif_sin': 'It has no game glossary terms: there is nothing to compare.',
           'dif_nada': 'Its game glossary terms say the same in English and in Korean.',
           'sin_cond': 'no condition: the source publishes no activation', 'al_usar': 'when used',
           'sin_recarga': 'none (the source says 0 s)', 'dura': 'lasts', 'texto': 'published by thanosvibs (skills API)',
           'activa': 'Activates:', 'recarga': 'Cooldown:', 'etapa': 'Stage', 'unspec': 'unspecified', 'errores': 'What the English gets wrong'},
}

# ---------------------------------------------------------------------------- modelo (aparte de app.js)
def rellenar(patron, nums):
    nums = list(nums or []); i = [0]
    def uno(_):
        if i[0] < len(nums): i[0] += 1; return str(nums[i[0] - 1])
        return '#'
    return re.sub('#', uno, patron)

def lado(fila, lang):
    return fila['en'] if lang == 'en' or fila.get('es') is None else fila['es']

def texto_efecto(f, lang):
    """El texto de un efecto en un idioma, en un renglón, con los marcadores como los resuelve la app."""
    s = rellenar(lado(TB['desc'][f['p']], lang), f.get('v'))
    s = ' '.join(x.strip() for x in re.split(r'<br\s*/?>', s, flags=re.I) if x.strip())
    s = s.replace('$TIME', f"{f['d']} s" if 'd' in f else UI[lang]['unspec']).replace('$TICK', f"{f['t']} s" if 't' in f else UI[lang]['unspec'])
    grupo = (f['g'] if lang == 'es' else VOC[f['g']]) if 'g' in f else None
    return re.sub(r'\$HERO(?:SUBTYPE|CLASS)\d*', lambda m: grupo or UI[lang]['unspec'], s)

def entradas(p, si):
    """Las entradas de «Cómo funciona»: las del análisis con fuentes en la skill, más el golpe, en el orden de la skill."""
    out = []
    for i, (ie, d, obj, fuentes) in enumerate(AN[p]['fx']):
        fs = [s for s in fuentes if s[0] == si]
        if fs: out.append({'ie': ie, 'd': d, 'obj': obj, 'fs': fs})
    golpe = [[si, ti, fi] for ti, st in enumerate(SK[p][si]['st']) for fi, f in enumerate(st['fx']) if 'pi' in TB['desc'][f['p']]]
    if golpe: out.append({'ie': GOLPE, 'd': 'r', 'obj': None, 'fs': golpe})
    return sorted(out, key=lambda x: min(t * 1000 + f for _, t, f in x['fs']))

def terminos(es):
    ids = {CAT['efectos'][x['ie']]['id'] for x in es}
    return [y for y in GLO['terminos'] if ids & set(y['efectos'])]

def activacion(sk, lang):
    acs = [st.get('ac') for st in sk['st']]
    if acs and all(a is not None for a in acs) and len(set(acs)) == 1:
        st = sk['st'][0]
        return rellenar(lado(TB['act'][st['ac']], lang), st.get('av'))
    if all(a is None for a in acs):
        return UI[lang]['al_usar'] if sk['sl'].startswith('Active') else UI[lang]['sin_cond']
    return None

def plano(s):
    return re.sub(r'\s+', ' ', s or '').strip()

# ---------------------------------------------------------------------------- casos
def caso(cid, uni, slot, foco=None):
    u = next(x for x in PJ[cid]['uniforms'] if x['name'] == uni)
    p = u['p']; si = next(i for i, sk in enumerate(SK[p]) if sk['sl'] == slot)
    return {'cid': cid, 'uid': u['id'], 'p': p, 'si': si, 'sk': SK[p][si], 'foco': foco, 'nombre': f'{PJ[cid]["name"]} — {uni}, {slot}'}

ANGELA_UNI = caso('angela', "Asgard's Assassin", 'Uniform Passive')
VOODOO_T2 = caso('doctor-voodoo', 'Savage Avengers', 'Tier-2 Passive')
SURFER_LID = caso('silver-surfer', 'Void Knight', 'Leader Skill')
SURFER_UNI = caso('silver-surfer', 'Void Knight', 'Uniform Passive')
ANGELA_A3 = caso('angela', "Asgard's Assassin", 'Active 3', foco=(2, 1))     # etapa 3, Parálisis
BEAST_UNI = caso('beast', 'Age of Apocalypse', 'Uniform Passive')
CASOS = [ANGELA_UNI, VOODOO_T2, SURFER_LID, SURFER_UNI, ANGELA_A3, BEAST_UNI]

# Lo que el modelo dice de cada caso (para no depender solo de la app al chequear)
ok('modelo: Angela, el marcador de la pasiva de uniforme lo resolvió Leads & Supports',
   [(f.get('g'), f.get('gs')) for st in ANGELA_UNI['sk']['st'] for f in st['fx']] == [('Supervillano', 'l')])
ok('modelo: Doctor Voodoo, la Tier-2 va al equipo y a él', sorted({x['d'] for x in entradas(VOODOO_T2['p'], VOODOO_T2['si'])}) == ['e', 'q'])
ok('modelo: Silver Surfer, el liderazgo se activa al estar mermado', activacion(SURFER_LID['sk'], 'es') == 'al estar mermado')
ok('modelo: la pasiva de uniforme de Silver Surfer tiene un término que difiere',
   any(y.get('difiere') for y in terminos(entradas(SURFER_UNI['p'], SURFER_UNI['si']))))
ok('modelo: la Activa 3 de Angela tiene 4 etapas', len(ANGELA_A3['sk']['st']) == 4)
ok('modelo: la pasiva de uniforme de Beast AoA no tiene efectos', not any(st['fx'] for st in BEAST_UNI['sk']['st']))

# ---------------------------------------------------------------------------- en la página
def abrir_ficha(pg, c):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', PJ[c['cid']]['name']); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{c["cid"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    pg.select_option('select[data-a="uniformSel"]', c['uid']); pg.wait_for_timeout(150)
    pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(200)

def selector(c, ti=None, fi=None):
    if ti is None: return f'#skt-{c["si"]}'
    return f'.skill [data-a="skTip"][data-si="{c["si"]}"][data-st="{ti}"][data-fx="{fi}"]'

def llevar(pg, sel, y):
    """Deja lo que se va a tocar a la altura y de la ventana."""
    pg.evaluate("([s, y]) => { const el = document.querySelector(s); window.scrollTo({ top: el.getBoundingClientRect().top + scrollY - y, behavior: 'instant' }); }", [sel, y])
    pg.wait_for_timeout(80)

def abierto(pg): return pg.locator('#skpop').count() == 1

def secciones(pg):
    return pg.evaluate("""() => [...document.querySelectorAll('#skpop section.tipsec')].map(s => ({
        k: s.dataset.sec, h: s.querySelector('h4').textContent.trim(), txt: s.textContent.replace(/\\s+/g, ' ').trim(),
        resumenes: [...s.querySelectorAll(':scope > details.tipef > summary')].map(x => x.textContent.replace(/\\s+/g, ' ').trim()),
        abiertos: [...s.querySelectorAll(':scope > details.tipef')].map(x => x.open) }))""")

def ubicacion(pg, sel_ancla):
    return pg.evaluate("""(s) => { const a = (s.startsWith('#skt-') ? document.querySelector(s).closest('.top') : document.querySelector(s)).getBoundingClientRect();
        const p = document.getElementById('skpop').getBoundingClientRect(), techo = document.querySelector('.fcab').getBoundingClientRect().bottom;
        return { a: [a.top, a.bottom], p: [p.top, p.bottom, p.left, p.right], techo, alto: innerHeight, ancho: document.documentElement.clientWidth,
                 docw: document.documentElement.scrollWidth }; }""", sel_ancla)

def chequear_contenido(pg, c, lang, etiqueta):
    U = UI[lang]; es = entradas(c['p'], c['si']); ts = terminos(es); sk = c['sk']
    S = {s['k']: s for s in secciones(pg)}
    ok(f'{etiqueta}: las cinco secciones, en orden y con su título', [s['k'] for s in secciones(pg)] == ['como', 'cuando', 'texto', 'certeza', 'coreano']
       and [S[k]['h'] for k in ('como', 'cuando', 'texto', 'certeza', 'coreano')] == U['secs'], [s['h'] for s in secciones(pg)])
    titulo = plano(pg.locator('#skpop-t').text_content())
    nom = TB['name'][sk['n']]
    ok(f'{etiqueta}: el título nombra la skill', lado(nom, lang) in titulo and nom['en'] in titulo, titulo)
    # 1. Cómo funciona: una entrada por efecto, en orden, con su destino (y los aliados si es al equipo)
    if es:
        esperados = []
        for x in es:
            e = CAT['efectos'][x['ie']]
            r = f"{e[lang]} {U['d'][x['d']]}" + (f" → {lado(TB['tgt'][x['obj']], lang)}" if x['d'] == 'q' else '')
            esperados.append(r)
        res = S['como']['resumenes']
        ok(f'{etiqueta}: «Cómo funciona», un efecto por renglón con a quién le llega', len(res) == len(esperados)
           and all(r.startswith(e) for r, e in zip(res, esperados)), list(zip(res, esperados))[:6])
    else:
        ok(f'{etiqueta}: «Cómo funciona» avisa que no hay efectos', U['vacia'] in S['como']['txt'], S['como']['txt'][:120])
    # 2. Cuándo, cuánto, a quién
    act = activacion(sk, lang)
    tx = S['cuando']['txt']
    rec = f"{sk['cd']} s" if sk.get('cd') else U['sin_recarga'] if sk.get('cd') == 0 else None
    ok(f'{etiqueta}: «Cuándo, cuánto, a quién» dice la activación y la recarga',
       (act is None or f"{U['activa']} {act}" in tx) and (rec is None or f"{U['recarga']} {rec}" in tx), (act, rec, tx[:200]))
    fxs = [f for st in sk['st'] for f in st['fx']]
    faltan = [texto_efecto(f, lang) for f in fxs if texto_efecto(f, lang) not in tx]
    duras = [f"{U['dura']} {f['d']} s" for f in fxs if 'd' in f]
    ok(f'{etiqueta}: cada efecto con su texto (los números) y su duración', not faltan and all(d in tx for d in duras), (faltan[:2], duras[:3]))
    if len(sk['st']) > 1:
        ok(f'{etiqueta}: una lista por etapa', all(f"{U['etapa']} {i + 1}" in tx for i in range(len(sk['st']))))
    if not fxs:
        ok(f'{etiqueta}: «Cuándo» avisa que no hay efectos', U['vacia'] in tx)
    # 3. Texto del juego: inglés y español, y el aviso del coreano con sus términos
    tt = S['texto']['txt']
    faltan = [texto_efecto(f, l) for l in ('en', 'es') for f in fxs if texto_efecto(f, l) not in tt]
    ok(f'{etiqueta}: «Texto del juego» en inglés y en español, tal cual', not faltan and nom['en'] in tt and nom['es'] in tt, faltan[:2])
    ok(f'{etiqueta}: el coreano: el aviso de que no hay y sus términos (o que no tiene)', U['ko_no'] in tt
       and (all(f"{y[lang]}: {y['ko']}" in tt for y in ts) if ts else U['ko_sin'] in tt), [f"{y[lang]}: {y['ko']}" for y in ts])
    # 4. Certeza y fuentes
    ct = S['certeza']['txt']
    lect = [CAT['efectos'][x['ie']] for x in es]
    ok(f'{etiqueta}: «Certeza y fuentes»: el texto es de thanosvibs, con su chip, y cada lectura con su certeza',
       U['texto'] in ct and 'THANO$VIB$ — Characters' in ct and all(e[lang] in ct for e in lect)
       and pg.locator('#skpop section[data-sec="certeza"] .cert').count() >= 1 + len({e['id'] for e in lect}), ct[:160])
    # 5. Diferencias entre idiomas (el coreano es el original)
    ko = S['coreano']['txt']; dif = [y for y in ts if y.get('difiere')]
    if dif:
        errs = [e for e in GLO['errores'] if any(y.get('error') == e['id'] for y in dif)]
        ok(f'{etiqueta}: «Diferencias entre idiomas (el coreano es el original)»: cada término que difiere y el error del inglés',
           all(y[lang] in ko and y['difiere'][lang] in ko for y in dif) and all(e['titulo'][lang] in ko for e in errs)
           and (not errs or U['errores'] in ko), [y['id'] for y in dif])
    else:
        ok(f'{etiqueta}: «Diferencias entre idiomas (el coreano es el original)» avisa por qué no hay', (U['dif_nada'] if ts else U['dif_sin']) in ko, ko[:120])
    return S

errores, avisos = [], []
def escuchar(pg):
    pg.on('pageerror', lambda e: errores.append(str(e)))
    pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' else (avisos.append(m.text) if m.type == 'warning' else None))

D_ = carpeta_datos()
srv, url = levantar(D_, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); escuchar(pg)
        pg.goto(url); pg.wait_for_selector('.ccard')

        # -------------------------------------------------- cada caso, en español
        for c in CASOS:
            abrir_ficha(pg, c)
            et = c['nombre']
            ti, fi = c['foco'] or (None, None)
            sel = selector(c, ti, fi)
            llevar(pg, sel, 300)
            y0 = pg.evaluate('scrollY')
            pg.click(sel); pg.wait_for_timeout(200)
            ok(f'{et}: se abre', abierto(pg) and pg.get_attribute(f'#skt-{c["si"]}', 'aria-expanded') == 'true')
            ok(f'{et}: abrir no mueve la página', abs(pg.evaluate('scrollY') - y0) < 2, (pg.evaluate('scrollY'), y0))
            ok(f'{et}: el foco queda adentro', pg.evaluate("document.getElementById('skpop').contains(document.activeElement)"))
            u = ubicacion(pg, sel)
            ok(f'{et}: anclado debajo de lo tocado, dentro de la ventana y sin desbordar', u['p'][0] >= u['a'][1] - 1 and u['p'][0] - u['a'][1] < 20
               and u['p'][1] <= u['alto'] + 1 and u['p'][2] >= 0 and u['p'][3] <= u['ancho'] and u['docw'] <= u['ancho'], u)
            S = chequear_contenido(pg, c, 'es', et)
            if c['foco']:
                vis = pg.evaluate("""() => { const p = document.getElementById('skpop'), f = p.querySelector('details.tipef.foco');
                    if (!f) return null; const a = f.getBoundingClientRect(), b = p.getBoundingClientRect();
                    return { open: f.open, txt: f.querySelector('summary').textContent.replace(/\\s+/g, ' ').trim(), dentro: a.top >= b.top - 1 && a.top < b.bottom - 20,
                             linea: !!p.querySelector('section[data-sec="cuando"] li.tipfx.foco') }; }""")
                foco_ie = [x for x in entradas(c['p'], c['si']) if [c['si'], ti, fi] in x['fs']]
                ok(f'{et}: abierto en el efecto tocado: ese efecto, desplegado, a la vista y marcado también en «Cuándo»',
                   vis and vis['open'] and vis['txt'].startswith(CAT['efectos'][foco_ie[0]['ie']]['es']) and vis['dentro'] and vis['linea'], vis)
            pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
            ok(f'{et}: Esc lo cierra y el foco vuelve a la skill', not abierto(pg)
               and pg.evaluate('document.activeElement && document.activeElement.id') == f'skt-{c["si"]}'
               and pg.get_attribute(f'#skt-{c["si"]}', 'aria-expanded') == 'false')

        # -------------------------------------------------- Activa 3 de Angela: una fila de daño abre en el golpe
        c = ANGELA_A3; abrir_ficha(pg, c)
        sel = selector(c, 3, 0); llevar(pg, sel, 300); pg.click(sel); pg.wait_for_timeout(200)
        f = pg.evaluate("() => { const f = document.querySelector('#skpop details.tipef.foco'); return f && [f.open, f.querySelector('summary').textContent.replace(/\\s+/g, ' ').trim()]; }")
        ok('Activa 3: una fila de daño abre en «Daño de la skill», contra el rival', f and f[0] and f[1].startswith('Daño de la skill Contra el rival'), f)
        pg.keyboard.press('Escape')

        # -------------------------------------------------- Doctor Voodoo: tocar afuera, teclado, historial, atrás
        c = VOODOO_T2; abrir_ficha(pg, c)
        # la leyenda de las rotaciones, abierta: no se tiene que plegar
        pg.evaluate("document.querySelector('#fcuerpo details.usgrupo').open = true")
        sel = selector(c); llevar(pg, sel, 300)
        n0, largo0, y0 = pg.evaluate('history.state.n'), pg.evaluate('history.length'), pg.evaluate('scrollY')
        pg.click(sel); pg.wait_for_timeout(150)
        pg.click('.fcab h1'); pg.wait_for_timeout(150)
        ok('tocar afuera lo cierra y el foco vuelve a la skill', not abierto(pg) and pg.evaluate('document.activeElement.id') == f'skt-{c["si"]}')
        ok('abrir y cerrar no abre otra entrada del historial, no pliega lo abierto ni mueve la página',
           pg.evaluate('history.state.n') == n0 and pg.evaluate('history.length') == largo0 and abs(pg.evaluate('scrollY') - y0) < 2
           and pg.evaluate("document.querySelector('#fcuerpo details.usgrupo').open"), (pg.evaluate('history.state.n'), n0, pg.evaluate('scrollY'), y0))
        # el botón de cerrar
        pg.click(sel); pg.wait_for_timeout(150); pg.click('#skpop [data-a="tipCerrar"]'); pg.wait_for_timeout(100)
        ok('el botón ✕ lo cierra y devuelve el foco', not abierto(pg) and pg.evaluate('document.activeElement.id') == f'skt-{c["si"]}')
        # el mismo disparador lo cierra; otra skill lo cambia
        pg.click(sel); pg.wait_for_timeout(150); pg.click(sel); pg.wait_for_timeout(150)
        ok('tocar otra vez la misma skill lo cierra', not abierto(pg))
        pg.click(sel); pg.wait_for_timeout(150)
        otra = f'#skt-{c["si"] - 1}'; pg.click(otra); pg.wait_for_timeout(150)     # la de arriba: el popover no la tapa
        tit = plano(pg.locator('#skpop-t').text_content()) if abierto(pg) else ''
        ok('tocar otra skill abre la de esa', abierto(pg) and TB['name'][SK[c['p']][c['si'] - 1]['n']]['en'] in tit
           and pg.get_attribute(sel, 'aria-expanded') == 'false' and pg.get_attribute(otra, 'aria-expanded') == 'true', tit)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        # tocar la cabecera fuera del nombre (en su margen derecho) también lo abre
        llevar(pg, sel, 300)
        caja = pg.locator(f'#skt-{c["si"]}').locator('xpath=..').bounding_box()
        pg.mouse.click(caja['x'] + caja['width'] - 5, caja['y'] + caja['height'] / 2); pg.wait_for_timeout(150)
        ok('tocar la cabecera (fuera del nombre) también lo abre', abierto(pg))
        # ← y → no cambian de personaje con el popover abierto
        cid0 = pg.evaluate('history.state.charId')
        pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(250)
        ok('← y → no cambian de personaje con el popover abierto', abierto(pg) and pg.evaluate('history.state.charId') == cid0)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        # teclado: Enter abre, Tab y Shift+Tab no salen, Esc devuelve el foco
        pg.focus(sel); pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
        n_foc = pg.evaluate("[...document.querySelectorAll('#skpop button, #skpop a[href], #skpop summary')].filter(x => x.getClientRects().length).length")
        adentro = []
        for _ in range(n_foc + 3):
            pg.keyboard.press('Tab'); adentro.append(pg.evaluate("document.getElementById('skpop').contains(document.activeElement) && document.activeElement !== document.getElementById('skpop')"))
        for _ in range(4):
            pg.keyboard.press('Shift+Tab'); adentro.append(pg.evaluate("document.getElementById('skpop').contains(document.activeElement)"))
        ok('teclado: Enter lo abre y Tab y Shift+Tab dan la vuelta adentro', abierto(pg) and all(adentro), (n_foc, adentro))
        pg.keyboard.press('Tab')   # al primer resumen o al ✕: Enter en un resumen lo despliega
        foco = pg.evaluate("document.activeElement.tagName")
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        ok('teclado: Esc lo cierra y el foco vuelve a la skill', not abierto(pg) and pg.evaluate('document.activeElement.id') == f'skt-{c["si"]}', foco)
        # encima de la skill, si abajo no entra; con una skill larga, del alto que hay
        llevar(pg, sel, 820); pg.click(sel); pg.wait_for_timeout(200)
        u = ubicacion(pg, sel)
        ok('cerca del borde de abajo se abre encima de la skill, bajo la cabecera fija', u['p'][1] <= u['a'][0] + 1 and u['a'][0] - u['p'][1] < 20
           and u['p'][0] >= u['techo'] - 1, u)
        pg.evaluate("window.scrollBy({ top: 120, behavior: 'instant' })"); pg.wait_for_timeout(150)
        u3 = ubicacion(pg, sel)
        ok('se mueve con la página', abs((u3['a'][0] - u3['p'][1]) - (u['a'][0] - u['p'][1])) < 1.5 and abs(u3['a'][0] - u['a'][0] + 120) < 1.5, (u, u3))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        # «Atrás» (Alt+← o el botón del navegador) con el popover abierto
        pg.click(sel); pg.wait_for_timeout(150)
        pg.go_back(); pg.wait_for_timeout(400)
        ok('«Atrás» con el popover abierto vuelve al lugar anterior y lo cierra', not abierto(pg) and pg.evaluate('history.state.view') == 'roster')
        pg.go_forward(); pg.wait_for_selector('.fcab'); pg.wait_for_timeout(300)
        ok('y adelante vuelve a la ficha en Skills, sin el popover', not abierto(pg) and pg.evaluate('history.state.fichaTab') == 'skills'
           and pg.evaluate('history.state.charId') == c['cid'])
        # una skill corta, encima: al desplegar algo crece hacia arriba, sin tapar la skill
        cb = BEAST_UNI; abrir_ficha(pg, cb); selb = selector(cb)
        llevar(pg, selb, 820); pg.click(selb); pg.wait_for_timeout(200)
        u = ubicacion(pg, selb)
        pg.locator('#skpop details.tiptx summary').first.click(); pg.wait_for_timeout(100)
        u2 = ubicacion(pg, selb)
        ok('encima, al desplegar algo crece hacia arriba y no tapa la skill', u['p'][1] <= u['a'][0] + 1 and abs(u2['p'][1] - u['p'][1]) < 1.5
           and u2['p'][0] < u['p'][0] - 5 and u2['p'][0] >= u2['techo'] - 1, (u, u2))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)

        # captura (compu): la Tier-2 de Doctor Voodoo, con el primer efecto desplegado
        c = VOODOO_T2; sel = selector(c)
        abrir_ficha(pg, c); llevar(pg, sel, 215); pg.click(sel); pg.wait_for_timeout(200)
        pg.locator('#skpop details.tipef summary').first.click(); pg.wait_for_timeout(150)
        pg.screenshot(path=f'{CAPTURAS}/tooltip_1300.png')
        pg.keyboard.press('Escape')

        # -------------------------------------------------- en inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        for c in CASOS:
            abrir_ficha(pg, c)
            ti, fi = c['foco'] or (None, None)
            sel = selector(c, ti, fi); llevar(pg, sel, 300); pg.click(sel); pg.wait_for_timeout(200)
            chequear_contenido(pg, c, 'en', c['nombre'] + ' (inglés)')
            pg.keyboard.press('Escape'); pg.wait_for_timeout(80)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('compu: sin errores de página ni de consola', not errores, errores[:3])
        b.close()

        # -------------------------------------------------- celular
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True); escuchar(pg)
        pg.goto(url); pg.wait_for_selector('.ccard')
        for c in (VOODOO_T2, ANGELA_A3):
            abrir_ficha(pg, c)
            sel = selector(c); llevar(pg, sel, 300); pg.tap(sel); pg.wait_for_timeout(250)
            g = pg.evaluate("""() => { const p = document.getElementById('skpop'), r = p.getBoundingClientRect(), f = document.getElementById('skpop-fondo').getBoundingClientRect();
                return { r: [r.top, r.bottom, r.left, r.right], alto: innerHeight, ancho: innerWidth, docw: document.documentElement.scrollWidth,
                         sw: p.scrollWidth, cw: p.clientWidth, sh: p.scrollHeight, ch: p.clientHeight, fondo: [f.width, f.height],
                         anchos: [...p.querySelectorAll('*')].filter(x => x.getBoundingClientRect().right > innerWidth + 1).length }; }""")
            ok(f'celular, {c["nombre"]}: hoja inferior a todo el ancho, con fondo y sin desbordes', abierto(pg) and abs(g['r'][1] - g['alto']) <= 1
               and g['r'][2] == 0 and abs(g['r'][3] - g['ancho']) <= 1 and g['r'][0] > 0 and g['docw'] <= g['ancho'] and g['sw'] <= g['cw']
               and g['anchos'] == 0 and g['fondo'] == [g['ancho'], g['alto']], g)
            S = chequear_contenido(pg, c, 'es', f'celular, {c["nombre"]}')
            if c is VOODOO_T2:
                pg.screenshot(path=f'{CAPTURAS}/tooltip_390.png')
            else:
                ok('celular: una skill larga se recorre adentro de la hoja', g['sh'] > g['ch'], (g['sh'], g['ch']))
            pg.tap('#skpop-fondo', position={'x': 195, 'y': 40}); pg.wait_for_timeout(150)
            ok(f'celular, {c["nombre"]}: tocar el fondo la cierra', not abierto(pg))
        pg.tap(selector(ANGELA_A3)); pg.wait_for_timeout(200)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        ok('celular: Esc la cierra', not abierto(pg))
        ok('celular: sin errores de página ni de consola', not errores, errores[:3])
        if avisos: print('   avisos de consola:', avisos[:5])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
