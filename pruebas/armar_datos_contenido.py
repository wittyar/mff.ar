"""Datos de prueba con el contenido curado del repo, solo para las pruebas (nunca van al repo).

El contenido curado (scripts/contenido/) llega a data.js recién cuando corre el build con work/ (el
workflow «Actualizar datos MFF»). Para probar la app con el contenido nuevo antes de eso, esto copia la
carpeta de datos ORIGEN (la del repo o una armada con armar_datos_prueba.py, con images/) a DESTINO y
reemplaza en su data.js los globales que el build copia tal cual del contenido curado:
  MFF_CATALOGO  (catalogo.json: certeza, sirve, contra, grupos, efectos, skills, soporte)
  MFF_GLOSARIO  (glosario.json)
  MFF_GUIA      (guia.json, con la version_fuente que ya tenía)
  MFF_MODOS     (modos.json → modos)
Corta si el catálogo nuevo cambia los ids o el orden de los efectos o de las etiquetas (el análisis de
cada variante los referencia por posición: eso pide el build entero). datos.json lleva la huella del
data.js nuevo. No toca lo que el build deriva del contenido (la guía por personaje, docs/AUDITORIA.md,
docs/CATALOGO.md): eso sigue como en ORIGEN.

  python3 armar_datos_contenido.py ORIGEN DESTINO
  MFF_DATOS=DESTINO python3 verif_....py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, json, os, re, shutil, sys

RAIZ = RAIZ
C = os.path.join(RAIZ, 'scripts', 'contenido')


def cargar(n):
    return json.load(open(os.path.join(C, n), encoding='utf-8'))


def main(origen, destino):
    if os.path.exists(destino):
        raise SystemExit(f'{destino} ya existe')
    shutil.copytree(origen, destino, symlinks=True)
    ruta = os.path.join(destino, 'data.js')
    s = open(ruta, encoding='utf-8').read()
    dec = json.JSONDecoder()

    def viejo(nombre):
        m = re.search(r'^window\.' + nombre + r' = ', s, re.M)
        obj, fin = dec.raw_decode(s, m.end())
        return obj, m.start(), fin

    cat = cargar('catalogo.json')
    nuevos = {
        'MFF_CATALOGO': {k: cat[k] for k in ('certeza', 'sirve', 'contra', 'grupos', 'efectos', 'skills', 'soporte')},
        'MFF_GLOSARIO': cargar('glosario.json'),
        'MFF_GUIA': {**cargar('guia.json'), 'version_fuente': viejo('MFF_GUIA')[0]['version_fuente']},
        'MFF_MODOS': cargar('modos.json')['modos'],
    }
    cat_viejo = viejo('MFF_CATALOGO')[0]
    # Con MFF_ANALISIS_DESPUES=1 sigue igual: el paso siguiente (armar_datos_build.py) recalcula el análisis
    # con el catálogo nuevo, que es lo que referencia los efectos por posición.
    if ([e['id'] for e in cat_viejo['efectos']] != [e['id'] for e in nuevos['MFF_CATALOGO']['efectos']]
            or list(cat_viejo['skills']) != list(nuevos['MFF_CATALOGO']['skills'])) \
            and os.environ.get('MFF_ANALISIS_DESPUES') != '1':
        raise SystemExit('el catálogo cambió ids u orden de efectos o etiquetas: hace falta el build entero '
                         '(o MFF_ANALISIS_DESPUES=1 si después va armar_datos_build.py)')
    for nombre, valor in nuevos.items():
        _, ini, fin = viejo(nombre)
        s = s[:ini] + f'window.{nombre} = ' + json.dumps(valor, ensure_ascii=False) + s[fin:]
    open(ruta, 'w', encoding='utf-8', newline='\n').write(s)
    m = json.load(open(os.path.join(destino, 'datos.json'), encoding='utf-8'))
    b = open(ruta, 'rb').read()
    m['archivos']['data.js'] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    with open(os.path.join(destino, 'datos.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'{destino}: data.js con {", ".join(nuevos)} del contenido curado del repo')


if __name__ == '__main__':
    main(*sys.argv[1:3])
