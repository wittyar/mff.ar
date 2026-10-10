"""«Cómo funciona» de todas las skills (1.0.19): abre la ficha de cada una de las 888 variantes en la pestaña
Skills, toca la cabecera de cada skill y lo cierra, en español y en inglés. Cada popover tiene que abrirse con
sus cinco secciones, sin «undefined» ni «NaN» en el texto y sin errores de página: un efecto sin entrada en el
análisis, un término o una etiqueta que falta tiran un error. Complementa a verif_tooltip_skill.py, que
prueba seis skills a fondo contra un modelo. Los clics van dentro de la página (son miles)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js
from playwright.sync_api import sync_playwright

ok = Chequeo()
PJ = datos_js('MFF_SEED_CHARACTERS')['MFF_SEED_CHARACTERS']
VARS = [[c['id'], None] for c in PJ] + [[c['id'], u['id']] for c in PJ for u in c.get('uniforms', [])]
BARRIDO = """async (vars) => {
  const errs = [], onErr = (e) => errs.push(String(e.message || e.reason));
  window.addEventListener('error', onErr); window.addEventListener('unhandledrejection', onErr);
  let skills = 0, titulo = null;
  for (const [cid, uid] of vars) {
    const el = document.createElement('button'); el.dataset.a = 'open'; el.dataset.cid = cid;
    if (uid) el.dataset.uid = uid;
    document.body.appendChild(el); el.click(); el.remove();
    const tab = document.querySelector('[data-a="fichaTab"][data-v="skills"]');
    if (!tab) { errs.push(`${cid} ${uid}: sin pestaña Skills`); continue; }
    if (!document.querySelector('.sktit')) tab.click();
    for (const b of [...document.querySelectorAll('.sktit')]) {
      const antes = errs.length;
      b.click(); skills++;
      const pop = document.getElementById('skpop');
      if (!pop) { errs.push(`${cid} ${uid} ${b.id}: no se abrió` + (errs.length > antes ? '' : ' (sin error)')); continue; }
      const secs = pop.querySelectorAll('.tipsec').length, txt = pop.innerText;
      titulo = titulo || pop.querySelector('.tipsec h4').textContent;
      if (secs !== 5) errs.push(`${cid} ${uid} ${b.id}: ${secs} secciones`);
      if (/undefined|NaN|\\[object Object\\]/.test(txt)) errs.push(`${cid} ${uid} ${b.id}: texto con undefined/NaN`);
      pop.querySelector('[data-a="tipCerrar"]').click();
      if (document.getElementById('skpop')) errs.push(`${cid} ${uid} ${b.id}: no se cerró`);
    }
  }
  window.removeEventListener('error', onErr); window.removeEventListener('unhandledrejection', onErr);
  return { skills, errs, titulo };
}"""
srv, url = levantar(carpeta_datos(), origen_local())
try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        for lang in ('es', 'en'):
            pg = b.new_page(viewport={'width': 1300, 'height': 900})
            errores_pagina = []
            pg.on('pageerror', lambda e: errores_pagina.append(str(e)))
            pg.goto(url); pg.wait_for_selector('#app main')
            if lang == 'en':
                pg.click('[data-a="lang"]'); pg.wait_for_timeout(200)
            skills, errs, titulos = 0, [], set()
            for i in range(0, len(VARS), 120):
                r = pg.evaluate(BARRIDO, VARS[i:i + 120])
                skills += r['skills']; errs += r['errs']; titulos.add(r['titulo'])
            ok(f'{lang}: el popover está en el idioma de la app', titulos == {'Cómo funciona' if lang == 'es' else 'How it works'}, str(titulos))
            print(f'{lang}: {len(VARS)} variantes, {skills} skills, {len(errs)} errores')
            for e in errs[:30]:
                print('   ', e)
            ok(f'{lang}: todas las skills abren su «Cómo funciona» bien', not errs, f'{len(errs)} errores')
            ok(f'{lang}: sin errores de página', not errores_pagina, '; '.join(errores_pagina[:3]))
            ok(f'{lang}: más de 5000 skills recorridas', skills > 5000, str(skills))
            pg.close()
        b.close()
finally:
    srv.terminate()
ok.fin()
