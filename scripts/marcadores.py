#!/usr/bin/env python3
"""Lo que thanosvibs publica sin resolver en el texto de algunos efectos: a qué facción,
tipo, raza o habilidad se refiere ("Increases basic damage dealt to $HEROSUBTYPE1 faction
by 30%"). El valor no viene en ningún campo de la API, así que se completa, en este orden:

1. scripts/contenido/marcadores.csv, a mano: el id del efecto en la API y el valor (como
   lo muestra la app, o en inglés como lo nombra el juego). Gana sobre la wiki.
2. La wiki de Future Fight: la misma skill (por nombre, en la página del personaje; la
   pasiva de uniforme, en el "Bonus" de ese uniforme) con el mismo porcentaje, en el mismo
   sentido (daño infligido o recibido) y un valor de la clase que pide el texto (una
   facción para "faction", un tipo para "$HEROCLASS1 types", una habilidad para
   "ability"...). Si la skill tiene varios efectos así (el mismo daño contra héroes y
   contra villanos), la wiki tiene que nombrar la misma cantidad de valores distintos, y se
   asignan en el orden en que aparecen; si no coincide, no se usa.
Lo que no se completa queda sin resolver: la app lo marca "sin especificar" y
docs/AUDITORIA.md lo lista para cargarlo a mano.

Lo usa skills_api.py: cada efecto resuelto lleva el valor en español (g) y de dónde salió
(gs: 'm' a mano, 'w' wiki).

Corrido solo (python3 scripts/marcadores.py, con work/ bajado), agrega a la tabla a mano
una fila con el valor vacío por cada marcador sin resolver que todavía no esté. No toca
las filas que ya tiene."""
import csv, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from auditar import anclas, limpiar, norm, wslug
from dominio import ABIL, ALLIES, GENDER, SIDE, TYPE

_DIR = os.path.dirname(os.path.abspath(__file__))
TABLA = os.path.join(_DIR, 'contenido', 'marcadores.csv')
COLUMNAS = ['id', 'valor', 'personaje', 'skill', 'efecto']
MARCADOR = re.compile(r'\$HERO(?:SUBTYPE|CLASS)\d*')


def _vocab(d, sin=()):
    """[(cómo lo escribe la wiki, en minúsculas; cómo lo nombra el juego; cómo lo muestra la app)]"""
    return [(k.lower(), k, v) for k, v in d.items() if k not in sin]


FACC = _vocab(SIDE)
TIPOS = _vocab(TYPE)
RAZAS = _vocab(ALLIES, sin=('Other',))
GEN = _vocab(GENDER, sin=('Neutral',))   # en un texto de personajes, "Neutral" es el bando
HAB = _vocab(ABIL)
# Clase del marcador según el texto del efecto: (valores posibles, lo que sigue al valor en la wiki)
CLASES = {
    'faccion': (FACC, r'(?:-type)?\s+(?:faction|factions|characters?|types?)'),
    'tipo': (TIPOS, r'(?:-type)?\s+(?:types?|characters?)'),
    'habilidad': (HAB, r'\s+(?:ability|abilities)'),
    'personajes': (RAZAS + FACC + GEN, r'(?:-type)?\s+(?:characters?|types?|faction)'),
    'tipos2': (GEN + TIPOS + RAZAS, r'(?:-type)?\s+(?:types?|characters?)'),
}
# El "Bonus" de cada uniforme en la página: la cabecera con su nombre y el texto que sigue.
_BONUS = re.compile(r'^!\s*(?:\[\[File:[^\]]*\]\])?\s*([^\n]+?)\s*\n\|-\s*\n\|\s*class="header2"\s*\|\s*Bonus\s*\n'
                    r'(.*?)(?=class="header2"|\n!|\Z)', re.S | re.M)


def clase(texto):
    if '$HEROCLASS' in texto:
        return 'tipo'
    if '$HEROSUBTYPE1 faction' in texto:
        return 'faccion'
    if re.search(r'\$HEROSUBTYPE1 [Aa]bility|with \$HEROSUBTYPE1 ability', texto):
        return 'habilidad'
    if '$HEROSUBTYPE1 characters' in texto:
        return 'personajes'
    if '$HEROSUBTYPE1 types' in texto:
        return 'tipos2'
    raise SystemExit(f'marcador en un texto que scripts/marcadores.py no sabe leer: {texto!r}')


def sentido(texto):
    """'r' si habla del daño recibido, 'i' si del infligido."""
    return 'r' if re.search(r'\breceived\b', texto, re.I) else 'i'


def candidatos(txt, kind):
    """[(posición, valor en español, porcentaje, sentido)] que nombra el texto de la wiki, en
    orden. La wiki lo escribe de dos formas: "...dealt to SUPER HERO faction by 45%" y, en los
    bonus de uniforme, "35% increase to damage dealt against UNIVERSAL-type Characters". El
    sentido sale de la última mención de daño recibido o infligido antes del valor, dentro
    de la oración."""
    voc, cola = CLASES[kind]
    t = txt.replace('İ', 'I')
    out = set()
    for term, _, es in sorted(voc, key=lambda x: -len(x[0])):
        valor = rf'(?<![a-z])(?<!super ){re.escape(term)}{cola}\b'
        for m in re.finditer(r'(?P<v>' + valor + r')[^.\n%]{0,40}?\bby\s+\+?(?P<n>\d+(?:\.\d+)?)\s*%', t, re.I):
            out.add((m.start('v'), es, m.group('n')))
        for m in re.finditer(r'(?P<n>\d+(?:\.\d+)?)\s*%\s+(?:increase|decrease)[^.\n%]{0,40}?\b(?:against|from|to)\s+(?P<v>'
                             + valor + ')', t, re.I):
            out.add((m.start('v'), es, m.group('n')))
    res = []
    for pos, es, n in sorted(out):
        antes = t[t.rfind('.', 0, pos) + 1:pos]
        dichos = re.findall(r'\b(received|dealt|attacking)\b', antes, re.I)
        res.append((pos, es, n, 'r' if dichos and dichos[-1].lower() == 'received' else 'i'))
    return res


def bonus_uniforme(wt, uniforme):
    """Texto del "Bonus" de un uniforme en la página (la pasiva de uniforme se llama como el
    uniforme). La wiki a veces lo nombra más corto ("Infinity War" por "Marvel Studios'
    Avengers: Infinity War"): vale el nombre exacto y, si no está, el único que esté contenido
    en el otro."""
    bloques = [(norm(m.group(1)), limpiar(m.group(2))) for m in _BONUS.finditer(wt)]
    u = norm(uniforme)
    exactos = [t for n, t in bloques if n == u]
    if exactos:
        return exactos
    parecidos = [t for n, t in bloques if n and (n in u or u in n)]
    return parecidos if len(parecidos) == 1 else []


def valor_es(v, kind, donde):
    """Valor de la tabla a mano (en español o en inglés) como lo muestra la app; tiene que
    ser de la clase que pide el texto del efecto."""
    v = v.strip()
    for _, en, es in CLASES[kind][0]:
        if v in (es, en):
            return es
    raise SystemExit(f'{donde}: «{v}» no sirve para este efecto; los valores posibles son: '
                     + ', '.join(es for _, _, es in CLASES[kind][0]))


def leer_tabla():
    if not os.path.exists(TABLA):
        return []
    with open(TABLA, encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        if r.fieldnames != COLUMNAS:
            raise SystemExit(f'contenido/marcadores.csv: la primera fila tiene que ser {",".join(COLUMNAS)} '
                             f'(tiene {",".join(r.fieldnames or [])})')
        return list(r)


def tabla_manual(clase_de):
    """({id: valor en español} de las filas con valor, [ids que la API ya no trae])."""
    out, huerfanos = {}, []
    for i, fila in enumerate(leer_tabla(), start=2):
        if not (fila['valor'] or '').strip():
            continue
        ide = int(fila['id'])
        if ide not in clase_de:
            huerfanos.append(ide)
            continue
        out[ide] = valor_es(fila['valor'], clase_de[ide], f'contenido/marcadores.csv, fila {i}')
    return out, huerfanos


def efectos():
    """Cada efecto de la API con marcador: [{id, p, slot, skill, texto, clase, pct, sentido}]."""
    out = []
    for fn in sorted(glob.glob('work/skills_api/*.json')):
        d = json.load(open(fn, encoding='utf-8'))
        for slot, sk in (d.get('skills') or {}).items():
            if not isinstance(sk, dict) or 'stages' not in sk:
                continue
            for st in sk.get('stages') or []:
                for ab in st.get('abils') or []:
                    texto = re.sub(r'</?b>', '', ab.get('description') or '')
                    if MARCADOR.search(texto):
                        out.append({'id': ab['id'], 'p': d['portrait'], 'slot': slot, 'skill': sk.get('name') or '',
                                    'texto': texto, 'clase': clase(texto), 'pct': re.findall(r'(\d+(?:\.\d+)?)%', texto)[-1],
                                    'sentido': sentido(texto)})
    return out


def resolver():
    """({id: (valor en español, 'm'|'w')}, efectos, avisos). avisos: conflictos (ids que la
    wiki resuelve distinto en dos skills), huerfanos (ids de la tabla a mano que la API ya no
    trae) y distintos (valores a mano que no coinciden con la wiki; gana el de la tabla)."""
    chars = json.load(open('work/characters.json'))
    fila = {r['portrait']: r for r in chars}
    base = {r['base_portrait']: r['character'] for r in chars if r['uniformed'] == 'False'}
    efs = efectos()
    wiki, conflictos, paginas = {}, set(), {}
    por_skill = {}
    for e in efs:
        por_skill.setdefault((e['p'], e['skill']), []).append(e)
    for (p, skill), es in por_skill.items():
        nombre = base[fila[p]['base_portrait']]
        if nombre not in paginas:
            ruta = f'work/wikitext/{wslug(nombre)}.json'
            wt = json.load(open(ruta, encoding='utf-8'))['wt'] if os.path.exists(ruta) else ''
            paginas[nombre] = (wt, anclas(wt))
        wt, an = paginas[nombre]
        textos = [limpiar(a['txt']) for a in an if a['n'] == norm(skill)]
        if any(e['slot'] == 'Uniform Passive' for e in es):
            textos += bonus_uniforme(wt, skill)
        if not textos:
            continue
        for kind, pct, sen in {(e['clase'], e['pct'], e['sentido']) for e in es}:
            grupo = list({e['id']: e for e in es if (e['clase'], e['pct'], e['sentido']) == (kind, pct, sen)})
            vals = []
            for t in textos:
                for _, val, n, s in candidatos(t, kind):
                    if (n, s) == (pct, sen) and val not in vals:
                        vals.append(val)
            if len(vals) != len(grupo):
                continue
            for ide, val in zip(grupo, vals):
                if wiki.get(ide, val) != val:
                    conflictos.add(ide)
                wiki[ide] = val
    clase_de = {e['id']: e['clase'] for e in efs}
    manual, huerfanos = tabla_manual(clase_de)
    out = {i: (v, 'w') for i, v in wiki.items() if i not in conflictos}
    distintos = sorted(i for i in manual if i in out and out[i][0] != manual[i])
    out.update({i: (v, 'm') for i, v in manual.items()})
    return out, efs, {'conflictos': sorted(conflictos), 'huerfanos': sorted(huerfanos), 'distintos': distintos}


def personaje(p, fila):
    r = fila[p]
    return r['character'] + ('' if r['uniformed'] == 'False' else f" — {r['uniform']}")


def plantilla():
    """Agrega a la tabla a mano las filas vacías de los marcadores sin resolver que no tiene."""
    out, efs, _ = resolver()
    fila = {r['portrait']: r for r in json.load(open('work/characters.json'))}
    filas = leer_tabla()
    ya = {int(f['id']) for f in filas}
    nuevas = {}
    for e in efs:
        if e['id'] in out or e['id'] in ya:
            continue
        n = nuevas.setdefault(e['id'], {'id': e['id'], 'valor': '', 'personaje': [], 'skill': e['skill'], 'efecto': e['texto']})
        if personaje(e['p'], fila) not in n['personaje']:
            n['personaje'].append(personaje(e['p'], fila))
    for n in nuevas.values():
        n['personaje'] = ' / '.join(n['personaje'])
    todas = filas + sorted(nuevas.values(), key=lambda n: (n['personaje'], n['skill'], n['id']))
    with open(TABLA, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS, lineterminator='\n')
        w.writeheader()
        w.writerows(todas)
    print(f'contenido/marcadores.csv: {len(filas)} filas que ya tenía, {len(nuevas)} nuevas sin valor')


if __name__ == '__main__':
    plantilla()
