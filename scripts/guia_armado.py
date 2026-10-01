#!/usr/bin/env python3
"""Guía de armado de Cynicalex: la planilla pública «Cynicalex Mega Guides» de Google
Sheets. De la pestaña CHAMP BUILDING (una fila por personaje) salen el mejor uniforme,
los C.T.P., el ISO-8, el obelisco, la rotación, si necesita artefacto, su lugar en la tier
list, cómo se consigue y las notas; de la pestaña TIER LIST, la leyenda de los emojis.

La planilla se edita a mano, seguido, y su formato es libre. Por eso no se lee directo:
fetch_all.py la baja y llama a aceptar(), que la compara con lo que este lector entiende.
Si es compatible pasa a ser la copia en uso (fuentes/guia-armado/, versionada en el repo:
el workflow semanal la commitea con los datos); si no, la copia en uso no se toca y
estado.json anota la fecha y los motivos, que la app muestra en Ajustes.

Compatible quiere decir:
- CHAMP BUILDING tiene la fila de encabezados (la que empieza con «PK») con todas las
  columnas que se usan (COLUMNAS) y, arriba, la versión de la guía («V12.2.0»).
- Siguen estando, textuales, las líneas de la leyenda cuyo significado usa este lector
  (lineas_leyenda()): si cambian, lo que diría la app podría no ser lo que dice la planilla.
- TIER LIST tiene la línea de leyenda de los emojis («🤝 = SUPPORT     🔨 = PVP …»).
- Hay al menos MIN_FILAS filas de personajes y, en los nombres (personaje + uniforme,
  contra thanosvibs) y en cada columna que se interpreta (C.T.P., ISO-8, obelisco,
  artefacto, emojis), se entiende al menos el 80% de los valores (MIN_ENTENDIDO): menos que eso
  es otro formato, no un valor nuevo suelto.
Un valor suelto que no se entiende (un C.T.P. nuevo, un emoji sin leyenda, una fila sin
personaje en thanosvibs) no hace incompatible la planilla: viaja tal cual, la app lo
muestra marcado y Ajustes lo lista."""
import csv, hashlib, io, json, os, re, unicodedata

_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA = os.path.join(_RAIZ, 'fuentes', 'guia-armado')
ARCHIVOS = {'armado': 'champ-building.csv', 'tierlist': 'tier-list.csv'}
PLANILLA = 'https://docs.google.com/spreadsheets/d/1H0Hcl9oVZV9gA266xkJAqPv5bD1qwqhC5NeVbLj_-FE'
GID = {'armado': '190850363', 'tierlist': '1844623213'}
MIN_FILAS = 200
MIN_ENTENDIDO = 0.8


def url_csv(pestana):
    return f'{PLANILLA}/export?format=csv&gid={GID[pestana]}'


# Columnas de CHAMP BUILDING que se usan, por nombre de encabezado (se ubican por nombre:
# una columna nueva en el medio no rompe nada). Las demás se ignoran: el tier, el tipo de
# ataque, aliados/bando/instinto y las opciones de uniforme ya vienen de thanosvibs, y
# «Story Mode» no tiene leyenda.
COLUMNAS = {
    'pk': 'PK', 'nombre': 'Best Uni Character Name', 'uniforme': 'Best Uniform',
    'adq': 'Acquisition', 'iso': 'Best ISO-8 Set', 'obelisco': 'Obelisk (SL/AC)',
    'rot': 'Proc Rotation', 'rotc': 'Best CTP Rotation', 'proc': 'Proc/Frenzy Skill',
    'mejor': 'Best CTP', 'segundo': '2nd Best CTP', 'pve': 'Meta CTP (PVE)', 'pve_alt': 'Off-Meta CTP (PVE)',
    'pvp': 'Meta CTP (PVP)', 'pvp_alt': 'Off-Meta CTP (PVP)',
    'art': 'Needs Artifact?', 'rank': 'Tier List Rank', 'bling': 'Tier List Bling', 'nota': 'Notes',
}
CTP_COLS = ['mejor', 'segundo', 'pve', 'pve_alt', 'pvp', 'pvp_alt']

# Leyenda de CHAMP BUILDING que usa este lector, tal como está escrita en la planilla.
LEY_ADQ = [('SLS', 'Shadowland Selectors'), ('SS', 'Dimension Mission Support Shop'),
           ('EQ', 'Epic Quest'), ('HQ', 'Heroic Quest')]
LEY_ART = [('Y', 'Must have for character to function'), ('X', 'Nice to have'), ('O', 'Optional / Not needed')]
LEY_ROT = [('c', 'cancel by pressing next skill'), ('dc', 'delayed skill cancel'),
           ('H', 'hold skill for proc duration'), ('k / kite', 'run around for a couple seconds')]
LEY_CTP = ['CTP+ = Reforged required', 'Elemental characters: Judgement', 'ABX: Rage', 'Judgement+ can replace Rage']
LEY_ISO_CAT = [('offensive', ['POAH', 'OD', 'HE']), ('shield', ['DDE', 'BP']), ('defensive', ['PC', 'TS', 'SS'])]
LEY_ISO_SET = [('POAH', 'Power of Angry Hulk'), ('OD', 'Overdrive'), ('HE', "Hawk's Eye"), ('BP', 'Binary Power'),
               ('DDE', 'Drastic Density Enhancement'), ('PC', 'Protect the Captain'), ('TS', 'Tenacious Symbiote'),
               ('SS', 'Spider Sense')]


def lineas_leyenda():
    return ([f'{k} = {v}' for k, v in LEY_ADQ + LEY_ART + LEY_ROT] + LEY_CTP
            + [f'{k}: {", ".join(v)}' for k, v in LEY_ISO_CAT] + [f'{k} = {v}' for k, v in LEY_ISO_SET])


# Valores que se entienden en las columnas sin leyenda propia. «N» en «Needs Artifact?»
# es la respuesta no; «Optional» y «Support» viajan como texto.
ISO_TOKENS = re.compile(r'dont waste gold|offensive|defensive|shield')
OBELISCO = ['Proc', 'Invincible', 'GBI', 'Mini-Rage', 'Fire', 'Lightning', 'Mind', 'Cold', 'Poison', 'HP']
ART_SUELTOS = ['N', 'Optional', 'Support']


class Incompatible(Exception):
    def __init__(self, motivos, version=None):
        super().__init__('; '.join(motivos))
        self.motivos, self.version = motivos, version


def clave(s):
    """Nombre comparable: sin tildes, mayúsculas ni signos («Spider-Man 2099» = «spiderman2099»)."""
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]', '', s.lower())


def _filas(texto):
    return list(csv.reader(io.StringIO(texto)))


def _vacio(s):
    return s in ('', '-')


def leyenda_emojis(filas):
    """{emoji: significado} de la primera línea de leyenda de la pestaña TIER LIST, o {}."""
    for f in filas[:10]:
        for c in f:
            partes = re.split(r'\s{2,}', c.strip().split('\n')[0].strip())
            ms = [re.fullmatch(r'(\S+) = (.+)', p) for p in partes]
            if len(partes) >= 3 and all(ms) and all(not any(ch.isalnum() for ch in m.group(1)) for m in ms):
                return {m.group(1): m.group(2).strip() for m in ms}
    return {}


def _sin_vs(s):
    return s.replace('️', '')


def _emojis(s, leyenda):
    """Emojis de la columna «Tier List Bling» con leyenda (como los escribe la leyenda) y lo
    que sobra sin leyenda."""
    claves = sorted(((_sin_vs(k), k) for k in leyenda), key=lambda x: -len(x[0]))
    s = _sin_vs(s)
    out, resto, i = [], '', 0
    while i < len(s):
        if s[i].isspace():
            i += 1
            continue
        k = next((k for k in claves if s.startswith(k[0], i)), None)
        if k:
            if k[1] not in out:
                out.append(k[1])
            i += len(k[0])
        else:
            resto += s[i]
            i += 1
    return out, resto


def _retratos(filas_tv):
    """(personaje, uniforme) -> retrato, con los nombres como los escribe thanosvibs en cada
    fila (un uniforme puede cambiar el nombre: «Amadeus Cho» con Heroic Age). Una clave que
    se repite con retratos distintos no se usa: la fila de la planilla queda sin personaje."""
    out, dobles = {}, set()
    for r in filas_tv:
        k = (clave(r['character']), clave(r['uniform']))
        if k in out and out[k] != r['portrait']:
            dobles.add(k)
        out[k] = r['portrait']
    for k in dobles:
        del out[k]
    return out


def leer(texto_armado, texto_tierlist, filas_tv, ctps_tv):
    """Lee las dos pestañas. Devuelve {version, emojis, pj: {retrato: {...}}, sin_pj, raros,
    cuenta, filas}. Si falta lo que hace falta para leerla (encabezados, versión, leyenda)
    levanta Incompatible con los motivos."""
    filas = _filas(texto_armado)
    i_enc = next((i for i, f in enumerate(filas[:15]) if f and f[0].strip() == 'PK'), None)
    if i_enc is None:
        raise Incompatible(['CHAMP BUILDING no tiene la fila de encabezados (la que empieza con «PK»)'])
    enc = [c.strip() for c in filas[i_enc]]
    motivos = []
    faltan = [n for n in COLUMNAS.values() if n not in enc]
    if faltan:
        motivos.append('faltan columnas: ' + ', '.join(f'«{n}»' for n in faltan))
    version = next((c.strip() for f in filas[:i_enc] for c in f if re.fullmatch(r'V\d+(\.\d+)+', c.strip())), None)
    if not version:
        motivos.append('no está la versión de la guía (la celda «V…» arriba de los encabezados)')
    celdas = {c.strip() for f in filas for c in f}
    sin_ley = [l for l in lineas_leyenda() if l not in celdas]
    if sin_ley:
        motivos.append('la leyenda cambió; ya no dice ' + ', '.join(f'«{l}»' for l in sin_ley))
    emojis = leyenda_emojis(_filas(texto_tierlist))
    if not emojis:
        motivos.append('TIER LIST no tiene la línea de leyenda de los emojis («🤝 = SUPPORT …»)')
    if motivos:
        raise Incompatible(motivos, version)

    col = {k: enc.index(n) for k, n in COLUMNAS.items()}
    retratos = _retratos(filas_tv)
    ctp_ids = {clave(c['name']) for c in ctps_tv}
    ley_art = dict(LEY_ART)
    obelisco = {o.lower(): o for o in OBELISCO}
    pj, sin_pj = {}, []
    raros = {k: [] for k in ('ctp', 'iso', 'obelisco', 'art', 'bling')}
    cuenta = {k: [0, 0] for k in ('nombres', 'ctp', 'iso', 'obelisco', 'art', 'bling')}   # [se entienden, total]

    def contar(k, ok, crudo):
        cuenta[k][1] += 1
        if ok:
            cuenta[k][0] += 1
        else:
            raros[k].append(crudo)

    for f in filas[i_enc + 1:]:
        f = f + [''] * (len(enc) - len(f))
        v = {k: f[i].strip() for k, i in col.items()}
        if not v['pk']:
            continue
        cuenta['nombres'][1] += 1
        p = retratos.get((clave(v['nombre']), clave(v['uniforme'])))
        if not p or p in pj:
            sin_pj.append(f"{v['pk']}: {v['nombre']} / {v['uniforme']}" + (' (repetido)' if p else ''))
            continue
        cuenta['nombres'][0] += 1
        e = {}
        if not _vacio(v['adq']):
            e['adq'] = [x for x in re.split(r'\s*[,;/]\s*', v['adq']) if not _vacio(x)]
        if not _vacio(v['iso']):
            bajo = v['iso'].lower()
            e['iso'] = list(dict.fromkeys(ISO_TOKENS.findall(bajo)))
            resto = re.sub(r'[,\s]+', ' ', ISO_TOKENS.sub(' ', bajo)).strip()
            if resto:
                e['iso_x'] = resto
            contar('iso', not resto, v['iso'])
        if not _vacio(v['obelisco']):
            ts = [x.strip() for x in v['obelisco'].split(',') if x.strip()]
            ob, ob_x = [obelisco[x.lower()] for x in ts if x.lower() in obelisco], [x for x in ts if x.lower() not in obelisco]
            if ob:
                e['ob'] = ob
            if ob_x:
                e['ob_x'] = ob_x
            contar('obelisco', not ob_x, v['obelisco'])
        for k in ('rot', 'rotc', 'proc', 'rank', 'nota'):
            if not _vacio(v[k]):
                e[k] = v[k]
        ctps = []
        for k in CTP_COLS:
            if _vacio(v[k]):
                continue
            m = re.fullmatch(r'([A-Za-z][A-Za-z ]*?)\s*(\+?)', v[k])
            ok = bool(m) and clave(m.group(1)) in ctp_ids
            ctps.append({'k': k, 'c': clave(m.group(1)), 'r': bool(m.group(2))} if ok else {'k': k, 'x': v[k]})
            contar('ctp', ok, v[k])
        if ctps:
            e['ctp'] = ctps
        if not _vacio(v['art']):
            m = re.fullmatch(r'([YXO])(?: \((PVP|PVE)\))?', v['art'])
            if m:
                e['art'] = {'t': ley_art[m.group(1)], 'v': v['art']}
                if m.group(2):
                    e['art']['modo'] = {'PVP': 'PvP', 'PVE': 'PvE'}[m.group(2)]
            elif v['art'] in ART_SUELTOS:
                e['art'] = {'t': v['art'], 'v': v['art']}
            else:
                e['art_x'] = v['art']
            contar('art', bool(m) or v['art'] in ART_SUELTOS, v['art'])
        if not _vacio(v['bling']):
            bl, resto = _emojis(v['bling'], emojis)
            if bl:
                e['bl'] = bl
            if resto:
                e['bl_x'] = resto
            contar('bling', not resto, v['bling'])
        pj[p] = e
    return {'version': version, 'emojis': emojis, 'pj': pj, 'sin_pj': sin_pj, 'filas': cuenta['nombres'][1],
            'raros': {k: sorted(set(x)) for k, x in raros.items() if x}, 'cuenta': cuenta}


_NOMBRE_CUENTA = {'nombres': 'personaje y mejor uniforme (contra thanosvibs)', 'ctp': 'columnas de C.T.P.',
                  'iso': '«Best ISO-8 Set»', 'obelisco': '«Obelisk (SL/AC)»', 'art': '«Needs Artifact?»',
                  'bling': '«Tier List Bling» (emojis)'}


def motivos_umbral(r):
    """Motivos de incompatibilidad por cantidad: pocas filas o columnas que casi no se entienden."""
    m = []
    if r['filas'] < MIN_FILAS:
        m.append(f"tiene {r['filas']} filas de personajes (se esperan al menos {MIN_FILAS})")
    for k, (ok, total) in r['cuenta'].items():
        if total and ok < MIN_ENTENDIDO * total:
            m.append(f'{_NOMBRE_CUENTA[k]}: se entienden {ok} de {total} valores')
    return m


def _ruta(nombre):
    return os.path.join(CARPETA, nombre)


def estado():
    with open(_ruta('estado.json'), encoding='utf-8') as f:
        return json.load(f)


def _guardar_estado(e):
    with open(_ruta('estado.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(e, f, ensure_ascii=False, indent=1)
        f.write('\n')


def texto_en_uso(pestana):
    with open(_ruta(ARCHIVOS[pestana]), encoding='utf-8', newline='') as f:
        return f.read()


def _texto(b):
    try:
        t = b.decode('utf-8')
    except UnicodeDecodeError:
        raise Incompatible(['no llegó texto UTF-8'])
    if t.lstrip().startswith('<'):
        raise Incompatible(['llegó una página web en vez del CSV: la planilla dejó de ser pública o cambió de dirección'])
    return t


def rechazar(motivos, hoy, version=None):
    """Anota en estado.json que la planilla de hoy no se usa, y por qué. La copia en uso
    sigue siendo la última compatible."""
    e = estado()
    e['comprobada'] = hoy
    e['rechazo'] = {'version': version, 'motivos': motivos}
    _guardar_estado(e)
    return f"AVISO guía de armado: no se usa la planilla bajada hoy ({'; '.join(motivos)}); sigue la {e['version']} del {e['tomada']}"


def aceptar(crudo, filas_tv, ctps_tv, hoy):
    """crudo: {'armado': bytes, 'tierlist': bytes}, recién bajados. Si es compatible pasa a
    ser la copia en uso; si no, se rechaza. Devuelve la línea para el log."""
    try:
        textos = {k: _texto(b) for k, b in crudo.items()}
        r = leer(textos['armado'], textos['tierlist'], filas_tv, ctps_tv)
        m = motivos_umbral(r)
        if m:
            raise Incompatible(m, r['version'])
    except Incompatible as x:
        return rechazar(x.motivos, hoy, x.version)
    sha = {ARCHIVOS[k]: hashlib.sha256(b).hexdigest() for k, b in crudo.items()}
    e = estado() if os.path.exists(_ruta('estado.json')) else None
    if e and e['sha256'] == sha:
        e.update(comprobada=hoy, rechazo=None)
        _guardar_estado(e)
        return f"guía de armado: sin cambios ({e['version']} del {e['tomada']})"
    os.makedirs(CARPETA, exist_ok=True)
    for k, b in crudo.items():
        with open(_ruta(ARCHIVOS[k]), 'wb') as f:
            f.write(b)
    _guardar_estado({'version': r['version'], 'tomada': hoy, 'comprobada': hoy, 'sha256': sha, 'rechazo': None})
    return (f"guía de armado: {r['version']} | {len(r['pj'])} personajes"
            + (f" | sin personaje: {r['sin_pj']}" if r['sin_pj'] else '')
            + (f" | sin interpretar: {r['raros']}" if r['raros'] else ''))
