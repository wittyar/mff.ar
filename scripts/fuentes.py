#!/usr/bin/env python3
"""Transforma al modelo de la app las fuentes que no son personajes ni skills:

- thanosvibs: C.T.P.s (/api/ctps), artefactos (/api/artifacts), Alliance Battle
  (/api/abxl-data: restricciones por día y equipos recomendados), los "cancels" de la
  API de skills, los efectos de líder y de soporte (/api/supports; los liderazgos que no
  publica, desde la Leader Skill de la API de skills: scripts/liderazgos.py), las rotaciones
  de skills (/api/rotations/default) y la Beginner's Guide (/api/beginners/mff-content/1..5).
- scripts/contenido/: lo curado a mano de la guía y la wiki (guia.json, modos.json),
  con la fuente de cada bloque, y lo que Leads & Supports no publica para pasar la Leader Skill
  de la API a un liderazgo (liderazgos_api.json).
- Los bonos de equipo: la sección Team Bonus de la página de cada personaje en la wiki, y lo que se
  vio en el juego (scripts/contenido/bonos.json), que manda (scripts/bonos.py).
- La guía de armado de Cynicalex (planilla de Google), de su copia en uso en
  fuentes/guia-armado/ (la acepta o la rechaza scripts/guia_armado.py al bajarla).

Lo llama build.py y deja work/fuentes.json.

Traducción: los textos en inglés se traducen por texto exacto desde
scripts/traducciones/ (ctps, abx, guia, soportes, rotaciones, armado, bonos). Las líneas de los
artefactos cambian solo en sus números, así que se traducen por patrón
(traducciones/artefactos.json, con '#' en lugar de cada número). Lo que falta no se
inventa: viaja en inglés, la app lo marca y el build lo lista en
work/sin_traducir_fuentes.json. Los nombres de C.T.P., artefacto y modo quedan en
inglés, como los de personaje: son el identificador del juego.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dominio import TYPE, ALLIES, GENDER, SIDE, ABIL
import guia_armado as GA
from bonos import bonos as bonos_de_equipo
from strikers import strikers as strikers_de
from liderazgos import derivar as derivar_liderazgos, validar as validar_liderazgos

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


TX = Textos('ctps.json', 'abx.json', 'guia.json', 'soportes.json', 'rotaciones.json', 'armado.json', 'bonos.json')

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


# Lo que thanosvibs escribe distinto que el juego, y el build corrige porque el juego manda (Ezequiel, 5 de octubre de
# 2026). Va con aviso: el dato corregido lleva el de thanosvibs (tv) y la fuente del juego (f), y la sección 5 de
# docs/AUDITORIA.md lo lista. Nombres de C.T.P. (nombre de thanosvibs: el del juego y su fuente): la ficha de cada
# C.T.P. dice «C.T.P. of Judgment» en sus tres grados. El id sigue saliendo del nombre de thanosvibs: es la clave del
# ícono, de la guía de armado y de lo que guarda la capa.
_CTP_NOMBRE_JUEGO = {'Judgement': ('Judgment', 'juego-ctp')}


def nombre_ctp(nombre):
    """El nombre de un C.T.P. de thanosvibs como lo usa la app, y lo que lleva el dato si lo corrige (tv y f)."""
    if nombre not in _CTP_NOMBRE_JUEGO:
        return nombre, {}
    juego, f = _CTP_NOMBRE_JUEGO[nombre]
    return juego, {'tv': nombre, 'f': [f]}


def ctps(guia):
    grupo = {c: g['id'] for g in guia['ctp_ranking']['grupos'] for c in g['ctps']}
    out = []
    datos = cargar('work/ctps.json')
    for c in datos:
        cid = slug(c['name'])
        nombre, corregido = nombre_ctp(c['name'])
        if corregido:
            print(f"AVISO: C.T.P. {c['name']!r}: el juego lo escribe {nombre!r}, y se usa el del juego")
        out.append({'id': cid, 'name': nombre, 'grupo': grupo.get(cid),
                    'desc': TX(c.get('description')), 'descR': TX(c.get('description_reforged')), **corregido})
    sobran = set(_CTP_NOMBRE_JUEGO) - {c['name'] for c in datos}
    if sobran:
        print(f'AVISO: /api/ctps ya no publica {sorted(sobran)}: sobra su nombre del juego en fuentes.py (_CTP_NOMBRE_JUEGO)')
    ids = {c['id'] for c in out}
    sobran = set(grupo) - ids
    if sobran:
        raise SystemExit(f'contenido/guia.json nombra C.T.P.s que /api/ctps no publica: {sorted(sobran)}')
    sin_grupo = sorted(c['id'] for c in out if not c['grupo'])
    if sin_grupo:
        print('AVISO: C.T.P.s sin grupo en el ranking de la guía (¿nuevos?):', sin_grupo)
    return out


_SANGRIA = re.compile(r'^((?:&emsp;)*)(•\s*)?(.*)$')
# Líneas de artefacto que el juego dice distinto, como los nombres de C.T.P. (_CTP_NOMBRE_JUEGO): (artefacto, línea de
# thanosvibs): la línea del juego y su fuente. Planet Eater (Galactus): la ficha del artefacto en coreano dice «적용
# 대상: 파워 코스믹 타입인 팀원만», solo los integrantes con Poder Cósmico (captura 213 del 4 de octubre de 2026); va
# con las palabras con que thanosvibs restringe otros artefactos a una habilidad («Applies to: Allies with … Ability»).
_ARTEFACTO_LINEA_JUEGO = {('Planet Eater', 'Applies to: Self'): ('Applies to: Allies with Power Cosmic Ability', 'juego-ficha-ko')}


def linea_artefacto(artefacto, texto):
    """Una línea del texto de un artefacto como la usa la app, y lo que lleva el dato si la corrige (tv y f)."""
    if (artefacto, texto) not in _ARTEFACTO_LINEA_JUEGO:
        return texto, {}
    juego, f = _ARTEFACTO_LINEA_JUEGO[(artefacto, texto)]
    return juego, {'tv': texto, 'f': [f]}


def artefactos(retratos_base):
    """Artefacto exclusivo de cada personaje (por retrato base). El texto viene en líneas
    con marcadores [P1]..[Pn] que se llenan con los valores de cada nivel de estrellas
    (3 a 6); la sangría es la jerarquía del texto del juego (efectos dentro de una
    condición) y viaja como nivel, no como HTML."""
    out, corregidas = [], set()
    for a in cargar('work/artifacts.json'):
        if a['portrait'] not in retratos_base:
            raise SystemExit(f"artefacto {a['artifact_name']} de un retrato que no está en el roster: {a['portrait']}")
        lineas = []
        for ln in a['text']:
            m = _SANGRIA.match(ln)
            if '&' in m.group(3):
                raise SystemExit(f"artefacto {a['artifact_name']}: entidad HTML sin tratar en {ln!r}")
            texto, corregida = linea_artefacto(a['artifact_name'], m.group(3))
            if corregida:
                corregidas.add((a['artifact_name'], m.group(3)))
                print(f"AVISO: artefacto {a['artifact_name']}: el juego dice {texto!r} donde thanosvibs dice "
                      f"{m.group(3)!r}, y se usa lo del juego")
            lineas.append({'n': len(m.group(1)) // len('&emsp;'), 'b': 1 if m.group(2) else 0, 't': TXP(texto), **corregida})
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
    sobran = sorted(set(_ARTEFACTO_LINEA_JUEGO) - corregidas)
    if sobran:
        print(f'AVISO: /api/artifacts ya no publica {sobran}: sobra su línea del juego en fuentes.py (_ARTEFACTO_LINEA_JUEGO)')
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


def nombres_pj(chars):
    """El personaje de cada retrato, como lo nombra el roster (el de su base): la restricción de un liderazgo que
    la Leader Skill da a «Self» (scripts/liderazgos.py)."""
    base = {r['portrait']: r['character'] for r in chars if r['uniformed'] == 'False'}
    return {r['portrait']: base[r['base_portrait']] for r in chars}


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


def guia_armado(chars):
    """La guía de armado de Cynicalex, de la copia en uso: por retrato del mejor uniforme
    de cada personaje, con la leyenda que usa la app y el estado de la última comprobación.
    Los C.T.P. van por id (los de /api/ctps); lo que no se entiende viaja crudo y se lista."""
    try:
        r = GA.leer(GA.texto_en_uso('armado'), GA.texto_en_uso('tierlist'), chars, cargar('work/ctps.json'))
    except GA.Incompatible as e:
        raise SystemExit('la copia en uso de la guía de armado (fuentes/guia-armado/) no se puede leer: '
                         + '; '.join(e.motivos))
    for e in r['pj'].values():
        for x in e.get('iso', []) + e.get('ob', []):
            TX(x)
        if 'art' in e:
            TX(e['art']['t'])
        if 'nota' in e:
            TX(e['nota'])
    sets = dict(GA.LEY_ISO_SET)
    leyenda = {
        'adq': dict(GA.LEY_ADQ),
        'art': [[k, TX(v)] for k, v in GA.LEY_ART],
        'rot': [[k, TX(v)] for k, v in GA.LEY_ROT],
        'ctp': [TX(x) for x in GA.LEY_CTP],
        'iso': {cat: [sets[x] for x in xs] for cat, xs in GA.LEY_ISO_CAT},
        'emojis': {k: TX(v) for k, v in r['emojis'].items()},
    }
    if r['sin_pj']:
        print('AVISO guía de armado: filas sin personaje en thanosvibs:', r['sin_pj'])
    if r['raros']:
        print('AVISO guía de armado: valores que no se interpretan:', r['raros'])
    return {'version': r['version'], 'estado': GA.estado(), 'leyenda': leyenda, 'pj': r['pj'],
            'sin_pj': r['sin_pj'], 'raros': r['raros']}


def bonos(paginas, chars, juego):
    """Los bonos de equipo (scripts/bonos.py) y su auditoría, con los nombres de sus stats
    traducidos. Los integrantes van por nombre de personaje: build.py los pasa a sus ids.
    paginas: las páginas de los personajes en la wiki (work/wikitext)."""
    B = bonos_de_equipo(paginas, [r['character'] for r in chars if r['uniformed'] == 'False'], juego)
    for b in B['bonos']:
        for version in b['v']:
            for stat, _ in version:
                TX(stat)
    return B['bonos'], B['auditoria']


def strikers(paginas, chars):
    """Los strikers de cada personaje (scripts/strikers.py) y su auditoría. Van por nombre de
    personaje: build.py los pasa a sus ids."""
    S = strikers_de(paginas, [r['character'] for r in chars if r['uniformed'] == 'False'])
    return S['strikers'], S['auditoria']


def validar_contenido(guia, modos, bonos_juego, listas, stats_ok):
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
    recorrer(guia); recorrer(modos); recorrer(bonos_juego)
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
    bonos_juego = cargar(os.path.join(_DIR, 'contenido', 'bonos.json'))
    validar_contenido(guia, modos, bonos_juego, listas, set(guia['stats']))
    malas = sorted({f for _, f in [*_CTP_NOMBRE_JUEGO.values(), *_ARTEFACTO_LINEA_JUEGO.values()]} - set(guia['fuentes']))
    if malas:
        raise SystemExit(f'fuentes.py corrige con fuentes sin definir en contenido/guia.json: {malas}')
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
    sop = soportes(retratos, {r['character'] for r in chars})
    # Los liderazgos que Leads & Supports no publica, desde la Leader Skill de la API (Ezequiel, 4 de octubre de
    # 2026), con "src": "api". Van en una entrada nueva: la de Leads & Supports puede ser de varios retratos.
    a_mano = cargar(os.path.join(_DIR, 'contenido', 'liderazgos_api.json'))
    mal = validar_liderazgos(a_mano, skills['tablas'], cargar(os.path.join(_DIR, 'contenido', 'catalogo.json')))
    mal = mal or [f'el «Give Power» de {o["p"]}: fuente sin definir en contenido/guia.json: {k}'
                  for o in a_mano['otorga'] for k in o['fuente'] if k not in guia['fuentes']]
    if mal:
        raise SystemExit('scripts/contenido/liderazgos_api.json tiene errores:\n  ' + '\n  '.join(mal))
    liderazgos = derivar_liderazgos(sop, skills['skills'], skills['tablas'], nombres_pj(chars), a_mano)
    for a in liderazgos['a_mano']['avisos']:
        print(f'AVISO: scripts/contenido/liderazgos_api.json: {a}')
    for p, slots in liderazgos['derivados'].items():
        sop[p] = {**sop.get(p, {}), **slots}
    # Las activaciones que van con el texto de la API, con su traducción de la API (o sin traducir, y se lista).
    for en, es in liderazgos['textos'].items():
        if es is None:
            TX.faltan.add(en)
        else:
            TX.usados[en] = es
    salida = {
        'ctps': ctps(guia),
        'artefactos': artefactos(base),
        'abx': abx(retratos),
        'cancels': skills.get('cancels', {}),
        'soportes': sop,
        'liderazgos_auditoria': liderazgos,
        'rotaciones': rotaciones(retratos),
        'guia_pj': guia_personajes(retratos, modos['modos']),
        'guia': guia, 'modos': modos['modos'], 'version_guia_fuente': version_fuente,
        'armado': guia_armado(chars),
    }
    paginas = [cargar(f) for f in sorted(glob.glob('work/wikitext/*.json'))]
    salida['bonos'], salida['bonos_auditoria'] = bonos(paginas, chars, bonos_juego)
    salida['strikers'], salida['strikers_auditoria'] = strikers(paginas, chars)
    salida['txt'] = dict(sorted(TX.usados.items()))
    json.dump(salida, open('work/fuentes.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(sorted(TX.faltan), open('work/sin_traducir_fuentes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"fuentes: {len(salida['ctps'])} C.T.P.s | {len(salida['artefactos'])} artefactos | "
          f"ABX {len(salida['abx']['restricciones'])} restricciones, {len(salida['abx']['equipos'])} equipos | "
          f"soportes de {len(salida['soportes'])} retratos (liderazgo de la Leader Skill de la API: "
          f"{len(liderazgos['derivados'])} retratos, {len(liderazgos['sin_derivar'])} slots sin derivar) | "
          f"rotaciones de {len(salida['rotaciones'])} retratos | "
          f"guía: {len(salida['guia_pj'])} personajes mencionados | guía de armado {salida['armado']['version']}: "
          f"{len(salida['armado']['pj'])} personajes | bonos de equipo {len(salida['bonos'])} | "
          f"strikers de {len(salida['strikers'])} personajes | "
          f"textos traducidos {len(salida['txt'])}, "
          f"sin traducir {len(TX.faltan)}")


if __name__ == '__main__':
    main()
