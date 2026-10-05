#!/usr/bin/env python3
"""Completitud de los datos: qué le falta a cada variante (un personaje con un uniforme) para tener la
información que la app muestra y usa. docs/AUDITORIA.md marca lo que dos fuentes dicen distinto; esto,
lo que no está.

Lee solo lo que produce el build: data.js (los datos de la app) y datos.json (las imágenes que la app
baja). Escribe docs/COMPLETITUD.md: qué es «completo» y por qué es esperable cada pieza, el resumen, una
tabla por tipo de faltante y la lista por personaje. Con --json RUTA escribe además lo mismo en JSON,
para buscar en foros lo que falta.

Cada faltante dice de dónde podría salir. Lo que no existe en el juego no es un faltante (un personaje sin
artefacto, si ninguna fuente dice que tenga uno), y lo que una fuente dice a propósito tampoco: va aparte,
con la razón. Por ejemplo, lo que la guía de armado no le da a quien dice que no vale la pena armar.

Lo llama build.py al final, con data.js y datos.json ya escritos. Con el mismo data.js da el mismo informe:
la fecha es la de los datos, no la del día."""
import argparse, collections, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from liderazgos import ROTULOS, derivar, motivo_txt

_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join('docs', 'COMPLETITUD.md')

# Los globales de data.js que se leen.
GLOBALES = ('MFF_VERSION', 'MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_TABLAS', 'MFF_PERFIL', 'MFF_ANALISIS',
            'MFF_CATALOGO', 'MFF_ROLES_LISTAS', 'MFF_BONOS', 'MFF_STRIKERS', 'MFF_ARTEFACTOS', 'MFF_SOPORTES',
            'MFF_ROTACIONES', 'MFF_GUIA', 'MFF_GUIA_ARMADO', 'MFF_SEED_IMAGES', 'MFF_SEED_TIERLISTS',
            'MFF_SEED_TIER_ASSIGNMENTS')


def cargar_datajs(ruta):
    """{global: valor} de data.js: cada «window.MFF_X = <JSON>;»."""
    texto = open(ruta, encoding='utf-8').read()
    dec, out = json.JSONDecoder(), {}
    for m in re.finditer(r'^window\.(MFF_[A-Z_]+) = ', texto, re.M):
        out[m.group(1)], _ = dec.raw_decode(texto, m.end())
    faltan = [g for g in GLOBALES if g not in out]
    if faltan:
        raise SystemExit(f'data.js no trae {", ".join(faltan)}: correr scripts/build.py')
    return out


# ---------------------------------------------------------------------------
# Qué es «completo»: las piezas, qué se pide de cada una y por qué es esperable que esté.
# ---------------------------------------------------------------------------
PIEZAS = [
    ('identidad', 'Identidad',
     'Clase, bando, género, raza, habilidades, habilidad de World Boss, instinto y tipo de ataque.',
     'thanosvibs los publica para todos [Comprobado], salvo el instinto, que la app toma del infobox de la '
     'wiki: que todos tengan uno en el juego es [Probable]. El tipo de ataque se deduce del daño de las '
     'activas.'),
    ('stats', 'Stats',
     'Recuperación y las cinco resistencias elementales.',
     'Son los stats que thanosvibs publica [Comprobado]; la ficha muestra los del personaje en todas sus '
     'variantes.'),
    ('skills', 'Skills',
     'Liderazgo, pasiva, pasiva de Tier-2 y las cinco activas; la Definitiva con Tier-3 o Trascendido; la '
     'Striker con Tier-4; la pasiva de uniforme en cada uniforme. Cada skill con efectos tipados, sin '
     'marcadores sin resolver ($HEROSUBTYPE1, $TIME sin duración), sin códigos en lugar de nombres, sin '
     'objetivos sin nombre, sin «Give Power» vacíos y, las activas, con su recarga.',
     'Son las skills de toda variante en el juego [Comprobado]: los 598 uniformes de los datos traen su '
     'pasiva de uniforme. El análisis, los roles y la sinergia leen sus efectos.'),
    ('lideres', 'Liderazgo y soportes',
     'Su liderazgo, el de Leads & Supports o, si no lo publica, el que el build deriva de su Leader Skill; los '
     'soportes que sus pasivas le dan al equipo, en Leads & Supports, con el nombre de la skill de la que salen.',
     'La sinergia y los órdenes PvP y PvE solo ven lo que publica Leads & Supports y los liderazgos que el build '
     'deriva de la Leader Skill de la API [Comprobado] (Ezequiel, 4 de octubre de 2026; docs/AUDITORIA.md, '
     'sección 12).'),
    ('artefacto', 'Artefacto',
     'Si existe, su texto con los valores de 3★ a 6★ y su ícono.',
     'La ficha lo muestra por estrellas [Comprobado]. Un personaje sin artefacto no es un faltante si '
     'ninguna fuente dice que tenga uno (ni Leads & Supports ni la guía de armado).'),
    ('strikers', 'Strikers',
     'Quiénes pueden aparecer a pegar con él (pestaña Striker de la wiki).',
     'En el juego cada personaje tiene sus strikers [Probable]: la lista de Kingpin coincide con la del '
     'juego. Suman en la sinergia y en los órdenes PvP y PvE.'),
    ('bonos', 'Bonos de equipo',
     'Sus bonos de equipo, con nombre.',
     'El juego da bonos a los personajes que van juntos [Comprobado]; que todos tengan alguno es '
     '[Probable]. Suman en la sinergia.'),
    ('ctp', 'C.T.P.',
     'Su fila en la Ideal CTP List; C.T.P. en la guía de armado y, si tiene función en PvP o en PvE, el meta de '
     'ese contexto.',
     'Todos llevan un C.T.P. desde el Nv. 30 [Comprobado]. La ficha muestra los dos; las tarjetas de '
     'equipo, los de la guía de armado según el contexto.'),
    ('armado', 'Guía de armado',
     'Su fila hecha, con C.T.P., ISO-8 y obelisco, salvo que la guía diga que no vale la pena armarlo (ISO-8 '
     '«dont waste gold») o la Ideal CTP List lo ponga en «Not worth».',
     'La guía de armado tiene una fila por personaje y la completa para la mayoría [Comprobado]; la pestaña '
     'Armado la muestra.'),
    ('listas', 'Tier lists',
     'Su lugar en la tier list General de thanosvibs; la función en PvP y en PvE va como dato.',
     'La General ubica a todo el roster [Comprobado]. Estar o no en Arena (PvP) o en Alianza y World Boss '
     'Legend (PvE) es la función en el contexto, que dice la lista: no estar no es un faltante.'),
    ('imagenes', 'Retrato e íconos',
     'Su retrato y los íconos de su clase, bando, raza, género, habilidades y habilidad de World Boss, '
     'publicados en datos.json.',
     'La app baja lo que publica datos.json [Comprobado].'),
    ('rotaciones', 'Rotación',
     'Una rotación de thanosvibs para la variante, o la de la guía de armado si la guía es de ese '
     'uniforme.',
     'Toda variante usa sus activas en algún orden, y las skills cambian con cada uniforme [Probable]. '
     'thanosvibs publica las rotaciones por uniforme.'),
    ('perfil', 'Perfil y roles',
     'Con qué pega (ataque, tipos de daño, elementos) y sus roles.',
     'Los calcula el build de sus skills [Comprobado]; la sinergia los usa.'),
    ('uniforme', 'Datos del uniforme',
     'Costo, materiales y las cinco opciones de uniforme (retratos del roster).',
     'thanosvibs los publica para cada uniforme [Comprobado].'),
]

# Tipos de faltante: pieza, título, nivel (variante o personaje), de dónde podría salir, rótulo corto (para
# la lista por personaje) y por qué falta. Cada uno se detecta abajo; el orden es el de las tablas.
TIPOS = collections.OrderedDict([
    ('instinto', ('identidad', 'Instinto desconocido', 'personaje',
                  'la wiki (infobox o categoría de la página), el juego o foros', 'instinto',
                  'thanosvibs no publica el instinto y la app lo toma del infobox de la wiki, que no lo da para estos '
                  'personajes. Que todos tengan uno en el juego es [Probable].')),
    ('identidad', ('identidad', 'Dato de identidad vacío', 'variante', 'thanosvibs', 'identidad',
                   'thanosvibs publica estos datos para todos los personajes.')),
    ('stats', ('stats', 'Stats', 'personaje', 'thanosvibs', 'stats',
               'thanosvibs publica recuperación y resistencias de todos los personajes.')),
    ('skill_falta', ('skills', 'Skill que falta', 'variante', 'thanosvibs (API de skills), la wiki o foros', 'falta la skill',
                     'La API de skills no trae una skill que la variante tiene en el juego por su tier o por ser '
                     'uniforme (docs/AUDITORIA.md, sección 4, lista las de Tier-4 sin Striker y las de skill 6 sin '
                     'Definitiva).')),
    ('skill_vacia', ('skills', 'Skill sin efectos', 'variante',
                     'la wiki (en la pasiva de uniforme, el «Bonus» del uniforme) o foros', 'skill sin efectos',
                     'La skill está en la API, sin ningún efecto. Que el juego le dé uno es [Probable]: de la pasiva de '
                     'uniforme, la wiki publica el «Bonus» de cada uniforme.')),
    ('sin_clasificar', ('skills', 'Efecto que el catálogo no clasifica', 'variante',
                        'a mano (scripts/contenido/catalogo.json)', 'efecto sin clasificar',
                        'Una etiqueta de efecto que el catálogo no clasifica (docs/AUDITORIA.md, sección 9).')),
    ('marcador', ('skills', 'Facción, tipo, raza o habilidad sin resolver ($HEROSUBTYPE1)', 'variante',
                  'el juego o foros, y a mano en scripts/contenido/marcadores.csv', 'marcador sin resolver',
                  'El efecto nombra una facción, un tipo, una raza o una habilidad con un marcador que ni la tabla a '
                  'mano, ni Leads & Supports, ni la wiki resolvieron: la app lo muestra «sin especificar». Son los de '
                  'docs/AUDITORIA.md, sección 8, que los cuenta por id de la API (un id se repite en los uniformes '
                  'que comparten la skill); acá va cada variante.')),
    ('duracion', ('skills', 'Duración sin publicar ($TIME)', 'variante', 'thanosvibs (Leads & Supports), la wiki o foros',
                  '$TIME sin duración',
                  'La API publica «$TIME» sin la duración del efecto: la app lo muestra «sin especificar». Si Leads & '
                  'Supports publica el mismo slot con una duración, se dice; si no, y lo que otorga trae la suya, '
                  'también: que sea la misma no está comprobado.')),
    ('codigo', ('skills', 'Código en lugar de un nombre', 'variante', 'thanosvibs (ids de la API de skills), la wiki o foros',
                'código sin nombre',
                'El texto trae un número donde va el nombre de un efecto, de un elemento o de unas ranuras, y la app '
                'lo muestra como viene (docs/AUDITORIA.md, sección 7). Los de tres cifras son ids de habilidades de la '
                'API; los de cifras sueltas parecen ranuras o elementos.')),
    ('objetivo', ('skills', 'Objetivo sin nombre (Target ID)', 'variante', 'thanosvibs (Leads & Supports) o foros',
                  'objetivo sin nombre',
                  'La etapa se aplica a un grupo de aliados que la API no nombra («Target ID: 72»): la app no puede '
                  'decir a quiénes les llega. Si Leads & Supports restringe el mismo slot, se dice a quiénes.')),
    ('otorga', ('skills', '«Give Power» sin lo que otorga', 'variante', 'thanosvibs (Leads & Supports), la wiki o foros',
                '«Give Power» vacío',
                '«Give Power» («Acquires the following effect…») sin el efecto que sigue: el análisis dice «Otorga un '
                'efecto que la fuente no dice». Si Leads & Supports publica el mismo slot, se dice qué trae.')),
    ('recarga', ('skills', 'Activa sin recarga', 'variante', 'la wiki o el juego', 'sin recarga',
                 'Las activas 1 a 5 se recargan por tiempo y la API publica 0 [Probable].')),
    ('liderazgo', ('lideres', 'Liderazgo sin completar', 'variante',
                   'thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/)',
                   'liderazgo sin completar',
                   'Leads & Supports no publica el liderazgo de la variante y el build no pudo derivar ese slot de su '
                   'Leader Skill (docs/AUDITORIA.md, sección 12, con el mismo motivo): un efecto o una activación sin '
                   'correspondencia con Leads & Supports, un valor que la API no publica, un «Give Power» o una '
                   'contradicción de Leads & Supports. La sinergia y los órdenes PvP y PvE no ven ese slot.')),
    ('soporte', ('lideres', 'Soporte que Leads & Supports no publica', 'variante',
                 'thanosvibs (Leads & Supports) o a mano desde la skill', 'soporte sin Leads & Supports',
                 'Según el análisis, la pasiva le da algo al equipo, y Leads & Supports no publica ese soporte (ni en '
                 'su slot ni con el nombre de la skill): la sinergia no lo cuenta.')),
    ('nombre_ls', ('lideres', 'Nombre en Leads & Supports distinto del de la skill', 'variante', 'el juego o foros',
                   'nombre en Leads & Supports',
                   'Leads & Supports nombra el soporte o el liderazgo con el nombre de otra skill de la variante o con '
                   'uno que la variante no tiene. El enlace del «Por qué» busca la skill por ese nombre: con el de otra '
                   'skill, cae en ella (la «Pasiva 4★ (secundaria)» de Jeff the Land Shark lleva a su Activa 5; la '
                   'Tier-2 de Polaris — Uncanny X-Men, a su Activa 1).')),
    ('artefacto', ('artefacto', 'Artefacto que falta', 'personaje', 'thanosvibs o la wiki', 'artefacto',
                   'thanosvibs no publica su artefacto y otra fuente dice que tiene uno.')),
    ('artefacto_valores', ('artefacto', 'Valores del artefacto incompletos', 'personaje',
                           'la wiki (página Artifact) o el juego', 'valores del artefacto',
                           'El texto del artefacto usa valores que thanosvibs no publica en esos niveles de estrellas: '
                           'la app los marca «sin dato» (docs/AUDITORIA.md, sección 6).')),
    ('strikers', ('strikers', 'Strikers', 'personaje', 'la wiki (pestaña Striker), el juego o foros', 'strikers',
                  'La app toma los strikers de la pestaña Striker de la página de la wiki: sin ella no tiene los suyos '
                  '(docs/AUDITORIA.md, sección 11). Que existan en el juego para todos es [Probable].')),
    ('bonos', ('bonos', 'Bonos de equipo que faltan', 'personaje',
               'la wiki (sección Team Bonus), capturas del juego o foros', 'bonos de equipo',
               'La app toma los bonos de la sección Team Bonus de la wiki y de lo que se vio en el juego. Sin ninguno, '
               'o solo con los del juego, faltan los demás [Probable].')),
    ('bono_sin_nombre', ('bonos', 'Bono de equipo sin nombre', 'personaje', 'capturas del juego o foros', 'bono sin nombre',
                         'Ninguna página de la wiki de sus integrantes le da nombre (docs/AUDITORIA.md, sección 10).')),
    ('ctp_ideal', ('ctp', 'Sin fila en la Ideal CTP List', 'personaje', 'thanosvibs (Ideal CTP List)', 'Ideal CTP List',
                   'La Ideal CTP List ubica a cada personaje en la fila de su C.T.P.')),
    ('ctp_guia', ('ctp', 'Sin C.T.P. en la guía de armado', 'personaje', 'la guía de armado o foros',
                  'C.T.P. en la guía de armado',
                  'La fila del personaje en la guía de armado está hecha pero no trae ningún C.T.P., y ni la guía ni la '
                  'Ideal CTP List dicen que no vale la pena: las tarjetas de equipo dicen «sin dato en la guía». La '
                  'ficha muestra el de la Ideal CTP List.')),
    ('ctp_contexto', ('ctp', 'Sin el C.T.P. de su contexto en la guía de armado', 'variante', 'la guía de armado o foros',
                      'C.T.P. de su contexto',
                      'La variante tiene función en el contexto (está en sus tier lists) y la fila del personaje en la '
                      'guía de armado no tiene el C.T.P. meta de ese contexto: su tarjeta de equipo dice «sin dato en la '
                      'guía».')),
    ('armado_vacio', ('armado', 'Fila vacía en la guía de armado', 'personaje', 'la guía de armado o foros',
                      'fila vacía en la guía de armado',
                      'La guía de armado tiene una fila por personaje y esta no tiene nada de lo que la guía completa '
                      '(C.T.P., ISO-8, obelisco, lugar en su tier list, cómo se consigue): no está hecha. La ficha y las '
                      'tarjetas de equipo dicen «sin dato».')),
    ('armado_guia', ('armado', 'ISO-8 u obelisco sin dato en la guía de armado', 'personaje', 'la guía de armado o foros',
                     'ISO-8 u obelisco en la guía de armado',
                     'La fila del personaje en la guía de armado está hecha pero no trae el ISO-8 o el obelisco, y la guía '
                     'no dice que no valga la pena armarlo: la pestaña Armado dice «—».')),
    ('lista_general', ('listas', 'Sin lugar en la tier list General', 'personaje', 'thanosvibs (tier list General)',
                       'tier list General', 'La tier list General de thanosvibs ubica a todo el roster.')),
    ('imagen', ('imagenes', 'Retrato o ícono', 'variante', 'thanosvibs (imágenes)', 'retrato o ícono',
                'La app baja lo que publica datos.json; sin el archivo, no muestra el retrato o el ícono. El ícono del '
                'bando Neutral no lo baja el build: que thanosvibs tenga uno es [Conjetura].')),
    ('rotacion', ('rotaciones', 'Rotación', 'variante', 'thanosvibs (rotaciones), la guía de armado o foros', 'rotación',
                  'thanosvibs publica rotaciones por uniforme, y la guía de armado, la del mejor uniforme de cada '
                  'personaje. Se dice si otro uniforme del personaje tiene la suya.')),
    ('perfil', ('perfil', 'Perfil de combate o roles', 'variante', 'thanosvibs (API de skills)', 'perfil',
                'El build calcula el perfil de las skills activas.')),
    ('uniforme', ('uniforme', 'Datos del uniforme', 'variante', 'thanosvibs (uniformes)', 'datos del uniforme',
                  'thanosvibs publica costo, materiales y opciones de cada uniforme.')),
])

SLOT_ES = {'Leader Skill': 'Liderazgo', 'Passive': 'Pasiva', 'Tier-2 Passive': 'Pasiva T2',
           'Uniform Passive': 'Pasiva de uniforme', 'Active 1': 'Activa 1', 'Active 2': 'Activa 2',
           'Active 3': 'Activa 3', 'Active 4': 'Activa 4', 'Active 5': 'Activa 5', 'Active Ult': 'Definitiva',
           'Striker Skill': 'Striker'}
BASICAS = ('Leader Skill', 'Passive', 'Tier-2 Passive', 'Active 1', 'Active 2', 'Active 3', 'Active 4', 'Active 5')
PASIVAS = ('Passive', 'Tier-2 Passive', 'Uniform Passive')
# Slots de Leads & Supports (los de app.js) y la skill de la que sale cada uno.
SLOT_LS = {'leader': 'Liderazgo', 'leader2': 'Liderazgo (secundario)', 'passive': 'Pasiva 4★',
           'passive2': 'Pasiva 4★ (secundaria)', 't2': 'Pasiva de Tier-2', 't22': 'Pasiva de Tier-2 (secundaria)',
           'uniform': 'Efecto de uniforme', 'uniform2': 'Efecto de uniforme (secundario)',
           'artifact': 'Skill exclusiva del artefacto', 'np': 'Elección de nuevo jugador'}
SKILL_DE_SLOT = {'leader': 'Leader Skill', 'leader2': 'Leader Skill', 'passive': 'Passive', 'passive2': 'Passive',
                 't2': 'Tier-2 Passive', 't22': 'Tier-2 Passive', 'uniform': 'Uniform Passive', 'uniform2': 'Uniform Passive'}
SLOTS_DE_SKILL = {}
for _k, _sl in SKILL_DE_SLOT.items():
    SLOTS_DE_SKILL.setdefault(_sl, []).append(_k)
LIDERAZGOS = ('leader', 'leader2')
# Las restricciones de Leads & Supports (r en MFF_SOPORTES), para decir a quiénes alcanza.
A_RESTRICCION = {'Ability': 'a la habilidad', 'Type': 'a la clase', 'Allies': 'a la raza', 'Side': 'al bando',
                 'Character': 'al personaje'}
STATS =('recovery_rate', 'fire_resist', 'cold_resist', 'lightning_resist', 'poison_resist', 'mind_resist')
# La tier list General de thanosvibs y la fila de la Ideal CTP List que dice que ningún C.T.P. vale la pena.
GENERAL = 'tv-general'
NO_VALE = 'Not worth'
# Lo que la guía de armado pone como ISO-8 de quien no vale la pena armar (scripts/guia_armado.py, ISO_TOKENS).
NO_INVERTIR = 'dont waste gold'

# Descripciones de la API con un número donde va un nombre (docs/AUDITORIA.md, sección 7: «códigos en
# lugar de nombres»), con la posición de cada código entre los números del texto. Si thanosvibs deja de
# usar una, el informe lo avisa: este chequeo ya no la encontraría.
CODIGOS = {
    'Increases damage dealt to targets with # effect by #%': (0,),
    '#s increase to the duration of #.': (1,),
    'Increases # damage by #% of # Resistance (up to #%)': (0, 2),
    'Accumulates #% of pure # damage when attacking (Max #%)': (1,),
    'Removes # from target (Includes all debuffs)': (0,),
    'Removes the effect # from #.': (0, 1),
    'Decreases # effect used by the Character by #%.': (0,),
    'Decreases damage received from reflected effects by #%.Effect: #': (1,),
    'Sets the Cooldown time of # skill to # sec': (0,),
}
# De qué fuentes podría salir cada faltante, como lista (en el JSON), según el texto de su fuente.
CANALES = (('thanosvibs', r'thanosvibs'), ('wiki', r'la wiki'), ('guia_armado', r'guía de armado'),
           ('juego', r'el juego|capturas del juego'), ('foros', r'foros'), ('a_mano', r'a mano'))


def _num(x):
    return str(x) if isinstance(x, int) else (str(int(x)) if float(x).is_integer() else str(x))


def _relleno(patron, nums):
    """El patrón de la API con sus números en lugar de cada '#'."""
    vals = list(nums or [])
    return re.sub('#', lambda m: _num(vals.pop(0)) if vals else '#', patron)


def _nombre_igual(a, b):
    """Dos nombres de skill iguales salvo mayúsculas, espacios o el tipo de apóstrofo."""
    def n(s):
        return re.sub(r'\s+', ' ', s.replace('’', "'").replace('‘', "'")).strip().casefold()
    return n(a) == n(b)


def _y(xs, y=' y '):
    xs = list(xs)
    return ', '.join(xs[:-1]) + y + xs[-1] if len(xs) > 1 else ''.join(xs)


def _ni(xs):
    """Una lista para una frase negativa: «no trae ISO-8 ni obelisco»."""
    return _y(xs, ' ni ')


class Datos:
    """Lo que se lee de data.js, con los índices que usan los chequeos."""

    def __init__(self, D, imagenes_publicadas):
        self.D = D
        self.TB = D['MFF_TABLAS']
        self.SK, self.AN = D['MFF_SKILLS'], D['MFF_ANALISIS']
        # Leads & Supports tal como lo publica (SO) y los liderazgos que el build deriva de la Leader Skill de la API
        # (los slots con "src": "api"), que se separan: los chequeos de abajo miran lo que publica Leads & Supports.
        self.SO, self.derivados = {}, {}
        for p, e in D['MFF_SOPORTES'].items():
            ls = {k: x for k, x in e.items() if not (isinstance(x, dict) and x.get('src') == 'api')}
            der = {k: x for k, x in e.items() if isinstance(x, dict) and x.get('src') == 'api'}
            if ls:
                self.SO[p] = ls
            if der:
                self.derivados[p] = der
        self.CAT = D['MFF_CATALOGO']
        self.IMG, self.pub = D['MFF_SEED_IMAGES'], imagenes_publicadas
        self.AS = D['MFF_SEED_TIER_ASSIGNMENTS']
        self.GA = D['MFF_GUIA_ARMADO']['pj']
        self.ideal = D['MFF_GUIA']['ctp_ranking']['lista_ideal']
        listas = {t['id']: t for t in D['MFF_SEED_TIERLISTS']}
        for lid in [self.ideal['id'], GENERAL] + [l for c in D['MFF_ROLES_LISTAS'].values() for l in c]:
            if lid not in listas or lid not in self.AS:
                raise SystemExit(f'data.js no trae la tier list {lid}')
        self.filas_ideal = {r['id']: r['label'] for r in listas[self.ideal['id']]['rows']}
        self.avisos = []
        if NO_VALE not in self.filas_ideal.values():
            self.avisos.append(f"la {self.ideal['nombre']} ya no tiene la fila «{NO_VALE}»: lo que la guía de armado no "
                               'trae de los personajes que no vale la pena armar cuenta como faltante (revisar NO_VALE)')
        if not any(e.get('iso') == [NO_INVERTIR] for e in self.GA.values()):
            self.avisos.append(f'ninguna fila de la guía de armado dice «{NO_INVERTIR}» como ISO-8: lo que no trae de los '
                               'personajes que no vale la pena armar cuenta como faltante (revisar NO_INVERTIR)')
        ausentes = sorted(p for p in CODIGOS if p not in {f['en'] for f in self.TB['desc']})
        if ausentes:
            self.avisos.append('estas descripciones con códigos ya no están en los datos y el chequeo de códigos no las '
                               'busca más (revisar CODIGOS): ' + '; '.join(f'«{p}»' for p in ausentes))
        self.art = {a['p']: a for a in D['MFF_ARTEFACTOS']}
        self.bonos_de = collections.defaultdict(list)
        for b in D['MFF_BONOS']:
            for c in b['m']:
                self.bonos_de[c].append(b)
        self.tgt_sin_nombre = {i for i, f in enumerate(self.TB['tgt']) if re.fullmatch(r'Target ID: \d+', f['en'])}
        self.otorga = next(i for i, e in enumerate(self.CAT['efectos']) if e['id'] == 'otorga')
        self.con_lid = {p for p, e in self.SO.items() if any(k in e for k in LIDERAZGOS)}
        self.nombre_pj = {ch['id']: ch['name'] for ch in D['MFF_SEED_CHARACTERS']}
        # Las variantes: cada personaje (en el orden de data.js) con su base y sus uniformes.
        self.personajes = []
        for ch in D['MFF_SEED_CHARACTERS']:
            vs = [self._variante(ch, None)] + [self._variante(ch, u) for u in ch['uniforms']]
            for v in vs:
                v['todas'] = vs
            self.personajes.append({'ch': ch, 'vs': vs})
        self.retratos = {v['p'] for x in self.personajes for v in x['vs']}
        # Los slots de liderazgo que el build no pudo derivar, con su motivo: la misma función que usa el build
        # (scripts/liderazgos.py), sobre Leads & Supports tal como lo publica. Lo que deriva tiene que ser lo que trae
        # data.js.
        L = derivar(self.SO, self.SK, self.TB, {v['p']: x['ch']['name'] for x in self.personajes for v in x['vs']})
        if L['derivados'] != self.derivados:
            raise SystemExit('data.js no trae los liderazgos que scripts/liderazgos.py deriva de sus datos: correr '
                             'scripts/build.py')
        self.sin_derivar = collections.defaultdict(list)
        for x in L['sin_derivar']:
            self.sin_derivar[x['p']].append(x)

    @staticmethod
    def _variante(ch, u):
        """Lo que la app ve de una variante (app.js, variant()): el uniforme pisa lo que redefine."""
        def g(k):
            return (u.get(k) if u else None) or ch[k]
        return {'cid': ch['id'], 'uid': u['id'] if u else None, 'p': u['p'] if u else ch['p'],
                'clave': ch['id'] + '::' + (u['id'] if u else 'base'), 'pj': ch['name'],
                'uni': u['name'] if u else None, 'nombre': ch['name'] + (' — ' + u['name'] if u else ''),
                'c': g('c'), 'f': g('f'), 'race': g('race'), 'gender': g('gender'), 'wba': g('wba'),
                't': u['tier'] if u else ch['t'], 'ab': (u.get('ab') if u else None) or ch['abilities'], 'u': u}

    def nombre_skill(self, sk):
        return self.TB['name'][sk['n']]['en'] if sk['n'] is not None else ''

    def funcion(self, clave, ctx):
        """¿Tiene función en el contexto? Como app.js (rolEn, tieneFuncion): está en una fila de las tier lists
        de ese contexto que le da un rol que no lo deja fuera."""
        for lid, roles in self.D['MFF_ROLES_LISTAS'][ctx].items():
            for fid in self.AS[lid].get(clave, []):
                rol, nivel = roles[fid]
                if (rol in ('dps', 'soporte') and nivel > 0) or rol in ('lider', 'striker'):
                    return True
        return False

    def ls_de_skill(self, p, sk):
        """Los slots de Leads & Supports del retrato que salen de esta skill (por su tipo)."""
        e = self.SO.get(p, {})
        return [k for k in SLOTS_DE_SKILL.get(sk['sl'], []) if k in e]


# ---------------------------------------------------------------------------
# Los chequeos. Cada uno agrega a la lista de la variante (o del personaje) lo que encuentra: {'tipo',
# 'que', 'fuente'} y, si hace falta, 'datos' con lo estructurado. Lo que no cuenta va a la lista aparte.
# ---------------------------------------------------------------------------
def falta(lista, tipo, que, fuente=None, **datos):
    fuente = fuente or TIPOS[tipo][3]
    x = {'tipo': tipo, 'que': que, 'fuente': fuente,
         'canales': [c for c, patron in CANALES if re.search(patron, fuente)]}
    if datos:
        x['datos'] = datos
    lista.append(x)


def chequear_personaje(X, pj, out, aparte):
    """Lo que es del personaje y vale para todas sus variantes."""
    ch, vs = pj['ch'], pj['vs']
    if ch['ins'] == 'Desconocido':
        falta(out, 'instinto', 'la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da')
    if any(k not in ch['stats'] for k in STATS):
        falta(out, 'stats', 'faltan ' + ', '.join(k for k in STATS if k not in ch['stats']))
    # La fila de la guía de armado: la de su mejor uniforme (app.js, armadoDe).
    armado = next((X.GA[v['p']] for v in vs if v['p'] in X.GA), None)
    # Artefacto: existe si thanosvibs lo publica; si no, solo falta si otra fuente dice que tiene uno.
    a = X.art.get(ch['p'])
    if a is None:
        dicen = [f"Leads & Supports ({SLOT_LS['artifact']})" for v in vs if 'artifact' in X.SO.get(v['p'], {})][:1]
        # «Needs Artifact?» de la guía de armado: cualquier respuesta salvo «N» dice que lo tiene.
        if armado and (armado.get('art') or {}).get('v') not in (None, 'N'):
            dicen.append(f"la guía de armado («Needs Artifact?»: {armado['art']['v']})")
        if dicen:
            falta(out, 'artefacto', 'thanosvibs no publica su artefacto, y ' + _y(dicen) + ' dice que tiene uno')
        else:
            aparte.append({'tipo': 'sin_artefacto', 'que': 'no tiene artefacto, y ninguna fuente dice que tenga uno'})
    else:
        usados = {int(x[2:-1]) for ln in a['lineas'] for x in re.findall(r'\[P\d+\]', ln['t'])}
        cortos = [e for e in ('3', '4', '5', '6') if usados and len(a['valores'].get(e, [])) < max(usados)]
        if cortos:
            falta(out, 'artefacto_valores', f"{a['name']}: thanosvibs no publica todos sus valores en "
                  + _y(e + '★' for e in cortos), artefacto=a['name'], estrellas=cortos)
    st = X.D['MFF_STRIKERS'].get(ch['id'])
    if st is None:
        falta(out, 'strikers', 'la wiki no tiene la pestaña Striker de su página')
    elif not st:
        falta(out, 'strikers', 'la pestaña Striker de la wiki no trae ninguna fila que se pueda leer')
    bonos = sorted(X.bonos_de.get(ch['id'], []), key=lambda b: [X.nombre_pj[c] for c in b['m']])
    if not bonos:
        falta(out, 'bonos', 'no tiene ningún bono de equipo: la wiki no lista ninguno con él')
    elif all('wiki-bonos' not in b['f'] for b in bonos):
        falta(out, 'bonos', f'solo tiene los {len(bonos)} que se vieron en el juego: la wiki no lista ninguno con él')
    for b in bonos:
        con = _y(X.nombre_pj[c] for c in b['m'] if c != ch['id'])
        if not b['n']:
            falta(out, 'bono_sin_nombre', f'el bono con {con} no tiene nombre en ninguna página de la wiki',
                  integrantes=[X.nombre_pj[c] for c in b['m']])
        if len(b['v']) > 1:
            aparte.append({'tipo': 'bono_empatado', 'que': f"«{b['n'] or 'sin nombre'}», con {con}: {len(b['v'])} "
                           'versiones empatadas entre las páginas de la wiki (docs/AUDITORIA.md, sección 10)',
                           'datos': {'bono': b['n'], 'integrantes': [X.nombre_pj[c] for c in b['m']]}})
    claves = [v['clave'] for v in vs]
    filas_ideal = sorted({X.filas_ideal[f] for k in claves for f in X.AS[X.ideal['id']].get(k, [])})
    if not filas_ideal:
        falta(out, 'ctp_ideal', f"no está en la {X.ideal['nombre']}")
    # La guía de armado: su fila, con C.T.P., ISO-8 y obelisco. Una fila sin nada de lo que la guía completa no
    # está hecha; en una hecha, lo que falta no cuenta si la guía dice que no vale invertir en él («dont waste
    # gold» como ISO-8) o la Ideal CTP List lo pone en «Not worth».
    if armado is None or not any(armado.get(k) for k in ('ctp', 'iso', 'iso_x', 'ob', 'ob_x', 'adq', 'rank')):
        falta(out, 'armado_vacio', 'la guía de armado no tiene su fila' if armado is None else
              'su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se '
              'consigue', fuente=TIPOS['armado_vacio'][3] + (f"; la {X.ideal['nombre']} lo pone en "
                                                             + _y(f'«{f}»' for f in filas_ideal) if filas_ideal else ''))
    else:
        sin = [x for x, k in (('C.T.P.', 'ctp'), ('ISO-8', 'iso'), ('obelisco', 'ob')) if not armado.get(k) and not armado.get(k + '_x')]
        if sin and (armado.get('iso') == [NO_INVERTIR] or filas_ideal == [NO_VALE]):
            aparte.append({'tipo': 'armado_no_vale', 'que': f"la guía de armado no le da {_ni(sin)}, y "
                           + (f'dice «{NO_INVERTIR}» como ISO-8' if armado.get('iso') == [NO_INVERTIR] else
                              f"la {X.ideal['nombre']} lo pone en «{NO_VALE}»")})
        else:
            if 'C.T.P.' in sin:
                falta(out, 'ctp_guia', f"su fila en la guía de armado no trae ningún C.T.P.; la {X.ideal['nombre']} lo "
                      'pone en ' + _y(f'«{f}»' for f in filas_ideal), ideal=filas_ideal)
            if [x for x in sin if x != 'C.T.P.']:
                falta(out, 'armado_guia', f"su fila en la guía de armado no trae {_ni(x for x in sin if x != 'C.T.P.')}")
    if not any(k in X.AS[GENERAL] for k in claves):
        falta(out, 'lista_general', 'no está en la tier list General')


def chequear_variante(X, v, out):
    """Lo de cada variante."""
    p, u = v['p'], v['u']
    for k, nom in (('c', 'clase'), ('f', 'bando'), ('race', 'raza'), ('gender', 'género'), ('wba', 'habilidad de World Boss')):
        if not v[k]:
            falta(out, 'identidad', f'sin {nom}')
    if not v['ab']:
        falta(out, 'identidad', 'sin habilidades')
    sks = X.SK.get(p, [])
    chequear_skills(X, v, sks, out)
    chequear_lideres(X, v, sks, out)
    # Retrato e íconos: lo que data.js referencia tiene que estar publicado en datos.json.
    ret = X.IMG.get('portrait-' + (v['uid'] or v['cid']))
    if ret is None or ret not in X.pub:
        falta(out, 'imagen', 'su retrato no está en datos.json')
    for val in [v['c'], v['f'], v['race'], v['gender'], v['wba']] + list(v['ab']):
        ruta = X.IMG.get('icon-' + val)
        if ruta is None or ruta not in X.pub:
            falta(out, 'imagen', f'el ícono de «{val}» no está en datos.json', valor=val)
    if v['uid'] is None and p in X.art:
        ruta = X.IMG.get('art-' + p)
        if ruta is None or ruta not in X.pub:
            falta(out, 'imagen', 'el ícono de su artefacto no está en datos.json')
    # Rotación: la de thanosvibs para esta variante, o la de la guía de armado si su fila es de esta variante.
    def con_rotacion_guia(w):
        ga = X.GA.get(w['p'])
        return bool(ga and (ga.get('rot') or ga.get('rotc')))
    if not X.D['MFF_ROTACIONES'].get(p) and not con_rotacion_guia(v):
        otras = [w['uni'] or 'la base' for w in v['todas'] if X.D['MFF_ROTACIONES'].get(w['p'])]
        guia = [w['uni'] or 'la base' for w in v['todas'] if con_rotacion_guia(w)]
        falta(out, 'rotacion', 'ni thanosvibs ni la guía de armado le dan rotación',
              fuente=TIPOS['rotacion'][3] + ('; thanosvibs publica la de ' + _y(otras) if otras else '')
              + ('; la guía de armado tiene la de ' + _y(guia) if guia else ''))
    pf = X.D['MFF_PERFIL'].get(p)
    if not pf or not pf['esc']:
        falta(out, 'perfil', 'sin perfil de combate: no se sabe con qué pega')
    # El C.T.P. de su contexto en la guía de armado: lo que muestran las tarjetas de equipo de PvP y PvE. Sin
    # ningún C.T.P. en la fila del personaje, eso ya se dice en el personaje.
    armado = next((X.GA[w['p']] for w in v['todas'] if w['p'] in X.GA), None)
    for ctx, nom in (('pvp', 'PvP'), ('pve', 'PvE')):
        v['funcion_' + ctx] = X.funcion(v['clave'], ctx)
        if v['funcion_' + ctx] and armado and armado.get('ctp') and not any(x['k'] == ctx for x in armado['ctp']):
            falta(out, 'ctp_contexto', f'tiene función en {nom} y la guía de armado no le da el C.T.P. meta de {nom}',
                  contexto=ctx)
    if u is not None:
        if not u['cost']:
            falta(out, 'uniforme', 'sin costo')
        if not (u.get('up') or {}).get('material1'):
            falta(out, 'uniforme', 'sin materiales de mejora')
        if len(u.get('op') or []) != 5 or any(x not in X.retratos for x in u['op']):
            falta(out, 'uniforme', 'las opciones de uniforme no son cinco retratos del roster')


def chequear_skills(X, v, sks, out):
    TB, p = X.TB, v['p']
    hay = {sk['sl'] for sk in sks}
    esperadas = list(BASICAS) + (['Active Ult'] if v['t'] != 'T2' else []) + (['Striker Skill'] if v['t'] == 'T4' else []) \
        + (['Uniform Passive'] if v['uid'] else [])
    for sl in esperadas:
        if sl not in hay:
            por = {'Active Ult': ' (es Tier-3 o Trascendido)', 'Striker Skill': ' (es Tier-4)'}.get(sl, '')
            falta(out, 'skill_falta', f'{SLOT_ES[sl]}: la API de skills no la trae{por}', slot=sl)
    an = X.AN.get(p, {'fx': []})
    for si, ti, fi in an.get('sc', []):
        sk = sks[si]
        falta(out, 'sin_clasificar', f"{SLOT_ES[sk['sl']]}: «{TB['ab'][sk['st'][ti]['fx'][fi]['a']]['en']}»", slot=sk['sl'])
    for ie, d, obj, fuentes in an['fx']:
        if ie != X.otorga:
            continue
        for si, ti, fi in fuentes:
            sk = sks[si]
            dice = [f['s'] + (f" ({_num(f['d'])} s)" if f.get('d') is not None else '')
                    for k in X.ls_de_skill(p, sk) for f in X.SO[p][k].get('fx', [])]
            falta(out, 'otorga', f"{SLOT_ES[sk['sl']]} «{X.nombre_skill(sk)}»: otorga un efecto que la API no dice",
                  fuente=f"thanosvibs (Leads & Supports publica el mismo slot: {', '.join(dice)})" if dice else 'la wiki o foros',
                  slot=sk['sl'], skill=X.nombre_skill(sk))
    for sk in sks:
        nombre, ls = X.nombre_skill(sk), X.ls_de_skill(p, sk)
        if not any(st['fx'] for st in sk['st']):
            falta(out, 'skill_vacia', f"{SLOT_ES[sk['sl']]} «{nombre}»: la API la publica sin ningún efecto",
                  fuente='la wiki (el «Bonus» del uniforme) o foros' if sk['sl'] == 'Uniform Passive' else 'la wiki o foros',
                  slot=sk['sl'], skill=nombre)
        if re.fullmatch(r'Active \d', sk['sl']) and not sk['cd']:
            falta(out, 'recarga', f"{SLOT_ES[sk['sl']]} «{nombre}»: la API publica recarga {sk['cd']}",
                  slot=sk['sl'], skill=nombre)
        for ti, st in enumerate(sk['st']):
            if st.get('tg') in X.tgt_sin_nombre:
                r = [X.SO[p][k]['r'] for k in ls if X.SO[p][k].get('r')]
                falta(out, 'objetivo', f"{SLOT_ES[sk['sl']]} «{nombre}»: se aplica a «{TB['tgt'][st['tg']]['en']}»",
                      fuente=(f'thanosvibs (Leads & Supports restringe el mismo slot {A_RESTRICCION[r[0][0]]} {r[0][1]})'
                              if r else 'foros'),
                      slot=sk['sl'], skill=nombre, objetivo=TB['tgt'][st['tg']]['en'])
            for fi, f in enumerate(st['fx']):
                patron = TB['desc'][f['p']]['en']
                texto = _relleno(patron, f.get('v')).replace('<br>', ' ')
                if re.search(r'\$HERO(?:SUBTYPE|CLASS)', patron) and not f.get('g'):
                    falta(out, 'marcador', f"{SLOT_ES[sk['sl']]} «{nombre}»: «{texto}»", slot=sk['sl'], skill=nombre, texto=texto)
                if ('$TIME' in patron and f.get('d') is None) or ('$TICK' in patron and f.get('t') is None):
                    # Si Leads & Supports publica el mismo slot con una duración, o si lo que otorga trae la suya.
                    ls_d = sorted({X.SO[p][k]['d'] for k in ls if X.SO[p][k].get('d') is not None}
                                  | {g['d'] for k in ls for g in X.SO[p][k].get('fx', []) if g.get('d') is not None})
                    otorga_d = sorted({g['d'] for g in st['fx'][fi + 1:] + [g for s2 in sk['st'][ti + 1:] for g in s2['fx']]
                                       if g.get('d') is not None})
                    falta(out, 'duracion', f"{SLOT_ES[sk['sl']]} «{nombre}»: «{texto}»",
                          fuente=(f"thanosvibs (Leads & Supports publica el mismo slot con {_y(_num(x) + ' s' for x in ls_d)})"
                                  if ls_d else f"thanosvibs (lo que otorga dura {_y(_num(x) + ' s' for x in otorga_d)}, que "
                                  'podría ser la misma), la wiki o foros' if otorga_d else 'la wiki o foros'),
                          slot=sk['sl'], skill=nombre, texto=texto)
                if patron in CODIGOS:
                    cods = [f['v'][i] for i in CODIGOS[patron]]
                    falta(out, 'codigo', f"{SLOT_ES[sk['sl']]} «{nombre}», {TB['ab'][f['a']]['en']}: «{texto}»",
                          fuente=('thanosvibs (es el id de una habilidad de la API de skills)'
                                  if all(len(str(c)) == 3 for c in cods) else 'la wiki o foros'),
                          slot=sk['sl'], skill=nombre, etiqueta=TB['ab'][f['a']]['en'], codigos=cods, texto=texto)


def chequear_lideres(X, v, sks, out):
    p = v['p']
    e = X.SO.get(p, {})
    # Liderazgo: el de Leads & Supports o, si no lo publica, el que el build deriva de la Leader Skill de la API
    # (scripts/liderazgos.py). Falta cada slot que no se pudo derivar, con sus motivos (docs/AUDITORIA.md, sección 12).
    for x in X.sin_derivar.get(p, []):
        falta(out, 'liderazgo', f"{SLOT_LS[x['slot']]}: no se pudo derivar de la Leader Skill: "
              + '; '.join(motivo_txt(m, d) for m, d in x['motivos']),
              slot_ls=x['slot'], motivos=[m for m, _ in x['motivos']])
    # Soportes: lo que sus pasivas le dan al equipo (según el análisis) tiene que estar en Leads & Supports, en el
    # slot de la skill o con su nombre en otro slot (eso último lo marca el chequeo de nombres).
    dan = collections.defaultdict(set)
    for ie, d, obj, fuentes in X.AN.get(p, {'fx': []})['fx']:
        if d == 'q':
            for si, _, _ in fuentes:
                if sks[si]['sl'] in PASIVAS:
                    dan[sks[si]['sl']].add(X.CAT['efectos'][ie]['es'])
    nombres_ls = [x['n'] for k, x in e.items() if k not in LIDERAZGOS and isinstance(x, dict) and x.get('n')]
    for sk in sks:
        sl = sk['sl']
        if sl in dan and not any(k in e for k in SLOTS_DE_SKILL[sl]) \
                and not any(_nombre_igual(n, X.nombre_skill(sk)) for n in nombres_ls):
            falta(out, 'soporte', f"{SLOT_ES[sl]} «{X.nombre_skill(sk)}» le da al equipo "
                  + ', '.join(f'«{x}»' for x in sorted(dan[sl])) + ', y Leads & Supports no lo publica',
                  slot=sl, skill=X.nombre_skill(sk), da=sorted(dan[sl]))
    # Nombres: cada slot de Leads & Supports con nombre tiene que llevar el de la skill de su tipo.
    for k in [k for k in SLOT_LS if k in e]:
        x = e[k]
        if k not in SKILL_DE_SLOT or not x.get('n'):
            continue
        propia = next((s for s in sks if s['sl'] == SKILL_DE_SLOT[k]), None)
        if propia is not None and _nombre_igual(x['n'], X.nombre_skill(propia)):
            continue
        otra = next((s for s in sks if _nombre_igual(x['n'], X.nombre_skill(s))), None)
        que = f"{SLOT_LS[k]}: Leads & Supports la llama «{x['n']}», " + (
            f"que es su {SLOT_ES[otra['sl']]}" if otra else 'que no es ninguna de sus skills')
        if propia is not None:
            que += f"; su {SLOT_ES[propia['sl']]} se llama «{X.nombre_skill(propia)}»"
        falta(out, 'nombre_ls', que, slot_ls=k, nombre_ls=x['n'], skill=X.nombre_skill(propia) if propia else None,
              es_de=otra['sl'] if otra else None)


# ---------------------------------------------------------------------------
# Resultado, resumen e informe
# ---------------------------------------------------------------------------
def armar(X):
    """Por personaje (en orden alfabético): sus faltantes, lo que no cuenta (todo del personaje) y lo de cada
    variante."""
    res = []
    for pj in X.personajes:
        propios, aparte = [], []
        chequear_personaje(X, pj, propios, aparte)
        variantes = []
        for v in pj['vs']:
            fs = []
            chequear_variante(X, v, fs)
            variantes.append({'v': v, 'faltantes': fs})
        res.append({'ch': pj['ch'], 'faltantes': propios, 'aparte': aparte, 'variantes': variantes})
    res.sort(key=lambda r: (r['ch']['name'].casefold(), r['ch']['name']))
    return res


def resumen(res):
    por_tipo = {t: {'variantes': set(), 'personajes': set(), 'casos': 0} for t in TIPOS}
    for r in res:
        for f in r['faltantes']:
            c = por_tipo[f['tipo']]
            c['casos'] += 1
            c['personajes'].add(r['ch']['id'])
            c['variantes'].update(x['v']['p'] for x in r['variantes'])
        for x in r['variantes']:
            for f in x['faltantes']:
                c = por_tipo[f['tipo']]
                c['casos'] += 1
                c['personajes'].add(r['ch']['id'])
                c['variantes'].add(x['v']['p'])
    cuenta = {t: {'variantes': len(c['variantes']), 'personajes': len(c['personajes']), 'casos': c['casos']}
              for t, c in por_tipo.items()}
    orden = sorted((t for t in TIPOS if cuenta[t]['casos']),
                   key=lambda t: (-cuenta[t]['variantes'], -cuenta[t]['casos'], list(TIPOS).index(t)))
    return {'variantes': sum(len(r['variantes']) for r in res),
            'completas': sum(1 for r in res for x in r['variantes'] if not r['faltantes'] and not x['faltantes']),
            'personajes': len(res),
            'personajes_completos': sum(1 for r in res if not r['faltantes'] and not any(x['faltantes'] for x in r['variantes'])),
            'por_tipo': cuenta, 'orden': orden}


def _celda(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def _ancla(titulo):
    """El ancla que GitHub le da a un título de sección."""
    return re.sub(r'[^\w\- ]', '', titulo.lower()).replace(' ', '-')


def _quien(r, vs):
    """Cómo se nombra a un grupo de variantes del mismo personaje en una tabla."""
    if len(vs) == 1:
        return vs[0]['nombre']
    if len(vs) == len(r['variantes']):
        return f"{r['ch']['name']} (sus {len(vs)} variantes)"
    return f"{r['ch']['name']} ({', '.join(v['uni'] or 'base' for v in vs)})"


def _breve(fs):
    """Los faltantes de una variante, cortos: el rótulo de cada tipo y, si son de skills o de Leads & Supports,
    en cuáles."""
    por = collections.OrderedDict()
    for f in fs:
        d = f.get('datos') or {}
        donde = SLOT_ES.get(d.get('slot')) or SLOT_LS.get(d.get('slot_ls')) or d.get('valor') or \
            {'pvp': 'PvP', 'pve': 'PvE'}.get(d.get('contexto'))
        por.setdefault(f['tipo'], collections.Counter())
        if donde:
            por[f['tipo']][donde] += 1
    out = []
    for t, c in por.items():
        out.append(TIPOS[t][4] + (': ' + ', '.join(k + (f' ({n})' if n > 1 else '') for k, n in c.items()) if c else ''))
    return '; '.join(out)


def informe(X, res, R):
    ver = X.D['MFF_VERSION']
    s = ['# Completitud de los datos\n']
    s.append(f"Generado por `scripts/completitud.py` sobre `data.js` (juego {ver['juego']}, datos del {ver['generado']}, "
             f"formato {ver['formato']}) y `datos.json`.\n")
    s.append('Qué le falta a cada variante (un personaje con un uniforme) para tener la información que la app muestra y '
             'usa, y de dónde podría salir. Lo que dos fuentes dicen distinto está en `docs/AUDITORIA.md`; esto es lo que '
             'no está. Lo que no existe en el juego no es un faltante (un personaje sin artefacto, si ninguna fuente dice '
             'que tenga uno), y lo que una fuente dice a propósito va aparte.\n')
    for a in X.avisos:
        s.append(f'**Aviso:** {a}.\n')
    s.append('## Qué es «completo»\n')
    s.append('Una variante está completa si no le falta nada de esto. Lo del personaje (instinto, stats, artefacto, '
             'strikers, bonos, Ideal CTP List, guía de armado, tier list General) vale para todas sus variantes.\n')
    s.append('| Pieza | Qué se pide | Por qué es esperable que esté |')
    s.append('|---|---|---|')
    s += [f'| {t} | {_celda(q)} | {_celda(pq)} |' for _, t, q, pq in PIEZAS]
    s.append('')
    s.append('## Resumen\n')
    s.append(f"{R['completas']} de {R['variantes']} variantes completas ({round(100 * R['completas'] / R['variantes'])}%); "
             f"{R['personajes_completos']} de {R['personajes']} personajes con todas sus variantes completas.\n")
    s.append('Lo que falta, de lo que deja incompletas más variantes a lo que deja menos (lo que falta en el personaje '
             'cuenta en todas sus variantes):\n')
    s.append('| Faltante | Variantes | Personajes | Casos | De dónde podría salir |')
    s.append('|---|---|---|---|---|')
    for t in R['orden']:
        c = R['por_tipo'][t]
        s.append(f"| [{TIPOS[t][1]}](#{_ancla(TIPOS[t][1])}) | {c['variantes']} | {c['personajes']} | {c['casos']} | "
                 f"{_celda(TIPOS[t][3])} |")
    sin = [TIPOS[t][1] for t in TIPOS if not R['por_tipo'][t]['casos']]
    if sin:
        s.append('\nSin casos: ' + '; '.join(sin) + '.')
    s.append('')
    s += conocidos(X, res, R)
    s += no_cuenta(res)
    s.append('## Por tipo de faltante\n')
    s.append('Las variantes de un personaje con el mismo faltante van en una fila.\n')
    for t in TIPOS:
        filas = []
        for r in res:
            if TIPOS[t][2] == 'personaje':
                fs = [f for f in r['faltantes'] if f['tipo'] == t]
                if fs:
                    filas.append((_quien(r, [x['v'] for x in r['variantes']]), fs))
                continue
            grupos = collections.OrderedDict()
            for x in r['variantes']:
                fs = [f for f in x['faltantes'] if f['tipo'] == t]
                if fs:
                    clave = json.dumps([(f['que'], f['fuente']) for f in fs], ensure_ascii=False)
                    grupos.setdefault(clave, (fs, []))[1].append(x['v'])
            filas += [(_quien(r, vs), fs) for fs, vs in grupos.values()]
        if not filas:
            continue
        c = R['por_tipo'][t]
        nivel = TIPOS[t][2]
        s.append(f'### {TIPOS[t][1]}\n')
        s.append(f"{c['casos']} {'caso' if c['casos'] == 1 else 'casos'} en {c['personajes']} "
                 f"{'personaje' if c['personajes'] == 1 else 'personajes'}"
                 + (f" y {c['variantes']} {'variante' if c['variantes'] == 1 else 'variantes'}" if nivel == 'variante' else '')
                 + f'. {TIPOS[t][5]}\n')
        s.append(f"| {'Personaje' if nivel == 'personaje' else 'Variante'} | Qué falta | De dónde podría salir |")
        s.append('|---|---|---|')
        for quien, fs in filas:
            ques = collections.Counter(f['que'] for f in fs)
            fuentes = list(dict.fromkeys(f['fuente'] for f in fs))
            s.append(f"| {_celda(quien)} | {_celda('; '.join(q + (f' ({n} veces)' if n > 1 else '') for q, n in ques.items()))} "
                     f"| {_celda('; '.join(fuentes))} |")
        s.append('')
    s.append('## Por personaje\n')
    s.append('Los personajes con algún faltante, en orden alfabético: primero lo del personaje y después cada variante '
             'incompleta. El detalle está en las tablas de arriba.\n')
    for r in res:
        n = len(r['faltantes']) + sum(len(x['faltantes']) for x in r['variantes'])
        if not n:
            continue
        inc = sum(1 for x in r['variantes'] if r['faltantes'] or x['faltantes'])
        nv = len(r['variantes'])
        s.append(f"<details><summary>{r['ch']['name']}: {n} {'faltante' if n == 1 else 'faltantes'}, {inc} de {nv} "
                 f"{'variante incompleta' if nv == 1 else 'variantes incompletas'}</summary>\n")
        if r['faltantes']:
            s.append('- **Personaje:** ' + _breve(r['faltantes']))
        for x in r['variantes']:
            if x['faltantes']:
                s.append(f"- **{x['v']['uni'] or 'Base'}:** " + _breve(x['faltantes']))
        s.append('\n</details>\n')
    return '\n'.join(s)


def conocidos(X, res, R):
    """Cómo quedan, en este inventario, los problemas que ya se sabía que no cerraban."""
    def de_tipo(t, var=True):
        return [(r, x, f) for r in res for x in (r['variantes'] if var else [None])
                for f in (x['faltantes'] if var else r['faltantes']) if f['tipo'] == t]
    marc = de_tipo('marcador')
    lid = de_tipo('liderazgo')
    motivos = collections.Counter(m for _, _, f in lid for m in f['datos']['motivos'])
    stk = de_tipo('strikers', var=False)
    bon = de_tipo('bonos', var=False)
    solo_juego = [r['ch']['name'] for r, _, f in bon if f['que'].startswith('solo')]
    empates = {(a['datos']['bono'] or '', tuple(a['datos']['integrantes']))
               for r in res for a in r['aparte'] if a['tipo'] == 'bono_empatado'}
    nom = de_tipo('nombre_ls')
    s = ['### Lo que ya se sabía que no cierra\n']
    s.append(f"- **Marcadores sin resolver:** {len(marc)} efectos en {R['por_tipo']['marcador']['variantes']} variantes. "
             'docs/AUDITORIA.md (sección 8) los cuenta por id de la API, que se repite en los uniformes que comparten '
             'la skill.')
    s.append(f"- **Liderazgos:** Leads & Supports publica el de {len(X.con_lid)} variantes, y el build deriva el de "
             f"{len(X.derivados)} más de su Leader Skill ({sum(len(x) for x in X.derivados.values())} slots, con "
             '"src": "api"; docs/AUDITORIA.md, sección 12). '
             + (f"{len(lid)} slots de {R['por_tipo']['liderazgo']['variantes']} variantes no se pudieron derivar ("
                + '; '.join(f'{ROTULOS[m]}, {n}' for m, n in sorted(motivos.items(), key=lambda x: (-x[1], x[0])))
                + '; un slot puede tener más de un motivo).' if lid else 'Ninguno quedó sin derivar.'))
    s.append(f"- **Strikers:** {sum(1 for _, _, f in stk if 'no tiene la pestaña' in f['que'])} personajes sin la pestaña "
             f"Striker en la wiki y {sum(1 for _, _, f in stk if 'ninguna fila' in f['que'])} con la pestaña sin filas que "
             'se puedan leer.')
    s.append(f"- **Bonos de equipo por confirmar:** los que se vieron en capturas del juego y esperan confirmación no están "
             f"en data.js, así que este informe no los ve. Sí ve {sum(1 for _, _, f in bon if f['que'].startswith('no tiene'))} "
             f"personajes sin ningún bono y {len(solo_juego)} solo con los del juego"
             + (f" ({_y(solo_juego)})" if solo_juego else '') + f". Los {len(empates)} bonos con versiones empatadas entre "
             'páginas de la wiki son diferencias entre fuentes (docs/AUDITORIA.md, sección 10): van en «Lo que no cuenta».')
    s.append(f"- **Nombres de Leads & Supports que no son los de la API de skills:** {len(nom)} en "
             f"{R['por_tipo']['nombre_ls']['variantes']} variantes; {sum(1 for _, _, f in nom if f['datos']['es_de'])} con el "
             'nombre de otra skill de la variante, entre ellos Jeff the Land Shark y Polaris — Uncanny X-Men.')
    s.append('')
    return s


def no_cuenta(res):
    """Lo que no es un faltante: no existe en el juego, o la fuente lo dice a propósito."""
    def personajes(tipo):
        return [r['ch']['name'] for r in res if any(a['tipo'] == tipo for a in r['aparte'])]
    vs = [x['v'] for r in res for x in r['variantes']]
    empates = {(a['datos']['bono'] or '', tuple(a['datos']['integrantes']))
               for r in res for a in r['aparte'] if a['tipo'] == 'bono_empatado'}
    s = ['### Lo que no cuenta como faltante\n']
    s.append(f"- **Sin artefacto:** {len(personajes('sin_artefacto'))} personajes, y ninguna fuente dice que tengan "
             'uno: ' + ', '.join(personajes('sin_artefacto')) + '.')
    s.append(f"- **Guía de armado sin C.T.P., ISO-8 u obelisco para quien no vale la pena armar:** "
             f"{len(personajes('armado_no_vale'))} personajes: la guía dice «{NO_INVERTIR}» como ISO-8 o la "
             f"Ideal CTP List los pone en «{NO_VALE}».")
    s.append(f"- **Bonos con versiones empatadas entre páginas de la wiki:** {len(empates)} (docs/AUDITORIA.md, sección 10). "
             'La app muestra todas las versiones.')
    s.append(f"- **Función en el contexto:** {sum(1 for v in vs if v['funcion_pvp'])} variantes tienen función en PvP y "
             f"{sum(1 for v in vs if v['funcion_pve'])} en PvE (están en las tier lists de ese contexto). Las demás no la "
             'tienen: la lista lo dice al no ponerlas.')
    s.append('- **Lo que este chequeo no mira:** las diferencias entre fuentes (docs/AUDITORIA.md), las traducciones, cómo '
             'se consigue cada artefacto, los stats de cada uniforme (data.js trae solo los del personaje) y el Set '
             'Striker, que la app no tiene.')
    s.append('')
    return s


def a_json(X, res, R):
    ver = X.D['MFF_VERSION']
    return {
        'datos': {'juego': ver['juego'], 'generado': ver['generado'], 'formato': ver['formato']},
        'avisos': X.avisos,
        'definicion': [{'pieza': k, 'titulo': t, 'que': q, 'por_que': pq} for k, t, q, pq in PIEZAS],
        'tipos': {t: {'pieza': x[0], 'titulo': x[1], 'nivel': x[2], 'fuente': x[3], 'por_que': x[5]}
                  for t, x in TIPOS.items()},
        'resumen': {'variantes': R['variantes'], 'completas': R['completas'], 'personajes': R['personajes'],
                    'personajes_completos': R['personajes_completos'],
                    'por_tipo': {t: R['por_tipo'][t] for t in R['orden']}},
        'personajes': [{
            'id': r['ch']['id'], 'nombre': r['ch']['name'], 'faltantes': r['faltantes'], 'no_cuenta': r['aparte'],
            'variantes': [{'retrato': x['v']['p'], 'clave': x['v']['clave'], 'uniforme': x['v']['uni'],
                           'completa': not r['faltantes'] and not x['faltantes'],
                           'funcion': {'pvp': x['v']['funcion_pvp'], 'pve': x['v']['funcion_pve']},
                           'faltantes': x['faltantes']} for x in r['variantes']],
        } for r in res],
    }


def main():
    ap = argparse.ArgumentParser(description='Qué le falta a cada variante: escribe docs/COMPLETITUD.md.')
    ap.add_argument('--json', metavar='RUTA', help='escribe también el inventario en JSON')
    a = ap.parse_args()
    D = cargar_datajs(os.path.join(_RAIZ, 'data.js'))
    with open(os.path.join(_RAIZ, 'datos.json'), encoding='utf-8') as f:
        publicadas = {r for r, _ in json.load(f)['imagenes']}
    X = Datos(D, publicadas)
    res = armar(X)
    R = resumen(res)
    with open(os.path.join(_RAIZ, SALIDA), 'w', encoding='utf-8', newline='\n') as f:
        f.write(informe(X, res, R))
    if a.json:
        with open(a.json, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(a_json(X, res, R), f, ensure_ascii=False, indent=1)
            f.write('\n')
    print(f"completitud: {R['completas']} de {R['variantes']} variantes completas | "
          + ' | '.join(f"{TIPOS[t][4]} {R['por_tipo'][t]['variantes']}" for t in R['orden'][:4]) + f' | {SALIDA}'
          + ''.join(f' | AVISO: {x}' for x in X.avisos))


if __name__ == '__main__':
    main()
