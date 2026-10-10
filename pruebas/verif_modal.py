"""La ventana del «Por qué» (carril modal, 5 de octubre de 2026). Ezequiel, 4 de octubre, mirando el «Por qué» de una
combinación de Ghost Rider y su tabla de C.T.P.: «Esto se tiene que poder ver más prolijo y legible... El desglose, podés
ponerlo en un modal, con los retratos para cada personaje». Chequea, sin work/:
1. La tarjeta (combinación y «cómo entraría»): el botón «Por qué y C.T.P.» donde se desplegaba el «Por qué», y nada del
   desglose, del detalle de PvP y PvE ni del bloque de C.T.P. en línea (van en la ventana; una sola ruta). Tus equipos y
   favoritos siguen con su bloque de C.T.P. plegado.
2. Abre: un <dialog> modal (:modal), con aria-modal, su título (aria-labelledby) y el foco en el título; la página de atrás
   no se mueve (no se recorre) y no recibe clics.
3. Arriba: los tres retratos con el líder primero y su marca (aro y «Líder»), los mismos puntos que la tarjeta, quién lidera
   y por qué (lo que suma su liderazgo con la cuenta de la app, y lo de los demás) y de dónde salen los puntos: las partes
   suman el puntaje de la tarjeta (sin contexto, la sinergia para él; en PvP, el del contexto) y los strikers no suman.
4. Pestañas: una por integrante, en el orden de los retratos, la del personaje de la ficha elegida al abrir; el clic, ← →,
   Inicio y Fin (con la vuelta); una sola visible y con tabindex que rota. Cada una con su retrato, lo que recibe (Efecto |
   Total | De dónde: cada parte con el retrato de quien la da y el enlace a su skill o artefacto) y lo que aporta.
5. El foco no sale: Tab y Shift+Tab dan la vuelta adentro. ← y → no pasan de ficha. Esc, el botón ✕ y el fondo la cierran,
   y el foco vuelve al botón de la tarjeta.
6. «Atrás»: de un enlace de la ventana a la skill de un compañero, el botón «Atrás» y el volver del navegador vuelven a la
   lista con la ventana abierta, en la misma pestaña y a la misma altura.
7. PvP (Adam Warlock — GotG3 + Wasp — Quantumania + Doctor Voodoo — Savage Avengers): las partes del contexto, quién lidera
   («Lidera Wasp: su liderazgo suma 10,5 en PvP») y «Además»; y «cómo entraría» (Jeff en Black Cat + Doctor Voodoo + Thor):
   el equipo de después, «Se gana» y «Se pierde».
8. Inglés: los rótulos de la ventana, sin restos en castellano.
9. Celular (390 px): a pantalla completa, sin scroll horizontal de la página ni de la ventana, pestañas que se tocan, y en la
   tabla «De dónde» va debajo del efecto.
10. Los colores: con los tokens de :root claros (puestos en la prueba: la app no tiene tema claro), el cuadro, los chips y
   las pestañas los siguen.
11. Sin errores de página ni de consola.
Capturas en carril-modal/shots: modal_{1300,390}_{oscuro,claro}.png (y _completo, el cuerpo entero), modal_pvp_1300_oscuro.png
y modal_entra_1300_oscuro.png."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright

ok = Chequeo()
SH = SALIDA
os.makedirs(SH, exist_ok=True)
ADAM, BC, JEFF = 'adam-warlock::adam-warlock-10200152', 'black-cat::black-cat-10400009', 'jeff-the-land-shark::base'
WASP, DV = 'wasp::wasp-10300051', 'doctor-voodoo::doctor-voodoo-10200204'
EQUIPO = {'id': 'eq-porque', 'name': 'Prueba del porqué', 'modeId': '', 'reason': '', 'members': [BC, DV, 'thor::base']}
FAVORITO = {'id': 'fav-1', 'members': [ADAM, BC, JEFF], 'ctx': None}
# Tokens claros (solo para la prueba y las capturas: la app es oscura).
CLARO = """:root{--bg:#f4f5f9;--bg-2:#e9ecf3;--surface:#ffffff;--surface-2:#f1f3f8;--surface-3:#e3e7ef;--text:#141925;
  --text-2:rgba(20,25,37,.72);--text-3:rgba(20,25,37,.5);--line:rgba(20,25,37,.1);--line-2:rgba(20,25,37,.2);--accent:#e0193f;
  --accent-2:#c8102e;--accent-soft:rgba(224,25,63,.1);--accent-glow:rgba(224,25,63,.3);--gold:#9a6400;--gold-soft:rgba(154,100,0,.12);
  --allies:#1d5fd0;--self:#15803d;--enemy:#c02626;--role-soporte:#15803d;color-scheme:light}"""
COMPLETO = ('dialog.pqdlg{max-height:none !important;height:auto !important;top:0 !important;bottom:auto !important;'
            'margin-top:0 !important;margin-bottom:0 !important} #pqdlg .pqm-cuerpo{overflow:visible !important}')

LEER = r"""() => {
  const pl = (el) => el ? el.textContent.replace(/\s+/g, ' ').trim() : null, d = document.getElementById('pqdlg');
  const sec = (k) => [...d.querySelectorAll('.pqm-sec')].find(s => pl(s.querySelector(':scope > h3')) === k);
  const lista = (ul) => ul ? [...ul.querySelectorAll(':scope > li')].map(li => [[...li.childNodes].filter(n => n.nodeName !== 'UL')
    .map(n => n.textContent).join('').replace(/\s+/g, ' ').trim(), [...li.querySelectorAll(':scope > ul > li')].map(pl)]) : null;
  const panel = d.querySelector('[role="tabpanel"]:not([hidden])');
  const hs = panel ? [...panel.querySelectorAll(':scope > h4')] : [];
  return {
    abierto: d.open, modal: d.matches(':modal'), ariaModal: d.getAttribute('aria-modal'), etiqueta: d.getAttribute('aria-labelledby'),
    titulo: pl(d.querySelector('#' + d.getAttribute('aria-labelledby'))), foco: document.activeElement && document.activeElement.id,
    sub: pl(d.querySelector('.pqm-sub')),
    fotos: [...d.querySelectorAll('.pqm-equipo .eqfoto')].map(f => ({ key: f.dataset.cid + '::' + (f.dataset.uid || 'base'), lider: f.classList.contains('lider'),
      pill: pl(f.querySelector('.pillider')), nuevo: f.classList.contains('nuevo'), boton: f.tagName === 'BUTTON' || f.hasAttribute('data-a') })),
    pts: pl(d.querySelector('.pqm-equipo .eqpts')), porque: pl(d.querySelector('.pqm-porque')),
    partes: [...d.querySelectorAll('.pqm-parte')].map(p => [pl(p.querySelector(':scope > .pqm-parteh > b')), pl(p.querySelector('.pqm-pts')),
      [...p.querySelectorAll(':scope > ul > li')].map(pl)]),
    tabs: [...d.querySelectorAll('[role="tab"]')].map(b => ({ key: b.dataset.key, sel: b.getAttribute('aria-selected'), ti: b.tabIndex, txt: pl(b),
      lider: b.classList.contains('lider'), foto: !!b.querySelector('.shot'), panel: b.getAttribute('aria-controls') })),
    visibles: [...d.querySelectorAll('[role="tabpanel"]')].filter(p => !p.hidden).map(p => p.id),
    panel: panel && { id: panel.id, quien: pl(panel.querySelector('.pqm-quien')), h: hs.map(pl),
      cols: [...panel.querySelectorAll('.pqm-th [role="columnheader"]')].map(pl),
      filas: [...panel.querySelectorAll('.pqm-fila:not(.pqm-th)')].map(f => [pl(f.querySelector('.pqm-ef')), pl(f.querySelector('.pqm-tot')),
        [...f.querySelectorAll('.pqm-de1')].map(c => ({ txt: pl(c), foto: !!c.querySelector('.shot'), enlace: !!c.querySelector('[data-a="irSkill"]') }))]),
      aporta: lista(panel.querySelector(':scope > ul.pqm-lista')), nada: [...panel.querySelectorAll(':scope > p.muted')].map(pl) },
    ademas: lista((sec(window.__ademas) || { querySelector: () => null }).querySelector(':scope > ul')),
    secciones: [...d.querySelectorAll('.pqm-sec > h3')].map(pl),
    ctp: (s => s && { rotulo: pl(s.querySelector(':scope > h3')), filas: [...s.querySelectorAll('tbody th')].map(th => pl(th)) })(d.querySelector('.pqm-sec.ga-eq')),
    html: getComputedStyle(document.documentElement).overflowY, ancho: [d.scrollWidth, d.clientWidth],
  };
}"""


def leer(pg, ademas='Además'):
    pg.evaluate('(k) => { window.__ademas = k; }', ademas)
    return pg.evaluate(LEER)


def num(s):
    """Un número de la app en castellano o en inglés: «+10,5*» → 10.5."""
    m = re.search(r'[\d.,]+', s or '')
    x = m.group(0)
    return float(x.replace('.', '').replace(',', '.')) if ',' in x or re.fullmatch(r'\d{1,3}(\.\d{3})+', x) else float(x)


def ficha(pg, nombre, cid, uid=None, tab='equipos'):
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', nombre); pg.wait_for_timeout(250)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid: pg.select_option('select[data-a="uniformSel"]', uid)
    pg.click(f'[data-a="fichaTab"][data-v="{tab}"]')
    if tab == 'equipos': pg.wait_for_selector('#combos .combo', timeout=90000)


def trio_card(pg, *cids):
    c = pg.locator('#combos .combo')
    for x in cids: c = c.filter(has=pg.locator(f'.eqfoto[data-cid="{x}"]'))
    return c.first


def abrir(pg, card):
    """Abre la ventana de la tarjeta con su botón; deja en window.__y la altura de la página antes del clic."""
    boton = card.locator('[data-a="pqAbrir"]')
    boton.scroll_into_view_if_needed(); pg.evaluate('window.__y = scrollY')
    boton.click(); pg.wait_for_selector('#pqdlg[open]'); pg.wait_for_timeout(80)
    return boton


def ev(pg, js, arg=None):
    """Una función de app.js, por el gancho (window.__ev)."""
    return pg.evaluate('([js, arg]) => window.__ev(js)(arg)', [js, arg])


def estado(pg): return pg.evaluate('({ ...history.state })')
def cuerpo_y(pg): return pg.evaluate("document.querySelector('#pqdlg .pqm-cuerpo').scrollTop")
def activo_en_dialogo(pg): return pg.evaluate("document.getElementById('pqdlg').contains(document.activeElement)")


D = carpeta_datos()
json.dump({'teams': [EQUIPO], 'favoritos': [FAVORITO]}, open(os.path.join(D, 'capa.json'), 'w', encoding='utf-8'), ensure_ascii=False)
srv, url = levantar(D, origen_local())
errores = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        def gancho(route):
            r = route.fetch(); route.fulfill(response=r, body=r.text().replace('\narrancar();\n})();', '\nwindow.__ev = s => eval(s);\narrancar();\n})();'))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(90000)

        # 1. La tarjeta.
        ficha(pg, 'Adam Warlock', 'adam-warlock', ADAM.split('::')[1])
        card = trio_card(pg, 'black-cat', 'jeff-the-land-shark')
        t = card.evaluate("""c => ({ boton: [...c.querySelectorAll('[data-a="pqAbrir"]')].map(b => [b.textContent.trim(), b.getAttribute('aria-haspopup'),
          b.previousElementSibling && b.previousElementSibling.classList.contains('combofila')]),
          enLinea: c.querySelectorAll('details, .cxpts, .pqm-parte, .ga-eq, table').length,
          lider: c.querySelector('.combolider').textContent.trim(), pts: c.querySelector('.eqpts').textContent.replace(/\\s+/g, ' ').trim(),
          fotos: [...c.querySelectorAll('.eqfoto')].map(f => f.dataset.cid + '::' + (f.dataset.uid || 'base')) })""")
        ok('1 la tarjeta: el botón «Por qué y C.T.P.» (abre una ventana) después de la fila, donde se desplegaba el «Por qué»',
           t['boton'] == [['Por qué y C.T.P.', 'dialog', True]], t['boton'])
        ok('1 la tarjeta no trae el desglose, el detalle ni el bloque de C.T.P. en línea', t['enLinea'] == 0, t['enLinea'])

        # 2. Abre.
        boton = abrir(pg, card)
        y0 = pg.evaluate('window.__y')
        R = leer(pg)
        ok('2 abre un <dialog> modal, con aria-modal y su título', R['abierto'] and R['modal'] and R['ariaModal'] == 'true'
           and R['etiqueta'] == 'pqm-t' and R['titulo'] == 'Por qué · Puntos para él', {k: R[k] for k in ('abierto', 'modal', 'ariaModal', 'titulo')})
        ok('2 el foco, en el título de la ventana', R['foco'] == 'pqm-t', R['foco'])
        ok('2 la página de atrás no se recorre (overflow oculto) ni se movió', R['html'] == 'hidden' and pg.evaluate('scrollY') == y0, (R['html'], pg.evaluate('scrollY'), y0))
        pg.mouse.move(650, 500); pg.mouse.wheel(0, 600); pg.wait_for_timeout(150)
        ok('2 la rueda recorre la ventana, no la página', pg.evaluate('scrollY') == y0 and cuerpo_y(pg) > 0, (pg.evaluate('scrollY'), cuerpo_y(pg)))
        pg.evaluate("document.querySelector('#pqdlg .pqm-cuerpo').scrollTop = 0")

        # 3. Arriba.
        ok('3 los tres retratos, el líder primero con su marca (aro y «Líder») y el de la ficha con su aro; no abren nada',
           [f['key'] for f in R['fotos']] == t['fotos'] and R['fotos'][0]['key'] == BC and R['fotos'][0]['lider'] and R['fotos'][0]['pill'] == 'Líder'
           and not any(f['lider'] for f in R['fotos'][1:]) and [f['nuevo'] for f in R['fotos']] == [f['key'] == ADAM for f in R['fotos']]
           and not any(f['boton'] for f in R['fotos']), R['fotos'])
        ok('3 los puntos, los mismos de la tarjeta', R['pts'] == t['pts'], (R['pts'], t['pts']))
        ok('3 el subtítulo nombra el trío con el líder primero', R['sub'] == 'Black Cat — Queen in Black + Adam Warlock — Marvel Studios\' Guardians of the Galaxy 3 + Jeff the Land Shark', R['sub'])
        cand = ev(pg, """(ks) => { const vs = ks.map(k => variant(...k.split('::'))); return candidatosLider(vs, null).map(c => [c.m.key, c.tiene, c.pts]); }""",
                  [ADAM, BC, JEFF])
        pts_bc = next(c[2] for c in cand if c[0] == BC)
        ok('3 quién lidera y por qué: lo que suma su liderazgo en la sinergia (la cuenta de la app) y lo de los demás',
           R['porque'].startswith(f'Lidera Black Cat: su liderazgo suma {pts_bc:g} en la sinergia') and 'Los demás: ' in R['porque']
           and all((x[0].split('::')[0].replace('-', ' ') in R['porque'].lower()) or x[0] == BC for x in cand), (R['porque'], cand))
        suma = sum(num(x[1]) for x in R['partes'] if x[1])
        ok('3 de dónde salen los puntos: las partes suman los puntos para él de la tarjeta', abs(suma - num(t['pts'])) < 1e-9
           and [x[0] for x in R['partes']][:1] == ['Liderazgo de Black Cat'], (suma, t['pts'], [x[:2] for x in R['partes']]))
        st = [x for x in R['partes'] if x[0].startswith('Desempate')]
        ok('3 los strikers, como desempate y sin puntos', all(x[1] is None for x in st), st)

        # 4. Pestañas.
        ok('4 una pestaña por integrante, en el orden de los retratos, con su retrato; el líder marcado',
           [x['key'] for x in R['tabs']] == t['fotos'] and all(x['foto'] for x in R['tabs']) and R['tabs'][0]['lider']
           and R['tabs'][0]['txt'] == 'Black Cat Líder', R['tabs'])
        ok('4 elegida la del personaje de la ficha, con su panel visible (uno solo) y el tabindex que rota',
           [x['sel'] for x in R['tabs']] == [str(x['key'] == ADAM).lower() for x in R['tabs']] and [x['ti'] for x in R['tabs']] == [0 if x['key'] == ADAM else -1 for x in R['tabs']]
           and R['visibles'] == [next(x['panel'] for x in R['tabs'] if x['key'] == ADAM)], (R['tabs'], R['visibles']))
        P = R['panel']
        ok('4 el panel: quién es, lo que recibe (Efecto | Total | De dónde) y lo que aporta',
           P['quien'] == "Adam Warlock — Marvel Studios' Guardians of the Galaxy 3" and P['h'] == ['Lo que recibe Adam Warlock', 'Lo que aporta Adam Warlock']
           and P['cols'] == ['Efecto', 'Total', 'De dónde'], P)
        ok('4 cada renglón: efecto, total y de dónde (cada parte con el retrato de quien la da y el enlace a su skill o artefacto)',
           len(P['filas']) == 10 and all(f[2] and all(c['foto'] and c['enlace'] for c in f[2]) for f in P['filas'])
           and P['filas'][0][:2] == ['Todos los ataques básicos', '+65%'] and P['filas'][0][2][0]['txt'] == 'Black Cat: Liderazgo +65%',
           P['filas'][:2])
        vill = next(f for f in P['filas'] if f[0] == 'Daño básico a villanos')
        ok('4 un renglón con artefactos: el total con «*» y lo que llega sin ellos; cada parte, de quién',
           vill[1] == '+75% +0,7% del instinto total* (sin artefactos: +45%)'
           and [c['txt'] for c in vill[2]] == ['Jeff the Land Shark: Pasiva 4★ +45%', 'Black Cat: Persona of Desire (a 6★) +10% +0,2% del instinto total*',
                                              'Jeff the Land Shark: Baby Land Shark (a 6★) +20% +0,5% del instinto total*'], vill)
        tabs = pg.locator('#pqdlg [role="tab"]')
        tabs.nth(2).click(); pg.wait_for_timeout(60)
        R2 = leer(pg)
        ok('4 el clic elige otra pestaña: su panel, solo', [x['sel'] for x in R2['tabs']] == ['false', 'false', 'true'] and R2['visibles'] == ['pqm-p2']
           and R2['panel']['h'][0] == 'Lo que recibe Jeff the Land Shark', (R2['tabs'], R2['visibles']))
        pasos = []
        for tecla in ('ArrowRight', 'ArrowRight', 'ArrowLeft', 'End', 'Home', 'ArrowLeft'):
            pg.keyboard.press(tecla); pg.wait_for_timeout(40)
            pasos.append(pg.evaluate("""() => [[...document.querySelectorAll('#pqdlg [role="tab"]')].findIndex(b => b.getAttribute('aria-selected') === 'true'),
              [...document.querySelectorAll('#pqdlg [role="tab"]')].indexOf(document.activeElement),
              [...document.querySelectorAll('#pqdlg [role="tabpanel"]')].filter(p => !p.hidden).map(p => p.id).join()]"""))
        ok('4 ← → Inicio y Fin pasan de pestaña (con la vuelta), llevan el foco y muestran su panel',
           pasos == [[0, 0, 'pqm-p0'], [1, 1, 'pqm-p1'], [0, 0, 'pqm-p0'], [2, 2, 'pqm-p2'], [0, 0, 'pqm-p0'], [2, 2, 'pqm-p2']], pasos)
        bc = (tabs.nth(0).click(), pg.wait_for_timeout(60), leer(pg))[2]['panel']
        ok('4 lo que aporta el líder (a los otros dos): su liderazgo, su Tier-2 y su artefacto, con el enlace y a quiénes',
           bc['aporta'] and bc['aporta'][0] == ['Liderazgo → Adam Warlock, Jeff the Land Shark', ['Todos los ataques básicos +65%', 'Ignorar esquiva +35%']]
           and [x[0] for x in bc['aporta'][1:]] == ['Pasiva de Tier-2 → Adam Warlock, Jeff the Land Shark', 'Persona of Desire (a 6★) (si lleva su artefacto) → Adam Warlock, Jeff the Land Shark'],
           bc['aporta'])
        tabs.nth(1).click(); pg.wait_for_timeout(60)

        # 5. El foco no sale; ← → no pasan de ficha; Esc, ✕ y el fondo cierran; el foco vuelve al botón.
        pg.locator('#pqm-t').focus()
        dentro = []
        for _ in range(45):
            pg.keyboard.press('Tab'); dentro.append(activo_en_dialogo(pg))
        for _ in range(45):
            pg.keyboard.press('Shift+Tab'); dentro.append(activo_en_dialogo(pg))
        ok('5 Tab y Shift+Tab (45 veces cada uno) no sacan el foco de la ventana', all(dentro), dentro.count(False))
        pg.locator('#pqm-t').focus(); pg.keyboard.press('Shift+Tab')
        ultimo = pg.evaluate("""() => { const fs = [...document.querySelectorAll('#pqdlg button, #pqdlg a[href], #pqdlg summary, #pqdlg [tabindex="0"]')]
          .filter(x => x.getClientRects().length && x.tabIndex >= 0); return document.activeElement === fs[fs.length - 1]; }""")
        pg.keyboard.press('Tab')
        primero = pg.evaluate("document.activeElement === document.querySelector('#pqdlg [data-a=\"pqCerrar\"]')")
        ok('5 Shift+Tab desde el título va al último y Tab desde el último, al primero (el botón de cerrar)', ultimo and primero, (ultimo, primero))
        pg.locator('#pqm-t').focus()
        antes = estado(pg)
        pg.keyboard.press('ArrowRight'); pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(150)
        ok('5 ← y → no pasan de ficha con la ventana abierta', estado(pg)['charId'] == antes['charId'] and leer(pg)['abierto'], estado(pg)['charId'])
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        ok('5 Esc la cierra y el foco vuelve al botón de la tarjeta', not leer(pg)['abierto'] and boton.evaluate('b => b === document.activeElement')
           and pg.evaluate('getComputedStyle(document.documentElement).overflowY') != 'hidden', leer(pg)['abierto'])
        abrir(pg, card); pg.click('#pqdlg [data-a="pqCerrar"]'); pg.wait_for_timeout(100)
        ok('5 el ✕ la cierra y el foco vuelve al botón', not leer(pg)['abierto'] and boton.evaluate('b => b === document.activeElement'))
        abrir(pg, card)
        # 1.0.25: con los tres paneles, el «Descartar» queda debajo de la ventana; el clic va al fondo, sobre la lista
        # de la izquierda (abajo hay una ficha que se abriría)
        ficha_antes = estado(pg)['charId']
        pg.mouse.click(40, 450); pg.wait_for_timeout(300)
        ok('5 el clic en el fondo no abre lo de la lista de atrás', estado(pg)['charId'] == ficha_antes, estado(pg)['charId'])
        capa = json.load(open(os.path.join(D, 'capa.json'), encoding='utf-8'))
        ok('5 un clic en el fondo la cierra, sin tocar lo de atrás (el «Descartar» de la tarjeta no se apretó)',
           not leer(pg)['abierto'] and not capa.get('descartados') and boton.evaluate('b => b === document.activeElement'), capa.get('descartados'))
        abrir(pg, card)
        pg.screenshot(path=f'{SH}/modal_1300_oscuro.png')
        estilo = pg.add_style_tag(content=CLARO); pg.wait_for_timeout(100)
        colores = pg.evaluate("""() => { const d = document.getElementById('pqdlg'), cs = (el) => getComputedStyle(el);
          const raiz = getComputedStyle(document.documentElement), tok = (k) => raiz.getPropertyValue(k).trim();
          const prueba = document.createElement('div'); document.body.appendChild(prueba);
          const color = (v) => { prueba.style.color = v; return getComputedStyle(prueba).color; };
          const r = { cuadro: [cs(d).backgroundColor, color(tok('--surface'))], texto: [cs(d).color, color(tok('--text'))],
            chip: [cs(d.querySelector('.pqm-de1')).backgroundColor, color(tok('--surface-2'))],
            pestaña: [cs(d.querySelector('[role="tab"][aria-selected="true"]')).backgroundColor, color(tok('--surface-2'))],
            linea: [cs(d.querySelector('.pqm-cab')).borderBottomColor, color(tok('--line'))] };
          prueba.remove(); return r; }""")
        ok('10 con los tokens claros, el cuadro, el texto, los chips, las pestañas y las líneas los siguen',
           all(a == b for a, b in colores.values()), colores)
        pg.screenshot(path=f'{SH}/modal_1300_claro.png')
        pg.set_viewport_size({'width': 1300, 'height': 3400}); est = pg.add_style_tag(content=COMPLETO); pg.wait_for_timeout(150)
        pg.locator('#pqdlg').screenshot(path=f'{SH}/modal_1300_claro_completo.png')
        estilo.evaluate('s => s.remove()'); pg.wait_for_timeout(80)
        pg.locator('#pqdlg').screenshot(path=f'{SH}/modal_1300_oscuro_completo.png')
        est.evaluate('s => s.remove()'); pg.set_viewport_size({'width': 1300, 'height': 900}); pg.wait_for_timeout(100)
        pg.keyboard.press('Escape')

        # 6. «Atrás» con la ventana abierta en otra pestaña y más abajo (PvP: Adam + Wasp + Doctor Voodoo).
        pg.select_option('select[data-a="eqOrden"]', 'pvp'); pg.wait_for_timeout(300); pg.wait_for_selector('#combos .combo')
        while not trio_card(pg, 'wasp', 'doctor-voodoo').count():
            sig = pg.locator('#combos [data-a="eqPagina"]').last
            if sig.is_disabled(): break
            sig.click(); pg.wait_for_timeout(250)
        card = trio_card(pg, 'wasp', 'doctor-voodoo')
        PAG = estado(pg)['eqPagina']
        abrir(pg, card)
        R = leer(pg)
        ok('7 PvP: el título, el líder primero y lo que suma su liderazgo en PvP', R['titulo'] == 'Por qué · PvP' and R['fotos'][0]['key'] == WASP
           and R['porque'].startswith('Lidera Wasp: su liderazgo suma 10,5 en PvP.'), (R['titulo'], R['porque']))
        ok('7 PvP: las partes del contexto (anti-mermas sin puntos; liderazgo, DPS y soportes con los suyos; desempate)',
           [x[0] for x in R['partes']] == ['Anti-mermas', 'Liderazgo de Wasp', 'DPS', 'Soportes y bonos de equipo', 'Desempate: 2 strikers']
           and [x[1] for x in R['partes']] == [None, '+10,5', '+4', '+3', None]
           and abs(sum(num(x[1]) for x in R['partes'] if x[1]) - num(R['pts'].split('pts')[0])) < 1e-9, R['partes'])
        ok('7 PvP: «Además», lo de los puntos para él (bonos, roles, clases y ventaja de clase)', 'Además' in R['secciones'] and R['ademas'], R['secciones'])
        ok('7 PvP: los C.T.P. de PvP, en la ventana', R['ctp'] and R['ctp']['rotulo'] == 'C.T.P. recomendados: Meta PvP · Fuera del meta PvP · Ideal CTP List' and len(R['ctp']['filas']) == 3, R['ctp'])
        pg.screenshot(path=f'{SH}/modal_pvp_1300_oscuro.png')
        pg.locator('#pqdlg [role="tab"]').nth(2).click(); pg.wait_for_timeout(60)
        pg.evaluate("document.querySelector('#pqdlg .pqm-cuerpo').scrollTop = 260"); y_dlg = cuerpo_y(pg)
        y_card = trio_card(pg, 'wasp', 'doctor-voodoo').bounding_box()['y']   # la tarjeta en la pantalla (scrollY lo pueden mover las fuentes web)
        tab_key = leer(pg)['tabs'][2]['key']
        enlace = pg.locator('#pqdlg [role="tabpanel"]:not([hidden]) .pqm-de [data-a="irSkill"]').first
        destino = enlace.evaluate('b => [b.dataset.cid, b.dataset.tab, b.dataset.ancla]')
        enlace.click(); pg.wait_for_selector('.fcab'); pg.wait_for_timeout(200)
        e = estado(pg)
        ok('6 el enlace de la ventana lleva a la skill en la ficha de quien la da, y la ventana se cierra',
           [e['charId'], e['fichaTab']] == destino[:2] and not leer(pg)['abierto'] and pg.locator('.resaltada').count() == 1, (e['charId'], e['fichaTab'], destino))
        pg.click('[data-a="atras"]'); pg.wait_for_selector('#pqdlg[open]', timeout=90000); pg.wait_for_timeout(300)
        R = leer(pg)
        ok('6 «Atrás»: la lista de PvP en su página (la tarjeta en su lugar), con la ventana abierta en la misma pestaña y a la misma altura',
           estado(pg)['eqPagina'] == PAG and R['abierto'] and next(x for x in R['tabs'] if x['sel'] == 'true')['key'] == tab_key
           and abs(cuerpo_y(pg) - y_dlg) < 3 and abs(trio_card(pg, 'wasp', 'doctor-voodoo').bounding_box()['y'] - y_card) < 5 and R['foco'] == 'pqm-t',
           (estado(pg)['eqPagina'], PAG, cuerpo_y(pg), y_dlg, round(trio_card(pg, 'wasp', 'doctor-voodoo').bounding_box()['y']), round(y_card), R['foco']))
        pg.locator('#pqdlg [role="tabpanel"]:not([hidden]) .pqm-de [data-a="irSkill"]').first.click(); pg.wait_for_selector('.fcab'); pg.wait_for_timeout(200)
        pg.go_back(); pg.wait_for_selector('#pqdlg[open]', timeout=90000); pg.wait_for_timeout(300)
        ok('6 el volver del navegador, lo mismo', leer(pg)['abierto'] and next(x for x in leer(pg)['tabs'] if x['sel'] == 'true')['key'] == tab_key
           and abs(cuerpo_y(pg) - y_dlg) < 3, cuerpo_y(pg))
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        ok('6 al cerrarla, el foco vuelve al botón de su tarjeta', pg.evaluate("document.activeElement.dataset.a") == 'pqAbrir'
           and trio_card(pg, 'wasp', 'doctor-voodoo').locator('[data-a="pqAbrir"]').evaluate('b => b === document.activeElement'))
        pg.select_option('select[data-a="eqOrden"]', 'foco'); pg.wait_for_timeout(300)

        # 7. «Cómo entraría»: Jeff en Black Cat + Doctor Voodoo + Thor.
        ficha(pg, 'Jeff the Land Shark', 'jeff-the-land-shark')
        sug = pg.locator('.card.eqsug', has_text=EQUIPO['name']).first
        ok('7 «cómo entraría»: el botón en la tarjeta y nada en línea', sug.locator('[data-a="pqAbrir"]').count() == 1
           and sug.locator('details, .ga-eq, table').count() == 0)
        pts_sug = sug.locator('.eqpts').text_content().strip()
        abrir(pg, sug)
        R = leer(pg, 'Se gana, además de lo de Jeff the Land Shark')
        ok('7 «cómo entraría»: el título con el equipo, en lugar de quién, y los puntos de la tarjeta',
           R['titulo'] == 'Por qué · Prueba del porqué' and R['sub'].endswith('· en lugar de Thor') and re.sub(r'\s+', ' ', pts_sug) == R['pts'], (R['titulo'], R['sub'], R['pts']))
        ok('7 «cómo entraría»: las partes suman la sinergia de después', abs(sum(num(x[1]) for x in R['partes'] if x[1]) - num(R['pts'])) < 1e-9, R['partes'])
        ok('7 «cómo entraría»: «Se gana» y «Se pierde»; la pestaña de Jeff, elegida',
           R['secciones'][-3:] == ['Se gana, además de lo de Jeff the Land Shark', 'Se pierde', 'C.T.P. recomendados: Mejor · 2.º mejor · Ideal CTP List'] and R['ademas']
           and next(x for x in R['tabs'] if x['sel'] == 'true')['key'] == JEFF, R['secciones'])
        pg.screenshot(path=f'{SH}/modal_entra_1300_oscuro.png')
        pg.keyboard.press('Escape')
        pg.click('[data-a="goTeams"]'); pg.wait_for_timeout(300)
        ok('1 Equipos de tu cuenta y Favoritos: su bloque de C.T.P., plegado, como antes', pg.locator('.grid .card details.ga-eq').count() == 2
           and not pg.locator('.grid .card details.ga-eq[open]').count() and pg.locator('.grid .card [data-a="pqAbrir"]').count() == 0,
           pg.locator('.grid .card details.ga-eq').count())

        # 8. Inglés.
        pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ficha(pg, 'Adam Warlock', 'adam-warlock', ADAM.split('::')[1])
        card = trio_card(pg, 'black-cat', 'jeff-the-land-shark')
        ok('8 inglés: el botón', card.locator('[data-a="pqAbrir"]').inner_text() == 'Why and C.T.P.', card.locator('[data-a="pqAbrir"]').inner_text())
        abrir(pg, card)
        R = leer(pg, 'Also')
        ok('8 inglés: el título, quién lidera, las columnas y los títulos del panel', R['titulo'] == 'Why · Points for it'
           and R['porque'].startswith(f'Black Cat leads: its leadership adds {pts_bc:g} to the synergy') and R['panel']['cols'] == ['Effect', 'Total', 'From']
           and R['panel']['h'] == ['What Adam Warlock gets', 'What Adam Warlock gives'] and R['tabs'][0]['txt'] == 'Black Cat Leader'
           and R['secciones'][:2] == ['Where the points come from', 'Members'], (R['titulo'], R['porque'], R['panel']['h'], R['secciones']))
        texto = pg.locator('#pqdlg').inner_text()
        restos = [x for x in ('Lo que recibe', 'Lo que aporta', 'De dónde', 'Lidera ', 'Los demás', 'Integrantes', 'Soportes', 'Además', 'Efecto',
                              'Se pierde', 'a todos', 'del instinto', 'al recibir', 'Liderazgo', 'Cerrar', 'recomendados', 'Desempate', 'Roles cubiertos')
                  if x in texto]
        ok('8 inglés: sin restos en castellano en la ventana', not restos, restos)
        ok('8 inglés: el ✕ dice «Close (Esc)»', pg.locator('#pqdlg [data-a="pqCerrar"]').get_attribute('aria-label') == 'Close (Esc)')
        pg.screenshot(path=f'{SH}/modal_1300_oscuro_en.png')
        pg.keyboard.press('Escape'); pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('11 sin errores de página ni de consola (compu)', not errores, errores[:3])
        b.close()

        # 9. Celular.
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(90000)
        ficha(pg, 'Adam Warlock', 'adam-warlock', ADAM.split('::')[1])
        card = trio_card(pg, 'black-cat', 'jeff-the-land-shark')
        boton = card.locator('[data-a="pqAbrir"]'); boton.scroll_into_view_if_needed(); boton.tap(); pg.wait_for_selector('#pqdlg[open]'); pg.wait_for_timeout(100)
        caja = pg.locator('#pqdlg').bounding_box()
        R = leer(pg)
        ok('9 celular: a pantalla completa', [round(caja[k]) for k in ('x', 'y', 'width', 'height')] == [0, 0, 390, 844], caja)
        fuera = pg.evaluate("""() => { const out = []; for (const el of document.querySelectorAll('#pqdlg *')) { const r = el.getBoundingClientRect();
          if (r.width && r.right > 390.5) out.push(el.className || el.tagName); } return out.slice(0, 5); }""")
        ok('9 celular: sin scroll horizontal de la página ni de la ventana, y nada se sale',
           pg.evaluate('document.documentElement.scrollWidth') <= 390 and R['ancho'][0] <= R['ancho'][1] and not fuera, (R['ancho'], fuera))
        pg.locator('#pqdlg [role="tab"]').nth(2).tap(); pg.wait_for_timeout(80)
        R = leer(pg)
        ok('9 celular: las pestañas se tocan', [x['sel'] for x in R['tabs']] == ['false', 'false', 'true'] and R['visibles'] == ['pqm-p2'])
        apila = pg.evaluate("""() => { const f = document.querySelector('#pqdlg [role="tabpanel"]:not([hidden]) .pqm-fila:not(.pqm-th)');
          const a = f.querySelector('.pqm-ef').getBoundingClientRect(), d = f.querySelector('.pqm-de').getBoundingClientRect(); return d.top >= a.bottom - 1; }""")
        ok('9 celular: «De dónde» va debajo del efecto', apila)
        pg.locator('#pqdlg [role="tab"]').nth(1).tap(); pg.wait_for_timeout(80)
        pg.screenshot(path=f'{SH}/modal_390_oscuro.png')
        pg.evaluate("document.querySelector('#pqdlg .pqm-cuerpo').scrollTop = document.querySelector('#pqdlg .pqm-tabs').offsetTop - 70")
        pg.screenshot(path=f'{SH}/modal_390_oscuro_pestanas.png')
        estilo = pg.add_style_tag(content=CLARO); pg.wait_for_timeout(80)
        pg.screenshot(path=f'{SH}/modal_390_claro_pestanas.png')
        pg.evaluate("document.querySelector('#pqdlg .pqm-cuerpo').scrollTop = 0"); pg.wait_for_timeout(50)
        pg.screenshot(path=f'{SH}/modal_390_claro.png')
        pg.set_viewport_size({'width': 390, 'height': 4200}); est = pg.add_style_tag(content=COMPLETO); pg.wait_for_timeout(150)
        pg.locator('#pqdlg').screenshot(path=f'{SH}/modal_390_claro_completo.png')
        estilo.evaluate('s => s.remove()'); pg.wait_for_timeout(80)
        pg.locator('#pqdlg').screenshot(path=f'{SH}/modal_390_oscuro_completo.png')
        est.evaluate('s => s.remove()'); pg.set_viewport_size({'width': 390, 'height': 844}); pg.wait_for_timeout(100)
        pg.locator('#pqdlg [data-a="pqCerrar"]').tap(); pg.wait_for_timeout(100)
        ok('9 celular: el ✕ la cierra', not leer(pg)['abierto'])
        ok('11 sin errores de página ni de consola (celular)', not errores, errores[:3])
        b.close()
finally:
    srv.terminate(); srv.wait()
ok.fin()
