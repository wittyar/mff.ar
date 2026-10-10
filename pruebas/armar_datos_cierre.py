"""Datos de prueba con las correcciones de thanosvibs que el próximo build hace con el juego (carril de cierre, 5 de
octubre de 2026; scripts/fuentes.py). Solo para las pruebas: nunca van al repo.

Sin work/ el build no corre. Esto copia la carpeta de datos ORIGEN (formato 7, con images/, la que deja
armar_datos_lideres.py) a DESTINO y le pone lo que el build va a cambiar, con las mismas funciones del repo:
- MFF_CTPS: el nombre de cada C.T.P. con fuentes.nombre_ctp (Judgement → Judgment, con tv y f).
- MFF_ARTEFACTOS: cada línea con fuentes.linea_artefacto (Planet Eater), con tv y f, y su traducción en MFF_TXT
  (fuentes.TXP, la tabla de traducciones/artefactos.json).
- docs/AUDITORIA.md: la sección 5 con auditar.correcciones_seccion (las restricciones corregidas salen de los rc de
  MFF_SOPORTES, como en auditar.Auditoria.fuentes).
datos.json lleva las huellas nuevas de data.js y docs/AUDITORIA.md.

  python3 armar_datos_cierre.py ORIGEN DESTINO"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import collections, hashlib, json, os, re, shutil, sys

RAIZ = RAIZ
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
import auditar  # noqa: E402
import fuentes  # noqa: E402


def main(origen, destino):
    if os.path.exists(destino):
        raise SystemExit(f'{destino} ya existe')
    shutil.copytree(origen, destino, symlinks=True)
    ruta = os.path.join(destino, 'data.js')
    s = open(ruta, encoding='utf-8').read()
    dec = json.JSONDecoder()

    def glob(nombre):
        m = re.search(r'^window\.' + nombre + r' = ', s, re.M)
        obj, fin = dec.raw_decode(s, m.end())
        return obj, m.start(), fin

    def poner(nombre, valor):
        nonlocal s
        _, ini, fin = glob(nombre)
        s = s[:ini] + f'window.{nombre} = ' + json.dumps(valor, ensure_ascii=False) + s[fin:]

    L = collections.defaultdict(list)
    ctps = glob('MFF_CTPS')[0]
    if any('tv' in c for c in ctps):
        raise SystemExit(f'{origen}/data.js ya trae los nombres corregidos')
    for c in ctps:
        nombre, corregido = fuentes.nombre_ctp(c['name'])
        if corregido:
            c['name'] = nombre
            c.update(corregido)
            L['ctp_nombre'].append((c['id'], c['tv'], c['name'], c['f']))
    poner('MFF_CTPS', ctps)
    arts = glob('MFF_ARTEFACTOS')[0]
    for a in arts:
        for ln in a['lineas']:
            texto, corregida = fuentes.linea_artefacto(a['name'], ln['t'])
            if corregida:
                ln['t'] = fuentes.TXP(texto)
                ln.update(corregida)
                L['art_linea'].append((a['p'], a['name'], ln['tv'], ln['t'], ln['f']))
    poner('MFF_ARTEFACTOS', arts)
    if fuentes.TX.faltan:
        raise SystemExit(f'sin traducción: {sorted(fuentes.TX.faltan)}')
    txt = glob('MFF_TXT')[0]
    txt.update(fuentes.TX.usados)
    poner('MFF_TXT', dict(sorted(txt.items())))
    for p, e in glob('MFF_SOPORTES')[0].items():
        for tipo, x in e.items():
            if isinstance(x, dict) and x.get('rc'):
                L['soporte'].append((p, tipo, x['rc'], x['r']))
    open(ruta, 'w', encoding='utf-8', newline='\n').write(s)

    ra = os.path.join(destino, 'docs', 'AUDITORIA.md')
    a = open(ra, encoding='utf-8').read()
    i, j = a.index('## 5. '), a.index('## 6. ')
    guia = json.load(open(os.path.join(RAIZ, 'scripts', 'contenido', 'guia.json'), encoding='utf-8'))
    a = a[:i] + '\n'.join(auditar.correcciones_seccion(L, guia['fuentes'])) + '\n' + a[j:]
    open(ra, 'w', encoding='utf-8', newline='\n').write(a)

    m = json.load(open(os.path.join(destino, 'datos.json'), encoding='utf-8'))
    for r in ('data.js', 'docs/AUDITORIA.md'):
        b = open(os.path.join(destino, r), 'rb').read()
        m['archivos'][r] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    with open(os.path.join(destino, 'datos.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f"{destino}: C.T.P. corregidos {[x[:3] for x in L['ctp_nombre']]}; líneas de artefacto {[x[:3] for x in L['art_linea']]}; "
          f"restricciones {len(L['soporte'])}")


if __name__ == '__main__':
    main(*sys.argv[1:3])
