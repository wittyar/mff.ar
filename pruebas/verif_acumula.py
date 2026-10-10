"""Qué se acumula y los topes (carril filtro2, segunda parte, 5 de octubre de 2026). Ezequiel: «el daño contra facciones si
se suma. EL ataque se suma. La defensa se suma. la vida se suma... Hay algunas estadsiticas que llegana tope, indice critico,
daño critico, esquiva. Las habilidades especificas, inmunidad a romper guardia, por ejemplo no se solapan es decir cuenta una
sola vez». Datos de formato 8: cada stat de soporte del catálogo dice si se acumula (acumula) y su tope (tope: claves de los
topes de la guía).
1. La app lee la regla del catálogo: para cada stat de los liderazgos, soportes y bonos, seAcumula dice lo mismo que
   MFF_CATALOGO.soporte (leído acá aparte), todos lo dicen, y los que cuentan una vez son los 25 esperados (Guaranteed Critical Rate desde la 1.0.22).
2. La de mayor valor (con líneas de prueba puestas en la página): Wolverine con «Lightning Immunity Chance» 80 contra la
   propia de Storm, 50: se le aplica la de 80 a los tres, la de Storm va atenuada («no se suma: ya lo tiene de Wolverine…»), el
   total es 80 y la pasiva de Storm «no suma». A igual valor (Wolverine y Captain America, 80), decide el orden: con Storm de
   líder, los demás por clave (captain-america antes que wolverine).
3. Topes (líneas de prueba): prob. de crítico 50 + 40 (pasa 75), vel. de ataque 20 + 15 (130 desde 100: quedan 30), recarga
   −30 − 25 (por su valor absoluto: 55 contra 50), daño crítico 20 (no pasa); un renglón con condición se cuenta con lo que le
   llega siempre. Sin pasar, con los datos: un liderazgo de crítico real muestra el tope y no avisa. El tope y la base salen de
   MFF_GUIA.topes (leído acá aparte), con su fuente.
4. Glosario: si se suma o cuenta una vez y el tope, efecto por efecto, como el catálogo; los que eran dudosos, con la nota de Ezequiel.
5. Lo que iniciarDatos confirma de los datos (data.js cambiado antes de arrancar): un anti-mermas con valor, líneas que no se
   pueden comparar y un soporte con más valor que un liderazgo cortan el arranque con su mensaje.
6. Inglés, celular (la ventana con el tope y el aviso, sin desborde) y capturas (shots/topes_*.png, acumula_glosario_*.png).
   Sin errores de página ni de consola (salvo los del punto 5, que se esperan)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, DATOS
from playwright.sync_api import sync_playwright

ok = Chequeo()
SH = SALIDA
FIN = '\narrancar();\n})();'
NO_ACUM = {'Guaranteed Critical Rate', 'Remove All Debuffs', 'Debuff Immunity', 'Burn Immunity', 'Fear Immunity', 'Stun Immunity', 'Guard Break Immunity',
           'Incapacitation Immunity', 'Physical Immunity Chance', 'Fire Immunity Chance', 'Lightning Immunity Chance',
           'Mind Immunity Chance', 'Barrier', 'Max HP Shield', 'Revive with % HP', 'Summon', 'Immortality + Death',
           'Immortality + Heal', 'Ignores Damage Increase/Decrease Effect Between Self and Opposing Faction',
           # #10 (9 de octubre de 2026): los de los liderazgos derivados de la Leader Skill
           'All Damage Immunity', 'Cold Immunity Chance', 'Energy Shield', 'Physical Shield', 'Bleed Immunity', 'Fracture Immunity'}
ST, WO, CA = 'storm::base', 'wolverine::base', 'captain-america::base'

def gancho_app(route):
    r = route.fetch(); s = r.text()
    if s.count(FIN) != 1: raise SystemExit('app.js no termina como se esperaba')
    route.fulfill(response=r, body=s.replace(FIN, '\nwindow.__ev = s => eval(s);' + FIN))

# Lo que dice la tabla de lo que recibe un integrante, con las líneas de prueba puestas: por renglón, el efecto, el total, el
# tope, el aviso y de dónde (con si va atenuada cada parte). poner: [[clave, slot, línea]]; se sacan al terminar.
TABLA = r"""([poner, keys, foco, ctx]) => {
  const por = new Map(allVariants().map(x => [x.key, x])), viejas = [];
  for (const [k, slot, x] of poner) { const so = SOPORTES[por.get(k).p]; viejas.push([so, slot, so[slot]]); so[slot] = x; }
  _NO_ACUM_DE.clear(); _SLOTS.clear();
  try {
    const vs = keys.map(k => por.get(k)), e = ctx ? enContexto(vs, ctx, true) : null, lider = e ? e.lider : liderDe(vs, null);
    const pl = (el) => el ? el.textContent.replace(/\s+/g, ' ').trim() : null;
    const m = vs[keys.indexOf(foco)], d = document.createElement('div');
    d.innerHTML = recibeTablaHtml(m, sumaDe(origenesDe(m, vs, lider)), nombreEn(vs), 'x');
    const filas = [...d.querySelectorAll('.pqm-fila:not(.pqm-th)')].map(f => ({
      ef: pl(f.querySelector('.pqm-ef').firstChild), cond: pl(f.querySelector('.pqm-cond')), tot: pl(f.querySelector('.pqm-tot')),
      tope: pl(f.querySelector('.pqtope')), fuente: (f.querySelector('.pqtope a.fuente') || {}).textContent || null,
      pasa: pl(f.querySelector('.pqpasa')), rep: f.classList.contains('rep'),
      de: [...f.querySelectorAll('.pqm-de1')].map(x => [pl(x), x.classList.contains('rep')]) }));
    const sc = synergy(vs, { lider });
    return { lider: lider && lider.key, filas,
             razones: sc.razones.filter(r => r.tipo === 'soporte').map(r => [r.de.key, r.k, r.pts, r.a.map(x => x.key)]) };
  } finally {
    for (const [so, slot, x] of viejas) if (x === undefined) delete so[slot]; else so[slot] = x;
    _NO_ACUM_DE.clear(); _SLOTS.clear();
  }
}"""

def patch_soportes(data, cambio):
    """data.js con MFF_SOPORTES cambiado por cambio(soportes)."""
    m = re.search(r'^window\.MFF_SOPORTES = ', data, re.M)
    obj, fin = json.JSONDecoder().raw_decode(data, m.end())
    cambio(obj)
    return data[:m.end()] + json.dumps(obj, ensure_ascii=False) + data[fin:]

errores = []
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        pg.route(lambda u: '/app.js' in u, gancho_app)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(120000)
        ev = lambda js, a=None: pg.evaluate('([js, a]) => window.__ev(js)(a)', [js, a])

        # 1. la regla, del catálogo
        r = ev(r"""() => { const stats = new Set(), mal = [];
          for (const so of Object.values(SOPORTES)) for (const x of Object.values(so)) if (x && x.fx) for (const f of x.fx) stats.add(f.s);
          for (const b of BONOS) for (const v of b.v) for (const [s] of v) stats.add(s);
          for (const s of stats) { const c = window.MFF_CATALOGO.soporte[s];
            if (!c || typeof c.acumula !== 'boolean' || seAcumula({ s }) !== c.acumula) mal.push(s); }
          return { n: stats.size, mal, no: [...stats].filter(s => !seAcumula({ s })).sort(),
                   cat: Object.keys(window.MFF_CATALOGO.soporte).filter(s => !window.MFF_CATALOGO.soporte[s].acumula).sort() }; }""")
        ok('1 cada stat de los liderazgos, soportes y bonos dice si se acumula, y la app (seAcumula) dice lo mismo que el catálogo',
           r['n'] > 70 and not r['mal'], {k: r[k] for k in ('n', 'mal')})
        ok('1 los que cuentan una vez son los 25 (las habilidades y Guaranteed Critical Rate)', set(r['cat']) == NO_ACUM, sorted(set(r['cat']) ^ NO_ACUM))

        # 2. la de mayor valor
        NOM = ev("() => Object.fromEntries(['Lightning Immunity Chance', 'Critical Rate', 'Attack Speed', 'Skill Cooldown', 'Critical Damage'].map(s => [s, trTxt(s)]))")
        LIC = lambda v: {'fx': [{'s': 'Lightning Immunity Chance', 'v': v}]}
        t = ev(TABLA, [[[WO, 'passive2', LIC(80)]], [ST, WO, CA], CA, None])
        fila = [f for f in t['filas'] if f['ef'] == NOM['Lightning Immunity Chance']]
        ok('2 a Captain America le llega la de Storm (50) y la de Wolverine (80): se le aplica la de 80, el total es 80 y la de Storm va atenuada',
           len(fila) >= 1 and any(f['tot'] and f['tot'].startswith('+80') and not f['rep'] for f in fila)
           and any(any(rep and d.startswith('Storm') and 'no se suma: ya lo tiene de Wolverine' in d for d, rep in f['de']) for f in fila), fila)
        ok('2 la pasiva de Storm no suma (no se le aplica a nadie) y la de prueba de Wolverine sí',
           any(k == ST and s == 'passive' and pts == 0 for k, s, pts, a in t['razones']) and any(k == WO and s == 'passive2' and pts > 0 for k, s, pts, a in t['razones']),
           t['razones'])
        t2 = ev(TABLA, [[[WO, 'passive2', LIC(80)]], [ST, WO, CA], ST, None])
        f2 = [f for f in t2['filas'] if f['ef'] == NOM['Lightning Immunity Chance']]
        ok('2 a Storm tampoco: la suya, propia, pierde con la de mayor valor', any(any(rep and d.startswith('Storm') for d, rep in f['de']) for f in f2)
           and any(f['tot'] and f['tot'].startswith('+80') for f in f2), f2)
        # a igual valor, el orden: lidera Storm (líder sin contexto de este trío, si lo es) y los demás por clave
        t3 = ev(TABLA, [[[WO, 'passive2', LIC(80)], [CA, 't22', LIC(80)]], [ST, WO, CA], ST, None])
        f3 = [f for f in t3['filas'] if f['ef'] == NOM['Lightning Immunity Chance']]
        aplicada = [d for f in f3 for d, rep in f['de'] if not rep]
        esperado = 'Captain America' if t3['lider'] not in (WO,) else 'Wolverine'
        ok(f'2 a igual valor (80 y 80) decide el orden: líder {t3["lider"]}, después por clave; se le aplica la de {esperado}',
           len(aplicada) == 1 and aplicada[0].startswith(esperado), (t3['lider'], f3))

        # 3. topes
        guia = ev("() => window.MFF_GUIA.topes")
        tope = {k: (it['tope'], it.get('base') or 0) for it in guia['items'] if it['tope'] is not None for k in it['stats']}
        fuente = ev("() => window.MFF_GUIA.fuentes[window.MFF_GUIA.topes.fuente[0]].nombre")
        ac = ev("() => { for (const so of Object.values(SOPORTES)) for (const x of Object.values(so)) if (x && x.ac) return x.ac; return null; }")
        prueba = [[WO, 'passive2', {'fx': [{'s': 'Critical Rate', 'v': 50}, {'s': 'Attack Speed', 'v': 20}, {'s': 'Skill Cooldown', 'v': -30}]}],
                  [ST, 't22', {'fx': [{'s': 'Critical Rate', 'v': 40}, {'s': 'Attack Speed', 'v': 15}, {'s': 'Skill Cooldown', 'v': -25},
                                      {'s': 'Critical Damage', 'v': 20}]}]]
        t = ev(TABLA, [prueba, [WO, ST, CA], CA, None])
        F = {f['ef']: f for f in t['filas']}
        crit, vel, rec, cd = (F.get(NOM[x]) for x in ('Critical Rate', 'Attack Speed', 'Skill Cooldown', 'Critical Damage'))
        ok(f'3 prob. de crítico: 50 + 40 = 90, «Tope de la guía: {tope["crit"][0]}%.», con la fuente, y el aviso (quedan {tope["crit"][0] - tope["crit"][1]})',
           crit and crit['tot'].startswith('+90') and crit['tope'].startswith(f'Tope de la guía: {tope["crit"][0]}%.') and crit['fuente'] == fuente
           and crit['pasa'] == f'Pasa el tope: los potenciadores suman 90% y hasta el tope quedan {tope["crit"][0] - tope["crit"][1]}%; lo de más no suma.', crit)
        ok(f'3 vel. de ataque: 20 + 15 = 35, tope {tope["aspd"][0]}% desde {tope["aspd"][1]}%: quedan {tope["aspd"][0] - tope["aspd"][1]} y avisa',
           vel and vel['tope'].startswith(f'Tope de la guía: {tope["aspd"][0]}% (desde {tope["aspd"][1]}%).')
           and vel['pasa'] == f'Pasa el tope: los potenciadores suman 35% y hasta el tope quedan {tope["aspd"][0] - tope["aspd"][1]}%; lo de más no suma.', vel)
        ok('3 recarga: −30 − 25, por su valor absoluto (55) contra 50, avisa', rec and rec['tot'].startswith('−55')
           and rec['pasa'] == f'Pasa el tope: los potenciadores suman 55% y hasta el tope quedan {tope["cd"][0]}%; lo de más no suma.', rec)
        ok('3 daño crítico: 20 no pasa lo que queda (100): el tope sin aviso', cd and cd['tope'] and not cd['pasa'], cd)
        if ac:
            prueba_c = [[WO, 'passive2', {'fx': [{'s': 'Critical Rate', 'v': 50}]}], [ST, 't22', {'ac': ac, 'fx': [{'s': 'Critical Rate', 'v': 30}]}]]
            t = ev(TABLA, [prueba_c, [WO, ST, CA], CA, None])
            cs = [f for f in t['filas'] if f['ef'] == NOM['Critical Rate']]
            siempre, cond = next((f for f in cs if not f['cond']), None), next((f for f in cs if f['cond']), None)
            ok('3 con condición: el renglón condicional (30) se cuenta con lo que llega siempre (50): «Con lo que le llega siempre, pasa el tope… 80%»',
               siempre and not siempre['pasa'] and cond and cond['pasa'] == f'Con lo que le llega siempre, pasa el tope: los potenciadores suman 80% y hasta el tope quedan {tope["crit"][0]}%; lo de más no suma.', cs)
        else:
            ok('3 hay una línea con condición en los datos para la prueba', False, ac)
        # sin pasar, con datos reales: un liderazgo de crítico
        real = ev(r"""() => { for (const v of allVariants()) { const so = SOPORTES[v.p]; if (!so || !so.leader || !so.leader.fx.some(f => f.s === 'Critical Rate')) continue;
            const otros = allVariants().filter(x => x.cid !== v.cid).slice(0, 40);
            for (let i = 0; i < otros.length; i++) for (let j = i + 1; j < otros.length; j++) { const vs = [v, otros[i], otros[j]];
              if (otros[i].cid === otros[j].cid || liderDe(vs, null) !== v) continue;
              const d = document.createElement('div'); d.innerHTML = recibeTablaHtml(otros[i], sumaDe(origenesDe(otros[i], vs, v)), nombreEn(vs), 'x');
              const f = [...d.querySelectorAll('.pqm-fila:not(.pqm-th)')].find(x => x.querySelector('.pqm-ef').firstChild.textContent.trim() === trTxt('Critical Rate'));
              if (f) return [vs.map(x => x.key), f.querySelector('.pqm-tot').textContent.trim(), (f.querySelector('.pqtope') || {}).textContent, !!f.querySelector('.pqpasa')]; } }
          return null; }""")
        ok('3 con datos reales (un liderazgo de crítico): el tope, sin aviso', real and real[2] and real[2].strip().startswith(f'Tope de la guía: {tope["crit"][0]}%.') and not real[3], real)

        # 4. Glosario
        pg.evaluate("window.__ev('ui.view = \"glosario\"; ui.glTab = \"app\"; ui.glBusca = \"\"; render()')"); pg.wait_for_selector('#ef-critico', state='attached')
        gl = pg.evaluate("""() => Object.fromEntries(['critico', 'quita_debuffs', 'ataques_todos', 'curacion', 'velocidades', 'resistencias', 'inmune_elemento', 'superarmadura']
          .map(id => [id, [...document.querySelectorAll('#ef-' + id + ' .annota')].map(x => x.textContent.replace(/\\s+/g, ' ').trim())]))""")
        linea = lambda id, pre: next((x for x in gl[id] if x.startswith(pre)), None)
        dos = 'Si a alguien le llega de dos fuentes (liderazgo, soporte o bono de equipo):'
        ok('4 quitar todos los debuffs: cuenta una vez; todos los ataques: se suma', linea('quita_debuffs', dos) == dos + ' cuenta una vez, la de mayor valor'
           and linea('ataques_todos', dos) == dos + ' se suma', [linea('quita_debuffs', dos), linea('ataques_todos', dos)])
        ok('4 inmunidad a un elemento (probabilidad): cuenta una vez', linea('inmune_elemento', dos) == dos + ' cuenta una vez, la de mayor valor', gl['inmune_elemento'])
        cur = linea('curacion', dos)
        ok('4 curación: uno por uno, con la nota de Ezequiel (la curación se suma y no es la tasa de recuperación)', cur and 'Curación: se suma' in cur
           and 'otra cosa que el índice de recuperación' in cur and '[Conjetura]' not in cur and 'cuenta una vez' in cur, cur)
        sup = linea('superarmadura', dos)
        ok('4 superarmadura con defensas: se suma, con la nota de Ezequiel', sup and 'se suma' in sup and 'Ezequiel, 5 de octubre de 2026' in sup
           and '[Conjetura]' not in sup, sup)
        top = 'Tope, en un liderazgo, soporte o bono de equipo:'
        ok('4 crítico: el tope de la guía con su fuente', linea('critico', top) == f'{top} {tope["crit"][0]}% {fuente}', linea('critico', top))
        ok('4 velocidades: los dos topes, con nombre', linea('velocidades', top) and 'Velocidad atq. 130% (desde 100%)' in linea('velocidades', top)
           and 'Velocidad de movimiento 130% (desde 100%)' in linea('velocidades', top), linea('velocidades', top))
        ok('4 resistencias: 200%', linea('resistencias', top) == f'{top} {tope["elemres"][0]}% {fuente}', linea('resistencias', top))
        # #24: el efecto va plegado; a la vista, la marca corta de si se suma o cuenta una vez y la del tope
        marca = lambda id_: pg.locator(f'#ef-{id_} > summary .glmarcas').text_content()
        ok('4 a la vista: quitar todos los debuffs, «cuenta una vez»; crítico, su tope', 'cuenta una vez' in marca('quita_debuffs')
           and f'tope {tope["crit"][0]}%' in marca('critico'), [marca('quita_debuffs'), marca('critico')])
        for id_ in ('curacion', 'critico'):
            pg.evaluate(f"document.getElementById('ef-{id_}').open = true")
            pg.locator(f'#ef-{id_}').scroll_into_view_if_needed(); pg.wait_for_timeout(150)
            pg.locator(f'#ef-{id_}').screenshot(path=f'{SH}/acumula_glosario_{id_}.png')

        # 6. la ventana con el tope y el aviso (líneas de prueba), en castellano, inglés y celular
        def ventana(png, ancho):
            pg.set_viewport_size({'width': ancho, 'height': 900})
            pg.evaluate("""([poner, id]) => window.__ev(`(() => { const por = new Map(allVariants().map(x => [x.key, x]));
              window.__viejas = ${JSON.stringify(poner)}.map(([k, slot, x]) => { const so = SOPORTES[por.get(k).p], v = [so, slot, so[slot]]; so[slot] = x; return v; });
              _NO_ACUM_DE.clear(); _SLOTS.clear();
              ui.view = 'detail'; ui.charId = 'captain-america'; ui.uniformId = 'base'; render();
              abrirPq({ id: ${JSON.stringify(id)}, charId: 'captain-america', uid: 'base', tab: 'captain-america::base', y: 0 }); })()`)""",
              [prueba, f'c||{CA},{WO},{ST}'])
            pg.wait_for_selector('#pqdlg[open]')
            pg.evaluate("document.querySelector('#pqdlg .pqm-panel:not([hidden]) .pqpasa').scrollIntoView({ block: 'center' })"); pg.wait_for_timeout(250)
            pg.screenshot(path=f'{SH}/{png}')
            fuera = pg.evaluate("""() => { const d = document.querySelector('#pqdlg'), lim = d.getBoundingClientRect().right;
              return [...d.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect(); return r.width && r.right > lim + 0.5; })
                .map(e => (e.className || e.tagName)).slice(0, 4); }""")
            avisos = pg.evaluate("() => [...document.querySelectorAll('#pqdlg .pqm-panel:not([hidden]) .pqpasa')].map(x => x.textContent)")
            pg.evaluate("window.__ev('cerrarPq(false); for (const [so, slot, x] of window.__viejas) if (x === undefined) delete so[slot]; else so[slot] = x; _NO_ACUM_DE.clear(); _SLOTS.clear();')")
            return fuera, avisos
        fuera, avisos = ventana('topes_1300.png', 1300)
        ok('6 en la ventana, en la pestaña de Captain America: los avisos de crítico, vel. de ataque y recarga', len(avisos) == 3, avisos)
        fuera, avisos = ventana('topes_390.png', 390)
        ok('6 celular: la ventana con el tope y el aviso, sin desborde', not fuera and len(avisos) == 3, fuera)
        pg.set_viewport_size({'width': 1300, 'height': 900})
        pg.click('[data-a="lang"]'); pg.wait_for_selector('.ccard, .fcab, .glbusca')
        t = ev(TABLA, [prueba, [WO, ST, CA], CA, None])
        F = {f['ef']: f for f in t['filas']}
        en = F.get(ev("() => trTxt('Critical Rate')"))
        ok('6 inglés: «Guide cap: 75%.» y «Over the cap: the buffs add up to 90% and only 75% is left to the cap; the rest adds nothing.»',
           en and en['tope'].startswith(f'Guide cap: {tope["crit"][0]}%.') and en['pasa'] == f'Over the cap: the buffs add up to 90% and only {tope["crit"][0]}% is left to the cap; the rest adds nothing.', en)
        pg.evaluate("window.__ev('ui.view = \"glosario\"; ui.glTab = \"app\"; render()')"); pg.wait_for_selector('#ef-critico', state='attached')
        gl_en = pg.evaluate("() => [...document.querySelectorAll('#ef-quita_debuffs .annota, #ef-critico .annota')].map(x => x.textContent.replace(/\\s+/g, ' ').trim())")
        ok('6 inglés, Glosario: «it counts once, the highest value» y «Cap, in a leadership, support or team bonus: 75%»',
           any(x.endswith('it counts once, the highest value') for x in gl_en) and any(x.startswith('Cap, in a leadership, support or team bonus: 75%') for x in gl_en), gl_en)
        pg.click('[data-a="lang"]')
        b.close()

        # 5. lo que iniciarDatos confirma: cada caso, en una página con el data.js cambiado; el arranque corta con su mensaje
        data = open(f'{DATOS}/data.js', encoding='utf-8').read()
        def rad_con_valor(so):
            # todas las líneas con número (si fuera una sola, cortaría antes por no poder compararlas)
            for p, s in so.items():
                for k, x in s.items():
                    if isinstance(x, dict):
                        for f in x.get('fx', []):
                            if f['s'] == 'Remove All Debuffs': f['v'] = 50
        def barrera_mezclada(so):
            for p, s in so.items():
                for k, x in s.items():
                    if isinstance(x, dict) and any(f['s'] == 'Barrier' for f in x.get('fx', [])):
                        next(f for f in x['fx'] if f['s'] == 'Barrier')['v'] = 2
                        return
        def escudo_soporte(so):
            p = next(p for p, s in so.items() if not s.get('passive2'))
            so[p]['passive2'] = {'fx': [{'s': 'Max HP Shield', 'v': 99}]}
        for nombre, cambio, msj in (('anti-mermas con valor (todas las líneas de quitar todos los debuffs con número)', rad_con_valor, 'anti-mermas con valor (Remove All Debuffs)'),
                                    ('una barrera con número y otra con texto', barrera_mezclada, 'Barrier no se acumula y sus líneas no se pueden comparar'),
                                    ('un soporte con más valor que un liderazgo', escudo_soporte, 'un soporte trae Max HP Shield con más valor que un liderazgo')):
            nuevo = patch_soportes(data, cambio)
            b2 = p.chromium.launch(); pg2 = b2.new_page(); errs = []
            pg2.on('pageerror', lambda e: errs.append(str(e)))
            pg2.route(lambda u: u.split('?')[0].endswith('/data.js'), lambda route: route.fulfill(status=200, body=nuevo, content_type='application/javascript'))
            pg2.goto(url); pg2.wait_for_timeout(4000)
            # Desde la 1.0.31 el error no queda suelto: la pantalla de error lo muestra y se le avisa al servidor (rescate).
            fatal = pg2.evaluate("(document.querySelector('.fatal p') || {}).textContent || ''")
            ok(f'5 {nombre}: el arranque corta con «{msj}…»', msj in fatal and not errs, (fatal[:200], errs[:2]))
            b2.close()
finally:
    srv.terminate(); srv.wait()

ok('sin errores de página ni de consola', not errores, errores[:5])
ok.fin()
