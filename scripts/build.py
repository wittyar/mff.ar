#!/usr/bin/env python3
"""Reconstruye data.js, datos.json, mff-thanosvibs-import.json, docs/AUDITORIA.md y
docs/CATALOGO.md desde work/. Correr tras fetch_all.py y parse_instinto.py.

Orden: skills_api.py (work/skills_parsed.json), fuentes.py (work/fuentes.json),
catalogo.py (valida el catálogo de efectos contra los datos; docs/CATALOGO.md),
auditar.py (work/verificacion.json y docs/AUDITORIA.md) y _core.py (personajes y tier
lists, work/build2.json); acá se junta todo en data.js.

datos.json es lo que la app instalada consulta en GitHub para saber si hay datos nuevos:
versión, formato, sha256 y tamaño de cada archivo que baja, y la lista de imágenes con
su origen. Por eso data.js y el informe se escriben en UTF-8 con finales de línea \n
en cualquier sistema, y .gitattributes impide que git los convierta: el hash publicado
tiene que ser el de lo que se descarga."""
import hashlib, json, os, datetime
import subprocess, sys
# Los módulos del pipeline (dominio, version_juego) viven al lado de este script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Sin los insumos de fetch_all no hay nada que construir. Se avisa en una linea en vez
# de reventar con un traceback: este script lo corre la app de escritorio y el texto
# va directo a la pantalla del usuario.
_faltan = [f for f in ('work/characters.json', 'work/instintos.json', 'work/uniforms.json',
                       'work/updates.json', 'work/ctps.json', 'work/artifacts.json', 'work/abxl.json',
                       'work/supports.json', 'work/rotations.json', 'work/wiki_artifact.json',
                       'work/guia/changelog.json', 'work/guia/parte1.txt', 'work/guia/parte2.txt')
           if not os.path.exists(f)]
if not os.path.isdir('work/skills_api') or not os.listdir('work/skills_api'):
    _faltan.append('work/skills_api/')
if _faltan:
    raise SystemExit('Faltan datos para construir: ' + ', '.join(_faltan) +
                     '\nCorre primero: python scripts/fetch_all.py --datos'
                     '  (o el boton "Actualizar datos del juego" en Ajustes)')
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'skills_api.py')], check=True)
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'fuentes.py')], check=True)
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'catalogo.py')], check=True)
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'auditar.py')], check=True)
exec(open(os.path.join(os.path.dirname(__file__), '_core.py')).read())

b = json.load(open('work/build2.json'))
chars, images, assign, tierlists = b['characters'], b['images'], b['assign'], b['tierlists']
vocab, SKILLS, TABLAS, BUFFS = b['vocab'], b['skills'], b['tablas'], b['buffs']
PERFILES, ANALISIS = b['perfiles'], b['analisis']
# El catálogo de efectos (scripts/contenido/catalogo.json, validado por catalogo.py): lo que la
# app necesita para mostrar el análisis de cada variante.
_CAT = json.load(open(os.path.join(os.path.dirname(__file__), 'contenido', 'catalogo.json'), encoding='utf-8'))
CATALOGO = {k: _CAT[k] for k in ('certeza', 'sirve', 'contra', 'grupos', 'efectos', 'skills')}
FUENTES = json.load(open('work/fuentes.json', encoding='utf-8'))
VERIF = json.load(open('work/verificacion.json', encoding='utf-8'))['por_retrato']
# Íconos de C.T.P.s y artefactos: arte de terceros que baja fetch_all --imagenes, igual
# que los retratos; si falta el archivo la app muestra el nombre sin ícono.
for c in FUENTES['ctps']:
    images['ctp-' + c['id']] = f"images/items/ctp_{c['id']}.png"
for a in FUENTES['artefactos']:
    images['art-' + a['p']] = f"images/items/artifact_{a['p']}.png"
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
 'SKILL_TAGS': ABIL_VALUES,
 'FACTIONS': ['Superhéroe','Supervillano','Neutral'],
 # Ventaja de tipo: a qué clases le gana cada una y con qué fuerza. Combate > Velocidad >
 # Detonación > Combate (wiki, páginas de cada clase); Universal le gana a las otras tres con
 # una ventaja menor y no tiene debilidad (guía de thanosvibs, parte 3, Type Enhancement;
 # confirmado por Ezequiel). docs/MODELO.md, etapa 1.
 'VENTAJA_TIPO': {'Combate': {'Velocidad': 'normal'}, 'Velocidad': {'Detonación': 'normal'},
                  'Detonación': {'Combate': 'normal'},
                  'Universal': {'Combate': 'menor', 'Velocidad': 'menor', 'Detonación': 'menor'}}
}
hoy = hoy.isoformat()
# Version del juego y fecha del snapshot, como dato de la app (no solo como comentario):
# la app de escritorio las compara contra thanosvibs para avisar si hay una mas nueva.
# FORMATO sube cuando una app y unos datos de versiones distintas ya no se entienden: a la
# app nueva le falta algo que los datos viejos no traen, o la anterior leería mal los nuevos.
# La app solo acepta datos de su mismo formato: con datos de otro, los baja al arrancar o
# avisa que hace falta actualizarla.
# 2: el perfil de combate de cada retrato viene calculado (MFF_PERFIL) y la app ya no lo
#    deduce de las skills: la app nueva no puede usar datos sin él.
# 3: el análisis de cada variante (MFF_ANALISIS) y el catálogo de efectos (MFF_CATALOGO) para
#    mostrarlo; los uniformes traen sus propios roles.
FORMATO = 3
VERSION = {'juego': gv, 'generado': hoy, 'formato': FORMATO}
header = f"""// data.js — TA GUIANAEL MFF (generado por scripts/build.py el {hoy}; juego {gv})
// Fuentes: thanosvibs.money (personajes, uniformes, skills, tier lists, C.T.P., artefactos,
// soportes, rotaciones, Alliance Battle, guía, retratos e íconos), future-fight.fandom.com
// (instintos y el contraste de docs/AUDITORIA.md) y la guía de armado de Cynicalex Mega
// Guides (Google Sheets). Crédito: THANO$VIB$, Future Fight Wiki y Cynicalex Mega Guides.
// Uso personal.
"""
# Las listas llegan con las filas rotuladas de la fuente; el rango S-D solo se usa
# como plantilla para las listas que arme el usuario dentro de la app.
DEFAULT_ROWS = [{'id': r, 'label': r} for r in ['S', 'A', 'B', 'C', 'D']]
tl = tierlists
parts = [header,
 'window.MFF_VERSION = ' + json.dumps(VERSION, ensure_ascii=False) + ';\n',
 'window.MFF_SEED = ' + json.dumps(SEED, ensure_ascii=False, indent=1) + ';\n',
 'window.MFF_SEED_CHARACTERS = ' + json.dumps(chars, ensure_ascii=False) + ';\n',
 '// Skills por retrato. Cada efecto guarda el índice de su patrón y sus números;\n'
 '// el texto se arma en la app desde MFF_TABLAS, en el idioma activo.\n',
 'window.MFF_SKILLS = ' + json.dumps(SKILLS, ensure_ascii=False) + ';\n',
 'window.MFF_TABLAS = ' + json.dumps(TABLAS, ensure_ascii=False) + ';\n',
 'window.MFF_BUFFS = ' + json.dumps(BUFFS, ensure_ascii=False) + ';\n',
 '// Perfil de combate por retrato (scripts/modelo.py, docs/MODELO.md): de qué ataque sale su daño\n'
 '// (esc: [ataque, % del total]), los tipos de daño (tip) y los elementos (ele).\n',
 'window.MFF_PERFIL = ' + json.dumps(PERFILES, ensure_ascii=False) + ';\n',
 '// Lo que hace cada variante con sus skills (scripts/modelo.py, docs/MODELO.md): por retrato, cada\n'
 '// efecto del catálogo con su destino (e: él, q: el equipo, r: el rival, i: sus invocaciones), a qué\n'
 '// aliados va, y de qué skills sale ([skill, etapa, efecto] en MFF_SKILLS); ns: lo que es para él y\n'
 '// no le sirve; sc: lo que el catálogo no clasifica.\n',
 'window.MFF_ANALISIS = ' + json.dumps(ANALISIS, ensure_ascii=False, separators=(',', ':')) + ';\n',
 '// Catálogo de efectos (scripts/contenido/catalogo.json, docs/CATALOGO.md).\n',
 'window.MFF_CATALOGO = ' + json.dumps(CATALOGO, ensure_ascii=False) + ';\n',
 '// C.T.P.s, artefactos, Alliance Battle, soportes, rotaciones, guía y modos\n'
 '// (scripts/fuentes.py y scripts/contenido/).\n',
 'window.MFF_CTPS = ' + json.dumps(FUENTES['ctps'], ensure_ascii=False) + ';\n',
 'window.MFF_ARTEFACTOS = ' + json.dumps(FUENTES['artefactos'], ensure_ascii=False) + ';\n',
 'window.MFF_ABX = ' + json.dumps(FUENTES['abx'], ensure_ascii=False) + ';\n',
 'window.MFF_CANCELS = ' + json.dumps(FUENTES['cancels'], ensure_ascii=False) + ';\n',
 'window.MFF_SOPORTES = ' + json.dumps(FUENTES['soportes'], ensure_ascii=False) + ';\n',
 'window.MFF_ROTACIONES = ' + json.dumps(FUENTES['rotaciones'], ensure_ascii=False) + ';\n',
 '// Contraste con la wiki y chequeos internos por retrato (scripts/auditar.py; informe en docs/AUDITORIA.md).\n',
 'window.MFF_VERIFICACION = ' + json.dumps(VERIF, ensure_ascii=False) + ';\n',
 'window.MFF_GUIA_PJ = ' + json.dumps(FUENTES['guia_pj'], ensure_ascii=False) + ';\n',
 'window.MFF_GUIA = ' + json.dumps({**FUENTES['guia'], 'version_fuente': FUENTES['version_guia_fuente']}, ensure_ascii=False) + ';\n',
 'window.MFF_MODOS = ' + json.dumps(FUENTES['modos'], ensure_ascii=False) + ';\n',
 '// Guía de armado de Cynicalex (copia en uso de fuentes/guia-armado/, por retrato del mejor\n'
 '// uniforme) y el estado de su última comprobación (scripts/guia_armado.py).\n',
 'window.MFF_GUIA_ARMADO = ' + json.dumps(FUENTES['armado'], ensure_ascii=False) + ';\n',
 '// Traducciones de los textos de esas fuentes: inglés -> español (lo que falta viaja en inglés).\n',
 'window.MFF_TXT = ' + json.dumps(FUENTES['txt'], ensure_ascii=False) + ';\n',
 'window.MFF_SEED_IMAGES = ' + json.dumps(images, ensure_ascii=False) + ';\n',
 'window.MFF_VOCAB_EN = ' + json.dumps(vocab, ensure_ascii=False, indent=1) + ';\n',
 'window.MFF_DEFAULT_TIER_ROWS = ' + json.dumps(DEFAULT_ROWS, ensure_ascii=False) + ';\n',
 'window.MFF_SEED_TIERLISTS = ' + json.dumps(tl, ensure_ascii=False) + ';\n',
 'window.MFF_SEED_TIER_ASSIGNMENTS = ' + json.dumps(assign, ensure_ascii=False) + ';\n',
 """
"""]
with open('data.js', 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(parts))
state = {
  'characters': chars, 'teams': [],
  'modes': [{'id': m['id'], 'name': m['nombre'], 'teamSize': m['equipo']['tam']}
            for m in FUENTES['modos'] if m.get('equipo')],
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
from imagenes import origen
def huella(ruta):
    with open(ruta, 'rb') as f:
        contenido = f.read()
    return {'sha256': hashlib.sha256(contenido).hexdigest(), 'bytes': len(contenido)}
manifiesto = {'formato': FORMATO, 'juego': gv, 'generado': hoy,
              'archivos': {r: huella(r) for r in ('data.js', 'docs/AUDITORIA.md')},
              'imagenes': [[r, origen(r)] for r in sorted(set(images.values()))]}
with open('datos.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(manifiesto, f, ensure_ascii=False, indent=1)
    f.write('\n')
print(f"data.js {os.path.getsize('data.js')//1024} KB | import {os.path.getsize('mff-thanosvibs-import.json')//1024} KB"
      f" | juego {gv} | listas {len(tl)} | sets de skills {len(SKILLS)}")
