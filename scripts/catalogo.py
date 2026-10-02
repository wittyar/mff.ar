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
  tienen que estar clasificados. Uno nuevo que no está se avisa y va a la auditoría (sección 9),
  sin cortar la actualización semanal, igual que un marcador o una traducción que falta.

Escribe docs/CATALOGO.md (el catálogo entero, para leerlo y revisarlo) y work/catalogo.json
(lo que falta clasificar, para auditar.py)."""
import collections, datetime, json, os, sys

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)
from version_juego import ultima

RUTA = os.path.join(_DIR, 'contenido', 'catalogo.json')
SLOTS_SOPORTE = ('leader', 'leader2', 'passive', 'passive2', 't2', 't22', 'uniform', 'uniform2', 'artifact')
EFECTOS_ARTEFACTO = ('effect3', 'effect4', 'effect5', 'effect6')


def cargar(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)


# -- coherencia ------------------------------------------------------------------
def validar(cat, fuentes):
    """Lista de problemas del contenido curado (vacía si está bien)."""
    mal = []
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

    def mapeo(x, donde, con_para):
        claves = {'efectos', 'condicion', 'nota'} | ({'para'} if con_para else set())
        if set(x) - claves or 'efectos' not in x or (con_para and 'para' not in x):
            mal.append(f"{donde}: lleva {', '.join(sorted(claves))} ({'para y efectos obligatorios' if con_para else 'efectos obligatorio'})")
            return
        if con_para and x['para'] not in cat['para']:
            mal.append(f"{donde}: para desconocido {x['para']!r}")
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
    usados = {e for x in cat['skills'].values() for y in (x['por_patron'].values() if 'por_patron' in x else [x])
              for e in y.get('efectos', [])} | {e for x in cat['soporte'].values() for e in x.get('efectos', [])}
    mal += [f'efecto {i} sin ninguna etiqueta ni stat que apunte a él' for i in ids_efecto if i not in usados]
    return mal


# -- uso en los datos --------------------------------------------------------------
def usos(sp, su):
    """Retratos que usan cada etiqueta, cada patrón de cada etiqueta y cada stat."""
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
    # Diccionarios comunes: consultar algo que los datos no traen no lo agrega.
    return {'etiqueta': dict(etiqueta), 'patron': {l: dict(ps) for l, ps in patron.items()}, 'stat': dict(stat)}


def cobertura(cat, U):
    """Lo de los datos que el catálogo no clasifica, y lo del catálogo que los datos ya no traen."""
    S, SO = cat['skills'], cat['soporte']
    falta = {'etiquetas': sorted(l for l in U['etiqueta'] if l not in S),
             'patrones': sorted((l, p) for l in U['patron'] if 'por_patron' in S.get(l, {})
                                for p in U['patron'][l] if p not in S[l]['por_patron']),
             'stats': sorted(s for s in U['stat'] if s not in SO)}
    sobra = {'etiquetas': sorted(l for l in S if l not in U['etiqueta']),
             'patrones': sorted((l, p) for l, x in S.items() if 'por_patron' in x and l in U['patron']
                                for p in x['por_patron'] if p not in U['patron'][l]),
             'stats': sorted(s for s in SO if s not in U['stat'])}
    return falta, sobra


# -- documento ---------------------------------------------------------------------
def md(s):
    """Texto de la fuente dentro de código en línea, sin romperlo."""
    return '`' + s.replace('`', "'") + '`'


def retratos(n):
    return f"{n} retrato{'' if n == 1 else 's'}"


def fuente_md(f):
    """Una fuente de contenido/guia.json en Markdown: con su enlace, o solo su nombre si no tiene
    dirección (la guía dentro del juego)."""
    return f"[{f['nombre']}]({f['url']})" if 'url' in f else f['nombre']


def documento(cat, U, fuentes, version, falta):
    hoy = datetime.date.today().isoformat()

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
    for stat, x in cat['soporte'].items():
        extra = ([cond(x['condicion'])] if 'condicion' in x else []) + (['Nota: ' + x['nota']['es']] if 'nota' in x else [])
        for e in x['efectos']:
            de_stat[e].append((len(U['stat'].get(stat, ())), stat, extra))
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
         '- **Le sirve:** a quién le aporta algo, según con qué pega cada variante (docs/MODELO.md, perfil de combate).',
         '- **PvE / PvP:** la lectura de cada modo. Si el efecto no trae una propia, vale la de su grupo.',
         '- **Certeza:**']
    s += [f"  - [{k.capitalize()}] {v['es']}" for k, v in cat['certeza'].items()]
    s += ['- **Skills:** las etiquetas que apuntan al efecto, de la más usada a la menos, con cuántos retratos la usan.',
          '- **Leads & Supports:** los stats que apuntan al efecto, con cuántos retratos lo dan.\n',
          f"{len(cat['grupos'])} grupos, {len(cat['efectos'])} efectos, {len(cat['skills'])} etiquetas de skills y "
          f"{len(cat['soporte'])} stats de Leads & Supports. "
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
            s.append(f"`{e['id']}` · {e['en']} · Se aplica {lado} · Le sirve: {cat['sirve'][e['sirve']]['es'][0].lower()}"
                     f"{cat['sirve'][e['sirve']]['es'][1:]}.\n")
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
                s.append('- **Leads & Supports:**')
                for n, stat, extra in sorted(de_stat[e['id']], key=lambda x: (-x[0], x[1].lower())):
                    s.append(f'  - {md(stat)} ({retratos(n)})' + (' — ' + '; '.join(extra) if extra else ''))
            s.append('')
    citadas = sorted({k for L in [g[x] for g in cat['grupos'] for x in ('pve', 'pvp')] +
                      [e[x] for e in cat['efectos'] for x in ('pve', 'pvp') if x in e] for k in L.get('fuente', [])})
    s.append('## Fuentes\n')
    s += [f"- {fuente_md(fuentes[k])}" for k in citadas]
    s.append('')
    return '\n'.join(s)


def main():
    cat = cargar(RUTA)
    fuentes = cargar(os.path.join(_DIR, 'contenido', 'guia.json'))['fuentes']
    mal = validar(cat, fuentes)
    if mal:
        raise SystemExit('scripts/contenido/catalogo.json tiene errores:\n  ' + '\n  '.join(mal))
    U = usos(cargar('work/skills_parsed.json'), cargar('work/supports.json'))
    falta, sobra = cobertura(cat, U)
    for k, v in falta.items():
        if v:
            print(f'AVISO: catálogo de efectos: {k} de los datos sin clasificar (docs/AUDITORIA.md, sección 9): {v}')
    for k, v in sobra.items():
        if v:
            print(f'AVISO: catálogo de efectos: {k} que los datos ya no traen: {v}')
    version = ultima(cargar('work/updates.json'))[1]
    os.makedirs('docs', exist_ok=True)
    open('docs/CATALOGO.md', 'w', encoding='utf-8', newline='\n').write(documento(cat, U, fuentes, version, falta))
    usos_falta = {'etiquetas': {l: sorted(U['etiqueta'][l])[:3] for l in falta['etiquetas']},
                  'patrones': [[l, p, sorted(U['patron'][l][p])[:3]] for l, p in falta['patrones']],
                  'stats': {s: sorted(U['stat'][s])[:3] for s in falta['stats']}}
    json.dump({'falta': usos_falta, 'sobra': sobra,
               'total': {'etiquetas': len(U['etiqueta']), 'stats': len(U['stat']), 'efectos': len(cat['efectos'])}},
              open('work/catalogo.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"catálogo de efectos: {len(cat['efectos'])} efectos | etiquetas {len(U['etiqueta'])} | stats {len(U['stat'])} | "
          f"sin clasificar {sum(len(v) for v in falta.values())} | docs/CATALOGO.md")


if __name__ == '__main__':
    main()
