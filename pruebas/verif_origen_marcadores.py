"""1.0.17: de dónde salió el valor de un marcador ($HEROSUBTYPE1, $HEROCLASS1) en la ficha.

El build lo completa con la tabla a mano (gs 'm'), con Leads & Supports ('l', desde el formato 6) o
con la wiki ('w'), y la ficha lo dice en el título del valor. Un origen que la app no conoce es un
error, no un dato de la wiki. Sin work/: con los datos del repo o los de MFF_DATOS
(armar_datos_prueba.py, mientras el data.js del repo sea de formato 5).

1 un retrato por origen, en español y en inglés: los valores completados en el idioma, cada uno con
  el título de su origen (Angela — Asgard's Assassin para 'l' si lo trae), y nada crudo ($HERO)
2 lo que sigue sin especificar: el aviso nombra Leads & Supports y la wiki y manda a la tabla a mano
3 sin errores de página ni de consola (ni valores sin inglés) en esas fichas
4 un gs inventado ('x') en el efecto de Leads & Supports: la ficha tira «origen de marcador
  desconocido: x» y no lo muestra como dato de otro origen"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js, RAIZ, DATOS
from playwright.sync_api import sync_playwright

ok = Chequeo()
DJ = datos_js('MFF_VERSION', 'MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_TABLAS', 'MFF_VOCAB_EN')
FORMATO = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))['formato_datos']
if DJ['MFF_VERSION']['formato'] != FORMATO:
    raise SystemExit(f'{DATOS}/data.js es de formato {DJ["MFF_VERSION"]["formato"]} y la app pide el {FORMATO}: '
                     'armá datos de prueba con armar_datos_prueba.py y pasalos con MFF_DATOS')

TITULO = {'m': {'es': 'Dato cargado a mano (scripts/contenido/marcadores.csv): ', 'en': 'Entered by hand (scripts/contenido/marcadores.csv): '},
          'l': {'es': 'Dato de Leads & Supports de thanosvibs: ', 'en': 'From thanosvibs Leads & Supports: '},
          'w': {'es': 'Dato de la wiki de Future Fight: ', 'en': 'From the Future Fight wiki: '}}
PEND = {'es': ('sin especificar', 'ni Leads & Supports ni la wiki de Future Fight lo dicen. Se completa a mano en scripts/contenido/marcadores.csv'),
        'en': ('unspecified', 'neither Leads & Supports nor the Future Fight wiki says so. It is filled in by hand in scripts/contenido/marcadores.csv')}
PREFIERO = {'l': 'angela3', 'm': 'jeffthelandshark', 'w': 'abomination'}

var = {}
for c in DJ['MFF_SEED_CHARACTERS']:
    var[c['p']] = (c['id'], '', c['name'], c['name'])
    for u in c['uniforms']:
        var[u['p']] = (c['id'], u['id'], c['name'], f"{c['name']} — {u['name']}")


def marcadores_de(p):
    """[(índices [skill, etapa, efecto], g, gs)] de los efectos con marcador del retrato."""
    out = []
    for si, sk in enumerate(DJ['MFF_SKILLS'].get(p, [])):
        for ti, st in enumerate(sk.get('st') or []):
            for fi, f in enumerate(st['fx']):
                if '$HERO' in DJ['MFF_TABLAS']['desc'][f['p']]['en']:
                    out.append(([si, ti, fi], f.get('g'), f.get('gs')))
    return out


con = {}
for p in DJ['MFF_SKILLS']:
    for _, g, gs in marcadores_de(p):
        if g:
            con.setdefault(gs, []).append(p)
print('efectos completados por origen:', {k: len(v) for k, v in con.items()})
ok('los datos solo traen orígenes conocidos', set(con) <= set(TITULO), sorted(con))
ok("los datos traen los tres orígenes ('m', 'l', 'w')", set(con) >= set(TITULO), sorted(con))
retratos = {gs: (PREFIERO[gs] if PREFIERO[gs] in con.get(gs, []) else con[gs][0]) for gs in TITULO if con.get(gs)}
pendiente = next(p for p in DJ['MFF_SKILLS'] if p in var and any(not g for _, g, _ in marcadores_de(p)))
print('retratos:', retratos, '· sin especificar:', pendiente)


def abrir(pg, p):
    cid, uid, nombre, _ = var[p]
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', ''); pg.wait_for_timeout(50); pg.fill('#q', nombre); pg.wait_for_timeout(200)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid:
        pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(150)
    pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(200)


def leer(pg):
    return pg.evaluate("""() => ({
        ok: [...document.querySelectorAll('.fxitems .tpl-ok')].map(e => [e.textContent, e.title]),
        pend: [...document.querySelectorAll('.fxitems .tpl')].map(e => [e.textContent, e.title]),
        crudo: /\\$HERO/.test(document.querySelector('#fcuerpo').textContent),
        cab: document.querySelector('.fcab h1').textContent,
        uni: (document.querySelector('select[data-a="uniformSel"]') || {}).value || ''})""")


D = carpeta_datos()
srv, url = levantar(D, origen_local())
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        errores, consola = [], []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type in ('error', 'warning') and consola.append(f'{m.type}: {m.text}'))
        pg.goto(url); pg.wait_for_selector('.ccard')
        for lang in ('es', 'en'):
            if lang == 'en':
                pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
            for gs, p in retratos.items():
                abrir(pg, p)
                r = leer(pg)
                esp = sorted((g if lang == 'es' else DJ['MFF_VOCAB_EN'][g], s) for _, g, s in marcadores_de(p) if g)
                vistos = sorted((v, next((k for k, x in TITULO.items() if tt.startswith(x[lang])), tt)) for v, tt in r['ok'])
                ok(f"1 [{lang}] {var[p][3]} ({gs}): valores con el título de su origen", vistos == esp and not r['crudo'],
                   (vistos, esp, r['crudo']))
                if gs == 'l':
                    ok(f"1 [{lang}] el título de Leads & Supports, completo", all(
                        tt == TITULO['l'][lang] + ('la skill publica este efecto sin decir a quién se refiere.' if lang == 'es'
                                                   else 'the skill publishes this effect without saying whom it refers to.')
                        for v, tt in r['ok'] if tt.startswith(TITULO['l'][lang])), r['ok'])
            abrir(pg, pendiente)
            r = leer(pg)
            n_pend = sum(1 for _, g, _ in marcadores_de(pendiente) if not g)
            bien = [x for x in r['pend'] if x[0] == PEND[lang][0] and PEND[lang][1] in x[1]]
            ok(f'2 [{lang}] {var[pendiente][3]}: sin especificar con el aviso nuevo', len(bien) == n_pend and not r['crudo'],
               (n_pend, r['pend'][:2]))
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('3 sin errores de página', not errores, errores[:3])
        ok('3 sin errores ni avisos de consola', not consola, consola[:3])

        # 4. gs inventado en el efecto de Leads & Supports (en memoria: la app lee window.MFF_SKILLS). Se
        # cambia con la ficha en Resumen, que no muestra skills; al pasar a Skills, el render tiene que cortar.
        p = retratos['l']
        (si, ti, fi), g, _ = next(x for x in marcadores_de(p) if x[2] == 'l')
        abrir(pg, p)
        pg.click('[data-a="fichaTab"][data-v="resumen"]'); pg.wait_for_timeout(150)
        pg.evaluate("([p, si, ti, fi]) => { window.MFF_SKILLS[p][si].st[ti].fx[fi].gs = 'x'; }", [p, si, ti, fi])
        pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(300)
        r = leer(pg)
        ok('4 gs inventado: tira el error', errores and all('origen de marcador desconocido: x' in e for e in errores), errores[:3])
        ok('4 gs inventado: no se muestra con ningún origen', not r['ok'] and pg.locator('.skill').count() == 0,
           (r['ok'], pg.locator('.skill').count()))
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
