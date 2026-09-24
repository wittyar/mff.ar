#!/usr/bin/env python3
"""Transforma al modelo de la app las fuentes que no son personajes ni skills:

- thanosvibs: C.T.P.s (/api/ctps), artefactos (/api/artifacts), Alliance Battle
  (/api/abxl-data: restricciones por día y equipos recomendados), los "cancels" de la
  API de skills y la Beginner's Guide (/api/beginners/mff-content/1..5).
- scripts/contenido/: lo curado a mano de la guía y la wiki (guia.json, modos.json),
  con la fuente de cada bloque.

Lo llama build.py y deja work/fuentes.json.

Traducción: los textos en inglés se traducen por texto exacto desde
scripts/traducciones/ (ctps.json, abx.json, guia.json). Lo que falta no se inventa:
viaja en inglés, la app lo marca y el build lo lista en work/sin_traducir_fuentes.json.
Los nombres de C.T.P., artefacto y modo quedan en inglés, como los de personaje: son el
identificador del juego.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dominio import TYPE, ALLIES, GENDER, SIDE

_DIR = os.path.dirname(os.path.abspath(__file__))


def slug(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


class Textos:
    """Traducción por texto exacto. Registra lo usado (viaja en MFF_TXT) y lo que falta."""
    def __init__(self, *archivos):
        self.tabla = {}
        for a in archivos:
            self.tabla.update(json.load(open(os.path.join(_DIR, 'traducciones', a), encoding='utf-8')))
        self.usados, self.faltan = {}, set()

    def __call__(self, en):
        en = (en or '').strip()
        if not en:
            return en
        es = self.tabla.get(en)
        if es is None:
            self.faltan.add(en)
        else:
            self.usados[en] = es
        return en


TX = Textos('ctps.json', 'abx.json', 'guia.json')


def cargar(ruta):
    return json.load(open(ruta, encoding='utf-8'))


def ctps(guia):
    grupo = {c: g['id'] for g in guia['ctp_ranking']['grupos'] for c in g['ctps']}
    out = []
    for c in cargar('work/ctps.json'):
        cid = slug(c['name'])
        out.append({'id': cid, 'name': c['name'], 'grupo': grupo.get(cid),
                    'desc': TX(c.get('description')), 'descR': TX(c.get('description_reforged'))})
    ids = {c['id'] for c in out}
    sobran = set(grupo) - ids
    if sobran:
        raise SystemExit(f'contenido/guia.json nombra C.T.P.s que /api/ctps no publica: {sorted(sobran)}')
    sin_grupo = sorted(c['id'] for c in out if not c['grupo'])
    if sin_grupo:
        print('AVISO: C.T.P.s sin grupo en el ranking de la guía (¿nuevos?):', sin_grupo)
    return out


def artefactos(retratos_base):
    out = []
    for a in cargar('work/artifacts.json'):
        if a['portrait'] not in retratos_base:
            raise SystemExit(f"artefacto {a['artifact_name']} de un retrato que no está en el roster: {a['portrait']}")
        out.append({'p': a['portrait'], 'name': a['artifact_name'], 'pasiva': a['passive_name'],
                    'pve': a['pve_score'], 'pvp': a['pvp_score'], 'desde': a['update']})
    return out


# Palabras de las restricciones de Alliance Battle -> valor del dominio en la app.
_RESTR = {**TYPE, **GENDER, **ALLIES, 'Hero': SIDE['Super Hero'], 'Villain': SIDE['Super Villain']}


def restriccion(texto):
    if texto == 'No Restriction':
        return []
    tokens = texto.split()
    faltan = [t for t in tokens if t not in _RESTR]
    if faltan:
        raise SystemExit(f'restricción de Alliance Battle con palabras desconocidas: {texto!r} ({faltan})')
    return [_RESTR[t] for t in tokens]


def abx(retratos):
    d = cargar('work/abxl.json')
    restr = [{'d': r['day'], 'm': r['mode'], 'r': restriccion(r['restriction'])} for r in d['restrictions']]
    equipos = []
    for t in d['teams']:
        pj = [t['char1'], t['char2'], t['char3']]
        faltan = [p for p in pj if p not in retratos]
        if faltan:
            print(f"AVISO: equipo de Alliance Battle (día {t['day']}, {t['mode']}) con retratos que no están en el roster: {faltan}")
            continue
        equipos.append({'d': t['day'], 'm': t['mode'], 'r': restriccion(t['restriction']),
                        'titulo': TX(t.get('title')), 'pj': pj, 'lider': t['leader'], 'dps': t['dps'],
                        'v': t.get('version_added')})
    return {'restricciones': restr, 'equipos': equipos}


def guia_personajes(retratos, modos):
    """Dónde recomienda la guía a cada personaje (partes 1 y 2, secciones de personajes):
    sección, C.T.P.s sugeridos y el texto de uso. Las etiquetas de modo son derivadas:
    salen de buscar en la sección y el texto las palabras clave de cada modo."""
    claves = [(m['id'], [k.lower() for k in m.get('claves_guia', [])]) for m in modos]
    out = {}
    for parte in (1, 2):
        sec = sub = None
        cur = None
        for ln in open(f'work/guia/parte{parte}.txt', encoding='utf-8').read().split('\n'):
            f = ln.split('||')
            tag = f[0]
            if tag == 'c':
                sec, sub, cur = f[3], None, None
                continue
            if tag == 'h':
                sub, cur = f[1], None
                continue
            if not (sec or '').startswith('Characters - '):
                continue
            nuevo = None
            if tag in ('p', 'lp') and len(f) >= 4 and f[2] in retratos:
                nuevo = {'p': f[2], 'textos': []}
            elif tag == 'eqb' and len(f) >= 7 and f[3] in retratos:
                nuevo = {'p': f[3], 'textos': [f[6]]}
            elif tag == 'colimg':
                for m in re.finditer(r'\(([^,()]+),([^,()]+)\)', ln):
                    if m.group(1) in retratos:
                        out.setdefault(m.group(1), []).append({'parte': parte, 'sec': TX(sec), 'sub': TX(sub),
                                                               'ctps': [], 'textos': [], 'modos': []})
                cur = None
                continue
            elif cur and tag == 'subp' and len(f) >= 3:
                if f[2].startswith('ctp_'):
                    cur['ctps'].append(f[2][4:])
                elif f[2] == '6obelisk':
                    cur['ctps'].append('obelisco6')
                continue
            elif cur and tag == 'pt':
                cur['textos'].append(f[1])
                continue
            elif cur and tag == 'eqbrt' and len(f) >= 7 and f[5] == 'Usefulness':
                cur['textos'].append(f[6])
                continue
            if nuevo:
                cur = {'parte': parte, 'sec': TX(sec), 'sub': TX(sub), 'ctps': [], 'textos': nuevo['textos'], 'modos': []}
                out.setdefault(nuevo['p'], []).append(cur)
                if tag == 'eqb':
                    cur = None
    for entradas in out.values():
        for e in entradas:
            e['textos'] = [TX(x) for x in e['textos']]
            pajar = ' '.join([e['sec'] or '', e['sub'] or ''] + e['textos']).lower()
            e['modos'] = [mid for mid, ks in claves if any(k in pajar for k in ks)]
    return out


def validar_contenido(guia, modos, listas, stats_ok):
    """Las claves que usa lo curado a mano tienen que existir: una fuente mal escrita o un
    stat inexistente se mostraría vacío en la app sin que nadie se entere."""
    fuentes = set(guia['fuentes'])
    malas = set()
    def fu(x):
        for k in (x or []):
            if k not in fuentes:
                malas.add(k)
    def recorrer(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.endswith('fuente') and isinstance(v, list):
                    fu(v)
                else:
                    recorrer(v)
        elif isinstance(o, list):
            for v in o:
                recorrer(v)
    recorrer(guia); recorrer(modos)
    if malas:
        raise SystemExit(f'fuentes sin definir en contenido/guia.json: {sorted(malas)}')
    usados = set()
    def st(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ('stats', 'prioridad', 'pool', 'mejor') and isinstance(v, list):
                    usados.update(x for x in v if x != 'ataque')
                else:
                    st(v)
        elif isinstance(o, list):
            for v in o:
                st(v)
    st(guia)
    malos = usados - stats_ok
    if malos:
        raise SystemExit(f'stats sin definir en contenido/guia.json: {sorted(malos)}')
    for m in modos['modos']:
        faltan = [l for l in m.get('listas', []) if l not in listas]
        if faltan:
            print(f"AVISO: el modo {m['id']} referencia listas que no se importaron: {faltan}")


def main():
    chars = cargar('work/characters.json')
    base = {r['base_portrait'] for r in chars}
    retratos = {r['portrait'] for r in chars} | base
    guia = cargar(os.path.join(_DIR, 'contenido', 'guia.json'))
    modos = cargar(os.path.join(_DIR, 'contenido', 'modos.json'))
    listas = {json.load(open(f, encoding='utf-8'))['slug'] for f in glob.glob('work/tierlists/*.json')}
    validar_contenido(guia, modos, listas, set(guia['stats']))
    # La guía curada se escribió sobre una versión; si thanosvibs publica otra, se avisa
    # para revisarla (y la app lo muestra), en vez de mostrar recomendaciones viejas como vigentes.
    version_fuente = cargar('work/guia/changelog.json')[0]['update_version']
    if version_fuente != guia['version_guia']:
        print(f"AVISO: la Beginner's Guide de thanosvibs pasó a {version_fuente} y contenido/guia.json "
              f"está escrito sobre {guia['version_guia']}: revisarlo")
    # Los tipos de control que cortan a los jefes de Alliance Battle se muestran traducidos.
    for m in modos['modos']:
        for tipos in (m.get('cancels') or {}).values():
            for x in tipos:
                TX(x)
    skills = cargar('work/skills_parsed.json')
    salida = {
        'ctps': ctps(guia),
        'artefactos': artefactos(base),
        'abx': abx(retratos),
        'cancels': skills.get('cancels', {}),
        'guia_pj': guia_personajes(retratos, modos['modos']),
        'guia': guia, 'modos': modos['modos'], 'version_guia_fuente': version_fuente,
    }
    salida['txt'] = dict(sorted(TX.usados.items()))
    json.dump(salida, open('work/fuentes.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(sorted(TX.faltan), open('work/sin_traducir_fuentes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"fuentes: {len(salida['ctps'])} C.T.P.s | {len(salida['artefactos'])} artefactos | "
          f"ABX {len(salida['abx']['restricciones'])} restricciones, {len(salida['abx']['equipos'])} equipos | "
          f"guía: {len(salida['guia_pj'])} personajes mencionados | textos traducidos {len(salida['txt'])}, "
          f"sin traducir {len(TX.faltan)}")


if __name__ == '__main__':
    main()
