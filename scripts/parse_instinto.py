#!/usr/bin/env python3
"""Saca el instinto de cada personaje del wikitext de Fandom.

Es lo único que sigue viniendo de la wiki: thanosvibs no publica el instinto en
ninguna de sus APIs. Las skills salen de scripts/skills_api.py.
"""
import glob, json, re

resultado = {}
for fn in glob.glob('work/wikitext/*.json'):
    d = json.load(open(fn, encoding='utf-8'))
    m = re.search(r'\|\s*instinct\s*=\s*(?:\[\[:Category:\w+\|)?([A-Za-z]+)', d['wt'])
    resultado[d['name']] = {'instinct': m.group(1) if m else ''}
json.dump(resultado, open('work/instintos.json', 'w'), ensure_ascii=False)
con = sum(1 for v in resultado.values() if v['instinct'])
print(f'instintos: {con}/{len(resultado)} personajes con instinto en la wiki')
