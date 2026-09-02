#!/usr/bin/env python3
"""Reconstruye data.js y mff-thanosvibs-import.json desde work/. Correr tras fetch_all y parse_skills."""
import json, os, datetime
exec(open(os.path.join(os.path.dirname(__file__), '_core.py')).read())  # deja work/build2.json

b = json.load(open('work/build2.json'))
chars, images, assign = b['characters'], b['images'], b['assign']
gv = json.load(open('work/gen_versions.json'))[0]['gameVersion']
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
hoy = datetime.date.today().isoformat()
header = f"""// data.js — Comparador MFF (generado por scripts/build.py el {hoy}; juego {gv})
// Fuentes: thanosvibs.money (personajes/uniformes/retratos/íconos/tier list) y
// future-fight.fandom.com (skills e instintos). Cada skill trae 'fx' (efectos por objetivo).
// Crédito: THANO$VIB$ y Future Fight Wiki. Uso personal.
"""
tl = [{"id": "tv-general", "name": f"THANO$VIB$ General {gv} (aprox.)"}]
parts = [header,
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
 'window.MFF_TEAM_SUGGESTIONS = [];\n',
 'window.MFF_SEED_IMAGES = ' + json.dumps(images, ensure_ascii=False) + ';\n',
 'window.MFF_SEED_TIERLISTS = ' + json.dumps(tl, ensure_ascii=False) + ';\n',
 'window.MFF_SEED_TIER_ASSIGNMENTS = ' + json.dumps({'tv-general': assign}, ensure_ascii=False) + ';\n',
 """
window.MFF_skillTiming = function (skill) {
  if (skill.perm) return 'Permanente';
  if (skill.slot === 'Definitiva') return 'Barra de habilidad llena';
  if (skill.cd) return skill.cd + 's de recarga';
  return '—';
};
"""]
open('data.js','w').write('\n'.join(parts))
state = {
  'characters': chars, 'teams': [], 'modes': SEED['MODES'],
  'customTierLists': tl, 'tierAssignments': {'tv-general': assign},
  'taxonomies': {
    'factions': [{'value':v,'icon':images.get('icon-'+v,'')} for v in SEED['FACTIONS']],
    'instincts': [{'value':v,'icon':''} for v in SEED['INSTINCTS']],
    'races': [{'value':v,'icon':images.get('icon-'+v,'')} for v in SEED['RACES']],
    'genders': [{'value':v,'icon':images.get('icon-'+v,'')} for v in SEED['GENDERS']],
    'skillTags': [{'value':v,'icon':images.get('icon-'+v,'')} for v in SEED['SKILL_TAGS']],
  },
  'images': images, 'logo': ''}
json.dump(state, open('mff-thanosvibs-import.json','w'), ensure_ascii=False, indent=1)
print(f"data.js {os.path.getsize('data.js')//1024} KB | import {os.path.getsize('mff-thanosvibs-import.json')//1024} KB | juego {gv}")
