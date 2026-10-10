"""La comparativa por efecto (#6, 1.0.35, datos de formato 13): la vista por defecto y el paso a «Ficha»; una fila por
destino y efecto del análisis de los comparados; el número de cada efecto (MFF_CATALOGO.valor) contra un modelo escrito
acá; quién da más («MAYOR») y el empate; lo igual en todos en una línea; lo que tiene uno solo, aparte; el filtro por
destino; «Ver textos»; en inglés; el celular sin desborde; sin errores de página ni de consola. Datos: MFF_DATOS."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, DATOS
from playwright.sync_api import sync_playwright
ok = Chequeo()
SP = PRUEBAS
s = open(f'{DATOS}/data.js', encoding='utf-8').read()


def load(n):
    i = s.find(f'window.{n} = ') + len(f'window.{n} = '); j = s.find(';\n', i); return json.loads(s[i:j])


A, S, T, CAT, C = load('MFF_ANALISIS'), load('MFF_SKILLS'), load('MFF_TABLAS'), load('MFF_CATALOGO'), load('MFF_SEED_CHARACTERS')
PJ = [('doctor-voodoo', 'doctor-voodoo-10200204'), ('black-cat', 'black-cat-10400009'), ('jeff-the-land-shark', '')]
retrato = {(c['id'], ''): c['p'] for c in C} | {(c['id'], u['id']): u['p'] for c in C for u in c['uniforms']}
PS = [retrato[x] for x in PJ]


# ---- modelo: las filas, sus números y quién da más ----
def valor(f, e):
    i = CAT['valor'][str(f['p'])][e]
    if i is None: return None
    pat = T['desc'][f['p']]['en']; pos = [k for k, ch in enumerate(pat) if ch == '#'][i]
    return (f['v'][i], pat[pos + 1:pos + 2] == '%')


filas = {}
for k, p in enumerate(PS):
    for ie, d, obj, fu in A[p]['fx']:
        e = CAT['efectos'][ie]['id']
        r = filas.setdefault(f'{d}|{e}', [set() for _ in PS])
        for si, ti, fi in fu:
            f = S[p][si]['st'][ti]['fx'][fi]
            r[k].add((valor(f, e), f.get('d')))


def mayor(cel):
    tienen = [k for k, c in enumerate(cel) if c]
    nums = [v for c in cel for v, _ in c if v]
    medible = bool(nums) and all(x[1] == nums[0][1] for x in nums)
    def m(c):
        n = max((v[0] for v, _ in c if v), default=float('-inf')) if medible else 0
        return (n, max((d if d is not None else float('-inf') for v, d in c if not medible or (v and v[0] == n)), default=float('-inf')))
    ms = {k: m(cel[k]) for k in tienen}
    top = max(ms.values())
    comparable = top[1] != float('-inf') or medible
    arriba = sorted(k for k in tienen if ms[k] == top)
    if not comparable or len(tienen) < 2: return [], False
    return (arriba, False) if len(arriba) < len(tienen) else ([], True)


modelo = {c: mayor(r) for c, r in filas.items()}
print('filas del modelo:', len(filas))

FUERA = """(w) => { const out = [];
  for (const el of document.querySelectorAll('main *')) { if (!el.checkVisibility()) continue; const r = el.getBoundingClientRect();
    if (r.width && r.right > w + 1) out.push(el.className || el.tagName); }
  return { doc: document.documentElement.scrollWidth, fuera: [...new Set(out)].slice(0, 8) }; }"""

srv, url = levantar(carpeta_datos(), origen_local())
errores, consola = [], []
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1440, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: consola.append(m.text) if m.type == 'error' else None)
        pg.goto(url); pg.wait_for_selector('.ccard')
        ok('datos de formato 13, con MFF_CATALOGO.valor', pg.evaluate('MFF_VERSION.formato') >= 13 and pg.evaluate('!!MFF_CATALOGO.valor'))
        pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(200)
        for cid, uid in PJ:
            pg.fill('#q', cid.split('-')[0]); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{cid}"][data-uid="{uid}"]'); pg.wait_for_timeout(150)
        pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_timeout(500)
        ok('la comparativa abre por efecto', pg.locator('.cpe').count() == 1 and pg.locator('table.cmpt').count() == 0)
        pg.click('[data-a="cmpVista"][data-v="ficha"]'); pg.wait_for_timeout(300)
        ok('«Ficha»: la tabla de antes', pg.locator('table.cmpt').count() == 1 and pg.locator('.cpe').count() == 0)
        pg.click('[data-a="cmpVista"][data-v="efecto"]'); pg.wait_for_timeout(300)

        # ---- todas las filas, sin juntar ni separar ----
        pg.click('[data-a="cmpIguales"]'); pg.click('[data-a="cmpSolos"]'); pg.wait_for_timeout(300)
        claves = pg.evaluate("[...document.querySelectorAll('.cpefila')].map(f => f.dataset.clave)")
        ok('una fila por destino y efecto del análisis de los tres', sorted(claves) == sorted(filas) and len(claves) == len(set(claves)),
           sorted(set(claves) ^ set(filas)))
        dom = pg.evaluate("""[...document.querySelectorAll('.cpefila')].map(f => ({ c: f.dataset.clave,
          m: [...f.querySelectorAll(':scope > .cpecel')].map((x, i) => x.classList.contains('mayor') ? i : -1).filter(i => i >= 0),
          e: !!f.querySelector(':scope > .cpelab .cpechip') }))""")
        mal = [(x['c'], x['m'], x['e'], modelo[x['c']]) for x in dom if (x['m'], x['e']) != (modelo[x['c']][0], modelo[x['c']][1])]
        ok('«MAYOR» y «EMPATE» como el modelo, en todas las filas', not mal, mal[:5])

        def celdas(c):
            return pg.evaluate("(c) => [...document.querySelector(`.cpefila[data-clave=\"${c}\"]`).querySelectorAll(':scope > .cpecel')].map(x => x.innerText.replace(/\\s+/g, ' ').trim())", c)
        x = celdas('q|ataques_todos')
        ok('equipo, todos los ataques: 30% LÍD · MAYOR 65% LÍD · —', x[0] == '30% LÍD' and x[1] == 'MAYOR 65% LÍD' and x[2] == '—', x)
        x = celdas('q|dano_contra')
        ok('equipo, daño contra una facción: la facción completada (Supervillano)', 'Supervillano' in x[0] and '50%' in x[0], x)
        x = celdas('e|dano_skill')
        ok('texto combinado: daño de skill 50% y 40%, cada uno con su número y de qué sale', x[0].endswith('50% T2') and x[1].endswith('40% T2') and 'DAÑO DE SKILL Y EXTRA' in x[1], x)
        x = celdas('e|dano_extra')
        ok('texto combinado: daño extra 45% y 35% (el segundo número)', x[0].endswith('45% T2') and x[1].endswith('35% T2'), x)
        x = celdas('e|critico')
        ok('frenesí: la probabilidad de crítico es el tercer número (Jeff 60%)', x[2].startswith('MAYOR FRENESÍ 60%') and '25%' in x[0] and '30%' in x[1], x)
        x = celdas('r|paralizar')
        ok('parálisis: sin número, MAYOR por duración (Jeff, 3 s)', x[2].startswith('MAYOR') and '3 s' in x[2], x)
        x = celdas('r|vulnerable_rival')
        ok('más daño recibido: dice de qué sale (Pánico, Control mental)', 'Pánico' in x[0] and 'Control mental' in x[0], x)

        # ---- lo igual y lo de uno solo ----
        pg.click('[data-a="cmpIguales"]'); pg.wait_for_timeout(300)
        iguales = pg.evaluate("[...document.querySelectorAll('.cpeigual b')].map(b => b.textContent)")
        ok('igual en todos: le quita los potenciadores, en una línea y sin slots',
           'Le quita los potenciadores al rival' in iguales and pg.locator('.cpeigual .slotbadge').count() == 0, iguales)
        pg.click('[data-a="cmpSolos"]'); pg.wait_for_timeout(300)
        n_solos = pg.locator('.cpesolo li:not(.cpequien)').count()
        esperados = sum(1 for c, r in filas.items() if sum(1 for x in r if x) == 1)
        ok('lo que tiene uno solo, aparte: todas', n_solos == esperados, (n_solos, esperados))
        jeff = pg.locator('.cpesec[data-d="q"] .cpesolo > ul').nth(2).inner_text()
        ok('equipo, solo Jeff: mermas más cortas 24%', 'Mermas más cortas' in jeff and '24%' in jeff, jeff)

        # ---- destino y textos ----
        pg.click('[data-a="cmpDestino"][data-v="r"]'); pg.wait_for_timeout(300)
        ok('filtro «Contra el rival»: una sola sección', pg.evaluate("[...document.querySelectorAll('.cpesec')].map(x => x.dataset.d)") == ['r'])
        pg.click('.cpefila[data-clave="r|paralizar"] [data-a="cmpTextos"]'); pg.wait_for_timeout(300)
        tx = pg.locator('.cpefila[data-clave="r|paralizar"] .cpetx').inner_text()
        ok('«Ver textos»: lo que dice cada skill', 'Parálisis' in tx and 'Ocultar textos' in pg.locator('.cpefila[data-clave="r|paralizar"] [data-a="cmpTextos"]').inner_text(), tx[:200])
        pg.screenshot(path=f'{SP}/cmp_efecto_1440.png', full_page=True)
        pg.click('[data-a="cmpDestino"][data-v="todo"]'); pg.wait_for_timeout(300)

        # ---- inglés ----
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(400)
        ok('inglés: la vista y sus marcas', pg.locator('[data-a="cmpVista"][data-v="efecto"]').inner_text() == 'By effect'
           and pg.locator('.cpecel.mayor .cpemayor').first.inner_text() == 'TOP' and 'LDR' in celdas('q|ataques_todos')[0], celdas('q|ataques_todos'))
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)

        # ---- celular ----
        pg.set_viewport_size({'width': 390, 'height': 800}); pg.wait_for_timeout(400)
        r = pg.evaluate(FUERA, 390)
        ok('celular: sin desborde', r['doc'] <= 390 and not r['fuera'], r)
        ok('celular: cada renglón dice de quién es', pg.locator('.cpefila .cpequien').first.is_visible())
        pg.screenshot(path=f'{SP}/cmp_efecto_390.png', full_page=True)
        b.close()
finally:
    srv.terminate()
ok('sin errores de página', not errores, errores[:3])
ok('sin errores de consola', not consola, consola[:3])
ok.fin()
