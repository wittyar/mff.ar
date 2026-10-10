#!/usr/bin/env python3
"""Auditoría entre fuentes: lo que publica thanosvibs contra la wiki de Future Fight, y
thanosvibs contra sí mismo.

No corrige nada: la app sigue mostrando thanosvibs (es la fuente de las skills y de
los personajes). Lo que no coincide se marca para revisarlo, con los dos valores y de
dónde sale cada uno. La wiki la edita la comunidad y en muchas páginas quedó vieja
(uniformes sin sección, valores anteriores a un rebalanceo): una diferencia no dice
cuál de las dos está bien.

Deja:
- work/verificacion.json: por retrato, lo que la ficha muestra en "Verificación".
- docs/AUDITORIA.md: el informe completo.

Lo llama build.py después de skills_api.py, fuentes.py y catalogo.py (la sección 9 lista lo que el
catálogo de efectos no clasifica, de work/catalogo.json; la 10, lo que no cierra en los bonos de
equipo de la wiki; la 11, en los strikers, y la 12, los liderazgos que Leads & Supports no publica y
el build deriva de la Leader Skill de la API, de work/fuentes.json).
"""
import collections, datetime, difflib, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from version_juego import ultima
from catalogo import fuente_md
from liderazgos import A_MANO, LIDERAZGOS, ROTULOS, motivo_txt, slot_txt

_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI = 'https://future-fight.fandom.com/wiki/'


def cargar(ruta):
    return json.load(open(ruta, encoding='utf-8'))


def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').casefold())


def parecido(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def limpiar(v):
    """Valor de un campo de la wiki sin enlaces, imágenes ni formato."""
    v = re.sub(r'\[\[File:[^\]]*\]\]', '', v)
    v = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', v)
    v = re.sub(r"<[^>]+>|'''?|\{\{[^}]*\}\}", '', v)
    return re.sub(r'\s+', ' ', v).strip()


def wslug(s):
    return re.sub(r'[^A-Za-z0-9]+', '_', s)


# ---------------------------------------------------------------------------
# Lectura de la wiki
# ---------------------------------------------------------------------------
def infoboxes(wt):
    """Pestañas del infobox: [{'uniforme': nombre o None (vale para todas), campos}].

    Hay dos plantillas: "Character Info Box 2022" (una sola, con campos numerados por
    pestaña: type1, tab1...) y "CharacterInfoboxNew" (una por uniforme, con su campo
    'uniform'). Los nombres de campo con espacios ("atk type") quedan con guion bajo."""
    tabs = []
    m = re.search(r'\{\{Character Info Box 2022[^\n]*\n(.*?)\n\}\}', wt, re.S)
    if m:
        por = collections.defaultdict(dict)
        for c in re.finditer(r'^\|\s*([a-z_]+?)(\d*)\s*=\s*(.*)$', m.group(1), re.M):
            por[c.group(2)][c.group(1)] = limpiar(c.group(3))
        comunes = por.pop('', {})
        if not por:
            tabs.append({'uniforme': None, 'campos': comunes})
        for k in sorted(por, key=int):
            campos = dict(comunes, **por[k])
            tabs.append({'uniforme': campos.get('tab'), 'campos': campos})
    for m in re.finditer(r'\{\{(?:Template:)?CharacterInfoboxNew\s*\n(.*?)\n\}\}', wt, re.S):
        campos = {}
        for c in re.finditer(r'^\|\s*([a-z][a-z ]*?)\s*=\s*(.*)$', m.group(1), re.M):
            campos[c.group(1).replace(' ', '_')] = limpiar(c.group(2))
        tabs.append({'uniforme': campos.get('uniform'), 'campos': campos})
    return tabs


# Un nombre de skill en la wiki: en negrita ('''Nombre''') o como cabecera de tabla
# (| class="header2" |Nombre (Physical Attack)).
_ANCLA = re.compile(r"'''(?!')([^\n]{2,80}?)(?<!')'''|^\|\s*class=\"header2\"\s*\|\s*([^\n]+)$", re.M)
_DANO = re.compile(r'Damage:?\s*(\d+(?:\.\d+)?)\s*% of (?:Physical Attack|Energy Attack|Max HP|HP)'
                   r'|(\d+(?:\.\d+)?)%\s+(?:[A-Z][a-z]+\s+)?Damage,\s*Add', re.I)
_CD = re.compile(r'Cooldown Time:?\s*(\d+(?:\.\d+)?)\s*(?:second|sec)', re.I)
_UNIF = re.compile(r'^==\s*(?:\[\[File:[^\]]*\]\])?\s*"(.+?)"\s*Uniform\s*==\s*$', re.M)
_H2 = re.compile(r'^==[^=].*$', re.M)


def anclas(wt):
    """Cada nombre de skill de la página con el texto que lo sigue (hasta el próximo
    nombre) y la sección de uniforme en la que está (None si es general)."""
    marcas = {m.start(): None for m in _H2.finditer(wt)}
    for m in _UNIF.finditer(wt):
        marcas[m.start()] = m.group(1)
    orden = sorted(marcas.items())
    ms = list(_ANCLA.finditer(wt))
    out = []
    for i, m in enumerate(ms):
        nom = re.sub(r'\[\[File:[^\]]*\]\]', '', (m.group(1) or m.group(2) or ''))
        nom = re.sub(r'\s*\([^)]*\)\s*$', '', nom).strip()
        fin = ms[i + 1].start() if i + 1 < len(ms) else len(wt)
        u = None
        for p, n in orden:
            if p > m.start():
                break
            u = n
        # El texto de la skill termina antes de la próxima imagen: en las páginas viejas
        # las variantes por uniforme van inline, precedidas por el ícono del uniforme.
        txt = wt[m.end():fin]
        corte = txt.find('\n[[File:')
        out.append({'n': norm(nom), 'u': u, 'txt': txt if corte < 0 else txt[:corte]})
    return out


# ---------------------------------------------------------------------------
# Chequeos
# ---------------------------------------------------------------------------
class Auditoria:
    def __init__(self):
        self.chars = cargar('work/characters.json')
        self.sp = cargar('work/skills_parsed.json')
        self.NAME, self.DESC = self.sp['tablas']['name'], self.sp['tablas']['desc']
        self.titulos = cargar('work/wiki_titles.json')
        self.por_nombre = collections.defaultdict(list)
        for r in self.chars:
            self.por_nombre[r['character']].append(r)
        self.paginas = {}
        for nombre in self.por_nombre:
            fn = f'work/wikitext/{wslug(nombre)}.json'
            if os.path.exists(fn):
                self.paginas[nombre] = cargar(fn)['wt']
        self.por_retrato = collections.defaultdict(lambda: {'ok': 0, 'nd': 0, 'dif': []})
        self.res = collections.Counter()
        self.listas = collections.defaultdict(list)   # para el informe

    def dif(self, p, **x):
        self.por_retrato[p]['dif'].append(x)

    # -- skills --------------------------------------------------------------
    def danos_api(self, sk):
        out = set()
        for st in sk.get('st') or []:
            for f in st.get('fx') or []:
                d = self.DESC[f['p']]
                if d.get('pi') is not None and f.get('v'):
                    out.add(float(f['v'][d['pi']]))
        return sorted(out)

    def skills(self):
        """Daño (% de ataque o de vida) y recarga de cada skill activa, Definitiva y
        Striker: thanosvibs contra la wiki. La skill se busca por nombre en la página
        del personaje, primero en la sección de su uniforme."""
        for nombre, rs in self.por_nombre.items():
            wt = self.paginas.get(nombre)
            A = anclas(wt) if wt else []
            # Con secciones por uniforme, lo general es lo compartido ("All Uniforms");
            # en las páginas viejas, sin secciones, lo general describe al uniforme base.
            con_secciones = any(a['u'] for a in A)
            for r in rs:
                p = r['portrait']
                for sk in self.sp['skills'].get(p, []):
                    if not (sk['sl'].startswith('Active') or sk['sl'] == 'Striker Skill'):
                        continue
                    en = self.NAME[sk['n']]['en']
                    n = norm(en)
                    self.res['skills'] += 1
                    cands = [a for a in A if a['n'] == n] or [a for a in A if a['n'] and parecido(a['n'], n) >= 0.85]
                    if not cands:
                        self.res['skills_sin_wiki'] += 1
                        self.por_retrato[p]['nd'] += 1
                        continue
                    propia = [c for c in cands if c['u'] and (norm(c['u']) == norm(r['uniform'])
                                                              or parecido(norm(c['u']), norm(r['uniform'])) >= 0.8)]
                    general = [c for c in cands if not c['u']] if (con_secciones or r['uniformed'] == 'False') else []
                    if not (propia or general):
                        # Solo aparece en la sección de otro uniforme: sus números son de
                        # ese uniforme, así que no se compara.
                        self.res['skills_otra_seccion'] += 1
                        self.por_retrato[p]['nd'] += 1
                        continue
                    a = (propia or general)[0]
                    self.res['skills_en_wiki'] += 1
                    api_d = self.danos_api(sk)
                    wiki_d = sorted({float(x or y) for x, y in _DANO.findall(a['txt'])})
                    api_cd = sk.get('cd')
                    wiki_cd = sorted({float(x) for x in _CD.findall(a['txt'])})
                    bien = True
                    if api_d or wiki_d:
                        if api_d == wiki_d:
                            self.res['dano_ok'] += 1
                        elif not wiki_d:
                            self.res['dano_sin_dato'] += 1
                        elif set(wiki_d) < set(api_d):
                            self.res['dano_parcial'] += 1   # la wiki lista menos etapas
                        else:
                            self.res['dano_dif'] += 1
                            bien = False
                            self.dif(p, t='dano', sl=sk['sl'], n=en, api=api_d, wiki=wiki_d)
                            self.listas['dano'].append((nombre, r['uniform'], sk['sl'], en, api_d, wiki_d))
                    if api_cd:
                        if not wiki_cd:
                            self.res['cd_sin_dato'] += 1
                        elif float(api_cd) in wiki_cd:
                            self.res['cd_ok'] += 1
                        else:
                            self.res['cd_dif'] += 1
                            bien = False
                            self.dif(p, t='cd', sl=sk['sl'], n=en, api=api_cd, wiki=wiki_cd)
                            self.listas['cd'].append((nombre, r['uniform'], sk['sl'], en, api_cd, wiki_cd))
                    if bien:
                        self.por_retrato[p]['ok'] += 1

    # -- infobox ---------------------------------------------------------------
    CAMPOS = (('type', 'type', ('Combat', 'Blast', 'Speed', 'Universal')),
              ('side', 'side', ('Super Hero', 'Super Villain', 'Neutral')),
              ('gender', 'gender', ('Male', 'Female', 'Neutral')),
              ('allies', 'allies', ('Human', 'Mutant', 'Inhuman', 'Alien', 'Creature', 'Other')))

    def ataque_api(self, p):
        suma = collections.Counter()
        for sk in self.sp['skills'].get(p, []):
            if not sk['sl'].startswith('Active'):
                continue
            for st in sk.get('st') or []:
                for f in st.get('fx') or []:
                    d = self.DESC[f['p']]
                    if d.get('pi') is not None and f.get('v'):
                        suma[d['src']] += f['v'][d['pi']]
        return {'Physical Attack': 'Physical', 'Energy Attack': 'Energy', 'HP': 'HP'}.get(suma.most_common(1)[0][0]) \
            if len(suma) == 1 else ('Mixed' if suma else None)

    def infobox(self):
        """Clase, bando, género, raza y tipo de ataque: el infobox de la wiki (por
        uniforme cuando tiene pestañas) contra thanosvibs. Si la wiki da varios valores
        para el personaje y el de thanosvibs está entre ellos, no se cuenta como diferencia."""
        for nombre, rs in self.por_nombre.items():
            wt = self.paginas.get(nombre)
            tabs = infoboxes(wt) if wt else []
            if not tabs:
                self.res['infobox_sin'] += len(rs)
                continue
            for r in rs:
                tab = next((x for x in tabs if x['uniforme'] and norm(x['uniforme']) == norm(r['uniform'])), None)
                if tab is None:
                    parecidos = [x for x in tabs if x['uniforme'] and parecido(norm(x['uniforme']), norm(r['uniform'])) >= 0.8]
                    # Un infobox sin pestañas describe al personaje base: los uniformes
                    # pueden cambiar clase, bando o género, así que solo vale para el base.
                    tab = parecidos[0] if parecidos else next(
                        (x for x in tabs if x['uniforme'] is None and r['uniformed'] == 'False'), None)
                if tab is None:
                    self.res['infobox_sin_pestana'] += 1
                    continue
                self.res['infobox_con'] += 1
                c = tab['campos']
                for campo, api_k, valores in self.CAMPOS:
                    w = c.get(campo) or (c.get('species') if campo == 'allies' else None)
                    if not w:
                        continue
                    hallados = [v for v in valores if v.casefold() in w.casefold()]
                    api = r[api_k]
                    if api in hallados:
                        self.res[f'{campo}_ok'] += 1
                    elif hallados:
                        self.res[f'{campo}_dif'] += 1
                        self.dif(r['portrait'], t=campo, api=api, wiki=w)
                        self.listas[campo].append((nombre, r['uniform'], api, w))
                w = c.get('atk_type')
                api = self.ataque_api(r['portrait'])
                if w and api:
                    if api == 'Mixed' or norm(w) == norm(api):
                        self.res['atk_ok'] += 1
                    else:
                        self.res['atk_dif'] += 1
                        self.dif(r['portrait'], t='atk', api=api, wiki=w)
                        self.listas['atk'].append((nombre, r['uniform'], api, w))

    def instinto(self):
        """Instinto: el campo del infobox (de donde lo toma la app) contra la categoría
        de la página."""
        INST = ('Justice', 'Order', 'Destruction', 'Cruelty')
        inst = cargar('work/instintos.json')
        for nombre, wt in self.paginas.items():
            cats = {m.group(1) for m in re.finditer(r'\[\[Category:(Justice|Order|Destruction|Cruelty)\]\]', wt)}
            campo = (inst.get(nombre) or {}).get('instinct')
            if not cats or not campo:
                continue
            if campo in cats:
                self.res['instinto_ok'] += 1
            else:
                self.res['instinto_dif'] += 1
                for r in self.por_nombre[nombre]:
                    self.dif(r['portrait'], t='instinto', api=campo, wiki=', '.join(sorted(cats)))
                self.listas['instinto'].append((nombre, campo, sorted(cats)))

    # -- thanosvibs contra sí mismo -------------------------------------------
    def interno(self):
        """La API de personajes marca Tier-4 y la skill 6 (Tier-3 o Trascendido); las
        skills de ese retrato tienen que acompañar."""
        for r in self.chars:
            p = r['portrait']
            sls = {sk['sl'] for sk in self.sp['skills'].get(p, [])}
            if not sls:
                continue
            if r['tier-4'] == 'True' and 'Striker Skill' not in sls:
                self.res['t4_sin_striker'] += 1
                self.dif(p, t='t4')
                self.listas['t4'].append((r['character'], r['uniform']))
            if r['skill6'] in ('Tier-3', 'Transcended') and 'Active Ult' not in sls:
                self.res['s6_sin_ult'] += 1
                self.dif(p, t='s6', v=r['skill6'])
                self.listas['s6'].append((r['character'], r['uniform'], r['skill6']))
        marcas = [i for i, d in enumerate(self.DESC) if re.search(r'\$[A-Z]+', d.get('en') or '')]
        usos = collections.Counter()
        for p, sks in self.sp['skills'].items():
            for sk in sks:
                for st in sk.get('st') or []:
                    for f in st.get('fx') or []:
                        if f['p'] in marcas:
                            usos[p] += 1
        self.res['marcadores_patrones'] = len(marcas)
        self.res['marcadores_retratos'] = len(usos)
        # Los de facción, tipo o raza: cómo los completó skills_api.py (marcadores.py).
        m = cargar('work/marcadores.json')
        nombre = {r['portrait']: r['character'] + ('' if r['uniformed'] == 'False' else f" — {r['uniform']}")
                  for r in self.chars}
        pend = {}
        for e in m['pendientes']:
            x = pend.setdefault(e['id'], [[], e['skill'], e['texto']])
            if nombre[e['p']] not in x[0]:
                x[0].append(nombre[e['p']])
        self.marcadores = {**m, 'sin_resolver': len(pend),
                           'pendientes': sorted(((i, pjs, sk, tx) for i, (pjs, sk, tx) in pend.items()),
                                                key=lambda x: (x[1][0], x[2], x[0]))}

    # -- fuentes: soportes y artefactos ----------------------------------------
    def fuentes(self):
        f = cargar('work/fuentes.json')
        vistos = set()
        for p, e in f['soportes'].items():
            for tipo, x in e.items():
                if isinstance(x, dict) and x.get('rc') and (id(x), tipo) not in vistos:
                    vistos.add((id(x), tipo))
                    self.listas['soporte'].append((p, tipo, x['rc'], x['r']))
        self.res['soportes_corregidos'] = len(self.listas['soporte'])
        # Lo que el build corrige con el juego (fuentes.py): el dato corregido lleva el de thanosvibs (tv) y su fuente.
        self.listas['ctp_nombre'] = [(c['id'], c['tv'], c['name'], c['f']) for c in f['ctps'] if 'tv' in c]
        self.listas['art_linea'] = [(a['p'], a['name'], ln['tv'], ln['t'], ln['f']) for a in f['artefactos']
                                    for ln in a['lineas'] if 'tv' in ln]
        # Artefactos: los números del texto a 6★ contra los de la página Artifact de la
        # wiki (que los lista a 6★, "Lv.4").
        wt = cargar('work/wiki_artifact.json')['wt']
        filas = {}
        for fila in wt.split('\n|-')[1:]:
            m = re.search(r"^\|\s*\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", fila.strip(), re.M)
            if not m:
                continue
            desc = fila.split('style="text-align:left;" |', 1)[-1]
            filas[norm(m.group(1))] = sorted({float(x) for x in re.findall(r'(?<![\w.])(\d+(?:\.\d+)?)', limpiar(desc))})
        nombres = {r['base_portrait']: r['character'] for r in self.chars}
        for a in cargar('work/artifacts.json'):
            texto = ' '.join(a['text']).replace('&emsp;', ' ')
            usados = [int(x) for x in re.findall(r'\[P(\d+)\]', texto)]
            completos = {e: v for e, v in a['values'].items() if len(v) >= max(usados, default=0)}
            if len(completos) < len(a['values']):
                self.res['artefactos_incompletos'] += 1
                self.listas['art_incompleto'].append((a['character'], a['artifact_name'],
                                                      sorted(set(a['values']) - set(completos))))
                self.dif(a['portrait'], t='art_incompleto', v=sorted(set(a['values']) - set(completos)))
            if '6' not in completos:
                continue
            def numeros(vals):
                lleno = re.sub(r'\[P(\d+)\]', lambda m: vals[int(m.group(1)) - 1], texto)
                return {float(x) for x in re.findall(r'(?<![\w.])(\d+(?:\.\d+)?)', lleno)} - {4.0}
            w = filas.get(norm(nombres.get(a['portrait'], a['character'])))
            if w is None:
                self.res['artefactos_sin_wiki'] += 1
                continue
            w_s = set(w) - {4.0}                      # el "Lv.4" del nombre en la wiki
            por_est = {e: numeros(v) for e, v in completos.items()}
            if por_est['6'] == w_s:
                self.res['artefactos_ok'] += 1
                continue
            otro = [e for e, ns in sorted(por_est.items()) if ns == w_s]
            if otro:
                # La wiki dice listar 6★ pero sus números son los de otro nivel.
                self.res['artefactos_otro_nivel'] += 1
                self.listas['art_nivel'].append((a['character'], a['artifact_name'], otro[0]))
                continue
            self.res['artefactos_dif'] += 1
            solo_api, solo_wiki = sorted(por_est['6'] - w_s), sorted(w_s - por_est['6'])
            self.dif(a['portrait'], t='art', api=solo_api, wiki=solo_wiki)
            self.listas['art'].append((a['character'], a['artifact_name'], solo_api, solo_wiki))

    def correr(self):
        self.skills()
        self.infobox()
        self.instinto()
        self.interno()
        self.fuentes()


# ---------------------------------------------------------------------------
# Salidas
# ---------------------------------------------------------------------------
def pct(a, b):
    return f'{round(100 * a / b)}%' if b else '—'


def fmt(xs):
    return ', '.join(f'{x:g}' for x in xs) if isinstance(xs, list) else f'{xs:g}' if isinstance(xs, float) else str(xs)


def informe(A, version, hallazgos, fuentes, catalogo, bonos, strikers, liderazgos):
    R, L = A.res, A.listas
    hoy = datetime.date.today().isoformat()
    s = []
    s.append('# Auditoría de datos\n')
    s.append(f'Generado por `scripts/auditar.py` el {hoy}, sobre los datos del juego {version} '
             f'(thanosvibs) y la wiki de Future Fight bajada en la misma sincronización.\n')
    s.append('La app muestra thanosvibs, salvo lo que el build corrige con aviso (sección 5). Esto marca dónde otra '
             'fuente dice otra cosa, con los dos valores; no corrige nada. La wiki la edita la comunidad y muchas páginas quedaron '
             'viejas (uniformes sin sección, valores de antes de un rebalanceo), así que una '
             'diferencia es algo para revisar en el juego, no un error confirmado de ninguna de las dos.\n')
    s.append('En la app, cada ficha muestra lo que le toca en "Verificación entre fuentes".\n')
    s.append('## Resumen\n')
    s.append('| Chequeo | Coinciden | Difieren | Sin dato para comparar |')
    s.append('|---|---|---|---|')
    s.append(f"| Daño de skills (thanosvibs vs wiki) | {R['dano_ok']} (+{R['dano_parcial']} donde la wiki lista menos etapas) | {R['dano_dif']} | {R['dano_sin_dato']} |")
    s.append(f"| Recarga de skills | {R['cd_ok']} | {R['cd_dif']} | {R['cd_sin_dato']} |")
    for campo, nom in (('type', 'Clase'), ('side', 'Bando'), ('gender', 'Género'), ('allies', 'Raza'), ('atk', 'Tipo de ataque')):
        s.append(f"| {nom} (infobox de la wiki) | {R[campo + '_ok']} | {R[campo + '_dif']} | — |")
    s.append(f"| Instinto (campo vs categoría de la wiki) | {R['instinto_ok']} | {R['instinto_dif']} | — |")
    s.append(bonos_resumen(bonos))
    s.append(strikers_resumen(strikers))
    s.append(f"| Artefactos a 6★ (thanosvibs vs wiki) | {R['artefactos_ok']} (+{R['artefactos_otro_nivel']} donde la wiki lista otro nivel de estrellas) | {R['artefactos_dif']} | {R['artefactos_sin_wiki']} sin fila en la wiki; {R['artefactos_incompletos']} con niveles incompletos en thanosvibs |")
    s.append('')
    s.append(f"Cobertura de la wiki: de {R['skills']} skills (activas, Definitiva y Striker) de thanosvibs, "
             f"{R['skills_en_wiki']} ({pct(R['skills_en_wiki'], R['skills'])}) se pudieron comparar; "
             f"{R['skills_otra_seccion']} están en la página pero solo en la sección de otro uniforme, y el resto "
             f"no aparece (sobre todo uniformes que la wiki no documenta). Infobox: {R['infobox_con']} retratos "
             f"con pestaña en la wiki, {R['infobox_sin_pestana']} sin pestaña de su uniforme y {R['infobox_sin']} "
             f"de personajes sin infobox legible.\n")
    falta = catalogo['falta']
    n_falta = len(falta['etiquetas']) + len(falta['patrones']) + len(falta['stats'])
    s.append(f"Catálogo de efectos (docs/CATALOGO.md): {catalogo['total']['etiquetas']} etiquetas de skills y "
             f"{catalogo['total']['stats']} stats de Leads & Supports y {catalogo['total']['stats_bonos']} de bonos de equipo "
             'en los datos; '
             + ('todos clasificados.\n' if not n_falta else f'{n_falta} sin clasificar (sección 9).\n'))
    s.append(f"Liderazgos: el build deriva de la Leader Skill de la API el de {len(liderazgos['derivados'])} variantes "
             f"que Leads & Supports no publica; {len(liderazgos['sin_derivar'])} slots no se pudieron derivar (sección 12).\n")

    s.append('## 1. Skills: daño y recarga\n')
    s.append('Método: cada skill de thanosvibs se busca por nombre en la página de la wiki del personaje, '
             'en la sección de su uniforme o en la general (la de "All Uniforms"; en las páginas viejas, sin '
             'secciones por uniforme, la general solo vale para el uniforme base). Nombres parecidos al 85% '
             'cuentan, porque la wiki tiene erratas como "Turque Chain". Se comparan los % de daño distintos '
             'de la skill (de ataque físico, de energía o de vida) y la recarga. "Menos etapas" = la wiki lista '
             'solo algunos de los % que trae thanosvibs: no es una contradicción. La Definitiva de Tier-3 y la '
             'Striker no tienen recarga (se cargan con su barra), así que solo se compara su daño.\n')
    if L['dano']:
        s.append(f"### Daño distinto ({len(L['dano'])})\n")
        s.append('| Personaje | Uniforme | Slot | Skill | thanosvibs | wiki |')
        s.append('|---|---|---|---|---|---|')
        for n, u, sl, sk, a, w in sorted(L['dano']):
            s.append(f'| {n} | {u} | {sl} | {sk} | {fmt(a)} | {fmt(w)} |')
        s.append('')
    if L['cd']:
        s.append(f"### Recarga distinta ({len(L['cd'])})\n")
        s.append('| Personaje | Uniforme | Slot | Skill | thanosvibs (s) | wiki (s) |')
        s.append('|---|---|---|---|---|---|')
        for n, u, sl, sk, a, w in sorted(L['cd']):
            s.append(f'| {n} | {u} | {sl} | {sk} | {a} | {fmt(w)} |')
        s.append('')

    s.append('## 2. Infobox: clase, bando, género, raza y tipo de ataque\n')
    s.append('El tipo de ataque de thanosvibs no es un campo: se deriva de con qué escalan los % de daño '
             'de sus skills activas (igual que en la ficha). Cuando la wiki dice otra cosa, sus propias '
             'skills suelen darle la razón a thanosvibs (Ghost Rider Robbie Reyes: infobox "Physical", '
             'skills "% of Energy Attack").\n')
    for campo, nom in (('type', 'Clase'), ('side', 'Bando'), ('gender', 'Género'), ('allies', 'Raza'), ('atk', 'Tipo de ataque')):
        if L[campo]:
            s.append(f'### {nom} ({len(L[campo])})\n')
            s.append('| Personaje | Uniforme | thanosvibs | wiki |')
            s.append('|---|---|---|---|')
            for n, u, a, w in sorted(L[campo]):
                s.append(f'| {n} | {u} | {a} | {w} |')
            s.append('')

    s.append('## 3. Instinto\n')
    s.append('thanosvibs no publica el instinto: la app lo toma del infobox de la wiki. Acá, los '
             'personajes cuya página lo contradice en sus categorías.\n')
    if L['instinto']:
        s.append('| Personaje | Infobox (lo que usa la app) | Categoría de la página |')
        s.append('|---|---|---|')
        for n, c, cats in sorted(L['instinto']):
            s.append(f"| {n} | {c} | {', '.join(cats)} |")
    s.append('')

    s.append('## 4. thanosvibs contra sí mismo\n')
    s.append(f"- Retratos marcados Tier-4 sin Striker Skill en sus skills: {R['t4_sin_striker']}"
             + (': ' + '; '.join(f'{n} ({u})' for n, u in sorted(L['t4'])) if L['t4'] else '.'))
    s.append(f"- Retratos con skill 6 (Tier-3 o Trascendido) sin Definitiva en sus skills: {R['s6_sin_ult']}"
             + (': ' + '; '.join(f'{n} ({u}, {k})' for n, u, k in sorted(L['s6'])) if L['s6'] else '.'))
    s.append(f"- Textos de efecto con marcadores de plantilla sin resolver (`$HEROSUBTYPE`, `$HEROCLASS`, `$TIME`...): "
             f"{R['marcadores_patrones']} patrones, usados por {R['marcadores_retratos']} retratos. La facción, el "
             f"tipo o la raza se completan como dice la sección 8; lo que no, la app lo muestra \"sin especificar\" "
             f"en vez de inventar el valor.")
    s.append('')

    s += correcciones_seccion(L, fuentes)

    s.append('## 6. Artefactos\n')
    s.append('Los números del texto a 6★ de thanosvibs contra la tabla de la página Artifact de la '
             'wiki (que los lista a 6★, "Lv.4"). Se listan los números que están en una sola de las dos.\n')
    if L['art']:
        s.append('| Personaje | Artefacto | Solo en thanosvibs | Solo en la wiki |')
        s.append('|---|---|---|---|')
        for n, a, sa, sw in sorted(L['art']):
            s.append(f'| {n} | {a} | {fmt(sa)} | {fmt(sw)} |')
        s.append('')
    if L['art_nivel']:
        s.append(f"En {len(L['art_nivel'])} la wiki dice listar 6★ pero sus números son exactamente los de otro nivel "
                 f"de estrellas de thanosvibs (no es una contradicción de valores): "
                 + '; '.join(f'{n} ({a}): {e}★' for n, a, e in sorted(L['art_nivel'])) + '.\n')
    if L['art_incompleto']:
        s.append('Incompletos en thanosvibs (faltan valores en esos niveles de estrellas; la app marca "sin dato"):\n')
        for n, a, ests in sorted(L['art_incompleto']):
            s.append(f"- {n}, {a}: {', '.join(e + '★' for e in ests)}")
        s.append('')

    s.append('## 7. Hallazgos revisados a mano\n')
    s.append('Lo que no se puede detectar con un chequeo automático (scripts/contenido/hallazgos.json).\n')
    for x in hallazgos:
        citas = ', '.join(fuente_md(fuentes[k]) for k in x['fuente'])
        s.append(f"- **{x['titulo']}** — {x['es']} ({citas})")
    s.append('')

    s += marcadores_seccion(A.marcadores)

    sobra = catalogo['sobra']
    s.append('## 9. Efectos que el catálogo no clasifica\n')
    s.append('Cada etiqueta de efecto de las skills y cada stat de Leads & Supports y de los bonos de equipo apunta a '
             'efectos del catálogo (scripts/contenido/catalogo.json; docs/CATALOGO.md lo muestra entero). Lo que '
             'thanosvibs o la wiki agreguen y el catálogo no tenga se lista acá hasta que se clasifique a mano; '
             'mientras tanto, la app lo cuenta para todos y lo dice.\n')
    if not n_falta:
        s.append('Ninguno: todo lo que traen los datos está clasificado.\n')
    else:
        s.append('| Qué | Texto de la fuente | Ejemplos |')
        s.append('|---|---|---|')
        s += [f"| Etiqueta | `{l}` | {', '.join(ej)} |" for l, ej in falta['etiquetas'].items()]
        s += [f"| Patrón de `{l}` | `{p}` | {', '.join(ej)} |" for l, p, ej in falta['patrones']]
        s += [f"| Stat | `{x}` | {', '.join(ej)} |" for x, ej in falta['stats'].items()]
        s.append('')
    if any(sobra.values()):
        s.append('En el catálogo pero ya no en los datos (thanosvibs los cambió o los sacó): '
                 + '; '.join(f'`{x}`' if isinstance(x, str) else f'`{x[0]}` con `{x[1]}`'
                             for k in ('etiquetas', 'patrones', 'stats') for x in sobra[k]) + '.\n')
    s += bonos_seccion(bonos, fuentes)
    s += strikers_seccion(strikers)
    s += liderazgos_seccion(liderazgos, A.chars, fuentes)
    return '\n'.join(s)


_AVISOS_MARCADORES = (
    ('conflictos', 'La wiki da valores distintos para el mismo efecto en dos skills (no se usa)'),
    ('conflictos_soportes', 'Leads & Supports da valores distintos para el mismo efecto en dos retratos (no se usa)'),
    ('huerfanos', 'Ids de la tabla a mano que la API ya no trae'),
    ('mano_soportes', 'Valores a mano distintos de Leads & Supports (gana la tabla)'),
    ('mano_wiki', 'Valores a mano distintos de la wiki (gana la tabla)'),
    ('soportes_wiki', 'Valores de Leads & Supports distintos de la wiki (gana Leads & Supports)'),
)


def marcadores_seccion(M):
    """Sección 8: de dónde salió el valor de cada marcador (scripts/marcadores.py, por skills_api.py) y
    lo que queda por cargar a mano."""
    s = ['## 8. Facción, tipo o raza que la fuente no publica\n']
    s.append(f"thanosvibs publica {M['ids']} efectos con un marcador (`$HEROSUBTYPE1`, `$HEROCLASS1`) en vez de la "
             'facción, el tipo, la raza o la habilidad a la que se refieren (`Increases basic damage dealt to '
             '$HEROSUBTYPE1 faction by 30%`). El build los completa en este orden (Ezequiel, 3 de octubre de 2026): la '
             'tabla a mano (scripts/contenido/marcadores.csv); Leads & Supports, en los slots de la misma skill (Leader '
             'Skill: `leader` y `leader2`; Passive: `passive` y `passive2`; Tier-2 Passive: `t2` y `t22`; Uniform Passive: '
             '`uniform` y `uniform2`), con «Basic Damage Dealt to …» o «Basic Damage Received from …» en el mismo sentido, '
             'el mismo porcentaje (el recibido, sin el signo) y un grupo de la clase que pide el texto, y la wiki: la '
             'misma skill con el mismo porcentaje, en el mismo sentido (daño infligido o recibido). Si la skill trae el '
             'mismo efecto varias veces, la fuente tiene que dar tantos valores distintos como efectos, y se asignan en '
             'el orden en que aparecen (qué valor va a cuál de esos efectos no se sabe: dos fuentes que dan los mismos '
             'valores en otro orden no difieren). En la ficha, el valor completado va subrayado y dice de dónde salió.\n')
    s.append(f"De los {M['ids']}: {M['manual']} a mano, {M['soportes']} de Leads & Supports, {M['wiki']} de la wiki y "
             f"{M['sin_resolver']} sin resolver (la app los muestra \"sin especificar\").\n")
    avisos = [(k, texto) for k, texto in _AVISOS_MARCADORES if M[k]]
    for clave, texto in avisos:
        s.append(f"- **{texto}:** {', '.join(str(i) for i in M[clave])}")
    if avisos:
        s.append('')
    if M['pendientes']:
        s.append('Para completar uno: en scripts/contenido/marcadores.csv, la columna `valor` de su id, escrita como la '
                 'muestra la app (Superhéroe, Supervillano, Neutral, Combate, Mutante...) o en inglés como la nombra el '
                 'juego. `python3 scripts/marcadores.py` agrega las filas que falten.\n')
        s.append('| Personaje | Skill | Efecto | id |')
        s.append('|---|---|---|---|')
        for ide, pjs, sk, tx in M['pendientes']:
            s.append(f"| {' / '.join(pjs)} | {sk} | `{tx}` | {ide} |")
        s.append('')
    return s


def _version(v):
    """Los stats de una versión de un bono: «All Basic Attacks +5.2%, Skill Cooldown −4.9%»."""
    return ', '.join(f"{st} {'+' if x > 0 else '−'}{abs(x):g}%" for st, x in v)


def bonos_resumen(bonos):
    A = bonos['auditoria']
    wiki = sum(1 for b in bonos['bonos'] if b['f'] == ['wiki-bonos'])
    distintos = len(A['mayorias']) + len(A['empates'])
    return (f"| Bonos de equipo (las páginas de la wiki entre sí) | {wiki - distintos} | {len(A['mayorias'])} por mayoría, "
            f"{len(A['empates'])} empatados | {len(A['sin_seccion'])} páginas sin la sección |")


def strikers_resumen(strikers):
    A = strikers['auditoria']
    return (f"| Strikers (pestaña Striker de la wiki) | {A['filas']} filas en {A['paginas']} páginas | "
            f"{len(A['ilegibles'])} filas que no se pudieron leer; {len(A['imposibles'])} con más de 100% | "
            f"{len(A['sin_pestana'])} páginas sin la pestaña |")


def strikers_seccion(strikers):
    """Sección 11: lo que no cierra en los strikers."""
    A = strikers['auditoria']
    s = ['## 11. Strikers: la pestaña Striker de la wiki\n']
    s.append('thanosvibs no publica los strikers. La app los toma de la pestaña Striker de la página de cada '
             f"personaje en la wiki ({A['paginas']} páginas la tienen, {A['filas']} filas): quién puede aparecer a "
             'pegar junto a él y con qué probabilidad, cuando él ataca o cuando lo atacan (scripts/strikers.py).\n')
    s.append(f"Personajes sin la pestaña en su página ({len(A['sin_pestana'])}): {', '.join(A['sin_pestana'])}. "
             'En la app no tienen strikers propios; sí pueden ser strikers de otros.\n')
    if A['ilegibles']:
        s.append(f"### Lo que no se pudo leer ({len(A['ilegibles'])})\n")
        s.append('Esa fila no cuenta.\n')
        for x in A['ilegibles']:
            s.append(f"- {x['pagina']}: {x['motivo']} (`{x['fila']}`)")
        s.append('')
    if A['repetidos']:
        s.append(f"### Repetidos en la misma página ({len(A['repetidos'])})\n")
        s.append('Vale la primera fila.\n')
        for x in A['repetidos']:
            s.append(f"- {x['pagina']}: {x['striker']}")
        s.append('')
    if A['imposibles']:
        s.append(f"### Probabilidades imposibles ({len(A['imposibles'])})\n")
        s.append('Más de 100%: un error de la wiki. No se corrige ni se topea: la app la muestra tal cual, marcada como '
                 'dato imposible de la fuente. Hay que verla en el juego.\n')
        for x in A['imposibles']:
            s.append(f"- {x['pagina']}: {x['striker']}, {x['p']:g}% "
                     f"{'cuando él ataca' if x['cuando'] == 'ataca' else 'cuando lo atacan'}")
        s.append('')
    return s


_ESTADO_VERIFICACION = {
    'igual': 'iguales', 'distinto': 'distintos', 'sin_derivar': 'que no se pueden derivar',
    'solo_ls': 'que la Leader Skill no da aparte', 'solo_api': 'que Leads & Supports no publica',
}


def liderazgos_seccion(L, chars, fuentes):
    """Sección 12: los liderazgos que Leads & Supports no publica y el build deriva de la Leader Skill de la API
    (scripts/liderazgos.py): lo aprendido, la verificación contra Leads & Supports, lo derivado y lo que no se pudo
    derivar, con su motivo. fuentes: las de contenido/guia.json, para citar lo que dice el juego."""
    nombre = {r['portrait']: r['character'] + ('' if r['uniformed'] == 'False' else f" — {r['uniform']}")
              for r in chars}

    def pj(p):
        return f'{nombre[p]} (`{p}`)'

    def motivos(x):
        return '; '.join(motivo_txt(m, d) for m, d in x['motivos'])

    def personaje(p):
        return nombre[p].split(' — ')[0]

    def agrupar(xs, det):
        """[(detalle, [(retrato, slot)])]: las de un personaje con el mismo slot y el mismo detalle, juntas."""
        grupos = {}
        for x in sorted(xs, key=lambda x: (nombre[x['p']], x['slot'])):
            grupos.setdefault((personaje(x['p']), x['slot'], det(x)), []).append((x['p'], x['slot']))
        return [(d, ps) for (_, _, d), ps in sorted(grupos.items(), key=lambda kv: (kv[0][0].casefold(), kv[0][1]))]

    def quienes(ps):
        """Un grupo de variantes de un personaje: con su nombre si es una sola, con los retratos si son varias."""
        slot = f", `{ps[0][1]}`" if ps[0][1] else ''
        if len(ps) == 1:
            return pj(ps[0][0]) + slot
        return f"{personaje(ps[0][0])} ({', '.join(f'`{p}`' for p, _ in ps)})" + slot

    def variantes(n):
        return f"{n} {'variante' if n == 1 else 'variantes'}"

    V = L['verificacion']
    con_ls = {x['p'] for x in V}        # cada slot de liderazgo de Leads & Supports tiene su verificación
    nd_v = {x['p'] for x in L['sin_derivar']}
    s = ['## 12. Liderazgos que Leads & Supports no publica\n']
    s.append('Leads & Supports de thanosvibs no publica el liderazgo de todas las variantes. Los que no publica los deriva '
             'el build de la Leader Skill de la API de skills (Ezequiel, 4 de octubre de 2026; scripts/liderazgos.py, '
             'explicado en docs/MODELO.md) y van en los datos con `"src": "api"`: la app dice «según la skill del juego». La '
             'Leader Skill se parte en los dos slots de liderazgo de Leads & Supports, y cada efecto, cada activación y la '
             'condición de cada efecto pasan a lo que publica Leads & Supports según las variantes que tienen las dos cosas '
             '(la correspondencia aprendida, abajo) o, lo que Leads & Supports no publica en ningún liderazgo, según '
             f'{A_MANO} (la correspondencia a mano: un stat del catálogo para cada efecto, y la activación con el texto de '
             'la API). Todo o nada por slot: si algo no cierra, ese slot no se deriva y va abajo con su motivo. Lo derivado no '
             'lleva «Notable», que es una marca de thanosvibs que la API no tiene.\n')
    s.append(f"{len(con_ls)} variantes tienen liderazgo de Leads & Supports y {len(nombre) - len(con_ls)} no. El build "
             f"deriva el de {len(L['derivados'])} ({sum(len(x) for x in L['derivados'].values())} slots); "
             f"{len(L['sin_derivar'])} slots, de {len(nd_v)} variantes, no se pudieron derivar.\n")
    C = L['correspondencia']
    s.append('### Correspondencia aprendida\n')
    s.append(f"De las variantes con liderazgo de Leads & Supports, efecto por efecto: lo que da cada uno de los "
             f"{len(C['efectos'])} efectos de la API (el número del texto, con su signo) y en cuántas variantes se ve.\n")
    s.append('| Efecto de la API | Leads & Supports | Variantes |')
    s.append('|---|---|---|')
    for (ab, desc, g), stats, n in sorted(C['efectos'], key=lambda x: (-x[2], x[0][1])):
        da = ', '.join(st + ('' if val is None else f" {'−' if val[1] < 0 else '+'}n{val[0] + 1}") for st, val in stats)
        s.append(f"| «{desc}» ({ab}){f', con {g}' if g else ''} | {da} | {n} |")
    s.append('')
    s.append('`n1`, `n2`...: el primer número del texto, el segundo... La duración es la del efecto, si la publica.\n')
    s.append('Activaciones: ' + '; '.join(f'«{a}» → «{b}» ({variantes(n)})' for a, b, n in C['activaciones']) + '.\n')
    if C['condiciones']:
        s.append('Condición de cada efecto: ' + '; '.join(f"«{t}» → {', '.join(c or 'ninguna' for c in cs)} ({variantes(n)})"
                                                         for t, cs, n in C['condiciones']) + '.\n')
    X = L['contradicciones']
    contra = ([(f"El efecto «{c[1]}» ({c[0]})", [(', '.join(st for st, _ in v), ps) for v, ps in vals]) for c, vals in X['efectos']]
              + [(f'La activación «{c}»', [(v or 'ninguna', ps) for v, ps in vals]) for c, vals in X['activaciones']]
              + [(f'La condición de «{c}»', [(', '.join(x or 'ninguna' for x in v), ps) for v, ps in vals])
                 for c, vals in X['condiciones']])
    if contra:
        s.append('Contradicciones: Leads & Supports publica distinto lo mismo de la API, así que no se usan.\n')
        for que, vals in contra:
            s.append(f"- {que}: " + ' / '.join(f"{v} ({', '.join(f'`{p}`' for p in ps)})" for v, ps in vals) + '.')
        s.append('')
    M = L['a_mano']
    s.append('### Correspondencia a mano\n')
    s.append(f'De {A_MANO}: lo que Leads & Supports no publica en ningún liderazgo. Cada efecto, con su texto de la API, da '
             'un stat del catálogo con el número del texto, y cada activación va con el texto de la API. Variantes: las que '
             'lo tienen en la Leader Skill.\n')
    s.append('| Efecto de la API | Stat | Variantes |')
    s.append('|---|---|---|')
    s += [f'| «{desc}» ({ab}) | {stat} +n1 | {n} |' for ab, desc, stat, n in M['efectos']]
    s.append('')
    s.append('Activaciones: ' + '; '.join(f'«{a}» ({variantes(n)})' for a, n in M['activaciones']) + '.\n')
    if M['otorga']:
        s.append('«Give Power» que dice el juego: la API no publica qué otorga la Leader Skill, y la ficha del juego sí. El '
                 'slot lleva la restricción del objetivo de la API y, de lo que dice el juego, los efectos, la activación y '
                 'la recarga; la app cita su fuente.\n')
        for p, skill, fs, juego in M['otorga']:
            der = next((f"`{k}` {slot_txt(x)}" for k, x in L['derivados'].get(p, {}).items() if 'otorga' in x), 'no se derivó')
            s.append(f"- {pj(p)}, {skill}: {der}. {', '.join(fuente_md(fuentes[k]) for k in fs)}: {juego}")
        s.append('')
    if M['avisos']:
        s.append('Avisos: ' + '; '.join(M['avisos']) + '.\n')
    s.append('### Verificación contra Leads & Supports\n')
    n = collections.Counter(x['estado'] for x in V)
    s.append('Cada slot de liderazgo de Leads & Supports contra el que la misma regla deriva de su Leader Skill, en stats, '
             'valores, duración, condición, restricción, activación y recarga (no en el nombre ni en «Notable»): de '
             f"{len(V)} slots, " + ', '.join(f'{n[e]} {t}' for e, t in _ESTADO_VERIFICACION.items() if n[e]) + '.\n')
    for estado, titulo in (('distinto', 'Distintos (lo derivado / Leads & Supports)'), ('sin_derivar', 'No se pueden derivar'),
                           ('solo_ls', 'Solo en Leads & Supports'), ('solo_api', 'Solo en la Leader Skill')):
        xs = [x for x in V if x['estado'] == estado]
        if not xs:
            continue
        s.append(f'{titulo}:\n')
        s += [f"- {quienes(ps)}: {det}." if det else f'- {quienes(ps)}.' for det, ps in agrupar(
            xs, lambda x: '; '.join(x['dif']) if 'dif' in x else motivos(x) if 'motivos' in x else '')]
        s.append('')
    s.append(f"### Sin derivar ({len(L['sin_derivar'])} slots en {len(nd_v)} variantes)\n")
    s.append('Variantes sin liderazgo de Leads & Supports con un slot de su Leader Skill que no se pudo derivar, con todos '
             'sus motivos. En docs/COMPLETITUD.md son el faltante «Liderazgo sin completar».\n')
    por = collections.Counter(m for x in L['sin_derivar'] for m, _ in x['motivos'])
    s.append('Por motivo (un slot puede tener más de uno): ' + '; '.join(f'{ROTULOS[m]}, {k}' for m, k in por.most_common())
             + '. Van juntas las variantes de un personaje con los mismos motivos.\n')
    for m, que in (('efecto', 'Efectos sin stat (no están en el catálogo o falta cargarlos a mano)'),
                   ('activacion', 'Activaciones sin correspondencia')):
        n = collections.Counter(d for x in L['sin_derivar'] for mm, d in x['motivos'] if mm == m)
        if n:
            s.append(f'{que}, con los slots que dejan sin derivar: '
                     + '; '.join(f'{d if m == "efecto" else f"«{d}»"}, {k}' for d, k in sorted(n.items(), key=lambda x: (-x[1], x[0])))
                     + '.\n')
    s += [f'- {quienes(ps)}: {det}.' for det, ps in agrupar(L['sin_derivar'], motivos)]
    s.append('')
    s.append(f"### Derivados ({len(L['derivados'])} variantes)\n")
    s.append('Van juntas las variantes de un personaje con el mismo liderazgo derivado.\n')
    der = [{'p': p, 'slot': k, 'x': x[k]} for p, x in L['derivados'].items() for k in LIDERAZGOS if k in x]
    por_p = collections.defaultdict(list)
    for x in der:
        por_p[x['p']].append(f"`{x['slot']}` {slot_txt(x['x'])}")
    s += [f'- {quienes(ps)}: {det}.' for det, ps in agrupar([{'p': p, 'slot': '', 't': '; '.join(ts)} for p, ts in por_p.items()],
                                                            lambda x: x['t'])]
    s.append('')
    return s


def correcciones_seccion(L, fuentes):
    """Sección 5: lo que el build corrige de thanosvibs, con aviso (fuentes.py). L: las listas de la auditoría."""
    def lista(xs):
        return xs if xs else ['Ninguna en estos datos.']
    s = ['## 5. Lo que el build corrige de thanosvibs\n']
    s.append('El build corrige estos datos de thanosvibs con aviso, y la app usa el corregido.\n')
    s.append('### Restricciones de liderazgos y soportes\n')
    s.append('La fuente las clasifica mal; la ficha muestra la original.\n')
    s += lista([f'- `{p}` ({tipo}): la fuente dice {rc[0]} "{rc[1]}"; se usa {r[0]} "{r[1]}".' for p, tipo, rc, r in L['soporte']])
    s.append('')
    s.append('### Nombres de C.T.P.\n')
    s.append('Va el nombre que escribe la ficha del C.T.P. en el juego. El id sigue siendo el de thanosvibs: es la clave del '
             'ícono, de la guía de armado y de lo que guarda la capa.\n')
    s += lista([f"- `{cid}`: thanosvibs dice «{tv}»; se usa «{juego}», como lo escribe el juego "
                f"({', '.join(fuente_md(fuentes[k]) for k in fs)})." for cid, tv, juego, fs in L['ctp_nombre']])
    s.append('')
    s.append('### Texto de los artefactos\n')
    s.append('Va lo que dice la ficha del artefacto en el juego; la app marca la línea y dice lo que publica thanosvibs.\n')
    s += lista([f"- `{p}` ({nombre}): thanosvibs dice «{tv}»; se usa «{t}», como dice el juego "
                f"({', '.join(fuente_md(fuentes[k]) for k in fs)})." for p, nombre, tv, t, fs in L['art_linea']])
    s.append('')
    return s


def bonos_seccion(bonos, fuentes):
    """Sección 10: lo que no cierra en los bonos de equipo."""
    B, A = bonos['bonos'], bonos['auditoria']
    s = ['## 10. Bonos de equipo: la wiki contra sí misma\n']
    tam = collections.Counter(len(b['m']) for b in B)
    juego = [b for b in B if b['f'] != ['wiki-bonos']]
    s.append('thanosvibs no publica los bonos de equipo. La app los toma de la sección Team Bonus de la página de '
             f"cada personaje en la wiki ({A['paginas']} páginas la tienen) y de lo que se vio en el juego "
             '(scripts/contenido/bonos.json), que manda sobre la wiki. Un bono aparece en la página de cada '
             'integrante: valen el nombre y los stats que dice la mayoría de sus páginas, y si empatan la app muestra '
             'todas las versiones empatadas. La wiki redondea los valores a un decimal (scripts/bonos.py).\n')
    s.append(f"{len(B)} bonos: {tam[2]} de dos integrantes y {tam[3]} de tres; {len(juego)} del juego "
             f"({', '.join(fuente_md(fuentes[k]) for k in sorted({k for b in juego for k in b['f']}))}).\n"
             if juego else f"{len(B)} bonos: {tam[2]} de dos integrantes y {tam[3]} de tres.\n")
    s.append(f"Personajes sin la sección en su página ({len(A['sin_seccion'])}): {', '.join(A['sin_seccion'])}. Sus bonos "
             'están solo si la página de otro integrante los lista.\n')
    if A['juego']:
        s.append(f"### Del juego ({len(A['juego'])})\n")
        s.append('| Bono | Integrantes | La wiki decía |')
        s.append('|---|---|---|')
        for j in A['juego']:
            wiki = ' / '.join(_version(v) for v in j['wiki']) or 'no lo tiene'
            s.append(f"| {j['nombre']} | {', '.join(j['integrantes'])} | {wiki} |")
        s.append('')
    for clave, titulo, nota in (
            ('empates', 'Versiones empatadas', 'Ninguna versión tiene más páginas: la app las muestra todas.'),
            ('mayorias', 'Versiones en minoría', 'Vale la primera, la de más páginas.')):
        if A[clave]:
            s.append(f'### {titulo} ({len(A[clave])})\n')
            s.append(nota + '\n')
            s.append('| Integrantes | Versiones (páginas que dicen cada una) |')
            s.append('|---|---|')
            for x in A[clave]:
                s.append(f"| {', '.join(x['integrantes'])} | "
                         + ' — '.join(f"{_version(v)} ({', '.join(ps)})" for v, ps in x['versiones']) + ' |')
            s.append('')
    if A['nombres_empatados']:
        s.append(f"### Nombres empatados ({len(A['nombres_empatados'])})\n")
        s.append('La app los muestra juntos, separados por « / ».\n')
        for x in A['nombres_empatados']:
            s.append(f"- {', '.join(x['integrantes'])}: {' / '.join(x['nombres'])}")
        s.append('')
    sin_nombre = [b for b in B if not b['n']]
    if sin_nombre:
        s.append('Sin nombre en ninguna de sus páginas: ' + '; '.join(', '.join(b['m']) for b in sin_nombre) + '.\n')
    if A['desconocidos']:
        s.append('### Stats que la app no conoce\n')
        s.append('Van como los escribe la wiki: la sinergia los cuenta para todos y dice que no están clasificados. '
                 'Si son un stat conocido con otro nombre, se agregan a STATS en scripts/bonos.py.\n')
        for st, ps in A['desconocidos'].items():
            s.append(f"- `{st}`: {', '.join(ps)}")
        s.append('')
    if A['falta_en_pagina']:
        s.append(f"### Bonos que la página de un integrante no lista ({len(A['falta_en_pagina'])})\n")
        por_pagina = collections.defaultdict(list)
        for x in A['falta_en_pagina']:
            por_pagina[x['pagina']].append(' + '.join(i for i in x['integrantes'] if i != x['pagina']))
        for p, otros in sorted(por_pagina.items()):
            s.append(f"- {p}: con {'; con '.join(otros)}")
        s.append('')
    if A['ilegibles']:
        s.append(f"### Lo que no se pudo leer ({len(A['ilegibles'])})\n")
        s.append('Esa página no cuenta para ese bono.\n')
        for x in A['ilegibles']:
            s.append(f"- {x['pagina']}" + (f", {x['bono']}" if x['bono'] else '') + f": {x['motivo']}")
        s.append('')
    return s


def main():
    A = Auditoria()
    A.correr()
    version = ultima(cargar('work/updates.json'))[1]
    hallazgos = cargar(os.path.join(_DIR, 'contenido', 'hallazgos.json'))
    fuentes = cargar(os.path.join(_DIR, 'contenido', 'guia.json'))['fuentes']
    malas = sorted({k for x in hallazgos for k in x['fuente'] if k not in fuentes})
    if malas:
        raise SystemExit(f'contenido/hallazgos.json cita fuentes sin definir en contenido/guia.json: {malas}')
    os.makedirs('docs', exist_ok=True)
    catalogo = cargar('work/catalogo.json')
    f = cargar('work/fuentes.json')
    bonos = {'bonos': f['bonos'], 'auditoria': f['bonos_auditoria']}
    strikers = {'strikers': f['strikers'], 'auditoria': f['strikers_auditoria']}
    open('docs/AUDITORIA.md', 'w', encoding='utf-8', newline='\n').write(
        informe(A, version, hallazgos, fuentes, catalogo, bonos, strikers, f['liderazgos_auditoria']))
    por = {p: v for p, v in A.por_retrato.items() if v['ok'] or v['nd'] or v['dif']}
    json.dump({'resumen': dict(A.res), 'por_retrato': por}, open('work/verificacion.json', 'w', encoding='utf-8'),
              ensure_ascii=False)
    R = A.res
    print(f"auditoría: skills en la wiki {R['skills_en_wiki']}/{R['skills']} | daño distinto {R['dano_dif']} | "
          f"recarga distinta {R['cd_dif']} | infobox distinto {sum(R[k + '_dif'] for k in ('type', 'side', 'gender', 'allies', 'atk'))} | "
          f"instinto {R['instinto_dif']} | artefactos {R['artefactos_dif']} | docs/AUDITORIA.md")


if __name__ == '__main__':
    main()
