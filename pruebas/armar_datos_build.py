"""Datos de prueba con lo que el próximo build va a cambiar en data.js, solo para las pruebas (nunca van al repo).

Sin work/ el build no corre. Esto copia la carpeta de datos ORIGEN (con images/) a DESTINO y le pone a su data.js lo
que va a escribir el build del repo, sacado del mismo build.py (sus líneas, evaluadas acá) y del contenido curado:
- MFF_VERSION.formato y el formato de datos.json: FORMATO de scripts/build.py (7 desde la segunda parte del carril
  de consistencia: el catálogo trae a quién le sirve cada stat de liderazgo, soporte y bono; 8 desde la segunda parte
  del carril filtro2: cada uno dice además si se acumula y su tope).
- MFF_SEED.SKILL_TAGS: la línea ABIL_VALUES de build.py sobre MFF_SEED_CHARACTERS (que son los `chars` del build).
- MFF_CATALOGO: la línea CATALOGO de build.py sobre scripts/contenido/catalogo.json.
- MFF_VALOR: la línea VALOR de build.py sobre scripts/contenido/valor_equipos.json, si build.py la tiene.
- MFF_ANALISIS: scripts/modelo.py (analisis) con ese catálogo, sobre MFF_SKILLS, MFF_TABLAS y MFF_PERFIL (con los
  datos de hoy y el catálogo de hoy da exactamente el MFF_ANALISIS publicado).
- Los roles de MFF_SEED_CHARACTERS: scripts/modelo.py (roles) sobre ese análisis, como _core.py (carril Q: el «Give
  Power» de Stryfe — The Tyrant of Spring le suma Soporte).
datos.json lleva la huella del data.js nuevo. Nada más cambia: el resto del contenido curado (glosario, guía, modos) lo
copia armar_datos_contenido.py.

  python3 armar_datos_build.py ORIGEN DESTINO
  MFF_DATOS=DESTINO python3 verif_....py"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, json, os, re, shutil, sys

RAIZ = RAIZ
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
import modelo  # noqa: E402


def linea_de(build, nombre):
    """La línea de build.py que define `nombre` (una sola, de una línea)."""
    ls = [l for l in build.splitlines() if l.startswith(nombre + ' = ')]
    if len(ls) != 1:
        raise SystemExit(f'build.py tiene {len(ls)} líneas «{nombre} = »: este script espera una')
    return ls[0].split('=', 1)[1]


def main(origen, destino):
    if os.path.exists(destino):
        raise SystemExit(f'{destino} ya existe')
    build = open(os.path.join(RAIZ, 'scripts', 'build.py'), encoding='utf-8').read()
    contenido = os.path.join(RAIZ, 'scripts', 'contenido')
    shutil.copytree(origen, destino, symlinks=True)
    ruta = os.path.join(destino, 'data.js')
    s = open(ruta, encoding='utf-8').read()
    dec = json.JSONDecoder()

    def glob(nombre):
        m = re.search(r'^window\.' + nombre + r' = ', s, re.M)
        if not m:
            return None, None, None
        obj, fin = dec.raw_decode(s, m.end())
        return obj, m.start(), fin

    def poner(nombre, valor, **kw):
        nonlocal s
        _, ini, fin = glob(nombre)
        texto = f'window.{nombre} = ' + json.dumps(valor, ensure_ascii=False, **kw)
        if ini is None:
            # Un global nuevo (MFF_VALOR): va después de MFF_ROLES_LISTAS, donde lo escribe el build.
            _, _, fin_roles = glob('MFF_ROLES_LISTAS')
            ini = fin = s.index('\n', fin_roles) + 1
            texto += ';\n'
        s = s[:ini] + texto + s[fin:]

    cambios = []
    formato = int(linea_de(build, 'FORMATO'))
    version = glob('MFF_VERSION')[0]
    cambios.append(f"formato {version['formato']} → {formato}")
    poner('MFF_VERSION', {**version, 'formato': formato})

    chars = glob('MFF_SEED_CHARACTERS')[0]
    seed = glob('MFF_SEED')[0]
    antes = seed['SKILL_TAGS']
    seed['SKILL_TAGS'] = eval(linea_de(build, 'ABIL_VALUES'), {'chars': chars, 'sorted': sorted})
    poner('MFF_SEED', seed, indent=1)
    cambios.append(f"SKILL_TAGS {len(antes)} → {len(seed['SKILL_TAGS'])}")

    _cat = json.load(open(os.path.join(contenido, 'catalogo.json'), encoding='utf-8'))
    catalogo = eval(linea_de(build, 'CATALOGO'), {'_CAT': _cat})
    poner('MFF_CATALOGO', catalogo)
    cambios.append('MFF_CATALOGO (' + ', '.join(catalogo) + ')')

    if any(l.startswith('VALOR = ') for l in build.splitlines()):
        _valor = json.load(open(os.path.join(contenido, 'valor_equipos.json'), encoding='utf-8'))
        valor = eval(linea_de(build, 'VALOR'), {'_VALOR': _valor})
        poner('MFF_VALOR', valor, separators=(',', ':'))
        cambios.append('MFF_VALOR (' + ', '.join(valor) + ')')

    skills, tablas, perfiles = glob('MFF_SKILLS')[0], glob('MFF_TABLAS')[0], glob('MFF_PERFIL')[0]
    an_viejo = glob('MFF_ANALISIS')[0]
    an = {p: modelo.analisis(sks, tablas, _cat, perfiles[p]) for p, sks in skills.items()}
    poner('MFF_ANALISIS', an, separators=(',', ':'))
    cambios.append(f'MFF_ANALISIS ({sum(an[p] != an_viejo.get(p) for p in an)} de {len(an)} retratos cambian)')

    # Los roles, como _core.py (roles_de): los del retrato base en el personaje y, si difieren, los de cada uniforme.
    vacio = modelo.roles({'fx': []}, [], _cat)
    ro = {p: modelo.roles(an[p], sks, _cat) for p, sks in skills.items()}
    cambian = []
    for ch in chars:
        base = ro.get(ch['p'], vacio)
        if ch['r'] != base:
            cambian.append(ch['p'])
            ch['r'] = base
        for u in ch['uniforms']:
            propio = ro.get(u['p'], vacio)
            nuevo = propio if propio != base else None
            if u.get('r') != nuevo:
                cambian.append(u['p'])
            if nuevo is None:
                u.pop('r', None)
            else:
                u['r'] = nuevo
    poner('MFF_SEED_CHARACTERS', chars)
    cambios.append(f'roles ({len(cambian)} retratos cambian: {cambian})')

    open(ruta, 'w', encoding='utf-8', newline='\n').write(s)
    m = json.load(open(os.path.join(destino, 'datos.json'), encoding='utf-8'))
    b = open(ruta, 'rb').read()
    m['formato'] = formato
    m['archivos']['data.js'] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    with open(os.path.join(destino, 'datos.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print(f'{destino}: ' + '; '.join(cambios))


if __name__ == '__main__':
    main(*sys.argv[1:3])
