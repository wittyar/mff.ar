"""Aceptación semanal de la guía de armado (scripts/guia_armado.py): con la planilla real y
con copias alteradas a mano. Lo compatible pasa a ser la copia en uso; lo incompatible se
rechaza con motivos y la copia en uso queda intacta, byte por byte."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import csv, hashlib, io, json, os, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f'{RAIZ}/scripts')
from harness import Chequeo
import guia_armado as G

ok = Chequeo()
RAIZ = RAIZ
TV = json.load(open(f'{RAIZ}/work/characters.json'))
CTPS = json.load(open(f'{RAIZ}/work/ctps.json'))
REAL = {k: open(os.path.join(G.CARPETA, G.ARCHIVOS[k]), 'rb').read() for k in G.ARCHIVOS}
ESTADO_REAL = open(os.path.join(G.CARPETA, 'estado.json'), encoding='utf-8').read()

# Todo en una carpeta temporal: la copia en uso de prueba arranca igual a la del repo.
tmp = tempfile.mkdtemp(prefix='guia-')
G.CARPETA = tmp
def reset():
    for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
    for k, b in REAL.items(): open(os.path.join(tmp, G.ARCHIVOS[k]), 'wb').write(b)
    open(os.path.join(tmp, 'estado.json'), 'w', encoding='utf-8').write(ESTADO_REAL)
def copia(): return {k: hashlib.sha256(open(os.path.join(tmp, G.ARCHIVOS[k]), 'rb').read()).hexdigest() for k in G.ARCHIVOS}
def est(): return json.load(open(os.path.join(tmp, 'estado.json'), encoding='utf-8'))
def tabla(b): return list(csv.reader(io.StringIO(b.decode('utf-8'))))
def bytes_de(filas):
    s = io.StringIO(); csv.writer(s, lineterminator='\r\n').writerows(filas); return s.getvalue().encode('utf-8')
def mutar(f_armado=None, f_tier=None):
    out = dict(REAL)
    if f_armado: t = tabla(REAL['armado']); f_armado(t); out['armado'] = bytes_de(t)
    if f_tier: t = tabla(REAL['tierlist']); f_tier(t); out['tierlist'] = bytes_de(t)
    return out
ENC = next(i for i, f in enumerate(tabla(REAL['armado'])) if f and f[0] == 'PK')
def col(t, nombre): return t[ENC].index(nombre)

def rechazo(nombre, crudo, *pedazos, dia='2026-10-12'):
    reset(); antes = copia()
    linea = G.aceptar(crudo, TV, CTPS, dia)
    e = est()
    motivos = ' | '.join((e.get('rechazo') or {}).get('motivos', []))
    ok(f'rechaza: {nombre}', e['rechazo'] is not None and all(p in motivos for p in pedazos)
       and copia() == antes and e['version'] == 'V12.2.0' and e['tomada'] == '2026-10-01' and e['comprobada'] == dia
       and linea.startswith('AVISO'), motivos[:300])

# 1. la misma planilla: sin cambios
reset(); antes = copia()
linea = G.aceptar(REAL, TV, CTPS, '2026-10-05'); e = est()
ok('1 misma planilla: sin cambios, comprobada hoy, sin rechazo', 'sin cambios' in linea and copia() == antes
   and e['comprobada'] == '2026-10-05' and e['tomada'] == '2026-10-01' and e['rechazo'] is None, linea)

# 2. cambió una nota (compatible): pasa a ser la copia en uso
def nota(t): t[ENC + 1][col(t, 'Notes')] = 'nota nueva de prueba'
crudo = mutar(nota)
reset(); linea = G.aceptar(crudo, TV, CTPS, '2026-10-05'); e = est()
ok('2 contenido nuevo compatible: se toma', copia()['armado'] == hashlib.sha256(crudo['armado']).hexdigest()
   and e['tomada'] == '2026-10-05' and e['rechazo'] is None, linea[:120])

# 3-10. incompatibles
def renombrar(t): t[ENC][col(t, 'Best CTP')] = 'Top CTP'
rechazo('columna renombrada', mutar(renombrar), 'faltan columnas', '«Best CTP»')
def sin_enc(t):
    for _ in range(20): t.insert(0, [''] * len(t[0]))
rechazo('encabezados corridos fuera de las primeras 15 filas', mutar(sin_enc), 'fila de encabezados')
def sin_version(t):
    for f in t[:ENC]: f[:] = ['' if x.startswith('V12') else x for x in f]
rechazo('sin versión', mutar(sin_version), 'versión de la guía')
def leyenda(t):
    for f in t:
        for i, x in enumerate(f):
            if x == 'CTP+ = Reforged required': f[i] = 'CTP+ = Reforge needed'
rechazo('una línea de la leyenda cambió', mutar(leyenda), 'la leyenda cambió', '«CTP+ = Reforged required»')
def sin_emojis(t):
    for f in t[:5]: f[:] = ['' if '=' in x else x for x in f]
rechazo('TIER LIST sin leyenda de emojis', mutar(f_tier=sin_emojis), 'leyenda de los emojis')
def recortar(t): del t[ENC + 151:]
rechazo('pocas filas', mutar(recortar), 'tiene 150 filas')
def ctp_otro_formato(t):
    for f in t[ENC + 1:]:
        for c in ('Best CTP', '2nd Best CTP', 'Meta CTP (PVE)', 'Off-Meta CTP (PVE)', 'Meta CTP (PVP)', 'Off-Meta CTP (PVP)'):
            i = col(t, c)
            if f[i] not in ('', '-'): f[i] = 'CTP of ' + f[i].title()
rechazo('C.T.P. escritos de otra forma', mutar(ctp_otro_formato), 'columnas de C.T.P.: se entienden 0 de')
def nombres_otro_formato(t):
    for f in t[ENC + 1:]:
        f[col(t, 'Best Uni Character Name')] = f[0]
rechazo('nombres reemplazados por la clave', mutar(nombres_otro_formato), 'personaje y mejor uniforme')
rechazo('llega una página web', {'armado': b'<!DOCTYPE html><html>login</html>', 'tierlist': REAL['tierlist']}, 'página web')

# 11. no se pudo bajar
reset(); antes = copia()
linea = G.rechazar(['no se pudo bajar la planilla: HTTP Error 404'], '2026-10-12'); e = est()
ok('11 no se pudo bajar: se anota y la copia queda', copia() == antes and e['rechazo']['motivos'] == ['no se pudo bajar la planilla: HTTP Error 404']
   and e['comprobada'] == '2026-10-12' and e['tomada'] == '2026-10-01', linea)

# 12. después de un rechazo, una compatible lo limpia
G.aceptar(REAL, TV, CTPS, '2026-10-19'); e = est()
ok('12 una compatible después de un rechazo lo limpia', e['rechazo'] is None and e['comprobada'] == '2026-10-19')

# 13. una columna nueva en el medio no cambia nada de lo leído
def columna_nueva(t):
    for f in t: f.insert(5, 'X' if f is t[ENC] else '')
    t[ENC][5] = 'Columna Nueva'
crudo = mutar(columna_nueva)
r0 = G.leer(REAL['armado'].decode(), REAL['tierlist'].decode(), TV, CTPS)
r1 = G.leer(crudo['armado'].decode(), crudo['tierlist'].decode(), TV, CTPS)
reset(); linea = G.aceptar(crudo, TV, CTPS, '2026-10-05')
ok('13 columna nueva en el medio: se acepta y se lee igual', r0['pj'] == r1['pj'] and est()['rechazo'] is None, linea[:80])

# 14. un C.T.P. desconocido suelto: se acepta y queda listado
def ctp_nuevo(t): t[ENC + 1][col(t, 'Best CTP')] = 'WISDOM+'
crudo = mutar(ctp_nuevo)
reset(); linea = G.aceptar(crudo, TV, CTPS, '2026-10-05'); e = est()
r = G.leer(crudo['armado'].decode(), crudo['tierlist'].decode(), TV, CTPS)
p1 = next(p for p, x in r['pj'].items() if any(c.get('x') == 'WISDOM+' for c in x.get('ctp', [])))
ok('14 un C.T.P. nuevo suelto: se acepta, viaja crudo y queda en «sin interpretar»', e['rechazo'] is None and 'WISDOM+' in r['raros']['ctp']
   and 'WISDOM+' in linea, p1)

# 15. la planilla real: cobertura completa
r = G.leer(REAL['armado'].decode(), REAL['tierlist'].decode(), TV, CTPS)
bases = {t['base_portrait'] for t in TV}
base_de = {t['portrait']: t['base_portrait'] for t in TV}
ok('15 las 290 filas tienen personaje, uno por personaje, y no falta ninguno', len(r['pj']) == r['filas'] == 290 and not r['sin_pj']
   and {base_de[p] for p in r['pj']} == bases, (len(r['pj']), r['filas'], len(bases)))
# 16. fuentes.py (lo que va a data.js) usa la copia en uso y lleva el rechazo
os.chdir(RAIZ)
import fuentes
reset(); G.aceptar(mutar(renombrar), TV, CTPS, '2026-10-12')
out = fuentes.guia_armado(TV)
ok('16 data.js lleva la copia en uso y el rechazo con sus motivos', out['pj'] == r['pj'] and out['version'] == 'V12.2.0'
   and out['estado']['rechazo']['motivos'] == ['faltan columnas: «Best CTP»'] and out['estado']['comprobada'] == '2026-10-12'
   and out['raros'] == r['raros'] and out['leyenda']['iso']['shield'] == ['Drastic Density Enhancement', 'Binary Power'], out['estado'])
shutil.rmtree(tmp)
ok.fin()
