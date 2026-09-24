#!/usr/bin/env python3
"""Transforma las fuentes de thanosvibs que no son personajes ni skills al modelo de la
app: C.T.P.s (/api/ctps) y artefactos (/api/artifacts). Lo llama build.py y deja
work/fuentes.json.

Los nombres de C.T.P. y de artefacto quedan en inglés por la misma razón que los de
personaje y uniforme: son el identificador con el que se cruza el juego.
"""
import json, re


def slug(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


def ctps():
    out = []
    for c in json.load(open('work/ctps.json', encoding='utf-8')):
        out.append({'id': slug(c['name']), 'name': c['name']})
    return out


def artefactos(retratos_base):
    out = []
    for a in json.load(open('work/artifacts.json', encoding='utf-8')):
        if a['portrait'] not in retratos_base:
            # Un artefacto de un personaje que no está en el roster no tiene dónde mostrarse.
            raise SystemExit(f"artefacto {a['artifact_name']} de un retrato que no está en el roster: {a['portrait']}")
        out.append({'p': a['portrait'], 'name': a['artifact_name'], 'pasiva': a['passive_name'],
                    'pve': a['pve_score'], 'pvp': a['pvp_score'], 'desde': a['update']})
    return out


def main():
    chars = json.load(open('work/characters.json', encoding='utf-8'))
    base = {r['base_portrait'] for r in chars}
    salida = {'ctps': ctps(), 'artefactos': artefactos(base)}
    json.dump(salida, open('work/fuentes.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"fuentes: {len(salida['ctps'])} C.T.P.s | {len(salida['artefactos'])} artefactos")


if __name__ == '__main__':
    main()
