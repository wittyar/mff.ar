"""Datos de prueba de formato 6, solo para las pruebas (nunca van al repo).

La 1.0.17 pide datos de formato 6 (los marcadores también se completan con Leads & Supports, gs 'l'),
pero el data.js del repo sigue en formato 5 hasta que corra el workflow «Actualizar datos MFF». Esto
copia data.js, datos.json y docs/ del repo a CARPETA, les pone el formato de version.json y completa
con Leads & Supports cuatro marcadores que en el data.js del repo están sin resolver, con el valor que
Leads & Supports publica para ese slot y ese porcentaje (MFF_SOPORTES):
  angela3 (Angela — Asgard's Assassin), pasiva de uniforme: Supervillano («Basic Damage Dealt to Villains» 40)
  dormammu1 (Dormammu — Damnation), Leader Skill: Superhéroe («Basic Damage Dealt to Heroes» 60)
  ebonymaw3 (Ebony Maw — General's Hand), pasiva de uniforme, los dos: Universal («Basic Damage Dealt
    to Universals» 40 y «Basic Damage Received from Universals» -35); su T2 sigue sin especificar
Lo que ya venía completado a mano ('m') o por la wiki ('w') queda igual. datos.json lleva el formato
nuevo y la huella del data.js nuevo. images/ lleva un PNG de 1x1 por cada imagen que lista datos.json:
así la app no baja nada de thanosvibs y la consola no da 404 (el clon no trae images/).

  python3 armar_datos_prueba.py CARPETA
  MFF_DATOS=CARPETA python3 verif_....py      (harness.py toma los datos de ahí)

Para si el data.js del repo ya es del formato de version.json (ya corrió el workflow): entonces las
pruebas van con los datos del repo, sin MFF_DATOS."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, json, os, shutil, struct, sys, zlib

RAIZ = RAIZ
# (retrato, slot de la skill, slot de Leads & Supports, [(stat de Leads & Supports, valor)] en el orden
# de los marcadores de la skill)
L = [('angela3', 'Uniform Passive', 'uniform', [('Basic Damage Dealt to Villains', 'Supervillano')]),
     ('dormammu1', 'Leader Skill', 'leader', [('Basic Damage Dealt to Heroes', 'Superhéroe')]),
     ('ebonymaw3', 'Uniform Passive', 'uniform', [('Basic Damage Dealt to Universals', 'Universal'),
                                                  ('Basic Damage Received from Universals', 'Universal')])]


def png_1x1():
    def bloque(tipo, datos):
        return struct.pack('>I', len(datos)) + tipo + datos + struct.pack('>I', zlib.crc32(tipo + datos))
    return (b'\x89PNG\r\n\x1a\n' + bloque(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 6, 0, 0, 0))
            + bloque(b'IDAT', zlib.compress(b'\x00\x00\x00\x00\x00')) + bloque(b'IEND', b''))


def main(destino):
    formato = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))['formato_datos']
    lineas = open(os.path.join(RAIZ, 'data.js'), encoding='utf-8').read().split('\n')
    glob = {}
    for i, l in enumerate(lineas):
        if l.startswith('window.MFF_') and ' = ' in l and l.endswith(';'):
            nombre, cuerpo = l[len('window.'):].split(' = ', 1)
            if cuerpo.startswith(('{', '[')) and cuerpo.endswith(('};', '];')):
                glob[nombre] = i
    version = json.loads(lineas[glob['MFF_VERSION']][len('window.MFF_VERSION = '):-1])
    if version['formato'] == formato:
        raise SystemExit(f'el data.js del repo ya es de formato {formato}: las pruebas van con los datos del repo, sin MFF_DATOS')
    version['formato'] = formato
    lineas[glob['MFF_VERSION']] = 'window.MFF_VERSION = ' + json.dumps(version, ensure_ascii=False) + ';'
    skills = json.loads(lineas[glob['MFF_SKILLS']][len('window.MFF_SKILLS = '):-1])
    tablas = json.loads(lineas[glob['MFF_TABLAS']][len('window.MFF_TABLAS = '):-1])
    soportes = json.loads(lineas[glob['MFF_SOPORTES']][len('window.MFF_SOPORTES = '):-1])
    for p, slot, slot_ls, pares in L:
        efs = [f for sk in skills[p] if sk['sl'] == slot for st in sk.get('st') or [] for f in st['fx']
               if '$HERO' in tablas['desc'][f['p']]['en']]
        if len(efs) != len(pares) or any(f.get('g') for f in efs):
            raise SystemExit(f'{p} {slot}: se esperaban {len(pares)} marcadores sin completar y hay '
                             f'{[(f.get("g"), f.get("gs")) for f in efs]}')
        for f, (stat, valor) in zip(efs, pares):
            ls = [x for x in soportes[p][slot_ls]['fx'] if x['s'] == stat]
            if len(ls) != 1 or abs(ls[0]['v']) != f['v'][-1]:
                raise SystemExit(f'{p}: Leads & Supports no publica «{stat}» con {f["v"][-1]} ({soportes[p][slot_ls]["fx"]})')
            f['g'], f['gs'] = valor, 'l'
    lineas[glob['MFF_SKILLS']] = 'window.MFF_SKILLS = ' + json.dumps(skills, ensure_ascii=False) + ';'
    os.makedirs(destino, exist_ok=True)
    datajs = '\n'.join(lineas).encode('utf-8')
    open(os.path.join(destino, 'data.js'), 'wb').write(datajs)
    if os.path.isdir(os.path.join(destino, 'docs')):
        shutil.rmtree(os.path.join(destino, 'docs'))
    shutil.copytree(os.path.join(RAIZ, 'docs'), os.path.join(destino, 'docs'))
    m = json.load(open(os.path.join(RAIZ, 'datos.json'), encoding='utf-8'))
    m['formato'] = formato
    m['archivos']['data.js'] = {'sha256': hashlib.sha256(datajs).hexdigest(), 'bytes': len(datajs)}
    for rel in m['archivos']:
        if rel != 'data.js':
            b = open(os.path.join(destino, rel), 'rb').read()
            assert m['archivos'][rel] == {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}, rel
    json.dump(m, open(os.path.join(destino, 'datos.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    png = png_1x1()
    imagenes = m['imagenes']
    for ruta, _ in imagenes:
        os.makedirs(os.path.dirname(os.path.join(destino, ruta)), exist_ok=True)
        open(os.path.join(destino, ruta), 'wb').write(png)
    print(f'{destino}: data.js de formato {formato} con {sum(len(x[3]) for x in L)} marcadores de Leads & Supports '
          f'({", ".join(x[0] for x in L)}), docs/ y {len(imagenes)} imágenes de 1x1')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(os.path.abspath(sys.argv[1]))
