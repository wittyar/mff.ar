/* TA GUIANAEL MFF — app en JS vanilla, sin build. La sirve desktop/servidor.py (la app de
 * escritorio): sin ese servidor no arranca, porque la capa del usuario se guarda a través de él.
 *
 * Reglas de datos (importante):
 *   - data.js es la ÚNICA fuente de personajes, uniformes, skills, imágenes y tier lists importadas.
 *     Nunca se copia a la capa: regenerar data.js se ve al recargar, sin borrar nada.
 *   - La capa del usuario vive en capa.json, en la carpeta de datos (GET/PUT /api/capa): ediciones
 *     y personajes propios, equipos, tier lists propias, cambios sobre las importadas, imágenes
 *     subidas, atributos marcados, hojas de ruta, topes cargados y preferencias.
 */
(function () {
'use strict';

// ============================================================================
// DATOS DE data.js (solo lectura)
// Al cargar app.js solo se toman las variables de data.js; nada las interpreta hasta que
// arrancar() confirma que son del formato de esta versión (si no, pantallaDatos() baja las
// publicadas). Lo que se deriva de ellas se arma en iniciarDatos(), después de esa
// confirmación: con datos de otro formato, o sin data.js, un campo puede no estar.
// ============================================================================
const SEED           = window.MFF_SEED;
const CHARS_SEED     = window.MFF_SEED_CHARACTERS || [];
const IMAGES_SEED    = window.MFF_SEED_IMAGES || {};
const TIERLISTS_SEED = window.MFF_SEED_TIERLISTS || [];
const ASSIGN_SEED    = window.MFF_SEED_TIER_ASSIGNMENTS || {};
const SKILLS         = window.MFF_SKILLS || {};   // skills por retrato
const PERFIL         = window.MFF_PERFIL;         // con qué pega cada retrato (scripts/modelo.py)
const ANALISIS       = window.MFF_ANALISIS;       // lo que hace cada retrato con sus skills (scripts/modelo.py)
const CATALOGO       = window.MFF_CATALOGO;       // catálogo de efectos (scripts/contenido/catalogo.json)
const BONOS          = window.MFF_BONOS;          // bonos de equipo (scripts/bonos.py)
const STRIKERS       = window.MFF_STRIKERS;       // strikers de cada personaje (scripts/strikers.py)
const ROLES_LISTAS   = window.MFF_ROLES_LISTAS;   // rol que da cada fila de las listas de PvP y PvE (scripts/contenido/roles_listas.json)
const VALOR          = window.MFF_VALOR;          // cuánto vale un equipo en PvP y en PvE (scripts/contenido/valor_equipos.json)
const GLOSARIO       = window.MFF_GLOSARIO;       // glosario de skills del juego, inglés y coreano (scripts/contenido/glosario.json)
const TB             = window.MFF_TABLAS || {};   // patrones y etiquetas, en los dos idiomas
const BUFFS          = window.MFF_BUFFS || {};    // buffs clave por retrato
const CTPS           = window.MFF_CTPS || [];     // C.T.P.s (scripts/fuentes.py)
const ARTES          = window.MFF_ARTEFACTOS || []; // artefactos exclusivos, por retrato base
const DEFAULT_ROWS   = window.MFF_DEFAULT_TIER_ROWS || [{id:'S',label:'S'},{id:'A',label:'A'},{id:'B',label:'B'},{id:'C',label:'C'},{id:'D',label:'D'}];
const SLOT_ORDER     = ['Leader Skill','Passive','Tier-2 Passive','Uniform Passive',
                        'Active 1','Active 2','Active 3','Active 4','Active 5','Active Ult','Striker Skill'];
const SLOT_ES = { 'Leader Skill':'Liderazgo', 'Passive':'Pasiva', 'Tier-2 Passive':'Pasiva T2',
  'Uniform Passive':'Pasiva de uniforme', 'Striker Skill':'Striker', 'Active Ult':'Definitiva',
  'Active 1':'Activa 1','Active 2':'Activa 2','Active 3':'Activa 3','Active 4':'Activa 4','Active 5':'Activa 5' };
const REMOVED        = null; // marca explícita: entrada de una lista importada que el usuario quitó

// ============================================================================
// CAPA DE USUARIO
// ============================================================================
function blankUser () {
  return {
    charEdits: {},                    // id de data.js -> personaje editado (reemplaza al del seed)
    charNew: [],                      // personajes creados a mano
    teams: [],                        // equipos de tu cuenta: {id, name, members (claves, en orden canónico), lider (la clave del líder declarado), reason, modeId}
    favoritos: [],                    // equipos de 3 marcados con ★ en las combinaciones: {id, members, ctx: 'pvp', 'pve' o null}
    descartados: [],                  // equipos de 3 ocultos de las combinaciones: sus tres personajes (ids, en orden), con cualquier uniforme
    lists: [],                        // tier lists propias: {id,name,rows}
    assign: {},                       // listId -> {clave: [filaId, ...] | null}
    images: {},                       // 'portrait-x' / 'fullbody-x' / 'brand-logo' subidos
    marcas: {},                       // '<retrato>::<tipo de skill>' -> {it:1, gb:1, ...}
    modes: [],                        // modos propios: {id, name, teamSize}; los del juego salen de MFF_MODOS
    ruta: {},                         // personaje -> id del último paso de la hoja de ruta que ya hizo
    topes: {},                        // personaje -> {stat: {v: pantalla, b: buffs}} de la calculadora de topes
    mesa: { members: [], modeId: '', abxDia: 1, abxDif: '', name: '' },  // la mesa de trabajo (MESA): claves, el líder primero
    prefs: { lang:'es', view:'grid', sort:'name', dir:1, filtersOpen:false, refList: (TIERLISTS_SEED[0]||{}).id || '',
             kind:'todo', objetivo:'', atributo:'', para:'', restr:'',
             filters:{ c:[], r:[], t:[], f:[], ins:[], race:[], origin:[], ab:[], lid:[], sop:[] },
             flags:{ t4:false, trans:false, nuevo:false } }
  };
}
let U = blankUser();                   // la real llega del servidor en arrancar()
/** Capa guardada (o importada) -> capa completa: completa lo que falte con los valores por
 *  defecto y convierte formatos viejos. Es el único camino de entrada de una capa. */
function normalizarCapa (saved) {
  const base = blankUser();
  const sp = saved.prefs || {};
  // Los valores por defecto de las preferencias se toman antes de mezclar:
  // Object.assign(base, saved) reemplaza base.prefs entera por la guardada, y una capa
  // de una versión anterior (sin filters o sin flags) dejaba la app en blanco.
  const prefs = base.prefs, filters = prefs.filters, flags = prefs.flags;
  const u = Object.assign(base, saved);
  u.prefs = Object.assign(prefs, sp);
  u.prefs.filters = Object.assign(filters, sp.filters || {});
  u.prefs.flags = Object.assign(flags, sp.flags || {});
  // Una entrada guardaba una sola fila (texto); desde que puede estar en varias filas
  // de la misma lista guarda una lista de filas. Las capas viejas se convierten acá.
  for (const l in u.assign) for (const k in u.assign[l]) {
    if (typeof u.assign[l][k] === 'string') u.assign[l][k] = [u.assign[l][k]];
  }
  // Los modos de juego salen ahora de la sección Modos, con su tamaño de equipo según la
  // fuente. Las capas viejas traían copiados cuatro modos de ejemplo sin fuente (uno,
  // "Incursión", ni siquiera es un modo del juego): se quitan si siguen sin tocar.
  const EJEMPLO = { pvp:'PvP|3', alianza:'Alianza|3', incursion:'Incursión|5', sombras:'Mundo de Sombras|3' };
  u.modes = (u.modes || []).filter(m => EJEMPLO[m.id] !== m.name + '|' + m.teamSize);
  // Los favoritos guardan el contexto del orden en que se marcaron; los de antes no lo traen y quedan sin
  // contexto, que es como se mostraban.
  for (const f of u.favoritos) if (!('ctx' in f)) f.ctx = null;
  // Los equipos se guardan en orden canónico (mesaGuardar); los de antes, en el orden en que se armaron.
  for (const tt of u.teams) tt.members = tt.members.slice().sort();
  return u;
}
/** Lee capa.json. Sin archivo (primer uso) es una capa vacía; un archivo ilegible es un
 *  error que corta el arranque: seguir con una capa vacía y guardar la pisaría. */
async function cargarCapa () {
  const { capa } = await apiLocal('/api/capa');
  return capa ? normalizarCapa(capa) : blankUser();
}
/** Guarda la capa. Un PUT a la vez y siempre con el último estado: si llegan cambios
 *  mientras uno viaja, sale uno más al terminar. Un error queda a la vista con un botón
 *  para reintentar, y cerrar la ventana con algo sin guardar pide confirmación. */
const GUARDADO = { enCurso: false, pendiente: false, error: null };
function saveUser () {
  if (GUARDADO.enCurso) { GUARDADO.pendiente = true; return; }
  GUARDADO.enCurso = true; GUARDADO.pendiente = false;
  fetch('/api/capa', { method: 'PUT', headers: { 'X-MFF': '1', 'Content-Type': 'application/json' }, body: JSON.stringify(U) })
    .then(async r => { if (!r.ok) throw new Error((await r.json()).error || ('HTTP ' + r.status)); GUARDADO.error = null; })
    .catch(e => { GUARDADO.error = e.message; verificarServidor(); })
    .finally(() => { GUARDADO.enCurso = false; pintarAvisos(); if (GUARDADO.pendiente) saveUser(); });
}
window.addEventListener('beforeunload', (e) => {
  if (GUARDADO.enCurso || GUARDADO.pendiente || GUARDADO.error) { e.preventDefault(); e.returnValue = ''; }
});

// ---- vistas derivadas (data.js + capa de usuario) ----
let CHARS = [], CHAR_BY_ID = {}, LISTS = [];
let CONSULTA = null;                   // última consulta de combinaciones de 3 (pestaña Equipos); se vacía en rebuild()
function rebuild () {
  CONSULTA = null;
  _ROL.clear();
  _PUESTO_SC.clear();
  _ULTIMO.clear();
  CHARS = CHARS_SEED.map(c => U.charEdits[c.id] || c).concat(U.charNew);
  CHAR_BY_ID = {}; CHARS.forEach(c => { CHAR_BY_ID[c.id] = c; });
  LISTS = TIERLISTS_SEED.concat(U.lists);
  declararLideres();
}
// LÍDER DECLARADO (Ezequiel, 6 de octubre de 2026: «una de las posiciones corresponde al líder y necesita estar declarado
// como tal para el cálculo de estadísticas»). Cada equipo guardado lleva su líder (lider: la clave de un integrante),
// y todo lo que se calcula del equipo (la sinergia, lo que le llega a cada uno, los C.T.P., cómo entraría otro) usa ese.
// Los equipos guardados antes de la 1.0.25 no lo traen: se les declara el que mostraba su tarjeta (el de la sinergia de
// la app; sin ningún liderazgo que sume, el primero en orden canónico), se guarda y Equipos dice cuáles fueron.
function declararLideres () {
  const sin = U.teams.filter(tt => !tt.lider);
  if (!sin.length) return;
  for (const tt of sin) {
    const vs = tt.members.map(k => variant(...k.split('::'))).filter(Boolean), l = liderDe(vs, null);
    tt.lider = (l || vs[0]).key;
  }
  ui.avisoLideres = sin.map(tt => tt.name);
  saveUser();
}
/** El líder declarado de un equipo guardado, entre sus integrantes (vs). */
function liderEquipo (tt, vs) {
  const l = vs.find(x => x.key === tt.lider);
  if (!l) throw new Error('equipo guardado con un líder que no es de sus integrantes: ' + tt.name);
  return l;
}
function commit () { saveUser(); rebuild(); render(); }

function imgUrl (id) { return U.images[id] || IMAGES_SEED[id] || ''; }
function listById (id) { return LISTS.find(l => l.id === id) || null; }
/** Nombre de la lista en el idioma activo. Las listas propias solo tienen uno. */
function listName (l) { return l ? ((LANG === 'en' && l.nameEn) || l.name) : ''; }
function rowsOf (list) { return (list && list.rows && list.rows.length) ? list.rows : DEFAULT_ROWS; }
/** Las listas se muestran agrupadas: las cinco principales de thanosvibs (general,
 *  soportes y las de modo), el resto de las que publica la comunidad, y las propias. */
const GRUPOS_LISTA = [['principal', 'tl_g_main'], ['comunidad', 'tl_g_community'], ['propia', 'tl_g_own']];
function listasAgrupadas () {
  return GRUPOS_LISTA.map(([g, k]) => ({ g, k, ls: LISTS.filter(l => (l.group || 'propia') === g) }))
                     .filter(x => x.ls.length);
}
/** Plantillas de filas para las listas propias. Los rótulos quedan en el idioma en que
 *  se creó la lista: después son del usuario y se editan como cualquier fila. */
const PLANTILLAS = [
  { id:'rango',    k:'tp_rank',      filas: () => ['S', 'A', 'B', 'C', 'D'] },
  { id:'rangomas', k:'tp_rank_plus', filas: () => ['SS', 'S', 'A', 'B', 'C', 'D'] },
  { id:'uso',      k:'tp_role',      filas: () => [t('tp_r_lead'), t('tp_r_main'), t('tp_r_support'), t('tp_r_striker')] },
  { id:'ctp',      k:'tp_ctp',       filas: () => CTPS.map(c => c.name) },
  { id:'vacia',    k:'tp_empty',     filas: () => [t('tp_new_row')] },
];
function filasDePlantilla (id) {
  const p = PLANTILLAS.find(x => x.id === id) || PLANTILLAS[0];
  const base = Date.now();
  return p.filas().map((label, i) => ({ id: 'f-' + base + '-' + i, label }));
}
function esPropia (list) { return !!list && U.lists.some(l => l.id === list.id); }
/** Qué se ubica en una lista. Las importadas son siempre de personajes; las propias
 *  pueden ser de C.T.P.s, de artefactos o de tus equipos. */
const TIPOS_LISTA = [['personajes', 'tk_chars'], ['ctp', 'tk_ctp'], ['artefacto', 'tk_art'], ['equipo', 'tk_team']];
function tipoLista (list) { return (list && list.kind) || 'personajes'; }
/** Personaje del roster cuyo retrato base es p (los artefactos vienen por retrato). */
function charDeRetrato (p) { return CHARS.find(c => c.p === p) || null; }
/** Entradas ubicables en una lista: {key, nom, sub, img} y, si es un personaje, su variante. */
function itemsDeLista (list) {
  switch (tipoLista(list)) {
    case 'ctp': return CTPS.map(c => ({ key: 'ctp:' + c.id, nom: 'C.T.P. of ' + c.name, sub: '', img: imgUrl('ctp-' + c.id) }));
    case 'artefacto': return ARTES.map(a => { const ch = charDeRetrato(a.p);
      return { key: 'art:' + a.p, nom: a.name, sub: ch ? ch.name : a.p, cid: ch && ch.id,
               img: imgUrl('art-' + a.p) || (ch ? imgUrl('portrait-' + ch.id) : '') }; });
    case 'equipo': return U.teams.map(eq => { const vs = eq.members.map(k => variant(...k.split('::'))).filter(Boolean);
      return { key: 'eq:' + eq.id, nom: eq.name, sub: vs.map(fullLabel).join(' + '),
               img: vs[0] ? imgUrl('portrait-' + vs[0].id) : '' }; });
    default: return allVariants().map(v => ({ key: v.key, nom: v.name, sub: v.uid ? v.sub : '', v,
                                              img: imgUrl('portrait-' + v.id) }));
  }
}
/** Asignaciones efectivas de una lista: las de data.js con los cambios del usuario encima. */
function assignOf (listId) {
  const out = Object.assign({}, ASSIGN_SEED[listId] || {});
  const mine = U.assign[listId] || {};
  for (const k in mine) { if (mine[k] === REMOVED) delete out[k]; else out[k] = mine[k]; }
  return out;
}
/** Filas en las que está una entrada (vacío si no está ubicada). Una entrada puede
 *  estar en varias filas de la misma lista: muchas listas son por categoría. Lee la
 *  entrada sola (lo mismo que assignOf(listId)[key], sin copiar la lista entera). */
function filasDe (listId, key) {
  const mia = (U.assign[listId] || {})[key];
  if (mia === REMOVED) return [];
  return mia || (ASSIGN_SEED[listId] || {})[key] || [];
}
/** Deja una entrada en exactamente estas filas, en el orden de la lista. Sin filas queda
 *  sin ubicar: en una importada eso es una marca explícita (REMOVED) sobre la fuente. */
function setFilas (listId, key, filas) {
  const orden = rowsOf(listById(listId)).map(r => r.id);
  const limpias = [...new Set(filas)].filter(r => orden.includes(r)).sort((a, b) => orden.indexOf(a) - orden.indexOf(b));
  U.assign[listId] = U.assign[listId] || {};
  if (limpias.length) U.assign[listId][key] = limpias;
  else if ((ASSIGN_SEED[listId] || {})[key]) U.assign[listId][key] = REMOVED;
  else delete U.assign[listId][key];
  commit();
}

// ============================================================================
// IDIOMA
// ============================================================================
// Una sola tabla con los dos idiomas por clave: así es imposible que una cadena
// exista en uno y falte en el otro. El vocabulario del dominio (clases, roles,
// slots, etiquetas) viaja en data.js, generado por el mismo pipeline que lo tradujo.
const VOCAB_EN = window.MFF_VOCAB_EN || {};
const T = {
  nav_roster:        { es:'Roster',              en:'Roster' },
  nav_tierlists:     { es:'Tier lists',          en:'Tier lists' },
  nav_teams:         { es:'Equipos',             en:'Teams' },
  nav_modes:         { es:'Modos',               en:'Modes' },
  md_title:          { es:'Modos de juego',      en:'Game modes' },
  md_note:           { es:'Qué da cada modo, cómo armar el equipo y con quién. Todo sale de fuentes citadas: donde no hay fuente, no se afirma.',
                       en:'What each mode gives, how to build the team and with whom. Everything comes from cited sources: where there is none, nothing is claimed.' },
  md_guide:          { es:'Guía de thanosvibs', en:'thanosvibs guide' },
  md_guide_old:      { es:'hay versión nueva:',  en:'new version out:' },
  md_guide_old_t:    { es:'El contenido curado se escribió sobre una versión anterior de la guía: puede haber recomendaciones desactualizadas.',
                       en:'The curated content was written on an earlier guide version: some recommendations may be outdated.' },
  md_f_todos:        { es:'Todos',               en:'All' },
  md_f_pve:          { es:'PvE',                 en:'PvE' },
  md_f_pvp:          { es:'PvP',                 en:'PvP' },
  md_f_diario:       { es:'Diario',              en:'Daily' },
  md_f_semanal:      { es:'Semanal',             en:'Weekly' },
  md_team:           { es:'Equipo',              en:'Team' },
  md_what:           { es:'Qué da y qué hacer',  en:'What it gives and what to do' },
  md_source:         { es:'Fuente',              en:'Source' },
  md_recs:           { es:'Personajes recomendados', en:'Recommended characters' },
  md_no_list:        { es:'Ninguna lista publicada cubre este modo.', en:'No published list covers this mode.' },
  md_see_list:       { es:'Ver lista',           en:'Open list' },
  md_guide_mentions: { es:'Mencionados en la guía', en:'Mentioned in the guide' },
  md_guide_mentions_note:{ es:'(derivado: la guía nombra el modo al hablar de ellos)', en:'(derived: the guide names the mode when talking about them)' },
  md_abx:            { es:'Restricciones y equipos por día', en:'Restrictions and teams by day' },
  md_cancel_read:    { es:'En cada integrante, "Parálisis: 1/4" quiere decir que sus skills 1 y 4 aplican parálisis (6 = la definitiva).',
                       en:'On each member, "Paralyze: 1/4" means their skills 1 and 4 apply Paralyze (6 = the ultimate).' },
  md_day:            { es:'Día del ciclo',       en:'Cycle day' },
  md_day_note:       { es:'Ciclo de {n} días. La fuente no dice qué día es hoy: elegilo mirando el juego.',
                       en:'{n}-day cycle. The source does not say which day is today: pick it from the game.' },
  md_no_restr:       { es:'sin restricción',     en:'no restriction' },
  md_no_teams:       { es:'La fuente no recomienda equipos para este día.', en:'The source recommends no teams for this day.' },
  md_added:          { es:'agregado en',         en:'added in' },
  md_r_lead:         { es:'Líder',               en:'Lead' },
  md_r_dps:          { es:'DPS',                 en:'DPS' },
  md_r_leaddps:      { es:'Líder y DPS',         en:'Lead and DPS' },
  md_r_support:      { es:'Soporte',             en:'Support' },
  md_ctps:           { es:'C.T.P. recomendados', en:'Recommended C.T.P.s' },
  md_reforged:       { es:'Reforjado',           en:'Reforged' },
  md_go_pve:         { es:'Ver armado de PvE (ISO, urus, gear, opciones de uniforme) ↓', en:'See the PvE build (ISO, Uru, gear, uniform options) ↓' },
  md_go_pvp:         { es:'Ver armado de PvP (ISO, urus, gear, opciones de uniforme) ↓', en:'See the PvP build (ISO, Uru, gear, uniform options) ↓' },
  md_builds:         { es:'Armado según el tipo de modo', en:'Build by mode type' },
  md_builds_note:    { es:'Reglas generales de la guía, cruzadas con la wiki. La ficha de cada personaje las aplica a su tipo de ataque.',
                       en:"General rules from the guide, cross-checked with the wiki. Each character's sheet applies them to its attack type." },
  md_urus:           { es:'Urus',                en:'Urus' },
  md_uru_pvp:        { es:'PvP: igual dos urus de ataque por pieza y priorizar la recarga; después vida, o evasión en personajes de evasión.',
                       en:'PvP: still two attack Urus per gear and prioritise Skill Cooldown; then HP, or Dodge for Dodge-heavy characters.' },
  md_gear4:          { es:'Opción del 4.º gear', en:'4th gear option' },
  md_obelisk:        { es:'Custom gear (obelisco)', en:'Custom gear (Obelisk)' },
  md_uni_opts:       { es:'Opciones de uniforme', en:'Uniform options' },
  md_own_attack:     { es:'el ataque del personaje', en:"the character's attack" },
  iso_blanca:        { es:'blanca',              en:'white' },
  iso_roja:          { es:'roja',                en:'red' },
  iso_azul:          { es:'azul',                en:'blue' },
  iso_verde:         { es:'verde',               en:'green' },
  iso_naranja:       { es:'naranja',             en:'orange' },
  iso_amarilla:      { es:'amarilla',            en:'yellow' },
  iso_violeta:       { es:'violeta',             en:'purple' },
  iso_caos:          { es:'caos',                en:'chaos' },
  us_lists:          { es:'Tier lists',          en:'Tier lists' },
  us_in_n_lists:     { es:'está en {n} de {t}',  en:'in {n} of {t}' },
  us_atk:            { es:'Tipo de ataque (derivado)', en:'Attack type (derived)' },
  us_atk_note:       { es:'Derivado de sus skills activas: el stat con el que escala su % de daño. Define qué urus y qué piedras ISO le sirven.',
                       en:'Derived from its active skills: the stat its damage % scales with. It decides which Urus and ISO stones suit it.' },
  us_atk_none:       { es:'Sus skills activas no hacen daño.', en:'Its active skills deal no damage.' },
  at_fisico:         { es:'Ataque físico',       en:'Physical Attack' },
  at_energia:        { es:'Ataque de energía',   en:'Energy Attack' },
  at_vida:           { es:'Vida (su daño escala con la vida)', en:'HP (its damage scales with HP)' },
  at_mixto:          { es:'Mixto',               en:'Mixed' },
  us_sup:            { es:'Lo que le da al equipo', en:'What it gives the team' },
  us_sup_none:       { es:'thanosvibs no le lista efectos de líder ni de soporte a este retrato.',
                       en:'thanosvibs lists no lead or support effects for this portrait.' },
  us_otorga:         { es:'Su Leader Skill da un poder que ninguna fuente publica («Give Power»: la API no dice qué otorga ni por cuánto tiempo).',
                       en:'Its Leader Skill grants a power no source publishes ("Give Power": the API does not say what it grants or for how long).' },
  sp_leader:         { es:'Liderazgo',           en:'Leadership' },
  sp_leader2:        { es:'Liderazgo (secundario)', en:'Leadership (Secondary)' },
  sp_passive:        { es:'Pasiva 4★',           en:'4★ Passive' },
  sp_passive2:       { es:'Pasiva 4★ (secundaria)', en:'4★ Passive (Secondary)' },
  sp_t2:             { es:'Pasiva de Tier-2',    en:'Tier-2 Passive' },
  sp_t22:            { es:'Pasiva de Tier-2 (secundaria)', en:'Tier-2 Passive (Secondary)' },
  sp_uniform:        { es:'Efecto de uniforme',  en:'Uniform Effect' },
  sp_uniform2:       { es:'Efecto de uniforme (secundario)', en:'Uniform Effect (Secondary)' },
  sp_artifact:       { es:'Skill exclusiva del artefacto', en:'Artifact Exclusive Skill' },
  sp_inst:           { es:'del instinto total',  en:'of total Instinct' },
  sp_cap:            { es:'acumula hasta',       en:'stacks up to' },
  sp_all:            { es:'Sin restricción',     en:'No restriction' },
  sp_applies:        { es:'Aplica a',            en:'Applies to' },
  sp_corrected:      { es:'Corregido: la fuente dice', en:'Corrected: the source says' },
  sp_r_Ability:      { es:'habilidad',           en:'ability' },
  sp_r_Type:         { es:'clase',               en:'class' },
  sp_r_Allies:       { es:'raza',                en:'race' },
  sp_r_Side:         { es:'bando',               en:'side' },
  sp_r_Character:    { es:'personaje',           en:'character' },
  sp_cd:             { es:'recarga',             en:'cooldown' },
  sp_req:            { es:'Requiere',            en:'Requires' },
  sp_notable:        { es:'Notable',             en:'Notable' },
  sp_notable_t:      { es:'thanosvibs lo marca como notable', en:'thanosvibs marks it as notable' },
  sp_est:            { es:'a {n}★',              en:'at {n}★' },
  sp_src_api:        { es:'según la skill del juego', en:'per the game skill' },
  sp_src_api_t:      { es:'Leads & Supports no publica este liderazgo: sale de la Leader Skill de la API de skills de thanosvibs.',
                       en:'Leads & Supports does not publish this leadership: it comes from the Leader Skill in the thanosvibs skills API.' },
  sp_src_otorga_t:   { es:'Leads & Supports no publica este liderazgo: sale de la Leader Skill de la API de skills de thanosvibs, que no dice qué otorga su «Give Power»; eso lo dice la ficha del juego.',
                       en:'Leads & Supports does not publish this leadership: it comes from the Leader Skill in the thanosvibs skills API, which does not say what its "Give Power" grants; the in-game profile does.' },
  sp_np:             { es:'Buena elección para empezar (thanosvibs)', en:'New player pick (thanosvibs)' },
  us_guide:          { es:'En la guía de principiantes', en:"In the Beginner's Guide" },
  us_guide_none:     { es:'La guía no lo nombra en sus secciones de personajes.', en:'The guide does not name it in its character sections.' },
  us_obelisk:        { es:'Obelisco',            en:'Obelisk' },
  us_cancels:        { es:'Controles que aplica (cortan a los jefes):', en:'Controls it applies (they cancel the bosses):' },
  us_cancels_none:   { es:'No aplica ninguno de los controles que cortan a los jefes de {m}.',
                       en:'It applies none of the controls that cancel {m} bosses.' },
  us_cancels_ni:     { es:' ni de ',             en:' or ' },
  us_equipos:        { es:'Cómo se arma un equipo, según la guía', en:'How a team is built, per the guide' },
  us_equipos_tema:   { es:'Equipos temáticos',   en:'Themed teams' },
  us_abx_teams:      { es:'Equipos recomendados que lo incluyen:', en:'Recommended teams that include it:' },
  us_abx_none:       { es:'No está en los equipos recomendados.', en:'Not in the recommended teams.' },
  us_day:            { es:'Día',                 en:'Day' },
  ar_title:          { es:'Cómo armarlo',        en:'How to build it' },
  ar_note:           { es:'El C.T.P. que le asignan las fuentes, su artefacto, el ISO-8 y el obelisco de la guía de armado, las opciones del uniforme y las reglas generales de la guía de principiantes aplicadas a su tipo de ataque.',
                       en:'The C.T.P. the sources assign it, its artifact, the building guide’s ISO-8 and Obelisk, the uniform’s options and the Beginner’s Guide general rules applied to its attack type.' },
  ar_more:           { es:'Reglas completas en Modos ↓', en:'Full rules in Modes ↓' },
  ar_rules:          { es:'Reglas generales de la guía para su tipo de ataque: ISO-8 y urus',
                       en:'General guide rules for its attack type: ISO-8 and urus' },
  ar_ctp_nolist:     { es:'No está en esa lista.', en:'Not in that list.' },
  ar_ctp_noimport:   { es:'Esa lista no está entre las importadas: sincronizá las tier lists.', en:'That list is not among the imported ones: sync the tier lists.' },
  ar_ctp_guide:      { es:'Sugeridos por la guía de principiantes:', en:"Suggested by the Beginner's Guide:" },
  ar_iso_pve:        { es:'PvE: uno de los {n} sets de ataque.', en:'PvE: one of the {n} Attack sets.' },
  ar_uru_fisico:     { es:'Urus de ataque físico.', en:'Physical Attack Urus.' },
  ar_uru_energia:    { es:'Urus de ataque de energía.', en:'Energy Attack Urus.' },
  ar_uru_vida:       { es:'Su daño escala con la vida: la guía no da una regla de urus para este caso (sí dice que para estos personajes la vida importa).',
                       en:'Its damage scales with HP: the guide gives no Uru rule for this case (it does say HP matters for these characters).' },
  ar_uru_mixto:      { es:'Pega con ataque físico y de energía: la guía no da una regla de urus para este caso.',
                       en:'It hits with both Physical and Energy Attack: the guide gives no Uru rule for this case.' },
  ar_uru_ninguno:    { es:'Sus skills activas no hacen daño: la regla de urus de ataque no aplica.',
                       en:'Its active skills deal no damage: the attack Uru rule does not apply.' },
  ar_art:            { es:'Artefacto',           en:'Artifact' },
  ar_art_none:       { es:'thanosvibs no le lista artefacto exclusivo.', en:'thanosvibs lists no exclusive artifact for it.' },
  ar_score_t:        { es:'Puntaje de thanosvibs, de 0 a 3', en:'thanosvibs score, 0 to 3' },
  ar_since:          { es:'desde la',            en:'since' },
  ar_nodata:         { es:'sin dato',            en:'no data' },
  ar_nodata_t:       { es:'La fuente no trae este valor para este nivel de estrellas.', en:'The source has no value for this star level.' },
  ar_obtain:         { es:'Cómo se consigue',    en:'How to get it' },
  ar_corregida:      { es:'Corregida con el juego: thanosvibs dice «{tv}».', en:'Corrected with the game: thanosvibs says "{tv}".' },
  ga_title:          { es:'Guía de armado de Cynicalex', en:"Cynicalex's Character Building Guide" },
  ga_none:           { es:'La guía de armado no lo incluye.', en:'The building guide does not include it.' },
  ga_no_data:        { es:'Los datos cargados no traen la guía de armado: son de antes de que la app la sumara. Actualizá los datos desde Ajustes.',
                       en:'The loaded data has no building guide: it predates the app adding it. Update the data from Settings.' },
  ga_best_uni:       { es:'Mejor uniforme:',     en:'Best uniform:' },
  ga_this_uni:       { es:'el que estás viendo', en:'the one you are viewing' },
  ga_tier:           { es:'Su tier list:',       en:'Its tier list:' },
  ga_acq:            { es:'Cómo se consigue:',   en:'How to get it:' },
  ga_unknown:        { es:'La app no interpreta este valor de la guía: va tal cual.', en:'The app does not interpret this guide value: shown as is.' },
  ga_rot:            { es:'Rotación de proc',    en:'Proc rotation' },
  ga_rotc:           { es:'Rotación con su mejor C.T.P.', en:'Best C.T.P. rotation' },
  ga_proc:           { es:'Skill de proc / frenesí', en:'Proc / Frenzy skill' },
  ga_rot_none:       { es:'La guía de armado no le da rotación.', en:'The building guide gives it no rotation.' },
  ga_rot_legend:     { es:'Notación de la guía de armado', en:"Building guide's notation" },
  ga_ctp_title:      { es:'Según la guía de armado de Cynicalex:', en:"Per Cynicalex's building guide:" },
  ga_ctp_none:       { es:'La guía de armado no le asigna C.T.P.', en:'The building guide assigns it no C.T.P.' },
  ga_ctp_mejor:      { es:'Mejor',               en:'Best' },
  ga_ctp_segundo:    { es:'2.º mejor',           en:'2nd best' },
  ga_ctp_pve:        { es:'Meta PvE',            en:'PvE meta' },
  ga_ctp_pve_alt:    { es:'Fuera del meta PvE',  en:'PvE off-meta' },
  ga_ctp_pvp:        { es:'Meta PvP',            en:'PvP meta' },
  ga_ctp_pvp_alt:    { es:'Fuera del meta PvP',  en:'PvP off-meta' },
  ga_ctp_notes:      { es:'Notas de la guía sobre C.T.P.', en:"The guide's C.T.P. notes" },
  ctp_eq_title:      { es:'C.T.P. recomendados: {a} · {b} · Ideal CTP List', en:'Recommended C.T.P.: {a} · {b} · Ideal CTP List' },
  ctp_rec_title:     { es:'Recomendado, en cada contexto (lo mismo que dicen sus tarjetas de equipo): lo que dice la guía de armado de Cynicalex y lo que dice la Ideal CTP List (de la comunidad, en thanosvibs), cada uno con su fuente. Pueden no coincidir.',
                       en:'Recommended, in each context (what its team cards say): what Cynicalex\'s building guide says and what the Ideal CTP List (community, on thanosvibs) says, each with its source. They may disagree.' },
  ctp_ideal_col:     { es:'Ideal CTP List',      en:'Ideal CTP List' },
  ctp_sin_ideal:     { es:'La Ideal CTP List no lo tiene (ni a otro uniforme del personaje).', en:'The Ideal CTP List does not have it (nor another uniform of the character).' },
  ctp_sin_armado:    { es:'La guía de armado no le da uno en este contexto.', en:'The building guide gives none in this context.' },
  ctp_ctx_sin:       { es:'Sin contexto',        en:'No context' },
  ctp_ctx_pvp:       { es:'PvP',                 en:'PvP' },
  ctp_ctx_pve:       { es:'PvE',                 en:'PvE' },
  ctp_sin_col:       { es:'La guía de armado no le da uno en esta columna.', en:'The building guide gives none in this column.' },
  ctp_not_worth:     { es:'Ninguno: no vale la pena («Not worth»)', en:'None: not worth it («Not worth»)' },
  ga_eq_other:       { es:'Con un uniforme al lado del nombre, la recomendación es para ese (el que tiene la fuente), no para el que lleva en este equipo.',
                       en:'A uniform next to the name means the recommendation is for that one (the one the source has), not the one used in this team.' },
  ga_art:            { es:'¿Necesita artefacto? Según la guía de armado:', en:'Needs an artifact? Per the building guide:' },
  ga_iso_title:      { es:'ISO-8 y obelisco',    en:'ISO-8 and Obelisk' },
  ga_iso:            { es:'Set de ISO-8:',       en:'ISO-8 set:' },
  ga_obelisk:        { es:'Obelisco (SL/AC):',   en:'Obelisk (SL/AC):' },
  op_note:           { es:'Cada opción se habilita teniendo el uniforme de su fila; debajo, el stat que conviene elegir según la guía de principiantes.',
                       en:'Each option unlocks by owning the uniform in its row; below it, the stat worth picking per the Beginner’s Guide.' },
  op_base:           { es:'El uniforme base no tiene opciones: elegí un uniforme arriba.', en:'The base uniform has no options: pick a uniform above.' },
  op_none:           { es:'thanosvibs no le lista opciones a este uniforme.', en:'thanosvibs lists no options for this uniform.' },
  ru_title:          { es:'Hoja de ruta',        en:'Roadmap' },
  ru_note:           { es:'Los pasos de la guía para esta variante, según su tier máximo y si sube a Tier-3 o trasciende. Marcá hasta dónde llegaste con el personaje: queda guardado en tu capa.',
                       en:'The guide’s steps for this variant, by its max tier and whether it goes Tier-3 or Transcends. Mark how far you got with the character: it is saved in your layer.' },
  ru_done:           { es:'Hecho hasta acá',     en:'Done up to here' },
  ru_undo:           { es:'Desmarcar',           en:'Unmark' },
  ru_this_t3:        { es:'Esta variante sube a Tier-3.', en:'This variant goes to Tier-3.' },
  ru_this_tp:        { es:'Esta variante trasciende su Potencial (no tiene Tier-3).', en:'This variant Transcends its Potential (it has no Tier-3).' },
  ru_no_t3:          { es:'Esta variante no tiene Tier-3 ni Trascendencia: su techo es Tier-2.', en:'This variant has neither Tier-3 nor Transcendence: Tier-2 is its ceiling.' },
  ru_no_t4:          { es:'Esta variante no tiene Tier-4.', en:'This variant has no Tier-4.' },
  ru_notes:          { es:'Notas de la guía',    en:'Guide notes' },
  cap_title:         { es:'Topes de stats',      en:'Stat caps' },
  cap_note:          { es:'Poné lo que muestra la pantalla de stats del juego y, si querés, lo que suman los buffs con duración de sus skills (esa pantalla no los muestra). Se guarda por personaje en tu capa.',
                       en:'Enter what the in-game stats page shows and, optionally, what the timed buffs from its skills add (that page does not show them). Saved per character in your layer.' },
  cap_stat:          { es:'Stat',                en:'Stat' },
  cap_cap:           { es:'Tope',                en:'Cap' },
  cap_val:           { es:'Pantalla %',          en:'Stats page %' },
  cap_buff:          { es:'+ buffs %',           en:'+ buffs %' },
  cap_state:         { es:'Estado',              en:'Status' },
  cap_short:         { es:'faltan {n}%',         en:'{n}% short' },
  cap_ok:            { es:'en el tope',          en:'capped' },
  cap_over:          { es:'pasado por {n}%: sobra', en:'over by {n}%: wasted' },
  cap_base:          { es:'arranca en {n}%',     en:'starts at {n}%' },
  cap_none:          { es:'Sin tope:',           en:'No cap:' },
  vf_title:          { es:'Verificación entre fuentes', en:'Cross-source check' },
  vf_tag:            { es:'{n} diferencias entre fuentes', en:'{n} source differences' },
  vf_tag_1:          { es:'1 diferencia entre fuentes', en:'1 source difference' },
  vf_resumen:        { es:'Skills de este uniforme contra la wiki — coinciden: {ok} · difieren: {d} · no están en la wiki: {nd}.',
                       en:'Skills of this uniform against the wiki — match: {ok} · differ: {d} · not on the wiki: {nd}.' },
  vf_sin_dif:        { es:'Nada distinto entre lo que se pudo contrastar.', en:'Nothing differs in what could be checked.' },
  vf_nota:           { es:'La app muestra thanosvibs; una diferencia es para revisar en el juego (la wiki suele estar vieja), no un error confirmado. Informe completo:',
                       en:'The app shows thanosvibs; a difference is something to check in-game (the wiki is often outdated), not a confirmed error. Full report:' },
  vf_dano:           { es:'daño {a}% en thanosvibs, {w}% en la wiki', en:'damage {a}% on thanosvibs, {w}% on the wiki' },
  vf_cd:             { es:'recarga {a} s en thanosvibs, {w} s en la wiki', en:'cooldown {a} s on thanosvibs, {w} s on the wiki' },
  vf_atk:            { es:'Tipo de ataque: {a} según sus skills; el infobox de la wiki dice {w}', en:'Attack type: {a} per its skills; the wiki infobox says {w}' },
  vf_inst:           { es:'Instinto: {a} en el infobox de la wiki (el que usa la app); la categoría de la página dice {w}', en:'Instinct: {a} in the wiki infobox (the one the app uses); the page category says {w}' },
  vf_t4:             { es:'thanosvibs lo marca Tier-4 pero no trae su Striker Skill.', en:'thanosvibs marks it Tier-4 but has no Striker Skill for it.' },
  vf_s6:             { es:'thanosvibs le marca skill 6 ({v}) pero no trae la Definitiva.', en:'thanosvibs marks a 6th skill ({v}) but has no Ultimate for it.' },
  vf_art:            { es:'Artefacto a 6★: números solo en thanosvibs {a}; solo en la wiki {w}', en:'Artifact at 6★: numbers only on thanosvibs {a}; only on the wiki {w}' },
  vf_art_inc:        { es:'Artefacto: la fuente no trae todos los valores de {v}.', en:'Artifact: the source lacks some values at {v}.' },
  vf_type:           { es:'Clase: {a} en thanosvibs, {w} en la wiki', en:'Class: {a} on thanosvibs, {w} on the wiki' },
  vf_side:           { es:'Bando: {a} en thanosvibs, {w} en la wiki', en:'Side: {a} on thanosvibs, {w} on the wiki' },
  vf_gender:         { es:'Género: {a} en thanosvibs, {w} en la wiki', en:'Gender: {a} on thanosvibs, {w} on the wiki' },
  vf_allies:         { es:'Raza: {a} en thanosvibs, {w} en la wiki', en:'Race: {a} on thanosvibs, {w} on the wiki' },
  rot_title:         { es:'Rotaciones de skills', en:'Skill rotations' },
  rot_none:          { es:'thanosvibs no publica rotaciones para este uniforme.', en:'thanosvibs publishes no rotations for this uniform.' },
  rot_legend:        { es:'Cómo se leen',        en:'How to read them' },
  rot_other:         { es:'Hay rotaciones para:', en:'There are rotations for:' },
  nav_new_char:      { es:'+ Personaje',         en:'+ Character' },
  nav_settings:      { es:'Ajustes',             en:'Settings' },
  nav_glossary:      { es:'Glosario',            en:'Glossary' },
  nav_history:       { es:'Histórico',           en:'History' },
  hi_title:          { es:'Histórico de los personajes', en:'Character history' },
  hi_note:           { es:'Qué llegó en cada versión del juego (personajes, uniformes, Tier-3, Potencial Trascendido y Tier-4, según thanosvibs) y lo que dicen de cada personaje las notas de actualización del foro oficial, con el link a cada nota. El texto de las notas va como lo publica el foro, en inglés.',
                       en:'What came in each game version (characters, uniforms, Tier-3, Potential Transcendence and Tier-4, per thanosvibs) and what the official forum update notes say about each character, with the link to each note.' },
  hi_pj:             { es:'Personaje',           en:'Character' },
  hi_pj_todos:       { es:'Todos',               en:'All' },
  hi_t_todos:        { es:'Todo',                en:'All' },
  hi_t_personaje:    { es:'Personaje nuevo',     en:'New character' },
  hi_t_uniforme:     { es:'Uniforme',            en:'Uniform' },
  hi_t_t3:           { es:'Tier-3',              en:'Tier-3' },
  hi_t_tp:           { es:'Potencial Trascendido', en:'Potential Transcendence' },
  hi_t_t4:           { es:'Tier-4',              en:'Tier-4' },
  hi_t_balance:      { es:'Skills y balance',    en:'Skills and balance' },
  hi_sin_nota:       { es:'La nota de esta versión no lo nombra (o la versión no tiene nota): ver docs/HISTORICO.md.',
                       en:'This version\'s note does not name it (or the version has no note): see docs/HISTORICO.md.' },
  hi_nota_sin_v:     { es:'Nota sin versión de thanosvibs a {d} días o menos', en:'Note with no thanosvibs version within {d} days' },
  hi_nota_err:       { es:'el foro no deja leerla',  en:'the forum does not let it be read' },
  hi_vacio:          { es:'Nada con estos filtros.', en:'Nothing with these filters.' },
  hi_mas:            { es:'Más versiones',       en:'More versions' },
  hi_cuenta:         { es:'{n} versiones con algo', en:'{n} versions with something' },
  hi_ficha:          { es:'Historial',           en:'History' },
  hi_ficha_ver:      { es:'Ver en el Histórico', en:'See in History' },
  gl_title:          { es:'Glosario',            en:'Glossary' },
  gl_note:           { es:'Qué hace cada efecto, en dos pestañas. En la primera, el glosario de skills del juego: el coreano es el original y, donde el inglés no dice lo mismo, se aclara. En la segunda, todos los efectos que la app reconoce en las skills y en Leads & Supports, con cómo se leen en PvE y en PvP.',
                       en:'What each effect does, in two tabs. In the first, the in-game skill glossary: the Korean is the original and, where the English says something else, it is pointed out. In the second, every effect the app recognizes in skills and in Leads & Supports, with how it reads in PvE and PvP.' },
  gl_busca:          { es:'Buscar en español, inglés o coreano', en:'Search in Spanish, English or Korean' },
  gl_una_vez_corto:  { es:'cuenta una vez',      en:'counts once' },
  gl_tope_corto:     { es:'tope',                en:'cap' },
  gl_tab_juego:      { es:'Glosario del juego · {n}', en:'Game glossary · {n}' },
  gl_tab_app:        { es:'Efectos de la app · {n}', en:'App effects · {n}' },
  gl_app_aviso:      { es:'Los grupos y los efectos de esta pestaña son de la app (su catálogo de efectos), no términos del juego. Cada uno dice a qué término del glosario del juego corresponde, si lo hay.',
                       en:"The groups and effects in this tab belong to the app (its effects catalog), not to the game's terms. Each one says which in-game glossary term it matches, if any." },
  gl_errores_sum:    { es:'Lo que el inglés traduce mal: {n} errores que se repiten y {m} diferencias más', en:'What the English gets wrong: {n} repeated mistakes and {m} other differences' },
  gl_en_otra:        { es:'{n} en la otra pestaña', en:'{n} in the other tab' },
  gl_nada:           { es:'Nada coincide con la búsqueda.', en:'Nothing matches the search.' },
  gl_errores:        { es:'Lo que el inglés traduce mal', en:'What the English gets wrong' },
  gl_otras:          { es:'Otras diferencias',   en:'Other differences' },
  gl_terminos:       { es:'Glosario del juego',  en:'Game glossary' },
  gl_terminos_nota:  { es:'Los {n} términos del glosario de skills del juego (Skill Name Glossary · 스킬 용어 사전), en su orden.',
                       en:'The {n} terms of the in-game skill glossary (Skill Name Glossary · 스킬 용어 사전), in its order.' },
  gl_efectos:        { es:'Efectos de las skills', en:'Skill effects' },
  gl_efectos_nota:   { es:'Todos los efectos del catálogo de la app, por grupo: cómo se lee cada uno en PvE y en PvP, a quién le sirve y cómo aparece en las skills. Si un efecto no trae lectura propia, vale la de su grupo.',
                       en:"Every effect in the app's catalog, by group: how each one reads in PvE and PvP, whom it helps and how it shows up in skills. If an effect has no reading of its own, its group's applies." },
  gl_difiere_tag:    { es:'el inglés difiere', en:'English differs' },
  gl_en_ko:          { es:'Inglés y coreano:',  en:'English and Korean:' },
  gl_lo_da:          { es:'Lo da:',             en:'Granted by:' },
  gl_op_fija:        { es:'opción fija',        en:'locked option' },
  gl_op_fija_t:      { es:'La opción fija del C.T.P. (고정 옵션): la tienen el de 6★ y los reforjados (Mighty y Brilliant).',
                       en:"The C.T.P.'s locked option (고정 옵션): the 6★ one and the reforged ones (Mighty and Brilliant) have it." },
  gl_op_reforjado:   { es:'opción de reforjado', en:'reforge option' },
  gl_op_reforjado_t: { es:'Una opción de reforjado del C.T.P. (재련 옵션): solo la tienen los reforjados (Mighty y Brilliant).',
                       en:"One of the C.T.P.'s reforge options (재련 옵션): only the reforged ones (Mighty and Brilliant) have it." },
  gl_en_catalogo:    { es:'En el catálogo:',    en:'In the catalog:' },
  gl_termino:        { es:'Término del glosario del juego', en:'In-game glossary term' },
  gl_en_skills:      { es:'En las skills:',     en:'In skills:' },
  gl_le_sirve:       { es:'Le sirve:',          en:'Helps:' },
  gl_le_sirve_skills: { es:'Le sirve, en las skills:', en:'Helps, in skills:' },
  gl_le_sirve_ls:    { es:'Le sirve, como liderazgo, soporte o bono de equipo:', en:'Helps, as a leadership, support or team bonus:' },
  gl_acumula:        { es:'Si a alguien le llega de dos fuentes (liderazgo, soporte o bono de equipo):', en:'If it reaches someone from two sources (leadership, support or team bonus):' },
  gl_se_suma:        { es:'se suma',             en:'it adds up' },
  gl_una_vez:        { es:'cuenta una vez, la de mayor valor', en:'it counts once, the highest value' },
  gl_tope:           { es:'Tope, en un liderazgo, soporte o bono de equipo:', en:'Cap, in a leadership, support or team bonus:' },
  gl_falta_en:       { es:'sin captura en inglés',  en:'no English capture' },
  gl_falta_ko:       { es:'sin captura en coreano', en:'no Korean capture' },

  search_ph:         { es:'Buscar personaje o uniforme…', en:'Search character or uniform…' },
  filters:           { es:'Filtros',             en:'Filters' },
  clear:             { es:'Limpiar',             en:'Clear' },
  all:               { es:'Todo',                en:'All' },
  bases:             { es:'Bases',               en:'Base' },
  uniforms:          { es:'Uniformes',           en:'Uniforms' },
  cards:             { es:'Tarjetas',            en:'Cards' },
  compact:           { es:'Compacto',            en:'Compact' },
  table:             { es:'Tabla',               en:'Table' },
  sort:              { es:'Ordenar',             en:'Sort' },
  invert:            { es:'Invertir orden',      en:'Reverse order' },
  compare:           { es:'Comparar',            en:'Compare' },
  comparing:         { es:'Comparando',          en:'Comparing' },
  of:                { es:'de',                  en:'of' },

  s_name:            { es:'Nombre',              en:'Name' },
  s_tier:            { es:'Tier',                en:'Tier' },
  s_class:           { es:'Clase',               en:'Class' },
  s_side:            { es:'Bando',               en:'Side' },
  s_rank:            { es:'Posición en la lista',en:'Position in list' },
  s_skills:          { es:'Cantidad de skills',  en:'Skill count' },

  f_class:           { es:'Clase',               en:'Class' },
  f_role:            { es:'Rol',                 en:'Role' },
  f_tier:            { es:'Tier',                en:'Tier' },
  f_side:            { es:'Bando',               en:'Side' },
  f_instinct:        { es:'Instinto',            en:'Instinct' },
  f_race:            { es:'Raza',                en:'Race' },
  f_origin:          { es:'Origen',              en:'Origin' },
  f_ability:         { es:'Habilidad',           en:'Ability' },
  f_shortcuts:       { es:'Atajos',              en:'Shortcuts' },
  f_only_t4:         { es:'Solo T4',             en:'T4 only' },
  f_transcended:     { es:'Trascendidos',        en:'Transcended' },
  f_new:             { es:'Nuevos',              en:'New' },
  f_reflist:         { es:'Lista de referencia (define la posición que se muestra)',
                       en:'Reference list (sets the position shown)' },
  none_f:            { es:'— ninguna —',         en:'— none —' },

  no_match:          { es:'Ningún personaje o uniforme coincide con estos filtros.',
                       en:'No character or uniform matches these filters.' },
  clear_filters:     { es:'Limpiar filtros',     en:'Clear filters' },

  c_character:       { es:'Personaje',           en:'Character' },
  c_instinct:        { es:'Instinto',            en:'Instinct' },
  c_roles:           { es:'Roles',               en:'Roles' },
  c_striker:         { es:'Striker',             en:'Striker' },
  sk_bar_ult:        { es:'se carga con la barra de ult', en:'charged by the ult bar' },
  sk_bar_stk:        { es:'se carga con la barra de striker', en:'charged by the striker bar' },
  c_worldboss:       { es:'World Boss',          en:'World Boss' },
  c_skills:          { es:'Skills',              en:'Skills' },
  c_list:            { es:'Lista',               en:'List' },
  base:              { es:'Base',                en:'Base' },
  transcended_tag:   { es:'TRASCENDIDO',         en:'TRANSCENDED' },
  new_tag:           { es:'NUEVO',               en:'NEW' },

  back_roster:       { es:'← Roster',            en:'← Roster' },
  back_to:           { es:'Volver a {x}',        en:'Back to {x}' },
  compare_this:      { es:'+ Comparar esta versión', en:'+ Compare this version' },
  edit:              { es:'Editar',              en:'Edit' },
  d_uniform:         { es:'Uniforme',            en:'Uniform' },
  ft_resumen:        { es:'Resumen',             en:'Overview' },
  ft_skills:         { es:'Skills',              en:'Skills' },
  an_note:           { es:'Lo que hace con sus skills según el catálogo de efectos: a quién le llega cada efecto, desde qué skill y cuándo, si le sirve, y cómo se lee en PvE y en PvP. Cada lectura dice si lo afirma una fuente (comprobado), si sale del texto del efecto (probable) o si es una suposición (conjetura).',
                       en:'What it does with its skills according to the effect catalog: whom each effect reaches, from which skill and when, whether it is useful to it, and how it reads in PvE and PvP. Each reading says whether a source states it (verified), it follows from the effect text (likely) or it is an assumption (conjecture).' },
  an_resumen:        { es:'En resumen',          en:'In short' },
  an_pega:           { es:'Cómo pega',           en:'How it hits' },
  an_escala:         { es:'Escala con',          en:'Scales with' },
  an_tipos:          { es:'Daño',                en:'Damage' },
  an_elems:          { es:'Elementos',           en:'Elements' },
  an_sin_elem:       { es:'sin elemento',        en:'no element' },
  an_e:              { es:'Para él',             en:'For itself' },
  an_q:              { es:'Para el equipo',      en:'For the team' },
  an_r:              { es:'Contra el rival',     en:'Against the foe' },
  an_i:              { es:'Para sus invocaciones', en:'For its summons' },
  an_nada:           { es:'Nada.',               en:'Nothing.' },
  an_pve_pvp:        { es:'PvE y PvP',           en:'PvE and PvP' },
  an_lider:          { es:'como líder',          en:'as leader' },
  an_varia:          { es:'varía:',              en:'varies:' },
  an_dura:           { es:'dura',                en:'lasts' },
  an_no_sirve:       { es:'No le sirve',         en:'Not useful to it' },
  an_no_sirve_t:     { es:'Es para él, pero le sirve solo {x}.', en:'It is for itself, but it only helps {x}.' },
  an_otorga:         { es:'Otorga un efecto que la fuente no dice', en:'Grants an effect the source does not name' },
  an_otorga_t:       { es:'La skill dice «Acquires the following effect» y no trae ese efecto. Si es un liderazgo o un soporte, Leads & Supports suele decir cuál es (pestaña Resumen).',
                       en:'The skill says "Acquires the following effect" and does not include it. If it is a leadership or a support, Leads & Supports usually says which (Overview tab).' },
  an_sc:             { es:'Sin clasificar',      en:'Not classified' },
  an_sc_t:           { es:'Efectos que el catálogo todavía no clasifica (thanosvibs sumó una etiqueta nueva): se ven como los publica la fuente.',
                       en:'Effects the catalog does not classify yet (thanosvibs added a new label): shown as the source publishes them.' },
  an_roles:          { es:'Roles (deducidos)',   en:'Roles (derived)' },
  an_roles_t:        { es:'No existen en el juego: dicen qué le aporta al equipo. Soporte: le da algo a sus aliados fuera del liderazgo. Tanque: provoca o le baja al equipo el daño que recibe. Control: le aplica al rival 3 o más controles distintos. Daño: todos.',
                       en:'They do not exist in the game: they say what it brings to the team. Support: gives something to its allies outside its leadership. Tank: provokes or lowers the damage the team takes. Control: applies 3 or more different controls to the foe. Damage: everyone.' },
  an_sin_datos:      { es:'La fuente no publica sus skills: no hay nada que analizar.', en:'The source does not publish its skills: there is nothing to analyse.' },
  cert_comprobado:   { es:'comprobado',          en:'verified' },
  cert_probable:     { es:'probable',            en:'likely' },
  cert_conjetura:    { es:'conjetura',           en:'conjecture' },
  // «Cómo funciona» de una skill (se abre al tocarla en la pestaña Skills)
  tt_abrir:          { es:'Cómo funciona esta skill', en:'How this skill works' },
  tt_cerrar:         { es:'Cerrar (Esc)',        en:'Close (Esc)' },
  tt_como:           { es:'Cómo funciona',       en:'How it works' },
  tt_cuando:         { es:'Cuándo, cuánto, a quién', en:'When, how much, to whom' },
  tt_texto:          { es:'Texto del juego',     en:'Game text' },
  tt_certeza:        { es:'Certeza y fuentes',   en:'Certainty and sources' },
  tt_coreano:        { es:'Diferencias con el coreano', en:'Differences with the Korean' },
  tt_vacia:          { es:'La fuente no publica efectos para esta skill.', en:'The source publishes no effects for this skill.' },
  tt_grupo:          { es:'Grupo',               en:'Group' },
  tt_recarga:        { es:'Recarga',             en:'Cooldown' },
  tt_sin_recarga:    { es:'no tiene (la fuente pone 0 s)', en:'none (the source says 0 s)' },
  rc_skill_0:        { es:'la skill no tiene (la fuente pone 0 s)', en:'the skill has none (the source says 0 s)' },
  rc_skill:          { es:'la skill se recarga en {n}', en:'the skill recharges in {n}' },
  rc_efecto:         { es:'según Leads & Supports, el efecto {x} se recarga en {n}', en:'per Leads & Supports, the {x} effect recharges in {n}' },
  rc_efectos:        { es:'según Leads & Supports, los efectos {x} se recargan en {n}', en:'per Leads & Supports, the {x} effects recharge in {n}' },
  tt_sin_dato:       { es:'la fuente no la publica', en:'the source does not publish it' },
  tt_carga:          { es:'Carga que da',        en:'Charge it gives' },
  tt_al_usar:        { es:'al usarla',           en:'when used' },
  tt_sin_cond:       { es:'sin condición: la fuente no publica una activación', en:'no condition: the source publishes no activation' },
  tt_etapa_sin_ac:   { es:'la etapa no publica una propia', en:'the stage publishes none of its own' },
  tt_etapa_vacia:    { es:'La fuente no publica efectos en esta etapa.', en:'The source publishes no effects in this stage.' },
  tt_ls:             { es:'Según Leads & Supports', en:'According to Leads & Supports' },
  tt_ls_api:         { es:'Según la skill del juego', en:'According to the game skill' },
  tt_ls_mixto:       { es:'Según Leads & Supports y la skill del juego', en:'According to Leads & Supports and the game skill' },
  tt_en:             { es:'En inglés, como lo publica thanosvibs', en:'In English, as thanosvibs publishes it' },
  tt_es:             { es:'En español, con la traducción de la app', en:'In Spanish, with the app\'s translation' },
  tt_ko_no:          { es:'En coreano: los datos no traen el texto de las skills en coreano.', en:'In Korean: the data has no Korean text for skills.' },
  tt_ko_terminos:    { es:'Sus términos del glosario del juego, en coreano:', en:'Its game glossary terms, in Korean:' },
  tt_ko_sin:         { es:'Tampoco tiene términos del glosario del juego.', en:'It has no game glossary terms either.' },
  tt_f_texto:        { es:'Texto, números, activación y objetivo: los publica thanosvibs (API de skills).', en:'Text, numbers, activation and target: published by thanosvibs (skills API).' },
  tt_f_trad:         { es:'La traducción al español es la de la app, por patrón.', en:'The Spanish translation is the app\'s own, by pattern.' },
  tt_f_sintrad:      { es:'{n} sin traducir: va el inglés.', en:'{n} untranslated: shown in English.' },
  tt_f_analisis:     { es:'Qué efecto es cada uno y a quién le llega: el catálogo y el análisis de la app (docs/MODELO.md, etapa 2). Los datos no traen una certeza para eso.',
                       en:'Which effect each one is and whom it reaches: the app\'s catalog and analysis (docs/MODELO.md, stage 2). The data carries no certainty for that.' },
  tt_f_lecturas:     { es:'Lecturas de PvE y PvP', en:'PvE and PvP readings' },
  tt_del_grupo:      { es:'(la del grupo {x})',   en:'(the {x} group\'s)' },
  tt_f_glosario:     { es:'Glosario del juego',   en:'Game glossary' },
  tt_dif_nada:       { es:'Sus términos del glosario del juego dicen lo mismo en inglés y en coreano.', en:'Its game glossary terms say the same in English and in Korean.' },
  tt_dif_sin:        { es:'No tiene términos del glosario del juego: no hay con qué comparar.', en:'It has no game glossary terms: there is nothing to compare.' },
  el_Physical:       { es:'físico',              en:'physical' },
  el_Energy:         { es:'de energía',          en:'energy' },
  el_Fire:           { es:'fuego',               en:'fire' },
  el_Cold:           { es:'frío',                en:'cold' },
  el_Lightning:      { es:'rayo',                en:'lightning' },
  el_Poison:         { es:'veneno',              en:'poison' },
  el_Mind:           { es:'mente',               en:'mind' },
  ft_armado:         { es:'Armado',              en:'Build' },
  ft_progreso:       { es:'Tu progreso',         en:'Your progress' },
  ft_fuentes:        { es:'Fuentes',             en:'Sources' },
  st_dano:           { es:'Daño',                en:'Damage' },
  ay_label:          { es:'Cómo se lee',         en:'How to read it' },
  rs_donde:          { es:'Dónde rinde',         en:'Where it performs' },
  rs_da:             { es:'Qué le da al equipo', en:'What it gives the team' },
  rs_necesita:       { es:'Qué necesita',        en:'What it needs' },
  rs_quien:          { es:'Quién es',            en:'Who it is' },
  rs_pega:           { es:'Pega con',            en:'Hits with' },
  rs_ver_armado:     { es:'Ver el armado completo →', en:'See the full build →' },
  rs_det_sop:        { es:'Detalle de lo que da: activación, recarga, condiciones y categorías', en:'What it gives in detail: activation, cooldown, conditions and categories' },
  rs_mas_fuentes:    { es:'Lo demás que dicen las fuentes', en:'What else the sources say' },
  rs_ctp_armado:     { es:'guía de armado',      en:'building guide' },
  rs_ctp_ideal:      { es:'Ideal CTP List',      en:'Ideal CTP List' },
  sk_resumen:        { es:'Strikers: {n} con él ({a} lo ayudan, él ayuda a {b})', en:'Strikers: {n} with it ({a} help it, it helps {b})' },
  sk_con:            { es:'Con',                 en:'With' },
  sk_lo_ayudan:      { es:'Aparece junto a él',  en:'Shows up next to it' },
  sk_el_ayuda:       { es:'Él aparece junto al otro', en:'It shows up next to them' },
  sk_no:             { es:'no',                  en:'no' },
  sk_de_nadie:       { es:'No es striker de nadie en la wiki.', en:'It is nobody\'s striker on the wiki.' },
  sk_sin_dato:       { es:'sin dato',            en:'no data' },
  sk_sin_dato_t:     { es:'La wiki no tiene la pestaña Striker de este personaje.', en:'The wiki has no Striker tab for this character.' },
  ft_equipos:        { es:'Equipos',             en:'Teams' },
  nav_prev:          { es:'Anterior del listado', en:'Previous in the list' },
  nav_next:          { es:'Siguiente del listado', en:'Next in the list' },
  nav_pos:           { es:'{i} de {n}',          en:'{i} of {n}' },
  nav_out:           { es:'fuera del listado',   en:'not in the list' },
  nav_title:         { es:'Posición en el listado del roster, con sus filtros y su orden (también con ← y →)',
                       en:'Position in the roster list, with its filters and order (also with ← and →)' },
  eq_mine:           { es:'En tus equipos',      en:'In your teams' },
  eq_none:           { es:'Todavía no armaste equipos. Cuando armes, acá vas a ver en cuáles está y cómo entraría en los demás.',
                       en:'You have not built any team yet. Once you do, this shows which ones it is in and how it would fit the others.' },
  eq_in_none:        { es:'No está en ninguno de tus equipos.', en:'It is not in any of your teams.' },
  eq_build:          { es:'Llevar a la mesa',    en:'Take to the desk' },
  eq_why:            { es:'Por qué',             en:'Why' },
  pq_abrir:          { es:'Por qué y C.T.P.',    en:'Why and C.T.P.' },
  pq_abrir_t:        { es:'De dónde salen los puntos, quién lidera y por qué, lo que recibe y aporta cada integrante y sus C.T.P. recomendados',
                       en:'Where the points come from, who leads and why, what each member gets and gives, and their recommended C.T.P.' },
  pq_puntos:         { es:'De dónde salen los puntos', en:'Where the points come from' },
  pq_lidera_ctx:     { es:'Lidera {x}: su liderazgo suma {p} en {c}.', en:'{x} leads: its leadership adds {p} in {c}.' },
  pq_lidera_sc:      { es:'Lidera {x}: su liderazgo suma {p} en la sinergia (2 por cada liderazgo que le llega y le sirve a otro integrante; 3 si es Notable).',
                       en:'{x} leads: its leadership adds {p} to the synergy (2 for each leadership that reaches and helps another member; 3 if Notable).' },
  pq_lidera_sin:     { es:'Lidera {x}, aunque no tiene liderazgo: ninguno suma en {c}.', en:'{x} leads, although it has no leadership: none adds in {c}.' },
  pq_demas:          { es:'Los demás: {l}.',     en:'The others: {l}.' },
  pq_cand:           { es:'{x}, {p}',            en:'{x}, {p}' },
  pq_cand_sin:       { es:'{x} no tiene liderazgo', en:'{x} has no leadership' },
  pq_cand_anti:      { es:'{x} no puede liderar: con su liderazgo, no todos tienen anti-mermas', en:'{x} cannot lead: with its leadership, not everyone has debuff removal' },
  pq_empate_puesto:  { es:'Empata con {y}: lidera por estar mejor ubicado en las tier lists ({l}).', en:'Tied with {y}: it leads because it ranks better in the tier lists ({l}).' },
  pq_empate_orden:   { es:'Con {y} empata también en las tier lists ({l}): decide un orden fijo.', en:'With {y} it is also tied in the tier lists ({l}): a fixed order decides.' },
  pq_sin_lider:      { es:'Nadie lidera: ningún liderazgo le llega y le sirve a otro integrante.', en:'Nobody leads: no leadership reaches and helps another member.' },
  pq_p_sop:          { es:'Soportes',            en:'Supports' },
  pq_p_bonos:        { es:'Bonos de equipo',     en:'Team bonuses' },
  pq_p_otras:        { es:'Roles, clases y ventaja de clase', en:'Roles, classes and class advantage' },
  pq_integrantes:    { es:'Integrantes',         en:'Members' },
  pq_recibe:         { es:'Lo que recibe {x}',   en:'What {x} gets' },
  pq_nada:           { es:'Ningún soporte ni liderazgo le llega y le sirve.', en:'No support or leadership reaches it and is useful to it.' },
  pq_col_efecto:     { es:'Efecto',              en:'Effect' },
  pq_col_total:      { es:'Total',               en:'Total' },
  pq_tope:           { es:'Tope de la guía: {t}.', en:'Guide cap: {t}.' },
  pq_tope_base:      { es:'{n}% (desde {b}%)',   en:'{n}% (from {b}%)' },
  pq_tope_t:         { es:'El tope lo dice la guía. Acá se cuenta solo lo de esta tabla: lo que el personaje ya tiene (su equipo, sus C.T.P., los bonos de equipo) lo acerca más.',
                       en:'The guide sets the cap. Only this table is counted here: what the character already has (gear, C.T.P.s, team bonuses) brings it closer.' },
  pq_tope_pasa:      { es:'Pasa el tope: los buffs suman {x}% y hasta el tope quedan {r}%; lo de más no suma.',
                       en:'Over the cap: the buffs add up to {x}% and only {r}% is left to the cap; the rest adds nothing.' },
  pq_tope_pasa_cond: { es:'Con lo que le llega siempre, pasa el tope: los buffs suman {x}% y hasta el tope quedan {r}%; lo de más no suma.',
                       en:'With what it always gets, it goes over the cap: the buffs add up to {x}% and only {r}% is left to the cap; the rest adds nothing.' },
  pq_col_de:         { es:'De dónde',            en:'From' },
  pq_sin_art:        { es:'sin artefactos: {x}', en:'without artifacts: {x}' },
  pq_aporta:         { es:'Lo que aporta {x}',   en:'What {x} gives' },
  pq_aporta_nada:    { es:'Nada de lo suyo les llega y les sirve a los demás.', en:'Nothing of its own reaches and helps the others.' },
  pq_ver:            { es:'En la ficha de {x}', en:'On {x}\'s sheet' },
  pq_si_art:         { es:'si lleva su artefacto', en:'if it has its artifact' },
  pq_sin_skill:      { es:'La ficha de este personaje no tiene esta skill.', en:'This character\'s sheet does not have this skill.' },
  pq_ademas:         { es:'Además',              en:'Also' },
  pq_gana:           { es:'Se gana, además de lo de {x}', en:'Also gained, besides what {x} brings' },
  pq_pierde:         { es:'Se pierde',           en:'Lost' },
  pq_todos:          { es:'a todos',             en:'everyone' },
  ya_propio:         { es:'propio ({s})',        en:'as its own ({s})' },
  ya_su_lid:         { es:'de su liderazgo',     en:'from its own leadership' },
  ya_lid:            { es:'del liderazgo de {x}', en:'from {x}\'s leadership' },
  ya_sop:            { es:'de {x} ({s})',        en:'from {x} ({s})' },
  rep_no_suma:       { es:'no se suma: ya lo tiene {de}', en:'not added: it already has it {de}' },
  rep_quien:         { es:'{y} ya lo tiene {de}', en:'{y} already has it {de}' },
  rep_nada:          { es:'no suma',             en:'adds nothing' },
  rep_regla:         { es:'Si a alguien le llega lo mismo de dos fuentes, las estadísticas (ataques, defensas, vida, daño, crítico...) se suman, y las habilidades (anti-mermas, inmunidades, barrera, escudos, revivir, invocar...) cuentan una vez: la de mayor valor y, a igual valor, la propia; si no, la del liderazgo del líder; si no, la del primer soporte en el orden del equipo (el líder primero y los demás en un orden fijo). Las otras no le suman, y el «Por qué» las muestra atenuadas. Qué se suma y qué no lo dice el Glosario, en cada efecto.',
                       en:'When someone gets the same thing from two sources, stats (attacks, defenses, HP, damage, critical...) add up, and abilities (debuff removal, immunities, barrier, shields, revive, summon...) count once: the highest value and, on equal value, its own; otherwise, the leader\'s leadership; otherwise, the first support in the team order (the leader first, then the rest in a fixed order). The others do not add for it, and the «Why» shows them dimmed. What adds up and what does not is in the Glossary, under each effect.' },
  eq_could:          { es:'Cómo entraría en tus otros equipos', en:'How it would fit your other teams' },
  eq_could_note:     { es:'Con {v}: el mejor cambio en cada equipo según la sinergia de la app, siempre que quede con vínculo con alguien del equipo (le da un soporte o el liderazgo, recibe uno suyo o forman juntos un bono de equipo).',
                       en:'With {v}: the best change in each team according to the app\'s synergy, as long as it has a link with someone in the team (gives it a support or the leadership, receives one of its own, or they form a team bonus together).' },
  eq_instead:        { es:'en lugar de {x}',     en:'instead of {x}' },
  eq_room:           { es:'hay lugar: sumándolo', en:'there is room: adding it' },
  eq_before:         { es:'antes {n}',           en:'before {n}' },
  eq_name_swap:      { es:'{e} (con {v})',       en:'{e} (with {v})' },
  eq_no_gain:        { es:'No mejoran con él:',  en:'Not improved by it:' },
  eq_no_link:        { es:'Sin vínculo con nadie del equipo:', en:'No link with anyone in the team:' },
  eq_new:            { es:'Combinaciones de 3 con él', en:'Combinations of 3 with it' },
  eq_new_note:       { es:'Todas las parejas de compañeros que tienen vínculo con él (le dan un soporte o el liderazgo, reciben uno suyo o forman con él un bono de equipo), una por trío de personajes, con el mejor uniforme de cada uno para el orden elegido. Un efecto cuenta solo si le sirve a quien lo recibe: a quién le sirve cada uno lo dice el Glosario, en su efecto. Los puntos para él son la sinergia de la app contando solo lo que lo involucra: lo que le dan, lo que da él, los bonos de equipo en los que está o que le sirven, la ventaja de clase con él, y los roles y las clases del equipo. El líder es el mismo en todas las pantallas: el que más suma con su liderazgo al equipo (en los órdenes PvP y PvE, con los pesos del contexto); a igual puntaje, el mejor ubicado en las tier lists del contexto (sin contexto, la General).',
                       en:'Every pair of teammates with a link with it (they give it a support or the leadership, receive one of its own, or form a team bonus with it), one per trio of characters, with each one\'s best uniform for the chosen order. An effect only counts if it is useful to whoever receives it: the Glossary says whom each one helps, under its effect. Points for it are the app\'s synergy counting only what involves it: what it gets, what it gives, the team bonuses it is part of or that are useful to it, class advantage with it, and the team\'s roles and classes. The leader is the same on every screen: the one whose leadership adds the most to the team (in the PvP and PvE orders, with that context\'s weights); on a tie, the one ranked best in the context\'s tier lists (with no context, the General list).' },
  eq_calc:           { es:'Calculando las combinaciones…', en:'Working out the combinations…' },
  eq_sort:           { es:'Ordenar por',         en:'Sort by' },
  eq_sort_foco:      { es:'Puntos para él',      en:'Points for it' },
  eq_con:            { es:'Con',                 en:'With' },
  eq_con_any:        { es:'cualquiera',          en:'anyone' },
  eq_excluir:        { es:'Sin',                 en:'Without' },
  eq_excluir_ph:     { es:'excluir a…',          en:'exclude…' },
  eq_incluir:        { es:'Volver a incluirlo',  en:'Include it again' },
  eq_cob:            { es:'Solo si recibe:',     en:'Only if it gets:' },
  eq_cob_title:      { es:'Solo las combinaciones cuya tarjeta muestra ✓ en todo lo marcado (también con *: si el compañero lleva su artefacto). Cada pareja de compañeros va con su mejor combinación de uniformes que lo cumple.',
                       en:'Only the combinations whose card shows ✓ in everything checked (also with *: if the teammate has its artifact). Each pair of teammates comes with its best uniform combination that meets it.' },
  eq_comp:           { es:'Compañeros:',         en:'Teammates:' },
  eq_ultimo:         { es:'Solo el último uniforme', en:'Latest uniform only' },
  eq_ultimo_t:       { es:'De cada compañero entra solo su uniforme más nuevo; él va con el uniforme elegido.',
                       en:'Each teammate comes only with its newest uniform; it keeps the chosen uniform.' },
  eq_ultimo_nota:    { es:'Solo el último uniforme: de cada compañero entra solo su uniforme más nuevo (si no tiene uniformes, la base; si tiene, la base no entra), y {x} va con el uniforme elegido. El más nuevo es el que salió en la versión del juego más alta, según thanosvibs (la letra va después del número: 9.1.5a antes que 9.1.5b), y, a igual versión, el de número de uniforme más alto en el juego.',
                       en:'Latest uniform only: each teammate comes only with its newest uniform (with no uniforms, the base; with uniforms, the base is left out), and {x} keeps the chosen uniform. The newest is the one released in the highest game version, according to thanosvibs (the letter goes after the number: 9.1.5a before 9.1.5b), and, on the same version, the one with the highest uniform number in the game.' },
  eq_ultimo_de:      { es:'{n} sin «Solo el último uniforme»', en:'{n} without «Latest uniform only»' },
  eq_count:          { es:'{n} combinaciones',   en:'{n} combinations' },
  eq_count_1:        { es:'1 combinación',       en:'1 combination' },
  eq_none_q:         { es:'Ninguna combinación con estos filtros.', en:'No combination with these filters.' },
  eq_leader:         { es:'Líder: {x}',          en:'Leader: {x}' },
  eq_lider_de:       { es:'Líder: {x}',          en:'Leader: {x}' },
  eq_lider_pill:     { es:'Líder',               en:'Leader' },
  eq_no_leader:      { es:'Ningún liderazgo le suma', en:'No leadership adds for it' },
  eq_fav_add:        { es:'Marcar como favorito', en:'Mark as favorite' },
  eq_descartar:      { es:'Descartar',           en:'Discard' },
  eq_descartar_title:{ es:'Ocultarlo en las combinaciones de los tres personajes, con cualquier uniforme',
                       en:'Hide it from the combinations of all three characters, with any uniform' },
  eq_restaurar:      { es:'Restaurar',           en:'Restore' },
  eq_count_desc:     { es:'{n} descartados',     en:'{n} discarded' },
  eq_count_desc_1:   { es:'1 descartado',        en:'1 discarded' },
  eq_ver_desc:       { es:'Ver descartados ({n})', en:'Show discarded ({n})' },
  eq_ver_lista:      { es:'Volver a la lista',   en:'Back to the list' },
  eq_none_desc:      { es:'No hay descartados con él (con estos filtros).', en:'No discarded teams with it (with these filters).' },
  eq_fav_rm:         { es:'Quitar de favoritos', en:'Remove from favorites' },
  eq_pts_for:        { es:'pts para él',         en:'pts for it' },
  eq_pts_team:       { es:'{n} del equipo',      en:'{n} for the team' },
  cx_orden:          { es:'{c} · puntaje de equipo · {l}', en:'{c} · team score · {l}' },
  cx_pts_pvp:        { es:'pts PvP',             en:'PvP pts' },
  cx_pts_pve:        { es:'pts PvE',             en:'PvE pts' },
  cx_para_el:        { es:'{a} para él · {b} del equipo', en:'{a} for it · {b} for the team' },
  cx_nota:           { es:'Equipos para {c}, con las reglas de Ezequiel. Entran si alguno es DPS en {l}{req}. Cada compañero tiene vínculo con él o es DPS. Puntaje, con la tabla de valor: cada stat del liderazgo del líder suma, por cada integrante al que le llega y le sirve, su peso ({stats}), y el {cond}% de eso si el liderazgo se activa con una condición (al recibir un debuff, por ejemplo); cada nivel de fila de cada DPS (3, 2 o 1{mejor}), {dps}; cada soporte con el que a otro se le aplica algo que le sirve, {sop}, y cada bono de equipo activo, {bono}. Los strikers del trío no suman: a igual puntaje, desempatan. El líder es el que más suma y es el mismo en las listas de los tres: a igual puntaje, el mejor ubicado en las tier lists y después un orden fijo.',
                       en:'Teams for {c}, with Ezequiel\'s rules. They make it if someone is a DPS in {l}{req}. Each teammate has a link with it or is a DPS. Score, with the value table: each stat of the leader\'s leadership adds its weight for each member it reaches and helps ({stats}), and {cond}% of that if the leadership activates on a condition (when debuffed, for example); each row level of each DPS (3, 2 or 1{mejor}), {dps}; each support that gives another member something useful that applies to it, {sop}, and each active team bonus, {bono}. The trio\'s strikers do not add: on equal score, they break the tie. The leader is the one that adds the most and is the same in the lists of all three: on a tie, the best placed on the tier lists, then a fixed order.' },
  cx_req_anti:       { es:' y si los tres tienen anti-mermas ({a}): del liderazgo del líder, del soporte de alguno (también el propio) o de sus propias skills, sin contar los que tienen probabilidad', en:' and all three have debuff removal ({a}): from the leader\'s leadership, someone\'s support (its own too) or their own skills, not counting those with a probability' },
  cx_req_no:         { es:'; los anti-mermas no hacen falta', en:'; debuff removal is not required' },
  cx_o:              { es:' o ',                  en:' or ' },
  cx_mejor_lista:    { es:', el mejor de las listas', en:', the best of the lists' },
  cx_propuesta:      { es:'Los pesos son una propuesta: se ajustan con casos.', en:'The weights are a proposal: they get adjusted with cases.' },
  cx_sin_funcion_pvp: { es:'{x} no figura en la tier list de PvP ({l}){f}: no tiene función en PvP y este orden no arma combinaciones.',
                       en:'{x} is not on the PvP tier list ({l}){f}: it has no role in PvP, so this order builds no combinations.' },
  cx_sin_funcion_pve: { es:'{x} no figura en las tier lists de PvE ({l}){f}: no tiene función en PvE y este orden no arma combinaciones.',
                       en:'{x} is not on the PvE tier lists ({l}){f}: it has no role in PvE, so this order builds no combinations.' },
  cx_o_solo:         { es:', o solo como {f}',   en:', or only as {f}' },
  cx_anti:           { es:'Anti-mermas',         en:'Debuff removal' },
  cx_de_lid:         { es:'{x} (liderazgo)',     en:'{x} (leadership)' },
  cx_de_sop:         { es:'{x} (soporte)',       en:'{x} (support)' },
  cx_de_propio:      { es:'{x} (propio: {s})',   en:'{x} (own: {s})' },
  cx_prob:           { es:'{x}: anti-mermas propio de su {s} ({a}): tiene probabilidad, no cuenta', en:'{x}: own debuff removal from its {s} ({a}): it has a probability, so it does not count' },
  cx_lider:          { es:'Liderazgo de {x}',    en:'{x}\'s leadership' },
  cx_lider_nada:     { es:'Ningún liderazgo de los que valen en este contexto', en:'No leadership that counts in this context' },
  cx_lider_cond:     { es:'cuenta el {p}%',      en:'counts {p}%' },
  cx_dps:            { es:'DPS',                 en:'DPS' },
  cx_sinergia:       { es:'Soportes y bonos de equipo', en:'Supports and team bonuses' },
  cx_desempate:      { es:'desempate: {n} strikers', en:'tiebreak: {n} strikers' },
  cx_desempate_1:    { es:'desempate: 1 striker',  en:'tiebreak: 1 striker' },
  cx_striker_de:     { es:'{b} de {a}',          en:'{b} for {a}' },
  d_race:            { es:'Raza',                en:'Race' },
  d_gender:          { es:'Género',              en:'Gender' },
  d_origin:          { es:'Origen',              en:'Origin' },
  d_cost:            { es:'Costo del uniforme',  en:'Uniform cost' },
  d_abilities:       { es:'Habilidades:',        en:'Abilities:' },
  d_tuc:             { es:'Cartas TUC:',         en:'TUC cards:' },
  d_no_skills:       { es:'thanosvibs no publica skills para este uniforme todavía.',
                       en:'thanosvibs does not publish skills for this uniform yet.' },
  d_portraits:       { es:'Retratos propios',    en:'Custom portraits' },
  d_portraits_note:  { es:'Si subís una imagen, reemplaza la de thanosvibs solo en tu capa.',
                       en:'Uploading an image replaces the thanosvibs one in your layer only.' },
  d_upload:          { es:'Subir retrato',       en:'Upload portrait' },
  d_revert_img:      { es:'Volver al original',  en:'Back to original' },

  cmp_title:         { es:'Comparativa',         en:'Comparison' },
  cmp_note:          { es:'Las celdas resaltadas marcan coincidencias entre las columnas.',
                       en:'Highlighted cells mark matches across columns.' },
  cmp_remove:        { es:'Quitar',              en:'Remove' },
  cmp_unplaced:      { es:'sin ubicar',          en:'unplaced' },
  cmp_missing_slot:  { es:'— no tiene —',        en:'— none —' },
  cmp_mas:           { es:'{n} efectos más',     en:'{n} more effects' },
  cmp_mas_1:         { es:'1 efecto más',        en:'1 more effect' },
  cmp_lleno:         { es:'Ya hay {n} para comparar: quitá una para sumar {x}.', en:'There are already {n} to compare: remove one to add {x}.' },
  cmp_synergy:       { es:'Sinergia estimada',   en:'Estimated synergy' },
  cmp_pts:           { es:'pts',                 en:'pts' },
  cmp_no_synergy:    { es:'Sin señales fuertes de sinergia en esta selección.',
                       en:'No strong synergy signals in this selection.' },
  cmp_heuristic:     { es:'Pesan los efectos de líder y de soporte de thanosvibs que alcanzan a otro integrante y le sirven (a quién le sirve cada uno lo dice el Glosario, en su efecto; el liderazgo, el del líder del equipo: el que más suma con el suyo; a igual puntaje, el mejor ubicado en la lista General). Cada bono de equipo con todos sus integrantes en el equipo suma 1 (de la wiki, o del juego si se cargó). Se suman dos lecturas propias: roles derivados de las skills y ventaja de clase (la guía de thanosvibs y la wiki). No es un cálculo del juego.',
                       en:'What weighs most are the thanosvibs lead and support effects that reach another member and are useful to it (the Glossary says whom each one helps, under its effect; leadership, the team leader\'s: the one whose leadership adds the most; on a tie, the one ranked best in the General list). Each team bonus with all its members in the team adds 1 (from the wiki, or from the game when entered). Two readings of our own are added: roles derived from skills and class advantage (per the thanosvibs guide and the wiki). Not a game calculation.' },
  sy_unclassified:   { es:'efecto sin clasificar: cuenta para todos', en:'unclassified effect: counts for everyone' },
  sy_bonus:          { es:'Bono de equipo',      en:'Team bonus' },
  sy_bonus_noname:   { es:'sin nombre en la wiki', en:'unnamed on the wiki' },
  sy_bonus_ver:      { es:'la wiki no coincide: versión {i} de {n}', en:'the wiki disagrees: version {i} of {n}' },
  bn_title:          { es:'Bonos de equipo',     en:'Team bonuses' },
  bn_note:           { es:'Llevarlo junto a estos personajes les sube estos stats a todos los del equipo. Son del personaje: valen con cualquier uniforme. En la sinergia, cada bono activo suma 1.',
                       en:'Teaming it up with these characters raises these stats for the whole team. They belong to the character: any uniform works. In the synergy, each active bonus adds 1.' },
  bn_none:           { es:'No tiene bonos de equipo conocidos: la wiki no los lista y todavía no se cargaron del juego.',
                       en:'No known team bonuses: the wiki does not list them and they have not been entered from the game yet.' },
  bn_show:           { es:'Ver sus {n} bonos',   en:'Show its {n} bonuses' },
  bn_noname:         { es:'(sin nombre en la wiki)', en:'(unnamed on the wiki)' },
  bn_tie:            { es:'La wiki no coincide: sus páginas dicen otra cosa', en:'The wiki disagrees: its pages say different things' },
  sk_title:          { es:'Strikers',            en:'Strikers' },
  sk_note:           { es:'Pueden aparecer a pegar junto a él, con esa probabilidad, cuando él ataca o cuando lo atacan. Según Ezequiel, el striker tiene que estar en el mismo equipo, y suma muy poco: en los equipos no da puntos, desempata. Son del personaje: valen con cualquier uniforme.',
                       en:'They may show up to strike alongside it, with that chance, when it attacks or when it is attacked. Per Ezequiel, the striker has to be on the same team, and it adds very little: in teams it gives no points, it breaks ties. They belong to the character: any uniform works.' },
  sk_de_nota:        { es:'Aparece junto a ellos cuando ellos atacan o los atacan.', en:'It shows up alongside them when they attack or are attacked.' },
  sk_sin_pestana:    { es:'La wiki no tiene sus strikers.', en:'The wiki does not list its strikers.' },
  sk_ataca:          { es:'{p}% al atacar',     en:'{p}% on attack' },
  sk_atacado:        { es:'{p}% al ser atacado', en:'{p}% when attacked' },
  sk_imposible:      { es:'Dato imposible de la fuente: una probabilidad no puede pasar de 100%. La wiki dice esto y la app lo muestra tal cual, sin corregirlo (docs/AUDITORIA.md, sección 11).',
                       en:'Impossible value from the source: a chance cannot exceed 100%. The wiki says this and the app shows it as is, uncorrected (docs/AUDITORIA.md, section 11).' },
  cmp_abilities:     { es:'Habilidades',         en:'Abilities' },
  cmp_cost:          { es:'Costo',               en:'Cost' },

  tl_title:          { es:'Tier lists',          en:'Tier lists' },
  tl_note:           { es:'Las listas importadas son todas las que se publican en thanosvibs, con las filas y los rótulos que les puso su autor: no son rangos S–D.',
                       en:'The imported lists are every list published on thanosvibs, with the rows and labels their author wrote: they are not S–D ranks.' },
  tl_new_ph:         { es:'Nombre de una lista nueva', en:'Name for a new list' },
  tl_create:         { es:'+ Crear lista',       en:'+ Create list' },
  tl_source:         { es:'Fuente:',             en:'Source:' },
  tl_author:         { es:'autor:',              en:'author:' },
  tl_game:           { es:'juego',               en:'game' },
  tl_placed:         { es:'ubicados',            en:'placed' },
  tl_own:            { es:'Lista propia',        en:'Your own list' },
  tl_delete:         { es:'Borrar lista',        en:'Delete list' },
  tl_undo:           { es:'Deshacer mis cambios', en:'Undo my changes' },
  tl_drop_here:      { es:'Arrastrá acá',        en:'Drop here' },
  tl_show_pool:      { es:'Mostrar sin ubicar',  en:'Show unplaced' },
  tl_hide_pool:      { es:'Ocultar sin ubicar',  en:'Hide unplaced' },
  tl_filter:         { es:'Filtrar…',            en:'Filter…' },
  tl_nothing:        { es:'Nada coincide.',      en:'Nothing matches.' },
  tl_more:           { es:'más: filtrá para acotar.', en:'more: filter to narrow it down.' },
  tl_confirm_del:    { es:'¿Borrar esta lista y sus asignaciones?', en:'Delete this list and its placements?' },
  tl_spots:          { es:'ubicaciones',         en:'placements' },
  tl_rename:         { es:'Nombre de la lista',  en:'List name' },
  tl_rows_edit:      { es:'Editar filas',        en:'Edit rows' },
  tl_rows_done:      { es:'Listo',               en:'Done' },
  tl_row_up:         { es:'Subir',               en:'Move up' },
  tl_row_down:       { es:'Bajar',               en:'Move down' },
  tl_row_del:        { es:'Borrar fila',         en:'Delete row' },
  tl_row_add:        { es:'+ Agregar fila',      en:'+ Add row' },
  tl_rows_note2:     { es:'El orden de las filas es el orden de la lista.', en:'Row order is the list order.' },
  tl_row_del_confirm:{ es:'Entradas en esta fila: {n}. Se sacan de ella (las que estén también en otra fila siguen ahí). ¿Borrar la fila?',
                       en:'Entries in this row: {n}. They are removed from it (those also in another row stay there). Delete the row?' },
  tl_dup:            { es:'Duplicar como mía',   en:'Duplicate as mine' },
  tl_dup_title:      { es:'Crea una lista propia con las mismas filas y ubicaciones, para editarla sin tocar la importada.',
                       en:'Creates an own list with the same rows and placements, to edit it without touching the imported one.' },
  tl_copy_suffix:    { es:'(copia)',             en:'(copy)' },
  tp_title:          { es:'Plantilla de filas',  en:'Row template' },
  tp_ctp:            { es:'Por C.T.P. (una fila por C.T.P.)', en:'By C.T.P. (one row per C.T.P.)' },
  tk_title:          { es:'Qué se ubica en la lista', en:'What the list ranks' },
  tk_chars:          { es:'Personajes y uniformes', en:'Characters and uniforms' },
  tk_ctp:            { es:'C.T.P.s',              en:'C.T.P.s' },
  tk_art:            { es:'Artefactos',           en:'Artifacts' },
  tk_team:           { es:'Mis equipos',          en:'My teams' },
  tp_rank:           { es:'Rango S–D',           en:'Rank S–D' },
  tp_rank_plus:      { es:'Rango SS–D',          en:'Rank SS–D' },
  tp_role:           { es:'Uso: líder / principal / soporte / striker', en:'Use: lead / main / support / striker' },
  tp_empty:          { es:'Vacía (una fila)',    en:'Empty (one row)' },
  tp_new_row:        { es:'Fila nueva',          en:'New row' },
  tp_r_lead:         { es:'Líder',               en:'Lead' },
  tp_r_main:         { es:'Principal (DPS)',     en:'Main (DPS)' },
  tp_r_support:      { es:'Soporte',             en:'Support' },
  tp_r_striker:      { es:'Striker',             en:'Striker' },
  tl_g_main:         { es:'Principales',         en:'Main' },
  tl_g_community:    { es:'Comunidad',           en:'Community' },
  tl_g_own:          { es:'Mías',                en:'Mine' },
  tl_published:      { es:'publicada',           en:'published' },
  tl_votes:          { es:'votos',               en:'votes' },
  tl_rating_title:   { es:'Puntaje promedio que le dan los usuarios de thanosvibs', en:'Average score given by thanosvibs users' },
  tl_description:    { es:'Descripción del autor', en:'Author\'s description' },
  tl_notes:          { es:'Notas de esta versión', en:'Notes for this version' },
  tl_author_lang:    { es:'Textos del autor, en su idioma original: igual que los rótulos de las filas, no se traducen.',
                       en:'Author\'s texts, in their original language: like the row labels, they are not translated.' },
  tl_multi:          { es:'Está en más de una fila de esta lista', en:'It is in more than one row of this list' },
  tl_remove_row:     { es:'Quitar de esta fila', en:'Remove from this row' },
  tl_done:           { es:'Listo',               en:'Done' },
  tl_rows_note:      { es:'Puede estar en varias filas a la vez: marcá todas las que correspondan.',
                       en:'It can be in several rows at once: tick every row that applies.' },
  tl_open_sheet:     { es:'Ver ficha',           en:'Open sheet' },

  tm_title:          { es:'Equipos',             en:'Teams' },
  tm_note:           { es:'Los que guardaste desde la mesa, con la sinergia estimada por la app. Se arman en la mesa, a la derecha.',
                       en:'The ones you saved from the desk, with the synergy the app estimates. You build them on the desk, on the right.' },
  tm_nomode:         { es:'Sin modo (3)',        en:'No mode (3)' },
  tm_lleno:          { es:'El equipo ya tiene {n} de {n}: quitá uno para sumar a {x}.', en:'The team already has {n} of {n}: remove one to add {x}.' },
  tm_sobran:         { es:'Este modo es de {n} y hay {m}: quitá {k} para guardarlo.', en:'This mode takes {n} and there are {m}: remove {k} to save it.' },
  tm_synergy_pts:    { es:'pts de sinergia',     en:'synergy pts' },
  tm_empty:          { es:'Todavía no armaste ningún equipo.', en:'You have not built any team yet.' },
  tm_mine:           { es:'Equipos de tu cuenta', en:'Your account\'s teams' },
  tm_dup:            { es:'{x} ya está en «{e}», del mismo modo.', en:'{x} is already in «{e}», same mode.' },
  tm_favs:           { es:'Favoritos',           en:'Favorites' },
  tm_fav_ctx:        { es:'marcado en {c}',      en:'marked in {c}' },
  tm_ya_esta:        { es:'Ese equipo ya está guardado con este modo y este líder: «{e}».', en:'That team is already saved with this mode and this leader: «{e}».' },
  tm_favs_note:      { es:'Los que marcaste con ★ en las combinaciones de cada personaje. Desde acá los armás para tu cuenta.',
                       en:'The ones you starred in each character\'s combinations. Build them for your account from here.' },
  tm_no_leader:      { es:'Ningún liderazgo suma', en:'No leadership adds' },
  tm_desc:           { es:'Descartados ({n})',   en:'Discarded ({n})' },
  tm_desc_note:      { es:'Los equipos que ocultaste de las combinaciones de sus tres personajes, con cualquier uniforme. Restaurarlos los vuelve a mostrar.',
                       en:'The teams you hid from their three characters\' combinations, with any uniform. Restoring brings them back.' },

  ed_edit:           { es:'Editar personaje',    en:'Edit character' },
  ed_new:            { es:'Nuevo personaje',     en:'New character' },
  ed_note:           { es:'Se guarda en tu capa, aparte de data.js. Regenerar los datos no lo pisa.',
                       en:'Saved in your layer, separate from data.js. Regenerating the data does not overwrite it.' },
  ed_step_data:      { es:'Datos',               en:'Details' },
  ed_step_unis:      { es:'Uniformes',           en:'Uniforms' },
  ed_step_review:    { es:'Revisar',             en:'Review' },
  ed_name:           { es:'Nombre',              en:'Name' },
  ed_striker:        { es:'Striker (número de skill)', en:'Striker (skill number)' },
  ed_uni_name:       { es:'Nombre del uniforme', en:'Uniform name' },
  ed_cost:           { es:'Costo',               en:'Cost' },
  ed_add_uni:        { es:'+ Agregar uniforme',  en:'+ Add uniform' },
  ed_back:           { es:'Atrás',               en:'Back' },
  ed_next:           { es:'Siguiente',           en:'Next' },
  ed_save:           { es:'Guardar',             en:'Save' },
  ed_discard:        { es:'Descartar mi edición', en:'Discard my edit' },
  ed_need_name:      { es:'Poné un nombre.',     en:'Enter a name.' },
  ed_no_skills:      { es:'Los personajes propios no llevan skills: las skills vienen tipadas de la API de thanosvibs y no se cargan a mano.',
                       en:'Your own characters have no skills: skills come typed from the thanosvibs API and are not entered by hand.' },

  st_title:          { es:'Ajustes',             en:'Settings' },
  st_note:           { es:'Los datos del juego salen de data.js y no se guardan acá. Esto es solo lo tuyo.',
                       en:'Game data comes from data.js and is not stored here. This is only your own layer.' },
  st_layer:          { es:'Tu capa guardada',    en:'Your saved layer' },
  st_own_chars:      { es:'Personajes propios o editados', en:'Own or edited characters' },
  st_teams:          { es:'Equipos',             en:'Teams' },
  st_own_lists:      { es:'Tier lists propias',  en:'Your own tier lists' },
  st_list_changes:   { es:'Cambios sobre listas importadas', en:'Changes to imported lists' },
  st_images:         { es:'Imágenes subidas',    en:'Uploaded images' },
  st_export:         { es:'Exportar mi capa (JSON)', en:'Export my layer (JSON)' },
  st_import:         { es:'Importar',            en:'Import' },
  st_export_csv:     { es:'Exportar roster (CSV)', en:'Export roster (CSV)' },
  st_reset:          { es:'Borrar todo lo mío',  en:'Delete everything of mine' },
  st_brand:          { es:'Marca',               en:'Branding' },
  st_no_logo:        { es:'Sin logo',            en:'No logo' },
  st_upload_logo:    { es:'Subir logo',          en:'Upload logo' },
  st_remove:         { es:'Quitar',              en:'Remove' },
  st_modes:          { es:'Modos propios (tamaño de equipo)', en:'Your own modes (team size)' },
  st_modes_note:     { es:'Los modos del juego, con su tamaño de equipo según la fuente, están en la sección Modos. Acá podés sumar los tuyos para armar equipos.',
                       en:'Game modes, with their team size per the source, are in the Modes section. Here you can add your own for building teams.' },
  tm_modes_game:     { es:'Modos del juego',     en:'Game modes' },
  tm_modes_own:      { es:'Modos propios',       en:'Your own modes' },
  ms_title:          { es:'Mesa',                en:'Desk' },
  ms_team:           { es:'Equipo',              en:'Team' },
  ms_libre:          { es:'Lugar libre',         en:'Free slot' },
  ms_libre_nota:     { es:'«Poner en la mesa» en una ficha, «+» en la lista o «Llevar a la mesa» en un equipo.',
                       en:'«Put on the desk» on a sheet, «+» on the list or «Take to the desk» on a team.' },
  ms_lider:          { es:'Líder',               en:'Leader' },
  ms_hacer_lider:    { es:'Hacer líder',         en:'Make leader' },
  ms_quitar:         { es:'Quitar',              en:'Remove' },
  ms_modo:           { es:'Modo',                en:'Mode' },
  ms_dia:            { es:'Día',                 en:'Day' },
  ms_dif:            { es:'Dificultad',          en:'Difficulty' },
  ms_restr:          { es:'Restricción del día', en:"Day's restriction" },
  ms_restr_src:      { es:'Alliance Battle, según thanosvibs', en:'Alliance Battle, per thanosvibs' },
  ms_recibe:         { es:'Lo que le llega a cada uno', en:'What reaches each one' },
  ms_recibe_nota:    { es:'Soportes de los demás y el propio, y el liderazgo del líder (el primero), si le sirven. * solo con el artefacto.',
                       en:"Supports from the others and their own, and the leader's leadership (the first one), if they serve them. * only with the artifact." },
  ms_bonos:          { es:'Bonos de equipo activos', en:'Active team bonuses' },
  ms_sin_bonos:      { es:'Ninguno con estos integrantes.', en:'None with these members.' },
  ms_nombre_ph:      { es:'Nombre (opcional)',   en:'Name (optional)' },
  ms_guardar:        { es:'Guardar en Mis equipos', en:'Save to My teams' },
  ms_vaciar:         { es:'Vaciar',              en:'Clear' },
  ms_guardado:       { es:'Guardado en Mis equipos: «{e}».', en:'Saved to My teams: «{e}».' },
  ms_pocos:          { es:'Para guardarlo hacen falta al menos 2.', en:'It takes at least 2 to save it.' },
  ms_ya:             { es:'{x} ya está en la mesa.', en:'{x} is already on the desk.' },
  ms_cambia:         { es:'{x} ya estaba en la mesa con otro uniforme: queda con este.', en:'{x} was already on the desk with another uniform: it now has this one.' },
  ms_poner:          { es:'Poner en la mesa',    en:'Put on the desk' },
  ms_en_mesa:        { es:'En la mesa',          en:'On the desk' },
  ms_cmp:            { es:'Comparar',            en:'Compare' },
  ms_cmp_vacio:      { es:'Hasta 4: «+ Comparar esta versión» en una ficha o «Comparar» en el roster.',
                       en:'Up to 4: «+ Compare this version» on a sheet or «Compare» on the roster.' },
  ms_cmp_ir:         { es:'Comparar {n} →',      en:'Compare {n} →' },
  ms_lista_n:        { es:'Personajes · {n} de {t}', en:'Characters · {n} of {t}' },
  ms_lista_tab:      { es:'Lista',               en:'List' },
  ms_ver_tab:        { es:'Ver',                 en:'View' },
  tm_lideres:        { es:'Estos equipos no tenían el líder declarado: quedó el que mostraba su tarjeta (el de la sinergia de la app). Revisalo en cada uno: {e}.',
                       en:'These teams had no declared leader: they got the one their card showed (the app synergy\'s). Check each one: {e}.' },
  base_word:         { es:'Base',                en:'Base' },
  st_add_mode:       { es:'+ Agregar modo',      en:'+ Add mode' },
  st_new_mode:       { es:'Modo nuevo',          en:'New mode' },
  st_sources:        { es:'Fuentes',             en:'Sources' },
  st_sources_txt:    { es:'Personajes, uniformes, skills, tier lists, C.T.P., artefactos, soportes, rotaciones, Alliance Battle, guía de principiantes, retratos e íconos: ',
                       en:"Characters, uniforms, skills, tier lists, C.T.P.s, artifacts, supports, rotations, Alliance Battle, Beginner's Guide, portraits and icons: " },
  st_sources_txt2:   { es:'. Instintos, requisitos de tier, reglas de ISO, urus y gear, y el contraste de docs/AUDITORIA.md: ',
                       en:'. Instincts, tier requirements, ISO, Uru and gear rules, and the cross-check in docs/AUDITORIA.md: ' },
  st_sources_txt3:   { es:'. Guía de armado por personaje (mejor uniforme, C.T.P., ISO-8, obelisco, rotación, artefacto y su tier list): ',
                       en:'. Per-character building guide (best uniform, C.T.P., ISO-8, Obelisk, rotation, artifact and its tier list): ' },
  st_sources_txt4:   { es:'. Uso personal, sin fin comercial.', en:'. Personal use, non-commercial.' },
  ga_st_note:        { es:'La planilla se revisa cada lunes, con los datos. Si cambió de formato y la app ya no la entiende, se sigue usando la última versión compatible y acá se avisa por qué.',
                       en:'The spreadsheet is checked every Monday along with the data. If its format changed and the app no longer understands it, the last compatible version stays in use and this section says why.' },
  ga_st_version:     { es:'Versión en uso',      en:'Version in use' },
  ga_st_taken:       { es:'tomada el {f}',       en:'taken on {f}' },
  ga_st_checked:     { es:'Última revisión',     en:'Last check' },
  ga_st_ok:          { es:'compatible',          en:'compatible' },
  ga_st_bad:         { es:'no se pudo usar',     en:'could not be used' },
  ga_st_chars:       { es:'Personajes',          en:'Characters' },
  ga_st_rejected:    { es:'El {f} la planilla{n} no se pudo usar: se sigue con la {v}, tomada el {t}. Motivos:',
                       en:'On {f} the spreadsheet{n} could not be used: still on {v}, taken on {t}. Reasons:' },
  ga_st_nopj:        { es:'Filas de la guía sin personaje en la app ({n})', en:'Guide rows with no character in the app ({n})' },
  ga_st_raros:       { es:'Valores que la app no interpreta y muestra tal cual ({n})', en:'Values the app does not interpret and shows as is ({n})' },
  st_confirm_reset:  { es:'Se borran tus equipos, listas, ediciones e imágenes. Los datos del juego no se tocan. ¿Seguimos?',
                       en:'This deletes your teams, lists, edits and images. Game data is untouched. Continue?' },
  st_bad_import:     { es:'Ese archivo no es una capa de usuario válida: ', en:'That file is not a valid user layer: ' },
  st_translation:    { es:'Traducción',          en:'Translation' },
  st_translation_txt:{ es:'Los efectos y los nombres de skill están traducidos por patrón, con el original a la vista. Los nombres de personaje y de uniforme quedan en inglés a propósito: son el identificador con el que se cruza el juego, la wiki y thanosvibs.',
                       en:'Effects and skill names are translated by pattern, with the original in view. Character and uniform names stay in English on purpose: they are the identifier used to cross-reference the game, the wiki and thanosvibs.' },

  st_stage:          { es:'Etapa',               en:'Stage' },
  st_activation:     { es:'Se activa',           en:'Activates' },
  st_target:         { es:'Objetivo',            en:'Target' },
  al_ver:            { es:'Ver qué personajes cumplen este objetivo', en:'See which characters this target covers' },
  al_count:          { es:'{n} personajes',      en:'{n} characters' },
  al_by_uniform:     { es:'Cuenta el uniforme que lleva puesto: la clase, el bando, la raza y las habilidades pueden cambiar con el uniforme.',
                       en:'The uniform worn is what counts: class, side, race and abilities can change with the uniform.' },
  al_only_with:      { es:'Solo con',            en:'Only with' },
  al_except_with:    { es:'Salvo con',           en:'Except with' },
  al_none:           { es:'Ningún personaje lo cumple con los datos actuales.', en:'No character matches it with the current data.' },
  al_close:          { es:'Cerrar',              en:'Close' },
  c_ult:             { es:'Ult',                 en:'Ult' },
  every:             { es:'cada',                en:'every' },
  permanent_fx:      { es:'permanente',          en:'permanent' },
  team_fx:           { es:'al equipo',           en:'team' },
  c_keybuffs:        { es:'Buffs clave',         en:'Key buffs' },
  c_uni_cost:        { es:'Costo de mejora',     en:'Upgrade cost' },
  c_dmg_total:       { es:'Daño total de activas', en:'Total active damage' },
  d_kits:            { es:'Kits',                en:'Kits' },
  d_gold:            { es:'Oro',                 en:'Gold' },
  d_xp:              { es:'XP',                  en:'XP' },
  tpl_title:         { es:'La fuente no especifica cuál: publica un marcador de plantilla sin resolver.',
                       en:'The source does not say which: it publishes an unresolved template marker.' },
  tpl_unspec:        { es:'sin especificar',      en:'unspecified' },
  tpl_pending:       { es:'thanosvibs publica este efecto sin decir a quién se refiere, y ni Leads & Supports ni la wiki de Future Fight lo dicen. Se completa a mano en scripts/contenido/marcadores.csv (la lista está en docs/AUDITORIA.md).',
                       en:'thanosvibs publishes this effect without saying whom it refers to, and neither Leads & Supports nor the Future Fight wiki says so. It is filled in by hand in scripts/contenido/marcadores.csv (the list is in docs/AUDITORIA.md).' },
  tpl_wiki:          { es:'Dato de la wiki de Future Fight: thanosvibs publica este efecto sin decir a quién se refiere.',
                       en:'From the Future Fight wiki: thanosvibs publishes this effect without saying whom it refers to.' },
  tpl_manual:        { es:'Dato cargado a mano (scripts/contenido/marcadores.csv): thanosvibs publica este efecto sin decir a quién se refiere.',
                       en:'Entered by hand (scripts/contenido/marcadores.csv): thanosvibs publishes this effect without saying whom it refers to.' },
  tpl_ls:            { es:'Dato de Leads & Supports de thanosvibs: la skill publica este efecto sin decir a quién se refiere.',
                       en:'From thanosvibs Leads & Supports: the skill publishes this effect without saying whom it refers to.' },
  // índice para armar equipos (CATEGORIAS)
  ct_title:          { es:'Lo que da, en las categorías para armar equipos', en:'What it gives, in the team-building categories' },
  ct_fis:            { es:'Ataque físico',        en:'Physical Attack' },
  ct_ene:            { es:'Ataque de energía',    en:'Energy Attack' },
  ct_atk:            { es:'Todos los ataques',    en:'All Attacks' },
  ct_fuego:          { es:'Daño de fuego',        en:'Fire Damage' },
  ct_hielo:          { es:'Daño de hielo',        en:'Cold Damage' },
  ct_rayo:           { es:'Daño eléctrico',       en:'Lightning Damage' },
  ct_veneno:         { es:'Daño de veneno',       en:'Poison Damage' },
  ct_mente:          { es:'Daño mental',          en:'Mind Damage' },
  ct_elems:          { es:'Daño de todos los elementos', en:'All Element Damage' },
  ct_evasion:        { es:'Ignorar evasión',      en:'Ignore Dodge' },
  ct_defensas:       { es:'Todas las defensas',   en:'All Defenses' },
  ct_vida:           { es:'Vida',                 en:'HP' },
  ct_mermas:         { es:'Anti-mermas',         en:'Debuff removal' },
  f_lid:             { es:'Su liderazgo da',      en:'Its leadership gives' },
  f_sop:             { es:'Su soporte da',        en:'Its support gives' },
  f_para:            { es:'Que le llegue y le sirva a', en:'Reaching and useful to' },
  f_para_how:        { es:'Se elige desde la ficha de un personaje: Resumen › «Líderes que se lo dan».',
                       en:'Chosen from a character sheet: Summary › "Leaders that give it".' },
  f_para_rm:         { es:'Quitar',               en:'Remove' },
  f_para_gone:       { es:'un personaje que ya no está en los datos (no filtra)', en:'a character no longer in the data (not filtering)' },
  f_restr:           { es:'Liderazgo o soporte solo para', en:'Leadership or support only for' },
  cd_lid:            { es:'Liderazgo',            en:'Leadership' },
  cd_sop:            { es:'Soporte',              en:'Support' },
  ls_title:          { es:'Le sirve de un liderazgo o un soporte:', en:'Useful to it from a leadership or support:' },
  ls_note:           { es:'El ataque, según el daño de sus skills activas: con qué ataque escala y qué elementos lleva.',
                       en:'Attack, by the damage of its active skills: which attack it scales with and which elements it carries.' },
  ls_also:           { es:'y, como a cualquiera:', en:'and, like anyone:' },
  ls_leaders:        { es:'Líderes que se lo dan', en:'Leaders that give it' },
  ls_supports:       { es:'Soportes que se lo dan', en:'Supports that give it' },
  cb_note:           { es:'Debajo de cada una, lo que recibe él: los soportes de sus compañeros y los suyos, sus anti-mermas propios (los de sus skills; uno con probabilidad no cuenta) y el liderazgo del líder elegido (también si el líder es él), solo lo que le llega y le sirve. ✓ lo recibe, ✗ no; * solo si el compañero lleva su artefacto. No cambia los puntos: en la sinergia, un soporte cuenta si a otro se le aplica algo que le sirve.',
                       en:'Under each one, what it gets: its teammates\' supports and its own, its own debuff removal (from its skills; one with a probability does not count) and the chosen leader\'s leadership (also when it is the leader), only what reaches it and is useful to it. ✓ it gets it, ✗ it does not; * only if the teammate has its artifact. It does not change the points: in the synergy, a support counts if it gives another member something useful that applies to it.' },
  cb_ataque:         { es:'Ataque',               en:'Attack' },
  cb_art:            { es:'* Solo si el compañero que lo da lleva su artefacto.', en:'* Only if the teammate who gives it has its artifact.' },
  pt_art:            { es:'* Cuenta el soporte del artefacto de un integrante, como si lo llevara: vale solo si lo lleva.',
                       en:'* It counts a member\'s artifact support as if it were equipped: it only applies if it is.' },
  c_targets:         { es:'Beneficia a',          en:'Buffs' },
  c_attrs:           { es:'Atributos marcados',   en:'Marked attributes' },
  f_attrs:           { es:'Atributo marcado por vos', en:'Attribute you marked' },
  at_edit:           { es:'Marcar atributos',     en:'Mark attributes' },
  at_done:           { es:'Listo',                en:'Done' },
  at_mark:           { es:'Marcar:',              en:'Mark:' },
  st_marks:          { es:'Skills con marcas',    en:'Skills with marks' },
  st_routes:         { es:'Hojas de ruta marcadas', en:'Roadmaps marked' },
  st_caps:           { es:'Topes cargados',      en:'Cap sheets' },
  f_targets:         { es:'Beneficia a (buffs de equipo)', en:'Buffs (team-wide effects)' },
  f_any_target:      { es:'— cualquiera —',        en:'— any —' },
  ac_title:           { es:'Actualizaciones',     en:'Updates' },
  ac_note:            { es:'La app busca datos nuevos cada vez que se abre y los baja sola. Salen de GitHub, donde se arman cada lunes a partir de thanosvibs, la wiki y la guía de armado de Cynicalex.',
                        en:'The app looks for new data every time it opens and downloads it on its own. It comes from GitHub, where it is built every Monday from thanosvibs, the wiki and Cynicalex’s building guide.' },
  ac_app:             { es:'Versión de la app',   en:'App version' },
  ac_local:           { es:'Datos del juego',     en:'Game data' },
  ac_built:           { es:'armados el',          en:'built on' },
  ac_remote:          { es:'Publicados en GitHub', en:'Published on GitHub' },
  ac_checked:         { es:'consultado a las',    en:'checked at' },
  ac_check:           { es:'Buscar ahora',        en:'Check now' },
  ac_checking:        { es:'Buscando…',           en:'Checking…' },
  ac_uptodate:        { es:'Estás al día.',       en:'You are up to date.' },
  ac_new:             { es:'Hay datos nuevos.',   en:'New data available.' },
  ac_folder:          { es:'Carpeta de datos',    en:'Data folder' },
  ac_folder_note:     { es:'Ahí están capa.json (tus listas, equipos y ajustes) y respaldos/, con una copia por día.',
                        en:'It holds capa.json (your lists, teams and settings) and respaldos/, with one copy per day.' },
  av_dl:              { es:'Bajando datos nuevos del juego', en:'Downloading new game data' },
  av_dl_done:         { es:'Datos del juego actualizados', en:'Game data updated' },
  av_dl_use:          { es:'Usar ahora',          en:'Use now' },
  av_dl_use_t:        { es:'Recarga la ventana',  en:'Reloads the window' },
  av_dl_err:          { es:'No se pudieron bajar los datos nuevos:', en:'The new data could not be downloaded:' },
  av_incompat:        { es:'Hay datos nuevos del juego, pero son para una versión más nueva de la app.',
                        en:'There is new game data, but it is for a newer version of the app.' },
  av_check_err:       { es:'No se pudo buscar actualizaciones:', en:'Could not check for updates:' },
  av_hide:            { es:'Ocultar',             en:'Hide' },
  ac_new_app:         { es:'Hay una versión nueva de la app.', en:'There is a new app version.' },
  ap_new:             { es:'Versión {v} disponible.', en:'Version {v} available.' },
  ap_go:              { es:'Actualizar',          en:'Update' },
  ap_notes:           { es:'Novedades',           en:"What's new" },
  ap_confirm:         { es:'¿Actualizar la app a la versión {v}? Se reinicia sola; tus datos no se tocan.',
                        en:'Update the app to version {v}? It restarts on its own; your data is not touched.' },
  ap_updating:        { es:'Actualizando la app a la versión {v}…', en:'Updating the app to version {v}…' },
  ap_restart:         { es:'Versión {v} instalada. Reiniciando…', en:'Version {v} installed. Restarting…' },
  ap_err:             { es:'No se pudo actualizar la app:', en:'The app could not be updated:' },
  ap_installer:       { es:'Cambia la base del programa: hace falta el instalador completo (tus datos no se tocan).',
                        en:'The program base changes: the full installer is needed (your data is not touched).' },
  ap_installer_go:    { es:'Bajar instalador',    en:'Download installer' },
  ap_repo:            { es:'Estás usando la app desde el repo: se actualiza con git pull.',
                        en:'You are running the app from the repo: update it with git pull.' },
  av_img:             { es:'Bajando retratos e íconos:', en:'Downloading portraits and icons:' },
  av_img_n:           { es:'{n} de {total}',      en:'{n} of {total}' },
  av_img_err:         { es:'Faltan imágenes:',    en:'Missing images:' },
  ac_img:             { es:'Retratos e íconos',   en:'Portraits and icons' },
  ac_img_ok:          { es:'los {total}, completos.', en:'all {total}, complete.' },
  ac_img_miss:        { es:'faltan {n} de {total}.', en:'{n} of {total} missing.' },
  ac_img_np:          { es:'{n} no están publicados en thanosvibs (se muestra el nombre sin ícono).',
                        en:'{n} are not published on thanosvibs (the name is shown without an icon).' },
  pd_title:           { es:'Actualizando los datos del juego', en:'Updating game data' },
  pd_note:            { es:'Esta versión de la app usa datos de otro formato: se bajan de GitHub y la ventana se recarga sola.',
                        en:'This app version uses data in another format: it is downloaded from GitHub and the window reloads on its own.' },
  pd_nueva:           { es:'Los datos publicados son de formato {r} y esta versión de la app ({v}) usa el {a}: los lee una versión más nueva de la app. Actualizala acá abajo; tus datos y tu capa no se tocan.',
                        en:'The published data is format {r} and this app version ({v}) uses {a}: a newer app version reads it. Update it below; your data and your layer are not touched.' },
  pd_nueva_falta:     { es:'Los datos publicados son de formato {r} y esta versión de la app ({v}) usa el {a}, pero la versión de la app que los lee todavía no está publicada: volvé a abrir la app en un rato.',
                        en:'The published data is format {r} and this app version ({v}) uses {a}, but the app version that reads it is not published yet: open the app again in a while.' },
  pd_vieja:           { es:'Los datos publicados son de formato {r} y esta versión de la app usa el {a}: esperá a la próxima publicación de datos y volvé a abrir la app.',
                        en:'The published data is format {r} and this app version uses {a}: wait for the next data publication and open the app again.' },
  pd_err_nov:         { es:'No se pudo consultar qué hay publicado en GitHub:', en:'Could not check what is published on GitHub:' },
  sy_srv_down:        { es:'Se cerró el programa de la app.', en:'The app program closed.' },
  sy_srv_down_note:   { es:'Esta ventana sigue con lo que ya había cargado, pero tus cambios no se guardan, los retratos e íconos que no estaban cargados no aparecen y la sincronización no anda. Cerrala y abrí la app de nuevo; si vuelve a pasar, el motivo queda en registro.txt, en la carpeta de datos.',
                        en:'This window keeps what it had already loaded, but your changes are not saved, portraits and icons that were not loaded yet do not show up and sync does not work. Close it and open the app again; if it happens again, the reason is in registro.txt, in the data folder.' },
  gd_error:           { es:'No se guardó tu último cambio.', en:'Your last change was not saved.' },
  gd_retry:           { es:'Reintentar',            en:'Retry' },
  ar_file_t:          { es:'Esta app se abre desde su acceso directo', en:'This app opens from its shortcut' },
  ar_file:            { es:'Abrir index.html suelto no funciona: tus listas, equipos y ajustes se guardan a través del programa. Abrila desde su acceso directo (o con MFF.bat, desde el repo).',
                        en:'Opening index.html directly does not work: your lists, teams and settings are saved through the program. Open it from its shortcut (or with MFF.bat, from the repo).' },
  ar_capa_t:          { es:'No se pudo cargar tu capa', en:'Your layer could not be loaded' },
  ar_capa:            { es:'La app no arranca para no pisar lo que tenés guardado. Si el archivo capa.json se dañó, en la carpeta respaldos/ hay copias de los últimos días.',
                        en:'The app does not start so it does not overwrite what you have saved. If capa.json got damaged, the respaldos/ folder has copies from the last few days.' },
  lang_title:        { es:'Ver la app en inglés', en:'View the app in Spanish' },
  untranslated:      { es:'sin traducir',        en:'untranslated' },
};
function t (k) {
  const e = T[k];
  if (!e) throw new Error('cadena sin definir en la tabla de idioma: ' + k);
  return e[LANG];
}
/** Valor del dominio (clase, rol, slot, etiqueta) en un idioma. */
function domIdioma (v, lang) {
  if (lang === 'es' || v == null) return v;
  const en = VOCAB_EN[v];
  if (en === undefined) { console.warn('valor de dominio sin inglés en MFF_VOCAB_EN:', v); return v; }
  return en;
}
/** En el idioma activo. Un solo parámetro: se usa como .map(dom). */
function dom (v) { return domIdioma(v, LANG); }
let LANG = U.prefs.lang;

// ---------------------------------------------------------------------------
// APP DE ESCRITORIO
// La app corre servida por desktop/servidor.py: ese proceso guarda la capa del usuario
// y puede llamar a thanosvibs (el navegador no: la API no manda
// Access-Control-Allow-Origin).
// ---------------------------------------------------------------------------
let ESCRITORIO = null;               // respuesta de /api/estado (se pide en arrancar)
async function apiLocal (ruta, metodo) {
  const r = await fetch(ruta, { method: metodo || 'GET', headers: { 'X-MFF': '1' } });
  const cuerpo = await r.json();
  if (!r.ok) throw new Error(cuerpo.error || ('HTTP ' + r.status));
  return cuerpo;
}

// ---- actualizaciones ----
// Al abrir se pregunta a GitHub (vía el servidor) si hay datos nuevos. Si hay y son del
// formato de esta versión, se bajan solos con el avance a la vista; al terminar, un botón
// recarga la ventana para usarlos (no se recarga sola: podrías estar a mitad de algo).
// Un error queda a la vista: nunca se traga.
const NOV = { buscando: false, hora: null, datos: null, app: null, oculto: false };
// Estado de las tareas que arrancó esta página (una tarea terminada antes de recargar no
// vuelve a avisar).
const PROG = { datos: null, imagenes: null, app: null, poll: null };
let REINICIANDO = null;               // versión que se espera después de aplicar un parche
async function buscarNovedades () {
  NOV.buscando = true; pintarActualizaciones();
  try {
    const n = await apiLocal('/api/novedades');
    NOV.datos = n.datos; NOV.app = n.app; NOV.hora = new Date(); NOV.oculto = false;
    if (n.datos.hay && n.datos.compatible) arrancarTarea('datos', '/api/datos/actualizar');
  } catch (e) { NOV.datos = { error: e.message }; verificarServidor(); }
  NOV.buscando = false;
  pintarAvisos(); pintarActualizaciones();
}
async function arrancarTarea (nombre, ruta) {
  try { PROG[nombre] = await apiLocal(ruta, 'POST'); }
  catch (e) { PROG[nombre] = { error: e.message, terminado: true }; pintarAvisos(); pintarActualizaciones(); return; }
  pintarAvisos();
  if (!PROG.poll) PROG.poll = setInterval(seguirTareas, 700);
}
async function seguirTareas () {
  let p;
  try { p = await apiLocal('/api/progreso'); }
  catch (e) {
    clearInterval(PROG.poll); PROG.poll = null;
    // Si se estaba aplicando un parche, lo más probable es que ya esté reiniciando.
    if (PROG.app && PROG.app.corriendo) esperarReinicio(NOV.app.version); else verificarServidor();
    return;
  }
  let siguen = false;
  for (const n of ['datos', 'imagenes', 'app']) {
    if (!PROG[n] || PROG[n].terminado) continue;
    PROG[n] = p[n];
    if (p[n].corriendo) siguen = true;
    if (n === 'app' && p[n].terminado && !p[n].error) esperarReinicio(p[n].resultado.version);
    if (n === 'imagenes') {
      refrescarImagenes();
      if (p[n].terminado) { try { ESCRITORIO = await apiLocal('/api/estado'); } catch (e) {} }
    }
  }
  if (!siguen) { clearInterval(PROG.poll); PROG.poll = null; }
  pintarAvisos(); pintarActualizaciones();
}
/** Aplicado un parche, el programa se relanza en el mismo puerto: se espera a que conteste
 *  con la versión nueva y se recarga la ventana. */
function esperarReinicio (version) {
  REINICIANDO = version; pintarAvisos();
  const limite = Date.now() + 60000;
  const intento = setInterval(async () => {
    try {
      const e = await apiLocal('/api/estado');
      if (e.version === version) { clearInterval(intento); recargar(); }
    } catch (e) {}
    if (Date.now() > limite) { clearInterval(intento); REINICIANDO = null; SERVIDOR_CAIDO = true; pintarAvisos(); }
  }, 1000);
}
function actualizarApp () {
  const a = NOV.app;
  if (!confirm(t('ap_confirm').replace('{v}', a.version) + (a.notas ? '\n\n' + a.notas : ''))) return;
  arrancarTarea('app', '/api/app/actualizar');
}
/** Mientras bajan las imágenes, las que se veían rotas se vuelven a pedir: van
 *  apareciendo sin redibujar la vista. */
function refrescarImagenes () {
  document.querySelectorAll('img').forEach(img => {
    if (img.complete && img.naturalWidth === 0 && /\/images\//.test(img.src)) img.src = img.src.split('?')[0] + '?r=' + Date.now();
  });
}
/** Recarga la ventana volviendo a la misma sección (la ficha abierta no se conserva). */
const VISTAS_PRINCIPALES = ['roster', 'tierlist', 'modos', 'teams', 'glosario', 'historico', 'settings'];
function recargar () {
  try { sessionStorage.setItem('mff_volver', VISTAS_PRINCIPALES.includes(ui.view) ? ui.view : 'roster'); } catch (e) {}
  location.reload();
}
function mb (bytes) { return (bytes / 1048576).toFixed(1).replace('.', LANG === 'es' ? ',' : '.') + ' MB'; }
/** Primer arranque de una versión que usa otro formato de datos (o sin data.js): baja
 *  los publicados antes de mostrar nada, porque la app no puede leer los que hay. Primero pregunta qué hay publicado: si
 *  los datos son de un formato más nuevo que el de esta versión, no hay nada que bajar y se ofrece la versión de la app
 *  que los lee (el mismo aviso de siempre, con su botón o el instalador; antes de la 1.0.24 esta pantalla no lo ofrecía
 *  y la app quedaba trabada: le pasó a la 1.0.22 el 5 de octubre de 2026); si son de uno más viejo, se espera a la
 *  próxima publicación. */
async function pantallaDatos () {
  const pintar = (extra) => pantallaFatal(t('pd_title'), t('pd_note') + (extra ? ' ' + extra : ''));
  pintar();
  let n;
  try { n = await apiLocal('/api/novedades'); }
  catch (e) { return pintar(t('pd_err_nov') + ' ' + e.message); }
  if (n.datos.error) return pintar(t('pd_err_nov') + ' ' + n.datos.error);
  NOV.datos = n.datos; NOV.app = n.app; NOV.hora = new Date();
  const r = n.datos.remoto.formato, a = ESCRITORIO.formato_datos;
  const txt = (k) => t(k).replace('{r}', r).replace('{a}', a).replace('{v}', ESCRITORIO.version);
  if (r > a) {
    if (n.app.error) return pantallaFatal(t('pd_title'), txt('pd_nueva') + ' ' + t('pd_err_nov') + ' ' + n.app.error);
    if (!n.app.hay) return pantallaFatal(t('pd_title'), txt('pd_nueva_falta'));
    $('#app').innerHTML = `<main><div class="fatal"><h1>${h(t('pd_title'))}</h1><p>${h(txt('pd_nueva'))}</p><div id="avisos"></div></div></main>`;
    return pintarAvisos();
  }
  if (r < a) return pantallaFatal(t('pd_title'), txt('pd_vieja'));
  try { await apiLocal('/api/datos/actualizar', 'POST'); }
  catch (e) { return pintar(t('av_dl_err') + ' ' + e.message); }
  const poll = setInterval(async () => {
    let p;
    try { p = (await apiLocal('/api/progreso')).datos; }
    catch (e) { clearInterval(poll); return pintar(t('av_dl_err') + ' ' + e.message); }
    if (p.terminado) {
      clearInterval(poll);
      return p.error ? pintar(t('av_dl_err') + ' ' + p.error) : location.reload();
    }
    if (p.total) pintar(`${mb(p.hecho)} / ${mb(p.total)}`);
  }, 700);
}
// Si el servidor se cae con la ventana abierta, la página sigue con app.js y data.js ya
// cargados: lo que no esté cargado (retratos, íconos, guardar la capa, la sincronización)
// falla, y un retrato roto no dice por qué. Cuando algo no carga se le pregunta al
// servidor si sigue ahí; si no contesta, se avisa arriba de todo. Una consulta a la vez:
// una página de retratos rotos dispara decenas de errores juntos.
let SERVIDOR_CAIDO = false, verificandoServidor = false;
function verificarServidor () {
  if (SERVIDOR_CAIDO || verificandoServidor || REINICIANDO) return;
  verificandoServidor = true;
  fetch('/api/estado', { headers: { 'X-MFF': '1' }, cache: 'no-store' })
    .then(() => {}, () => { SERVIDOR_CAIDO = true; pintarAvisos(); })
    .finally(() => { verificandoServidor = false; });
}
/** Avisos de la app que van arriba de cualquier vista: servidor cerrado y capa sin
 *  guardar. Se repintan solos (pintarAvisos) sin redibujar la vista. */
function avisosHtml () {
  const out = [];
  if (SERVIDOR_CAIDO) out.push(`<div class="srvcaido"><b>${h(t('sy_srv_down'))}</b> ${h(t('sy_srv_down_note'))}</div>`);
  if (GUARDADO.error) out.push(`<div class="srvcaido"><b>${h(t('gd_error'))}</b> ${h(GUARDADO.error)}
    <button class="btn sm" data-a="reintentarGuardado">${h(t('gd_retry'))}</button></div>`);
  const p = PROG.datos, r = (NOV.datos && NOV.datos.remoto) || {};
  if (p && p.corriendo) {
    const pct = p.total ? Math.round(100 * p.hecho / p.total) : 0;
    out.push(`<div class="aviso-app"><b>${h(t('av_dl'))} ${h(r.juego || '')}</b> ${p.total ? h(mb(p.hecho) + ' / ' + mb(p.total)) : ''}
      <div class="barra"><i style="width:${pct}%"></i></div></div>`);
  } else if (p && p.terminado && p.error) {
    out.push(`<div class="srvcaido"><b>${h(t('av_dl_err'))}</b> ${h(p.error)}
      <button class="btn sm" data-a="reintentarDatos">${h(t('gd_retry'))}</button></div>`);
  } else if (p && p.terminado) {
    out.push(`<div class="aviso-app ok"><b>${h(t('av_dl_done'))} ${h(r.juego || '')}.</b>
      <button class="btn sm primary" data-a="usarDatos" title="${h(t('av_dl_use_t'))}">${h(t('av_dl_use'))}</button></div>`);
  }
  const im = PROG.imagenes;
  if (ESCRITORIO.imagenes.error) out.push(`<div class="srvcaido"><b>${h(t('av_img_err'))}</b> ${h(ESCRITORIO.imagenes.error)}</div>`);
  if (im && im.corriendo) {
    const pct = im.total ? Math.round(100 * im.hecho / im.total) : 0;
    out.push(`<div class="aviso-app"><b>${h(t('av_img'))}</b> ${h(t('av_img_n').replace('{n}', im.hecho).replace('{total}', im.total))}
      <div class="barra"><i style="width:${pct}%"></i></div></div>`);
  } else if (im && im.terminado && im.error) {
    out.push(`<div class="srvcaido"><b>${h(t('av_img_err'))}</b> ${h(im.error)}
      <button class="btn sm" data-a="reintentarImagenes">${h(t('gd_retry'))}</button></div>`);
  }
  const ap = PROG.app, na = NOV.app;
  if (REINICIANDO) out.push(`<div class="aviso-app ok"><b>${h(t('ap_restart').replace('{v}', REINICIANDO))}</b></div>`);
  else if (ap && ap.corriendo) {
    const pct = ap.total ? Math.round(100 * ap.hecho / ap.total) : 0;
    out.push(`<div class="aviso-app"><b>${h(t('ap_updating').replace('{v}', na.version))}</b><div class="barra"><i style="width:${pct}%"></i></div></div>`);
  } else if (ap && ap.terminado && ap.error) {
    out.push(`<div class="srvcaido"><b>${h(t('ap_err'))}</b> ${h(ap.error)}
      <button class="btn sm" data-a="actualizarApp">${h(t('gd_retry'))}</button></div>`);
  } else if (na && na.hay) {
    const notas = na.notas ? `<details class="notas"><summary>${h(t('ap_notes'))}</summary>${h(na.notas)}</details>` : '';
    if (ESCRITORIO.desde_repo) out.push(`<div class="aviso-app"><b>${h(t('ap_new').replace('{v}', na.version))}</b> ${h(t('ap_repo'))}${notas}</div>`);
    else if (na.aplicable) out.push(`<div class="aviso-app"><b>${h(t('ap_new').replace('{v}', na.version))}</b>
      <button class="btn sm primary" data-a="actualizarApp">${h(t('ap_go'))}</button>${notas}</div>`);
    else out.push(`<div class="aviso-app"><b>${h(t('ap_new').replace('{v}', na.version))}</b> ${h(t('ap_installer'))}
      <a class="btn sm primary" href="${h(na.instalador)}" target="_blank" rel="noopener">${h(t('ap_installer_go'))}</a>${notas}</div>`);
  }
  if (NOV.datos && NOV.datos.hay && !NOV.datos.compatible) out.push(`<div class="aviso-app">${h(t('av_incompat'))}</div>`);
  const errores = [NOV.datos && NOV.datos.error, NOV.app && NOV.app.error].filter(Boolean);
  if (errores.length && !NOV.oculto) out.push(`<div class="aviso-app">${h(t('av_check_err'))} ${h([...new Set(errores)].join(' · '))}
    <button class="btn sm" data-a="ocultarAviso">${h(t('av_hide'))}</button></div>`);
  return out.join('');
}
function pintarAvisos () { const el = $('#avisos'); if (el) el.innerHTML = avisosHtml(); }
/** La ventana avisa que sigue abierta: el servidor se apaga solo cuando ninguna late
 *  (desktop/lanzador.py). Al volver a primer plano late enseguida, porque minimizada el
 *  navegador espacia los timers. */
function latir () {
  fetch('/api/latido', { method: 'POST', headers: { 'X-MFF': '1' } }).then(() => {}, () => verificarServidor());
}

// ============================================================================
// ESTADO DE UI (no persistido)
// ============================================================================
let ui = {
  view: 'roster', search: '', page: 0,
  pickMode: false, picks: [], avisoPick: null,  // avisoPick: por qué no se sumó la última que se tocó
  charId: null, uniformId: 'base',
  tierList: (TIERLISTS_SEED[0] || {}).id || '',
  avisoMesa: null,                   // { txt, ok }: por qué la mesa no sumó al último que se puso, o que se guardó (ok)
  movil: 'centro',                   // ventana angosta: qué panel se ve ('lista', 'centro' o 'mesa')
  plFiltros: false,                  // la lista de la izquierda con el panel de filtros abierto
  avisoLideres: null,                // equipos de antes a los que se les declaró el líder al cargar la capa (declararLideres)
  newListName: '', newListTpl: 'rango', newListKind: 'personajes', editRows: false, poolOpen: false, poolSearch: '', marcando: false,
  edStep: 0, edDraft: null, edId: null,
  dragKey: null, dragFrom: '', tlPick: null,
  aliados: null,                     // objetivo de grupo cuya lista de personajes está abierta
  tip: null,                         // «Cómo funciona» abierto: { key de la variante, si: skill, ti y fi: el efecto tocado o null }
  fichaTab: 'resumen',               // pestaña de la ficha; se conserva al pasar de un personaje a otro
  modoFiltro: 'todos', modoAbierto: null, abxDia: 1,
  glBusca: '',                       // búsqueda del glosario
  glTab: 'juego',                    // pestaña del glosario: 'juego' (sus términos) o 'app' (el catálogo de efectos)
  hiPj: '', hiTipo: 'todos', hiN: 20, // Histórico: personaje, tipo de hecho y cuántas versiones se ven
  artEst: '6',                       // nivel de estrellas que muestra el artefacto de la ficha
  // combinaciones de 3 de la pestaña Equipos: orden, filtros (se excluye por personaje) y página
  eqOrden: 'foco', eqExcluir: [], eqCon: '', eqPagina: 0, eqCalculando: null,
  eqCobertura: [],                   // grupos de COBERTURA marcados: solo los tríos en que los recibe
  eqUltimo: false,                   // «Solo el último uniforme»: de cada compañero, solo su uniforme más nuevo
  eqVerDescartados: false,           // la lista muestra solo los descartados, para restaurarlos
  volverY: null,                     // posición a la que se vuelve con «Atrás» (ver HISTORIAL)
  volverAbiertos: [],                // plegados que se vuelven a abrir con «Atrás» (ver HISTORIAL)
  pq: null,                          // ventana del «Por qué» abierta: { id de su tarjeta, charId y uid de la ficha, tab, y }
  volverPq: null,                    // la que se vuelve a abrir con «Atrás» (ver HISTORIAL)
  entradaNueva: false                // el próximo render abre otra entrada del historial aunque no cambie el lugar
};

// ============================================================================
// HELPERS
// ============================================================================
const $ = (s, r) => (r || document).querySelector(s);
/** Texto escapado para HTML, en el contenido o en un atributo: también las comillas, que innerHTML deja como están
 *  (un title con «"Give Power"» se cortaba en la primera). */
function h (v) {
  const d = document.createElement('div'); d.textContent = v == null ? '' : String(v);
  return d.innerHTML.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
function classColor (c) { return ({'Combate':'var(--class-combate)','Detonación':'var(--class-detonacion)','Velocidad':'var(--class-velocidad)','Universal':'var(--class-universal)'})[c] || 'var(--text-3)'; }
function dmgColor (d) { return ({'Físico':'var(--dmg-fisico)','Energía':'var(--dmg-energia)','PG':'var(--dmg-pg)'})[d] || 'var(--text-3)'; }
function tierColor (t) { return ({'T2':'var(--tier-t2)','T3':'var(--tier-t3)','T4':'var(--tier-t4)'})[t] || 'var(--text-3)'; }
function roleColor (r) { return ({'Daño':'var(--role-dano)','Soporte':'var(--role-soporte)','Control':'var(--role-control)','Tanque':'var(--role-tanque)'})[r] || 'var(--line-2)'; }
function rowColor (i, n) {
  const scale = ['#ff6a5c','#ff6b3d','#ffb020','#7ed957','#4dd0e1','#7aa8ff','#a78bfa','#8a8f9c','#6b7080'];
  return scale[Math.min(i, scale.length - 1)] || '#6b7080';
}
function tagSolid (label, color) { return `<span class="tag solid" style="background:${color}">${h(label)}</span>`; }
function tagGhost (label, color) { return `<span class="tag ghost" style="color:${color}">${h(label)}</span>`; }
function icon (value) { const u = imgUrl('icon-' + value); return u ? `<img src="${u}" alt="" style="width:15px;height:15px;border-radius:3px;vertical-align:-3px">` : ''; }
function shot (id, cls) { const u = imgUrl('portrait-' + id); return u ? `<img class="${cls||''}" src="${u}" alt="" loading="lazy">` : `<span class="ph">SIN RETRATO</span>`; }
function slotClass (slot) { return slot === 'Liderazgo' ? 'lead' : slot === 'Pasiva' ? 'pass' : slot === 'Definitiva' ? 'ult' : ''; }
function pluralUni (n) { return LANG === 'es' ? n + (n === 1 ? ' uniforme' : ' uniformes')
                                                : n + (n === 1 ? ' uniform' : ' uniforms'); }
/** La wiki no publica el instinto de todos: mostrar "Desconocido" es ruido, se omite. */
function insTag (v) { return v && v !== 'Desconocido' ? `<span class="tag dim">${h(dom(v))}</span>` : ''; }
/** Marca de trascendido: glifo aparte porque no todas las fuentes de texto traen ✦. */
function transTag (on) { return on ? `<span class="tag solid" style="background:var(--gold)" title="${h(t('transcended_tag'))}">TR</span>` : ''; }

function findUniform (ch, uid) { return ch && ch.uniforms.find(u => u.id === uid); }
/** Vista efectiva de "personaje base" o "personaje con uniforme X": el uniforme pisa lo que redefine. */
/** Vista efectiva de "base" o "personaje con uniforme X". Las skills salen del set
 *  del retrato correspondiente: cada uniforme tiene el suyo en la API. */
function variant (cid, uid) {
  const ch = CHAR_BY_ID[cid]; if (!ch) return null;
  const u = uid && uid !== 'base' ? findUniform(ch, uid) : null;
  const p = u ? u.p : ch.p;
  const skills = SKILLS[p] || [];
  if (!u) return { cid: ch.id, uid: null, key: ch.id + '::base', id: ch.id, name: ch.name, sub: 'Base',
                   c: ch.c, f: ch.f, race: ch.race, gender: ch.gender, t: ch.t, ins: ch.ins, r: ch.r, ab: ch.abilities || [],
                   striker: ch.striker, wba: ch.wba, trans: ch.trans, nuevo: ch.new, cost: '',
                   p, up: null, op: null, ch, skills };
  return { cid: ch.id, uid: u.id, key: ch.id + '::' + u.id, id: u.id, name: ch.name, sub: u.name,
           c: u.c || ch.c, f: u.f || ch.f, race: u.race || ch.race, gender: u.gender || ch.gender,
           t: u.tier || ch.t, ins: ch.ins, r: u.r || ch.r,
           ab: u.ab || ch.abilities || [],
           striker: u.striker != null ? u.striker : ch.striker, wba: u.wba || ch.wba,
           trans: u.trans, nuevo: u.new, cost: u.cost || '',
           p, up: u.up || null, op: u.op || null, ch, skills };
}
/** Totales que muestra thanosvibs: carga combinada de las cinco activas. */
function cargas (skills) {
  let ult = 0, stk = 0;
  skills.forEach(sk => { if (sk.ult) ult += sk.ult; if (sk.stk) stk += sk.stk; });
  return { ult: Math.round(ult * 10) / 10, stk: Math.round(stk * 10) / 10 };
}
/** Suma del % de ataque de todas las etapas de las skills activas. */
function danoTotal (skills) {
  let n = 0;
  skills.forEach(sk => { if (!/^Active/.test(sk.sl)) return;
    (sk.st || []).forEach(st => (st.fx || []).forEach(f => { const d = dano(f); if (d) n += d.pct; })); });
  return Math.round(n);
}
/** Índices de etiqueta de efecto presentes en un set de skills (para filtrar). */
function efectosDe (skills) {
  const out = new Set();
  skills.forEach(sk => (sk.st || []).forEach(st => (st.fx || []).forEach(f => out.add(f.a))));
  return out;
}
function allVariants () {
  const out = [];
  CHARS.forEach(ch => { out.push(variant(ch.id, null)); ch.uniforms.forEach(u => out.push(variant(ch.id, u.id))); });
  return out;
}
function fullLabel (v) { return v.uid ? v.name + ' — ' + v.sub : v.name; }

// FUENTE DE UN LIDERAZGO. Los de MFF_SOPORTES son de Leads & Supports, salvo los que el build completa con la
// Leader Skill de la API de skills cuando Leads & Supports no los publica (src: 'api'). Donde la app muestra un
// liderazgo, dice cuáles no son de Leads & Supports: «según la skill del juego». Si la API no dice qué otorga el
// «Give Power» de la Leader Skill y lo dice el juego, el slot trae esa fuente (otorga: scripts/liderazgos.py).
/** ¿Sale de la Leader Skill de la API (src 'api') y no de Leads & Supports? */
function esDeApi (x) { return x.src === 'api'; }
/** « (según la skill del juego)» para un liderazgo que no es de Leads & Supports, o nada. */
function srcTxt (x) { return esDeApi(x) ? ' (' + t('sp_src_api') + ')' : ''; }
/** Lo mismo, como etiqueta, con la explicación en el title. */
function srcHtml (x) {
  return esDeApi(x) ? ` <span class="tag dim srcapi" title="${h(t(x.otorga ? 'sp_src_otorga_t' : 'sp_src_api_t'))}">${h(t('sp_src_api'))}</span>` : '';
}
/** Las fuentes de unos liderazgos y soportes: Leads & Supports y, si alguno sale de la API, sus skills, más las de lo
 *  que otorga un «Give Power» según el juego. */
function fuentesSop (xs) {
  const base = xs.some(esDeApi) ? (xs.every(esDeApi) ? ['tv-pj'] : ['tv-sup', 'tv-pj']) : ['tv-sup'];
  return [...new Set([...base, ...xs.flatMap(x => x.otorga || [])])];
}
/** ¿Un efecto de líder o de soporte (MFF_SOPORTES) alcanza a la variante b? */
function aplicaA (x, b) {
  if (!x.r) return true;
  const [cat, val] = x.r;
  switch (cat) {
    case 'Ability':   return (b.ab || []).includes(val);
    case 'Type':      return b.c === val;
    case 'Allies':    return b.race === val;
    case 'Side':      return b.f === val;
    case 'Character': return b.name === val;
  }
  throw new Error('restricción de soporte desconocida: ' + cat);
}
// Para quién sirve cada efecto de líder, de soporte y de bono de equipo: la regla de su stat en el catálogo
// (MFF_CATALOGO.soporte; scripts/contenido/catalogo.json), la misma que muestran el Glosario y el «Cómo
// funciona». Mira el perfil de combate de quien lo recibe (perfilDano): con qué ataque escala (escala:), qué
// elementos (elemento:) y qué tipos de daño (tipo:) tienen sus skills activas, y qué resistencias le suben el
// daño (resistencia:), con «*» para cualquiera; «todos» le sirve a cualquiera y «nadie», a ninguno. Un stat que
// el catálogo no tiene (thanosvibs sumó uno nuevo, o la wiki escribe un stat de bono que no conoce) cuenta para
// todos y la sinergia lo dice. PIDE lo arma iniciarDatos(): por stat que pide algo, [qué mira del perfil, qué
// valor pide (null: cualquiera)], o ['nadie', null].
const MIRA = { escala: 'src', elemento: 'elem', tipo: 'tipo', resistencia: 'res' };
let PIDE;
/** [qué mira, qué valor] de una regla del catálogo para un stat; null si le sirve a cualquiera. Una regla que la
 *  app no sabe evaluar (de las que miran las skills, como aplica_debuffs) corta: el build no la deja pasar. */
function reglaStat (stat, r) {
  if (r === 'todos') return null;
  if (r === 'nadie') return ['nadie', null];
  const i = r.indexOf(':'), mira = MIRA[r.slice(0, i)];
  if (i < 0 || !mira) throw new Error(`regla de «le sirve» que la app no sabe evaluar en ${stat}: ${r}`);
  const valor = r.slice(i + 1);
  return [mira, valor === '*' ? null : valor];
}
/** Perfil de combate de un retrato, calculado en el build (scripts/modelo.py): de qué ataque
 *  sale su daño (esc), de qué tipo es (tip), qué elementos lleva (ele) y qué resistencias le
 *  suben el daño (res). Un personaje agregado a mano no tiene skills ni perfil: no pega con nada
 *  conocido y ningún efecto que pida algo le sirve. */
const SIN_PERFIL = { esc: [], tip: [], ele: [], res: [] };
function perfilDe (v) { return PERFIL[v.p] || SIN_PERFIL; }
/** El perfil en conjuntos, para preguntarle millones de veces en la consulta de combinaciones. */
const _PERFIL = new Map();
function perfilDano (v) {
  let pf = _PERFIL.get(v.p);
  if (pf) return pf;
  const m = perfilDe(v);
  pf = { src: new Set(m.esc.map(e => e[0])), tipo: new Set(m.tip), elem: new Set(m.ele), res: new Set(m.res) };
  if (v.p) _PERFIL.set(v.p, pf);
  return pf;
}
/** ¿Le sirve a b este efecto (una línea de un soporte, un liderazgo o un bono de equipo)? */
function sirve (f, b) {
  const q = PIDE[f.s];
  if (!q) return true;
  if (q[0] === 'nadie') return false;
  const de = perfilDano(b)[q[0]];
  return q[1] ? de.has(q[1]) : de.size > 0;
}
/** ¿Le sirve a b algo de este soporte o liderazgo? (Que le llegue lo dice aplicaA.) La mayoría
 *  no pide nada: se anota cuáles piden, porque la consulta de combinaciones pregunta esto
 *  millones de veces. */
const _PIDE_ALGO = new WeakMap();
function leSirve (x, b) {
  let pide = _PIDE_ALGO.get(x);
  if (pide === undefined) { pide = x.fx.some(f => PIDE[f.s]); _PIDE_ALGO.set(x, pide); }
  if (!pide) return true;
  for (const f of x.fx) if (sirve(f, b)) return true;
  return false;
}
// ÍNDICE PARA ARMAR EQUIPOS: lo que da cada liderazgo y cada soporte, en las categorías con
// las que se arman los equipos (las pidió el usuario), con los stats de thanosvibs que entran
// en cada una; a quién le sirve cada stat lo dice su regla en el catálogo (sirve()). Se ven en la
// ficha, filtran el roster y dicen en cada combinación de 3 qué le dan al personaje sus
// compañeros. No cambian los puntos de la sinergia.
const CATEGORIAS = [
  { k: 'fis',      s: ['Physical Attack'], ataque: true },
  { k: 'ene',      s: ['Energy Attack'], ataque: true },
  { k: 'atk',      s: ['All Basic Attacks', 'All Basic Attacks (Stackable)'], ataque: true },
  { k: 'fuego',    s: ['Fire Damage', 'Fire Damage by % Fire Resist'], ataque: true },
  { k: 'hielo',    s: ['Cold Damage'], ataque: true },
  { k: 'rayo',     s: ['Lightning Damage'], ataque: true },
  { k: 'veneno',   s: ['Poison Damage'], ataque: true },
  { k: 'mente',    s: ['Mind Damage'], ataque: true },
  { k: 'elems',    s: ['All Element Damage'], ataque: true },
  { k: 'evasion',  s: ['Ignore Dodge'] },
  { k: 'defensas', s: ['All Basic Defenses', 'Super Armor, All Basic Defenses'] },
  { k: 'vida',     s: ['HP'] },
  { k: 'mermas',   s: [] },                           // los de anti-mermas de la tabla de valor (iniciarDatos)
];
const CAT = Object.fromEntries(CATEGORIAS.map(c => [c.k, c]));
const CAT_DE = {};                    // stat de thanosvibs -> categoría
for (const c of CATEGORIAS) for (const s of c.s) CAT_DE[s] = c.k;
/** Categorías de un liderazgo o un soporte, en el orden de CATEGORIAS; con b, solo las de
 *  los efectos que le sirven a b (que le llegue lo dice aplicaA). */
function categoriasDe (x, b) {
  const ks = new Set();
  for (const f of x.fx) { const k = CAT_DE[f.s]; if (k && (!b || sirve(f, b))) ks.add(k); }
  return CATEGORIAS.filter(c => ks.has(c.k)).map(c => c.k);
}
/** Las categorías que le sirven a b: las de ataque según con qué pega, y las demás. */
function categoriasQueSirven (b) {
  return CATEGORIAS.filter(c => c.s.some(s => sirve({ s }, b))).map(c => c.k);
}
/** ¿Este liderazgo o soporte pasa el filtro del índice? Con restr ('Tipo|valor'), solo si es
 *  para esa restricción; con para (una variante), solo lo que le llega y le sirve; con
 *  categorías, alguno de sus efectos tiene que ser de una de ellas. */
function slotPasa (x, cats, para, restr) {
  if (restr && (!x.r || x.r.join('|') !== restr)) return false;
  if (para && !aplicaA(x, para)) return false;
  if (!cats.length) return !para || leSirve(x, para);
  return x.fx.some(f => cats.includes(CAT_DE[f.s]) && (!para || sirve(f, para)));
}
/** Lo que el filtro del índice encontró en v, para mostrarlo en el roster:
 *  { lid: [categorías], sop: [categorías] }, o null si v no pasa. */
function indiceDe (v, F, para, restr) {
  if (para && v.cid === para.cid) return null;
  const s = SOPORTES[v.p]; if (!s) return null;
  const da = (ks, cats) => {
    const out = new Set(); let pasa = false;
    for (const k of ks) {
      const x = s[k]; if (!x || !slotPasa(x, cats, para, restr)) continue;
      pasa = true;
      for (const c of categoriasDe(x, para)) if (!cats.length || cats.includes(c)) out.add(c);
    }
    return pasa ? CATEGORIAS.filter(c => out.has(c.k)).map(c => c.k) : null;
  };
  if (!F.lid.length && !F.sop.length) {
    const lid = da(LIDERAZGOS, []), sop = da(SLOTS_SOPORTE, []);
    return lid || sop ? { lid: lid || [], sop: sop || [] } : null;
  }
  const lid = F.lid.length ? da(LIDERAZGOS, F.lid) : [], sop = F.sop.length ? da(SLOTS_SOPORTE, F.sop) : [];
  return lid && sop ? { lid, sop } : null;
}
/** Lo que recibe el foco en el equipo: los soportes de los otros integrantes y el liderazgo
 *  del líder elegido (también si el líder es él: el liderazgo es para todo el equipo); lo
 *  que le llega y le sirve, por categoría. { categoría: true, o false si solo llega con un
 *  artefacto }. Es la suma de lo que le da cada integrante (aporte). */
function cobertura (foco, vs, lider) {
  const out = {};
  for (const a of vs) for (const [c, sinArtefacto] of Object.entries(aporte(foco, a, a === lider))) out[c] = out[c] || sinArtefacto;
  return out;
}
/** Lo que le da al foco un integrante del equipo, por categoría (lo que le llega según recibe());
 *  como cobertura(). */
function aporte (foco, a, esLider) {
  const out = {};
  for (const { k, fx } of recibe(foco, a, esLider)) for (const f of fx) {
    const c = CAT_DE[f.s];
    if (c) out[c] = out[c] || k !== 'artifact';
  }
  return out;
}
/** Lo que le llega a `destino` de un integrante `a` del equipo y le sirve: los soportes de `a` (también
 *  los suyos, si `a` es `destino`: el soporte propio cuenta para su dueño, Ezequiel, 4 de octubre de 2026),
 *  si `a` es el líder su liderazgo (también si `a` es `destino`: el liderazgo es para todo el equipo) y, si
 *  `a` es `destino`, sus anti-mermas propios que cuentan (los de sus skills, recibePropio()). [{ de: a, k, x,
 *  fx: [los efectos que le sirven] }], en el orden en que se aplican (ver «Efectos iguales que no se suman»): de él
 *  mismo, los de sus skills, sus soportes y su liderazgo; de otro, su liderazgo y sus soportes. De acá salen la
 *  cobertura de la tarjeta y su «Por qué» (lo que recibe y aporta cada integrante, en la ventana). En la
 *  sinergia, en cambio, un soporte cuenta solo si le llega a otro integrante (synergy). */
function recibe (destino, a, esLider) {
  const propio = a === destino, out = propio ? recibePropio(a) : [], s = SOPORTES[a.p];
  if (s) for (const k of propio ? (esLider ? SLOTS_SOPORTE.concat(LIDERAZGOS) : SLOTS_SOPORTE) : (esLider ? LIDERAZGOS.concat(SLOTS_SOPORTE) : SLOTS_SOPORTE)) {
    const x = s[k];
    if (!x || !aplicaA(x, destino)) continue;
    const fx = x.fx.filter(f => sirve(f, destino));
    if (fx.length) out.push({ de: a, k, x, fx });
  }
  return out;
}
// ANTI-MERMAS PROPIOS (Ezequiel, 4 de octubre de 2026). Lo que las skills de un personaje le dan a él mismo
// cuenta como anti-mermas para su dueño (Knull: su pasiva de Tier-2, al recibir un debuff), aunque Leads &
// Supports no lo publique, porque no es para el equipo. Uno que se activa con una probabilidad (Hulkling: 25% al
// recibir un golpe) no cubre: se muestra con su probabilidad y se dice que no cuenta. Salen del análisis
// (MFF_ANALISIS): los efectos de los stats de anti-mermas de la tabla de valor, según el catálogo, que van a él
// (destino «e»), de sus pasivas (no de las activas ni de la Striker).
/** Efecto del catálogo (índice) -> el stat de anti-mermas que le corresponde. Lo arma iniciarDatos(). */
let STAT_ANTI;
const _ANTI_PROPIO = new Map();
/** Los anti-mermas propios de v: { cuenta: [...], prob: [...] }, cada uno { sk, st, s, p }: la skill, la etapa,
 *  el stat de anti-mermas y la probabilidad de su activación (null si no tiene; solo en prob). Uno por etapa. */
function antiPropio (v) {
  let r = _ANTI_PROPIO.get(v.p);
  if (r) return r;
  r = { cuenta: [], prob: [] };
  const an = ANALISIS[v.p], vistas = new Set();
  if (an) for (const [ie, d, , fuentes] of an.fx) {
    if (d !== 'e' || !STAT_ANTI.has(ie)) continue;
    for (const [si, ti] of fuentes) {
      const sk = v.skills[si];
      if (/^Active/.test(sk.sl) || sk.sl === 'Striker Skill' || vistas.has(si + '|' + ti)) continue;
      vistas.add(si + '|' + ti);
      const st = sk.st[ti], p = probabilidad(st);
      (p == null ? r.cuenta : r.prob).push({ sk, st, s: STAT_ANTI.get(ie), p });
    }
  }
  if (v.p) _ANTI_PROPIO.set(v.p, r);
  return r;
}
/** La probabilidad de la activación de una etapa («25% al recibir un golpe»: 25), o null si no tiene (o es 100%). */
function probabilidad (st) {
  const a = st.ac != null ? fila('act', st.ac) : null;
  if (!a || !/^\{?#\}?%/.test(a.en)) return null;
  const p = (st.av || [])[0];
  if (typeof p !== 'number') throw new Error('activación con probabilidad sin el número: ' + a.en);
  return p >= 100 ? null : p;
}
/** La activación de una etapa, en el idioma activo («al recibir un debuff»), o «sin condición». */
function activacionTxt (st) { return st.ac != null ? txt('act', st.ac, st.av) : t('tt_sin_cond'); }
/** Los anti-mermas propios de v que cuentan, como lo de recibe(): { de: v, k: 'propio', x, fx }, con la skill
 *  (x.sk), su activación (x.ac, ya en el idioma activo) y su entrada de antiPropio (x.ap). */
function recibePropio (v) {
  return antiPropio(v).cuenta.map(ap => {
    const { sk, st, s } = ap, x = { sk, ac: st.ac != null ? txt('act', st.ac, st.av) : null, fx: [{ s }], ap };
    return { de: v, k: 'propio', x, fx: x.fx };
  });
}
// EFECTOS IGUALES (Ezequiel, 5 de octubre de 2026: «El juego no permite el solapado de habilidades iguales... el antimermas
// de apocalipsis y el de deadpool solo va a funcionar uno»; y después: «el daño contra facciones si se suma. EL ataque se
// suma. La defensa se suma. la vida se suma... Las habilidades especificas, inmunidad a romper guardia, por ejemplo no se
// solapan es decir cuenta una sola vez»). Si se suma lo dice el catálogo, en cada stat (MFF_CATALOGO.soporte, acumula): las
// estadísticas se suman; las habilidades (anti-mermas, inmunidades, barrera, escudos, revivir, invocar...) cuentan una vez.
// Una habilidad que a un integrante le llega de dos o más fuentes se le aplica una sola vez: la de mayor valor y, a igual
// valor, la primera en este orden: lo propio (sus anti-mermas de las skills y lo de sus soportes que le llega), el liderazgo
// del líder y los soportes de los demás en el orden del equipo (el líder primero y los otros en un orden fijo, su clave: el
// mismo desde la lista de cualquiera). Las demás fuentes no le suman nada a ese integrante: un soporte o un liderazgo suma
// en la sinergia, y un soporte en PvP y PvE, solo si a algún otro integrante le llega algo que se le aplica y le sirve, y
// las pantallas muestran atenuada la fuente que no se aplica, con la que sí. iniciarDatos confirma lo que esto supone de
// los datos (que las líneas de un mismo stat se puedan comparar, entre otras cosas).
/** ¿Se suma el efecto f (una línea de un liderazgo, un soporte o un bono de equipo) cuando a un integrante le llega de más
 *  de una fuente? Lo dice el catálogo; un stat que el catálogo no tiene se suma, y la tabla de lo que recibe lo marca sin
 *  clasificar. */
function seAcumula (f) { const c = CATALOGO.soporte[f.s]; return !c || c.acumula; }
const _NO_ACUM = new WeakMap();
/** ¿Trae x (un liderazgo o un soporte) algún efecto que no se acumula? Pocos: se anota, porque la consulta de
 *  combinaciones lo pregunta millones de veces. */
function traeNoAcumulable (x) {
  let r = _NO_ACUM.get(x);
  if (r === undefined) { r = x.fx.some(f => !seAcumula(f)); _NO_ACUM.set(x, r); }
  return r;
}
/** El valor de la línea x en el stat s, para elegir la mayor entre las que no se acumulan: su número (el mayor, si lo trae
 *  dos veces) o null si no trae (iniciarDatos confirma que las de un mismo stat traen todas número o ninguna). */
function valorEn (x, s) {
  let v = null;
  for (const f of x.fx) if (f.s === s && typeof f.v === 'number' && (v === null || f.v > v)) v = f.v;
  return v;
}
/** Lo que trae v que no se acumula, por stat, cada uno en el orden en que se aplica: propio, lo de él (sus anti-mermas de
 *  las skills, con su entrada de antiPropio de x, y después sus soportes que le llegan); lid, sus liderazgos; sop, sus
 *  soportes. Cada uno, { k, x, val: valorEn }. No depende del equipo: se guarda por retrato (variant() arma otra variante
 *  cada vez). */
const _NO_ACUM_DE = new Map();
function noAcumulablesDe (v) {
  let r = _NO_ACUM_DE.get(v.p);
  if (r) return r;
  r = { propio: new Map(), lid: new Map(), sop: new Map() };
  const pon = (m, s, e) => { const l = m.get(s); if (l) l.push(e); else m.set(s, [e]); };
  for (const ap of antiPropio(v).cuenta) pon(r.propio, ap.s, { k: 'propio', x: ap, val: null });
  const so = SOPORTES[v.p];
  if (so) for (const [k] of TIPOS_SOPORTE) {
    const x = so[k];
    if (!x || !traeNoAcumulable(x)) continue;
    const lid = LIDERAZGOS.includes(k), propio = !lid && aplicaA(x, v);
    for (const s of new Set(x.fx.filter(f => !seAcumula(f)).map(f => f.s))) {
      const e = { k, x, val: valorEn(x, s) };
      pon(lid ? r.lid : r.sop, s, e);
      if (propio) pon(r.propio, s, e);
    }
  }
  if (v.p) _NO_ACUM_DE.set(v.p, r);
  return r;
}
/** El equipo en el orden en que se aplican sus soportes: el líder primero y los demás por su clave. */
function ordenEquipo (vs, lider) {
  const otros = vs.filter(x => x !== lider).sort((a, b) => a.key < b.key ? -1 : a.key > b.key ? 1 : 0);
  return lider ? [lider].concat(otros) : otros;
}
/** La fuente cuya línea del stat s, uno que no se acumula, se le aplica a m en el equipo vs con ese líder: de las que le
 *  llegan, la de mayor valor y, a igual valor (o sin valor), la primera en el orden: lo propio, el liderazgo del líder y los
 *  soportes de los demás en ordenEquipo. { de, k, x, val, r }, o null si no le llega de nadie. Sin armar ordenEquipo, porque
 *  se pregunta millones de veces: r es su lugar en ese orden (0 lo propio, 1 el liderazgo del líder, 2 sus soportes, 3 los
 *  de los demás, y entre dos de los demás, el de clave menor); entre las líneas de uno mismo, la primera. */
function fuenteQueSeAplica (m, s, vs, lider) {
  let p = null;
  const toma = (de, e, r) => {
    if (p && !(e.val !== null && p.val !== null && e.val !== p.val ? e.val > p.val : r < p.r || (r === p.r && de !== p.de && de.key < p.de.key))) return;
    p = { de, k: e.k, x: e.x, val: e.val, r };
  };
  const propio = noAcumulablesDe(m).propio.get(s);
  if (propio) for (const e of propio) toma(m, e, 0);
  if (lider) { const ls = noAcumulablesDe(lider).lid.get(s); if (ls) for (const e of ls) if (aplicaA(e.x, m)) toma(lider, e, 1); }
  for (const a of vs) {
    if (a === m) continue;
    const ss = noAcumulablesDe(a).sop.get(s);
    if (ss) for (const e of ss) if (aplicaA(e.x, m)) toma(a, e, a === lider ? 2 : 3);
  }
  return p;
}
/** La fuente de la que le llegan primero a m los anti-mermas (cualquiera de sus stats), en el mismo orden: la que lo
 *  cubre. Los anti-mermas no traen valor (iniciarDatos lo confirma), así que entre dos decide el orden, como en
 *  fuenteQueSeAplica. null si no le llegan. */
function primeraAnti (m, vs, lider) {
  const ap = antiPropio(m).cuenta[0];
  if (ap) return { de: m, k: 'propio', x: ap };
  const da = (a, ks) => {
    const so = SOPORTES[a.p];
    if (so) for (const k of ks) { const x = so[k]; if (x && aplicaA(x, m) && x.fx.some(f => ANTI_MERMAS.has(f.s))) return { de: a, k, x }; }
    return null;
  };
  let r = da(m, SLOTS_SOPORTE) || (lider && da(lider, LIDERAZGOS));
  if (r) return r;
  for (const a of ordenEquipo(vs, lider)) if (a !== m && (r = da(a, SLOTS_SOPORTE))) return r;
  return null;
}
/** ¿Es la fuente p la línea (de, k, x) de recibe()? La de las skills trae su entrada de antiPropio en x.ap. Cada integrante,
 *  por su clave: variant() arma otra variante cada vez. */
function esLaFuente (p, de, k, x) { return p.de.key === de.key && p.k === k && p.x === (k === 'propio' ? x.ap : x); }
/** De los efectos fx (los que le sirven) que le llegan a m de la línea (de, k, x): los que se le aplican (si) y los que no
 *  se suman porque ya los tiene de otra fuente (no: [[efecto, esa fuente]]). */
function aplicacion (m, de, k, x, fx, vs, lider) {
  const si = [], no = [];
  for (const f of fx) {
    if (seAcumula(f)) { si.push(f); continue; }
    const p = fuenteQueSeAplica(m, f.s, vs, lider);
    if (esLaFuente(p, de, k, x)) si.push(f); else no.push([f, p]);
  }
  return { si, no };
}
/** ¿Le llega a b algo de x (el slot k de de) que se le aplica y le sirve? */
function aplicaAlgo (b, de, k, x, vs, lider) {
  if (!aplicaA(x, b) || !leSirve(x, b)) return false;
  if (!traeNoAcumulable(x)) return true;
  for (const f of x.fx) if (sirve(f, b) && (seAcumula(f) || esLaFuente(fuenteQueSeAplica(b, f.s, vs, lider), de, k, x))) return true;
  return false;
}
/** A quiénes del equipo (menos de) les llega x y les sirve: { si: a los que se les aplica algo, no: [[integrante, [[efecto,
 *  la fuente que ya se lo da]]]] los que reciben algo que ya tienen }, o null si no le llega ni le sirve a nadie más.
 *  conNo: también lo que no se suma (para mostrarlo; la consulta de combinaciones no lo pide). */
function reparto (de, k, x, vs, lider, conNo) {
  let si = null, no = null;
  for (const b of vs) {
    if (b === de || !aplicaA(x, b) || !leSirve(x, b)) continue;
    if (!traeNoAcumulable(x)) { (si || (si = [])).push(b); continue; }
    if (!conNo) { if (aplicaAlgo(b, de, k, x, vs, lider)) (si || (si = [])).push(b); continue; }
    const ap = aplicacion(b, de, k, x, x.fx.filter(f => sirve(f, b)), vs, lider);
    if (ap.si.length) (si || (si = [])).push(b);
    if (ap.no.length) (no || (no = [])).push([b, ap.no]);
  }
  return si || no ? { si: si || [], no: no || [] } : null;
}
/** De quién ya tiene m un efecto (p, de fuenteQueSeAplica): «propio (Pasiva T2)», «de su liderazgo», «del liderazgo de
 *  Thanos» o «de Wasp (Pasiva 4★)». nombre: cómo se nombra a cada integrante; con html, el nombre va con su title y el
 *  resto escapado. */
function yaDe (m, p, nombre, html) {
  const slot = p.k === 'propio' ? slotEs(p.x.sk.sl) : t(CLAVE_SOPORTE[p.k]), esc = html ? h : (s) => s;
  if (p.de.key === m.key) return esc(t(LIDERAZGOS.includes(p.k) ? 'ya_su_lid' : 'ya_propio').replace('{s}', slot));
  return esc(t(LIDERAZGOS.includes(p.k) ? 'ya_lid' : 'ya_sop').replace('{s}', slot)).replace('{x}', () => html ? nombreHtml(p.de, nombre) : nombre(p.de));
}
/** Las fuentes distintas de unos efectos que no se suman ([[efecto, fuente]]), en su orden. */
function fuentesDistintas (fs) {
  const m = new Map();
  for (const [, p] of fs) { const c = p.de.key + '|' + p.k + (p.k === 'propio' ? '|' + p.x.sk.sl : ''); if (!m.has(c)) m.set(c, p); }
  return [...m.values()];
}
/** «(no se suma: ya lo tiene de su liderazgo)», atenuado: lo que le llega a m de una fuente y ya tiene de otra (p). */
function noSumaHtml (m, p, nombre) { return `<span class="muted pqrep">(${h(t('rep_no_suma')).replace('{de}', () => yaDe(m, p, nombre, true))})</span>`; }
/** « (Deadpool ya lo tiene de su liderazgo)», atenuado: los integrantes a los que les llega algo de una fuente que no se les
 *  suma (no: [[integrante, [[efecto, fuente]]]]), con de quién ya lo tienen. Vacío si no hay. */
function yaLoTienenHtml (no, nombre) {
  if (!no.length) return '';
  const y = LANG === 'es' ? ' y ' : ' and ';
  return ` <span class="muted pqrep">(${no.map(([b, fs]) => h(t('rep_quien')).replace('{y}', () => nombreHtml(b, nombre))
    .replace('{de}', () => fuentesDistintas(fs).map(p => yaDe(b, p, nombre, true)).join(y))).join('; ')})</span>`;
}
/** Los anti-mermas propios de los integrantes que no cuentan, por tener probabilidad: un renglón por cada uno. */
function antiProbHtml (vs, nombre) {
  return vs.flatMap(m => antiPropio(m).prob.map(x => h(t('cx_prob')).replace('{x}', () => nombreHtml(m, nombre))
    .replace('{s}', () => h(slotEs(x.sk.sl))).replace('{a}', () => h(activacionTxt(x.st)))));
}
/** Personajes a los que alcanza una restricción, con las variantes que la cumplen: cuenta
 *  el uniforme puesto, que puede cambiar la clase, el bando, la raza y las habilidades. */
function alcanzados (r) {
  return CHARS.map(ch => {
    const vs = [variant(ch.id, null)].concat(ch.uniforms.map(u => variant(ch.id, u.id)));
    const si = vs.filter(v => aplicaA({ r }, v));
    return si.length ? { vs, si } : null;
  }).filter(Boolean).sort((a, b) => a.vs[0].name.localeCompare(b.vs[0].name));
}
/** Ventana con los personajes que cumplen un objetivo de grupo. Uno por personaje con su
 *  retrato base, salvo que la base no lo cumpla: ahí va cada uniforme que sí. */
function aliadosModal () {
  const i = ui.aliados, r = grupoDe(i), grupos = alcanzados(r);
  const tile = (v, nota) => `<button class="altile" data-a="open" data-cid="${v.cid}" data-uid="${v.uid || ''}"
      title="${h(v.name + (nota ? ' — ' + nota : ''))}">
      <span class="shot">${shot(v.id)}</span><span class="alnm">${h(v.name)}</span>
      ${nota ? `<span class="alnota">${h(nota)}</span>` : ''}</button>`;
  const tiles = grupos.flatMap(g => {
    const base = g.si.find(v => !v.uid);
    if (!base) return g.si.map(v => tile(v, t('al_only_with') + ' ' + v.sub));
    const fuera = g.vs.filter(v => !g.si.includes(v));
    return [tile(base, fuera.length ? t('al_except_with') + ' ' + fuera.map(v => v.sub).join(', ') : '')];
  });
  const porUniforme = grupos.some(g => g.si.length !== g.vs.length);
  return `<div class="backdrop" data-a="aliadosCerrar"><div class="modal ancho" data-a="aliadosModal">
    <div class="row alcab">
      <div><div class="altitulo">${h(txt('tgt', i))}</div>
        <div>${restrHtml({ r })} <span class="muted">· ${h(t('al_count').replace('{n}', grupos.length))}</span></div></div>
      <button class="btn sm" data-a="aliadosCerrar">${h(t('al_close'))}</button>
    </div>
    ${porUniforme ? `<p class="muted" style="margin-bottom:10px">${h(t('al_by_uniform'))}</p>` : ''}
    ${tiles.length ? `<div class="algrid">${tiles.join('')}</div>` : `<p class="muted">${h(t('al_none'))}</p>`}
  </div></div>`;
}
// ---------------------------------------------------------------------------
// UN EFECTO DE LIDERAZGO, SOPORTE O BONO DE EQUIPO
// Una sola forma de escribirlo, la misma en todas las pantallas (Resumen, «Cómo funciona», comparativa,
// bonos de equipo, detalle de PvP y PvE y «Por qué»): el stat, el valor con la parte del instinto y, entre
// paréntesis, cuándo llega (la activación y su recarga, lo que pide, la condición del efecto, cuánto dura y
// hasta dónde acumula). Los números van en el idioma de la app: +5,2% y −40% en español, +5.2% y −40% en
// inglés.
// ---------------------------------------------------------------------------
/** Un número en el idioma de la app, con hasta dos decimales: 0,7 (es), 0.7 (en). */
function numTxt (n) { return (Math.round(n * 100) / 100).toLocaleString(LANG === 'es' ? 'es-AR' : 'en-US', { maximumFractionDigits: 2 }); }
/** Un porcentaje con su signo: +65%, −40%. */
function pctTxt (n) { const r = Math.round(n * 100) / 100; return (r > 0 ? '+' : r < 0 ? '−' : '') + numTxt(Math.abs(r)) + '%'; }
/** El valor de un efecto: «+20% +0,4% del instinto total», «1 golpe», o vacío si no tiene número. */
function valorTxt (v, i) {
  const out = [];
  if (typeof v === 'string') out.push(trTxt(v)); else if (v != null) out.push(pctTxt(v));
  if (i != null) out.push(pctTxt(i) + ' ' + t('sp_inst'));
  return out.join(' ');
}
/** Cuándo llega el efecto f de x (vacío si llega siempre): la activación del liderazgo o del soporte y su
 *  recarga, lo que pide (Tier-2), la condición del efecto («con 2 personajes de Combate»), cuánto dura y, si
 *  acumula, hasta dónde. */
function condicionTxt (x, f) {
  const p = [];
  if (x.ac) p.push(minuscula(trTxt(x.ac)));
  if (x.cd) p.push(t('sp_cd') + ' ' + numTxt(x.cd) + ' s');
  if (x.req) p.push(minuscula(t('sp_req')) + ' ' + trTxt(x.req));
  if (f.c) p.push(trTxt(f.c));
  const d = f.d != null ? f.d : x.d;
  if (d != null) p.push(t('an_dura') + ' ' + numTxt(d) + ' s');
  if (f.tope != null) p.push(t('sp_cap') + ' ' + numTxt(f.tope) + '%');
  return p.join(', ');
}
/** El efecto f de x (un liderazgo o un soporte de MFF_SOPORTES, o una versión de un bono de equipo), en
 *  partes: { s: el stat de thanosvibs, val: valorTxt, cond: condicionTxt }. El texto y el HTML salen de acá. */
function efectoSoporte (x, f) { return { s: f.s, val: valorTxt(f.v, f.i), cond: condicionTxt(x, f) }; }
/** En texto: «Quita todos los debuffs (al recibir un debuff, recarga 20 s, dura 12 s)». */
function efectoSoporteTxt (x, f) {
  const e = efectoSoporte(x, f);
  return trTxt(e.s) + (e.val ? ' ' + e.val : '') + (e.cond ? ` (${e.cond})` : '') + (sinClasificar(e.s) ? ` (${t('sy_unclassified')})` : '');
}
/** Un renglón de efecto en HTML, con el mismo texto que efectoSoporteTxt: el stat, el valor en negrita, lo
 *  que va pegado al valor (extra: el «*» de la suma del «Por qué») y, atenuada, la condición. */
function renglonHtml (s, val, cond, extra) {
  return `${trHtml(s)}${val ? ` <b>${h(val)}</b>` : ''}${extra || ''}${cond ? ` <span class="muted">(${h(cond)})</span>` : ''}${
    sinClasificar(s) ? ` <span class="muted">(${h(t('sy_unclassified'))})</span>` : ''}`;
}
function efectoSoporteHtml (x, f) { const e = efectoSoporte(x, f); return renglonHtml(e.s, e.val, e.cond); }
const LIDERAZGOS = ['leader', 'leader2'];
const ROLES_EQUIPO = ['Tanque', 'Control', 'Daño', 'Soporte'];
/** Bonos de equipo de cada personaje (MFF_BONOS), por id. Cada versión de sus stats (más de una
 *  si las páginas de la wiki empatan) tiene la forma de un efecto de soporte ({ fx: [{ s, v }] }),
 *  para que la sinergia les aplique sirve() y efectoSoporteTxt(). Lo arma iniciarDatos(). */
let BONOS_DE;
/** De quiénes es striker cada personaje: { cid: [[cid del personaje, %, 'ataca'|'atacado'], ...] }, al
 *  revés de STRIKERS. Lo arma iniciarDatos(). */
let STRIKERS_DE;
/** Por efecto del catálogo (id): el efecto, los términos del glosario del juego que le corresponden,
 *  las etiquetas de skills que apuntan a él (índices en MFF_TABLAS.ab, solo las que traen los
 *  datos) y los stats de liderazgo, soporte y bono de equipo que apuntan a él (MFF_CATALOGO.soporte).
 *  Lo arma iniciarDatos(). */
let GL_DE;
/** ¿Están en el equipo todos estos personajes? */
function estanTodos (cids, vs) {
  for (const c of cids) {
    let esta = false;
    for (const x of vs) if (x.cid === c) { esta = true; break; }
    if (!esta) return false;
  }
  return true;
}
/** Ventaja de tipo (SEED.VENTAJA_TIPO): a qué clases le gana cada una, 'normal' o 'menor'
 *  (la de Universal sobre las otras tres). LE_GANA_A: la amenaza de cada clase, la que le gana
 *  con ventaja normal; Universal no tiene. Las arma iniciarDatos(). */
let VENTAJA, LE_GANA_A;
/** Sinergia de un grupo de variantes. Lo que puntúa más son los efectos de líder y de
 *  soporte de thanosvibs que alcanzan a otro integrante, se le aplican (una habilidad, una sola
 *  vez: ver «Efectos iguales») y le sirven (sirve()): los de soporte
 *  valen en cualquier lugar del equipo; el liderazgo, el del líder del equipo (liderDe: el
 *  mismo sea cual sea el orden y desde la lista de quien se mire; lider, si se pasa, es el de
 *  un contexto). Cada bono de equipo con todos sus integrantes en el equipo
 *  suma 1 (de la wiki, o del juego si se cargó). Se suman dos lecturas propias, dichas como tales:
 *  los roles derivados de las skills y la ventaja de tipo (Combate > Velocidad > Detonación >
 *  Combate; Universal le gana a las tres con ventaja menor y no tiene debilidad). No es un
 *  cálculo del juego.
 *  foco: cuenta solo lo que involucra a ese integrante (los equipos armados para él).
 *  Escrita con bucles y sin armar textos si no hacen falta: la consulta de combinaciones la
 *  llama cientos de miles de veces. */
function synergy (vs, { soloPuntaje = false, foco = null, lider } = {}) {
  if (vs.length < 2) return { score: 0, razones: [], aplicados: [], lider: null, art: false };
  // razones: lo que suma, para explicarlo (sin soloPuntaje): cada soporte o liderazgo con los
  // integrantes a los que se les aplica algo que les sirve (a) y a los que solo les llega lo que ya
  // tienen (no: [[integrante, [[efecto, la fuente que ya se lo da]]]]; si no se le aplica a nadie, va
  // con 0), cada versión de un bono de equipo, los roles, las clases y cada ventaja de clase, cada una
  // con lo que suma (pts; el punto de un bono va con su primera versión). Los textos salen de ahí
  // (razonesTxt y el «Por qué»).
  // aplicados: { de, a: [integrantes] }, los soportes y bonos de equipo que suman: quién le da algo a
  // quién (en un bono de equipo, cada integrante a los otros, que están juntos por el bono). El
  // liderazgo no va: vincula según quién lidera (vinculoLider), y el líder depende del contexto.
  // art: algún soporte de artefacto sumó (cuenta como si lo llevara; los puntos lo marcan con «*»).
  const razones = [], aplicados = []; let score = 0, art = false;
  // El líder del equipo (liderDe, sin contexto; o el que se pasa, el de la tarjeta en PvP o PvE), el mismo desde la lista
  // de cualquiera de los integrantes: de él depende qué se le aplica a cada uno (ver «Efectos iguales que no se suman»).
  if (lider === undefined) lider = liderDe(vs, null);
  // Un soporte o un liderazgo suma si a otro integrante le llega algo que se le aplica y le sirve (reparto: lo que no
  // tiene valor, solo si no lo tiene ya de una fuente anterior). Con foco (un equipo armado para un integrante) solo
  // cuenta lo que lo involucra: lo que le dan a él y lo que da él. Lo que los demás se dan entre ellos no suma para él.
  // Sin soloPuntaje, también va a las razones, con 0, lo que le llega y no se le suma (para decirlo).
  const suma = (tipo, a, k, x) => {
    const r = reparto(a, k, x, vs, lider, !soloPuntaje); if (!r) return;
    const involucra = (ms) => ms.includes(foco);
    if (foco && a !== foco && !involucra(r.si) && !r.no.some(([b]) => b === foco)) return;
    const pts = r.si.length && (!foco || a === foco || involucra(r.si)) ? (x.sig ? 3 : 2) : 0;
    if (pts) { score += pts; if (tipo === 'soporte') aplicados.push({ de: a, a: r.si }); if (k === 'artifact') art = true; }
    if (!soloPuntaje) razones.push({ tipo, de: a, k, x, a: r.si, no: r.no, pts });
  };
  // Soportes: pasivas de 4★ y Tier-2, efecto de uniforme y artefacto (si lo lleva).
  for (const a of vs) { const s = SOPORTES[a.p]; if (s) for (const k of SLOTS_SOPORTE) if (s[k]) suma('soporte', a, k, s[k]); }
  // Liderazgo: con foco, cuenta si lo involucra.
  const sl = lider && SOPORTES[lider.p];
  if (sl) for (const k of LIDERAZGOS) if (sl[k]) suma('liderazgo', lider, k, sl[k]);
  // Bonos de equipo: con todos sus integrantes en el equipo, les suben stats a todos. Cada uno suma
  // 1 si le sirve a alguien; con foco, si lo involucra: él está en el bono o le sirve a él. Sus
  // integrantes quedan vinculados entre sí, porque están juntos por el bono; a los demás les llega
  // como a cualquiera que esté en el equipo, así que no los vincula.
  for (const a of vs) {
    const bonos = BONOS_DE[a.cid]; if (!bonos) continue;
    for (const b of bonos) {
      if (b.m[0] !== a.cid || !estanTodos(b.m, vs)) continue;     // cada bono, una vez: desde su primer integrante
      const reciben = vs.filter(x => b.vs.some(v => leSirve(v, x)));
      if (!reciben.length || (foco && !b.m.includes(foco.cid) && !reciben.includes(foco))) continue;
      const integrantes = vs.filter(x => b.m.includes(x.cid));
      score += 1;
      for (const x of integrantes) aplicados.push({ de: x, a: integrantes.filter(y => y !== x) });
      // cada versión de sus stats (más de una si las páginas de la wiki no coinciden), a quienes les sirve; su
      // punto va con la primera
      if (!soloPuntaje) b.vs.forEach((v, i) => razones.push({ tipo: 'bono', b, i, x: v, integrantes, a: reciben.filter(x => leSirve(v, x)), pts: i ? 0 : 1 }));
    }
  }
  const covered = ROLES_EQUIPO.filter(r => vs.some(v => v.r.includes(r)));
  if (covered.length >= 2) { score += 1; if (!soloPuntaje) razones.push({ tipo: 'roles', roles: covered, pts: 1 }); }
  if (vs.every((v, i) => vs.findIndex(w => w.c === v.c) === i)) { score += 1; if (!soloPuntaje) razones.push({ tipo: 'clases', pts: 1 }); }
  // a cubre la debilidad de b si a le gana a la clase que le gana a b (un Universal también,
  // con su ventaja menor: suma lo mismo y la razón lo dice).
  for (const a of vs) for (const b of vs) {
    const amenaza = LE_GANA_A[b.c], fuerza = amenaza && VENTAJA[a.c][amenaza];
    if (a !== b && fuerza && (!foco || a === foco || b === foco)) {
      score += 1;
      if (!soloPuntaje) razones.push({ tipo: 'ventaja', a, b, amenaza, fuerza, pts: 1 });
    }
  }
  return { score, razones, aplicados, lider, art };
}
/** Nombre de un bono de equipo en las razones: «Bono de equipo «X» (A + B)», con la versión si la
 *  wiki no coincide (sin version, el bono entero: el detalle de PvP y PvE lo cuenta una vez). */
function nombreBono (r, version = true) {
  const nombre = `${t('sy_bonus')} ${r.b.n ? '«' + r.b.n + '»' : t('sy_bonus_noname')} (${r.integrantes.map(x => x.name).join(' + ')})`;
  return version && r.b.vs.length > 1 ? `${nombre} · ${t('sy_bonus_ver').replace('{i}', r.i + 1).replace('{n}', r.b.vs.length)}` : nombre;
}
/** El «*» de unos puntos que cuentan el soporte de un artefacto como si lo llevara (como el de las casillas). */
function artPts (art) { return art ? `<span class="pqart" title="${h(t('pt_art'))}">*</span>` : ''; }
/** Una razón de la sinergia que no es un efecto (roles, clases o ventaja de clase), en texto, con los
 *  integrantes nombrados por `nombre`. */
function razonTxt (r, nombre) {
  const ES = LANG === 'es';
  if (r.tipo === 'roles') return (ES ? 'Roles cubiertos (derivados de las skills): ' : 'Roles covered (derived from skills): ') + r.roles.map(dom).join(' + ') + '.';
  if (r.tipo === 'clases') return ES ? 'Clases distintas: no comparten la misma debilidad.' : 'Different classes: they do not share the same weakness.';
  if (r.tipo !== 'ventaja') throw new Error('razón de la sinergia desconocida: ' + r.tipo);
  return (ES ? `${nombre(r.a)} (${dom(r.a.c)}) cubre la debilidad de ${nombre(r.b)} (${dom(r.b.c)}) contra ${dom(r.amenaza)}`
             : `${nombre(r.a)} (${dom(r.a.c)}) covers ${nombre(r.b)}'s (${dom(r.b.c)}) weakness against ${dom(r.amenaza)}`)
    + (r.fuerza === 'menor' ? (ES ? ' (ventaja menor).' : ' (minor advantage).') : '.');
}
/** Las razones de la sinergia en texto, una por línea (la comparativa). A cada integrante, solo los
 *  efectos que le sirven: los que reciben lo mismo van en una línea. */
function razonesTxt (razones) {
  const ES = LANG === 'es', out = [];
  // A cada uno, lo que le sirve; lo que ya tiene de otra fuente (r.no), con «(no se suma: ya lo tiene de X)».
  const lineas = (prefijo, x, bs, no) => {
    const grupos = new Map();
    for (const b of bs.concat(no.map(([b]) => b).filter(b => !bs.includes(b)))) {
      const ya = new Map((no.find(([y]) => y === b) || [b, []])[1]);
      const fx = x.fx.filter(f => sirve(f, b)), txts = fx.map(f => efectoSoporteTxt(x, f)
        + (ya.has(f) ? ` (${t('rep_no_suma').replace('{de}', yaDe(b, ya.get(f), fullLabel, false))})` : '')), k = txts.join('\u0000');
      if (!grupos.has(k)) grupos.set(k, { txts, bs: [] });
      grupos.get(k).bs.push(b);
    }
    for (const g of grupos.values()) out.push(`${prefijo} → ${g.bs.map(fullLabel).join(', ')}: ${g.txts.join(' · ')}`);
  };
  for (const r of razones) {
    if (r.tipo === 'soporte') lineas(`${fullLabel(r.de)} · ${t(CLAVE_SOPORTE[r.k])}${r.k === 'artifact' ? ' (' + t('pq_si_art') + ')' : ''}`, r.x, r.a, r.no || []);
    else if (r.tipo === 'liderazgo') lineas(`${ES ? 'Con' : 'With'} ${fullLabel(r.de)} ${ES ? 'de líder' : 'as leader'}${srcTxt(r.x)}`, r.x, r.a, r.no || []);
    else if (r.tipo === 'bono') lineas(nombreBono(r), r.x, r.a, []);
    else out.push(razonTxt(r, fullLabel));
  }
  return [...new Set(out)];
}
/** ¿Un stat que el catálogo no tiene (MFF_CATALOGO.soporte)? Cuenta para todos y se dice. */
function sinClasificar (s) { return !CATALOGO.soporte[s]; }
/** Las razones de la sinergia en piezas, para comparar dos equipos (comoEntra): un efecto de un soporte,
 *  de un liderazgo o de un bono de equipo que le llega a un integrante, o una razón entera (roles, clases,
 *  ventaja de clase). { r, f, para, clave } (f y para, solo en las de un efecto). */
function piezas (razones) {
  const out = [];
  for (const r of razones) {
    if (r.tipo === 'roles' || r.tipo === 'clases' || r.tipo === 'ventaja') {
      out.push({ r, clave: r.tipo + '|' + (r.tipo === 'roles' ? r.roles.join('+') : r.tipo === 'ventaja' ? r.a.key + '|' + r.b.key : '') });
      continue;
    }
    // Solo lo que se le aplica: lo que ya tenía de otra fuente (r.no) no es una pieza.
    const origen = r.tipo === 'bono' ? 'b|' + r.b.m.join('+') + '|' + r.i : 's|' + r.de.key + '|' + r.k;
    const ya = (b, f) => !!r.no && r.no.some(([y, fs]) => y === b && fs.some(([g]) => g === f));
    for (const b of r.a) r.x.fx.forEach((f, n) => { if (sirve(f, b) && !ya(b, f)) out.push({ r, f, para: b, clave: origen + '|' + n + '|' + b.key }); });
  }
  return out;
}
/** ¿x tiene un vínculo con v en el equipo por un soporte o un bono de equipo? Le da algo (un soporte),
 *  recibe algo de él o forman juntos un bono. El liderazgo vincula según quién lidera (vinculoLider).
 *  Las clases y los roles no cuentan: un equipo armado alrededor de v no lleva compañeros que no
 *  tengan nada que ver con él. */
function vinculo (v, x, aplicados) {
  for (const e of aplicados) if ((e.de === v && e.a.includes(x)) || (e.de === x && e.a.includes(v))) return true;
  return false;
}
/** ¿El liderazgo vincula a x con v? Si el líder del equipo es v y su liderazgo le llega a x, o es x y le
 *  llega a v. El líder es el del contexto: sin contexto, el de la sinergia (liderSinContexto); en PvP y
 *  PvE, el del modo (Ezequiel, 4 de octubre de 2026, regla 2: un solo líder, el del modo, para todo lo de
 *  ese modo). */
function vinculoLider (v, x, lider) { return (lider === v && llegaLiderazgo(v, x)) || (lider === x && llegaLiderazgo(x, v)); }
/** ¿Le llega a b algo del liderazgo de a que se le aplica y le sirve? Se cuenta de a pares, con a de líder: lo que no se
 *  acumula se le aplica si gana entre lo propio de b, el liderazgo y los soportes de a (fuenteQueSeAplica). El tercero no
 *  cambiaría eso: ningún soporte trae más valor que un liderazgo del mismo stat (iniciarDatos lo confirma). */
function llegaLiderazgo (a, b) {
  const s = SOPORTES[a.p], vs = [a, b];
  return !!s && LIDERAZGOS.some(k => s[k] && aplicaAlgo(b, a, k, s[k], vs, a));
}

// ---------------------------------------------------------------------------
// TEXTO DE LAS SKILLS
// Un efecto guarda el índice de su patrón y sus números; el texto se arma acá.
// ---------------------------------------------------------------------------
/** Fila de una tabla de data.js. */
function fila (tabla, i) { return (i == null || !TB[tabla]) ? null : TB[tabla][i]; }
// thanosvibs publica algunas descripciones con marcadores de plantilla sin resolver
// ($HEROSUBTYPE1, $HEROCLASS1, $TIME). $TIME y $TICK tienen un campo real detrás y se
// resuelven con él. La facción, el tipo o la raza no vienen en ningún campo de la skill: el
// build los completa con la tabla a mano, con Leads & Supports o con la wiki (f.g, y de dónde
// salió en f.gs: 'm', 'l' o 'w') y se muestran marcados con su origen. Lo que no se completó
// se marca "sin especificar" en vez de inventarle un valor o dejar el marcador crudo a la vista.
const ORIGEN_MARCADOR = { m: 'tpl_manual', l: 'tpl_ls', w: 'tpl_wiki' };
/** lang: el idioma del texto (el «Texto del juego» muestra los dos); las marcas y sus títulos van en el de la app. */
function marcadores (texto, f, lang) {
  const chip = (clave, titulo) => `<i class="tpl" title="${h(t(titulo))}">${h(t(clave))}</i>`;
  const grupo = () => {
    if (!(f && f.g)) return chip('tpl_unspec', 'tpl_pending');
    const titulo = ORIGEN_MARCADOR[f.gs];
    if (!titulo) throw new Error('origen de marcador desconocido: ' + f.gs);
    return `<span class="tpl-ok" title="${h(t(titulo))}">${h(domIdioma(f.g, lang || LANG))}</span>`;
  };
  return texto
    .replace(/\$TIME/g, () => (f && f.d != null) ? f.d + ' s' : chip('tpl_unspec', 'tpl_title'))
    .replace(/\$TICK/g, () => (f && f.t != null) ? f.t + ' s' : chip('tpl_unspec', 'tpl_title'))
    .replace(/\$HERO(?:SUBTYPE|CLASS)\d*/g, grupo);
}
/** Reemplaza cada '#' del patrón por el número que le toca, en orden. */
function rellenar (patron, nums) {
  let i = 0;
  return String(patron).replace(/#/g, () => (nums && nums[i] !== undefined ? nums[i++] : '#'));
}
/** {txt, sinTraducir} de una fila, en el idioma activo o en el pedido (el «Texto del juego» muestra los dos). */
function texto (tabla, i, nums, lang = LANG) {
  const f = fila(tabla, i);
  if (!f) return null;
  if (lang === 'en') return { txt: rellenar(f.en, nums), sinTraducir: false };
  if (f.es == null) return { txt: rellenar(f.en, nums), sinTraducir: true };
  return { txt: rellenar(f.es, nums), sinTraducir: false };
}
// Tres objetivos de la fuente traen un "\n" literal (dos caracteres) metiendo la
// condicion de activacion adentro del objetivo. Se muestra como separador, no crudo.
const BARRA_N = /\\n/g;
function txt (tabla, i, nums, lang) { const r = texto(tabla, i, nums, lang); return r ? r.txt.replace(BARRA_N, ' · ') : ''; }
/** Los números de daño de un efecto, si el patrón es una línea de daño. */
function dano (f) {
  const d = fila('desc', f.p);
  if (!d || d.pi === undefined || !f.v) return null;
  return { pct: f.v[d.pi], flat: d.fi !== undefined ? f.v[d.fi] : null, src: d.src, elem: d.elem };
}
function esDano (f) { return dano(f) !== null; }
/** Nombre de la skill: traducción con el original al lado, que es con lo que se busca. */
function nombreSkill (sk) {
  const f = fila('name', sk.n);
  if (!f) return '';
  if (LANG === 'en' || f.es == null) return `<span class="nm">${h(f.en)}</span>`;
  return `<span class="nm">${h(f.es)}<span class="orig">${h(f.en)}</span></span>`;
}
function slotEs (sl) { return LANG === 'es' ? (SLOT_ES[sl] || sl) : sl; }
/** ¿El objetivo de la etapa es alguien distinto de uno mismo? */
function esAjeno (idxObjetivo) {
  const f = fila('tgt', idxObjetivo);
  return !!f && f.en.trim().toLowerCase() !== 'self';
}
/** Si el objetivo es un grupo de aliados (clase, bando, raza o habilidad), la restricción
 *  que lo define: la misma forma que las de líder y soporte, así que vale aplicaA. */
function grupoDe (idxObjetivo) { const f = fila('tgt', idxObjetivo); return f && f.r ? f.r : null; }
/** Etiqueta de un objetivo. Si es un grupo de aliados se toca y muestra quiénes lo cumplen. */
function objetivoTag (i, flecha) {
  const texto = h((flecha ? '→ ' : '') + txt('tgt', i));
  return grupoDe(i)
    ? `<button class="tag objetivo grupo" data-a="verAliados" data-tg="${i}" title="${h(t('al_ver'))}">${texto}</button>`
    : `<span class="tag objetivo">${texto}</span>`;
}
/** Lo mismo dentro de una línea de texto (el objetivo de una etapa). */
function objetivoTexto (i) {
  const texto = h(txt('tgt', i));
  return grupoDe(i) ? `<button class="objlink" data-a="verAliados" data-tg="${i}" title="${h(t('al_ver'))}">${texto}</button>` : texto;
}
/** Si todas las etapas declaran el mismo valor, devuelve ese índice; si no, null. */
function comunEnEtapas (sk, campo) {
  const vals = (sk.st || []).map(st => st[campo]).filter(x => x != null);
  if (!vals.length || vals.length !== (sk.st || []).length) return null;
  return vals.every(v => v === vals[0]) ? vals[0] : null;
}
// Atributos que el juego tiene pero la API de thanosvibs no publica (los verifiqué en
// las 886 respuestas). Los marca el usuario a mano y viven en su capa, así que
// sobreviven a cualquier sincronización.
const ATRIBUTOS = [
  { k:'it',  es:'Ignora objetivo',        en:'Ignore Targeting' },
  { k:'iat', es:'Ignora todo objetivo',   en:'Ignore All Targeting' },
  { k:'gb',  es:'Rotura de guardia',      en:'Guard Break' },
  { k:'sgb', es:'Superrotura de guardia', en:'Super Guard Break' },
];
function atrNombre (k) { const a = ATRIBUTOS.find(x => x.k === k); return a ? a[LANG] : k; }
/** Clave estable de una skill: el retrato y el tipo no cambian al regenerar los datos. */
function claveSkill (portrait, tipo) { return portrait + '::' + tipo; }
function marcasDe (portrait, tipo) { return U.marcas[claveSkill(portrait, tipo)] || {}; }
function marcar (portrait, tipo, k, valor) {
  const clave = claveSkill(portrait, tipo);
  const m = Object.assign({}, U.marcas[clave]);
  if (valor) m[k] = 1; else delete m[k];
  if (Object.keys(m).length) U.marcas[clave] = m; else delete U.marcas[clave];
  commit();
}
/** Atributos marcados en un set de skills, para filtrar y comparar. */
function atributosDe (portrait, skills) {
  const out = new Set();
  skills.forEach(sk => Object.keys(marcasDe(portrait, sk.sl)).forEach(k => out.add(k)));
  return out;
}

/** Índices de objetivo ajeno que toca un set de skills (para filtrar y comparar). */
function objetivosDe (skills) {
  const out = new Set();
  skills.forEach(sk => (sk.st || []).forEach(st => { if (esAjeno(st.tg)) out.add(st.tg); }));
  return out;
}
function slotClase (sl) {
  return sl === 'Leader Skill' ? 'lead'
       : (sl === 'Passive' || sl === 'Tier-2 Passive' || sl === 'Uniform Passive') ? 'pass'
       : sl === 'Active Ult' ? 'ult'
       : sl === 'Striker Skill' ? 'stk' : '';
}

/** El texto de un efecto en renglones (la fuente los separa con <br>), en HTML y con los marcadores
 *  resueltos, en el idioma activo o en el pedido. sinTraducir: falta la traducción y va el inglés. */
function renglonesEfecto (f, lang) {
  const r = texto('desc', f.p, f.v, lang);
  return { renglones: r.txt.split(/<br\s*\/?>/i).map(x => x.trim()).filter(Boolean).map(x => marcadores(h(x), f, lang)), sinTraducir: r.sinTraducir };
}
/** Lo que la fuente dice de un efecto aparte del texto: cada cuánto, cuánto dura y si lo marca persistente
 *  (persistent) o de equipo (team_buff). Con dura, la duración lo dice («dura 5 s»): fuera del renglón de la
 *  skill, «5 s» solo no se entiende. */
function metaEfecto (f, dura) {
  const meta = [];
  if (f.t != null) meta.push(t('every') + ' ' + f.t + ' s');
  if (f.d != null) meta.push((dura ? t('an_dura') + ' ' : '') + f.d + ' s');
  if (f.m) meta.push(t('permanent_fx'));
  if (f.b) meta.push(t('team_fx'));
  return meta;
}
/** Un efecto que no es daño: etiqueta tipada + texto, uno por línea. Al tocarlo se abre el «Cómo funciona»
 *  de la skill en ese efecto (si, ti, fi: skill, etapa y efecto). */
function efectoLinea (f, si, ti, fi) {
  const { renglones, sinTraducir } = renglonesEfecto(f), meta = metaEfecto(f), etiqueta = txt('ab', f.a);
  // Duración, tick y marcas van pegadas al final de la última línea, no en un renglón aparte.
  return `<div class="fxline" data-a="skTip" data-si="${si}" data-st="${ti}" data-fx="${fi}">
    <span class="fxtag" title="${h(etiqueta)}">${h(etiqueta)}</span>
    <div class="fxitems ${sinTraducir ? 'sintrad' : ''}"
         ${sinTraducir ? `title="${h(t('untranslated'))}"` : ''}>
      ${renglones.map((x, i) => `<div>${x}${
        i === renglones.length - 1 && meta.length ? ` <span class="dur">${h(meta.join(' · '))}</span>` : ''}</div>`).join('')}
    </div></div>`;
}

/** Una skill (la si de la variante v): tabla de daño por etapa arriba, y el resto de los efectos abajo. La
 *  cabecera abre su «Cómo funciona»; cada renglón, el mismo, en ese efecto. */
function skillCard (sk, v, si) {
  const etapas = sk.st || [];
  const marcas = marcasDe(v.p, sk.sl), abierta = !!ui.tip && ui.tip.si === si;
  const filasDano = [];
  etapas.forEach((st, i) => {
    (st.fx || []).forEach((f, fi) => {
      const dn = dano(f);
      if (dn) filasDano.push({ i, st, dn, f, fi });
    });
  });
  // A quien le pega y que lo dispara son datos de cabecera, no una nota al pie: se
  // muestran junto al nombre cuando valen para toda la skill.
  const tgComun = comunEnEtapas(sk, 'tg'), acComun = comunEnEtapas(sk, 'ac');
  const cabecera = [];
  ATRIBUTOS.forEach(a => { if (marcas[a.k]) cabecera.push(`<span class="tag atributo">${h(a[LANG])}</span>`); });
  if (esAjeno(tgComun)) cabecera.push(objetivoTag(tgComun, true));
  if (acComun != null) {
    const st0 = sk.st.find(x => x.ac === acComun) || {};
    cabecera.push(`<span class="tag dim">${h(t('st_activation'))}: ${h(txt('act', acComun, st0.av))}</span>`);
  }
  const varias = etapas.length > 1;

  // Cada etapa, junta (Ezequiel, 6 de octubre de 2026: «lo que ocurre en cada skill en cada etapa tiene que estar
  // unido»): su activación y su objetivo si difieren de la skill, el daño (% del ataque, el fijo y el elemento) y los
  // demás efectos, en ese orden. Antes el daño de todas las etapas iba en una tabla y los efectos aparte.
  const danoLinea = (r) => `<div class="stdano" data-a="skTip" data-si="${si}" data-st="${r.i}" data-fx="${r.fi}">
      <span class="fxlabel dano">${h(t('st_dano'))}</span>
      <b class="num">${h(r.dn.pct)}%</b> <span class="muted">${h(srcEs(r.dn.src))}</span>
      ${r.dn.flat != null ? `<span class="num">+${h(r.dn.flat)}</span>` : ''}
      ${r.st.el != null ? `<span class="tag dim">${h(txt('elem', r.st.el))}</span>` : `<span class="muted">${h(elemEs(r.dn.elem))}</span>`}</div>`;
  const otros = etapas.map((st, i) => {
    const danos = filasDano.filter(r => r.i === i).map(danoLinea);
    const fx = (st.fx || []).map((f, fi) => esDano(f) ? '' : efectoLinea(f, si, i, fi)).filter(Boolean);
    const meta = [];
    if (st.ac != null && st.ac !== acComun) meta.push(`<span class="stmeta">${h(t('st_activation'))}: ${h(txt('act', st.ac, st.av))}</span>`);
    if (st.tg != null && st.tg !== tgComun) meta.push(`<span class="stmeta">${h(t('st_target'))}: ${objetivoTexto(st.tg)}</span>`);
    if (!danos.length && !fx.length && !meta.length) return '';
    return `<div class="stageblock${varias ? ' varias' : ''}">
      ${varias ? `<span class="stnum" title="${h(t('st_stage'))} ${i + 1}">${i + 1}</span>` : ''}
      <div class="stcuerpo">${meta.length ? `<div class="stagehead">${meta.join('')}</div>` : ''}${danos.join('')}${fx.join('')}</div></div>`;
  }).join('');

  const cargas = [recargaHtml(v, sk)];
  if (sk.ult != null) cargas.push(`<span class="tag dim">${h(t('c_ult'))} ${h(sk.ult)}%</span>`);
  if (sk.stk != null) cargas.push(`<span class="tag dim">${h(t('c_striker'))} ${h(sk.stk)}%</span>`);

  // El tipo y el nombre son el botón del «Cómo funciona» (para el teclado); el resto de la cabecera
  // también lo abre al tocarlo, salvo el objetivo de grupo, que muestra quiénes lo cumplen.
  return `<div class="skill" id="${anclaSkill(sk.sl)}">
    <div class="top" data-a="skTip" data-si="${si}">
      <button class="sktit" id="skt-${si}" data-a="skTip" data-si="${si}" aria-haspopup="dialog" aria-expanded="${abierta}"${
        abierta ? ' aria-controls="skpop"' : ''} title="${h(t('tt_abrir'))}">
        <span class="slotbadge ${slotClase(sk.sl)}">${h(slotEs(sk.sl))}</span>
        ${nombreSkill(sk)}
      </button>
      ${cabecera.join('')}
      ${cargas.join('')}
    </div>
    <div class="body">${otros}
      ${ui.marcando ? `<div class="marcador">
        <span class="muted">${h(t('at_mark'))}</span>
        ${ATRIBUTOS.map(a => `<label class="chk"><input type="checkbox" data-a="marca"
            data-p="${h(v.p)}" data-sl="${h(sk.sl)}" data-k="${a.k}"
            ${marcas[a.k] ? 'checked' : ''}> ${h(a[LANG])}</label>`).join('')}
      </div>` : ''}
    </div>
  </div>`;
}
/** La recarga de una skill, la misma en su tarjeta, la comparativa y el «Cómo funciona», en dos niveles: la de
 *  la skill (o que se carga con su barra) y, si Leads & Supports le da a un efecto de esa skill una recarga
 *  distinta (soportesDeSkill), también esa. El liderazgo secundario de Thanos — Wise Harvester: «la skill no
 *  tiene (la fuente pone 0 s); según Leads & Supports, el efecto Quita todos los debuffs se recarga en 20 s». */
function recargaTxt (v, sk) {
  const propia = sk.cd ? numTxt(sk.cd) + ' s' : sk.cd === 0 ? t('tt_sin_recarga')
    : sk.sl === 'Active Ult' ? t('sk_bar_ult') : sk.sl === 'Striker Skill' ? t('sk_bar_stk') : t('tt_sin_dato');
  const otras = soportesDeSkill(v, sk).map(([k]) => SOPORTES[v.p][k]).filter(x => x.cd && x.cd !== sk.cd);
  if (!otras.length) return propia;
  return [sk.cd ? t('rc_skill').replace('{n}', propia) : sk.cd === 0 ? t('rc_skill_0') : propia].concat(otras.map(x =>
    t(x.fx.length > 1 ? 'rc_efectos' : 'rc_efecto').replace('{x}', x.fx.map(f => trTxt(f.s)).join(' + ')).replace('{n}', numTxt(x.cd) + ' s'))).join('; ');
}
/** recargaTxt como etiqueta, con su rótulo: «Recarga: 12 s». */
function recargaHtml (v, sk) { return `<span class="tag dim rec">${h(t('tt_recarga'))}: ${h(recargaTxt(v, sk))}</span>`; }
function srcEs (v) {
  if (LANG === 'en') return v;
  return { 'Physical Attack':'ataque físico', 'Energy Attack':'ataque de energía', 'HP':'vida' }[v] || v;
}
function elemEs (v) { return LANG === 'en' ? v : (txt('elem', (TB.elem || []).findIndex(x => x.en === v)) || v); }

/** Columnas de la comparación. */
const MAX_COMPARAR = 4;
/** Elige o deja de elegir una variante para comparar. Con MAX_COMPARAR elegidas no suma otra: lo dice
 *  (ui.avisoPick, en la mesa) en vez de descartar una. */
function togglePick (cid, uid) {
  const key = cid + '::' + (uid || 'base');
  const i = ui.picks.findIndex(x => x.key === key);
  ui.avisoPick = null;
  if (i > -1) { ui.picks.splice(i, 1); return; }
  if (ui.picks.length >= MAX_COMPARAR) {
    ui.avisoPick = t('cmp_lleno').replace('{n}', MAX_COMPARAR).replace('{x}', fullLabel(variant(cid, uid)));
    return;
  }
  ui.picks.push({ cid, uid: uid || null, key });
}
function readFile (file, cb) { const r = new FileReader(); r.onload = () => cb(r.result); r.readAsDataURL(file); }

// ============================================================================
// ROSTER
// ============================================================================
const SORTS = {
  name:   { k:'s_name',   get: v => fullLabel(v).toLowerCase() },
  tier:   { k:'s_tier',   get: v => ({T4:0,T3:1,T2:2})[v.t] },
  clase:  { k:'s_class',  get: v => v.c },
  bando:  { k:'s_side',   get: v => v.f },
  rank:   { k:'s_rank',   get: v => rankIndex(v.key) },
  skills: { k:'s_skills', get: v => -v.skills.length }
};
/** Índices de fila (en orden) de una entrada en una lista. */
function indicesFila (list, key) {
  const rows = rowsOf(list);
  return filasDe(list.id, key).map(r => rows.findIndex(x => x.id === r)).filter(i => i > -1).sort((a, b) => a - b);
}
/** Posición en la lista de referencia: la mejor fila en la que esté. */
function rankIndex (key) {
  const list = listById(U.prefs.refList); if (!list) return 999;
  const idx = indicesFila(list, key);
  return idx.length ? idx[0] : 999;
}
/** Las filas de una entrada en una lista: la mejor (su rótulo y su color) y los rótulos de todas; null si
 *  no está ubicada. */
function filaEn (list, key) {
  const idx = indicesFila(list, key); if (!idx.length) return null;
  const rows = rowsOf(list);
  return { label: rows[idx[0]].label, color: rowColor(idx[0], rows.length), todas: idx.map(i => rows[i].label) };
}
/** Sus filas en la lista de referencia (filaEn), o null. */
function rankLabel (key) { const list = listById(U.prefs.refList); return list ? filaEn(list, key) : null; }
/** Rótulo de la mejor fila, con "+N" si la entrada está en más filas. */
function rankTexto (rank) { return rank.label + (rank.todas.length > 1 ? ' +' + (rank.todas.length - 1) : ''); }

/** El filtro del índice (lo que da su liderazgo o su soporte) con su personaje de destino, o
 *  null si no se está usando. para.falta: el personaje elegido ya no está en los datos. */
function filtroIndice () {
  const P = U.prefs, F = P.filters;
  if (!F.lid.length && !F.sop.length && !P.para && !P.restr) return null;
  const para = P.para ? variant(...P.para.split('::')) : null;
  return { F, para, restr: P.restr, falta: !!P.para && !para };
}
function rosterData () {
  const q = ui.search.trim().toLowerCase();
  const P = U.prefs, F = P.filters, G = P.flags, FI = filtroIndice();
  let list = allVariants().filter(v => {
    if (P.kind === 'base' && v.uid) return false;
    if (P.kind === 'uni' && !v.uid) return false;
    if (q && !(v.name.toLowerCase().includes(q) || v.sub.toLowerCase().includes(q))) return false;
    if (F.c.length && !F.c.includes(v.c)) return false;
    if (F.t.length && !F.t.includes(v.t)) return false;
    if (F.f.length && !F.f.includes(v.f)) return false;
    if (F.ins.length && !F.ins.includes(v.ins)) return false;
    if (F.race.length && !F.race.includes(v.race)) return false;
    if (F.origin.length && !F.origin.includes(v.ch.origin)) return false;
    if (F.r.length && !F.r.some(r => v.r.includes(r))) return false;
    if (F.ab.length && !F.ab.some(a => v.ab.includes(a))) return false;
    if (G.t4 && v.t !== 'T4') return false;
    if (G.trans && !v.trans) return false;
    if (G.nuevo && !v.nuevo) return false;
    if (P.objetivo !== '' && !objetivosDe(v.skills).has(Number(P.objetivo))) return false;
    if (P.atributo !== '' && !atributosDe(v.p, v.skills).has(P.atributo)) return false;
    if (FI && !indiceDe(v, FI.F, FI.para, FI.restr)) return false;
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

/** Las restricciones que tienen los liderazgos y soportes de los datos, por tipo:
 *  [[tipo, [valores]]] en un orden fijo. */
function restriccionesSoporte () {
  const por = {};
  for (const s of Object.values(SOPORTES)) for (const [k] of TIPOS_SOPORTE) {
    const x = s[k]; if (x && x.r) (por[x.r[0]] = por[x.r[0]] || new Set()).add(x.r[1]);
  }
  const orden = ['Type', 'Side', 'Allies', 'Ability', 'Character'];
  for (const cat in por) if (!orden.includes(cat)) throw new Error('restricción de soporte desconocida: ' + cat);
  return orden.filter(cat => por[cat]).map(cat => [cat, [...por[cat]].sort()]);
}
/** Filtros del índice: qué da su liderazgo, qué da su soporte, para quién (el personaje que
 *  se elige desde su ficha) y si es un liderazgo o soporte solo para una clase, un bando, una
 *  raza, una etiqueta o un personaje. */
function filtrosIndice () {
  const P = U.prefs, F = P.filters, FI = filtroIndice();
  const chips = (cat) => CATEGORIAS.map(c => `<button class="chip ${F[cat].includes(c.k) ? 'on' : ''}" data-a="filter"
    data-cat="${cat}" data-v="${c.k}">${h(t('ct_' + c.k))}</button>`).join('');
  return `<div class="filtergroup ancho"><div class="lbl">${h(t('f_lid'))}</div><div class="row">${chips('lid')}</div></div>
    <div class="filtergroup ancho"><div class="lbl">${h(t('f_sop'))}</div><div class="row">${chips('sop')}</div></div>
    <div class="filtergroup"><div class="lbl">${h(t('f_para'))}</div>
      ${P.para ? `<button class="tag dim eqfuera" data-a="paraQuitar" title="${h(t('f_para_rm'))}">${
        h(FI.falta ? t('f_para_gone') : fullLabel(FI.para))} ✕</button>`
               : `<div class="muted" style="font-size:12px">${h(t('f_para_how'))}</div>`}</div>
    <div class="filtergroup"><div class="lbl">${h(t('f_restr'))}</div>
      <select data-a="restr" style="width:100%">
        <option value="">${h(t('f_any_target'))}</option>
        ${restriccionesSoporte().map(([cat, vals]) => `<optgroup label="${h(t('sp_r_' + cat))}">${vals.map(val =>
          `<option value="${h(cat + '|' + val)}" ${cat + '|' + val === P.restr ? 'selected' : ''}>${h(cat === 'Character' ? val : dom(val))}</option>`).join('')}</optgroup>`).join('')}
      </select></div>`;
}
/** En el roster, con el filtro del índice: lo que encontró en el liderazgo y el soporte. */
function indiceLinea (v) {
  const FI = filtroIndice(); if (!FI) return '';
  const x = indiceDe(v, FI.F, FI.para, FI.restr); if (!x) return '';
  const parte = (k, cats, extra) => cats.length ? `<div><span class="muted">${h(t(k))}:</span> ${cats.map(c => h(t('ct_' + c))).join(' · ')}${extra || ''}</div>` : '';
  const s = SOPORTES[v.p], api = LIDERAZGOS.some(k => s[k] && esDeApi(s[k]) && slotPasa(s[k], FI.F.lid, FI.para, FI.restr));
  return `<div class="indlinea">${parte('cd_lid', x.lid, api ? srcHtml({ src: 'api' }) : '')}${parte('cd_sop', x.sop)}</div>`;
}
/** Cuántos filtros del roster están puestos (los mismos para el roster y la lista de la izquierda). */
function filtrosActivos () {
  const P = U.prefs;
  return Object.values(P.filters).reduce((n, a) => n + a.length, 0) + Object.values(P.flags).filter(Boolean).length
       + (P.objetivo !== '' ? 1 : 0) + (P.atributo !== '' ? 1 : 0) + (P.para ? 1 : 0) + (P.restr ? 1 : 0);
}
/** El panel de filtros del roster: el mismo en el roster y en la lista de la izquierda (una sola regla, rosterData). */
function filtrosHtml () {
  const P = U.prefs, F = P.filters, G = P.flags;
  // El valor que viaja en data-v es siempre el del snapshot (español): el idioma solo
  // cambia lo que se ve, nunca la clave con la que se filtra ni la del ícono.
  const group = (clave, cat, values, ancho) => `<div class="filtergroup ${ancho ? 'ancho' : ''}"><div class="lbl">${h(t(clave))}</div><div class="row">${
    values.map(v => `<button class="chip ${F[cat].includes(v) ? 'on' : ''}" data-a="filter" data-cat="${cat}" data-v="${h(v)}">${icon(v)}${h(dom(v))}</button>`).join('')
  }</div></div>`;
  return `
      ${group('f_class','c',SEED.CLASSES)}
      ${group('f_role','r',SEED.ROLES)}
      ${group('f_tier','t',SEED.TIERS)}
      ${group('f_side','f',SEED.FACTIONS)}
      ${group('f_instinct','ins',SEED.INSTINCTS)}
      ${group('f_race','race',SEED.RACES)}
      ${group('f_origin','origin',[...new Set(CHARS.map(c => c.origin).filter(Boolean))].sort())}
      ${group('f_ability','ab',SEED.SKILL_TAGS, true)}
      ${filtrosIndice()}
      <div class="filtergroup"><div class="lbl">${h(t('f_shortcuts'))}</div><div class="row">
        <button class="chip ${G.t4 ? 'on' : ''}" data-a="flag" data-v="t4">${h(t('f_only_t4'))}</button>
        <button class="chip ${G.trans ? 'on' : ''}" data-a="flag" data-v="trans">${h(t('f_transcended'))}</button>
        <button class="chip ${G.nuevo ? 'on' : ''}" data-a="flag" data-v="nuevo">${h(t('f_new'))}</button>
      </div></div>
      <div class="filtergroup"><div class="lbl">${h(t('f_attrs'))}</div>
        <select data-a="atributo" style="width:100%">
          <option value="">${h(t('f_any_target'))}</option>
          ${ATRIBUTOS.map(a => `<option value="${a.k}" ${a.k === P.atributo ? 'selected' : ''}>${h(a[LANG])}</option>`).join('')}
        </select>
      </div>
      <div class="filtergroup"><div class="lbl">${h(t('f_targets'))}</div>
        <select data-a="objetivo" style="width:100%">
          <option value="">${h(t('f_any_target'))}</option>
          ${(TB.tgt || []).map((f, i) => ({ f, i })).filter(x => x.f.en.trim().toLowerCase() !== 'self')
            .sort((a, b) => (LANG === 'es' ? (a.f.es || a.f.en) : a.f.en).localeCompare(LANG === 'es' ? (b.f.es || b.f.en) : b.f.en))
            .map(x => `<option value="${x.i}" ${String(x.i) === String(P.objetivo) ? 'selected' : ''}>${h(txt('tgt', x.i))}</option>`).join('')}
        </select>
      </div>
      <div class="filtergroup"><div class="lbl">${h(t('f_reflist'))}</div>
        <select data-a="refList" style="width:100%">
          <option value="">${h(t('none_f'))}</option>
          ${listasAgrupadas().map(gr => ({ k: gr.k, ls: gr.ls.filter(l => tipoLista(l) === 'personajes') })).filter(gr => gr.ls.length)
            .map(gr => `<optgroup label="${h(t(gr.k))}">${gr.ls.map(l =>
            `<option value="${l.id}" ${l.id === U.prefs.refList ? 'selected' : ''}>${h(listName(l))}</option>`).join('')}</optgroup>`).join('')}
        </select>
      </div>
`;
}
function toolbar (total, shown) {
  const P = U.prefs;
  const active = filtrosActivos();
  // Con el panel de filtros abierto la barra no queda fija: el panel es más alto que la
  // pantalla y, fijo arriba, sus últimos grupos solo se veían al llegar al final de la página.
  return `<div class="toolbar ${P.filtersOpen ? 'conpanel' : ''}">
    <div class="line">
      <div class="search"><input id="q" placeholder="${h(t('search_ph'))}" value="${h(ui.search)}" data-a="search"></div>
      <button class="btn ${U.prefs.filtersOpen ? 'primary' : ''}" data-a="toggleFilters">${h(t('filters'))}${active ? ' · ' + active : ''}</button>
      ${active || ui.search ? `<button class="btn sm" data-a="clearFilters">${h(t('clear'))}</button>` : ''}
      <div class="seg">
        <button class="${P.kind === 'todo' ? 'on' : ''}" data-a="kind" data-v="todo">${h(t('all'))}</button>
        <button class="${P.kind === 'base' ? 'on' : ''}" data-a="kind" data-v="base">${h(t('bases'))}</button>
        <button class="${P.kind === 'uni' ? 'on' : ''}" data-a="kind" data-v="uni">${h(t('uniforms'))}</button>
      </div>
      <div class="seg">
        <button class="${U.prefs.view === 'grid' ? 'on' : ''}" data-a="view" data-v="grid">${h(t('cards'))}</button>
        <button class="${U.prefs.view === 'dense' ? 'on' : ''}" data-a="view" data-v="dense">${h(t('compact'))}</button>
        <button class="${U.prefs.view === 'table' ? 'on' : ''}" data-a="view" data-v="table">${h(t('table'))}</button>
      </div>
      <select data-a="sort" title="${h(t('sort'))}">${Object.entries(SORTS).map(([k, o]) => `<option value="${k}" ${k === U.prefs.sort ? 'selected' : ''}>${h(t(o.k))}</option>`).join('')}</select>
      <button class="btn icon" data-a="dir" title="${h(t('invert'))}">${U.prefs.dir === 1 ? '↑' : '↓'}</button>
      <button class="btn ${ui.pickMode ? 'primary' : ''}" data-a="pickMode">${ui.pickMode ? `${h(t('comparing'))} (${ui.picks.length}/${MAX_COMPARAR})` : h(t('compare'))}</button>
      <span class="count"><b>${shown}</b> ${h(t('of'))} ${total}</span>
    </div>
    ${U.prefs.filtersOpen ? `<div class="filterpanel">${filtrosHtml()}    </div>` : ''}
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
          title="${h(listName(listById(U.prefs.refList)) + ': ' + rank.todas.join(' · '))}">${h(rankTexto(rank))}</span></div>` : ''}
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
      <div class="rolebar" title="${h(v.r.map(dom).join(' · '))}">${SEED.ROLES.map(r => `<span style="background:${v.r.includes(r) ? roleColor(r) : 'var(--line)'}"></span>`).join('')}</div>
      <div class="muted" style="font-size:11.5px">${h(dom(v.f))} · ${v.skills.length} skills</div>
      ${indiceLinea(v)}
    </div>
  </div>`;
}

function tableHtml (rows) {
  const cols = ['c_character','f_class','f_tier','f_side','c_instinct','c_roles','c_striker','c_worldboss','c_skills','c_list'];
  return `<div class="tablewrap"><table class="dt"><thead><tr>${cols.map(k => `<th>${h(t(k))}</th>`).join('')}</tr></thead><tbody>
    ${rows.map(v => {
      const rank = rankLabel(v.key);
      const u = imgUrl('portrait-' + v.id);
      return `<tr data-a="open" data-cid="${v.cid}" data-uid="${v.uid || ''}">
        <td><div class="cellname">${u ? `<img class="thumb" src="${u}" alt="" loading="lazy">` : '<span class="thumb"></span>'}
          <div><div style="font-weight:600">${h(v.uid ? v.sub : v.name)}</div>${v.uid ? `<div class="muted" style="font-size:11.5px">${h(v.name)}</div>` : `<div class="muted" style="font-size:11.5px">${h(t('base'))}</div>`}${indiceLinea(v)}</div></div></td>
        <td>${tagGhost(dom(v.c), classColor(v.c))}</td>
        <td style="white-space:nowrap">${tagSolid(v.t, tierColor(v.t))}${transTag(v.trans)}</td>
        <td class="muted">${h(dom(v.f))}</td>
        <td class="muted">${h(v.ins === 'Desconocido' ? '—' : dom(v.ins))}</td>
        <td>${v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}">${h(dom(r))}</span>`).join(' ')}</td>
        <td class="mono">${v.striker != null ? h(v.striker) : '—'}</td>
        <td class="muted">${h(dom(v.wba) || '—')}</td>
        <td class="mono">${v.skills.length}</td>
        <td>${rank ? `<span class="tag solid" style="background:${rank.color}" title="${h(rank.todas.join(' · '))}">${h(rankTexto(rank))}</span>` : '<span class="muted">—</span>'}</td>
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
    ? `<div class="empty"><div class="big">∅</div><div>${h(t('no_match'))}</div>
       <button class="btn sm" style="margin-top:12px" data-a="clearFilters">${h(t('clear_filters'))}</button></div>`
    : U.prefs.view === 'table' ? tableHtml(slice)
    : `<div class="grid ${U.prefs.view === 'dense' ? 'dense' : ''}">${slice.map(cardHtml).join('')}</div>`;
  return toolbar(total, rows.length) + body + pager(pages, ui.page, 'page');
}
/** Paginador: extremos, vecinos de la actual y "…" entre medio, así llega a todas las páginas sin una fila de
 *  veintitantos botones. `accion` es el data-a que atiende el clic. */
function pager (pages, cur, accion) {
  if (pages <= 1) return '';
  const nums = [];
  for (let i = 0; i < pages; i++) {
    if (i < 2 || i > pages - 3 || Math.abs(i - cur) <= 1) nums.push(i);
    else if (nums[nums.length - 1] !== '…') nums.push('…');
  }
  return `<div class="row" style="justify-content:center;margin-top:22px">
    <button class="btn sm" data-a="${accion}" data-p="${Math.max(0, cur - 1)}" ${cur === 0 ? 'disabled' : ''}>←</button>
    ${nums.map(n => n === '…' ? '<span class="muted">…</span>' : `<button class="btn sm ${n === cur ? 'primary' : ''}" data-a="${accion}" data-p="${n}">${n + 1}</button>`).join('')}
    <button class="btn sm" data-a="${accion}" data-p="${Math.min(pages - 1, cur + 1)}" ${cur === pages - 1 ? 'disabled' : ''}>→</button>
  </div>`;
}

// ============================================================================
// FICHA
// ============================================================================
const STAT_ES = { recovery_rate:'Recuperación', fire_resist:'Res. fuego', cold_resist:'Res. frío',
                  lightning_resist:'Res. rayo', poison_resist:'Res. veneno', mind_resist:'Res. mental' };
function statLabel (k) { return LANG === 'es' ? (STAT_ES[k] || k) : dom(k); }
// La ficha va en pestañas, con una cabecera fija arriba (foto, nombre y uniforme): el
// uniforme cambia casi todo lo de abajo, así que su selector tiene que estar siempre a la
// vista. Cada pestaña responde una pregunta: qué es y para qué sirve, qué hace (las skills
// tal como las publica la fuente, y su análisis según el modelo), cómo se arma, cuánto
// avanzaste con él, y el resto.
const FICHA_TABS = ['resumen', 'skills', 'armado', 'equipos', 'fuentes'];
function renderDetail () {
  const ch = CHAR_BY_ID[ui.charId];
  if (!ch) { ui.view = 'roster'; return renderRoster(); }
  const v = variant(ch.id, ui.uniformId);
  const cuerpo = { resumen: fichaResumen, skills: fichaSkills, armado: fichaArmado, equipos: fichaEquipos, fuentes: fichaFuentes }[ui.fichaTab];
  if (!cuerpo) throw new Error('pestaña de la ficha desconocida: ' + ui.fichaTab);
  const ant = lugarAnterior();
  return `
  <div class="row" style="margin-bottom:14px">
    ${ant && ant.view !== 'roster' ? `<button class="btn sm primary" data-a="atras" title="${h(t('back_to').replace('{x}', nombreLugar(ant, true)))}">← ${h(nombreLugar(ant))}</button>` : ''}
    <button class="btn sm" data-a="back">${h(t('back_roster'))}</button>
    ${botonPoner(v)}
    <button class="btn sm" data-a="pickThis" data-cid="${ch.id}" data-uid="${v.uid || ''}" ${ui.picks.some(p => p.key === v.key) ? 'disabled' : ''}>${h(t('compare_this'))}</button>
    <button class="btn sm" data-a="edit" data-cid="${ch.id}">${h(t('edit'))}</button>
    <button class="btn sm ${ui.marcando ? 'primary' : ''}" data-a="marcarModo">${h(ui.marcando ? t('at_done') : t('at_edit'))}</button>
  </div>
  ${fichaCabecera(ch, v)}
  <div class="fcuerpo" id="fcuerpo">${cuerpo(ch, v)}</div>`;
}
/** Cabecera fija: quién es, con qué uniforme y qué parte de la ficha se está viendo. */
/** Una regla o una explicación, a un «?» junto al título, en vez de un párrafo arriba de lo que explica (#24). */
function ayudaHtml (texto) {
  return `<details class="ayuda"><summary title="${h(t('ay_label'))}" aria-label="${h(t('ay_label'))}">?</summary><div class="ayudatx">${h(texto)}</div></details>`;
}
/** Abre la ficha de un personaje (con un uniforme) desde el roster o desde las flechas. */
function abrirFicha (cid, uid) {
  ui.view = 'detail'; ui.charId = cid; ui.uniformId = uid || 'base'; ui.movil = 'centro';
  ui.eqPagina = 0; ui.eqCon = ''; ui.eqVerDescartados = false;
  render(); window.scrollTo(0, 0);
}
/** Anterior y siguiente en el listado del roster tal como está filtrado y ordenado: la misma
 *  entrada (personaje y uniforme) o, si esa no está, la primera de ese personaje. */
function vecinosEnListado (v) {
  const lista = rosterData();
  let i = lista.findIndex(x => x.key === v.key);
  if (i < 0) i = lista.findIndex(x => x.cid === v.cid);
  return { i, n: lista.length, prev: i > 0 ? lista[i - 1] : null, next: i > -1 && i < lista.length - 1 ? lista[i + 1] : null };
}
function navFicha (v) {
  const nav = vecinosEnListado(v);
  const flecha = (x, txt, k) => x
    ? `<button class="btn icon fnavb" data-a="fichaVecina" data-cid="${x.cid}" data-uid="${x.uid || ''}" title="${h(t(k) + ': ' + fullLabel(x))}">${txt}</button>`
    : `<button class="btn icon fnavb" disabled title="${h(t(k))}">${txt}</button>`;
  return `<div class="fnav">${flecha(nav.prev, '‹', 'nav_prev')}
    <span class="muted" title="${h(t('nav_title'))}">${h(nav.i > -1 ? t('nav_pos').replace('{i}', nav.i + 1).replace('{n}', nav.n) : t('nav_out'))}</span>
    ${flecha(nav.next, '›', 'nav_next')}</div>`;
}
function fichaCabecera (ch, v) {
  const actual = v.uid || 'base';
  const opcion = (uid, nombre, tier) => `<option value="${uid}" ${actual === uid ? 'selected' : ''}>${h(nombre)} · ${h(tier)}</option>`;
  return `<div class="fcab">
    <div class="fcab-id">
      <div class="fcab-face shot">${shot(v.id)}</div>
      <div class="fcab-nom"><h1>${h(ch.name)}</h1>
        <div class="row">${tagGhost(dom(v.c), classColor(v.c))}${tagSolid(v.t, tierColor(v.t))}${v.trans ? tagSolid(t('transcended_tag'), 'var(--gold)') : ''}${
          v.nuevo ? tagSolid(t('new_tag'), 'var(--gold)') : ''}</div></div>
      ${navFicha(v)}
      <label class="fcab-uni"><span>${h(t('d_uniform'))}</span>
        <select data-a="uniformSel">${opcion('base', t('base'), ch.t)}${ch.uniforms.map(u => opcion(u.id, u.name, u.tier)).join('')}</select></label>
    </div>
    <div class="ftabs" role="tablist">${FICHA_TABS.map(k => `<button class="ftab ${ui.fichaTab === k ? 'on' : ''}" role="tab"
      aria-selected="${ui.fichaTab === k}" data-a="fichaTab" data-v="${k}">${h(t('ft_' + k))}</button>`).join('')}</div>
  </div>`;
}
/** Resumen: qué es (datos del uniforme puesto) y para qué se usa según las fuentes. */
function fichaResumen (ch, v) {
  // Primero la respuesta (#24, Ezequiel, 6 de octubre de 2026: priorizar la información): dónde rinde, qué le da al
  // equipo y qué necesita. Después quién es, y plegado lo demás que dicen las fuentes.
  const vf = verifDe(ch, v);
  const stats = Object.entries(ch.stats || {}).filter(([, val]) => parseFloat(val) !== 0);
  const box = (k, val) => `<div class="stat"><div class="k">${h(k)}</div><div class="v">${val}</div></div>`;
  return `<div class="resumen3">
      <section class="bloque"><h4>${h(t('rs_donde'))}</h4>${usoListas(ch, v)}</section>
      <section class="bloque"><h4>${h(t('rs_da'))}</h4>${queDaHtml(v)}</section>
      <section class="bloque"><h4>${h(t('rs_necesita'))}</h4>${queNecesitaHtml(ch, v)}</section>
    </div>
    <div class="section fid"><h3>${h(t('rs_quien'))}</h3>
    <div class="row">
      <span class="tag dim">${h(dom(v.f))}</span>${insTag(v.ins)}
      ${v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}" title="${h(t('an_roles_t'))}">${h(dom(r))}</span>`).join('')}
      ${vf.dif.length ? `<a href="#verif" class="tag ghost" style="color:var(--gold)" data-a="irVerif" title="${h(t('vf_title'))}">⚠ ${h(verifCuenta(vf))}</a>` : ''}
    </div>
    <div class="row"><span class="muted">${h(t('rs_pega'))}</span> ${pegaAn(v)}</div>
    <div class="statgrid">
      ${box(t('d_race'), icon(v.race) + h(dom(v.race) || '—'))}
      ${box(t('d_gender'), icon(v.gender) + h(dom(v.gender) || '—'))}
      ${box(t('d_origin'), h(dom(ch.origin) || '—'))}
      ${box(t('c_striker'), v.striker != null ? 'Skill ' + h(v.striker) : '—')}
      ${box(t('c_worldboss'), icon(v.wba) + h(dom(v.wba) || '—'))}
      ${v.cost ? box(t('d_cost'), h(v.cost)) : ''}
      ${stats.map(([k, val]) => box(statLabel(k), h(val))).join('')}
    </div>
    <div class="row">
      <span class="muted">${h(t('d_abilities'))}</span>
      ${(v.ab || []).map(a => `<span class="tag dim">${icon(a)}${h(dom(a))}</span>`).join('') || '<span class="muted">—</span>'}
    </div>
    ${(ch.tuc || []).length ? `<div class="row"><span class="muted">${h(t('d_tuc'))}</span>${ch.tuc.map(x => `<span class="tag dim">${h(x)}</span>`).join('')}</div>` : ''}
    ${leSirveHtml(v)}
    </div>
    <div class="section"><h3>${h(t('rs_mas_fuentes'))}</h3>
      <details class="usgrupo usodet"><summary>${h(t('rs_det_sop'))}</summary>${usoSoportes(v)}</details>
      <details class="usgrupo"><summary>Alliance Battle</summary>${usoABX(ch, v)}</details>
      <details class="usgrupo"><summary>${h(t('us_guide'))}</summary>${usoGuia(ch, v)}</details>
      <details class="usgrupo"><summary>${h(t('ga_title'))}</summary>${usoArmado(ch, v)}</details>
    </div>`;
}
/** Lo que le da al equipo, corto: cada liderazgo o soporte con lo que da y a quién. El detalle (activación, recarga,
 *  condiciones, categorías) va plegado más abajo (usoSoportes). */
function queDaHtml (v) {
  const s = SOPORTES[v.p], tipos = s ? TIPOS_SOPORTE.filter(([k]) => s[k]) : [];
  const otorga = otorgaSinPublicar(v) ? `<p class="usotorga" style="color:var(--gold)">⚠ ${h(t('us_otorga'))}</p>` : '';
  if (!tipos.length) return `${otorga}<p class="muted">${h(t('us_sup_none'))}</p>`;
  return `${otorga}${tipos.map(([k, clave]) => { const x = s[k];
    return `<div class="rsda">
      <div class="row" style="gap:5px"><span class="slotbadge ${k.startsWith('leader') ? 'lead' : 'pass'}">${h(t(clave))}</span>
        ${x.sig ? `<span class="tag solid" style="background:var(--gold)" title="${h(t('sp_notable_t'))}">${h(t('sp_notable'))}</span>` : ''}
        ${x.est ? `<span class="tag dim">${h(t('sp_est').replace('{n}', x.est))}</span>` : ''}${srcHtml(x)}</div>
      <div class="rsfx">${x.fx.map(f => h(efectoSoporteTxt(x, f))).join(' · ')}</div>
      <div>${restrHtml(x)}</div></div>`; }).join('')}
    <div class="fuentes">${fuentesHtml(fuentesSop(tipos.map(([k]) => s[k])))}</div>`;
}
/** Lo que necesita, corto: C.T.P. (las dos fuentes), artefacto, ISO-8 y obelisco. El detalle, en la pestaña Armado. */
function queNecesitaHtml (ch, v) {
  const r = ctpRecomendado(v, null), a = GUIA_ARMADO ? armadoDe(ch) : null, art = ARTES.find(x => x.p === ch.p);
  const fila = (k, val) => `<div class="rsfila"><span class="muted">${h(k)}</span><span>${val}</span></div>`;
  const ctps = [r.armado ? `${r.armado.cols.filter(([, c]) => c).map(([, c]) => ctpCorto(c)).join(' ')} <span class="muted">${h(t('rs_ctp_armado'))}</span>${otraVar(r.armado.vv, v)}` : '',
                r.ideal ? `${r.ideal.filas.map(ctpFilaIdeal).join(' ')} <span class="muted">${h(t('rs_ctp_ideal'))}</span>${otraVar(r.ideal.vv, v)}` : '']
    .filter(Boolean).map(x => `<div class="row" style="gap:5px">${x}</div>`).join('');
  return `${fila('C.T.P.', ctps || '<span class="muted">—</span>')}
    ${fila(t('ar_art'), art ? `${h(art.name)}${a && a.e.art ? ` <span class="muted">· ${trHtml(a.e.art.t)}</span>` : ''}` : '<span class="muted">—</span>')}
    ${fila('ISO-8', a && (a.e.iso || a.e.iso_x) ? `${(a.e.iso || []).map(trHtml).join(', ')}${a.e.iso_x ? sinInterpretar(a.e.iso_x) : ''}` : '<span class="muted">—</span>')}
    ${fila(t('ga_obelisk'), a && (a.e.ob || a.e.ob_x) ? `${(a.e.ob || []).map(trHtml).join(', ')}${(a.e.ob_x || []).map(sinInterpretar).join('')}` : '<span class="muted">—</span>')}
    <button class="btn sm" data-a="fichaTab" data-v="armado">${h(t('rs_ver_armado'))}</button>`;
}
/** Skills del uniforme puesto: cargas, buffs clave, rotaciones y cada skill. */
function fichaSkills (ch, v) {
  if (!v.skills.length) return `<div class="empty"><div class="big">?</div><div>${h(t('d_no_skills'))}</div></div>`;
  const car = cargas(v.skills), kb = BUFFS[v.p] || {}, ks = Object.keys(kb);
  return `<div class="chargebar">
      <span>${h(t('c_ult'))}</span><div class="bar"><i style="width:${Math.min(100, car.ult)}%;background:var(--accent)"></i></div><b>${car.ult}%</b>
      <span>${h(t('c_striker'))}</span><div class="bar"><i style="width:${Math.min(100, car.stk)}%;background:var(--role-control)"></i></div><b>${car.stk}%</b>
    </div>
    ${ks.length ? `<div class="keybuffs">
      <div class="kbhead">${h(t('c_keybuffs'))}</div>
      ${ks.map(k => `<div class="kbrow"><span class="kbname">${h(k)}</span>
         <span class="kbsrc">${kb[k].map(x => `<span class="tag dim">${h(slotEs(x))}</span>`).join('')}</span></div>`).join('')}
    </div>` : ''}
    ${v.skills.map((sk, si) => skillCard(sk, v, si)).join('')}
    ${panelRotaciones(ch, v)}`;
}
// ---------------------------------------------------------------------------
// ANÁLISIS (docs/MODELO.md, etapa 2): lo que hace la variante con sus skills según el catálogo de efectos (MFF_ANALISIS).
// Desde la 1.0.27 no tiene pestaña propia (#33: hay que rehacerla para que conteste preguntas); lo usan el «Cómo
// funciona» de cada skill y el «Pega con» del Resumen.
// ---------------------------------------------------------------------------
/** El efecto de una fuente [skill, etapa, efecto] y cómo lo clasifica el catálogo. */
function fuenteAn (v, [si, ti, fi]) {
  const sk = v.skills[si], st = sk.st[ti], f = st.fx[fi], m = CATALOGO.skills[fila('ab', f.a).en];
  return { sk, st, f, m: m.por_patron ? m.por_patron[fila('desc', f.p).en] : m };
}
/** La condición del catálogo; las fuentes de una entrada comparten la misma. Contra una
 *  facción, un tipo o una raza que la skill nombra con un marcador, va lo que se completó. */
function condicionAn (v, fuentes) {
  const c = fuenteAn(v, fuentes[0]).m.condicion;
  if (!c) return '';
  if (c.varia) return t('an_varia') + ' ' + bi(c.varia);
  if (c.dura) return t('an_dura') + ' ' + bi(c.dura);
  const contra = bi(CATALOGO.contra[c.contra]);
  if (!c.marcador) return contra;
  return contra + ': ' + [...new Set(fuentes.map(x => fuenteAn(v, x).f.g))].map(g => g ? dom(g) : t('tpl_unspec')).join(', ');
}
/** La certeza de una lectura (CATALOGO.certeza): comprobado, probable o conjetura. */
function certHtml (c) { return `<span class="cert ${c}">${h(t('cert_' + c))}</span>`; }
function lecturaAn (L, modo) {
  return `<div class="anlect"><b>${h(modo)}</b>${h(bi(L))} ${certHtml(L.certeza)}${fuentesHtml(L.fuente)}</div>`;
}
/** La primera letra en minúscula, para seguir una frase («A quien tiene Perforación»). */
function minuscula (x) { return x ? x[0].toLowerCase() + x.slice(1) : x; }
/** A quién le sirve un efecto del catálogo, en HTML: la regla del efecto (la de sus skills) y, si un stat de liderazgo,
 *  soporte o bono de equipo que apunta a él tiene otra (MFF_CATALOGO.soporte: las velocidades, las resistencias...),
 *  la lista de esos stats con la suya, que es la que usa la app en los equipos. Lo muestran el Glosario y el «Cómo
 *  funciona», cada uno con sus renglones: renglon(rótulo, texto), los dos ya en HTML. */
function leSirveEfectoHtml (e, renglon) {
  const regla = (r) => h(minuscula(bi(CATALOGO.sirve[r])));
  const otros = GL_DE[e.id].stats.filter(st => CATALOGO.soporte[st].sirve !== e.sirve);
  if (!otros.length) return renglon(h(t('gl_le_sirve')), regla(e.sirve));
  return renglon(h(t('gl_le_sirve_skills')), regla(e.sirve)) + renglon(h(t('gl_le_sirve_ls')), `<ul class="sirvestat">${
    otros.map(st => `<li>${h(trTxt(st))}: ${regla(CATALOGO.soporte[st].sirve)}</li>`).join('')}</ul>`);
}
/** Si se suma, cuando a alguien le llega de dos fuentes (Efectos iguales), cada stat de liderazgo, soporte o bono de equipo
 *  que apunta al efecto (MFF_CATALOGO.soporte, acumula): una sola respuesta si todos dicen lo mismo y ninguno trae nota; si
 *  no, uno por uno, con su nota (la de los dudosos dice [Conjetura]). Nada si ningún stat apunta a él. Como
 *  leSirveEfectoHtml. */
function acumulaEfectoHtml (e, renglon) {
  const sts = GL_DE[e.id].stats;
  if (!sts.length) return '';
  const dice = (st) => h(t(CATALOGO.soporte[st].acumula ? 'gl_se_suma' : 'gl_una_vez'));
  const nota = (st) => CATALOGO.soporte[st].nota ? ` <span class="muted">— ${h(bi(CATALOGO.soporte[st].nota))}</span>` : '';
  if (sts.every(st => CATALOGO.soporte[st].acumula === CATALOGO.soporte[sts[0]].acumula && !CATALOGO.soporte[st].nota)) {
    return renglon(h(t('gl_acumula')), dice(sts[0]));
  }
  return renglon(h(t('gl_acumula')), `<ul class="sirvestat">${sts.map(st => `<li>${h(trTxt(st))}: ${dice(st)}${nota(st)}</li>`).join('')}</ul>`);
}
/** El tope de los stats de liderazgo, soporte o bono de equipo que apuntan al efecto (topesDe), con la fuente de la guía:
 *  uno solo si todos los stats del efecto tienen el mismo; si no, el de cada uno que tiene. Nada si ninguno tiene. Como
 *  leSirveEfectoHtml. */
function topeEfectoHtml (e, renglon) {
  const todos = GL_DE[e.id].stats, sts = todos.filter(st => topesDe(st).length);
  if (!sts.length) return '';
  const txt = (st) => topesDe(st).map(x => topeTxt(x, topesDe(st).length > 1)).join(', '), fuente = ' ' + fuentesHtml(GUIA.topes.fuente);
  if (sts.length === todos.length && sts.every(st => txt(st) === txt(sts[0]))) return renglon(h(t('gl_tope')), h(txt(sts[0])) + fuente);
  return renglon(h(t('gl_tope')), `<ul class="sirvestat">${sts.map(st => `<li>${h(trTxt(st))}: ${h(txt(st))}</li>`).join('')}</ul>${fuente}`);
}
/** La primera letra en mayúscula, para que una frase arranque un renglón («Contra una facción: …»). */
function mayuscula (x) { return x ? x[0].toUpperCase() + x.slice(1) : x; }
/** El nombre de un efecto del análisis. Un «Give Power» que queda como entrada es uno que no dice qué otorga. */
function nombreAnTxt (e) { return e.id === 'otorga' ? t('an_otorga') : bi(e); }
function nombreAnHtml (e) {
  return `<span class="annom" ${e.id === 'otorga' ? `title="${h(t('an_otorga_t'))}"` : ''}>${h(nombreAnTxt(e))}</span>`;
}
/** Un efecto para él que no le sirve, según la regla «le sirve» del catálogo. */
function noSirveHtml (e) {
  return `<span class="tag solid nosirve" title="${h(t('an_no_sirve_t').replace('{x}', minuscula(bi(CATALOGO.sirve[e.sirve]))))}">${h(t('an_no_sirve'))}</span>`;
}
/** Las lecturas de PvE y de PvP; si dicen lo mismo, en una sola línea. */
function lecturasAn (pve, pvp) {
  if (pve && pvp && JSON.stringify(pve) === JSON.stringify(pvp)) return lecturaAn(pve, t('an_pve_pvp'));
  return (pve ? lecturaAn(pve, 'PvE') : '') + (pvp ? lecturaAn(pvp, 'PvP') : '');
}
/** Con qué pega: de qué ataque sale su daño, de qué tipo y con qué elementos (etapa 1). */
function pegaAn (v) {
  const pf = perfilDe(v);
  if (!pf.esc.length) return `<span class="muted">${h(t('us_atk_none'))}</span>`;
  return `${h(t('an_escala'))} ${ataqueHtml(tipoAtaque(v))} · ${h(t('an_tipos'))} ${pf.tip.map(x => h(t('el_' + x))).join(' + ')} · ${
    h(t('an_elems'))}: ${pf.ele.length ? pf.ele.map(x => h(t('el_' + x))).join(', ') : h(t('an_sin_elem'))}`;
}

// ---------------------------------------------------------------------------
// CÓMO FUNCIONA UNA SKILL
// Al tocar una skill en la pestaña Skills (la cabecera o uno de sus renglones) se abre, anclado a lo
// tocado, lo que la app sabe de ella; en el celular, como hoja inferior. No trae texto propio: sale del
// análisis y del catálogo de efectos (qué es cada efecto, a quién le llega, a quién le sirve y cómo se
// lee, con su certeza), del glosario del juego, de las skills de thanosvibs (activación, recarga,
// objetivo, duración y texto) y de Leads & Supports. Cinco secciones: cómo funciona; cuándo, cuánto y a
// quién; el texto del juego; certeza y fuentes; y lo que el inglés traduce distinto del coreano. Se abre
// y se cierra sin volver a pintar la ficha (no se pliega nada de lo que estaba abierto), no abre otra
// entrada del historial y se cierra con Esc, tocando afuera o con su botón.
// ---------------------------------------------------------------------------
const TIP_CELULAR = '(max-width: 600px)';      // hasta este ancho va como hoja inferior (el mismo de styles.css)
/** El efecto [skill, etapa, efecto] de una variante. */
function efectoDe (v, [si, ti, fi]) { return v.skills[si].st[ti].fx[fi]; }
/** ¿La entrada sale del efecto fi de la etapa ti de su skill? */
function tocaEfecto (x, ti, fi) { return x.fuentes.some(s => s[1] === ti && s[2] === fi); }
/** Lo que hace la skill si de v, en el orden de la skill: las entradas del análisis que salen de ella (un
 *  efecto del catálogo con su destino, sus aliados y su condición), el golpe (el análisis no lo trae: es el
 *  perfil de combate; va contra el rival, como lo da el catálogo) y lo que el catálogo no clasifica, cada
 *  una con sus fuentes en esta skill ([skill, etapa, efecto]). Un «Give Power» seguido de lo que otorga no
 *  es una entrada: lo otorgado, sí. Un efecto que no cae en ninguna es un error. */
function entradasSkill (v, si) {
  const an = ANALISIS[v.p], sk = v.skills[si], out = [];
  an.fx.forEach(([ie, d, objetivo, fuentes], i) => {
    const fs = fuentes.filter(x => x[0] === si);
    if (fs.length) out.push({ ie, d, objetivo, fuentes: fs, ns: (an.ns || []).includes(i) });
  });
  for (const x of an.sc || []) if (x[0] === si) out.push({ sc: true, fuentes: [x] });
  const golpe = [];
  sk.st.forEach((st, ti) => st.fx.forEach((f, fi) => { if (esDano(f)) golpe.push([si, ti, fi]); }));
  if (golpe.length) out.push({ ie: CATALOGO.efectos.findIndex(e => e.id === 'golpe'), d: 'r', objetivo: null, fuentes: golpe, ns: false });
  sk.st.forEach((st, ti) => st.fx.forEach((f, fi) => {
    if (!out.some(x => tocaEfecto(x, ti, fi)) && !fuenteAn(v, [si, ti, fi]).m.efectos.includes('otorga'))
      throw new Error(`efecto de ${v.p} sin entrada en el análisis: ${sk.sl}, etapa ${ti + 1}, efecto ${fi + 1}`);
  }));
  const pos = (x) => Math.min(...x.fuentes.map(([, ti, fi]) => ti * 1000 + fi));
  return out.sort((a, b) => pos(a) - pos(b));
}
/** Los términos del glosario del juego que corresponden a los efectos de las entradas, en el orden del glosario. */
function terminosSkill (es) {
  const ids = new Set(es.filter(x => !x.sc).map(x => CATALOGO.efectos[x.ie].id));
  return GLOSARIO.terminos.filter(y => y.efectos.some(id => ids.has(id)));
}
/** El rótulo de los liderazgos y soportes de una skill según su fuente: Leads & Supports, la skill del juego o las dos. */
function rotuloLs (xs) { return xs.every(esDeApi) ? 'tt_ls_api' : xs.some(esDeApi) ? 'tt_ls_mixto' : 'tt_ls'; }
/** Los liderazgos y soportes de Leads & Supports que la ficha atribuye a esta skill (skillDeSoporte). */
function soportesDeSkill (v, sk) {
  const s = SOPORTES[v.p];
  return s ? TIPOS_SOPORTE.filter(([k]) => k !== 'artifact' && s[k] && skillDeSoporte(v, k, s[k]) === sk) : [];
}
/** A quién le llega una entrada (el destino del análisis) y, si es al equipo, a qué aliados. */
function destinoTipHtml (x) {
  return `<span class="tag tipd ${x.d}">${h(t('an_' + x.d))}</span>${x.d === 'q' ? ` <span class="tag objetivo">→ ${h(txt('tgt', x.objetivo))}</span>` : ''}`;
}
/** Cómo funciona: una entrada por efecto, plegada, con su destino. Abiertas: las del efecto tocado o, si
 *  son una o dos, todas. */
function tipComoHtml (v, es, foco) {
  if (!es.length) return `<p class="muted">${h(t('tt_vacia'))}</p>`;
  const abiertas = foco.length ? foco : es.length <= 2 ? es : [];
  return es.map(x => `<details class="tipef${foco.includes(x) ? ' foco' : ''}"${abiertas.includes(x) ? ' open' : ''}>
    <summary>${x.sc ? `<span class="annom">${h(t('an_sc'))}:</span> ${h(fila('ab', efectoDe(v, x.fuentes[0]).a).en)}`
      : `${nombreAnHtml(CATALOGO.efectos[x.ie])} ${destinoTipHtml(x)}${x.ns ? noSirveHtml(CATALOGO.efectos[x.ie]) : ''}`}</summary>
    ${x.sc ? `<p class="muted">${h(t('an_sc_t'))}</p>` : efectoTipHtml(v, x)}</details>`).join('');
}
/** Las lecturas de un efecto, con su certeza: [{ modo, L, grupo }], una sola si PvE y PvP dicen lo mismo. En el
 *  modo en que no trae lectura propia vale la de su grupo (grupo: su nombre; si no, null). */
function lecturasEfecto (e) {
  const g = CATALOGO.grupos.find(y => y.id === e.grupo);
  const [pve, pvp] = ['pve', 'pvp'].map(m => ({ L: e[m] || g[m], grupo: e[m] ? null : bi(g) }));
  return JSON.stringify(pve) === JSON.stringify(pvp) ? [{ modo: t('an_pve_pvp'), ...pve }] : [{ modo: 'PvE', ...pve }, { modo: 'PvP', ...pvp }];
}
function delGrupo (x) { return x.grupo ? ' ' + t('tt_del_grupo').replace('{x}', x.grupo) : ''; }
/** Una entrada de «Cómo funciona», abierta: qué es (su grupo y, si lo tiene, el término del glosario del
 *  juego), contra qué, a quién le sirve, las notas del catálogo (del efecto y de la etiqueta de la skill) y
 *  sus lecturas de PvE y de PvP, con su certeza. */
function efectoTipHtml (v, x) {
  const e = CATALOGO.efectos[x.ie], g = CATALOGO.grupos.find(y => y.id === e.grupo), cond = condicionAn(v, x.fuentes);
  const notas = [...new Set([e.nota, ...x.fuentes.map(s => CATALOGO.skills[fila('ab', efectoDe(v, s).a).en].nota)].filter(Boolean))];
  return `<ul class="tiplista">
      <li><b>${h(t('tt_grupo'))} ${h(bi(g))}:</b> ${h(bi(g.que))}</li>
      ${GL_DE[e.id].terminos.map(y => `<li><b>${h(nombreGl(y))}</b> <span class="muted">(${h(otrosNombresGl(y).join(', '))})</span>: ${h(bi(y.que))}</li>`).join('')}
      ${cond ? `<li>${h(mayuscula(cond))}</li>` : ''}
      ${leSirveEfectoHtml(e, (r, x) => `<li><b>${r}</b> ${x}</li>`)}
      ${acumulaEfectoHtml(e, (r, x) => `<li><b>${r}</b> ${x}</li>`)}
      ${topeEfectoHtml(e, (r, x) => `<li><b>${r}</b> ${x}</li>`)}
      ${notas.map(n => `<li class="muted">${h(bi(n))}</li>`).join('')}
    </ul>
    ${lecturasEfecto(e).map(l => lecturaAn(l.L, l.modo + delGrupo(l))).join('')}`;
}
/** Cuándo, cuánto y a quién: la activación, la recarga y la carga de la skill; por etapa, su activación y su
 *  objetivo si cambian, y cada efecto con su texto (los números), lo que la fuente dice aparte (duración,
 *  intervalo, persistente, de equipo) y a quién le llega según el análisis. Al final, plegado, lo que dice
 *  Leads & Supports de la misma skill. */
function tipCuandoHtml (v, sk, es, ti, fi) {
  const acComun = comunEnEtapas(sk, 'ac'), tgComun = comunEnEtapas(sk, 'tg'), sinAc = sk.st.every(st => st.ac == null);
  const activacion = acComun != null ? txt('act', acComun, sk.st.find(st => st.ac === acComun).av)
    : sinAc ? t(/^Active/.test(sk.sl) ? 'tt_al_usar' : 'tt_sin_cond') : null;
  const carga = [sk.ult != null ? t('c_ult') + ' ' + numTxt(sk.ult) + '%' : '', sk.stk != null ? t('c_striker') + ' ' + numTxt(sk.stk) + '%' : '']
    .filter(Boolean).join(', ');
  const dato = (k, val) => `<li><b>${h(t(k))}:</b> ${h(val)}</li>`;
  // El golpe no lleva a quién: siempre es contra el rival, como dice «Cómo funciona».
  const linea = (f, i, j) => {
    const { renglones, sinTraducir } = renglonesEfecto(f);
    const ds = esDano(f) ? [] : [...new Set(es.filter(x => !x.sc && tocaEfecto(x, i, j)).map(x => x.d))];
    return `<li class="tipfx${i === ti && j === fi ? ' foco' : ''}"><span${sinTraducir ? ` class="sintrad" title="${h(t('untranslated'))}"` : ''}>${renglones.join(' ')}</span>${
      metaEfecto(f, true).map(m => ` <span class="dur">${h(m)}</span>`).join('')}${ds.map(d => ` <span class="tag tipd ${d}">${h(t('an_' + d))}</span>`).join('')}</li>`;
  };
  const etapas = sk.st.map((st, i) => {
    const ls = [];
    if (acComun == null && !sinAc) ls.push(dato('st_activation', st.ac != null ? txt('act', st.ac, st.av) : t('tt_etapa_sin_ac')));
    if (tgComun == null && st.tg != null) ls.push(dato('st_target', txt('tgt', st.tg)));
    st.fx.forEach((f, j) => ls.push(linea(f, i, j)));
    if (!st.fx.length) ls.push(`<li class="muted">${h(t('tt_etapa_vacia'))}</li>`);
    const lista = `<ul class="tiplista">${ls.join('')}</ul>`;
    return sk.st.length > 1 ? `<div class="tipetapa"><div class="tipeh">${h(t('st_stage'))} ${i + 1}</div>${lista}</div>` : lista;
  }).join('');
  const ls = soportesDeSkill(v, sk);
  return `<ul class="tiplista">
      ${activacion != null ? dato('st_activation', activacion) : ''}
      ${dato('tt_recarga', recargaTxt(v, sk))}
      ${carga ? dato('tt_carga', carga) : ''}
      ${tgComun != null ? dato('st_target', txt('tgt', tgComun)) : ''}
    </ul>
    ${sk.st.some(st => st.fx.length) ? etapas : `<p class="muted">${h(t('tt_vacia'))}</p>`}
    ${ls.length ? `<details class="tipls"><summary>${h(t(rotuloLs(ls.map(([k]) => SOPORTES[v.p][k]))))}</summary>
      <div class="sops">${ls.map(([k, clave]) => soporteHtml(k, clave, SOPORTES[v.p][k])).join('')}</div></details>` : ''}`;
}
/** El texto del juego, plegado: tal como lo publica thanosvibs y con la traducción de la app (el nombre y,
 *  por etapa, la activación, el objetivo y cada efecto). El coreano: los datos no lo traen para las skills,
 *  solo para los términos del glosario. */
function tipTextoHtml (sk, terminos) {
  const marca = (sinTraducir, html) => sinTraducir ? `<span class="sintrad" title="${h(t('untranslated'))}">${html}</span>` : html;
  const enIdioma = (lang) => {
    const nom = texto('name', sk.n, null, lang);
    if (!sk.st.some(st => st.fx.length)) return `<p class="tipnom">${marca(nom.sinTraducir, h(nom.txt))}</p><p class="muted">${h(t('tt_vacia'))}</p>`;
    return `<p class="tipnom">${marca(nom.sinTraducir, h(nom.txt))}</p>` + sk.st.map((st, i) => {
      const ls = [];
      if (st.ac != null) { const r = texto('act', st.ac, st.av, lang); ls.push(`<li><b>${h(t('st_activation'))}:</b> ${marca(r.sinTraducir, h(r.txt))}</li>`); }
      if (st.tg != null) { const r = texto('tgt', st.tg, null, lang); ls.push(`<li><b>${h(t('st_target'))}:</b> ${marca(r.sinTraducir, h(r.txt.replace(BARRA_N, ' · ')))}</li>`); }
      for (const f of st.fx) { const r = renglonesEfecto(f, lang); ls.push(`<li>${marca(r.sinTraducir, r.renglones.join(' '))}</li>`); }
      return (sk.st.length > 1 ? `<div class="tipeh">${h(t('st_stage'))} ${i + 1}</div>` : '') + (ls.length ? `<ul class="tiplista">${ls.join('')}</ul>` : '');
    }).join('');
  };
  return `<details class="tiptx"><summary>${h(t('tt_en'))}</summary>${enIdioma('en')}</details>
    <details class="tiptx"><summary>${h(t('tt_es'))}</summary>${enIdioma('es')}</details>
    <p class="muted">${h(t('tt_ko_no'))}</p>
    ${terminos.length ? `<p class="muted">${h(t('tt_ko_terminos'))}</p><ul class="tiplista">${terminos.map(y => `<li>${h(nombreGl(y))}: <span lang="ko">${h(y.ko)}</span>${
      y.falta ? ` <span class="tag dim">${h(t('gl_falta_' + y.falta))}</span>` : ''}</li>`).join('')}</ul>` : `<p class="muted">${h(t('tt_ko_sin'))}</p>`}`;
}
/** Certeza y fuentes: el texto es de thanosvibs; la traducción, de la app; lo que completó un marcador, de su
 *  origen; qué efecto es cada uno y a quién le llega, del catálogo y el análisis (los datos no traen una
 *  certeza para eso); las lecturas, con la certeza del catálogo; y las fuentes del glosario y de Leads &
 *  Supports. */
function tipCertezaHtml (v, sk, es, terminos) {
  const fxs = sk.st.flatMap(st => st.fx);
  const sinTrad = [fila('name', sk.n), ...sk.st.flatMap(st => [fila('act', st.ac), fila('tgt', st.tg)]), ...fxs.map(f => fila('desc', f.p))]
    .filter(r => r && r.es == null).length;
  const marcas = [...new Map(fxs.filter(f => fila('desc', f.p).en.includes('$HERO')).map(f => [f.g + '|' + f.gs, f])).values()];
  // Las lecturas, solo con su certeza (el texto y la fuente de cada una están en «Cómo funciona»); PvE y PvP
  // van juntas si tienen la misma certeza y salen del mismo lado (propia o del grupo).
  const lecturas = [...new Set(es.filter(x => !x.sc).map(x => CATALOGO.efectos[x.ie]))];
  const certezas = (e) => { const ls = lecturasEfecto(e);
    const juntas = ls.length === 2 && ls[0].L.certeza === ls[1].L.certeza && ls[0].grupo === ls[1].grupo ? [{ ...ls[0], modo: t('an_pve_pvp') }] : ls;
    return juntas.map(l => `${h(l.modo)} ${certHtml(l.L.certeza)}${l.grupo ? `<span class="muted">${h(delGrupo(l))}</span>` : ''}`).join(', '); };
  return `<ul class="tiplista">
    <li>${h(t('tt_f_texto'))} ${certHtml('comprobado')} ${fuentesHtml(['tv-pj'])}</li>
    <li>${h(t('tt_f_trad'))}${sinTrad ? ' ' + h(t('tt_f_sintrad').replace('{n}', sinTrad)) : ''}</li>
    ${marcas.map(f => `<li><b>${h(f.g ? dom(f.g) : t('tpl_unspec'))}:</b> ${h(t(f.g ? ORIGEN_MARCADOR[f.gs] : 'tpl_pending'))}${
      f.gs === 'l' ? ' ' + fuentesHtml(['tv-sup']) : ''}</li>`).join('')}
    ${es.length ? `<li>${h(t('tt_f_analisis'))}</li>` : ''}
    ${lecturas.length ? `<li>${h(t('tt_f_lecturas'))} ${fuentesHtml([...new Set(lecturas.flatMap(e => lecturasEfecto(e).flatMap(l => l.L.fuente || [])))])}
      <ul>${lecturas.map(e => `<li>${h(nombreAnTxt(e))}: ${certezas(e)}</li>`).join('')}</ul></li>` : ''}
    ${terminos.length ? `<li>${h(t('tt_f_glosario'))}: ${fuentesHtml([...new Set(terminos.flatMap(y => y.fuente))])}</li>` : ''}
    ${soportesDeSkill(v, sk).length ? (xs => `<li>${h(t(rotuloLs(xs)))}: ${fuentesHtml(fuentesSop(xs))}</li>`)(soportesDeSkill(v, sk).map(([k]) => SOPORTES[v.p][k])) : ''}
  </ul>`;
}
/** Lo que el inglés traduce distinto del coreano en los términos del glosario de sus efectos, y los errores
 *  del inglés que se repiten, plegados. */
function tipCoreanoHtml (terminos) {
  const difieren = terminos.filter(y => y.difiere);
  if (!difieren.length) return `<p class="muted">${h(t(terminos.length ? 'tt_dif_nada' : 'tt_dif_sin'))}</p>`;
  const errores = GLOSARIO.errores.filter(e => difieren.some(y => y.error === e.id));
  return `<ul class="tiplista">${difieren.map(y => `<li><b>${h(nombreGl(y))}</b> <span class="muted" lang="ko">${h(y.ko)}</span>: ${h(bi(y.difiere))}</li>`).join('')}</ul>
    ${errores.length ? `<div class="tipeh">${h(t('gl_errores'))}</div>${errores.map(e =>
      `<details class="tiperr"><summary>${h(bi(e.titulo))}</summary><p>${h(bi(e.texto))}</p></details>`).join('')}` : ''}`;
}
/** ¿El «Cómo funciona» abierto sigue siendo de lo que se ve (la pestaña Skills de la misma variante)? */
function tipVigente () {
  const v = ui.view === 'detail' && ui.fichaTab === 'skills' ? variant(ui.charId, ui.uniformId) : null;
  return !!v && v.key === ui.tip.key;
}
/** El «Cómo funciona» abierto (ui.tip), o nada. Va al final de #app, fuera de main, como las ventanas. */
function tipHtml () {
  if (!ui.tip) return '';
  const v = variant(ui.charId, ui.uniformId), { si, ti, fi } = ui.tip, sk = v.skills[si];
  if (!sk) throw new Error(`${fullLabel(v)} no tiene la skill ${si}`);
  const es = entradasSkill(v, si), terminos = terminosSkill(es), foco = ti == null ? [] : es.filter(x => tocaEfecto(x, ti, fi));
  const seccion = (k, cuerpo) => `<section class="tipsec" data-sec="${k}"><h4>${h(t('tt_' + k))}</h4>${cuerpo}</section>`;
  return `<div class="skpop-fondo" id="skpop-fondo"></div>
    <div class="skpop" id="skpop" role="dialog" aria-modal="true" aria-labelledby="skpop-t" tabindex="-1">
      <div class="tiphead">
        <div class="tiptit" id="skpop-t"><span class="slotbadge ${slotClase(sk.sl)}">${h(slotEs(sk.sl))}</span>${nombreSkill(sk)}</div>
        <button class="btn icon" data-a="tipCerrar" title="${h(t('tt_cerrar'))}" aria-label="${h(t('tt_cerrar'))}">✕</button>
      </div>
      <div class="muted tipsub">${h(fullLabel(v))}</div>
      ${seccion('como', tipComoHtml(v, es, foco))}
      ${seccion('cuando', tipCuandoHtml(v, sk, es, ti, fi))}
      ${seccion('texto', tipTextoHtml(sk, terminos))}
      ${seccion('certeza', tipCertezaHtml(v, sk, es, terminos))}
      ${seccion('coreano', tipCoreanoHtml(terminos))}
    </div>`;
}
/** Abre el «Cómo funciona» de la skill si (en el efecto fi de la etapa ti, si se tocó un renglón), lo ubica,
 *  le pasa el foco y, si se abrió en un efecto, lo lleva a la vista. */
function abrirTip (si, ti, fi) {
  ui.tip = { key: variant(ui.charId, ui.uniformId).key, si, ti, fi };
  $('#app').insertAdjacentHTML('beforeend', tipHtml());
  const b = document.getElementById('skt-' + si);
  b.setAttribute('aria-expanded', 'true'); b.setAttribute('aria-controls', 'skpop');
  posicionarTip();
  const pop = document.getElementById('skpop'), foco = pop.querySelector('.tipef.foco');
  pop.focus({ preventScroll: true });
  if (foco) pop.scrollTop = foco.offsetTop - pop.querySelector('.tiphead').offsetHeight - 8;
}
/** Lo cierra; con devolverFoco, el foco vuelve a la skill, sin mover la página. */
function cerrarTip (devolverFoco) {
  const b = document.getElementById('skt-' + ui.tip.si);
  ui.tip = null;
  document.getElementById('skpop').remove(); document.getElementById('skpop-fondo').remove();
  b.setAttribute('aria-expanded', 'false'); b.removeAttribute('aria-controls');
  if (devolverFoco) b.focus({ preventScroll: true });
}
/** En la compu va debajo de lo tocado; si ahí no entra, encima; si tampoco, del lado con más lugar. Su alto
 *  no pasa del lugar de ese lado: lo que se despliega adentro se recorre adentro. Encima, crece hacia arriba.
 *  Va en coordenadas de la página: se mueve con ella y pasa por debajo de la cabecera fija. En el celular es
 *  una hoja inferior y la ubica styles.css. */
function posicionarTip () {
  const pop = document.getElementById('skpop'), { si, ti, fi } = ui.tip;
  Object.assign(pop.style, { top: '', bottom: '', left: '', maxHeight: '' });
  if (matchMedia(TIP_CELULAR).matches) return;
  const ancla = ti == null ? document.getElementById('skt-' + si).closest('.top')
    : document.querySelector(`.skill [data-a="skTip"][data-si="${si}"][data-st="${ti}"][data-fx="${fi}"]`);
  const r = ancla.getBoundingClientRect(), techo = document.querySelector('.fcab').getBoundingClientRect().bottom;
  const debajo = innerHeight - r.bottom - 12, encima = r.top - techo - 12, abajo = pop.offsetHeight <= debajo || debajo >= encima;
  pop.style.maxHeight = Math.min(parseFloat(getComputedStyle(pop).maxHeight), Math.max(240, abajo ? debajo : encima)) + 'px';
  // Sin un contenedor ubicado, top y bottom se miden desde el bloque inicial (el alto de la ventana desde arriba de la página).
  if (abajo) pop.style.top = r.bottom + 6 + scrollY + 'px';
  else pop.style.bottom = document.documentElement.clientHeight - (r.top - 6 + scrollY) + 'px';
  pop.style.left = Math.max(16, Math.min(r.left, document.documentElement.clientWidth - pop.offsetWidth - 16)) + scrollX + 'px';
}
/** Tab y Shift+Tab dan la vuelta adentro del «Cómo funciona»: el foco no se va a la página de atrás. */
function atraparFoco (e) {
  const pop = document.getElementById('skpop');
  const fs = [...pop.querySelectorAll('button, a[href], summary')].filter(x => x.getClientRects().length);
  const a = document.activeElement, primero = fs[0], ultimo = fs[fs.length - 1];
  if (e.shiftKey ? (a === primero || a === pop || !pop.contains(a)) : (a === ultimo || !pop.contains(a))) {
    e.preventDefault(); (e.shiftKey ? ultimo : primero).focus();
  }
}
/** Cómo armarlo: lo que las fuentes le asignan al personaje; las reglas generales de su
 *  tipo de ataque (iguales para todos) van plegadas. Los bloques van en dos columnas que se reparten la altura
 *  (Ezequiel, 6 de octubre de 2026: sin el espacio en blanco que dejaba una grilla de filas parejas). */
function fichaArmado (ch, v) {
  const ta = tipoAtaque(v);
  return `<div class="section"><h3>${h(t('ar_title'))} ${ayudaHtml(t('ar_note'))}</h3>
    <p class="muted" style="margin-bottom:12px"><a href="#armado" data-a="irArmadoModos">${h(t('ar_more'))}</a></p>
    <div class="armado2">
      <div class="bloque"><h4>C.T.P.</h4>${armadoCTP(ch, v)}</div>
      <div class="bloque" id="artefacto"><h4>${h(t('ar_art'))}</h4>${armadoArtefacto(ch)}${artArmado(ch)}</div>
      <div class="bloque"><h4>${h(t('ga_iso_title'))}</h4>${isoArmado(ch, v)}</div>
      <div class="bloque"><h4>${h(t('md_uni_opts'))}</h4>${armadoOpciones(v)}</div>
    </div>
    <details class="reglas"><summary>${h(t('ar_rules'))}</summary>
      <div class="armado2">
        <div class="bloque"><h4>ISO-8</h4>${armadoISO(ta)}</div>
        <div class="bloque"><h4>${h(t('md_urus'))}</h4>${armadoUrus(ta)}</div>
      </div></details></div>
  ${fichaProgreso(ch, v)}`;
}
/** Tu avance con el personaje: hoja de ruta y topes de stats (se guardan en la capa). */
function fichaProgreso (ch, v) {
  return `<div class="section"><h3>${h(t('ft_progreso'))}</h3>
    <div class="usogrid par">
      <div class="bloque"><h4>${h(t('ru_title'))}</h4>${armadoRuta(ch, v)}</div>
      <div class="bloque"><h4>${h(t('cap_title'))}</h4>${armadoTopes(ch)}</div>
    </div></div>`;
}
/** Abre el armador con estos integrantes, para guardarlo como equipo de tu cuenta. */
function botonArmar (vs, modo, nombre, etiqueta) {
  return `<button class="btn sm" data-a="teamDesde" data-m="${vs.map(x => x.key).join(',')}"
    data-modo="${modo || ''}" data-nombre="${h(nombre || '')}">${h(etiqueta || t('eq_build'))}</button>`;
}
// «POR QUÉ» DE UNA TARJETA DE EQUIPO (combinaciones de 3 y «Cómo entraría en tus otros equipos»), EN UNA VENTANA
// (Ezequiel, 4 de octubre de 2026: «Esto se tiene que poder ver más prolijo y legible... El desglose, podés ponerlo
// en un modal, con los retratos para cada personaje»). La tarjeta tiene un botón donde antes se desplegaba; la
// ventana (un <dialog> fuera de #app: pintar la página no la toca) tiene arriba el equipo (los retratos, con el
// líder primero y su marca, los puntos de la tarjeta y quién lidera y por qué) y de dónde salen los puntos, parte
// por parte (en PvP y PvE, el detalle del contexto; si no, la sinergia); después, una pestaña por integrante con lo
// que recibe (un renglón por stat y condición, con el total de lo que se le aplica, el tope de la guía si el stat
// tiene, y de dónde sale cada parte: quién la da, el enlace a la skill o al artefacto y lo que suma) y lo que
// aporta; abajo, lo demás (en PvP y PvE, lo de los puntos para él; en «cómo entraría», lo que se gana y lo que se
// pierde) y los C.T.P. recomendados en el contexto de la tarjeta. Son las cuentas de siempre (recibe, enContexto,
// synergy, ctpRecomendado), las mismas de la tarjeta. Con los nombres cortos (el completo, en el title) y «a todos»
// si algo les llega a todos. Cada efecto, con efectoSoporteHtml.
/** Cómo se nombra a cada integrante: el personaje, sin uniforme, si en el equipo no hay otro con el
 *  mismo nombre; si no, el nombre completo. */
function nombreEn (vs) { return (x) => vs.some(y => y !== x && y.name === x.name) ? fullLabel(x) : x.name; }
function nombreHtml (x, nombre) { return `<span title="${h(fullLabel(x))}">${h(nombre(x))}</span>`; }
/** A quiénes les llega algo: «a todos» si les llega a todos los del equipo; si no, sus nombres. */
function aQuienesHtml (ms, vs, nombre) { return ms.length === vs.length ? h(t('pq_todos')) : ms.map(x => nombreHtml(x, nombre)).join(', '); }
/** Lo que le llega al foco, por origen, en el orden en que se aplica (ver «Efectos iguales que no se suman»): lo
 *  suyo, el líder (su liderazgo y sus soportes) y los demás en el orden del equipo; al final, el artefacto de cada
 *  uno. [{ de, art, skills: [lo de recibe(), con no: los efectos que no se le suman → la fuente que ya se los da] }] */
function origenesDe (foco, vs, lider) {
  const pjs = [], arts = [];
  for (const a of [foco].concat(ordenEquipo(vs, lider).filter(x => x !== foco))) {
    const rs = recibe(foco, a, a === lider).map(r => Object.assign(r, { no: new Map(aplicacion(foco, r.de, r.k, r.x, r.fx, vs, lider).no) }));
    const sin = rs.filter(r => r.k !== 'artifact'), con = rs.filter(r => r.k === 'artifact');
    if (sin.length) pjs.push({ de: a, art: false, skills: sin });
    if (con.length) arts.push({ de: a, art: true, skills: con });
  }
  return pjs.concat(arts);
}
/** La suma de lo que le llega: un renglón por stat y condición (los que llegan siempre primero). De cada uno, lo que
 *  se le aplica sin artefacto y lo que solo con uno: v y i (% del instinto), [sin, con], null si de ese lado no se le
 *  aplica nada con número; sin: si algo de lo que se le aplica le llega sin artefacto; de: de dónde sale cada parte, en el
 *  orden de los orígenes ({ o: el origen, r: lo de recibe(), f: el efecto, ya: la fuente que se le aplica en su lugar, si
 *  esta no se le suma }); rep: si no se le suma ninguna parte. Una habilidad que le llega de dos fuentes va en las dos
 *  partes, pero en el total solo la que se le aplica (Efectos iguales). */
function sumaDe (origenes) {
  const m = new Map();
  for (const o of origenes) for (const r of o.skills) for (const f of r.fx) {
    const cond = condicionTxt(r.x, f), txt = typeof f.v === 'string' ? f.v : null, clave = f.s + '|' + cond + '|' + (txt || '');
    let l = m.get(clave);
    if (!l) m.set(clave, l = { s: f.s, cond, txt, v: [null, null], i: [null, null], sin: false, de: [], rep: true });
    const j = o.art ? 1 : 0, ya = r.no.get(f) || null;
    if (!ya) {
      if (typeof f.v === 'number') l.v[j] = (l.v[j] || 0) + f.v;
      if (f.i != null) l.i[j] = (l.i[j] || 0) + f.i;
      if (!o.art) l.sin = true;
      l.rep = false;
    }
    l.de.push({ o, r, f, ya });
  }
  return [...m.values()].sort((a, b) => !!a.cond - !!b.cond);
}
/** ¿El renglón lleva «*» (algo de lo que se le aplica solo llega con un artefacto)? Con número, si un artefacto le suma;
 *  sin número, si solo se le aplica por artefactos. Si no se le aplica nada, no. */
function conArtefacto (l) { return !l.rep && (l.v[1] != null || l.i[1] != null || (!l.sin && l.v[0] == null && l.i[0] == null)); }
/** El «*» de lo que solo llega si el compañero lleva su artefacto. */
function marcaArt () { return `<span class="pqart" title="${h(t('cb_art'))}">*</span>`; }
// TOPES (Ezequiel, 5 de octubre de 2026: «Hay algunas estadsiticas que llegana tope, indice critico, daño critico,
// esquiva»). El tope de cada stat lo dice la guía (MFF_GUIA.topes, con su fuente), y qué stat de liderazgo, soporte o bono
// de equipo lo tiene, el catálogo (MFF_CATALOGO.soporte, tope: claves de la guía); acá no hay ningún número. Lo muestran
// la tabla de lo que recibe cada integrante (con el aviso si lo que suman los buffs pasa lo que queda hasta el tope: el
// tope menos la base, si el stat arranca en una), el Glosario y «Cómo funciona».
/** Los topes de un stat de liderazgo, soporte o bono: [{ k: la clave de la guía, tope, base (0 si no arranca en una) }],
 *  vacío si no tiene. */
function topesDe (s) {
  const c = CATALOGO.soporte[s];
  if (!c || !c.tope) return [];
  return c.tope.map(k => {
    const it = GUIA.topes.items.find(y => y.stats.includes(k) && y.tope != null);
    if (!it) throw new Error(`el tope ${k} de ${s} no está en la guía (MFF_GUIA.topes)`);
    return { k, tope: it.tope, base: it.base || 0 };
  });
}
/** Un tope, para leerlo: «75%» o «130% (desde 100%)»; con el nombre del stat de la guía si conNombre. */
function topeTxt (x, conNombre) {
  return (conNombre ? statNom(x.k) + ' ' : '') + (x.base ? t('pq_tope_base').replace('{n}', numTxt(x.tope)).replace('{b}', numTxt(x.base)) : numTxt(x.tope) + '%');
}
/** El tope de un renglón de lo que recibe (sumaDe), si su stat tiene: el tope, con la fuente de la guía y, si lo que suman los
 *  buffs que se le aplican pasa lo que queda hasta el tope, el aviso de que lo de más no suma. Un renglón con condición se
 *  cuenta con lo que le llega siempre del mismo stat (siempre: el total de su renglón sin condición). Cuenta el valor
 *  absoluto: la recarga se escribe en negativo. */
function topeFilaHtml (l, siempre) {
  const ts = topesDe(l.s);
  if (!ts.length) return '';
  const total = l.v[0] == null && l.v[1] == null ? null : (l.v[0] || 0) + (l.v[1] || 0);
  const suma = total == null ? null : Math.abs(total + (l.cond ? siempre : 0)), queda = Math.min(...ts.map(x => x.tope - x.base));
  return `<div class="muted pqtope" title="${h(t('pq_tope_t'))}">${h(t('pq_tope').replace('{t}', ts.map(x => topeTxt(x, ts.length > 1)).join(', ')))} ${
    fuentesHtml(GUIA.topes.fuente)}</div>${suma != null && suma > queda ? `<div class="pqpasa">${h(t(l.cond && siempre ? 'pq_tope_pasa_cond' : 'pq_tope_pasa')
      .replace('{x}', numTxt(suma)).replace('{r}', numTxt(queda)))}</div>` : ''}`;
}
/** Lo que recibe el integrante m, en una tabla «Efecto | Total | De dónde»: un renglón por stat y condición (sumaDe), con
 *  la leyenda del «*» si algún renglón la lleva. hid: el id del título que la nombra. */
function recibeTablaHtml (m, suma, nombre, hid) {
  // De cada stat, lo que le llega siempre (su renglón sin condición): con eso se cuenta el tope de un renglón con condición.
  const siempre = new Map(suma.filter(l => !l.cond).map(l => [l.s, (l.v[0] || 0) + (l.v[1] || 0)]));
  return `<div class="pqm-tabla" role="table" aria-labelledby="${hid}">
      <div class="pqm-fila pqm-th" role="row"><span role="columnheader">${h(t('pq_col_efecto'))}</span><span role="columnheader">${
        h(t('pq_col_total'))}</span><span role="columnheader">${h(t('pq_col_de'))}</span></div>
      ${suma.map(l => recibeFilaHtml(m, l, nombre, siempre.get(l.s) || 0)).join('')}
    </div>${suma.some(conArtefacto) ? `<p class="muted pqley">${h(t('cb_art'))}</p>` : ''}`;
}
/** Un renglón de la tabla: el efecto (con su condición, que es la de todas sus partes), el total de lo que se le aplica
 *  (con «*» si algo de él solo llega con un artefacto y, si también llega algo sin artefacto, cuánto) y de dónde sale cada
 *  parte: quién la da (su retrato y su nombre), el enlace a su skill o a su artefacto y lo que suma. La parte que no se le
 *  suma (una habilidad que se le aplica de otra fuente: Efectos iguales) va atenuada, con de dónde la tiene; si no se le
 *  suma ninguna, el renglón entero. Si el stat tiene tope, debajo del efecto (topeFilaHtml; siempre: lo que le llega sin
 *  condición del mismo stat). */
function recibeFilaHtml (m, l, nombre, siempre) {
  const tot = (p) => p[0] == null && p[1] == null ? null : (p[0] || 0) + (p[1] || 0);
  const art = conArtefacto(l), val = l.rep ? '' : valorTxt(l.txt != null ? l.txt : tot(l.v), tot(l.i));
  const sin = art && (l.v[0] != null || l.i[0] != null) ? valorTxt(l.v[0], l.i[0]) : '';
  return `<div class="pqm-fila${l.rep ? ' rep' : ''}" role="row">
      <div class="pqm-ef" role="cell">${trHtml(l.s)}${sinClasificar(l.s) ? ` <span class="muted">(${h(t('sy_unclassified'))})</span>` : ''}${
        l.cond ? ` <div class="muted pqm-cond">(${h(l.cond)})</div>` : ''}${topeFilaHtml(l, siempre)}</div>
      <div class="pqm-tot" role="cell">${val ? `<b>${h(val)}</b>` : ''}${art ? marcaArt() : ''}${
        sin ? ` <div class="muted">(${h(t('pq_sin_art').replace('{x}', sin))})</div>` : ''}</div>
      <div class="pqm-de" role="cell">${l.de.map(({ o, r, f, ya }) => { const v = valorTxt(f.v, f.i);
        return `<span class="pqm-de1${ya ? ' rep' : ''}"><span class="shot" aria-hidden="true">${shot(r.de.id)}</span><span>${nombreHtml(r.de, nombre)}: ${
          enlaceSkill(r)}${v ? ` <b>${h(v)}</b>` : ''}${o.art ? marcaArt() : ''}${ya ? ' ' + noSumaHtml(m, ya, nombre) : ''}</span></span>`; }).join('')}</div>
    </div>`;
}
// Slot de Leads & Supports -> tipo de la skill que lo da en la ficha.
const SKILL_DE_SLOT = { leader: 'Leader Skill', leader2: 'Leader Skill', passive: 'Passive', passive2: 'Passive',
  t2: 'Tier-2 Passive', t22: 'Tier-2 Passive', uniform: 'Uniform Passive', uniform2: 'Uniform Passive' };
/** La skill de la ficha de v que da su soporte o liderazgo k. Un liderazgo es la Leader Skill. Un
 *  soporte, la skill con el nombre que le da Leads & Supports, que a veces es de otro tipo (la «Pasiva
 *  4★ (secundaria)» de Jeff the Land Shark es su Activa 5, Jeff's Cuddle Buddy); si ninguna lo lleva
 *  (no tiene nombre, o lo escribe distinto), la de su tipo. null si la ficha no la tiene. */
function skillDeSoporte (v, k, x) {
  const nombre = (sk) => { const f = fila('name', sk.n); return f ? f.en : null; };
  const porNombre = !LIDERAZGOS.includes(k) && x.n ? v.skills.find(sk => nombre(sk) === x.n) : null;
  return porNombre || v.skills.find(sk => sk.sl === SKILL_DE_SLOT[k]) || null;
}
/** Ancla de una skill en la pestaña Skills de la ficha: hay una por tipo. */
function anclaSkill (sl) { return 'sk-' + slugId(sl); }
/** Enlace a la skill (o al artefacto) que da un soporte o un liderazgo, en la ficha de quien lo da, con
 *  su uniforme: la abre en la pestaña donde se ve, la lleva a la vista y la resalta. */
function enlaceSkill ({ de, k, x }) {
  const rotulo = k === 'propio' ? slotEs(x.sk.sl) : t(CLAVE_SOPORTE[k]), sinSkill = `<span title="${h(t('pq_sin_skill'))}">${h(rotulo)}</span>`;
  let tab, ancla, txt = rotulo, extra = '', titulo = t('pq_ver').replace('{x}', fullLabel(de));
  if (k === 'artifact') {
    const art = ARTES.find(y => y.p === de.ch.p);
    if (!art) return sinSkill;
    tab = 'armado'; ancla = 'artefacto'; txt = art.name; titulo += ': ' + art.name + ' · ' + art.pasiva;
    extra = x.est ? ` <span class="muted">(${h(t('sp_est').replace('{n}', x.est))})</span>` : '';
  } else {
    const sk = k === 'propio' ? x.sk : skillDeSoporte(de, k, x);
    if (!sk) return sinSkill;
    const f = fila('name', sk.n);
    tab = 'skills'; ancla = anclaSkill(sk.sl); titulo += ': ' + slotEs(sk.sl) + (f ? ' · ' + f.en : '');
  }
  return `<button class="objlink" data-a="irSkill" data-cid="${de.cid}" data-uid="${de.uid || ''}" data-tab="${tab}" data-ancla="${ancla}"
    title="${h(titulo)}">${h(txt)}</button>${extra}${srcHtml(x)}`;
}
/** Lo que da el foco a los demás (sus soportes y, si es el líder de la tarjeta, su liderazgo, según
 *  recibe()), como grupos de agrupar(): uno por slot, con a quiénes les llega cada efecto. */
function daGrupos (foco, vs, lider) {
  const gs = new Map();
  for (const b of vs) if (b !== foco) for (const r of recibe(b, foco, foco === lider)) {
    let g = gs.get(r.k);
    if (!g) gs.set(r.k, g = { r: { tipo: LIDERAZGOS.includes(r.k) ? 'liderazgo' : 'soporte', de: foco, k: r.k, x: r.x }, fx: new Map() });
    const no = new Map(aplicacion(b, foco, r.k, r.x, r.fx, vs, lider).no);
    for (const f of r.fx) {
      if (!g.fx.has(f)) g.fx.set(f, { si: [], no: [] });
      if (no.has(f)) g.fx.get(f).no.push([b, [[f, no.get(f)]]]); else g.fx.get(f).si.push(b);
    }
  }
  const orden = TIPOS_SOPORTE.map(([k]) => k);
  return [...gs.values()].sort((a, b) => orden.indexOf(a.r.k) - orden.indexOf(b.r.k));
}
/** Piezas (piezas()) en grupos: las de un efecto, por origen (un soporte o liderazgo de alguien, o una
 *  versión de un bono de equipo), con a quiénes les llega cada efecto; las demás razones, solas. */
function agrupar (ps) {
  const gs = new Map(), out = [];
  for (const p of ps) {
    if (!p.f) { out.push({ r: p.r }); continue; }
    let g = gs.get(p.r);
    if (!g) { gs.set(p.r, g = { r: p.r, fx: new Map() }); out.push(g); }
    if (!g.fx.has(p.f)) g.fx.set(p.f, { si: [], no: [] });
    g.fx.get(p.f).si.push(p.para);
  }
  return out;
}
/** Un grupo, para una viñeta: de dónde sale y, debajo, cada efecto con a quiénes les llega (en la cabecera, si les
 *  llega a los mismos). conEnlace: la cabecera es el enlace a la skill o al artefacto, sin el nombre de quien lo da (lo
 *  que aporta un integrante, en su pestaña). tras: lo que va después de la cabecera (lo que suma). */
function grupoHtml (g, vs, nombre, conEnlace, tras) {
  const { r } = g;
  if (!g.fx) { const txt = razonTxt(r, nombre), largo = razonTxt(r, fullLabel);
    return (largo !== txt ? `<span title="${h(largo)}">${h(txt)}</span>` : h(txt)) + (tras || ''); }
  const art = r.k === 'artifact' ? ` <span class="muted">(${h(t('pq_si_art'))})</span>` : '';
  const cab = r.tipo === 'bono' ? h(nombreBono(r)) : conEnlace ? enlaceSkill(r) + art
    : `${nombreHtml(r.de, nombre)}: ${h(t(CLAVE_SOPORTE[r.k]))}${art}${srcHtml(r.x)}`;
  // Cada efecto con a quiénes se les aplica (si) y, atenuado, a quiénes les llega y ya lo tienen de otra fuente (no).
  const efs = [...g.fx].sort((a, b) => r.x.fx.indexOf(a[0]) - r.x.fx.indexOf(b[0]));
  const quienes = (e) => e.si.map(x => x.key).join('|') + '/' + e.no.map(([x, [[, p]]]) => x.key + ':' + p.de.key + ':' + p.k).join('|');
  const iguales = efs.every(([, e]) => quienes(e) === quienes(efs[0][1]));
  const a = (e) => ` → ${aQuienesHtml(e.si, vs, nombre)}${yaLoTienenHtml(e.no, nombre)}`;
  return `${cab}${iguales ? a(efs[0][1]) : ''}${tras || ''}<ul>${efs.map(([f, e]) => `<li>${efectoSoporteHtml(r.x, f)}${iguales ? '' : a(e)}</li>`).join('')}</ul>`;
}
/** Grupos (agrupar, daGrupos) como lista. */
function gruposHtml (gs, vs, conEnlace) {
  const nombre = nombreEn(vs);
  return `<ul class="pqm-lista">${gs.map(g => `<li>${grupoHtml(g, vs, nombre, conEnlace)}</li>`).join('')}</ul>`;
}
// STRIKERS EN UN EQUIPO (Ezequiel, 4 de octubre de 2026: «suman, MUY poco... sería un sistema de desempate»). No
// suman puntos en ningún lado: a igual puntaje, desempatan (el orden de las combinaciones y el mejor lugar en «cómo
// entraría»), y cada tarjeta dice cuántos.
/** Los strikers de un equipo: [a, b, %, cuándo] por cada integrante b que es striker de otro a (de la pestaña
 *  Striker de la wiki). Con foco, solo los pares en que está él. */
function strikersDe (vs, foco) {
  const out = [];
  for (const a of vs) for (const [x, p, cuando] of STRIKERS[a.cid] || []) {
    const b = vs.find(y => y !== a && y.cid === x);
    if (b && (!foco || a === foco || b === foco)) out.push([a, b, p, cuando]);
  }
  return out;
}
/** Cuántos son (strikersDe), sin armarlos: la consulta de combinaciones lo pregunta cientos de miles de veces. */
function cuantosStrikers (vs, foco) {
  let n = 0;
  for (const a of vs) { const ss = STRIKER_SET[a.cid]; if (ss) for (const b of vs) if (b !== a && ss.has(b.cid) && (!foco || a === foco || b === foco)) n++; }
  return n;
}
/** Un striker del equipo, en texto: «Jeff de Adam Warlock (5% al atacar)». */
function strikerParHtml ([a, b, p, cuando], nombre) {
  return `${h(t('cx_striker_de')).replace('{b}', () => nombreHtml(b, nombre)).replace('{a}', () => nombreHtml(a, nombre))} (${strikerProbHtml(p, cuando)})`;
}
/** El desempate de una tarjeta: «desempate: 2 strikers», o nada si no tiene. */
function desempateHtml (n) { return n ? `<div class="muted desempate">${h(t(n === 1 ? 'cx_desempate_1' : 'cx_desempate').replace('{n}', n))}</div>` : ''; }
/** El rótulo del desempate, como parte de un puntaje: «Desempate: 2 strikers». */
function desempateRotulo (n) { return h(mayuscula(t(n === 1 ? 'cx_desempate_1' : 'cx_desempate').replace('{n}', n))); }
/** Los puntos de una combinación, como en su tarjeta: en PvP y PvE, los del contexto y, debajo, los de siempre (para él y
 *  del equipo), contados con el líder del contexto; si no, los puntos para él y los del equipo. stk: cuántos strikers
 *  desempatan (los del trío en PvP y PvE; si no, los de él). */
function ptsComboHtml (e, ctx, sc, equipo, stk) {
  return e ? `<div class="eqpts"><b>${numTxt(e.score)}</b>${artPts(e.art)} ${h(t('cx_pts_' + ctx))}
      <div class="muted">${h(t('cx_para_el')).replace('{a}', () => sc.score + artPts(sc.art)).replace('{b}', () => equipo.score + artPts(equipo.art))}</div>
      ${desempateHtml(stk)}</div>`
    : `<div class="eqpts"><b>${sc.score}</b>${artPts(sc.art)} ${h(t('eq_pts_for'))}
      <div class="muted">${h(t('eq_pts_team')).replace('{n}', () => equipo.score + artPts(equipo.art))}</div>
      ${desempateHtml(stk)}</div>`;
}
/** Los puntos de «cómo entraría» en un equipo (comoEntra), como en su tarjeta: la sinergia después, lo que gana y la de antes. */
function ptsEntraHtml (o) {
  return `<div class="eqpts"><b>${o.despues.score}</b>${artPts(o.despues.art)} ${h(t('tm_synergy_pts'))} <span class="eqdelta">+${o.delta}</span>
    <div class="muted">${h(t('eq_before')).replace('{n}', () => o.antes.score + artPts(o.antes.art))}</div>${desempateHtml(cuantosStrikers(o.vs, null))}</div>`;
}
/** Las partes de un puntaje, en la ventana del «Por qué»: cada una con su rótulo, lo que suma (si suma) y sus viñetas.
 *  partes: [[rótulo (HTML), puntos o null, [viñetas (HTML)], con el «*» de un artefacto]]. */
function partesHtml (partes) {
  return `<div class="pqm-partes">${partes.map(([k, pts, vi, art]) => `<div class="pqm-parte">
      <div class="pqm-parteh"><b>${k}</b>${pts != null ? ` <span class="pqm-pts">+${h(numTxt(pts))}${artPts(art)}</span>` : ''}</div>
      ${vi.length ? `<ul class="pqm-lista">${vi.map(x => `<li>${x}</li>`).join('')}</ul>` : ''}</div>`).join('')}</div>`;
}
/** De dónde salen los puntos de la sinergia (sc: synergy(), con sus razones; sin contexto y en «cómo entraría»): el
 *  liderazgo del líder, los soportes, los bonos de equipo y las lecturas propias (roles, clases y ventaja de clase), cada
 *  una con lo que suma (pts de cada razón) y sus viñetas, y los strikers (st: strikersDe), como desempate. Si las partes
 *  no dan el puntaje, es un error. */
function partesSinergia (sc, vs, st) {
  const nombre = nombreEn(vs), quien = (x) => nombreHtml(x, nombre), a = (ms) => aQuienesHtml(ms, vs, nombre);
  const de = (...tipos) => sc.razones.filter(r => tipos.includes(r.tipo)), suma = (rs) => rs.reduce((n, r) => n + r.pts, 0);
  const lid = de('liderazgo'), sop = de('soporte'), bonos = de('bono'), otras = de('roles', 'clases', 'ventaja'), partes = [];
  // Cada liderazgo y soporte con a quiénes se les aplica y, atenuado, a quiénes les llega algo que ya tienen (con 0 si es lo único).
  const pts = (r) => r.pts ? ptsHtml(r.pts) : `<span class="muted pqrep">· ${h(t('rep_nada'))}</span>`;
  if (lid.length) partes.push([h(t('cx_lider')).replace('{x}', () => quien(lid[0].de)), suma(lid),
    lid.map(r => `${enlaceSkill(r)} → ${a(r.a)}${yaLoTienenHtml(r.no, nombre)} ${pts(r)}`)]);
  if (sop.length) partes.push([h(t('pq_p_sop')), suma(sop), sop.map(r => `${quien(r.de)}: ${enlaceSkill(r)}${r.k === 'artifact' ? artPts(true) : ''} → ${
    a(r.a)}${yaLoTienenHtml(r.no, nombre)} ${pts(r)}`), sop.some(r => r.k === 'artifact' && r.pts)]);
  if (bonos.length) partes.push([h(t('pq_p_bonos')), suma(bonos), agrupar(piezas(bonos)).map(g => grupoHtml(g, vs, nombre, false, g.r.pts ? ' ' + ptsHtml(g.r.pts) : ''))]);
  if (otras.length) partes.push([h(t('pq_p_otras')), suma(otras), otras.map(r => grupoHtml({ r }, vs, nombre, false, ' ' + ptsHtml(r.pts)))]);
  const total = partes.reduce((n, p) => n + p[1], 0);
  if (total !== sc.score) throw new Error(`las partes de la sinergia suman ${total} y su puntaje es ${sc.score}`);
  if (st.length) partes.push([desempateRotulo(st.length), null, st.map(x => strikerParHtml(x, nombre))]);
  return partesHtml(partes);
}
/** Los integrantes como candidatos a liderar, con la cuenta de liderDe: { m, tiene (algún liderazgo), puede (en PvP, si
 *  con su liderazgo todos tienen anti-mermas), pts (lo que suma su liderazgo; null si no puede), puesto (el que desempata:
 *  en las tier lists del contexto o, sin contexto, en la General) }. */
function candidatosLider (vs, ctx) {
  if (!ctx) return vs.map(m => ({ m, tiene: !!SOPORTES[m.p] && LIDERAZGOS.some(k => SOPORTES[m.p][k]), puede: true,
                                  pts: ptsLiderSinContexto(m, vs), puesto: puestoSinContexto(m) }));
  const C = CONTEXTO[ctx], sl = vs.map(slotsDe), cub = cubiertos(vs, sl);
  return vs.map((m, i) => { const puede = puedeLiderar(vs, i, C, sl, cub);
    return { m, tiene: sl[i].lid.length > 0, puede, pts: puede ? ptsLiderazgo(vs, i, C, sl) : null, puesto: rolEn(m, ctx).puesto }; });
}
/** Quién lidera y por qué: lo que suma su liderazgo (en el contexto o en la sinergia), lo de los demás y, si empata, qué
 *  desempata (el puesto en las tier lists del contexto o en la General, y después un orden fijo). */
function porQueLideraHtml (vs, lider, ctx) {
  if (!lider) return `<p class="pqm-porque">${h(t('pq_sin_lider'))}</p>`;
  const nombre = nombreEn(vs), quien = (x) => nombreHtml(x, nombre), cs = candidatosLider(vs, ctx);
  const yo = cs.find(c => c.m === lider), otros = cs.filter(c => c !== yo), c = ctx ? t('ctp_ctx_' + ctx) : '';
  const lidera = (!yo.tiene ? h(t('pq_lidera_sin')) : h(t(ctx ? 'pq_lidera_ctx' : 'pq_lidera_sc')).replace('{p}', () => h(numTxt(yo.pts))))
    .replace('{x}', () => `<b>${quien(lider)}</b>`).replace('{c}', () => h(c));
  const cand = (x) => h(t(!x.tiene ? 'pq_cand_sin' : !x.puede ? 'pq_cand_anti' : 'pq_cand')).replace('{x}', () => quien(x.m))
    .replace('{p}', () => h(numTxt(x.pts)));
  const listas = h(ctx ? nombresListas(ctx === 'pvp' ? LISTAS_PVP : LISTAS_PVE) : listName(listById(LISTA_SIN_CONTEXTO)));
  const empatan = otros.filter(x => x.puede && x.pts === yo.pts), igual = empatan.filter(x => x.puesto === yo.puesto);
  const peor = empatan.filter(x => x.puesto !== yo.puesto), nombres = (xs) => xs.map(x => quien(x.m)).join(', ');
  return `<p class="pqm-porque">${lidera} ${h(t('pq_demas')).replace('{l}', () => otros.map(cand).join('; '))}${
    peor.length ? ' ' + h(t('pq_empate_puesto')).replace('{y}', () => nombres(peor)).replace('{l}', () => listas) : ''}${
    igual.length ? ' ' + h(t('pq_empate_orden')).replace('{y}', () => nombres(igual)).replace('{l}', () => listas) : ''}</p>`;
}
/** Qué tarjeta tiene abierta la ventana, en su id (el data-pq de su botón): 'c|contexto|claves' (una combinación de 3: el
 *  personaje de la ficha y los dos compañeros; el contexto, el del orden en que se abrió, o vacío) o 't|equipo|clave' (cómo
 *  entraría la variante en uno de tus equipos). Lo que muestra sale de nuevo de los datos, con las cuentas de la tarjeta:
 *  { v (el de la ficha), vs, lider, ctx, e (el puntaje de contexto), sc (la sinergia de la tarjeta), equipo, demas, o
 *  (comoEntra), ctp (el contexto de los C.T.P.), st (los strikers que desempatan) }. Una tarjeta cuyo equipo o cuyos
 *  personajes no están es un error: su botón solo se pinta con ellos. */
function pqDatos (id) {
  const [tipo, a, b] = id.split('|');
  if (tipo === 'c') {
    const ctx = a || null, vs = b.split(',').map(k => variant(...k.split('::')));
    if (vs.some(x => !x)) throw new Error('«Por qué» de una combinación con un personaje que no está: ' + id);
    const v = vs[0], e = ctx ? enContexto(vs, ctx, true) : null, lider = e ? e.lider : liderDe(vs, null);
    const sc = synergy(vs, { foco: v, lider });
    return { v, vs, lider, ctx, e, sc, equipo: synergy(vs, { soloPuntaje: true, lider }), ctp: ctx, st: strikersDe(vs, e ? null : v),
             demas: piezas(sc.razones).filter(p => !p.f || p.r.tipo === 'bono'), o: null };
  }
  if (tipo !== 't') throw new Error('tarjeta del «Por qué» desconocida: ' + id);
  const tt = U.teams.find(x => x.id === a), v = variant(...b.split('::'));
  if (!tt || !v) throw new Error('«Por qué» de «cómo entraría» con un equipo o un personaje que no está: ' + id);
  const o = comoEntra(v, tt);
  if (o.sinVinculo) throw new Error('«Por qué» de «cómo entraría» en un equipo con el que no tiene vínculo: ' + id);
  return { v, vs: o.vs, lider: o.despues.lider, ctx: null, e: null, sc: o.despues, ctp: o.ctp, st: strikersDe(o.vs, null), o };
}
/** El botón de una tarjeta que abre su «Por qué» (la ventana). id: de qué tarjeta es (pqDatos). */
function porqueBoton (id) {
  return `<button type="button" class="btn sm pqabrir" data-a="pqAbrir" data-pq="${h(id)}" aria-haspopup="dialog" title="${h(t('pq_abrir_t'))}">${
    h(t('pq_abrir'))}</button>`;
}
/** Un integrante, en su pestaña: quién es, lo que recibe (la tabla) y lo que aporta (daGrupos, con el enlace a cada skill). */
function integranteHtml (m, vs, lider, i, activo) {
  const nombre = nombreEn(vs), suma = sumaDe(origenesDe(m, vs, lider)), da = daGrupos(m, vs, lider);
  return `<div class="pqm-panel" role="tabpanel" id="pqm-p${i}" aria-labelledby="pqm-tab${i}" tabindex="0"${activo ? '' : ' hidden'}>
      <div class="pqm-quien"><b>${h(fullLabel(m))}</b>${m === lider ? ` <span class="pqm-pill">${h(t('eq_lider_pill'))}</span>` : ''}</div>
      <h4 id="pqm-r${i}">${h(t('pq_recibe').replace('{x}', nombre(m)))}</h4>
      ${suma.length ? recibeTablaHtml(m, suma, nombre, 'pqm-r' + i) : `<p class="muted">${h(t('pq_nada'))}</p>`}
      ${antiProbHtml([m], nombre).map(x => `<p class="muted pqprob">${x}</p>`).join('')}
      <h4>${h(t('pq_aporta').replace('{x}', nombre(m)))}</h4>
      ${da.length ? gruposHtml(da, vs, true) : `<p class="muted">${h(t('pq_aporta_nada'))}</p>`}
    </div>`;
}
/** La ventana del «Por qué» de una tarjeta (pq: { id, tab: la clave del integrante elegido }): la cabecera (con el botón de
 *  cerrar) y, debajo, el equipo y quién lidera, de dónde salen los puntos, una pestaña por integrante (el líder primero;
 *  arranca en el personaje de la ficha), lo demás y los C.T.P. */
function pqHtml (pq, d) {
  const { v, vs, lider, ctx, o } = d, nombre = nombreEn(vs), orden = conLider(vs, lider);
  const tab = orden.some(x => x.key === pq.tab) ? pq.tab : v.key;
  const titulo = t('eq_why') + ' · ' + (o ? o.tt.name : ctx ? t('ctp_ctx_' + ctx) : t('eq_sort_foco'));
  const sub = orden.map(fullLabel).join(' + ') + (o ? ' · ' + (o.sale ? t('eq_instead').replace('{x}', fullLabel(o.sale)) : t('eq_room')) : '');
  const sec = (k, cuerpo, cls) => `<section class="pqm-sec${cls ? ' ' + cls : ''}"><h3>${k}</h3>${cuerpo}</section>`;
  const tabs = orden.map((m, i) => { const sel = m.key === tab, tit = m === lider ? t('eq_lider_de').replace('{x}', fullLabel(m)) : fullLabel(m);
    return `<button type="button" class="pqm-tab${m === lider ? ' lider' : ''}" role="tab" id="pqm-tab${i}" aria-controls="pqm-p${i}" aria-selected="${sel}"
      tabindex="${sel ? 0 : -1}" data-a="pqTab" data-i="${i}" data-key="${h(m.key)}" title="${h(tit)}"><span class="shot" aria-hidden="true">${shot(m.id)}</span>
      <span class="pqm-tabnom">${h(nombre(m))}${m === lider ? ` <span class="pqm-pill">${h(t('eq_lider_pill'))}</span>` : ''}</span></button>`; }).join('');
  const ademas = o ? (o.gana.length ? sec(h(t('pq_gana').replace('{x}', nombre(v))), gruposHtml(agrupar(o.gana), vs)) : '')
    : ctx && d.demas.length ? sec(h(t('pq_ademas')), gruposHtml(agrupar(d.demas), vs)) : '';
  return `<div class="pqm-cab">
      <h2 id="pqm-t" tabindex="-1">${h(titulo)}</h2>
      <button type="button" class="btn icon" data-a="pqCerrar" title="${h(t('tt_cerrar'))}" aria-label="${h(t('tt_cerrar'))}">✕</button>
    </div>
    <div class="pqm-cuerpo">
      <p class="muted pqm-sub">${h(sub)}</p>
      <section class="pqm-sec pqm-equipo">${retratosEquipo(vs, v.key, lider, true)}${o ? ptsEntraHtml(o) : ptsComboHtml(d.e, ctx, d.sc, d.equipo, d.st.length)}</section>
      ${porQueLideraHtml(vs, lider, ctx)}
      ${sec(h(t('pq_puntos')), d.e ? detalleContexto(d.e, vs, ctx) : partesSinergia(d.sc, vs, d.st))}
      ${sec(h(t('pq_integrantes')), `<div class="pqm-tabs" role="tablist" aria-label="${h(t('pq_integrantes'))}">${tabs}</div>
        ${orden.map((m, i) => integranteHtml(m, vs, lider, i, m.key === tab)).join('')}`)}
      ${ademas}
      ${o && o.pierde.length ? sec(h(t('pq_pierde')), gruposHtml(agrupar(o.pierde), o.antesVs), 'pqm-pierde') : ''}
      ${sec(h(ctpsRotulo(d.ctp)), ctpsTablaHtml(orden, d.ctp), 'ga-eq')}
    </div>`;
}
// La ventana: un <dialog> modal (el resto de la página queda inerte), con el foco adentro (Tab da la vuelta), Esc y el
// botón de cerrar, aria-modal y su título; al cerrarla, el foco vuelve al botón que la abrió. Su estado (ui.pq) va en el
// historial: si desde ella se va a una skill, «Atrás» vuelve con la ventana abierta, en la misma pestaña y altura.
/** El <dialog> de la ventana, fuera de #app (render() no lo toca). Se crea la primera vez. */
function dialogoPq () {
  let d = document.getElementById('pqdlg');
  if (d) return d;
  d = document.createElement('dialog');
  d.id = 'pqdlg'; d.className = 'pqdlg';
  d.setAttribute('aria-modal', 'true'); d.setAttribute('aria-labelledby', 'pqm-t');
  // Esc del navegador (y el gesto de volver, donde lo haya): se cierra como con el botón.
  d.addEventListener('cancel', (e) => { e.preventDefault(); cerrarPq(true); });
  // Un clic en el fondo (fuera del cuadro) la cierra; arrastrar desde adentro (al seleccionar texto) no.
  let desdeFondo = false;
  d.addEventListener('mousedown', (e) => { desdeFondo = e.target === d; });
  d.addEventListener('click', (e) => { if (e.target === d && desdeFondo) cerrarPq(true); });
  document.body.appendChild(d);
  return d;
}
/** El botón de la tarjeta que abrió la ventana, si está en la página. */
function botonPq (id) { return document.querySelector(`#app [data-a="pqAbrir"][data-pq="${CSS.escape(id)}"]`); }
/** ¿La ventana sigue siendo de lo que se ve (la pestaña Equipos de la misma ficha y el mismo uniforme)? */
function pqVigente (pq) { return ui.view === 'detail' && ui.charId === pq.charId && ui.uniformId === pq.uid && ui.fichaTab === 'equipos'; }
/** Abre la ventana de una tarjeta (pq: { id, charId, uid, tab, y }), con el foco en su título y, si se vuelve a ella, a la
 *  altura en que estaba. */
function abrirPq (pq) {
  const dlg = dialogoPq(), html = pqHtml(pq, pqDatos(pq.id));
  ui.pq = pq;
  dlg.innerHTML = html;
  dlg.showModal();
  if (pq.y) dlg.querySelector('.pqm-cuerpo').scrollTop = pq.y;
  dlg.querySelector('#pqm-t').focus({ preventScroll: true });
}
/** La cierra; con devolverFoco, el foco vuelve al botón que la abrió (sin mover la página). */
function cerrarPq (devolverFoco) {
  const pq = ui.pq;
  if (!pq) return;
  ui.pq = null;
  const dlg = document.getElementById('pqdlg');
  dlg.close(); dlg.innerHTML = '';
  const b = devolverFoco && botonPq(pq.id);
  if (b) b.focus({ preventScroll: true });
}
/** Para el historial: la ventana abierta, con la altura a la que se la recorrió; null si no hay. */
function pqAnotado () {
  if (!ui.pq) return null;
  return { ...ui.pq, y: document.querySelector('#pqdlg .pqm-cuerpo').scrollTop };
}
/** Elige la pestaña i de la ventana (sin volver a pintarla: lo desplegado y la altura quedan). */
function elegirTabPq (i) {
  const dlg = document.getElementById('pqdlg');
  dlg.querySelectorAll('[role="tab"]').forEach((b, j) => {
    b.setAttribute('aria-selected', String(j === i)); b.tabIndex = j === i ? 0 : -1;
    if (j === i) ui.pq.tab = b.dataset.key;
  });
  dlg.querySelectorAll('[role="tabpanel"]').forEach((p, j) => { p.hidden = j !== i; });
}
/** Las teclas con la ventana abierta: Esc la cierra, Tab y Shift+Tab dan la vuelta adentro y, en las pestañas, ← → Inicio
 *  y Fin pasan de una a otra (sin Alt ni Ctrl: Alt+← es volver). Ninguna llega a la página de atrás (las flechas de la
 *  ficha, por ejemplo). */
function teclaPq (e) {
  const dlg = document.getElementById('pqdlg');
  if (e.key === 'Escape') { e.preventDefault(); cerrarPq(true); return; }
  if (e.key === 'Tab') {
    const fs = [...dlg.querySelectorAll('button, a[href], summary, [tabindex="0"]')].filter(x => x.getClientRects().length && x.tabIndex >= 0);
    const i = fs.indexOf(document.activeElement);
    if (e.shiftKey ? i <= 0 : (i === fs.length - 1 || !dlg.contains(document.activeElement))) {
      e.preventDefault(); (e.shiftKey ? fs[fs.length - 1] : fs[0]).focus();
    }
    return;
  }
  const tab = e.target.closest && e.target.closest('#pqdlg [role="tab"]');
  if (!tab || e.altKey || e.ctrlKey || e.metaKey) return;
  const tabs = [...dlg.querySelectorAll('[role="tab"]')], i = tabs.indexOf(tab);
  const j = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
  if (j == null) return;
  e.preventDefault();
  const k = (j + tabs.length) % tabs.length;
  elegirTabPq(k); tabs[k].focus();
}
/** Equipos: cómo entra el personaje (con el uniforme elegido) en los equipos que armaste y
 *  todas las combinaciones de 3 con él. */
function fichaEquipos (ch, v) {
  const suyos = U.teams.filter(tt => tt.members.some(k => k.split('::')[0] === ch.id));
  const otros = U.teams.filter(tt => !suyos.includes(tt)).map(tt => comoEntra(v, tt));
  const sinVinculo = otros.filter(o => o.sinVinculo), entra = otros.filter(o => !o.sinVinculo);
  const mejoran = entra.filter(o => o.delta > 0).sort((a, b) => b.delta - a.delta);
  const no = entra.filter(o => o.delta <= 0);
  return `<div class="section"><h3>${h(t('eq_mine'))}</h3>
    ${!U.teams.length ? `<p class="muted" style="margin-bottom:10px">${h(t('eq_none'))}</p>` : ''}
    ${suyos.length ? `<div class="grid eqgrid">${suyos.map(tt => equipoCard(tt)).join('')}</div>`
                   : U.teams.length ? `<p class="muted">${h(t('eq_in_none'))}</p>` : ''}
    <div class="row" style="margin-top:10px">${botonPoner(v)}</div>
  </div>
  ${otros.length ? `<div class="section"><h3>${h(t('eq_could'))}</h3>
    <p class="muted" style="margin-bottom:10px">${h(t('eq_could_note').replace('{v}', fullLabel(v)))}</p>
    ${mejoran.map(o => `<div class="card eqsug">
      <div class="row" style="justify-content:space-between">
        <div><b>${h(o.tt.name)}</b>${o.modo ? ` <span class="tag dim">${h(o.modo)}</span>` : ''}
          <div class="muted">${h(o.sale ? t('eq_instead').replace('{x}', fullLabel(o.sale)) : t('eq_room'))}</div></div>
        ${ptsEntraHtml(o)}
      </div>
      ${retratosEquipo(o.vs, v.key, o.despues.lider)}
      <div class="row">${porqueBoton('t|' + o.tt.id + '|' + v.key)}${botonArmar(conLider(o.vs, o.despues.lider), o.tt.modeId, t('eq_name_swap').replace('{e}', o.tt.name).replace('{v}', v.name))}</div>
    </div>`).join('')}
    ${no.length ? `<p class="muted">${h(t('eq_no_gain'))} ${no.map(o => `${h(o.tt.name)} (${o.delta >= 0 ? '±0' : o.delta})`).join(' · ')}</p>` : ''}
    ${sinVinculo.length ? `<p class="muted">${h(t('eq_no_link'))} ${sinVinculo.map(o => h(o.tt.name)).join(' · ')}</p>` : ''}
  </div>` : ''}
  ${bonosHtml(ch)}
  ${strikersHtml(ch)}
  ${combinacionesHtml(v)}`;
}
/** Los bonos de equipo del personaje (valen con cualquier uniforme), plegados: el nombre, con
 *  quiénes, qué suben y de dónde sale cada uno. Primero los de tres. */
function bonosHtml (ch) {
  const bonos = (BONOS_DE[ch.id] || []).slice().sort((a, b) => b.m.length - a.m.length || (a.n || '').localeCompare(b.n || ''));
  if (!bonos.length) return `<div class="section" id="bonos"><h3>${h(t('bn_title'))}</h3><p class="muted">${h(t('bn_none'))}</p></div>`;
  return `<div class="section" id="bonos"><h3>${h(t('bn_title'))} ${ayudaHtml(t('bn_note'))}</h3>
    <details class="reglas"><summary>${h(t('bn_show').replace('{n}', bonos.length))}</summary>
      <div class="grid eqgrid">${bonos.map(b => `<div class="card bono">
        <b>${h(b.n || t('bn_noname'))}</b>
        ${retratosEquipo(b.m.filter(c => c !== ch.id).map(c => variant(c, null)), null)}
        ${b.vs.length > 1 ? `<div class="muted bonoaviso">${h(t('bn_tie'))}</div>` : ''}
        ${b.vs.map(v => `<div class="bonostats">${h(v.fx.map(f => efectoSoporteTxt(v, f)).join(' · '))}</div>`).join('')}
        <div class="fuentes">${fuentesHtml(b.f)}</div>
      </div>`).join('')}</div>
    </details>
  </div>`;
}
/** La probabilidad de que aparezca un striker y cuándo: «12% al atacar», en la ficha, el «Por qué» y el detalle
 *  de PvP y PvE. Más de 100% es un dato imposible de la wiki (Daken: Doctor Octopus, 219%): va tal cual, sin
 *  topear, marcado (docs/AUDITORIA.md, sección 11). */
function strikerProbHtml (p, cuando) {
  const txt = h(t('sk_' + cuando).replace('{p}', numTxt(p)));
  return p > 100 ? `<span class="imposible" title="${h(t('sk_imposible'))}">${txt} ⚠</span>` : txt;
}
/** Los strikers del personaje (de la pestaña Striker de la wiki; valen con cualquier uniforme) y de
 *  quiénes es striker, plegados: cada uno con su retrato, su probabilidad de aparecer y cuándo, de
 *  mayor a menor probabilidad. */
function strikersHtml (ch) {
  // Una fila por personaje con los dos sentidos (#24, caso del 6 de octubre de 2026): la relación no es simétrica, y
  // en dos grillas había que cruzarlas a ojo. «Sin dato»: la wiki no tiene la pestaña Striker de ese lado.
  const suyos = STRIKERS[ch.id], de = STRIKERS_DE[ch.id] || [], filas = new Map();
  for (const [cid, p, c] of suyos || []) filas.set(cid, { cid, ayudan: [p, c] });
  for (const [cid, p, c] of de) filas.set(cid, Object.assign(filas.get(cid) || { cid }, { ayuda: [p, c] }));
  const max = (f) => Math.max(f.ayudan ? f.ayudan[0] : 0, f.ayuda ? f.ayuda[0] : 0);
  const celda = (x, conDato) => x ? strikerProbHtml(x[0], x[1])
    : conDato ? `<span class="muted">${h(t('sk_no'))}</span>` : `<span class="muted" title="${h(t('sk_sin_dato_t'))}">${h(t('sk_sin_dato'))}</span>`;
  const lista = [...filas.values()].sort((a, b) => max(b) - max(a));
  return `<div class="section" id="strikers"><h3>${h(t('sk_title'))} ${ayudaHtml(t('sk_note') + ' ' + t('sk_de_nota'))}</h3>
    ${!suyos ? `<p class="muted">${h(t('sk_sin_pestana'))}</p>` : ''}${!de.length ? `<p class="muted">${h(t('sk_de_nadie'))}</p>` : ''}
    ${lista.length ? `<details class="reglas"><summary>${h(t('sk_resumen').replace('{n}', lista.length).replace('{a}', (suyos || []).length).replace('{b}', de.length))}</summary>
      <div class="tablawrap"><table class="sktabla"><thead><tr><th>${h(t('sk_con'))}</th><th>${h(t('sk_lo_ayudan'))}</th><th>${h(t('sk_el_ayuda'))}</th></tr></thead>
      <tbody>${lista.map(f => { const x = variant(f.cid, null);
        return `<tr><td><button class="plabrir sk" data-a="open" data-cid="${x.cid}" data-uid=""><span class="plfoto" style="--cc:${classColor(x.c)}">${shot(x.id)}</span>
          <span class="pltx"><b>${h(x.name)}</b></span></button></td>
          <td>${celda(f.ayudan, !!suyos)}</td><td>${celda(f.ayuda, !!STRIKERS[f.cid])}</td></tr>`; }).join('')}</tbody></table></div>
    </details>` : ''}
    <div class="fuentes">${fuentesHtml(['wiki-strikers'])}</div>
  </div>`;
}
/** El mejor lugar para v en un equipo: reemplazando a cada integrante o, si hay lugar,
 *  sumándolo. Solo valen los lugares donde queda con vínculo con alguien del
 *  equipo; si no hay ninguno, no encaja. Con lo que se gana y se pierde según las razones (en
 *  piezas): de lo que se gana quedan afuera lo que le llega a v y lo que da él, que el «Por qué» de
 *  la tarjeta dice aparte. */
function comoEntra (v, tt) {
  const vs = tt.members.map(k => variant(...k.split('::'))).filter(Boolean), lider = liderEquipo(tt, vs);
  // El líder es el declarado; si sale él, el que entra ocupa su lugar y lidera.
  const opciones = vs.map((x, i) => ({ sale: x, vs: vs.map((y, j) => j === i ? v : y), lider: x === lider ? v : lider }));
  if (vs.length < tamModo(tt.modeId)) opciones.push({ sale: null, vs: vs.concat(v), lider });
  const validas = opciones.map(o => Object.assign(o, { despues: synergy(o.vs, { lider: o.lider }) }))
    .filter(o => o.vs.some(x => x !== v && (vinculo(v, x, o.despues.aplicados) || vinculoLider(v, x, o.despues.lider))));
  if (!validas.length) return { tt, sinVinculo: true };
  const antes = synergy(vs, { lider });
  // El mejor lugar: el de más puntos; a igual puntaje, el de más strikers (desempatan).
  const mejor = validas.sort((a, b) => b.despues.score - a.despues.score || cuantosStrikers(b.vs, null) - cuantosStrikers(a.vs, null))[0];
  const modo = modosEquipo().find(m => m.id === tt.modeId);
  const pa = piezas(antes.razones), pd = piezas(mejor.despues.razones);
  const habia = new Set(pa.map(p => p.clave)), hay = new Set(pd.map(p => p.clave));
  return { tt, antes, antesVs: vs, vs: mejor.vs, sale: mejor.sale, despues: mejor.despues, delta: mejor.despues.score - antes.score,
           modo: modo ? modo.name : '', ctp: modo ? modo.ctp : null,
           gana: pd.filter(p => !habia.has(p.clave) && !(p.f && p.r.tipo !== 'bono' && (p.para === v || p.r.de === v))),
           pierde: pa.filter(p => !hay.has(p.clave)) };
}
/** Retratos de un equipo. Con su líder (liderDe), el líder va primero (a la izquierda, como en el juego) con su
 *  marca: el aro del color de acento y la pastilla «Líder», también en el title. El de la clave `resaltada` (el
 *  personaje de la ficha) va marcado aparte. Cada uno abre su ficha; fijo: no abren nada (la ventana del «Por qué»,
 *  donde cada integrante tiene su pestaña). */
function retratosEquipo (vs, resaltada, lider, fijo) {
  return `<div class="row eqfotos">${conLider(vs, lider).map(x => { const titulo = x === lider ? t('eq_lider_de').replace('{x}', fullLabel(x)) : fullLabel(x);
    const cls = `eqfoto${x.key === resaltada ? ' nuevo' : ''}${x === lider ? ' lider' : ''}`, cuerpo = `<span class="shot">${shot(x.id)}${
      x === lider ? `<span class="pillider"${fijo ? '' : ' aria-hidden="true"'}>${h(t('eq_lider_pill'))}</span>` : ''}</span><span>${h(x.name)}</span>`;
    return fijo ? `<span class="${cls}" data-cid="${x.cid}" data-uid="${x.uid || ''}" title="${h(titulo)}">${cuerpo}</span>`
      : `<button class="${cls}" data-a="open" data-cid="${x.cid}" data-uid="${x.uid || ''}" title="${h(titulo)}" aria-label="${h(titulo)}">${cuerpo}</button>`; }).join('')}</div>`;
}
// COMBINACIONES DE 3 CON ÉL: una consulta sobre los datos, no listas armadas de antemano.
// Para el personaje (con el uniforme elegido) recorre todas las parejas de compañeros y se
// queda con los equipos en que los dos tienen vínculo con él (vinculo() y, por el liderazgo,
// vinculoLider() con el líder de cada orden: sin contexto, el de la sinergia; en PvP y PvE, el del
// contexto), con el puntaje para
// él (synergy con foco: lo que le dan, lo que da él, sus bonos de equipo, la ventaja de clase
// con él, roles y clases). Antes eran tres equipos por tamaño de una búsqueda aproximada, y salían
// siempre los mismos seis soportes sin forma de ver los demás.
// Solo se recorren las parejas en que cada uno puede vincularse con él (puedeVincular): si
// ningún soporte ni liderazgo de uno le llega al otro y le sirve, ni están juntos en un bono de
// equipo, en ningún equipo se vinculan. La consulta queda en memoria (la última) hasta el
// próximo cambio de datos (rebuild()); el orden, los filtros y las páginas trabajan sobre ella.
const POR_PAGINA = 20;
// Contextos PvP y PvE: las tier lists de thanosvibs de esos modos (Arena de Equipos; Batalla de
// Alianza y World Boss Legend), las de scripts/contenido/roles_listas.json. Las arma iniciarDatos().
let LISTAS_PVP, LISTAS_PVE;
function puedeVincular (de, a) {
  const s = SOPORTES[de.p];
  if (s && TIPOS_SOPORTE.some(([k]) => s[k] && aplicaA(s[k], a) && leSirve(s[k], a))) return true;
  const bonos = BONOS_DE[de.cid];
  return !!bonos && bonos.some(b => b.m.includes(a.cid));
}
// CONTEXTO PvP / PvE (reglas de Ezequiel, 2 y 4 de octubre de 2026). Un equipo vale según dónde se usa:
// - Quién es DPS, soporte o líder sale de las filas de las tier lists del contexto (rolEn). Un trío
//   sin ningún DPS de ese contexto no sirve.
// - Lo demás está en la tabla de valor (MFF_VALOR, scripts/contenido/valor_equipos.json), una fila por
//   contexto: el requisito (en PvP, que los tres tengan anti-mermas, del liderazgo del líder o del soporte
//   de alguno; si viene de un soporte, el lugar de líder queda para otro liderazgo), cuánto suma cada stat
//   del liderazgo del líder por cada integrante al que le llega y le sirve (y qué parte, si el liderazgo
//   se activa con una condición: el slot trae ac), cuánto cada nivel de fila de cada DPS (3 la más alta),
//   cada soporte que le llega a otro y le sirve y cada bono de equipo activo que le sirve a alguien. Los
//   strikers no suman: a igual puntaje, desempatan (strikersDe).
// El líder es el que más suma de los que cumplen; a igual puntaje, el mejor ubicado en las tier lists
// del contexto y después la clave. Es el mismo en las listas de los tres (Ezequiel, 2 de octubre de
// 2026: «único + condicional a la mitad», sin mirar los porcentajes).
// Lo arma iniciarDatos(): ANTI_MERMAS, los stats que cuentan como anti-mermas, y CONTEXTO[ctx], la fila de
// la tabla con vale (índice de cada stat que pesa), peso (el de cada uno, por índice) y llega (a quiénes
// les llega cada uno, en bits de integrante: 0-2 por un liderazgo permanente, 3-5 por uno condicional;
// se reusa en los cientos de miles de tríos de la consulta).
let ANTI_MERMAS, CONTEXTO;
/** A cuántos integrantes marcan los bits 0-2. */
const aCuantos = (bits) => (bits & 1) + (bits >> 1 & 1) + (bits >> 2 & 1);
/** Los strikers de cada personaje, como conjunto, para preguntar rápido. Lo arma iniciarDatos(). */
let STRIKER_SET;
/** Rol de una variante en un contexto, según las filas de las listas de ese contexto en las que está
 *  (las de thanosvibs, con tus cambios): { dps, soporte (nivel de la mejor fila, 0 si no lo es),
 *  lider, striker, fuera, filas: [[lista, fila]], puesto (la suma de su puesto() en esas listas:
 *  desempata al líder) }. Se guarda hasta el próximo rebuild(). */
const _ROL = new Map();
function rolEn (v, ctx) {
  const k = ctx + '|' + v.key;
  let r = _ROL.get(k);
  if (r) return r;
  r = { dps: 0, soporte: 0, lider: false, striker: false, fuera: false, filas: [], puesto: 0 };
  for (const [lid, roles] of Object.entries(ROLES_LISTAS[ctx])) {
    const l = listById(lid);
    if (!l) throw new Error('falta la tier list ' + lid);
    r.puesto += puesto(l, v.key);
    for (const fid of filasDe(lid, v.key)) {
      const rf = roles[fid];
      if (!rf) throw new Error(`fila ${fid} de ${lid} sin rol en roles_listas.json`);
      const [rol, nivel] = rf;
      if (rol === 'dps' || rol === 'soporte') r[rol] = Math.max(r[rol], nivel);
      else r[rol] = true;
      r.filas.push([l, fid]);
    }
  }
  _ROL.set(k, r);
  return r;
}
/** ¿Tiene función en el contexto? Según Ezequiel, quien no figura en las tier lists del contexto, o
 *  solo en una fila que lo deja fuera («Not for wbl»), no la tiene (Thor base, en PvP y en PvE), y
 *  el orden de ese contexto no le arma combinaciones. */
/** Las filas de las listas del contexto que lo dejan fuera (rol «fuera» en MFF_ROLES_LISTAS), para el aviso:
 *  «, o solo como «Not for wbl»», o nada si el contexto no tiene. */
function filasFueraTxt (ctx) {
  const fs = Object.entries(ROLES_LISTAS[ctx]).flatMap(([lid, filas]) => Object.entries(filas).filter(([, [rol]]) => rol === 'fuera')
    .map(([fid]) => '«' + rowsOf(listById(lid)).find(r => r.id === fid).label + '»'));
  return fs.length ? t('cx_o_solo').replace('{f}', fs.join(', ')) : '';
}
function tieneFuncion (v, ctx) { const r = rolEn(v, ctx); return r.dps > 0 || r.soporte > 0 || r.lider || r.striker; }
/** Liderazgos y soportes de un retrato (con el slot de cada soporte), y cuáles dan anti-mermas, para el
 *  puntaje de contexto. */
const _SLOTS = new Map();
function slotsDe (v) {
  let s = _SLOTS.get(v.p);
  if (s) return s;
  const so = SOPORTES[v.p] || {};
  s = { lid: [], lidK: [], sop: [], sopK: [], antiLid: [], antiSop: [] };   // lidK y sopK: el slot de cada uno de lid y sop
  for (const [k] of TIPOS_SOPORTE) {
    const x = so[k];
    if (!x) continue;
    const lid = LIDERAZGOS.includes(k), anti = x.fx.some(f => ANTI_MERMAS.has(f.s));
    if (lid) { s.lid.push(x); s.lidK.push(k); } else { s.sop.push(x); s.sopK.push(k); }
    if (anti) (lid ? s.antiLid : s.antiSop).push(x);
  }
  if (v.p) _SLOTS.set(v.p, s);
  return s;
}
// LÍDER DE UN EQUIPO (Ezequiel, 4 de octubre de 2026: la regla de la 1.0.16 para todo). Un equipo tiene un
// solo líder, el mismo sea cual sea el orden de sus integrantes y desde la lista de quien se lo mire: el que
// más puntos de liderazgo suma en el contexto; a igual puntaje, el mejor ubicado en las tier lists del
// contexto (sin contexto, la General de thanosvibs) y después la clave. En PvP solo puede liderar uno con el
// que todos tienen anti-mermas. Lo usan la sinergia (puntos para él, del equipo, tus equipos, favoritos, la
// comparativa, «cómo entraría» y las tier lists sin contexto) y los órdenes PvP y PvE.
const LISTA_SIN_CONTEXTO = 'tv-general';
const _PUESTO_SC = new Map();
/** Puesto de una variante en la lista que desempata al líder sin contexto (puesto()). Se guarda hasta el
 *  próximo rebuild(). */
function puestoSinContexto (v) {
  let p = _PUESTO_SC.get(v.key);
  if (p === undefined) {
    const l = listById(LISTA_SIN_CONTEXTO);
    if (!l) throw new Error('falta la tier list ' + LISTA_SIN_CONTEXTO + ', la que desempata al líder sin contexto');
    _PUESTO_SC.set(v.key, p = puesto(l, v.key));
  }
  return p;
}
/** Lo que suma el liderazgo de a en un equipo sin contexto: cada slot de liderazgo con el que a otro integrante le llega
 *  algo que se le aplica y le sirve, 3 si es Notable y 2 si no, como en la sinergia (con a de líder). */
function ptsLiderSinContexto (a, vs) {
  const s = SOPORTES[a.p]; if (!s) return 0;
  let pts = 0;
  for (const k of LIDERAZGOS) {
    const x = s[k]; if (!x) continue;
    for (const b of vs) if (b !== a && aplicaAlgo(b, a, k, x, vs, a)) { pts += x.sig ? 3 : 2; break; }
  }
  return pts;
}
/** El líder de un equipo sin contexto: el que más suma con su liderazgo (ptsLiderSinContexto). null si ninguno suma. */
function liderSinContexto (vs) {
  let lider = null, ptsLider = 0;
  for (const a of vs) {
    const pts = ptsLiderSinContexto(a, vs);
    if (pts && (pts > ptsLider || (pts === ptsLider && (puestoSinContexto(a) < puestoSinContexto(lider)
        || (puestoSinContexto(a) === puestoSinContexto(lider) && a.key < lider.key))))) { lider = a; ptsLider = pts; }
  }
  return lider;
}
/** ¿Puede liderar vs[i] en el contexto (la fila C de la tabla de valor)? En PvP, solo si con su liderazgo los tres
 *  tienen anti-mermas (cubreSop: a quiénes ya se los cubre otra cosa, cubiertos()). sl: los slotsDe de cada uno. */
function puedeLiderar (vs, i, C, sl, cubreSop) {
  return C.requisito !== 'anti_mermas' || vs.every((m, j) => cubreSop[j] || sl[i].antiLid.some(x => aplicaA(x, m)));
}
/** Lo que suma el liderazgo de vs[i] en el contexto (la fila C de la tabla de valor). Cada stat que vale cuenta una
 *  vez por integrante, aunque el liderazgo lo traiga en varias líneas (Arachknight 2099: todos los ataques +45%,
 *  +55% o +65% según sus Infinity Warps), con la de más peso: el suyo si le llega por un liderazgo permanente y la
 *  parte del condicional si solo le llega por uno que se activa con una condición (Silver Surfer: al recibir un
 *  debuff). Usa C.llega, que se reusa en los cientos de miles de tríos de la consulta. */
function ptsLiderazgo (vs, i, C, sl) {
  const vale = C.vale, llega = C.llega;
  llega.fill(0);
  for (let n = 0; n < sl[i].lid.length; n++) {
    const x = sl[i].lid[n], b = x.ac ? 3 : 0;
    for (const f of x.fx) {
      const k = vale.get(f.s);
      if (k === undefined) continue;
      // Uno que no se acumula (la tabla de hoy no pesa ninguno) suma si es el que se le aplica (fuenteQueSeAplica).
      for (let j = 0; j < vs.length; j++) if (aplicaA(x, vs[j]) && sirve(f, vs[j])
          && (seAcumula(f) || esLaFuente(fuenteQueSeAplica(vs[j], f.s, vs, vs[i]), vs[i], sl[i].lidK[n], x))) llega[k] |= 1 << (b + j);
    }
  }
  let pts = 0;
  for (let k = 0; k < llega.length; k++) {
    const bits = llega[k];
    pts += aCuantos(bits) * C.peso[k] + aCuantos(bits >> 3 & ~bits) * C.peso[k] * C.condicional;
  }
  return pts;
}
/** El líder de un equipo en PvP o PvE, con lo que enContexto ya sabe de él (los slots de cada uno, sus roles y a
 *  quiénes les cubre anti-mermas un soporte): de los que pueden liderar (puedeLiderar), el que más suma con su
 *  liderazgo (ptsLiderazgo); a igual puntaje, el mejor ubicado en las tier lists del contexto y después la clave.
 *  { li: su índice en vs (-1 si en PvP ninguno deja a todos con anti-mermas), pts: sus puntos de liderazgo }. */
function liderContexto (vs, ctx, sl, roles, cubreSop) {
  const C = CONTEXTO[ctx];
  let li = -1, ptsLider = 0;
  for (let i = 0; i < vs.length; i++) {
    if (!puedeLiderar(vs, i, C, sl, cubreSop)) continue;
    const pts = ptsLiderazgo(vs, i, C, sl);
    if (li < 0 || pts > ptsLider || (pts === ptsLider && (roles[i].puesto < roles[li].puesto
        || (roles[i].puesto === roles[li].puesto && vs[i].key < vs[li].key)))) { li = i; ptsLider = pts; }
  }
  return { li, pts: ptsLider };
}
/** Quiénes del equipo tienen anti-mermas sin el liderazgo del líder: de un soporte de alguno (también el propio)
 *  o de sus propias skills (antiPropio; los que tienen probabilidad no cuentan). sl: los slotsDe de cada uno. */
function cubiertos (vs, sl) { return vs.map(m => sl.some(s => s.antiSop.some(x => aplicaA(x, m))) || antiPropio(m).cuenta.length > 0); }
/** El líder de un equipo en un contexto (null, 'pvp' o 'pve'); null si no lo tiene. */
function liderDe (vs, ctx) {
  if (!ctx) return liderSinContexto(vs);
  const sl = vs.map(slotsDe);
  const { li } = liderContexto(vs, ctx, sl, vs.map(x => rolEn(x, ctx)), cubiertos(vs, sl));
  return li < 0 ? null : vs[li];
}
/** Un equipo con su líder primero (a la izquierda, como en el juego) y los demás en su orden. */
function conLider (vs, lider) { return lider ? [lider].concat(vs.filter(x => x !== lider)) : vs; }
/** Un trío en un contexto. null si no entra: sin ningún DPS de ese contexto o, en PvP, sin un líder
 *  con el que los tres tengan anti-mermas. Si entra: { score, lider, partes: { lider, dps, sinergia },
 *  strikers: cuántos (desempatan), art: si sumó el soporte de un artefacto }; con detalle, también de
 *  dónde sale cada punto (detalleContexto lo escribe). */
function enContexto (vs, ctx, detalle) {
  const roles = vs.map(x => rolEn(x, ctx));
  if (!roles.some(r => r.dps)) return null;
  const sl = vs.map(slotsDe);
  const cubreSop = cubiertos(vs, sl);
  const { li, pts: ptsLider } = liderContexto(vs, ctx, sl, roles, cubreSop);
  if (li < 0) return null;
  const C = CONTEXTO[ctx];
  let dps = 0;
  for (const r of roles) dps += r.dps * C.dps;
  // Un soporte suma si a otro integrante le llega algo que se le aplica y le sirve (reparto: lo que no tiene valor, solo
  // si no lo tiene ya de una fuente anterior). Con detalle, también qué soportes (de quién, cuál, a quiénes se les aplica
  // y a quiénes les llega algo que ya tienen; con 0 los que no suman por eso) y qué bonos sumaron.
  let sinergia = 0, art = false;
  const sops = detalle ? [] : null, bonos = detalle ? [] : null, lider = vs[li];
  for (let a = 0; a < vs.length; a++) for (let n = 0; n < sl[a].sop.length; n++) {
    const x = sl[a].sop[n], k = sl[a].sopK[n];
    if (!detalle) {
      if (!vs.some((b, j) => j !== a && aplicaAlgo(b, vs[a], k, x, vs, lider))) continue;
      sinergia += C.soporte;
      if (k === 'artifact') art = true;
      continue;
    }
    const r = reparto(vs[a], k, x, vs, lider, true);
    if (!r) continue;
    if (r.si.length) { sinergia += C.soporte; if (k === 'artifact') art = true; }
    sops.push({ de: vs[a], k, x, a: r.si, no: r.no, pts: r.si.length ? C.soporte : 0 });
  }
  for (const a of vs) for (const b of BONOS_DE[a.cid] || []) {
    if (b.m[0] === a.cid && estanTodos(b.m, vs) && vs.some(x => b.vs.some(bv => leSirve(bv, x)))) {
      sinergia += C.bono;
      if (detalle) bonos.push({ b, integrantes: vs.filter(x => b.m.includes(x.cid)), a: vs.filter(x => b.vs.some(bv => leSirve(bv, x))) });
    }
  }
  // Los strikers del trío no suman: desempatan (strikersDe).
  const out = { score: ptsLider + dps + sinergia, lider: vs[li], partes: { lider: ptsLider, dps, sinergia }, strikers: cuantosStrikers(vs, null), art };
  if (detalle) Object.assign(out, { roles, sl, cubreSop, sops, bonos });
  return out;
}
function consultaCon (v) {
  if (CONSULTA && CONSULTA.clave === v.key) return CONSULTA;
  const pool = allVariants().filter(x => x.cid !== v.cid);
  const puede = pool.map(x => puedeVincular(x, v) || puedeVincular(v, x));
  // En los contextos PvP y PvE, un DPS de ese contexto entra aunque no tenga vínculo con él.
  const dps = pool.map(x => rolEn(x, 'pvp').dps > 0 || rolEn(x, 'pve').dps > 0);
  // El liderazgo vincula según quién lidera (vinculoLider), de a pares: si el de cada compañero le llega a
  // él (ld) y si el suyo le llega a cada compañero (lv). vinculosFila lo suma con el líder de cada orden.
  const ld = Uint8Array.from(pool, x => llegaLiderazgo(x, v)), lv = Uint8Array.from(pool, x => llegaLiderazgo(v, x));
  // sv: quiénes tienen un soporte que trae algo que no se acumula (y él, svV). En un trío con alguno, el vínculo por un
  // soporte depende del líder (de él depende qué se le aplica a cada uno: ver «Efectos iguales»).
  const sv = Uint8Array.from(pool, sopNoAcumulable), svV = sopNoAcumulable(v);
  const max = pool.length * (pool.length - 1) / 2;
  // G: qué compañeros tienen vínculo con él por un soporte o un bono de equipo (1, el primero; 2, el
  // segundo), con el líder de la sinergia. P: los puntos para él y L: el líder de la sinergia, el de la
  // tarjeta sin contexto (0 él, 1 o 2 el compañero, 3 ninguno; lo usan el filtro de cobertura y los
  // vínculos sin contexto). Van las filas que pueden entrar en algún orden: con los dos vinculados, con
  // cualquiera de los tres de líder (en un trío con sv, por un soporte con cualquier líder: puede), o con
  // un DPS de PvP o PvE en lugar del que no.
  // S: cuántos strikers del trío lo involucran (desempatan los puntos para él).
  const A = new Int32Array(max), B = new Int32Array(max), P = new Int16Array(max), G = new Uint8Array(max), L = new Uint8Array(max),
        S = new Uint8Array(max);
  // Un solo arreglo de equipo y unas solas opciones para los cientos de miles de llamadas
  // (synergy no se los guarda: lo que devuelve se usa acá mismo y se descarta).
  const vs = [v, null, null], op = { soloPuntaje: true, foco: v };
  let n = 0;
  for (let i = 0; i < pool.length; i++) {
    if (!puede[i] && !dps[i]) continue;
    vs[1] = pool[i];
    for (let j = i + 1; j < pool.length; j++) {
      if ((!puede[j] && !dps[j]) || pool[i].cid === pool[j].cid) continue;
      vs[2] = pool[j];
      let g = 0, pts = 0, li = 3;
      if (puede[i] || puede[j]) {
        const sc = synergy(vs, op);
        if (puede[i] && vinculo(v, pool[i], sc.aplicados)) g |= 1;
        if (puede[j] && vinculo(v, pool[j], sc.aplicados)) g |= 2;
        pts = sc.score;
        if (sc.lider) li = vs.indexOf(sc.lider);
      }
      const gs = svV || sv[i] || sv[j] ? (puede[i] ? 1 : 0) | (puede[j] ? 2 : 0) : g;
      const f = gs | (ld[i] || lv[i] ? 1 : 0) | (ld[j] || lv[j] ? 2 : 0);
      if (f !== 3 && !((f & 1 || dps[i]) && (f & 2 || dps[j]))) continue;
      A[n] = i; B[n] = j; P[n] = pts; G[n] = g; L[n] = li; S[n] = cuantosStrikers(vs, v); n++;
    }
  }
  CONSULTA = { clave: v.key, cid: v.cid, v, pool, puede: Uint8Array.from(puede), sv, svV, ld, lv, A, B, P, G, L, S, n, vista: null };
  return CONSULTA;
}
/** ¿Tiene v algún soporte que trae algo que no se acumula? */
function sopNoAcumulable (v) { const so = SOPORTES[v.p]; return !!so && SLOTS_SOPORTE.some(k => so[k] && traeNoAcumulable(so[k])); }
/** Con qué compañeros (1, vs[1]; 2, vs[2]) tiene vs[0] un vínculo por un soporte o un bono de equipo, con este líder (G de
 *  la consulta, contado con otro). */
function vinculosSoporte (vs, lider) {
  const ap = synergy(vs, { soloPuntaje: true, foco: vs[0], lider }).aplicados;
  return (vinculo(vs[0], vs[1], ap) ? 1 : 0) | (vinculo(vs[0], vs[2], ap) ? 2 : 0);
}
/** Con qué compañeros de la fila i de la consulta tiene vínculo él (1, el primero; 2, el segundo), con li de
 *  líder (0 él, 1 o 2 el compañero, 3 ninguno): por un soporte o un bono de equipo (g: el de la consulta, G, que
 *  se contó con el líder de la sinergia) y por el liderazgo del líder (vinculoLider). */
function vinculosFila (q, i, li, g = q.G[i]) {
  const a = q.A[i], b = q.B[i];
  return g | (li === 0 ? (q.lv[a] ? 1 : 0) | (q.lv[b] ? 2 : 0) : li === 1 ? (q.ld[a] ? 1 : 0) : li === 2 ? (q.ld[b] ? 2 : 0) : 0);
}
/** Contexto del orden elegido: 'pvp', 'pve' o null (puntos para él, o una tier list). */
function contextoOrden () { return ui.eqOrden === 'pvp' || ui.eqOrden === 'pve' ? ui.eqOrden : null; }
/** Tier lists del orden elegido: las de PvP, las de PvE o una sola (cualquiera de personajes). */
function listasOrden () {
  const o = ui.eqOrden;
  const ids = o === 'pvp' ? LISTAS_PVP : o === 'pve' ? LISTAS_PVE : o.startsWith('lista:') ? [o.slice(6)] : [];
  return ids.map(id => { const l = listById(id); if (!l) throw new Error('falta la tier list ' + id); return l; });
}
/** Puesto de una variante en una lista: su mejor fila (0 es la de arriba); sin ubicar, una
 *  fila más abajo que la última. */
function puesto (l, key) { const i = indicesFila(l, key); return i.length ? i[0] : rowsOf(l).length; }
/** Su lugar en una lista, como en el roster: la mejor fila con «+N» si está en más (todas, en el title), o «—». */
function puestoHtml (l, key) { const f = filaEn(l, key); return f ? `<span title="${h(f.todas.join(' · '))}">${h(rankTexto(f))}</span>` : '—'; }
// SOLO EL ÚLTIMO UNIFORME (Ezequiel, 5 de octubre de 2026: «vamos a agregar un filtro mas en el armado de equipos... SOLO
// ultimo uniforme»). En las combinaciones de 3, de cada compañero entra solo su uniforme más nuevo: sin uniformes, la
// base; con uniformes, la base no entra. El personaje de la ficha va con el uniforme elegido. El más nuevo es el que salió
// en la versión del juego más alta (up.update de thanosvibs, comparada como versión: 10.2 < 12.0 < 12.0.5; la letra va
// después del número, 9.1.5a antes que 9.1.5b) y, a igual versión, el de número de uniforme más alto en el juego (el del
// id: deadpool-10800164, Deadpool & Wolverine, va antes que deadpool-10700164, Nicepool). Desde los datos de formato 9,
// todos los uniformes traen su versión (el build la saca de /api/updates de thanosvibs).
/** La versión del juego en que salió un uniforme, para comparar: { n: [números], l: letra o '' }. */
function versionUniforme (u) {
  const s = u.up.update;
  const m = /^(\d+(?:\.\d+)*)([a-z]?)$/.exec(s);
  if (!m) throw new Error(`versión de juego que la app no sabe leer en el uniforme ${u.id}: ${s}`);
  return { n: m[1].split('.').map(Number), l: m[2] };
}
/** Orden de dos versiones (versionUniforme): los números, de a uno (12.0 = 12.0.0), y después la letra. */
function cmpVersion (a, b) {
  for (let i = 0; i < Math.max(a.n.length, b.n.length); i++) { const d = (a.n[i] || 0) - (b.n[i] || 0); if (d) return d; }
  return a.l < b.l ? -1 : a.l > b.l ? 1 : 0;
}
/** El número de un uniforme en el juego: el del final de su id (deadpool-10800164). */
function numeroUniforme (u) {
  const m = /-(\d+)$/.exec(u.id);
  if (!m) throw new Error('uniforme sin el número del juego en su id: ' + u.id);
  return Number(m[1]);
}
/** La clave de la variante de un personaje que entra con «Solo el último uniforme»: sin uniformes, la base; con uniformes,
 *  el más nuevo. Se guarda hasta el próximo rebuild(). */
const _ULTIMO = new Map();
function ultimoUniforme (ch) {
  let k = _ULTIMO.get(ch.id);
  if (k) return k;
  if (!ch.uniforms.length) k = ch.id + '::base';
  else {
    const mejor = ch.uniforms.map(u => ({ u, ver: versionUniforme(u) }))
      .reduce((m, x) => !m || (cmpVersion(x.ver, m.ver) || numeroUniforme(x.u) - numeroUniforme(m.u)) > 0 ? x : m, null);
    k = ch.id + '::' + mejor.u.id;
  }
  _ULTIMO.set(ch.id, k);
  return k;
}
/** ¿Entra esta variante con «Solo el último uniforme»? */
function esUltimo (x) { return ultimoUniforme(x.ch) === x.key; }
/** Filas de la consulta en el orden elegido y con los filtros, una por trío de personajes: la
 *  primera en ese orden (el mejor uniforme de cada uno para ese orden) que pasa los filtros; con
 *  casillas de cobertura, la primera con ✓ en todas. Con tier lists, gana el trío mejor ubicado
 *  (suma de puestos); a igual puesto, más puntos para él; a igual puntaje, más strikers (desempatan);
 *  después, el mejor ubicado en tu lista de referencia. Los tríos descartados no van (o van solos, si
 *  se piden). Con «Solo el último uniforme», cada compañero con su uniforme más nuevo (esUltimo), y cuántas
 *  quedarían sin ese filtro: { filas, ocultos, sinUltimo (null sin el filtro) }. */
function vistaConsulta (q) {
  // Descartes en los que está él: los otros dos personajes de cada uno.
  const descartes = new Set(U.descartados.filter(d => d.includes(q.cid)).map(d => d.filter(c => c !== q.cid).join('|')));
  const clave = [ui.eqOrden, ui.eqExcluir.join(','), ui.eqCon, ui.eqCobertura.join(','), ui.eqUltimo, ui.eqVerDescartados,
                 [...descartes].join(',')].join('|');
  if (q.vista && q.vista.clave === clave) return q.vista;
  const ls = listasOrden(), ctx = contextoOrden();
  const pos = q.pool.map(x => ls.reduce((suma, l) => suma + puesto(l, x.key), 0));
  const ref = q.pool.map(x => rankIndex(x.key));
  const dpsCtx = ctx ? q.pool.map(x => rolEn(x, ctx).dps > 0) : null;
  // Con casillas de cobertura, el líder de cada fila, el de su tarjeta: en PvP y PvE, el del
  // contexto (sale de enContexto, acá abajo); si no, el de la sinergia (consultaCon).
  const cubre = ui.eqCobertura.length ? filtroCobertura(q, ui.eqCobertura) : null;
  const lider = cubre && (ctx ? new Uint8Array(q.n) : q.L);
  // Orden por una sola clave numérica por fila, de 64 bits: el orden nativo de un BigUint64Array es
  // varias veces más rápido que comparar de a pares. Cada parte entra en su lugar: si no entrara, el
  // orden saldría mal sin avisar. Sin contexto: puestos, puntos para él al revés, sus strikers al revés
  // (desempatan), referencia y fila, solo con los dos compañeros vinculados. En PvP y PvE: el puntaje
  // de contexto al revés (en centésimas: los pesos de la tabla de valor tienen decimales), los strikers
  // del trío al revés, los puestos, la referencia y la fila, si el trío entra, con cada compañero
  // vinculado o DPS de ese contexto. El liderazgo vincula con el líder de cada orden: sin contexto, el de
  // la sinergia; en PvP y PvE, el del contexto (vinculosFila). La clave son dos mitades de 31 bits: lo
  // que ordena primero y, abajo, la referencia y la fila.
  const claves = new BigUint64Array(q.n), vs = [q.v, null, null];
  const sirveEn = (f, i) => (f & 1 || dpsCtx[q.A[i]]) && (f & 2 || dpsCtx[q.B[i]]);
  let m = 0;
  for (let i = 0; i < q.n; i++) {
    const ps = pos[q.A[i]] + pos[q.B[i]], rf = ref[q.A[i]] + ref[q.B[i]];
    let pts, stk, tope;
    if (!ctx) {
      if (vinculosFila(q, i, q.L[i]) !== 3) continue;
      pts = q.P[i]; stk = q.S[i]; tope = 128;
    } else {
      // Antes de calcular el trío: ¿podría entrar con alguno de los tres de líder? En un trío con algún soporte que trae
      // algo que no se acumula, el vínculo por un soporte depende del líder: con cualquiera, el que puede (q.puede).
      const sv = q.svV || q.sv[q.A[i]] || q.sv[q.B[i]], a = q.A[i], b = q.B[i];
      const gs = sv ? (q.puede[a] ? 1 : 0) | (q.puede[b] ? 2 : 0) : q.G[i];
      if (!sirveEn(gs | (q.ld[a] || q.lv[a] ? 1 : 0) | (q.ld[b] || q.lv[b] ? 2 : 0), i)) continue;
      vs[1] = q.pool[a]; vs[2] = q.pool[b];
      const e = enContexto(vs, ctx);
      if (!e) continue;
      // El vínculo con el líder del contexto: si no es el de la sinergia y en el trío el soporte depende del líder, se cuenta con él,
      // salvo que no haga falta: si con el liderazgo y los DPS ya alcanza, la fila entra sea cual sea el vínculo por un soporte.
      const li = vs.indexOf(e.lider);
      const g = sv && li !== q.L[i] && (q.puede[a] || q.puede[b]) && !sirveEn(vinculosFila(q, i, li, 0), i) ? vinculosSoporte(vs, e.lider) : q.G[i];
      if (!sirveEn(vinculosFila(q, i, li, g), i)) continue;
      pts = Math.round(e.score * 100); stk = e.strikers; tope = 65536;
      if (lider) lider[i] = vs.indexOf(e.lider);
    }
    if (ps >= 4096 || pts < 0 || pts >= tope || stk >= 8 || rf >= 2048) throw new Error('orden de combinaciones fuera de rango: ' + [ps, pts, stk, rf]);
    const alto = ctx ? ((65535 - pts) * 8 + (7 - stk)) * 4096 + ps : (ps * 128 + (127 - pts)) * 8 + (7 - stk);
    claves[m++] = BigInt(alto) << 31n | BigInt(rf * 1048576 + i);
  }
  const ordenadas = claves.subarray(0, m).sort();
  const fuera = new Set(ui.eqExcluir), vistos = new Set(), filas = [];
  // Con «Solo el último uniforme», también las parejas que quedarían sin él (para decir cuántas quedan).
  const todas = ui.eqUltimo ? new Set() : null;
  let ocultos = 0, sinUltimo = 0;
  for (const k of ordenadas) {
    const i = Number(k & 0xFFFFFn);
    const a = q.pool[q.A[i]], b = q.pool[q.B[i]];
    if (fuera.has(a.cid) || fuera.has(b.cid) || (ui.eqCon && a.cid !== ui.eqCon && b.cid !== ui.eqCon)) continue;
    const pareja = a.cid < b.cid ? a.cid + '|' + b.cid : b.cid + '|' + a.cid;
    // Con casillas de cobertura, cada pareja va con su primera combinación de uniformes que las cumple.
    if (cubre && !cubre(i, lider[i])) continue;
    if (todas && !todas.has(pareja)) { todas.add(pareja); if (descartes.has(pareja) === ui.eqVerDescartados) sinUltimo++; }
    if (vistos.has(pareja) || (todas && !(esUltimo(a) && esUltimo(b)))) continue;
    vistos.add(pareja);
    const descartado = descartes.has(pareja);
    if (descartado) ocultos++;
    if (descartado === ui.eqVerDescartados) filas.push(i);
  }
  q.vista = { clave, filas, ocultos, sinUltimo: todas ? sinUltimo : null };
  return q.vista;
}
/** Un descarte: los tres personajes, en orden (vale para cualquier uniforme de cada uno). */
function trioDe (cids) { return cids.slice().sort(); }
function estaDescartado (cids) { const k = trioDe(cids).join('|'); return U.descartados.some(d => d.join('|') === k); }
function claveFavorito (keys) { return keys.slice().sort().join('|'); }
function esFavorito (keys) { const c = claveFavorito(keys); return U.favoritos.some(f => claveFavorito(f.members) === c); }
function estrella (keys) {
  const on = esFavorito(keys);
  return `<button class="btn sm icon estrella ${on ? 'on' : ''}" data-a="favorito" data-m="${keys.join(',')}"
    title="${h(t(on ? 'eq_fav_rm' : 'eq_fav_add'))}">${on ? '★' : '☆'}</button>`;
}
// Cobertura de un trío: lo que le dan al personaje sus compañeros, en cinco grupos (el ataque
// junta todas las categorías de ataque que le sirven).
const COBERTURA = [{ k: 'ataque', cats: CATEGORIAS.filter(c => c.ataque).map(c => c.k) },
  ...CATEGORIAS.filter(c => !c.ataque).map(c => ({ k: c.k, cats: [c.k] }))];
/** Los grupos en que la tarjeta muestra ✓: le llega algo de sus categorías, también si solo con
 *  un artefacto. En bits: el n, COBERTURA[n]. */
function gruposCubiertos (cob) {
  let bits = 0;
  COBERTURA.forEach((g, n) => { if (g.cats.some(c => c in cob)) bits |= 1 << n; });
  return bits;
}
/** Filtro de cobertura de vistaConsulta: (fila, líder) → ¿su tarjeta muestra ✓ en todos estos
 *  grupos? Líder: 0 él, 1 o 2 el compañero A o B de la fila, 3 ninguno. Como la cobertura es la
 *  suma de lo que le da cada integrante (aporte), se arma con lo de cada uno, calculado una vez
 *  con su liderazgo y sin él. */
function filtroCobertura (q, grupos) {
  const quiere = COBERTURA.reduce((bits, g, n) => grupos.includes(g.k) ? bits | 1 << n : bits, 0);
  const de = (a) => [gruposCubiertos(aporte(q.v, a, false)), gruposCubiertos(aporte(q.v, a, true))];
  const foco = de(q.v), pool = q.pool.map(de);
  return (i, li) => ((foco[li === 0 ? 1 : 0] | pool[q.A[i]][li === 1 ? 1 : 0] | pool[q.B[i]][li === 2 ? 1 : 0]) & quiere) === quiere;
}
function coberturaHtml (cob) {
  // ' *': solo le llega si el compañero lleva su artefacto.
  const nom = (c) => t('ct_' + c) + (c in cob && !cob[c] ? ' *' : '');
  const cubiertos = gruposCubiertos(cob);
  return `<div class="row cobertura">${COBERTURA.map((g, n) => {
    const cs = g.cats.filter(c => c in cob);
    const estado = !(cubiertos >> n & 1) ? 'no' : cs.some(c => cob[c]) ? 'si' : 'art';
    const nombre = g.k === 'ataque' ? t('cb_ataque') + (cs.length ? ': ' + cs.map(nom).join(', ') : '') : nom(g.k);
    return `<span class="tag cob ${estado}" ${cs.some(c => !cob[c]) ? `title="${h(t('cb_art'))}"` : ''}>${estado === 'no' ? '✗' : '✓'} ${h(nombre)}</span>`;
  }).join('')}</div>`;
}
/** De dónde salen los puntos de contexto de un trío (enContexto con detalle), en la ventana del «Por qué»: una parte del
 *  puntaje por renglón, con sus viñetas: los anti-mermas (en PvP), el liderazgo del líder (cada efecto y a quiénes les
 *  llega), los DPS con su fila, los soportes y bonos de equipo (de quién es cada soporte, con el enlace a su skill, y a
 *  quiénes les llega; cada bono) y los strikers, como desempate. Con los nombres cortos (el completo, en el title) y «a
 *  todos» si algo les llega a los tres. */
function detalleContexto (e, vs, ctx) {
  const nombre = nombreEn(vs), quien = (x) => nombreHtml(x, nombre), a = (ms) => aQuienesHtml(ms, vs, nombre);
  const partes = [], C = CONTEXTO[ctx];   // [rótulo (HTML), puntos o null, [viñetas (HTML)], con el «*» de un artefacto]
  if (C.requisito === 'anti_mermas') {
    const fuentes = new Map();
    // De cada uno, quién lo cubre: la fuente de anti-mermas que se le aplica (primeraAnti: lo propio, de sus skills o de su
    // soporte; el liderazgo del líder; o el soporte de otro, en el orden del equipo).
    vs.forEach(m => {
      const p = primeraAnti(m, vs, e.lider), clave = p.k === 'propio' ? 'cx_de_propio' : LIDERAZGOS.includes(p.k) ? 'cx_de_lid' : 'cx_de_sop';
      const k = clave + '|' + p.de.key;
      if (!fuentes.has(k)) fuentes.set(k, { p, clave, ms: [] });
      fuentes.get(k).ms.push(m);
    });
    partes.push([h(t('cx_anti')), null, [...fuentes.values()].map(f => `${h(t(f.clave)).replace('{x}', () => quien(f.p.de))
      .replace('{s}', () => h(f.p.k === 'propio' ? slotEs(f.p.x.sk.sl) : ''))} → ${a(f.ms)}`).concat(antiProbHtml(vs, nombre))]);
  }
  // Por stat que vale y activación: sus líneas (un liderazgo puede traer varias del mismo stat; cada una
  // con efectoSoporteTxt, que ya dice la activación), a quiénes llega y cuánto suma (su peso por cada uno). Las
  // de un liderazgo condicional cuentan la parte del condicional, y solo para quien no recibe el mismo stat de
  // uno permanente (cada stat cuenta una vez por integrante, la de más peso).
  // Uno que no se acumula suma si es el que se le aplica (como en ptsLiderazgo; la tabla de hoy no pesa ninguno).
  const grupos = new Map(), lleno = new Set(), slL = slotsDe(e.lider);
  slL.lid.forEach((x, n) => { for (const f of x.fx) {
    if (!C.vale.has(f.s)) continue;
    const k = f.s + '|' + (x.ac || '');
    const g = grupos.get(k) || { s: f.s, ac: x.ac, txt: [], ms: new Set(), no: new Map() };
    grupos.set(k, g);
    g.txt.push(efectoSoporteTxt(x, f) + srcTxt(x));
    vs.forEach(m => { if (!aplicaA(x, m) || !sirve(f, m)) return;
      if (!seAcumula(f)) { const p = fuenteQueSeAplica(m, f.s, vs, e.lider); if (!esLaFuente(p, e.lider, slL.lidK[n], x)) { g.no.set(m, [[f, p]]); return; } }
      g.ms.add(m); if (!x.ac) lleno.add(f.s + '|' + m.key); });
  } });
  const liderazgo = [...grupos.values()].map(g => {
    const ms = vs.filter(m => g.ms.has(m) && !(g.ac && lleno.has(g.s + '|' + m.key)));
    const pts = ms.length * C.peso[C.vale.get(g.s)] * (g.ac ? C.condicional : 1);
    return ms.length || g.no.size ? `${h(g.txt.join(' / ') + (g.ac ? ': ' + t('cx_lider_cond').replace('{p}', numTxt(C.condicional * 100)) : ''))} → ${
      a(ms)}${yaLoTienenHtml([...g.no], nombre)} ${ptsHtml(pts)}` : null;
  }).filter(Boolean);
  partes.push([h(t('cx_lider')).replace('{x}', () => quien(e.lider)), e.partes.lider, liderazgo.length ? liderazgo : [h(t('cx_lider_nada'))]]);
  const dps = vs.map((m, j) => ({ m, r: e.roles[j] })).filter(x => x.r.dps).map(({ m, r }) =>
    `${quien(m)} (${h(r.filas.filter(([l, fid]) => ROLES_LISTAS[ctx][l.id][fid][0] === 'dps')
      .map(([l, fid]) => `${listName(l)}: ${rowsOf(l).find(x => x.id === fid).label}`).join(', '))})`);
  partes.push([h(t('cx_dps')), e.partes.dps, dps]);
  // Cada soporte con a quiénes se les aplica y, atenuado, a quiénes les llega algo que ya tienen (con 0 si es lo único).
  if (e.sops.length || e.bonos.length) partes.push([h(t('cx_sinergia')), e.partes.sinergia, e.sops.map(x => `${quien(x.de)}: ${enlaceSkill(x)}${
      x.k === 'artifact' ? artPts(true) : ''} → ${a(x.a)}${yaLoTienenHtml(x.no, nombre)}${x.pts ? '' : ` <span class="muted pqrep">· ${h(t('rep_nada'))}</span>`}`)
    .concat(e.bonos.map(x => `${h(nombreBono({ b: x.b, integrantes: x.integrantes, i: 0 }, false))} → ${a(x.a)}`)), e.art]);
  // Los strikers no suman: se dicen como desempate, sin puntos.
  const st = strikersDe(vs, null);
  if (st.length) partes.push([desempateRotulo(st.length), null, st.map(x => strikerParHtml(x, nombre))]);
  return partesHtml(partes);
}
/** Los puntos de una línea del detalle de PvP o PvE: «(+2,5)». */
function ptsHtml (pts) { return `<span class="muted">(+${h(numTxt(pts))})</span>`; }
/** La nota de un orden de contexto (PvP o PvE): las reglas, con los pesos de la tabla de valor (MFF_VALOR). */
function notaContexto (ctx) {
  const C = CONTEXTO[ctx], listas = ctx === 'pvp' ? LISTAS_PVP : LISTAS_PVE;
  return t('cx_nota').replace('{c}', ctx === 'pvp' ? 'PvP' : 'PvE').replace('{l}', nombresListas(listas))
    .replace('{req}', C.requisito === 'anti_mermas'
      ? t('cx_req_anti').replace('{a}', VALOR.anti_mermas.map(trTxt).join(t('cx_o'))) : t('cx_req_no'))
    .replace('{stats}', C.liderazgo.map(x => trTxt(x.stat) + ' ' + numTxt(x.peso)).join(', '))
    .replace('{cond}', numTxt(C.condicional * 100)).replace('{dps}', numTxt(C.dps))
    .replace('{mejor}', listas.length > 1 ? t('cx_mejor_lista') : '')
    .replace('{sop}', numTxt(C.soporte)).replace('{bono}', numTxt(C.bono))
    + (VALOR.propuesta ? ' ' + t('cx_propuesta') : '');
}
function opcionHtml (val, txt, sel) { return `<option value="${h(val)}" ${val === sel ? 'selected' : ''}>${h(txt)}</option>`; }
function nombresListas (ids) { return ids.map(id => listName(listById(id))).join(' + '); }
/** El orden de las combinaciones: puntos para él, los contextos PvP y PvE, o una tier list. */
function ordenCombinacionesHtml () {
  return `<label>${h(t('eq_sort'))}
        <select data-a="eqOrden">
          ${opcionHtml('foco', t('eq_sort_foco'), ui.eqOrden)}
          ${opcionHtml('pvp', t('cx_orden').replace('{c}', 'PvP').replace('{l}', nombresListas(LISTAS_PVP)), ui.eqOrden)}
          ${opcionHtml('pve', t('cx_orden').replace('{c}', 'PvE').replace('{l}', nombresListas(LISTAS_PVE)), ui.eqOrden)}
          ${listasAgrupadas().map(gr => ({ k: gr.k, ls: gr.ls.filter(l => tipoLista(l) === 'personajes') })).filter(gr => gr.ls.length)
            .map(gr => `<optgroup label="${h(t(gr.k))}">${gr.ls.map(l => opcionHtml('lista:' + l.id, listName(l), ui.eqOrden)).join('')}</optgroup>`).join('')}
        </select></label>`;
}
function combinacionesHtml (v) {
  const cab = `<h3>${h(t('eq_new'))} ${ayudaHtml(t('eq_new_note') + ' ' + t('rep_regla') + ' ' + t('cb_note'))}</h3>`;
  const ctx = contextoOrden();
  // Sin función en el contexto, no hay lista: solo el aviso y el orden, para cambiarlo. Tampoco se
  // calcula la consulta.
  if (ctx && !tieneFuncion(v, ctx)) {
    return `<div class="section" id="combos">${cab}<div class="row eqfiltros">${ordenCombinacionesHtml()}</div>
      <p class="muted cxnota">${h(t('cx_sin_funcion_' + ctx).replace('{x}', fullLabel(v)).replace('{f}', filasFueraTxt(ctx))
        .replace('{l}', nombresListas(ctx === 'pvp' ? LISTAS_PVP : LISTAS_PVE)))}</p></div>`;
  }
  if (!CONSULTA || CONSULTA.clave !== v.key) {
    // La consulta tarda (más de un segundo con quien tiene un liderazgo para todos): primero
    // se pinta la pestaña con el aviso y recién después se calcula.
    if (ui.eqCalculando !== v.key) {
      ui.eqCalculando = v.key;
      requestAnimationFrame(() => setTimeout(() => { consultaCon(v); ui.eqCalculando = null; render(); volverAPosicion(); }, 0));
    }
    return `<div class="section" id="combos">${cab}<p class="muted">${h(t('eq_calc'))}</p></div>`;
  }
  const q = CONSULTA, { filas, ocultos, sinUltimo } = vistaConsulta(q), ls = listasOrden();
  const paginas = Math.max(1, Math.ceil(filas.length / POR_PAGINA));
  ui.eqPagina = Math.min(ui.eqPagina, paginas - 1);
  const personajes = CHARS.filter(c => c.id !== v.cid).sort((a, b) => a.name.localeCompare(b.name));
  const fila = (i) => {
    const vs = [v, q.pool[q.A[i]], q.pool[q.B[i]]], keys = vs.map(x => x.key);
    // En PvP y PvE, el líder y los puntos son los del contexto, y los de siempre (abajo) se cuentan con ese líder. De
    // dónde sale cada punto lo dice la ventana del «Por qué».
    const e = ctx ? enContexto(vs, ctx) : null, lider = e ? e.lider : liderDe(vs, null);
    const sc = synergy(vs, { foco: v, lider, soloPuntaje: true }), equipo = synergy(vs, { soloPuntaje: true, lider });
    return `<div class="card combo">
      <div class="combofila">
        ${estrella(keys)}${retratosEquipo(vs, v.key, lider)}
        <div class="combotx">
          <div>${h(vs.slice(1).map(fullLabel).join(' + '))}</div>
          <div class="combolider">${h(lider ? t('eq_leader').replace('{x}', fullLabel(lider)) : t('eq_no_leader'))}</div>
          ${coberturaHtml(cobertura(v, vs, lider))}
          ${ls.map(l => `<div class="muted">${h(listName(l))}: ${conLider(vs, lider).map(x => puestoHtml(l, x.key)).join(' · ')}</div>`).join('')}
        </div>
        ${ptsComboHtml(e, ctx, sc, equipo, e ? e.strikers : cuantosStrikers(vs, v))}
        ${botonArmar(conLider(vs, lider), '', '')}
        ${ui.eqVerDescartados
          ? `<button class="btn sm" data-a="restaurar" data-c="${vs.map(x => x.cid).join(',')}">${h(t('eq_restaurar'))}</button>`
          : `<button class="btn sm" data-a="descartar" data-c="${vs.map(x => x.cid).join(',')}" title="${h(t('eq_descartar_title'))}">${h(t('eq_descartar'))}</button>`}
      </div>
      ${porqueBoton('c|' + (ctx || '') + '|' + keys.join(','))}
    </div>`;
  };
  const numero = (n) => n.toLocaleString(LANG === 'es' ? 'es-AR' : 'en-US');
  const cuantos = (n, k) => t(n === 1 ? k + '_1' : k).replace('{n}', numero(n));
  return `<div class="section" id="combos">${cab}
    <div class="row eqfiltros">
      ${ordenCombinacionesHtml()}
      <label>${h(t('eq_con'))}
        <select data-a="eqCon">${opcionHtml('', t('eq_con_any'), ui.eqCon)}${personajes.map(c => opcionHtml(c.id, c.name, ui.eqCon)).join('')}</select></label>
      <label>${h(t('eq_excluir'))}
        <select data-a="eqExcluir">${opcionHtml('', t('eq_excluir_ph'), '')}${personajes.filter(c => !ui.eqExcluir.includes(c.id)).map(c => opcionHtml(c.id, c.name, '')).join('')}</select></label>
    </div>
    <div class="row" style="gap:6px;margin-bottom:10px"><div class="muted">${h(t('eq_comp'))}</div>
      <label class="chk" title="${h(t('eq_ultimo_t'))}"><input type="checkbox" data-a="eqUltimo"${ui.eqUltimo ? ' checked' : ''}> ${h(t('eq_ultimo'))}</label></div>
    ${ui.eqUltimo ? `<p class="muted cxnota ultnota">${h(t('eq_ultimo_nota').replace('{x}', fullLabel(v)))}</p>` : ''}
    <div class="row" style="gap:6px;margin-bottom:10px" title="${h(t('eq_cob_title'))}"><div class="muted">${h(t('eq_cob'))}</div>
      ${COBERTURA.map(g => `<label class="chk"><input type="checkbox" data-a="eqCobertura" data-g="${g.k}"${ui.eqCobertura.includes(g.k) ? ' checked' : ''}>
        ${h(g.k === 'ataque' ? t('cb_ataque') : t('ct_' + g.k))}</label>`).join('')}</div>
    ${ctx ? `<p class="muted cxnota">${h(notaContexto(ctx))}</p>` : ''}
    ${ui.eqExcluir.length ? `<div class="row" style="gap:6px;margin-bottom:10px">${ui.eqExcluir.map(cid =>
      `<button class="tag dim eqfuera" data-a="eqIncluir" data-cid="${h(cid)}" title="${h(t('eq_incluir'))}">${h(CHAR_BY_ID[cid].name)} ✕</button>`).join('')}</div>` : ''}
    <div class="row" style="justify-content:space-between;margin-bottom:10px">
      <span class="muted">${h((ui.eqVerDescartados ? cuantos(ocultos, 'eq_count_desc') : cuantos(filas.length, 'eq_count'))
        + (sinUltimo != null ? ' (' + t('eq_ultimo_de').replace('{n}', numero(sinUltimo)) + ')' : '')
        + (!ui.eqVerDescartados && ocultos ? ' · ' + cuantos(ocultos, 'eq_count_desc') : ''))}</span>
      ${ocultos || ui.eqVerDescartados ? `<button class="btn sm ${ui.eqVerDescartados ? 'primary' : ''}" data-a="eqVerDescartados">${h(ui.eqVerDescartados
        ? t('eq_ver_lista') : t('eq_ver_desc').replace('{n}', numero(ocultos)))}</button>` : ''}
    </div>
    ${filas.length ? filas.slice(ui.eqPagina * POR_PAGINA, (ui.eqPagina + 1) * POR_PAGINA).map(fila).join('')
                   : `<p class="muted">${h(t(ui.eqVerDescartados ? 'eq_none_desc' : 'eq_none_q'))}</p>`}
    ${pager(paginas, ui.eqPagina, 'eqPagina')}
  </div>`;
}
/** El resto: verificación entre fuentes y el retrato propio. */
function fichaFuentes (ch, v) {
  return `<div class="section" id="verif"><h3>${h(t('vf_title'))}</h3><div class="bloque">${usoVerificacion(ch, v)}</div></div>
  ${historialFicha(ch)}
  <div class="section"><h3>${h(t('d_portraits'))}</h3>
    <p class="muted" style="margin-bottom:10px">${h(t('d_portraits_note'))}</p>
    <div class="row">
      <label class="btn sm" style="cursor:pointer">${h(t('d_upload'))}<input type="file" accept="image/*" hidden data-a="upload" data-img="portrait-${v.id}"></label>
      ${U.images['portrait-' + v.id] ? `<button class="btn sm danger" data-a="clearImg" data-img="portrait-${v.id}">${h(t('d_revert_img'))}</button>` : ''}
    </div>
  </div>`;
}
/** Al cambiar de pestaña, el contenido arranca desde arriba (un poco debajo de la cabecera
 *  fija) si la página ya estaba más abajo. Sin animación: el contenido ya cambió. */
function irA (id) {
  const cab = document.querySelector('.fcab'), cuerpo = document.getElementById(id);
  if (!cab || !cuerpo) return;
  const destino = cuerpo.getBoundingClientRect().top + scrollY - document.querySelector('nav.topnav').offsetHeight - cab.offsetHeight - 14;
  if (scrollY > destino) window.scrollTo({ top: destino, behavior: 'instant' });
}

// ============================================================================
// HISTÓRICO (Ezequiel, 5 de octubre de 2026: «una pestaña de histórico... cada cambio con el link a su nota»; por ahora,
// solo los personajes). Lo arma scripts/historico.py (MFF_HISTORICO, datos de formato 10): las versiones del juego con su
// nombre y fecha (thanosvibs), las notas del foro oficial que van a cada una y los hechos: [clave, tipo, versión, nota,
// líneas de la nota en inglés, fecha si es una nota sin versión]. La clave de una llegada es la de la variante
// (cid::base o cid::uniforme); la de un hecho de balance, la del personaje (las notas no dicen el uniforme). Lo que no
// cierra entre las dos fuentes, en docs/HISTORICO.md.
// ============================================================================
const HISTORICO = window.MFF_HISTORICO;
const HI_TIPOS = ['personaje', 'uniforme', 't3', 'tp', 't4', 'balance'];
/** El personaje de un hecho. */
function cidHecho (x) { return x[0].split('::')[0]; }
/** Para qué variante o personaje es un hecho: su nombre, y el botón que abre su ficha. */
function hechoQuien (x) {
  const [cid, uid] = x[0].split('::');
  const v = variant(cid, uid || null);
  if (!v) throw new Error('el histórico nombra una variante que no está en el roster: ' + x[0]);
  const nom = uid ? fullLabel(v) : v.name;
  return `<button class="objlink" data-a="open" data-cid="${v.cid}" data-uid="${v.uid || ''}">${h(nom)}</button>`;
}
function notaLink (id) {
  const n = HISTORICO.notas[id];
  if (!n) throw new Error('el histórico cita una nota que no está en MFF_HISTORICO.notas: ' + id);
  return `<a href="${h(n[2])}" target="_blank" rel="noopener">${h(n[0].trim())}</a> <span class="muted">(${h(n[1])}${n[3] ? ', ' + h(t('hi_nota_err')) : ''})</span>`;
}
/** Un hecho dentro de la fila de su personaje: su tipo y, si la nota trae texto sobre él, el texto plegado (la primera
 *  línea a la vista). La nota misma va una vez, en la cabecera de la versión (#24: antes se repetía en cada hecho); acá
 *  solo si la versión tiene más de una, para decir de cuál sale, o si el hecho no tiene ninguna. */
function hechoHtml (x, variasNotas) {
  return `<span class="hihecho"><span class="tag dim">${h(t('hi_t_' + x[1]))}</span>
    ${x[3] != null ? (variasNotas ? `<span class="hinota">${notaLink(x[3])}</span>` : '') : (x[1] !== 'balance' ? `<span class="muted">${h(t('hi_sin_nota'))}</span>` : '')}
    ${x[4].length > 1 ? `<details><summary class="muted">${h(x[4][0])}</summary><ul class="hitexto" lang="en">${x[4].slice(1).map(l => `<li>${h(l)}</li>`).join('')}</ul></details>`
      : x[4].length ? `<span class="muted hitexto1" lang="en">${h(x[4][0])}</span>` : ''}</span>`;
}
/** Los grupos del histórico, del más nuevo al más viejo: una versión (con sus notas) o una nota sin versión, con sus
 *  hechos filtrados. */
function gruposHistorico (filtro) {
  const porV = new Map(), sinV = new Map();
  for (const x of HISTORICO.hechos) {
    if (!filtro(x)) continue;
    if (x[2] != null) { if (!porV.has(x[2])) porV.set(x[2], []); porV.get(x[2]).push(x); }
    else { if (!sinV.has(x[3])) sinV.set(x[3], []); sinV.get(x[3]).push(x); }
  }
  const out = HISTORICO.versiones.filter(v => porV.has(v[0])).map(v => ({ fecha: v[2], v, hechos: porV.get(v[0]) }));
  for (const [id, hs] of sinV) out.push({ fecha: HISTORICO.notas[id][1], nota: id, hechos: hs });
  return out.sort((a, b) => a.fecha < b.fecha ? 1 : a.fecha > b.fecha ? -1 : 0);
}
/** Una versión (o una nota sin versión), plegada (#24): a la vista su número, su nombre, su fecha y cuántos hechos de
 *  cada tipo trae; al abrirla, sus notas (una vez) y una fila por personaje con sus hechos. La primera va abierta. */
function grupoHistoricoHtml (g, conQuien, abierta) {
  const orden = (x) => HI_TIPOS.indexOf(x[1]);
  const notas = g.v ? g.v[3] : [g.nota], varias = notas.length > 1;
  const porQuien = new Map();
  for (const x of g.hechos.slice().sort((a, b) => orden(a) - orden(b))) { if (!porQuien.has(x[0])) porQuien.set(x[0], []); porQuien.get(x[0]).push(x); }
  const cuenta = HI_TIPOS.map(k => [k, g.hechos.filter(x => x[1] === k).length]).filter(([, n]) => n);
  const cab = g.v ? `<b>${h(g.v[0])}</b> · ${h(g.v[1])} · <span class="muted">${h(g.v[2])}</span>`
    : `<span class="muted">${h(t('hi_nota_sin_v').replace('{d}', HISTORICO.ventana))}</span>`;
  return `<details class="hiversion"${abierta ? ' open' : ''}><summary class="hicab"><span>${cab}</span>
      <span class="hicuenta">${cuenta.map(([k, n]) => `<span class="tag dim">${h(t('hi_t_' + k))} ${n}</span>`).join('')}</span></summary>
    ${notas.length ? `<div class="hinotas">${notas.map(notaLink).join('<br>')}</div>` : ''}
    <div class="hifilas">${[...porQuien.values()].map(hs => `<div class="hifila">${conQuien ? `<div class="hiquien">${hechoQuien(hs[0])}</div>` : ''}
      <div class="hihechos">${hs.map(x => hechoHtml(x, varias)).join('')}</div></div>`).join('')}</div></details>`;
}
function renderHistorico () {
  const pj = ui.hiPj, tipo = ui.hiTipo;
  const grupos = gruposHistorico(x => (!pj || cidHecho(x) === pj) && (tipo === 'todos' || x[1] === tipo));
  const personajes = CHARS.slice().sort((a, b) => a.name.localeCompare(b.name));
  return `<div class="page-head"><div><h1>${h(t('hi_title'))} ${ayudaHtml(t('hi_note'))}</h1></div></div>
    <div class="row" style="gap:10px;margin-bottom:12px;flex-wrap:wrap">
      <label>${h(t('hi_pj'))} <select data-a="hiPj">${opcionHtml('', t('hi_pj_todos'), pj)}${personajes.map(c => opcionHtml(c.id, c.name, pj)).join('')}</select></label>
      <div class="seg">${['todos'].concat(HI_TIPOS).map(k => `<button class="${tipo === k ? 'on' : ''}" data-a="hiTipo" data-v="${k}">${h(t(k === 'todos' ? 'hi_t_todos' : 'hi_t_' + k))}</button>`).join('')}</div>
    </div>
    <p class="muted">${h(t('hi_cuenta').replace('{n}', grupos.length))}</p>
    ${grupos.length ? grupos.slice(0, ui.hiN).map((g, i) => grupoHistoricoHtml(g, true, i === 0)).join('') : `<p class="muted">${h(t('hi_vacio'))}</p>`}
    ${grupos.length > ui.hiN ? `<button class="btn" data-a="hiMas">${h(t('hi_mas'))}</button>` : ''}`;
}
/** El bloque «Historial» de la ficha: lo del personaje, de lo más nuevo a lo más viejo, con el link al Histórico. */
function historialFicha (ch) {
  const grupos = gruposHistorico(x => cidHecho(x) === ch.id);
  return `<div class="section" id="historial"><h3>${h(t('hi_ficha'))}</h3>
    ${grupos.length ? grupos.map((g, i) => grupoHistoricoHtml(g, true, i === 0)).join('') : `<p class="muted">${h(t('hi_vacio'))}</p>`}
    <p><button class="btn sm" data-a="goHistorico" data-cid="${ch.id}">${h(t('hi_ficha_ver'))}</button></p></div>`;
}

// ============================================================================
// GLOSARIO
// El glosario de skills del juego (scripts/contenido/glosario.json): qué dice cada término y lo
// que el inglés traduce distinto del coreano, que es el original. Y todos los efectos del catálogo,
// por grupo, con sus lecturas de PvE y de PvP, a quién le sirven y cómo aparecen en las skills.
// ============================================================================
/** Para buscar: sin tildes ni mayúsculas. */
function plano (s) { return String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
function nombreGl (x) { return LANG === 'es' ? x.es : x.en; }
/** Los otros nombres de un término: el inglés (si la app está en español y es distinto) y el coreano. */
function otrosNombresGl (x) { return [LANG === 'es' && x.en !== x.es ? x.en : '', x.ko].filter(Boolean); }
function enlaceGl (destino, texto, titulo) {
  return `<a href="#${destino}" class="tag ghost" data-a="irGlos" data-v="${destino}"${titulo ? ` title="${h(titulo)}"` : ''}>${h(texto)}</a>`;
}
/** Un término del juego, plegado (#24): a la vista sus nombres, lo que dice en una línea y sus marcas (el inglés
 *  difiere, lo da un C.T.P.); al abrirlo, el texto entero, lo que el inglés traduce distinto, qué C.T.P. lo da y de
 *  qué opción sale, la nota y a qué efectos del catálogo corresponde. */
function terminoGl (x, errores) {
  const otros = otrosNombresGl(x).join(' · ');
  return `<details class="glitem" id="gl-${x.id}">
    <summary><span class="glnom"><b>${h(nombreGl(x))}</b><span class="muted">${h(otros)}</span></span>
      <span class="glcorto">${h(bi(x.que))}</span>
      <span class="glmarcas">${x.difiere ? `<span class="tag solid gldif">${h(t('gl_difiere_tag'))}</span>` : ''}
        ${x.ctp ? `<span class="tag dim">C.T.P.</span>` : ''}
        ${x.falta ? `<span class="tag dim">${h(t('gl_falta_' + x.falta))}</span>` : ''}</span></summary>
    <div class="glcuerpo">
    <p>${h(bi(x.que))}</p>
    ${x.difiere ? `<div class="gldifbox"><b>${h(t('gl_en_ko'))}</b> ${h(bi(x.difiere))}
      ${x.error ? `<div class="row">${enlaceGl('gle-' + x.error, bi(errores[x.error].titulo))}</div>` : ''}</div>` : ''}
    ${x.ctp ? `<div class="muted">${h(t('gl_lo_da'))} ${x.ctp.map(c => `${h(CTPS.find(k => k.id === c.id).name)} (<span title="${
      h(t('gl_op_' + c.opcion + '_t'))}">${h(t('gl_op_' + c.opcion))}</span>)`).join(', ')}</div>` : ''}
    ${x.nota ? `<div class="muted">${h(bi(x.nota))}</div>` : ''}
    ${x.efectos.length ? `<div class="row"><span class="muted">${h(t('gl_en_catalogo'))}</span>${
      x.efectos.map(id => enlaceGl('ef-' + id, bi(GL_DE[id].e))).join('')}</div>` : ''}
    <div class="fuentes">${fuentesHtml(x.fuente)}</div></div>
  </details>`;
}
/** Los errores del inglés que se repiten, con sus términos, y las otras diferencias: plegados, con cuántos son. */
function erroresGl () {
  const otras = GLOSARIO.terminos.filter(x => x.difiere && !x.error);
  return `<details class="glerrs"><summary>${h(t('gl_errores_sum').replace('{n}', GLOSARIO.errores.length).replace('{m}', otras.length))}</summary>
    ${GLOSARIO.errores.map(e => `<div class="glerr" id="gle-${e.id}"><b>${h(bi(e.titulo))}</b><p>${h(bi(e.texto))}</p>
      <div class="row">${GLOSARIO.terminos.filter(x => x.error === e.id).map(x => enlaceGl('gl-' + x.id, nombreGl(x))).join('')}</div></div>`).join('')}
    <h4 class="glh4">${h(t('gl_otras'))}</h4>
    ${otras.map(x => `<div class="glotra">${enlaceGl('gl-' + x.id, nombreGl(x))} ${h(bi(x.difiere))}</div>`).join('')}
  </details>`;
}
/** Un efecto del catálogo, plegado: a la vista su nombre, el inglés y los términos del juego que le corresponden; al
 *  abrirlo, sus lecturas de PvE y de PvP, su nota, a quién le sirve, si se suma, su tope y con qué etiquetas aparece. */
function efectoGl (e) {
  const d = GL_DE[e.id];
  return `<details class="glitem glef" id="ef-${e.id}">
    <summary><span class="glnom"><b>${h(bi(e))}</b>${LANG === 'es' ? `<span class="muted">${h(e.en)}</span>` : ''}</span>
      <span class="glcorto">${h(t('gl_le_sirve'))} ${h(minuscula(bi(CATALOGO.sirve[e.sirve])))}</span>
      <span class="glmarcas">${resumenAcumula(d)}${d.terminos.map(x => `<span class="tag ghost" title="${h(t('gl_termino'))}">${h(nombreGl(x))}</span>`).join('')}</span></summary>
    <div class="glcuerpo">
    ${d.terminos.length ? `<div class="row">${d.terminos.map(x => enlaceGl('gl-' + x.id, nombreGl(x) + ' · ' + x.ko, t('gl_termino'))).join('')}</div>` : ''}
    ${lecturasAn(e.pve, e.pvp)}
    ${e.nota ? `<div class="muted annota">${h(bi(e.nota))}</div>` : ''}
    ${leSirveEfectoHtml(e, (r, x) => `<div class="muted annota">${r} ${x}</div>`)}
    ${acumulaEfectoHtml(e, (r, x) => `<div class="muted annota">${r} ${x}</div>`)}
    ${topeEfectoHtml(e, (r, x) => `<div class="muted annota">${r} ${x}</div>`)}
    ${d.etiquetas.length ? `<div class="glet"><span class="muted">${h(t('gl_en_skills'))}</span>${
      d.etiquetas.map(i => `<span class="tag dim">${h(txt('ab', i))}</span>`).join('')}</div>` : ''}</div>
  </details>`;
}
/** La marca corta de si se suma o cuenta una vez y del tope, para la línea del efecto; nada si sus stats no coinciden
 *  (el detalle lo dice uno por uno). */
function resumenAcumula (d) {
  const sts = d.stats;
  if (!sts.length) return '';
  const a = CATALOGO.soporte[sts[0]].acumula, iguales = sts.every(st => CATALOGO.soporte[st].acumula === a);
  const topes = sts.flatMap(topesDe);
  return `${iguales ? `<span class="tag dim">${h(t(a ? 'gl_se_suma' : 'gl_una_vez_corto'))}</span>` : ''}${
    topes.length ? `<span class="tag dim">${h(t('gl_tope_corto'))} ${h(topeTxt(topes[0], false))}</span>` : ''}`;
}
// GLOSARIO EN DOS PESTAÑAS (#24, caso del 6 de octubre de 2026): lo que es del juego (sus 44 términos) separado de lo que es
// de la app (su catálogo de efectos, por grupo). Cada entrada a la vista en una línea, con el detalle plegado. La
// búsqueda vale para las dos y dice cuántas hay en la otra.
function renderGlosario () {
  const q = plano(ui.glBusca.trim());
  const pasa = (...nombres) => !q || nombres.some(n => plano(n).includes(q));
  const terminos = GLOSARIO.terminos.filter(x => pasa(x.es, x.en, x.ko));
  const efectos = CATALOGO.efectos.filter(e => { const d = GL_DE[e.id];
    return pasa(e.es, e.en, ...d.terminos.flatMap(x => [x.es, x.en, x.ko]), ...d.etiquetas.flatMap(i => [fila('ab', i).en, txt('ab', i)])); });
  const errores = Object.fromEntries(GLOSARIO.errores.map(e => [e.id, e]));
  const juego = ui.glTab === 'juego', aca = juego ? terminos.length : efectos.length, otra = juego ? efectos.length : terminos.length;
  return `<div class="page-head"><div><h1>${h(t('gl_title'))} ${ayudaHtml(t('gl_note'))}</h1></div></div>
    <div class="row glbusca"><div class="search"><input id="q" placeholder="${h(t('gl_busca'))}" value="${h(ui.glBusca)}" data-a="glBusca"></div>
      <div class="seg gltabs" role="tablist">
        <button class="${juego ? 'on' : ''}" role="tab" aria-selected="${juego}" data-a="glTab" data-v="juego">${h(t('gl_tab_juego').replace('{n}', terminos.length))}</button>
        <button class="${juego ? '' : 'on'}" role="tab" aria-selected="${!juego}" data-a="glTab" data-v="app">${h(t('gl_tab_app').replace('{n}', efectos.length))}</button>
      </div>
      ${q && otra ? `<span class="muted">${h(t('gl_en_otra').replace('{n}', otra))}</span>` : ''}</div>
    ${!aca ? `<div class="empty"><div>${h(t('gl_nada'))}</div></div>` : ''}
    ${juego ? `${q ? '' : erroresGl()}
      ${terminos.length ? `<div class="section"><h3>${h(t('gl_terminos'))} ${ayudaHtml(t('gl_terminos_nota').replace('{n}', GLOSARIO.terminos.length))}</h3>
        <div class="gllista">${terminos.map(x => terminoGl(x, errores)).join('')}</div></div>` : ''}`
    : `<p class="glaviso">${h(t('gl_app_aviso'))}</p>
      ${efectos.length ? `<div class="section"><h3>${h(t('gl_efectos'))} ${ayudaHtml(t('gl_efectos_nota'))}</h3>
      ${CATALOGO.grupos.filter(g => efectos.some(e => e.grupo === g.id)).map(g => `<div class="glgrupo">
        <div class="angh"><b>${h(bi(g))}</b> <span class="muted">${h(bi(g.que))}</span>
          ${g.pve || g.pvp ? `<details class="ayuda"><summary title="${h(t('ay_label'))}" aria-label="${h(t('ay_label'))}">?</summary><div class="ayudatx">${lecturasAn(g.pve, g.pvp)}</div></details>` : ''}</div>
        <div class="gllista">${efectos.filter(e => e.grupo === g.id).map(efectoGl).join('')}</div>
      </div>`).join('')}</div>` : ''}`}`;
}

// ============================================================================
// COMPARACIÓN
// ============================================================================
const CMP_FX = 6;                      // efectos de cada skill a la vista; el resto, plegado
function renderCompare () {
  const vs = ui.picks.map(p => variant(p.cid, p.uid)).filter(Boolean);
  if (vs.length < 2) { ui.view = 'roster'; return renderRoster(); }
  const same = (get) => { const m = {}; vs.forEach(v => { const k = get(v); m[k] = (m[k] || 0) + 1; }); return m; };
  const cC = same(v => v.c), cF = same(v => v.f), cT = same(v => v.t), cI = same(v => v.ins);
  const slots = SLOT_ORDER.filter(sl => vs.some(v => v.skills.some(sk => sk.sl === sl)));
  const car = vs.map(v => cargas(v.skills));
  const syn = synergy(vs), razones = razonesTxt(syn.razones);
  const cell = (v, txt, counts, key) => `<td class="${counts && counts[key] > 1 ? 'same' : ''}">${txt}</td>`;
  // Los efectos de una skill: los primeros CMP_FX a la vista y el resto plegado, con cuántos son.
  const fxCmp = (f) => `<div class="cmpfx"><span class="fxtag">${h(txt('ab', f.a))}</span>${
    marcadores(h(txt('desc', f.p, f.v).replace(/<br\s*\/?>/gi, ' ')), f)}</div>`;
  const attr = (label, fn) => `<tr><th>${h(label)}</th>${vs.map(v => `<td>${fn(v)}</td>`).join('')}</tr>`;

  return `
  <div class="row" style="margin-bottom:14px"><button class="btn sm" data-a="back">${h(t('back_roster'))}</button></div>
  <div class="page-head"><div><h1>${h(t('cmp_title'))}</h1>
    <div class="sub">${h(t('cmp_note'))}</div></div></div>
  <div class="cmp"><table class="cmpt">
    <thead><tr><th></th>${vs.map(v => `<th><div class="cmphead">
      ${imgUrl('portrait-' + v.id) ? `<img src="${imgUrl('portrait-' + v.id)}" alt="">` : ''}
      <div><div style="font-weight:700;font-size:14px">${h(v.uid ? v.sub : v.name)}</div>
      <div class="muted">${h(v.uid ? v.name : t('base'))}</div></div>
      <button class="btn sm danger" data-a="unpick" data-cid="${v.cid}" data-uid="${v.uid || ''}">${h(t('cmp_remove'))}</button>
    </div></th>`).join('')}</tr></thead>
    <tbody>
      <tr><th>${h(t('f_class'))}</th>${vs.map(v => cell(v, tagGhost(dom(v.c), classColor(v.c)), cC, v.c)).join('')}</tr>
      <tr><th>${h(t('f_tier'))}</th>${vs.map(v => cell(v, tagSolid(v.t, tierColor(v.t)) + transTag(v.trans), cT, v.t)).join('')}</tr>
      <tr><th>${h(t('f_side'))}</th>${vs.map(v => cell(v, h(dom(v.f)), cF, v.f)).join('')}</tr>
      <tr><th>${h(t('c_instinct'))}</th>${vs.map(v => cell(v, h(v.ins === 'Desconocido' ? '—' : dom(v.ins)), cI, v.ins)).join('')}</tr>
      ${attr(t('c_roles'), v => v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}">${h(dom(r))}</span>`).join(' '))}
      ${attr(t('c_striker'), v => v.striker != null ? 'Skill ' + h(v.striker) : '—')}
      ${attr(t('c_worldboss'), v => icon(v.wba) + h(dom(v.wba) || '—'))}
      ${attr(t('cmp_abilities'), v => (v.ab || []).map(a => `<span class="tag dim">${h(dom(a))}</span>`).join(' ') || '—')}
      ${attr(t('cmp_cost'), v => h(v.cost || '—'))}
      <tr><th>${h(t('c_ult'))}</th>${vs.map((v, i) => `<td class="num">${car[i].ult}%</td>`).join('')}</tr>
      <tr><th>${h(t('c_striker'))}</th>${vs.map((v, i) => `<td class="num">${car[i].stk}%</td>`).join('')}</tr>
      <tr><th>${h(t('c_dmg_total'))}</th>${vs.map(v => `<td class="num">${danoTotal(v.skills)}%</td>`).join('')}</tr>
      <tr><th>${h(t('c_attrs'))}</th>${vs.map(v => { const a = [...atributosDe(v.p, v.skills)];
        return `<td>${a.length ? a.map(k => `<span class="tag atributo">${h(atrNombre(k))}</span>`).join(' ')
                               : '<span class="muted">—</span>'}</td>`; }).join('')}</tr>
      <tr><th>${h(t('c_targets'))}</th>${vs.map(v => { const o = [...objetivosDe(v.skills)];
        return `<td>${o.length ? o.map(i => objetivoTag(i)).join(' ')
                               : '<span class="muted">—</span>'}</td>`; }).join('')}</tr>
      <tr><th>${h(t('c_keybuffs'))}</th>${vs.map(v => `<td>${
        Object.keys(BUFFS[v.p] || {}).map(b => `<span class="tag dim">${h(b)}</span>`).join(' ') || '—'}</td>`).join('')}</tr>
      <tr><th>${h(t('c_uni_cost'))}</th>${vs.map(v => `<td>${v.up
        ? `<div class="muted">${h(t('d_kits'))}: ${(v.up.uniform_kits || []).reduce((a, b) => a + b, 0)}
           · ${h(t('d_gold'))}: ${((v.up.gold || []).reduce((a, b) => a + b, 0) / 1000).toFixed(0)}k
           · ${h(t('d_xp'))}: ${((v.up.uniform_xp || []).reduce((a, b) => a + b, 0) / 1000).toFixed(0)}k</div>`
        : '<span class="muted">—</span>'}</td>`).join('')}</tr>
      ${LISTS.filter(l => vs.some(v => indicesFila(l, v.key).length)).map(l => {
        const rows = rowsOf(l);
        return `<tr><th>${h(listName(l))}</th>${vs.map(v => {
          const idx = indicesFila(l, v.key);
          return `<td>${!idx.length ? `<span class="muted">${h(t('cmp_unplaced'))}</span>`
            : idx.map(i => `<span class="tag solid" style="background:${rowColor(i, rows.length)}">${h(rows[i].label)}</span>`).join(' ')}</td>`;
        }).join('')}</tr>`;
      }).join('')}
      ${slots.map(sl => `<tr class="slotrow"><th>${h(slotEs(sl))}</th>${vs.map(v => {
        const sk = v.skills.find(x => x.sl === sl);
        if (!sk) return `<td><span class="muted">${h(t('cmp_missing_slot'))}</span></td>`;
        const dmg = [];
        (sk.st || []).forEach(st => (st.fx || []).forEach(f => { const d = dano(f); if (d) dmg.push(d); }));
        const otros = [];
        (sk.st || []).forEach(st => (st.fx || []).forEach(f => { if (!esDano(f)) otros.push(f); }));
        const tgC = comunEnEtapas(sk, 'tg'), acC = comunEnEtapas(sk, 'ac');
        const mk = marcasDe(v.p, sk.sl);
        return `<td><div style="font-weight:600;margin-bottom:4px">${nombreSkill(sk)}</div>
          ${Object.keys(mk).length ? `<div class="row" style="margin-bottom:5px">${
            ATRIBUTOS.filter(a => mk[a.k]).map(a => `<span class="tag atributo">${h(a[LANG])}</span>`).join('')}</div>` : ''}
          ${esAjeno(tgC) ? `<div class="row" style="margin-bottom:5px">${objetivoTag(tgC, true)}</div>` : ''}
          ${acC != null ? `<div class="muted" style="margin-bottom:5px">${h(t('st_activation'))}: ${h(txt('act', acC, (sk.st.find(x => x.ac === acC) || {}).av))}</div>` : ''}
          ${(sk.st || []).some(st => st.tg != null && st.tg !== tgC)
            ? `<div class="muted" style="margin-bottom:5px">${(sk.st || []).filter(st => st.tg != null && st.tg !== tgC)
                .map((st, i) => `${h(t('st_stage'))} ${(sk.st.indexOf(st) + 1)}: ${objetivoTexto(st.tg)}`).join(' · ')}</div>` : ''}
          <div class="row" style="gap:4px;margin-bottom:6px">
            ${recargaHtml(v, sk)}
            ${sk.ult != null ? `<span class="tag dim">${h(t('c_ult'))} ${h(sk.ult)}%</span>` : ''}
            ${sk.stk != null ? `<span class="tag dim">${h(t('c_striker'))} ${h(sk.stk)}%</span>` : ''}
          </div>
          ${dmg.length ? `<div class="muted" style="margin-bottom:5px">${dmg.map(d =>
             `<b>${h(d.pct)}%</b>${d.flat != null ? ' +' + h(d.flat) : ''}`).join(' · ')}</div>` : ''}
          ${otros.slice(0, CMP_FX).map(fxCmp).join('')}
          ${otros.length > CMP_FX ? `<details class="cmpmas"><summary>${h(t(otros.length - CMP_FX === 1 ? 'cmp_mas_1' : 'cmp_mas')
            .replace('{n}', otros.length - CMP_FX))}</summary>${otros.slice(CMP_FX).map(fxCmp).join('')}</details>` : ''}</td>`;
      }).join('')}</tr>`).join('')}
    </tbody>
  </table></div>
  <div class="card" style="margin-top:18px">
    <div class="row" style="justify-content:space-between;margin-bottom:8px">
      <h3 style="margin:0">${h(t('cmp_synergy'))}</h3><span class="muted">${syn.score}${artPts(syn.art)} ${h(t('cmp_pts'))}</span></div>
    <div style="height:5px;background:var(--surface-3);border-radius:3px;overflow:hidden;margin-bottom:10px">
      <div style="height:100%;width:${Math.min(100, syn.score * 12)}%;background:linear-gradient(90deg,var(--accent),var(--gold))"></div></div>
    ${razones.length ? `<ul style="margin:0;padding-left:18px">${razones.map(r => `<li>${h(r)}</li>`).join('')}</ul>`
      : `<p class="muted">${h(t('cmp_no_synergy'))}</p>`}
    <p class="muted" style="margin-top:10px">${h(t('cmp_heuristic'))}</p>
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
  const items = itemsDeLista(list);
  const byRow = {}; rows.forEach(r => { byRow[r.id] = []; });
  const unset = [];
  let ubicados = 0, ubicaciones = 0;
  items.forEach(it => {
    const fs = (a[it.key] || []).filter(r => byRow[r]);
    if (fs.length) { fs.forEach(r => byRow[r].push(it)); ubicados++; ubicaciones += fs.length; } else unset.push(it);
  });
  const imported = TIERLISTS_SEED.some(l => l.id === list.id);
  // Tocar una ficha abre el selector de filas (sirve en el celular, donde no hay
  // arrastrar y soltar); en la compu también se puede arrastrar para moverla.
  const chip = (it, fila) => `<span class="tlchip" draggable="true" data-a="tlAbrir" data-key="${h(it.key)}" data-from="${h(fila)}"
      title="${h(it.sub ? it.nom + ' — ' + it.sub : it.nom)}">
      ${it.img ? `<img src="${it.img}" alt="" loading="lazy">` : ''}
      <span class="who">${h(it.nom)}</span>${it.sub ? `<span class="what">${h(it.sub)}</span>` : ''}
      ${(a[it.key] || []).length > 1 ? `<span class="multi" title="${h(t('tl_multi'))}">×${a[it.key].length}</span>` : ''}
      ${fila ? `<span class="x" data-a="unassign" data-key="${h(it.key)}" data-row="${h(fila)}" title="${h(t('tl_remove_row'))}">✕</span>` : ''}</span>`;
  const conteo = `<span class="tag dim">${ubicados} ${h(t('tl_placed'))}${ubicaciones > ubicados ? ` · ${ubicaciones} ${h(t('tl_spots'))}` : ''}</span>`;

  return `
  <div class="page-head"><div><h1>${h(t('tl_title'))}</h1>
    <div class="sub">${h(t('tl_note'))}</div></div>
    <div class="row">
      <input placeholder="${h(t('tl_new_ph'))}" value="${h(ui.newListName)}" data-a="newListName" style="width:220px">
      <select data-a="newListKind" title="${h(t('tk_title'))}">${TIPOS_LISTA.map(([id, k]) =>
        `<option value="${id}" ${id === ui.newListKind ? 'selected' : ''}>${h(t(k))}</option>`).join('')}</select>
      <select data-a="newListTpl" title="${h(t('tp_title'))}">${PLANTILLAS.map(p =>
        `<option value="${p.id}" ${p.id === ui.newListTpl ? 'selected' : ''}>${h(t(p.k))}</option>`).join('')}</select>
      <button class="btn" data-a="addList">${h(t('tl_create'))}</button>
    </div>
  </div>
  <div class="tlbar">${listasAgrupadas().map(gr => `<div class="tlgroup"><span class="tlglabel">${h(t(gr.k))}</span>
    ${gr.ls.map(l => `<button class="chip ${l.id === list.id ? 'on' : ''}" data-a="pickList" data-id="${l.id}"
      title="${h(l.author ? l.author + (l.gameVersion ? ' · ' + l.gameVersion : '') : '')}">${h(listName(l))}</button>`).join('')}</div>`).join('')}</div>
  <div class="tlsource">
    ${imported
      ? `<span>${h(t('tl_source'))} <a href="https://thanosvibs.money/tierlist" target="_blank" rel="noopener">THANO$VIB$</a> · «${h(list.source)}»</span>
         ${list.author ? `<span class="tag dim">${h(t('tl_author'))} ${h(list.author)}</span>` : ''}
         ${list.gameVersion ? `<span class="tag dim">${h(t('tl_game'))} ${h(list.gameVersion)}</span>` : ''}
         ${list.published ? `<span class="tag dim">${h(t('tl_published'))} ${h(list.published)}</span>` : ''}
         ${list.ratings ? `<span class="tag dim" title="${h(t('tl_rating_title'))}">★ ${h(list.rating)} · ${h(list.ratings)} ${h(t('tl_votes'))}</span>` : ''}
         ${(list.tags || []).map(x => `<span class="tag ghost" style="color:var(--text-3)">${h(x)}</span>`).join('')}
         ${conteo}`
      : `<span>${h(t('tl_own'))}</span>
         <input value="${h(list.name)}" data-a="listName" data-id="${list.id}" title="${h(t('tl_rename'))}" style="width:220px;padding:5px 9px">
         <span class="tag dim">${h(t((TIPOS_LISTA.find(x => x[0] === tipoLista(list)) || TIPOS_LISTA[0])[1]))}</span>
         ${conteo}
         <button class="btn sm ${ui.editRows ? 'primary' : ''}" data-a="editRows">${h(ui.editRows ? t('tl_rows_done') : t('tl_rows_edit'))}</button>
         <button class="btn sm danger" data-a="removeList" data-id="${list.id}">${h(t('tl_delete'))}</button>`}
    ${imported ? `<button class="btn sm" data-a="dupList" data-id="${list.id}" title="${h(t('tl_dup_title'))}">${h(t('tl_dup'))}</button>` : ''}
    ${imported && U.assign[list.id] && Object.keys(U.assign[list.id]).length
      ? `<button class="btn sm" data-a="resetList" data-id="${list.id}">${h(t('tl_undo'))} (${Object.keys(U.assign[list.id]).length})</button>` : ''}
  </div>
  ${list.description || list.notes ? `<div class="tlmeta">
    ${list.description ? `<details><summary>${h(t('tl_description'))}</summary><p class="autor">${h(list.description)}</p></details>` : ''}
    ${list.notes ? `<details><summary>${h(t('tl_notes'))}</summary><p class="autor">${h(list.notes)}</p></details>` : ''}
    <span class="muted">${h(t('tl_author_lang'))}</span>
  </div>` : ''}
  ${esPropia(list) && ui.editRows ? `<div class="card roweditor">
    ${rows.map((r, i) => `<div class="row">
      <span class="tag solid" style="background:${rowColor(i, rows.length)};min-width:26px;justify-content:center">${i + 1}</span>
      <input value="${h(r.label)}" data-a="rowLabel" data-row="${h(r.id)}" style="flex:1;min-width:140px">
      <button class="btn sm icon" data-a="rowMove" data-row="${h(r.id)}" data-dir="-1" ${i === 0 ? 'disabled' : ''} title="${h(t('tl_row_up'))}">↑</button>
      <button class="btn sm icon" data-a="rowMove" data-row="${h(r.id)}" data-dir="1" ${i === rows.length - 1 ? 'disabled' : ''} title="${h(t('tl_row_down'))}">↓</button>
      <button class="btn sm danger icon" data-a="rowDel" data-row="${h(r.id)}" ${rows.length === 1 ? 'disabled' : ''} title="${h(t('tl_row_del'))}">✕</button>
    </div>`).join('')}
    <div class="row"><button class="btn sm" data-a="rowAdd">${h(t('tl_row_add'))}</button>
      <span class="muted">${h(t('tl_rows_note2'))}</span></div>
  </div>` : ''}
  ${rows.map((r, i) => `<div class="tierrow" data-a="drop" data-row="${h(r.id)}">
    <div class="tierlabel" style="background:${rowColor(i, rows.length)}">${h(r.label)}</div>
    <div class="tieritems">${byRow[r.id].map(v => chip(v, r.id)).join('') || `<span class="muted" style="align-self:center">${h(t('tl_drop_here'))}</span>`}</div>
  </div>`).join('')}
  <div style="margin-top:18px">
    <div class="row">
      <button class="btn sm" data-a="togglePool">${h(ui.poolOpen ? t('tl_hide_pool') : t('tl_show_pool'))} (${unset.length})</button>
      ${ui.poolOpen ? `<input placeholder="${h(t('tl_filter'))}" value="${h(ui.poolSearch)}" data-a="poolSearch" style="width:220px">` : ''}
    </div>
    ${ui.poolOpen ? (() => {
      const q2 = ui.poolSearch.trim().toLowerCase();
      const pool = (q2 ? unset.filter(it => (it.nom + ' ' + it.sub).toLowerCase().includes(q2)) : unset);
      return `<div class="tieritems" data-a="drop" data-row="" style="margin-top:10px;max-height:360px;overflow-y:auto;
        border:1px dashed var(--line-2);border-radius:var(--r-md)">
        ${pool.slice(0, 150).map(it => chip(it, '')).join('') || `<span class="muted">${h(t('tl_nothing'))}</span>`}
        ${pool.length > 150 ? `<span class="muted" style="align-self:center">…${pool.length - 150} ${h(t('tl_more'))}</span>` : ''}
      </div>`;
    })() : ''}
  </div>
  ${ui.tlPick ? selectorFilas(list, rows, a, items) : ''}`;
}

/** Selector de filas de una entrada: una casilla por fila, así puede estar en varias. */
function selectorFilas (list, rows, a, items) {
  const it = items.find(x => x.key === ui.tlPick);
  if (!it) { ui.tlPick = null; return ''; }
  const v = it.v, mias = a[it.key] || [];
  // A qué ficha lleva "Ver ficha": la del personaje, o la del dueño del artefacto.
  const ficha = v ? { cid: v.cid, uid: v.uid || '' } : it.cid ? { cid: it.cid, uid: '' } : null;
  return `<div class="backdrop" data-a="tlCerrar"><div class="modal" data-a="tlModal">
    <div class="row" style="justify-content:space-between;margin-bottom:12px">
      <div class="cellname">${it.img ? `<img class="thumb" src="${it.img}" alt="">` : ''}
        <div><div style="font-weight:700">${h(v ? (v.uid ? v.sub : v.name) : it.nom)}</div>
        <div class="muted">${h(v ? (v.uid ? v.name : t('base')) : it.sub)} · ${h(listName(list))}</div></div></div>
      <button class="btn sm" data-a="tlCerrar">${h(t('tl_done'))}</button>
    </div>
    <p class="muted" style="margin-bottom:10px">${h(t('tl_rows_note'))}</p>
    <div class="filasel">${rows.map((r, i) => `<label class="chk">
      <input type="checkbox" data-a="tlFila" data-row="${h(r.id)}" ${mias.includes(r.id) ? 'checked' : ''}>
      <span class="tag solid" style="background:${rowColor(i, rows.length)}">${h(r.label)}</span></label>`).join('')}</div>
    ${ficha ? `<div class="row" style="margin-top:14px">
      <button class="btn sm" data-a="open" data-cid="${ficha.cid}" data-uid="${ficha.uid}">${h(t('tl_open_sheet'))}</button>
    </div>` : ''}
  </div></div>`;
}

// ============================================================================
// FUENTES CURADAS: textos traducidos, fuentes citadas y vocabulario de stats
// ============================================================================
const GUIA   = window.MFF_GUIA || { fuentes: {}, stats: {} };
const MODOS  = window.MFF_MODOS || [];
const ABX    = window.MFF_ABX || { restricciones: [], equipos: [] };
const CANCELS = window.MFF_CANCELS || {};
const GUIA_PJ = window.MFF_GUIA_PJ || {};
const SOPORTES = window.MFF_SOPORTES || {};
const ROTACIONES = window.MFF_ROTACIONES || {};
const VERIF = window.MFF_VERIFICACION || {};
const TXT    = window.MFF_TXT || {};
// Guía de armado de Cynicalex (scripts/guia_armado.py). null: los datos cargados son
// anteriores a que la app la sumara.
const GUIA_ARMADO = window.MFF_GUIA_ARMADO || null;
/** Texto de una fuente en inglés, en el idioma activo. Sin traducción cargada se muestra
 *  el inglés marcado, como las líneas de efecto: nunca se inventa una. Devuelve HTML.
 *  '[n]' es el salto de línea de la guía de thanosvibs. */
function trHtml (en) {
  if (!en) return '';
  const br = (s) => h(s).replace(/\[n\]/g, '<br>');
  if (LANG === 'en') return br(en);
  const es = TXT[en];
  return es == null ? `<span class="sintrad" title="${h(t('untranslated'))}">${br(en)}</span>` : br(es);
}
/** Texto plano (para atributos title). */
function trTxt (en) { return !en ? '' : (LANG === 'en' ? en : (TXT[en] || en)).replace(/\[n\]/g, ' '); }
/** Objeto {es, en} de lo curado a mano. */
function bi (o) { return o ? (o[LANG] || o.es || '') : ''; }
function statNom (k) { const s = GUIA.stats[k]; return s ? bi(s) : k; }
/** Chips con las fuentes citadas: con su enlace, o sin él si la fuente no tiene dirección (la
 *  guía dentro del juego). */
function fuentesHtml (claves) {
  return (claves || []).map(k => { const f = GUIA.fuentes[k]; if (!f) throw new Error('fuente desconocida: ' + k);
    return f.url ? `<a class="fuente" href="${h(f.url)}" target="_blank" rel="noopener" title="${h(t('md_source'))}">${h(f.nombre)}</a>`
                 : `<span class="fuente" title="${h(t('md_source'))}">${h(f.nombre)}</span>`; }).join('');
}
/** Retrato de la API -> variante del roster (base o uniforme). */
let _PORT = null;
function varDeRetrato (p) {
  if (!_PORT) { _PORT = {};
    CHARS.forEach(ch => { if (ch.p) _PORT[ch.p] = [ch.id, null]; (ch.uniforms || []).forEach(u => { if (u.p) _PORT[u.p] = [ch.id, u.id]; }); }); }
  const x = _PORT[p]; return x ? variant(x[0], x[1]) : null;
}
/** Ficha chica de personaje que abre su ficha al tocarla. */
function miniPj (v, extra, nota) {
  if (!v) return '';
  const u = imgUrl('portrait-' + v.id);
  return `<span class="minipj" data-a="open" data-cid="${v.cid}" data-uid="${v.uid || ''}" title="${h((nota ? nota + ' — ' : '') + fullLabel(v))}">
    ${u ? `<img src="${u}" alt="" loading="lazy">` : ''}<span class="who">${h(v.name)}</span>${v.uid ? `<span class="what">${h(v.sub)}</span>` : ''}${extra || ''}</span>`;
}
function ctpIcono (id) { const u = imgUrl('ctp-' + id); return u ? `<img class="ctpico" src="${u}" alt="" loading="lazy">` : ''; }
/** Un C.T.P. plegable con lo que hace según thanosvibs (normal y reforjado). */
function ctpDetalle (c, extra) {
  return `<details class="ctp"><summary>${ctpIcono(c.id)}<b>C.T.P. of ${h(c.name)}</b>${extra || ''}</summary>
    <p>${trHtml(c.desc)}</p>${c.descR ? `<p class="muted"><b>${h(t('md_reforged'))}:</b> ${trHtml(c.descR)}</p>` : ''}</details>`;
}
/** Controles de Alliance Battle que aplican las skills de un retrato, como etiquetas:
 *  "Parálisis: 1/4" = las skills 1 y 4 (6 = la definitiva). */
function cortesHtml (p, tipos) {
  const c = CANCELS[p] || {};
  return tipos.filter(x => c[x]).map(x => `<span class="tag cancel" title="${h(c[x].map(slotEs).join(', '))}">${h(trTxt(x))}: ${h(c[x].map(s => s.replace('Active ', '').replace('Ult', '6')).join('/'))}</span>`).join('');
}

// ============================================================================
// FICHA: PARA QUÉ SE USA
// Lo que dicen las fuentes del personaje y de sus uniformes: listas, guía, Alliance
// Battle y lo que le da al equipo. Lo derivado (el tipo de ataque) se dice derivado.
// ============================================================================
/** Base y uniformes del personaje, como variantes. */
function variantesDe (ch) { return [variant(ch.id, null)].concat(ch.uniforms.map(u => variant(ch.id, u.id))); }
/** Rótulo de la variante cuando no es la que está abierta en la ficha. */
function otraVar (vv, v) { return vv.key === v.key ? '' : `<span class="tag dim varx">${h(vv.uid ? vv.sub : t('base'))}</span>`; }

const SRC_ATAQUE = { 'Physical Attack': 'fisico', 'Energy Attack': 'energia', 'HP': 'vida' };
/** Tipo de ataque derivado de las skills activas: con qué stat escala su % de daño.
 *  {k: fisico|energia|vida|mixto, reparto: [{src, k, pct}]}, o null si no hacen daño. */
/** Tipo de ataque de la variante, del perfil: físico, energía, vida o mixto (con el reparto). */
function tipoAtaque (v) {
  const esc = perfilDe(v).esc;
  if (!esc.length) return null;
  const reparto = esc.map(([src, pct]) => ({ src, k: SRC_ATAQUE[src], pct }));
  return { k: reparto.length === 1 ? reparto[0].k : 'mixto', reparto };
}
function ataqueHtml (ta) {
  if (!ta) return `<span class="muted" title="${h(t('us_atk_note'))}">${h(t('us_atk_none'))}</span>`;
  const nom = (x) => x.k ? t('at_' + x.k) : x.src;
  const color = { fisico: 'var(--dmg-fisico)', energia: 'var(--dmg-energia)', vida: 'var(--dmg-pg)' }[ta.k] || 'var(--text)';
  return `<span style="color:${color};font-weight:700" title="${h(t('us_atk_note'))}">${h(ta.k === 'mixto' ? t('at_mixto') : nom(ta.reparto[0]))}</span>${
    ta.k === 'mixto' ? `<div class="muted">${ta.reparto.map(x => h(nom(x)) + ' ' + x.pct + '%').join(' · ')}</div>` : ''}`;
}
/** Posiciones del personaje (todas sus variantes) en las tier lists de personajes. */
function usoListas (ch, v) {
  const vs = variantesDe(ch);
  const linea = (l, siempre) => {
    const rows = rowsOf(l), fs = [];
    vs.forEach(vv => indicesFila(l, vv.key).forEach(i => fs.push({ i, r: rows[i], vv })));
    if (!fs.length && !siempre) return '';
    fs.sort((a, b) => a.i - b.i);
    return `<div class="uslista"><span class="usl" title="${h(listName(l))}">${h(listName(l))}</span>
      <span class="usf">${fs.length ? fs.map(f => `<span class="tag solid" style="background:${rowColor(f.i, rows.length)}" title="${h(f.r.label)}">${h(f.r.label)}</span>${otraVar(f.vv, v)}`).join(' ')
                                   : '<span class="muted">—</span>'}</span>
      <button class="btn sm" data-a="verLista" data-id="${l.id}">${h(t('md_see_list'))}</button></div>`;
  };
  const grupos = listasAgrupadas().map(g => ({ g, ls: g.ls.filter(l => tipoLista(l) === 'personajes') }));
  return grupos.map(({ g, ls }) => {
    if (g.g === 'principal') return `<div class="usgrupo">${ls.map(l => linea(l, true)).join('')}</div>`;
    const con = ls.map(l => linea(l, false)).filter(Boolean);
    return con.length ? `<details class="usgrupo"><summary>${h(t(g.k))}: ${h(t('us_in_n_lists').replace('{n}', con.length).replace('{t}', ls.length))}</summary>${con.join('')}</details>` : '';
  }).join('');
}

/** Nombre de una skill de soporte: traducido si la tabla de nombres de skills lo tiene. */
let _NOMBRES = null;
function nombreTabla (en) {
  if (!_NOMBRES) { _NOMBRES = new Map(); (TB.name || []).forEach(f => _NOMBRES.set(f.en, f)); }
  const f = _NOMBRES.get(en);
  if (!f || LANG === 'en' || f.es == null) return `<span class="nm">${h(en)}</span>`;
  return `<span class="nm">${h(f.es)}<span class="orig">${h(f.en)}</span></span>`;
}
const TIPOS_SOPORTE = [['leader', 'sp_leader'], ['leader2', 'sp_leader2'], ['passive', 'sp_passive'], ['passive2', 'sp_passive2'],
  ['t2', 'sp_t2'], ['t22', 'sp_t22'], ['uniform', 'sp_uniform'], ['uniform2', 'sp_uniform2'], ['artifact', 'sp_artifact']];
const SLOTS_SOPORTE = TIPOS_SOPORTE.map(([k]) => k).filter(k => !LIDERAZGOS.includes(k));
const CLAVE_SOPORTE = Object.fromEntries(TIPOS_SOPORTE);   // slot -> su nombre en la tabla de idioma
function restrHtml (x) {
  if (!x.r) return `<span class="muted">${h(t('sp_all'))}</span>`;
  const [cat, val] = x.r;
  const corr = x.rc ? ` <span class="corr" title="${h(t('sp_corrected') + ' ' + x.rc.join(': '))}">⚠</span>` : '';
  return `<span class="muted">${h(t('sp_applies'))}: ${h(t('sp_r_' + cat))}</span> ${icon(val)}<b>${h(cat === 'Character' ? val : dom(val))}</b>${corr}`;
}
/** Un liderazgo o un soporte (Resumen y «Cómo funciona»): de qué slot es, su nombre, a quiénes llega, sus
 *  categorías y cada efecto con efectoSoporteHtml, que dice también su activación, su recarga, cuánto dura y
 *  lo que pide. */
function soporteHtml (tipo, clave, x) {
  return `<div class="sop">
    <div class="soph"><span class="slotbadge ${tipo.startsWith('leader') ? 'lead' : 'pass'}">${h(t(clave))}</span>
      ${x.n ? nombreTabla(x.n) : ''}
      ${x.sig ? `<span class="tag solid" style="background:var(--gold)" title="${h(t('sp_notable_t'))}">${h(t('sp_notable'))}</span>` : ''}
      ${x.est ? `<span class="tag dim">${h(t('sp_est').replace('{n}', x.est))}</span>` : ''}${srcHtml(x)}</div>
    <div class="sopr">${restrHtml(x)}</div>
    ${categoriasDe(x).length ? `<div class="row sopcats" title="${h(t('ct_title'))}">${categoriasDe(x).map(k =>
      `<span class="tag ghost">${h(t('ct_' + k))}</span>`).join('')}</div>` : ''}
    <ul class="sopfx">${x.fx.map(f => `<li>${efectoSoporteHtml(x, f)}</li>`).join('')}</ul>
  </div>`;
}
/** Qué le sirve de un liderazgo o un soporte: las categorías de ataque según con qué pega
 *  (el daño de sus skills activas) y las que le sirven a cualquiera, con atajos al roster
 *  filtrado por los que se lo dan. */
function leSirveHtml (v) {
  const cats = categoriasQueSirven(v);
  const atq = cats.filter(k => CAT[k].ataque), resto = cats.filter(k => !CAT[k].ataque);
  return `<div class="row lesirve">
    <span class="muted" title="${h(t('ls_note'))}">${h(t('ls_title'))}</span>
    ${atq.map(k => `<span class="tag dim">${h(t('ct_' + k))}</span>`).join('')}
    <span class="muted">${h(t('ls_also'))} ${resto.map(k => h(t('ct_' + k))).join(' · ')}</span>
    <span class="row" style="gap:6px">
      <button class="btn sm" data-a="paraVer" data-tipo="lid">${h(t('ls_leaders'))}</button>
      <button class="btn sm" data-a="paraVer" data-tipo="sop">${h(t('ls_supports'))}</button></span>
  </div>`;
}
/** ¿Su Leader Skill da un poder que ninguna fuente publica? Es la entrada «otorga» del análisis (un «Give Power»
 *  que no dice qué otorga, scripts/modelo.py) que sale de la Leader Skill, salvo que lo diga el juego: entonces el
 *  liderazgo lo trae, con su fuente (otorga). Lo que Leads & Supports publica en esas variantes no se toma como lo que
 *  otorga: solo se avisa (5 de octubre de 2026). */
function otorgaSinPublicar (v) {
  const an = ANALISIS[v.p], so = SOPORTES[v.p] || {};
  if (LIDERAZGOS.some(k => so[k] && so[k].otorga)) return false;
  return !!an && an.fx.some(([ie, , , fuentes]) => CATALOGO.efectos[ie].id === 'otorga'
    && fuentes.some(([si]) => v.skills[si].sl === 'Leader Skill'));
}
/** Lo que el retrato le da al equipo según thanosvibs (Leads & Supports), y el aviso de un «Give Power» de su Leader
 *  Skill que ninguna fuente publica. */
function usoSoportes (v) {
  const s = SOPORTES[v.p];
  const tipos = s ? TIPOS_SOPORTE.filter(([k]) => s[k]) : [];
  const otorga = otorgaSinPublicar(v) ? `<p class="usotorga" style="color:var(--gold)">⚠ ${h(t('us_otorga'))}</p>` : '';
  if (!tipos.length) return `${otorga}<p class="muted">${h(t('us_sup_none'))}</p>`;
  return `${s.np ? `<p><span class="tag solid" style="background:var(--role-soporte)">${h(t('sp_np'))}</span></p>` : ''}
    ${otorga}<div class="sops">${tipos.map(([k, clave]) => soporteHtml(k, clave, s[k])).join('')}</div>
    <div class="fuentes">${fuentesHtml(fuentesSop(tipos.map(([k]) => s[k])))}</div>
    ${equiposGuiaHtml()}`;
}

/** Lo que dice la guía de principiantes de cómo se arma un equipo (líder, principal y soporte; dónde vale el
 *  liderazgo y dónde los soportes), plegado: todas sus notas, en el orden de la guía. */
function equiposGuiaHtml () {
  const E = GUIA.equipos, notas = (xs) => xs.map(x => `<p class="muted">${h(bi(x))}</p>`).join('');
  return `<details class="usgrupo"><summary>${h(t('us_equipos'))}</summary>
    <p><b>PvE</b></p>${notas(E.pve)}<p><b>PvP</b></p>${notas(E.pvp)}
    <p><b>${h(t('us_equipos_tema'))}</b></p>${notas([E.tematicos])}
    <div class="fuentes">${fuentesHtml(E.fuente)}</div></details>`;
}
/** Dónde lo recomienda la guía de principiantes (cualquiera de sus variantes). */
function usoGuia (ch, v) {
  const es = variantesDe(ch).flatMap(vv => (GUIA_PJ[vv.p] || []).map(e => ({ e, vv })));
  if (!es.length) return `<p class="muted">${h(t('us_guide_none'))}</p>`;
  const modo = (id) => { const m = MODOS.find(x => x.id === id); return m ? m.nombre : id; };
  return es.map(({ e, vv }) => `<div class="usguia">
      <div class="muted">${trHtml(e.sec)}${e.sub ? ' › ' + trHtml(e.sub) : ''} ${otraVar(vv, v)}</div>
      ${e.textos.map(x => `<p>${trHtml(x)}</p>`).join('')}
      ${e.ctps.length || e.modos.length ? `<div class="row" style="gap:5px">
        ${e.ctps.map(c => { const x = CTPS.find(y => y.id === c);
          return x ? `<span class="tag dim">${ctpIcono(c)}C.T.P. of ${h(x.name)}</span>` : `<span class="tag dim">${h(c === 'obelisco6' ? t('us_obelisk') : c)}</span>`; }).join('')}
        ${e.modos.map(m => `<span class="tag ghost" style="color:var(--allies)" title="${h(t('md_guide_mentions_note'))}">${h(modo(m))}</span>`).join('')}</div>` : ''}
    </div>`).join('') + `<div class="fuentes">${fuentesHtml(['tv-guia-1', 'tv-guia-2'])}</div>`;
}

/** Alliance Battle: equipos recomendados que lo incluyen y qué controles aplica. */
function usoABX (ch, v) {
  const ps = new Map(variantesDe(ch).map(vv => [vv.p, vv]));
  const eqs = ABX.equipos.filter(e => e.pj.some(p => ps.has(p)));
  const ab = MODOS.find(m => m.abx);
  const cortes = ab && ab.cancels ? Object.entries(ab.cancels).map(([modo, tipos]) => {
    const c = cortesHtml(v.p, tipos); return c ? `<div class="row" style="gap:5px"><span class="tag dim">${h(modo)}</span>${c}</div>` : ''; }).join('') : '';
  const rol = (e, p) => p === e.lider && e.dps.includes(p) ? t('md_r_leaddps') : p === e.lider ? t('md_r_lead') : e.dps.includes(p) ? t('md_r_dps') : t('md_r_support');
  return `${cortes ? `<p class="muted">${h(t('us_cancels'))}</p>${cortes}`
                  : `<p class="muted">${h(t('us_cancels_none').replace('{m}', Object.keys(ab.cancels).join(t('us_cancels_ni'))))}</p>`}
    ${eqs.length ? `<p class="muted" style="margin-top:8px">${h(t('us_abx_teams'))}</p>
      <div class="usabx">${eqs.map(e => { const p = e.pj.find(x => ps.has(x));
        return `<div class="row" style="gap:5px"><span class="tag dim">${h(t('us_day'))} ${e.d}</span><span class="tag dim">${h(e.m)}</span>
          <span class="tag ghost">${h(rol(e, p))}</span>${otraVar(ps.get(p), v)}
          <span class="minis">${e.pj.filter(x => x !== p).map(x => miniPj(varDeRetrato(x))).join('')}</span></div>`; }).join('')}</div>`
    : `<p class="muted" style="margin-top:8px">${h(t('us_abx_none'))}</p>`}
    <div class="fuentes">${fuentesHtml(['tv-abxl'])}</div>`;
}

/** La fila de la guía de armado del personaje: la de su mejor uniforme (hay una por
 *  personaje). {e, vv} o null. */
function armadoDe (ch) {
  for (const vv of variantesDe(ch)) { const e = GUIA_ARMADO.pj[vv.p]; if (e) return { e, vv }; }
  return null;
}
/** Chip de la fuente, con la versión de la planilla en uso. */
function fuenteArmado () {
  return `<div class="fuentes">${fuentesHtml(['cyn-armado'])}<span class="tag dim">${h(GUIA_ARMADO.version)}</span></div>`;
}
/** Un valor de la guía que la app no interpreta: va tal cual, marcado. */
function sinInterpretar (x) { return `<span class="sinint" title="${h(t('ga_unknown'))}">${h(x)}</span>`; }
/** Lo que dice la guía de armado del personaje: su mejor uniforme, su lugar en la tier list
 *  de la guía con los emojis y su leyenda, cómo se consigue y la nota. */
function usoArmado (ch, v) {
  if (!GUIA_ARMADO) return `<p class="muted">${h(t('ga_no_data'))}</p>`;
  const a = armadoDe(ch);
  if (!a) return `<p class="muted">${h(t('ga_none'))}</p>`;
  const { e, vv } = a, L = GUIA_ARMADO.leyenda;
  return `<div class="row ga-mejor" style="gap:6px;margin-bottom:6px"><span class="muted">${h(t('ga_best_uni'))}</span>${miniPj(vv)}
      ${vv.key === v.key ? `<span class="muted">(${h(t('ga_this_uni'))})</span>` : ''}</div>
    ${e.rank || e.bl || e.bl_x ? `<div class="row ga-tier" style="gap:5px;margin-bottom:6px"><span class="muted">${h(t('ga_tier'))}</span>
      ${e.rank ? `<span class="tag ghost">${h(e.rank)}</span>` : ''}
      ${(e.bl || []).map(k => `<span class="tag dim">${k} ${trHtml(L.emojis[k])}</span>`).join('')}
      ${e.bl_x ? sinInterpretar(e.bl_x) : ''}</div>` : ''}
    ${e.adq ? `<div class="row ga-adq" style="gap:5px;margin-bottom:6px"><span class="muted">${h(t('ga_acq'))}</span>
      ${e.adq.map(x => `<span class="tag dim">${h(x)}${L.adq[x] ? ' · ' + h(L.adq[x]) : ''}</span>`).join('')}</div>` : ''}
    ${e.nota ? `<p class="ga-nota">${trHtml(e.nota)}</p>` : ''}
    ${fuenteArmado()}`;
}
/** Rotación y skill de proc según la guía de armado, con su notación. Son de su mejor
 *  uniforme: si es otro, se dice cuál. */
function rotacionArmado (ch, v) {
  if (!GUIA_ARMADO) return `<p class="muted">${h(t('ga_no_data'))}</p>`;
  const a = armadoDe(ch);
  if (!a) return `<p class="muted">${h(t('ga_none'))}</p>`;
  const filas = [['ga_rot', a.e.rot], ['ga_rotc', a.e.rotc], ['ga_proc', a.e.proc]].filter(x => x[1]);
  return `${filas.length ? `<div class="rots ga-rot">${filas.map(([k, x]) => `<div class="rot" data-k="${k}"><div class="roth"><b>${h(t(k))}</b>${otraVar(a.vv, v)}</div>
      <div class="rotd">${h(x)}</div></div>`).join('')}</div>
    <details class="usgrupo"><summary>${h(t('ga_rot_legend'))}</summary>
      <table class="abx"><tbody>${GUIA_ARMADO.leyenda.rot.map(([k, x]) => `<tr><th>${h(k)}</th><td>${trHtml(x)}</td></tr>`).join('')}</tbody></table></details>`
    : `<p class="muted">${h(t('ga_rot_none'))}</p>`}
    ${fuenteArmado()}`;
}

// ============================================================================
// FICHA: CÓMO ARMARLO
// Las reglas generales de la guía (las mismas de Modos → Armado) aplicadas a su tipo
// de ataque, el C.T.P. que le asignan las fuentes y su artefacto.
// ============================================================================
function slugId (s) { return String(s).toLowerCase().replace(/[^a-z0-9]/g, ''); }
/** C.T.P. según la Ideal CTP List (una fila por C.T.P.) y según la guía de principiantes. */
function armadoCTP (ch, v) {
  const li = GUIA.ctp_ranking.lista_ideal, l = listById(li.id);
  let lista;
  if (!l) lista = `<p class="muted">${h(t('ar_ctp_noimport'))}</p>`;
  else {
    const rows = rowsOf(l), fs = [];
    variantesDe(ch).forEach(vv => indicesFila(l, vv.key).forEach(i => fs.push({ r: rows[i], vv })));
    lista = fs.length ? `<div class="ctps">${fs.map(f => { const c = CTPS.find(x => x.id === slugId(f.r.label));
        return c ? ctpDetalle(c, otraVar(f.vv, v)) : `<div class="row" style="gap:6px">${ctpFilaIdeal(f.r.label)}${otraVar(f.vv, v)}</div>`; }).join('')}</div>`
      : `<p class="muted">${h(t('ar_ctp_nolist'))}</p>`;
  }
  const guia = [...new Set(variantesDe(ch).flatMap(vv => (GUIA_PJ[vv.p] || []).flatMap(e => e.ctps)))];
  return `${ctpRecFichaHtml(v)}
    <p class="muted" style="margin-top:12px">${h(li.nombre)}: ${h(bi(li))}</p>${lista}
    ${guia.length ? `<p class="muted" style="margin-top:8px">${h(t('ar_ctp_guide'))}</p>
      <div class="ctps">${guia.map(id => { const c = CTPS.find(x => x.id === id);
        return c ? ctpDetalle(c) : `<span class="tag dim">${h(id === 'obelisco6' ? t('us_obelisk') : id)}</span>`; }).join('')}</div>` : ''}
    <div class="fuentes">${fuentesHtml(li.fuente.concat(['tv-guia-1', 'tv-guia-2', 'tv-ctps']))}</div>
    ${ctpsArmado(ch, v)}`;
}
/** C.T.P. según la guía de armado: uno por C.T.P. (y reforjado o no), con los lugares en los
 *  que lo pone (mejor, segundo, meta y fuera del meta de PvE y de PvP). */
function ctpsArmado (ch, v) {
  const titulo = (variante) => `<p class="muted" style="margin-top:12px">${h(t('ga_ctp_title'))} ${variante}</p>`;
  if (!GUIA_ARMADO) return titulo('') + `<p class="muted">${h(t('ga_no_data'))}</p>`;
  const a = armadoDe(ch);
  if (!a) return titulo('') + `<p class="muted">${h(t('ga_none'))}</p>`;
  const grupos = [];
  (a.e.ctp || []).forEach(x => { const id = x.c ? x.c + (x.r ? '+' : '') : '?' + x.x;
    let g = grupos.find(y => y.id === id); if (!g) grupos.push(g = { id, x, ks: [] }); g.ks.push(x.k); });
  const extra = (g) => `<span class="ctproles">${g.x.r ? reforjadoTag() : ''}${
    g.ks.map(k => `<span class="tag ghost">${h(t('ga_ctp_' + k))}</span>`).join('')}</span>`;
  return `${titulo(otraVar(a.vv, v))}
    ${grupos.length ? `<div class="ctps ga-ctp">${grupos.map(g => { const c = g.x.c && CTPS.find(y => y.id === g.x.c);
        return c ? ctpDetalle(c, extra(g)) : `<div class="row" style="gap:6px">${sinInterpretar(g.x.x)}${extra(g)}</div>`; }).join('')}</div>`
      : `<p class="muted">${h(t('ga_ctp_none'))}</p>`}
    ${notasCtpArmado()}
    ${fuenteArmado()}`;
}
/** La etiqueta de un C.T.P. que la guía de armado pide reforjado. */
function reforjadoTag () { return `<span class="tag solid" style="background:var(--gold)">${h(t('md_reforged'))}</span>`; }
/** Las notas de la guía de armado sobre C.T.P. (su leyenda), plegadas. */
function notasCtpArmado () {
  return `<details class="usgrupo"><summary>${h(t('ga_ctp_notes'))}</summary>
      <ul class="sopfx">${GUIA_ARMADO.leyenda.ctp.map(x => `<li>${trHtml(x)}</li>`).join('')}</ul></details>`;
}
/** Columnas de la guía de armado para el C.T.P. de un contexto: el tipo del modo de un equipo (el ctp de
 *  MODOS), el orden de las combinaciones o el que se eligió al marcar un favorito. En PvP, el meta y fuera
 *  del meta de PvP; en PvE, los de PvE; sin contexto (sin modo, un modo propio, «puntos para él» o una tier
 *  list), el mejor y el segundo. */
function columnasCtp (ctx) {
  const cols = ctx === null ? ['mejor', 'segundo'] : { pvp: ['pvp', 'pvp_alt'], pve: ['pve', 'pve_alt'] }[ctx];
  if (!cols) throw new Error('tipo de modo sin columnas de C.T.P. en la guía de armado: ' + ctx);
  return cols;
}
/** Un C.T.P. de la guía de armado, corto: ícono, nombre y si va reforjado. Un valor que la app no
 *  interpreta va tal cual, marcado. */
function ctpCorto (x) {
  if (!x.c) return sinInterpretar(x.x);
  const c = CTPS.find(y => y.id === x.c);
  return `<span class="row" style="gap:4px">${ctpIcono(c.id)}<span>${h(c.name)}</span>${x.r ? reforjadoTag() : ''}</span>`;
}
// C.T.P. RECOMENDADO (Ezequiel, 4 de octubre de 2026): una sola respuesta, la misma en la ficha y en todas las
// tarjetas de equipo (combinaciones, «cómo entraría», tus equipos y favoritos), siempre con su fuente. Desde el 5 de
// octubre, con las dos fuentes que tiene la app, una al lado de la otra (Ezequiel: «sumar la única lista de recomendación
// de C.T.P. que tenemos ya en la aplicación... sino estamos dando información a medias»): la guía de armado de Cynicalex y
// la Ideal CTP List; si no coinciden, se ven las dos.
/** El C.T.P. recomendado para v en un contexto (null, 'pvp' o 'pve'), según cada fuente:
 *  - armado: las dos columnas del contexto en la guía de armado (columnasCtp; la fila es la de su mejor uniforme), si le
 *    da alguna: { vv, cols: [[columna, entrada de la guía o null], ...] }; si no, null.
 *  - ideal: las filas de la Ideal CTP List en las que está (esta variante o, si no está, otra del personaje; «Not worth»
 *    se dice): { vv, filas: [rótulos] }; si no está, null. No depende del contexto.
 *  vv: la variante de la que sale. */
function ctpRecomendado (v, ctx) {
  const out = { armado: null, ideal: null };
  const a = GUIA_ARMADO ? armadoDe(v.ch) : null;
  if (a) {
    const cols = columnasCtp(ctx).map(k => [k, (a.e.ctp || []).find(y => y.k === k) || null]);
    if (cols.some(([, c]) => c)) out.armado = { vv: a.vv, cols };
  }
  const l = listById(GUIA.ctp_ranking.lista_ideal.id);
  if (l) {
    const rows = rowsOf(l);
    for (const vv of [v].concat(variantesDe(v.ch).filter(x => x.key !== v.key))) {
      const fs = indicesFila(l, vv.key);
      if (fs.length) { out.ideal = { vv, filas: fs.map(i => rows[i].label) }; break; }
    }
  }
  return out;
}
/** Una fila de la Ideal CTP List: el C.T.P. que nombra, «Not worth» dicho, u otro rótulo tal cual, marcado. */
function ctpFilaIdeal (rotulo) {
  const id = slugId(rotulo), c = CTPS.find(x => x.id === id);
  if (c) return `<span class="row" style="gap:4px">${ctpIcono(c.id)}<span>${h(c.name)}</span></span>`;
  return id === 'notworth' ? `<span>${h(t('ctp_not_worth'))}</span>` : sinInterpretar(rotulo);
}
/** La fuente de una recomendación, como enlace: la guía de armado (con su versión) o la Ideal CTP List. */
function ctpFuenteLink (fuente) {
  return fuente === 'armado' ? `<span class="ctpfuente">${fuentesHtml(['cyn-armado'])} <span class="tag dim">${h(GUIA_ARMADO.version)}</span></span>`
    : `<span class="ctpfuente">${fuentesHtml(GUIA.ctp_ranking.lista_ideal.fuente)} <span class="tag dim">${h(GUIA.ctp_ranking.lista_ideal.nombre)}</span></span>`;
}
/** Lo que recomienda, en celdas: las dos columnas de la guía de armado (una que no da, «—») y la de la Ideal CTP List, cada
 *  una con el uniforme del que sale si no es el que lleva (x). */
function ctpCeldasHtml (r, celda, x) {
  const ov = (q) => q ? otraVar(q.vv, x) : '';
  const guia = r.armado
    ? r.armado.cols.map(([, c], i) => `<td ${celda} data-f="armado">${c ? ctpCorto(c) : `<span class="muted" title="${h(t('ctp_sin_col'))}">—</span>`}${i ? '' : ov(r.armado)}</td>`).join('')
    : `<td ${celda} colspan="2" data-f="armado"><span class="muted ctpsin" title="${h(t('ctp_sin_armado'))}">—</span></td>`;
  const ideal = r.ideal ? `${r.ideal.filas.map(ctpFilaIdeal).join('')}${ov(r.ideal)}` : `<span class="muted ctpsin" title="${h(t('ctp_sin_ideal'))}">—</span>`;
  return guia + `<td ${celda} data-f="ideal">${ideal}</td>`;
}
/** Lo que recomienda, en líneas (la ficha): la guía de armado, cada columna con su rótulo, y la Ideal CTP List, cada una
 *  con su fuente y el uniforme del que sale si no es v. */
function ctpLineaHtml (r, v) {
  const guia = r.armado
    ? `<span class="row ctp-armado" style="gap:6px">${r.armado.cols.map(([k, c]) => `<span class="row" style="gap:4px"><span class="muted">${h(t('ga_ctp_' + k))}:</span>${
        c ? ctpCorto(c) : `<span class="muted" title="${h(t('ctp_sin_col'))}">—</span>`}</span>`).join('')}${otraVar(r.armado.vv, v)}${ctpFuenteLink('armado')}</span>`
    : `<span class="row ctp-armado" style="gap:6px"><span class="muted ctpsin">${h(t('ctp_sin_armado'))}</span>${ctpFuenteLink('armado')}</span>`;
  const ideal = r.ideal
    ? `<span class="row ctp-ideal" style="gap:6px"><span class="muted">${h(t('ctp_ideal_col'))}:</span>${r.ideal.filas.map(ctpFilaIdeal).join('')}${otraVar(r.ideal.vv, v)}${ctpFuenteLink('ideal')}</span>`
    : `<span class="row ctp-ideal" style="gap:6px"><span class="muted ctpsin">${h(t('ctp_sin_ideal'))}</span>${ctpFuenteLink('ideal')}</span>`;
  return guia + ideal;
}
/** Las fuentes de las recomendaciones, con sus chips: la guía de armado (con su versión y sus notas) y la Ideal CTP List. */
function ctpFuentesHtml () {
  return `${GUIA_ARMADO ? notasCtpArmado() + fuenteArmado() : ''}
    <div class="fuentes">${fuentesHtml(GUIA.ctp_ranking.lista_ideal.fuente)}<span class="tag dim">${h(GUIA.ctp_ranking.lista_ideal.nombre)}</span></div>`;
}
/** El C.T.P. recomendado (ctpRecomendado) a cada integrante de un equipo en un contexto: una fila por integrante, con las
 *  dos columnas de la guía de armado y la de la Ideal CTP List, y las fuentes abajo. Si la recomendación es de otro
 *  uniforme que el que lleva, se dice. */
function ctpsTablaHtml (vs, ctx) {
  const cols = columnasCtp(ctx), celda = 'style="white-space:normal;vertical-align:top;padding:4px 10px 4px 0"';
  const rs = vs.map(x => ctpRecomendado(x, ctx));
  const otra = rs.some((r, i) => (r.armado && r.armado.vv.key !== vs[i].key) || (r.ideal && r.ideal.vv.key !== vs[i].key));
  const filas = vs.map((x, i) => `<tr><th ${celda}>${h(x.name)}</th>${ctpCeldasHtml(rs[i], celda, x)}</tr>`);
  return `<table class="abx" style="table-layout:fixed;width:100%;max-width:760px"><colgroup><col style="width:28%"><col><col><col></colgroup>
      <thead><tr><th ${celda}></th>${cols.map(k => `<th ${celda}>${h(t('ga_ctp_' + k))}</th>`).join('')}<th ${celda}>${h(t('ctp_ideal_col'))}</th></tr></thead>
      <tbody>${filas.join('')}</tbody></table>
    ${otra ? `<p class="muted">${h(t('ga_eq_other'))}</p>` : ''}
    ${ctpFuentesHtml()}`;
}
/** El rótulo de los C.T.P. de un equipo: las columnas del contexto y la Ideal CTP List. */
function ctpsRotulo (ctx) { const cols = columnasCtp(ctx); return t('ctp_eq_title').replace('{a}', t('ga_ctp_' + cols[0])).replace('{b}', t('ga_ctp_' + cols[1])); }
/** Los C.T.P. de un equipo, plegados (tus equipos y favoritos; en las combinaciones y «cómo entraría», van en la ventana
 *  del «Por qué»). */
function ctpsEquipo (vs, ctx) { return `<details class="usgrupo ga-eq"><summary>${h(ctpsRotulo(ctx))}</summary>${ctpsTablaHtml(vs, ctx)}</details>`; }
/** En la ficha, el C.T.P. recomendado en cada contexto (lo mismo que dicen sus tarjetas de equipo). */
function ctpRecFichaHtml (v) {
  const rs = [null, 'pvp', 'pve'].map(ctx => [ctx, ctpRecomendado(v, ctx)]);
  return `<p class="muted">${h(t('ctp_rec_title'))}</p>
    <ul class="ctprec">${rs.map(([ctx, r]) => `<li><b>${h(t('ctp_ctx_' + (ctx || 'sin')))}</b>
      <div class="ctprec-l">${ctpLineaHtml(r, v)}</div></li>`).join('')}</ul>`;
}
/** Si necesita artefacto, según la guía de armado (con su leyenda). */
function artArmado (ch) {
  if (!GUIA_ARMADO) return '';
  const a = armadoDe(ch);
  if (!a || !(a.e.art || a.e.art_x)) return '';
  const x = a.e.art;
  return `<p class="ga-art" style="margin-top:10px"><span class="muted">${h(t('ga_art'))}</span>
    ${x ? `<b title="${h(x.v)}">${trHtml(x.t)}${x.modo ? ' (' + h(x.modo) + ')' : ''}</b>` : sinInterpretar(a.e.art_x)}</p>${fuenteArmado()}`;
}
/** ISO-8 y obelisco según la guía de armado: cada categoría con sus sets (y las piedras de los
 *  que tiene la guía de principiantes). */
function isoArmado (ch, v) {
  if (!GUIA_ARMADO) return `<p class="muted">${h(t('ga_no_data'))}</p>`;
  const a = armadoDe(ch);
  if (!a) return `<p class="muted">${h(t('ga_none'))}</p>`;
  const e = a.e, L = GUIA_ARMADO.leyenda, sets = GUIA.iso.sets_pve.concat(GUIA.iso.sets_pvp);
  const set = (nombre) => { const s = sets.find(x => x.nombre === nombre);
    return `<div class="isoset">${h(nombre)}${s ? piedrasHtml(s.piedras) : ''}</div>`; };
  return `${otraVar(a.vv, v) ? `<div class="row" style="margin-bottom:6px">${otraVar(a.vv, v)}</div>` : ''}
    <p class="muted">${h(t('ga_iso'))}</p>
    ${(e.iso || []).map(k => `<div class="isocat"><b>${trHtml(k)}</b>${(L.iso[k] || []).map(set).join('')}</div>`).join('')}
    ${e.iso_x ? `<p class="ga-iso-x">${sinInterpretar(e.iso_x)}</p>` : ''}
    ${!e.iso && !e.iso_x ? '<p class="muted">—</p>' : ''}
    <p class="muted" style="margin-top:8px">${h(t('ga_obelisk'))}</p>
    ${e.ob || e.ob_x ? `<div class="row ga-ob" style="gap:5px">${(e.ob || []).map(x => `<span class="tag dim">${trHtml(x)}</span>`).join('')}${
      (e.ob_x || []).map(sinInterpretar).join('')}</div>` : '<p class="muted">—</p>'}
    ${fuenteArmado()}`;
}
/** Sets ISO de ataque (PvE), la nota de piedra que corresponde a su tipo de ataque y las notas de ISO-8 de la
 *  guía (todas, como en Modos). */
function armadoISO (ta) {
  const G = GUIA.iso, P = G.piedras, k = ta ? ta.k : null;
  const piedras = k === 'fisico' ? ['roja'] : k === 'energia' ? ['blanca'] : k === 'mixto' ? ['roja', 'blanca'] : [];
  return `<p class="muted">${h(t('ar_iso_pve').replace('{n}', G.sets_pve.length))}</p>
    ${G.sets_pve.map(s => `<div class="isoset"><b>${h(s.nombre)}</b> ${piedrasHtml(s.piedras)}
      <div class="muted">${s.stats.map(statNom).join(' · ')}</div></div>`).join('')}
    ${piedras.map(p => `<p>${piedrasHtml([p])} <b>${h(P[p].nombre)}</b>: ${h(bi(P[p]))}</p>`).join('')}
    <p>${piedrasHtml(['caos'])} <b>${h(P.caos.nombre)}</b>: ${h(bi(P.caos))}</p>
    ${G.notas_pve.map(x => `<p class="muted">${h(bi(x))}</p>`).join('')}
    ${G.notas_pvp.map(x => `<p class="muted"><b>PvP:</b> ${h(bi(x))}</p>`).join('')}
    <div class="fuentes">${fuentesHtml(G.fuente)}</div>`;
}
/** Urus: primero los del tipo de ataque del personaje; después, los topes en orden. */
function armadoUrus (ta) {
  const G = GUIA.urus, k = ta ? ta.k : 'ninguno';
  return `<p><b>${h(t('ar_uru_' + k))}</b></p>
    <p class="muted">${h(bi(G.ataque))}</p>
    <p class="muted">${h(bi(G.prioridad_nota))}</p>
    <ol class="prio">${G.prioridad.map(x => `<li>${h(statNom(x))}</li>`).join('')}</ol>
    <p class="muted"><b>${h(t('md_gear4'))}:</b> ${GUIA.gear4.prioridad.map(x => h(statNom(x))).join(' › ')}.</p>
    ${GUIA.gear4.notas.map(x => `<p class="muted">${h(bi(x))}</p>`).join('')}
    <div class="fuentes">${fuentesHtml(G.fuente.concat(GUIA.gear4.fuente.filter(x => !G.fuente.includes(x))))}</div>`;
}
/** Artefacto exclusivo: el texto del juego con los valores del nivel de estrellas elegido. Una línea que el build
 *  corrige con el juego (scripts/fuentes.py) va marcada, con lo que publica thanosvibs, y cita su fuente. */
function armadoArtefacto (ch) {
  const a = ARTES.find(x => x.p === ch.p);
  if (!a) return `<p class="muted">${h(t('ar_art_none'))}</p>`;
  const est = ui.artEst, vals = a.valores[est] || [];
  const linea = (ln) => {
    const es = LANG === 'en' ? ln.t : TXT[ln.t];
    const txt = h(es == null ? ln.t : es).replace(/\[P(\d+)\]/g, (_, n) => vals[n - 1] != null ? `<b>${h(vals[n - 1])}</b>`
      : `<i class="tpl" title="${h(t('ar_nodata_t'))}">${h(t('ar_nodata'))}</i>`);
    return `<div class="artl" style="padding-left:${ln.n * 14}px">${ln.b ? '• ' : ''}${es == null
      ? `<span class="sintrad" title="${h(t('untranslated'))}">${txt}</span>` : txt}${ln.tv
      ? ` <span class="corr" title="${h(t('ar_corregida').replace('{tv}', ln.tv))}">⚠</span>` : ''}</div>`;
  };
  const puntaje = (lbl, n) => `<span class="tag dim" title="${h(t('ar_score_t'))}">${lbl} ${'★'.repeat(n)}${'☆'.repeat(Math.max(0, 3 - n))}</span>`;
  return `<div class="row" style="gap:8px;margin-bottom:6px;flex-wrap:nowrap">${imgUrl('art-' + a.p) ? `<img class="artico" src="${imgUrl('art-' + a.p)}" alt="">` : ''}
      <div><b>${h(a.name)}</b><div class="muted">${h(a.pasiva)} · ${h(t('ar_since'))} ${h(a.desde)}</div></div></div>
    <div class="row" style="gap:6px;margin-bottom:8px">${puntaje('PvE', a.pve)}${puntaje('PvP', a.pvp)}</div>
    <div class="seg" style="margin-bottom:8px">${Object.keys(a.valores).map(e => `<button class="${e === est ? 'on' : ''}" data-a="artEst" data-v="${e}">${e}★</button>`).join('')}</div>
    <div class="artlineas">${a.lineas.map(linea).join('')}</div>
    ${a.obtencion.length ? `<details class="usgrupo"><summary>${h(t('ar_obtain'))} (${a.obtencion.length})</summary>
      <ul class="sopfx">${a.obtencion.map(x => `<li>${trHtml(x)}</li>`).join('')}</ul></details>` : ''}
    <div class="fuentes">${fuentesHtml(['tv-art', ...new Set(a.lineas.flatMap(ln => ln.f || []))])}</div>`;
}
/** Opciones del uniforme abierto: qué uniforme habilita cada una (thanosvibs) y qué stat
 *  conviene elegir en cada rango (guía de principiantes). */
function armadoOpciones (v) {
  if (!v.uid) return `<p class="muted">${h(t('op_base'))}</p>`;
  if (!v.op) return `<p class="muted">${h(t('op_none'))}</p>`;
  const G = GUIA.opciones_uniforme;
  return `<p class="muted" style="margin-bottom:6px">${h(t('op_note'))}</p>
    <div class="opuni">${v.op.map((p, i) => { const vv = varDeRetrato(p);
      return `<div class="opfila"><b>${h(G.rangos[i].rango)}</b>${vv ? miniPj(vv) : `<span class="muted">${h(p)}</span>`}
        <div class="muted opstat">${G.rangos[i].mejor.map(k => k === 'ataque' ? h(t('md_own_attack')) : h(statNom(k))).join(' › ')}</div></div>`; }).join('')}</div>
    <p class="muted" style="margin-top:6px">${h(bi(G.pvp))}</p>
    <div class="fuentes">${fuentesHtml(['tv-uni'].concat(G.fuente))}</div>`;
}
/** Hoja de ruta de la guía para esta variante: los pasos que le tocan según su tier
 *  máximo y si sube a Tier-3 o trasciende, con los requisitos de la wiki. El usuario
 *  marca hasta dónde llegó con ese personaje. */
function armadoRuta (ch, v) {
  const P = GUIA.progresion, R = Object.fromEntries(P.requisitos.items.map(x => [x.id, x]));
  // Un T2 llega hasta el paso de antes de subir a Tier-3; un T3, hasta el de antes de Tier-4 (el orden de la guía).
  const corte = { T2: 't3', T3: 't4' }[v.t], fin = corte ? P.pasos.findIndex(p => p.id === corte) : P.pasos.length;
  if (fin < 0) throw new Error('la hoja de ruta de la guía no tiene el paso ' + corte);
  const pasos = P.pasos.slice(0, fin);
  // El avance es del personaje: si marcó un paso que esta variante no tiene (Tier-4 en
  // una sin Tier-4), todos los que sí tiene quedan hechos.
  const hecho = Math.min(P.pasos.findIndex(p => p.id === U.ruta[ch.id]), pasos.length - 1);
  const extra = (p) => {
    if (p.id === 't3') return `<div class="req"><b>${h(t(v.trans ? 'ru_this_tp' : 'ru_this_t3'))}</b> ${h(bi(R[v.trans ? 'tp' : 't3']))}</div>`;
    if (p.id === 't4') return `<div class="req">${h(bi(R.t4))}</div><div class="req aviso">${h(bi(P.requisitos.discrepancia))}</div>`;
    return '';
  };
  return `<p class="muted">${h(t('ru_note'))}</p>
    <ol class="ruta">${pasos.map((p, i) => `<li class="${i <= hecho ? 'hecho' : ''}">
      <div class="row" style="gap:6px;flex-wrap:nowrap;align-items:flex-start"><span style="flex:1">${h(bi(p))}</span>
        ${i === hecho ? `<button class="btn sm" data-a="ruta" data-cid="${ch.id}" data-v="${i ? pasos[i - 1].id : ''}">${h(t('ru_undo'))}</button>`
                      : `<button class="btn sm" data-a="ruta" data-cid="${ch.id}" data-v="${p.id}">${h(t('ru_done'))}</button>`}</div>
      ${extra(p)}</li>`).join('')}</ol>
    ${v.t === 'T2' ? `<p class="muted">${h(t('ru_no_t3'))}</p>` : v.t === 'T3' ? `<p class="muted">${h(t('ru_no_t4'))}</p>` : ''}
    <details class="usgrupo"><summary>${h(t('ru_notes'))}</summary>${P.notas.map(x => `<p class="muted">${h(bi(x))}</p>`).join('')}</details>
    <div class="fuentes">${fuentesHtml(P.fuente.concat(P.requisitos.fuente))}</div>`;
}
/** Estado de un stat frente a su tope: lo que falta, en el tope o lo que sobra. */
function estadoTope (cid, k, tope) {
  const x = (U.topes[cid] || {})[k] || {};
  if (x.v == null && x.b == null) return '<span class="muted">—</span>';
  const total = (x.v || 0) + (x.b || 0), dif = Math.round((total - tope) * 10) / 10;
  return dif < 0 ? `<span style="color:var(--allies)">${h(t('cap_short').replace('{n}', -dif))}</span>`
       : dif === 0 ? `<span style="color:var(--self)">${h(t('cap_ok'))}</span>`
       : `<span style="color:var(--gold)">${h(t('cap_over').replace('{n}', dif))}</span>`;
}
/** Calculadora de topes: el usuario pone lo que muestra la pantalla de stats (y los
 *  buffs con duración, que esa pantalla no suma) y ve cuánto le falta o le sobra. */
function armadoTopes (ch) {
  const T2 = GUIA.topes, mis = U.topes[ch.id] || {};
  const conTope = T2.items.filter(x => x.tope != null).flatMap(x => x.stats.map(k => ({ k, tope: x.tope, base: x.base })));
  const sinTope = T2.items.filter(x => x.tope == null).flatMap(x => x.stats);
  const num = (k, f) => `<input type="number" step="0.1" inputmode="decimal" data-a="tope" data-cid="${ch.id}" data-k="${k}" data-f="${f}"
      value="${(mis[k] || {})[f] != null ? mis[k][f] : ''}" aria-label="${h(statNom(k) + ' ' + t(f === 'v' ? 'cap_val' : 'cap_buff'))}">`;
  return `<p class="muted">${h(t('cap_note'))}</p>
    <div class="stagewrap"><table class="topes"><thead><tr><th>${h(t('cap_stat'))}</th><th>${h(t('cap_cap'))}</th>
      <th>${h(t('cap_val'))}</th><th>${h(t('cap_buff'))}</th><th>${h(t('cap_state'))}</th></tr></thead><tbody>
      ${conTope.map(x => `<tr><td>${h(statNom(x.k))}${x.base ? `<div class="muted">${h(t('cap_base').replace('{n}', x.base))}</div>` : ''}</td>
        <td class="num">${x.tope}%</td><td>${num(x.k, 'v')}</td><td>${num(x.k, 'b')}</td>
        <td data-estado="${x.k}">${estadoTope(ch.id, x.k, x.tope)}</td></tr>`).join('')}
    </tbody></table></div>
    <p class="muted">${h(t('cap_none'))} ${sinTope.map(statNom).map(h).join(', ')}.</p>
    <details class="usgrupo"><summary>${h(t('ru_notes'))}</summary>${T2.notas.map(x => `<p class="muted">${h(bi(x))}</p>`).join('')}</details>
    <div class="fuentes">${fuentesHtml(T2.fuente)}</div>`;
}
// ============================================================================
// FICHA: ROTACIONES
// ============================================================================
/** Notación de las rotaciones: **tramo del proc** en negrita, *palabra* en cursiva. */
function notacionHtml (s) {
  return h(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\*(.+?)\*/g, '<i>$1</i>');
}
function rotacionHtml (r) {
  const es = r.n || LANG === 'en' ? r.desc : TXT[r.desc];
  const falta = es == null;
  return `<div class="rot"><div class="roth"><span class="tag dim">${h(bi(GUIA.rotaciones.categorias[r.cat]))}</span><b>${trHtml(r.nom)}</b></div>
    <div class="rotd ${falta ? 'sintrad' : ''}" ${falta ? `title="${h(t('untranslated'))}"` : ''}>${notacionHtml(falta ? r.desc : es)}</div></div>`;
}
/** Rotaciones de skills del retrato abierto, con la leyenda de la notación. */
function panelRotaciones (ch, v) {
  const rs = ROTACIONES[v.p] || [], G = GUIA.rotaciones;
  const otras = rs.length ? [] : variantesDe(ch).filter(vv => vv.key !== v.key && (ROTACIONES[vv.p] || []).length);
  return `<div class="section"><h3>${h(t('rot_title'))} · ${h(v.uid ? v.sub : t('base'))}</h3>
    ${rs.length ? `<div class="rots">${rs.map(rotacionHtml).join('')}</div>` : `<p class="muted">${h(t('rot_none'))}</p>`}
    ${otras.length ? `<div class="row" style="gap:5px;margin:6px 0"><span class="muted">${h(t('rot_other'))}</span>${otras.map(vv =>
      `<button class="btn sm" data-a="uniform" data-uid="${vv.uid || 'base'}">${h(vv.uid ? vv.sub : t('base'))}</button>`).join('')}</div>` : ''}
    <details class="usgrupo"><summary>${h(t('rot_legend'))}</summary>
      <table class="abx"><tbody>${G.leyenda.map(x => `<tr><th>${h(x.k)}</th><td>${h(bi(x))}</td></tr>`).join('')}</tbody></table>
      <p class="muted" style="margin-top:6px">${h(bi(G.nota))}</p></details>
    <div class="fuentes">${fuentesHtml(G.fuente)}</div>
    <h4 class="subrot">${h(t('ga_title'))}</h4>${rotacionArmado(ch, v)}</div>`;
}

// ============================================================================
// FICHA: VERIFICACIÓN ENTRE FUENTES (scripts/auditar.py)
// ============================================================================
/** Diferencias del retrato abierto y, para lo que es del personaje (artefacto), del base. */
function verifDe (ch, v) {
  const propio = VERIF[v.p] || { ok: 0, nd: 0, dif: [] };
  const base = v.p !== ch.p ? (VERIF[ch.p] || { dif: [] }).dif.filter(d => d.t === 'art' || d.t === 'art_incompleto') : [];
  return { ok: propio.ok, nd: propio.nd, dif: propio.dif.concat(base) };
}
const CAMPO_VERIF = { type: 'vf_type', side: 'vf_side', gender: 'vf_gender', allies: 'vf_allies' };
function verifLinea (d) {
  const n = (x) => Array.isArray(x) ? x.join(', ') : String(x);
  const sk = () => `${slotEs(d.sl)} · <b>${h(d.n)}</b>: `;
  switch (d.t) {
    case 'dano': return sk() + h(t('vf_dano').replace('{a}', n(d.api)).replace('{w}', n(d.wiki)));
    case 'cd': return sk() + h(t('vf_cd').replace('{a}', n(d.api)).replace('{w}', n(d.wiki)));
    case 'atk': return h(t('vf_atk').replace('{a}', n(d.api)).replace('{w}', n(d.wiki)));
    case 'instinto': return h(t('vf_inst').replace('{a}', n(d.api)).replace('{w}', n(d.wiki)));
    case 't4': return h(t('vf_t4'));
    case 's6': return h(t('vf_s6').replace('{v}', d.v));
    case 'art': return h(t('vf_art').replace('{a}', n(d.api) || '—').replace('{w}', n(d.wiki) || '—'));
    case 'art_incompleto': return h(t('vf_art_inc').replace('{v}', d.v.map(e => e + '★').join(', ')));
  }
  if (CAMPO_VERIF[d.t]) return h(t(CAMPO_VERIF[d.t]).replace('{a}', n(d.api)).replace('{w}', n(d.wiki)));
  throw new Error('diferencia de verificación desconocida: ' + d.t);
}
/** Cuántas diferencias entre fuentes tiene: todas las de verifDe(), las mismas en el Resumen y en Más. */
function verifCuenta (vf) { const n = vf.dif.length; return t(n === 1 ? 'vf_tag_1' : 'vf_tag').replace('{n}', n); }
/** Más › Verificación: cuántas diferencias hay (verifCuenta, como el Resumen), cuántas skills se pudieron
 *  contrastar con la wiki (las que difieren en daño o recarga, una vez cada una) y cada diferencia. */
function usoVerificacion (ch, v) {
  const vf = verifDe(ch, v), skills = new Set(vf.dif.filter(d => d.t === 'dano' || d.t === 'cd').map(d => d.sl)).size;
  return `${vf.dif.length ? `<p class="vfcuenta"><b>⚠ ${h(verifCuenta(vf))}</b></p>` : ''}
    <p class="muted">${h(t('vf_resumen').replace('{ok}', vf.ok).replace('{d}', skills).replace('{nd}', vf.nd))}</p>
    ${vf.dif.length ? `<ul class="sopfx verif">${vf.dif.map(d => `<li>${verifLinea(d)}</li>`).join('')}</ul>`
                    : `<p>${h(t('vf_sin_dif'))}</p>`}
    <p class="muted">${h(t('vf_nota'))} <a href="docs/AUDITORIA.md" target="_blank" rel="noopener">docs/AUDITORIA.md</a></p>`;
}


// ============================================================================
// MODOS DE JUEGO
// ============================================================================
function renderModos () {
  const F = ui.modoFiltro;
  const lista = MODOS.filter(m => (F === 'todos') || m.tipo === F || m.frecuencia === F);
  const desact = GUIA.version_fuente && GUIA.version_fuente !== GUIA.version_guia;
  return `<div class="page-head"><div><h1>${h(t('md_title'))}</h1>
      <div class="sub">${h(t('md_note'))}</div></div>
      <div class="row"><span class="tag dim">${h(t('md_guide'))} ${h(GUIA.version_guia)}</span>
        ${desact ? `<span class="tag solid" style="background:var(--gold)" title="${h(t('md_guide_old_t'))}">${h(t('md_guide_old'))} ${h(GUIA.version_fuente)}</span>` : ''}</div></div>
    <div class="seg" style="margin-bottom:14px">${['todos', 'pve', 'pvp', 'diario', 'semanal'].map(k =>
      `<button class="${F === k ? 'on' : ''}" data-a="modoFiltro" data-v="${k}">${h(t('md_f_' + k))}</button>`).join('')}</div>
    <div class="modos">${lista.map(modoCard).join('')}</div>
    <div class="section" id="armado" style="margin-top:28px"><h3>${h(t('md_builds'))}</h3>
      <p class="muted" style="margin-bottom:12px">${h(t('md_builds_note'))}</p>
      <div class="armados">${armadoHtml('pve')}${armadoHtml('pvp')}</div>
    </div>`;
}

function modoCard (m) {
  const abierto = ui.modoAbierto === m.id;
  const eq = m.equipo;
  return `<div class="modo ${abierto ? 'on' : ''}">
    <div class="modohead" data-a="modoAbrir" data-id="${m.id}">
      <span class="tag solid" style="background:${m.tipo === 'pvp' ? 'var(--role-control)' : 'var(--role-soporte)'}">${m.tipo === 'pvp' ? 'PvP' : 'PvE'}</span>
      <span class="modonom">${h(m.nombre)}</span>
      <span class="tag dim">${h(t('md_f_' + m.frecuencia))}</span>
      ${eq ? `<span class="tag dim">${h(t('md_team'))} ${eq.tam}${eq.escuadras ? ' × ' + eq.escuadras : ''}</span>` : ''}
      <span class="flecha">${abierto ? '▾' : '▸'}</span>
    </div>
    ${abierto ? `<div class="modobody">
      <div class="bloque"><h4>${h(t('md_what'))}</h4>
        <ul>${(m.que || []).map(x => `<li>${h(bi(x))}</li>`).join('')}</ul>
        <div class="fuentes">${fuentesHtml(m.fuente)}</div>
        ${m.corrobora ? `<p class="muted">${h(bi(m.corrobora))}</p><div class="fuentes">${fuentesHtml(m.corrobora_fuente)}</div>` : ''}
      </div>
      ${eq ? `<div class="bloque"><h4>${h(t('md_team'))}</h4><p>${h(bi(eq))}</p><div class="fuentes">${fuentesHtml(eq.fuente)}</div></div>` : ''}
      ${(m.avisos || []).length ? `<div class="bloque aviso">${m.avisos.map(x => `<p>${h(bi(x))}</p>`).join('')}<div class="fuentes">${fuentesHtml(m.avisos_fuente)}</div></div>` : ''}
      ${m.abx ? panelABX(m) : ''}
      ${panelRecomendados(m)}
      ${m.ctp ? panelCTPs(m.ctp) : ''}
      ${m.ctp ? `<p class="muted"><a href="#armado" data-a="irArmado" data-v="${m.ctp}">${h(t(m.ctp === 'pvp' ? 'md_go_pvp' : 'md_go_pve'))}</a></p>` : ''}
    </div>` : ''}
  </div>`;
}

/** Personajes recomendados para un modo: las primeras filas de sus listas, las filas de
 *  PvP de todas las listas (modos PvP) y las menciones de la guía. */
function panelRecomendados (m) {
  const bloques = [];
  (m.listas || []).forEach(id => { const l = listById(id); if (l) bloques.push(bloqueLista(l, (r, i) => i < 3)); });
  if (m.pvp_filas) LISTS.filter(l => l.group && l.rows.some(r => /pvp/i.test(r.label)))
    .forEach(l => bloques.push(bloqueLista(l, r => /pvp/i.test(r.label))));
  const guia = Object.entries(GUIA_PJ).filter(([, es]) => es.some(e => e.modos.includes(m.id)));
  return `<div class="bloque"><h4>${h(t('md_recs'))}</h4>
    ${bloques.join('') || `<p class="muted">${h(t('md_no_list'))}</p>`}
    ${guia.length ? `<div class="reclista"><div class="reclh">${h(t('md_guide_mentions'))}
        <span class="muted">${h(t('md_guide_mentions_note'))}</span></div>
      <div class="minis">${guia.map(([p, es]) => { const v = varDeRetrato(p);
        const txt = es.filter(e => e.modos.includes(m.id)).flatMap(e => e.textos).map(trTxt).join(' · ');
        return v ? miniPj(v, '', txt) : ''; }).join('')}</div>
      <div class="fuentes">${fuentesHtml(['tv-guia-1', 'tv-guia-2'])}</div></div>` : ''}
  </div>`;
}
/** Filas elegidas de una lista importada, con sus personajes. */
function bloqueLista (l, elegir) {
  const rows = rowsOf(l), a = assignOf(l.id);
  const filas = rows.map((r, i) => ({ r, i })).filter(x => elegir(x.r, x.i));
  if (!filas.length) return '';
  const vs = allVariants();
  return `<div class="reclista"><div class="reclh"><b>${h(listName(l))}</b>
      <span class="muted">${h(l.author || '')}${l.gameVersion ? ' · ' + h(t('tl_game')) + ' ' + h(l.gameVersion) : ''}</span>
      <button class="btn sm" data-a="verLista" data-id="${l.id}">${h(t('md_see_list'))}</button></div>
    ${filas.map(({ r, i }) => { const en = vs.filter(v => (a[v.key] || []).includes(r.id));
      return en.length ? `<div class="recfila"><span class="tag solid" style="background:${rowColor(i, rows.length)}" title="${h(r.label)}">${h(r.label)}</span>
        <div class="minis">${en.map(v => miniPj(v)).join('')}</div></div>` : ''; }).join('')}
  </div>`;
}

/** Alliance Battle: restricciones de un día del ciclo (los días, los modos y su orden, como los publica la
 *  fuente) y los equipos recomendados, con qué integrante corta a los jefes (cancels) y con qué skill. */
function panelABX (m) {
  const dia = ui.abxDia, dias = [...new Set(ABX.restricciones.map(r => r.d))].sort((a, b) => a - b);
  const rs = ABX.restricciones.filter(r => r.d === dia);
  const eqs = ABX.equipos.filter(e => e.d === dia);

  const restr = (r) => r.length ? r.map(x => `<span class="tag dim">${icon(x)}${h(dom(x))}</span>`).join(' ') : `<span class="muted">${h(t('md_no_restr'))}</span>`;
  const cortes = (p, modo) => cortesHtml(p, (m.cancels || {})[modo] || []);
  return `<div class="bloque"><h4>${h(t('md_abx'))}</h4>
    <div class="row" style="margin-bottom:8px"><span class="muted">${h(t('md_day'))}</span>
      <select data-a="abxDia">${dias.map(d => `<option value="${d}" ${d === dia ? 'selected' : ''}>${d}</option>`).join('')}</select>
      <span class="muted">${h(t('md_day_note').replace('{n}', dias.length))}</span></div>
    <table class="abx"><tbody>${rs.map(r => `<tr><th>${h(r.m)}</th><td>${restr(r.r)}</td></tr>`).join('')}</tbody></table>
    ${m.cancels ? `<p class="muted" style="margin:8px 0">${h(bi(m.cancels_nota))} ${Object.entries(m.cancels).map(([modo, tipos]) =>
      `<b>${h(modo)}</b>: ${h(tipos.map(trTxt).join(', '))}`).join(' · ')}.
      ${h(t('md_cancel_read'))}</p>` : ''}
    ${eqs.length ? `<div class="abxeqs">${eqs.map(e => `<div class="abxeq">
        <div class="row" style="gap:6px;margin-bottom:6px"><span class="tag dim">${h(e.m)}</span>
          ${e.titulo ? `<span class="tag ghost" style="color:var(--gold)">${trHtml(e.titulo)}</span>` : ''}
          <span class="muted">${h(t('md_added'))} ${h(e.v || '?')}</span></div>
        ${e.pj.map(p => { const v = varDeRetrato(p);
          const rol = p === e.lider && e.dps.includes(p) ? t('md_r_leaddps') : p === e.lider ? t('md_r_lead') : e.dps.includes(p) ? t('md_r_dps') : t('md_r_support');
          return `<div class="abxpj">${miniPj(v)}<span class="tag dim">${h(rol)}</span>${cortes(p, e.m)}</div>`; }).join('')}
      </div>`).join('')}</div>` : `<p class="muted">${h(t('md_no_teams'))}</p>`}
    <div class="fuentes">${fuentesHtml(['tv-abxl'])}</div>
  </div>`;
}

/** C.T.P.s recomendados para un tipo de modo, con la descripción de thanosvibs. */
function panelCTPs (tipo) {
  const grupos = (GUIA.ctp_ranking || { grupos: [] }).grupos.filter(g => g.id === tipo || (g.id === 'otros'));
  return `<div class="bloque"><h4>${h(t('md_ctps'))}</h4>
    ${grupos.map(g => `<p class="muted">${h(bi(g))}</p><div class="ctps">${g.ctps.map(id => {
      const c = CTPS.find(x => x.id === id); return c ? ctpDetalle(c) : ''; }).join('')}</div>`).join('')}
    <div class="fuentes">${fuentesHtml(GUIA.ctp_ranking && GUIA.ctp_ranking.fuente)}</div>
  </div>`;
}

/** Piedras de un set ISO, como puntos de color. */
function piedrasHtml (ps) {
  const P = GUIA.iso.piedras;
  return `<span class="piedras">${ps.map(k => `<i style="background:${P[k].color}" title="${h(P[k].nombre)} (${h(t('iso_' + k))})"></i>`).join('')}</span>`;
}
/** Armado general según el tipo de modo: ISO, urus, 4.º gear, opciones de uniforme, obelisco. */
function armadoHtml (tipo) {
  const G = GUIA, pvp = tipo === 'pvp';
  const sets = pvp ? G.iso.sets_pvp : G.iso.sets_pve;
  return `<div class="card armado"><h3 style="margin-bottom:10px">${pvp ? 'PvP' : 'PvE'}</h3>
    <h4>ISO-8</h4>
    ${sets.map(s => `<div class="isoset"><b>${h(s.nombre)}</b> ${piedrasHtml(s.piedras)}
      <div class="muted">${s.stats.map(statNom).join(' · ')}${s.es ? ' — ' + h(bi(s)) : ''}</div></div>`).join('')}
    ${!pvp ? `<p class="muted">${h(bi(G.iso.efecto_pve))}</p>` : ''}
    ${(pvp ? G.iso.notas_pvp : G.iso.notas_pve).map(x => `<p class="muted">${h(bi(x))}</p>`).join('')}
    <p class="muted"><i>${h(bi(G.iso.composicion_fuente))}</i></p>
    <h4>${h(t('md_urus'))}</h4>
    <p class="muted">${h(bi(G.urus.ataque))}</p>
    ${pvp ? `<p class="muted">${h(t('md_uru_pvp'))}</p>`
          : `<ol class="prio">${G.urus.prioridad.map(k => `<li>${h(statNom(k))}</li>`).join('')}</ol>
             <p class="muted">${h(bi(G.urus.prioridad_nota))}</p>${G.urus.reglas.map(x => `<p class="muted">${h(bi(x))}</p>`).join('')}`}
    <h4>${h(t('md_gear4'))}</h4>
    <ol class="prio">${G.gear4.prioridad.map(k => `<li>${h(statNom(k))}</li>`).join('')}</ol>
    ${G.gear4.notas.map(x => `<p class="muted">${h(bi(x))}</p>`).join('')}
    <h4>${h(t('md_obelisk'))}</h4>
    ${pvp ? `<p class="muted">${h(bi(G.obelisco.pvp))}</p>` : G.obelisco.notas.map(x => `<p class="muted">${h(bi(x))}</p>`).join('')}
    <h4>${h(t('md_uni_opts'))}</h4>
    ${pvp ? `<p class="muted">${h(bi(G.opciones_uniforme.pvp))}</p><p class="aviso">${h(bi(G.opciones_uniforme.pvp_inconsistencia))}</p>`
          : `<table class="abx"><tbody>${G.opciones_uniforme.rangos.map(r => `<tr><th>${h(r.rango)}</th>
              <td>${r.mejor.map(k => k === 'ataque' ? h(t('md_own_attack')) : h(statNom(k))).join(' › ')}</td></tr>`).join('')}</tbody></table>`}
    <div class="fuentes">${fuentesHtml(['tv-guia-3', 'wiki-iso', 'wiki-uru', 'wiki-gear'])}</div>
  </div>`;
}

// ============================================================================
// EQUIPOS
// ============================================================================
/** Modos para armar equipos: los del juego con tamaño de equipo según su fuente, y los
 *  propios. {id, name, tam, juego, ctp}: ctp es el tipo del modo ('pvp', 'pve' o null), el de
 *  MODOS en los del juego; los propios no tienen. */
function modosEquipo () {
  return MODOS.filter(m => m.equipo && m.equipo.tam).map(m => ({ id: m.id, name: m.nombre, tam: m.equipo.tam, juego: true, ctp: m.ctp }))
    .concat(U.modes.map(m => ({ id: m.id, name: m.name, tam: m.teamSize, juego: false, ctp: null })));
}
function tamModo (id) { const m = modosEquipo().find(x => x.id === id); return m ? m.tam : 3; }
/** Un equipo guardado, con su sinergia. En el armador se puede borrar; en la ficha, no. */
function equipoCard (tt, borrable) {
  const vs = tt.members.map(k => variant(...k.split('::'))).filter(Boolean), lider = liderEquipo(tt, vs);
  const sc = synergy(vs, { lider }), modo = modosEquipo().find(m => m.id === tt.modeId);
  return `<div class="card" style="position:relative">
    ${borrable ? `<button class="btn sm danger" data-a="teamRemove" data-id="${tt.id}" style="position:absolute;top:10px;right:10px">✕</button>` : ''}
    <div style="font-weight:600;padding-right:34px;margin-bottom:8px">${h(tt.name)}</div>
    ${modo ? `<div class="row" style="margin-bottom:6px"><span class="tag dim">${h(modo.name)}</span></div>` : ''}
    <div class="eqcompacto" style="margin-bottom:8px">${retratosEquipo(vs, null, lider)}</div>
    <div class="muted">${conLider(vs, lider).map(fullLabel).join(' + ')}</div>
    ${tt.reason ? `<p class="muted" style="margin-top:6px">${h(tt.reason)}</p>` : ''}
    <div class="muted" style="margin-top:6px">${sc.score}${artPts(sc.art)} ${h(t('tm_synergy_pts'))}</div>
    ${borrable ? `<label class="row eqlider">${h(t('ms_lider'))}
      <select data-a="teamLider" data-id="${tt.id}">${vs.map(x => `<option value="${x.key}" ${x === lider ? 'selected' : ''}>${h(fullLabel(x))}</option>`).join('')}</select></label>`
      : `<div class="muted">${h(t('eq_leader').replace('{x}', fullLabel(lider)))}</div>`}
    ${ctpsEquipo(conLider(vs, lider), modo ? modo.ctp : null)}
    ${borrable ? `<div class="row" style="margin-top:8px">${botonArmar(conLider(vs, lider), tt.modeId, tt.name)}</div>` : ''}
  </div>`;
}
/** Un favorito: equipo de 3 marcado con ★ en las combinaciones de un personaje (el primero). */
function favoritoCard (f) {
  const vs = f.members.map(k => variant(...k.split('::'))).filter(Boolean);
  const sc = synergy(vs);
  return `<div class="card eqsug">
    <div class="row" style="justify-content:space-between;align-items:flex-start">
      <div class="row" style="gap:10px;align-items:flex-start">${estrella(f.members)}${retratosEquipo(vs, vs[0].key, sc.lider)}</div>
      <div class="eqpts"><b>${sc.score}</b>${artPts(sc.art)} ${h(t('tm_synergy_pts'))}</div>
    </div>
    <div class="muted">${h(conLider(vs, sc.lider).map(fullLabel).join(' + '))}${f.ctx ? ` <span class="tag dim">${h(t('tm_fav_ctx').replace('{c}', t('ctp_ctx_' + f.ctx)))}</span>` : ''}</div>
    <div><b>${h(sc.lider ? t('eq_leader').replace('{x}', fullLabel(sc.lider)) : t('tm_no_leader'))}</b></div>
    ${ctpsEquipo(conLider(vs, sc.lider), f.ctx)}
    <div class="row">${botonArmar(conLider(vs, sc.lider), '', '')}</div>
  </div>`;
}
function renderTeams () {
  return `
  <div class="page-head"><div><h1>${h(t('tm_title'))}</h1>
    <div class="sub">${h(t('tm_note'))}</div></div></div>
  ${ui.avisoLideres ? `<div class="avisoeq">⚠ ${h(t('tm_lideres').replace('{e}', ui.avisoLideres.join(' · ')))}</div>` : ''}
  ${U.descartados.length ? `<div class="section"><details class="usgrupo"><summary>${h(t('tm_desc').replace('{n}', U.descartados.length))}</summary>
    <p class="muted" style="margin:8px 0 10px">${h(t('tm_desc_note'))}</p>
    ${U.descartados.map(d => { const vs = d.map(c => variant(c, null)).filter(Boolean);
      return `<div class="card combo"><div class="combofila">${retratosEquipo(vs, '')}
        <div class="combotx">${h(vs.map(x => x.name).join(' + '))}</div>
        <button class="btn sm" data-a="restaurar" data-c="${d.join(',')}">${h(t('eq_restaurar'))}</button></div></div>`; }).join('')}
  </details></div>` : ''}
  ${U.favoritos.length ? `<div class="section"><h3>${h(t('tm_favs'))}</h3>
    <p class="muted" style="margin-bottom:10px">${h(t('tm_favs_note'))}</p>
    <div class="grid eqgrid">${U.favoritos.map(favoritoCard).join('')}</div></div>` : ''}
  <div class="section"><h3>${h(t('tm_mine'))}</h3>
  ${U.teams.length ? `<div class="grid eqgrid">${U.teams.map(tt => equipoCard(tt, true)).join('')}</div>`
  : `<div class="empty"><div class="big">◇</div><div>${h(t('tm_empty'))}</div></div>`}</div>`;
}

// ============================================================================
// MESA DE TRABAJO (1.0.25, Ezequiel, 6 de octubre de 2026: «lo podemos probar a ver si realmente mejora»)
// La pantalla va en tres paneles: en la ficha, la lista del roster a la izquierda (la misma de las flechas ‹ ›);
// en el centro, la sección; a la derecha, en todas las secciones, la mesa. La mesa es el único lugar donde se arma
// un equipo: sus integrantes en orden (el primero es el líder, como en el juego), el modo y, en Alliance Battle, el
// día y la dificultad, con la restricción marcada en cada integrante; los bonos de equipo activos; lo que le llega a
// cada uno (las casillas de cobertura de las combinaciones, sin puntajes); guardarlo en Mis equipos. Abajo, los que
// se van a comparar. Se guarda en la capa (U.mesa): sigue ahí al cambiar de sección y al volver a abrir la app.
// En una ventana angosta los paneles se ven de a uno, con pestañas abajo (ui.movil).
// ============================================================================
function mesaVs () { return U.mesa.members.map(k => variant(...k.split('::'))).filter(Boolean); }
/** Restricción del día de Alliance Battle elegida en la mesa ({ d, m, r }), o null si el modo no es Alliance Battle. */
function restriccionMesa () {
  if (U.mesa.modeId !== 'alliance-battle') return null;
  const del = ABX.restricciones.filter(r => r.d === U.mesa.abxDia);
  return del.find(r => r.m === U.mesa.abxDif) || del[0];
}
/** ¿v cumple un valor de una restricción de Alliance Battle? Cada valor es una clase, un bando, un género o una raza. */
function cumpleRestriccion (v, x) {
  if (SEED.CLASSES.includes(x)) return v.c === x;
  if (SEED.FACTIONS.includes(x)) return v.f === x;
  if (SEED.GENDERS.includes(x)) return v.gender === x;
  if (SEED.RACES.includes(x)) return v.race === x;
  throw new Error('restricción de Alliance Battle que no es clase, bando, género ni raza: ' + x);
}
/** Pone una variante en la mesa: al final, o en el lugar del mismo personaje si ya estaba con otro uniforme (el
 *  juego no deja dos veces al mismo). Con la mesa llena no suma: lo dice. */
function ponerEnMesa (key) {
  const v = variant(...key.split('::')), m = U.mesa, max = tamModo(m.modeId);
  ui.avisoMesa = null;
  if (m.members.includes(key)) { ui.avisoMesa = { txt: t('ms_ya').replace('{x}', fullLabel(v)) }; return; }
  const i = m.members.findIndex(k => k.split('::')[0] === v.cid);
  if (i > -1) { m.members[i] = key; ui.avisoMesa = { txt: t('ms_cambia').replace('{x}', v.name) }; return; }
  if (m.members.length >= max) { ui.avisoMesa = { txt: t('tm_lleno').replace(/\{n\}/g, max).replace('{x}', fullLabel(v)) }; return; }
  m.members.push(key);
}
function botonPoner (v) {
  const ya = U.mesa.members.includes(v.key);
  return `<button class="btn sm ${ya ? '' : 'primary'}" data-a="mesaPoner" data-key="${v.key}" ${ya ? 'disabled' : ''}>${h(t(ya ? 'ms_en_mesa' : 'ms_poner'))}</button>`;
}
/** La lista de la izquierda (en la ficha y en Equipos): el roster con sus filtros, su búsqueda y su orden (los mismos
 *  del roster: una sola regla, rosterData), para pasar de uno a otro y poner en la mesa. */
function panelListaHtml () {
  const lista = rosterData(), P = U.prefs, activos = filtrosActivos(), total = allVariants().length;
  const v = ui.view === 'detail' ? variant(ui.charId, ui.uniformId) : null;
  return `<div class="panelcab"><span>${h(t('ms_lista_n').replace('{n}', lista.length).replace('{t}', total))}</span>
      ${ui.view === 'detail' ? `<button class="btn sm" data-a="back">${h(t('nav_roster'))}</button>` : ''}</div>
    <div class="plfiltros">
      <div class="search"><input id="q" placeholder="${h(t('search_ph'))}" value="${h(ui.search)}" data-a="search"></div>
      <div class="row">
        <button class="btn sm ${ui.plFiltros ? 'primary' : ''}" data-a="plFiltros" aria-expanded="${ui.plFiltros}">${h(t('filters'))}${activos ? ' · ' + activos : ''}</button>
        ${activos || ui.search ? `<button class="btn sm" data-a="clearFilters">${h(t('clear'))}</button>` : ''}
        <div class="seg">${[['todo', 'all'], ['base', 'bases'], ['uni', 'uniforms']].map(([k, c]) =>
          `<button class="${P.kind === k ? 'on' : ''}" data-a="kind" data-v="${k}">${h(t(c))}</button>`).join('')}</div>
      </div>
      ${ui.plFiltros ? `<div class="filterpanel plpanel">${filtrosHtml()}</div>` : ''}
    </div>
    <div class="plitems">${lista.length ? lista.map(x => `<div class="plit${v && x.key === v.key ? ' on' : ''}">
      <button class="plabrir" data-a="fichaVecina" data-cid="${x.cid}" data-uid="${x.uid || ''}" ${v && x.key === v.key ? 'aria-current="true"' : ''}>
        <span class="plfoto" style="--cc:${classColor(x.c)}">${shot(x.id)}</span>
        <span class="pltx"><b>${h(x.name)}</b><small>${h(x.uid ? x.sub : t('base_word'))}</small></span>
        <span class="tag dim">${h(x.t)}</span></button>
      ${U.mesa.members.includes(x.key) ? `<span class="plmas en" title="${h(t('ms_en_mesa'))}" aria-label="${h(t('ms_en_mesa'))}">✓</span>`
        : `<button class="plmas" data-a="mesaPoner" data-key="${x.key}" title="${h(t('ms_poner') + ': ' + fullLabel(x))}" aria-label="${h(t('ms_poner') + ': ' + fullLabel(x))}">+</button>`}
    </div>`).join('') : `<p class="muted plvacio">${h(t('no_match'))}</p>`}</div>`;
}
function mesaHtml () {
  const m = U.mesa, vs = mesaVs(), max = tamModo(m.modeId), modos = modosEquipo(), lider = vs[0] || null;
  const rs = restriccionMesa();
  // Personajes que ya están en otro equipo de tu cuenta del mismo modo: dentro de un modo no se repiten (las dos
  // escuadras de Alliance Conquest). Se avisa; no se impide.
  // El equipo guardado igual al de la mesa no cuenta: es el mismo.
  const enModo = new Map(), este = m.members.slice().sort().join('|');
  if (m.modeId) U.teams.filter(tt => tt.modeId === m.modeId && tt.members.join('|') !== este)
    .forEach(tt => tt.members.forEach(k => { const cid = k.split('::')[0]; if (!enModo.has(cid)) enModo.set(cid, tt.name); }));
  const bonos = [];
  for (const a of vs) for (const b of BONOS_DE[a.cid] || []) if (b.m[0] === a.cid && estanTodos(b.m, vs)) bonos.push(b);
  const lugares = [];
  for (let i = 0; i < Math.max(max, vs.length); i++) {
    const x = vs[i];
    lugares.push(x ? `<div class="mslot${i === 0 ? ' lider' : ''}${i >= max ? ' sobra' : ''}">
        <button class="msfoto" data-a="fichaVecina" data-cid="${x.cid}" data-uid="${x.uid || ''}" title="${h(fullLabel(x))}" style="--cc:${classColor(x.c)}">${shot(x.id)}</button>
        <div class="mstx"><span class="msrol">${i === 0 ? h(t('ms_lider')) : '&nbsp;'}</span><b>${h(x.name)}</b><small>${h(x.uid ? x.sub : t('base_word'))}</small></div>
        <div class="msacc">${i > 0 ? `<button class="btn icon sm" data-a="mesaLider" data-i="${i}" title="${h(t('ms_hacer_lider'))}" aria-label="${h(t('ms_hacer_lider') + ': ' + fullLabel(x))}">↑</button>` : ''}
          <button class="btn icon sm" data-a="mesaQuitar" data-i="${i}" title="${h(t('ms_quitar'))}" aria-label="${h(t('ms_quitar') + ': ' + fullLabel(x))}">×</button></div>
      </div>` : `<div class="mslot libre"><span class="msfoto"></span><div class="mstx"><b>${h(t('ms_libre'))}</b>${i === vs.length ? `<small>${h(t('ms_libre_nota'))}</small>` : ''}</div></div>`);
  }
  const dias = [...new Set(ABX.restricciones.map(r => r.d))].sort((a, b) => a - b);
  const avisos = [ui.avisoMesa && !ui.avisoMesa.ok ? ui.avisoMesa.txt : null,
    vs.length > max ? t('tm_sobran').replace('{n}', max).replace('{m}', vs.length).replace('{k}', vs.length - max) : null,
    ...vs.filter(x => enModo.has(x.cid)).map(x => t('tm_dup').replace('{x}', x.name).replace('{e}', enModo.get(x.cid)))].filter(Boolean);
  return `<div class="panelcab"><span>${h(t('ms_title'))} · ${h(t('ms_team'))}</span><span>${vs.length} / ${max}</span></div>
    <div class="msbloque">
      <select data-a="mesaModo" aria-label="${h(t('ms_modo'))}">
        <option value="">${h(t('tm_nomode'))}</option>
        ${[[true, 'tm_modes_game'], [false, 'tm_modes_own']].map(([juego, k]) => { const ms = modos.filter(x => x.juego === juego);
          return ms.length ? `<optgroup label="${h(t(k))}">${ms.map(x => `<option value="${x.id}" ${x.id === m.modeId ? 'selected' : ''}>${h(x.name)} (${x.tam})</option>`).join('')}</optgroup>` : ''; }).join('')}
      </select>
      ${rs ? `<div class="row msabx"><label>${h(t('ms_dia'))} <select data-a="mesaDia">${dias.map(d => `<option value="${d}" ${d === m.abxDia ? 'selected' : ''}>${d}</option>`).join('')}</select></label>
        <label>${h(t('ms_dif'))} <select data-a="mesaDif">${ABX.restricciones.filter(r => r.d === m.abxDia).map(r => `<option ${r.m === rs.m ? 'selected' : ''}>${h(r.m)}</option>`).join('')}</select></label></div>` : ''}
    </div>
    <div class="msslots">${lugares.join('')}</div>
    ${ui.avisoMesa && ui.avisoMesa.ok ? `<div class="okmesa">✓ ${h(ui.avisoMesa.txt)}</div>` : ''}
    ${avisos.map(x => `<div class="avisoeq">⚠ ${h(x)}</div>`).join('')}
    ${rs ? `<div class="panelcab sub"><span>${h(t('ms_restr'))}</span></div><div class="msbloque">
      ${rs.r.length ? `<table class="msrestr"><thead><tr><th></th>${vs.map(x => `<th title="${h(fullLabel(x))}">${h(x.name.slice(0, 3))}</th>`).join('')}</tr></thead>
        <tbody>${rs.r.map(x => `<tr><td>${icon(x)}${h(dom(x))}</td>${vs.map(y => cumpleRestriccion(y, x) ? '<td class="si">✓</td>' : '<td class="no">✗</td>').join('')}</tr>`).join('')}</tbody></table>`
        : `<p class="muted">${h(t('md_no_restr'))}</p>`}
      <div class="fuentes muted">${h(t('ms_restr_src'))}</div></div>` : ''}
    ${vs.length >= 2 ? `<div class="panelcab sub"><span>${h(t('ms_recibe'))}</span></div><div class="msbloque">
      ${vs.map(x => `<div class="msrecibe"><b>${h(x.name)}</b>${coberturaHtml(cobertura(x, vs, lider))}</div>`).join('')}
      <p class="muted">${h(t('ms_recibe_nota'))}</p></div>
    <div class="panelcab sub"><span>${h(t('ms_bonos'))}</span></div><div class="msbloque">
      ${bonos.length ? bonos.map(b => `<div class="msbono"><b>${h(b.n || t('bn_noname'))}</b> <span class="muted">${h(b.m.map(c => CHAR_BY_ID[c].name).join(' + '))}</span>
        ${b.vs.map(v => `<div class="muted">${h(v.fx.map(f => efectoSoporteTxt(v, f)).join(' · '))}</div>`).join('')}</div>`).join('')
        : `<p class="muted">${h(t('ms_sin_bonos'))}</p>`}</div>` : ''}
    <div class="msbloque">
      <input data-a="mesaNombre" value="${h(m.name)}" placeholder="${h(t('ms_nombre_ph'))}" aria-label="${h(t('ms_nombre_ph'))}">
      <div class="row"><button class="btn primary" data-a="mesaGuardar" ${vs.length < 2 || vs.length > max ? 'disabled' : ''}>${h(t('ms_guardar'))}</button>
        <button class="btn" data-a="mesaVaciar" ${vs.length || m.name ? '' : 'disabled'}>${h(t('ms_vaciar'))}</button></div>
    </div>
    <div class="panelcab sub"><span>${h(t('ms_cmp'))}</span><span>${ui.picks.length} / ${MAX_COMPARAR}</span></div>
    <div class="msbloque">
      ${ui.picks.length ? ui.picks.map(pk => { const x = variant(pk.cid, pk.uid);
        return `<div class="mscmp"><button class="plabrir" data-a="fichaVecina" data-cid="${x.cid}" data-uid="${x.uid || ''}"><span class="plfoto" style="--cc:${classColor(x.c)}">${shot(x.id)}</span>
          <span class="pltx"><b>${h(x.name)}</b><small>${h(x.uid ? x.sub : t('base_word'))}</small></span></button>
          <button class="btn icon sm" data-a="unpick" data-cid="${x.cid}" data-uid="${x.uid || ''}" aria-label="${h(t('ms_quitar') + ': ' + fullLabel(x))}">×</button></div>`; }).join('')
        : `<p class="muted">${h(t('ms_cmp_vacio'))}</p>`}
      ${ui.avisoPick ? `<div class="avisoeq">⚠ ${h(ui.avisoPick)}</div>` : ''}
      ${ui.picks.length >= 2 ? `<button class="btn primary" data-a="goCompare">${h(t('ms_cmp_ir').replace('{n}', ui.picks.length))}</button>` : ''}
    </div>`;
}
/** Pestañas de abajo en una ventana angosta: qué panel se ve. */
function movilTabsHtml (conLista) {
  const tabs = (conLista ? [['lista', t('ms_lista_tab')]] : []).concat([['centro', t('ms_ver_tab')], ['mesa', t('ms_title') + ' · ' + U.mesa.members.length]]);
  return `<nav class="movtabs" aria-label="${h(t('ms_title'))}">${tabs.map(([k, n]) => `<button data-a="movil" data-v="${k}" aria-pressed="${ui.movil === k}">${h(n)}</button>`).join('')}</nav>`;
}

// ============================================================================
// EDITOR DE PERSONAJES (capa de usuario)
// ============================================================================
function blankDraft () {
  return { name:'', c:'Combate', f:SEED.FACTIONS[0], r:[], t:'T2', ins:SEED.INSTINCTS[0], race:SEED.RACES[0],
           gender:SEED.GENDERS[0], origin:'Original MFF', abilities:[], tuc:[], stats:{}, striker:4, wba:'',
           trans:false, new:false, uniforms:[] };
}
function renderEditor () {
  const d = ui.edDraft, steps = [t('ed_step_data'), t('ed_step_unis'), t('ed_step_review')];
  const pick = (opts, field, multi) => opts.map(v => {
    const on = multi ? d[field].includes(v) : d[field] === v;
    return `<button class="chip ${on ? 'on' : ''}" data-a="edPick" data-f="${field}" data-v="${h(v)}" data-multi="${multi ? 1 : 0}">${icon(v)}${h(dom(v))}</button>`;
  }).join('');
  const field = (label, inner) => `<div style="margin-bottom:12px"><div class="lbl" style="font-size:10px;text-transform:uppercase;letter-spacing:.09em;color:var(--text-3);margin-bottom:6px;font-weight:700">${h(label)}</div>${inner}</div>`;
  let body = '';
  if (ui.edStep === 0) {
    body = field(t('ed_name'), `<input style="width:100%;max-width:420px" data-a="edField" data-f="name" value="${h(d.name)}">`)
      + field(t('f_class'), `<div class="row">${pick(SEED.CLASSES, 'c', false)}</div>`)
      + field(t('f_side'), `<div class="row">${pick(SEED.FACTIONS, 'f', false)}</div>`)
      + field(t('f_tier'), `<div class="row">${pick(SEED.TIERS, 't', false)}</div>`)
      + field(t('f_instinct'), `<div class="row">${pick(SEED.INSTINCTS, 'ins', false)}</div>`)
      + field(t('f_race'), `<div class="row">${pick(SEED.RACES, 'race', false)}</div>`)
      + field(t('d_gender'), `<div class="row">${pick(SEED.GENDERS, 'gender', false)}</div>`)
      + field(t('c_roles'), `<div class="row">${pick(SEED.ROLES, 'r', true)}</div>`)
      + field(t('cmp_abilities'), `<div class="row">${pick(SEED.SKILL_TAGS, 'abilities', true)}</div>`)
      + field(t('ed_striker'), `<input type="number" min="1" max="6" style="width:90px" data-a="edField" data-f="striker" value="${h(d.striker)}">`);
  } else if (ui.edStep === 1) {
    body = d.uniforms.map((u, i) => `<div class="card" style="margin-bottom:12px">
      <div class="row">
        <input placeholder="${h(t('ed_uni_name'))}" style="flex:2;min-width:180px" data-a="edUni" data-i="${i}" data-f="name" value="${h(u.name)}">
        <select data-a="edUni" data-i="${i}" data-f="tier">${SEED.TIERS.map(x => `<option ${x === u.tier ? 'selected' : ''}>${x}</option>`).join('')}</select>
        <input placeholder="${h(t('ed_cost'))}" style="flex:1;min-width:120px" data-a="edUni" data-i="${i}" data-f="cost" value="${h(u.cost || '')}">
        <button class="btn sm danger" data-a="edUniDel" data-i="${i}">✕</button>
      </div>
    </div>`).join('') + `<button class="btn" data-a="edUniAdd">${h(t('ed_add_uni'))}</button>`
      + `<p class="muted" style="margin-top:12px">${h(t('ed_no_skills'))}</p>`;
  } else {
    body = `<div class="card"><div style="font-weight:700;font-size:17px">${h(d.name || 'Sin nombre')}</div>
      <div class="muted">${[dom(d.c), dom(d.f), d.t, dom(d.ins), d.r.map(dom).join('/')].filter(Boolean).join(' · ')}</div>
      <div class="muted">${pluralUni(d.uniforms.length)}</div></div>`;
  }
  return `<div class="page-head"><div><h1>${h(ui.edId ? t('ed_edit') : t('ed_new'))}</h1>
    <div class="sub">${h(t('ed_note'))}</div></div></div>
  <div class="row" style="margin-bottom:18px">${steps.map((s, i) => `<button class="chip ${i === ui.edStep ? 'on' : ''}" data-a="edStep" data-i="${i}">${i + 1}. ${s}</button>`).join('')}</div>
  ${body}
  <div class="row" style="justify-content:space-between;margin-top:22px">
    <button class="btn" data-a="edPrev" ${ui.edStep === 0 ? 'disabled' : ''}>${h(t('ed_back'))}</button>
    <div class="row">
      ${ui.edId && U.charEdits[ui.edId] ? `<button class="btn danger" data-a="edRevert">${h(t('ed_discard'))}</button>` : ''}
      ${ui.edStep === 2 ? `<button class="btn primary" data-a="edSave">${h(t('ed_save'))}</button>` : `<button class="btn primary" data-a="edNext">${h(t('ed_next'))}</button>`}
    </div>
  </div>`;
}

// ============================================================================
// AJUSTES
// ============================================================================
function renderSettings () {
  const mine = Object.keys(U.charEdits).length + U.charNew.length;
  const changed = Object.values(U.assign).reduce((n, o) => n + Object.keys(o).length, 0);
  return `<div class="page-head"><div><h1>${h(t('st_title'))}</h1>
    <div class="sub">${h(t('st_note'))}</div></div></div>

  <div class="section"><h3>${h(t('st_layer'))}</h3>
    <div class="statgrid">
      <div class="stat"><div class="k">${h(t('st_own_chars'))}</div><div class="v">${mine}</div></div>
      <div class="stat"><div class="k">${h(t('st_teams'))}</div><div class="v">${U.teams.length}</div></div>
      <div class="stat"><div class="k">${h(t('st_own_lists'))}</div><div class="v">${U.lists.length}</div></div>
      <div class="stat"><div class="k">${h(t('st_list_changes'))}</div><div class="v">${changed}</div></div>
      <div class="stat"><div class="k">${h(t('st_images'))}</div><div class="v">${Object.keys(U.images).length}</div></div>
      <div class="stat"><div class="k">${h(t('st_marks'))}</div><div class="v">${Object.keys(U.marcas || {}).length}</div></div>
      <div class="stat"><div class="k">${h(t('st_routes'))}</div><div class="v">${Object.keys(U.ruta).length}</div></div>
      <div class="stat"><div class="k">${h(t('st_caps'))}</div><div class="v">${Object.keys(U.topes).length}</div></div>
    </div>
    <div class="row" style="margin-top:12px">
      <button class="btn" data-a="exportUser">${h(t('st_export'))}</button>
      <label class="btn" style="cursor:pointer">${h(t('st_import'))}<input type="file" accept=".json" hidden data-a="importUser"></label>
      <button class="btn" data-a="exportCsv">${h(t('st_export_csv'))}</button>
      <button class="btn danger" data-a="resetUser">${h(t('st_reset'))}</button>
    </div>
  </div>

  ${seccionActualizaciones()}

  ${seccionGuiaArmado()}

  <div class="section"><h3>${h(t('st_brand'))}</h3>
    <div style="width:200px;height:52px;border-radius:var(--r-sm);overflow:hidden;background:var(--surface-2);display:flex;align-items:center;justify-content:center">
      ${U.images['brand-logo'] ? `<img src="${U.images['brand-logo']}" style="max-width:100%;max-height:100%">` : `<span class="muted">${h(t('st_no_logo'))}</span>`}
    </div>
    <div class="row" style="margin-top:10px">
      <label class="btn sm" style="cursor:pointer">${h(t('st_upload_logo'))}<input type="file" accept="image/*" hidden data-a="upload" data-img="brand-logo"></label>
      ${U.images['brand-logo'] ? `<button class="btn sm danger" data-a="clearImg" data-img="brand-logo">${h(t('st_remove'))}</button>` : ''}
    </div>
  </div>

  <div class="section"><h3>${h(t('st_modes'))}</h3>
    <p class="muted" style="margin-bottom:10px">${h(t('st_modes_note'))}</p>
    <div style="display:flex;flex-direction:column;gap:8px;max-width:520px">
      ${U.modes.map((m, i) => `<div class="row">
        <input value="${h(m.name)}" data-a="modeName" data-i="${i}" style="flex:1">
        <input type="number" min="1" max="8" value="${m.teamSize}" data-a="modeSize" data-i="${i}" style="width:80px">
        <button class="btn sm danger" data-a="modeDel" data-i="${i}">✕</button>
      </div>`).join('')}
    </div>
    <button class="btn sm" style="margin-top:10px" data-a="modeAdd">${h(t('st_add_mode'))}</button>
  </div>

  <div class="section"><h3>${h(t('st_translation'))}</h3>
    <p class="muted">${h(t('st_translation_txt'))}</p>
  </div>

  <div class="section"><h3>${h(t('st_sources'))}</h3>
    <p class="muted">${h(t('st_sources_txt'))}<a href="https://thanosvibs.money" target="_blank" rel="noopener">THANO$VIB$</a>${h(t('st_sources_txt2'))}<a href="https://future-fight.fandom.com" target="_blank" rel="noopener">Future Fight Wiki</a>${
      h(t('st_sources_txt3'))}<a href="https://docs.google.com/spreadsheets/d/1H0Hcl9oVZV9gA266xkJAqPv5bD1qwqhC5NeVbLj_-FE" target="_blank" rel="noopener">Cynicalex Mega Guides</a>${h(t('st_sources_txt4'))}</p>
  </div>`;
}

/** Estado de la guía de armado de Cynicalex: qué versión se usa, cuándo se revisó por
 *  última vez y, si la planilla de esa revisión no se pudo usar, por qué. También lo que la
 *  app no cruza o no interpreta. */
function seccionGuiaArmado () {
  const G = GUIA_ARMADO;
  if (!G) return `<div class="section"><h3>${h(t('ga_title'))}</h3><p class="muted">${h(t('ga_no_data'))}</p></div>`;
  const E = G.estado, rx = E.rechazo, raros = Object.entries(G.raros);
  const nRaros = raros.reduce((n, [, xs]) => n + xs.length, 0);
  const COL = { ctp: 'C.T.P.', iso: 'Best ISO-8 Set', obelisco: 'Obelisk (SL/AC)', art: 'Needs Artifact?', bling: 'Tier List Bling' };
  return `<div class="section" id="guia-armado"><h3>${h(t('ga_title'))}</h3>
    <p class="muted" style="margin-bottom:12px">${h(t('ga_st_note'))}</p>
    <div class="statgrid" style="margin-bottom:12px">
      <div class="stat"><div class="k">${h(t('ga_st_version'))}</div><div class="v">${h(G.version)}</div>
        <div class="muted" style="font-size:11px">${h(t('ga_st_taken').replace('{f}', E.tomada))}</div></div>
      <div class="stat"><div class="k">${h(t('ga_st_checked'))}</div><div class="v">${h(E.comprobada)}</div>
        <div class="muted" style="font-size:11px">${h(t(rx ? 'ga_st_bad' : 'ga_st_ok'))}</div></div>
      <div class="stat"><div class="k">${h(t('ga_st_chars'))}</div><div class="v">${Object.keys(G.pj).length}</div></div>
    </div>
    ${rx ? `<div class="bloque aviso ga-rechazo" style="margin-bottom:12px"><p><b>⚠ ${h(t('ga_st_rejected').replace('{f}', E.comprobada)
        .replace('{n}', rx.version && rx.version !== G.version ? ' (' + rx.version + ')' : '').replace('{v}', G.version).replace('{t}', E.tomada))}</b></p>
      <ul class="sopfx">${rx.motivos.map(m => `<li>${h(m)}</li>`).join('')}</ul></div>` : ''}
    ${G.sin_pj.length ? `<details class="usgrupo"><summary>${h(t('ga_st_nopj').replace('{n}', G.sin_pj.length))}</summary>
      <ul class="sopfx">${G.sin_pj.map(x => `<li>${h(x)}</li>`).join('')}</ul></details>` : ''}
    ${nRaros ? `<details class="usgrupo"><summary>${h(t('ga_st_raros').replace('{n}', nRaros))}</summary>
      <ul class="sopfx">${raros.map(([k, xs]) => xs.map(x => `<li>${h(COL[k])}: <span class="sinint">${h(x)}</span></li>`).join('')).join('')}</ul></details>` : ''}
    <div class="fuentes">${fuentesHtml(['cyn-armado', 'cyn-tierlist'])}</div>
  </div>`;
}

/** Sección de actualizaciones de Ajustes. Se repinta sola (pintarActualizaciones) cuando
 *  llega la respuesta de GitHub o avanza una descarga. */
function seccionActualizaciones () {
  const loc = ESCRITORIO.datos_local || {}, n = NOV.datos || {}, rem = n.remoto || {};
  const p = PROG.datos;
  let estado;
  if (NOV.buscando) estado = `<span class="muted">${h(t('ac_checking'))}</span>`;
  else if (n.error || (NOV.app && NOV.app.error)) estado = `<span class="tag solid" style="background:var(--danger)">${h(t('av_check_err'))}</span> <span class="muted">${h([n.error, NOV.app && NOV.app.error].filter(Boolean).join(' · '))}</span>`;
  else if (p && p.corriendo) estado = `<span class="muted">${h(t('av_dl'))}…</span>`;
  else if (n.hay && !n.compatible) estado = `<span class="tag solid" style="background:var(--gold)">${h(t('av_incompat'))}</span>`;
  else if (n.hay || (NOV.app && NOV.app.hay)) estado = `<span class="tag solid" style="background:var(--gold)">${h(t(n.hay ? 'ac_new' : 'ac_new_app'))}</span>`;
  else if (NOV.hora) estado = `<span class="tag dim">${h(t('ac_uptodate'))}</span>`;
  else estado = '';
  return `<div class="section" id="seccion-actualizaciones"><h3>${h(t('ac_title'))}</h3>
    <p class="muted" style="margin-bottom:12px">${h(t('ac_note'))}</p>
    <div class="statgrid" style="margin-bottom:12px">
      <div class="stat"><div class="k">${h(t('ac_app'))}</div><div class="v">${h(ESCRITORIO.version)}</div>
        <div class="muted" style="font-size:11px">${NOV.app && NOV.app.hay ? h(t('ap_new').replace('{v}', NOV.app.version)) : ''}</div></div>
      <div class="stat"><div class="k">${h(t('ac_local'))}</div><div class="v">${h(loc.juego || '?')}</div>
        <div class="muted" style="font-size:11px">${h(t('ac_built'))} ${h(loc.generado || '?')}</div></div>
      <div class="stat"><div class="k">${h(t('ac_remote'))}</div><div class="v">${h(rem.juego || '—')}</div>
        <div class="muted" style="font-size:11px">${rem.generado ? h(t('ac_built') + ' ' + rem.generado) : ''}
          ${NOV.hora ? ' · ' + h(t('ac_checked')) + ' ' + h(NOV.hora.toLocaleTimeString(LANG === 'es' ? 'es-AR' : 'en-US', { hour: '2-digit', minute: '2-digit', hour12: LANG !== 'es' })) : ''}</div></div>
    </div>
    <div class="row" style="margin-bottom:12px">${estado}
      <button class="btn sm" data-a="buscarNovedades" ${NOV.buscando || (p && p.corriendo) ? 'disabled' : ''}>${h(t('ac_check'))}</button></div>
    <p class="muted" style="margin-bottom:8px">${h(t('ac_img'))}: ${h(imagenesTexto())}</p>
    <p class="muted">${h(t('ac_folder'))}: <code>${h(ESCRITORIO.datos)}</code>. ${h(t('ac_folder_note'))}</p>
  </div>`;
}
function imagenesTexto () {
  const im = ESCRITORIO.imagenes, r = PROG.imagenes && PROG.imagenes.resultado;
  const np = r ? r.no_publicadas.length : 0;
  if (!im.faltan) return t('ac_img_ok').replace('{total}', im.total);
  return t('ac_img_miss').replace('{n}', im.faltan).replace('{total}', im.total) + (np ? ' ' + t('ac_img_np').replace('{n}', np) : '');
}
function pintarActualizaciones () {
  const el = $('#seccion-actualizaciones');
  if (el) el.outerHTML = seccionActualizaciones();
}

// ============================================================================
// NAV + DISPATCH
// ============================================================================
function renderNav () {
  const link = (view, clave, act) => `<button class="navlink ${ui.view === view ? 'on' : ''}" data-a="${act}">${h(t(clave))}</button>`;
  return `<nav class="topnav">
    <span class="brand" data-a="back">${U.images['brand-logo']
      ? `<img src="${U.images['brand-logo']}" style="height:26px">`
      : `<span class="dot"></span>TA GUIANAEL <span style="color:var(--accent)">MFF</span>`}</span>
    ${link('roster','nav_roster','back')}
    ${link('tierlist','nav_tierlists','goTier')}
    ${link('modos','nav_modes','goModos')}
    ${link('teams','nav_teams','goTeams')}
    ${link('glosario','nav_glossary','goGlosario')}
    ${link('historico','nav_history','goHistorico')}
    <span class="navspace"></span>
    <div class="navtools">
      <button class="langbtn" data-a="lang" title="${h(t('lang_title'))}">
        <span class="${LANG === 'es' ? 'on' : ''}">ES</span><span class="${LANG === 'en' ? 'on' : ''}">EN</span>
      </button>
      ${link('editor','nav_new_char','goEditor')}
      ${link('settings','nav_settings','goSettings')}
    </div>
  </nav>`;
}
function render () {
  anotarLugar();
  // El «Cómo funciona» de una skill es de la pestaña Skills en que se abrió: si se pinta otra cosa, queda cerrado. La
  // ventana del «Por qué», lo mismo con la pestaña Equipos (anotarLugar ya la anotó para volver con «Atrás»).
  if (ui.tip && !tipVigente()) ui.tip = null;
  if (ui.pq && !pqVigente(ui.pq)) cerrarPq(false);
  let body;
  switch (ui.view) {
    case 'detail':   body = renderDetail(); break;
    case 'compare':  body = renderCompare(); break;
    case 'tierlist': body = renderTierList(); break;
    case 'modos':    body = renderModos(); break;
    case 'teams':    body = renderTeams(); break;
    case 'glosario': body = renderGlosario(); break;
    case 'historico': body = renderHistorico(); break;
    case 'editor':   body = renderEditor(); break;
    case 'settings': body = renderSettings(); break;
    default:         body = renderRoster();
  }
  // Los avisos van fuera de <main>: la barra del roster se pega arriba de main con margen
  // negativo y los taparía.
  // Tres paneles (ver MESA DE TRABAJO): la lista y la mesa conservan su desplazamiento al repintar.
  const conLista = (ui.view === 'detail' && ui.charId != null) || ui.view === 'teams', previo = {};
  for (const sel of ['.plista', '.mesa']) { const x = $(sel); if (x) previo[sel] = x.scrollTop; }
  $('#app').innerHTML = renderNav() + '<div id="avisos" class="avisos">' + avisosHtml() + '</div>'
    + `<div class="trabajo${conLista ? ' con-lista' : ''}" data-movil="${ui.movil}">`
    + (conLista ? `<aside class="plista" aria-label="${h(t('ms_lista_tab'))}">${panelListaHtml()}</aside>` : '')
    + '<main>' + body + '</main>'
    + `<aside class="mesa" aria-label="${h(t('ms_title'))}">${mesaHtml()}</aside></div>` + movilTabsHtml(conLista)
    + (ui.aliados != null ? aliadosModal() : '') + tipHtml();
  for (const sel in previo) { const x = $(sel); if (x) x.scrollTop = previo[sel]; }
  const actual = $('.plista .plit.on'), pl = $('.plista');
  if (actual && pl && (actual.offsetTop < pl.scrollTop || actual.offsetTop + actual.offsetHeight > pl.scrollTop + pl.clientHeight))
    pl.scrollTop = actual.offsetTop - pl.clientHeight / 2;
  const q = $('#q');
  if (q && ui.focusSearch) { q.focus(); q.setSelectionRange(q.value.length, q.value.length); }
  sincronizarLugar();
  if (ui.tip) posicionarTip();
}

// ============================================================================
// HISTORIAL («Atrás»)
// Cada lugar (una vista; en la ficha, un personaje) es una entrada del historial de la
// ventana. Al irse de un lugar queda anotado cómo estaba (uniforme, pestaña, página de las
// combinaciones o del roster, posición, los plegados con id que estaban abiertos y la ventana
// del «Por qué» de una tarjeta, con su pestaña y su altura), y «Atrás» —el botón de la ficha,
// Alt+← o el botón de volver del mouse— vuelve a ese lugar tal cual. Ir a una skill desde un
// «Por qué» abre otra entrada aunque sea la ficha del mismo personaje (el líder puede ser él).
// ============================================================================
function lugar () { return ui.view === 'detail' ? 'detail:' + ui.charId : ui.view; }
function fotoLugar () {
  return { lugar: lugar(), view: ui.view, charId: ui.charId, uniformId: ui.uniformId, fichaTab: ui.fichaTab,
           eqPagina: ui.eqPagina, eqCon: ui.eqCon, eqVerDescartados: ui.eqVerDescartados, page: ui.page, tierList: ui.tierList };
}
/** Antes de pintar: si cambió el lugar, el anterior queda anotado con su posición y se abre
 *  una entrada nueva que recuerda de dónde se vino. */
function anotarLugar () {
  const previo = history.state, nueva = ui.entradaNueva;
  ui.entradaNueva = false;
  if (!previo || !previo.lugar) { history.replaceState({ ...fotoLugar(), n: 0, y: 0, abiertos: [], desde: null }, ''); return; }
  if (previo.lugar === lugar() && !nueva) return;
  history.replaceState({ ...previo, y: scrollY, abiertos: [...document.querySelectorAll('main details[open][id]')].map(d => d.id), pq: pqAnotado() }, '');
  ui.volverY = null;
  history.pushState({ ...fotoLugar(), n: previo.n + 1, y: 0, abiertos: [],
                      desde: { view: previo.view, charId: previo.charId, uniformId: previo.uniformId, fichaTab: previo.fichaTab } }, '');
}
/** Después de pintar: la entrada actual sigue lo que cambió en el lugar (pestaña, uniforme,
 *  página), para volver a él como quedó. */
function sincronizarLugar () {
  const s = history.state, nuevo = { ...s, ...fotoLugar() };
  if (JSON.stringify(nuevo) !== JSON.stringify(s)) history.replaceState(nuevo, '');
}
/** El lugar del que se vino, si lo hay. */
function lugarAnterior () { const s = history.state; return s && s.n > 0 ? s.desde : null; }
/** Nombre de un lugar: el personaje (con su uniforme y la pestaña) o la sección. */
function nombreLugar (d, largo) {
  if (d.view === 'detail') {
    const v = variant(d.charId, d.uniformId);
    if (!v) return t('nav_roster');
    return largo ? fullLabel(v) + ' · ' + t('ft_' + d.fichaTab) : v.name;
  }
  return t({ tierlist: 'nav_tierlists', modos: 'nav_modes', teams: 'nav_teams', glosario: 'nav_glossary', historico: 'nav_history', settings: 'nav_settings',
             editor: 'nav_new_char', compare: 'cmp_title' }[d.view] || 'nav_roster');
}
window.addEventListener('popstate', (e) => {
  const s = e.state;
  if (!s || !s.lugar) return;
  if (ui.pq) cerrarPq(false);
  Object.assign(ui, { view: s.view, charId: s.charId, uniformId: s.uniformId, fichaTab: s.fichaTab, eqPagina: s.eqPagina,
                      eqCon: s.eqCon, eqVerDescartados: s.eqVerDescartados, page: s.page, tierList: s.tierList,
                      aliados: null, tip: null, tlPick: null, focusSearch: false, volverY: s.y,
                      volverAbiertos: s.abiertos || [],   // una entrada anotada por una versión anterior no los trae
                      volverPq: s.pq || null });
  render();
  volverAPosicion();
});
/** Vuelve a la posición anotada, con los plegados que estaban abiertos (cambian el alto de la página;
 *  uno que ya no está, porque la lista cambió, no se abre) y la ventana del «Por qué», si estaba abierta
 *  y su tarjeta sigue en la página. Si la pestaña Equipos todavía calcula las combinaciones, se aplica
 *  cuando termina (la lista cambia el alto de la página). */
function volverAPosicion () {
  if (ui.volverY == null || ui.eqCalculando) return;
  for (const id of ui.volverAbiertos) { const d = document.getElementById(id); if (d) d.open = true; }
  window.scrollTo({ top: ui.volverY, behavior: 'instant' });   // sin la animación de html{scroll-behavior}
  const pq = ui.volverPq;
  ui.volverY = null; ui.volverAbiertos = []; ui.volverPq = null;
  if (pq && pqVigente(pq) && botonPq(pq.id)) abrirPq(pq);
}
/** Lleva a la vista un elemento de la ficha (una skill, el artefacto), debajo de la cabecera fija, y lo
 *  resalta hasta que se vuelva a pintar. */
function resaltar (id) {
  const el = document.getElementById(id);
  if (!el) throw new Error('la ficha no tiene el ancla ' + id);
  const arriba = document.querySelector('nav.topnav').offsetHeight + document.querySelector('.fcab').offsetHeight + 14;
  window.scrollTo({ top: el.getBoundingClientRect().top + scrollY - arriba, behavior: 'instant' });
  el.classList.add('resaltada');
}

// ============================================================================
// EVENTOS
// ============================================================================
document.addEventListener('click', (e) => {
  // Con el «Cómo funciona» de una skill abierto, tocar afuera lo cierra y el toque sigue su curso (si fue otra
  // skill, la abre); si fue lo mismo que lo abrió, solo lo cierra. Si el foco no quedó en otra cosa, vuelve a
  // la skill.
  const tipAntes = ui.tip && !e.target.closest('#skpop') ? ui.tip : null;
  if (tipAntes) cerrarTip(document.activeElement === document.body);
  const el = e.target.closest('[data-a]'); if (!el) return;
  const a = el.getAttribute('data-a'), d = el.dataset;
  const P = U.prefs;
  if (/^go/.test(a) || a === 'back') ui.movil = 'centro';   // ir a otra sección muestra la sección (ventana angosta)
  switch (a) {
    case 'back': {
      const ant = lugarAnterior();
      if (ant && ant.view === 'roster') { history.back(); break; }
      ui.view = 'roster'; ui.charId = null; ui.focusSearch = false; render(); break; }
    case 'atras': history.back(); break;
    case 'lang': LANG = U.prefs.lang = (LANG === 'es' ? 'en' : 'es'); commit(); break;
    case 'toggleFilters': P.filtersOpen = !P.filtersOpen; commit(); break;
    case 'clearFilters': P.filters = { c:[], r:[], t:[], f:[], ins:[], race:[], origin:[], ab:[], lid:[], sop:[] };
      P.flags = { t4:false, trans:false, nuevo:false }; P.kind = 'todo'; P.objetivo = ''; P.atributo = '';
      P.para = ''; P.restr = '';
      ui.search = ''; ui.page = 0; commit(); break;
    case 'filter': { const cur = P.filters[d.cat];
      P.filters[d.cat] = cur.includes(d.v) ? cur.filter(x => x !== d.v) : cur.concat(d.v);
      ui.page = 0; commit(); break; }
    case 'flag': P.flags[d.v] = !P.flags[d.v]; ui.page = 0; commit(); break;
    case 'paraQuitar': P.para = ''; ui.page = 0; commit(); break;
    case 'paraVer': { const v = variant(ui.charId, ui.uniformId), cats = categoriasQueSirven(v);
      P.filters.lid = d.tipo === 'lid' ? cats : []; P.filters.sop = d.tipo === 'sop' ? cats : [];
      // La búsqueda se vacía: casi siempre es la que se usó para llegar a este personaje.
      P.para = v.key; P.restr = ''; P.filtersOpen = true; ui.search = '';
      ui.view = 'roster'; ui.charId = null; ui.page = 0; commit(); window.scrollTo(0, 0); break; }
    case 'view': P.view = d.v; ui.page = 0; commit(); break;
    case 'kind': P.kind = d.v; ui.page = 0; commit(); break;
    case 'dir': P.dir = -P.dir; commit(); break;
    case 'page': ui.page = parseInt(d.p, 10); render(); window.scrollTo({top:0,behavior:'smooth'}); break;
    case 'pickMode': ui.pickMode = !ui.pickMode; ui.avisoPick = null; ui.view = 'roster'; render(); break;
    // «+ Comparar esta versión» la suma y lleva al roster a elegir las otras; las elegidas se ven en la mesa.
    case 'pick': case 'pickThis': {
      e.stopPropagation();
      togglePick(d.cid, d.uid || null);
      if (a === 'pickThis') { ui.pickMode = true; ui.view = 'roster'; }
      render(); break; }
    case 'unpick': { const key = d.cid + '::' + (d.uid || 'base');
      ui.picks = ui.picks.filter(p => p.key !== key); ui.avisoPick = null;
      if (ui.picks.length < 2 && ui.view === 'compare') ui.view = 'roster';
      render(); break; }
    case 'goCompare': ui.view = 'compare'; ui.avisoPick = null; render(); window.scrollTo(0, 0); break;
    case 'open': {
      ui.tlPick = null; ui.aliados = null;
      if (ui.pickMode) { togglePick(d.cid, d.uid || null); render(); break; }
      abrirFicha(d.cid, d.uid); break; }
    case 'fichaVecina': abrirFicha(d.cid, d.uid); break;
    // Desde el «Por qué» de una tarjeta de equipo: la skill (o el artefacto) en la ficha de quien la da.
    case 'irSkill': ui.entradaNueva = true; ui.fichaTab = d.tab; abrirFicha(d.cid, d.uid); resaltar(d.ancla); break;
    case 'uniform': ui.uniformId = d.uid; ui.eqPagina = 0; render(); break;
    case 'fichaTab': ui.fichaTab = d.v; render(); irA('fcuerpo'); break;
    // Seleccionar texto de una skill no abre su «Cómo funciona».
    case 'skTip': { const si = +d.si, ti = d.st == null ? null : +d.st, fi = d.fx == null ? null : +d.fx;
      if (getSelection().toString() || (tipAntes && tipAntes.si === si && tipAntes.ti === ti && tipAntes.fi === fi)) break;
      abrirTip(si, ti, fi); break; }
    case 'tipCerrar': cerrarTip(true); break;
    // La ventana del «Por qué» de una tarjeta de equipo: arranca en el personaje de la ficha.
    case 'pqAbrir': abrirPq({ id: d.pq, charId: ui.charId, uid: ui.uniformId, tab: null, y: 0 }); break;
    case 'pqTab': elegirTabPq(+d.i); break;
    case 'pqCerrar': cerrarPq(true); break;
    case 'verAliados': ui.aliados = parseInt(d.tg, 10); render(); break;
    case 'aliadosCerrar': ui.aliados = null; render(); break;

    case 'goTier': ui.view = 'tierlist'; render(); break;
    case 'goModos': ui.view = 'modos'; render(); break;
    case 'goGlosario': ui.view = 'glosario'; ui.focusSearch = false; render(); break;
    case 'goHistorico': ui.view = 'historico'; ui.hiPj = d.cid || ''; ui.hiN = 20; render(); window.scrollTo(0, 0); break;
    case 'hiTipo': ui.hiTipo = d.v; ui.hiN = 20; render(); break;
    case 'hiMas': ui.hiN += 20; render(); break;
    case 'irGlos': {
      // Si la búsqueda deja afuera el destino, se vacía para que aparezca (sin volver a poner el
      // foco en la búsqueda: en el celular abriría el teclado).
      e.preventDefault();
      const tab = d.v.startsWith('ef-') ? 'app' : 'juego';
      if (ui.glTab !== tab) { ui.glTab = tab; render(); }
      if (!document.getElementById(d.v)) { ui.glBusca = ''; ui.focusSearch = false; render(); }
      const destino = document.getElementById(d.v);
      for (let x = destino; x; x = x.parentElement.closest('details')) if (x.tagName === 'DETAILS') x.open = true;
      destino.scrollIntoView({ behavior: 'smooth', block: 'start' });
      destino.classList.add('glfoco');
      setTimeout(() => destino.classList.remove('glfoco'), 1600);
      break; }
    case 'modoFiltro': ui.modoFiltro = d.v; render(); break;
    case 'modoAbrir': ui.modoAbierto = ui.modoAbierto === d.id ? null : d.id; render(); break;
    case 'verLista': ui.view = 'tierlist'; ui.tierList = d.id; render(); window.scrollTo(0, 0); break;
    case 'irArmado': e.preventDefault(); document.getElementById('armado')?.scrollIntoView({ behavior: 'smooth' }); break;
    case 'irArmadoModos': e.preventDefault(); ui.view = 'modos'; render();
      document.getElementById('armado')?.scrollIntoView({ behavior: 'smooth' }); break;
    case 'artEst': ui.artEst = d.v; render(); break;
    case 'irVerif': e.preventDefault(); ui.fichaTab = 'fuentes'; render(); irA('fcuerpo'); break;
    case 'ruta': if (d.v) U.ruta[d.cid] = d.v; else delete U.ruta[d.cid]; commit(); break;
    case 'pickList': ui.tierList = d.id; render(); break;
    case 'addList': { const name = ui.newListName.trim(); if (!name) break;
      const id = 'mia-' + Date.now();
      U.lists.push({ id, name, kind: ui.newListKind, rows: filasDePlantilla(ui.newListTpl) });
      ui.newListName = ''; ui.tierList = id; ui.editRows = false; commit(); break; }
    case 'dupList': { const orig = listById(d.id); if (!orig) break;
      const id = 'mia-' + Date.now();
      // Copia filas y ubicaciones efectivas (las de la fuente con tus cambios encima).
      U.lists.push({ id, name: listName(orig) + ' ' + t('tl_copy_suffix'), rows: rowsOf(orig).map(r => ({ id: r.id, label: r.label })) });
      U.assign[id] = JSON.parse(JSON.stringify(assignOf(orig.id)));
      ui.tierList = id; commit(); break; }
    case 'editRows': ui.editRows = !ui.editRows; render(); break;
    case 'rowAdd': { const l = U.lists.find(x => x.id === ui.tierList); if (!l) break;
      l.rows.push({ id: 'f-' + Date.now(), label: t('tp_new_row') }); commit(); break; }
    case 'rowMove': { const l = U.lists.find(x => x.id === ui.tierList); if (!l) break;
      const i = l.rows.findIndex(r => r.id === d.row), j = i + parseInt(d.dir, 10);
      if (i < 0 || j < 0 || j >= l.rows.length) break;
      [l.rows[i], l.rows[j]] = [l.rows[j], l.rows[i]];
      // Las filas de cada entrada se guardan en el orden de la lista: se reordenan.
      const orden = l.rows.map(r => r.id);
      Object.values(U.assign[l.id] || {}).forEach(fs => { if (fs) fs.sort((x, y) => orden.indexOf(x) - orden.indexOf(y)); });
      commit(); break; }
    case 'rowDel': { const l = U.lists.find(x => x.id === ui.tierList); if (!l || l.rows.length < 2) break;
      const mias = U.assign[l.id] || {};
      const n = Object.values(mias).filter(fs => fs && fs.includes(d.row)).length;
      if (n && !confirm(t('tl_row_del_confirm').replace('{n}', n))) break;
      l.rows = l.rows.filter(r => r.id !== d.row);
      for (const k in mias) {
        if (!mias[k]) continue;
        mias[k] = mias[k].filter(r => r !== d.row);
        if (!mias[k].length) delete mias[k];
      }
      commit(); break; }
    case 'removeList': { if (!confirm(t('tl_confirm_del'))) break;
      U.lists = U.lists.filter(l => l.id !== d.id); delete U.assign[d.id];
      ui.tierList = (LISTS[0] || {}).id || ''; commit(); break; }
    case 'resetList': delete U.assign[d.id]; commit(); break;
    case 'togglePool': ui.poolOpen = !ui.poolOpen; render(); break;
    case 'unassign': e.stopPropagation();
      setFilas(ui.tierList, d.key, filasDe(ui.tierList, d.key).filter(r => r !== d.row)); break;
    case 'tlAbrir': ui.tlPick = d.key; render(); break;
    case 'tlCerrar': ui.tlPick = null; render(); break;

    case 'goTeams': ui.view = 'teams'; render(); break;
    case 'eqIncluir': ui.eqExcluir = ui.eqExcluir.filter(c => c !== d.cid); ui.eqPagina = 0; render(); break;
    // Descartar y restaurar no cambian los datos del juego: sin rebuild(), la consulta queda.
    case 'descartar': if (!estaDescartado(d.c.split(','))) U.descartados.unshift(trioDe(d.c.split(','))); saveUser(); render(); break;
    case 'restaurar': { const k = trioDe(d.c.split(',')).join('|');
      U.descartados = U.descartados.filter(x => x.join('|') !== k); saveUser(); render(); break; }
    case 'eqVerDescartados': ui.eqVerDescartados = !ui.eqVerDescartados; ui.eqPagina = 0; render(); break;
    case 'eqPagina': ui.eqPagina = parseInt(d.p, 10); render(); irA('combos'); break;
    // ★ no cambia los datos del juego: se guarda sin rebuild() para no rehacer la consulta. Guarda el
    // contexto del orden en que se marcó (PvP, PvE o ninguno): su tarjeta lo usa para el C.T.P.
    case 'favorito': { const keys = d.m.split(','), c = claveFavorito(keys);
      const i = U.favoritos.findIndex(f => claveFavorito(f.members) === c);
      if (i > -1) U.favoritos.splice(i, 1); else U.favoritos.unshift({ id: 'fav-' + Date.now(), members: keys, ctx: contextoOrden() });
      saveUser(); render(); break; }
    // «Llevar a la mesa» (combinaciones, favoritos, tus equipos): el equipo reemplaza lo que había en la mesa, con su
    // líder primero, su modo y su nombre. No cambia de sección: la mesa está a la vista.
    case 'teamDesde': U.mesa.members = d.m.split(','); U.mesa.modeId = d.modo || ''; U.mesa.name = d.nombre || '';
      ui.avisoMesa = null; if (ui.movil !== 'centro') ui.movil = 'mesa'; saveUser(); render(); break;
    case 'mesaPoner': ponerEnMesa(d.key); saveUser(); render(); break;
    case 'mesaQuitar': U.mesa.members.splice(+d.i, 1); ui.avisoMesa = null; saveUser(); render(); break;
    case 'mesaLider': U.mesa.members.unshift(U.mesa.members.splice(+d.i, 1)[0]); saveUser(); render(); break;
    case 'mesaVaciar': U.mesa.members = []; U.mesa.name = ''; ui.avisoMesa = null; saveUser(); render(); break;
    // Se guarda en orden canónico (el que lo muestra va con su líder primero): el mismo equipo es uno solo. Si ya está
    // guardado con ese modo, no se repite y se dice.
    case 'mesaGuardar': { const m = U.mesa, max = tamModo(m.modeId);
      if (m.members.length < 2) { ui.avisoMesa = { txt: t('ms_pocos') }; render(); break; }
      if (m.members.length > max) break;
      const members = m.members.slice().sort(), modeId = m.modeId || '', lider = m.members[0];
      const ya = U.teams.find(x => x.modeId === modeId && x.lider === lider && x.members.join('|') === members.join('|'));
      if (ya) { ui.avisoMesa = { txt: t('tm_ya_esta').replace('{e}', ya.name) }; render(); break; }
      const nombre = m.name || mesaVs().map(fullLabel).join(' + ');
      U.teams.unshift({ id: 'eq-' + Date.now(), name: nombre, members, lider, reason: '', modeId });
      ui.avisoMesa = { txt: t('ms_guardado').replace('{e}', nombre), ok: true }; commit(); break; }
    case 'glTab': ui.glTab = d.v; render(); break;
    case 'plFiltros': ui.plFiltros = !ui.plFiltros; render(); break;
    case 'movil': ui.movil = d.v; render(); window.scrollTo(0, 0); break;
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
    case 'edUniAdd': ui.edDraft.uniforms.push({ id:'u-' + Date.now(), name:'', tier:'T2', cost:'', striker:4 }); render(); break;
    case 'edUniDel': ui.edDraft.uniforms.splice(parseInt(d.i, 10), 1); render(); break;
    case 'edRevert': delete U.charEdits[ui.edId]; ui.view = 'detail'; ui.charId = ui.edId; ui.edId = null; commit(); break;
    case 'edSave': { const dr = ui.edDraft;
      if (!dr.name.trim()) { alert(t('ed_need_name')); break; }
      const id = ui.edId || ('mio-' + dr.name.toLowerCase().replace(/[^a-z0-9]+/g, '-') + '-' + Date.now());
      const ch = Object.assign({}, dr, { id, uniforms: dr.uniforms.map((u, i) => Object.assign({}, u, { id: u.id || id + '-u' + i })) });
      if (ui.edId && CHARS_SEED.some(c => c.id === ui.edId)) U.charEdits[id] = ch;
      else if (ui.edId) U.charNew = U.charNew.map(c => c.id === id ? ch : c);
      else U.charNew.unshift(ch);
      ui.view = 'detail'; ui.charId = id; ui.uniformId = 'base'; ui.edId = null; commit(); break; }

    case 'marcarModo': ui.marcando = !ui.marcando; if (ui.marcando) ui.fichaTab = 'skills'; render(); break;
    case 'goSettings': ui.view = 'settings'; render(); break;
    case 'buscarNovedades': buscarNovedades(); break;
    case 'reintentarDatos': arrancarTarea('datos', '/api/datos/actualizar'); break;
    case 'reintentarImagenes': arrancarTarea('imagenes', '/api/imagenes/bajar'); break;
    case 'actualizarApp': actualizarApp(); break;
    case 'usarDatos': recargar(); break;
    case 'ocultarAviso': NOV.oculto = true; pintarAvisos(); break;
    case 'modeAdd': U.modes.push({ id:'modo-' + Date.now(), name:t('st_new_mode'), teamSize:3 }); commit(); break;
    case 'modeDel': U.modes.splice(parseInt(d.i, 10), 1); commit(); break;
    case 'clearImg': delete U.images[d.img]; commit(); break;
    case 'resetUser': if (confirm(t('st_confirm_reset'))) {
      U = blankUser(); commit(); } break;
    case 'reintentarGuardado': saveUser(); pintarAvisos(); break;
    case 'exportUser': download('mff-mi-capa.json', JSON.stringify(U, null, 2), 'application/json'); break;
    case 'exportCsv': exportCsv(); break;
  }
});

document.addEventListener('input', (e) => {
  const el = e.target.closest('[data-a]'); if (!el) return;
  const a = el.getAttribute('data-a'), d = el.dataset;
  if (a === 'search') { ui.search = el.value; ui.page = 0; ui.focusSearch = true; render(); return; }
  if (a === 'glBusca') { ui.glBusca = el.value; ui.focusSearch = true; render(); return; }
  if (a === 'newListName') { ui.newListName = el.value; return; }
  if (a === 'rowLabel') { const l = U.lists.find(x => x.id === ui.tierList); const r = l && l.rows.find(x => x.id === d.row);
    if (r) { r.label = el.value; saveUser(); } return; }
  if (a === 'listName') { const l = U.lists.find(x => x.id === d.id); if (l) { l.name = el.value; saveUser(); } return; }
  if (a === 'poolSearch') { ui.poolSearch = el.value; render(); $('[data-a="poolSearch"]')?.focus(); return; }
  if (a === 'mesaNombre') { U.mesa.name = el.value; saveUser(); return; }
  if (a === 'edField') { ui.edDraft[d.f] = el.value; return; }
  if (a === 'edUni') { ui.edDraft.uniforms[d.i][d.f] = el.value; return; }
  if (a === 'modeName') { U.modes[d.i].name = el.value; saveUser(); return; }
  if (a === 'modeSize') { U.modes[d.i].teamSize = Math.max(1, parseInt(el.value, 10) || 3); saveUser(); return; }
  if (a === 'tope') {
    const mis = U.topes[d.cid] = U.topes[d.cid] || {}, x = mis[d.k] = mis[d.k] || {};
    const n = parseFloat(el.value);
    if (el.value.trim() === '' || isNaN(n)) delete x[d.f]; else x[d.f] = n;
    if (!Object.keys(x).length) delete mis[d.k];
    if (!Object.keys(mis).length) delete U.topes[d.cid];
    saveUser();
    const it = GUIA.topes.items.find(i => i.stats.includes(d.k));
    const celda = document.querySelector(`[data-estado="${d.k}"]`);
    if (celda) celda.innerHTML = estadoTope(d.cid, d.k, it.tope);
    return; }
});

document.addEventListener('change', (e) => {
  const el = e.target.closest('[data-a]'); if (!el) return;
  const a = el.getAttribute('data-a'), d = el.dataset;
  if (a === 'sort') { U.prefs.sort = el.value; commit(); return; }
  if (a === 'newListTpl') { ui.newListTpl = el.value; return; }
  if (a === 'newListKind') { ui.newListKind = el.value; return; }
  if (a === 'abxDia') { ui.abxDia = parseInt(el.value, 10); render(); return; }
  if (a === 'uniformSel') { ui.uniformId = el.value; ui.eqPagina = 0; render(); return; }
  if (a === 'eqOrden') { ui.eqOrden = el.value; ui.eqPagina = 0; render(); return; }
  if (a === 'eqCon') { ui.eqCon = el.value; ui.eqPagina = 0; render(); return; }
  if (a === 'hiPj') { ui.hiPj = el.value; ui.hiN = 20; render(); return; }
  if (a === 'eqExcluir') { if (el.value) ui.eqExcluir = ui.eqExcluir.concat(el.value); ui.eqPagina = 0; render(); return; }
  if (a === 'eqCobertura') { ui.eqCobertura = COBERTURA.map(g => g.k).filter(k => k === d.g ? el.checked : ui.eqCobertura.includes(k));
    ui.eqPagina = 0; render(); return; }
  if (a === 'eqUltimo') { ui.eqUltimo = el.checked; ui.eqPagina = 0; render(); return; }
  if (a === 'rowLabel' || a === 'listName') { rebuild(); render(); return; }
  if (a === 'refList') { U.prefs.refList = el.value; commit(); return; }
  if (a === 'objetivo') { U.prefs.objetivo = el.value; ui.page = 0; commit(); return; }
  if (a === 'atributo') { U.prefs.atributo = el.value; ui.page = 0; commit(); return; }
  if (a === 'restr') { U.prefs.restr = el.value; ui.page = 0; commit(); return; }
  // Un modo más chico que el equipo no le saca a nadie: la mesa dice cuántos sobran y no guarda hasta que se quiten.
  if (a === 'teamLider') { U.teams.find(x => x.id === d.id).lider = el.value; ui.avisoLideres = null; commit(); return; }
  if (a === 'mesaModo') { U.mesa.modeId = el.value; ui.avisoMesa = null; saveUser(); render(); return; }
  if (a === 'mesaDia') { U.mesa.abxDia = parseInt(el.value, 10); U.mesa.abxDif = ''; saveUser(); render(); return; }
  if (a === 'mesaDif') { U.mesa.abxDif = el.value; saveUser(); render(); return; }
  if (a === 'edUni') { ui.edDraft.uniforms[d.i][d.f] = el.value; return; }
  if (a === 'marca') { marcar(d.p, d.sl, d.k, el.checked); return; }
  if (a === 'tlFila') { const actuales = filasDe(ui.tierList, ui.tlPick);
    setFilas(ui.tierList, ui.tlPick, el.checked ? actuales.concat(d.row) : actuales.filter(r => r !== d.row)); return; }
  if (a === 'upload') { const f = el.files[0]; if (f) readFile(f, url => { U.images[d.img] = url; commit(); }); return; }
  if (a === 'importUser') { const f = el.files[0]; if (!f) return;
    const r = new FileReader();
    r.onload = () => { try { U = normalizarCapa(JSON.parse(r.result)); commit(); }
                       catch (err) { alert(t('st_bad_import') + err.message); } };
    r.readAsText(f); return; }
});

// arrastrar y soltar en las tier lists: arrastrar mueve la entrada desde la fila de la
// que sale (las otras filas en las que esté no cambian); para sumarla a otra fila sin
// sacarla de esta está el selector que se abre al tocarla.
document.addEventListener('dragstart', (e) => {
  const el = e.target.closest('[draggable="true"][data-key]'); if (!el) return;
  ui.dragKey = el.dataset.key; ui.dragFrom = el.dataset.from || '';
  e.dataTransfer.setData('text/plain', el.dataset.key); e.dataTransfer.effectAllowed = 'move';
});
document.addEventListener('dragover', (e) => {
  const z = e.target.closest('[data-a="drop"]'); if (!z) return;
  e.preventDefault(); z.closest('.tierrow')?.classList.add('over');
});
document.addEventListener('dragleave', (e) => { e.target.closest('[data-a="drop"]')?.closest('.tierrow')?.classList.remove('over'); });
document.addEventListener('drop', (e) => {
  const z = e.target.closest('[data-a="drop"]'); if (!z) return;
  e.preventDefault();
  const key = ui.dragKey, desde = ui.dragFrom; ui.dragKey = null; ui.dragFrom = ''; if (!key) return;
  const hacia = z.dataset.row || '';
  const resto = filasDe(ui.tierList, key).filter(r => r !== desde);
  setFilas(ui.tierList, key, hacia ? resto.concat(hacia) : resto);
});
// Íconos de C.T.P. y de artefacto (images/items/): thanosvibs no publica algunos (hoy
// devuelve 404 para los artefactos de Annihilus, Galactus y Red Skull) y el resto puede
// no haberse bajado todavía. Si uno no carga se quita: el nombre siempre va al lado.
// Los retratos no entran acá: que falte uno se tiene que ver.
// Toda imagen que falla puede ser el servidor de escritorio cerrado: se verifica.
document.addEventListener('error', (e) => {
  const el = e.target;
  if (!el || el.tagName !== 'IMG') return;
  if (/\/images\/items\//.test(el.src)) el.remove();
  verificarServidor();
}, true);
document.addEventListener('keydown', (e) => {
  // Con la ventana del «Por qué» abierta, las teclas son de ella (teclaPq).
  if (ui.pq) { teclaPq(e); return; }
  // Con el «Cómo funciona» abierto: Esc lo cierra (el foco vuelve a la skill) y Tab no sale de él.
  if (ui.tip && e.key === 'Escape') { e.preventDefault(); cerrarTip(true); return; }
  if (ui.tip && e.key === 'Tab') { atraparFoco(e); return; }
  if (e.key === 'Escape' && ui.tlPick) { ui.tlPick = null; render(); }
  if (e.key === 'Escape' && ui.aliados != null) { ui.aliados = null; render(); }
  // En la ficha, ← y → pasan al anterior y al siguiente del listado (no mientras se escribe ni con algo abierto).
  if ((e.key === 'ArrowLeft' || e.key === 'ArrowRight') && ui.view === 'detail' && ui.aliados == null && ui.tip == null
      && !e.target.closest('input, select, textarea') && !e.altKey && !e.ctrlKey && !e.metaKey) {
    const ch = CHAR_BY_ID[ui.charId], v = ch && variant(ch.id, ui.uniformId);
    const x = v && vecinosEnListado(v)[e.key === 'ArrowLeft' ? 'prev' : 'next'];
    if (x) { e.preventDefault(); abrirFicha(x.cid, x.uid); }
  }
});
// Al cambiar el tamaño de la ventana, el «Cómo funciona» se vuelve a ubicar (o pasa a hoja inferior y vuelve).
window.addEventListener('resize', () => { if (ui.tip) posicionarTip(); });

function download (name, text, type) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([text], { type }));
  a.download = name; a.click(); URL.revokeObjectURL(a.href);
}
function exportCsv () {
  const head = ['clave','personaje','uniforme','clase','bando','tier','trascendido','instinto','raza','genero','origen',
                'roles','habilidades','striker','world_boss','costo',
                'slot','skill','cooldown','carga_ult','carga_striker','etapa','efecto','descripcion',
                'pct_ataque','dano_extra','elemento','duracion'];
  const rows = [head];
  allVariants().forEach(v => {
    const base = [v.key, v.name, v.uid ? v.sub : '', v.c, v.f, v.t, v.trans ? 'sí' : 'no', v.ins, v.race, v.gender,
                  v.ch.origin, v.r.join('|'), (v.ab || []).join('|'), v.striker, v.wba, v.cost];
    if (!v.skills.length) rows.push(base.concat(['', '', '', '', '', '', '', '', '']));
    v.skills.forEach(sk => (sk.st || []).forEach((st, i) => (st.fx || []).forEach(f => {
      const d = dano(f);
      rows.push(base.concat([sk.sl, txt('name', sk.n), sk.cd, sk.ult != null ? sk.ult : '',
        sk.stk != null ? sk.stk : '', i + 1, txt('ab', f.a),
        txt('desc', f.p, f.v).replace(/<br\s*\/?>/gi, ' '),
        d ? d.pct : '', d && d.flat != null ? d.flat : '',
        st.el != null ? txt('elem', st.el) : '', f.d != null ? f.d : ''])); })));
  });
  download('mff-roster.csv', '﻿' + rows.map(r => r.map(c => '"' + String(c == null ? '' : c).replace(/"/g, '""') + '"').join(',')).join('\n'), 'text/csv');
}

/** Pantalla de error que corta el arranque: dice qué pasó y qué hacer, en vez de una app
 *  a medias. */
function pantallaFatal (titulo, detalle) {
  $('#app').innerHTML = `<main><div class="fatal"><h1>${h(titulo)}</h1><p>${h(detalle)}</p></div></main>`;
}
/** Lo que se deriva de data.js. Lo llama arrancar() cuando ya confirmó que los datos son del
 *  formato de esta versión. */
function iniciarDatos () {
  PIDE = {};
  for (const [stat, x] of Object.entries(CATALOGO.soporte)) { const q = reglaStat(stat, x.sirve); if (q) PIDE[stat] = q; }
  for (const [p, so] of Object.entries(SOPORTES)) for (const [k] of TIPOS_SOPORTE) {
    if (so[k] && 'src' in so[k] && so[k].src !== 'api') throw new Error(`fuente de liderazgo o soporte desconocida en ${p} (${k}): ${so[k].src}`);
    if (so[k] && so[k].otorga && !(LIDERAZGOS.includes(k) && esDeApi(so[k]))) throw new Error(`«Give Power» resuelto fuera de un liderazgo de la API en ${p} (${k})`);
  }
  ANTI_MERMAS = new Set(VALOR.anti_mermas);
  for (const st of VALOR.anti_mermas) {
    if (CAT_DE[st]) throw new Error('stat de anti-mermas que ya está en otra categoría: ' + st);
    CAT.mermas.s.push(st); CAT_DE[st] = 'mermas';
  }
  STAT_ANTI = new Map();
  for (const st of VALOR.anti_mermas) for (const id of CATALOGO.soporte[st].efectos) {
    const ie = CATALOGO.efectos.findIndex(e => e.id === id);
    if (!STAT_ANTI.has(ie)) STAT_ANTI.set(ie, st);
  }
  // Lo que no se acumula (Efectos iguales): de las líneas de un stat que le llegan a alguien se aplica la de mayor valor,
  // así que tienen que poder compararse (todas con número, o ninguna); los anti-mermas no traen valor (primeraAnti mira
  // solo el orden); y ningún soporte trae más valor que un liderazgo del mismo stat (el vínculo por el liderazgo se
  // cuenta de a pares, sin el tercero: llegaLiderazgo).
  const noAcum = new Map();
  for (const [p, so] of Object.entries(SOPORTES)) for (const [k] of TIPOS_SOPORTE) {
    const x = so[k];
    if (x) for (const f of x.fx) if (!seAcumula(f)) {
      const c = noAcum.get(f.s) || { tipos: new Map(), lid: Infinity, sop: -Infinity };
      noAcum.set(f.s, c);
      c.tipos.set(typeof f.v === 'number' ? 'número' : f.v == null ? 'sin valor' : 'texto «' + f.v + '»', p + ' (' + k + ')');
      if (typeof f.v === 'number') { if (LIDERAZGOS.includes(k)) c.lid = Math.min(c.lid, f.v); else c.sop = Math.max(c.sop, f.v); }
    }
  }
  for (const [st, c] of noAcum) {
    if (c.tipos.size > 1) throw new Error(`${st} no se acumula y sus líneas no se pueden comparar para elegir la de mayor valor: ${
      [...c.tipos].map(([tipo, donde]) => tipo + ' en ' + donde).join(', ')}`);
    if (ANTI_MERMAS.has(st) && !c.tipos.has('sin valor')) throw new Error(`anti-mermas con valor (${st}): primeraAnti elige solo por el orden`);
    if (c.sop > c.lid) throw new Error(`un soporte trae ${st} con más valor que un liderazgo: el vínculo por el liderazgo (llegaLiderazgo) tendría que contarse con el tercero`);
  }
  CONTEXTO = {};
  for (const ctx of ['pvp', 'pve']) {
    const c = VALOR.contextos[ctx];
    if (!c) throw new Error('la tabla de valor (MFF_VALOR) no tiene la fila ' + ctx);
    CONTEXTO[ctx] = { ...c, vale: new Map(c.liderazgo.map((x, k) => [x.stat, k])), peso: c.liderazgo.map(x => x.peso),
                      llega: new Uint8Array(c.liderazgo.length) };
  }
  // Los stats con los que la app arma algo tienen que decir a quién le sirven (el build ya lo valida para la tabla).
  for (const st of CATEGORIAS.flatMap(c => c.s)) {
    if (!CATALOGO.soporte[st]) throw new Error('stat de una categoría sin regla de «le sirve» en el catálogo: ' + st);
  }
  BONOS_DE = {};
  for (const b of BONOS) {
    const bono = { n: b.n, m: b.m, f: b.f, vs: b.v.map(v => ({ fx: v.map(([s, x]) => ({ s, v: x })) })) };
    for (const c of b.m) (BONOS_DE[c] = BONOS_DE[c] || []).push(bono);
  }
  STRIKERS_DE = {};
  for (const [cid, filas] of Object.entries(STRIKERS)) for (const [x, p, cuando] of filas) (STRIKERS_DE[x] = STRIKERS_DE[x] || []).push([cid, p, cuando]);
  GL_DE = Object.fromEntries(CATALOGO.efectos.map(e => [e.id, { e, terminos: [], etiquetas: [], stats: [] }]));
  for (const x of GLOSARIO.terminos) for (const id of x.efectos) GL_DE[id].terminos.push(x);
  for (const [st, x] of Object.entries(CATALOGO.soporte)) for (const id of x.efectos) GL_DE[id].stats.push(st);
  TB.ab.forEach((r, i) => {
    const m = CATALOGO.skills[r.en];
    if (!m) return;
    for (const id of new Set((m.por_patron ? Object.values(m.por_patron) : [m]).flatMap(y => y.efectos))) GL_DE[id].etiquetas.push(i);
  });
  LISTAS_PVP = Object.keys(ROLES_LISTAS.pvp);
  LISTAS_PVE = Object.keys(ROLES_LISTAS.pve);
  STRIKER_SET = Object.fromEntries(Object.entries(STRIKERS).map(([c, filas]) => [c, new Set(filas.map(f => f[0]))]));
  VENTAJA = SEED.VENTAJA_TIPO;
  LE_GANA_A = {};
  for (const [c, sobre] of Object.entries(VENTAJA)) for (const [d, f] of Object.entries(sobre)) if (f === 'normal') LE_GANA_A[d] = c;
}
async function arrancar () {
  // Sin su servidor (index.html suelto, o servido por otro programa) no hay dónde
  // guardar la capa: se dice eso en vez de arrancar a medias.
  try { ESCRITORIO = await apiLocal('/api/estado'); } catch (e) { ESCRITORIO = null; }
  if (!ESCRITORIO || ESCRITORIO.app !== 'mff-escritorio') return pantallaFatal(t('ar_file_t'), t('ar_file'));
  try { U = await cargarCapa(); }
  catch (e) { return pantallaFatal(t('ar_capa_t'), e.message + ' ' + t('ar_capa')); }
  LANG = U.prefs.lang;
  latir();
  setInterval(latir, ESCRITORIO.latido_cada * 1000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) latir(); });
  if (!window.MFF_VERSION || window.MFF_VERSION.formato !== ESCRITORIO.formato_datos) return pantallaDatos();
  iniciarDatos();
  rebuild();
  try {
    const v = sessionStorage.getItem('mff_volver');
    if (VISTAS_PRINCIPALES.includes(v)) ui.view = v;
    sessionStorage.removeItem('mff_volver');
  } catch (e) {}
  render();
  buscarNovedades();
  if (ESCRITORIO.imagenes.faltan) arrancarTarea('imagenes', '/api/imagenes/bajar');
}
arrancar();
})();
