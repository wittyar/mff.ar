/* Comparador MFF — standalone vanilla JS app (no build step, runs from file:// or any static host). */
(function(){
'use strict';
const SEED = window.MFF_SEED, CHARS_SEED = window.MFF_SEED_CHARACTERS, TEAMS_SEED = window.MFF_TEAM_SUGGESTIONS;
const LS_KEY = 'mff_standalone_v2';
const TIER_RANKS = ['S','A','B','C','D'];
const SLOT_ORDER = ['Liderazgo','Pasiva','Activa 1','Activa 2','Activa 3','Activa 4','Activa 5','Definitiva'];

function deepCopy(o){ return JSON.parse(JSON.stringify(o)); }

function defaultState(){
  return {
    characters: deepCopy(CHARS_SEED),
    teams: deepCopy(TEAMS_SEED),
    modes: deepCopy(SEED.MODES),
    customTierLists: deepCopy(window.MFF_SEED_TIERLISTS || []),
    tierAssignments: deepCopy(window.MFF_SEED_TIER_ASSIGNMENTS || {}),
    taxonomies: {
      factions: SEED.FACTIONS.map(v=>({value:v,icon:''})),
      instincts: SEED.INSTINCTS.map(v=>({value:v,icon:''})),
      races: SEED.RACES.map(v=>({value:v,icon:''})),
      genders: SEED.GENDERS.map(v=>({value:v,icon:''})),
      skillTags: SEED.SKILL_TAGS.map(v=>({value:v,icon:''}))
    },
    images: deepCopy(window.MFF_SEED_IMAGES || {}),
    logo: ''
  };
}
let state = load();
function load(){
  try { const raw = localStorage.getItem(LS_KEY); if (raw) return Object.assign(defaultState(), JSON.parse(raw)); } catch(e){}
  return defaultState();
}
function save(){ try { localStorage.setItem(LS_KEY, JSON.stringify(state)); } catch(e){ console.warn('save failed', e); } }

// ---- transient UI state (not persisted) ----
let ui = {
  view: 'roster', search: '', filters: { c:[], r:[], f:[], t:[], ins:[], ab:[] }, filtersOpen: false, rosterPage: 0,
  compareMode: false, compareSelection: [],
  selectedCharId: null, viewUniformIds: [],
  showTeamBuilder: false, teamBuilder: { name:'', memberIds:[], reason:'', modeId:'' }, teamBuilderSearch:'', teamBuilderPage:0,
  tierListModeView: '', newTierListName: '',
  adminStep: 0, adminDraft: null, adminEditId: null,
  admin_field_dragKey: null
};

const $ = (sel, root) => (root||document).querySelector(sel);
const $all = (sel, root) => Array.from((root||document).querySelectorAll(sel));
function h(str){ const d=document.createElement('div'); d.textContent=str==null?'':String(str); return d.innerHTML; }

// ---- color helpers ----
function classColor(c){ return { 'Combate':'var(--class-combate)','Detonación':'var(--class-detonacion)','Velocidad':'var(--class-velocidad)','Universal':'var(--class-universal)' }[c] || 'var(--text-dim)'; }
function dmgColor(d){ return { 'Físico':'var(--dmg-fisico)','Energía':'var(--dmg-energia)','PG':'var(--dmg-pg)' }[d] || 'var(--text-dim)'; }
function tierColor(t){ return { 'T1':'var(--tier-t1)','T2':'var(--tier-t2)','T3':'var(--tier-t3)' }[t] || 'var(--text-dim)'; }
function roleColor(r){ return { 'Daño':'var(--role-dano)','Soporte':'var(--role-soporte)','Control':'var(--role-control)','Tanque':'var(--role-tanque)' }[r] || 'var(--text-dim)'; }
function tag(label, color, outline){ return `<span class="tag${outline?' outline':''}" style="${outline?`color:${color};border-color:${color}`:`background:${color};color:#111`}">${h(label)}</span>`; }

function findChar(cid){ return state.characters.find(c=>c.id===cid); }
function findUniform(ch, uid){ return ch && ch.uniforms.find(u=>u.id===uid); }
function resolveMember(cid, uid){
  const ch = findChar(cid); if (!ch) return null;
  const base = ch.baseSkills || [];
  if (!uid) return { id: ch.id, name: ch.name, c: ch.c, f: ch.f, t: ch.t, ins: ch.ins, r: ch.r, uniforms: ch.uniforms, rawSkills: base };
  const u = findUniform(ch, uid); if (!u) return { id: ch.id, name: ch.name, c: ch.c, f: ch.f, t: ch.t, ins: ch.ins, r: ch.r, uniforms: ch.uniforms, rawSkills: base };
  return { id: ch.id, name: ch.name+' ('+u.name+')', c: u.c||ch.c, f: ch.f, t: u.tier||ch.t, ins: u.ins||ch.ins, r: (u.r&&u.r.length)?u.r:ch.r, uniforms: ch.uniforms, rawSkills: base.concat(u.skills) };
}
function synergyScore(chars){
  if (chars.length < 2) return { score:0, reasons:[] };
  const reasons = []; let score = 0;
  const factions = chars.map(c=>c.f);
  if (factions.every(f=>f===factions[0])) { score+=2; reasons.push('Misma facción: bonos de equipo activos.'); }
  const roles = new Set(chars.flatMap(c=>c.r));
  const want = ['Tanque','Control','Daño']; const covered = want.filter(r=>roles.has(r));
  if (covered.length>=2) { score+=covered.length; reasons.push('Roles complementarios: '+covered.join(' + ')+'.'); }
  for (let i=0;i<chars.length;i++) for (let j=0;j<chars.length;j++){
    if (i===j) continue;
    if (SEED.CLASS_ADVANTAGE[chars[i].c]===chars[j].c) { score+=1; reasons.push(chars[i].name+' ('+chars[i].c+') cubre la debilidad de clase de '+chars[j].name+'.'); }
  }
  return { score, reasons: [...new Set(reasons)] };
}

// ---- images ----
function imgTag(id, w, ht, ph){
  const url = state.images[id];
  if (url) return `<div class="portrait" style="height:${ht||'100%'}"><img src="${url}"/></div>`;
  return `<div class="portrait" style="height:${ht||'100%'}"><span class="ph">${h(ph||'RETRATO')}</span></div>`;
}
function iconImg(value){
  const url = state.images['icon-'+value];
  return url ? `<img class="taxicon" src="${url}" alt=""/>` : '';
}
function skillFx(sk){
  if (!sk.fx) return h(sk.d);
  const L = { self:'A sí mismo', enemy:'Al oponente', allies:'Al equipo' };
  let out = '';
  if (sk.fx.general) out += `<div class="fxline">${sk.fx.general.map(h).join(' · ')}</div>`;
  for (const k of ['self','enemy','allies']) if (sk.fx[k] && sk.fx[k].length)
    out += `<div class="fxline"><span class="fxlabel fx-${k}">${L[k]}</span>${sk.fx[k].map(x=>`<span class="fxitem">${h(x)}</span>`).join('')}</div>`;
  return out || h(sk.d);
}
function readFileAsDataUrl(file, cb){
  const r = new FileReader();
  r.onload = () => cb(r.result);
  r.readAsDataURL(file);
}

// ============================================================================
// ROSTER
// ============================================================================
function flatUniformEntries(){
  return state.characters.flatMap(ch => ch.uniforms.map(u => ({
    ch, u, effC: u.c||ch.c, effR: (u.r&&u.r.length)?u.r:ch.r, effIns: u.ins||ch.ins, effT: u.tier||ch.t
  })));
}
function rosterFiltered(){
  const q = ui.search.trim().toLowerCase();
  const F = ui.filters;
  const variantsOf = (ch) => [{c:ch.c,r:ch.r,ins:ch.ins,t:ch.t}, ...ch.uniforms.map(u=>({c:u.c||ch.c,r:(u.r&&u.r.length)?u.r:ch.r,ins:u.ins||ch.ins,t:u.tier||ch.t}))];
  const filteredChars = state.characters.filter(ch=>{
    if (q && !ch.name.toLowerCase().includes(q) && !ch.uniforms.some(u=>u.name.toLowerCase().includes(q))) return false;
    if (F.f.length && !F.f.includes(ch.f)) return false;
    if (F.ab.length && !F.ab.some(a=>(ch.abilities||[]).includes(a))) return false;
    const variants = variantsOf(ch);
    return variants.some(v => (!F.c.length||F.c.includes(v.c)) && (!F.r.length||F.r.some(r=>v.r.includes(r))) && (!F.t.length||F.t.includes(v.t)) && (!F.ins.length||F.ins.includes(v.ins)));
  });
  const filteredUniEntries = flatUniformEntries().filter(({ch,u,effC,effR,effIns,effT})=>{
    if (q && !ch.name.toLowerCase().includes(q) && !u.name.toLowerCase().includes(q)) return false;
    if (F.f.length && !F.f.includes(ch.f)) return false;
    if (F.ab.length && !F.ab.some(a=>(ch.abilities||[]).includes(a))) return false;
    if (F.c.length && !F.c.includes(effC)) return false;
    if (F.r.length && !F.r.some(r=>effR.includes(r))) return false;
    if (F.t.length && !F.t.includes(effT)) return false;
    if (F.ins.length && !F.ins.includes(effIns)) return false;
    return true;
  });
  const byChar = {}; filteredUniEntries.forEach(e=>{ (byChar[e.ch.id]=byChar[e.ch.id]||[]).push(e); });
  const filteredIds = new Set(filteredChars.map(c=>c.id));
  const cards = [];
  state.characters.forEach(ch=>{
    if (filteredIds.has(ch.id)) cards.push({ kind:'char', ch });
    (byChar[ch.id]||[]).forEach(e=>cards.push({ kind:'uniform', e }));
  });
  return { cards, totalChars: state.characters.length, filteredChars: filteredChars.length,
    totalUnis: flatUniformEntries().length, filteredUnis: filteredUniEntries.length };
}

function renderRoster(){
  const { cards, filteredChars, totalChars, filteredUnis, totalUnis } = rosterFiltered();
  const PAGE=20; const totalPages = Math.max(1, Math.ceil(cards.length/PAGE));
  ui.rosterPage = Math.min(ui.rosterPage, totalPages-1);
  const pageCards = cards.slice(ui.rosterPage*PAGE, (ui.rosterPage+1)*PAGE);
  const F = ui.filters;
  const chipRow = (label, cat, values) => `<div style="margin-bottom:6px"><div class="hint" style="margin-bottom:4px;text-transform:uppercase;font-size:10px;letter-spacing:.06em">${label}</div><div class="row">${
    values.map(v=>`<button class="chip ${F[cat].includes(v)?'active':''}" data-act="filter" data-cat="${cat}" data-val="${h(v)}">${iconImg(v)}${h(v)}</button>`).join('')
  }</div></div>`;
  const abilityOpts = state.taxonomies.skillTags.map(t=>t.value);
  const factionOpts = state.taxonomies.factions.map(t=>t.value);
  const instinctOpts = state.taxonomies.instincts.map(t=>t.value);
  return `
  <div class="row" style="margin-bottom:16px">
    <input id="searchInput" placeholder="Buscar personaje o uniforme…" value="${h(ui.search)}" style="flex:1;min-width:220px" data-act="search"/>
    <button class="btn ghost" data-act="toggleFilters">Filtros${(F.c.length+F.r.length+F.f.length+F.t.length+F.ins.length+F.ab.length)?` (${F.c.length+F.r.length+F.f.length+F.t.length+F.ins.length+F.ab.length})`:''}</button>
    <button class="btn ghost" data-act="clearFilters">Limpiar filtros</button>
  </div>
  ${ui.filtersOpen ? `<div class="card" style="margin-bottom:16px;background:#0f1422">
    <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(180px,1fr))">
      <div>${chipRow('Clase','c',SEED.CLASSES)}</div>
      <div>${chipRow('Rol','r',SEED.ROLES)}</div>
      <div>${chipRow('Bando','f',factionOpts)}</div>
      <div>${chipRow('Tier','t',SEED.TIERS)}</div>
      <div>${chipRow('Habilidad','ab',abilityOpts)}</div>
      <div>${chipRow('Instinto','ins',instinctOpts)}</div>
    </div>
  </div>` : ''}
  <div class="hint">${filteredChars} de ${totalChars} personajes · ${filteredUnis} de ${totalUnis} uniformes</div>
  <div class="grid">
    ${pageCards.map(item=>{
      if (item.kind==='char'){
        const ch = item.ch;
        const selected = ui.compareSelection.some(x=>x.cid===ch.id && !x.uid);
        return `<div class="card" style="cursor:pointer;position:relative;${selected?'box-shadow:0 0 0 2px var(--red)':''}" data-act="openChar" data-cid="${ch.id}">
          ${ui.compareMode?`<div class="check ${selected?'on':''}" data-act="toggleCompare" data-cid="${ch.id}">${selected?'✓':''}</div>`:''}
          ${imgTag('portrait-'+ch.id,0,'130px')}
          <div style="font-weight:600;font-size:16px">${h(ch.name)}</div>
          <div class="row">${iconImg(ch.c)}${tag(ch.c, classColor(ch.c), true)}${tag(ch.t, tierColor(ch.t))}${tag(ch.ins, 'var(--text-dim)', true)}</div>
          <div class="hint" style="margin:0">${h(ch.f)} · ${ch.r.join(' / ')}</div>
        </div>`;
      } else {
        const {ch,u,effC,effR,effIns,effT} = item.e;
        const selected = ui.compareSelection.some(x=>x.cid===ch.id && x.uid===u.id);
        return `<div class="card dashed" style="cursor:pointer;position:relative;background:#0f1422;${selected?'box-shadow:0 0 0 2px var(--red)':''}" data-act="openUniform" data-cid="${ch.id}" data-uid="${u.id}">
          ${ui.compareMode?`<div class="check ${selected?'on':''}" data-act="toggleCompare" data-cid="${ch.id}" data-uid="${u.id}">${selected?'✓':''}</div>`:''}
          ${imgTag('portrait-'+u.id,0,'130px')}
          <div style="font-weight:600;font-size:16px">${h(u.name)}</div>
          <div class="hint" style="margin:0;color:var(--gold)">${h(ch.name)}</div>
          <div class="row">${iconImg(effC)}${tag(effC, classColor(effC), true)}${tag(effT, tierColor(effT))}${tag(effIns, 'var(--text-dim)', true)}</div>
          <div class="hint" style="margin:0">${h(ch.f)} · ${effR.join(' / ')}</div>
        </div>`;
      }
    }).join('')}
  </div>
  ${cards.length===0?'<div class="hint" style="text-align:center;padding:40px 0">Ningún resultado coincide con estos filtros.</div>':''}
  ${totalPages>1?`<div class="pagination">
    <button class="btn small ghost" data-act="rosterPage" data-p="${Math.max(0,ui.rosterPage-1)}">← Anterior</button>
    ${Array.from({length:totalPages},(_,i)=>`<button class="btn small ${i===ui.rosterPage?'primary':'ghost'}" data-act="rosterPage" data-p="${i}">${i+1}</button>`).join('')}
    <button class="btn small ghost" data-act="rosterPage" data-p="${Math.min(totalPages-1,ui.rosterPage+1)}">Siguiente →</button>
  </div>`:''}
  ${ui.compareMode && ui.compareSelection.length>=2 ? `<div style="position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:center;padding:14px;background:linear-gradient(to top,var(--bg) 70%,transparent)">
    <button class="btn primary" data-act="goCompare">Comparar ${ui.compareSelection.length}</button>
  </div>` : ''}
  `;
}

// ============================================================================
// DETAIL
// ============================================================================
function renderDetail(){
  const ch = findChar(ui.selectedCharId); if (!ch) { ui.view='roster'; return renderRoster(); }
  const sorted = ch.uniforms.slice().sort((a,b)=>(parseInt(b.year)||0)-(parseInt(a.year)||0));
  const mkRows = (skills) => skills.map((sk,i)=>`<div class="skillrow">
    <div class="name">${h(sk.slot)} — ${h(sk.n)}</div>
    <div class="desc">${skillFx(sk)}</div>
    <div class="row">
      <span class="tag outline" style="color:var(--gold);border-color:var(--gold)">${h(window.MFF_skillTiming(sk))}</span>
      ${sk.dmg&&sk.dmg!=='Ninguno'?`<span class="tag outline" style="color:${dmgColor(sk.dmg)};border-color:${dmgColor(sk.dmg)}">${h(sk.dmg)}</span>`:''}
      ${sk.ii?'<span class="tag outline">Ignora iframe</span>':''}
      ${sk.iframe?'<span class="tag outline">Tiene iframe</span>':''}
      ${sk.gb?'<span class="tag outline">Rotura de Guardia</span>':''}
      ${sk.sgb?'<span class="tag outline">Superrotura de Guardia</span>':''}
    </div></div>`).join('');
  const selectorItems = [{id:'base',name:'Base'}, ...sorted.map(u=>({id:u.id,name:u.name}))];
  const teams = state.teams.filter(t=>t.members.some(k=>k.split('::')[0]===ch.id));
  return `
  <button class="btn ghost" data-act="backRoster" style="margin-bottom:16px">← Volver al roster</button>
  <div style="display:flex;gap:22px;align-items:flex-start;flex-wrap:wrap">
    <div style="width:420px;max-width:100%;position:sticky;top:80px;display:flex;flex-direction:column;gap:10px">
      <div class="hint" style="margin:0;text-transform:uppercase;font-size:11px">Comparar con uniforme</div>
      <div class="row" style="overflow-x:auto;flex-wrap:nowrap;padding-bottom:4px">
        ${selectorItems.map(u=>`<button class="chip ${ui.viewUniformIds.includes(u.id)?'active':''}" data-act="selectView" data-uid="${u.id}" style="flex:none">${h(u.name)}</button>`).join('')}
      </div>
      <div class="row" style="gap:16px">
        ${['base',...ui.viewUniformIds.filter(x=>x!=='base')].filter((v,i,a)=>a.indexOf(v)===i && (v==='base'?true:ui.viewUniformIds.includes(v))).map(vid=>{
          if (!ui.viewUniformIds.includes(vid)) return '';
          const label = vid==='base' ? 'Base' : (findUniform(ch,vid)||{}).name;
          const pid = vid==='base' ? ch.id : vid;
          return `<div style="display:flex;flex-direction:column;gap:6px">
            <div class="hint" style="margin:0;color:var(--gold);text-transform:uppercase;font-size:11px">${h(label)}</div>
            <div style="width:100px;height:100px;border-radius:8px;overflow:hidden">${imgTag('portrait-'+pid,0,'100px')}</div>
            <div style="width:190px;height:260px;border-radius:8px;overflow:hidden">${imgTag('fullbody-'+pid,0,'260px','Cuerpo entero')}</div>
            <label class="btn small ghost" style="text-align:center;cursor:pointer">Subir retrato<input type="file" accept="image/*" style="display:none" data-act="uploadImg" data-imgid="portrait-${pid}"/></label>
            <label class="btn small ghost" style="text-align:center;cursor:pointer">Subir cuerpo entero<input type="file" accept="image/*" style="display:none" data-act="uploadImg" data-imgid="fullbody-${pid}"/></label>
          </div>`;
        }).join('')}
      </div>
    </div>
    <div style="flex:1;min-width:280px">
      <h1>${h(ch.name)}</h1>
      <div class="row" style="margin-bottom:8px">${tag(ch.c,classColor(ch.c),true)}${tag(ch.f,'var(--gold)')}${tag(ch.t,tierColor(ch.t))}${tag(ch.ins,'var(--text-dim)',true)}</div>
      <div class="hint">Roles: ${ch.r.join(', ')} · Modos: ${ch.modes.map(mid=>{const m=state.modes.find(x=>x.id===mid);return m?m.name:mid;}).join(', ')} · Raza: ${h(ch.race||'—')} · Género: ${h(ch.gender||'—')} · Habilidades: ${(ch.abilities||[]).map(a=>iconImg(a)+h(a)).join(', ')||'—'}</div>
      <button class="btn ghost" data-act="editChar" data-cid="${ch.id}" style="margin-top:8px">Editar personaje</button>

      ${teams.length?`<div class="section" style="margin-top:22px"><h3>Equipos sugeridos</h3><div class="grid">
        ${teams.map(t=>`<div class="card"><div class="hint" style="margin:0;color:var(--red);text-transform:uppercase;font-size:10px">${h(t.name)}</div>
          <div style="font-weight:600;font-size:13px">${t.members.map(k=>{const r=resolveMember(...k.split('::'));return r?r.name:k;}).join(' + ')}</div>
          <p class="hint" style="margin:0">${h(t.reason)}</p></div>`).join('')}
      </div></div>`:''}

      <div class="section" style="margin-top:22px">
        <h3>Uniformes (${ch.uniforms.length})</h3>
        <p class="hint">"Base" son las estadísticas generales; cada uniforme las suma a lo suyo. El check ✓ es para comparar habilidades.</p>
        <div class="grid">
          ${sorted.map(u=>{
            const isViewing = ui.viewUniformIds.includes(u.id);
            return `<div class="card" style="${isViewing?'outline:2px solid var(--red);outline-offset:2px':''}">
              <div class="row" style="justify-content:space-between">
                <div style="font-weight:600">${h(u.name)}</div>
              </div>
              <div class="row">${tag(u.tier,tierColor(u.tier))}<span class="hint" style="margin:0">${h(u.year)}</span></div>
              ${mkRows(ch.baseSkills.concat(u.skills))}
            </div>`;
          }).join('')}
          <div class="card">
            <div style="font-weight:600">Base (${h(ch.name)})</div>
            ${mkRows(ch.baseSkills)}
          </div>
        </div>
      </div>
    </div>
  </div>`;
}

// ============================================================================
// COMPARE (characters and/or specific uniforms, up to 4)
// ============================================================================
function renderCompare(){
  const compareChars = ui.compareSelection.map(sel=>resolveMember(sel.cid, sel.uid)).filter(Boolean);
  const colTemplate = 'repeat('+Math.max(compareChars.length,1)+',1fr)';
  const cnt = (list, get) => { const m={}; list.forEach(v=>{const k=get(v); m[k]=(m[k]||0)+1;}); return m; };
  const classCounts = cnt(compareChars,c=>c.c), factionCounts = cnt(compareChars,c=>c.f), tierCounts = cnt(compareChars,c=>c.t);
  const slots = SLOT_ORDER.filter(slot=>compareChars.some(c=>c.rawSkills.some(sk=>sk.slot===slot)));
  const synergy = compareChars.length>=2 ? synergyScore(compareChars) : {score:0,reasons:[]};
  const pct = Math.min(100, Math.round(synergy.score/10*100));
  return `
  <button class="btn ghost" data-act="backRoster" style="margin-bottom:16px">← Volver al roster</button>
  <h1>Comparativa</h1>
  <div class="grid" style="grid-template-columns:${colTemplate};margin-bottom:20px">
    ${compareChars.map(c=>`<div class="card">
      <div style="font-weight:700;font-size:17px;margin-bottom:6px">${h(c.name)}</div>
      <div style="font-size:12.5px;display:flex;flex-direction:column;gap:5px">
        <div>Clase: ${tag(c.c, classCounts[c.c]>1?'var(--red)':'#333')}</div>
        <div>Bando: ${tag(c.f, factionCounts[c.f]>1?'var(--red)':'#333')}</div>
        <div>Rol: ${c.r.join(', ')}</div>
        <div>Tier: ${tag(c.t, tierCounts[c.t]>1?'var(--red)':'#333')}</div>
        <div class="hint" style="margin:0">Uniformes: ${c.uniforms.map(u=>u.name).join(', ')}</div>
      </div>
    </div>`).join('')}
  </div>
  <div class="section">
    <h3>Habilidades</h3>
    <p class="hint">Se resalta cuando coincide tipo de daño en el mismo slot.</p>
    ${slots.map(slot=>{
      const raw = compareChars.map(c=>c.rawSkills.find(sk=>sk.slot===slot)||null);
      const present = raw.filter(Boolean);
      const dmgCounts = {}; present.forEach(sk=>{ if (sk.dmg&&sk.dmg!=='Ninguno') dmgCounts[sk.dmg]=(dmgCounts[sk.dmg]||0)+1; });
      return `<div style="margin-bottom:10px">
        <div class="hint" style="margin:0 0 4px;text-transform:uppercase;font-size:11px">${h(slot)}</div>
        <div class="grid" style="grid-template-columns:${colTemplate}">
          ${raw.map(sk=>{
            if (!sk) return `<div class="card"><span class="hint" style="margin:0">— No tiene este slot —</span></div>`;
            const highlight = sk.dmg!=='Ninguno' && dmgCounts[sk.dmg]>1;
            return `<div class="card">
              <div style="font-weight:600;font-size:14px;margin-bottom:4px">${h(sk.n)}</div>
              <div style="margin:0 0 6px;font-size:12.5px;opacity:.85">${skillFx(sk)}</div>
              <div class="row">
                <span class="tag outline" style="color:var(--gold);border-color:var(--gold)">${h(window.MFF_skillTiming(sk))}</span>
                <span class="tag${highlight?'':' outline'}" style="${highlight?`background:var(--red);color:#111`:`color:${dmgColor(sk.dmg)};border-color:${dmgColor(sk.dmg)}`}">${h(sk.dmg)}</span>
              </div>
            </div>`;
          }).join('')}
        </div>
      </div>`;
    }).join('')}
  </div>
  <div class="card">
    <div class="row" style="margin-bottom:8px">
      <h3 style="margin:0">Sinergia automática</h3>
      <div style="flex:1;height:6px;background:#333;border-radius:4px;overflow:hidden"><div style="height:100%;width:${pct}%;background:var(--red)"></div></div>
      <span class="hint" style="margin:0">${synergy.score} pts</span>
    </div>
    ${synergy.reasons.length?`<ul style="margin:0;padding-left:18px;font-size:13px">${synergy.reasons.map(r=>`<li>${h(r)}</li>`).join('')}</ul>`
      :`<p class="hint" style="margin:0">Sin señales de sinergia fuertes entre esta selección.</p>`}
  </div>`;
}

// ============================================================================
// TEAMS
// ============================================================================
function renderTeams(){
  const modeOpts = [{id:'',name:'Sin modo específico (3 por defecto)'}, ...state.modes];
  const tb = ui.teamBuilder;
  const mode = state.modes.find(m=>m.id===tb.modeId);
  const max = mode ? mode.teamSize : 3;
  const modeMap = state.tierAssignments[tb.modeId] || {};
  const rankIdx = (key) => { const i=TIER_RANKS.indexOf(modeMap[key]); return i===-1?TIER_RANKS.length:i; };
  const q = (ui.teamBuilderSearch||'').trim().toLowerCase();
  let entries = state.characters.flatMap(c=>[
    {key:c.id, label:c.name, m:c.name.toLowerCase().includes(q)},
    ...c.uniforms.map(u=>({key:c.id+'::'+u.id, label:u.name+' — '+c.name, m: !q || c.name.toLowerCase().includes(q) || u.name.toLowerCase().includes(q)}))
  ]).filter(e=>!q||e.m);
  entries.sort((a,b)=>rankIdx(a.key)-rankIdx(b.key));
  const PS=24; const totalPages=Math.max(1,Math.ceil(entries.length/PS));
  ui.teamBuilderPage = Math.min(ui.teamBuilderPage, totalPages-1);
  const pageEntries = entries.slice(ui.teamBuilderPage*PS,(ui.teamBuilderPage+1)*PS);
  return `
  <div class="row" style="justify-content:space-between;margin-bottom:16px">
    <div><h1>Equipos sugeridos</h1><p class="hint">Combinaciones curadas y las que armás vos, con sinergia automática.</p></div>
    <button class="btn ghost" data-act="openTeamBuilder">+ Armar equipo</button>
  </div>
  ${ui.showTeamBuilder ? `<div class="card" style="margin-bottom:20px">
    <div class="field"><label>Nombre del equipo (opcional)</label><input id="tbName" style="width:100%" value="${h(tb.name)}" data-act="tbName"/></div>
    <div class="field" style="margin-top:8px"><label>Modo de juego (define el tamaño máximo)</label>
      <select data-act="tbMode">${modeOpts.map(m=>`<option value="${m.id}" ${m.id===tb.modeId?'selected':''}>${h(m.name)}${m.teamSize?` (${m.teamSize})`:''}</option>`).join('')}</select>
    </div>
    <div class="field" style="margin-top:8px"><label>Miembros (${tb.memberIds.length} / ${max}) — ordenados por la tier list de este modo</label>
      <input placeholder="Buscar personaje o uniforme…" style="width:100%;margin-bottom:8px" value="${h(ui.teamBuilderSearch)}" data-act="tbSearch"/>
      <div class="row">
        ${pageEntries.map(e=>{
          const selected = tb.memberIds.includes(e.key);
          const pid = e.key.includes('::') ? e.key.split('::')[1] : e.key;
          return `<div title="${h(e.label)}" data-act="tbToggle" data-key="${e.key}" style="width:56px;height:56px;border-radius:8px;overflow:hidden;cursor:pointer;flex:none;${selected?'box-shadow:0 0 0 2px var(--red)':'box-shadow:0 0 0 1px rgba(240,240,240,.16)'}">${imgTag('portrait-'+pid,56,'56px')}</div>`;
        }).join('')}
      </div>
      ${totalPages>1?`<div class="row" style="margin-top:8px">${Array.from({length:totalPages},(_,i)=>`<button class="btn small ${i===ui.teamBuilderPage?'primary':'ghost'}" data-act="tbPage" data-p="${i}">${i+1}</button>`).join('')}</div>`:''}
    </div>
    <div class="field" style="margin-top:8px"><label>Motivo (opcional)</label><textarea style="width:100%;min-height:50px" data-act="tbReason">${h(tb.reason)}</textarea></div>
    <div class="row" style="justify-content:flex-end;margin-top:10px">
      <button class="btn ghost" data-act="closeTeamBuilder">Cancelar</button>
      <button class="btn primary" data-act="saveTeam" ${tb.memberIds.length<2?'disabled':''}>Guardar equipo</button>
    </div>
  </div>`:''}
  <div class="grid">
    ${state.teams.map(t=>{
      const chars = t.members.map(k=>resolveMember(...k.split('::'))).filter(Boolean);
      const sc = synergyScore(chars);
      return `<div class="card" style="position:relative">
        <button class="btn small ghost" data-act="removeTeam" data-id="${t.id}" style="position:absolute;top:8px;right:8px">✕</button>
        <div style="font-weight:600;padding-right:18px">${h(t.name)}</div>
        <div style="color:var(--red);font-size:13px">${chars.map(c=>c.name).join(' + ')}</div>
        <p class="hint" style="margin:0">${h(t.reason)}</p>
        <div class="hint" style="margin:0">${sc.score} pts de sinergia</div>
      </div>`;
    }).join('')}
  </div>`;
}

// ============================================================================
// TIER LIST
// ============================================================================
function tierDefs(){ return [...state.modes.map(m=>({key:m.id,label:m.name,removable:false})), ...state.customTierLists.map(l=>({key:l.id,label:l.name,removable:true}))]; }
function renderTierList(){
  const defs = tierDefs();
  const active = ui.tierListModeView || (defs[0]&&defs[0].key) || '';
  const entries = state.characters.flatMap(ch=>[{key:ch.id+'::base', label:ch.name+' (base)', uid:ch.id}, ...ch.uniforms.map(u=>({key:ch.id+'::'+u.id, label:u.name+' — '+ch.name, uid:u.id}))]);
  const modeMap = state.tierAssignments[active] || {};
  const rankColor = {S:'var(--red)',A:'#ff7a3d',B:'#ffb020',C:'#8a8f9c',D:'#555'};
  const rows = TIER_RANKS.map(rank=>({
    rank, items: entries.filter(e=>modeMap[e.key]===rank)
  }));
  const unranked = entries.filter(e=>!modeMap[e.key]);
  return `
  <h1>Tier list</h1>
  <p class="hint">La armás vos: asigná cada uniforme a un rango (S/A/B/C/D), arrastrando o con los botones. Un tier list por modo o categoría.</p>
  <div class="row" style="margin-bottom:10px">
    ${defs.map(d=>`<span style="display:inline-flex;gap:2px;align-items:center">
      <button class="tabbtn ${d.key===active?'active':''}" data-act="tierMode" data-key="${d.key}">${h(d.label)}</button>
      ${d.removable?`<button class="btn small ghost" data-act="removeTierList" data-key="${d.key}" title="Borrar">✕</button>`:''}
    </span>`).join('')}
  </div>
  <div class="row" style="margin-bottom:20px">
    <input placeholder="Nombre de una tier list nueva (ej: Mis favoritos)" style="width:280px" value="${h(ui.newTierListName)}" data-act="newTierListName"/>
    <button class="btn ghost" data-act="addTierList">+ Crear tier list</button>
  </div>
  <div style="margin-bottom:16px">
    ${rows.map(row=>`<div class="rankrow" data-act="dropRank" data-rank="${row.rank}">
      <span class="rankbadge" style="background:${rankColor[row.rank]}">${row.rank}</span>
      <div class="row">${row.items.map(e=>`<span class="tierchip" draggable="true" data-act="dragItem" data-key="${e.key}">
        ${imgTag('portrait-'+e.uid,26,'',' ').replace('class="portrait"','class="ph2"')}
        ${h(e.label)}<button class="btn small ghost" data-act="unassignTier" data-key="${e.key}" style="padding:0 4px">✕</button>
      </span>`).join('')}</div>
    </div>`).join('')}
  </div>
  <details ${unranked.length?'':'style="display:none"'}>
    <summary style="font-size:12px;color:var(--red);cursor:pointer">Asignar más uniformes (${unranked.length})…</summary>
    <div style="display:flex;flex-direction:column;gap:5px;margin-top:8px;max-height:280px;overflow-y:auto" data-act="dropUnranked">
      ${unranked.map(e=>`<div class="row" style="background:var(--surface);border-radius:7px;padding:5px 8px" draggable="true" data-act="dragItem" data-key="${e.key}">
        <span style="flex:1;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${h(e.label)}</span>
        <div class="row" style="flex:none">${TIER_RANKS.map(r=>`<button class="btn small ghost" data-act="assignTier" data-key="${e.key}" data-rank="${r}">${r}</button>`).join('')}</div>
      </div>`).join('')}
    </div>
  </details>`;
}

// ============================================================================
// SETTINGS
// ============================================================================
function renderSettings(){
  const taxSection = (cat, title) => `<div class="card" style="margin-bottom:14px">
    <h3>${h(title)}</h3>
    <div style="display:flex;flex-direction:column;gap:6px">
      ${state.taxonomies[cat].map((it,i)=>`<div class="row">
        <input data-act="taxIcon" data-cat="${cat}" data-i="${i}" value="${h(it.icon)}" placeholder="Ícono/emoji" style="width:70px"/>
        <input data-act="taxValue" data-cat="${cat}" data-i="${i}" value="${h(it.value)}" style="flex:1"/>
        <button class="btn small ghost" data-act="taxRemove" data-cat="${cat}" data-i="${i}">✕</button>
      </div>`).join('')}
    </div>
    <button class="btn small ghost" data-act="taxAdd" data-cat="${cat}" style="margin-top:8px">+ Agregar</button>
  </div>`;
  return `
  <h1>Configuración</h1>
  <div class="card" style="margin-bottom:14px">
    <h3>Logo</h3>
    <p class="hint">Si lo cargás, reemplaza el texto de la marca en el encabezado.</p>
    <div style="width:220px;height:56px;border-radius:8px;overflow:hidden;background:var(--surface2)">${imgTag('brand-logo',220,'56px','Logo')}</div>
    <label class="btn small ghost" style="margin-top:8px;display:inline-block;cursor:pointer">Subir logo<input type="file" accept="image/*" style="display:none" data-act="uploadImg" data-imgid="brand-logo"/></label>
    ${state.images['brand-logo']?`<button class="btn small ghost" data-act="clearLogo" style="margin-left:6px">Quitar</button>`:''}
  </div>
  <div class="card" style="margin-bottom:14px">
    <h3>Modos de juego</h3>
    <div style="display:flex;flex-direction:column;gap:6px">
      ${state.modes.map((m,i)=>`<div class="row">
        <input data-act="modeIcon" data-i="${i}" value="${h(m.icon||'')}" placeholder="Ícono" style="width:70px"/>
        <input data-act="modeName" data-i="${i}" value="${h(m.name)}" style="flex:2"/>
        <label class="hint" style="margin:0">Tamaño</label>
        <input type="number" min="2" max="8" data-act="modeSize" data-i="${i}" value="${m.teamSize}" style="width:70px"/>
        <button class="btn small ghost" data-act="modeRemove" data-i="${i}">✕</button>
      </div>`).join('')}
    </div>
    <button class="btn small ghost" data-act="modeAdd" style="margin-top:8px">+ Agregar modo</button>
  </div>
  ${taxSection('races','Raza')}${taxSection('genders','Género')}${taxSection('factions','Bando')}${taxSection('instincts','Instinto')}${taxSection('skillTags','Habilidad (Etiqueta)')}
  `;
}

// ============================================================================
// ADMIN (add/edit character)
// ============================================================================
function blankDraft(){ return { name:'', c:'Combate', f: state.taxonomies.factions[0]?.value||'', r:[], t:'T2', ins: state.taxonomies.instincts[0]?.value||'', race:'', gender:'', modes:[], abilities:[], baseSkills:[], uniforms:[{name:'',tier:'T2',year:'',skills:[]}] }; }
function renderAdmin(){
  const d = ui.adminDraft; const steps=['Datos básicos','Uniformes','Revisar'];
  const single = (field) => (val) => { d[field]=val; };
  const chipPicker = (opts, field, multi) => opts.map(v=>{
    const active = multi ? d[field].includes(v) : d[field]===v;
    return `<button class="chip ${active?'active':''}" data-act="adminPick" data-field="${field}" data-val="${h(v)}" data-multi="${multi?1:0}">${h(v)}</button>`;
  }).join('');
  let body = '';
  if (ui.adminStep===0){
    body = `<div class="field"><label>Nombre</label><input style="width:100%" data-act="adminField" data-field="name" value="${h(d.name)}"/></div>
    <div class="field"><label>Clase</label><div class="row">${chipPicker(SEED.CLASSES,'c',false)}</div></div>
    <div class="field"><label>Bando</label><div class="row">${chipPicker(state.taxonomies.factions.map(x=>x.value),'f',false)}</div></div>
    <div class="field"><label>Instinto</label><div class="row">${chipPicker(state.taxonomies.instincts.map(x=>x.value),'ins',false)}</div></div>
    <div class="field"><label>Raza</label><div class="row">${chipPicker(state.taxonomies.races.map(x=>x.value),'race',false)}</div></div>
    <div class="field"><label>Género</label><div class="row">${chipPicker(state.taxonomies.genders.map(x=>x.value),'gender',false)}</div></div>
    <div class="field"><label>Rol (uno o más)</label><div class="row">${chipPicker(SEED.ROLES,'r',true)}</div></div>
    <div class="field"><label>Tier</label><div class="row">${chipPicker(SEED.TIERS,'t',false)}</div></div>
    <div class="field"><label>Modos donde destaca</label><div class="row">${state.modes.map(m=>`<button class="chip ${d.modes.includes(m.id)?'active':''}" data-act="adminPick" data-field="modes" data-val="${m.id}" data-multi="1">${h(m.name)}</button>`).join('')}</div></div>
    <div class="field"><label>Habilidades destacadas (hasta 3)</label><div class="row">${chipPicker(state.taxonomies.skillTags.map(x=>x.value),'abilities',true)}</div></div>`;
  } else if (ui.adminStep===1){
    body = d.uniforms.map((u,ui2)=>`<div class="card" style="margin-bottom:12px">
      <div class="row">
        <input placeholder="Nombre del uniforme" style="flex:2" data-act="adminUField" data-u="${ui2}" data-field="name" value="${h(u.name)}"/>
        <input placeholder="Tier" style="flex:1" data-act="adminUField" data-u="${ui2}" data-field="tier" value="${h(u.tier)}"/>
        <input placeholder="Año" style="flex:1" data-act="adminUField" data-u="${ui2}" data-field="year" value="${h(u.year)}"/>
      </div>
      <div class="field" style="margin-top:6px"><label>¿Cambia la clase?</label><div class="row">
        <button class="chip ${!u.c?'active':''}" data-act="adminUField" data-u="${ui2}" data-field="c" data-val="">Igual que el personaje</button>
        ${SEED.CLASSES.map(v=>`<button class="chip ${u.c===v?'active':''}" data-act="adminUField" data-u="${ui2}" data-field="c" data-val="${v}">${v}</button>`).join('')}
      </div></div>
      ${u.skills.map((sk,si)=>`<div class="card" style="background:#0f1422;margin-top:8px">
        <div class="row">
          <select data-act="adminSkField" data-u="${ui2}" data-s="${si}" data-field="slot">${SLOT_ORDER.map(s=>`<option ${s===sk.slot?'selected':''}>${s}</option>`).join('')}</select>
          <select data-act="adminSkField" data-u="${ui2}" data-s="${si}" data-field="dmg">${SEED.DAMAGE_TYPES.map(s=>`<option ${s===sk.dmg?'selected':''}>${s}</option>`).join('')}</select>
          <label class="hint" style="margin:0"><input type="checkbox" data-act="adminSkField" data-u="${ui2}" data-s="${si}" data-field="ii" ${sk.ii?'checked':''}/> Ignora iframe</label>
          <button class="btn small ghost" data-act="adminSkRemove" data-u="${ui2}" data-s="${si}">✕</button>
        </div>
        <input placeholder="Nombre habilidad" style="width:100%;margin-top:6px" data-act="adminSkField" data-u="${ui2}" data-s="${si}" data-field="n" value="${h(sk.n)}"/>
        <textarea placeholder="Descripción" style="width:100%;margin-top:6px" data-act="adminSkField" data-u="${ui2}" data-s="${si}" data-field="d">${h(sk.d)}</textarea>
      </div>`).join('')}
      <button class="btn small ghost" data-act="adminSkAdd" data-u="${ui2}" style="margin-top:8px">+ Agregar habilidad</button>
    </div>`).join('') + `<button class="btn ghost" data-act="adminUAdd">+ Agregar otro uniforme</button>`;
  } else {
    body = `<div class="card"><div style="font-weight:600;font-size:18px">${h(d.name)}</div>
      <div class="hint">${[d.c,d.f,d.t,d.r.join('/')].filter(Boolean).join(' · ')}</div>
      <div class="hint">${d.uniforms.length} uniforme(s), ${d.uniforms.reduce((n,u)=>n+u.skills.length,0)} habilidades.</div></div>`;
  }
  return `<h1>${ui.adminEditId?'Editar personaje':'Agregar personaje'}</h1>
  <p class="hint">Paso ${ui.adminStep+1} de 3 — ${steps[ui.adminStep]}</p>
  <div class="row" style="margin-bottom:16px">${steps.map((s,i)=>`<button class="tabbtn ${i===ui.adminStep?'active':''}" data-act="adminStep" data-i="${i}">${i+1}. ${s}</button>`).join('')}</div>
  ${body}
  <div class="row" style="justify-content:space-between;margin-top:20px">
    <button class="btn ghost" data-act="adminPrev" ${ui.adminStep===0?'disabled':''}>Atrás</button>
    ${ui.adminStep===2?`<button class="btn primary" data-act="adminSave">${ui.adminEditId?'Guardar cambios':'Guardar personaje'}</button>`:`<button class="btn primary" data-act="adminNext">Siguiente</button>`}
  </div>`;
}

// ============================================================================
// NAV + RENDER DISPATCH
// ============================================================================
function renderNav(){
  const logo = state.images['brand-logo'];
  return `<nav class="topnav">
    <span class="brand" data-act="backRoster">${logo?`<img src="${logo}" style="height:28px;vertical-align:middle"/>`:`TA GUIANAEL <span class="accent">MFF</span>`}</span>
    <a data-act="backRoster">Roster</a>
    <button class="navbtn" data-act="toggleCompareMode">${ui.compareMode?'Salir de modo comparar':'Comparar personajes'}</button>
    <a data-act="goTeams">Equipos sugeridos</a>
    <a data-act="goTierList">Tier list</a>
    <a data-act="goAdmin">+ Agregar personaje</a>
    <a data-act="goSettings">Configuración</a>
    <button class="navbtn" data-act="exportJson">Exportar (JSON)</button>
    <label class="navbtn" style="cursor:pointer">Importar (JSON)<input type="file" accept=".json" style="display:none" data-act="importJson"/></label>
    <button class="navbtn" data-act="exportCsv">Exportar (CSV)</button>
  </nav>`;
}
function render(){
  let body;
  switch(ui.view){
    case 'detail': body = renderDetail(); break;
    case 'compare': body = renderCompare(); break;
    case 'teams': body = renderTeams(); break;
    case 'tierlist': body = renderTierList(); break;
    case 'settings': body = renderSettings(); break;
    case 'admin': body = renderAdmin(); break;
    default: body = renderRoster();
  }
  $('#app').innerHTML = renderNav() + '<main>' + body + '</main>';
}

// ============================================================================
// EVENT HANDLING (delegated)
// ============================================================================
function findMemberSel(cid, uid){ return ui.compareSelection.find(x=>x.cid===cid && (x.uid||null)===(uid||null)); }

document.addEventListener('click', (e)=>{
  const el = e.target.closest('[data-act]'); if (!el) return;
  const act = el.getAttribute('data-act');
  switch(act){
    case 'backRoster': ui.view='roster'; ui.selectedCharId=null; ui.compareMode=false; ui.compareSelection=[]; render(); break;
    case 'toggleFilters': ui.filtersOpen=!ui.filtersOpen; render(); break;
    case 'clearFilters': ui.filters={c:[],r:[],f:[],t:[],ins:[],ab:[]}; ui.search=''; ui.rosterPage=0; render(); break;
    case 'filter': { const cat=el.dataset.cat, val=el.dataset.val; const single=['c','f','t','ins'].includes(cat); const cur=ui.filters[cat];
      if (single) ui.filters[cat] = (cur.length===1&&cur[0]===val)?[]:[val];
      else ui.filters[cat] = cur.includes(val)?cur.filter(x=>x!==val):[...cur,val];
      ui.rosterPage=0; render(); break; }
    case 'rosterPage': ui.rosterPage=parseInt(el.dataset.p,10); render(); break;
    case 'toggleCompareMode': ui.compareMode=!ui.compareMode; ui.compareSelection=[]; ui.view='roster'; render(); break;
    case 'toggleCompare': { const cid=el.dataset.cid, uid=el.dataset.uid||null; const has=findMemberSel(cid,uid);
      if (has) ui.compareSelection = ui.compareSelection.filter(x=>x!==has);
      else { ui.compareSelection.push({cid,uid}); if (ui.compareSelection.length>4) ui.compareSelection.shift(); }
      render(); break; }
    case 'goCompare': ui.view='compare'; render(); break;
    case 'openChar': if (!ui.compareMode){ ui.view='detail'; ui.selectedCharId=el.dataset.cid; ui.viewUniformIds=['base']; render(); } break;
    case 'openUniform': if (!ui.compareMode){ ui.view='detail'; ui.selectedCharId=el.dataset.cid; ui.viewUniformIds=[el.dataset.uid]; render(); } break;
    case 'selectView': { const uid=el.dataset.uid; const i=ui.viewUniformIds.indexOf(uid);
      if (i>-1) ui.viewUniformIds.splice(i,1); else { ui.viewUniformIds.push(uid); if (ui.viewUniformIds.length>2) ui.viewUniformIds.shift(); }
      render(); break; }
    case 'editChar': ui.view='admin'; ui.adminEditId=el.dataset.cid; ui.adminStep=0; { const ch=findChar(el.dataset.cid); ui.adminDraft = deepCopy({ ...ch, uniforms: ch.uniforms }); } render(); break;
    case 'goTeams': ui.view='teams'; render(); break;
    case 'openTeamBuilder': ui.showTeamBuilder=true; ui.teamBuilder={name:'',memberIds:[],reason:'',modeId:''}; ui.teamBuilderSearch=''; ui.teamBuilderPage=0; render(); break;
    case 'closeTeamBuilder': ui.showTeamBuilder=false; render(); break;
    case 'tbToggle': { const key=el.dataset.key; const tb=ui.teamBuilder; const mode=state.modes.find(m=>m.id===tb.modeId); const max=mode?mode.teamSize:3;
      const i=tb.memberIds.indexOf(key); if (i>-1) tb.memberIds.splice(i,1); else { tb.memberIds.push(key); if (tb.memberIds.length>max) tb.memberIds.shift(); }
      render(); break; }
    case 'tbPage': ui.teamBuilderPage=parseInt(el.dataset.p,10); render(); break;
    case 'saveTeam': { const tb=ui.teamBuilder; if (tb.memberIds.length<2) break;
      const chars = tb.memberIds.map(k=>resolveMember(...k.split('::'))).filter(Boolean);
      const auto = synergyScore(chars);
      state.teams.unshift({ id:'team-'+Date.now(), name: tb.name || chars.map(c=>c.name).join(' + '), members: tb.memberIds.slice(), reason: tb.reason || auto.reasons[0] || 'Combinación creada manualmente.' });
      ui.showTeamBuilder=false; save(); render(); break; }
    case 'removeTeam': state.teams = state.teams.filter(t=>t.id!==el.dataset.id); save(); render(); break;
    case 'goTierList': ui.view='tierlist'; render(); break;
    case 'tierMode': ui.tierListModeView=el.dataset.key; render(); break;
    case 'addTierList': { const name=(ui.newTierListName||'').trim(); if (!name) break; const id='custom-'+Date.now();
      state.customTierLists.push({id,name}); ui.newTierListName=''; ui.tierListModeView=id; save(); render(); break; }
    case 'removeTierList': { const key=el.dataset.key; state.customTierLists=state.customTierLists.filter(l=>l.id!==key); delete state.tierAssignments[key];
      if (ui.tierListModeView===key) ui.tierListModeView=''; save(); render(); break; }
    case 'assignTier': { const key=el.dataset.key, rank=el.dataset.rank; const active=ui.tierListModeView||(tierDefs()[0]||{}).key;
      state.tierAssignments[active]=state.tierAssignments[active]||{}; state.tierAssignments[active][key]=rank; save(); render(); break; }
    case 'unassignTier': { const key=el.dataset.key; const active=ui.tierListModeView||(tierDefs()[0]||{}).key;
      if (state.tierAssignments[active]) delete state.tierAssignments[active][key]; save(); render(); break; }
    case 'goSettings': ui.view='settings'; render(); break;
    case 'modeAdd': state.modes.push({id:'mode-'+Date.now(), name:'Modo nuevo', teamSize:3, icon:''}); save(); render(); break;
    case 'modeRemove': state.modes.splice(parseInt(el.dataset.i,10),1); save(); render(); break;
    case 'taxAdd': state.taxonomies[el.dataset.cat].push({value:'Nuevo',icon:''}); save(); render(); break;
    case 'taxRemove': state.taxonomies[el.dataset.cat].splice(parseInt(el.dataset.i,10),1); save(); render(); break;
    case 'clearLogo': delete state.images['brand-logo']; save(); render(); break;
    case 'goAdmin': ui.view='admin'; ui.adminEditId=null; ui.adminStep=0; ui.adminDraft=blankDraft(); render(); break;
    case 'adminPick': { const field=el.dataset.field, val=el.dataset.val, multi=el.dataset.multi==='1'; const d=ui.adminDraft;
      if (multi) { const i=d[field].indexOf(val); if (i>-1) d[field].splice(i,1); else { d[field].push(val); if (field==='abilities'&&d[field].length>3) d[field].shift(); } }
      else d[field] = (d[field]===val) ? d[field] : val;
      render(); break; }
    case 'adminUAdd': ui.adminDraft.uniforms.push({name:'',tier:'T2',year:'',skills:[]}); render(); break;
    case 'adminSkAdd': ui.adminDraft.uniforms[parseInt(el.dataset.u,10)].skills.push({slot:'Activa 1',n:'',d:'',dmg:'Ninguno',ii:false,tags:[]}); render(); break;
    case 'adminSkRemove': ui.adminDraft.uniforms[parseInt(el.dataset.u,10)].skills.splice(parseInt(el.dataset.s,10),1); render(); break;
    case 'adminUField': if (el.tagName==='BUTTON'){ ui.adminDraft.uniforms[parseInt(el.dataset.u,10)][el.dataset.field]=el.dataset.val; render(); } break;
    case 'adminStep': ui.adminStep=parseInt(el.dataset.i,10); render(); break;
    case 'adminPrev': ui.adminStep=Math.max(0,ui.adminStep-1); render(); break;
    case 'adminNext': ui.adminStep=Math.min(2,ui.adminStep+1); render(); break;
    case 'adminSave': { const d=ui.adminDraft; const id = ui.adminEditId || ((d.name||'personaje').toLowerCase().replace(/[^a-z0-9]+/g,'-')+'-'+Date.now());
      const uniforms = d.uniforms.map((u,i)=>({...u, id: u.id || (id+'-u'+i)}));
      const newChar = { id, name:d.name||'Sin nombre', c:d.c, f:d.f, r:d.r, t:d.t, ins:d.ins, race:d.race, gender:d.gender, modes:d.modes, abilities:d.abilities, baseSkills:d.baseSkills||[], uniforms };
      if (ui.adminEditId) state.characters = state.characters.map(c=>c.id===ui.adminEditId?newChar:c);
      else state.characters.unshift(newChar);
      if (d.f && !state.taxonomies.factions.some(x=>x.value===d.f)) state.taxonomies.factions.push({value:d.f,icon:''});
      save(); ui.view = ui.adminEditId ? 'detail' : 'roster'; ui.selectedCharId = ui.adminEditId || ui.selectedCharId; ui.adminEditId=null; render(); break; }
    case 'exportJson': { const blob=new Blob([JSON.stringify(state,null,2)],{type:'application/json'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='mff-comparador-backup.json'; a.click(); break; }
    case 'exportCsv': exportCsv(); break;
  }
});
document.addEventListener('change', (e)=>{
  const el = e.target.closest('[data-act]'); if (!el) return;
  const act = el.getAttribute('data-act');
  if (act==='search'){ ui.search=el.value; ui.rosterPage=0; render(); return; }
  if (act==='uploadImg'){ const f=el.files[0]; if (f) readFileAsDataUrl(f, url=>{ state.images[el.dataset.imgid]=url; save(); render(); }); return; }
  if (act==='importJson'){ const f=el.files[0]; if (f){ const r=new FileReader(); r.onload=()=>{ try { state=Object.assign(defaultState(), JSON.parse(r.result)); save(); render(); } catch(err){ alert('Archivo inválido'); } }; r.readAsText(f); } return; }
  if (act==='tbName'){ ui.teamBuilder.name=el.value; return; }
  if (act==='tbReason'){ ui.teamBuilder.reason=el.value; return; }
  if (act==='tbMode'){ const mode=state.modes.find(m=>m.id===el.value); const max=mode?mode.teamSize:3; ui.teamBuilder.modeId=el.value; ui.teamBuilder.memberIds=ui.teamBuilder.memberIds.slice(-max); render(); return; }
  if (act==='tbSearch'){ ui.teamBuilderSearch=el.value; ui.teamBuilderPage=0; render(); return; }
  if (act==='newTierListName'){ ui.newTierListName=el.value; return; }
  if (act==='modeIcon'){ state.modes[el.dataset.i].icon=el.value; save(); return; }
  if (act==='modeName'){ state.modes[el.dataset.i].name=el.value; save(); return; }
  if (act==='modeSize'){ state.modes[el.dataset.i].teamSize=Math.max(2,parseInt(el.value,10)||3); save(); return; }
  if (act==='taxIcon'){ state.taxonomies[el.dataset.cat][el.dataset.i].icon=el.value; save(); return; }
  if (act==='taxValue'){ state.taxonomies[el.dataset.cat][el.dataset.i].value=el.value; save(); return; }
  if (act==='adminField'){ ui.adminDraft[el.dataset.field]=el.value; return; }
  if (act==='adminUField'){ ui.adminDraft.uniforms[el.dataset.u][el.dataset.field]=el.value; return; }
  if (act==='adminSkField'){ const sk=ui.adminDraft.uniforms[el.dataset.u].skills[el.dataset.s]; const f=el.dataset.field;
    sk[f] = el.type==='checkbox' ? el.checked : el.value; if (f==='slot'||f==='dmg') render(); return; }
});
// Drag & drop for tier list
document.addEventListener('dragstart', (e)=>{ const el=e.target.closest('[data-act="dragItem"]'); if (el){ ui.admin_field_dragKey = el.dataset.key; e.dataTransfer.setData('text/plain', el.dataset.key); } });
document.addEventListener('dragover', (e)=>{ if (e.target.closest('[data-act="dropRank"],[data-act="dropUnranked"]')) e.preventDefault(); });
document.addEventListener('drop', (e)=>{
  const rankEl = e.target.closest('[data-act="dropRank"]'); const poolEl = e.target.closest('[data-act="dropUnranked"]');
  if (!rankEl && !poolEl) return;
  e.preventDefault();
  const key = ui.admin_field_dragKey; if (!key) return;
  const active = ui.tierListModeView || (tierDefs()[0]||{}).key;
  state.tierAssignments[active] = state.tierAssignments[active] || {};
  if (rankEl) state.tierAssignments[active][key] = rankEl.dataset.rank;
  else delete state.tierAssignments[active][key];
  ui.admin_field_dragKey = null; save(); render();
});

function exportCsv(){
  const rows = [['personaje_id','personaje_nombre','clase','faccion','tier','instinto','uniforme_id','uniforme_nombre','uniforme_tier','uniforme_anio','slot','habilidad','descripcion','tipo_dano']];
  state.characters.forEach(ch=>{
    if (!ch.uniforms.length) rows.push([ch.id,ch.name,ch.c,ch.f,ch.t,ch.ins,'','','','','','','','']);
    ch.uniforms.forEach(u=>{
      const skills = (ch.baseSkills||[]).concat(u.skills);
      if (!skills.length) rows.push([ch.id,ch.name,ch.c,ch.f,ch.t,ch.ins,u.id,u.name,u.tier,u.year,'','','','']);
      skills.forEach(sk=>rows.push([ch.id,ch.name,ch.c,ch.f,ch.t,ch.ins,u.id,u.name,u.tier,u.year,sk.slot,sk.n,sk.d,sk.dmg]));
    });
  });
  const csv = rows.map(r=>r.map(c=>'"'+String(c==null?'':c).replace(/"/g,'""')+'"').join(',')).join('\n');
  const blob = new Blob([csv],{type:'text/csv'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='mff-personajes-uniformes.csv'; a.click();
}

render();
})();
