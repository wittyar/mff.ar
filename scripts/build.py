#!/usr/bin/env python3
"""Reconstruye data.js y mff-thanosvibs-import.json desde work/. Correr tras fetch_all y parse_skills."""
import json, os, datetime
# skills_api.py deja work/skills_parsed.json; _core.py lo consume y deja work/build2.json
import subprocess, sys
# Sin los insumos de fetch_all no hay nada que construir. Se avisa en una linea en vez
# de reventar con un traceback: este script lo corre la app de escritorio y el texto
# va directo a la pantalla del usuario.
_faltan = [f for f in ('work/characters.json', 'work/instintos.json', 'work/uniforms.json',
                       'work/updates.json') if not os.path.exists(f)]
if not os.path.isdir('work/skills_api') or not os.listdir('work/skills_api'):
    _faltan.append('work/skills_api/')
if _faltan:
    raise SystemExit('Faltan datos para construir: ' + ', '.join(_faltan) +
                     '\nCorre primero: python scripts/fetch_all.py --datos'
                     '  (o el boton "Actualizar datos del juego" en Ajustes)')
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'skills_api.py')], check=True)
exec(open(os.path.join(os.path.dirname(__file__), '_core.py')).read())

b = json.load(open('work/build2.json'))
chars, images, assign, tierlists = b['characters'], b['images'], b['assign'], b['tierlists']
vocab, SKILLS, TABLAS, BUFFS = b['vocab'], b['skills'], b['tablas'], b['buffs']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from version_juego import ultima
hoy = datetime.date.today()
gv = ultima(json.load(open('work/updates.json')), hoy)[1]
ABIL_VALUES = sorted({a for c in chars for a in c['abilities']})
SEED = {
 'CLASSES': ['Combate','Detonación','Velocidad','Universal'],
 'ROLES': ['Daño','Soporte','Control','Tanque'],
 'TIERS': ['T2','T3','T4'],
 'INSTINCTS': ['Justicia','Orden','Destrucción','Crueldad','Desconocido'],
 'RACES': ['Humano','Mutante','Inhumano','Alienígena','Criatura','Otro'],
 'GENDERS': ['Masculino','Femenino','Neutro'],
 'DAMAGE_TYPES': ['Físico','Energía','PG','Ninguno'],
 'MODES': [
   {'id':'pvp','name':'PvP','teamSize':3},
   {'id':'alianza','name':'Alianza','teamSize':3},
   {'id':'incursion','name':'Incursión','teamSize':5},
   {'id':'sombras','name':'Mundo de Sombras','teamSize':3}],
 'SKILL_TAGS': ABIL_VALUES,
 'FACTIONS': ['Superhéroe','Supervillano','Neutral'],
 'CLASS_ADVANTAGE': {'Combate':'Velocidad','Velocidad':'Detonación','Detonación':'Combate','Universal':None}
}
hoy = hoy.isoformat()
# Version del juego y fecha del snapshot, como dato de la app (no solo como comentario):
# la app de escritorio las compara contra thanosvibs para avisar si hay una mas nueva.
VERSION = {'juego': gv, 'generado': hoy}
header = f"""// data.js — TA GUIANAEL MFF (generado por scripts/build.py el {hoy}; juego {gv})
// Fuentes: thanosvibs.money (personajes/uniformes/retratos/íconos/tier list) y
// future-fight.fandom.com (skills e instintos). Cada skill trae 'fx' (efectos por objetivo).
// Crédito: THANO$VIB$ y Future Fight Wiki. Uso personal.
"""
# Las listas llegan con las filas rotuladas de la fuente; el rango S-D solo se usa
# como plantilla para las listas que arme el usuario dentro de la app.
DEFAULT_ROWS = [{'id': r, 'label': r} for r in ['S', 'A', 'B', 'C', 'D']]
tl = tierlists
parts = [header,
 'window.MFF_VERSION = ' + json.dumps(VERSION, ensure_ascii=False) + ';\n',
 'window.MFF_SEED = ' + json.dumps(SEED, ensure_ascii=False, indent=1) + ';\n',
 """
function sk(slot, n, d, dmg, ii, tags, opts) {
  opts = opts || {};
  let cd = null, perm = false;
  if (slot === 'Pasiva' || slot === 'Liderazgo') perm = true;
  else if (slot === 'Definitiva') { cd = null; perm = false; }
  else { const idx = parseInt(slot.replace(/\\D/g, ''), 10) || 1; cd = 6 + idx * 2; }
  if (opts.cd !== undefined) cd = opts.cd;
  if (opts.perm !== undefined) perm = opts.perm;
  const iframe = opts.iframe !== undefined ? opts.iframe : (slot === 'Definitiva');
  return { slot, n, d, dmg, ii: !!ii, tags: tags || [], cd, perm, iframe: !!iframe, gb: !!opts.gb, sgb: !!opts.sgb };
}
window.MFF_sk = sk;
""",
 'window.MFF_SEED_CHARACTERS = ' + json.dumps(chars, ensure_ascii=False) + ';\n',
 '// Skills por retrato. Cada efecto guarda el índice de su patrón y sus números;\n'
 '// el texto se arma en la app desde MFF_TABLAS, en el idioma activo.\n',
 'window.MFF_SKILLS = ' + json.dumps(SKILLS, ensure_ascii=False) + ';\n',
 'window.MFF_TABLAS = ' + json.dumps(TABLAS, ensure_ascii=False) + ';\n',
 'window.MFF_BUFFS = ' + json.dumps(BUFFS, ensure_ascii=False) + ';\n',
 'window.MFF_TEAM_SUGGESTIONS = [];\n',
 'window.MFF_SEED_IMAGES = ' + json.dumps(images, ensure_ascii=False) + ';\n',
 'window.MFF_VOCAB_EN = ' + json.dumps(vocab, ensure_ascii=False, indent=1) + ';\n',
 'window.MFF_DEFAULT_TIER_ROWS = ' + json.dumps(DEFAULT_ROWS, ensure_ascii=False) + ';\n',
 'window.MFF_SEED_TIERLISTS = ' + json.dumps(tl, ensure_ascii=False) + ';\n',
 'window.MFF_SEED_TIER_ASSIGNMENTS = ' + json.dumps(assign, ensure_ascii=False) + ';\n',
 """
"""]
open('data.js','w').write('\n'.join(parts))
state = {
  'characters': chars, 'teams': [], 'modes': SEED['MODES'],
  'customTierLists': tl, 'tierAssignments': assign,
  'taxonomies': {
    'factions': [{'value':v,'icon':images.get('icon-'+v,'')} for v in SEED['FACTIONS']],
    'instincts': [{'value':v,'icon':''} for v in SEED['INSTINCTS']],
    'races': [{'value':v,'icon':images.get('icon-'+v,'')} for v in SEED['RACES']],
    'genders': [{'value':v,'icon':images.get('icon-'+v,'')} for v in SEED['GENDERS']],
    'skillTags': [{'value':v,'icon':images.get('icon-'+v,'')} for v in SEED['SKILL_TAGS']],
  },
  'images': images, 'logo': ''}
json.dump(state, open('mff-thanosvibs-import.json','w'), ensure_ascii=False, indent=1)
print(f"data.js {os.path.getsize('data.js')//1024} KB | import {os.path.getsize('mff-thanosvibs-import.json')//1024} KB"
      f" | juego {gv} | listas {len(tl)} | sets de skills {len(SKILLS)}")
