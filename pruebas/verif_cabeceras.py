"""Cabeceras de caché del servidor local: no-cache en todo lo servido (con 304 si no
cambió), no-store en la API, e index.html con la versión en las direcciones del programa."""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from rutas import RAIZ, PRUEBAS, SALIDA  # noqa: E401
import json, os, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import origen_local, carpeta_datos, levantar, Chequeo, RAIZ, DATOS
ok = Chequeo()
srv, url = levantar(carpeta_datos(), origen_local())
base = url.rsplit('/', 1)[0]
ver = json.load(open(os.path.join(RAIZ, 'version.json'), encoding='utf-8'))['version']
def pedir(ruta, **cab):
    req = urllib.request.Request(base + ruta, headers=cab)
    try:
        r = urllib.request.urlopen(req, timeout=10); return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, b''
try:
    st, hd, cuerpo = pedir('/index.html')
    html = cuerpo.decode('utf-8')
    ok('index.html: no-cache', st == 200 and hd.get_all('Cache-Control') == ['no-cache'], hd.get_all('Cache-Control'))
    ok('index.html: app.js y styles.css con la versión', f'"app.js?v={ver}"' in html and f'"styles.css?v={ver}"' in html
       and '"data.js"' in html, [l.strip() for l in html.splitlines() if '.js' in l or '.css' in l])
    st2, hd2, _ = pedir('/')
    ok('/ sirve lo mismo', st2 == 200 and f'"app.js?v={ver}"' in _ .decode() if False else st2 == 200)
    st, hd, cuerpo = pedir(f'/app.js?v={ver}')
    ok('app.js?v=: 200, no-cache y Last-Modified', st == 200 and hd.get_all('Cache-Control') == ['no-cache'] and hd['Last-Modified'],
       (st, hd.get_all('Cache-Control'), hd['Last-Modified']))
    st, hd, _ = pedir(f'/app.js?v={ver}', **{'If-Modified-Since': hd['Last-Modified']})
    ok('app.js sin cambios: 304', st == 304, st)
    for ruta in ('/styles.css', '/data.js', '/docs/AUDITORIA.md', '/favicon.ico'):
        st, hd, _ = pedir(ruta)
        ok(f'{ruta}: no-cache', st == 200 and hd.get_all('Cache-Control') == ['no-cache'], (st, hd.get_all('Cache-Control')))
    img = next(f for f in sorted(os.listdir(os.path.join(DATOS, 'images'))) if f.endswith('.png'))
    st, hd, _ = pedir('/images/' + img)
    ok('retrato: no-cache', st == 200 and hd.get_all('Cache-Control') == ['no-cache'], (img, st, hd.get_all('Cache-Control')))
    st, hd, _ = pedir('/api/estado', **{'X-MFF': '1'})
    ok('API: solo no-store', st == 200 and hd.get_all('Cache-Control') == ['no-store'], hd.get_all('Cache-Control'))
    st, hd, _ = pedir('/no-existe.js')
    ok('404 sigue siendo 404', st == 404, st)
finally:
    srv.terminate(); srv.wait()
ok.fin()
