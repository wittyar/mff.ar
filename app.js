/* TA GUIANAEL MFF — app standalone en JS vanilla. Sin build: corre desde file:// o cualquier host estático.
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
const SKILLS         = window.MFF_SKILLS || {};   // skills por retrato
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
const LS_KEY = 'mff_user_v1';
function blankUser () {
  return {
    charEdits: {},                    // id de data.js -> personaje editado (reemplaza al del seed)
    charNew: [],                      // personajes creados a mano
    teams: [],
    lists: [],                        // tier lists propias: {id,name,rows}
    assign: {},                       // listId -> {clave: [filaId, ...] | null}
    images: {},                       // 'portrait-x' / 'fullbody-x' / 'brand-logo' subidos
    marcas: {},                       // '<retrato>::<tipo de skill>' -> {it:1, gb:1, ...}
    modes: [],                        // modos propios: {id, name, teamSize}; los del juego salen de MFF_MODOS
    prefs: { lang:'es', view:'grid', sort:'name', dir:1, filtersOpen:false, refList: (TIERLISTS_SEED[0]||{}).id || '',
             kind:'todo', objetivo:'', atributo:'', filters:{ c:[], r:[], t:[], f:[], ins:[], race:[], origin:[], ab:[] },
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
 *  estar en varias filas de la misma lista: muchas listas son por categoría. */
function filasDe (listId, key) { return assignOf(listId)[key] || []; }
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
  ar_note:           { es:'El C.T.P. que le asignan las fuentes, su artefacto y las reglas generales de la guía aplicadas a su tipo de ataque.',
                       en:'The C.T.P. the sources assign it, its artifact and the guide’s general rules applied to its attack type.' },
  ar_more:           { es:'Reglas completas en Modos ↓', en:'Full rules in Modes ↓' },
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
  nav_new_char:      { es:'+ Personaje',         en:'+ Character' },
  nav_settings:      { es:'Ajustes',             en:'Settings' },

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
  c_worldboss:       { es:'World Boss',          en:'World Boss' },
  c_skills:          { es:'Skills',              en:'Skills' },
  c_list:            { es:'Lista',               en:'List' },
  base:              { es:'Base',                en:'Base' },
  transcended_tag:   { es:'TRASCENDIDO',         en:'TRANSCENDED' },
  new_tag:           { es:'NUEVO',               en:'NEW' },

  back_roster:       { es:'← Roster',            en:'← Roster' },
  compare_this:      { es:'+ Comparar esta versión', en:'+ Compare this version' },
  edit:              { es:'Editar',              en:'Edit' },
  d_current_uniform: { es:'Uniforme actual',     en:'Current uniform' },
  d_race:            { es:'Raza',                en:'Race' },
  d_gender:          { es:'Género',              en:'Gender' },
  d_origin:          { es:'Origen',              en:'Origin' },
  d_cost:            { es:'Costo del uniforme',  en:'Uniform cost' },
  d_uniforms:        { es:'Uniformes',           en:'Uniforms' },
  d_abilities:       { es:'Habilidades:',        en:'Abilities:' },
  d_tuc:             { es:'Cartas TUC:',         en:'TUC cards:' },
  d_uni_section:     { es:'Uniformes',           en:'Uniforms' },
  d_uni_note:        { es:'Cada uniforme tiene su propio set completo de skills; elegí uno para verlo.',
                       en:'Each uniform has its own complete skill set; pick one to see it.' },
  d_uni_noskills:    { es:'Este uniforme no tiene skills propias en la wiki.',
                       en:'This uniform has no skills of its own on the wiki.' },
  d_no_skills:       { es:'La wiki no publica skills para este personaje todavía.',
                       en:'The wiki does not publish skills for this character yet.' },
  d_teams:           { es:'Equipos donde aparece', en:'Teams it appears in' },
  d_portraits:       { es:'Retratos propios',    en:'Custom portraits' },
  d_portraits_note:  { es:'Si subís una imagen reemplaza la de thanosvibs solo en este navegador.',
                       en:'Uploading an image replaces the thanosvibs one in this browser only.' },
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
  cmp_heuristic:     { es:'Heurística propia (bando, cobertura de roles y ventaja de clase), no un cálculo del juego.',
                       en:'Our own heuristic (side, role coverage and class advantage), not a game calculation.' },
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

  ed_edit:           { es:'Editar personaje',    en:'Edit character' },
  ed_new:            { es:'Nuevo personaje',     en:'New character' },
  ed_note:           { es:'Se guarda en tu navegador, aparte de data.js. Regenerar los datos no lo pisa.',
                       en:'Saved in your browser, separate from data.js. Regenerating the data does not overwrite it.' },
  ed_step_data:      { es:'Datos',               en:'Details' },
  ed_step_unis:      { es:'Uniformes',           en:'Uniforms' },
  ed_step_review:    { es:'Revisar',             en:'Review' },
  ed_name:           { es:'Nombre',              en:'Name' },
  ed_striker:        { es:'Striker (número de skill)', en:'Striker (skill number)' },
  ed_uni_name:       { es:'Nombre del uniforme', en:'Uniform name' },
  ed_cost:           { es:'Costo',               en:'Cost' },
  ed_add_skill:      { es:'+ Skill',             en:'+ Skill' },
  ed_add_uni:        { es:'+ Agregar uniforme',  en:'+ Add uniform' },
  ed_skill_name:     { es:'Nombre',              en:'Name' },
  ed_desc:           { es:'Descripción',         en:'Description' },
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
  st_sources_txt:    { es:'Personajes, uniformes, retratos, íconos y tier lists: ',
                       en:'Characters, uniforms, portraits, icons and tier lists: ' },
  st_sources_txt2:   { es:'. Skills e instintos: ', en:'. Skills and instincts: ' },
  st_sources_txt3:   { es:'. Uso personal, sin fin comercial.', en:'. Personal use, non-commercial.' },
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
  c_ult:             { es:'Ult',                 en:'Ult' },
  c_striker:         { es:'Striker',             en:'Striker' },
  c_cooldown:        { es:'Recarga',             en:'Cooldown' },
  every:             { es:'cada',                en:'every' },
  permanent_fx:      { es:'permanente',          en:'permanent' },
  team_fx:           { es:'al equipo',           en:'team' },
  c_keybuffs:        { es:'Buffs clave',         en:'Key buffs' },
  c_uni_cost:        { es:'Costo de mejora',     en:'Upgrade cost' },
  c_dmg_total:       { es:'Daño total de activas', en:'Total active damage' },
  d_upgrade:         { es:'Mejora del uniforme', en:'Uniform upgrade' },
  d_kits:            { es:'Kits',                en:'Kits' },
  d_gold:            { es:'Oro',                 en:'Gold' },
  d_xp:              { es:'XP',                  en:'XP' },
  d_materials:       { es:'Materiales',          en:'Materials' },
  f_effect:          { es:'Efecto',              en:'Effect' },
  tpl_title:         { es:'La fuente no especifica cuál: publica un marcador de plantilla sin resolver.',
                       en:'The source does not say which: it publishes an unresolved template marker.' },
  tpl_faction:       { es:'sin especificar',      en:'unspecified' },
  tpl_class:         { es:'sin especificar',      en:'unspecified' },
  tpl_time:          { es:'sin especificar',      en:'unspecified' },
  c_targets:         { es:'Beneficia a',          en:'Buffs' },
  c_attrs:           { es:'Atributos marcados',   en:'Marked attributes' },
  f_attrs:           { es:'Atributo marcado por vos', en:'Attribute you marked' },
  at_edit:           { es:'Marcar atributos',     en:'Mark attributes' },
  at_done:           { es:'Listo',                en:'Done' },
  at_mark:           { es:'Marcar:',              en:'Mark:' },
  st_marks:          { es:'Skills con marcas',    en:'Skills with marks' },
  f_targets:         { es:'Beneficia a (buffs de equipo)', en:'Buffs (team-wide effects)' },
  f_any_target:      { es:'— cualquiera —',        en:'— any —' },
  sy_title:          { es:'Sincronización',       en:'Sync' },
  sy_go:             { es:'Sincronizar',          en:'Sync now' },
  sy_note:            { es:'Baja los datos de thanosvibs y regenera el snapshot local. La página se recarga sola al terminar.',
                        en:'Downloads the data from thanosvibs and rebuilds the local snapshot. The page reloads when it finishes.' },
  sy_local:           { es:'Datos locales',         en:'Local data' },
  sy_remote:          { es:'Última versión publicada', en:'Latest published version' },
  sy_snapshot:        { es:'snapshot',              en:'snapshot' },
  sy_uptodate:        { es:'Estás al día.',         en:'You are up to date.' },
  sy_outdated:        { es:'Hay una versión más nueva del juego que la de tus datos.',
                        en:'There is a newer game version than the one in your data.' },
  sy_unknown:         { es:'No se pudo consultar la versión publicada.',
                        en:'Could not check the published version.' },
  sy_data:            { es:'Actualizar datos del juego', en:'Update game data' },
  sy_data_note:       { es:'Personajes, uniformes, skills y costos. Tarda unos minutos.',
                        en:'Characters, uniforms, skills and costs. Takes a few minutes.' },
  sy_tier:            { es:'Actualizar tier lists',  en:'Update tier lists' },
  sy_tier_note:       { es:'Todas las listas públicas de thanosvibs. Es rápido.',
                        en:'Every public thanosvibs list. Quick.' },
  sy_img:             { es:'Bajar retratos que falten', en:'Download missing portraits' },
  sy_img_note:        { es:'Solo los que no estén en images/. La primera vez son 56 MB.',
                        en:'Only the ones missing from images/. The first time it is 56 MB.' },
  sy_running:         { es:'Sincronizando…',        en:'Syncing…' },
  sy_done:            { es:'Listo. Recargando…',    en:'Done. Reloading…' },
  sy_failed:          { es:'Falló la sincronización', en:'Sync failed' },
  sy_busy:            { es:'Ya hay una sincronización en curso.', en:'A sync is already running.' },
  sy_needdata:        { es:'Primero hay que actualizar los datos del juego: las tier lists se arman sobre ellos.',
                        en:'Update the game data first: the tier lists are built on top of it.' },
  sy_offline:         { es:'Sincronización disponible solo en la app de escritorio',
                        en:'Sync is available only in the desktop app' },
  sy_offline_note:    { es:'Estás viendo el HTML suelto. thanosvibs no habilita CORS, así que el navegador no puede bajar los datos por su cuenta: hace falta abrir la app con MFF.bat.',
                        en:'You are viewing the plain HTML. thanosvibs does not enable CORS, so the browser cannot fetch the data on its own: open the app with MFF.bat.' },
  lang_switch:       { es:'English',             en:'Español' },
  lang_title:        { es:'Ver la app en inglés', en:'View the app in Spanish' },
  untranslated:      { es:'sin traducir',        en:'untranslated' },
  fx_general:        { es:'General',             en:'General' },
  fx_self:           { es:'A sí mismo',          en:'Self' },
  fx_enemy:          { es:'Al oponente',         en:'Enemy' },
  fx_allies:         { es:'Al equipo',           en:'Allies' },
  timing_permanent:  { es:'Permanente',          en:'Permanent' },
  timing_ultimate:   { es:'Barra de habilidad llena', en:'Skill gauge full' },
  timing_cd:         { es:'s de recarga',        en:'s cooldown' },
  ignores_iframe:    { es:'Ignora iframe',       en:'Ignores iframe' },
  has_iframe:        { es:'Tiene iframe',        en:'Has iframe' },
  page_prev:         { es:'←',                   en:'←' },
  page_next:         { es:'→',                   en:'→' }
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
// Cuando la app corre servida por desktop/servidor.py, ese proceso puede llamar a
// thanosvibs (el navegador no: la API no manda Access-Control-Allow-Origin). Se
// detecta preguntandole al servidor; si no contesta, es el HTML suelto.
// ---------------------------------------------------------------------------
let ESCRITORIO = null;               // respuesta de /api/estado, o null
let SYNC = { progreso: null, poll: null };
async function apiLocal (ruta, metodo) {
  const r = await fetch(ruta, { method: metodo || 'GET', headers: { 'X-MFF': '1' } });
  const cuerpo = await r.json();
  if (!r.ok) throw new Error(cuerpo.error || ('HTTP ' + r.status));
  return cuerpo;
}
async function detectarEscritorio () {
  // Desde file:// no hay servidor al que preguntarle, y fetch tira un error de consola
  // que no aporta nada. Se sale antes.
  if (location.protocol === 'file:') return;
  try {
    const e = await apiLocal('/api/estado');
    if (e && e.app === 'mff-escritorio') { ESCRITORIO = e; render(); }
  } catch (e) { ESCRITORIO = null; }
}
function pollProgreso () {
  clearInterval(SYNC.poll);
  SYNC.poll = setInterval(async () => {
    try {
      const p = await apiLocal('/api/progreso');
      SYNC.progreso = p;
      if (p.terminado) {
        clearInterval(SYNC.poll); SYNC.poll = null;
        if (!p.error) { try { sessionStorage.setItem('mff_volver', 'settings'); } catch (e) {}
                        setTimeout(() => location.reload(), 1200); }
      }
      if (ui.view === 'settings') render();
    } catch (e) { clearInterval(SYNC.poll); SYNC.poll = null; }
  }, 1500);
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
  modoFiltro: 'todos', modoAbierto: null, abxDia: 1,
  artEst: '6'                        // nivel de estrellas que muestra el artefacto de la ficha
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
                   c: ch.c, f: ch.f, t: ch.t, ins: ch.ins, r: ch.r, ab: ch.abilities || [],
                   striker: ch.striker, wba: ch.wba, trans: ch.trans, nuevo: ch.new, cost: '',
                   p, up: null, ch, skills };
  return { cid: ch.id, uid: u.id, key: ch.id + '::' + u.id, id: u.id, name: ch.name, sub: u.name,
           c: u.c || ch.c, f: u.f || ch.f, t: u.tier || ch.t, ins: ch.ins, r: ch.r, ab: u.ab || ch.abilities || [],
           striker: u.striker != null ? u.striker : ch.striker, wba: u.wba || ch.wba,
           trans: u.trans, nuevo: u.new, cost: u.cost || '',
           p, up: u.up || null, ch, skills };
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

/** Heurística propia: bando compartido, cobertura de roles y ventaja de clase. No sale del juego. */
function synergy (vs) {
  if (vs.length < 2) return { score: 0, reasons: [] };
  const reasons = []; let score = 0;
  const ES = LANG === 'es';
  if (vs.every(v => v.f === vs[0].f)) { score += 2;
    reasons.push(ES ? 'Mismo bando (' + dom(vs[0].f) + '): bonos de equipo activos.'
                    : 'Same side (' + dom(vs[0].f) + '): team bonuses active.'); }
  const roles = new Set(vs.flatMap(v => v.r));
  const covered = ['Tanque','Control','Daño','Soporte'].filter(r => roles.has(r));
  if (covered.length >= 2) { score += covered.length;
    reasons.push((ES ? 'Roles cubiertos: ' : 'Roles covered: ') + covered.map(dom).join(' + ') + '.'); }
  const classes = new Set(vs.map(v => v.c));
  if (classes.size === vs.length) { score += 1;
    reasons.push(ES ? 'Clases distintas: no comparten la misma debilidad.'
                    : 'Different classes: they do not share the same weakness.'); }
  vs.forEach(a => vs.forEach(b => {
    if (a !== b && SEED.CLASS_ADVANTAGE[a.c] === b.c) {
      score += 1;
      reasons.push(ES ? fullLabel(a) + ' (' + dom(a.c) + ') cubre la debilidad de clase de ' + fullLabel(b) + '.'
                      : fullLabel(a) + ' (' + dom(a.c) + ') covers the class weakness of ' + fullLabel(b) + '.');
    }
  }));
  return { score, reasons: [...new Set(reasons)] };
}

// ---------------------------------------------------------------------------
// TEXTO DE LAS SKILLS
// Un efecto guarda el índice de su patrón y sus números; el texto se arma acá.
// ---------------------------------------------------------------------------
/** Fila de una tabla de data.js. */
function fila (tabla, i) { return (i == null || !TB[tabla]) ? null : TB[tabla][i]; }
// thanosvibs publica algunas descripciones con marcadores de plantilla sin resolver
// ($HEROSUBTYPE1, $HEROCLASS2, $TIME). Los que tienen un campo real detrás se resuelven
// con ese campo; los que no, se marcan como "sin especificar en la fuente" en vez de
// inventarles un valor o dejar el marcador crudo a la vista.
function marcadores (texto, f) {
  const chip = (clave) => `<i class="tpl" title="${h(t('tpl_title'))}">${h(t(clave))}</i>`;
  return texto
    .replace(/\$TIME/g, () => (f && f.d != null) ? f.d + ' s' : chip('tpl_time'))
    .replace(/\$TICK/g, () => (f && f.t != null) ? f.t + ' s' : chip('tpl_time'))
    .replace(/\$HEROSUBTYPE\d*/g, () => chip('tpl_faction'))
    .replace(/\$HEROCLASS\d*/g, () => chip('tpl_class'));
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
  if (esAjeno(tgComun)) cabecera.push(`<span class="tag objetivo">→ ${h(txt('tgt', tgComun))}</span>`);
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
    if (st.tg != null && st.tg !== tgComun) meta.push(`<span class="stmeta">${h(t('st_target'))}: ${h(txt('tgt', st.tg))}</span>`);
    if (!fx.length && !meta.length) return '';
    return `<div class="stageblock">
      ${varias || meta.length ? `<div class="stagehead">${varias ? `<span class="stnum">${i + 1}</span>` : ''}${meta.join('')}</div>` : ''}
      ${fx.map(efectoLinea).join('')}</div>`;
  }).join('');

  const cargas = [];
  if (sk.cd) cargas.push(`<span class="tag dim">CD ${h(sk.cd)}s</span>`);
  if (sk.ult != null) cargas.push(`<span class="tag dim">${h(t('c_ult'))} ${h(sk.ult)}%</span>`);
  if (sk.stk != null) cargas.push(`<span class="tag dim">${h(t('c_striker'))} ${h(sk.stk)}%</span>`);

  return `<div class="skill">
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
    if (P.objetivo !== '' && !objetivosDe(v.skills).has(Number(P.objetivo))) return false;
    if (P.atributo !== '' && !atributosDe(v.p, v.skills).has(P.atributo)) return false;
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
  const active = Object.values(F).reduce((n, a) => n + a.length, 0) + Object.values(G).filter(Boolean).length
               + (P.objetivo !== '' ? 1 : 0) + (P.atributo !== '' ? 1 : 0);
  // El valor que viaja en data-v es siempre el del snapshot (español): el idioma solo
  // cambia lo que se ve, nunca la clave con la que se filtra ni la del ícono.
  const group = (clave, cat, values) => `<div class="filtergroup"><div class="lbl">${h(t(clave))}</div><div class="row">${
    values.map(v => `<button class="chip ${F[cat].includes(v) ? 'on' : ''}" data-a="filter" data-cat="${cat}" data-v="${h(v)}">${icon(v)}${h(dom(v))}</button>`).join('')
  }</div></div>`;
  return `<div class="toolbar">
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
      ${group('f_ability','ab',SEED.SKILL_TAGS)}
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
          <div><div style="font-weight:600">${h(v.uid ? v.sub : v.name)}</div>${v.uid ? `<div class="muted" style="font-size:11.5px">${h(v.name)}</div>` : `<div class="muted" style="font-size:11.5px">${h(t('base'))}</div>`}</div></div></td>
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
  return toolbar(total, rows.length) + body + pager(pages) +
    (ui.pickMode && ui.picks.length >= 2
      ? `<div style="position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:center;padding:16px;
           background:linear-gradient(to top,var(--bg) 62%,transparent);z-index:50">
           <button class="btn primary" data-a="goCompare">${h(t('compare'))} ${ui.picks.length} →</button></div>` : '');
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
function statLabel (k) { return LANG === 'es' ? (STAT_ES[k] || k) : dom(k); }
function renderDetail () {
  const ch = CHAR_BY_ID[ui.charId];
  if (!ch) { ui.view = 'roster'; return renderRoster(); }
  const v = variant(ch.id, ui.uniformId);
  const rank = rankLabel(v.key);
  const stats = Object.entries(ch.stats || {}).filter(([, val]) => parseFloat(val) !== 0);
  const teams = U.teams.filter(eq => eq.members.some(k => k.split('::')[0] === ch.id));
  const car = cargas(v.skills);
  const box = (k, val) => `<div class="stat"><div class="k">${h(k)}</div><div class="v">${val}</div></div>`;

  return `
  <div class="row" style="margin-bottom:14px">
    <button class="btn sm" data-a="back">${h(t('back_roster'))}</button>
    <button class="btn sm" data-a="pickThis" data-cid="${ch.id}" data-uid="${v.uid || ''}">${h(t('compare_this'))}</button>
    <button class="btn sm" data-a="edit" data-cid="${ch.id}">${h(t('edit'))}</button>
    <button class="btn sm ${ui.marcando ? 'primary' : ''}" data-a="marcarModo">${h(ui.marcando ? t('at_done') : t('at_edit'))}</button>
  </div>
  <div class="hero">
    <div class="glow" style="background:radial-gradient(60% 120% at 12% 0%, ${classColor(v.c)}22, transparent 70%)"></div>
    <div class="inner">
      <div class="face">${shot(v.id)}</div>
      <div class="meta">
        <h1>${h(ch.name)}</h1>
        ${rank ? `<div class="row"><span class="muted">${h(listName(listById(U.prefs.refList)))}:</span>
          <span class="tag solid" style="background:${rank.color}" title="${h(rank.todas.join(' · '))}">${h(rankTexto(rank))}</span></div>` : ''}
        <div class="row">
          ${tagGhost(dom(v.c), classColor(v.c))}
          ${tagSolid(v.t, tierColor(v.t))}${v.trans ? tagSolid(t('transcended_tag'), 'var(--gold)') : ''}
          <span class="tag dim">${h(dom(v.f))}</span>
          ${insTag(v.ins)}
          ${v.nuevo ? tagSolid(t('new_tag'),'var(--gold)') : ''}
          ${v.r.map(r => `<span class="tag ghost" style="color:${roleColor(r)}">${h(dom(r))}</span>`).join('')}
        </div>
        <div class="statgrid">
          ${box(t('d_current_uniform'), h(v.uid ? v.sub : t('base')))}
          ${box(t('d_race'), icon(ch.race) + h(dom(ch.race) || '—'))}
          ${box(t('d_gender'), icon(ch.gender) + h(dom(ch.gender) || '—'))}
          ${box(t('d_origin'), h(dom(ch.origin) || '—'))}
          ${box(t('c_striker'), v.striker != null ? 'Skill ' + h(v.striker) : '—')}
          ${box(t('c_worldboss'), icon(v.wba) + h(dom(v.wba) || '—'))}
          ${box(t('us_atk'), ataqueHtml(tipoAtaque(v.skills)))}
          ${v.cost ? box(t('d_cost'), h(v.cost)) : ''}
          ${box(t('d_uniforms'), h(String(ch.uniforms.length)))}
          ${stats.map(([k, val]) => box(statLabel(k), h(val))).join('')}
        </div>
        <div class="row">
          <span class="muted">${h(t('d_abilities'))}</span>
          ${(v.ab || []).map(a => `<span class="tag dim">${icon(a)}${h(dom(a))}</span>`).join('') || '<span class="muted">—</span>'}
        </div>
        ${(ch.tuc || []).length ? `<div class="row"><span class="muted">${h(t('d_tuc'))}</span>${ch.tuc.map(x => `<span class="tag dim">${h(x)}</span>`).join('')}</div>` : ''}
      </div>
    </div>
  </div>

  ${panelUso(ch, v)}
  ${panelArmado(ch, v)}

  <div class="section">
    <h3>${h(t('d_uni_section'))} · ${pluralUni(ch.uniforms.length)}</h3>
    <div class="unitabs">
      <button class="unitab ${v.uid ? '' : 'on'}" data-a="uniform" data-uid="base">
        ${imgUrl('portrait-' + ch.id) ? `<img src="${imgUrl('portrait-' + ch.id)}" alt="">` : ''}${h(t('base'))}</button>
      ${ch.uniforms.map(u => `<button class="unitab ${v.uid === u.id ? 'on' : ''}" data-a="uniform" data-uid="${u.id}">
        ${imgUrl('portrait-' + u.id) ? `<img src="${imgUrl('portrait-' + u.id)}" alt="">` : ''}${h(u.name)}
        <span class="tag solid" style="background:${tierColor(u.tier)};font-size:9px">${h(u.tier)}</span></button>`).join('')}
    </div>
    <p class="muted" style="margin-bottom:12px">${h(t('d_uni_note'))}
</p>
    ${(() => { const kb = BUFFS[v.p] || {}; const ks = Object.keys(kb);
       return ks.length ? `<div class="keybuffs">
         <div class="kbhead">${h(t('c_keybuffs'))}</div>
         ${ks.map(k => `<div class="kbrow"><span class="kbname">${h(k)}</span>
            <span class="kbsrc">${kb[k].map(x => `<span class="tag dim">${h(slotEs(x === 'Leader Skill' ? 'Leader Skill' : x))}</span>`).join('')}</span></div>`).join('')}
       </div>` : ''; })()}
    ${v.skills.length
      ? `<div class="chargebar">
           <span>${h(t('c_ult'))}</span><div class="bar"><i style="width:${Math.min(100, car.ult)}%;background:var(--accent)"></i></div><b>${car.ult}%</b>
           <span>${h(t('c_striker'))}</span><div class="bar"><i style="width:${Math.min(100, car.stk)}%;background:var(--role-control)"></i></div><b>${car.stk}%</b>
         </div>` + v.skills.map(sk => skillCard(sk, v.p)).join('')
      : `<div class="empty"><div class="big">?</div><div>${h(t('d_no_skills'))}</div></div>`}
  </div>

  ${teams.length ? `<div class="section"><h3>${h(t('d_teams'))}</h3><div class="grid">
    ${teams.map(eq => `<div class="card"><div style="font-weight:600">${h(eq.name)}</div>
      <div class="muted">${eq.members.map(k => { const r = variant(...k.split('::')); return r ? fullLabel(r) : k; }).join(' + ')}</div>
      <p class="muted" style="margin-top:6px">${h(eq.reason)}</p></div>`).join('')}
  </div></div>` : ''}

  <div class="section"><h3>${h(t('d_portraits'))}</h3>
    <p class="muted" style="margin-bottom:10px">${h(t('d_portraits_note'))}</p>
    <div class="row">
      <label class="btn sm" style="cursor:pointer">${h(t('d_upload'))}<input type="file" accept="image/*" hidden data-a="upload" data-img="portrait-${v.id}"></label>
      ${U.images['portrait-' + v.id] ? `<button class="btn sm danger" data-a="clearImg" data-img="portrait-${v.id}">${h(t('d_revert_img'))}</button>` : ''}
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
  const slots = SLOT_ORDER.filter(sl => vs.some(v => v.skills.some(sk => sk.sl === sl)));
  const car = vs.map(v => cargas(v.skills));
  const syn = synergy(vs);
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
        return `<td>${o.length ? o.map(i => `<span class="tag objetivo">${h(txt('tgt', i))}</span>`).join(' ')
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
          ${esAjeno(tgC) ? `<div class="row" style="margin-bottom:5px"><span class="tag objetivo">→ ${h(txt('tgt', tgC))}</span></div>` : ''}
          ${acC != null ? `<div class="muted" style="margin-bottom:5px">${h(t('st_activation'))}: ${h(txt('act', acC, (sk.st.find(x => x.ac === acC) || {}).av))}</div>` : ''}
          ${(sk.st || []).some(st => st.tg != null && st.tg !== tgC)
            ? `<div class="muted" style="margin-bottom:5px">${(sk.st || []).filter(st => st.tg != null && st.tg !== tgC)
                .map((st, i) => `${h(t('st_stage'))} ${(sk.st.indexOf(st) + 1)}: ${h(txt('tgt', st.tg))}`).join(' · ')}</div>` : ''}
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
    ${syn.reasons.length ? `<ul style="margin:0;padding-left:18px">${syn.reasons.map(r => `<li>${h(r)}</li>`).join('')}</ul>`
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
const TXT    = window.MFF_TXT || {};
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
/** Chips con las fuentes citadas, cada una con su enlace. */
function fuentesHtml (claves) {
  return (claves || []).map(k => { const f = GUIA.fuentes[k]; if (!f) return '';
    return `<a class="fuente" href="${h(f.url)}" target="_blank" rel="noopener" title="${h(t('md_source'))}">${h(f.nombre)}</a>`; }).join('');
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
function tipoAtaque (skills) {
  const suma = {};
  skills.forEach(sk => { if (!/^Active/.test(sk.sl)) return;
    (sk.st || []).forEach(st => (st.fx || []).forEach(f => { const d = dano(f); if (d && d.pct) suma[d.src] = (suma[d.src] || 0) + d.pct; })); });
  const total = Object.values(suma).reduce((a, b) => a + b, 0);
  if (!total) return null;
  const reparto = Object.entries(suma).sort((a, b) => b[1] - a[1])
    .map(([src, n]) => ({ src, k: SRC_ATAQUE[src], pct: Math.round(n * 100 / total) }));
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
    <ul class="sopfx">${x.fx.map(efectoSoporteHtml).join('')}</ul>
    ${extra.length ? `<div class="muted">${extra.join(' · ')}</div>` : ''}
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
    <div class="fuentes">${fuentesHtml(li.fuente.concat(['tv-guia-1', 'tv-guia-2', 'tv-ctps']))}</div>`;
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
function panelArmado (ch, v) {
  const ta = tipoAtaque(v.skills);
  return `<div class="section"><h3>${h(t('ar_title'))}</h3>
    <p class="muted" style="margin-bottom:12px">${h(t('ar_note'))}
      <a href="#armado" data-a="irArmadoModos">${h(t('ar_more'))}</a></p>
    <div class="usogrid">
      <div class="bloque"><h4>C.T.P.</h4>${armadoCTP(ch, v)}</div>
      <div class="bloque"><h4>${h(t('ar_art'))}</h4>${armadoArtefacto(ch)}</div>
      <div class="bloque"><h4>ISO-8</h4>${armadoISO(ta)}</div>
      <div class="bloque"><h4>${h(t('md_urus'))}</h4>${armadoUrus(ta)}</div>
    </div></div>`;
}

function panelUso (ch, v) {
  return `<div class="section uso"><h3>${h(t('us_title'))}</h3>
    <p class="muted" style="margin-bottom:12px">${h(t('us_note'))}</p>
    <div class="usogrid">
      <div class="bloque"><h4>${h(t('us_lists'))}</h4>${usoListas(ch, v)}</div>
      <div class="bloque"><h4>${h(t('us_sup'))}</h4>${usoSoportes(v)}</div>
      <div class="bloque"><h4>${h(t('us_guide'))}</h4>${usoGuia(ch, v)}</div>
      <div class="bloque"><h4>Alliance Battle</h4>${usoABX(ch, v)}</div>
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
      ${eq ? `<span class="tag dim">${h(t('md_team'))} ${eq.tam}</span>` : ''}
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
 *  propios. {id, name, tam}. */
function modosEquipo () {
  return MODOS.filter(m => m.equipo && m.equipo.tam).map(m => ({ id: m.id, name: m.nombre, tam: m.equipo.tam, juego: true }))
    .concat(U.modes.map(m => ({ id: m.id, name: m.name, tam: m.teamSize, juego: false })));
}
function tamModo (id) { const m = modosEquipo().find(x => x.id === id); return m ? m.tam : 3; }
function renderTeams () {
  const eq = ui.team;                 // 't' es la función de idioma: el equipo se llama 'eq'
  const max = tamModo(eq.modeId);
  const modos = modosEquipo();
  const q = ui.teamSearch.trim().toLowerCase();
  const pool = allVariants().filter(v => !q || fullLabel(v).toLowerCase().includes(q)).sort((a, b) => rankIndex(a.key) - rankIndex(b.key));
  const PS = 40, pages = Math.max(1, Math.ceil(pool.length / PS));
  ui.teamPage = Math.min(ui.teamPage, pages - 1);
  const slice = pool.slice(ui.teamPage * PS, (ui.teamPage + 1) * PS);
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
    <input placeholder="${h(t('tm_search'))}" value="${h(ui.teamSearch)}" data-a="teamSearch" style="width:100%;margin-bottom:10px">
    <div class="row" style="gap:6px">
      ${slice.map(v => `<div title="${h(fullLabel(v))}" data-a="teamToggle" data-key="${v.key}"
        style="width:50px;height:50px;border-radius:9px;overflow:hidden;cursor:pointer;flex:none;
        box-shadow:0 0 0 ${eq.members.includes(v.key) ? '2px var(--accent)' : '1px var(--line-2)'}">
        ${imgUrl('portrait-' + v.id) ? `<img src="${imgUrl('portrait-' + v.id)}" style="width:100%;height:100%;object-fit:cover" loading="lazy">` : ''}
      </div>`).join('')}
    </div>
    ${pages > 1 ? `<div class="row" style="margin-top:10px">${Array.from({length: Math.min(pages, 12)}, (_, i) => `<button class="btn sm ${i === ui.teamPage ? 'primary' : ''}" data-a="teamPage" data-p="${i}">${i + 1}</button>`).join('')}</div>` : ''}
    <textarea placeholder="${h(t('tm_reason_ph'))}" style="width:100%;margin-top:10px;min-height:54px" data-a="teamReason">${h(eq.reason)}</textarea>
    <div class="row" style="justify-content:flex-end;margin-top:10px">
      <button class="btn" data-a="teamClose">${h(t('tm_cancel'))}</button>
      <button class="btn primary" data-a="teamSave" ${eq.members.length < 2 ? 'disabled' : ''}>${h(t('tm_save'))}</button>
    </div>
  </div>` : ''}
  ${U.teams.length ? `<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(260px,1fr))">
    ${U.teams.map(tt => {
      const vs = tt.members.map(k => variant(...k.split('::'))).filter(Boolean);
      const sc = synergy(vs);
      return `<div class="card" style="position:relative">
        <button class="btn sm danger" data-a="teamRemove" data-id="${tt.id}" style="position:absolute;top:10px;right:10px">✕</button>
        <div style="font-weight:600;padding-right:34px;margin-bottom:8px">${h(tt.name)}</div>
        ${tt.modeId && modos.find(m => m.id === tt.modeId) ? `<div class="row" style="margin-bottom:6px"><span class="tag dim">${h(modos.find(m => m.id === tt.modeId).name)}</span></div>` : ''}
        <div class="row" style="gap:5px;margin-bottom:8px">${vs.map(v => imgUrl('portrait-' + v.id)
          ? `<img src="${imgUrl('portrait-' + v.id)}" title="${h(fullLabel(v))}" style="width:44px;height:44px;border-radius:8px;object-fit:cover">` : '').join('')}</div>
        <div class="muted">${vs.map(fullLabel).join(' + ')}</div>
        ${tt.reason ? `<p class="muted" style="margin-top:6px">${h(tt.reason)}</p>` : ''}
        <div class="muted" style="margin-top:6px">${sc.score} ${h(t('tm_synergy_pts'))}</div>
      </div>`;
    }).join('')}</div>`
  : `<div class="empty"><div class="big">◇</div><div>${h(t('tm_empty'))}</div></div>`}`;
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
    </div>
    <div class="row" style="margin-top:12px">
      <button class="btn" data-a="exportUser">${h(t('st_export'))}</button>
      <label class="btn" style="cursor:pointer">${h(t('st_import'))}<input type="file" accept=".json" hidden data-a="importUser"></label>
      <button class="btn" data-a="exportCsv">${h(t('st_export_csv'))}</button>
      <button class="btn danger" data-a="resetUser">${h(t('st_reset'))}</button>
    </div>
  </div>

  ${seccionSync()}

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
    <p class="muted">${h(t('st_sources_txt'))}<a href="https://thanosvibs.money" target="_blank" rel="noopener">THANO$VIB$</a>${h(t('st_sources_txt2'))}<a href="https://future-fight.fandom.com" target="_blank" rel="noopener">Future Fight Wiki</a>${h(t('st_sources_txt3'))}</p>
  </div>`;
}

/** Sección de sincronización. Solo tiene sentido dentro de la app de escritorio. */
function seccionSync () {
  if (!ESCRITORIO) {
    return `<div class="section"><h3>${h(t('sy_title'))}</h3>
      <div class="card"><div style="font-weight:600;margin-bottom:6px">${h(t('sy_offline'))}</div>
      <p class="muted">${h(t('sy_offline_note'))}</p></div></div>`;
  }
  const loc = ESCRITORIO.local || {}, rem = ESCRITORIO.remota || {};
  const p = SYNC.progreso;
  const corriendo = !!(p && p.corriendo);
  let aviso;
  if (!rem.juego) aviso = `<span class="muted">${h(t('sy_unknown'))}</span>`;
  else if (rem.juego === loc.juego) aviso = `<span class="tag dim">${h(t('sy_uptodate'))}</span>`;
  else aviso = `<span class="tag solid" style="background:var(--gold)">${h(t('sy_outdated'))}</span>`;

  // Las tier lists regeneran data.js y para eso el build necesita los insumos de la
  // sincronizacion de datos, que un paquete recien descomprimido todavia no tiene.
  const listo = ESCRITORIO.listo !== false;
  const boton = (clave, nota, que) => {
    const bloqueado = (que === 'tierlists' && !listo);
    return `<div class="syncrow">
      <div><div style="font-weight:600">${h(t(clave))}</div>
        <div class="muted">${h(bloqueado ? t('sy_needdata') : t(nota))}</div></div>
      <button class="btn ${corriendo || bloqueado ? '' : 'primary'}" data-a="sync" data-v="${que}"
        ${corriendo || bloqueado ? 'disabled' : ''}>
        ${h(corriendo && p.que === que ? t('sy_running') : t('sy_go'))}</button>
    </div>`;
  };

  return `<div class="section"><h3>${h(t('sy_title'))}</h3>
    <p class="muted" style="margin-bottom:12px">${h(t('sy_note'))}</p>
    <div class="statgrid" style="margin-bottom:12px">
      <div class="stat"><div class="k">${h(t('sy_local'))}</div>
        <div class="v">${h(loc.juego || '?')}</div>
        <div class="muted" style="font-size:11px">${h(t('sy_snapshot'))} ${h(loc.generado || '?')}</div></div>
      <div class="stat"><div class="k">${h(t('sy_remote'))}</div><div class="v">${h(rem.juego || '—')}</div></div>
    </div>
    <div class="row" style="margin-bottom:12px">${aviso}</div>
    ${boton('sy_data', 'sy_data_note', 'datos')}
    ${boton('sy_tier', 'sy_tier_note', 'tierlists')}
    ${boton('sy_img', 'sy_img_note', 'imagenes')}
    ${p ? `<div class="synclog ${p.error ? 'mal' : ''}">
      ${p.error ? `<div class="syncerr">${h(t('sy_failed'))}: ${h(p.error)}</div>` : ''}
      ${p.terminado && !p.error ? `<div class="syncok">${h(t('sy_done'))}</div>` : ''}
      <pre>${h((p.lineas || []).slice(-40).join('\n'))}</pre>
    </div>` : ''}
  </div>`;
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
  let body;
  switch (ui.view) {
    case 'detail':   body = renderDetail(); break;
    case 'compare':  body = renderCompare(); break;
    case 'tierlist': body = renderTierList(); break;
    case 'modos':    body = renderModos(); break;
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
    case 'lang': LANG = U.prefs.lang = (LANG === 'es' ? 'en' : 'es'); commit(); break;
    case 'toggleFilters': P.filtersOpen = !P.filtersOpen; commit(); break;
    case 'clearFilters': P.filters = { c:[], r:[], t:[], f:[], ins:[], race:[], origin:[], ab:[] };
      P.flags = { t4:false, trans:false, nuevo:false }; P.kind = 'todo'; P.objetivo = ''; P.atributo = '';
      ui.search = ''; ui.page = 0; commit(); break;
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
      ui.tlPick = null;
      if (ui.pickMode) { togglePick(d.cid, d.uid || null); render(); break; }
      ui.view = 'detail'; ui.charId = d.cid; ui.uniformId = d.uid || 'base'; render(); window.scrollTo(0, 0); break; }
    case 'uniform': ui.uniformId = d.uid; render(); break;

    case 'goTier': ui.view = 'tierlist'; render(); break;
    case 'goModos': ui.view = 'modos'; render(); break;
    case 'modoFiltro': ui.modoFiltro = d.v; render(); break;
    case 'modoAbrir': ui.modoAbierto = ui.modoAbierto === d.id ? null : d.id; render(); break;
    case 'verLista': ui.view = 'tierlist'; ui.tierList = d.id; render(); window.scrollTo(0, 0); break;
    case 'irArmado': e.preventDefault(); document.getElementById('armado')?.scrollIntoView({ behavior: 'smooth' }); break;
    case 'irArmadoModos': e.preventDefault(); ui.view = 'modos'; render();
      document.getElementById('armado')?.scrollIntoView({ behavior: 'smooth' }); break;
    case 'artEst': ui.artEst = d.v; render(); break;
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

    case 'marcarModo': ui.marcando = !ui.marcando; render(); break;
    case 'goSettings': ui.view = 'settings'; render(); break;
    case 'sync': {
      const que = d.v;
      apiLocal('/api/sync/' + que, 'POST')
        .then(p => { SYNC.progreso = p; render(); pollProgreso(); })
        .catch(err => {
          SYNC.progreso = null; render();
          alert(err.message === 'sin-datos' ? t('sy_needdata')
              : err.message === 'ya hay una sincronizacion en curso' ? t('sy_busy') : err.message);
        });
      SYNC.progreso = { corriendo: true, que, lineas: [], error: null, terminado: false };
      render(); break; }
    case 'modeAdd': U.modes.push({ id:'modo-' + Date.now(), name:t('st_new_mode'), teamSize:3 }); commit(); break;
    case 'modeDel': U.modes.splice(parseInt(d.i, 10), 1); commit(); break;
    case 'clearImg': delete U.images[d.img]; commit(); break;
    case 'resetUser': if (confirm(t('st_confirm_reset'))) {
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
});

document.addEventListener('change', (e) => {
  const el = e.target.closest('[data-a]'); if (!el) return;
  const a = el.getAttribute('data-a'), d = el.dataset;
  if (a === 'sort') { U.prefs.sort = el.value; commit(); return; }
  if (a === 'newListTpl') { ui.newListTpl = el.value; return; }
  if (a === 'newListKind') { ui.newListKind = el.value; return; }
  if (a === 'abxDia') { ui.abxDia = parseInt(el.value, 10); render(); return; }
  if (a === 'rowLabel' || a === 'listName') { rebuild(); render(); return; }
  if (a === 'refList') { U.prefs.refList = el.value; commit(); return; }
  if (a === 'objetivo') { U.prefs.objetivo = el.value; ui.page = 0; commit(); return; }
  if (a === 'atributo') { U.prefs.atributo = el.value; ui.page = 0; commit(); return; }
  if (a === 'teamMode') { ui.team.modeId = el.value; ui.team.members = ui.team.members.slice(-tamModo(el.value)); render(); return; }
  if (a === 'edUni') { ui.edDraft.uniforms[d.i][d.f] = el.value; return; }
  if (a === 'marca') { marcar(d.p, d.sl, d.k, el.checked); return; }
  if (a === 'tlFila') { const actuales = filasDe(ui.tierList, ui.tlPick);
    setFilas(ui.tierList, ui.tlPick, el.checked ? actuales.concat(d.row) : actuales.filter(r => r !== d.row)); return; }
  if (a === 'upload') { const f = el.files[0]; if (f) readFile(f, url => { U.images[d.img] = url; commit(); }); return; }
  if (a === 'importUser') { const f = el.files[0]; if (!f) return;
    const r = new FileReader();
    r.onload = () => { try { U = Object.assign(blankUser(), JSON.parse(r.result)); commit(); }
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
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && ui.tlPick) { ui.tlPick = null; render(); }
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
    const base = [v.key, v.name, v.uid ? v.sub : '', v.c, v.f, v.t, v.trans ? 'sí' : 'no', v.ins, v.ch.race, v.ch.gender,
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

rebuild();
try { if (sessionStorage.getItem('mff_volver') === 'settings') { ui.view = 'settings'; sessionStorage.removeItem('mff_volver'); } } catch (e) {}
render();
detectarEscritorio();
})();
