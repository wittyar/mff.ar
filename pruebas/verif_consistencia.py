"""Consistencia entre pantallas (carril de consistencia, 4 de octubre de 2026): la misma pregunta tiene que tener la
misma respuesta en cada pantalla que la contesta. Para las 888 variantes, cada pregunta junta lo que dice cada
pantalla (el HTML que pinta la app, leído con el DOM, o la función que ese lugar usa) y falla si difieren.

Preguntas que ya tienen respuesta única (la auditoría de inventario-app.md, secciones 2 y 4):
- formato_soportes: cada efecto de un liderazgo, un soporte o un bono de equipo dice lo mismo en el Resumen, el «Cómo
  funciona», el «Por qué», la comparativa, los bonos de la ficha y el detalle de PvP y PvE (tríos al azar).
- verificacion: el Resumen y Más cuentan las mismas diferencias entre fuentes, y Más lista esas.
- recarga: la tarjeta de la skill, su «Cómo funciona» y la comparativa dicen la misma recarga (en dos niveles).
- tier_list: la fila de cada variante en cada lista, con su «+N», es la misma en el roster (tarjeta y tabla), el
  Resumen y la tarjeta de combinación; la comparativa muestra todas esas filas.
- habilidades: el filtro de habilidad del roster y el editor ofrecen todas las habilidades que muestran las fichas.
- efectos_de_skill: la comparativa muestra todos los efectos de cada skill que muestra su tarjeta (los primeros a la
  vista y el resto plegado).
- strikers: la probabilidad de cada striker (y la marca de dato imposible) es la misma en la ficha, el «Por qué» y
  el detalle de PvP y PvE.

Preguntas que dependen de una regla que está decidiendo Ezequiel (PENDIENTES, abajo): no se prueban todavía. Para
sumar una, se le pone `js` (una función que se evalúa en la página con el gancho de verif_velres.py y devuelve
{casos, mal, ejemplos}) y queda en la lista de las que corren.

Con el data.js de hoy, «habilidades» falla (Zombi y Guardianes de la Galaxia): lo arregla el próximo build. Para
probar con lo que va a dar ese build: armar_datos_build.py ORIGEN DESTINO y MFF_DATOS=DESTINO."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo
from playwright.sync_api import sync_playwright

ok = Chequeo()

# Comunes: se evalúan una vez en la página y quedan en window.__c.
COMUNES = r"""() => {
  const pl = (el) => el ? el.textContent.replace(/\s+/g, ' ').trim() : null;
  const doc = (html) => { const d = document.createElement('div'); d.innerHTML = html; return d; };
  const vs = allVariants();
  // La comparativa de a pares (las 888 variantes, en 444 comparaciones): cada columna, por variante.
  // La vista «Ficha» de la comparativa (desde la 1.0.35 abre por efecto).
  const cmp = new Map(), picks = ui.picks, vista = ui.cmpVista;
  ui.cmpVista = 'ficha';
  for (let i = 0; i < vs.length; i += 2) {
    const par = [vs[i], vs[(i + 1) % vs.length]];
    ui.picks = par.map(v => ({ cid: v.cid, uid: v.uid, key: v.key }));
    const d = doc(renderCompare());
    // Las filas de las listas van antes de las de los slots, en el orden de LISTS (dos listas pueden llamarse igual).
    const filas = [...d.querySelectorAll('table.cmpt > tbody > tr')], otras = filas.filter(tr => !tr.classList.contains('slotrow'));
    const ls = LISTS.filter(l => par.some(v => indicesFila(l, v.key).length)), deListas = otras.slice(otras.length - ls.length);
    if (ls.some((l, n) => pl(deListas[n].querySelector('th')) !== listName(l))) throw new Error('la comparativa no tiene las listas en el orden de LISTS');
    par.forEach((v, j) => {
      const slots = {}, listas = {};
      for (const tr of filas.filter(tr => tr.classList.contains('slotrow'))) slots[pl(tr.querySelector('th'))] = tr.querySelectorAll('td')[j];
      ls.forEach((l, n) => { listas[l.id] = deListas[n].querySelectorAll('td')[j]; });
      if (!cmp.has(v.key)) cmp.set(v.key, { slots, listas });
    });
  }
  ui.picks = picks; ui.cmpVista = vista;
  window.__c = { pl, doc, vs, cmp };
  return { variantes: vs.length, comparadas: cmp.size };
}"""

PREGUNTAS = [
  dict(id='formato_soportes', desc='cada efecto de liderazgo, soporte o bono, igual en el Resumen, el «Cómo funciona», el «Por qué», '
       'la comparativa, los bonos y el detalle de PvP y PvE', js=r"""() => {
  const { pl, doc, vs } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], pantallas: {} };
  const anota = (pantalla) => { out.pantallas[pantalla] = (out.pantallas[pantalla] || 0) + 1; };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  for (const v of vs) {
    const s = SOPORTES[v.p]; if (!s) continue;
    const tipos = TIPOS_SOPORTE.filter(([k]) => s[k]);
    const resumen = [...doc(usoSoportes(v)).querySelectorAll('.sops > .sop')].map(b => [...b.querySelectorAll('ul.sopfx > li')].map(pl));
    const como = {};
    v.skills.forEach((sk, si) => { const ls = soportesDeSkill(v, sk); if (!ls.length) return;
      [...doc(tipCuandoHtml(v, sk, entradasSkill(v, si), null, null)).querySelectorAll('details.tipls .sop')]
        .forEach((b, n) => { como[ls[n][0]] = [...b.querySelectorAll('ul.sopfx > li')].map(pl); }); });
    tipos.forEach(([k], n) => {
      const x = s[k], lid = LIDERAZGOS.includes(k);
      x.fx.forEach((f, i) => {
        out.casos++;
        const canon = efectoSoporteTxt(x, f), dice = { canon };
        dice.resumen = resumen[n] && resumen[n][i]; anota('resumen');
        if (como[k]) { dice.como = como[k][i]; anota('como'); }
        // A quien le llega y le sirve: la ventana del «Por qué» de su tarjeta (lo que aporta él, en su pestaña, y lo que recibe
        // el otro, en la tabla «Efecto | Total | De dónde»: el stat con su condición y, en «De dónde», su parte con el valor)
        // y la comparativa con los dos.
        const b = vs.find(b => b.cid !== v.cid && aplicaA(x, b) && sirve(f, b));
        if (b) {
          const lider = lid ? v : null, nombre = nombreEn([b, v]);
          // (cada efecto, sin el «→ a quiénes» que lleva si los efectos del slot no van a los mismos: desde el 5 de octubre de 2026,
          // uno que no se le suma va aparte)
          const aporta = [...doc(integranteHtml(v, [b, v], lider, 0, true)).querySelectorAll(':scope > .pqm-panel > ul.pqm-lista > li > ul > li')].map(li => pl(li).split(' → ')[0]);
          dice.porque = aporta.includes(canon) ? canon : aporta; anota('porque');
          const ep = efectoSoporte(x, f), ef = trTxt(ep.s) + (sinClasificar(ep.s) ? ` (${t('sy_unclassified')})` : '') + (ep.cond ? ` (${ep.cond})` : '');
          // el efecto de cada renglón, sin el tope de la guía que va debajo de los que tienen (desde la segunda parte del carril
          // filtro2; lo pregunta acumulacion_y_topes)
          const efTxt = (r) => { const c = r.querySelector('.pqm-ef').cloneNode(true); c.querySelectorAll('.pqtope, .pqpasa').forEach(x => x.remove()); return pl(c); };
          const fila = [...doc(integranteHtml(b, [b, v], lider, 0, true)).querySelectorAll('.pqm-tabla > .pqm-fila:not(.pqm-th)')]
            .find(r => efTxt(r) === ef);
          const de = fila ? [...fila.querySelectorAll('.pqm-de1 > span:last-child')].map(pl) : [];
          dice.porque_tabla = de.some(p => p.startsWith(nombre(v) + ': ') && p.replace(/\*$/, '').endsWith(ep.val ? ' ' + ep.val : '')) ? canon : [ef, ep.val, de];
          anota('porque_tabla');
          const linea = razonesTxt([{ tipo: lid ? 'liderazgo' : 'soporte', de: v, k, x, a: [b] }])[0], nb = ' → ' + fullLabel(b) + ': ';
          const piezas = linea.slice(linea.indexOf(nb) + nb.length).split(' · ');
          dice.comparativa = piezas.includes(canon) ? canon : piezas; anota('comparativa');
        }
        if (Object.values(dice).some(x => x !== canon && x !== undefined)) falla([fullLabel(v), k, dice]);
      });
    });
  }
  // Bonos de equipo: la ficha (Equipos › Bonos) y la comparativa.
  for (const ch of CHARS) for (const b of BONOS_DE[ch.id] || []) {
    if (b.m[0] !== ch.id) continue;
    const stats = new Set([...doc(bonosHtml(ch)).querySelectorAll('.card.bono .bonostats')].map(pl));
    const integrantes = b.m.map(c => variant(c, null));
    b.vs.forEach((x, i) => {
      out.casos++; anota('bonos');
      const piezas = x.fx.map(f => efectoSoporteTxt(x, f)), canon = piezas.join(' · ');
      // «Bono de equipo «X» (A + B) → A, B: efectos»: los efectos van después del primer «: » que sigue a «→».
      const comparativa = razonesTxt([{ tipo: 'bono', b, i, x, integrantes, a: integrantes }]).flatMap(l => l.slice(l.indexOf(': ', l.indexOf(' → ')) + 2).split(' · '));
      if (!stats.has(canon) || !comparativa.length || !comparativa.every(p => piezas.includes(p))) falla([b.n, i, { canon, comparativa }]);
    });
  }
  // Detalle de PvP y PvE: 400 tríos al azar por contexto (semilla fija); cada renglón del liderazgo.
  let semilla = 7; const azar = (n) => { semilla = (semilla * 1103515245 + 12345) % 2147483648; return semilla % n; };
  for (const ctx of ['pvp', 'pve']) {
    let hechos = 0, intentos = 0;
    while (hechos < 400 && intentos < 200000) {
      intentos++;
      const tr = [vs[azar(vs.length)], vs[azar(vs.length)], vs[azar(vs.length)]];
      if (new Set(tr.map(x => x.cid)).size < 3) continue;
      const e = enContexto(tr, ctx, true); if (!e) continue;
      hechos++;
      // Cada línea del liderazgo, con el formato de las demás pantallas y su fuente si sale de la API (40ebed3: el detalle
      // la dice en cada línea; los liderazgos de la API los deriva el build desde el carril Q).
      const canon = new Set(slotsDe(e.lider).lid.flatMap(x => x.fx.map(f => efectoSoporteTxt(x, f) + srcTxt(x))));
      const rotulo = t('cx_lider').replace('{x}', nombreEn(tr)(e.lider));
      const parte = [...doc(detalleContexto(e, tr, ctx)).querySelectorAll('.pqm-parte')].find(p => pl(p.querySelector('.pqm-parteh > b')) === rotulo);
      if (!parte) { falla([tr.map(fullLabel), ctx, 'el detalle no tiene la parte del liderazgo']); continue; }
      for (const li of parte.querySelectorAll(':scope > ul.pqm-lista > li')) {
        const txt = pl(li); if (txt === t('cx_lider_nada')) continue;
        out.casos++; anota('detalle_' + ctx);
        const cond = ': ' + t('cx_lider_cond').replace('{p}', numTxt(CONTEXTO[ctx].condicional * 100)), antes = txt.slice(0, txt.lastIndexOf(' → '));
        const piezas = (antes.endsWith(cond) ? antes.slice(0, -cond.length) : antes).split(' / ');
        if (!piezas.every(p => canon.has(p))) falla([tr.map(fullLabel), ctx, piezas, [...canon]]);
      }
    }
  }
  return out;
}"""),
  dict(id='verificacion', desc='el Resumen y Fuentes (antes Más) cuentan las mismas diferencias entre fuentes, y Más lista esas', js=r"""() => {
  const { pl, doc, vs } = window.__c, out = { casos: 0, mal: 0, ejemplos: [] };
  for (const v of vs) {
    out.casos++;
    const r = pl(doc(fichaResumen(v.ch, v)).querySelector('[data-a="irVerif"]'));
    const m = doc(fichaFuentes(v.ch, v)), n = pl(m.querySelector('.vfcuenta')), lis = m.querySelectorAll('ul.verif > li').length;
    const dif = verifDe(v.ch, v).dif.length;
    if (r !== n || (dif ? lis !== dif || !r.includes(String(dif)) : r !== null)) { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push([fullLabel(v), r, n, lis]); }
  }
  return out;
}"""),
  dict(id='recarga', desc='la recarga de cada skill, igual en su tarjeta, su «Cómo funciona» y la comparativa', js=r"""() => {
  const { pl, doc, vs, cmp } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], dos_niveles: 0 };
  const rot = t('tt_recarga') + ':';
  for (const v of vs) v.skills.forEach((sk, si) => {
    out.casos++;
    const tarjeta = pl(doc(skillCard(sk, v, si)).querySelector('.tag.rec'));
    const como = [...doc(tipCuandoHtml(v, sk, entradasSkill(v, si), null, null)).querySelectorAll(':scope > ul.tiplista > li')].map(pl).find(x => x.startsWith(rot)) || null;
    const td = cmp.get(v.key).slots[slotEs(sk.sl)], comparativa = td ? pl(td.querySelector('.tag.rec')) : null;
    if (tarjeta && tarjeta.includes('Leads & Supports')) out.dos_niveles++;
    if (!tarjeta || tarjeta !== como || tarjeta !== comparativa) { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push([fullLabel(v), sk.sl, tarjeta, como, comparativa]); }
  });
  return out;
}"""),
  dict(id='tier_list', desc='la fila de cada variante en cada lista (con «+N»), igual en el roster, la tabla, el Resumen y la tarjeta de '
       'combinación; la comparativa, todas sus filas', js=r"""() => {
  const { pl, doc, vs, cmp } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], con_mas: 0 }, ref = U.prefs.refList;
  for (const l of LISTS.filter(l => tipoLista(l) === 'personajes')) {
    U.prefs.refList = l.id;
    for (const v of vs) {
      out.casos++;
      const f = filaEn(l, v.key), esperado = f ? rankTexto(f).replace(/\s+/g, ' ').trim() : null;   // como lo lee pl()
      if (f && f.todas.length > 1) out.con_mas++;
      const dice = {
        roster: pl(doc(cardHtml(v)).querySelector('.tag.rank')),
        tabla: (x => x === '—' ? null : x)(pl(doc(tableHtml([v])).querySelector('tbody tr td:last-child'))),
        // el Resumen (1.0.27) ya no repite la fila de la lista de referencia: dice las cinco principales (Dónde rinde)
        combinacion: (x => x === '—' ? null : x)(pl(doc(puestoHtml(l, v.key)))),
      };
      const td = cmp.get(v.key).listas[l.id];
      const todas = td ? [...td.querySelectorAll('.tag')].map(pl) : [];
      if (Object.values(dice).some(x => x !== esperado) || JSON.stringify(todas) !== JSON.stringify(f ? f.todas.map(x => x.replace(/\s+/g, ' ').trim()) : [])) {
        out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push([listName(l), fullLabel(v), esperado, dice, todas]);
      }
    }
  }
  U.prefs.refList = ref;
  return out;
}"""),
  dict(id='habilidades', desc='el filtro de habilidad del roster y el editor ofrecen todas las habilidades que muestran las fichas', js=r"""() => {
  const { pl, doc, vs } = window.__c, out = { casos: 0, mal: 0, ejemplos: [] };
  const abierto = U.prefs.filtersOpen; U.prefs.filtersOpen = true;
  const filtro = new Set([...doc(toolbar(0, 0)).querySelectorAll('[data-a="filter"][data-cat="ab"]')].map(pl));
  U.prefs.filtersOpen = abierto;
  const draft = ui.edDraft, paso = ui.edStep; ui.edDraft = blankDraft(); ui.edStep = 0;
  const editor = new Set([...doc(renderEditor()).querySelectorAll('[data-a="edPick"][data-f="abilities"]')].map(pl));
  ui.edDraft = draft; ui.edStep = paso;
  const faltan = {};
  for (const v of vs) {
    out.casos++;
    const row = [...doc(fichaResumen(v.ch, v)).querySelectorAll('.fid > .row')].find(r => pl(r.querySelector('.muted')) === t('d_abilities'));
    const ficha = [...row.querySelectorAll('.tag')].map(pl);
    const fuera = ficha.filter(a => !filtro.has(a) || !editor.has(a));
    if (fuera.length) { out.mal++; fuera.forEach(a => { faltan[a] = (faltan[a] || 0) + 1; }); }
  }
  if (out.mal) out.ejemplos.push(faltan);
  out.filtro = filtro.size;
  return out;
}"""),
  dict(id='efectos_de_skill', desc='la comparativa muestra todos los efectos de cada skill que muestra su tarjeta', js=r"""() => {
  const { pl, doc, vs, cmp } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], plegados: 0 };
  for (const v of vs) v.skills.forEach((sk, si) => {
    out.casos++;
    // En la tarjeta, cada renglón del efecto va en su div (y la duración al final); la comparativa los junta con un espacio.
    const tarjeta = [...doc(skillCard(sk, v, si)).querySelectorAll('.fxline')].map(x => { const c = x.querySelector('.fxitems').cloneNode(true);
      c.querySelectorAll('.dur').forEach(d => d.remove());
      return pl(x.querySelector('.fxtag')) + ' | ' + [...c.querySelectorAll(':scope > div')].map(pl).join(' '); });
    const td = cmp.get(v.key).slots[slotEs(sk.sl)];
    const comparativa = [...td.querySelectorAll('.cmpfx')].map(x => { const c = x.cloneNode(true), tag = c.querySelector('.fxtag'); tag.remove(); return pl(tag) + ' | ' + pl(c); });
    if (td.querySelector('details.cmpmas')) out.plegados++;
    if (JSON.stringify(tarjeta) !== JSON.stringify(comparativa)) { out.mal++; if (out.ejemplos.length < 3) out.ejemplos.push([fullLabel(v), sk.sl, tarjeta.length, comparativa.length]); }
  });
  return out;
}"""),
  dict(id='strikers', desc='la probabilidad de cada striker (y la marca de dato imposible), igual en la ficha, el «Por qué» y el detalle', js=r"""() => {
  const { pl, doc } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], imposibles: 0 };
  const esperado = (p, cuando) => t('sk_' + cuando).replace('{p}', numTxt(p)) + (p > 100 ? ' ⚠' : '');
  for (const [cid, filas] of Object.entries(STRIKERS)) {
    const a = variant(cid, null), ficha = doc(strikersHtml(a.ch));
    for (const [x, p, cuando] of filas) {
      out.casos++;
      const b = variant(x, null), e = esperado(p, cuando);
      // 1.0.27: la tabla de strikers, una fila por personaje; la segunda columna, si aparece junto a él
      const fila = [...ficha.querySelectorAll('.sktabla tbody tr')].find(tr => tr.querySelector(`[data-cid="${x}"]`)), celda = fila && fila.querySelectorAll('td')[1];
      const enFicha = celda ? pl(celda) : null, marcaFicha = !!(celda && celda.querySelector('.imposible'));
      // La ventana del «Por qué» de los dos (sin contexto, con él en foco): el primer renglón del desempate, en sus puntos.
      const n = strikersDe([a, b], a).length, rot = mayuscula(t(n === 1 ? 'cx_desempate_1' : 'cx_desempate').replace('{n}', n));
      const parte = [...doc(pqHtml({ id: 'x', tab: null }, pqDatos('c||' + a.key + ',' + b.key))).querySelectorAll('.pqm-parte')]
        .find(pt => pl(pt.querySelector('.pqm-parteh > b')) === rot);
      const li = parte && parte.querySelector('ul.pqm-lista > li');
      const enPq = li ? pl(li).slice(pl(li).lastIndexOf('(') + 1, -1) : null, marcaPq = !!(li && li.querySelector('.imposible'));
      if (p > 100) out.imposibles++;
      if (enFicha !== e || enPq !== e || marcaFicha !== (p > 100) || marcaPq !== (p > 100)) { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push([cid, x, e, enFicha, enPq]); }
    }
  }
  // El detalle de PvP y PvE: un trío con el striker y su dueño, en cada contexto donde entre.
  for (const [cid, filas] of Object.entries(STRIKERS)) for (const [x, p, cuando] of filas) {
    if (p <= 100) continue;
    const a = variant(cid, null), b = variant(x, null);
    for (const ctx of ['pvp', 'pve']) for (const c of allVariants()) {
      if (c.cid === a.cid || c.cid === b.cid) continue;
      const e = enContexto([a, b, c], ctx, true); if (!e || !e.strikers) continue;
      // los strikers no suman: el detalle los dice como desempate («Desempate: N strikers»)
      const cab = mayuscula(t(e.strikers === 1 ? 'cx_desempate_1' : 'cx_desempate').replace('{n}', e.strikers));
      const parte = [...doc(detalleContexto(e, [a, b, c], ctx)).querySelectorAll('.pqm-parte')].find(pt => pl(pt.querySelector('.pqm-parteh > b')) === cab);
      const txt = parte ? [...parte.querySelectorAll('li')].map(pl).find(s => s.includes(esperado(p, cuando).replace(' ⚠', ''))) : null;
      out.casos++;
      if (!txt || !txt.endsWith('(' + esperado(p, cuando) + ')') || !parte.querySelector('.imposible') || parte.querySelector('.pqm-pts')) {
        out.mal++; out.ejemplos.push([cid, x, ctx, txt]); }
      break;
    }
  }
  return out;
}"""),  dict(id='strikers_desempatan', desc='los strikers no suman en ningún puntaje (sinergia, PvP y PvE): a igual puntaje desempatan, en '
       'el orden de las combinaciones, y la tarjeta y el detalle dicen cuántos', js=r"""() => {
  const { pl, doc } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], filas: 0, con_desempate: 0 };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  const antes = { eqOrden: ui.eqOrden, eqCobertura: ui.eqCobertura, eqExcluir: ui.eqExcluir, eqCon: ui.eqCon, eqVerDescartados: ui.eqVerDescartados };
  for (const k of ['adam-warlock::adam-warlock-10200152', 'thanos::thanos-10700075']) {
    const v = allVariants().find(x => x.key === k);
    CONSULTA = null; const q = consultaCon(v);
    for (const o of ['foco', 'pvp', 'pve', 'lista:tv-soportes']) {
      const ctx = o === 'pvp' || o === 'pve' ? o : null;
      if (ctx && !tieneFuncion(v, ctx)) continue;
      Object.assign(ui, { eqOrden: o, eqCobertura: [], eqExcluir: [], eqCon: '', eqVerDescartados: false }); q.vista = null;
      const ls = listasOrden(), filas = vistaConsulta(q).filas;
      let previo = null;
      for (const i of filas) {
        const vs = [v, q.pool[q.A[i]], q.pool[q.B[i]]];
        const e = ctx ? enContexto(vs, ctx, true) : null, lider = e ? e.lider : liderDe(vs, null);
        const pts = e ? e.score : synergy(vs, { foco: v, lider }).score, stk = e ? e.strikers : cuantosStrikers(vs, v);
        // en PvP y PvE el orden es puntaje, strikers y después puestos; en una tier list, puestos, puntaje y strikers
        const ps = ctx ? 0 : ls.reduce((n, l) => n + puesto(l, vs[1].key) + puesto(l, vs[2].key), 0);
        out.filas++; out.casos++;
        if (stk !== (e ? strikersDe(vs, null) : strikersDe(vs, v)).length) falla([k, o, 'cuenta', vs.map(x => x.key)]);
        if (e && e.score !== e.partes.lider + e.partes.dps + e.partes.sinergia) falla([k, o, 'puntaje', vs.map(x => x.key)]);
        // el orden: a igual puntaje (y, en una tier list, igual puesto), más strikers primero
        if (previo && previo.ps === ps && previo.pts === pts && previo.stk < stk) falla([k, o, 'orden', previo.keys, vs.map(x => x.key)]);
        if (previo && previo.ps === ps && previo.pts === pts && previo.stk !== stk) out.con_desempate++;
        previo = { ps, pts, stk, keys: vs.map(x => x.key) };
      }
      // la primera página: cada tarjeta dice cuántos («desempate: N strikers»), y la ventana de su «Por qué» también, arriba
      // y en sus puntos, como desempate y sin puntos
      CONSULTA = q; ui.eqPagina = 0; const d = doc(combinacionesHtml(v));
      [...d.querySelectorAll('.combo')].forEach((c, n) => {
        const i = filas[n], vs = [v, q.pool[q.A[i]], q.pool[q.B[i]]], e = ctx ? enContexto(vs, ctx) : null;
        const stk = e ? e.strikers : cuantosStrikers(vs, v);
        const dice = pl(c.querySelector('.eqpts .desempate'));
        const esp = stk ? t(stk === 1 ? 'cx_desempate_1' : 'cx_desempate').replace('{n}', stk) : null;
        const id = c.querySelector('[data-a="pqAbrir"]').dataset.pq, m = doc(pqHtml({ id, tab: null }, pqDatos(id)));
        const arriba = pl(m.querySelector('.pqm-equipo .eqpts .desempate'));
        const st = [...m.querySelectorAll('.pqm-parteh')].filter(x => /striker/i.test(pl(x))).map(x => [pl(x.querySelector(':scope > b')), !!x.querySelector('.pqm-pts')]);
        const bien = stk ? st.length === 1 && st[0][0] === mayuscula(esp) && !st[0][1] : !st.length;
        if (dice !== esp || arriba !== esp || !bien) falla([k, o, 'tarjeta', vs.map(x => x.key), dice, esp, arriba, st]);
      });
    }
  }
  Object.assign(ui, antes); CONSULTA = null;
  return out;
}"""),
  dict(id='lider_del_trio', desc='el líder de un equipo es uno solo: el mismo en cualquier orden y desde la lista de cualquiera '
       '(sinergia, puntos para él, tus equipos, favoritos y comparativa sin contexto; PvP y PvE con el suyo), y se pinta primero, '
       'con su marca', js=r"""() => {
  const { pl, doc, vs: todas } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], en_contexto: 0, sin_lider: 0 };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  let semilla = 7;
  const azar = (n) => { semilla = (semilla * 1103515245 + 12345) % 2147483648; return semilla % n; };
  const perms = (a) => [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]].map(p => p.map(i => a[i]));
  const k = (x) => x ? x.key : null;
  // Pintado: el líder primero (a la izquierda), el único con la marca (clase lider y la pastilla) y el title que lo dice.
  const pintado = (html, lider) => { const fotos = [...doc(html).querySelectorAll('.eqfoto')];
    return !lider ? !fotos.some(f => f.classList.contains('lider'))
      : fotos[0].dataset.cid === lider.cid && (fotos[0].dataset.uid || null) === lider.uid && fotos[0].classList.contains('lider')
        && fotos.filter(f => f.classList.contains('lider')).length === 1 && pl(fotos[0].querySelector('.pillider')) === t('eq_lider_pill')
        && fotos[0].title === t('eq_lider_de').replace('{x}', fullLabel(lider)); };
  for (let n = 0; n < 1500; n++) {
    const tres = [];
    while (tres.length < 3) { const v = todas[azar(todas.length)]; if (!tres.some(x => x.cid === v.cid)) tres.push(v); }
    const l0 = liderDe(tres, null);
    out.casos++; if (!l0) out.sin_lider++;
    // Sin contexto: el mismo en cualquier orden, en la sinergia del equipo y en la de cada uno (puntos para él).
    if (perms(tres).some(p => liderDe(p, null) !== l0 || synergy(p).lider !== l0 || p.some(f => synergy(p, { foco: f }).lider !== l0)))
      falla(['sin contexto', tres.map(k), k(l0)]);
    if (!pintado(retratosEquipo(tres, tres[0].key, l0), l0)) falla(['pintado', tres.map(k), k(l0)]);
    // Tus equipos y favoritos: el mismo líder, dicho y pintado primero.
    // Tus equipos (1.0.25): el líder declarado (acá, el de la sinergia o, sin ninguno que sume, el primero), dicho y pintado primero.
    const ld = l0 || tres[0];
    const eq = doc(equipoCard({ id: 'x', name: 'x', members: tres.map(k), lider: k(ld), reason: '', modeId: '' }));
    const fav = doc(favoritoCard({ id: 'f', members: tres.map(k), ctx: null }));
    const dice = l0 ? t('eq_leader').replace('{x}', fullLabel(l0)) : t('tm_no_leader');
    if (!pl(eq).includes(t('eq_leader').replace('{x}', fullLabel(ld))) || !pl(fav).includes(dice) || !pintado(eq.innerHTML, ld) || !pintado(fav.innerHTML, l0))
      falla(['tus equipos o favoritos', tres.map(k), k(l0)]);
    // PvP y PvE: el del contexto, el mismo en cualquier orden; la sinergia de la tarjeta se cuenta con ese.
    for (const ctx of ['pvp', 'pve']) {
      const e0 = enContexto(tres, ctx);
      if (!e0) continue;
      out.en_contexto++;
      if (perms(tres).some(p => { const e = enContexto(p, ctx); return !e || e.lider !== e0.lider || liderDe(p, ctx) !== e0.lider
          || synergy(p, { foco: p[0], lider: e0.lider }).lider !== e0.lider; })) falla([ctx, tres.map(k), k(e0.lider)]);
    }
  }
  return out;
}"""),
  dict(id='ctp_recomendado', desc='el C.T.P. recomendado de cada variante sin contexto, en PvP y en PvE, igual en su ficha (Armado) y '
       'en las tarjetas de equipo (combinaciones, tus equipos, «cómo entraría» y favoritos: ctpsEquipo), por fuente (Ezequiel, 5 de '
       'octubre: la guía de armado y la Ideal CTP List, las dos): lo que dice cada una, el uniforme del que sale y, en la ficha, '
       'el enlace a su fuente; y que lo que se ve sea lo que dice cada fuente (la fila de la guía y la de la lista, leídas acá)', js=r"""() => {
  const { pl, doc, vs } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], armado: 0, ideal: 0, distintos: 0 };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  // Lo que recomienda, sin los rótulos de las columnas, sin la fuente y sin el uniforme (se comparan aparte); lo que una
  // fuente no da, «SIN» (la ficha lo dice con una frase, la tabla con «—»).
  const limpio = (els) => els.map(el => { const c = el.cloneNode(true);
    c.querySelectorAll('.ctpfuente, .varx').forEach(x => x.remove());
    c.querySelectorAll('.ctpsin').forEach(x => x.replaceWith('SIN'));
    c.querySelectorAll('.muted').forEach(x => { if (x.textContent.trim().endsWith(':')) x.remove(); });
    return c.textContent.replace(/\s+/g, ''); }).join('');
  const uni = (els) => els.map(el => [...el.querySelectorAll('.varx')].map(pl).join('|')).join('');
  const LI = MFF_GUIA.ctp_ranking.lista_ideal, L = MFF_SEED_TIERLISTS.find(l => l.id === LI.id), A = MFF_SEED_TIER_ASSIGNMENTS[LI.id];
  const fuenteArm = MFF_GUIA.fuentes['cyn-armado'].nombre, fuenteIdeal = MFF_GUIA.fuentes[LI.fuente[0]].nombre;
  for (const v of vs) {
    const ficha = [...doc(ctpRecFichaHtml(v)).querySelectorAll('ul.ctprec > li')];
    // La Ideal CTP List leída acá: las filas de esta variante o, si no está, de la primera otra del personaje que esté.
    const otras = [v.key].concat([v.ch.id + '::base'].concat(v.ch.uniforms.map(u => v.ch.id + '::' + u.id)).filter(k => k !== v.key));
    const kIdeal = otras.find(k => (A[k] || []).length);
    const ideal = kIdeal ? A[kIdeal].map(id => L.rows.find(r => r.id === id).label) : null;
    [null, 'pvp', 'pve'].forEach((ctx, n) => {
      const li = ficha[n], tr = doc(ctpsEquipo([v], ctx)).querySelector('tbody tr');
      for (const f of ['armado', 'ideal']) {
        const fr = li.querySelector('.ctp-' + f), td = [...tr.querySelectorAll('td[data-f="' + f + '"]')];
        out.casos++;
        const a = { dice: limpio([fr]), uni: uni([fr]) }, b = { dice: limpio(td), uni: uni(td) };
        if (JSON.stringify(a) !== JSON.stringify(b)) falla([v.key, ctx, f, a, b]);
        const link = pl(fr.querySelector('.ctpfuente a.fuente'));
        if (link !== (f === 'armado' ? fuenteArm : fuenteIdeal)) falla([v.key, ctx, f, 'fuente', link]);
        if (a.dice !== 'SIN') out[f]++;
      }
      // La Ideal CTP List: lo que dice la ficha es lo de la lista.
      const fi = li.querySelector('.ctp-ideal');
      if (!ideal !== !!fi.querySelector('.ctpsin')) falla([v.key, ctx, 'ideal', kIdeal, ideal]);
      if (ideal && (fi.querySelectorAll(':scope > span:not(.muted):not(.ctpfuente):not(.varx), :scope > .sinint').length !== ideal.length))
        falla([v.key, ctx, 'ideal filas', ideal]);
      if (!li.querySelector('.ctp-armado .ctpsin') && ideal) out.distintos++;
    });
  }
  return out;
}"""),
  dict(id='le_sirve', desc='a quién le sirve cada stat de liderazgo, soporte o bono: la regla del catálogo (MFF_CATALOGO.soporte), '
       'la misma en la app (sirve(), lo que usan el Resumen, el filtro, las casillas, el «Por qué», la sinergia y PvP/PvE; '
       'contra un evaluador aparte sobre MFF_PERFIL) y en el «Le sirve:» del Glosario y del «Cómo funciona»', js=r"""() => {
  const { pl, doc, vs } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], stats: 0, efectos: 0, como: 0 };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  const SO = MFF_CATALOGO.soporte, SIRVE = MFF_CATALOGO.sirve;
  // Evaluador aparte: el perfil crudo de data.js.
  const pf = (b) => { const m = MFF_PERFIL[b.p] || { esc: [], tip: [], ele: [], res: [] };
    return { escala: m.esc.map(e => e[0]), elemento: m.ele, tipo: m.tip, resistencia: m.res }; };
  const evalua = (r, b) => { if (r === 'todos') return true; if (r === 'nadie') return false;
    const i = r.indexOf(':'), de = pf(b)[r.slice(0, i)], val = r.slice(i + 1);
    if (!de) throw new Error('regla desconocida ' + r);
    return val === '*' ? de.length > 0 : de.includes(val); };
  // 1. La app, para cada stat del catálogo y cada variante.
  for (const [st, x] of Object.entries(SO)) {
    out.stats++;
    for (const b of vs) { out.casos++; if (sirve({ s: st }, b) !== evalua(x.sirve, b)) falla(['app', st, x.sirve, b.key, sirve({ s: st }, b)]); }
  }
  // 2. El «Le sirve:» de cada efecto: lo que dice el catálogo (la regla del efecto y, si un stat que apunta a él tiene
  //    otra, la de ese stat), igual en el Glosario y en el «Cómo funciona» de una skill que lo trae.
  const regla = (r) => minuscula(SIRVE[r][LANG] || SIRVE[r].es);
  // Los renglones «Le sirve…» de un pedazo de HTML: el texto, o [rótulo, [cada stat de la lista]].
  const lineas = (nodos) => nodos.map(n => { const ul = n.querySelector('ul.sirvestat');
      if (!ul) return pl(n);
      const c = n.cloneNode(true); c.querySelector('ul.sirvestat').remove();
      return [pl(c), [...ul.querySelectorAll(':scope > li')].map(pl)]; })
    .filter(x => ['gl_le_sirve', 'gl_le_sirve_skills', 'gl_le_sirve_ls'].some(k => (Array.isArray(x) ? x[0] : x).startsWith(t(k))));
  MFF_CATALOGO.efectos.forEach((e, ie) => {
    const stats = Object.entries(SO).filter(([, x]) => x.efectos.includes(e.id));
    const otros = stats.filter(([, x]) => x.sirve !== e.sirve);
    const esperado = otros.length
      ? [t('gl_le_sirve_skills') + ' ' + regla(e.sirve), [t('gl_le_sirve_ls'), otros.map(([st, x]) => trTxt(st) + ': ' + regla(x.sirve))]]
      : [t('gl_le_sirve') + ' ' + regla(e.sirve)];
    out.efectos++; out.casos++;
    const glosario = lineas([...doc(efectoGl(e)).querySelectorAll('.annota')]);
    if (JSON.stringify(glosario) !== JSON.stringify(esperado)) falla(['glosario', e.id, glosario, esperado]);
    // Una variante que lo trae en sus skills: su «Cómo funciona».
    for (const v of vs) {
      const an = MFF_ANALISIS[v.p]; if (!an) continue;
      const fx = an.fx.find(y => y[0] === ie); if (!fx) continue;
      out.como++; out.casos++;
      const como = lineas([...doc(efectoTipHtml(v, { ie, d: fx[1], objetivo: fx[2], fuentes: fx[3], ns: false })).querySelectorAll('ul.tiplista > li')]);
      if (JSON.stringify(como) !== JSON.stringify(esperado)) falla(['como', e.id, v.key, como, esperado]);
      break;
    }
  });
  return out;
}"""),
  dict(id='aplica_a_si_mismo_y_anti_mermas', desc='qué es anti-mermas (los stats de la tabla de valor, en la casilla, el '
       'índice y el filtro de PvP) y si lo propio cuenta para su dueño: sus soportes y sus anti-mermas propios sin probabilidad '
       'le llegan (la casilla, el «Por qué» y el filtro de PvP dicen lo mismo); los que tienen probabilidad no cuentan y se '
       'dicen (el «Por qué» y el detalle de PvP)', js=r"""() => {
  const { pl, doc, vs } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], con_propio: 0, con_prob: 0, soporte_propio: 0, detalle: 0, sin_trio: 0 };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  // 1. Anti-mermas es lo mismo en todas partes: la tabla de valor, el filtro de PvP (ANTI_MERMAS) y la casilla y el
  //    índice (la categoría mermas).
  out.casos++;
  if (JSON.stringify([...ANTI_MERMAS]) !== JSON.stringify(MFF_VALOR.anti_mermas) || JSON.stringify(CAT.mermas.s) !== JSON.stringify(MFF_VALOR.anti_mermas))
    falla(['qué es anti-mermas', [...ANTI_MERMAS], CAT.mermas.s, MFF_VALOR.anti_mermas]);
  const anti = new Set(MFF_VALOR.anti_mermas);
  const rotulos = MFF_VALOR.anti_mermas.map(trTxt);
  for (const v of vs) {
    const so = SOPORTES[v.p] || {}, ap = antiPropio(v);
    // Lo que se da a sí mismo: sus soportes que le llegan y le sirven, y sus anti-mermas propios que cuentan.
    const propios = SLOTS_SOPORTE.filter(k => so[k] && aplicaA(so[k], v) && so[k].fx.some(f => sirve(f, v)));
    const antiSop = SLOTS_SOPORTE.some(k => so[k] && aplicaA(so[k], v) && so[k].fx.some(f => anti.has(f.s)));
    if (propios.length) out.soporte_propio++;
    if (ap.cuenta.length) out.con_propio++;
    if (ap.prob.length) out.con_prob++;
    const tiene = antiSop || ap.cuenta.length > 0;
    // La casilla (cobertura de un equipo de él solo), el filtro de PvP (cubiertos) y lo que le llega (recibe).
    const casilla = 'mermas' in cobertura(v, [v], null), filtro = cubiertos([v], [slotsDe(v)])[0];
    const llega = recibe(v, v, false), llegaAnti = llega.some(r => r.fx.some(f => anti.has(f.s)));
    const llegaSop = propios.every(k => llega.some(r => r.k === k));
    // El «Por qué» de un equipo de él solo (su pestaña en la ventana): la tabla de lo que recibe dice anti-mermas si le
    // llegan, y los propios con probabilidad, aparte.
    const d = doc(integranteHtml(v, [v], null, 0, true));
    const suma = [...d.querySelectorAll('.pqm-tabla > .pqm-fila:not(.pqm-th) > .pqm-ef')].map(pl), probs = [...d.querySelectorAll('.pqprob')].map(pl);
    const porque = suma.some(l => rotulos.some(r => l.startsWith(r)));
    out.casos += 6;
    const r = { tiene, casilla, filtro, llegaAnti, porque, llegaSop, probs: probs.length, prob: ap.prob.length };
    if (casilla !== tiene || filtro !== tiene || llegaAnti !== tiene || porque !== tiene || !llegaSop || probs.length !== ap.prob.length)
      falla([fullLabel(v), r]);
  }
  // 2. El detalle de PvP de un trío con alguien que tiene un anti-mermas propio con probabilidad lo dice, y no cuenta; uno con
  //    un anti-mermas propio que cuenta dice de dónde sale.
  const conProb = vs.filter(v => antiPropio(v).prob.length), conPropio = vs.filter(v => antiPropio(v).cuenta.length);
  const dar = vs.filter(v => rolEn(v, 'pvp').dps > 0);
  for (const [grupo, prob] of [[conProb, true], [conPropio, false]]) for (const v of grupo) {
    // Un trío que entre: él y dos DPS de PvP cualquiera, el primero que entre.
    let hecho = false;
    for (let i = 0; i < dar.length && !hecho; i++) for (let j = i + 1; j < dar.length && !hecho; j++) {
      const tr = [v, dar[i], dar[j]];
      if (new Set(tr.map(x => x.cid)).size < 3) continue;
      const e = enContexto(tr, 'pvp', true); if (!e) continue;
      hecho = true; out.casos++; out.detalle++;
      const parte = [...doc(detalleContexto(e, tr, 'pvp')).querySelectorAll('.pqm-parte')].find(x => pl(x.querySelector('.pqm-parteh > b')) === t('cx_anti'));
      const lineas = parte ? [...parte.querySelectorAll(':scope > ul.pqm-lista > li')].map(pl) : [];
      const nombre = nombreEn(tr);
      // Con probabilidad: un renglón por cada uno, que dice que no cuenta. Si no: de dónde sale el suyo (un soporte de
      // alguno, si lo hay; si no, el propio).
      const de = tr.find(x => slotsDe(x).antiSop.some(y => aplicaA(y, v)));
      const rotulo = prob ? null : de ? t('cx_de_sop').replace('{x}', nombre(de))
        : t('cx_de_propio').replace('{x}', nombre(v)).replace('{s}', slotEs(antiPropio(v).cuenta[0].sk.sl));
      const dice = prob ? lineas.filter(l => l.startsWith(nombre(v) + ': ') && l.endsWith(t('cx_prob').split('{a}): ')[1])).length === antiPropio(v).prob.length
                        : lineas.some(l => l.startsWith(rotulo + ' → '));
      if (!dice) falla(['detalle', fullLabel(v), prob, rotulo, lineas]);
    }
    if (!hecho) out.sin_trio++;
  }
  return out;
}"""),
  dict(id='liderazgos_sin_leads_supports', desc='la fuente de cada liderazgo: los que el build completa con la Leader Skill de '
       'la API (src «api») dicen «según la skill del juego» en todas las pantallas que muestran un liderazgo (Resumen y su cita, '
       '«Cómo funciona», detalle de PvP, el «Por qué» (lo que recibe uno y lo que aporta el líder), comparativa e índice del roster), y los de Leads & Supports no: '
       'marcando uno de Leads & Supports en memoria, en las nueve pantallas; y con los datos (los del build, o los de '
       'armar_datos_lideres.py), en el Resumen y el «Cómo funciona» de la Leader Skill de cada variante con liderazgo', js=r"""() => {
  const { pl, doc, vs } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], hoy_api: 0 };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  for (const so of Object.values(SOPORTES)) for (const [k] of TIPOS_SOPORTE) if (so[k] && esDeApi(so[k])) out.hoy_api++;
  const etq = t('sp_src_api'), porKey = new Map(vs.map(x => [x.key, x]));
  // El trío del «Por qué» 3 (verif_porque): Adam Warlock — GotG3 + Wasp — Quantumania (líder) + Doctor Voodoo — Savage Avengers.
  const adam = porKey.get('adam-warlock::adam-warlock-10200152'), wasp = porKey.get('wasp::wasp-10300051'), dv = porKey.get('doctor-voodoo::doctor-voodoo-10200204');
  const tr = [adam, wasp, dv], x = SOPORTES[wasp.p].leader;
  const pantallas = () => {
    const r = {};
    const res = doc(usoSoportes(wasp));
    const lid = [...res.querySelectorAll('.sop')].find(b => b.querySelector('.slotbadge.lead'));
    r.resumen = !!lid.querySelector('.srcapi');
    r.cita = pl(res.querySelector('.fuentes')).includes(MFF_GUIA.fuentes['tv-pj'].nombre);
    const si = wasp.skills.findIndex(sk => sk.sl === 'Leader Skill'), sk = wasp.skills[si];
    const como = doc(tipCuandoHtml(wasp, sk, entradasSkill(wasp, si), null, null));
    r.como = pl(como.querySelector('details.tipls > summary')) !== t('tt_ls') && !!como.querySelector('details.tipls .srcapi');
    const e = enContexto(tr, 'pvp', true);
    r.lider_pvp = e && e.lider === wasp;
    const det = [...doc(detalleContexto(e, tr, 'pvp')).querySelectorAll('.pqm-parte')].find(p => pl(p.querySelector('.pqm-parteh > b')) === t('cx_lider').replace('{x}', nombreEn(tr)(wasp)));
    r.detalle = !!det && [...det.querySelectorAll(':scope > ul.pqm-lista > li')].some(li => pl(li).includes('(' + etq + ')'));
    // La ventana del «Por qué» de la tarjeta de Adam en PvP: lo que recibe él (la tabla, en su pestaña) y lo que aporta
    // Wasp (en la suya).
    const pq = doc(pqHtml({ id: 'x', tab: null }, pqDatos('c|pvp|' + tr.map(x => x.key).join(','))));
    const panel = (m) => pq.querySelector('#' + pq.querySelector(`[role="tab"][data-key="${m.key}"]`).getAttribute('aria-controls'));
    r.porque = !!panel(adam).querySelector(':scope > .pqm-tabla .pqm-de .srcapi');
    r.aporta = !!panel(wasp).querySelector(':scope > ul.pqm-lista .srcapi');
    r.comparativa = razonesTxt(synergy(tr, { lider: wasp }).razones).some(l => l.includes(fullLabel(wasp)) && l.includes('(' + etq + ')'));
    const F = U.prefs.filters, antes = F.lid.slice();
    F.lid.splice(0, F.lid.length, 'atk');
    r.indice = !!doc(indiceLinea(wasp)).querySelector('.srcapi');
    F.lid.splice(0, F.lid.length, ...antes);
    return r;
  };
  // Con los datos de hoy (Leads & Supports): ninguna lo dice.
  const hoy = pantallas();
  // Marcado como de la API, en memoria: todas lo dicen.
  x.src = 'api'; _SLOTS.clear();
  let api;
  try { api = pantallas(); } finally { delete x.src; _SLOTS.clear(); }
  for (const [k, v] of Object.entries(api)) {
    out.casos += 2;
    if (k === 'lider_pvp') { if (!v || !hoy[k]) falla([k, hoy[k], v]); continue; }
    if (!v || hoy[k]) falla([k, 'hoy', hoy[k], 'api', v]);
  }
  out.pantallas = Object.keys(api).length;
  // Con los datos: en el Resumen y en el «Cómo funciona» de la Leader Skill de cada variante con liderazgo, cada uno de
  // la API dice «según la skill del juego» y los de Leads & Supports no (carril Q: los deriva el build).
  out.variantes = 0;
  for (const v of vs) {
    const so = SOPORTES[v.p], ks = so ? LIDERAZGOS.filter(k => so[k]) : [];
    if (!ks.length) continue;
    const bloques = [...doc(usoSoportes(v)).querySelectorAll('.sop')].filter(b => b.querySelector('.slotbadge.lead'));
    const dice = bloques.map(b => !!b.querySelector('.srcapi')), debe = ks.map(k => esDeApi(so[k]));
    const si = v.skills.findIndex(sk => sk.sl === 'Leader Skill');
    const rot = si < 0 ? null : pl(doc(tipCuandoHtml(v, v.skills[si], entradasSkill(v, si), null, null)).querySelector('details.tipls > summary'));
    const rotDebe = t(debe.every(x => x) ? 'tt_ls_api' : debe.some(x => x) ? 'tt_ls_mixto' : 'tt_ls');
    out.casos++; out.variantes++;
    if (debe.some(x => x)) out.de_la_api = (out.de_la_api || 0) + 1;
    if (JSON.stringify(dice) !== JSON.stringify(debe) || rot !== rotDebe) falla([fullLabel(v), dice, debe, rot]);
  }
  return out;
}"""),
  dict(id='ultimo_uniforme', desc='«Solo el último uniforme» (Ezequiel, 5 de octubre de 2026): el mismo en todas las pantallas donde '
       'se arma (las combinaciones de 3 en los cuatro órdenes: puntos para él, PvP, PvE y una tier list) y el de la regla, con un '
       'evaluador aparte sobre MFF_SEED_CHARACTERS: cada compañero con su último uniforme, cada pareja que ya iba con los últimos con la '
       'misma fila, la cuenta de las que había y, en la pantalla, la casilla marcada, la nota y la primera página', js=r"""() => {
  const { doc, vs: todas } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], listas: 0, filas: 0, entran: 0 };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  // Evaluador aparte: la versión del juego de up.update (números y letra) y, a igual versión, el número del id; sin uniformes,
  // la base. Desde los datos de formato 9 todos traen versión: uno sin versión es una falla.
  const ver = (u) => { const s = u.up && u.up.update; if (s == null) { falla(['sin versión', u.id]); return null; } const m = /^(\d+(?:\.\d+)*)([a-z]?)$/.exec(s);
    const n = m[1].split('.').map(Number); while (n.length < 6) n.push(0); return n.concat([m[2] ? m[2].charCodeAt(0) : 0]); };
  const cmp = (a, b) => { for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] - b[i]; return 0; };
  const ULT = new Set();
  for (const ch of MFF_SEED_CHARACTERS) {
    if (!ch.uniforms.length) { ULT.add(ch.id + '::base'); continue; }
    let mejor = null;
    for (const u of ch.uniforms) { const v = ver(u); if (!v) { ULT.add(ch.id + '::' + u.id); continue; }
      const k = v.concat([Number(u.id.split('-').pop())]); if (!mejor || cmp(k, mejor[0]) > 0) mejor = [k, u]; }
    if (mejor) ULT.add(ch.id + '::' + mejor[1].id);
  }
  out.entran = ULT.size;
  for (const v of todas) { out.casos++; if (esUltimo(v) !== ULT.has(v.key)) falla(['regla', v.key, esUltimo(v)]); }
  const antes = { eqOrden: ui.eqOrden, eqUltimo: ui.eqUltimo, eqPagina: ui.eqPagina }, par = (a, b) => a.cid < b.cid ? a.cid + '|' + b.cid : b.cid + '|' + a.cid;
  for (const k of ['deadpool::deadpool-10800164', 'knull::knull-10100241', 'adam-warlock::adam-warlock-10200152', 'wasp::wasp-10300051']) {
    const v = todas.find(x => x.key === k); CONSULTA = null; const q = consultaCon(v);
    for (const o of ['foco', 'pvp', 'pve', 'lista:tv-soportes']) {
      if ((o === 'pvp' || o === 'pve') && !tieneFuncion(v, o)) continue;
      Object.assign(ui, { eqOrden: o, eqExcluir: [], eqCon: '', eqCobertura: [], eqVerDescartados: false, eqUltimo: false, eqPagina: 0 }); q.vista = null;
      const sin = vistaConsulta(q).filas.slice();
      ui.eqUltimo = true; q.vista = null;
      const con = vistaConsulta(q), conPar = new Map(con.filas.map(i => [par(q.pool[q.A[i]], q.pool[q.B[i]]), i]));
      out.listas++; out.filas += con.filas.length;
      for (const i of con.filas) { out.casos++; if (!ULT.has(q.pool[q.A[i]].key) || !ULT.has(q.pool[q.B[i]].key)) falla(['compañero', k, o, q.pool[q.A[i]].key, q.pool[q.B[i]].key]); }
      for (const i of sin) { const a = q.pool[q.A[i]], b = q.pool[q.B[i]]; if (!ULT.has(a.key) || !ULT.has(b.key)) continue;
        out.casos++; if (conPar.get(par(a, b)) !== i) falla(['fila', k, o, a.key, b.key]); }
      out.casos++; if (con.sinUltimo !== sin.length) falla(['cuenta', k, o, con.sinUltimo, sin.length]);
      const d = doc(combinacionesHtml(v)), c = d.querySelector('input[data-a="eqUltimo"]');
      const fotos = [...d.querySelectorAll('.combo')].map(x => [...x.querySelectorAll('.eqfoto')].map(f => f.dataset.cid + '::' + (f.dataset.uid || 'base')).filter(kk => kk !== k));
      out.casos++;
      if (!c || !c.hasAttribute('checked') || !d.querySelector('.ultnota') || !fotos.length || fotos.some(fs => fs.some(kk => !ULT.has(kk)))) falla(['pantalla', k, o, !!c, fotos.length]);
    }
  }
  Object.assign(ui, antes, { eqExcluir: [], eqCon: '', eqCobertura: [] }); CONSULTA = null;
  return out;
}"""),
  dict(id='habilidad_una_vez', desc='una habilidad (lo que no se acumula, según el catálogo: anti-mermas, inmunidades, barrera, '
       'escudos...) que a un integrante le llega de dos fuentes cuenta una vez, la de mayor valor (Ezequiel, 5 de octubre de 2026), en todas '
       'las pantallas: con un evaluador aparte (el catálogo leído acá; la de mayor valor y, a igual valor, el orden: lo propio, el liderazgo '
       'del líder y los soportes, el líder primero y los demás por clave), lo que no se suma es lo mismo en «Lo que recibe» y «Lo que '
       'aporta» de la ventana, en los puntos (la sinergia y el detalle de PvP y PvE) y en la comparativa; quién cubre a cada uno en la '
       'línea de anti-mermas; un soporte que no se le aplica a nadie no suma (tríos al azar con dos o tres que traen una habilidad; con '
       'habilidades con valor de prueba en unas variantes, porque en los datos de hoy ninguna con valor le llega a nadie de dos fuentes)', js=r"""() => {
  const { doc, vs: todas } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], trios: 0, en_pvp: 0, en_pve: 0, con_repetidos: 0, de_prueba: 0, pantallas: {} };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  const NOLID = ['passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact'], LID = ['leader', 'leader2'];
  const so = (a) => SOPORTES[a.p] || {};
  // la regla, del catálogo leído acá aparte (un stat que no tiene se suma)
  const noAcum = (f) => { const c = window.MFF_CATALOGO.soporte[f.s]; return !!c && !c.acumula; };
  const valor = (F, s) => { let v = null; for (const f of F.fx) if (f.s === s && typeof f.v === 'number' && (v === null || f.v > v)) v = f.v; return v; };
  let semilla = 23; const azar = (n) => { semilla = (semilla * 1103515245 + 12345) % 2147483648; return semilla % n; };
  // Habilidades con valor de prueba: en unas variantes, en un slot vacío, una inmunidad con probabilidad o revivir con un valor
  // al azar (stats que ningún liderazgo trae, así que el vínculo por el liderazgo no cambia). Se sacan al terminar.
  const PRUEBA = ['Lightning Immunity Chance', 'Fire Immunity Chance', 'Revive with % HP'], VALORES = [30, 50, 80], puestas = [];
  for (const v of todas.filter((x, n) => n % 9 === 4)) { const s = so(v), k = ['passive2', 't22', 'uniform2'].find(k => !s[k]);
    if (!SOPORTES[v.p] || !k || puestas.some(([p]) => p === v.p)) continue;
    s[k] = { fx: [{ s: PRUEBA[azar(PRUEBA.length)], v: VALORES[azar(VALORES.length)] }] }; puestas.push([v.p, k]); }
  _NO_ACUM_DE.clear(); _SLOTS.clear();
  out.de_prueba = puestas.length;
  try {
  // Evaluador aparte: las fuentes de lo que le llega a m, en el orden en que se aplican.
  const fuentes = (m, eq, lider) => {
    const fs = antiPropio(m).cuenta.map(ap => ({ de: m, k: 'propio', fx: [{ s: ap.s }] }));
    for (const k of NOLID) { const x = so(m)[k]; if (x && aplicaA(x, m)) fs.push({ de: m, k, x, fx: x.fx }); }
    if (lider) for (const k of LID) { const x = so(lider)[k]; if (x && aplicaA(x, m)) fs.push({ de: lider, k, x, fx: x.fx }); }
    const otros = eq.filter(a => a !== lider).sort((a, b) => a.key < b.key ? -1 : 1);
    for (const a of (lider ? [lider] : []).concat(otros)) if (a !== m) for (const k of NOLID) { const x = so(a)[k]; if (x && aplicaA(x, m)) fs.push({ de: a, k, x, fx: x.fx }); }
    return fs;
  };
  // no: 'receptor|quien da|slot' con algún efecto que le sirve y no se le aplica; aplica: los que tienen alguno que sí; cubre: de
  // cada uno, la primera fuente de anti-mermas ('quien da|propio, lid o sop').
  const evalua = (eq, lider) => {
    const no = new Set(), aplica = new Set(), cubre = new Map();
    for (const m of eq) {
      const fs = fuentes(m, eq, lider), primera = new Map();
      // de cada habilidad, la que se le aplica: la de mayor valor; a igual valor (o sin valor), la primera
      for (const F of fs) for (const f of F.fx) if (noAcum(f)) { const p = primera.get(f.s), v = valor(F, f.s);
        if (!p || (v !== null && p.v !== null && v > p.v)) primera.set(f.s, { F, v }); }
      const anti = fs.find(F => F.fx.some(f => ANTI_MERMAS.has(f.s)));
      if (anti) cubre.set(m.key, anti.de.key + '|' + (anti.k === 'propio' ? 'propio' : LID.includes(anti.k) ? 'lid' : 'sop'));
      for (const F of fs) {
        const sirven = F.fx.filter(f => sirve(f, m)); if (!sirven.length) continue;
        const si = sirven.filter(f => !noAcum(f) || primera.get(f.s).F === F);
        if (si.length < sirven.length) no.add(m.key + '|' + F.de.key + '|' + F.k);
        if (si.length) aplica.add(m.key + '|' + F.de.key + '|' + F.k);
      }
    }
    return { no, aplica, cubre };
  };
  // Lo que dice una pantalla: los receptores de un «(X ya lo tiene …)» (los nombres seguidos de « ya lo tiene »).
  const tras = t('rep_quien').split('{y}')[1].split('{de}')[0];
  const quienes = (el) => [...el.querySelectorAll('.pqrep span[title]')].filter(sp => sp.nextSibling && sp.nextSibling.nodeType === 3 && sp.nextSibling.textContent.startsWith(tras)).map(sp => sp.title);
  const igual = (a, b) => JSON.stringify([...a].sort()) === JSON.stringify([...b].sort());
  const cand = todas.filter(v => antiPropio(v).cuenta.length || NOLID.concat(LID).some(k => so(v)[k] && so(v)[k].fx.some(noAcum)));
  for (let n = 0; out.trios < 500 && n < 20000; n++) {
    const eq = [cand[azar(cand.length)], cand[azar(cand.length)], n % 3 ? cand[azar(cand.length)] : todas[azar(todas.length)]];
    if (new Set(eq.map(x => x.cid)).size < 3) continue;
    out.trios++;
    const clave = new Map(eq.map(x => [fullLabel(x), x.key]));
    for (const ctx of [null, 'pvp', 'pve']) {
      const e = ctx ? enContexto(eq, ctx, true) : null;
      if (ctx && !e) continue;
      if (ctx) out['en_' + ctx]++;
      const lider = e ? e.lider : liderDe(eq, null), M = evalua(eq, lider), c = ctx || 'sc';
      if (M.no.size) out.con_repetidos++;
      // «Lo que recibe» (cada parte atenuada: quién la da) y «Lo que aporta» (a quiénes no se les suma) de cada integrante.
      const recibe = new Set(), aporta = new Set();
      eq.forEach(m => { const d = doc(integranteHtml(m, eq, lider, 0, true));
        for (const x of d.querySelectorAll('.pqm-de1.rep')) recibe.add(m.key + '|' + clave.get(x.querySelector('span[title]').title));
        for (const li of d.querySelectorAll(':scope > .pqm-panel > ul.pqm-lista > li')) for (const q of quienes(li)) aporta.add(clave.get(q) + '|' + m.key); });
      // Lo que tiene que decir cada pantalla: 'receptor|quien da', de todo lo que no se suma (recibe), de lo que da otro (aporta,
      // los puntos de la sinergia y la comparativa) o solo de los soportes de otro (el detalle de PvP y PvE: su liderazgo va por stat
      // de la tabla de valor, y la tabla de hoy no pesa nada sin valor).
      const proj = (f) => new Set([...M.no].filter(p => f(...p.split('|'))).map(p => p.split('|').slice(0, 2).join('|')));
      const todo = proj(() => true), deOtros = proj((r, d) => r !== d), sopDeOtros = proj((r, d, k) => r !== d && NOLID.includes(k));
      out.casos += 2;
      if (!igual(recibe, todo)) falla([c, 'recibe', eq.map(x => x.key), [...recibe], [...M.no]]);
      if (!igual(aporta, deOtros)) falla([c, 'aporta', eq.map(x => x.key), [...aporta], [...M.no]]);
      // Los puntos: la sinergia (sin contexto) o el detalle (PvP y PvE), con quién da cada línea.
      const puntos = new Set(), cub = new Map();
      if (!ctx) {
        const sc = synergy(eq, { lider }), d = doc(partesSinergia(sc, eq, []));
        const rotLid = lider ? t('cx_lider').replace('{x}', nombreEn(eq)(lider)) : null;
        for (const p of d.querySelectorAll('.pqm-parte')) { const lid = p.querySelector('.pqm-parteh > b').textContent === rotLid;
          for (const li of p.querySelectorAll(':scope > ul.pqm-lista > li')) { const da = lid ? lider.key : clave.get((li.querySelector('span[title]') || {}).title);
            for (const q of quienes(li)) puntos.add(clave.get(q) + '|' + da); } }
        // un soporte que no se le aplica a nadie más va con 0 (y el puntaje, sin él)
        for (const r of sc.razones) if (r.tipo === 'soporte' || r.tipo === 'liderazgo') {
          const algo = eq.some(b => b !== r.de && M.aplica.has(b.key + '|' + r.de.key + '|' + r.k));
          out.casos++; if (!!r.pts !== algo) falla([c, 'suma', eq.map(x => x.key), r.de.key, r.k, r.pts]); }
        // la comparativa: cada línea con «(no se suma:», quién da y a quiénes
        const ns = t('rep_no_suma').split('{de}')[0];
        for (const l of razonesTxt(sc.razones)) { if (!l.includes('(' + ns)) continue;
          const pre = l.slice(0, l.indexOf(' → ')), tras2 = l.slice(l.indexOf(' → ') + 3);
          const da = eq.find(x => pre.includes(fullLabel(x)) && !eq.some(y => y !== x && fullLabel(y).length > fullLabel(x).length && pre.includes(fullLabel(y))));
          for (const b of eq) { const f = fullLabel(b); if (b !== da && (tras2.startsWith(f + ': ') || tras2.startsWith(f + ', ') || tras2.includes(', ' + f + ': ') || tras2.includes(', ' + f + ', ')))
            out.pantallas.comparativa = (out.pantallas.comparativa || 0) + 1, puntos.add('cmp|' + b.key + '|' + da.key); } }
        const cmp = new Set([...puntos].filter(p => p.startsWith('cmp|')).map(p => p.slice(4)));
        for (const p of [...puntos]) if (p.startsWith('cmp|')) puntos.delete(p);
        out.casos++; if (!igual(cmp, deOtros)) falla([c, 'comparativa', eq.map(x => x.key), [...cmp], [...M.no]]);
      } else {
        const d = doc(detalleContexto(e, eq, ctx));
        for (const p of d.querySelectorAll('.pqm-parte')) {
          const rot = p.querySelector('.pqm-parteh > b').textContent;
          for (const li of p.querySelectorAll(':scope > ul.pqm-lista > li')) {
            if (rot === t('cx_sinergia')) { const da = clave.get((li.querySelector('span[title]') || {}).title); for (const q of quienes(li)) puntos.add(clave.get(q) + '|' + da); }
            if (rot === t('cx_anti') && li.textContent.includes(' → ')) {
              const sp = [...li.querySelectorAll('span[title]')], txt = li.textContent, tipo = txt.includes(t('cx_de_lid').split('{x}')[1]) ? 'lid' : txt.includes(t('cx_de_sop').split('{x}')[1]) ? 'sop' : 'propio';
              const ms = txt.endsWith('→ ' + t('pq_todos')) ? eq.map(x => x.key) : sp.slice(1).map(x => clave.get(x.title));
              for (const m of ms) cub.set(m, clave.get(sp[0].title) + '|' + tipo);
            }
          }
        }
        // los soportes que suman, como el evaluador; y la parte de soportes y bonos con su peso
        const n = e.sops.filter(x => eq.some(b => b !== x.de && M.aplica.has(b.key + '|' + x.de.key + '|' + x.k))).length;
        out.casos++; if (e.partes.sinergia !== n * CONTEXTO[ctx].soporte + e.bonos.length * CONTEXTO[ctx].bono || e.sops.some(x => !!x.pts !== (x.a.length > 0)))
          falla([c, 'suma', eq.map(x => x.key), e.partes.sinergia, n]);
        if (CONTEXTO[ctx].requisito === 'anti_mermas') { out.casos++;
          const esp = new Map(eq.map(m => [m.key, M.cubre.get(m.key)]));
          if (JSON.stringify([...cub].sort()) !== JSON.stringify([...esp].sort())) falla([c, 'anti', eq.map(x => x.key), [...cub], [...esp]]); }
      }
      out.casos++; if (!igual(puntos, ctx ? sopDeOtros : deOtros)) falla([c, 'puntos', eq.map(x => x.key), [...puntos], [...M.no]]);
    }
  }
  } finally {
    for (const [p, k] of puestas) delete SOPORTES[p][k];
    _NO_ACUM_DE.clear(); _SLOTS.clear();
  }
  return out;
}"""),
  dict(id='acumulacion_y_topes', desc='qué se acumula y los topes (Ezequiel, 5 de octubre de 2026; datos de formato 8): cada stat de los '
       'liderazgos, soportes y bonos dice en el catálogo si se acumula, y la app (seAcumula) dice lo mismo; el Glosario y «Cómo funciona» '
       'dicen de cada efecto lo que dice el catálogo (si se suma o cuenta una vez, con la nota de los dudosos, y el tope de la guía con su '
       'fuente); en lo que recibe cada integrante (la ventana del «Por qué»), cada stat con tope lo muestra con los números de la guía '
       '(MFF_GUIA.topes, leído acá aparte) y su fuente, ninguno sin tope lo muestra, y el aviso sale cuando lo que suman los buffs pasa lo '
       'que queda hasta el tope (300 tríos al azar con los datos, donde ninguno lo pasa, y 40 con crítico de prueba)', js=r"""() => {
  const { pl, doc, vs: todas } = window.__c, out = { casos: 0, mal: 0, ejemplos: [], stats: 0, efectos: 0, renglones: 0, con_tope: 0, avisos: 0, avisos_prueba: 0 };
  const falla = (x) => { out.mal++; if (out.ejemplos.length < 4) out.ejemplos.push(x); };
  const CAT = window.MFF_CATALOGO.soporte, G = window.MFF_GUIA, idioma = (x) => LANG === 'es' ? x.es : x.en;
  // 1. cada stat de los datos, en el catálogo, y la app como el catálogo
  const stats = new Set();
  for (const so of Object.values(SOPORTES)) for (const x of Object.values(so)) if (x && x.fx) for (const f of x.fx) stats.add(f.s);
  for (const b of BONOS) for (const v of b.v) for (const [st] of v) stats.add(st);
  for (const st of stats) { out.stats++; out.casos++;
    if (!CAT[st] || typeof CAT[st].acumula !== 'boolean' || seAcumula({ s: st }) !== CAT[st].acumula) falla(['acumula', st]); }
  // los topes de la guía, leídos acá: clave -> [tope, base]
  const TOPE = {}; for (const it of G.topes.items) if (it.tope != null) for (const k of it.stats) TOPE[k] = [it.tope, it.base || 0];
  const fuente = G.fuentes[G.topes.fuente[0]].nombre;
  const topeTxtEsp = (st) => { const ks = CAT[st].tope || [];
    return ks.map(k => (ks.length > 1 ? idioma(G.stats[k]) + ' ' : '') + (TOPE[k][1] ? t('pq_tope_base').replace('{n}', numTxt(TOPE[k][0])).replace('{b}', numTxt(TOPE[k][1]))
      : numTxt(TOPE[k][0]) + '%')).join(', '); };
  // 2. el Glosario y «Cómo funciona»: de cada efecto con stats, lo que dice el catálogo
  const esperado = (e) => { const sts = Object.keys(CAT).filter(st => CAT[st].efectos.includes(e.id));
    if (!sts.length) return null;
    const dice = (st) => t(CAT[st].acumula ? 'gl_se_suma' : 'gl_una_vez'), nota = (st) => CAT[st].nota ? ' — ' + idioma(CAT[st].nota) : '';
    const acum = sts.every(st => CAT[st].acumula === CAT[sts[0]].acumula && !CAT[st].nota) ? t('gl_acumula') + ' ' + dice(sts[0])
      : t('gl_acumula') + ' ' + sts.map(st => trTxt(st) + ': ' + dice(st) + nota(st)).join('');
    const con = sts.filter(st => (CAT[st].tope || []).length);
    const tope = !con.length ? null : con.length === sts.length && con.every(st => topeTxtEsp(st) === topeTxtEsp(con[0])) ? t('gl_tope') + ' ' + topeTxtEsp(con[0]) + ' ' + fuente
      : t('gl_tope') + ' ' + con.map(st => trTxt(st) + ': ' + topeTxtEsp(st)).join('') + ' ' + fuente;
    return { acum, tope }; };
  const lineas = (el) => [...el.querySelectorAll('.annota, li')].map(pl);
  const variante = new Map();   // efecto -> [v, entrada del análisis], para «Cómo funciona»
  for (const v of todas) { const an = ANALISIS[v.p]; if (an) for (const [ie, d, obj, fuentes] of an.fx) { const id = CATALOGO.efectos[ie].id; if (!variante.has(id)) variante.set(id, [v, { ie, fuentes }]); } }
  for (const e of CATALOGO.efectos) { const x = esperado(e); if (!x) continue; out.efectos++;
    const gl = lineas(doc(efectoGl(e)));
    out.casos++; if (!gl.includes(x.acum) || (x.tope && !gl.includes(x.tope)) || (!x.tope && gl.some(l => l.startsWith(t('gl_tope'))))) falla(['glosario', e.id, x, gl]);
    const vx = variante.get(e.id);
    if (vx) { const cf = lineas(doc(efectoTipHtml(vx[0], vx[1])));
      out.casos++; if (!cf.some(l => l.startsWith(x.acum)) || (x.tope && !cf.some(l => l.startsWith(x.tope)))) falla(['como_funciona', e.id, x, cf]); }
  }
  // 3. lo que recibe: cada renglón con su tope (y su fuente) si el stat tiene, y el aviso si lo que suman pasa lo que queda
  const nombre = new Map([...stats].map(st => [trTxt(st), st]));
  const revisa = (eq) => { const lider = liderDe(eq, null);
    for (const m of eq) { const d = doc(recibeTablaHtml(m, sumaDe(origenesDe(m, eq, lider)), nombreEn(eq), 'x')), siempre = new Map(), filas = [];
      for (const f of d.querySelectorAll('.pqm-fila:not(.pqm-th)')) { const st = nombre.get(pl(f.querySelector('.pqm-ef').firstChild)) || null;
        const tot = (pl(f.querySelector('.pqm-tot')) || '').match(/^([+−-])?([\d.,]+)%/), cond = !!f.querySelector('.pqm-cond');
        const n = tot ? Number(LANG === 'es' ? tot[2].replace(/\./g, '').replace(',', '.') : tot[2].replace(/,/g, '')) * (tot[1] === '−' || tot[1] === '-' ? -1 : 1) : null;
        filas.push({ f, st, cond, n }); if (st && !cond && n != null) siempre.set(st, n); }
      for (const { f, st, cond, n } of filas) { out.renglones++; out.casos++;
        const tope = f.querySelector('.pqtope'), pasa = f.querySelector('.pqpasa'), ks = st && CAT[st] ? CAT[st].tope || [] : [];
        if (!ks.length) { if (tope || pasa) falla(['tope_de_mas', m.key, st, pl(f)]); continue; }
        out.con_tope++;
        const esp = t('pq_tope').replace('{t}', topeTxtEsp(st));
        if (!tope || !pl(tope).startsWith(esp) || (tope.querySelector('.fuente') || {}).textContent !== fuente) { falla(['tope', m.key, st, pl(tope), esp]); continue; }
        const suma = n == null ? null : Math.abs(n + (cond ? siempre.get(st) || 0 : 0)), queda = Math.min(...ks.map(k => TOPE[k][0] - TOPE[k][1]));
        const deberia = suma != null && suma > queda;
        if (deberia) out.avisos++;
        if (deberia !== !!pasa || (pasa && !pl(pasa).includes(numTxt(suma) + '%'))) falla(['aviso', m.key, st, suma, queda, pl(pasa)]); } } };
  let semilla = 31; const azar = (n) => { semilla = (semilla * 1103515245 + 12345) % 2147483648; return semilla % n; };
  for (let n = 0, hechos = 0; hechos < 300 && n < 3000; n++) { const eq = [todas[azar(todas.length)], todas[azar(todas.length)], todas[azar(todas.length)]];
    if (new Set(eq.map(x => x.cid)).size < 3) continue; hechos++; revisa(eq); }
  out.casos++; if (out.avisos) falla(['con los datos, ningún trío pasa un tope', out.avisos]);
  // crítico de prueba en dos integrantes que no traen crítico: 50 y otro valor; el aviso cuando la suma pasa 75
  const sinCrit = todas.filter(v => SOPORTES[v.p] && !SOPORTES[v.p].t22 && !Object.values(SOPORTES[v.p]).some(x => x && x.fx && x.fx.some(f => f.s === 'Critical Rate')));
  const antes = out.avisos;
  for (let n = 0, hechos = 0; hechos < 40 && n < 4000; n++) { const eq = [sinCrit[azar(sinCrit.length)], sinCrit[azar(sinCrit.length)], todas[azar(todas.length)]];
    if (new Set(eq.map(x => x.cid)).size < 3 || Object.values(SOPORTES[eq[2].p] || {}).some(x => x && x.fx && x.fx.some(f => f.s === 'Critical Rate'))) continue; hechos++;
    SOPORTES[eq[0].p].t22 = { fx: [{ s: 'Critical Rate', v: 50 }] }; SOPORTES[eq[1].p].t22 = { fx: [{ s: 'Critical Rate', v: [10, 25, 26, 40][hechos % 4] }] };
    _NO_ACUM_DE.clear(); _SLOTS.clear();
    try { revisa(eq); } finally { delete SOPORTES[eq[0].p].t22; delete SOPORTES[eq[1].p].t22; _NO_ACUM_DE.clear(); _SLOTS.clear(); } }
  out.avisos_prueba = out.avisos - antes;
  out.casos++; if (!out.avisos_prueba) falla(['con crítico de prueba, algún aviso', out.avisos_prueba]);
  return out;
}"""),
]

# Las seis reglas que está decidiendo Ezequiel (y la de recomendados contra rol_en): qué pantallas las contestan hoy
# distinto (inventario-app.md, sección 2.1). Cuando se decidan, cada una pasa a PREGUNTAS con su js.
PENDIENTES = [
  dict(id='recomendados_contra_rol_en', desc='Modos › Personajes recomendados contra la función en PvP y PvE de las combinaciones'),
]

srv, url = levantar(carpeta_datos(), origen_local())
errores = []
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900})
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errores.append('consola: ' + m.text))
        def gancho(route):
            r = route.fetch(); cuerpo = r.text()
            assert cuerpo.count('\narrancar();\n})();') == 1
            route.fulfill(response=r, body=cuerpo.replace('\narrancar();\n})();', '\nwindow.__ev = s => eval(s);\narrancar();\n})();'))
        pg.route(lambda u: '/app.js' in u, gancho)
        pg.goto(url); pg.wait_for_selector('.ccard'); pg.set_default_timeout(0)
        for lang in ('es', 'en'):
            if lang == 'en':
                pg.click('[data-a="lang"]'); pg.wait_for_selector('.ccard')
            t0 = time.time(); c = pg.evaluate('(js) => window.__ev(js)()', COMUNES)
            print(f'[{lang}] comunes: {c} ({time.time() - t0:.1f} s)')
            for q in PREGUNTAS:
                t0 = time.time(); r = pg.evaluate('(js) => window.__ev(js)()', q['js'])
                extra = {k: v for k, v in r.items() if k not in ('casos', 'mal', 'ejemplos')}
                ok(f"[{lang}] {q['id']}: {q['desc']} ({r['casos']} casos{', ' + json.dumps(extra, ensure_ascii=False) if extra else ''})",
                   r['casos'] > 0 and r['mal'] == 0, f"{r['mal']} distintas: {json.dumps(r['ejemplos'], ensure_ascii=False)[:900]}" if r['mal'] else f'{time.time() - t0:.1f} s')
        pg.click('[data-a="lang"]')
        b.close()
finally:
    srv.terminate(); srv.wait()
for q in PENDIENTES:
    print('PENDIENTE', q['id'], '|', q['desc'], '(decisión de Ezequiel)')
ok('sin errores de página ni de consola', not errores, errores[:3])
ok.fin()
