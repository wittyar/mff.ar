"""El histórico de los personajes (Ezequiel, 5 de octubre de 2026: «una pestaña de histórico del juego... cada cambio
con el link a su nota»; «en primera instancia solo los personajes»).

Dos fuentes:
- /api/updates de thanosvibs (work/updates.json): cada versión del juego, con su nombre y su fecha (potes), y en qué
  versión llegó cada personaje, uniforme, Tier-3, Potencial Trascendido y Tier-4 (added_in, por retrato).
- Las notas de actualización del foro oficial (fuentes/foro/, las baja scripts/foro.py): el texto en inglés, por
  secciones (▣ o ■ al principio de la línea).

Cada nota va a la versión de thanosvibs de fecha más cercana, a VENTANA días o menos (las notas salen casi siempre el
día anterior). De cada llegada que publica thanosvibs sale un hecho, con el texto de la nota que nombra al personaje
(la sección de su tipo, si la hay); y de cada sección de la nota que habla de skills o de balance (BALANCE) y nombra a un
personaje, un hecho «balance» con esas líneas. Lo que no cierra entre las dos fuentes va a docs/HISTORICO.md: las
llegadas cuya nota no nombra al personaje, las versiones sin nota y las notas sin versión.

armar() devuelve MFF_HISTORICO y el texto de docs/HISTORICO.md. Solo biblioteca estándar."""
import datetime as dt, glob, html, json, os, re

VENTANA = 4
TIPOS = ('personaje', 'uniforme', 't3', 'tp', 't4', 'balance')
# De qué tipo es una sección, por su título. El orden importa: «Tier-4 and New Uniforms» es de los dos.
SECCION = [('t4', re.compile(r'tier[- ]?4', re.I)), ('t3', re.compile(r'tier[- ]?3', re.I)),
           ('tp', re.compile(r'transcend', re.I)), ('uniforme', re.compile(r'uniform', re.I)),
           ('personaje', re.compile(r'characters?|heroes|villains', re.I))]
BALANCE = re.compile(r'balanc|rework|adjust|skill|improve|enhance|change|revamp|buff', re.I)
MAX_LINEAS = 6
MAX_CHARS = 400


def lineas(h):
    """El HTML de una nota, en líneas de texto."""
    h = re.sub(r'(?i)<br\s*/?>|</p>|</div>|</li>|</h\d>|</tr>', '\n', h)
    t = html.unescape(re.sub(r'<[^>]+>', '', h)).replace('\xa0', ' ')
    return [re.sub(r'\s+', ' ', l).strip() for l in t.split('\n') if l.strip()]


def secciones(ls):
    """[(título, [líneas])]: una por cada línea que empieza con ▣ o ■; lo de antes de la primera, con título ''."""
    out = [('', [])]
    for l in ls:
        if l[0] in '▣■':
            out.append((l.lstrip('▣■ ').strip(), []))
        else:
            out[-1][1].append(l)
    return [s for s in out if s[0] or s[1]]


def tipo_seccion(titulo):
    return [k for k, rx in SECCION if rx.search(titulo)]


def alias(nombres):
    """Otros nombres con que las notas escriben a un personaje del roster: sin «The» adelante (The Thing → Thing), Mister
    y Mr., Doctor y Dr., y sin lo de entre paréntesis (Wasp (Nadia Van Dyne) → Nadia Van Dyne, el de adentro). Uno que
    choca con otro nombre del roster, o que sale de dos personajes, no se usa. {alias: nombre del roster}."""
    cand = {}
    for n in nombres:
        xs = set()
        if n.startswith('The '): xs.add(n[4:])
        for a, b in (('Mister ', 'Mr. '), ('Doctor ', 'Dr. ')):
            if n.startswith(a): xs.add(b + n[len(a):])
            if n.startswith(b): xs.add(a + n[len(b):])
        m = re.fullmatch(r'(.+?) \((.+)\)', n)
        if m: xs.add(m.group(2))
        for x in xs:
            cand.setdefault(x, set()).add(n)
    return {x: next(iter(ns)) for x, ns in cand.items() if len(ns) == 1 and x not in nombres}


def buscador(nombres):
    """Una función que dice qué personajes del roster aparecen en una línea (por su nombre o un alias): con mayúsculas como
    en el roster, o la línea en mayúsculas (las notas viejas escriben ‘QUICKSILVER’); el nombre más largo primero, así
    «Red Hulk» no cuenta también como «Hulk»."""
    canon = {n: n for n in nombres} | alias(nombres)
    orden = sorted(canon, key=len, reverse=True)
    rx = re.compile(r'(?<![\w-])(' + '|'.join(re.escape(n) for n in orden) + r')(?![\w-])')
    rx_may = re.compile(r'(?<![\w-])(' + '|'.join(re.escape(n.upper()) for n in orden) + r')(?![\w-])')
    may = {n.upper(): n for n in orden}

    def en(linea):
        hallados = {canon[x] for x in rx.findall(linea)}
        hallados |= {canon[may[x]] for x in rx_may.findall(linea)}
        return hallados
    return en


def corta(l):
    return l if len(l) <= MAX_CHARS else l[:MAX_CHARS - 1] + '…'


def fecha_ms(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date()


def armar(chars, updates, dir_foro):
    # Las versiones del juego, de thanosvibs (sin las que no tienen fecha).
    versiones = sorted(((dt.datetime.strptime(p['date'], '%B %d, %Y').date(), p['version'], p['name'])
                        for u in updates for p in u.get('potes') or []), key=lambda x: (x[0], x[1]))
    # Las notas, con su versión.
    indice = json.load(open(os.path.join(dir_foro, 'indice.json'), encoding='utf-8'))
    notas, sin_version = {}, []
    for n in indice:
        f = fecha_ms(n['fecha'])
        cerca = [v for v in versiones if abs((f - v[0]).days) <= VENTANA]
        v = min(cerca, key=lambda v: (abs((f - v[0]).days), v[1]))[1] if cerca else None
        texto = None
        if 'error' not in n:
            texto = secciones(lineas(json.load(open(os.path.join(dir_foro, f"{n['id']}.json"), encoding='utf-8'))['html']))
        notas[n['id']] = {'id': n['id'], 'titulo': n['titulo'], 'fecha': f, 'url': n['url'], 'v': v, 'texto': texto,
                          'error': n.get('error')}
        if v is None:
            sin_version.append(notas[n['id']])
    por_version = {}
    for n in sorted(notas.values(), key=lambda n: n['fecha']):
        if n['v']:
            por_version.setdefault(n['v'], []).append(n)

    # Los nombres del roster y de qué variante es cada retrato.
    nombre_de = {c['id']: c['name'] for c in chars}
    cid_de_nombre = {c['name']: c['id'] for c in chars}
    variante = {}
    for c in chars:
        variante[c['p']] = (c['id'], c['id'] + '::base')
        for u in c['uniforms']:
            variante[u['p']] = (c['id'], c['id'] + '::' + u['id'])
    en = buscador(list(cid_de_nombre))

    hechos, sin_nombrar, sin_retrato = [], [], []
    # 1. Las llegadas que publica thanosvibs.
    llaves = {'characters': 'personaje', 'uniforms': 'uniforme', 't3s': 't3', 'tps': 'tp', 't4s': 't4'}
    for u in updates:
        for campo, tipo in llaves.items():
            for x in u.get(campo) or []:
                if x['portrait'] not in variante:
                    sin_retrato.append((tipo, x['portrait'], x['added_in']))
                    continue
                cid, key = variante[x['portrait']]
                nombre = nombre_de[cid]
                nota, texto = None, []
                for n in por_version.get(x['added_in'], []):
                    if not n['texto']:
                        continue
                    secs = [(t, ls) for t, ls in n['texto'] if nombre in en(t) or any(nombre in en(l) for l in ls)]
                    if not secs:
                        continue
                    secs.sort(key=lambda s: tipo not in tipo_seccion(s[0]))
                    t, ls = secs[0]
                    nota = n['id']
                    texto = ([t] if t else []) + [corta(l) for l in ls if nombre in en(l)][:MAX_LINEAS]
                    break
                if nota is None:
                    sin_nombrar.append((tipo, key, x['added_in'], [n['id'] for n in por_version.get(x['added_in'], [])]))
                hechos.append({'k': key, 't': tipo, 'v': x['added_in'], 'n': nota, 'x': texto})
    # 2. Lo que las notas dicen de skills o de balance de cada personaje.
    for n in notas.values():
        for t, ls in n['texto'] or []:
            if not t or not BALANCE.search(t) or tipo_seccion(t):
                continue
            por_pj = {}
            for l in ls:
                for nombre in en(l):
                    por_pj.setdefault(nombre, []).append(corta(l))
            for nombre, xs in por_pj.items():
                hechos.append({'k': cid_de_nombre[nombre], 't': 'balance', 'v': n['v'], 'n': n['id'],
                               'x': [t] + xs[:MAX_LINEAS], 'f': n['fecha'].isoformat()})

    H = {
        'ventana': VENTANA,
        'versiones': [[v, nombre, f.isoformat(), [n['id'] for n in por_version.get(v, [])]]
                      for f, v, nombre in reversed(versiones)],
        'notas': {n['id']: [n['titulo'], n['fecha'].isoformat(), n['url']] + ([n['error']] if n['error'] else [])
                  for n in notas.values()},
        'hechos': [[h['k'], h['t'], h['v'], h['n'], h['x']] + ([h['f']] if 'f' in h else []) for h in hechos],
    }
    return H, informe(versiones, notas, por_version, hechos, sin_nombrar, sin_version, sin_retrato, nombre_de)


def informe(versiones, notas, por_version, hechos, sin_nombrar, sin_version, sin_retrato, nombre_de):
    def link(i):
        n = notas[i]
        return f"[{n['titulo'].strip()}]({n['url']})"
    cuenta = {t: sum(1 for h in hechos if h['t'] == t) for t in TIPOS}
    s = ['# Histórico: lo que no cierra entre thanosvibs y las notas del foro\n',
         'Generado por `scripts/historico.py` (lo llama `scripts/build.py`). Las llegadas (personaje, uniforme, Tier-3, '
         'Potencial Trascendido, Tier-4) y las versiones con su fecha salen de `/api/updates` de thanosvibs; el texto, de '
         'las notas de actualización del foro oficial (`fuentes/foro/`, `scripts/foro.py`). Cada nota va a la versión de '
         f'fecha más cercana, a {VENTANA} días o menos.\n',
         f"- Versiones: {len(versiones)}; con nota: {len(por_version)}. Notas: {len(notas)}; sin versión: {len(sin_version)}.",
         '- Hechos: ' + ', '.join(f'{t} {cuenta[t]}' for t in TIPOS) + '.\n']
    s.append(f'## Llegadas cuya nota no nombra al personaje ({len(sin_nombrar)})\n')
    s.append('thanosvibs las pone en esa versión, y la nota de esa versión no lo nombra (o la versión no tiene nota). '
             'Puede ser un nombre escrito distinto, un detalle que la nota trae en una imagen, o una versión mal asignada.\n')
    s.append('| Versión | Tipo | Variante | Notas de la versión |\n|---|---|---|---|')
    for tipo, key, v, ns in sorted(sin_nombrar, key=lambda x: (x[2], x[0], x[1])):
        s.append(f"| {v} | {tipo} | {key} | {', '.join(link(i) for i in ns) or 'sin nota'} |")
    s.append('')
    s.append(f'## Versiones sin nota ({len(versiones) - len(por_version)})\n')
    s.append(', '.join(f"{v} ({f.isoformat()})" for f, v, _ in versiones if v not in por_version) + '\n')
    s.append(f'## Notas sin versión ({len(sin_version)})\n')
    s += [f"- {n['fecha'].isoformat()}: {link(n['id'])}" for n in sin_version]
    s.append('')
    errores = [n for n in notas.values() if n['error']]
    s.append(f'## Notas que el foro no deja leer ({len(errores)})\n')
    s += [f"- {n['fecha'].isoformat()}: {link(n['id'])} — {n['error']}" for n in errores]
    s.append('')
    if sin_retrato:
        s.append(f'## Retratos de /api/updates que no están en el roster ({len(sin_retrato)})\n')
        s += [f'- {v} {tipo}: {p}' for tipo, p, v in sin_retrato]
        s.append('')
    return '\n'.join(s) + '\n'
