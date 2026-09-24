#!/usr/bin/env python3
"""Saca el instinto de cada personaje del wikitext de Fandom.

Es lo único que sigue viniendo de la wiki: thanosvibs no publica el instinto en
ninguna de sus APIs. Las skills salen de scripts/skills_api.py.

El infobox de la wiki declara el instinto en `instinct=` o, en las páginas con un
infobox por uniforme, en `instinct1=`, `instinct2=`...; y el valor viene escrito de
varias formas ("Justice", "[[Instinct|Order]]", "[[:Category:Cruelty|Cruelty]]",
"[[File:Order.png|16x16px]] [[Order]]"). Antes solo se reconocía `instinct=` con las
dos primeras, y 47 personajes que sí lo declaran quedaban como desconocidos.
"""
import glob, json, re

INSTINTOS = {'Justice', 'Order', 'Destruction', 'Cruelty'}
CAMPO = re.compile(r'^\|\s*instinct(\d*)\s*=\s*(.*)$', re.M)

resultado, avisos = {}, []
for fn in sorted(glob.glob('work/wikitext/*.json')):
    d = json.load(open(fn, encoding='utf-8'))
    valores = []
    for m in CAMPO.finditer(d['wt']):
        nombres = {w for w in re.findall(r'[A-Za-z]+', m.group(2)) if w in INSTINTOS}
        if len(nombres) > 1:
            avisos.append(f"{d['name']}: instinct{m.group(1)} nombra varios instintos {sorted(nombres)}")
        valores += sorted(nombres)
    distintos = sorted(set(valores))
    if len(distintos) > 1:
        # El modelo guarda un instinto por personaje; si la wiki declara uno distinto
        # por uniforme se avisa y queda el primero declarado.
        avisos.append(f"{d['name']}: la wiki declara instintos distintos por uniforme {distintos}; queda {valores[0]}")
    resultado[d['name']] = {'instinct': valores[0] if valores else ''}
json.dump(resultado, open('work/instintos.json', 'w'), ensure_ascii=False)
for a in avisos:
    print('AVISO', a)
con = sum(1 for v in resultado.values() if v['instinct'])
print(f'instintos: {con}/{len(resultado)} personajes con instinto en la wiki')
sin = sorted(n for n, v in resultado.items() if not v['instinct'])
if sin:
    print('  sin instinto declarado en el infobox:', ', '.join(sin))
