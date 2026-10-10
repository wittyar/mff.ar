"""Resumen de un JSON de medir_solapado.py (medidas/solapado.json, primera parte; solapado2.json, segunda): por contexto, cuántas listas y filas cambian, con ejemplos; los
tríos al azar; el filtro del último uniforme sobre todas las listas; los tiempos.
  python3 analizar_solapado.py medidas/solapado.json medidas/nombres.json"""
import json, sys
from collections import Counter

res = json.load(open(sys.argv[1]))
NOM = json.load(open(sys.argv[2]))
cid_nombre = {}
for k, n in NOM.items():
    if k.endswith('::base'): cid_nombre[k.split('::')[0]] = n
nk = lambda k: NOM.get(k, k)
np_ = lambda p: ' + '.join(cid_nombre.get(c, c) for c in p)
fmt = lambda n: f'{n:,}'.replace(',', '.')

print('viejo', res['viejo'], 'segundos', res['segundos'], 'errores', res['errores'])
for o, titulo in (('foco', 'Puntos para él'), ('pvp', 'PvP'), ('pve', 'PvE')):
    ls = res[o]
    cambian = {k: x for k, x in ls.items() if not x['igual']}
    antes, ahora = sum(x['antes'] for x in ls.values()), sum(x['ahora'] for x in ls.values())
    S = lambda c: sum(len(x[c]) for x in ls.values())
    con = lambda c: sum(1 for x in ls.values() if x[c])
    print(f"\n== {titulo}: {len(ls)} listas; cambian {len(cambian)} ({100 * len(cambian) / len(ls):.0f}%)")
    print(f"   filas {fmt(antes)} → {fmt(ahora)} ({100 * (ahora - antes) / antes:+.1f}%); salen {fmt(S('salen'))} en {con('salen')} listas, "
          f"entran {fmt(S('entran'))} en {con('entran')}; otra combinación de uniformes {fmt(S('otra_fila'))} en {con('otra_fila')}; "
          f"otro puntaje {fmt(S('puntaje'))} en {con('puntaje')}; otro líder {fmt(S('lider'))} en {con('lider')}; con otro orden {sum(1 for x in ls.values() if x['orden'])}")
    print(f"   listas que se achican {sum(1 for x in ls.values() if x['ahora'] < x['antes'])}, que crecen {sum(1 for x in ls.values() if x['ahora'] > x['antes'])}, "
          f"que quedan vacías {sum(1 for x in ls.values() if x['antes'] and not x['ahora'])}")
    # las que más bajan, en número y en proporción
    for k, x in sorted(cambian.items(), key=lambda kv: kv[1]['ahora'] - kv[1]['antes'])[:6]:
        print(f"   - {nk(k)}: {fmt(x['antes'])} → {fmt(x['ahora'])} (salen {len(x['salen'])}, entran {len(x['entran'])}, "
              f"otro puntaje {len(x['puntaje'])}, otro líder {len(x['lider'])})"
              + (f"; ej. {np_(x['salen'][0])} sale" if x['salen'] else '')
              + (f"; ej. {np_(x['ej_puntaje'][0][0])}: {x['ej_puntaje'][0][1]} → {x['ej_puntaje'][0][2]}" if x['ej_puntaje'] else ''))
    prop = [(k, x) for k, x in cambian.items() if x['antes'] >= 100]
    for k, x in sorted(prop, key=lambda kv: kv[1]['ahora'] / kv[1]['antes'])[:4]:
        print(f"   % {nk(k)}: {fmt(x['antes'])} → {fmt(x['ahora'])} ({100 * (x['ahora'] - x['antes']) / x['antes']:+.0f}%)")
    # cuánto cambia el puntaje en las que cambian (de los ejemplos guardados: hasta 3 por lista)
    d = Counter(round(n - v, 2) for x in ls.values() for _, v, n in x['ej_puntaje'])
    print('   diferencias de puntaje en los ejemplos (hasta 3 por lista):', d.most_common(8))
    if o == 'pvp' or o == 'pve':
        sube = [(k, x) for k, x in ls.items() if x['entran']]
        print(f"   listas con parejas que entran: {len(sube)}", [(nk(k), len(x['entran']), np_(x['entran'][0])) for k, x in sube[:3]])

print('\n== tríos al azar')
for n, x in res['trios'].items():
    r = x['repetidos']
    print(f" {n}: {fmt(x['n'])} tríos ({x['candidatas']} variantes son candidatas: en la primera parte, algo sin valor; en la segunda, algo que no se acumula; o anti-mermas propios); cambia la sinergia en {fmt(x['sinergia'])} "
          f"({100 * x['sinergia'] / x['n']:.1f}%), el líder sin contexto en {fmt(x['lider'])} ({100 * x['lider'] / x['n']:.1f}%); "
          f"en PvP entran {fmt(x['en_pvp'])} y cambia el puntaje o el líder en {fmt(x['pvp'])}; en PvE entran {fmt(x['en_pve'])} y cambia en {fmt(x['pve'])}; "
          f"con algo que no se suma {fmt(r['trios'])} ({100 * r['trios'] / x['n']:.1f}%): {sorted(r['stats'].items(), key=lambda kv: -kv[1])}")
    for t, v, w in x['ej'][:4]:
        print('   ej.', ' + '.join(nk(k) for k in t), '| sinergia', v[0], '→', w[0], '| líder', nk(v[1]) if v[1] else None, '→', nk(w[1]) if w[1] else None,
              '| pvp', v[2], '→', w[2], '| pve', v[3], '→', w[3])

print('\n== último uniforme (la app nueva, con la regla)')
for o in ('foco', 'pvp', 'pve'):
    ls = res[o]
    a, u = sum(x['ahora'] for x in ls.values()), sum(x['ultimo'] for x in ls.values())
    print(f" {o}: {len(ls)} listas, {fmt(a)} → {fmt(u)} combinaciones ({100 * (u - a) / a:+.1f}%); vacías con el filtro {sum(1 for x in ls.values() if x['ahora'] and not x['ultimo'])}")

print('\n== tiempos (ms)')
for o in ('foco', 'pvp', 'pve'):
    for n in ('viejo', 'nuevo'):
        xs = [x['ms'][n] for x in res[o].values()]
        tot_c, tot_v = sum(c or 0 for c, _ in xs), sum(v for _, v in xs)
        peor = max(res[o].items(), key=lambda kv: (kv[1]['ms'][n][0] or 0) + kv[1]['ms'][n][1])
        print(f" {o} {n}: consulta {fmt(tot_c)}, vista {fmt(tot_v)}; la más lenta {nk(peor[0])} {peor[1]['ms'][n]}")
