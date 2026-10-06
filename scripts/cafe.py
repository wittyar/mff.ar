#!/usr/bin/env python3
"""Las notas de actualización del foro coreano de MARVEL Future Fight, para revisar las del foro en inglés (#3).

El foro coreano es el café oficial de Naver (cafe.naver.com/futurefight, «마블 퓨처파이트 공식 커뮤니티»): las notas
de actualización van al tablero «점검 & 업데이트» (4) y las de parche a «패치 내역 안내» (141). El juego es coreano:
el texto coreano es el original y el inglés, su traducción.

Uso:
  python scripts/cafe.py            # la primera página de cada tablero y los pares que falten (el workflow semanal)
  python scripts/cafe.py --todo     # todas las páginas de los dos tableros (la primera vez)

De cada nota del foro en inglés (fuentes/foro/indice.json) se baja su par coreana: la nota del café de fecha más cercana,
a VENTANA días o menos (las dos salen casi siempre a la misma hora), con preferencia por la del mismo tipo (actualización
o parche, por el título: par()). Con --todo se rehacen todos los pares. Deja fuentes/cafe/<id>.json (id, título, fecha, url, las notas en inglés que acompaña, el texto en líneas y
cuántas imágenes trae) y fuentes/cafe/indice.json. Una nota ya bajada no se vuelve a pedir. Se guarda el texto y no el
HTML: el del editor de Naver pesa unas diez veces más.

Una consulta por vez, con PAUSA segundos entre una y otra, para no cargar los servidores de Naver. Solo biblioteca
estándar."""
import json, os, re, sys, time, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from historico import lineas

CAFE = 27907035
TABLEROS = (4, 141)
LISTA = ('https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json?search.clubid=%d&search.menuid={}'
         '&search.page={}&search.perPage=50&search.queryType=lastArticle' % CAFE)
ARTICULO = 'https://apis.naver.com/cafe-web/cafe-articleapi/v2.1/cafes/%d/articles/{}?useCafeId=true&requestFrom=A' % CAFE
VER = 'https://cafe.naver.com/futurefight/{}'
UA = {'User-Agent': 'Mozilla/5.0 (mff-comparador; uso personal)', 'Referer': 'https://cafe.naver.com/futurefight'}
PAUSA = 6
ESPERA = 60
INTENTOS = 4
VENTANA = 3
OTRO_TIPO = 12
# Qué es una nota en el café: el detalle de una actualización o de un parche, o el aviso de que terminó un parche (que
# trae el detalle); los avisos de mantenimiento y de las tiendas no. Una de parche es la que dice «패치» y no «업데이트»;
# en inglés, la que dice «patch».
NOTA = re.compile(r'업데이트 ?상세|패치 (내용 |완료 )?안내|불편사항 수정.*업데이트')
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fuentes', 'cafe')
FORO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'fuentes', 'foro', 'indice.json')


def pedir(url):
    """La respuesta de Naver, leída. Un corte de red (Naver corta a veces la conexión: «Connection reset by peer»): se
    espera ESPERA segundos y se pide otra vez, hasta INTENTOS veces; si sigue fallando, corta."""
    req = urllib.request.Request(url, headers=UA)
    for intento in range(1, INTENTOS + 1):
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=30).read())
            break
        except OSError as e:
            if intento == INTENTOS:
                raise
            print(f'  AVISO {url}: {e}; otra vez en {ESPERA} s', flush=True)
            time.sleep(ESPERA)
    time.sleep(PAUSA)
    return d


def es_parche_ko(titulo):
    return '패치' in titulo and '업데이트' not in titulo


def es_parche_en(titulo):
    return re.search(r'patch', titulo, re.I) is not None


def listar(todo):
    """Las notas de los dos tableros: {id: {id, titulo, fecha}}."""
    vistas = {}
    for menu in TABLEROS:
        pagina = 1
        while True:
            r = pedir(LISTA.format(menu, pagina))['message']['result']
            for a in r['articleList']:
                if NOTA.search(a['subject']):
                    vistas[a['articleId']] = {'id': a['articleId'], 'titulo': a['subject'], 'fecha': a['writeDateTimestamp']}
            if not todo or not r['hasNext']:
                break
            pagina += 1
    return vistas


def par(nota_en, vistas):
    """La nota coreana del mismo tipo (actualización o parche) de fecha más cercana, a VENTANA días o menos; una de otro
    tipo, solo a OTRO_TIPO horas o menos y contando esas horas de más. None si no hay. Los títulos no siempre coinciden:
    las «Patch Notes» de 2015 en inglés son actualizaciones en coreano; y una de otro tipo más lejos suele ser un parche
    de después, cuando la actualización coreana ya no está en el tablero."""
    tipo = es_parche_en(nota_en['titulo'])
    dt = lambda a: abs(a['fecha'] - nota_en['fecha'])
    hora = 3600 * 1000
    cand = [(dt(a) + (0 if es_parche_ko(a['titulo']) == tipo else OTRO_TIPO * hora), a) for a in vistas.values()
            if (dt(a) <= VENTANA * 24 * hora if es_parche_ko(a['titulo']) == tipo else dt(a) <= OTRO_TIPO * hora)]
    return min(cand, key=lambda c: c[0])[1] if cand else None


def guardar(indice, ruta):
    json.dump(sorted(indice.values(), key=lambda n: n['fecha']), open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def main(todo):
    os.makedirs(DIR, exist_ok=True)
    ruta_indice = os.path.join(DIR, 'indice.json')
    indice = {n['id']: n for n in json.load(open(ruta_indice, encoding='utf-8'))} if os.path.exists(ruta_indice) else {}
    vistas = listar(todo)
    # Con --todo se rehacen los pares de todas las notas en inglés (con la lista entera de los dos tableros); si no, se
    # buscan los de las que todavía no tienen.
    con_par = set() if todo else {e for n in indice.values() for e in n['en']}
    pares, sin = {}, 0
    for n in json.load(open(FORO, encoding='utf-8')):
        if n['id'] in con_par:
            continue
        a = par(n, vistas)
        if a:
            pares.setdefault(a['id'], (a, []))[1].append(n['id'])
        else:
            sin += 1
    if todo:
        for kid in [k for k in indice if k not in pares]:   # ya no es el par de ninguna nota en inglés
            os.remove(os.path.join(DIR, f'{kid}.json'))
            print(f"  fuera {kid} {indice.pop(kid)['titulo']}", flush=True)
        guardar(indice, ruta_indice)
    print(f'café: {len(vistas)} notas vistas; {len(pares)} pares; {sin} notas en inglés sin par en lo visto', flush=True)
    for kid, (a, ens) in pares.items():
        if kid in indice:
            ens = ens if todo else indice[kid]['en'] + ens
            if ens != indice[kid]['en']:   # cambió a qué notas en inglés acompaña
                ruta = os.path.join(DIR, f'{kid}.json')
                nota = json.load(open(ruta, encoding='utf-8'))
                nota['en'] = indice[kid]['en'] = ens
                json.dump(nota, open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            continue
        x = pedir(ARTICULO.format(kid))['result']['article']
        nota = {'id': x['id'], 'titulo': x['subject'], 'fecha': x['writeDate'], 'url': VER.format(x['id']), 'en': ens,
                'lineas': lineas(x['contentHtml']), 'imagenes': len(re.findall(r'<img\b|\[\[\[CONTENT-ELEMENT-', x['contentHtml']))}
        json.dump(nota, open(os.path.join(DIR, f"{x['id']}.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        indice[x['id']] = {k: nota[k] for k in ('id', 'titulo', 'fecha', 'url', 'en')}
        print(f"  {x['id']} {x['subject']}", flush=True)
        guardar(indice, ruta_indice)   # después de cada nota: si algo corta, no se vuelve a pedir lo ya bajado
    guardar(indice, ruta_indice)
    print(f'café: {len(indice)} notas en fuentes/cafe/', flush=True)


if __name__ == '__main__':
    main('--todo' in sys.argv[1:])
