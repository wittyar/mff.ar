"""Índice para armar equipos (1.0.10), contra un modelo aparte en Python (las mismas reglas,
escritas acá con los datos de data.js):

1 Ficha › Resumen › «Lo que le da al equipo»: las categorías de cada liderazgo y soporte.
2 Ficha › Resumen › «Le sirve»: las categorías de ataque según con qué pega.
3 Roster: filtros «Su liderazgo da», «Su soporte da», «Liderazgo o soporte solo para» y «Que
  le llegue y le sirva a» (desde la ficha), con el conjunto completo de resultados y lo que
  dice cada tarjeta. Incluye el caso del usuario: Satana de líder para Abomination.
4 Equipos › combinaciones de 3: la cobertura de cada trío (lo que le dan los compañeros y, desde el 4 de octubre de
  2026, sus propios soportes y sus anti-mermas propios sin probabilidad; anti-mermas son los stats de la tabla de valor).
5 Inglés, celular (nada se sale) y una capa vieja sin los filtros nuevos."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from analisis_haz import VAR, TODAS, SOP, aplica, C
from auditoria_equipos import PERFIL, sirve_fx, NOLIDER, LIDER, ANTI_STATS, anti_propio
from playwright.sync_api import sync_playwright

ok = Chequeo()
CATS = [('fis', {'Physical Attack'}), ('ene', {'Energy Attack'}), ('atk', {'All Basic Attacks', 'All Basic Attacks (Stackable)'}),
        ('fuego', {'Fire Damage', 'Fire Damage by % Fire Resist'}), ('hielo', {'Cold Damage'}), ('rayo', {'Lightning Damage'}),
        ('veneno', {'Poison Damage'}), ('mente', {'Mind Damage'}), ('elems', {'All Element Damage'}),
        ('evasion', {'Ignore Dodge'}), ('defensas', {'All Basic Defenses', 'Super Armor, All Basic Defenses'}),
        ('vida', {'HP'}), ('mermas', set(ANTI_STATS))]
ORDEN = [k for k, _ in CATS]
ATQ = ORDEN[:9]
CAT_DE = {s: k for k, ss in CATS for s in ss}
ES = {'fis': 'Ataque físico', 'ene': 'Ataque de energía', 'atk': 'Todos los ataques', 'fuego': 'Daño de fuego',
      'hielo': 'Daño de frío', 'rayo': 'Daño de rayo', 'veneno': 'Daño de veneno', 'mente': 'Daño mental',
      'elems': 'Daño de todos los elementos', 'evasion': 'Ignorar esquiva', 'defensas': 'Todas las defensas',
      'vida': 'PG', 'mermas': 'Anti-mermas'}
EN = {'fis': 'Physical Attack', 'ene': 'Energy Attack', 'atk': 'All Attacks', 'fuego': 'Fire Damage', 'hielo': 'Cold Damage',
      'rayo': 'Lightning Damage', 'veneno': 'Poison Damage', 'mente': 'Mind Damage', 'elems': 'All Element Damage',
      'evasion': 'Ignore Dodge', 'defensas': 'All Defenses', 'vida': 'HP', 'mermas': 'Debuff removal'}
SLOTS = ['leader', 'leader2', 'passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact']
SUB = {}
for c in C:
    SUB[f"{c['id']}::base"] = None
    for u in c['uniforms']:
        SUB[f"{c['id']}::{u['id']}"] = u['name']
def label(v): return v['name'] + (' — ' + SUB[v['key']] if SUB[v['key']] else '')
POR_LABEL = {label(v): v for v in TODAS}

def sv(f, b): return sirve_fx(f, PERFIL[b['p']])
def cats_slot(x, b=None):
    ks = {CAT_DE.get(f['s']) for f in x['fx'] if b is None or sv(f, b)}
    return [k for k in ORDEN if k in ks]
def cats_sirven(b): return [k for k, ss in CATS if any(sv({'s': s}, b) for s in ss)]
def slot_pasa(x, cats, para, restr):
    if restr and (not x.get('r') or '|'.join(x['r']) != restr): return False
    if para and not aplica(x, para): return False
    if not cats: return para is None or any(sv(f, para) for f in x['fx'])
    return any(CAT_DE.get(f['s']) in cats and (para is None or sv(f, para)) for f in x['fx'])
def indice(v, lid, sop, para, restr):
    """{lid: [cats], sop: [cats], api} o None, como lo que muestra la tarjeta. api: algún liderazgo que pasa el filtro
    sale de la Leader Skill de la API (carril Q), y la línea lo dice («según la skill del juego»)."""
    if para and v['cid'] == para['cid']: return None
    s = SOP.get(v['p']) or {}
    api = any(s.get(k) and s[k].get('src') == 'api' and slot_pasa(s[k], lid, para, restr) for k in LIDER)
    def da(ks, cats):
        out, pasa = set(), False
        for k in ks:
            x = s.get(k)
            if not x or not slot_pasa(x, cats, para, restr): continue
            pasa = True
            out |= {c for c in cats_slot(x, para) if not cats or c in cats}
        return [k for k in ORDEN if k in out] if pasa else None
    if not lid and not sop:
        a, b = da(LIDER, []), da(NOLIDER, [])
        return {'lid': a or [], 'sop': b or [], 'api': api} if (a is not None or b is not None) else None
    a = da(LIDER, lid) if lid else []
    b = da(NOLIDER, sop) if sop else []
    return {'lid': a, 'sop': b, 'api': api} if a is not None and b is not None else None
def cobertura(foco, vs, lider):
    # soportes de todos (también los suyos: 4 de octubre de 2026); liderazgo del líder elegido, sea quien sea (también
    # él); y sus anti-mermas propios sin probabilidad
    out = {}
    for a in vs:
        s = SOP.get(a['p']) or {}
        for k in SLOTS:
            x = s.get(k)
            if not x or not aplica(x, foco): continue
            if k in LIDER and a is not lider: continue
            for c in cats_slot(x, foco):
                out[c] = out.get(c, False) or k != 'artifact'
    if anti_propio(foco)[0]: out['mermas'] = True
    return out
def chips_cob(cob, L):
    nom = lambda c: L[c] + (' *' if c in cob and not cob[c] else '')
    res = []
    cs = [c for c in ATQ if c in cob]
    est = 'no' if not cs else ('si' if any(cob[c] for c in cs) else 'art')
    res.append((est, ('✗' if not cs else '✓') + ' ' + ('Ataque' if L is ES else 'Attack') + (': ' + ', '.join(nom(c) for c in cs) if cs else '')))
    for k in ORDEN[9:]:
        est = 'no' if k not in cob else ('si' if cob[k] else 'art')
        res.append((est, ('✗' if k not in cob else '✓') + ' ' + nom(k)))
    return res

# casos de ficha: cubrir cada categoría y cada tipo de slot, más perfiles de daño distintos
vistos, casos = set(), []
for v in TODAS:
    s = SOP.get(v['p']) or {}
    nuevo = {(k, c) for k in SLOTS if s.get(k) for c in cats_slot(s[k])} - vistos
    if nuevo: casos.append(v); vistos |= nuevo
perfiles = {}
for v in TODAS:
    clave = (tuple(sorted(PERFIL[v['p']][0])), tuple(sorted(PERFIL[v['p']][2])))
    perfiles.setdefault(clave, v)
print('fichas por categoría:', len(casos), '| perfiles de daño distintos:', len(perfiles))
FUERA = """() => { const conScroll = (e) => { for (let x = e.parentElement; x; x = x.parentElement) if (getComputedStyle(x).overflowX !== 'visible') return true; return false; };
  return [...document.querySelectorAll('#app *, main *, body *')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > innerWidth + 0.5 && !e.closest('details:not([open])') && !conScroll(e); })
  .map(e => (e.className || e.tagName) + ' → ' + Math.round(e.getBoundingClientRect().right)).slice(0, 4).concat(document.scrollingElement.scrollWidth > innerWidth ? ['página: ' + document.scrollingElement.scrollWidth] : []); }"""


def ir_roster(pg):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
def abrir(pg, v, tab='resumen'):
    ir_roster(pg)
    pg.fill('#q', ''); pg.wait_for_timeout(40); pg.fill('#q', v['name']); pg.wait_for_timeout(150)
    pg.click(f'.ccard[data-cid="{v["cid"]}"][data-uid=""], tr[data-cid="{v["cid"]}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if v['uid']:
        pg.select_option('select[data-a="uniformSel"]', v['uid']); pg.wait_for_timeout(100)
    pg.click(f'[data-a="fichaTab"][data-v="{tab}"]'); pg.wait_for_timeout(120)
def resultados(pg):
    """Todas las entradas del roster filtrado (vista tabla, todas las páginas) con su línea."""
    out = {}
    while True:
        for tr in pg.locator('tr[data-a="open"]').all():
            k = tr.get_attribute('data-cid') + '::' + (tr.get_attribute('data-uid') or 'base')
            out[k] = tr.locator('.indlinea').inner_text() if tr.locator('.indlinea').count() else ''
        sig = pg.locator('[data-a="page"]', has_text='→')
        if not sig.count() or sig.is_disabled(): break
        sig.click(); pg.wait_for_timeout(80)
    return out
def linea_esperada(x, L):
    if not x: return ''
    partes = []
    if x['lid']: partes.append(('Liderazgo' if L is ES else 'Leadership') + ': ' + ' · '.join(L[c] for c in x['lid'])
                               + ((' SEGÚN LA SKILL DEL JUEGO' if L is ES else ' PER THE GAME SKILL') if x['api'] else ''))
    if x['sop']: partes.append(('Soporte' if L is ES else 'Support') + ': ' + ' · '.join(L[c] for c in x['sop']))
    return '\n'.join(partes)
def limpiar_filtros(pg):
    ir_roster(pg)
    if pg.locator('[data-a="clearFilters"]').count(): pg.locator('[data-a="clearFilters"]').first.click(); pg.wait_for_timeout(80)
    if not pg.locator('.filterpanel').count(): pg.click('[data-a="toggleFilters"]'); pg.wait_for_timeout(80)
def comparar_roster(pg, nombre, lid=(), sop=(), para=None, restr='', L=ES):
    esperado = {v['key']: linea_esperada(indice(v, list(lid), list(sop), para, restr), L) for v in TODAS
                if indice(v, list(lid), list(sop), para, restr) is not None}
    got = resultados(pg)
    faltan, sobran = sorted(set(esperado) - set(got)), sorted(set(got) - set(esperado))
    malas = [(k, esperado[k], got[k]) for k in esperado if k in got and esperado[k] != got[k].strip()]
    ok(f'3 {nombre}: {len(esperado)} entradas, cada una con lo que da', not faltan and not sobran and not malas,
       {'faltan': faltan[:4], 'sobran': sobran[:4], 'malas': malas[:3]})
    return got


SOLO = set(sys.argv[1:])
def principal(url):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        # 1 categorías de cada bloque en «Lo que le da al equipo»
        malos = []
        for v in casos:
            abrir(pg, v)
            s = SOP.get(v['p']) or {}
            esperado = [[ES[c] for c in cats_slot(s[k])] for k in SLOTS if s.get(k)]
            got = pg.evaluate("() => [...document.querySelectorAll('.sops .sop')].map(b => [...b.querySelectorAll('.sopcats .tag')].map(t => t.textContent.trim()))")
            if got != esperado: malos.append((v['key'], esperado, got))
        ok(f'1 categorías de cada liderazgo y soporte ({len(casos)} fichas, todas las categorías y slots)', not malos, malos[:3])
        # 2 «Le sirve»: categorías de ataque según el perfil de daño
        malos = []
        for v in perfiles.values():
            abrir(pg, v)
            atq = [ES[c] for c in cats_sirven(v) if c in ATQ]
            got = pg.evaluate("() => [...document.querySelectorAll('.lesirve > .tag.dim')].map(t => t.textContent.trim())")
            resto = pg.evaluate("() => document.querySelector('.lesirve > span.muted:not([title])').textContent")
            if got != atq or not all(ES[k] in resto for k in ORDEN[9:]): malos.append((v['key'], PERFIL[v['p']], atq, got))
        ok(f'2 «Le sirve»: el ataque según con qué pega ({len(perfiles)} perfiles de daño distintos)', not malos, malos[:3])

        # 3 roster
        limpiar_filtros(pg)
        pg.click('[data-a="view"][data-v="table"]'); pg.wait_for_timeout(80)
        pg.click('[data-a="filter"][data-cat="lid"][data-v="fis"]'); pg.wait_for_timeout(80)
        comparar_roster(pg, 'liderazgo: ataque físico', lid=['fis'])
        pg.click('[data-a="filter"][data-cat="lid"][data-v="atk"]'); pg.wait_for_timeout(80)
        comparar_roster(pg, 'liderazgo: ataque físico o todos los ataques', lid=['fis', 'atk'])
        pg.click('[data-a="filter"][data-cat="sop"][data-v="evasion"]'); pg.wait_for_timeout(80)
        comparar_roster(pg, 'y además soporte: ignorar evasión', lid=['fis', 'atk'], sop=['evasion'])
        limpiar_filtros(pg)
        for c in ('vida', 'mermas'):
            pg.click(f'[data-a="filter"][data-cat="sop"][data-v="{c}"]'); pg.wait_for_timeout(60)
        comparar_roster(pg, 'soporte: vida o quita debuffs', sop=['vida', 'mermas'])
        limpiar_filtros(pg)
        pg.select_option('select[data-a="restr"]', 'Allies|Mutante'); pg.wait_for_timeout(80)
        comparar_roster(pg, 'solo para mutantes', restr='Allies|Mutante')
        pg.click('[data-a="filter"][data-cat="sop"][data-v="atk"]'); pg.wait_for_timeout(80)
        comparar_roster(pg, 'solo para mutantes y su soporte da todos los ataques', sop=['atk'], restr='Allies|Mutante')
        # desde la ficha: «Líderes que se lo dan», con el caso del usuario (Abomination, Satana)
        abom, ht = VAR['abomination::base'], next(v for v in TODAS if v['name'] == 'Human Torch' and not v['uid'])
        for foco, tipo in ((abom, 'lid'), (ht, 'lid'), (abom, 'sop')):
            limpiar_filtros(pg)
            abrir(pg, foco)
            pg.click(f'[data-a="paraVer"][data-tipo="{tipo}"]'); pg.wait_for_timeout(150)
            chip = pg.locator('[data-a="paraQuitar"]').text_content() if pg.locator('[data-a="paraQuitar"]').count() else ''
            cats = cats_sirven(foco)
            ok(f'3 {foco["name"]} › «{"Líderes" if tipo == "lid" else "Soportes"} que se lo dan»: abre el roster con el filtro y el personaje',
               label(foco) in chip and pg.locator(f'[data-a="filter"][data-cat="{tipo}"].on').count() == len(cats), chip)
            got = comparar_roster(pg, f'que le llegue y le sirva a {foco["name"]} ({tipo})', **{tipo: cats}, para=foco)
            if foco is abom and tipo == 'lid':
                satana = [k for k in got if k.startswith('satana')]
                ok('3 el caso del usuario: Satana no aparece como líder para Abomination', not satana, satana)
            if foco is ht and tipo == 'lid':
                ok('3 Satana aparece como líder para Human Torch', any(k.startswith('satana') for k in got), sorted(got)[:5])
        # sin categorías: cualquier liderazgo o soporte que le llegue y le sirva
        for c in cats_sirven(abom):
            pg.click(f'[data-a="filter"][data-cat="sop"][data-v="{c}"]'); pg.wait_for_timeout(40)
        comparar_roster(pg, 'solo el personaje, sin categorías', para=abom)
        pg.click('[data-a="paraQuitar"]'); pg.wait_for_timeout(80)
        ok('3 quitar el personaje del filtro', pg.locator('[data-a="paraQuitar"]').count() == 0
           and len(resultados(pg)) == len(TODAS))
        ok('sin errores de página', not errores, errores[:3])

        # 4 cobertura de las combinaciones
        malos, n = [], 0
        for foco in (abom, ht, VAR['ancient-one::base'] if 'ancient-one::base' in VAR else TODAS[3]):
            abrir(pg, foco, 'equipos')
            pg.wait_for_selector('.combo', timeout=60000)
            for card in pg.locator('.combo').all():
                ks = [e.get_attribute('data-cid') + '::' + (e.get_attribute('data-uid') or 'base') for e in card.locator('.eqfoto').all()]
                vs = [VAR[k] for k in ks]
                lt = card.locator('.combolider').text_content()
                lider = POR_LABEL.get(lt.split('Líder: ', 1)[1]) if lt.startswith('Líder: ') else None
                got = [(c.get_attribute('class').split()[-1], c.text_content().strip()) for c in card.locator('.cobertura .tag.cob').all()]
                esp = chips_cob(cobertura(foco, vs, lider), ES)    # el líder va primero: el foco es el de la ficha
                n += 1
                if got != esp: malos.append((ks, lt, esp, got))
        ok(f'4 cobertura de {n} combinaciones (3 personajes, primera página)', not malos, malos[:2])
        # 5 inglés
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(250)
        abrir(pg, abom)
        s = SOP.get(abom['p']) or {}
        esperado = [[EN[c] for c in cats_slot(s[k])] for k in SLOTS if s.get(k)]
        got = pg.evaluate("() => [...document.querySelectorAll('.sops .sop')].map(b => [...b.querySelectorAll('.sopcats .tag')].map(t => t.textContent.trim()))")
        lesirve = pg.locator('.lesirve').text_content()
        ok('5 inglés: categorías y «Le sirve»', got == esperado and 'Useful to it' in lesirve and 'Leaders that give it' in lesirve
           and all(EN[c] in lesirve for c in cats_sirven(abom)), (esperado, got, lesirve))
        abrir(pg, abom, 'equipos'); pg.wait_for_selector('.combo', timeout=60000)
        card = pg.locator('.combo').first
        ks = [e.get_attribute('data-cid') + '::' + (e.get_attribute('data-uid') or 'base') for e in card.locator('.eqfoto').all()]
        lt = card.locator('.combolider').text_content()
        lider = POR_LABEL.get(lt.split('Leader: ', 1)[1]) if lt.startswith('Leader: ') else None
        got = [(c.get_attribute('class').split()[-1], c.text_content().strip()) for c in card.locator('.cobertura .tag.cob').all()]
        ok('5 inglés: cobertura', got == chips_cob(cobertura(abom, [VAR[k] for k in ks], lider), EN), got)
        limpiar_filtros(pg)
        pg.click('[data-a="filter"][data-cat="lid"][data-v="evasion"]'); pg.wait_for_timeout(80)
        comparar_roster(pg, 'inglés: liderazgo ignorar evasión', lid=['evasion'], L=EN)
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(250)
        ok('sin errores de página (4 y 5)', not errores, errores[:3])
        b.close()

        # celular
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('#q')       # la capa quedó en vista tabla
        pg.click('[data-a="view"][data-v="grid"]'); pg.wait_for_timeout(80)
        limpiar_filtros(pg)
        pg.click('[data-a="filter"][data-cat="lid"][data-v="fis"]'); pg.wait_for_timeout(80)
        ok('celular: panel de filtros y tarjetas con lo que da, nada se sale', not pg.evaluate(FUERA), pg.evaluate(FUERA))
        limpiar_filtros(pg)
        abrir(pg, abom)
        ok('celular: Resumen con «Le sirve» y las categorías, nada se sale', not pg.evaluate(FUERA), pg.evaluate(FUERA))
        pg.click('[data-a="paraVer"][data-tipo="lid"]'); pg.wait_for_timeout(150)
        ok('celular: roster con el personaje en el filtro, nada se sale', not pg.evaluate(FUERA), pg.evaluate(FUERA))
        limpiar_filtros(pg)
        abrir(pg, abom, 'equipos'); pg.wait_for_selector('.combo', timeout=60000)
        ok('celular: combinaciones con la cobertura, nada se sale', not pg.evaluate(FUERA), pg.evaluate(FUERA))
        pg.screenshot(path='shots/indice_cel_combos.png', full_page=False)
        ok('sin errores de página (celular)', not errores, errores[:3])
        b.close()


srv, url = levantar(carpeta_datos(), origen_local())
try:
    principal(url)
finally:
    srv.terminate(); srv.wait()

# capa vieja: preferencias sin los filtros nuevos
d = carpeta_datos()
json.dump({'prefs': {'filtersOpen': True, 'filters': {'c': ['Combate'], 'r': [], 't': [], 'f': [], 'ins': [], 'race': [], 'origin': [], 'ab': []}}},
          open(os.path.join(d, 'capa.json'), 'w', encoding='utf-8'))
srv, url = levantar(d, origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        n_comb = sum(1 for v in TODAS if v['c'] == 'Combate')
        cuenta = pg.locator('.count b').inner_text()
        pg.click('[data-a="filter"][data-cat="lid"][data-v="vida"]'); pg.wait_for_timeout(100)
        esp = sum(1 for v in TODAS if v['c'] == 'Combate' and indice(v, ['vida'], [], None, ''))
        ok('capa vieja: arranca con su filtro de clase, el panel tiene los filtros nuevos y funcionan',
           cuenta == str(n_comb) and pg.locator('.count b').inner_text() == str(esp) and not errores,
           (cuenta, n_comb, pg.locator('.count b').inner_text(), esp, errores[:2]))
        capa = json.load(open(os.path.join(d, 'capa.json'), encoding='utf-8'))
        ok('capa vieja: al guardar quedan los filtros nuevos', capa['prefs']['filters'].get('lid') == ['vida']
           and capa['prefs'].get('para') == '' and capa['prefs'].get('restr') == '', capa['prefs'])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
