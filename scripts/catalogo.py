#!/usr/bin/env python3
"""Catálogo de efectos (scripts/contenido/catalogo.json; docs/MODELO.md, etapas 2 y 3).

thanosvibs publica el mismo efecto de dos lados que no se cruzan: la API de skills lo trae como
una etiqueta tipada ("ALL BASIC ATTACKS INCREASE") y Leads & Supports como un stat ("All Basic
Attacks"). En el catálogo, las dos apuntan a efectos únicos, y cada efecto dice qué es (su
grupo), a quién le sirve y cómo se lee en PvE y en PvP, con su certeza y su fuente.

Acá se valida contra los datos de la sincronización:
- El catálogo tiene que ser coherente: cada efecto en un grupo que existe, cada etiqueta y cada
  stat apuntando a efectos que existen, las fuentes citadas definidas en contenido/guia.json.
  Si no, se corta el build: es un error del contenido curado.
- Cada etiqueta de los datos (y cada patrón, en las que se clasifican por patrón) y cada stat
  (de Leads & Supports y de los bonos de equipo) tienen que estar clasificados. Uno nuevo que no
  está se avisa y va a la auditoría (sección 9), sin cortar la actualización semanal, igual que un
  marcador o una traducción que falta.

A quién le sirve: cada efecto tiene su regla (sirve), la de sus skills, que evalúa el build
(modelo.le_sirve, el «No le sirve» del análisis). Cada stat de liderazgo, soporte o bono de equipo
tiene la suya, que evalúa la app (sinergia, combinaciones, índice): casi siempre es la de su efecto;
las velocidades, las resistencias y el efecto de los debuffs tienen otra (reglas de Ezequiel).

Si se acumula: cada stat de liderazgo, soporte o bono de equipo dice qué pasa cuando a un integrante le llega de dos
fuentes (acumula, Ezequiel, 5 de octubre de 2026): las estadísticas se suman (true); las habilidades (anti-mermas,
inmunidades, barrera, escudos, revivir, invocar...) cuentan una vez, la de mayor valor (false). Y su tope, si la guía le
pone uno (tope: las claves de los topes de contenido/guia.json que le corresponden). Todos dicen si se acumulan, y cada
tope de la guía lo usa algún stat; si no, se corta el build.

Y la tabla de valor de los equipos (scripts/contenido/valor_equipos.json): cada stat que pesa o que cuenta como
anti-mermas tiene que estar en el catálogo (con su regla de «le sirve»), y cada modo de juego tiene que tener la
fila de su tipo. Si no, se corta el build.

También el glosario de skills del juego (scripts/contenido/glosario.json), en inglés y en coreano:
cada término con lo que dice, lo que el inglés traduce distinto del coreano y los efectos del
catálogo a los que corresponde. Un término que nombra un efecto, un error que se repite o un
C.T.P. que no existen corta el build.

Escribe docs/CATALOGO.md (el catálogo entero y el glosario, para leerlos y revisarlos) y
work/catalogo.json (lo que falta clasificar, para auditar.py)."""
import collections, datetime, json, os, sys

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)
from version_juego import ultima

RUTA = os.path.join(_DIR, 'contenido', 'catalogo.json')
RUTA_GLOSARIO = os.path.join(_DIR, 'contenido', 'glosario.json')
RUTA_VALOR = os.path.join(_DIR, 'contenido', 'valor_equipos.json')
# La fuente de cada idioma del glosario: un término sin la captura de un idioma no la cita.
CAPTURA = {'en': 'juego-glosario', 'ko': 'juego-glosario-ko'}
# De qué opción de un C.T.P. sale cada efecto que da (la ficha del C.T.P. en el juego): la opción fija (고정 옵션,
# «Locked Option»), que tienen el C.T.P. de 6★ y los reforjados (Mighty y Brilliant), o una opción de reforjado (재련
# 옵션, «Reforge Option»), que solo tienen los reforjados.
OPCIONES_CTP = {'fija': 'opción fija', 'reforjado': 'opción de reforjado'}
SLOTS_SOPORTE = ('leader', 'leader2', 'passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact')
# Las reglas de «le sirve» que la app sabe evaluar en un liderazgo, un soporte o un bono de equipo: las que
# miran el perfil de combate de quien lo recibe (app.js, iniciarDatos). Las demás (aplica_debuffs, invoca...)
# miran sus skills, y solo las evalúa el build, para el análisis (modelo.le_sirve).
REGLAS_SOPORTE = ('todos', 'nadie', 'escala:', 'elemento:', 'tipo:', 'resistencia:')
EFECTOS_ARTEFACTO = ('effect3', 'effect4', 'effect5', 'effect6')


def cargar(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


# -- coherencia ------------------------------------------------------------------
def validar(cat, guia):
    """Lista de problemas del contenido curado (vacía si está bien). guia: contenido/guia.json (sus fuentes, que cita el
    catálogo, y sus topes, que nombran los stats de soporte)."""
    mal = []
    fuentes = guia['fuentes']
    con_tope = {k for it in guia['topes']['items'] if it['tope'] is not None for k in it['stats']}
    ids_grupo = [g['id'] for g in cat['grupos']]
    ids_efecto = [e['id'] for e in cat['efectos']]
    for nombre, ids in (('grupo', ids_grupo), ('efecto', ids_efecto)):
        mal += [f'{nombre} repetido: {i}' for i, n in collections.Counter(ids).items() if n > 1]

    def texto(x, donde):
        if not (isinstance(x, dict) and set(x) == {'es', 'en'} and all(isinstance(x[k], str) and x[k] for k in x)):
            mal.append(f'{donde}: tiene que ser {{"es": ..., "en": ...}} con los dos textos')

    def lectura(x, donde):
        if not isinstance(x, dict) or not {'es', 'en', 'certeza'} <= set(x) or set(x) - {'es', 'en', 'certeza', 'fuente'}:
            mal.append(f'{donde}: una lectura lleva es, en, certeza y, si cita, fuente')
            return
        texto({'es': x['es'], 'en': x['en']}, donde)
        if x['certeza'] not in cat['certeza']:
            mal.append(f"{donde}: certeza desconocida {x['certeza']!r}")
        if x['certeza'] == 'comprobado' and not x.get('fuente'):
            mal.append(f'{donde}: «comprobado» sin fuente')
        mal.extend(f'{donde}: fuente sin definir en contenido/guia.json: {k}' for k in x.get('fuente', []) if k not in fuentes)

    def condicion(x, donde):
        claves = set(x) & {'contra', 'varia', 'dura'}
        if len(claves) != 1:
            mal.append(f'{donde}: una condición es una de contra, varia o dura')
            return
        if 'contra' in x:
            if x['contra'] not in cat['contra']:
                mal.append(f"{donde}: contra desconocido {x['contra']!r}")
            if set(x) - {'contra', 'valor', 'marcador'} or x.get('marcador', True) is not True:
                mal.append(f'{donde}: contra lleva, como mucho, valor o marcador (true)')
        else:
            k = claves.pop()
            if set(x) != {k}:
                mal.append(f'{donde}: {k} va solo')
            texto(x[k], f'{donde} ({k})')

    def mapeo(x, donde, de_skill):
        """Una etiqueta de skill lleva para (a qué lado va); un stat de Leads & Supports, sirve (a quién le sirve), acumula
        (si se suma cuando le llega a alguien de dos fuentes) y, si la guía le pone uno, tope."""
        propias = ('para',) if de_skill else ('sirve', 'acumula')
        claves = {'efectos', 'condicion', 'nota', *propias} | (set() if de_skill else {'tope'})
        if set(x) - claves or 'efectos' not in x or any(k not in x for k in propias):
            mal.append(f"{donde}: lleva {', '.join(sorted(claves))} ({', '.join(propias)} y efectos obligatorios)")
            return
        if de_skill and x['para'] not in cat['para']:
            mal.append(f"{donde}: para desconocido {x['para']!r}")
        if not de_skill:
            if x['sirve'] not in cat['sirve']:
                mal.append(f"{donde}: sirve desconocido {x['sirve']!r}")
            elif not any(x['sirve'] == r or (r.endswith(':') and x['sirve'].startswith(r)) for r in REGLAS_SOPORTE):
                mal.append(f"{donde}: la app no sabe evaluar en un liderazgo, soporte o bono la regla {x['sirve']!r} "
                           f"(sabe {', '.join(REGLAS_SOPORTE)})")
            if not isinstance(x['acumula'], bool):
                mal.append(f'{donde}: acumula es true (se suma) o false (cuenta una vez, la de mayor valor)')
            if 'tope' in x:
                t = x['tope']
                if not (isinstance(t, list) and t and all(isinstance(k, str) for k in t) and len(set(t)) == len(t)):
                    mal.append(f'{donde}: tope es una lista de claves de los topes de contenido/guia.json, sin repetir')
                else:
                    mal.extend(f'{donde}: {k!r} no es un stat con tope en contenido/guia.json' for k in t if k not in con_tope)
        if not x['efectos']:
            mal.append(f'{donde}: sin efectos')
        mal.extend(f'{donde}: efecto desconocido {e!r}' for e in x['efectos'] if e not in ids_efecto)
        if 'condicion' in x:
            condicion(x['condicion'], donde)
        if 'nota' in x:
            texto(x['nota'], f'{donde} (nota)')

    for k in ('certeza', 'para', 'sirve', 'contra'):
        for clave, v in cat[k].items():
            texto(v, f'{k}.{clave}')
    for g in cat['grupos']:
        texto(g['que'], f"grupo {g['id']} (que)")
        lectura(g['pve'], f"grupo {g['id']} (pve)")
        lectura(g['pvp'], f"grupo {g['id']} (pvp)")
    for e in cat['efectos']:
        d = f"efecto {e['id']}"
        if e['grupo'] not in ids_grupo:
            mal.append(f"{d}: grupo desconocido {e['grupo']!r}")
        if e['sirve'] not in cat['sirve']:
            mal.append(f"{d}: sirve desconocido {e['sirve']!r}")
        for k in ('pve', 'pvp'):
            if k in e:
                lectura(e[k], f'{d} ({k})')
        if 'nota' in e:
            texto(e['nota'], f'{d} (nota)')
    for label, x in cat['skills'].items():
        d = f'etiqueta {label!r}'
        if 'por_patron' in x:
            if set(x) - {'por_patron', 'nota'} or not x['por_patron']:
                mal.append(f'{d}: por_patron va solo (con nota, si hace falta)')
            for pat, y in x['por_patron'].items():
                mapeo(y, f'{d}, patrón {pat!r}', True)
            if 'nota' in x:
                texto(x['nota'], f'{d} (nota)')
        else:
            mapeo(x, d, True)
    for stat, x in cat['soporte'].items():
        mapeo(x, f'stat {stat!r}', False)
    con_stat = {k for x in cat['soporte'].values() if isinstance(x.get('tope'), list) for k in x['tope']}
    mal += [f'tope de contenido/guia.json que ningún stat de soporte nombra: {k}' for k in sorted(con_tope - con_stat)]
    usados = {e for x in cat['skills'].values() for y in (x['por_patron'].values() if 'por_patron' in x else [x])
              for e in y.get('efectos', [])} | {e for x in cat['soporte'].values() for e in x.get('efectos', [])}
    mal += [f'efecto {i} sin ninguna etiqueta ni stat que apunte a él' for i in ids_efecto if i not in usados]
    return mal


def validar_valor(valor, cat, modos, roles):
    """Lista de problemas de la tabla de valor de los equipos (vacía si está bien). modos: los de
    contenido/modos.json; roles: contenido/roles_listas.json (las tier lists de cada contexto)."""
    mal = []
    if set(valor) != {'nota', 'propuesta', 'anti_mermas', 'contextos'}:
        mal.append('valor: lleva nota, propuesta, anti_mermas y contextos')
        return mal
    if not (isinstance(valor['nota'], dict) and set(valor['nota']) == {'es', 'en'} and all(valor['nota'].values())):
        mal.append('valor: la nota tiene que ser {"es": ..., "en": ...} con los dos textos')
    if not isinstance(valor['propuesta'], bool):
        mal.append('valor: propuesta es true o false')

    def stat(st, donde):
        if st not in cat['soporte']:
            mal.append(f'valor: {donde}: {st!r} no es un stat del catálogo de efectos (soporte), así que no tiene regla de «le sirve»')

    def numero(x, donde, hasta=None):
        if isinstance(x, bool) or not isinstance(x, (int, float)) or x < 0 or (hasta is not None and x > hasta):
            mal.append(f'valor: {donde} tiene que ser un número de 0' + (f' a {hasta}' if hasta is not None else ' o más') + f', no {x!r}')

    if not valor['anti_mermas']:
        mal.append('valor: anti_mermas vacío')
    for st in valor['anti_mermas']:
        stat(st, 'anti_mermas')
    contextos = valor['contextos']
    for ctx, c in contextos.items():
        d = f'contexto {ctx}'
        if set(c) != {'requisito', 'liderazgo', 'condicional', 'dps', 'soporte', 'bono', 'strikers'}:
            mal.append(f'valor: {d}: lleva requisito, liderazgo, condicional, dps, soporte, bono y strikers')
            continue
        if c['requisito'] not in (None, 'anti_mermas'):
            mal.append(f"valor: {d}: requisito desconocido {c['requisito']!r} (la app sabe null y anti_mermas)")
        if c['strikers'] != 'desempate':
            mal.append(f"valor: {d}: strikers desconocido {c['strikers']!r} (los strikers desempatan: desempate)")
        vistos = set()
        for x in c['liderazgo']:
            if set(x) != {'stat', 'peso'}:
                mal.append(f'valor: {d}: cada stat del liderazgo lleva stat y peso')
                continue
            stat(x['stat'], f'{d}, liderazgo')
            numero(x['peso'], f"{d}, peso de {x['stat']}")
            if x['stat'] in vistos:
                mal.append(f"valor: {d}: {x['stat']!r} repetido en el liderazgo")
            vistos.add(x['stat'])
        numero(c['condicional'], f'{d}, condicional', 1)
        for k in ('dps', 'soporte', 'bono'):
            numero(c[k], f'{d}, {k}')
        if ctx not in roles:
            mal.append(f'valor: {d}: no tiene tier lists en contenido/roles_listas.json (de ahí salen sus DPS)')
    mal += [f"valor: el modo {m['id']} es de tipo {m['tipo']!r} y la tabla no tiene esa fila" for m in modos if m['tipo'] not in contextos]
    mal += [f'valor: falta la fila {ctx}, que usan los órdenes de las combinaciones' for ctx in roles if ctx not in contextos and ctx != 'nota']
    return mal


# -- uso en los datos --------------------------------------------------------------
def validar_glosario(glos, cat, fuentes, ctps):
    """Lista de problemas del glosario del juego (vacía si está bien): cada término con sus tres
    nombres y lo que dice; lo que difiere entre el inglés y el coreano, solo con las dos capturas;
    los efectos del catálogo, los errores que se repiten y los C.T.P. que nombra, existentes."""
    mal = []
    ids_efecto = {e['id'] for e in cat['efectos']}
    ids_error = [e['id'] for e in glos['errores']]
    ids = [x['id'] for x in glos['terminos']]
    mal += [f'glosario: id repetido: {i}' for i, n in collections.Counter(ids + ids_error).items() if n > 1]

    def texto(x, donde):
        if not (isinstance(x, dict) and set(x) == {'es', 'en'} and all(isinstance(x[k], str) and x[k] for k in x)):
            mal.append(f'{donde}: tiene que ser {{"es": ..., "en": ...}} con los dos textos')

    for e in glos['errores']:
        if set(e) != {'id', 'titulo', 'texto'}:
            mal.append(f"glosario: el error {e.get('id')} lleva id, titulo y texto")
            continue
        texto(e['titulo'], f"glosario: error {e['id']}, titulo")
        texto(e['texto'], f"glosario: error {e['id']}, texto")
        if not any(x.get('error') == e['id'] for x in glos['terminos']):
            mal.append(f"glosario: ningún término tiene el error {e['id']}")
    for x in glos['terminos']:
        donde = f"glosario: {x.get('id')}"
        if set(x) - {'id', 'en', 'ko', 'es', 'que', 'difiere', 'error', 'efectos', 'ctp', 'nota', 'falta', 'fuente'} \
                or not {'id', 'en', 'ko', 'es', 'que', 'efectos', 'fuente'} <= set(x):
            mal.append(f'{donde}: lleva id, en, ko, es, que, efectos y fuente, y puede llevar difiere, error, ctp, nota y falta')
            continue
        mal += [f'{donde}: falta el nombre {k}' for k in ('en', 'ko', 'es') if not (isinstance(x[k], str) and x[k])]
        texto(x['que'], donde + ', que')
        for k in ('difiere', 'nota'):
            if k in x:
                texto(x[k], f'{donde}, {k}')
        if 'error' in x and x['error'] not in ids_error:
            mal.append(f"{donde}: error que no existe: {x['error']}")
        if 'error' in x and 'difiere' not in x:
            mal.append(f'{donde}: tiene un error que se repite y no dice qué difiere en él')
        mal += [f'{donde}: efecto que el catálogo no tiene: {e}' for e in x['efectos'] if e not in ids_efecto]
        for c in x.get('ctp', []):
            if set(c) != {'id', 'opcion'} or c['id'] not in ctps or c['opcion'] not in OPCIONES_CTP:
                mal.append(f'{donde}: C.T.P. mal nombrado (lleva id y opcion: {", ".join(OPCIONES_CTP)}): {c}')
        if x.get('ctp') and 'tv-ctps' not in x['fuente']:
            mal.append(f'{donde}: nombra C.T.P.s sin citar tv-ctps')
        falta = x.get('falta')
        if falta is not None and falta not in CAPTURA:
            mal.append(f'{donde}: falta tiene que ser en o ko')
        for idioma, f in CAPTURA.items():
            if (falta == idioma) == (f in x['fuente']):
                mal.append(f'{donde}: ' + (f'sin la captura en {idioma}, no puede citar {f}' if falta == idioma
                                           else f'tiene que citar {f}'))
        if falta and 'difiere' in x:
            mal.append(f'{donde}: con un solo idioma no hay con qué comparar')
        mal += [f'{donde}: fuente sin definir en contenido/guia.json: {k}' for k in x['fuente'] if k not in fuentes]
    return mal


def usos(sp, su, bonos):
    """Retratos que usan cada etiqueta, cada patrón de cada etiqueta y cada stat de Leads & Supports, y bonos de
    equipo que traen cada stat (bonos: los de work/fuentes.json, con una o más versiones de sus stats)."""
    AB = [x['en'] for x in sp['tablas']['ab']]
    DESC = [x['en'] for x in sp['tablas']['desc']]
    etiqueta, patron = collections.defaultdict(set), collections.defaultdict(lambda: collections.defaultdict(set))
    for p, sks in sp['skills'].items():
        for sk in sks:
            for st in sk.get('st') or []:
                for f in st.get('fx') or []:
                    etiqueta[AB[f['a']]].add(p)
                    patron[AB[f['a']]][DESC[f['p']]].add(p)
    stat = collections.defaultdict(set)
    for r in su:
        for slot in SLOTS_SOPORTE:
            x = r.get(slot)
            if not x:
                continue
            for e in [e for k in ('effect',) + EFECTOS_ARTEFACTO for e in x.get(k) or []]:
                stat[e[0]].update([r['portrait']] + r['sameas'])
    bono = collections.defaultdict(set)
    for b in bonos:
        for version in b['v']:
            for st in version:
                bono[st[0]].add(b['n'])
    # Diccionarios comunes: consultar algo que los datos no traen no lo agrega.
    return {'etiqueta': dict(etiqueta), 'patron': {l: dict(ps) for l, ps in patron.items()}, 'stat': dict(stat),
            'bono': dict(bono)}


def cobertura(cat, U):
    """Lo de los datos que el catálogo no clasifica, y lo del catálogo que los datos ya no traen. Los stats son los
    de Leads & Supports y los de los bonos de equipo."""
    S, SO = cat['skills'], cat['soporte']
    stats = set(U['stat']) | set(U['bono'])
    falta = {'etiquetas': sorted(l for l in U['etiqueta'] if l not in S),
             'patrones': sorted((l, p) for l in U['patron'] if 'por_patron' in S.get(l, {})
                                for p in U['patron'][l] if p not in S[l]['por_patron']),
             'stats': sorted(s for s in stats if s not in SO)}
    sobra = {'etiquetas': sorted(l for l in S if l not in U['etiqueta']),
             'patrones': sorted((l, p) for l, x in S.items() if 'por_patron' in x and l in U['patron']
                                for p in x['por_patron'] if p not in U['patron'][l]),
             'stats': sorted(s for s in SO if s not in stats)}
    return falta, sobra


# -- documento ---------------------------------------------------------------------
def md(s):
    """Texto de la fuente dentro de código en línea, sin romperlo."""
    return '`' + s.replace('`', "'") + '`'


def retratos(n):
    return f"{n} retrato{'' if n == 1 else 's'}"


def quienes_dan(n, nb):
    """Cuántos retratos (Leads & Supports) y cuántos bonos de equipo dan un stat."""
    partes = [retratos(n)] if n or not nb else []
    if nb:
        partes.append(f"{nb} bono{'' if nb == 1 else 's'} de equipo")
    return ', '.join(partes)


def minuscula(s):
    return s[0].lower() + s[1:]


def fuente_md(f):
    """Una fuente de contenido/guia.json en Markdown: con su enlace, o solo su nombre si no tiene
    dirección (la guía dentro del juego)."""
    return f"[{f['nombre']}]({f['url']})" if 'url' in f else f['nombre']


def documento(cat, U, guia, version, falta, glos, ctps):
    hoy = datetime.date.today().isoformat()
    fuentes = guia['fuentes']
    # Los topes de la guía, por clave de stat: (tope, base o None) y su nombre.
    topes = {k: (it['tope'], it.get('base')) for it in guia['topes']['items'] if it['tope'] is not None for k in it['stats']}

    def tope(x):
        """El tope de un stat de soporte, como lo escribe el documento: «Prob. de crítico 75%», con su base si tiene."""
        return ', '.join(f"{guia['stats'][k]['es']} {topes[k][0]}%" + (f' (desde {topes[k][1]}%)' if topes[k][1] else '')
                         for k in x.get('tope', []))

    def acumula(x):
        return 'se acumula' if x['acumula'] else 'cuenta una vez (la de mayor valor)'

    def cita(L):
        f = ', '.join(fuente_md(fuentes[k]) for k in L.get('fuente', []))
        return f"{L['es']} [{L['certeza'].capitalize()}]" + (f' ({f})' if f else '')

    def cond(c):
        if 'contra' in c:
            t = cat['contra'][c['contra']]['es']
            if 'valor' in c:
                t += f": {c['valor']}"
            if c.get('marcador'):
                t += ' (cada skill dice cuál)'
            return t
        if 'varia' in c:
            return 'varía: ' + c['varia']['es']
        return 'dura ' + c['dura']['es']

    # Quién apunta a cada efecto: etiquetas (con su patrón, en las que se clasifican por patrón)
    # y stats, cada uno con cuántos retratos lo usan, su condición y su nota.
    de_skill, de_stat, lados = collections.defaultdict(list), collections.defaultdict(list), collections.defaultdict(set)
    for label, x in cat['skills'].items():
        filas = [(p, y) for p, y in x['por_patron'].items()] if 'por_patron' in x else [(None, x)]
        for pat, y in filas:
            n = len(U['patron'].get(label, {}).get(pat, ())) if pat else len(U['etiqueta'].get(label, ()))
            extra = ([cond(y['condicion'])] if 'condicion' in y else []) + (['Nota: ' + x['nota']['es']] if 'nota' in x else [])
            for e in y['efectos']:
                de_skill[e].append((n, label, pat, y['para'], extra))
                lados[e].add(y['para'])
    regla_de = {e['id']: e['sirve'] for e in cat['efectos']}
    for stat, x in cat['soporte'].items():
        extra = ([cond(x['condicion'])] if 'condicion' in x else []) + (['Nota: ' + x['nota']['es']] if 'nota' in x else [])
        for e in x['efectos']:
            # La regla del stat, cuando no es la de su efecto (las velocidades, las resistencias...); si se acumula y su tope.
            sirve = ['le sirve: ' + minuscula(cat['sirve'][x['sirve']]['es'])] if x['sirve'] != regla_de[e] else []
            suma = [acumula(x)] + (['tope: ' + tope(x)] if 'tope' in x else [])
            de_stat[e].append((len(U['stat'].get(stat, ())), len(U['bono'].get(stat, ())), stat, sirve + suma + extra))
    LADO = {frozenset({'propio'}): 'a su lado', frozenset({'rival'}): 'al rival',
            frozenset({'propio', 'rival'}): 'a su lado o al rival, según la etiqueta'}

    n_falta = sum(len(v) for v in falta.values())
    s = ['# Catálogo de efectos\n',
         f'Generado por `scripts/catalogo.py` el {hoy}, sobre los datos del juego {version}, desde '
         '`scripts/contenido/catalogo.json` (contenido curado: se edita ahí, no acá).\n',
         'thanosvibs publica el mismo efecto de dos lados que no se cruzan: las skills lo traen como una '
         'etiqueta (`ALL BASIC ATTACKS INCREASE`) y Leads & Supports como un stat (`All Basic Attacks`). '
         'Acá los dos apuntan al mismo efecto, y cada efecto dice qué es, a quién le sirve y cómo se lee en '
         'PvE y en PvP. Cuándo se activa y a quién le llega no es del efecto sino de cada skill o soporte '
         '(su activación, su objetivo, su restricción): eso lo muestra la ficha.\n',
         '## Cómo se lee\n',
         '- **Se aplica:** a su lado (él o los aliados que diga el objetivo de la skill) o al rival.',
         '- **Le sirve:** a quién le aporta algo en sus skills, según con qué pega cada variante (docs/MODELO.md, perfil de '
         'combate). Cada stat de liderazgo, soporte o bono de equipo tiene su propia regla, casi siempre la misma: '
         'cuando no, se dice al lado del stat.',
         '- **PvE / PvP:** la lectura de cada modo. Si el efecto no trae una propia, vale la de su grupo.',
         '- **Certeza:**']
    s += [f"  - [{k.capitalize()}] {v['es']}" for k, v in cat['certeza'].items()]
    s += ['- **Skills:** las etiquetas que apuntan al efecto, de la más usada a la menos, con cuántos retratos la usan.',
          '- **Leads & Supports y bonos de equipo:** los stats que apuntan al efecto, con cuántos retratos y cuántos bonos '
          'los dan, si se acumulan y su tope (ver *Qué se acumula y los topes*, al final).\n',
          f"{len(cat['grupos'])} grupos, {len(cat['efectos'])} efectos, {len(cat['skills'])} etiquetas de skills y "
          f"{len(cat['soporte'])} stats de Leads & Supports y de bonos de equipo. "
          + ('Todo lo que traen los datos está clasificado.\n' if not n_falta else
             f'**Sin clasificar: {n_falta}** (docs/AUDITORIA.md, sección 9).\n')]
    for g in cat['grupos']:
        s.append(f"## {g['es']}\n")
        s.append(g['que']['es'] + '\n')
        s.append(f"- **PvE:** {cita(g['pve'])}")
        s.append(f"- **PvP:** {cita(g['pvp'])}\n")
        for e in (e for e in cat['efectos'] if e['grupo'] == g['id']):
            s.append(f"### {e['es']}\n")
            lado = LADO[frozenset(lados[e['id']])] if lados[e['id']] else 'a su lado'
            s.append(f"`{e['id']}` · {e['en']} · Se aplica {lado} · Le sirve: {minuscula(cat['sirve'][e['sirve']]['es'])}.\n")
            for k, nom in (('pve', 'PvE'), ('pvp', 'PvP')):
                if k in e:
                    s.append(f'- **{nom}:** {cita(e[k])}')
            if 'nota' in e:
                s.append(f"- **Nota:** {e['nota']['es']}")
            mixto = len(lados[e['id']]) > 1
            if de_skill[e['id']]:
                s.append('- **Skills:**')
                for n, label, pat, para, extra in sorted(de_skill[e['id']], key=lambda x: (-x[0], x[1].lower())):
                    extra = (['al rival'] if mixto and para == 'rival' else []) + extra
                    s.append(f'  - {md(label)}' + (f', con {md(pat)}' if pat else '') + f' ({retratos(n)})'
                             + (' — ' + '; '.join(extra) if extra else ''))
            if de_stat[e['id']]:
                s.append('- **Leads & Supports y bonos de equipo:**')
                for n, nb, stat, extra in sorted(de_stat[e['id']], key=lambda x: (-x[0], -x[1], x[2].lower())):
                    s.append(f'  - {md(stat)} ({quienes_dan(n, nb)})' + (' — ' + '; '.join(extra) if extra else ''))
            s.append('')
    s += acumula_md(cat, acumula, tope, guia)
    s += glosario_md(glos, cat, ctps)
    citadas = sorted({k for L in [g[x] for g in cat['grupos'] for x in ('pve', 'pvp')] +
                      [e[x] for e in cat['efectos'] for x in ('pve', 'pvp') if x in e] + glos['terminos']
                      for k in L.get('fuente', [])})
    s.append('## Fuentes\n')
    s += [f"- {fuente_md(fuentes[k])}" for k in citadas]
    s.append('')
    return '\n'.join(s)


def acumula_md(cat, acumula, tope, guia):
    """La tabla de los stats de liderazgo, soporte y bono de equipo: si se acumulan y su tope (catalogo.json, acumula y
    tope; docs/MODELO.md, Efectos iguales)."""
    nota = lambda x: x['nota']['es'] if 'nota' in x else ''
    s = ['## Qué se acumula y los topes\n',
         'Cuando a un integrante del equipo le llega el mismo stat de dos o más fuentes (Ezequiel, 5 de octubre de 2026): las '
         'estadísticas se suman; las habilidades (los anti-mermas, las inmunidades, la barrera, los escudos, revivir, invocar, '
         'la inmortalidad) cuentan una vez, la de mayor valor y, a igual valor, la primera en este orden: la propia, la del '
         'liderazgo del líder y la de los soportes de los demás (docs/MODELO.md, *Efectos iguales*). El tope es el de la guía ('
         + fuente_md(guia['fuentes'][guia['topes']['fuente'][0]]) + '): con lo que suman los buffs, la app avisa si pasa lo '
         'que queda hasta el tope.\n',
         f"{sum(1 for x in cat['soporte'].values() if x['acumula'])} stats se acumulan y "
         f"{sum(1 for x in cat['soporte'].values() if not x['acumula'])} cuentan una vez; "
         f"{sum(1 for x in cat['soporte'].values() if 'tope' in x)} tienen tope.\n",
         '| Stat | Si llega de dos fuentes | Tope | Nota |', '|---|---|---|---|']
    for stat, x in sorted(cat['soporte'].items(), key=lambda kv: (kv[1]['acumula'], kv[0].lower())):
        s.append(f"| {md(stat)} | {acumula(x)} | {tope(x) or '—'} | {nota(x)} |")
    s.append('')
    return s


def glosario_md(glos, cat, ctps):
    """El glosario del juego en docs/CATALOGO.md: los errores que se repiten y cada término."""
    nombre = {e['id']: e['es'] for e in cat['efectos']}
    s = ['## Glosario del juego\n',
         f"El glosario de skills del juego (Skill Name Glossary en inglés, 스킬 용어 사전 en coreano), desde "
         f"`scripts/contenido/glosario.json`: {len(glos['terminos'])} términos, en el orden del juego. El "
         "coreano es el original: donde el inglés no dice lo mismo, se aclara. «Lo da» dice qué C.T.P. da el efecto y de "
         "qué opción sale: la opción fija (고정 옵션), que tienen el C.T.P. de 6★ y los reforjados, o una opción de "
         "reforjado (재련 옵션), que solo tienen los reforjados (Mighty y Brilliant).\n",
         '### Errores que se repiten\n']
    for e in glos['errores']:
        ts = ', '.join(x['es'] for x in glos['terminos'] if x.get('error') == e['id'])
        s.append(f"- **{e['titulo']['es']}** ({ts}). {e['texto']['es']}")
    s += ['', '### Términos\n']
    for x in glos['terminos']:
        s.append(f"- **{x['es']}**" + (f" ({x['en']})" if x['en'] != x['es'] else '') + f" · {x['ko']}: {x['que']['es']}")
        if 'difiere' in x:
            s.append(f"  - **El inglés y el coreano:** {x['difiere']['es']}")
        if x.get('ctp'):
            s.append('  - **Lo da:** ' + ', '.join(f"{ctps[c['id']]} ({OPCIONES_CTP[c['opcion']]})" for c in x['ctp']) + '.')
        if 'nota' in x:
            s.append(f"  - **Nota:** {x['nota']['es']}")
        if x['efectos']:
            s.append('  - **En el catálogo:** ' + ', '.join(nombre[e] for e in x['efectos']) + '.')
        if 'falta' in x:
            s.append(f"  - Sin la captura en {'inglés' if x['falta'] == 'en' else 'coreano'}.")
    s.append('')
    return s


def main():
    cat, glos = cargar(RUTA), cargar(RUTA_GLOSARIO)
    guia = cargar(os.path.join(_DIR, 'contenido', 'guia.json'))
    fuentes = guia['fuentes']
    fu = cargar('work/fuentes.json')
    ctps = {c['id']: c['name'] for c in fu['ctps']}
    mal = validar(cat, guia)
    if mal:
        raise SystemExit('scripts/contenido/catalogo.json tiene errores:\n  ' + '\n  '.join(mal))
    mal = validar_glosario(glos, cat, fuentes, ctps)
    if mal:
        raise SystemExit('scripts/contenido/glosario.json tiene errores:\n  ' + '\n  '.join(mal))
    mal = validar_valor(cargar(RUTA_VALOR), cat, cargar(os.path.join(_DIR, 'contenido', 'modos.json'))['modos'],
                        cargar(os.path.join(_DIR, 'contenido', 'roles_listas.json')))
    if mal:
        raise SystemExit('scripts/contenido/valor_equipos.json tiene errores:\n  ' + '\n  '.join(mal))
    U = usos(cargar('work/skills_parsed.json'), cargar('work/supports.json'), fu['bonos'])
    falta, sobra = cobertura(cat, U)
    for k, v in falta.items():
        if v:
            print(f'AVISO: catálogo de efectos: {k} de los datos sin clasificar (docs/AUDITORIA.md, sección 9): {v}')
    for k, v in sobra.items():
        if v:
            print(f'AVISO: catálogo de efectos: {k} que los datos ya no traen: {v}')
    version = ultima(cargar('work/updates.json'))[1]
    os.makedirs('docs', exist_ok=True)
    open('docs/CATALOGO.md', 'w', encoding='utf-8', newline='\n').write(documento(cat, U, guia, version, falta, glos, ctps))
    usos_falta = {'etiquetas': {l: sorted(U['etiqueta'][l])[:3] for l in falta['etiquetas']},
                  'patrones': [[l, p, sorted(U['patron'][l][p])[:3]] for l, p in falta['patrones']],
                  'stats': {s: sorted(U['stat'].get(s) or [f'bono «{n}»' for n in U['bono'][s]])[:3] for s in falta['stats']}}
    json.dump({'falta': usos_falta, 'sobra': sobra,
               'total': {'etiquetas': len(U['etiqueta']), 'stats': len(U['stat']), 'stats_bonos': len(U['bono']),
                         'efectos': len(cat['efectos'])}},
              open('work/catalogo.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"catálogo de efectos: {len(cat['efectos'])} efectos | etiquetas {len(U['etiqueta'])} | stats {len(U['stat'])} | "
          f"stats de bonos {len(U['bono'])} | "
          f"sin clasificar {sum(len(v) for v in falta.values())} | glosario: {len(glos['terminos'])} términos | docs/CATALOGO.md")


if __name__ == '__main__':
    main()
