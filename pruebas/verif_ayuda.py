"""La ayuda (1.0.48, Ezequiel, 27 de octubre de 2026): el botón «Ayuda» de arriba la activa y desactiva para toda la app;
activada, pasar el mouse por el nombre de una skill o por la etiqueta de un efecto muestra un tooltip con lo que hace, y
el clic abre el «Cómo funciona» en una ventana modal, también desde la comparativa en «Ficha». Y el roster ordenado por
lanzamiento, lo más nuevo primero, por defecto.

Casos (contra un modelo armado acá desde data.js, sin app.js):
  1. Roster: el orden por defecto es «Lanzamiento» y cada tarjeta llegó en la misma fecha o antes que la anterior
     (la fecha de su hecho «personaje» o «uniforme» en MFF_HISTORICO).
  2. Ficha de Doctor Voodoo — Savage Avengers, Skills: el tooltip de la Tier-2 (su nombre y sus efectos) y el de la
     etiqueta de un efecto, dentro de la ventana; se va al salir; desactivada, sin tooltip (el clic igual abre), y la
     preferencia queda guardada al recargar.
  3. Comparativa en «Ficha»: el nombre de una skill y un efecto abren la ventana de esa variante (el efecto, desplegado);
     Esc devuelve el foco al nombre.
  4. Comparativa «Por potenciador», 1366×768: cada «?» abierto cerca del borde de abajo queda dentro de la ventana
     (el error que vio Ezequiel: se abría hacia abajo, fuera de la pantalla); desactivada, ningún «?» a la vista.
  5. Celular: tocar una skill abre la hoja, sin tooltip.
Sin errores de página ni de consola."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
D = datos_js('MFF_SEED_CHARACTERS', 'MFF_HISTORICO', 'MFF_SKILLS', 'MFF_TABLAS', 'MFF_CATALOGO')
PJ = {c['id']: c for c in D['MFF_SEED_CHARACTERS']}
H, SK, TB, CAT = D['MFF_HISTORICO'], D['MFF_SKILLS'], D['MFF_TABLAS'], D['MFF_CATALOGO']

# ---- modelo: la fecha de llegada de cada variante ----
FECHA = {v[0]: v[2] for v in H['versiones']}
LLEGA = {x[0]: FECHA[x[2]] for x in H['hechos'] if x[1] in ('personaje', 'uniforme')}
faltan = [f'{c["id"]}::base' for c in PJ.values() if f'{c["id"]}::base' not in LLEGA] + \
         [f'{c["id"]}::{u["id"]}' for c in PJ.values() for u in c['uniforms'] if f'{c["id"]}::{u["id"]}' not in LLEGA]
ok('modelo: cada variante del roster tiene su llegada en el histórico', not faltan, faltan[:5])
MAS_NUEVA = max(LLEGA.values())

VOODOO = next(u for u in PJ['doctor-voodoo']['uniforms'] if u['name'] == 'Savage Avengers')
SI_T2 = next(i for i, s in enumerate(SK[VOODOO['p']]) if s['sl'] == 'Tier-2 Passive')
NOMBRE_T2 = TB['name'][SK[VOODOO['p']][SI_T2]['n']]

def abrir_ficha(pg, cid, uid):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', PJ[cid]['name']); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(150)
    pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(200)

def flotante(pg):
    return pg.evaluate("""() => { const c = document.getElementById('flotay'); if (!c || c.hidden) return null;
        const r = c.getBoundingClientRect();
        return { txt: c.textContent.replace(/\\s+/g, ' ').trim(), dentro: r.top >= 0 && r.bottom <= innerHeight + 1 && r.left >= 0
                 && r.right <= document.documentElement.clientWidth + 1 }; }""")

def pasar(pg, sel, y=None):
    """Lleva lo que se va a señalar a la vista (a la altura y, si se da) y después pasa el mouse: si lo llevara el hover,
    el desplazamiento llegaría después y ocultaría el tooltip (se oculta al desplazar)."""
    pg.evaluate("""([s, y]) => { const el = document.querySelector(s); el.scrollIntoView({ block: 'center', inline: 'center', behavior: 'instant' });
        if (y !== null) window.scrollTo({ top: el.getBoundingClientRect().top + scrollY - y, behavior: 'instant' }); }""", [sel, y])
    pg.evaluate("new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")    # que llegue el evento scroll
    pg.wait_for_timeout(120)
    pg.hover(sel); pg.wait_for_timeout(120)

errores = []
def escuchar(pg):
    pg.on('pageerror', lambda e: errores.append(str(e)))
    pg.on('console', lambda m: errores.append('consola: ' + m.text) if m.type == 'error' else None)

srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 1366, 'height': 768}); pg = ctx.new_page(); escuchar(pg)
        pg.goto(url); pg.wait_for_selector('.ccard')

        # ---- 1. roster por lanzamiento ----
        ok('roster: el orden por defecto es «Lanzamiento»', pg.eval_on_selector('select[data-a="sort"]', 'x => x.value') == 'lanz'
           and pg.eval_on_selector('select[data-a="sort"]', 'x => x.selectedOptions[0].textContent') == 'Lanzamiento')
        cartas = pg.evaluate("[...document.querySelectorAll('.ccard')].map(x => x.dataset.cid + '::' + (x.dataset.uid || 'base'))")
        fechas = [LLEGA[k] for k in cartas]
        ok('roster: lo más nuevo primero, y cada una llegó igual o antes que la anterior',
           fechas[0] == MAS_NUEVA and all(a >= b for a, b in zip(fechas, fechas[1:])), list(zip(cartas, fechas))[:6])
        ok('el botón «Ayuda», activado por defecto', pg.get_attribute('[data-a="ayudaToggle"]', 'aria-pressed') == 'true')

        # ---- 2. tooltip en la ficha ----
        abrir_ficha(pg, 'doctor-voodoo', VOODOO['id'])
        sel = f'#skt-{SI_T2}'
        pasar(pg, sel, 600)       # cerca del borde de abajo: el tooltip se abre encima
        f = flotante(pg)
        ok('ficha: el tooltip de la skill nombra la skill, dentro de la ventana, y dice que el clic abre el detalle',
           f and NOMBRE_T2['es'] in f['txt'] and f['dentro'] and 'Clic: el detalle' in f['txt'], f)
        pasar(pg, f'.skill [data-a="skTip"][data-si="{SI_T2}"] .fxtag', 300)
        f2 = flotante(pg)
        etq = pg.inner_text(f'.skill [data-a="skTip"][data-si="{SI_T2}"] .fxtag').strip()
        ok('ficha: el tooltip de un efecto, distinto del de la skill y dentro de la ventana', f2 and f2['txt'] != f['txt'] and f2['dentro'], (etq, f2))
        pg.mouse.move(5, 300); pg.wait_for_timeout(120)
        ok('ficha: al salir, el tooltip se va', flotante(pg) is None)
        pg.click(sel); pg.wait_for_timeout(200)
        ok('ficha: el clic abre la ventana y el tooltip se va', pg.locator('#skpop').count() == 1 and flotante(pg) is None)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)

        # desactivada
        pg.click('[data-a="ayudaToggle"]'); pg.wait_for_timeout(250)
        ok('desactivada: el botón dice que no', pg.get_attribute('[data-a="ayudaToggle"]', 'aria-pressed') == 'false')
        pasar(pg, sel, 300)
        ok('desactivada: sin tooltip', flotante(pg) is None)
        pg.click(sel); pg.wait_for_timeout(200)
        ok('desactivada: el clic igual abre la ventana', pg.locator('#skpop').count() == 1)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        pg.reload(); pg.wait_for_selector('#app'); pg.wait_for_timeout(400)
        ok('desactivada: queda guardada al recargar', pg.get_attribute('[data-a="ayudaToggle"]', 'aria-pressed') == 'false')
        pg.click('[data-a="ayudaToggle"]'); pg.wait_for_timeout(250)

        # ---- 3. comparativa en «Ficha» ----
        pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
        pg.click('[data-a="pickMode"]'); pg.wait_for_timeout(200)
        for cid, uid in (('doctor-voodoo', VOODOO['id']), ('black-cat', '')):
            pg.fill('#q', PJ[cid]['name']); pg.wait_for_timeout(250)
            pg.click(f'.ccard[data-cid="{cid}"][data-uid="{uid}"]'); pg.wait_for_timeout(150)
        pg.click('.mesa [data-a="goCompare"]'); pg.wait_for_timeout(500)
        pg.click('[data-a="cmpVista"][data-v="ficha"]'); pg.wait_for_timeout(300)
        clave = f'doctor-voodoo::{VOODOO["id"]}'
        bsel = f'.cmpsk[data-k="{clave}"][data-si="{SI_T2}"]'
        pasar(pg, bsel, 300)
        f = flotante(pg)
        ok('comparativa: el tooltip del nombre de la skill', f and NOMBRE_T2['es'] in f['txt'] and f['dentro'], f)
        pg.click(bsel); pg.wait_for_timeout(200)
        tit = pg.inner_text('#skpop-t') if pg.locator('#skpop').count() else ''
        ok('comparativa: el nombre abre la ventana de esa skill y queda expandido', NOMBRE_T2['en'] in tit
           and pg.get_attribute(bsel, 'aria-expanded') == 'true', tit)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        ok('comparativa: Esc la cierra y el foco vuelve al nombre', pg.locator('#skpop').count() == 0
           and pg.evaluate(f"document.activeElement === document.querySelector('{bsel}')"))
        fx = f'.cmpfx[data-k="{clave}"][data-si="{SI_T2}"]'
        if pg.locator(fx).count():
            pg.locator(fx).first.click(); pg.wait_for_timeout(200)
            foco = pg.evaluate("() => { const f = document.querySelector('#skpop details.tipef.foco'); return !!f && f.open; }")
            ok('comparativa: un efecto abre la ventana desplegada en ese efecto', foco)
            pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        else:
            ok('comparativa: la Tier-2 de Doctor Voodoo muestra efectos que no son daño', False)

        # ---- 4. el «?» de «Por potenciador» cerca del borde de abajo ----
        pg.click('[data-a="cmpVista"][data-v="pot"]'); pg.wait_for_timeout(400)
        n = pg.locator('main details.ayuda').count()
        fuera = []
        for i in range(n):
            d = pg.locator('main details.ayuda').nth(i)
            if not d.is_visible(): continue
            d.evaluate("x => window.scrollTo({ top: x.getBoundingClientRect().top + scrollY - (innerHeight - 40), behavior: 'instant' })")
            pg.wait_for_timeout(60)
            d.locator('summary').click(); pg.wait_for_timeout(80)
            r = d.locator('.ayudatx').evaluate("x => { const r = x.getBoundingClientRect(); return [r.top, r.bottom, r.left, r.right]; }")
            if r[0] < 0 or r[1] > 768 + 1 or r[2] < 0 or r[3] > 1366: fuera.append((i, r))
            d.locator('summary').click(); pg.wait_for_timeout(50)
        ok(f'«Por potenciador»: los {n} «?» abiertos cerca del borde de abajo quedan dentro de la ventana', n > 0 and not fuera, fuera[:3])
        pg.click('[data-a="ayudaToggle"]'); pg.wait_for_timeout(250)
        vis = pg.evaluate("[...document.querySelectorAll('details.ayuda')].filter(x => x.checkVisibility()).length")
        ok('desactivada: sin «?» a la vista', pg.locator('details.ayuda').count() > 0 and vis == 0, vis)
        pg.click('[data-a="ayudaToggle"]'); pg.wait_for_timeout(250)
        ok('compu: sin errores de página ni de consola', not errores, errores[:3])
        b.close()

        # ---- 5. celular ----
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); escuchar(pg)
        pg.goto(url); pg.wait_for_selector('.ccard')
        abrir_ficha(pg, 'doctor-voodoo', VOODOO['id'])
        pg.tap(f'#skt-{SI_T2}'); pg.wait_for_timeout(250)
        ok('celular: tocar la skill abre la hoja, sin tooltip', pg.locator('#skpop').count() == 1 and flotante(pg) is None)
        ok('celular: sin errores de página ni de consola', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
