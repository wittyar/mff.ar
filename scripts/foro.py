#!/usr/bin/env python3
"""Notas de actualización del foro oficial de MARVEL Future Fight (Netmarble), para el histórico.

Los tableros (TABLEROS): el de las notas (2196, «Update Details», «Patch Details») y el de avisos (2213), donde están las
notas de los parches de mitad de mes de 2020 y 2021 («6/10 Patch (Updated)») y algunas viejas («Patch 1.6: Howling
Commandos», «3.6.0 Patch Notes») que el de notas no tiene (#5); de los avisos se bajan solo esas, no los «Server Patch».

Uso:
  python scripts/foro.py            # la primera página de la lista y las notas nuevas que traiga (el workflow semanal)
  python scripts/foro.py --todo     # todas las páginas de la lista y todas las notas que falten (la primera vez)

Deja una copia de cada nota en fuentes/foro/<id>.json (id, título, fechas y el HTML del contenido) y la lista de las
notas en fuentes/foro/indice.json, en el repo: el build lee de ahí, sin red. Una nota ya bajada no se vuelve a pedir.
Nota es lo que el título dice que es una nota de actualización o de parche (NOTA, abajo); los avisos de mantenimiento y
lo demás del tablero no se bajan.

Una consulta por vez, con PAUSA segundos entre una y otra, para no cargar los servidores del foro. La lista corta el
contenido de cada artículo (203 caracteres), así que cada nota se pide aparte.
Solo biblioteca estándar."""
import json, os, re, sys, time, urllib.request

API = 'https://forum.netmarble.com/api/game/mherosgb/official/forum/futurefight_en'
LISTA = API + '/article/list?rows=15&start={}&viewType=pv&menuSeq={}&sort=RECENTLY'
ARTICULO = API + '/article/{}?menuSeq={}&viewFlag=true'
VER = 'https://forum.netmarble.com/futurefight_en/view/{}/{}'
UA = {'User-Agent': 'Mozilla/5.0 (mff-comparador; uso personal)'}
PAUSA = 6
ESPERA = 60
# Qué es una nota en cada tablero, por el título.
TABLEROS = {
    2196: re.compile(r'update details|patch details|patch notes|version details', re.I),
    2213: re.compile(r'^(\d+/\d+ |[\d.]+ )?patch (notes|details|\((updated|completed)\))|^patch \d+\.\d+:', re.I),
}
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fuentes', 'foro')


def pedir(url, negado_ok=False):
    """La respuesta del foro. Con negado_ok, un artículo que el foro no deja leer (51006, NO PERMISSION MEMBER ARTICLE
    ERROR: le pasa a la 1.3.1, de 2015) devuelve None; cualquier otro error corta."""
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
    except OSError as e:
        # Un corte de red o del foro: se espera ESPERA segundos y se pide una vez más; si vuelve a fallar, corta.
        print(f'  AVISO {url}: {e}; otra vez en {ESPERA} s', flush=True)
        time.sleep(ESPERA)
        d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
    time.sleep(PAUSA)
    if negado_ok and d.get('code') == 51006:
        return None
    if d.get('code') != 0:
        raise SystemExit(f'el foro contestó {d.get("code")} {d.get("msg")!r} a {url}')
    return d


def guardar(indice, ruta):
    json.dump(sorted(indice.values(), key=lambda n: n['fecha']), open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def main(todo):
    os.makedirs(DIR, exist_ok=True)
    ruta_indice = os.path.join(DIR, 'indice.json')
    indice = {n['id']: n for n in json.load(open(ruta_indice, encoding='utf-8'))} if os.path.exists(ruta_indice) else {}
    nuevas = []
    for menu, nota in TABLEROS.items():
        vistas, start, total = {}, 0, None
        while total is None or (todo and start < total):
            d = pedir(LISTA.format(start, menu))
            total = d['totalCount']
            for a in d['articleList']:
                vistas[a['id']] = a
            start += 15
        nuevas += [(menu, a) for a in vistas.values() if nota.search(a['title']) and a['id'] not in indice]
        print(f'foro, tablero {menu}: {len(vistas)} artículos vistos de {total}', flush=True)
    print(f'foro: {len(nuevas)} notas nuevas', flush=True)
    for menu, a in sorted(nuevas, key=lambda x: x[1]['regDate']):
        d = pedir(ARTICULO.format(a['id'], menu), negado_ok=True)
        if d is None:
            # Queda en el índice con el motivo, para no volver a pedirla; el build la cuenta como nota sin texto.
            indice[a['id']] = {'id': a['id'], 'titulo': a['title'], 'fecha': a['regDate'], 'url': VER.format(menu, a['id']),
                               'error': 'el foro no deja leerla (51006, NO PERMISSION MEMBER ARTICLE ERROR)'}
            print(f"  AVISO {a['id']} {a['title']}: el foro no deja leerla", flush=True)
            guardar(indice, ruta_indice)
            continue
        x = d['article']
        nota = {'id': x['id'], 'titulo': x['title'], 'fecha': x['regDate'], 'modificada': x.get('modDate'),
                'url': VER.format(menu, x['id']), 'html': x['content']}
        json.dump(nota, open(os.path.join(DIR, f"{x['id']}.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        indice[x['id']] = {k: nota[k] for k in ('id', 'titulo', 'fecha', 'url')}
        print(f"  {x['id']} {x['title']}", flush=True)
        guardar(indice, ruta_indice)   # después de cada nota: si algo corta, no se vuelve a pedir lo ya bajado
    guardar(indice, ruta_indice)
    print(f'foro: {len(indice)} notas en fuentes/foro/', flush=True)


if __name__ == '__main__':
    main('--todo' in sys.argv[1:])
