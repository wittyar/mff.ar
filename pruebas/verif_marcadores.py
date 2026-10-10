"""Marcadores de facción/tipo/raza ($HEROSUBTYPE1, $HEROCLASS1).

A. marcadores.py con tablas a mano de prueba (sobre los datos reales de work/): valor a mano
   en español y en inglés, valor de otra clase, cabecera mala, BOM, id que la API no trae,
   valor a mano distinto de la wiki, "Neutral" de bando, y la plantilla.
B. Lo que resolvió la wiki, contra la página con código aparte: el valor y el porcentaje
   juntos en una oración, en el mismo sentido (infligido/recibido).
C. La ficha (Playwright): valor subrayado con su origen, "sin especificar" con el aviso de
   la tabla a mano, en inglés, y de punta a punta con una tabla a mano de prueba (build
   completo -> data.js -> ficha).

1.0.17: la ficha ya conoce el origen 'l' (Leads & Supports, TITULO). Las cuentas de A y C (78 de la
wiki, la tabla del repo, AUDITORIA) y los avisos de resolver() son de la 1.0.16: con Leads & Supports
en marcadores.py cambian, y hay que volver a fijarlas con work/ bajado."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import csv, io, json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, datos_js, RAIZ
os.chdir(RAIZ)
sys.path.insert(0, f'{RAIZ}/scripts')
import marcadores as M

ok = Chequeo()
TABLA_REAL = M.TABLA
tmp = tempfile.mkdtemp(prefix='marc-')


def con_tabla(texto, bom=False):
    ruta = os.path.join(tmp, 'm.csv')
    with open(ruta, 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='') as f:
        f.write(texto)
    M.TABLA = ruta
    return ruta


def corre(texto, bom=False):
    con_tabla(texto, bom)
    try:
        return M.resolver(), None
    except SystemExit as e:
        return None, str(e)


CAB = 'id,valor,personaje,skill,efecto\n'
# ---------------------------------------------------------------- A
(base, efs, av), err = corre(CAB)
ok('A0 tabla vacía: 78 de la wiki, sin avisos', err is None and sum(1 for v in base.values() if v[1] == 'w') == 78
   and not any(av.values()), (len(base), av))
clase_de = {e['id']: e['clase'] for e in efs}
(r, _, av), err = corre(CAB + '1007760012,Superhéroe,,,\n1007760013,Super Villain,,,\n')
ok('A1 a mano en español y en inglés', err is None and r[1007760012] == ('Superhéroe', 'm') and r[1007760013] == ('Supervillano', 'm'),
   (r.get(1007760012), r.get(1007760013), err))
_, err = corre(CAB + '1007760012,Mutante,,,\n')
ok('A2 valor de otra clase corta el build y lista los posibles', err is not None and 'fila 2' in err and 'Superhéroe' in err
   and 'Mutante' not in err.split('posibles son:')[1], err)
_, err = corre('id;valor;personaje;skill;efecto\n1007760012;Superhéroe;;;\n')
ok('A3 cabecera distinta (separador ;) corta el build', err is not None and 'primera fila' in err, err)
(r, _, _), err = corre(CAB + '1007760012,Superhéroe,,,\n', bom=True)
ok('A4 con BOM (Bloc de notas) se lee igual', err is None and r[1007760012] == ('Superhéroe', 'm'), err)
(r, _, av), err = corre(CAB + '999999999,Superhéroe,,,\n1007760012,,,,\n')
ok('A5 id que la API no trae: aviso, y la fila vacía no cuenta', err is None and av['huerfanos'] == [999999999]
   and 1007760012 not in r, av)
sq = next(e['id'] for e in efs if e['p'] == 'squirrelgirl' and e['id'] in base)
(r, _, av), err = corre(CAB + f'{sq},Combate,,,\n')
ok('A6 a mano distinto de la wiki: gana la tabla y se avisa', err is None and r[sq] == ('Combate', 'm') and av['distintos'] == [sq], (r[sq], av))
fac = next(i for i, k in clase_de.items() if k == 'faccion' and i not in base)
pjs = next(i for i, k in clase_de.items() if k == 'personajes' and i not in base)
(r, _, _), err = corre(CAB + f'{fac},Neutral,,,\n{pjs},Neutral,,,\n')
ok('A7 "Neutral" es el bando, no el género (Neutro)', err is None and r[fac] == ('Neutral', 'm') and r[pjs] == ('Neutral', 'm'),
   (r.get(fac), r.get(pjs), err))
_, err = corre(CAB + f'{pjs},Neutro,,,\n')
ok('A8 "Neutro" (género) no sirve en un efecto de personajes', err is not None, err)
# plantilla: conserva lo cargado, agrega solo lo que falta, no agrega lo que resolvió la wiki
ruta = con_tabla(CAB + '1007760012,Superhéroe,a mano,x,y\n')
M.plantilla()
filas = list(csv.DictReader(open(ruta, encoding='utf-8')))
pend = {e['id'] for e in efs if e['id'] not in base}
ok('A9 plantilla: conserva la fila cargada tal cual y agrega las que faltan',
   filas[0] == {'id': '1007760012', 'valor': 'Superhéroe', 'personaje': 'a mano', 'skill': 'x', 'efecto': 'y'}
   and {int(f['id']) for f in filas} == pend and len(filas) == len(pend) and all(not f['valor'] for f in filas[1:]), len(filas))
M.plantilla()
ok('A10 plantilla corrida dos veces no duplica', len(list(csv.DictReader(open(ruta, encoding='utf-8')))) == len(filas))
real = list(csv.DictReader(open(TABLA_REAL, encoding='utf-8')))
DEL_JUEGO = {'1012391012', '1029004012', '1029004013'}   # b892477: las tres facciones que muestra el juego
ok('A11 la tabla del repo: una fila por marcador que la wiki no resuelve; con valor, solo las tres del juego',
   {int(f['id']) for f in real} == pend and len(real) == len(pend)
   and {f['id']: f['valor'] for f in real if f['valor']} == {i: 'Supervillano' for i in DEL_JUEGO}, len(real))
M.TABLA = TABLA_REAL

# ---------------------------------------------------------------- B
import dominio as D
EN = {}
for mapa in (D.SIDE, D.TYPE, D.ALLIES, D.GENDER, D.ABIL):
    for en, es in mapa.items():
        EN.setdefault(es, en)
chars = json.load(open('work/characters.json'))
base_de = {r['portrait']: r['base_portrait'] for r in chars}
nom = {r['base_portrait']: r['character'] for r in chars if r['uniformed'] == 'False'}


def pagina(p):
    wt = json.load(open(f"work/wikitext/{re.sub(r'[^A-Za-z0-9]+', '_', nom[base_de[p]])}.json"))['wt']
    wt = re.sub(r'\[\[File:[^\]]*\]\]', '', wt)
    wt = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', wt)
    return re.sub(r"<[^>]+>|'''?", ' ', wt)


malos = []
for e in efs:
    if base.get(e['id'], (None, ''))[1] != 'w':
        continue
    en = EN[base[e['id']][0]]
    txt = pagina(e['p'])
    hall = False
    for m in re.finditer(rf'(?i)({re.escape(en)}[^.%\n]{{0,45}}?\b{re.escape(e["pct"])}\s*%|\b{re.escape(e["pct"])}\s*%[^.%\n]{{0,60}}?{re.escape(en)})', txt):
        ini = max(txt.rfind('.', 0, m.start()), txt.rfind('\n', 0, m.start())) + 1
        oracion = txt[ini:m.end()]
        if ('received' in oracion.lower()) == ('received' in e['texto']):
            hall = True
    if not hall:
        malos.append((e['p'], e['skill'], e['texto'], en))
ok('B la wiki nombra cada valor resuelto con su % y su sentido', not malos, malos[:5])

# ---------------------------------------------------------------- C
from playwright.sync_api import sync_playwright
DJ = datos_js('MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_VOCAB_EN')
var = {}
for c in DJ['MFF_SEED_CHARACTERS']:
    var[c['p']] = (c['id'], '', c['name'])
    for u in c['uniforms']:
        var[u['p']] = (c['id'], u['id'], c['name'])


def esperados(p, lang):
    """(valores con g en orden de aparición, cuántos sin g) en las skills del retrato."""
    con, sin = [], 0
    for sk in DJ['MFF_SKILLS'][p]:
        for st in sk.get('st') or []:
            for f in st['fx']:
                if f.get('g'):
                    v = f['g'] if lang == 'es' else DJ['MFF_VOCAB_EN'][f['g']]
                    con.append((v, f['gs']))
    return con


def abrir(pg, p):
    cid, uid, nombre = var[p]
    pg.evaluate("document.querySelector('nav.topnav button').click()"); pg.wait_for_selector('#q')
    pg.fill('#q', ''); pg.wait_for_timeout(50); pg.fill('#q', nombre); pg.wait_for_timeout(200)
    pg.click(f'.ccard[data-cid="{cid}"][data-uid=""]'); pg.wait_for_selector('.fcab')
    if uid:
        pg.select_option('select[data-a="uniformSel"]', uid); pg.wait_for_timeout(120)
    pg.click('[data-a="fichaTab"][data-v="skills"]'); pg.wait_for_timeout(150)


TITULO = {'w': {'es': 'Dato de la wiki de Future Fight', 'en': 'From the Future Fight wiki'},
          'l': {'es': 'Dato de Leads & Supports de thanosvibs', 'en': 'From thanosvibs Leads & Supports'},
          'm': {'es': 'Dato cargado a mano', 'en': 'Entered by hand'}}
PEND = {'es': 'Se completa a mano en scripts/contenido/marcadores.csv', 'en': 'filled in by hand in scripts/contenido/marcadores.csv'}
SIN = {'es': 'sin especificar', 'en': 'unspecified'}


def leer(pg):
    ok_ = pg.evaluate("""() => [...document.querySelectorAll('.fxitems .tpl-ok')].map(e => [e.textContent, e.title])""")
    pend = pg.evaluate("""() => [...document.querySelectorAll('.fxitems .tpl')].map(e => [e.textContent, e.title])""")
    crudo = pg.evaluate("() => /\\$HERO/.test(document.querySelector('.fcuerpo').textContent)")
    return ok_, pend, crudo


def chequear(pg, p, lang, etiqueta, debe_pend=None):
    abrir(pg, p)
    ok_, pend, crudo = leer(pg)
    esp = esperados(p, lang)
    vistos = sorted(set((v, tt) for v, tt in ok_))
    quiero = sorted(set((v, gs) for v, gs in esp))
    bien = (sorted({v for v, _ in ok_}) == sorted({v for v, _ in esp})
            and all(any(TITULO[gs][lang] in tt for v2, tt in ok_ if v2 == v) for v, gs in esp)
            and not crudo)
    ok(f'C {etiqueta} [{lang}] valores completados con su origen', bien and len(ok_) >= len(set(esp)), (vistos, quiero))
    if debe_pend is not None:
        bien_p = (len(pend) > 0) == debe_pend and all(t_ == SIN[lang] and PEND[lang] in tt for t_, tt in pend
                                                      if PEND[lang] in tt or t_ == SIN[lang])
        ok(f'C {etiqueta} [{lang}] sin especificar con el aviso de la tabla', bien_p, pend[:3])


def ficha_casos(url, casos, lang_en=True, extra=None):
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1300, 'height': 900}); errores = []
        pg.on('pageerror', lambda e: errores.append(str(e)))
        pg.goto(url); pg.wait_for_selector('.ccard')
        for retrato, etq, pend in casos:
            chequear(pg, retrato, 'es', etq, pend)
        if extra:
            extra(pg)
        if lang_en:
            pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
            for retrato, etq, pend in casos:
                chequear(pg, retrato, 'en', etq, pend)
            pg.click('[data-a="lang"]'); pg.wait_for_timeout(300)
        ok('C sin errores de página', not errores, errores[:3])
        b.close()


# un retrato por clase de marcador resuelta, y Ebony Maw (lo que pidió el usuario)
por_clase = {}
for e in efs:
    if e['id'] in base and e['clase'] not in por_clase:
        por_clase[e['clase']] = e['p']
print('retratos por clase:', por_clase)
casos = [(p_, f'{k} ({p_})', None) for k, p_ in por_clase.items()]
casos += [('ebonymaw1', 'Ebony Maw Infinity War: uniforme resuelto por la wiki', False),
          ('ebonymaw2', 'Ebony Maw Dark Obsidian Armor: uniforme sí, T2 pendiente', True),
          ('ebonymaw3', "Ebony Maw General's Hand: todo pendiente", True)]
srv, url = levantar(carpeta_datos(), origen_local())
try:
    ficha_casos(url, casos)
finally:
    srv.terminate(); srv.wait()

# de punta a punta: tabla a mano de prueba -> build -> ficha (y después se restaura)
guardada = open(TABLA_REAL, encoding='utf-8').read()
respaldo = {f: open(f, 'rb').read() for f in ('data.js', 'datos.json', 'docs/AUDITORIA.md', 'mff-thanosvibs-import.json')}
try:
    lineas = guardada.splitlines(True)
    lineas = [re.sub(r'^(1007771012|1007771013),,', lambda m: m.group(1) + (',Superhéroe,' if m.group(1).endswith('2') else ',Super Villain,'), l)
              for l in lineas]
    open(TABLA_REAL, 'w', encoding='utf-8', newline='').write(''.join(lineas))
    subprocess.run([sys.executable, 'scripts/build.py'], check=True, capture_output=True)
    DJ = datos_js('MFF_SEED_CHARACTERS', 'MFF_SKILLS', 'MFF_VOCAB_EN')
    aud = open('docs/AUDITORIA.md', encoding='utf-8').read()
    ok('C build con la tabla: AUDITORIA cuenta los 2 nuevos a mano (5 con los del juego) y ya no los lista', '78 de la wiki, 5 a mano y 166 sin resolver' in aud
       and '| 1007771012 |' not in aud and '| 1007760012 |' in aud)
    srv, url = levantar(carpeta_datos(), origen_local())
    try:
        ficha_casos(url, [('ebonymaw2', 'Ebony Maw Dark Obsidian Armor con la tabla: T2 a mano, uniforme de la wiki', False)])
    finally:
        srv.terminate(); srv.wait()
finally:
    open(TABLA_REAL, 'w', encoding='utf-8', newline='').write(guardada)
    for f, b_ in respaldo.items():
        open(f, 'wb').write(b_)
ok('restaurado: data.js y la tabla como estaban', open(TABLA_REAL, encoding='utf-8').read() == guardada
   and open('data.js', 'rb').read() == respaldo['data.js'])
shutil.rmtree(tmp)
ok.fin()
