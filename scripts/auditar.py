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

Lo llama build.py después de skills_api.py y fuentes.py.
"""
import collections, datetime, difflib, glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from version_juego import ultima

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


def informe(A, version, hallazgos, fuentes):
    R, L = A.res, A.listas
    hoy = datetime.date.today().isoformat()
    s = []
    s.append('# Auditoría de datos\n')
    s.append(f'Generado por `scripts/auditar.py` el {hoy}, sobre los datos del juego {version} '
             f'(thanosvibs) y la wiki de Future Fight bajada en la misma sincronización.\n')
    s.append('La app muestra thanosvibs. Esto marca dónde otra fuente dice otra cosa, con los dos '
             'valores; no corrige nada. La wiki la edita la comunidad y muchas páginas quedaron '
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
    s.append(f"| Artefactos a 6★ (thanosvibs vs wiki) | {R['artefactos_ok']} (+{R['artefactos_otro_nivel']} donde la wiki lista otro nivel de estrellas) | {R['artefactos_dif']} | {R['artefactos_sin_wiki']} sin fila en la wiki; {R['artefactos_incompletos']} con niveles incompletos en thanosvibs |")
    s.append('')
    s.append(f"Cobertura de la wiki: de {R['skills']} skills (activas, Definitiva y Striker) de thanosvibs, "
             f"{R['skills_en_wiki']} ({pct(R['skills_en_wiki'], R['skills'])}) se pudieron comparar; "
             f"{R['skills_otra_seccion']} están en la página pero solo en la sección de otro uniforme, y el resto "
             f"no aparece (sobre todo uniformes que la wiki no documenta). Infobox: {R['infobox_con']} retratos "
             f"con pestaña en la wiki, {R['infobox_sin_pestana']} sin pestaña de su uniforme y {R['infobox_sin']} "
             f"de personajes sin infobox legible.\n")

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
    s.append(f"- Textos de efecto con marcadores de plantilla sin resolver ($HEROSUBTYPE, $HEROCLASS...): "
             f"{R['marcadores_patrones']} patrones, usados por {R['marcadores_retratos']} retratos. La app los "
             f"muestra como \"sin especificar en la fuente\" en vez de inventar el valor.")
    s.append('')

    s.append('## 5. Efectos de líder y soporte: restricciones corregidas\n')
    s.append('La fuente clasifica mal estas restricciones; el build las corrige con aviso y la ficha '
             'muestra la original.\n')
    for p, tipo, rc, r in L['soporte']:
        s.append(f'- `{p}` ({tipo}): la fuente dice {rc[0]} "{rc[1]}"; se usa {r[0]} "{r[1]}".')
    s.append('')

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
        citas = ', '.join(f"[{fuentes[k]['nombre']}]({fuentes[k]['url']})" for k in x['fuente'])
        s.append(f"- **{x['titulo']}** — {x['es']} ({citas})")
    s.append('')
    return '\n'.join(s)


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
    open('docs/AUDITORIA.md', 'w', encoding='utf-8').write(informe(A, version, hallazgos, fuentes))
    por = {p: v for p, v in A.por_retrato.items() if v['ok'] or v['nd'] or v['dif']}
    json.dump({'resumen': dict(A.res), 'por_retrato': por}, open('work/verificacion.json', 'w', encoding='utf-8'),
              ensure_ascii=False)
    R = A.res
    print(f"auditoría: skills en la wiki {R['skills_en_wiki']}/{R['skills']} | daño distinto {R['dano_dif']} | "
          f"recarga distinta {R['cd_dif']} | infobox distinto {sum(R[k + '_dif'] for k in ('type', 'side', 'gender', 'allies', 'atk'))} | "
          f"instinto {R['instinto_dif']} | artefactos {R['artefactos_dif']} | docs/AUDITORIA.md")


if __name__ == '__main__':
    main()
