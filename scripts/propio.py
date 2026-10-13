#!/usr/bin/env python3
"""Contenido propio sobre lo bajado de thanosvibs (Ezequiel, 13 de octubre de 2026: «me gustaría poder empezar a generar
mi propio contenido y luego apoyarme en thanosvibs como confirmación»).

fuentes/propio/ trae, de las fuentes del juego (las notas de los foros oficiales en inglés y en coreano), lo que thanosvibs
todavía no publica o publica distinto, en sus mismas formas:
  personajes.json   filas de /api/characters (nuevas o en lugar de las de thanosvibs), cambios de campos sobre las de
                    thanosvibs, entradas de /api/uniforms y de /api/updates, e instintos.
  skills/<p>.json   las skills de un retrato como /api/skills: las de otro retrato (desde, el de thanosvibs) con los slots
                    que el juego cambia o agrega encima (slots).
  artefactos.json   filas de /api/artifacts.      ctps.json   filas de /api/ctps.
  retratos/<p>.png  el retrato, de la ficha de la nota.

Lo propio manda: este script lo pone en work/ antes del build (build.py lo corre primero), guardando en cada dato que
reemplaza el de thanosvibs (_propio.tv, o null si thanosvibs no lo tenía), y al empezar deshace lo de la vez anterior: se
puede correr las veces que haga falta sobre la misma bajada. Cuando thanosvibs publica lo mismo, compara: lo que coincide
queda confirmado y lo que difiere va a work/propio.json, que auditar.py pone en docs/AUDITORIA.md (sección 13), junto con
los campos que las fuentes no dicen (sin_confirmar). Las fuentes de cada dato tienen que estar en contenido/guia.json.
Solo biblioteca estándar."""
import copy, glob, json, os, re, shutil

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PROPIO = os.path.join(RAIZ, 'fuentes', 'propio')
W = os.path.join(RAIZ, 'work')
IMAGENES = os.path.join(RAIZ, 'images', 'propio')
GUIA = os.path.join(RAIZ, 'scripts', 'contenido', 'guia.json')
MARCA = '_propio'
# Lo que el contenido propio agrega a una fila y que thanosvibs no tiene: sin_confirmar y notas no entran en la fila; la
# fuente sí (la app dice de dónde sale lo propio), pero no se compara.
META = ('sin_confirmar', 'notas')


def cargar(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


def escribir(ruta, x):
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(x, f, ensure_ascii=False)


def sin_meta(x):
    return {k: v for k, v in x.items() if k not in META}


# -- deshacer lo de la vez anterior -----------------------------------------------------------------------------------
def restaurar_lista(ruta):
    """Una lista de work/ sin lo propio: cada fila marcada vuelve a la de thanosvibs, o sale si thanosvibs no la tenía."""
    out = []
    for x in cargar(ruta):
        if isinstance(x, dict) and MARCA in x:
            if x[MARCA]['tv'] is not None:
                out.append(x[MARCA]['tv'])
        else:
            out.append(x)
    escribir(ruta, out)


def restaurar_dict(ruta):
    d = cargar(ruta)
    for k in [k for k, v in d.items() if isinstance(v, dict) and MARCA in v]:
        if d[k][MARCA]['tv'] is None:
            del d[k]
        else:
            d[k] = d[k][MARCA]['tv']
    escribir(ruta, d)


def restaurar_updates(ruta):
    out = []
    for v in cargar(ruta):
        if MARCA in v:
            continue
        for k in ('characters', 'uniforms', 't3s', 't4s'):
            if v.get(k):
                v[k] = [x for x in v[k] if MARCA not in x]
        out.append(v)
    escribir(ruta, out)


def restaurar_skills():
    for f in glob.glob(os.path.join(W, 'skills_api', '*.json')):
        d = cargar(f)
        if MARCA in d:
            if d[MARCA]['tv'] is None:
                os.remove(f)
            else:
                escribir(f, d[MARCA]['tv'])


def restaurar():
    restaurar_lista(os.path.join(W, 'characters.json'))
    restaurar_lista(os.path.join(W, 'artifacts.json'))
    restaurar_lista(os.path.join(W, 'ctps.json'))
    restaurar_dict(os.path.join(W, 'uniforms.json'))
    restaurar_dict(os.path.join(W, 'instintos.json'))
    restaurar_updates(os.path.join(W, 'updates.json'))
    restaurar_skills()


# -- comparar con thanosvibs ------------------------------------------------------------------------------------------
def norm(s):
    return re.sub(r'\s+', ' ', re.sub(r'</?b>|\^', '', s or '')).strip()


def huella_skill(sk):
    """Lo que se compara de una skill: nombre, recarga y cada efecto (etiqueta, texto y duración), sin orden ni golpes
    repetidos (thanosvibs repite la etapa de daño por golpe; la ficha de la nota no dice cuántos golpes da)."""
    fx = sorted({(a.get('abilityId'), norm(a.get('description')), a.get('duration'))
                 for st in sk.get('stages', []) for a in st.get('abils', [])}, key=str)
    return {'name': sk.get('name'), 'cooldown': sk.get('cooldown'), 'fx': fx}


def diferencias(propio, tv, campos=None):
    ks = [k for k in (campos or sorted(set(propio) | set(tv))) if k != 'fuente']
    return [f'{k}: propio {propio.get(k)!r}, thanosvibs {tv.get(k)!r}' for k in ks if propio.get(k) != tv.get(k)]


# -- aplicar ----------------------------------------------------------------------------------------------------------
def main():
    restaurar()
    guia = cargar(GUIA)['fuentes']
    P = cargar(os.path.join(PROPIO, 'personajes.json'))
    A = cargar(os.path.join(PROPIO, 'artefactos.json'))
    T = cargar(os.path.join(PROPIO, 'ctps.json'))
    S = {os.path.basename(f)[:-5]: cargar(f) for f in sorted(glob.glob(os.path.join(PROPIO, 'skills', '*.json')))}
    informe = {'aplicado': [], 'confirmado': [], 'difiere': [], 'sin_confirmar': []}

    # Las fuentes de todo, en la guía.
    def fuentes(x, donde):
        if not x.get('fuente'):
            raise SystemExit(f'fuentes/propio: {donde} sin fuente')
        malas = [k for k in x['fuente'] if k not in guia]
        if malas:
            raise SystemExit(f'fuentes/propio: {donde}: fuente sin definir en contenido/guia.json: {malas}')
        for c in x.get('sin_confirmar', []):
            informe['sin_confirmar'].append(f'{donde}: {c}')

    # Personajes y uniformes.
    ruta = os.path.join(W, 'characters.json')
    filas = cargar(ruta)
    por_p = {r['portrait']: i for i, r in enumerate(filas)}
    for r in P['filas']:
        p = r['portrait']
        fuentes(r, f'personaje {p}')
        nueva = sin_meta(r)
        if p in por_p:
            tv = filas[por_p[p]]
            d = diferencias(nueva, tv)
            (informe['difiere'] if d else informe['confirmado']).append(f'personaje {p}' + (': ' + '; '.join(d) if d else ''))
            filas[por_p[p]] = {**nueva, MARCA: {'tv': tv}}
        else:
            filas.append({**nueva, MARCA: {'tv': None}})
            informe['aplicado'].append(f'personaje {p} (thanosvibs no lo publica)')
    for c in P['cambios']:
        p = c['portrait']
        fuentes(c, f'cambio en {p}')
        if p not in por_p:
            raise SystemExit(f'fuentes/propio/personajes.json: cambio en {p}, que thanosvibs no publica')
        tv = filas[por_p[p]]
        if MARCA in tv:
            raise SystemExit(f'fuentes/propio/personajes.json: {p} tiene una fila propia y un cambio')
        d = {k: v for k, v in c['campos'].items() if tv.get(k) != v}
        if d:
            filas[por_p[p]] = {**tv, **c['campos'], MARCA: {'tv': tv}}
            informe['aplicado'].append(f'cambio en {p}: ' + ', '.join(f'{k} {tv.get(k)!r} → {v!r}' for k, v in d.items()))
        else:
            informe['confirmado'].append(f'cambio en {p}: thanosvibs ya publica {c["campos"]}')
    escribir(ruta, filas)

    ruta = os.path.join(W, 'uniforms.json')
    uni = cargar(ruta)
    for p, u in P['uniformes'].items():
        fuentes(u, f'uniforme {p}')
        nuevo = sin_meta(u)
        uni[p] = {**(uni.get(p) or {}), **nuevo, MARCA: {'tv': uni.get(p)}}
    escribir(ruta, uni)

    ruta = os.path.join(W, 'instintos.json')
    ins = cargar(ruta)
    for n, x in P['instintos'].items():
        fuentes(x, f'instinto de {n}')
        if n in ins and ins[n].get('instinct') == x['instinct']:
            informe['confirmado'].append(f'instinto de {n}')
            continue
        ins[n] = {'instinct': x['instinct'], MARCA: {'tv': ins.get(n)}}
    escribir(ruta, ins)

    ruta = os.path.join(W, 'updates.json')
    ups = cargar(ruta)
    for v in P['versiones']:
        fuentes(v, f'versión {v["version"]}')
        e = next((x for x in ups if x['version'] == v['version']), None)
        if e is None:
            e = {'version': v['version'], 'subtitle': v['subtitle'], 'img_format': 'jpg', 'themes': [],
                 'potes': [{'version': v['version'], 'name': v['subtitle'], 'date': v['fecha'], 'icon': '', 'main': 'True'}],
                 'characters': [], 'uniforms': [], 't3s': [], 'tps': [], 't4s': [], 'banners': [], MARCA: {'tv': None}}
            ups.insert(0, e)
        for k in ('characters', 'uniforms', 't3s', 't4s'):
            ya = {x['portrait'] for x in e.get(k) or []}
            e.setdefault(k, []).extend({'portrait': p, 'added_in': v['version'], MARCA: {'tv': None}}
                                       for p in v[k] if p not in ya)
    escribir(ruta, ups)

    # Skills: todas desde lo de thanosvibs ya restaurado, antes de escribir ninguna.
    def tv_skills(p):
        f = os.path.join(W, 'skills_api', p + '.json')
        return cargar(f) if os.path.exists(f) else None
    salida = {}
    for p, s in S.items():
        fuentes(s, f'skills de {p}')
        base = tv_skills(s['desde']) if s['desde'] else None
        if s['desde'] and base is None:
            raise SystemExit(f'fuentes/propio/skills/{p}.json: thanosvibs no publica las skills de {s["desde"]}')
        skills = copy.deepcopy(base['skills']) if base else {}
        skills.pop('cancels', None)
        for sl, sk in s['slots'].items():
            if sk['type'] != sl:
                raise SystemExit(f'fuentes/propio/skills/{p}.json: el slot {sl} trae una skill de tipo {sk["type"]}')
            skills[sl] = {**sk, 'fuente': s['fuente']}
        tv = tv_skills(p)
        if tv is not None and s['desde'] != p:
            d = [f'{sl}: ' + '; '.join(diferencias(huella_skill(sk), huella_skill(tv['skills'][sl])))
                 for sl, sk in s['slots'].items() if sl in tv['skills']
                 and huella_skill(sk) != huella_skill(tv['skills'][sl])]
            d += [f'{sl}: thanosvibs no lo publica' for sl in s['slots'] if sl not in tv['skills']]
            (informe['difiere'] if d else informe['confirmado']).append(f'skills de {p}' + (': ' + ' | '.join(d) if d else ''))
        elif tv is not None:
            for sl, sk in s['slots'].items():
                if sl in tv['skills']:
                    d = diferencias(huella_skill(sk), huella_skill(tv['skills'][sl]))
                    (informe['difiere'] if d else informe['confirmado']).append(f'{sl} de {p}' + (': ' + '; '.join(d) if d else ''))
                else:
                    informe['aplicado'].append(f'{sl} de {p} (thanosvibs no lo publica)')
        else:
            informe['aplicado'].append(f'skills de {p} (thanosvibs no las publica)')
        for n in s.get('notas', []):
            informe['sin_confirmar'].append(f'skills de {p}: {n}')
        salida[p] = {'portrait': p, 'skills': skills, MARCA: {'tv': tv}}
    for p, d in salida.items():
        escribir(os.path.join(W, 'skills_api', p + '.json'), d)

    # Artefactos y C.T.P.s.
    for archivo, clave, lista, campo in (('artifacts.json', 'portrait', A['artefactos'], 'artefacto'),
                                         ('ctps.json', 'name', T['ctps'], 'C.T.P.')):
        ruta = os.path.join(W, archivo)
        filas = cargar(ruta)
        por = {r[clave]: i for i, r in enumerate(filas)}
        for r in lista:
            fuentes(r, f'{campo} {r[clave]}')
            nueva = sin_meta(r)
            if r[clave] in por:
                tv = filas[por[r[clave]]]
                d = diferencias(nueva, tv, [k for k in nueva if k not in ('id', 'pve_score', 'pvp_score', 'acquisition')])
                (informe['difiere'] if d else informe['confirmado']).append(f'{campo} {r[clave]}' + (': ' + '; '.join(d) if d else ''))
                filas[por[r[clave]]] = {**nueva, MARCA: {'tv': tv}}
            else:
                filas.append({**nueva, MARCA: {'tv': None}})
                informe['aplicado'].append(f'{campo} {r[clave]} (thanosvibs no lo publica)')
        escribir(ruta, filas)

    # Retratos: la app los baja de fuentes/propio/retratos/ (imagenes.origen); acá, para la app servida desde el repo.
    os.makedirs(IMAGENES, exist_ok=True)
    for f in glob.glob(os.path.join(PROPIO, 'retratos', '*.png')):
        shutil.copyfile(f, os.path.join(IMAGENES, os.path.basename(f)))

    escribir(os.path.join(W, 'propio.json'), informe)
    print(f"contenido propio: {len(informe['aplicado'])} sin thanosvibs, {len(informe['confirmado'])} confirmados, "
          f"{len(informe['difiere'])} distintos de thanosvibs, {len(informe['sin_confirmar'])} sin confirmar")
    for x in informe['difiere']:
        print('AVISO: contenido propio distinto de thanosvibs (manda lo propio):', x)


def retratos():
    """Los retratos propios (los nombres de fuentes/propio/retratos/), para _core.py."""
    return {os.path.basename(f)[:-4] for f in glob.glob(os.path.join(PROPIO, 'retratos', '*.png'))}


if __name__ == '__main__':
    main()
