"""Datos de prueba con los liderazgos que el próximo build deriva de la Leader Skill de la API (carril Q, 5 de octubre
de 2026; scripts/liderazgos.py). Solo para las pruebas: nunca van al repo.

Sin work/ el build no corre. Esto copia la carpeta de datos ORIGEN (datos de formato 7, con images/) a DESTINO y le
pone lo que el build va a cambiar:
- MFF_SOPORTES: Leads & Supports tal como lo publica (sin los liderazgos que copiaba la regla anterior, los
  «Completados» de la sección 12 de ORIGEN/docs/AUDITORIA.md) más lo que deriva scripts/liderazgos.py del repo, con
  "src": "api", unido como lo une scripts/fuentes.py, con las correspondencias a mano de
  scripts/contenido/liderazgos_api.json (validadas con el catálogo del repo).
- MFF_TXT: la traducción de las activaciones que van con el texto de la API (de MFF_TABLAS), como en fuentes.py.
- docs/AUDITORIA.md: la línea del resumen y la sección 12, con las funciones de scripts/auditar.py del repo. El nombre
  de cada variante sale de data.js (el build usa work/characters.json: un uniforme que cambia el personaje lleva acá
  su nombre entre paréntesis).
- docs/COMPLETITUD.md: scripts/completitud.py del repo, sobre el data.js nuevo.
datos.json lleva las huellas nuevas de data.js y docs/AUDITORIA.md. Deja DESTINO/liderazgos.json con lo que devolvió
derivar() y lo copiado antes, para medir.

  python3 armar_datos_lideres.py ORIGEN DESTINO"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import hashlib, json, os, re, shutil, sys

RAIZ = RAIZ
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
import auditar  # noqa: E402
import completitud  # noqa: E402
import liderazgos  # noqa: E402


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

    sop, ini, fin = glob('MFF_SOPORTES')
    if any(isinstance(x, dict) and 'src' in x for e in sop.values() for x in e.values()):
        raise SystemExit(f'{origen}/data.js ya trae liderazgos con src')
    chars = glob('MFF_SEED_CHARACTERS')[0]
    nombres = {ch['p']: ch['name'] for ch in chars} | {u['p']: ch['name'] for ch in chars for u in ch['uniforms']}
    base = {ch['p']: ch['p'] for ch in chars} | {u['p']: ch['p'] for ch in chars for u in ch['uniforms']}
    # Lo que copiaba la regla anterior (fuentes.completar_liderazgos): entradas nuevas, solo con el liderazgo de la base.
    aud = open(os.path.join(origen, 'docs', 'AUDITORIA.md'), encoding='utf-8').read()
    copiados = re.findall(r'\(`([^`]+)`\) ← ', aud.split('### Completados')[1].split('\n### ')[0])
    for p in copiados:
        lid = {k: x for k, x in sop[base[p]].items() if k in liderazgos.LIDERAZGOS}
        if sop[p] != lid:
            raise SystemExit(f'{p}: no es una copia del liderazgo de su base')
    ls = {p: e for p, e in sop.items() if p not in copiados}
    # Las correspondencias a mano del contenido curado, validadas como en fuentes.main().
    a_mano = json.load(open(os.path.join(RAIZ, 'scripts', 'contenido', 'liderazgos_api.json'), encoding='utf-8'))
    T = glob('MFF_TABLAS')[0]
    mal = liderazgos.validar(a_mano, T, json.load(open(os.path.join(RAIZ, 'scripts', 'contenido', 'catalogo.json'),
                                                      encoding='utf-8')))
    if mal:
        raise SystemExit('scripts/contenido/liderazgos_api.json tiene errores:\n  ' + '\n  '.join(mal))
    L = liderazgos.derivar(ls, glob('MFF_SKILLS')[0], T, nombres, a_mano)
    for a in L['a_mano']['avisos']:
        print(f'AVISO: scripts/contenido/liderazgos_api.json: {a}')
    nuevo = dict(ls)
    for p, slots in L['derivados'].items():
        nuevo[p] = {**nuevo.get(p, {}), **slots}
    s = s[:ini] + 'window.MFF_SOPORTES = ' + json.dumps(nuevo, ensure_ascii=False) + s[fin:]
    # MFF_TXT: la traducción de las activaciones que van con el texto de la API, como en fuentes.main() (TX.usados).
    txt, ini, fin = glob('MFF_TXT')
    sin = [en for en, es in L['textos'].items() if es is None]
    if sin:
        print('AVISO: activaciones sin traducción en la API:', sin)
    txt.update({en: es for en, es in L['textos'].items() if es is not None})
    s = s[:ini] + 'window.MFF_TXT = ' + json.dumps(dict(sorted(txt.items())), ensure_ascii=False) + s[fin:]
    open(ruta, 'w', encoding='utf-8', newline='\n').write(s)

    # docs/AUDITORIA.md: el resumen y la sección 12, como los escribe auditar.py.
    filas = [{'portrait': ch['p'], 'character': ch['name'], 'uniformed': 'False', 'uniform': ''} for ch in chars] + [
        {'portrait': u['p'], 'character': ch['name'], 'uniformed': 'True', 'uniform': u['name']} for ch in chars for u in ch['uniforms']]
    ra = os.path.join(destino, 'docs', 'AUDITORIA.md')
    a = open(ra, encoding='utf-8').read()
    viejo = re.search(r'^Liderazgos: .*\n', a, re.M)
    # La misma línea que escribe auditar.informe (que necesita work/ entero).
    linea = (f"Liderazgos: el build deriva de la Leader Skill de la API el de {len(L['derivados'])} variantes que Leads & "
             f"Supports no publica; {len(L['sin_derivar'])} slots no se pudieron derivar (sección 12).\n")
    if 'Liderazgos: el build deriva de la Leader Skill de la API el de ' not in open(
            os.path.join(RAIZ, 'scripts', 'auditar.py'), encoding='utf-8').read():
        raise SystemExit('auditar.py ya no escribe así la línea del resumen: actualizar este script')
    a = a[:viejo.start()] + linea + a[viejo.end():]
    i = a.index('## 12. ')
    fuentes = json.load(open(os.path.join(RAIZ, 'scripts', 'contenido', 'guia.json'), encoding='utf-8'))['fuentes']
    a = a[:i] + '\n'.join(auditar.liderazgos_seccion(L, filas, fuentes))
    open(ra, 'w', encoding='utf-8', newline='\n').write(a)

    # docs/COMPLETITUD.md, sobre el data.js nuevo.
    completitud._RAIZ = destino
    sys.argv = ['completitud.py']
    completitud.main()

    m = json.load(open(os.path.join(destino, 'datos.json'), encoding='utf-8'))
    for r in ('data.js', 'docs/AUDITORIA.md'):
        b = open(os.path.join(destino, r), 'rb').read()
        m['archivos'][r] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    with open(os.path.join(destino, 'datos.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write('\n')
    json.dump({'copiados': copiados, **L}, open(os.path.join(destino, 'liderazgos.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f"{destino}: {len(copiados)} liderazgos copiados de la base, fuera; derivados {len(L['derivados'])} variantes "
          f"({sum(len(x) for x in L['derivados'].values())} slots); sin derivar {len(L['sin_derivar'])} slots")


if __name__ == '__main__':
    main(*sys.argv[1:3])
