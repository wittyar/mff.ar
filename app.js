/* Comparador MFF — app standalone en JS vanilla. Sin build: corre desde file:// o cualquier host estático.
 *
 * Reglas de datos (importante):
 *   - data.js es la ÚNICA fuente de personajes, uniformes, skills, imágenes y tier lists importadas.
 *     Nunca se copia a localStorage: regenerar data.js se ve al recargar, sin borrar nada.
 *   - localStorage guarda SOLO la capa del usuario: ediciones y personajes propios, equipos,
 *     tier lists propias, cambios sobre las importadas, imágenes subidas y preferencias.
 */
(function () {
'use strict';

// ============================================================================
// DATOS DE data.js (solo lectura)
// ============================================================================
const SEED           = window.MFF_SEED;
const CHARS_SEED     = window.MFF_SEED_CHARACTERS || [];
const IMAGES_SEED    = window.MFF_SEED_IMAGES || {};
const TIERLISTS_SEED = window.MFF_SEED_TIERLISTS || [];
const ASSIGN_SEED    = window.MFF_SEED_TIER_ASSIGNMENTS || {};
const DEFAULT_ROWS   = window.MFF_DEFAULT_TIER_ROWS || [{id:'S',label:'S'},{id:'A',label:'A'},{id:'B',label:'B'},{id:'C',label:'C'},{id:'D',label:'D'}];
const SLOT_ORDER     = ['Liderazgo','Pasiva','Activa 1','Activa 2','Activa 3','Activa 4','Activa 5','Definitiva'];
const REMOVED        = null; // marca explícita: entrada de una lista importada que el usuario quitó

// ============================================================================
// CAPA DE USUARIO
// ============================================================================
const LS_KEY = 'mff_user_v1';
function blankUser () {
  return {
    charEdits: {},                    // id de data.js -> personaje editado (reemplaza al del seed)
    charNew: [],                      // personajes creados a mano
    teams: [],
    lists: [],                        // tier lists propias: {id,name,rows}
    assign: {},                       // listId -> {clave: filaId | null}
    images: {},                       // 'portrait-x' / 'fullbody-x' / 'brand-logo' subidos
    modes: JSON.parse(JSON.stringify(SEED.MODES)),
    prefs: { view:'grid', sort:'name', dir:1, filtersOpen:false, refList: (TIERLISTS_SEED[0]||{}).id || '',
             kind:'todo', filters:{ c:[], r:[], t:[], f:[], ins:[], race:[], origin:[], ab:[] },
             flags:{ t4:false, trans:false, nuevo:false } }
  };
}
let U = loadUser();
function loadUser () {
  const base = blankUser();
  try {
    const raw = localStorage.getItem(LS_KEY);
    if (!raw) return base;
    const saved = JSON.parse(raw);
    const u = Object.assign(base, saved);
    u.prefs = Object.assign(base.prefs, saved.prefs || {});
    u.prefs.filters = Object.assign(base.prefs.filters, (saved.prefs||{}).filters || {});
    u.prefs.flags = Object.assign(base.prefs.flags, (saved.prefs||{}).flags || {});
    return u;
  } catch (e) { console.warn('capa de usuario ilegible, se arranca en limpio', e); return base; }
}
function saveUser () {
  try { localStorage.setItem(LS_KEY, JSON.stringify(U)); }
  catch (e) { alert('No se pudo guardar en este navegador: ' + e.message); }
}

// ---- vistas derivadas (data.js + capa de usuario) ----
let CHARS = [], CHAR_BY_ID = {}, LISTS = [];
function rebuild () {
  CHARS = CHARS_SEED.map(c => U.charEdits[c.id] || c).concat(U.charNew);
  CHAR_BY_ID = {}; CHARS.forEach(c => { CHAR_BY_ID[c.id] = c; });
  LISTS = TIERLISTS_SEED.concat(U.lists);
}
function commit () { saveUser(); rebuild(); render(); }

function imgUrl (id) { return U.images[id] || IMAGES_SEED[id] || ''; }
function listById (id) { return LISTS.find(l => l.id === id) || null; }
function rowsOf (list) { return (list && list.rows && list.rows.length) ? list.rows : DEFAULT_ROWS; }
/** Asignaciones efectivas de una lista: las de data.js con los cambios del usuario encima. */
function assignOf (listId) {
  const out = Object.assign({}, ASSIGN_SEED[listId] || {});
  const mine = U.assign[listId] || {};
  for (const k in mine) { if (mine[k] === REMOVED) delete out[k]; else out[k] = mine[k]; }
  return out;
}
function setAssign (listId, key, rowId) {
  U.assign[listId] = U.assign[listId] || {};
  U.assign[listId][key] = rowId;
  commit();
}

// ============================================================================
// ESTADO DE UI (no persistido)
// ============================================================================
let ui = {
  view: 'roster', search: '', page: 0,
  pickMode: false, picks: [],
  charId: null, uniformId: 'base',
  tierList: (TIERLISTS_SEED[0] || {}).id || '',
  teamOpen: false, team: { name:'', members:[], reason:'', modeId:'' }, teamSearch:'', teamPage:0,
  newListName: '', poolOpen: false, poolSearch: '',
  edStep: 0, edDraft: null, edId: null,
  dragKey: null
};

// ============================================================================
// HELPERS
// ============================================================================
const $ = (s, r) => (r || document).querySelector(s);
function h (v) { const d = document.createElement('div'); d.textContent = v == null ? '' : String(v); return d.innerHTML; }
function classColor (c) { return ({'Combate':'var(--class-combate)','Detonación':'var(--class-detonacion)','Velocidad':'var(--class-velocidad)','Universal':'var(--class-universal)'})[c] || 'var(--text-3)'; }
function dmgColor (d) { return ({'Físico':'var(--dmg-fisico)','Energía':'var(--dmg-energia)','PG':'var(--dmg-pg)'})[d] || 'var(--text-3)'; }
function tierColor (t) { return ({'T2':'var(--tier-t2)','T3':'var(--tier-t3)','T4':'var(--tier-t4)'})[t] || 'var(--text-3)'; }
function roleColor (r) { return ({'Daño':'var(--role-dano)','Soporte':'var(--role-soporte)','Control':'var(--role-control)','Tanque':'var(--role-tanque)'})[r] || 'var(--line-2)'; }
function rowColor (i, n) {
  const scale = ['#ff2d55','#ff6b3d','#ffb020','#7ed957','#4dd0e1','#7aa8ff','#a78bfa','#8a8f9c','#6b7080'];
  return scale[Math.min(i, scale.length - 1)] || '#6b7080';
}
function tagSolid (label, color) { return `<span class="tag solid" style="background:${color}">${h(label)}</span>`; }
function tagGhost (label, color) { return `<span class="tag ghost" style="color:${color}">${h(label)}</span>`; }
function icon (value) { const u = imgUrl('icon-' + value); return u ? `<img src="${u}" alt="" style="width:15px;height:15px;border-radius:3px;vertical-align:-3px">` : ''; }
function shot (id, cls) { const u = imgUrl('portrait-' + id); return u ? `<img class="${cls||''}" src="${u}" alt="" loading="lazy">` : `<span class="ph">SIN RETRATO</span>`; }
function slotClass (slot) { return slot === 'Liderazgo' ? 'lead' : slot === 'Pasiva' ? 'pass' : slot === 'Definitiva' ? 'ult' : ''; }
function pluralUni (n) { return n + (n === 1 ? ' uniforme' : ' uniformes'); }
/** La wiki no publica el instinto de todos: mostrar "Desconocido" es ruido, se omite. */
function insTag (v) { return v && v !== 'Desconocido' ? `<span class="tag dim">${h(v)}</span>` : ''; }
/** Marca de trascendido: glifo aparte porque no todas las fuentes de texto traen ✦. */
function transTag (on) { return on ? `<span class="tag solid" style="background:var(--gold)" title="Trascendido">TR</span>` : ''; }

function findUniform (ch, uid) { return ch && ch.uniforms.find(u => u.id === uid); }
/** Vista efectiva de "personaje base" o "personaje con uniforme X": el uniforme pisa lo que redefine. */
function variant (cid, uid) {
  const ch = CHAR_BY_ID[cid]; if (!ch) return null;
  const base = ch.baseSkills || [];
  const u = uid && uid !== 'base' ? findUniform(ch, uid) : null;
  if (!u) return { cid: ch.id, uid: null, key: ch.id + '::base', id: ch.id, name: ch.name, sub: 'Base',
                   c: ch.c, f: ch.f, t: ch.t, ins: ch.ins, r: ch.r, ab: ch.abilities || [],
                   striker: ch.striker, wba: ch.wba, trans: ch.trans, nuevo: ch.new, cost: '',
                   ch, skills: base };
  return { cid: ch.id, uid: u.id, key: ch.id + '::' + u.id, id: u.id, name: ch.name, sub: u.name,
           c: u.c || ch.c, f: u.f || ch.f, t: u.tier || ch.t, ins: ch.ins, r: ch.r, ab: u.ab || ch.abilities || [],
           striker: u.striker != null ? u.striker : ch.striker, wba: u.wba || ch.wba,
           trans: u.trans, nuevo: u.new, cost: u.cost || '',
           ch, skills: base.concat(u.skills) };
}
function allVariants () {
  const out = [];
  CHARS.forEach(ch => { out.push(variant(ch.id, null)); ch.uniforms.forEach(u => out.push(variant(ch.id, u.id))); });
  return out;
}
function fullLabel (v) { return v.uid ? v.name + ' — ' + v.sub : v.name; }

/** Heurística propia: bando compartido, cobertura de roles y ventaja de clase. No sale del juego. */
function synergy (vs) {
  if (vs.length < 2) return { score: 0, reasons: [] };
  const reasons = []; let score = 0;
  if (vs.every(v => v.f === vs[0].f)) { score += 2; reasons.push('Mismo bando (' + vs[0].f + '): bonos de equipo activos.'); }
  const roles = new Set(vs.flatMap(v => v.r));
  const covered = ['Tanque','Control','Daño','Soporte'].filter(r => roles.has(r));
  if (covered.length >= 2) { score += covered.length; reasons.push('Roles cubiertos: ' + covered.join(' + ') + '.'); }
  const classes = new Set(vs.map(v => v.c));
  if (classes.size === vs.length) { score += 1; reasons.push('Clases distintas: no comparten la misma debilidad.'); }
  vs.forEach(a => vs.forEach(b => {
    if (a !== b && SEED.CLASS_ADVANTAGE[a.c] === b.c) {
      score += 1;
      reasons.push(fullLabel(a) + ' (' + a.c + ') cubre la debilidad de clase de ' + fullLabel(b) + '.');
    }
  }));
  return { score, reasons: [...new Set(reasons)] };
}

function skillFx (sk) {
  const L = { general:'General', self:'A sí mismo', enemy:'Al oponente', allies:'Al equipo' };
  if (!sk.fx) return `<div class="fxline"><div class="fxitems"><span>${h(sk.d)}</span></div></div>`;
  let out = '';
  for (const k of ['general','self','enemy','allies']) {
    const arr = sk.fx[k];
    if (!arr || !arr.length) continue;
    out += `<div class="fxline"><span class="fxlabel fx-${k}">${L[k]}</span><div class="fxitems">${arr.map(x => `<span>${h(x)}</span>`).join('')}</div></div>`;
  }
  return out;
}
function skillCard (sk) {
  return `<div class="skill">
    <div class="top">
      <span class="slotbadge ${slotClass(sk.slot)}">${h(sk.slot)}</span>
      <span class="nm">${h(sk.n)}</span>
      <span class="tag dim">${h(window.MFF_skillTiming(sk))}</span>
      ${sk.dmg && sk.dmg !== 'Ninguno' ? tagGhost(sk.dmg, dmgColor(sk.dmg)) : ''}
    </div>
    <div class="body">
      ${skillFx(sk)}
      ${(sk.tags && sk.tags.length) || sk.ii || sk.iframe ? `<div class="row" style="margin-top:3px">
        ${(sk.tags || []).map(t => `<span class="tag dim">${h(t)}</span>`).join('')}
        ${sk.ii ? tagGhost('Ignora iframe','var(--accent-2)') : ''}
        ${sk.iframe ? tagGhost('Tiene iframe','var(--allies)') : ''}
      </div>` : ''}
    </div>
  </div>`;
}
/** Máximo 4 columnas en la comparación: al agregar la quinta se descarta la más vieja. */
function togglePick (cid, uid) {
  const key = cid + '::' + (uid || 'base');
  const i = ui.picks.findIndex(p => p.key === key);
  if (i > -1) { ui.picks.splice(i, 1); return; }
  ui.picks.push({ cid, uid: uid || null, key });
  if (ui.picks.length > 4) ui.picks.shift();
}
function readFile (file, cb) { const r = new FileReader(); r.onload = () => cb(r.result); r.readAsDataURL(file); }

// ============================================================================
// ROSTER
// ============================================================================
const SORTS = {
  name:   { label:'Nombre',  get: v => fullLabel(v).toLowerCase() },
  tier:   { label:'Tier',    get: v => ({T4:0,T3:1,T2:2})[v.t] },
  clase:  { label:'Clase',   get: v => v.c },
  bando:  { label:'Bando',   get: v => v.f },
  rank:   { label:'Posición en la lista', get: v => rankIndex(v.key) },
  skills: { label:'Cantidad de skills',   get: v => -v.skills.length }
};
function rankIndex (key) {
  const list = listById(U.prefs.refList); if (!list) return 999;
  const rows = rowsOf(list); const r = assignOf(list.id)[key];
  const i = rows.findIndex(x => x.id === r);
  return i === -1 ? 999 : i;
}
function rankLabel (key) {
  const list = listById(U.prefs.refList); if (!list) return null;
  const r = assignOf(list.id)[key]; if (!r) return null;
  const rows = rowsOf(list); const i = rows.findIndex(x => x.id === r);
  return i === -1 ? null : { label: rows[i].label, color: rowColor(i, rows.length) };
}

function rosterData () {
  const q = ui.search.trim().toLowerCase();
  const P = U.prefs, F = P.filters, G = P.flags;
  let list = allVariants().filter(v => {
    if (P.kind === 'base' && v.uid) return false;
    if (P.kind === 'uni' && !v.uid) return false;
    if (q && !(v.name.toLowerCase().includes(q) || v.sub.toLowerCase().includes(q))) return false;
    if (F.c.length && !F.c.includes(v.c)) return false;
    if (F.t.length && !F.t.includes(v.t)) return false;
    if (F.f.length && !F.f.includes(v.f)) return false;
    if (F.ins.length && !F.ins.includes(v.ins)) return false;
    if (F.race.length && !F.race.includes(v.ch.race)) return false;
    if (F.origin.length && !F.origin.includes(v.ch.origin)) return false;
    if (F.r.length && !F.r.some(r => v.r.includes(r))) return false;
    if (F.ab.length && !F.ab.some(a => v.ab.includes(a))) return false;
    if (G.t4 && v.t !== 'T4') return false;
    if (G.trans && !v.trans) return false;
    if (G.nuevo && !v.nuevo) return false;
    return true;
  });
  const s = SORTS[U.prefs.sort] || SORTS.name;
  list.sort((a, b) => {
    const x = s.get(a), y = s.get(b);
    if (x < y) return -1 * U.prefs.dir;
    if (x > y) return 1 * U.prefs.dir;
    return fullLabel(a).localeCompare(fullLabel(b));
  });
  return list;
}

function toolbar (total, shown) {
  const P = U.prefs, F = P.filters, G = P.flags;
  const active = Object.values(F).reduce((n, a) => n + a.length, 0) + Object.values(G).filter(Boolean).length;
  const group = (label, cat, values) => `<div class="filtergroup"><div class="lbl">${label}</div><div class="row">${
    values.map(v => `<button class="chip ${F[cat].includes(v) ? 'on' : ''}" data-a="filter" data-cat="${cat}" data-v="${h(v)}">${icon(v)}${h(v)}</button>`).join('')
  }</div></div>`;
  return `<div class="toolbar">
    <div class="line">
      <div class="search"><input id="q" placeholder="Buscar personaje o uniforme…" value="${h(ui.search)}" data-a="search"></div>
      <button class="btn ${U.prefs.filtersOpen ? 'primary' : ''}" data-a="toggleFilters">Filtros${active ? ' · ' + active : ''}</button>
      ${active || ui.search ? `<button class="btn sm" data-a="clearFilters">Limpiar</button>` : ''}
      <div class="seg">
        <button class="${P.kind === 'todo' ? 'on' : ''}" data-a="kind" data-v="todo">Todo</button>
        <button class="${P.kind === 'base' ? 'on' : ''}" data-a="kind" data-v="base">Bases</button>
        <button class="${P.kind === 'uni' ? 'on' : ''}" data-a="kind" data-v="uni">Uniformes</button>
      </div>
      <div class="seg">
        <button class="${U.prefs.view === 'grid' ? 'on' : ''}" data-a="view" data-v="grid" title="Tarjetas">Tarjetas</button>
        <button class="${U.prefs.view === 'dense' ? 'on' : ''}" data-a="view" data-v="dense" title="Compacto">Compacto</button>
        <button class="${U.prefs.view === 'table' ? 'on' : ''}" data-a="view" data-v="table" title="Tabla">Tabla</button>
      </div>
      <select data-a="sort" title="Ordenar">${Object.entries(SORTS).map(([k, s]) => `<option value="${k}" ${k === U.prefs.sort ? 'selected' : ''}>${h(s.label)}</option>`).join('')}</select>
      <button class="btn icon" data-a="dir" title="Invertir orden">${U.prefs.dir === 1 ? '↑' : '↓'}</button>
      <button class="btn ${ui.pickMode ? 'primary' : ''}" data-a="pickMode">${ui.pickMode ? `Comparando (${ui.picks.length}/4)` : 'Comparar'}</button>
      <span class="count"><b>${shown}</b> de ${total}</span>
    </div>
    ${U.prefs.filtersOpen ? `<div class="filterpanel">
      ${group('Clase','c',SEED.CLASSES)}
      ${group('Rol','r',SEED.ROLES)}
      ${group('Tier','t',SEED.TIERS)}
      ${group('Bando','f',SEED.FACTIONS)}
      ${group('Instinto','ins',SEED.INSTINCTS)}
      ${group('Raza','race',SEED.RACES)}
      ${group('Origen','origin',[...new Set(CHARS.map(c => c.origin).filter(Boolean))].sort())}
      ${group('Habilidad','ab',SEED.SKILL_TAGS)}
      <div class="filtergroup"><div class="lbl">Atajos</div><div class="row">
        <button class="chip ${G.t4 ? 'on' : ''}" data-a="flag" data-v="t4">Solo T4</button>
        <button class="chip ${G.trans ? 'on' : ''}" data-a="flag" data-v="trans">Trascendidos</button>
        <button class="chip ${G.nuevo ? 'on' : ''}" data-a="flag" data-v="nuevo">Nuevos</button>
      </div></div>
      <div class="filtergroup"><div class="lbl">Lista de referencia (define la posición que se muestra)</div>
        <select data-a="refList" style="width:100%">
          <option value="">— ninguna —</option>
          ${LISTS.map(l => `<option value="${l.id}" ${l.id === U.prefs.refList ? 'selected' : ''}>${h(l.name)}</option>`).join('')}
        </select>
      </div>
    </div>` : ''}
  </div>`;
}

function cardHtml (v) {
  const picked = ui.picks.some(p => p.key === v.key);
  const rank = rankLabel(v.key);
  return `<div class="ccard ${v.uid ? 'uni' : ''} ${picked ? 'sel' : ''}" style="--acc:${classColor(v.c)}" data-a="open" data-cid="${v.cid}" data-uid="${v.uid || ''}">
    ${ui.pickMode ? `<div class="pick ${picked ? 'on' : ''}" data-a="pick" data-cid="${v.cid}" data-uid="${v.uid || ''}">✓</div>` : ''}
    <div class="shot">
      ${shot(v.id)}
      <div class="tl"><span class="classdot" title="${h(v.c)}">${icon(v.c) || '<b style="font-size:10px">' + h(v.c[0]) + '</b>'}</span></div>
      ${!ui.pickMode && rank ? `<div class="tr"><span class="tag solid rank" style="background:${rank.color}"
          title="${h(((listById(U.prefs.refList)||{}).name||'') + ': ' + rank.label)}">${h(rank.label)}</span></div>` : ''}
      <div class="bl">
        <div class="nm">${h(v.uid ? v.sub : v.name)}</div>
        ${v.uid ? `<div class="of">${h(v.name)}</div>` : ''}
      </div>
    </div>
    <div class="cbody">
      <div class="row" style="gap:5px">
        ${tagSolid(v.t, tierColor(v.t))}${transTag(v.trans)}
        ${v.nuevo ? tagSolid('NUEVO', 'var(--gold)') : ''}
        ${insTag(v.ins)}
      </div>
      <div class="rolebar" title="${h(v.r.join(' · '))}">${SEED.ROLES.map(r => `<span style="background:${v.r.includes(r) ? roleColor(r) : 'var(--line)'}"></span>`).join('')}</div>
      <div class="muted" style="font-size:11.5px">${h(v.f)} · ${v.skills.length} skills</div>
    </div>
  </div>`;
}

function tableHtml (rows) {
  const cols = [['name','Personaje'],['c','Clase'],['t','Tier'],['f','Bando'],['ins','Instinto'],['r','Roles'],['striker','Striker'],['wba','World Boss'],['skills','Skills'],['rank','Lista']];
  return `<div class="tablewrap"><table class="dt"><thead><tr>${cols.map(c => `<th>${h(c[1])}</th>`).join('')}</tr></thead><tbody>
    ${rows.map(v => {
      const rank = rankLabel(v.key);
      const u = imgUrl('portrait-' + v.id);
      return `<tr data-a="open" data-cid="${v.cid}" data-uid="${v.uid || ''}">
        <td><div class="cellname">${u ? `<img class="thumb" src="${u}" alt="" loading="lazy">` : '<span class="thumb"></span>'}
          <div><div style="font-weight:600">${h(v.uid ? v.sub : v.name)}</div>${v.uid ? `<div class="muted" style="font-size:11.5px">${h(v.name)}</div>` : '<div class="muted" style="font-size:11.5px">Base</div>'}</div></div></td>
        <td>${tagGhost(v.c, classColor(v.c))}</td>
        <td style="white-space:nowrap">${tagSolid(v.t, tierColor(v.t))}${transTag(v.trans)}</td>
        <td class="muted">${h(v.f)}</td>
        <td class="muted">${h(v.ins === 'Desconocido' ? '—' : v.ins)}</td>
        <td>${v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}">${h(r)}</span>`).join(' ')}</td>
        <td class="mono">${v.striker != null ? h(v.striker) : '—'}</td>
        <td class="muted">${h(v.wba || '—')}</td>
        <td class="mono">${v.skills.length}</td>
        <td>${rank ? `<span class="tag solid" style="background:${rank.color}">${h(rank.label)}</span>` : '<span class="muted">—</span>'}</td>
      </tr>`;
    }).join('')}
  </tbody></table></div>`;
}

function renderRoster () {
  const rows = rosterData();
  const total = allVariants().length;
  const PAGE = U.prefs.view === 'table' ? 60 : 36;
  const pages = Math.max(1, Math.ceil(rows.length / PAGE));
  ui.page = Math.min(Math.max(0, ui.page), pages - 1);
  const slice = rows.slice(ui.page * PAGE, (ui.page + 1) * PAGE);
  const body = rows.length === 0
    ? `<div class="empty"><div class="big">∅</div><div>Ningún personaje o uniforme coincide con estos filtros.</div>
       <button class="btn sm" style="margin-top:12px" data-a="clearFilters">Limpiar filtros</button></div>`
    : U.prefs.view === 'table' ? tableHtml(slice)
    : `<div class="grid ${U.prefs.view === 'dense' ? 'dense' : ''}">${slice.map(cardHtml).join('')}</div>`;
  return toolbar(total, rows.length) + body + pager(pages) +
    (ui.pickMode && ui.picks.length >= 2
      ? `<div style="position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:center;padding:16px;
           background:linear-gradient(to top,var(--bg) 62%,transparent);z-index:50">
           <button class="btn primary" data-a="goCompare">Comparar ${ui.picks.length} →</button></div>` : '');
}
function pager (pages) {
  if (pages <= 1) return '';
  const cur = ui.page;
  const nums = [];
  for (let i = 0; i < pages; i++) {
    if (i < 2 || i > pages - 3 || Math.abs(i - cur) <= 1) nums.push(i);
    else if (nums[nums.length - 1] !== '…') nums.push('…');
  }
  return `<div class="row" style="justify-content:center;margin-top:22px">
    <button class="btn sm" data-a="page" data-p="${Math.max(0, cur - 1)}" ${cur === 0 ? 'disabled' : ''}>←</button>
    ${nums.map(n => n === '…' ? '<span class="muted">…</span>' : `<button class="btn sm ${n === cur ? 'primary' : ''}" data-a="page" data-p="${n}">${n + 1}</button>`).join('')}
    <button class="btn sm" data-a="page" data-p="${Math.min(pages - 1, cur + 1)}" ${cur === pages - 1 ? 'disabled' : ''}>→</button>
  </div>`;
}

// ============================================================================
// FICHA
// ============================================================================
const STAT_ES = { recovery_rate:'Recuperación', fire_resist:'Res. fuego', cold_resist:'Res. frío',
                  lightning_resist:'Res. rayo', poison_resist:'Res. veneno', mind_resist:'Res. mental' };
function renderDetail () {
  const ch = CHAR_BY_ID[ui.charId];
  if (!ch) { ui.view = 'roster'; return renderRoster(); }
  const v = variant(ch.id, ui.uniformId);
  const rank = rankLabel(v.key);
  const stats = Object.entries(ch.stats || {}).filter(([, val]) => parseFloat(val) !== 0);
  const teams = U.teams.filter(t => t.members.some(k => k.split('::')[0] === ch.id));
  const byslot = {}; v.skills.forEach(sk => { (byslot[sk.slot] = byslot[sk.slot] || []).push(sk); });
  const ordered = SLOT_ORDER.filter(s => byslot[s]);
  const extra = Object.keys(byslot).filter(s => !SLOT_ORDER.includes(s));
  const box = (k, val) => `<div class="stat"><div class="k">${h(k)}</div><div class="v">${val}</div></div>`;

  return `
  <div class="row" style="margin-bottom:14px">
    <button class="btn sm" data-a="back">← Roster</button>
    <button class="btn sm" data-a="pickThis" data-cid="${ch.id}" data-uid="${v.uid || ''}">+ Comparar esta versión</button>
    <button class="btn sm" data-a="edit" data-cid="${ch.id}">Editar</button>
  </div>
  <div class="hero">
    <div class="glow" style="background:radial-gradient(60% 120% at 12% 0%, ${classColor(v.c)}22, transparent 70%)"></div>
    <div class="inner">
      <div class="face">${shot(v.id)}</div>
      <div class="meta">
        <h1>${h(ch.name)}</h1>
        ${rank ? `<div class="row"><span class="muted">${h((listById(U.prefs.refList) || {}).name || '')}:</span>
          <span class="tag solid" style="background:${rank.color}">${h(rank.label)}</span></div>` : ''}
        <div class="row">
          ${tagGhost(v.c, classColor(v.c))}
          ${tagSolid(v.t, tierColor(v.t))}${v.trans ? tagSolid('TRASCENDIDO', 'var(--gold)') : ''}
          <span class="tag dim">${h(v.f)}</span>
          ${insTag(v.ins)}
          ${v.nuevo ? tagSolid('NUEVO','var(--gold)') : ''}
          ${v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}">${h(r)}</span>`).join('')}
        </div>
        <div class="statgrid">
          ${box('Uniforme actual', h(v.uid ? v.sub : 'Base'))}
          ${box('Raza', icon(ch.race) + h(ch.race || '—'))}
          ${box('Género', icon(ch.gender) + h(ch.gender || '—'))}
          ${box('Origen', h(ch.origin || '—'))}
          ${box('Striker', v.striker != null ? 'Skill ' + h(v.striker) : '—')}
          ${box('World Boss', icon(v.wba) + h(v.wba || '—'))}
          ${v.cost ? box('Costo del uniforme', h(v.cost)) : ''}
          ${box('Uniformes', h(String(ch.uniforms.length)))}
          ${stats.map(([k, val]) => box(STAT_ES[k] || k, h(val))).join('')}
        </div>
        <div class="row">
          <span class="muted">Habilidades:</span>
          ${(v.ab || []).map(a => `<span class="tag dim">${icon(a)}${h(a)}</span>`).join('') || '<span class="muted">—</span>'}
        </div>
        ${(ch.tuc || []).length ? `<div class="row"><span class="muted">Cartas TUC:</span>${ch.tuc.map(t => `<span class="tag dim">${h(t)}</span>`).join('')}</div>` : ''}
      </div>
    </div>
  </div>

  <div class="section">
    <h3>Uniformes · ${pluralUni(ch.uniforms.length)}</h3>
    <div class="unitabs">
      <button class="unitab ${v.uid ? '' : 'on'}" data-a="uniform" data-uid="base">
        ${imgUrl('portrait-' + ch.id) ? `<img src="${imgUrl('portrait-' + ch.id)}" alt="">` : ''}Base</button>
      ${ch.uniforms.map(u => `<button class="unitab ${v.uid === u.id ? 'on' : ''}" data-a="uniform" data-uid="${u.id}">
        ${imgUrl('portrait-' + u.id) ? `<img src="${imgUrl('portrait-' + u.id)}" alt="">` : ''}${h(u.name)}
        <span class="tag solid" style="background:${tierColor(u.tier)};font-size:9px">${h(u.tier)}</span></button>`).join('')}
    </div>
    <p class="muted" style="margin-bottom:12px">Se muestran las skills de la base más las propias del uniforme elegido.
      ${v.uid && (findUniform(ch, v.uid) || {}).skills.length === 0 ? '<b>Este uniforme no tiene skills propias en la wiki.</b>' : ''}</p>
    ${v.skills.length
      ? ordered.concat(extra).map(slot => byslot[slot].map(skillCard).join('')).join('')
      : `<div class="empty"><div class="big">?</div><div>La wiki no publica skills para este personaje todavía.</div></div>`}
  </div>

  ${teams.length ? `<div class="section"><h3>Equipos donde aparece</h3><div class="grid">
    ${teams.map(t => `<div class="card"><div style="font-weight:600">${h(t.name)}</div>
      <div class="muted">${t.members.map(k => { const r = variant(...k.split('::')); return r ? fullLabel(r) : k; }).join(' + ')}</div>
      <p class="muted" style="margin-top:6px">${h(t.reason)}</p></div>`).join('')}
  </div></div>` : ''}

  <div class="section"><h3>Retratos propios</h3>
    <p class="muted" style="margin-bottom:10px">Si subís una imagen reemplaza la de thanosvibs solo en este navegador.</p>
    <div class="row">
      <label class="btn sm" style="cursor:pointer">Subir retrato<input type="file" accept="image/*" hidden data-a="upload" data-img="portrait-${v.id}"></label>
      ${U.images['portrait-' + v.id] ? `<button class="btn sm danger" data-a="clearImg" data-img="portrait-${v.id}">Volver al original</button>` : ''}
    </div>
  </div>`;
}

// ============================================================================
// COMPARACIÓN
// ============================================================================
function renderCompare () {
  const vs = ui.picks.map(p => variant(p.cid, p.uid)).filter(Boolean);
  if (vs.length < 2) { ui.view = 'roster'; return renderRoster(); }
  const same = (get) => { const m = {}; vs.forEach(v => { const k = get(v); m[k] = (m[k] || 0) + 1; }); return m; };
  const cC = same(v => v.c), cF = same(v => v.f), cT = same(v => v.t), cI = same(v => v.ins);
  const slots = SLOT_ORDER.filter(s => vs.some(v => v.skills.some(sk => sk.slot === s)));
  const syn = synergy(vs);
  const cell = (v, txt, counts, key) => `<td class="${counts && counts[key] > 1 ? 'same' : ''}">${txt}</td>`;
  const attr = (label, fn) => `<tr><th>${h(label)}</th>${vs.map(v => `<td>${fn(v)}</td>`).join('')}</tr>`;

  return `
  <div class="row" style="margin-bottom:14px"><button class="btn sm" data-a="back">← Roster</button></div>
  <div class="page-head"><div><h1>Comparativa</h1>
    <div class="sub">Las celdas resaltadas marcan coincidencias entre las columnas.</div></div></div>
  <div class="cmp"><table class="cmpt">
    <thead><tr><th></th>${vs.map(v => `<th><div class="cmphead">
      ${imgUrl('portrait-' + v.id) ? `<img src="${imgUrl('portrait-' + v.id)}" alt="">` : ''}
      <div><div style="font-weight:700;font-size:14px">${h(v.uid ? v.sub : v.name)}</div>
      <div class="muted">${h(v.uid ? v.name : 'Base')}</div></div>
      <button class="btn sm danger" data-a="unpick" data-cid="${v.cid}" data-uid="${v.uid || ''}">Quitar</button>
    </div></th>`).join('')}</tr></thead>
    <tbody>
      <tr><th>Clase</th>${vs.map(v => cell(v, tagGhost(v.c, classColor(v.c)), cC, v.c)).join('')}</tr>
      <tr><th>Tier</th>${vs.map(v => cell(v, tagSolid(v.t, tierColor(v.t)) + transTag(v.trans), cT, v.t)).join('')}</tr>
      <tr><th>Bando</th>${vs.map(v => cell(v, h(v.f), cF, v.f)).join('')}</tr>
      <tr><th>Instinto</th>${vs.map(v => cell(v, h(v.ins === 'Desconocido' ? '—' : v.ins), cI, v.ins)).join('')}</tr>
      ${attr('Roles', v => v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}">${h(r)}</span>`).join(' '))}
      ${attr('Striker', v => v.striker != null ? 'Skill ' + h(v.striker) : '—')}
      ${attr('World Boss', v => icon(v.wba) + h(v.wba || '—'))}
      ${attr('Habilidades', v => (v.ab || []).map(a => `<span class="tag dim">${h(a)}</span>`).join(' ') || '—')}
      ${attr('Costo', v => h(v.cost || '—'))}
      ${LISTS.filter(l => Object.keys(assignOf(l.id)).length).map(l => {
        const a = assignOf(l.id), rows = rowsOf(l);
        return `<tr><th>${h(l.name)}</th>${vs.map(v => {
          const i = rows.findIndex(x => x.id === a[v.key]);
          return `<td>${i === -1 ? '<span class="muted">sin ubicar</span>' : `<span class="tag solid" style="background:${rowColor(i, rows.length)}">${h(rows[i].label)}</span>`}</td>`;
        }).join('')}</tr>`;
      }).join('')}
      ${slots.map(slot => `<tr class="slotrow"><th>${h(slot)}</th>${vs.map(v => {
        const sk = v.skills.find(s => s.slot === slot);
        if (!sk) return `<td><span class="muted">— no tiene —</span></td>`;
        return `<td><div style="font-weight:600;margin-bottom:4px">${h(sk.n)}</div>
          ${sk.dmg !== 'Ninguno' ? tagGhost(sk.dmg, dmgColor(sk.dmg)) : ''}
          <span class="tag dim">${h(window.MFF_skillTiming(sk))}</span>
          <div style="margin-top:6px">${skillFx(sk)}</div></td>`;
      }).join('')}</tr>`).join('')}
    </tbody>
  </table></div>
  <div class="card" style="margin-top:18px">
    <div class="row" style="justify-content:space-between;margin-bottom:8px">
      <h3 style="margin:0">Sinergia estimada</h3><span class="muted">${syn.score} pts</span></div>
    <div style="height:5px;background:var(--surface-3);border-radius:3px;overflow:hidden;margin-bottom:10px">
      <div style="height:100%;width:${Math.min(100, syn.score * 12)}%;background:linear-gradient(90deg,var(--accent),var(--gold))"></div></div>
    ${syn.reasons.length ? `<ul style="margin:0;padding-left:18px">${syn.reasons.map(r => `<li>${h(r)}</li>`).join('')}</ul>`
      : '<p class="muted">Sin señales fuertes de sinergia en esta selección.</p>'}
    <p class="muted" style="margin-top:10px">Heurística propia (bando, cobertura de roles y ventaja de clase), no un cálculo del juego.</p>
  </div>`;
}

// ============================================================================
// TIER LISTS
// ============================================================================
function renderTierList () {
  const list = listById(ui.tierList) || LISTS[0];
  if (!list) return `<div class="empty">No hay tier lists cargadas.</div>`;
  ui.tierList = list.id;
  const rows = rowsOf(list), a = assignOf(list.id);
  const vs = allVariants();
  const byRow = {}; rows.forEach(r => { byRow[r.id] = []; });
  const unset = [];
  vs.forEach(v => { const r = a[v.key]; if (r && byRow[r]) byRow[r].push(v); else unset.push(v); });
  const imported = TIERLISTS_SEED.some(l => l.id === list.id);
  const chip = (v) => `<span class="tlchip" draggable="true" data-a="drag" data-key="${v.key}" title="${h(fullLabel(v))}">
      ${imgUrl('portrait-' + v.id) ? `<img src="${imgUrl('portrait-' + v.id)}" alt="" loading="lazy">` : ''}
      <span class="who">${h(v.name)}</span>${v.uid ? `<span class="what">${h(v.sub)}</span>` : ''}
      <span class="x" data-a="unassign" data-key="${v.key}">✕</span></span>`;

  return `
  <div class="page-head"><div><h1>Tier lists</h1>
    <div class="sub">Cada lista importada conserva las filas y los rótulos que le puso su autor. No son rangos S–D.</div></div>
    <div class="row">
      <input placeholder="Nombre de una lista nueva" value="${h(ui.newListName)}" data-a="newListName" style="width:220px">
      <button class="btn" data-a="addList">+ Crear lista</button>
    </div>
  </div>
  <div class="tlbar">${LISTS.map(l => `<button class="chip ${l.id === list.id ? 'on' : ''}" data-a="pickList" data-id="${l.id}">${h(l.name)}</button>`).join('')}</div>
  <div class="tlsource">
    ${imported
      ? `<span>Fuente: <a href="https://thanosvibs.money" target="_blank" rel="noopener">THANO$VIB$</a> · «${h(list.source)}»</span>
         ${list.author ? `<span class="tag dim">autor: ${h(list.author)}</span>` : ''}
         ${list.gameVersion ? `<span class="tag dim">juego ${h(list.gameVersion)}</span>` : ''}
         <span class="tag dim">${Object.keys(a).length} ubicados</span>`
      : `<span>Lista propia</span><span class="tag dim">${Object.keys(a).length} ubicados</span>
         <button class="btn sm danger" data-a="removeList" data-id="${list.id}">Borrar lista</button>`}
    ${U.assign[list.id] && Object.keys(U.assign[list.id]).length
      ? `<button class="btn sm" data-a="resetList" data-id="${list.id}">Deshacer mis cambios (${Object.keys(U.assign[list.id]).length})</button>` : ''}
  </div>
  ${rows.map((r, i) => `<div class="tierrow" data-a="drop" data-row="${h(r.id)}">
    <div class="tierlabel" style="background:${rowColor(i, rows.length)}">${h(r.label)}</div>
    <div class="tieritems">${byRow[r.id].map(chip).join('') || '<span class="muted" style="align-self:center">Arrastrá acá</span>'}</div>
  </div>`).join('')}
  <div style="margin-top:18px">
    <div class="row">
      <button class="btn sm" data-a="togglePool">${ui.poolOpen ? 'Ocultar' : 'Mostrar'} sin ubicar (${unset.length})</button>
      ${ui.poolOpen ? `<input placeholder="Filtrar…" value="${h(ui.poolSearch)}" data-a="poolSearch" style="width:220px">` : ''}
    </div>
    ${ui.poolOpen ? (() => {
      const q2 = ui.poolSearch.trim().toLowerCase();
      const pool = (q2 ? unset.filter(v => fullLabel(v).toLowerCase().includes(q2)) : unset);
      return `<div class="tieritems" data-a="drop" data-row="" style="margin-top:10px;max-height:360px;overflow-y:auto;
        border:1px dashed var(--line-2);border-radius:var(--r-md)">
        ${pool.slice(0, 150).map(chip).join('') || '<span class="muted">Nada coincide.</span>'}
        ${pool.length > 150 ? `<span class="muted" style="align-self:center">…y ${pool.length - 150} más: filtrá para acotar.</span>` : ''}
      </div>`;
    })() : ''}
  </div>`;
}

// ============================================================================
// EQUIPOS
// ============================================================================
function renderTeams () {
  const t = ui.team;
  const mode = U.modes.find(m => m.id === t.modeId);
  const max = mode ? mode.teamSize : 3;
  const q = ui.teamSearch.trim().toLowerCase();
  const pool = allVariants().filter(v => !q || fullLabel(v).toLowerCase().includes(q)).sort((a, b) => rankIndex(a.key) - rankIndex(b.key));
  const PS = 40, pages = Math.max(1, Math.ceil(pool.length / PS));
  ui.teamPage = Math.min(ui.teamPage, pages - 1);
  const slice = pool.slice(ui.teamPage * PS, (ui.teamPage + 1) * PS);
  return `
  <div class="page-head"><div><h1>Equipos</h1>
    <div class="sub">Los que armás vos, con la sinergia estimada por la app.</div></div>
    <button class="btn primary" data-a="teamOpen">+ Armar equipo</button></div>
  ${ui.teamOpen ? `<div class="card" style="margin-bottom:20px">
    <div class="row" style="margin-bottom:10px">
      <input placeholder="Nombre del equipo" value="${h(t.name)}" data-a="teamName" style="flex:2;min-width:180px">
      <select data-a="teamMode" style="flex:1;min-width:160px">
        <option value="">Sin modo (3)</option>
        ${U.modes.map(m => `<option value="${m.id}" ${m.id === t.modeId ? 'selected' : ''}>${h(m.name)} (${m.teamSize})</option>`).join('')}
      </select>
    </div>
    <div class="muted" style="margin-bottom:6px">Miembros ${t.members.length} / ${max} — ordenados por ${h((listById(U.prefs.refList) || {}).name || 'nombre')}</div>
    <input placeholder="Buscar…" value="${h(ui.teamSearch)}" data-a="teamSearch" style="width:100%;margin-bottom:10px">
    <div class="row" style="gap:6px">
      ${slice.map(v => `<div title="${h(fullLabel(v))}" data-a="teamToggle" data-key="${v.key}"
        style="width:50px;height:50px;border-radius:9px;overflow:hidden;cursor:pointer;flex:none;
        box-shadow:0 0 0 ${t.members.includes(v.key) ? '2px var(--accent)' : '1px var(--line-2)'}">
        ${imgUrl('portrait-' + v.id) ? `<img src="${imgUrl('portrait-' + v.id)}" style="width:100%;height:100%;object-fit:cover" loading="lazy">` : ''}
      </div>`).join('')}
    </div>
    ${pages > 1 ? `<div class="row" style="margin-top:10px">${Array.from({length: Math.min(pages, 12)}, (_, i) => `<button class="btn sm ${i === ui.teamPage ? 'primary' : ''}" data-a="teamPage" data-p="${i}">${i + 1}</button>`).join('')}</div>` : ''}
    <textarea placeholder="Por qué funciona (opcional)" style="width:100%;margin-top:10px;min-height:54px" data-a="teamReason">${h(t.reason)}</textarea>
    <div class="row" style="justify-content:flex-end;margin-top:10px">
      <button class="btn" data-a="teamClose">Cancelar</button>
      <button class="btn primary" data-a="teamSave" ${t.members.length < 2 ? 'disabled' : ''}>Guardar</button>
    </div>
  </div>` : ''}
  ${U.teams.length ? `<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr))">
    ${U.teams.map(tt => {
      const vs = tt.members.map(k => variant(...k.split('::'))).filter(Boolean);
      const s = synergy(vs);
      return `<div class="card" style="position:relative">
        <button class="btn sm danger" data-a="teamRemove" data-id="${tt.id}" style="position:absolute;top:10px;right:10px">✕</button>
        <div style="font-weight:600;padding-right:34px;margin-bottom:8px">${h(tt.name)}</div>
        <div class="row" style="gap:5px;margin-bottom:8px">${vs.map(v => imgUrl('portrait-' + v.id)
          ? `<img src="${imgUrl('portrait-' + v.id)}" title="${h(fullLabel(v))}" style="width:44px;height:44px;border-radius:8px;object-fit:cover">` : '').join('')}</div>
        <div class="muted">${vs.map(fullLabel).join(' + ')}</div>
        ${tt.reason ? `<p class="muted" style="margin-top:6px">${h(tt.reason)}</p>` : ''}
        <div class="muted" style="margin-top:6px">${s.score} pts de sinergia</div>
      </div>`;
    }).join('')}</div>`
  : `<div class="empty"><div class="big">◇</div><div>Todavía no armaste ningún equipo.</div></div>`}`;
}

// ============================================================================
// EDITOR DE PERSONAJES (capa de usuario)
// ============================================================================
function blankDraft () {
  return { name:'', c:'Combate', f:SEED.FACTIONS[0], r:[], t:'T2', ins:SEED.INSTINCTS[0], race:SEED.RACES[0],
           gender:SEED.GENDERS[0], origin:'Original MFF', abilities:[], tuc:[], stats:{}, striker:4, wba:'',
           trans:false, new:false, baseSkills:[], uniforms:[] };
}
function renderEditor () {
  const d = ui.edDraft, steps = ['Datos','Uniformes','Revisar'];
  const pick = (opts, field, multi) => opts.map(v => {
    const on = multi ? d[field].includes(v) : d[field] === v;
    return `<button class="chip ${on ? 'on' : ''}" data-a="edPick" data-f="${field}" data-v="${h(v)}" data-multi="${multi ? 1 : 0}">${icon(v)}${h(v)}</button>`;
  }).join('');
  const field = (label, inner) => `<div style="margin-bottom:12px"><div class="lbl" style="font-size:10px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-3);margin-bottom:6px;font-weight:700">${h(label)}</div>${inner}</div>`;
  let body = '';
  if (ui.edStep === 0) {
    body = field('Nombre', `<input style="width:100%;max-width:420px" data-a="edField" data-f="name" value="${h(d.name)}">`)
      + field('Clase', `<div class="row">${pick(SEED.CLASSES, 'c', false)}</div>`)
      + field('Bando', `<div class="row">${pick(SEED.FACTIONS, 'f', false)}</div>`)
      + field('Tier', `<div class="row">${pick(SEED.TIERS, 't', false)}</div>`)
      + field('Instinto', `<div class="row">${pick(SEED.INSTINCTS, 'ins', false)}</div>`)
      + field('Raza', `<div class="row">${pick(SEED.RACES, 'race', false)}</div>`)
      + field('Género', `<div class="row">${pick(SEED.GENDERS, 'gender', false)}</div>`)
      + field('Roles', `<div class="row">${pick(SEED.ROLES, 'r', true)}</div>`)
      + field('Habilidades', `<div class="row">${pick(SEED.SKILL_TAGS, 'abilities', true)}</div>`)
      + field('Striker (número de skill)', `<input type="number" min="1" max="6" style="width:90px" data-a="edField" data-f="striker" value="${h(d.striker)}">`);
  } else if (ui.edStep === 1) {
    body = d.uniforms.map((u, i) => `<div class="card" style="margin-bottom:12px">
      <div class="row">
        <input placeholder="Nombre del uniforme" style="flex:2;min-width:180px" data-a="edUni" data-i="${i}" data-f="name" value="${h(u.name)}">
        <select data-a="edUni" data-i="${i}" data-f="tier">${SEED.TIERS.map(t => `<option ${t === u.tier ? 'selected' : ''}>${t}</option>`).join('')}</select>
        <input placeholder="Costo" style="flex:1;min-width:120px" data-a="edUni" data-i="${i}" data-f="cost" value="${h(u.cost || '')}">
        <button class="btn sm danger" data-a="edUniDel" data-i="${i}">✕</button>
      </div>
      ${u.skills.map((sk, si) => `<div class="card" style="margin-top:8px;background:var(--surface-2)">
        <div class="row">
          <select data-a="edSk" data-i="${i}" data-s="${si}" data-f="slot">${SLOT_ORDER.map(s => `<option ${s === sk.slot ? 'selected' : ''}>${s}</option>`).join('')}</select>
          <select data-a="edSk" data-i="${i}" data-s="${si}" data-f="dmg">${SEED.DAMAGE_TYPES.map(s => `<option ${s === sk.dmg ? 'selected' : ''}>${s}</option>`).join('')}</select>
          <input placeholder="Nombre" style="flex:1;min-width:150px" data-a="edSk" data-i="${i}" data-s="${si}" data-f="n" value="${h(sk.n)}">
          <button class="btn sm danger" data-a="edSkDel" data-i="${i}" data-s="${si}">✕</button>
        </div>
        <textarea placeholder="Descripción" style="width:100%;margin-top:6px" data-a="edSk" data-i="${i}" data-s="${si}" data-f="d">${h(sk.d)}</textarea>
      </div>`).join('')}
      <button class="btn sm" style="margin-top:8px" data-a="edSkAdd" data-i="${i}">+ Skill</button>
    </div>`).join('') + `<button class="btn" data-a="edUniAdd">+ Agregar uniforme</button>`;
  } else {
    body = `<div class="card"><div style="font-weight:700;font-size:17px">${h(d.name || 'Sin nombre')}</div>
      <div class="muted">${[d.c, d.f, d.t, d.ins, d.r.join('/')].filter(Boolean).join(' · ')}</div>
      <div class="muted">${pluralUni(d.uniforms.length)} · ${d.uniforms.reduce((n, u) => n + u.skills.length, 0)} skills propias</div></div>`;
  }
  return `<div class="page-head"><div><h1>${ui.edId ? 'Editar personaje' : 'Nuevo personaje'}</h1>
    <div class="sub">Se guarda en tu navegador, aparte de data.js. Regenerar los datos no lo pisa.</div></div></div>
  <div class="row" style="margin-bottom:18px">${steps.map((s, i) => `<button class="chip ${i === ui.edStep ? 'on' : ''}" data-a="edStep" data-i="${i}">${i + 1}. ${s}</button>`).join('')}</div>
  ${body}
  <div class="row" style="justify-content:space-between;margin-top:22px">
    <button class="btn" data-a="edPrev" ${ui.edStep === 0 ? 'disabled' : ''}>Atrás</button>
    <div class="row">
      ${ui.edId && U.charEdits[ui.edId] ? `<button class="btn danger" data-a="edRevert">Descartar mi edición</button>` : ''}
      ${ui.edStep === 2 ? `<button class="btn primary" data-a="edSave">Guardar</button>` : `<button class="btn primary" data-a="edNext">Siguiente</button>`}
    </div>
  </div>`;
}

// ============================================================================
// AJUSTES
// ============================================================================
function renderSettings () {
  const mine = Object.keys(U.charEdits).length + U.charNew.length;
  const changed = Object.values(U.assign).reduce((n, o) => n + Object.keys(o).length, 0);
  return `<div class="page-head"><div><h1>Ajustes</h1>
    <div class="sub">Los datos del juego salen de data.js y no se guardan acá. Esto es solo lo tuyo.</div></div></div>

  <div class="section"><h3>Tu capa guardada</h3>
    <div class="statgrid">
      <div class="stat"><div class="k">Personajes propios o editados</div><div class="v">${mine}</div></div>
      <div class="stat"><div class="k">Equipos</div><div class="v">${U.teams.length}</div></div>
      <div class="stat"><div class="k">Tier lists propias</div><div class="v">${U.lists.length}</div></div>
      <div class="stat"><div class="k">Cambios sobre listas importadas</div><div class="v">${changed}</div></div>
      <div class="stat"><div class="k">Imágenes subidas</div><div class="v">${Object.keys(U.images).length}</div></div>
    </div>
    <div class="row" style="margin-top:12px">
      <button class="btn" data-a="exportUser">Exportar mi capa (JSON)</button>
      <label class="btn" style="cursor:pointer">Importar<input type="file" accept=".json" hidden data-a="importUser"></label>
      <button class="btn" data-a="exportCsv">Exportar roster (CSV)</button>
      <button class="btn danger" data-a="resetUser">Borrar todo lo mío</button>
    </div>
  </div>

  <div class="section"><h3>Marca</h3>
    <div style="width:200px;height:52px;border-radius:var(--r-sm);overflow:hidden;background:var(--surface-2);display:flex;align-items:center;justify-content:center">
      ${U.images['brand-logo'] ? `<img src="${U.images['brand-logo']}" style="max-width:100%;max-height:100%">` : '<span class="muted">Sin logo</span>'}
    </div>
    <div class="row" style="margin-top:10px">
      <label class="btn sm" style="cursor:pointer">Subir logo<input type="file" accept="image/*" hidden data-a="upload" data-img="brand-logo"></label>
      ${U.images['brand-logo'] ? `<button class="btn sm danger" data-a="clearImg" data-img="brand-logo">Quitar</button>` : ''}
    </div>
  </div>

  <div class="section"><h3>Modos de juego (tamaño de equipo)</h3>
    <div style="display:flex;flex-direction:column;gap:8px;max-width:520px">
      ${U.modes.map((m, i) => `<div class="row">
        <input value="${h(m.name)}" data-a="modeName" data-i="${i}" style="flex:1">
        <input type="number" min="1" max="8" value="${m.teamSize}" data-a="modeSize" data-i="${i}" style="width:80px">
        <button class="btn sm danger" data-a="modeDel" data-i="${i}">✕</button>
      </div>`).join('')}
    </div>
    <button class="btn sm" style="margin-top:10px" data-a="modeAdd">+ Agregar modo</button>
  </div>

  <div class="section"><h3>Fuentes</h3>
    <p class="muted">Personajes, uniformes, retratos, íconos y tier lists: <a href="https://thanosvibs.money" target="_blank" rel="noopener">THANO$VIB$</a>.
      Skills e instintos: <a href="https://future-fight.fandom.com" target="_blank" rel="noopener">Future Fight Wiki</a>.
      Uso personal, sin fin comercial.</p>
  </div>`;
}

// ============================================================================
// NAV + DISPATCH
// ============================================================================
function renderNav () {
  const link = (view, label, act) => `<button class="navlink ${ui.view === view ? 'on' : ''}" data-a="${act}">${label}</button>`;
  return `<nav class="topnav">
    <span class="brand" data-a="back">${U.images['brand-logo']
      ? `<img src="${U.images['brand-logo']}" style="height:26px">`
      : `<span class="dot"></span>COMPARADOR <span style="color:var(--accent)">MFF</span>`}</span>
    ${link('roster','Roster','back')}
    ${link('tierlist','Tier lists','goTier')}
    ${link('teams','Equipos','goTeams')}
    <span class="navspace"></span>
    <div class="navtools">
      ${link('editor','+ Personaje','goEditor')}
      ${link('settings','Ajustes','goSettings')}
    </div>
  </nav>`;
}
function render () {
  let body;
  switch (ui.view) {
    case 'detail':   body = renderDetail(); break;
    case 'compare':  body = renderCompare(); break;
    case 'tierlist': body = renderTierList(); break;
    case 'teams':    body = renderTeams(); break;
    case 'editor':   body = renderEditor(); break;
    case 'settings': body = renderSettings(); break;
    default:         body = renderRoster();
  }
  $('#app').innerHTML = renderNav() + '<main>' + body + '</main>';
  const q = $('#q');
  if (q && ui.focusSearch) { q.focus(); q.setSelectionRange(q.value.length, q.value.length); }
}

// ============================================================================
// EVENTOS
// ============================================================================
document.addEventListener('click', (e) => {
  const el = e.target.closest('[data-a]'); if (!el) return;
  const a = el.getAttribute('data-a'), d = el.dataset;
  const P = U.prefs;
  switch (a) {
    case 'back': ui.view = 'roster'; ui.charId = null; ui.focusSearch = false; render(); break;
    case 'toggleFilters': P.filtersOpen = !P.filtersOpen; commit(); break;
    case 'clearFilters': P.filters = { c:[], r:[], t:[], f:[], ins:[], race:[], origin:[], ab:[] };
      P.flags = { t4:false, trans:false, nuevo:false }; P.kind = 'todo'; ui.search = ''; ui.page = 0; commit(); break;
    case 'filter': { const cur = P.filters[d.cat];
      P.filters[d.cat] = cur.includes(d.v) ? cur.filter(x => x !== d.v) : cur.concat(d.v);
      ui.page = 0; commit(); break; }
    case 'flag': P.flags[d.v] = !P.flags[d.v]; ui.page = 0; commit(); break;
    case 'view': P.view = d.v; ui.page = 0; commit(); break;
    case 'kind': P.kind = d.v; ui.page = 0; commit(); break;
    case 'dir': P.dir = -P.dir; commit(); break;
    case 'page': ui.page = parseInt(d.p, 10); render(); window.scrollTo({top:0,behavior:'smooth'}); break;
    case 'pickMode': ui.pickMode = !ui.pickMode; ui.picks = []; ui.view = 'roster'; render(); break;
    case 'pick': case 'pickThis': {
      e.stopPropagation();
      togglePick(d.cid, d.uid || null);
      if (a === 'pickThis') { ui.pickMode = true; ui.view = 'roster'; }
      render(); break; }
    case 'unpick': { const key = d.cid + '::' + (d.uid || 'base');
      ui.picks = ui.picks.filter(p => p.key !== key);
      if (ui.picks.length < 2) ui.view = 'roster';
      render(); break; }
    case 'goCompare': ui.view = 'compare'; render(); window.scrollTo(0, 0); break;
    case 'open': {
      if (ui.pickMode) { togglePick(d.cid, d.uid || null); render(); break; }
      ui.view = 'detail'; ui.charId = d.cid; ui.uniformId = d.uid || 'base'; render(); window.scrollTo(0, 0); break; }
    case 'uniform': ui.uniformId = d.uid; render(); break;

    case 'goTier': ui.view = 'tierlist'; render(); break;
    case 'pickList': ui.tierList = d.id; render(); break;
    case 'addList': { const name = ui.newListName.trim(); if (!name) break;
      const id = 'mia-' + Date.now();
      U.lists.push({ id, name, rows: DEFAULT_ROWS.slice() }); ui.newListName = ''; ui.tierList = id; commit(); break; }
    case 'removeList': { if (!confirm('¿Borrar esta lista y sus asignaciones?')) break;
      U.lists = U.lists.filter(l => l.id !== d.id); delete U.assign[d.id];
      ui.tierList = (LISTS[0] || {}).id || ''; commit(); break; }
    case 'resetList': delete U.assign[d.id]; commit(); break;
    case 'togglePool': ui.poolOpen = !ui.poolOpen; render(); break;
    case 'unassign': e.stopPropagation(); setAssign(ui.tierList, d.key, REMOVED); break;

    case 'goTeams': ui.view = 'teams'; render(); break;
    case 'teamOpen': ui.teamOpen = true; ui.team = { name:'', members:[], reason:'', modeId:'' }; ui.teamSearch = ''; ui.teamPage = 0; render(); break;
    case 'teamClose': ui.teamOpen = false; render(); break;
    case 'teamToggle': { const t = ui.team, mode = U.modes.find(m => m.id === t.modeId), max = mode ? mode.teamSize : 3;
      const i = t.members.indexOf(d.key);
      if (i > -1) t.members.splice(i, 1); else { t.members.push(d.key); if (t.members.length > max) t.members.shift(); }
      render(); break; }
    case 'teamPage': ui.teamPage = parseInt(d.p, 10); render(); break;
    case 'teamSave': { const t = ui.team; if (t.members.length < 2) break;
      const vs = t.members.map(k => variant(...k.split('::'))).filter(Boolean);
      U.teams.unshift({ id: 'eq-' + Date.now(), name: t.name || vs.map(fullLabel).join(' + '),
                        members: t.members.slice(), reason: t.reason });
      ui.teamOpen = false; commit(); break; }
    case 'teamRemove': U.teams = U.teams.filter(x => x.id !== d.id); commit(); break;

    case 'goEditor': ui.view = 'editor'; ui.edId = null; ui.edStep = 0; ui.edDraft = blankDraft(); render(); break;
    case 'edit': { ui.view = 'editor'; ui.edId = d.cid; ui.edStep = 0;
      ui.edDraft = JSON.parse(JSON.stringify(CHAR_BY_ID[d.cid])); render(); break; }
    case 'edStep': ui.edStep = parseInt(d.i, 10); render(); break;
    case 'edPrev': ui.edStep = Math.max(0, ui.edStep - 1); render(); break;
    case 'edNext': ui.edStep = Math.min(2, ui.edStep + 1); render(); break;
    case 'edPick': { const f = d.f, v = d.v, dr = ui.edDraft;
      if (d.multi === '1') { const i = dr[f].indexOf(v); if (i > -1) dr[f].splice(i, 1); else dr[f].push(v); }
      else dr[f] = v;
      render(); break; }
    case 'edUniAdd': ui.edDraft.uniforms.push({ id:'u-' + Date.now(), name:'', tier:'T2', year:'', cost:'', striker:4, skills:[] }); render(); break;
    case 'edUniDel': ui.edDraft.uniforms.splice(parseInt(d.i, 10), 1); render(); break;
    case 'edSkAdd': ui.edDraft.uniforms[parseInt(d.i, 10)].skills.push({ slot:'Activa 1', n:'', d:'', fx:null, dmg:'Ninguno', ii:false, tags:[], cd:null, perm:false, iframe:false, gb:false, sgb:false }); render(); break;
    case 'edSkDel': ui.edDraft.uniforms[parseInt(d.i, 10)].skills.splice(parseInt(d.s, 10), 1); render(); break;
    case 'edRevert': delete U.charEdits[ui.edId]; ui.view = 'detail'; ui.charId = ui.edId; ui.edId = null; commit(); break;
    case 'edSave': { const dr = ui.edDraft;
      if (!dr.name.trim()) { alert('Poné un nombre.'); break; }
      const id = ui.edId || ('mio-' + dr.name.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + Date.now());
      const ch = Object.assign({}, dr, { id, uniforms: dr.uniforms.map((u, i) => Object.assign({}, u, { id: u.id || id + '-u' + i })) });
      if (ui.edId && CHARS_SEED.some(c => c.id === ui.edId)) U.charEdits[id] = ch;
      else if (ui.edId) U.charNew = U.charNew.map(c => c.id === id ? ch : c);
      else U.charNew.unshift(ch);
      ui.view = 'detail'; ui.charId = id; ui.uniformId = 'base'; ui.edId = null; commit(); break; }

    case 'goSettings': ui.view = 'settings'; render(); break;
    case 'modeAdd': U.modes.push({ id:'modo-' + Date.now(), name:'Modo nuevo', teamSize:3 }); commit(); break;
    case 'modeDel': U.modes.splice(parseInt(d.i, 10), 1); commit(); break;
    case 'clearImg': delete U.images[d.img]; commit(); break;
    case 'resetUser': if (confirm('Se borran tus equipos, listas, ediciones e imágenes. Los datos del juego no se tocan. ¿Seguimos?')) {
      U = blankUser(); commit(); } break;
    case 'exportUser': download('mff-mi-capa.json', JSON.stringify(U, null, 2), 'application/json'); break;
    case 'exportCsv': exportCsv(); break;
  }
});

document.addEventListener('input', (e) => {
  const el = e.target.closest('[data-a]'); if (!el) return;
  const a = el.getAttribute('data-a'), d = el.dataset;
  if (a === 'search') { ui.search = el.value; ui.page = 0; ui.focusSearch = true; render(); return; }
  if (a === 'newListName') { ui.newListName = el.value; return; }
  if (a === 'poolSearch') { ui.poolSearch = el.value; render(); $('[data-a="poolSearch"]')?.focus(); return; }
  if (a === 'teamName') { ui.team.name = el.value; return; }
  if (a === 'teamReason') { ui.team.reason = el.value; return; }
  if (a === 'teamSearch') { ui.teamSearch = el.value; ui.teamPage = 0; render(); return; }
  if (a === 'edField') { ui.edDraft[d.f] = el.value; return; }
  if (a === 'edUni') { ui.edDraft.uniforms[d.i][d.f] = el.value; return; }
  if (a === 'edSk') { ui.edDraft.uniforms[d.i].skills[d.s][d.f] = el.value; return; }
  if (a === 'modeName') { U.modes[d.i].name = el.value; saveUser(); return; }
  if (a === 'modeSize') { U.modes[d.i].teamSize = Math.max(1, parseInt(el.value, 10) || 3); saveUser(); return; }
});

document.addEventListener('change', (e) => {
  const el = e.target.closest('[data-a]'); if (!el) return;
  const a = el.getAttribute('data-a'), d = el.dataset;
  if (a === 'sort') { U.prefs.sort = el.value; commit(); return; }
  if (a === 'refList') { U.prefs.refList = el.value; commit(); return; }
  if (a === 'teamMode') { const m = U.modes.find(x => x.id === el.value);
    ui.team.modeId = el.value; ui.team.members = ui.team.members.slice(-(m ? m.teamSize : 3)); render(); return; }
  if (a === 'edUni') { ui.edDraft.uniforms[d.i][d.f] = el.value; return; }
  if (a === 'edSk') { ui.edDraft.uniforms[d.i].skills[d.s][d.f] = el.value; return; }
  if (a === 'upload') { const f = el.files[0]; if (f) readFile(f, url => { U.images[d.img] = url; commit(); }); return; }
  if (a === 'importUser') { const f = el.files[0]; if (!f) return;
    const r = new FileReader();
    r.onload = () => { try { U = Object.assign(blankUser(), JSON.parse(r.result)); commit(); }
                       catch (err) { alert('Ese archivo no es una capa de usuario válida: ' + err.message); } };
    r.readAsText(f); return; }
});

// arrastrar y soltar en las tier lists
document.addEventListener('dragstart', (e) => {
  const el = e.target.closest('[data-a="drag"]'); if (!el) return;
  ui.dragKey = el.dataset.key; e.dataTransfer.setData('text/plain', el.dataset.key); e.dataTransfer.effectAllowed = 'move';
});
document.addEventListener('dragover', (e) => {
  const z = e.target.closest('[data-a="drop"]'); if (!z) return;
  e.preventDefault(); z.closest('.tierrow')?.classList.add('over');
});
document.addEventListener('dragleave', (e) => { e.target.closest('[data-a="drop"]')?.closest('.tierrow')?.classList.remove('over'); });
document.addEventListener('drop', (e) => {
  const z = e.target.closest('[data-a="drop"]'); if (!z) return;
  e.preventDefault();
  const key = ui.dragKey; ui.dragKey = null; if (!key) return;
  setAssign(ui.tierList, key, z.dataset.row || REMOVED);
});

function download (name, text, type) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], { type }));
  a.download = name; a.click(); URL.revokeObjectURL(a.href);
}
function exportCsv () {
  const head = ['clave','personaje','uniforme','clase','bando','tier','trascendido','instinto','raza','genero','origen',
                'roles','habilidades','striker','world_boss','costo','slot','skill','descripcion','dano','etiquetas'];
  const rows = [head];
  allVariants().forEach(v => {
    const base = [v.key, v.name, v.uid ? v.sub : '', v.c, v.f, v.t, v.trans ? 'sí' : 'no', v.ins, v.ch.race, v.ch.gender,
                  v.ch.origin, v.r.join('|'), (v.ab || []).join('|'), v.striker, v.wba, v.cost];
    if (!v.skills.length) rows.push(base.concat(['', '', '', '', '']));
    v.skills.forEach(sk => rows.push(base.concat([sk.slot, sk.n, sk.d, sk.dmg, (sk.tags || []).join('|')])));
  });
  download('mff-roster.csv', '﻿' + rows.map(r => r.map(c => '"' + String(c == null ? '' : c).replace(/"/g, '""') + '"').join(',')).join('\n'), 'text/csv');
}

rebuild();
render();
})();
