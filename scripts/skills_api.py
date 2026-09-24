#!/usr/bin/env python3
"""Transforma work/skills_api/*.json (la API de skills de thanosvibs) al formato del
snapshot, en los dos idiomas.

Por qué esta fuente y no la wiki: la API es el modelo de datos del juego. Trae las
skills de cada uniforme, la Uniform Passive y la Striker Skill, el cooldown y el
porcentaje de carga de ult y de striker, y cada efecto ya viene tipado (abilityId +
etiqueta) en vez de ser texto libre. De la wiki sale solo el instinto; auditar.py la usa
además para contrastar daño y recarga, sin cambiar nada de lo que sale de acá.
Lo que se pierde: la geometría del golpe (hits, melee/ranged, área, empuje), que la
API no publica.

Formato de salida
-----------------
Los 41.152 efectos usan solo 299 descripciones distintas y 228 etiquetas. Guardar el
texto en cada efecto, y encima en dos idiomas, daba 11 MB. En vez de eso el efecto
guarda el índice del patrón y sus números, y el texto se arma en el navegador:

    {"a": 12, "p": 3, "v": [152, 1067]}   ->  "Daño físico: 152% del ataque físico.
                                               504 de daño físico adicional."

Los diccionarios (patrones, etiquetas, elementos, objetivos, activaciones, nombres)
viajan una sola vez con las dos versiones.
"""
import json, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traducir

BOLD = re.compile(r'</?b>')
NUM = re.compile(r'\d+(?:\.\d+)?')

# Los patrones de daño tienen todos la misma forma: elemento, porcentaje sobre un
# atributo, y daño extra plano. Se anotan los índices para que la app pueda leer esos
# números sin volver a parsear el texto.
DMG_HEAD = re.compile(r'^(?P<elem>[A-Za-z ]+?) Damage:\s*#%\s*of\s*(?P<src>Physical Attack|Energy Attack|HP)')
DMG_FLAT = re.compile(r'Additional\s*#\s*[A-Za-z ]*?Damage\.?\s*$')

ORDEN = ['Leader Skill', 'Passive', 'Tier-2 Passive', 'Uniform Passive',
         'Active 1', 'Active 2', 'Active 3', 'Active 4', 'Active 5', 'Active Ult', 'Striker Skill']
# Claves del objeto `skills` que no son skills. `cancels` dice qué skills aplican cada
# control que corta los ataques especiales del jefe en Alliance Battle (Silence, Paralyze
# y Burn en Extreme; Snare, Shock y Fracture en Legend). Se guarda aparte: tomarla como
# skill creaba un slot "cancels" sin nombre ni etapas.
NO_SKILLS = {'cancels'}
# La fuente pone recarga 1 (o 0) a las skills que no se recargan por tiempo sino con
# una barra: la Definitiva de Tier-3 (barra de ult) y la Striker Skill (barra de
# striker). La Definitiva de los Trascendidos sí trae su recarga real (40 a 60 s). Se
# guardan sin recarga en vez de mostrar "CD 1s".
CON_BARRA = {'Active Ult', 'Striker Skill'}

def limpio(txt):
    return re.sub(r'\s{2,}', ' ', BOLD.sub('', txt or '')).strip()

class Tabla:
    """Diccionario inglés->español convertido en lista indexada, con las dos versiones."""
    def __init__(self, traduccion, por_patron=False):
        self.tr, self.por_patron = traduccion, por_patron
        self.idx, self.filas, self.faltan = {}, [], set()
    def id(self, valor):
        if not valor: return None
        clave = traducir.patron(valor) if self.por_patron else valor
        if clave in self.idx: return self.idx[clave]
        es = self.tr(clave)
        if es is None: self.faltan.add(clave)
        fila = {'en': clave, 'es': es}
        if self.por_patron:
            m = DMG_HEAD.match(clave)
            if m:
                # posición del % y del daño extra dentro de los números de la línea
                fila['pi'] = 0
                if DMG_FLAT.search(clave): fila['fi'] = 1
                fila['src'] = m.group('src')
                fila['elem'] = m.group('elem').strip()
        self.idx[clave] = len(self.filas)
        self.filas.append(fila)
        return self.idx[clave]

def main():
    T = {'desc': Tabla(traducir.EFECTOS.get, por_patron=True),
         'ab':   Tabla(traducir.traducir_etiqueta),
         'elem': Tabla(traducir.traducir_elemento),
         'tgt':  Tabla(traducir.traducir_objetivo),
         'act':  Tabla(lambda p: traducir.ACTIVACIONES.get(p), por_patron=True),
         'name': Tabla(traducir.traducir_skill)}
    salida, buffs, cancels = {}, {}, {}
    desconocidas = {}
    n_sk = n_st = n_fx = n_barra = 0

    def efecto(a):
        d = limpio(a.get('description'))
        f = {'a': T['ab'].id(a.get('ability')), 'p': T['desc'].id(d)}
        v = [float(x) if '.' in x else int(x) for x in NUM.findall(d)]
        if v: f['v'] = v
        if a.get('duration') is not None: f['d'] = a['duration']
        if a.get('tick') is not None: f['t'] = a['tick']
        if a.get('persistent'): f['m'] = 1
        if a.get('team_buff'): f['b'] = 1
        return f

    def etapa(st):
        e = {'fx': [efecto(a) for a in st.get('abils', [])]}
        if st.get('element'): e['el'] = T['elem'].id(st['element'])
        if st.get('target'): e['tg'] = T['tgt'].id(st['target'])
        if st.get('activation'):
            act = limpio(st['activation'])
            e['ac'] = T['act'].id(act)
            av = [float(x) if '.' in x else int(x) for x in NUM.findall(act)]
            if av: e['av'] = av
        return e

    for fn in sorted(glob.glob('work/skills_api/*.json')):
        d = json.load(open(fn, encoding='utf-8'))
        p = d.get('portrait') or os.path.basename(fn)[:-5]
        sk = d.get('skills') or {}
        # Una clave que no es skill conocida ni dato conocido corta el build: tomarla
        # como skill inventaría un slot, y descartarla en silencio perdería un dato.
        for tipo in sk:
            if tipo not in ORDEN and tipo not in NO_SKILLS:
                desconocidas.setdefault(tipo, []).append(p)
        if sk.get('cancels'):
            cancels[p] = sk['cancels']
        lista = []
        for tipo in [t for t in ORDEN if t in sk]:
            s = sk[tipo]
            cd = s.get('cooldown')
            if tipo in CON_BARRA and cd is not None and cd <= 1:
                cd = None
                n_barra += 1
            out = {'sl': tipo, 'n': T['name'].id(s.get('name')), 'cd': cd,
                   'st': [etapa(x) for x in s.get('stages', [])]}
            if s.get('ult_charge') is not None: out['ult'] = s['ult_charge']
            if s.get('striker_charge') is not None: out['stk'] = s['striker_charge']
            lista.append(out)
            n_sk += 1; n_st += len(out['st'])
            n_fx += sum(len(x['fx']) for x in out['st'])
        salida[p] = lista
        if d.get('key_abilities'):
            buffs[p] = {k: v.get('skills', []) for k, v in d['key_abilities'].items()}

    if desconocidas:
        raise SystemExit('claves de skills desconocidas en la API: ' +
                         '; '.join(f'{k} (en {len(v)} retratos, p.ej. {v[0]})' for k, v in desconocidas.items()) +
                         ' — decidir en scripts/skills_api.py si es skill (ORDEN) o dato aparte (NO_SKILLS)')
    tablas = {k: t.filas for k, t in T.items()}
    json.dump({'skills': salida, 'buffs': buffs, 'cancels': cancels, 'tablas': tablas},
              open('work/skills_parsed.json', 'w'), ensure_ascii=False)
    for k, t in T.items():
        json.dump(sorted(t.faltan), open(f'work/sin_traducir_{k}.json', 'w'), ensure_ascii=False, indent=1)
    tam = os.path.getsize('work/skills_parsed.json') / 1024 / 1024
    print(f'portraits: {len(salida)} | skills: {n_sk} | etapas: {n_st} | efectos: {n_fx} | {tam:.1f} MB'
          f' | con cancels: {len(cancels)} | de barra, sin recarga: {n_barra}')
    print('tablas: ' + ' | '.join(f'{k} {len(t.filas)}' for k, t in T.items()))
    faltan = {k: len(t.faltan) for k, t in T.items() if t.faltan}
    print('sin traducir:', faltan or 'nada')

if __name__ == '__main__':
    main()
