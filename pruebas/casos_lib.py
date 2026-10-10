"""Rankings de los casos con cualquier juego de pesos, igual que vistaConsulta: puntaje de mayor a
menor; a igual puntaje, puestos en las listas del contexto, referencia y orden de la consulta; un
trío por pareja de personajes (el primero en ese orden)."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json
SP = PRUEBAS
ACTUAL = (2, 2, 1, 1)   # liderazgo, dps, sinergia, striker

def cargar(*archivos):
    R = {'focos': {}, 'vars': {}}
    for a in archivos:
        d = json.load(open(f'{SP}/{a}'))
        R['focos'].update(d['focos']); R['vars'].update(d['vars'])
    return R

def ranking(R, foco, ctx, w=ACTUAL, n=None):
    F = R['focos'][foco]; pool = F['pool']; V = R['vars']
    filas = F['ctx'][ctx]
    def pts(f): return w[0] * f[2] + w[1] * f[3] + w[2] * f[4] + w[3] * f[5]
    orden = sorted(filas, key=lambda f: (-pts(f), f[6], f[7], f[9]))
    vistos, out = set(), []
    for f in orden:
        a, b = pool[f[0]], pool[f[1]]
        par = tuple(sorted((V[a][1], V[b][1])))
        if par in vistos: continue
        vistos.add(par); out.append((f, pts(f)))
        if n and len(out) >= n: break
    return out

def nombre(R, k): return R['vars'][k][0]

def miembros(R, foco, f):
    pool = R['focos'][foco]['pool']
    return [foco, pool[f[0]], pool[f[1]]]

def linea(R, foco, f, p):
    ms = miembros(R, foco, f)
    lider = nombre(R, ms[f[8]])
    otros = ' + '.join(nombre(R, k) for k in ms[1:])
    return f'{p:>3} | L{f[2]:>2} D{f[3]:>2} S{f[4]:>2} K{f[5]:>2} | líder {lider:<34.34} | {otros}'
