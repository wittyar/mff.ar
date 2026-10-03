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
    teams: [],
    favoritos: [],                    // equipos de 3 marcados con ★ en las combinaciones: {id, members}
    descartados: [],                  // equipos de 3 ocultos de las combinaciones: sus tres personajes (ids, en orden), con cualquier uniforme
    lists: [],                        // tier lists propias: {id,name,rows}
    assign: {},                       // listId -> {clave: [filaId, ...] | null}
    images: {},                       // 'portrait-x' / 'fullbody-x' / 'brand-logo' subidos
    marcas: {},                       // '<retrato>::<tipo de skill>' -> {it:1, gb:1, ...}
    modes: [],                        // modos propios: {id, name, teamSize}; los del juego salen de MFF_MODOS
    ruta: {},                         // personaje -> id del último paso de la hoja de ruta que ya hizo
    topes: {},                        // personaje -> {stat: {v: pantalla, b: buffs}} de la calculadora de topes
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
  CHARS = CHARS_SEED.map(c => U.charEdits[c.id] || c).concat(U.charNew);
  CHAR_BY_ID = {}; CHARS.forEach(c => { CHAR_BY_ID[c.id] = c; });
  LISTS = TIERLISTS_SEED.concat(U.lists);
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
  md_day_note:       { es:'Ciclo de 28 días. La fuente no dice qué día es hoy: elegilo mirando el juego.',
                       en:'28-day cycle. The source does not say which day is today: pick it from the game.' },
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
  us_title:          { es:'Para qué se usa',     en:'What it is used for' },
  us_note:           { es:'Lo que dicen las fuentes de este personaje y de sus uniformes. Lo derivado se dice derivado.',
                       en:'What the sources say about this character and its uniforms. Anything derived is labelled as such.' },
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
  sp_act:            { es:'Se activa',           en:'Activates' },
  sp_cd:             { es:'recarga',             en:'cooldown' },
  sp_dur:            { es:'duración',            en:'duration' },
  sp_req:            { es:'Requiere',            en:'Requires' },
  sp_notable:        { es:'Notable',             en:'Notable' },
  sp_notable_t:      { es:'thanosvibs lo marca como notable', en:'thanosvibs marks it as notable' },
  sp_at6:            { es:'a 6★',                en:'at 6★' },
  sp_np:             { es:'Buena elección para empezar (thanosvibs)', en:'New player pick (thanosvibs)' },
  us_guide:          { es:'En la guía de principiantes', en:"In the Beginner's Guide" },
  us_guide_none:     { es:'La guía no lo nombra en sus secciones de personajes.', en:'The guide does not name it in its character sections.' },
  us_obelisk:        { es:'Obelisco',            en:'Obelisk' },
  us_cancels:        { es:'Controles que aplica (cortan a los jefes):', en:'Controls it applies (they cancel the bosses):' },
  us_cancels_none:   { es:'No aplica ninguno de los controles que cortan a los jefes de Extreme ni de Legend.',
                       en:'It applies none of the controls that cancel Extreme or Legend bosses.' },
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
  ar_iso_pve:        { es:'PvE: uno de los tres sets de ataque.', en:'PvE: one of the three Attack sets.' },
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
  ga_eq_title:       { es:'C.T.P. según la guía de armado de Cynicalex: {a} · {b}', en:"C.T.P. per Cynicalex's building guide: {a} · {b}" },
  ga_eq_nodata:      { es:'sin dato en la guía', en:'no data in the guide' },
  ga_eq_other:       { es:'Con un uniforme al lado del nombre, la guía es para ese (el mejor del personaje), no para el que lleva en este equipo.',
                       en:"A uniform next to the name means the guide is for that one (the character's best), not the one used in this team." },
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
  gl_title:          { es:'Glosario',            en:'Glossary' },
  gl_note:           { es:'Qué hace cada efecto. Arriba, el glosario de skills del juego: el coreano es el original y, donde el inglés no dice lo mismo, se aclara. Abajo, todos los efectos que la app reconoce en las skills y en Leads & Supports, con cómo se leen en PvE y en PvP.',
                       en:'What each effect does. First, the in-game skill glossary: the Korean is the original and, where the English says something else, it is pointed out. Then, every effect the app recognizes in skills and in Leads & Supports, with how it reads in PvE and PvP.' },
  gl_busca:          { es:'Buscar en español, inglés o coreano', en:'Search in Spanish, English or Korean' },
  gl_cuenta:         { es:'{t} términos del juego · {e} efectos', en:'{t} game terms · {e} effects' },
  gl_nada:           { es:'Nada coincide con la búsqueda.', en:'Nothing matches the search.' },
  gl_errores:        { es:'Lo que el inglés traduce mal', en:'What the English gets wrong' },
  gl_errores_nota:   { es:'Tres errores del glosario en inglés que se repiten en varios términos, y las otras diferencias con el coreano.',
                       en:'Three mistakes of the English glossary that repeat across several terms, and the other differences with the Korean.' },
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
  gl_reforjado:      { es:'reforjado',          en:'reforged' },
  gl_sin_reforjar:   { es:'sin reforjar',       en:'not reforged' },
  gl_en_catalogo:    { es:'En el catálogo:',    en:'In the catalog:' },
  gl_termino:        { es:'Término del glosario del juego', en:'In-game glossary term' },
  gl_en_skills:      { es:'En las skills:',     en:'In skills:' },
  gl_le_sirve:       { es:'Le sirve:',          en:'Helps:' },
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
  ft_analisis:       { es:'Análisis',            en:'Analysis' },
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
  el_Physical:       { es:'físico',              en:'physical' },
  el_Energy:         { es:'de energía',          en:'energy' },
  el_Fire:           { es:'fuego',               en:'fire' },
  el_Cold:           { es:'frío',                en:'cold' },
  el_Lightning:      { es:'rayo',                en:'lightning' },
  el_Poison:         { es:'veneno',              en:'poison' },
  el_Mind:           { es:'mente',               en:'mind' },
  ft_armado:         { es:'Armado',              en:'Build' },
  ft_progreso:       { es:'Progreso',            en:'Progress' },
  ft_mas:            { es:'Más',                 en:'More' },
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
  eq_build:          { es:'Armar para mi cuenta', en:'Build for my account' },
  eq_build_with:     { es:'Armar un equipo con él', en:'Build a team with it' },
  eq_why:            { es:'Por qué',             en:'Why' },
  pq_recibe:         { es:'Lo que recibe {x}',   en:'What {x} gets' },
  pq_nada:           { es:'Ningún soporte ni liderazgo le llega y le sirve.', en:'No support or leadership reaches it and is useful to it.' },
  pq_sin_art:        { es:'sin artefactos: {x}', en:'without artifacts: {x}' },
  pq_desglose:       { es:'Desglose',            en:'Breakdown' },
  pq_lider:          { es:'líder',               en:'leader' },
  pq_art_de:         { es:'Artefacto de {x}',    en:'{x}\'s artifact' },
  pq_ver:            { es:'En la ficha de {x}', en:'On {x}\'s sheet' },
  pq_si_art:         { es:'si lleva su artefacto', en:'if it has its artifact' },
  pq_sin_skill:      { es:'La ficha de este personaje no tiene esta skill.', en:'This character\'s sheet does not have this skill.' },
  pq_ademas:         { es:'Además',              en:'Also' },
  pq_pierde:         { es:'Se pierde',           en:'Lost' },
  pq_todos:          { es:'a todos',             en:'everyone' },
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
  eq_new_note:       { es:'Todas las parejas de compañeros que tienen vínculo con él (le dan un soporte o el liderazgo, reciben uno suyo o forman con él un bono de equipo), una por trío de personajes, con el mejor uniforme de cada uno para el orden elegido. Un efecto cuenta solo si le sirve a quien lo recibe: los que suben un ataque o un daño elemental, solo a quien pega con eso según sus skills; las resistencias, solo a quien pega según su resistencia, y todas las velocidades, a nadie. Los puntos para él son la sinergia de la app contando solo lo que lo involucra: lo que le dan, lo que da él, los bonos de equipo en los que está o que le sirven, la ventaja de clase con él, y los roles y las clases del equipo. El líder es el que más le suma.',
                       en:'Every pair of teammates with a link with it (they give it a support or the leadership, receive one of its own, or form a team bonus with it), one per trio of characters, with each one\'s best uniform for the chosen order. An effect only counts if it is useful to whoever receives it: attack or elemental damage boosts, only for those whose skills hit with that; resists, only for those whose damage grows with their resist, and all speeds, for nobody. Points for it are the app\'s synergy counting only what involves it: what it gets, what it gives, the team bonuses it is part of or that are useful to it, class advantage with it, and the team\'s roles and classes. The leader is the one that adds the most for it.' },
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
  eq_count:          { es:'{n} combinaciones',   en:'{n} combinations' },
  eq_count_1:        { es:'1 combinación',       en:'1 combination' },
  eq_none_q:         { es:'Ninguna combinación con estos filtros.', en:'No combination with these filters.' },
  eq_leader:         { es:'Líder: {x}',          en:'Leader: {x}' },
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
  cx_nota_pvp:       { es:'Equipos para PvP, con las reglas de Ezequiel. Entran si alguno es DPS en {l} y si los tres tienen anti-mermas (Remove All Debuffs o Debuff Immunity), del liderazgo del líder o del soporte de alguno. Cada compañero tiene vínculo con él o es DPS. Puntaje: 2 por cada liderazgo que vale (todos los ataques, todas las defensas, PG, ignorar evasión) y cada uno al que le llega y le sirve, 1 si el liderazgo se activa con una condición (al recibir un debuff, por ejemplo); 2 por cada nivel de fila de cada DPS (3, 2 o 1); 1 por cada soporte que le llega a otro y le sirve, por cada bono de equipo activo y por cada striker del trío. El líder es el que más suma y es el mismo en las listas de los tres: a igual puntaje, el mejor ubicado en la tier list y después un orden fijo.',
                       en:'Teams for PvP, with Ezequiel\'s rules. They make it if someone is a DPS in {l} and all three have debuff removal (Remove All Debuffs or Debuff Immunity), from the leader\'s leadership or someone\'s support. Each teammate has a link with it or is a DPS. Score: 2 for each leadership that counts (all attacks, all defenses, HP, ignore dodge) and each one it reaches and helps, 1 if the leadership activates on a condition (when debuffed, for example); 2 for each row level of each DPS (3, 2 or 1); 1 for each support that reaches and helps another, each active team bonus and each striker in the trio. The leader is the one that adds the most and is the same in the lists of all three: on a tie, the best placed on the tier list, then a fixed order.' },
  cx_nota_pve:       { es:'Equipos para PvE, con las reglas de Ezequiel. Entran si alguno es DPS en {l}; los anti-mermas no hacen falta. Cada compañero tiene vínculo con él o es DPS. Puntaje: 2 por cada liderazgo de daño (ataque, daño elemental, daño a jefes) y cada uno al que le llega y pega con eso, 1 si el liderazgo se activa con una condición (al recibir un debuff, por ejemplo); 2 por cada nivel de fila de cada DPS (3, 2 o 1, el mejor de las dos listas); 1 por cada soporte que le llega a otro y le sirve, por cada bono de equipo activo y por cada striker del trío. El líder es el que más suma y es el mismo en las listas de los tres: a igual puntaje, el mejor ubicado en las tier lists y después un orden fijo.',
                       en:'Teams for PvE, with Ezequiel\'s rules. They make it if someone is a DPS in {l}; debuff removal is not required. Each teammate has a link with it or is a DPS. Score: 2 for each damage leadership (attack, elemental damage, boss damage) and each one it reaches that hits with it, 1 if the leadership activates on a condition (when debuffed, for example); 2 for each row level of each DPS (3, 2 or 1, the best of both lists); 1 for each support that reaches and helps another, each active team bonus and each striker in the trio. The leader is the one that adds the most and is the same in the lists of all three: on a tie, the best placed on the tier lists, then a fixed order.' },
  cx_sin_funcion_pvp: { es:'{x} no figura en la tier list de PvP ({l}): no tiene función en PvP y este orden no arma combinaciones.',
                       en:'{x} is not on the PvP tier list ({l}): it has no role in PvP, so this order builds no combinations.' },
  cx_sin_funcion_pve: { es:'{x} no figura en las tier lists de PvE ({l}), o solo como «Not for wbl»: no tiene función en PvE y este orden no arma combinaciones.',
                       en:'{x} is not on the PvE tier lists ({l}), or only as «Not for wbl»: it has no role in PvE, so this order builds no combinations.' },
  cx_anti:           { es:'Anti-mermas',         en:'Debuff removal' },
  cx_de_lid:         { es:'{x} (liderazgo)',     en:'{x} (leadership)' },
  cx_de_sop:         { es:'{x} (soporte)',       en:'{x} (support)' },
  cx_lider:          { es:'Liderazgo de {x}',    en:'{x}\'s leadership' },
  cx_lider_nada:     { es:'Ningún liderazgo de los que valen en este contexto', en:'No leadership that counts in this context' },
  cx_lider_mitad:    { es:'{c}: la mitad',       en:'{c}: half' },
  cx_dps:            { es:'DPS',                 en:'DPS' },
  cx_sinergia:       { es:'Soportes y bonos de equipo', en:'Supports and team bonuses' },
  cx_strikers:       { es:'Strikers',            en:'Strikers' },
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
  cmp_synergy:       { es:'Sinergia estimada',   en:'Estimated synergy' },
  cmp_pts:           { es:'pts',                 en:'pts' },
  cmp_no_synergy:    { es:'Sin señales fuertes de sinergia en esta selección.',
                       en:'No strong synergy signals in this selection.' },
  cmp_heuristic:     { es:'Pesan los efectos de líder y de soporte de thanosvibs que alcanzan a otro integrante y le sirven: los que suben un ataque o un daño elemental, solo a quien pega con eso según sus skills; las resistencias, solo a quien pega según su resistencia; todas las velocidades, a nadie (el liderazgo, con el mejor líder posible). Cada bono de equipo con todos sus integrantes en el equipo suma 1 (de la wiki, o del juego si se cargó). Se suman dos lecturas propias: roles derivados de las skills y ventaja de clase (la guía de thanosvibs y la wiki). No es un cálculo del juego.',
                       en:'What weighs most are the thanosvibs lead and support effects that reach another member and are useful to it: attack or elemental damage boosts only for those whose skills hit with that; resists only for those whose damage grows with their resist; all speeds for nobody (leadership, with the best possible leader). Each team bonus with all its members in the team adds 1 (from the wiki, or from the game when entered). Two readings of our own are added: roles derived from skills and class advantage (per the thanosvibs guide and the wiki). Not a game calculation.' },
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
  sk_note:           { es:'Pueden aparecer a pegar junto a él, con esa probabilidad, cuando él ataca o cuando lo atacan. Según Ezequiel, el striker tiene que estar en el mismo equipo. Son del personaje: valen con cualquier uniforme.',
                       en:'They may show up to strike alongside it, with that chance, when it attacks or when it is attacked. Per Ezequiel, the striker has to be on the same team. They belong to the character: any uniform works.' },
  sk_suyos:          { es:'Sus {n} strikers',    en:'Its {n} strikers' },
  sk_de:             { es:'Es striker de {n}',   en:'Striker of {n}' },
  sk_de_nota:        { es:'Aparece junto a ellos cuando ellos atacan o los atacan.', en:'It shows up alongside them when they attack or are attacked.' },
  sk_sin_pestana:    { es:'La wiki no tiene sus strikers.', en:'The wiki does not list its strikers.' },
  sk_de_nadie:       { es:'No es striker de nadie en la wiki.', en:'It is nobody\'s striker on the wiki.' },
  sk_ataca:          { es:'{p}% al atacar',     en:'{p}% on attack' },
  sk_atacado:        { es:'{p}% al ser atacado', en:'{p}% when attacked' },
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
  tm_note:           { es:'Los que armás vos, con la sinergia estimada por la app.',
                       en:'The ones you build, with the synergy the app estimates.' },
  tm_build:          { es:'+ Armar equipo',      en:'+ Build team' },
  tm_name_ph:        { es:'Nombre del equipo',   en:'Team name' },
  tm_nomode:         { es:'Sin modo (3)',        en:'No mode (3)' },
  tm_members:        { es:'Miembros',            en:'Members' },
  tm_sorted_by:      { es:'ordenados por',       en:'sorted by' },
  tm_search:         { es:'Buscar…',             en:'Search…' },
  tm_reason_ph:      { es:'Por qué funciona (opcional)', en:'Why it works (optional)' },
  tm_cancel:         { es:'Cancelar',            en:'Cancel' },
  tm_save:           { es:'Guardar',             en:'Save' },
  tm_synergy_pts:    { es:'pts de sinergia',     en:'synergy pts' },
  tm_empty:          { es:'Todavía no armaste ningún equipo.', en:'You have not built any team yet.' },
  tm_mine:           { es:'Equipos de tu cuenta', en:'Your account\'s teams' },
  tm_dup:            { es:'{x} ya está en «{e}», del mismo modo.', en:'{x} is already in «{e}», same mode.' },
  tm_in_use:         { es:'ya está en «{e}» (mismo modo)', en:'already in «{e}» (same mode)' },
  tm_favs:           { es:'Favoritos',           en:'Favorites' },
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
  st_pct:            { es:'% de ataque',         en:'% of attack' },
  st_flat:           { es:'Daño extra',          en:'Extra damage' },
  st_element:        { es:'Elemento',            en:'Element' },
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
  ct_mermas:         { es:'Quita todos los debuffs', en:'Removes All Debuffs' },
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
  cb_note:           { es:'Debajo de cada una, lo que recibe él: los soportes de sus compañeros y el liderazgo del líder elegido (también si el líder es él), solo lo que le llega y le sirve. ✓ lo recibe, ✗ no; * solo si el compañero lleva su artefacto. No cambia los puntos.',
                       en:'Under each one, what it gets: its teammates\' supports and the chosen leader\'s leadership (also when it is the leader), only what reaches it and is useful to it. ✓ it gets it, ✗ it does not; * only if the teammate has its artifact. It does not change the points.' },
  cb_ataque:         { es:'Ataque',               en:'Attack' },
  cb_art:            { es:'* Solo si el compañero que lo da lleva su artefacto.', en:'* Only if the teammate who gives it has its artifact.' },
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
/** Valor del dominio (clase, rol, slot, etiqueta) en el idioma activo. */
function dom (v) {
  if (LANG === 'es' || v == null) return v;
  const en = VOCAB_EN[v];
  if (en === undefined) { console.warn('valor de dominio sin inglés en MFF_VOCAB_EN:', v); return v; }
  return en;
}
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
const VISTAS_PRINCIPALES = ['roster', 'tierlist', 'modos', 'teams', 'glosario', 'settings'];
function recargar () {
  try { sessionStorage.setItem('mff_volver', VISTAS_PRINCIPALES.includes(ui.view) ? ui.view : 'roster'); } catch (e) {}
  location.reload();
}
function mb (bytes) { return (bytes / 1048576).toFixed(1).replace('.', LANG === 'es' ? ',' : '.') + ' MB'; }
/** Primer arranque de una versión que usa otro formato de datos (o sin data.js): baja
 *  los publicados antes de mostrar nada, porque la app no puede leer los que hay. */
async function pantallaDatos () {
  const pintar = (extra) => pantallaFatal(t('pd_title'), t('pd_note') + (extra ? ' ' + extra : ''));
  pintar();
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
  pickMode: false, picks: [],
  charId: null, uniformId: 'base',
  tierList: (TIERLISTS_SEED[0] || {}).id || '',
  teamOpen: false, team: { name:'', members:[], reason:'', modeId:'' }, teamSearch:'', teamPage:0,
  newListName: '', newListTpl: 'rango', newListKind: 'personajes', editRows: false, poolOpen: false, poolSearch: '', marcando: false,
  edStep: 0, edDraft: null, edId: null,
  dragKey: null, dragFrom: '', tlPick: null,
  aliados: null,                     // objetivo de grupo cuya lista de personajes está abierta
  fichaTab: 'resumen',               // pestaña de la ficha; se conserva al pasar de un personaje a otro
  modoFiltro: 'todos', modoAbierto: null, abxDia: 1,
  glBusca: '',                       // búsqueda del glosario
  artEst: '6',                       // nivel de estrellas que muestra el artefacto de la ficha
  // combinaciones de 3 de la pestaña Equipos: orden, filtros (se excluye por personaje) y página
  eqOrden: 'foco', eqExcluir: [], eqCon: '', eqPagina: 0, eqCalculando: null,
  eqCobertura: [],                   // grupos de COBERTURA marcados: solo los tríos en que los recibe
  eqVerDescartados: false,           // la lista muestra solo los descartados, para restaurarlos
  volverY: null,                     // posición a la que se vuelve con «Atrás» (ver HISTORIAL)
  volverAbiertos: [],                // plegados que se vuelven a abrir con «Atrás» (ver HISTORIAL)
  entradaNueva: false                // el próximo render abre otra entrada del historial aunque no cambie el lugar
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
// Para quién sirve cada efecto de líder, de soporte y de bono de equipo. Los que suben un
// ataque o un daño elemental solo le sirven a quien pega con eso, según el daño de sus skills
// activas (la 6 incluida): un liderazgo de daño de fuego no le aporta nada a uno que pega
// físico sin elemento. Todos los personajes hacen daño con sus activas, así que el resto (daño
// básico, crítico, ignorar evasión, vida, defensas, inmunidades...) le sirve a cualquiera;
// también los que dependen de qué debuffs aplica o de si tiene golpes en cadena, que las skills
// no marcan de una forma que se pueda leer sin suponer. Según Ezequiel, todas las velocidades no le
// sirven a nadie y las resistencias solo a quien tiene una mejora de daño según su resistencia
// (res del perfil: su artefacto o su Striker), en ese elemento. Un efecto que no está en ninguna
// de las dos listas (thanosvibs sumó uno nuevo, o la wiki escribe un stat de bono que la app no
// conoce) cuenta para todos y la sinergia lo dice.
// Cada regla: [qué mira del perfil (perfilDano), qué valor pide]; con null, cualquiera. 'nadie': a
// ninguno.
const PIDE = {
  'Physical Attack': ['src', 'Physical Attack'], 'Energy Attack': ['src', 'Energy Attack'],
  'Fire Damage': ['elem', 'Fire'], 'Fire Damage by % Fire Resist': ['elem', 'Fire'], 'Cold Damage': ['elem', 'Cold'],
  'Lightning Damage': ['elem', 'Lightning'], 'Poison Damage': ['elem', 'Poison'], 'Mind Damage': ['elem', 'Mind'],
  'All Element Damage': ['elem', null], 'Physical Reflect Damage Received': ['tipo', 'Physical'],
  'All Resistances': ['res', null], 'Fire Resist': ['res', 'Fire'], 'Cold Resist': ['res', 'Cold'],
  'Lightning Resist': ['res', 'Lightning'], 'Mind Resist': ['res', 'Mind'],
  'All Speeds': ['nadie', null],
};
const PARA_TODOS = new Set(['1s Pierce Duration Increase', '1s Snare Duration Increase', 'Additional Pierce Damage',
  'All Basic Attacks', 'All Basic Attacks (Stackable)', 'All Basic Defenses', 'All Debuffs Effect', 'All Reflect Damage Received',
  'Barrier', 'Basic Damage Dealt to Boss Types', 'Basic Damage Dealt to Enemies except Mutant Characters',
  'Basic Damage Dealt to Enemies with "Debuff Removal (Instinct)" Effect', 'Basic Damage Dealt to Enemies with "Removes All Debuffs" Effect',
  'Basic Damage Dealt to Enemies with 25% HP or Higher', 'Basic Damage Dealt to Females', 'Basic Damage Dealt to Heroes',
  'Basic Damage Dealt to Males', 'Basic Damage Dealt to Universals', 'Basic Damage Dealt to Villains', 'Basic Damage Received',
  'Basic Damage Received from Heroes', 'Basic Damage Received from Universals', 'Basic Damage Received from Villains', 'Bonus Damage',
  'Burn Immunity', 'Chain Hit Damage', 'Chain Hit Damage Received', 'Critical Damage', 'Critical Rate', 'Debuff Duration',
  'Debuff Immunity', 'Dodge', 'Energy Defense', 'Fear Immunity', 'Fire Immunity Chance', 'Guaranteed Critical Rate',
  'Guard Break Immunity', 'HP', 'Heal', 'Ignore Defense', 'Ignore Dodge', 'Ignore Non-Boss Damage Decrease',
  'Ignores Damage Increase/Decrease Effect Between Self and Opposing Faction', 'Immortality + Death', 'Immortality + Heal',
  'Incapacitation Immunity', 'Lightning Immunity Chance', 'Max HP Shield', 'Mind Immunity Chance',
  'Physical Immunity Chance', 'Recovery Rate', 'Remove All Debuffs', 'Revive with % HP', 'Skill Cooldown', 'Skill Damage',
  'Stun Immunity', 'Summon', 'Super Armor, All Basic Defenses',
  // los que solo traen los bonos de equipo (scripts/bonos.py)
  'Attack Speed', 'Crowd Control Time', 'Movement Speed', 'Physical Defense']);
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
/** ¿Le sirve a b este efecto (una línea de un soporte o liderazgo)? */
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
// en cada una. Las de ataque le sirven solo a quien pega con eso (sirve()); las otras cuatro,
// a cualquiera. Se ven en la ficha, filtran el roster y dicen en cada combinación de 3 qué le
// dan al personaje sus compañeros. No cambian los puntos de la sinergia.
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
  { k: 'mermas',   s: ['Remove All Debuffs'] },
];
const CAT = Object.fromEntries(CATEGORIAS.map(c => [c.k, c]));
const CAT_DE = {};                    // stat de thanosvibs -> categoría
for (const c of CATEGORIAS) for (const s of c.s) {
  if (!PIDE[s] && !PARA_TODOS.has(s)) throw new Error('categoría con un stat que no dice a quién le sirve: ' + s);
  CAT_DE[s] = c.k;
}
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
/** Lo que le llega a `destino` de un integrante `a` del equipo y le sirve: los soportes de `a` (los
 *  de cada uno son para los demás) y, si `a` es el líder, su liderazgo (también si `a` es `destino`:
 *  el liderazgo es para todo el equipo). [{ de: a, k, x, fx: [los efectos que le sirven] }], en el
 *  orden de TIPOS_SOPORTE. De acá salen la cobertura de la tarjeta y su «Por qué» (porqueHtml). */
function recibe (destino, a, esLider) {
  const out = [], s = SOPORTES[a.p];
  if (s) for (const [k] of TIPOS_SOPORTE) {
    const x = s[k];
    if (!x || !(LIDERAZGOS.includes(k) ? esLider : a !== destino) || !aplicaA(x, destino)) continue;
    const fx = x.fx.filter(f => sirve(f, destino));
    if (fx.length) out.push({ de: a, k, x, fx });
  }
  return out;
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
/** Un efecto de soporte en texto plano: "Ignorar evasión +25%". */
function efectoSoporteTxt (f) {
  const val = [];
  if (f.v != null) val.push(typeof f.v === 'number' ? (f.v > 0 ? '+' : '') + f.v + '%' : trTxt(f.v));
  if (f.i != null) val.push('+' + f.i + '% ' + t('sp_inst'));
  if (f.c) val.push(trTxt(f.c));
  return trTxt(f.s) + (val.length ? ' ' + val.join(' ') : '');
}
const LIDERAZGOS = ['leader', 'leader2'];
const ROLES_EQUIPO = ['Tanque', 'Control', 'Daño', 'Soporte'];
/** Bonos de equipo de cada personaje (MFF_BONOS), por id. Cada versión de sus stats (más de una
 *  si las páginas de la wiki empatan) tiene la forma de un efecto de soporte ({ fx: [{ s, v }] }),
 *  para que la sinergia les aplique sirve() y efectoSoporteTxt(). Lo arma iniciarDatos(). */
let BONOS_DE;
/** De quiénes es striker cada personaje: { cid: [[cid del personaje, %, 'ataca'|'atacado'], ...] }, al
 *  revés de STRIKERS. Lo arma iniciarDatos(). */
let STRIKERS_DE;
/** Por efecto del catálogo (id): el efecto, los términos del glosario del juego que le corresponden y
 *  las etiquetas de skills que apuntan a él (índices en MFF_TABLAS.ab, solo las que traen los
 *  datos). Lo arma iniciarDatos(). */
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
 *  soporte de thanosvibs que alcanzan a otro integrante y le sirven (sirve()): los de soporte
 *  valen en cualquier lugar del equipo; el liderazgo solo en el lugar de líder, así que se
 *  cuenta el mejor líder posible. Cada bono de equipo con todos sus integrantes en el equipo
 *  suma 1 (de la wiki, o del juego si se cargó). Se suman dos lecturas propias, dichas como tales:
 *  los roles derivados de las skills y la ventaja de tipo (Combate > Velocidad > Detonación >
 *  Combate; Universal le gana a las tres con ventaja menor y no tiene debilidad). No es un
 *  cálculo del juego.
 *  foco: cuenta solo lo que involucra a ese integrante (los equipos armados para él).
 *  Escrita con bucles y sin armar textos si no hacen falta: la consulta de combinaciones la
 *  llama cientos de miles de veces. */
function synergy (vs, { soloPuntaje = false, foco = null } = {}) {
  if (vs.length < 2) return { score: 0, razones: [], aplicados: [], lider: null };
  // razones: lo que suma, para explicarlo (sin soloPuntaje): cada soporte o liderazgo con los
  // integrantes a los que les llega y les sirve, cada versión de un bono de equipo, los roles, las
  // clases y cada ventaja de clase. Los textos salen de ahí (razonesTxt, porqueHtml).
  // aplicados: { de, a: [integrantes] }, lo que suma: quién le da algo a quién (en un bono de equipo,
  // cada integrante a los otros, que están juntos por el bono)
  const razones = [], aplicados = []; let score = 0;
  // Un soporte o un liderazgo suma si le llega a otro integrante y le sirve (sirve()). Con foco
  // (un equipo armado para un integrante) solo cuenta lo que lo involucra: lo que le dan a él y
  // lo que da él. Lo que los demás se dan entre ellos no suma para él.
  const cuenta = (a, x) => !foco || a === foco || (aplicaA(x, foco) && leSirve(x, foco));
  const alcanza = (a, x) => { const bs = []; for (const b of vs) if (b !== a && aplicaA(x, b) && leSirve(x, b)) bs.push(b); return bs; };
  // Soportes: pasivas de 4★ y Tier-2, efecto de uniforme y artefacto (si lo lleva).
  for (const a of vs) {
    const s = SOPORTES[a.p]; if (!s) continue;
    for (const [k] of TIPOS_SOPORTE) {
      const x = s[k]; if (!x || LIDERAZGOS.includes(k) || !cuenta(a, x)) continue;
      const bs = alcanza(a, x); if (!bs.length) continue;
      score += x.sig ? 3 : 2; aplicados.push({ de: a, a: bs });
      if (!soloPuntaje) razones.push({ tipo: 'soporte', de: a, k, x, a: bs });
    }
  }
  // Liderazgo: el del integrante que más alcanza a los demás (con foco, el que más le sirve a
  // él); si empatan, el primero.
  let lider = null, ptsLider = 0, xsLider = null;
  for (const a of vs) {
    const s = SOPORTES[a.p]; if (!s) continue;
    let pts = 0; const xs = [];
    for (const k of LIDERAZGOS) {
      const x = s[k]; if (!x || !cuenta(a, x)) continue;
      const bs = alcanza(a, x); if (!bs.length) continue;
      pts += x.sig ? 3 : 2; xs.push({ k, x, bs });
    }
    if (pts > ptsLider) { lider = a; ptsLider = pts; xsLider = xs; }
  }
  if (lider) {
    score += ptsLider;
    for (const o of xsLider) { aplicados.push({ de: lider, a: o.bs });
      if (!soloPuntaje) razones.push({ tipo: 'liderazgo', de: lider, k: o.k, x: o.x, a: o.bs }); }
  }
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
      // cada versión de sus stats (más de una si las páginas de la wiki no coinciden), a quienes les sirve
      if (!soloPuntaje) b.vs.forEach((v, i) => razones.push({ tipo: 'bono', b, i, x: v, integrantes, a: reciben.filter(x => leSirve(v, x)) }));
    }
  }
  const covered = ROLES_EQUIPO.filter(r => vs.some(v => v.r.includes(r)));
  if (covered.length >= 2) { score += 1; if (!soloPuntaje) razones.push({ tipo: 'roles', roles: covered }); }
  if (vs.every((v, i) => vs.findIndex(w => w.c === v.c) === i)) { score += 1; if (!soloPuntaje) razones.push({ tipo: 'clases' }); }
  // a cubre la debilidad de b si a le gana a la clase que le gana a b (un Universal también,
  // con su ventaja menor: suma lo mismo y la razón lo dice).
  for (const a of vs) for (const b of vs) {
    const amenaza = LE_GANA_A[b.c], fuerza = amenaza && VENTAJA[a.c][amenaza];
    if (a !== b && fuerza && (!foco || a === foco || b === foco)) {
      score += 1;
      if (!soloPuntaje) razones.push({ tipo: 'ventaja', a, b, amenaza, fuerza });
    }
  }
  return { score, razones, aplicados, lider };
}
/** Nombre de un bono de equipo en las razones: «Bono de equipo «X» (A + B)», con la versión si la
 *  wiki no coincide. */
function nombreBono (r) {
  const nombre = `${t('sy_bonus')} ${r.b.n ? '«' + r.b.n + '»' : t('sy_bonus_noname')} (${r.integrantes.map(x => x.name).join(' + ')})`;
  return r.b.vs.length > 1 ? `${nombre} · ${t('sy_bonus_ver').replace('{i}', r.i + 1).replace('{n}', r.b.vs.length)}` : nombre;
}
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
  const lineas = (prefijo, x, bs) => {
    const grupos = new Map();
    for (const b of bs) {
      const fx = x.fx.filter(f => sirve(f, b)), k = fx.map(f => x.fx.indexOf(f)).join(',');
      if (!grupos.has(k)) grupos.set(k, { fx, bs: [] });
      grupos.get(k).bs.push(b);
    }
    for (const g of grupos.values()) out.push(`${prefijo} → ${g.bs.map(fullLabel).join(', ')}: ${g.fx.map(f =>
      efectoSoporteTxt(f) + (sinClasificar(f.s) ? ' (' + t('sy_unclassified') + ')' : '')).join(' · ')}`);
  };
  for (const r of razones) {
    if (r.tipo === 'soporte') lineas(`${fullLabel(r.de)} · ${t(CLAVE_SOPORTE[r.k])}${r.k === 'artifact' ? ' (' + t('pq_si_art') + ')' : ''}`, r.x, r.a);
    else if (r.tipo === 'liderazgo') lineas(`${ES ? 'Con' : 'With'} ${fullLabel(r.de)} ${ES ? 'de líder' : 'as leader'}`, r.x, r.a);
    else if (r.tipo === 'bono') lineas(nombreBono(r), r.x, r.a);
    else out.push(razonTxt(r, fullLabel));
  }
  return [...new Set(out)];
}
/** ¿Un stat que no está en ninguna de las dos listas (PIDE, PARA_TODOS)? Cuenta para todos y se dice. */
function sinClasificar (s) { return !(PARA_TODOS.has(s) || PIDE[s]); }
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
    const origen = r.tipo === 'bono' ? 'b|' + r.b.m.join('+') + '|' + r.i : 's|' + r.de.key + '|' + r.k;
    for (const b of r.a) r.x.fx.forEach((f, n) => { if (sirve(f, b)) out.push({ r, f, para: b, clave: origen + '|' + n + '|' + b.key }); });
  }
  return out;
}
/** ¿x tiene un vínculo con v en el equipo? Le da algo (un soporte, o el liderazgo si es el
 *  líder que cuenta la sinergia), recibe algo de él o forman juntos un bono de equipo. Las clases
 *  y los roles no cuentan: un equipo armado alrededor de v no lleva compañeros que no tengan nada
 *  que ver con él. */
function vinculo (v, x, aplicados) {
  for (const e of aplicados) if ((e.de === v && e.a.includes(x)) || (e.de === x && e.a.includes(v))) return true;
  return false;
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
function marcadores (texto, f) {
  const chip = (clave, titulo) => `<i class="tpl" title="${h(t(titulo))}">${h(t(clave))}</i>`;
  const grupo = () => {
    if (!(f && f.g)) return chip('tpl_unspec', 'tpl_pending');
    const titulo = ORIGEN_MARCADOR[f.gs];
    if (!titulo) throw new Error('origen de marcador desconocido: ' + f.gs);
    return `<span class="tpl-ok" title="${h(t(titulo))}">${h(dom(f.g))}</span>`;
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
/** {txt, sinTraducir} de una fila, en el idioma activo. */
function texto (tabla, i, nums) {
  const f = fila(tabla, i);
  if (!f) return null;
  if (LANG === 'en') return { txt: rellenar(f.en, nums), sinTraducir: false };
  if (f.es == null) return { txt: rellenar(f.en, nums), sinTraducir: true };
  return { txt: rellenar(f.es, nums), sinTraducir: false };
}
// Tres objetivos de la fuente traen un "\n" literal (dos caracteres) metiendo la
// condicion de activacion adentro del objetivo. Se muestra como separador, no crudo.
const BARRA_N = /\\n/g;
function txt (tabla, i, nums) { const r = texto(tabla, i, nums); return r ? r.txt.replace(BARRA_N, ' · ') : ''; }
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

/** Un efecto que no es daño: etiqueta tipada + texto, uno por línea. */
function efectoLinea (f) {
  const r = texto('desc', f.p, f.v);
  if (!r) return '';
  const partes = r.txt.split(/<br\s*\/?>/i).map(x => x.trim()).filter(Boolean);
  // Duración, tick y marcas van pegadas al final de la última línea, no en un renglón aparte.
  const meta = [];
  if (f.t != null) meta.push(t('every') + ' ' + f.t + ' s');
  if (f.d != null) meta.push(f.d + ' s');
  if (f.m) meta.push(t('permanent_fx'));
  if (f.b) meta.push(t('team_fx'));
  const etiqueta = txt('ab', f.a);
  return `<div class="fxline">
    <span class="fxtag" title="${h(etiqueta)}">${h(etiqueta)}</span>
    <div class="fxitems ${r.sinTraducir ? 'sintrad' : ''}"
         ${r.sinTraducir ? `title="${h(t('untranslated'))}"` : ''}>
      ${partes.map((x, i) => `<div>${marcadores(h(x), f)}${
        i === partes.length - 1 && meta.length ? ` <span class="dur">${h(meta.join(' · '))}</span>` : ''}</div>`).join('')}
    </div></div>`;
}

/** Una skill: tabla de daño por etapa arriba, y el resto de los efectos abajo. */
function skillCard (sk, portrait) {
  const etapas = sk.st || [];
  const marcas = portrait ? marcasDe(portrait, sk.sl) : {};
  const filasDano = [];
  etapas.forEach((st, i) => {
    (st.fx || []).forEach(f => {
      const dn = dano(f);
      if (dn) filasDano.push({ i, st, dn, f });
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
  const hayObj = etapas.some(st => st.tg != null);
  const hayAct = etapas.some(st => st.ac != null);

  const tabla = filasDano.length ? `<div class="stagewrap"><table class="stages">
    <thead><tr>
      ${varias ? `<th>${h(t('st_stage'))}</th>` : ''}
      <th>${h(t('st_pct'))}</th><th>${h(t('st_flat'))}</th><th>${h(t('st_element'))}</th>
    </tr></thead><tbody>
    ${filasDano.map(r => `<tr>
      ${varias ? `<td class="stnum">${r.i + 1}</td>` : ''}
      <td class="num"><b>${h(r.dn.pct)}%</b> <span class="muted">${h(srcEs(r.dn.src))}</span></td>
      <td class="num">${r.dn.flat != null ? '+' + h(r.dn.flat) : '<span class="muted">—</span>'}</td>
      <td>${r.st.el != null ? `<span class="tag dim">${h(txt('elem', r.st.el))}</span>`
                            : `<span class="muted">${h(elemEs(r.dn.elem))}</span>`}</td>
    </tr>`).join('')}
    </tbody></table></div>` : '';

  const otros = etapas.map((st, i) => {
    const fx = (st.fx || []).filter(f => !esDano(f));
    const meta = [];
    if (st.ac != null && st.ac !== acComun) meta.push(`<span class="stmeta">${h(t('st_activation'))}: ${h(txt('act', st.ac, st.av))}</span>`);
    if (st.tg != null && st.tg !== tgComun) meta.push(`<span class="stmeta">${h(t('st_target'))}: ${objetivoTexto(st.tg)}</span>`);
    if (!fx.length && !meta.length) return '';
    return `<div class="stageblock">
      ${varias || meta.length ? `<div class="stagehead">${varias ? `<span class="stnum">${i + 1}</span>` : ''}${meta.join('')}</div>` : ''}
      ${fx.map(efectoLinea).join('')}</div>`;
  }).join('');

  const cargas = [];
  if (sk.cd) cargas.push(`<span class="tag dim">CD ${h(sk.cd)}s</span>`);
  else if (sk.sl === 'Active Ult' || sk.sl === 'Striker Skill') cargas.push(`<span class="tag dim">${h(t(sk.sl === 'Active Ult' ? 'sk_bar_ult' : 'sk_bar_stk'))}</span>`);
  if (sk.ult != null) cargas.push(`<span class="tag dim">${h(t('c_ult'))} ${h(sk.ult)}%</span>`);
  if (sk.stk != null) cargas.push(`<span class="tag dim">${h(t('c_striker'))} ${h(sk.stk)}%</span>`);

  return `<div class="skill" id="${anclaSkill(sk.sl)}">
    <div class="top">
      <span class="slotbadge ${slotClase(sk.sl)}">${h(slotEs(sk.sl))}</span>
      ${nombreSkill(sk)}
      ${cabecera.join('')}
      ${cargas.join('')}
    </div>
    <div class="body">${tabla}${otros}
      ${portrait && ui.marcando ? `<div class="marcador">
        <span class="muted">${h(t('at_mark'))}</span>
        ${ATRIBUTOS.map(a => `<label class="chk"><input type="checkbox" data-a="marca"
            data-p="${h(portrait)}" data-sl="${h(sk.sl)}" data-k="${a.k}"
            ${marcas[a.k] ? 'checked' : ''}> ${h(a[LANG])}</label>`).join('')}
      </div>` : ''}
    </div>
  </div>`;
}
function srcEs (v) {
  if (LANG === 'en') return v;
  return { 'Physical Attack':'ataque físico', 'Energy Attack':'ataque de energía', 'HP':'vida' }[v] || v;
}
function elemEs (v) { return LANG === 'en' ? v : (txt('elem', (TB.elem || []).findIndex(x => x.en === v)) || v); }

/** Máximo 4 columnas en la comparación: al agregar la quinta se descarta la más vieja. */
function togglePick (cid, uid) {
  const key = cid + '::' + (uid || 'base');
  const i = ui.picks.findIndex(x => x.key === key);
  if (i > -1) { ui.picks.splice(i, 1); return; }
  ui.picks.push({ cid, uid: uid || null, key });
  if (ui.picks.length > 4) ui.picks.shift();
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
function rankLabel (key) {
  const list = listById(U.prefs.refList); if (!list) return null;
  const idx = indicesFila(list, key); if (!idx.length) return null;
  const rows = rowsOf(list);
  return { label: rows[idx[0]].label, color: rowColor(idx[0], rows.length),
           todas: idx.map(i => rows[i].label) };
}
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
  const parte = (k, cats) => cats.length ? `<div><span class="muted">${h(t(k))}:</span> ${cats.map(c => h(t('ct_' + c))).join(' · ')}</div>` : '';
  return `<div class="indlinea">${parte('cd_lid', x.lid)}${parte('cd_sop', x.sop)}</div>`;
}
function toolbar (total, shown) {
  const P = U.prefs, F = P.filters, G = P.flags;
  const active = Object.values(F).reduce((n, a) => n + a.length, 0) + Object.values(G).filter(Boolean).length
               + (P.objetivo !== '' ? 1 : 0) + (P.atributo !== '' ? 1 : 0) + (P.para ? 1 : 0) + (P.restr ? 1 : 0);
  // El valor que viaja en data-v es siempre el del snapshot (español): el idioma solo
  // cambia lo que se ve, nunca la clave con la que se filtra ni la del ícono.
  const group = (clave, cat, values, ancho) => `<div class="filtergroup ${ancho ? 'ancho' : ''}"><div class="lbl">${h(t(clave))}</div><div class="row">${
    values.map(v => `<button class="chip ${F[cat].includes(v) ? 'on' : ''}" data-a="filter" data-cat="${cat}" data-v="${h(v)}">${icon(v)}${h(dom(v))}</button>`).join('')
  }</div></div>`;
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
      <button class="btn ${ui.pickMode ? 'primary' : ''}" data-a="pickMode">${ui.pickMode ? `${h(t('comparing'))} (${ui.picks.length}/4)` : h(t('compare'))}</button>
      <span class="count"><b>${shown}</b> ${h(t('of'))} ${total}</span>
    </div>
    ${U.prefs.filtersOpen ? `<div class="filterpanel">
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
  return toolbar(total, rows.length) + body + pager(pages, ui.page, 'page') +
    (ui.pickMode && ui.picks.length >= 2
      ? `<div style="position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:center;padding:16px;
           background:linear-gradient(to top,var(--bg) 62%,transparent);z-index:50">
           <button class="btn primary" data-a="goCompare">${h(t('compare'))} ${ui.picks.length} →</button></div>` : '');
}
/** Paginador del roster y del armador de equipos: extremos, vecinos de la actual y "…"
 *  entre medio, así llega a todas las páginas sin una fila de veintitantos botones.
 *  `accion` es el data-a que atiende el clic ('page' o 'teamPage'). */
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
const FICHA_TABS = ['resumen', 'skills', 'analisis', 'armado', 'equipos', 'progreso', 'mas'];
function renderDetail () {
  const ch = CHAR_BY_ID[ui.charId];
  if (!ch) { ui.view = 'roster'; return renderRoster(); }
  const v = variant(ch.id, ui.uniformId);
  const cuerpo = { resumen: fichaResumen, skills: fichaSkills, analisis: fichaAnalisis, armado: fichaArmado,
                   equipos: fichaEquipos, progreso: fichaProgreso, mas: fichaMas }[ui.fichaTab];
  const ant = lugarAnterior();
  return `
  <div class="row" style="margin-bottom:14px">
    ${ant && ant.view !== 'roster' ? `<button class="btn sm primary" data-a="atras" title="${h(t('back_to').replace('{x}', nombreLugar(ant, true)))}">← ${h(nombreLugar(ant))}</button>` : ''}
    <button class="btn sm" data-a="back">${h(t('back_roster'))}</button>
    <button class="btn sm" data-a="pickThis" data-cid="${ch.id}" data-uid="${v.uid || ''}">${h(t('compare_this'))}</button>
    <button class="btn sm" data-a="edit" data-cid="${ch.id}">${h(t('edit'))}</button>
    <button class="btn sm ${ui.marcando ? 'primary' : ''}" data-a="marcarModo">${h(ui.marcando ? t('at_done') : t('at_edit'))}</button>
  </div>
  ${fichaCabecera(ch, v)}
  <div class="fcuerpo" id="fcuerpo">${cuerpo(ch, v)}</div>`;
}
/** Cabecera fija: quién es, con qué uniforme y qué parte de la ficha se está viendo. */
/** Abre la ficha de un personaje (con un uniforme) desde el roster o desde las flechas. */
function abrirFicha (cid, uid) {
  ui.view = 'detail'; ui.charId = cid; ui.uniformId = uid || 'base';
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
  const rank = rankLabel(v.key), nDif = verifDe(ch, v).dif.length;
  const stats = Object.entries(ch.stats || {}).filter(([, val]) => parseFloat(val) !== 0);
  const box = (k, val) => `<div class="stat"><div class="k">${h(k)}</div><div class="v">${val}</div></div>`;
  return `<div class="fid">
    <div class="row">
      <span class="tag dim">${h(dom(v.f))}</span>${insTag(v.ins)}
      ${v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}">${h(dom(r))}</span>`).join('')}
      ${rank ? `<span class="muted">${h(listName(listById(U.prefs.refList)))}:</span>
        <span class="tag solid" style="background:${rank.color}" title="${h(rank.todas.join(' · '))}">${h(rankTexto(rank))}</span>` : ''}
      ${nDif ? `<a href="#verif" class="tag ghost" style="color:var(--gold)" data-a="irVerif" title="${h(t('vf_title'))}">⚠ ${h(t('vf_tag').replace('{n}', nDif))}</a>` : ''}
    </div>
    <div class="statgrid">
      ${box(t('d_race'), icon(v.race) + h(dom(v.race) || '—'))}
      ${box(t('d_gender'), icon(v.gender) + h(dom(v.gender) || '—'))}
      ${box(t('d_origin'), h(dom(ch.origin) || '—'))}
      ${box(t('c_striker'), v.striker != null ? 'Skill ' + h(v.striker) : '—')}
      ${box(t('c_worldboss'), icon(v.wba) + h(dom(v.wba) || '—'))}
      ${box(t('us_atk'), ataqueHtml(tipoAtaque(v)))}
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
  ${panelUso(ch, v)}`;
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
    ${panelRotaciones(ch, v)}
    ${v.skills.map(sk => skillCard(sk, v.p)).join('')}`;
}
// ---------------------------------------------------------------------------
// ANÁLISIS (docs/MODELO.md, etapa 2): lo que hace la variante con sus skills según el
// catálogo de efectos. Lo calcula el build (scripts/modelo.py, MFF_ANALISIS); acá se muestra:
// a quién le llega cada efecto, desde qué skill y cuándo, con qué condición, si le sirve, y
// cómo se lee en PvE y en PvP, con su certeza y su fuente.
// ---------------------------------------------------------------------------
const DESTINOS_AN = ['e', 'q', 'r', 'i'];
/** El efecto de una fuente [skill, etapa, efecto] y cómo lo clasifica el catálogo. */
function fuenteAn (v, [si, ti, fi]) {
  const sk = v.skills[si], st = sk.st[ti], f = st.fx[fi], m = CATALOGO.skills[fila('ab', f.a).en];
  return { sk, st, f, m: m.por_patron ? m.por_patron[fila('desc', f.p).en] : m };
}
/** Desde qué skills sale y cuándo (la activación de su etapa), sin repetir. */
function fuentesAnHtml (v, fuentes) {
  const vistas = new Set();
  return fuentes.map(x => {
    const { sk, st } = fuenteAn(v, x), ac = st.ac != null ? txt('act', st.ac, st.av) : '', clave = sk.sl + '|' + ac;
    if (vistas.has(clave)) return '';
    vistas.add(clave);
    return `<span class="tag dim">${h(slotEs(sk.sl))}${ac ? ' · ' + h(ac) : ''}</span>`;
  }).join('');
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
function lecturaAn (L, modo) {
  return `<div class="anlect"><b>${h(modo)}</b>${h(bi(L))} <span class="cert ${L.certeza}">${h(t('cert_' + L.certeza))}</span>${fuentesHtml(L.fuente)}</div>`;
}
/** La primera letra en minúscula, para seguir una frase («A quien tiene Perforación»). */
function minuscula (x) { return x ? x[0].toLowerCase() + x.slice(1) : x; }
/** Las lecturas de PvE y de PvP; si dicen lo mismo, en una sola línea. */
function lecturasAn (pve, pvp) {
  if (pve && pvp && JSON.stringify(pve) === JSON.stringify(pvp)) return lecturaAn(pve, t('an_pve_pvp'));
  return (pve ? lecturaAn(pve, 'PvE') : '') + (pvp ? lecturaAn(pvp, 'PvP') : '');
}
/** Una entrada: el efecto, a qué aliados si es al equipo, de qué skills sale, su condición,
 *  si no le sirve, sus lecturas propias y su nota. El build manda «Give Power» solo cuando
 *  la fuente no dice qué otorga. */
function filaAn (v, an, i) {
  const [ie, d, objetivo, fuentes] = an.fx[i], e = CATALOGO.efectos[ie];
  const vacio = e.id === 'otorga', cond = condicionAn(v, fuentes), noSirve = (an.ns || []).includes(i);
  return `<div class="anfila">
    <div class="row"><span class="annom" ${vacio ? `title="${h(t('an_otorga_t'))}"` : ''}>${h(vacio ? t('an_otorga') : bi(e))}</span>
      ${d === 'q' ? objetivoTag(objetivo, true) : ''}${fuentesAnHtml(v, fuentes)}
      ${cond ? `<span class="muted">${h(cond)}</span>` : ''}
      ${noSirve ? `<span class="tag solid nosirve" title="${h(t('an_no_sirve_t').replace('{x}', minuscula(bi(CATALOGO.sirve[e.sirve]))))}">${h(t('an_no_sirve'))}</span>` : ''}</div>
    ${lecturasAn(e.pve, e.pvp)}
    ${e.nota ? `<div class="muted annota">${h(bi(e.nota))}</div>` : ''}
  </div>`;
}
/** Lo que va a un destino (él, el equipo, el rival, sus invocaciones), por grupo del catálogo,
 *  cada grupo con su lectura de PvE y de PvP. */
function seccionAn (v, an, d) {
  const porGrupo = new Map();
  an.fx.forEach((x, i) => {
    if (x[1] !== d) return;
    const g = CATALOGO.efectos[x[0]].grupo;
    if (!porGrupo.has(g)) porGrupo.set(g, []);
    porGrupo.get(g).push(i);
  });
  if (!porGrupo.size) return d === 'i' ? '' : `<div class="section"><h3>${h(t('an_' + d))}</h3><p class="muted">${h(t('an_nada'))}</p></div>`;
  return `<div class="section"><h3>${h(t('an_' + d))}</h3>
    ${CATALOGO.grupos.filter(g => porGrupo.has(g.id)).map(g => `<div class="angrupo">
      <div class="angh"><b>${h(bi(g))}</b> <span class="muted">${h(bi(g.que))}</span></div>
      ${lecturasAn(g.pve, g.pvp)}
      ${porGrupo.get(g.id).map(i => filaAn(v, an, i)).join('')}
    </div>`).join('')}
  </div>`;
}
/** Una línea por destino con los grupos de lo que da. */
function resumenAn (an) {
  return DESTINOS_AN.map(d => {
    const gs = CATALOGO.grupos.filter(g => an.fx.some(x => x[1] === d && CATALOGO.efectos[x[0]].grupo === g.id));
    return gs.length ? `<div><b>${h(t('an_' + d))}:</b> ${gs.map(g => h(bi(g))).join(', ')}</div>` : '';
  }).join('');
}
/** Con qué pega: de qué ataque sale su daño, de qué tipo y con qué elementos (etapa 1). */
function pegaAn (v) {
  const pf = perfilDe(v);
  if (!pf.esc.length) return `<span class="muted">${h(t('us_atk_none'))}</span>`;
  return `${h(t('an_escala'))} ${ataqueHtml(tipoAtaque(v))} · ${h(t('an_tipos'))} ${pf.tip.map(x => h(t('el_' + x))).join(' + ')} · ${
    h(t('an_elems'))}: ${pf.ele.length ? pf.ele.map(x => h(t('el_' + x))).join(', ') : h(t('an_sin_elem'))}`;
}
function fichaAnalisis (ch, v) {
  const an = ANALISIS[v.p];
  if (!an) return `<div class="empty"><div class="big">?</div><div>${h(t('an_sin_datos'))}</div></div>`;
  return `<p class="muted" style="margin-bottom:12px">${h(t('an_note'))}</p>
    <div class="section anres"><h3>${h(t('an_resumen'))}</h3>
      ${resumenAn(an)}
      <div><b>${h(t('an_pega'))}:</b> ${pegaAn(v)}</div>
      <div title="${h(t('an_roles_t'))}"><b>${h(t('an_roles'))}:</b> ${v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}">${h(dom(r))}</span>`).join(' ')}</div>
    </div>
    ${DESTINOS_AN.map(d => seccionAn(v, an, d)).join('')}
    ${an.sc ? `<div class="section"><h3>${h(t('an_sc'))}</h3><p class="muted">${h(t('an_sc_t'))}</p>
      ${an.sc.map(([si, ti, fi]) => { const sk = v.skills[si];
        return `<div class="anfila"><span class="tag dim">${h(slotEs(sk.sl))}</span> ${h(fila('ab', sk.st[ti].fx[fi].a).en)}</div>`; }).join('')}</div>` : ''}`;
}
/** Cómo armarlo: lo que las fuentes le asignan al personaje; las reglas generales de su
 *  tipo de ataque (iguales para todos) van plegadas. */
function fichaArmado (ch, v) {
  const ta = tipoAtaque(v);
  return `<div class="section"><h3>${h(t('ar_title'))}</h3>
    <p class="muted" style="margin-bottom:12px">${h(t('ar_note'))}
      <a href="#armado" data-a="irArmadoModos">${h(t('ar_more'))}</a></p>
    <div class="usogrid par">
      <div class="bloque"><h4>C.T.P.</h4>${armadoCTP(ch, v)}</div>
      <div class="bloque" id="artefacto"><h4>${h(t('ar_art'))}</h4>${armadoArtefacto(ch)}${artArmado(ch)}</div>
      <div class="bloque"><h4>${h(t('ga_iso_title'))}</h4>${isoArmado(ch, v)}</div>
      <div class="bloque"><h4>${h(t('md_uni_opts'))}</h4>${armadoOpciones(v)}</div>
    </div>
    <details class="reglas"><summary>${h(t('ar_rules'))}</summary>
      <div class="usogrid par">
        <div class="bloque"><h4>ISO-8</h4>${armadoISO(ta)}</div>
        <div class="bloque"><h4>${h(t('md_urus'))}</h4>${armadoUrus(ta)}</div>
      </div></details></div>`;
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
// «POR QUÉ» DE UNA TARJETA DE EQUIPO (combinaciones de 3 y «Cómo entraría en tus otros equipos»)
// Arriba, la suma de lo que le llega al personaje de la ficha (el foco) y le sirve: el liderazgo del
// líder de la tarjeta, los soportes de sus compañeros y sus artefactos (recibe(), lo mismo que la
// cobertura de la tarjeta), un renglón por stat y sin topes (Ezequiel, 3 de octubre de 2026); lo que se
// activa con una condición, aparte y con la condición. Plegado, el desglose por origen, con un enlace a
// cada skill en la ficha de quien la da. Después, lo demás: lo que da él, los bonos de equipo, los roles,
// la ventaja de clase y sus strikers; y, si se compara con el equipo de antes, lo que se pierde. Con los
// nombres cortos (el completo, en el title) y «a todos» si algo les llega a todos.
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
/** Cuándo llega un efecto de un soporte o un liderazgo (vacío si llega siempre): la activación del slot,
 *  lo que pide (Tier-2), la condición del efecto («con 2 personajes de Combate»), cuánto dura y, si
 *  acumula, hasta dónde. */
function condicionTxt (x, f) {
  const p = [];
  if (x.ac) p.push(minuscula(trTxt(x.ac)));
  if (x.req) p.push(minuscula(t('sp_req')) + ' ' + trTxt(x.req));
  if (f.c) p.push(trTxt(f.c));
  const d = f.d != null ? f.d : x.d;
  if (d != null) p.push(numTxt(d) + ' s');
  if (f.tope != null) p.push(t('sp_cap') + ' ' + numTxt(f.tope) + '%');
  return p.join(', ');
}
/** Un renglón de efecto: el stat (el texto de la app), el valor y, aparte, la condición. */
function renglonHtml (s, val, cond, extra) {
  return `${trHtml(s)}${val ? ` <b>${h(val)}</b>` : ''}${extra || ''}${cond ? ` <span class="muted">(${h(cond)})</span>` : ''}${
    sinClasificar(s) ? ` <span class="muted">(${h(t('sy_unclassified'))})</span>` : ''}`;
}
function efectoPqHtml (x, f) { return renglonHtml(f.s, valorTxt(f.v, f.i), condicionTxt(x, f)); }
/** Cómo se nombra a cada integrante: el personaje, sin uniforme, si en el equipo no hay otro con el
 *  mismo nombre; si no, el nombre completo. */
function nombreEn (vs) { return (x) => vs.some(y => y !== x && y.name === x.name) ? fullLabel(x) : x.name; }
function nombreHtml (x, nombre) { return `<span title="${h(fullLabel(x))}">${h(nombre(x))}</span>`; }
/** A quiénes les llega algo: «a todos» si les llega a todos los del equipo; si no, sus nombres. */
function aQuienesHtml (ms, vs, nombre) { return ms.length === vs.length ? h(t('pq_todos')) : ms.map(x => nombreHtml(x, nombre)).join(', '); }
/** Lo que le llega al foco, por origen: primero el líder, después los demás en el orden del equipo y, al
 *  final, el artefacto de cada uno. [{ de, art, skills: [lo de recibe()] }] */
function origenesDe (foco, vs, lider) {
  const pjs = [], arts = [];
  for (const a of lider ? [lider].concat(vs.filter(x => x !== lider)) : vs) {
    const rs = recibe(foco, a, a === lider);
    const sin = rs.filter(r => r.k !== 'artifact'), con = rs.filter(r => r.k === 'artifact');
    if (sin.length) pjs.push({ de: a, art: false, skills: sin });
    if (con.length) arts.push({ de: a, art: true, skills: con });
  }
  return pjs.concat(arts);
}
/** La suma de lo que le llega: un renglón por stat y condición (los que llegan siempre primero), sin
 *  topes. De cada uno, lo que llega sin artefacto y lo que solo llega con uno: v y i (% del instinto),
 *  [sin, con], null si de ese lado no llega nada con número; sin: si algo le llega sin artefacto. */
function sumaDe (origenes) {
  const m = new Map();
  for (const o of origenes) for (const { x, fx } of o.skills) for (const f of fx) {
    const cond = condicionTxt(x, f), txt = typeof f.v === 'string' ? f.v : null, clave = f.s + '|' + cond + '|' + (txt || '');
    let l = m.get(clave);
    if (!l) m.set(clave, l = { s: f.s, cond, txt, v: [null, null], i: [null, null], sin: false });
    const j = o.art ? 1 : 0;
    if (typeof f.v === 'number') l.v[j] = (l.v[j] || 0) + f.v;
    if (f.i != null) l.i[j] = (l.i[j] || 0) + f.i;
    if (!o.art) l.sin = true;
  }
  return [...m.values()].sort((a, b) => !!a.cond - !!b.cond);
}
/** ¿El renglón lleva «*» (algo de él solo llega con un artefacto)? Con número, si un artefacto le suma;
 *  sin número, si solo llega por artefactos. */
function conArtefacto (l) { return l.v[1] != null || l.i[1] != null || (!l.sin && l.v[0] == null && l.i[0] == null); }
function sumaLineaHtml (l) {
  const tot = (p) => p[0] == null && p[1] == null ? null : (p[0] || 0) + (p[1] || 0);
  const art = conArtefacto(l), sin = art && (l.v[0] != null || l.i[0] != null) ? valorTxt(l.v[0], l.i[0]) : '';
  return `<li>${renglonHtml(l.s, valorTxt(l.txt != null ? l.txt : tot(l.v), tot(l.i)), l.cond,
    (art ? `&nbsp;<span class="pqart" title="${h(t('cb_art'))}">*</span>` : '') +
    (sin ? ` <span class="muted">(${h(t('pq_sin_art').replace('{x}', sin))})</span>` : ''))}</li>`;
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
  const rotulo = t(CLAVE_SOPORTE[k]), sinSkill = `<span title="${h(t('pq_sin_skill'))}">${h(rotulo)}</span>`;
  let tab, ancla, txt = rotulo, extra = '', titulo = t('pq_ver').replace('{x}', fullLabel(de));
  if (k === 'artifact') {
    const art = ARTES.find(y => y.p === de.ch.p);
    if (!art) return sinSkill;
    tab = 'armado'; ancla = 'artefacto'; txt = art.name; titulo += ': ' + art.name + ' · ' + art.pasiva;
    extra = ` <span class="muted">(${h(t('sp_at6'))})</span>`;
  } else {
    const sk = skillDeSoporte(de, k, x);
    if (!sk) return sinSkill;
    const f = fila('name', sk.n);
    tab = 'skills'; ancla = anclaSkill(sk.sl); titulo += ': ' + slotEs(sk.sl) + (f ? ' · ' + f.en : '');
  }
  return `<button class="objlink" data-a="irSkill" data-cid="${de.cid}" data-uid="${de.uid || ''}" data-tab="${tab}" data-ancla="${ancla}"
    title="${h(titulo)}">${h(txt)}</button>${extra}`;
}
/** Lo que da el foco a los demás (sus soportes y, si es el líder de la tarjeta, su liderazgo, según
 *  recibe()), como grupos de agrupar(): uno por slot, con a quiénes les llega cada efecto. */
function daGrupos (foco, vs, lider) {
  const gs = new Map();
  for (const b of vs) if (b !== foco) for (const r of recibe(b, foco, foco === lider)) {
    let g = gs.get(r.k);
    if (!g) gs.set(r.k, g = { r: { tipo: LIDERAZGOS.includes(r.k) ? 'liderazgo' : 'soporte', de: foco, k: r.k, x: r.x }, fx: new Map() });
    for (const f of r.fx) { if (!g.fx.has(f)) g.fx.set(f, []); g.fx.get(f).push(b); }
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
    if (!g.fx.has(p.f)) g.fx.set(p.f, []);
    g.fx.get(p.f).push(p.para);
  }
  return out;
}
/** Un grupo, como viñeta: de dónde sale y, debajo, cada efecto con a quiénes les llega (en la viñeta, si
 *  les llega a los mismos). */
function grupoHtml (g, vs, nombre) {
  const { r } = g;
  if (!g.fx) { const txt = razonTxt(r, nombre), largo = razonTxt(r, fullLabel);
    return `<li${largo !== txt ? ` title="${h(largo)}"` : ''}>${h(txt)}</li>`; }
  const cab = r.tipo === 'bono' ? h(nombreBono(r))
    : `${nombreHtml(r.de, nombre)}: ${h(t(CLAVE_SOPORTE[r.k]))}${r.k === 'artifact' ? ` <span class="muted">(${h(t('pq_si_art'))})</span>` : ''}`;
  const efs = [...g.fx].sort((a, b) => r.x.fx.indexOf(a[0]) - r.x.fx.indexOf(b[0]));
  const quienes = (ms) => ms.map(x => x.key).join('|'), iguales = efs.every(([, ms]) => quienes(ms) === quienes(efs[0][1]));
  const a = (ms) => ` → ${aQuienesHtml(ms, vs, nombre)}`;
  return `<li>${cab}${iguales ? a(efs[0][1]) : ''}<ul>${efs.map(([f, ms]) => `<li>${efectoPqHtml(r.x, f)}${iguales ? '' : a(ms)}</li>`).join('')}</ul></li>`;
}
/** Los strikers del equipo en los que está el foco, como viñetas: «Jeff de Adam Warlock (5% al atacar)». */
function strikersPqHtml (foco, vs, nombre) {
  const out = [];
  for (const a of vs) for (const [x, p, cuando] of STRIKERS[a.cid] || []) {
    const b = vs.find(y => y !== a && y.cid === x);
    if (b && (a === foco || b === foco)) out.push(`<li>${h(t('cx_striker_de')).replace('{b}', () => nombreHtml(b, nombre)).replace('{a}', () => nombreHtml(a, nombre))} (${
      h(t('sk_' + cuando).replace('{p}', p))})</li>`);
  }
  return out;
}
/** El «Por qué» de una tarjeta de equipo, plegado (ver arriba). id: el de la tarjeta (con él se vuelve
 *  a abrir con «Atrás»); lider: el de la tarjeta; demas: las piezas que van en «Además» junto a lo que
 *  da él (en una combinación, las que no son de un soporte ni de un liderazgo: esos, de él y para él,
 *  ya están); pierde: las que se pierden respecto del equipo `antes` («Cómo entraría»). */
function porqueHtml (id, foco, vs, lider, demas, pierde, antes) {
  const nombre = nombreEn(vs), os = origenesDe(foco, vs, lider), suma = sumaDe(os), st = strikersPqHtml(foco, vs, nombre);
  const ademas = daGrupos(foco, vs, lider).concat(agrupar(demas)).map(g => grupoHtml(g, vs, nombre));
  if (st.length) ademas.push(`<li>${h(t('cx_strikers'))}<ul>${st.join('')}</ul></li>`);
  const menos = pierde.length ? agrupar(pierde).map(g => grupoHtml(g, antes, nombreEn(antes))) : [];
  return `<details class="usgrupo pq" id="${h(id)}"><summary>${h(t('eq_why'))}</summary><div class="pqcuerpo">
    <div class="pqsec"><div class="pqh">${h(t('pq_recibe').replace('{x}', nombre(foco)))}</div>
      ${suma.length ? `<ul class="pqlista pqsuma">${suma.map(sumaLineaHtml).join('')}</ul>
        ${suma.some(conArtefacto) ? `<p class="muted pqley">${h(t('cb_art'))}</p>` : ''}
        <details class="pqdesg" id="${h(id)}-d"><summary>${h(t('pq_desglose'))}</summary>${os.map(o => `<div class="pqorig">
          <div class="pqoh">${o.art ? h(t('pq_art_de')).replace('{x}', () => nombreHtml(o.de, nombre)) : nombreHtml(o.de, nombre)}${
            !o.art && o.de === lider ? ` <span class="muted">(${h(t('pq_lider'))})</span>` : ''}</div>
          <ul class="pqlista">${o.skills.map(r => `<li>${enlaceSkill(r)}<ul>${r.fx.map(f => `<li>${efectoPqHtml(r.x, f)}</li>`).join('')}</ul></li>`).join('')}</ul>
        </div>`).join('')}</details>`
      : `<p class="muted">${h(t('pq_nada'))}</p>`}</div>
    ${ademas.length ? `<div class="pqsec"><div class="pqh">${h(t('pq_ademas'))}</div><ul class="pqlista">${ademas.join('')}</ul></div>` : ''}
    ${menos.length ? `<div class="pqsec pqmenos"><div class="pqh">${h(t('pq_pierde'))}</div><ul class="pqlista">${menos.join('')}</ul></div>` : ''}
  </div></details>`;
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
    <div class="row" style="margin-top:10px">${botonArmar([v], '', '', t('eq_build_with'))}</div>
  </div>
  ${otros.length ? `<div class="section"><h3>${h(t('eq_could'))}</h3>
    <p class="muted" style="margin-bottom:10px">${h(t('eq_could_note').replace('{v}', fullLabel(v)))}</p>
    ${mejoran.map(o => `<div class="card eqsug">
      <div class="row" style="justify-content:space-between">
        <div><b>${h(o.tt.name)}</b>${o.modo ? ` <span class="tag dim">${h(o.modo)}</span>` : ''}
          <div class="muted">${h(o.sale ? t('eq_instead').replace('{x}', fullLabel(o.sale)) : t('eq_room'))}</div></div>
        <div class="eqpts"><b>${o.despues.score}</b> ${h(t('tm_synergy_pts'))} <span class="eqdelta">+${o.delta}</span>
          <div class="muted">${h(t('eq_before').replace('{n}', o.antes.score))}</div></div>
      </div>
      ${retratosEquipo(o.vs, v.key)}
      ${porqueHtml('pq-t-' + o.tt.id, v, o.vs, o.despues.lider, o.gana, o.pierde, o.antesVs)}
      ${ctpsEquipo(o.vs, o.ctp)}
      <div class="row">${botonArmar(o.vs, o.tt.modeId, t('eq_name_swap').replace('{e}', o.tt.name).replace('{v}', v.name))}</div>
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
  return `<div class="section" id="bonos"><h3>${h(t('bn_title'))}</h3>
    <p class="muted">${h(t('bn_note'))}</p>
    <details class="reglas"><summary>${h(t('bn_show').replace('{n}', bonos.length))}</summary>
      <div class="grid eqgrid">${bonos.map(b => `<div class="card bono">
        <b>${h(b.n || t('bn_noname'))}</b>
        ${retratosEquipo(b.m.filter(c => c !== ch.id).map(c => variant(c, null)), null)}
        ${b.vs.length > 1 ? `<div class="muted bonoaviso">${h(t('bn_tie'))}</div>` : ''}
        ${b.vs.map(v => `<div class="bonostats">${h(v.fx.map(efectoSoporteTxt).join(' · '))}</div>`).join('')}
        <div class="fuentes">${fuentesHtml(b.f)}</div>
      </div>`).join('')}</div>
    </details>
  </div>`;
}
/** Los strikers del personaje (de la pestaña Striker de la wiki; valen con cualquier uniforme) y de
 *  quiénes es striker, plegados: cada uno con su retrato, su probabilidad de aparecer y cuándo, de
 *  mayor a menor probabilidad. */
function strikersHtml (ch) {
  const suyos = STRIKERS[ch.id], de = STRIKERS_DE[ch.id] || [];
  const fotos = (filas) => `<div class="row eqfotos">${filas.slice().sort((a, b) => b[1] - a[1]).map(([cid, p, cuando]) => {
    const x = variant(cid, null);
    return `<button class="eqfoto stk" data-a="open" data-cid="${x.cid}" data-uid="" title="${h(x.name)}"><span class="shot">${shot(x.id)}</span>
      <span class="stknom">${h(x.name)}</span><span>${h(t('sk_' + cuando).replace('{p}', p))}</span></button>`;
  }).join('')}</div>`;
  return `<div class="section" id="strikers"><h3>${h(t('sk_title'))}</h3>
    <p class="muted">${h(t('sk_note'))}</p>
    ${suyos ? (suyos.length ? `<details class="reglas"><summary>${h(t('sk_suyos').replace('{n}', suyos.length))}</summary>${fotos(suyos)}</details>` : '')
            : `<p class="muted">${h(t('sk_sin_pestana'))}</p>`}
    ${de.length ? `<details class="reglas"><summary>${h(t('sk_de').replace('{n}', de.length))}</summary>
      <p class="muted">${h(t('sk_de_nota'))}</p>${fotos(de)}</details>` : `<p class="muted">${h(t('sk_de_nadie'))}</p>`}
    <div class="fuentes">${fuentesHtml(['wiki-strikers'])}</div>
  </div>`;
}
/** El mejor lugar para v en un equipo: reemplazando a cada integrante o, si hay lugar,
 *  sumándolo. Solo valen los lugares donde queda con vínculo con alguien del
 *  equipo; si no hay ninguno, no encaja. Con lo que se gana y se pierde según las razones (en
 *  piezas): de lo que se gana quedan afuera lo que le llega a v y lo que da él, que el «Por qué» de
 *  la tarjeta dice aparte. */
function comoEntra (v, tt) {
  const vs = tt.members.map(k => variant(...k.split('::'))).filter(Boolean);
  const opciones = vs.map((x, i) => ({ sale: x, vs: vs.map((y, j) => j === i ? v : y) }));
  if (vs.length < tamModo(tt.modeId)) opciones.push({ sale: null, vs: vs.concat(v) });
  const validas = opciones.map(o => Object.assign(o, { despues: synergy(o.vs) }))
    .filter(o => o.vs.some(x => x !== v && vinculo(v, x, o.despues.aplicados)));
  if (!validas.length) return { tt, sinVinculo: true };
  const antes = synergy(vs);
  const mejor = validas.sort((a, b) => b.despues.score - a.despues.score)[0];
  const modo = modosEquipo().find(m => m.id === tt.modeId);
  const pa = piezas(antes.razones), pd = piezas(mejor.despues.razones);
  const habia = new Set(pa.map(p => p.clave)), hay = new Set(pd.map(p => p.clave));
  return { tt, antes, antesVs: vs, vs: mejor.vs, sale: mejor.sale, despues: mejor.despues, delta: mejor.despues.score - antes.score,
           modo: modo ? modo.name : '', ctp: modo ? modo.ctp : null,
           gana: pd.filter(p => !habia.has(p.clave) && !(p.f && p.r.tipo !== 'bono' && (p.para === v || p.r.de === v))),
           pierde: pa.filter(p => !hay.has(p.clave)) };
}
/** Retratos de un equipo; el de la clave `resaltada` (el personaje de la ficha) va marcado. */
function retratosEquipo (vs, resaltada) {
  return `<div class="row eqfotos">${vs.map(x => `<button class="eqfoto ${x.key === resaltada ? 'nuevo' : ''}" data-a="open" data-cid="${x.cid}"
    data-uid="${x.uid || ''}" title="${h(fullLabel(x))}"><span class="shot">${shot(x.id)}</span><span>${h(x.name)}</span></button>`).join('')}</div>`;
}
// COMBINACIONES DE 3 CON ÉL: una consulta sobre los datos, no listas armadas de antemano.
// Para el personaje (con el uniforme elegido) recorre todas las parejas de compañeros y se
// queda con los equipos en que los dos tienen vínculo con él (vinculo()), con el puntaje para
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
// CONTEXTO PvP / PvE (reglas de Ezequiel, 2 de octubre de 2026). Un equipo vale según dónde se usa:
// - Quién es DPS, soporte o líder sale de las filas de las tier lists del contexto (rolEn). Un trío
//   sin ningún DPS de ese contexto no sirve.
// - En PvP los tres tienen que tener anti-mermas (Remove All Debuffs o Debuff Immunity), del
//   liderazgo del líder o del soporte de alguno; si viene de un soporte, el lugar de líder queda
//   para otro liderazgo. En PvE no hace falta.
// - Los liderazgos que más valen: en PvP, todos los ataques, todas las defensas, la vida (PG) e
//   ignorar evasión; en PvE, los de daño (ataque, daño elemental y daño a jefes), cada uno a quien
//   pega con eso. Las defensas, desde que Ezequiel eligió a Thanos — Annihilation de líder por todo
//   lo que suma (anti-mermas, ataques y defensas) por sobre Black Cat — Queen in Black (ataques e
//   ignorar evasión): con los tres stats de antes, Black Cat sumaba el doble.
// - La sinergia (soportes y bonos de equipo) y los strikers son relevantes pero no definitorios:
//   pesan la mitad.
// Puntaje de contexto: 2 por cada stat que vale del liderazgo del líder y cada integrante al que le
// llega y le sirve (1 si el liderazgo se activa con una condición: el slot trae ac), 2 por cada nivel
// de fila de cada DPS (3 la más alta), 1 por cada soporte que le llega a otro y le sirve, 1 por cada
// bono de equipo activo que le sirve a alguien y 1 por cada striker del trío (uno es striker de otro).
// El líder es el que más suma de los que cumplen; a igual puntaje, el mejor ubicado en las tier lists
// del contexto y después la clave. Es el mismo en las listas de los tres (Ezequiel, 2 de octubre de
// 2026: «único + condicional a la mitad», sin mirar los porcentajes).
const ANTI_MERMAS = new Set(['Remove All Debuffs', 'Debuff Immunity']);
const LIDERAZGO_VALE = {
  pvp: new Set(['All Basic Attacks', 'All Basic Attacks (Stackable)', 'All Basic Defenses', 'HP', 'Ignore Dodge']),
  pve: new Set(['All Basic Attacks', 'All Basic Attacks (Stackable)', 'Physical Attack', 'Energy Attack', 'Fire Damage',
                'Fire Damage by % Fire Resist', 'Cold Damage', 'Lightning Damage', 'Poison Damage', 'Mind Damage',
                'All Element Damage', 'Basic Damage Dealt to Boss Types']),
};
for (const c of Object.values(LIDERAZGO_VALE)) for (const st of c) {
  if (!PIDE[st] && !PARA_TODOS.has(st)) throw new Error('liderazgo que vale con un stat que no dice a quién le sirve: ' + st);
}
const PESO = { lider: 2, dps: 2, sinergia: 1, striker: 1 };
/** Índice de cada stat que vale, por contexto, y a quiénes les llega cada uno (bits de integrante:
 *  0-2 por un liderazgo permanente, 3-5 por uno condicional), reusado en los cientos de miles de
 *  tríos de la consulta. */
const VALE_IDX = Object.fromEntries(Object.entries(LIDERAZGO_VALE).map(([c, st]) => [c, new Map([...st].map((x, i) => [x, i]))]));
const _LLEGA = Object.fromEntries(Object.entries(LIDERAZGO_VALE).map(([c, st]) => [c, new Uint8Array(st.size)]));
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
function tieneFuncion (v, ctx) { const r = rolEn(v, ctx); return r.dps > 0 || r.soporte > 0 || r.lider || r.striker; }
/** Liderazgos y soportes de un retrato, y cuáles dan anti-mermas, para el puntaje de contexto. */
const _SLOTS = new Map();
function slotsDe (v) {
  let s = _SLOTS.get(v.p);
  if (s) return s;
  const so = SOPORTES[v.p] || {};
  s = { lid: [], sop: [], antiLid: [], antiSop: [] };
  for (const [k] of TIPOS_SOPORTE) {
    const x = so[k];
    if (!x) continue;
    const lid = LIDERAZGOS.includes(k), anti = x.fx.some(f => ANTI_MERMAS.has(f.s));
    (lid ? s.lid : s.sop).push(x);
    if (anti) (lid ? s.antiLid : s.antiSop).push(x);
  }
  if (v.p) _SLOTS.set(v.p, s);
  return s;
}
/** Un trío en un contexto. null si no entra: sin ningún DPS de ese contexto o, en PvP, sin un líder
 *  con el que los tres tengan anti-mermas. Si entra: { score, lider, partes: { lider, dps, sinergia,
 *  striker } }; con detalle, también de dónde sale cada punto (detalleContexto lo escribe). */
function enContexto (vs, ctx, detalle) {
  const roles = vs.map(x => rolEn(x, ctx));
  if (!roles.some(r => r.dps)) return null;
  const sl = vs.map(slotsDe);
  const cubreSop = vs.map(m => sl.some(s => s.antiSop.some(x => aplicaA(x, m))));
  const vale = VALE_IDX[ctx], llega = _LLEGA[ctx];
  let li = -1, ptsLider = 0;
  for (let i = 0; i < vs.length; i++) {
    if (ctx === 'pvp' && !vs.every((m, j) => cubreSop[j] || sl[i].antiLid.some(x => aplicaA(x, m)))) continue;
    // Cada stat que vale cuenta una vez por integrante, aunque el liderazgo lo traiga en varias
    // líneas (Arachknight 2099: todos los ataques +45%, +55% o +65% según sus Infinity Warps), con
    // la de más peso: PESO.lider si le llega por un liderazgo permanente y la mitad si solo le llega
    // por uno que se activa con una condición (Silver Surfer: al recibir un debuff).
    llega.fill(0);
    for (const x of sl[i].lid) {
      const b = x.ac ? 3 : 0;
      for (const f of x.fx) {
        const k = vale.get(f.s);
        if (k === undefined) continue;
        for (let j = 0; j < vs.length; j++) if (aplicaA(x, vs[j]) && sirve(f, vs[j])) llega[k] |= 1 << (b + j);
      }
    }
    let pts = 0;
    for (const bits of llega) pts += aCuantos(bits) * PESO.lider + aCuantos(bits >> 3 & ~bits) * PESO.lider / 2;
    // El mismo líder sea cual sea el orden de vs: a igual puntaje, el mejor ubicado en las tier lists
    // del contexto y después la clave.
    if (li < 0 || pts > ptsLider || (pts === ptsLider && (roles[i].puesto < roles[li].puesto
        || (roles[i].puesto === roles[li].puesto && vs[i].key < vs[li].key)))) { li = i; ptsLider = pts; }
  }
  if (li < 0) return null;
  let dps = 0;
  for (const r of roles) dps += r.dps * PESO.dps;
  let sinergia = 0;
  for (let a = 0; a < vs.length; a++) for (const x of sl[a].sop) {
    if (vs.some((b, j) => j !== a && aplicaA(x, b) && leSirve(x, b))) sinergia += PESO.sinergia;
  }
  for (const a of vs) for (const b of BONOS_DE[a.cid] || []) {
    if (b.m[0] === a.cid && estanTodos(b.m, vs) && vs.some(x => b.vs.some(bv => leSirve(bv, x)))) sinergia += PESO.sinergia;
  }
  let striker = 0;
  for (const a of vs) { const ss = STRIKER_SET[a.cid]; if (ss) for (const b of vs) if (b !== a && ss.has(b.cid)) striker += PESO.striker; }
  const out = { score: ptsLider + dps + sinergia + striker, lider: vs[li], partes: { lider: ptsLider, dps, sinergia, striker } };
  if (detalle) Object.assign(out, { roles, sl, cubreSop });
  return out;
}
function consultaCon (v) {
  if (CONSULTA && CONSULTA.clave === v.key) return CONSULTA;
  const pool = allVariants().filter(x => x.cid !== v.cid);
  const puede = pool.map(x => puedeVincular(x, v) || puedeVincular(v, x));
  // En los contextos PvP y PvE, un DPS de ese contexto entra aunque no tenga vínculo con él.
  const dps = pool.map(x => rolEn(x, 'pvp').dps > 0 || rolEn(x, 'pve').dps > 0);
  const max = pool.length * (pool.length - 1) / 2;
  // F: qué compañeros tienen vínculo con él (1, el primero; 2, el segundo). P: los puntos para él y
  // L: el líder de la sinergia, el de la tarjeta (0 él, 1 o 2 el compañero, 3 ninguno; lo usa el
  // filtro de cobertura), solo con los dos vinculados (el orden «puntos para él» y las tier lists
  // solo usan esas filas).
  const A = new Int32Array(max), B = new Int32Array(max), P = new Int16Array(max), F = new Uint8Array(max), L = new Uint8Array(max);
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
      let f = 0, pts = 0, li = 3;
      if (puede[i] || puede[j]) {
        const sc = synergy(vs, op);
        if (puede[i] && vinculo(v, pool[i], sc.aplicados)) f |= 1;
        if (puede[j] && vinculo(v, pool[j], sc.aplicados)) f |= 2;
        pts = sc.score;
        if (sc.lider) li = vs.indexOf(sc.lider);
      }
      if (f !== 3 && !((f & 1 || dps[i]) && (f & 2 || dps[j]))) continue;
      A[n] = i; B[n] = j; P[n] = pts; F[n] = f; L[n] = li; n++;
    }
  }
  CONSULTA = { clave: v.key, cid: v.cid, v, pool, A, B, P, F, L, n, vista: null };
  return CONSULTA;
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
function puestoTexto (l, key) { const i = indicesFila(l, key); return i.length ? rowsOf(l)[i[0]].label : '—'; }
/** Filas de la consulta en el orden elegido y con los filtros, una por trío de personajes: la
 *  primera en ese orden (el mejor uniforme de cada uno para ese orden) que pasa los filtros; con
 *  casillas de cobertura, la primera con ✓ en todas. Con tier lists, gana el trío mejor ubicado
 *  (suma de puestos); a igual puesto, más puntos para él; después, el mejor ubicado en tu lista
 *  de referencia. Los tríos descartados no van (o van solos, si se piden): { filas, ocultos }. */
function vistaConsulta (q) {
  // Descartes en los que está él: los otros dos personajes de cada uno.
  const descartes = new Set(U.descartados.filter(d => d.includes(q.cid)).map(d => d.filter(c => c !== q.cid).join('|')));
  const clave = [ui.eqOrden, ui.eqExcluir.join(','), ui.eqCon, ui.eqCobertura.join(','), ui.eqVerDescartados,
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
  // Orden por una sola clave numérica por fila: el orden nativo de un Float64Array es varias veces
  // más rápido que comparar de a pares. Cada parte entra en su lugar: si no entrara, el orden
  // saldría mal sin avisar. Sin contexto: puestos, puntos para él al revés, referencia y fila, solo
  // con los dos compañeros vinculados. En PvP y PvE: el puntaje de contexto al revés, los puestos,
  // la referencia y la fila, con cada compañero vinculado o DPS de ese contexto, y si el trío entra.
  const claves = new Float64Array(q.n), vs = [q.v, null, null];
  let m = 0;
  for (let i = 0; i < q.n; i++) {
    const ps = pos[q.A[i]] + pos[q.B[i]], rf = ref[q.A[i]] + ref[q.B[i]];
    let pts;
    if (!ctx) {
      if (q.F[i] !== 3) continue;
      pts = q.P[i];
    } else {
      if (!((q.F[i] & 1 || dpsCtx[q.A[i]]) && (q.F[i] & 2 || dpsCtx[q.B[i]]))) continue;
      vs[1] = q.pool[q.A[i]]; vs[2] = q.pool[q.B[i]];
      const e = enContexto(vs, ctx);
      if (!e) continue;
      pts = e.score;
      if (lider) lider[i] = vs.indexOf(e.lider);
    }
    if (ps >= 4096 || pts < 0 || pts >= 128 || rf >= 2048) throw new Error('orden de combinaciones fuera de rango: ' + [ps, pts, rf]);
    claves[m++] = ctx ? (((127 - pts) * 4096 + ps) * 2048 + rf) * 1048576 + i
                      : ((ps * 128 + (127 - pts)) * 2048 + rf) * 1048576 + i;
  }
  const ordenadas = claves.subarray(0, m).sort();
  const fuera = new Set(ui.eqExcluir), vistos = new Set(), filas = [];
  let ocultos = 0;
  for (const k of ordenadas) {
    const i = k % 1048576;
    const a = q.pool[q.A[i]], b = q.pool[q.B[i]];
    if (fuera.has(a.cid) || fuera.has(b.cid) || (ui.eqCon && a.cid !== ui.eqCon && b.cid !== ui.eqCon)) continue;
    const pareja = a.cid < b.cid ? a.cid + '|' + b.cid : b.cid + '|' + a.cid;
    // Con casillas de cobertura, cada pareja va con su primera combinación de uniformes que las cumple.
    if (vistos.has(pareja) || (cubre && !cubre(i, lider[i]))) continue;
    vistos.add(pareja);
    const descartado = descartes.has(pareja);
    if (descartado) ocultos++;
    if (descartado === ui.eqVerDescartados) filas.push(i);
  }
  q.vista = { clave, filas, ocultos };
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
/** De dónde salen los puntos de contexto de un trío, un renglón por parte del puntaje con sus viñetas:
 *  los anti-mermas (en PvP), el liderazgo del líder (cada efecto y a quiénes les llega), los DPS con su
 *  fila, los soportes y bonos de equipo, y los strikers. Con los nombres cortos (el completo, en el
 *  title) y «a todos» si algo les llega a los tres. */
function detalleContexto (e, vs, ctx) {
  const nombre = nombreEn(vs), quien = (x) => nombreHtml(x, nombre), a = (ms) => aQuienesHtml(ms, vs, nombre);
  const partes = [];      // [rótulo (HTML), puntos o null, [viñetas (HTML)]]
  if (ctx === 'pvp') {
    const fuentes = new Map();
    vs.forEach(m => {
      const de = vs.find((x, k) => e.sl[k].antiSop.some(y => aplicaA(y, m)));
      const k = (de ? 'cx_de_sop|' : 'cx_de_lid|') + (de || e.lider).key;
      if (!fuentes.has(k)) fuentes.set(k, { de: de || e.lider, clave: de ? 'cx_de_sop' : 'cx_de_lid', ms: [] });
      fuentes.get(k).ms.push(m);
    });
    partes.push([h(t('cx_anti')), null, [...fuentes.values()].map(f => `${h(t(f.clave)).replace('{x}', () => quien(f.de))} → ${a(f.ms)}`)]);
  }
  // Por stat que vale y activación: sus líneas (un liderazgo puede traer varias del mismo stat) y a
  // quiénes llega. Las de un liderazgo condicional cuentan la mitad, y solo para quien no recibe el
  // mismo stat de uno permanente (cada stat cuenta una vez por integrante, la de más peso).
  const vale = LIDERAZGO_VALE[ctx], grupos = new Map(), lleno = new Set();
  for (const x of slotsDe(e.lider).lid) for (const f of x.fx) {
    if (!vale.has(f.s)) continue;
    const k = f.s + '|' + (x.ac || '');
    const g = grupos.get(k) || { s: f.s, ac: x.ac, txt: [], ms: new Set() };
    grupos.set(k, g);
    g.txt.push(efectoSoporteTxt(f));
    vs.forEach(m => { if (aplicaA(x, m) && sirve(f, m)) { g.ms.add(m); if (!x.ac) lleno.add(f.s + '|' + m.key); } });
  }
  const liderazgo = [...grupos.values()].map(g => {
    const ms = vs.filter(m => g.ms.has(m) && !(g.ac && lleno.has(g.s + '|' + m.key)));
    const cond = g.ac ? ` (${t('cx_lider_mitad').replace('{c}', minuscula(trTxt(g.ac)))})` : '';
    return ms.length ? `${h(g.txt.join(' / ') + cond)} → ${a(ms)}` : null;
  }).filter(Boolean);
  partes.push([h(t('cx_lider')).replace('{x}', () => quien(e.lider)), e.partes.lider, liderazgo.length ? liderazgo : [h(t('cx_lider_nada'))]]);
  const dps = vs.map((m, j) => ({ m, r: e.roles[j] })).filter(x => x.r.dps).map(({ m, r }) =>
    `${quien(m)} (${h(r.filas.filter(([l, fid]) => ROLES_LISTAS[ctx][l.id][fid][0] === 'dps')
      .map(([l, fid]) => `${listName(l)}: ${rowsOf(l).find(x => x.id === fid).label}`).join(', '))})`);
  partes.push([h(t('cx_dps')), e.partes.dps, dps]);
  if (e.partes.sinergia) partes.push([h(t('cx_sinergia')), e.partes.sinergia, []]);
  if (e.partes.striker) {
    const pares = [];
    for (const x of vs) for (const [c, p, cuando] of STRIKERS[x.cid] || []) {
      const b = vs.find(y => y !== x && y.cid === c);
      if (b) pares.push(`${h(t('cx_striker_de')).replace('{b}', () => quien(b)).replace('{a}', () => quien(x))} (${h(t('sk_' + cuando).replace('{p}', p))})`);
    }
    partes.push([h(t('cx_strikers')), e.partes.striker, pares]);
  }
  return `<ul class="cxpts">${partes.map(([k, pts, vi]) => `<li><b>${k}${pts != null ? ` +${pts}` : ''}</b>${
    vi.length ? `<ul>${vi.map(x => `<li>${x}</li>`).join('')}</ul>` : ''}</li>`).join('')}</ul>`;
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
  const cab = `<h3>${h(t('eq_new'))}</h3><p class="muted" style="margin-bottom:10px">${h(t('eq_new_note'))}</p>
    <p class="muted" style="margin-bottom:10px">${h(t('cb_note'))}</p>`;
  const ctx = contextoOrden();
  // Sin función en el contexto, no hay lista: solo el aviso y el orden, para cambiarlo. Tampoco se
  // calcula la consulta.
  if (ctx && !tieneFuncion(v, ctx)) {
    return `<div class="section" id="combos">${cab}<div class="row eqfiltros">${ordenCombinacionesHtml()}</div>
      <p class="muted cxnota">${h(t('cx_sin_funcion_' + ctx).replace('{x}', fullLabel(v))
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
  const q = CONSULTA, { filas, ocultos } = vistaConsulta(q), ls = listasOrden();
  const paginas = Math.max(1, Math.ceil(filas.length / POR_PAGINA));
  ui.eqPagina = Math.min(ui.eqPagina, paginas - 1);
  const personajes = CHARS.filter(c => c.id !== v.cid).sort((a, b) => a.name.localeCompare(b.name));
  const fila = (i) => {
    const vs = [v, q.pool[q.A[i]], q.pool[q.B[i]]], keys = vs.map(x => x.key);
    const sc = synergy(vs, { foco: v });
    // En PvP y PvE, el líder y los puntos son los del contexto; los de siempre quedan abajo.
    const e = ctx ? enContexto(vs, ctx, true) : null, lider = e ? e.lider : sc.lider;
    return `<div class="card combo">
      <div class="combofila">
        ${estrella(keys)}${retratosEquipo(vs, v.key)}
        <div class="combotx">
          <div>${h(vs.slice(1).map(fullLabel).join(' + '))}</div>
          <div class="combolider">${h(lider ? t('eq_leader').replace('{x}', fullLabel(lider)) : t('eq_no_leader'))}</div>
          ${e ? detalleContexto(e, vs, ctx) : ''}
          ${coberturaHtml(cobertura(v, vs, lider))}
          ${ls.map(l => `<div class="muted">${h(listName(l))}: ${vs.map(x => h(puestoTexto(l, x.key))).join(' · ')}</div>`).join('')}
        </div>
        ${e ? `<div class="eqpts"><b>${e.score}</b> ${h(t('cx_pts_' + ctx))}
          <div class="muted">${h(t('cx_para_el').replace('{a}', sc.score).replace('{b}', synergy(vs).score))}</div></div>`
            : `<div class="eqpts"><b>${sc.score}</b> ${h(t('eq_pts_for'))}
          <div class="muted">${h(t('eq_pts_team').replace('{n}', synergy(vs).score))}</div></div>`}
        ${botonArmar(vs, '', '')}
        ${ui.eqVerDescartados
          ? `<button class="btn sm" data-a="restaurar" data-c="${vs.map(x => x.cid).join(',')}">${h(t('eq_restaurar'))}</button>`
          : `<button class="btn sm" data-a="descartar" data-c="${vs.map(x => x.cid).join(',')}" title="${h(t('eq_descartar_title'))}">${h(t('eq_descartar'))}</button>`}
      </div>
      ${porqueHtml('pq-c-' + keys.join('_'), v, vs, lider, piezas(sc.razones).filter(p => !p.f || p.r.tipo === 'bono'), [], null)}
      ${ctpsEquipo(vs, ctx)}
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
    <div class="row" style="gap:6px;margin-bottom:10px" title="${h(t('eq_cob_title'))}"><div class="muted">${h(t('eq_cob'))}</div>
      ${COBERTURA.map(g => `<label class="chk"><input type="checkbox" data-a="eqCobertura" data-g="${g.k}"${ui.eqCobertura.includes(g.k) ? ' checked' : ''}>
        ${h(g.k === 'ataque' ? t('cb_ataque') : t('ct_' + g.k))}</label>`).join('')}</div>
    ${ctx ? `<p class="muted cxnota">${h(t('cx_nota_' + ctx).replace('{l}', nombresListas(ctx === 'pvp' ? LISTAS_PVP : LISTAS_PVE)))}</p>` : ''}
    ${ui.eqExcluir.length ? `<div class="row" style="gap:6px;margin-bottom:10px">${ui.eqExcluir.map(cid =>
      `<button class="tag dim eqfuera" data-a="eqIncluir" data-cid="${h(cid)}" title="${h(t('eq_incluir'))}">${h(CHAR_BY_ID[cid].name)} ✕</button>`).join('')}</div>` : ''}
    <div class="row" style="justify-content:space-between;margin-bottom:10px">
      <span class="muted">${h(ui.eqVerDescartados ? cuantos(ocultos, 'eq_count_desc')
        : cuantos(filas.length, 'eq_count') + (ocultos ? ' · ' + cuantos(ocultos, 'eq_count_desc') : ''))}</span>
      ${ocultos || ui.eqVerDescartados ? `<button class="btn sm ${ui.eqVerDescartados ? 'primary' : ''}" data-a="eqVerDescartados">${h(ui.eqVerDescartados
        ? t('eq_ver_lista') : t('eq_ver_desc').replace('{n}', numero(ocultos)))}</button>` : ''}
    </div>
    ${filas.length ? filas.slice(ui.eqPagina * POR_PAGINA, (ui.eqPagina + 1) * POR_PAGINA).map(fila).join('')
                   : `<p class="muted">${h(t(ui.eqVerDescartados ? 'eq_none_desc' : 'eq_none_q'))}</p>`}
    ${pager(paginas, ui.eqPagina, 'eqPagina')}
  </div>`;
}
/** El resto: verificación entre fuentes y el retrato propio. */
function fichaMas (ch, v) {
  return `<div class="section" id="verif"><h3>${h(t('vf_title'))}</h3><div class="bloque">${usoVerificacion(ch, v)}</div></div>
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
// GLOSARIO
// El glosario de skills del juego (scripts/contenido/glosario.json): qué dice cada término y lo
// que el inglés traduce distinto del coreano, que es el original. Y todos los efectos del catálogo,
// por grupo, con sus lecturas de PvE y de PvP, a quién le sirven y cómo aparecen en las skills.
// ============================================================================
/** Para buscar: sin tildes ni mayúsculas. */
function plano (s) { return String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
function nombreGl (x) { return LANG === 'es' ? x.es : x.en; }
function enlaceGl (destino, texto, titulo) {
  return `<a href="#${destino}" class="tag ghost" data-a="irGlos" data-v="${destino}"${titulo ? ` title="${h(titulo)}"` : ''}>${h(texto)}</a>`;
}
/** Un término del juego: sus nombres (el del idioma de la app primero), qué dice, lo que el inglés
 *  traduce distinto, qué C.T.P. lo da y a qué efectos del catálogo corresponde. */
function terminoGl (x, errores) {
  const otros = [LANG === 'es' && x.en !== x.es ? x.en : '', x.ko].filter(Boolean).join(' · ');
  return `<div class="glterm" id="gl-${x.id}">
    <div class="row"><b>${h(nombreGl(x))}</b><span class="muted">${h(otros)}</span>
      ${x.difiere ? `<span class="tag solid gldif">${h(t('gl_difiere_tag'))}</span>` : ''}
      ${x.falta ? `<span class="tag dim">${h(t('gl_falta_' + x.falta))}</span>` : ''}</div>
    <p>${h(bi(x.que))}</p>
    ${x.difiere ? `<div class="gldifbox"><b>${h(t('gl_en_ko'))}</b> ${h(bi(x.difiere))}
      ${x.error ? `<div class="row">${enlaceGl('gle-' + x.error, bi(errores[x.error].titulo))}</div>` : ''}</div>` : ''}
    ${x.ctp ? `<div class="muted">${h(t('gl_lo_da'))} ${x.ctp.map(c =>
      h(CTPS.find(k => k.id === c.id).name + ' ' + t(c.reforjado ? 'gl_reforjado' : 'gl_sin_reforjar'))).join(', ')}</div>` : ''}
    ${x.nota ? `<div class="muted">${h(bi(x.nota))}</div>` : ''}
    ${x.efectos.length ? `<div class="row"><span class="muted">${h(t('gl_en_catalogo'))}</span>${
      x.efectos.map(id => enlaceGl('ef-' + id, bi(GL_DE[id].e))).join('')}</div>` : ''}
    <div class="fuentes">${fuentesHtml(x.fuente)}</div>
  </div>`;
}
/** Los errores del inglés que se repiten, con sus términos, y las otras diferencias. */
function erroresGl () {
  return `<div class="section"><h3>${h(t('gl_errores'))}</h3>
    <p class="muted glnota">${h(t('gl_errores_nota'))}</p>
    ${GLOSARIO.errores.map(e => `<div class="glerr" id="gle-${e.id}"><b>${h(bi(e.titulo))}</b><p>${h(bi(e.texto))}</p>
      <div class="row">${GLOSARIO.terminos.filter(x => x.error === e.id).map(x => enlaceGl('gl-' + x.id, nombreGl(x))).join('')}</div></div>`).join('')}
    <h4 class="glh4">${h(t('gl_otras'))}</h4>
    ${GLOSARIO.terminos.filter(x => x.difiere && !x.error).map(x =>
      `<div class="glotra">${enlaceGl('gl-' + x.id, nombreGl(x))} ${h(bi(x.difiere))}</div>`).join('')}
  </div>`;
}
/** Un efecto del catálogo: su nombre, los términos del juego que le corresponden, sus lecturas de
 *  PvE y de PvP, su nota, a quién le sirve y las etiquetas con que aparece en las skills. */
function efectoGl (e) {
  const d = GL_DE[e.id];
  return `<div class="anfila glef" id="ef-${e.id}">
    <div class="row"><span class="annom">${h(bi(e))}</span>${LANG === 'es' ? `<span class="muted">${h(e.en)}</span>` : ''}
      ${d.terminos.map(x => enlaceGl('gl-' + x.id, nombreGl(x) + ' · ' + x.ko, t('gl_termino'))).join('')}</div>
    ${lecturasAn(e.pve, e.pvp)}
    ${e.nota ? `<div class="muted annota">${h(bi(e.nota))}</div>` : ''}
    <div class="muted annota">${h(t('gl_le_sirve'))} ${h(minuscula(bi(CATALOGO.sirve[e.sirve])))}</div>
    ${d.etiquetas.length ? `<div class="glet"><span class="muted">${h(t('gl_en_skills'))}</span>${
      d.etiquetas.map(i => `<span class="tag dim">${h(txt('ab', i))}</span>`).join('')}</div>` : ''}
  </div>`;
}
function renderGlosario () {
  const q = plano(ui.glBusca.trim());
  const pasa = (...nombres) => !q || nombres.some(n => plano(n).includes(q));
  const terminos = GLOSARIO.terminos.filter(x => pasa(x.es, x.en, x.ko));
  const efectos = CATALOGO.efectos.filter(e => { const d = GL_DE[e.id];
    return pasa(e.es, e.en, ...d.terminos.flatMap(x => [x.es, x.en, x.ko]), ...d.etiquetas.flatMap(i => [fila('ab', i).en, txt('ab', i)])); });
  const errores = Object.fromEntries(GLOSARIO.errores.map(e => [e.id, e]));
  return `<div class="page-head"><div><h1>${h(t('gl_title'))}</h1><div class="sub">${h(t('gl_note'))}</div></div></div>
    <div class="row glbusca"><div class="search"><input id="q" placeholder="${h(t('gl_busca'))}" value="${h(ui.glBusca)}" data-a="glBusca"></div>
      <span class="muted">${h(t('gl_cuenta').replace('{t}', terminos.length).replace('{e}', efectos.length))}</span></div>
    ${!terminos.length && !efectos.length ? `<div class="empty"><div>${h(t('gl_nada'))}</div></div>` : ''}
    ${q ? '' : erroresGl()}
    ${terminos.length ? `<div class="section"><h3>${h(t('gl_terminos'))}</h3>
      <p class="muted glnota">${h(t('gl_terminos_nota').replace('{n}', GLOSARIO.terminos.length))}</p>
      <div class="glterms">${terminos.map(x => terminoGl(x, errores)).join('')}</div></div>` : ''}
    ${efectos.length ? `<div class="section"><h3>${h(t('gl_efectos'))}</h3>
      <p class="muted glnota">${h(t('gl_efectos_nota'))}</p>
      ${CATALOGO.grupos.filter(g => efectos.some(e => e.grupo === g.id)).map(g => `<div class="angrupo">
        <div class="angh"><b>${h(bi(g))}</b> <span class="muted">${h(bi(g.que))}</span></div>
        ${lecturasAn(g.pve, g.pvp)}
        ${efectos.filter(e => e.grupo === g.id).map(efectoGl).join('')}
      </div>`).join('')}</div>` : ''}`;
}

// ============================================================================
// COMPARACIÓN
// ============================================================================
function renderCompare () {
  const vs = ui.picks.map(p => variant(p.cid, p.uid)).filter(Boolean);
  if (vs.length < 2) { ui.view = 'roster'; return renderRoster(); }
  const same = (get) => { const m = {}; vs.forEach(v => { const k = get(v); m[k] = (m[k] || 0) + 1; }); return m; };
  const cC = same(v => v.c), cF = same(v => v.f), cT = same(v => v.t), cI = same(v => v.ins);
  const slots = SLOT_ORDER.filter(sl => vs.some(v => v.skills.some(sk => sk.sl === sl)));
  const car = vs.map(v => cargas(v.skills));
  const syn = synergy(vs), razones = razonesTxt(syn.razones);
  const cell = (v, txt, counts, key) => `<td class="${counts && counts[key] > 1 ? 'same' : ''}">${txt}</td>`;
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
            ${sk.cd ? `<span class="tag dim">CD ${h(sk.cd)}s</span>` : ''}
            ${sk.ult != null ? `<span class="tag dim">${h(t('c_ult'))} ${h(sk.ult)}%</span>` : ''}
            ${sk.stk != null ? `<span class="tag dim">${h(t('c_striker'))} ${h(sk.stk)}%</span>` : ''}
          </div>
          ${dmg.length ? `<div class="muted" style="margin-bottom:5px">${dmg.map(d =>
             `<b>${h(d.pct)}%</b>${d.flat != null ? ' +' + h(d.flat) : ''}`).join(' · ')}</div>` : ''}
          ${otros.slice(0, 6).map(f => `<div class="cmpfx"><span class="fxtag">${h(txt('ab', f.a))}</span>${
             marcadores(h(txt('desc', f.p, f.v).replace(/<br\s*\/?>/gi, ' ')), f)}</div>`).join('')}
          ${otros.length > 6 ? `<div class="muted">+${otros.length - 6}</div>` : ''}</td>`;
      }).join('')}</tr>`).join('')}
    </tbody>
  </table></div>
  <div class="card" style="margin-top:18px">
    <div class="row" style="justify-content:space-between;margin-bottom:8px">
      <h3 style="margin:0">${h(t('cmp_synergy'))}</h3><span class="muted">${syn.score} ${h(t('cmp_pts'))}</span></div>
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
  return (claves || []).map(k => { const f = GUIA.fuentes[k]; if (!f) return '';
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
function efectoSoporteHtml (x) {
  const val = [];
  if (x.v != null) val.push(typeof x.v === 'number' ? h((x.v > 0 ? '+' : '') + x.v + '%') : trHtml(x.v));
  if (x.i != null) val.push(h('+' + x.i + '% ' + t('sp_inst')));
  if (x.tope != null) val.push(h(t('sp_cap') + ' ' + x.tope + '%'));
  if (x.c) val.push(trHtml(x.c));
  if (x.d != null) val.push(h(x.d + ' s'));
  return `<li>${trHtml(x.s)}${val.length ? ` <b>${val.join(' · ')}</b>` : ''}</li>`;
}
function restrHtml (x) {
  if (!x.r) return `<span class="muted">${h(t('sp_all'))}</span>`;
  const [cat, val] = x.r;
  const corr = x.rc ? ` <span class="corr" title="${h(t('sp_corrected') + ' ' + x.rc.join(': '))}">⚠</span>` : '';
  return `<span class="muted">${h(t('sp_applies'))}: ${h(t('sp_r_' + cat))}</span> ${icon(val)}<b>${h(cat === 'Character' ? val : dom(val))}</b>${corr}`;
}
function soporteHtml (tipo, clave, x) {
  const extra = [];
  if (x.ac) extra.push(h(t('sp_act')) + ': ' + trHtml(x.ac));
  if (x.cd) extra.push(h(t('sp_cd') + ' ' + x.cd + ' s'));
  if (x.d) extra.push(h(t('sp_dur') + ' ' + x.d + ' s'));
  if (x.req) extra.push(h(t('sp_req')) + ' ' + trHtml(x.req));
  return `<div class="sop">
    <div class="soph"><span class="slotbadge ${tipo.startsWith('leader') ? 'lead' : 'pass'}">${h(t(clave))}</span>
      ${x.n ? nombreTabla(x.n) : ''}
      ${x.sig ? `<span class="tag solid" style="background:var(--gold)" title="${h(t('sp_notable_t'))}">${h(t('sp_notable'))}</span>` : ''}
      ${x.est ? `<span class="tag dim">${h(t('sp_at6'))}</span>` : ''}</div>
    <div class="sopr">${restrHtml(x)}</div>
    ${categoriasDe(x).length ? `<div class="row sopcats" title="${h(t('ct_title'))}">${categoriasDe(x).map(k =>
      `<span class="tag ghost">${h(t('ct_' + k))}</span>`).join('')}</div>` : ''}
    <ul class="sopfx">${x.fx.map(efectoSoporteHtml).join('')}</ul>
    ${extra.length ? `<div class="muted">${extra.join(' · ')}</div>` : ''}
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
/** Lo que el retrato le da al equipo según thanosvibs (Leads & Supports). */
function usoSoportes (v) {
  const s = SOPORTES[v.p];
  const tipos = s ? TIPOS_SOPORTE.filter(([k]) => s[k]) : [];
  if (!tipos.length) return `<p class="muted">${h(t('us_sup_none'))}</p>`;
  return `${s.np ? `<p><span class="tag solid" style="background:var(--role-soporte)">${h(t('sp_np'))}</span></p>` : ''}
    <div class="sops">${tipos.map(([k, clave]) => soporteHtml(k, clave, s[k])).join('')}</div>
    <p class="muted">${h(bi(GUIA.equipos.pve[1]))}</p>
    <div class="fuentes">${fuentesHtml(['tv-sup', 'tv-guia-4'])}</div>`;
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
  return `${cortes ? `<p class="muted">${h(t('us_cancels'))}</p>${cortes}` : `<p class="muted">${h(t('us_cancels_none'))}</p>`}
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
        return c ? ctpDetalle(c, otraVar(f.vv, v)) : `<div class="row" style="gap:6px"><b>${h(f.r.label)}</b>${otraVar(f.vv, v)}</div>`; }).join('')}</div>`
      : `<p class="muted">${h(t('ar_ctp_nolist'))}</p>`;
  }
  const guia = [...new Set(variantesDe(ch).flatMap(vv => (GUIA_PJ[vv.p] || []).flatMap(e => e.ctps)))];
  return `<p class="muted">${h(li.nombre)}: ${h(bi(li))}</p>${lista}
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
/** Columnas de la guía de armado para los C.T.P. de un equipo, según el tipo de su modo (el ctp de
 *  MODOS) o el orden de las combinaciones: en PvP, el meta y fuera del meta de PvP; en PvE, los de PvE;
 *  sin tipo (sin modo, un modo propio, «puntos para él» o una tier list), el mejor y el segundo. */
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
/** Los C.T.P. que la guía de armado le da a cada integrante de un equipo en las dos columnas de su
 *  tipo de modo (columnasCtp), plegados; el rótulo dice las columnas y la fuente. La fila de la guía
 *  es la de su mejor uniforme: si el integrante lleva otro, se dice. Una columna que no está en su
 *  fila no se completa con otra: dice «sin dato en la guía», como el personaje que no tiene fila. */
function ctpsEquipo (vs, ctx) {
  const cols = columnasCtp(ctx), celda = 'style="white-space:normal;vertical-align:top;padding:4px 10px 4px 0"';
  const sinDato = (titulo) => `<span class="muted"${titulo ? ` title="${h(titulo)}"` : ''}>${h(t('ga_eq_nodata'))}</span>`;
  let otra = false;
  const filas = vs.map(x => {
    const a = armadoDe(x.ch);
    if (!a) return `<tr><th ${celda}>${h(x.name)}</th><td ${celda} colspan="2">${sinDato(t('ga_none'))}</td></tr>`;
    const ov = otraVar(a.vv, x);
    if (ov) otra = true;
    return `<tr><th ${celda}${ov ? ` title="${h(fullLabel(a.vv))}"` : ''}>${h(x.name)} ${ov}</th>${cols.map(k => { const c = (a.e.ctp || []).find(y => y.k === k);
      return `<td ${celda}>${c ? ctpCorto(c) : sinDato('')}</td>`; }).join('')}</tr>`;
  });
  return `<details class="usgrupo ga-eq"><summary>${h(t('ga_eq_title').replace('{a}', t('ga_ctp_' + cols[0])).replace('{b}', t('ga_ctp_' + cols[1])))}</summary>
    <table class="abx" style="table-layout:fixed;width:100%;max-width:640px"><colgroup><col style="width:34%"><col><col></colgroup>
      <thead><tr><th ${celda}></th>${cols.map(k => `<th ${celda}>${h(t('ga_ctp_' + k))}</th>`).join('')}</tr></thead>
      <tbody>${filas.join('')}</tbody></table>
    ${otra ? `<p class="muted">${h(t('ga_eq_other'))}</p>` : ''}
    ${notasCtpArmado()}
    ${fuenteArmado()}</details>`;
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
/** Sets ISO de ataque (PvE) y la nota de piedra que corresponde a su tipo de ataque. */
function armadoISO (ta) {
  const G = GUIA.iso, P = G.piedras, k = ta ? ta.k : null;
  const piedras = k === 'fisico' ? ['roja'] : k === 'energia' ? ['blanca'] : k === 'mixto' ? ['roja', 'blanca'] : [];
  return `<p class="muted">${h(t('ar_iso_pve'))}</p>
    ${G.sets_pve.map(s => `<div class="isoset"><b>${h(s.nombre)}</b> ${piedrasHtml(s.piedras)}
      <div class="muted">${s.stats.map(statNom).join(' · ')}</div></div>`).join('')}
    ${piedras.map(p => `<p>${piedrasHtml([p])} <b>${h(P[p].nombre)}</b>: ${h(bi(P[p]))}</p>`).join('')}
    ${k === 'vida' ? `<p>${h(bi(G.notas_pve[2]))}</p>` : ''}
    <p>${piedrasHtml(['caos'])} <b>${h(P.caos.nombre)}</b>: ${h(bi(P.caos))}</p>
    <p class="muted">${h(bi(G.notas_pve[1]))}</p>
    <p class="muted"><b>PvP:</b> ${h(bi(G.notas_pvp[0]))}</p>
    <div class="fuentes">${fuentesHtml(G.fuente)}</div>`;
}
/** Urus: primero los del tipo de ataque del personaje; después, los topes en orden. */
function armadoUrus (ta) {
  const G = GUIA.urus, k = ta ? ta.k : 'ninguno';
  return `<p><b>${h(t('ar_uru_' + k))}</b></p>
    <p class="muted">${h(bi(G.ataque))}</p>
    <p class="muted">${h(bi(G.prioridad_nota))}</p>
    <ol class="prio">${G.prioridad.map(x => `<li>${h(statNom(x))}</li>`).join('')}</ol>
    <p class="muted"><b>${h(t('md_gear4'))}:</b> ${GUIA.gear4.prioridad.map(x => h(statNom(x))).join(' › ')}. ${h(bi(GUIA.gear4.notas[1]))}</p>
    <div class="fuentes">${fuentesHtml(G.fuente.concat(GUIA.gear4.fuente.filter(x => !G.fuente.includes(x))))}</div>`;
}
/** Artefacto exclusivo: el texto del juego con los valores del nivel de estrellas elegido. */
function armadoArtefacto (ch) {
  const a = ARTES.find(x => x.p === ch.p);
  if (!a) return `<p class="muted">${h(t('ar_art_none'))}</p>`;
  const est = ui.artEst, vals = a.valores[est] || [];
  const linea = (ln) => {
    const es = LANG === 'en' ? ln.t : TXT[ln.t];
    const txt = h(es == null ? ln.t : es).replace(/\[P(\d+)\]/g, (_, n) => vals[n - 1] != null ? `<b>${h(vals[n - 1])}</b>`
      : `<i class="tpl" title="${h(t('ar_nodata_t'))}">${h(t('ar_nodata'))}</i>`);
    return `<div class="artl" style="padding-left:${ln.n * 14}px">${ln.b ? '• ' : ''}${es == null
      ? `<span class="sintrad" title="${h(t('untranslated'))}">${txt}</span>` : txt}</div>`;
  };
  const puntaje = (lbl, n) => `<span class="tag dim" title="${h(t('ar_score_t'))}">${lbl} ${'★'.repeat(n)}${'☆'.repeat(Math.max(0, 3 - n))}</span>`;
  return `<div class="row" style="gap:8px;margin-bottom:6px;flex-wrap:nowrap">${imgUrl('art-' + a.p) ? `<img class="artico" src="${imgUrl('art-' + a.p)}" alt="">` : ''}
      <div><b>${h(a.name)}</b><div class="muted">${h(a.pasiva)} · ${h(t('ar_since'))} ${h(a.desde)}</div></div></div>
    <div class="row" style="gap:6px;margin-bottom:8px">${puntaje('PvE', a.pve)}${puntaje('PvP', a.pvp)}</div>
    <div class="seg" style="margin-bottom:8px">${['3', '4', '5', '6'].map(e => `<button class="${e === est ? 'on' : ''}" data-a="artEst" data-v="${e}">${e}★</button>`).join('')}</div>
    <div class="artlineas">${a.lineas.map(linea).join('')}</div>
    ${a.obtencion.length ? `<details class="usgrupo"><summary>${h(t('ar_obtain'))} (${a.obtencion.length})</summary>
      <ul class="sopfx">${a.obtencion.map(x => `<li>${trHtml(x)}</li>`).join('')}</ul></details>` : ''}
    <div class="fuentes">${fuentesHtml(['tv-art'])}</div>`;
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
  const techo = v.t === 'T2' ? 'n70' : v.t === 'T3' ? 'n80' : 't4';
  const pasos = P.pasos.slice(0, P.pasos.findIndex(p => p.id === techo) + 1);
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
function usoVerificacion (ch, v) {
  const vf = verifDe(ch, v);
  return `<p class="muted">${h(t('vf_resumen').replace('{ok}', vf.ok).replace('{d}', vf.dif.filter(d => d.t === 'dano' || d.t === 'cd').length).replace('{nd}', vf.nd))}</p>
    ${vf.dif.length ? `<ul class="sopfx verif">${vf.dif.map(d => `<li>${verifLinea(d)}</li>`).join('')}</ul>`
                    : `<p>${h(t('vf_sin_dif'))}</p>`}
    <p class="muted">${h(t('vf_nota'))} <a href="docs/AUDITORIA.md" target="_blank" rel="noopener">docs/AUDITORIA.md</a></p>`;
}

function panelUso (ch, v) {
  return `<div class="section uso"><h3>${h(t('us_title'))}</h3>
    <p class="muted" style="margin-bottom:12px">${h(t('us_note'))}</p>
    <div class="usogrid">
      <div class="bloque"><h4>${h(t('us_lists'))}</h4>${usoListas(ch, v)}</div>
      <div class="bloque"><h4>${h(t('us_sup'))}</h4>${usoSoportes(v)}</div>
      <div class="bloque"><h4>${h(t('us_guide'))}</h4>${usoGuia(ch, v)}</div>
      <div class="bloque"><h4>Alliance Battle</h4>${usoABX(ch, v)}</div>
      <div class="bloque"><h4>${h(t('ga_title'))}</h4>${usoArmado(ch, v)}</div>
    </div></div>`;
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

/** Alliance Battle: restricciones de un día del ciclo de 28 y los equipos recomendados,
 *  con qué integrante corta a los jefes (cancels) y con qué skill. */
function panelABX (m) {
  const dia = ui.abxDia;
  const rs = ABX.restricciones.filter(r => r.d === dia);
  const eqs = ABX.equipos.filter(e => e.d === dia);
  const orden = ['Normal', 'Extreme', 'Legend', 'Infinite Challenge'];
  const restr = (r) => r.length ? r.map(x => `<span class="tag dim">${icon(x)}${h(dom(x))}</span>`).join(' ') : `<span class="muted">${h(t('md_no_restr'))}</span>`;
  const cortes = (p, modo) => cortesHtml(p, (m.cancels || {})[modo] || []);
  return `<div class="bloque"><h4>${h(t('md_abx'))}</h4>
    <div class="row" style="margin-bottom:8px"><span class="muted">${h(t('md_day'))}</span>
      <select data-a="abxDia">${Array.from({ length: 28 }, (_, i) => `<option value="${i + 1}" ${i + 1 === dia ? 'selected' : ''}>${i + 1}</option>`).join('')}</select>
      <span class="muted">${h(t('md_day_note'))}</span></div>
    <table class="abx"><tbody>${orden.filter(o => rs.some(r => r.m === o)).map(o => `<tr><th>${h(o)}</th><td>${restr(rs.find(r => r.m === o).r)}</td></tr>`).join('')}</tbody></table>
    ${m.cancels ? `<p class="muted" style="margin:8px 0">${h(bi(m.cancels_nota))} <b>Extreme</b>: ${h(m.cancels.Extreme.map(trTxt).join(', '))} · <b>Legend</b>: ${h(m.cancels.Legend.map(trTxt).join(', '))}.
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
  const vs = tt.members.map(k => variant(...k.split('::'))).filter(Boolean);
  const sc = synergy(vs), modo = modosEquipo().find(m => m.id === tt.modeId);
  return `<div class="card" style="position:relative">
    ${borrable ? `<button class="btn sm danger" data-a="teamRemove" data-id="${tt.id}" style="position:absolute;top:10px;right:10px">✕</button>` : ''}
    <div style="font-weight:600;padding-right:34px;margin-bottom:8px">${h(tt.name)}</div>
    ${modo ? `<div class="row" style="margin-bottom:6px"><span class="tag dim">${h(modo.name)}</span></div>` : ''}
    <div class="row" style="gap:5px;margin-bottom:8px">${vs.map(v => imgUrl('portrait-' + v.id)
      ? `<img src="${imgUrl('portrait-' + v.id)}" title="${h(fullLabel(v))}" style="width:44px;height:44px;border-radius:8px;object-fit:cover">` : '').join('')}</div>
    <div class="muted">${vs.map(fullLabel).join(' + ')}</div>
    ${tt.reason ? `<p class="muted" style="margin-top:6px">${h(tt.reason)}</p>` : ''}
    <div class="muted" style="margin-top:6px">${sc.score} ${h(t('tm_synergy_pts'))} · ${h(sc.lider ? t('eq_leader').replace('{x}', fullLabel(sc.lider)) : t('tm_no_leader'))}</div>
    ${ctpsEquipo(vs, modo ? modo.ctp : null)}
  </div>`;
}
/** Un favorito: equipo de 3 marcado con ★ en las combinaciones de un personaje (el primero). */
function favoritoCard (f) {
  const vs = f.members.map(k => variant(...k.split('::'))).filter(Boolean);
  const sc = synergy(vs);
  return `<div class="card eqsug">
    <div class="row" style="justify-content:space-between;align-items:flex-start">
      <div class="row" style="gap:10px;align-items:flex-start">${estrella(f.members)}${retratosEquipo(vs, vs[0].key)}</div>
      <div class="eqpts"><b>${sc.score}</b> ${h(t('tm_synergy_pts'))}</div>
    </div>
    <div class="muted">${h(vs.map(fullLabel).join(' + '))}</div>
    <div><b>${h(sc.lider ? t('eq_leader').replace('{x}', fullLabel(sc.lider)) : t('tm_no_leader'))}</b></div>
    ${ctpsEquipo(vs, null)}
    <div class="row">${botonArmar(vs, '', '')}</div>
  </div>`;
}
function renderTeams () {
  const eq = ui.team;                 // 't' es la función de idioma: el equipo se llama 'eq'
  const max = tamModo(eq.modeId);
  const modos = modosEquipo();
  const q = ui.teamSearch.trim().toLowerCase();
  const pool = allVariants().filter(v => !q || fullLabel(v).toLowerCase().includes(q)).sort((a, b) => rankIndex(a.key) - rankIndex(b.key));
  const PS = 40, pages = Math.max(1, Math.ceil(pool.length / PS));
  ui.teamPage = Math.min(ui.teamPage, pages - 1);
  const slice = pool.slice(ui.teamPage * PS, (ui.teamPage + 1) * PS);
  // Personajes que ya están en otro equipo de tu cuenta del mismo modo: dentro de un modo no se
  // repiten (por ejemplo, las dos escuadras de Alliance Conquest). Se avisa; no se impide.
  const enModo = new Map();
  if (eq.modeId) U.teams.filter(tt => tt.modeId === eq.modeId)
    .forEach(tt => tt.members.forEach(k => { const cid = k.split('::')[0]; if (!enModo.has(cid)) enModo.set(cid, tt.name); }));
  const repetidos = eq.members.map(k => k.split('::')[0]).filter(cid => enModo.has(cid));
  return `
  <div class="page-head"><div><h1>${h(t('tm_title'))}</h1>
    <div class="sub">${h(t('tm_note'))}</div></div>
    <button class="btn primary" data-a="teamOpen">${h(t('tm_build'))}</button></div>
  ${ui.teamOpen ? `<div class="card" style="margin-bottom:20px">
    <div class="row" style="margin-bottom:10px">
      <input placeholder="${h(t('tm_name_ph'))}" value="${h(eq.name)}" data-a="teamName" style="flex:2;min-width:180px">
      <select data-a="teamMode" style="flex:1;min-width:160px">
        <option value="">${h(t('tm_nomode'))}</option>
        ${[[true, 'tm_modes_game'], [false, 'tm_modes_own']].map(([juego, k]) => { const ms = modos.filter(m => m.juego === juego);
          return ms.length ? `<optgroup label="${h(t(k))}">${ms.map(m => `<option value="${m.id}" ${m.id === eq.modeId ? 'selected' : ''}>${h(m.name)} (${m.tam})</option>`).join('')}</optgroup>` : ''; }).join('')}
      </select>
    </div>
    <div class="muted" style="margin-bottom:6px">${h(t('tm_members'))} ${eq.members.length} / ${max} — ${h(t('tm_sorted_by'))} ${h(listName(listById(U.prefs.refList)) || t('s_name'))}</div>
    ${repetidos.map(cid => `<div class="avisoeq">⚠ ${h(t('tm_dup').replace('{x}', CHAR_BY_ID[cid].name).replace('{e}', enModo.get(cid)))}</div>`).join('')}
    <input placeholder="${h(t('tm_search'))}" value="${h(ui.teamSearch)}" data-a="teamSearch" style="width:100%;margin-bottom:10px">
    <div class="row" style="gap:6px">
      ${slice.map(v => `<div title="${h(fullLabel(v) + (enModo.has(v.cid) ? ' — ' + t('tm_in_use').replace('{e}', enModo.get(v.cid)) : ''))}" data-a="teamToggle" data-key="${v.key}"
        class="${enModo.has(v.cid) && !eq.members.includes(v.key) ? 'enuso' : ''}"
        style="width:50px;height:50px;border-radius:9px;overflow:hidden;cursor:pointer;flex:none;
        box-shadow:0 0 0 ${eq.members.includes(v.key) ? '2px var(--accent)' : '1px var(--line-2)'}">
        ${imgUrl('portrait-' + v.id) ? `<img src="${imgUrl('portrait-' + v.id)}" style="width:100%;height:100%;object-fit:cover" loading="lazy">` : ''}
      </div>`).join('')}
    </div>
    ${pager(pages, ui.teamPage, 'teamPage')}
    <textarea placeholder="${h(t('tm_reason_ph'))}" style="width:100%;margin-top:10px;min-height:54px" data-a="teamReason">${h(eq.reason)}</textarea>
    <div class="row" style="justify-content:flex-end;margin-top:10px">
      <button class="btn" data-a="teamClose">${h(t('tm_cancel'))}</button>
      <button class="btn primary" data-a="teamSave" ${eq.members.length < 2 ? 'disabled' : ''}>${h(t('tm_save'))}</button>
    </div>
  </div>` : ''}
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
  else if (n.error || (NOV.app && NOV.app.error)) estado = `<span class="tag solid" style="background:var(--accent)">${h(t('av_check_err'))}</span> <span class="muted">${h([n.error, NOV.app && NOV.app.error].filter(Boolean).join(' · '))}</span>`;
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
  let body;
  switch (ui.view) {
    case 'detail':   body = renderDetail(); break;
    case 'compare':  body = renderCompare(); break;
    case 'tierlist': body = renderTierList(); break;
    case 'modos':    body = renderModos(); break;
    case 'teams':    body = renderTeams(); break;
    case 'glosario': body = renderGlosario(); break;
    case 'editor':   body = renderEditor(); break;
    case 'settings': body = renderSettings(); break;
    default:         body = renderRoster();
  }
  // Los avisos van fuera de <main>: la barra del roster se pega arriba de main con margen
  // negativo y los taparía.
  $('#app').innerHTML = renderNav() + '<div id="avisos" class="avisos">' + avisosHtml() + '</div><main>' + body + '</main>'
    + (ui.aliados != null ? aliadosModal() : '');
  const q = $('#q');
  if (q && ui.focusSearch) { q.focus(); q.setSelectionRange(q.value.length, q.value.length); }
  sincronizarLugar();
}

// ============================================================================
// HISTORIAL («Atrás»)
// Cada lugar (una vista; en la ficha, un personaje) es una entrada del historial de la
// ventana. Al irse de un lugar queda anotado cómo estaba (uniforme, pestaña, página de las
// combinaciones o del roster, posición y los plegados con id que estaban abiertos, como el «Por
// qué» de una tarjeta), y «Atrás» —el botón de la ficha, Alt+← o el botón de volver del mouse—
// vuelve a ese lugar tal cual. Ir a una skill desde un «Por qué» abre otra entrada aunque sea la
// ficha del mismo personaje (el líder puede ser él).
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
  history.replaceState({ ...previo, y: scrollY, abiertos: [...document.querySelectorAll('main details[open][id]')].map(d => d.id) }, '');
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
  return t({ tierlist: 'nav_tierlists', modos: 'nav_modes', teams: 'nav_teams', glosario: 'nav_glossary', settings: 'nav_settings',
             editor: 'nav_new_char', compare: 'cmp_title' }[d.view] || 'nav_roster');
}
window.addEventListener('popstate', (e) => {
  const s = e.state;
  if (!s || !s.lugar) return;
  Object.assign(ui, { view: s.view, charId: s.charId, uniformId: s.uniformId, fichaTab: s.fichaTab, eqPagina: s.eqPagina,
                      eqCon: s.eqCon, eqVerDescartados: s.eqVerDescartados, page: s.page, tierList: s.tierList,
                      aliados: null, tlPick: null, focusSearch: false, volverY: s.y,
                      volverAbiertos: s.abiertos || [] });   // una entrada anotada por una versión anterior no los trae
  render();
  volverAPosicion();
});
/** Vuelve a la posición anotada, con los plegados que estaban abiertos (cambian el alto de la página;
 *  uno que ya no está, porque la lista cambió, no se abre). Si la pestaña Equipos todavía calcula las
 *  combinaciones, se aplica cuando termina (la lista cambia el alto de la página). */
function volverAPosicion () {
  if (ui.volverY == null || ui.eqCalculando) return;
  for (const id of ui.volverAbiertos) { const d = document.getElementById(id); if (d) d.open = true; }
  window.scrollTo({ top: ui.volverY, behavior: 'instant' });   // sin la animación de html{scroll-behavior}
  ui.volverY = null; ui.volverAbiertos = [];
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
  const el = e.target.closest('[data-a]'); if (!el) return;
  const a = el.getAttribute('data-a'), d = el.dataset;
  const P = U.prefs;
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
      ui.tlPick = null; ui.aliados = null;
      if (ui.pickMode) { togglePick(d.cid, d.uid || null); render(); break; }
      abrirFicha(d.cid, d.uid); break; }
    case 'fichaVecina': abrirFicha(d.cid, d.uid); break;
    // Desde el «Por qué» de una tarjeta de equipo: la skill (o el artefacto) en la ficha de quien la da.
    case 'irSkill': ui.entradaNueva = true; ui.fichaTab = d.tab; abrirFicha(d.cid, d.uid); resaltar(d.ancla); break;
    case 'uniform': ui.uniformId = d.uid; ui.eqPagina = 0; render(); break;
    case 'fichaTab': ui.fichaTab = d.v; render(); irA('fcuerpo'); break;
    case 'verAliados': ui.aliados = parseInt(d.tg, 10); render(); break;
    case 'aliadosCerrar': ui.aliados = null; render(); break;

    case 'goTier': ui.view = 'tierlist'; render(); break;
    case 'goModos': ui.view = 'modos'; render(); break;
    case 'goGlosario': ui.view = 'glosario'; ui.focusSearch = false; render(); break;
    case 'irGlos': {
      // Si la búsqueda deja afuera el destino, se vacía para que aparezca (sin volver a poner el
      // foco en la búsqueda: en el celular abriría el teclado).
      e.preventDefault();
      if (!document.getElementById(d.v)) { ui.glBusca = ''; ui.focusSearch = false; render(); }
      const destino = document.getElementById(d.v);
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
    case 'irVerif': e.preventDefault(); ui.fichaTab = 'mas'; render(); irA('fcuerpo'); break;
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
    case 'teamOpen': ui.teamOpen = true; ui.team = { name:'', members:[], reason:'', modeId:'' }; ui.teamSearch = ''; ui.teamPage = 0; render(); break;
    case 'teamClose': ui.teamOpen = false; render(); break;
    case 'eqIncluir': ui.eqExcluir = ui.eqExcluir.filter(c => c !== d.cid); ui.eqPagina = 0; render(); break;
    // Descartar y restaurar no cambian los datos del juego: sin rebuild(), la consulta queda.
    case 'descartar': if (!estaDescartado(d.c.split(','))) U.descartados.unshift(trioDe(d.c.split(','))); saveUser(); render(); break;
    case 'restaurar': { const k = trioDe(d.c.split(',')).join('|');
      U.descartados = U.descartados.filter(x => x.join('|') !== k); saveUser(); render(); break; }
    case 'eqVerDescartados': ui.eqVerDescartados = !ui.eqVerDescartados; ui.eqPagina = 0; render(); break;
    case 'eqPagina': ui.eqPagina = parseInt(d.p, 10); render(); irA('combos'); break;
    // ★ no cambia los datos del juego: se guarda sin rebuild() para no rehacer la consulta.
    case 'favorito': { const keys = d.m.split(','), c = claveFavorito(keys);
      const i = U.favoritos.findIndex(f => claveFavorito(f.members) === c);
      if (i > -1) U.favoritos.splice(i, 1); else U.favoritos.unshift({ id: 'fav-' + Date.now(), members: keys });
      saveUser(); render(); break; }
    case 'teamDesde': ui.view = 'teams'; ui.teamOpen = true; ui.teamSearch = ''; ui.teamPage = 0;
      ui.team = { name: d.nombre, members: d.m.split(','), reason: '', modeId: d.modo };
      render(); window.scrollTo(0, 0); break;
    case 'teamToggle': { const eq = ui.team, max = tamModo(eq.modeId);
      const i = eq.members.indexOf(d.key);
      if (i > -1) eq.members.splice(i, 1); else { eq.members.push(d.key); if (eq.members.length > max) eq.members.shift(); }
      render(); break; }
    case 'teamPage': ui.teamPage = parseInt(d.p, 10); render(); break;
    case 'teamSave': { const eq = ui.team; if (eq.members.length < 2) break;
      const vs = eq.members.map(k => variant(...k.split('::'))).filter(Boolean);
      U.teams.unshift({ id: 'eq-' + Date.now(), name: eq.name || vs.map(fullLabel).join(' + '),
                        members: eq.members.slice(), reason: eq.reason, modeId: eq.modeId || '' });
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
  if (a === 'teamName') { ui.team.name = el.value; return; }
  if (a === 'teamReason') { ui.team.reason = el.value; return; }
  if (a === 'teamSearch') { ui.teamSearch = el.value; ui.teamPage = 0; render(); return; }
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
  if (a === 'eqExcluir') { if (el.value) ui.eqExcluir = ui.eqExcluir.concat(el.value); ui.eqPagina = 0; render(); return; }
  if (a === 'eqCobertura') { ui.eqCobertura = COBERTURA.map(g => g.k).filter(k => k === d.g ? el.checked : ui.eqCobertura.includes(k));
    ui.eqPagina = 0; render(); return; }
  if (a === 'rowLabel' || a === 'listName') { rebuild(); render(); return; }
  if (a === 'refList') { U.prefs.refList = el.value; commit(); return; }
  if (a === 'objetivo') { U.prefs.objetivo = el.value; ui.page = 0; commit(); return; }
  if (a === 'atributo') { U.prefs.atributo = el.value; ui.page = 0; commit(); return; }
  if (a === 'restr') { U.prefs.restr = el.value; ui.page = 0; commit(); return; }
  if (a === 'teamMode') { ui.team.modeId = el.value; ui.team.members = ui.team.members.slice(-tamModo(el.value)); render(); return; }
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
  if (e.key === 'Escape' && ui.tlPick) { ui.tlPick = null; render(); }
  if (e.key === 'Escape' && ui.aliados != null) { ui.aliados = null; render(); }
  // En la ficha, ← y → pasan al anterior y al siguiente del listado (no mientras se escribe).
  if ((e.key === 'ArrowLeft' || e.key === 'ArrowRight') && ui.view === 'detail' && ui.aliados == null
      && !e.target.closest('input, select, textarea') && !e.altKey && !e.ctrlKey && !e.metaKey) {
    const ch = CHAR_BY_ID[ui.charId], v = ch && variant(ch.id, ui.uniformId);
    const x = v && vecinosEnListado(v)[e.key === 'ArrowLeft' ? 'prev' : 'next'];
    if (x) { e.preventDefault(); abrirFicha(x.cid, x.uid); }
  }
});

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
  BONOS_DE = {};
  for (const b of BONOS) {
    const bono = { n: b.n, m: b.m, f: b.f, vs: b.v.map(v => ({ fx: v.map(([s, x]) => ({ s, v: x })) })) };
    for (const c of b.m) (BONOS_DE[c] = BONOS_DE[c] || []).push(bono);
  }
  STRIKERS_DE = {};
  for (const [cid, filas] of Object.entries(STRIKERS)) for (const [x, p, cuando] of filas) (STRIKERS_DE[x] = STRIKERS_DE[x] || []).push([cid, p, cuando]);
  GL_DE = Object.fromEntries(CATALOGO.efectos.map(e => [e.id, { e, terminos: [], etiquetas: [] }]));
  for (const x of GLOSARIO.terminos) for (const id of x.efectos) GL_DE[id].terminos.push(x);
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
