#!/usr/bin/env python3
"""Las notas de actualización en inglés contra sus pares coreanas (#3): docs/NOTAS_COREANO.md.

El coreano es el original y el inglés, su traducción. Cada nota del foro en inglés (fuentes/foro/, scripts/foro.py) se
compara con su par del café coreano (fuentes/cafe/, scripts/cafe.py). Las dos suelen tener las mismas secciones (▣ o ■),
en el mismo orden: con la misma cantidad se comparan sección por sección; si no, la nota entera. De cada una se comparan
los porcentajes y los segundos (lo que más importa en una skill o un balance, y se escribe igual en los dos idiomas): un
valor que está en una y no en la otra puede ser un error de traducción, algo que el inglés no trae o algo que el coreano
dice en una imagen. Esas diferencias, con las líneas que las tienen, y las notas en inglés sin par van al informe; leerlas
y decidir es a mano.

Lo corre build.py; solo, `python scripts/cotejo_ko.py` (no necesita work/). Solo biblioteca estándar."""
import collections, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from historico import fecha_ms, lineas, secciones

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Los marcadores de imagen del editor viejo de Naver: no son texto.
IMAGEN_VIEJA = re.compile(r'^\[\[\[CONTENT-ELEMENT-\d+\]\]\]$')
# Por idioma, las expresiones de los porcentajes y las de los segundos. El inglés escribe a veces el valor de antes sin
# la unidad: «8 sec (down from 9)», «from 25 to 14 seconds».
VALOR = {'ko': ([re.compile(r'(\d+(?:\.\d+)?)\s*%')], [re.compile(r'(\d+(?:\.\d+)?)\s*초')]),
         'en': ([re.compile(r'(\d+(?:\.\d+)?)\s*%')],
                [re.compile(r'(\d+(?:\.\d+)?)\s*(?:sec|second)', re.I),
                 re.compile(r'(?:sec|second)s?\.?\s*\((?:down|up) from (\d+(?:\.\d+)?)\)', re.I),
                 re.compile(r'from (\d+(?:\.\d+)?)\s+to\s+\d+(?:\.\d+)?\s*(?:sec|second)', re.I)])}


def valores(ls, lang):
    """{valor: [líneas]}: cada porcentaje ('30%') y cada cantidad de segundos ('5 s'), con las líneas donde está (una
    línea por cada vez que aparece)."""
    pcts, segs = VALOR[lang]
    out = collections.defaultdict(list)
    for l in ls:
        for unidad, rxs in (('%', pcts), (' s', segs)):
            for rx in rxs:
                for m in rx.findall(l):
                    out[m + unidad].append(l)
    return out


def diferencias(lk, le):
    """[(valor, líneas coreanas, líneas inglesas)] de los valores que aparecen más veces en una que en la otra."""
    a, b = valores(lk, 'ko'), valores(le, 'en')
    return [(v, a.get(v, []), b.get(v, [])) for v in sorted(set(a) | set(b), key=lambda v: (float(v.split('%')[0].split()[0]), v))
            if len(a.get(v, [])) != len(b.get(v, []))]


def cotejar(dir_foro, dir_cafe):
    foro = {n['id']: n for n in json.load(open(os.path.join(dir_foro, 'indice.json'), encoding='utf-8'))}
    cafe = json.load(open(os.path.join(dir_cafe, 'indice.json'), encoding='utf-8'))
    con_par = {e for k in cafe for e in k['en']}
    pares, alineados = [], 0
    for k in cafe:
        legibles = [e for e in k['en'] if 'error' not in foro[e]]
        if not legibles:
            continue
        ko = [l for l in json.load(open(os.path.join(dir_cafe, f"{k['id']}.json"), encoding='utf-8'))['lineas']
              if not IMAGEN_VIEJA.match(l)]
        en = [l for e in legibles for l in lineas(json.load(open(os.path.join(dir_foro, f'{e}.json'), encoding='utf-8'))['html'])]
        sk, se = secciones(ko), secciones(en)
        alineada = len(sk) == len(se)
        alineados += alineada
        tramos = list(zip(sk, se)) if alineada else [(('', ko), ('', en))]
        difs = [(tk, te, d) for (tk, lk), (te, le) in tramos for d in [diferencias(lk, le)] if d]
        pares.append({'ko': k, 'en': [foro[e] for e in legibles], 'alineada': alineada, 'difs': difs})
    sin_par = [n for n in foro.values() if n['id'] not in con_par]
    return pares, alineados, sin_par


def informe(pares, alineados, sin_par):
    cuentas = sum(len(d) for p in pares for _, _, d in p['difs'])
    out = ['# Notas de actualización: el inglés contra el coreano', '',
           'Generado por `scripts/cotejo_ko.py` (lo llama `scripts/build.py`). Cada nota del foro en inglés (`fuentes/foro/`) '
           'contra su par del café coreano (`fuentes/cafe/`, `scripts/cafe.py`: la de fecha más cercana, del mismo tipo a 3 '
           'días o menos o de otro a 12 horas o menos). El coreano es el original. Se comparan los porcentajes y los segundos, sección por sección cuando '
           'las dos tienen las mismas secciones (si no, la nota entera): un valor que está en una y no en la otra puede ser un '
           'error de traducción, algo que el inglés no trae o algo que una de las dos dice en una imagen. Leerlo y decidir es '
           'a mano (#3).', '',
           f'- Pares: {len(pares)}; con las mismas secciones: {alineados}. Notas en inglés sin par: {len(sin_par)}.',
           f'- Pares con diferencias: {sum(1 for p in pares if p["difs"])}; valores distintos: {cuentas}.', '',
           '## Diferencias', '']
    for p in pares:
        if not p['difs']:
            continue
        k = p['ko']
        ens = ' + '.join(f"[{n['titulo'].strip()}]({n['url']})" for n in p['en'])
        out += [f"### {fecha_ms(k['fecha'])} · [{k['titulo'].strip()}]({k['url']}) · {ens}", '']
        for tk, te, d in p['difs']:
            if not p['alineada']:
                out.append('**(la nota entera: no tienen las mismas secciones)**')
            else:
                out.append(f'**{tk}** · **{te}**' if tk or te else '**(antes de la primera sección)**')
            out.append('')
            out += ['| Valor | Coreano | Inglés |', '|---|---|---|']
            for v, lk, le in d:
                celda = lambda ls: '<br>'.join(sorted(set(l.replace('|', '\\|')[:240] for l in ls))) or '—'
                out.append(f'| {v} | {celda(lk)} | {celda(le)} |')
            out.append('')
    out += ['## Notas en inglés sin par coreana', '',
            'Ninguna nota del café del mismo tipo a 3 días o menos, ni de otro a 12 horas o menos.', '']
    out += [f"- {fecha_ms(n['fecha'])} · [{n['titulo'].strip()}]({n['url']})" + (f" ({n['error']})" if 'error' in n else '')
            for n in sorted(sin_par, key=lambda n: n['fecha'])]
    return '\n'.join(out) + '\n'


def escribir(dir_foro, dir_cafe, destino):
    with open(destino, 'w', encoding='utf-8', newline='\n') as f:
        f.write(informe(*cotejar(dir_foro, dir_cafe)))


if __name__ == '__main__':
    escribir(os.path.join(RAIZ, 'fuentes', 'foro'), os.path.join(RAIZ, 'fuentes', 'cafe'), os.path.join(RAIZ, 'docs', 'NOTAS_COREANO.md'))
    print('docs/NOTAS_COREANO.md')
