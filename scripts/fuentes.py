#!/usr/bin/env python3
"""Transforma al modelo de la app las fuentes que no son personajes ni skills:

- thanosvibs: C.T.P.s (/api/ctps), artefactos (/api/artifacts), Alliance Battle
  (/api/abxl-data: restricciones por día y equipos recomendados), los "cancels" de la
  API de skills, los efectos de líder y de soporte (/api/supports), las rotaciones de
  skills (/api/rotations/default) y la Beginner's Guide (/api/beginners/mff-content/1..5).
- scripts/contenido/: lo curado a mano de la guía y la wiki (guia.json, modos.json),
  con la fuente de cada bloque.

Lo llama build.py y deja work/fuentes.json.

Traducción: los textos en inglés se traducen por texto exacto desde
scripts/traducciones/ (ctps, abx, guia, soportes, rotaciones). Las líneas de los
artefactos cambian solo en sus números, así que se traducen por patrón
(traducciones/artefactos.json, con '#' en lugar de cada número). Lo que falta no se
inventa: viaja en inglés, la app lo marca y el build lo lista en
work/sin_traducir_fuentes.json. Los nombres de C.T.P., artefacto y modo quedan en
inglés, como los de personaje: son el identificador del juego.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dominio import TYPE, ALLIES, GENDER, SIDE, ABIL

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


TX = Textos('ctps.json', 'abx.json', 'guia.json', 'soportes.json', 'rotaciones.json')

# Números de una línea de artefacto: los marcadores [P1]..[Pn] (el valor según las
# estrellas) y los números literales. El patrón es la línea con '#' en cada uno.
_NUM = re.compile(r'\[P\d+\]|\d+(?:\.\d+)?')


class Patrones:
    """Traducción por patrón de las líneas de artefacto: la tabla trae la línea con '#'
    en lugar de cada número, en el mismo orden en los dos idiomas; la traducción de
    cada línea concreta se registra en TX, que es lo que viaja a la app."""
    def __init__(self, archivo):
        tabla = json.load(open(os.path.join(_DIR, 'traducciones', archivo), encoding='utf-8'))
        # La fuente escribe igual una misma frase con mayúsculas distintas
        # ("total Instinct" / "Total Instinct"): el patrón se busca sin distinguirlas.
        self.tabla = {k.casefold(): v for k, v in tabla.items()}

    def __call__(self, en):
        en = (en or '').strip()
        if not en:
            return en
        nums = _NUM.findall(en)
        es = self.tabla.get(_NUM.sub('#', en).casefold())
        if es is None:
            TX.faltan.add(en)
            return en
        partes = es.split('#')
        if len(partes) - 1 != len(nums):
            raise SystemExit(f'traducciones/artefactos.json: la traducción de {en!r} no tiene '
                             f'{len(nums)} marcadores "#": {es!r}')
        TX.usados[en] = partes[0] + ''.join(n + p for n, p in zip(nums, partes[1:]))
        return en


TXP = Patrones('artefactos.json')


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


_SANGRIA = re.compile(r'^((?:&emsp;)*)(•\s*)?(.*)$')


def artefactos(retratos_base):
    """Artefacto exclusivo de cada personaje (por retrato base). El texto viene en líneas
    con marcadores [P1]..[Pn] que se llenan con los valores de cada nivel de estrellas
    (3 a 6); la sangría es la jerarquía del texto del juego (efectos dentro de una
    condición) y viaja como nivel, no como HTML."""
    out = []
    for a in cargar('work/artifacts.json'):
        if a['portrait'] not in retratos_base:
            raise SystemExit(f"artefacto {a['artifact_name']} de un retrato que no está en el roster: {a['portrait']}")
        lineas = []
        for ln in a['text']:
            m = _SANGRIA.match(ln)
            if '&' in m.group(3):
                raise SystemExit(f"artefacto {a['artifact_name']}: entidad HTML sin tratar en {ln!r}")
            lineas.append({'n': len(m.group(1)) // len('&emsp;'), 'b': 1 if m.group(2) else 0, 't': TXP(m.group(3))})
        # La fuente trae niveles sin valores (o con menos de los que usa el texto) en
        # algunos artefactos: se avisa y la app marca cada número que falta.
        usados = {int(x[2:-1]) for ln in lineas for x in re.findall(r'\[P\d+\]', ln['t'])}
        cortos = [f"{est}★ ({len(vals)} de {max(usados)})" for est, vals in sorted(a['values'].items())
                  if usados and max(usados) > len(vals)]
        if cortos:
            print(f"AVISO: artefacto {a['artifact_name']} ({a['character']}): la fuente no trae todos los valores en {', '.join(cortos)}")
        out.append({'p': a['portrait'], 'name': a['artifact_name'], 'pasiva': a['passive_name'],
                    'pve': a['pve_score'], 'pvp': a['pvp_score'], 'desde': a['update'],
                    'lineas': lineas, 'valores': a['values'], 'obtencion': [TXP(x) for x in a['acquisition']]})
    return out


# Efectos de /api/supports. Formato de la fuente (según el sitio de thanosvibs, que los
# muestra así): [efecto], [efecto, valor %] o [efecto, valor %, duración s | condición];
# en dos efectos sin valor, el segundo número es la duración. Los del artefacto exclusivo
# vienen por nivel de estrellas (effect3..effect6) como [efecto, valor %, % del instinto
# total] con la duración al final ([..., duración]) y, si acumula, el tope antes
# ([..., tope %, duración]); la wiki (página Artifact) lo confirma para Robbie Reyes y
# She-Hulk. Acá se pasan a objetos con nombre para que la app no dependa de posiciones.
_SOLO_DURACION = {'Remove All Debuffs', 'Debuff Immunity'}
_TIPOS_SOPORTE = ('leader', 'leader2', 'passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact')
# Restricción -> valor del dominio de la app, por categoría.
_RESTR_SOPORTE = {
    'Ability': ABIL, 'Type': TYPE, 'Allies': ALLIES,
    'Side': {'Hero': SIDE['Super Hero'], 'Villain': SIDE['Super Villain']},
}
# La fuente clasifica mal dos restricciones: "Zombie" no es una clase ni "Fantastic Four"
# una raza; las dos son habilidades. Se corrigen con aviso y la app muestra la original.
_RESTR_CORREGIDA = {('Type', 'Zombie'): 'Ability', ('Allies', 'Fantastic Four'): 'Ability'}
# Nombres de personaje que la fuente abrevia en las restricciones -> nombre en el roster.
_ALIAS_PJ = {'Kang': 'Kang the Conqueror'}


def _efecto_soporte(e, donde):
    s = e[0]
    if len(e) == 1:
        return {'s': TX(s)}
    if len(e) == 2:
        return {'s': TX(s), 'd': e[1]} if s in _SOLO_DURACION else {'s': TX(s), 'v': _valor(e[1])}
    if len(e) == 3:
        x = {'s': TX(s), 'v': _valor(e[1])}
        if isinstance(e[2], str):
            x['c'] = TX(e[2])
        else:
            x['d'] = e[2]
        return x
    raise SystemExit(f'soporte {donde}: efecto con forma desconocida {e!r}')


def _valor(v):
    return TX(v) if isinstance(v, str) else v


def _efecto_artefacto(e, donde):
    if len(e) not in (3, 4, 5):
        raise SystemExit(f'soporte {donde}: efecto de artefacto con forma desconocida {e!r}')
    x = {'s': TX(e[0]), 'v': e[1], 'i': e[2]}
    if len(e) == 4:
        x['d'] = e[3]
    if len(e) == 5:
        x['tope'], x['d'] = e[3], e[4]
    return x


def soportes(retratos, nombres):
    """Lo que un personaje le da al equipo, por retrato: liderazgo, pasiva de 4★, pasiva
    de Tier-2, efecto de uniforme y habilidad exclusiva del artefacto, con a quién se
    aplica. Cada entrada de la fuente vale también para los retratos de 'sameas'."""
    out, origen = {}, {}
    for s in cargar('work/supports.json'):
        e = {}
        if s['new_player_pick']:
            e['np'] = 1
        for tipo in _TIPOS_SOPORTE:
            v = s[tipo]
            if not v:
                continue
            donde = f"{s['portrait']}/{tipo}"
            x = {}
            if v.get('name'):
                x['n'] = v['name']
            if v.get('significant'):
                x['sig'] = 1
            r = v.get('restrictions') or []
            if r:
                cat, val = r
                if (cat, val) in _RESTR_CORREGIDA:
                    nueva = _RESTR_CORREGIDA[(cat, val)]
                    print(f'AVISO: soporte {donde}: la fuente restringe por {cat} "{val}", que es {nueva}; se usa {nueva}')
                    x['rc'] = [cat, val]
                    cat = nueva
                if cat == 'Character':
                    if val in _ALIAS_PJ:
                        print(f'AVISO: soporte {donde}: la fuente restringe al personaje "{val}"; en el roster es "{_ALIAS_PJ[val]}"')
                        x['rc'] = [cat, val]
                        val = _ALIAS_PJ[val]
                    if val not in nombres:
                        raise SystemExit(f'soporte {donde}: restringe al personaje {val!r}, que no está en el roster')
                    x['r'] = [cat, val]
                elif val in _RESTR_SOPORTE.get(cat, {}):
                    x['r'] = [cat, _RESTR_SOPORTE[cat][val]]
                else:
                    raise SystemExit(f'soporte {donde}: restricción desconocida {r!r}')
            if v.get('activation'):
                x['ac'] = TX(v['activation'])
            if v.get('cooltime'):
                x['cd'] = v['cooltime']
            if v.get('duration'):
                x['d'] = v['duration']
            if v.get('requirement'):
                x['req'] = TX(v['requirement'])
            if 'effect' in v:
                x['fx'] = [_efecto_soporte(ef, donde) for ef in v['effect']]
            else:
                # Del artefacto se guarda el nivel máximo (6★): el detalle por estrellas
                # está en el artefacto (MFF_ARTEFACTOS), que trae el texto completo.
                x['fx'] = [_efecto_artefacto(ef, donde) for ef in v['effect6']]
                x['est'] = 6
            desconocidos = set(v) - {'name', 'significant', 'restrictions', 'activation', 'cooltime',
                                     'duration', 'requirement', 'effect', 'effect3', 'effect4', 'effect5', 'effect6'}
            if desconocidos:
                raise SystemExit(f'soporte {donde}: campos que la app no conoce: {sorted(desconocidos)}')
            e[tipo] = x
        for p in [s['portrait']] + s['sameas']:
            if p not in retratos:
                print(f"AVISO: soporte de {s['portrait']} para un retrato que no está en el roster: {p}")
                continue
            if p in out and out[p] is not e:
                raise SystemExit(f"soporte: el retrato {p} tiene dos entradas ({origen[p]} y {s['portrait']})")
            out[p], origen[p] = e, s['portrait']
    return out


# Una descripción de rotación que es solo notación (números, c/dc/qc/h, negritas,
# paréntesis) no tiene nada que traducir.
_SOLO_NOTACION = re.compile(r'^[\s\*\d\(\)cdqhk,\.\-/→>]*$')


def rotaciones(retratos):
    """Rotaciones de skills por retrato, en el orden de la fuente, con su categoría
    (General, Proc o Rage) y su nombre."""
    out = {}
    for r in cargar('work/rotations.json'):
        p = r['character_id']
        if p not in retratos:
            print(f"AVISO: rotación de un retrato que no está en el roster: {p}")
            continue
        if r['category'] not in ('General', 'Proc', 'Rage'):
            raise SystemExit(f"rotación {r['id']} con categoría desconocida {r['category']!r}")
        d = r['description'].strip()
        x = {'cat': r['category'], 'nom': TX(r['rotation_name'])}
        if _SOLO_NOTACION.match(d.replace('**', '')):
            x['desc'], x['n'] = d, 1        # 'n': solo notación, se muestra igual en los dos idiomas
        else:
            x['desc'] = TX(d)
        out.setdefault(p, []).append(x)
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
    li = guia['ctp_ranking']['lista_ideal']
    if li['id'] not in listas:
        print(f"AVISO: contenido/guia.json usa la lista {li['nombre']} ({li['id']}), que no se importó: "
              f"la ficha no va a mostrar su C.T.P. ideal")


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
        'soportes': soportes(retratos, {r['character'] for r in chars}),
        'rotaciones': rotaciones(retratos),
        'guia_pj': guia_personajes(retratos, modos['modos']),
        'guia': guia, 'modos': modos['modos'], 'version_guia_fuente': version_fuente,
    }
    salida['txt'] = dict(sorted(TX.usados.items()))
    json.dump(salida, open('work/fuentes.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(sorted(TX.faltan), open('work/sin_traducir_fuentes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"fuentes: {len(salida['ctps'])} C.T.P.s | {len(salida['artefactos'])} artefactos | "
          f"ABX {len(salida['abx']['restricciones'])} restricciones, {len(salida['abx']['equipos'])} equipos | "
          f"soportes de {len(salida['soportes'])} retratos | rotaciones de {len(salida['rotaciones'])} retratos | "
          f"guía: {len(salida['guia_pj'])} personajes mencionados | textos traducidos {len(salida['txt'])}, "
          f"sin traducir {len(TX.faltan)}")


if __name__ == '__main__':
    main()
