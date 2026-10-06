"""Pantalla de rescate de TA GUIANAEL MFF (#2).

Una página propia del servidor (GET /rescate), hecha acá: no usa app.js, styles.css ni data.js, así que abre aunque
la app no pueda arrancar (la 1.0.22, el 5 de octubre de 2026, quedó trabada hasta reinstalar). La abre el lanzador
cuando la página no avisa a tiempo que arrancó o avisa un error. Desde ella: actualizar la app (el parche de la última
versión), bajar el instalador, volver al programa anterior (programa-anterior/, que guarda cada parche) y volver a bajar
los datos. Usa la API de siempre (/api/estado, /api/novedades, /api/progreso, /api/app/actualizar,
/api/datos/actualizar, /api/latido) y la suya (/api/rescate, /api/rescate/volver).

Solo biblioteca estándar: corre con el Python embebido del instalador.
"""
import json

TEXTOS = {
    'es': {
        'titulo': 'Pantalla de rescate',
        'intro': 'La app no pudo arrancar. Desde acá se puede actualizar, volver a la versión anterior o volver a bajar los datos; tu capa (listas, equipos, ajustes) no se toca.',
        'motivo_error': 'La app avisó este error al arrancar:',
        'motivo_tiempo': 'La app no avisó que arrancó en {n} segundos.',
        'motivo_ninguno': 'Se abrió a mano: la app no avisó ningún problema.',
        'estado': 'Lo instalado',
        'version': 'Versión de la app',
        'formato': 'Formato de datos que usa',
        'formato_n': 'formato {n}',
        'datos': 'Datos del juego',
        'sin_datos': 'no hay',
        'anterior': 'Programa anterior guardado',
        'sin_anterior': 'no hay (se guarda al aplicar un parche)',
        'publicada': 'Última versión publicada',
        'buscando': 'consultando…',
        'acciones': 'Qué hacer',
        'actualizar': 'Actualizar a la {v}',
        'actualizar_t': 'Baja el parche de la última versión, lo aplica y reinicia la app.',
        'al_dia': 'No hay una versión más nueva que la instalada.',
        'instalador': 'Bajar el instalador de la {v}',
        'instalador_t': 'Instala de nuevo el programa entero; tus datos y tu capa quedan.',
        'volver': 'Volver a la {v}',
        'volver_t': 'Vuelve a poner el programa que había antes del último parche y reinicia la app.',
        'volver_ok': '¿Volver a la versión {v}? La app se reinicia.',
        'datos_bajar': 'Volver a bajar los datos',
        'datos_bajar_t': 'Baja de nuevo los datos publicados para el formato de esta versión.',
        'abrir': 'Abrir la app',
        'repo': 'La app corre desde el repo: el programa se cambia con git (git pull, git checkout).',
        'trabajando': 'Trabajando…',
        'reiniciando': 'Reiniciando la app…',
        'listo_datos': 'Datos bajados. Ya podés abrir la app.',
        'error': 'Error:',
        'registro': 'Final de registro.txt',
    },
    'en': {
        'titulo': 'Rescue screen',
        'intro': 'The app could not start. From here you can update it, go back to the previous version or download the data again; your layer (lists, teams, settings) is not touched.',
        'motivo_error': 'The app reported this error on startup:',
        'motivo_tiempo': 'The app did not report that it started within {n} seconds.',
        'motivo_ninguno': 'Opened by hand: the app reported no problem.',
        'estado': 'What is installed',
        'version': 'App version',
        'formato': 'Data format it uses',
        'formato_n': 'format {n}',
        'datos': 'Game data',
        'sin_datos': 'none',
        'anterior': 'Saved previous program',
        'sin_anterior': 'none (it is saved when a patch is applied)',
        'publicada': 'Latest published version',
        'buscando': 'checking…',
        'acciones': 'What to do',
        'actualizar': 'Update to {v}',
        'actualizar_t': 'Downloads the patch of the latest version, applies it and restarts the app.',
        'al_dia': 'There is no version newer than the installed one.',
        'instalador': 'Download the {v} installer',
        'instalador_t': 'Installs the whole program again; your data and your layer stay.',
        'volver': 'Go back to {v}',
        'volver_t': 'Puts back the program from before the last patch and restarts the app.',
        'volver_ok': 'Go back to version {v}? The app restarts.',
        'datos_bajar': 'Download the data again',
        'datos_bajar_t': 'Downloads again the data published for this version\'s format.',
        'abrir': 'Open the app',
        'repo': 'The app runs from the repo: the program changes with git (git pull, git checkout).',
        'trabajando': 'Working…',
        'reiniciando': 'Restarting the app…',
        'listo_datos': 'Data downloaded. You can open the app now.',
        'error': 'Error:',
        'registro': 'End of registro.txt',
    },
}

ESTILO = """
:root{color-scheme:dark;--bg:#16181c;--panel:#1f2228;--line:#30343c;--text:#e8e6e1;--muted:#9a9890;--accent:#e0a33a;--danger:#d9534f}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:760px;margin:0 auto;padding:32px 16px 48px}
h1{font-size:26px;margin:0 0 8px}
h2{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:28px 0 10px}
p{margin:0 0 10px}
.motivo{border-left:3px solid var(--danger);background:var(--panel);padding:10px 14px;border-radius:6px;white-space:pre-wrap;word-break:break-word}
dl{display:grid;grid-template-columns:minmax(0,220px) minmax(0,1fr);gap:6px 14px;margin:0}
dt{color:var(--muted)} dd{margin:0;word-break:break-word}
.accion{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;padding:10px 0;border-top:1px solid var(--line)}
.accion:first-of-type{border-top:0}
.accion span{color:var(--muted);font-size:13px;flex:1 1 260px}
button,a.btn{font:inherit;background:var(--accent);color:#1a1408;border:0;border-radius:6px;padding:8px 14px;cursor:pointer;text-decoration:none;font-weight:600}
button.sec,a.btn.sec{background:transparent;color:var(--text);border:1px solid var(--line)}
button:disabled{opacity:.5;cursor:default}
#aviso{min-height:1.5em;margin-top:14px} #aviso.err{color:var(--danger)}
pre{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px;font-size:12px;overflow:auto;max-height:320px;white-space:pre-wrap;word-break:break-word}
"""

SCRIPT = r"""
const T = JSON.parse(document.getElementById('textos').textContent);
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
async function api (ruta, metodo) {
  const r = await fetch(ruta, { method: metodo || 'GET', headers: { 'X-MFF': '1' }, cache: 'no-store' });
  const c = await r.json();
  if (!r.ok) throw new Error(c.error || ('HTTP ' + r.status));
  return c;
}
function aviso (txt, err) { const a = $('#aviso'); a.textContent = txt; a.className = err ? 'err' : ''; }
function ocupado (si) { document.querySelectorAll('button').forEach(b => { b.disabled = si; }); }
let ESTADO = null, VERSION_ANTES = null;
async function cargar () {
  ESTADO = await api('/api/estado');
  VERSION_ANTES = ESTADO.version;
  setInterval(() => fetch('/api/latido', { method: 'POST', headers: { 'X-MFF': '1' } }), ESTADO.latido_cada * 1000);
  fetch('/api/latido', { method: 'POST', headers: { 'X-MFF': '1' } });
  const r = await api('/api/rescate');
  const m = r.motivo;
  $('#motivo').textContent = !m ? T.motivo_ninguno : m.tipo === 'error' ? T.motivo_error + '\n' + m.detalle
    : T.motivo_tiempo.replace('{n}', m.segundos);
  const d = ESTADO.datos_local;
  $('#version').textContent = ESTADO.version;
  $('#formato').textContent = ESTADO.formato_datos;
  $('#datos').textContent = d ? `${d.juego} · ${d.generado} · ${T.formato_n.replace('{n}', d.formato)}` : T.sin_datos;
  $('#anterior').textContent = r.programa_anterior || T.sin_anterior;
  $('#registro').textContent = r.registro;
  if (ESTADO.desde_repo) { $('#repo').hidden = false; }
  else if (r.programa_anterior) {
    $('#volver').hidden = false;
    $('#volver button').textContent = T.volver.replace('{v}', r.programa_anterior);
    $('#volver button').onclick = () => volver(r.programa_anterior);
  }
  $('#datosbajar button').onclick = bajarDatos;
  let n;
  try { n = await api('/api/novedades'); }
  catch (e) { n = { app: { error: e.message } }; }
  const a = n.app;
  if (a.error) { $('#publicada').textContent = T.error + ' ' + a.error; return; }
  $('#publicada').textContent = a.version;
  $('#instalador').hidden = false;
  $('#instalador a').textContent = T.instalador.replace('{v}', a.version);
  $('#instalador a').href = a.instalador;
  if (ESTADO.desde_repo) return;
  if (a.hay && a.aplicable) {
    $('#actualizar').hidden = false;
    $('#actualizar button').textContent = T.actualizar.replace('{v}', a.version);
    $('#actualizar button').onclick = actualizar;
  } else if (!a.hay) { $('#aldia').hidden = false; }
}
async function seguir (tarea) {
  for (;;) {
    await new Promise(r => setTimeout(r, 700));
    const p = (await api('/api/progreso'))[tarea];
    if (p.terminado) { if (p.error) throw new Error(p.error); return p.resultado; }
  }
}
async function esperarReinicio () {
  aviso(T.reiniciando);
  for (;;) {
    await new Promise(r => setTimeout(r, 1000));
    try { const e = await api('/api/estado'); if (e.version !== VERSION_ANTES) return location.replace('/index.html'); }
    catch (e) { /* el servidor se está reiniciando */ }
  }
}
async function actualizar () {
  ocupado(true); aviso(T.trabajando);
  try { await api('/api/app/actualizar', 'POST'); await seguir('app'); await esperarReinicio(); }
  catch (e) { aviso(T.error + ' ' + e.message, true); ocupado(false); }
}
async function volver (v) {
  if (!confirm(T.volver_ok.replace('{v}', v))) return;
  ocupado(true); aviso(T.trabajando);
  try { await api('/api/rescate/volver', 'POST'); await esperarReinicio(); }
  catch (e) { aviso(T.error + ' ' + e.message, true); ocupado(false); }
}
async function bajarDatos () {
  ocupado(true); aviso(T.trabajando);
  try { await api('/api/datos/actualizar', 'POST'); await seguir('datos'); aviso(T.listo_datos); }
  catch (e) { aviso(T.error + ' ' + e.message, true); }
  ocupado(false);
}
cargar().catch(e => aviso(T.error + ' ' + e.message, true));
"""


def _h(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def pagina(lang):
    t = TEXTOS[lang]
    textos = json.dumps(t, ensure_ascii=False).replace('</', '<\\/')
    def accion(id_, boton, ayuda, oculta=True):
        return f'<div class="accion" id="{id_}"{" hidden" if oculta else ""}>{boton}<span>{_h(ayuda)}</span></div>'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_h(t['titulo'])} · TA GUIANAEL MFF</title>
<link rel="icon" href="favicon.ico">
<style>{ESTILO}</style>
</head>
<body>
<main>
<h1>{_h(t['titulo'])}</h1>
<p>{_h(t['intro'])}</p>
<p class="motivo" id="motivo"></p>
<h2>{_h(t['estado'])}</h2>
<dl>
<dt>{_h(t['version'])}</dt><dd id="version"></dd>
<dt>{_h(t['formato'])}</dt><dd id="formato"></dd>
<dt>{_h(t['datos'])}</dt><dd id="datos"></dd>
<dt>{_h(t['anterior'])}</dt><dd id="anterior"></dd>
<dt>{_h(t['publicada'])}</dt><dd id="publicada">{_h(t['buscando'])}</dd>
</dl>
<h2>{_h(t['acciones'])}</h2>
<p id="repo" hidden>{_h(t['repo'])}</p>
{accion('actualizar', '<button></button>', t['actualizar_t'])}
<p id="aldia" hidden>{_h(t['al_dia'])}</p>
{accion('instalador', '<a class="btn sec" target="_blank" rel="noopener"></a>', t['instalador_t'])}
{accion('volver', '<button class="sec"></button>', t['volver_t'])}
{accion('datosbajar', f'<button class="sec">{_h(t["datos_bajar"])}</button>', t['datos_bajar_t'], oculta=False)}
{accion('abrir', f'<a class="btn sec" href="/index.html">{_h(t["abrir"])}</a>', '', oculta=False)}
<p id="aviso"></p>
<h2>{_h(t['registro'])}</h2>
<pre id="registro"></pre>
</main>
<script type="application/json" id="textos">{textos}</script>
<script>{SCRIPT}</script>
</body>
</html>
"""
