# Completitud de los datos

Generado por `scripts/completitud.py` sobre `data.js` (juego 12.2.5, datos del 2026-10-06, formato 10) y `datos.json`.

Qué le falta a cada variante (un personaje con un uniforme) para tener la información que la app muestra y usa, y de dónde podría salir. Lo que dos fuentes dicen distinto está en `docs/AUDITORIA.md`; esto es lo que no está. Lo que no existe en el juego no es un faltante (un personaje sin artefacto, si ninguna fuente dice que tenga uno), y lo que una fuente dice a propósito va aparte.

## Qué es «completo»

Una variante está completa si no le falta nada de esto. Lo del personaje (instinto, stats, artefacto, strikers, bonos, Ideal CTP List, guía de armado, tier list General) vale para todas sus variantes.

| Pieza | Qué se pide | Por qué es esperable que esté |
|---|---|---|
| Identidad | Clase, bando, género, raza, habilidades, habilidad de World Boss, instinto y tipo de ataque. | thanosvibs los publica para todos [Comprobado], salvo el instinto, que la app toma del infobox de la wiki: que todos tengan uno en el juego es [Probable]. El tipo de ataque se deduce del daño de las activas. |
| Stats | Recuperación y las cinco resistencias elementales. | Son los stats que thanosvibs publica [Comprobado]; la ficha muestra los del personaje en todas sus variantes. |
| Skills | Liderazgo, pasiva, pasiva de Tier-2 y las cinco activas; la Definitiva con Tier-3 o Trascendido; la Striker con Tier-4; la pasiva de uniforme en cada uniforme. Cada skill con efectos tipados, sin marcadores sin resolver ($HEROSUBTYPE1, $TIME sin duración), sin códigos en lugar de nombres, sin objetivos sin nombre, sin «Give Power» vacíos y, las activas, con su recarga. | Son las skills de toda variante en el juego [Comprobado]: los 598 uniformes de los datos traen su pasiva de uniforme. El análisis, los roles y la sinergia leen sus efectos. |
| Liderazgo y soportes | Su liderazgo, el de Leads & Supports o, si no lo publica, el que el build deriva de su Leader Skill; los soportes que sus pasivas le dan al equipo, en Leads & Supports, con el nombre de la skill de la que salen. | La sinergia y los órdenes PvP y PvE solo ven lo que publica Leads & Supports y los liderazgos que el build deriva de la Leader Skill de la API [Comprobado] (Ezequiel, 4 de octubre de 2026; docs/AUDITORIA.md, sección 12). |
| Artefacto | Si existe, su texto con los valores de 3★ a 6★ y su ícono. | La ficha lo muestra por estrellas [Comprobado]. Un personaje sin artefacto no es un faltante si ninguna fuente dice que tenga uno (ni Leads & Supports ni la guía de armado). |
| Strikers | Quiénes pueden aparecer a pegar con él (pestaña Striker de la wiki). | En el juego cada personaje tiene sus strikers [Probable]: la lista de Kingpin coincide con la del juego. Suman en la sinergia y en los órdenes PvP y PvE. |
| Bonos de equipo | Sus bonos de equipo, con nombre. | El juego da bonos a los personajes que van juntos [Comprobado]; que todos tengan alguno es [Probable]. Suman en la sinergia. |
| C.T.P. | Su fila en la Ideal CTP List; C.T.P. en la guía de armado y, si tiene función en PvP o en PvE, el meta de ese contexto. | Todos llevan un C.T.P. desde el Nv. 30 [Comprobado]. La ficha muestra los dos; las tarjetas de equipo, los de la guía de armado según el contexto. |
| Guía de armado | Su fila hecha, con C.T.P., ISO-8 y obelisco, salvo que la guía diga que no vale la pena armarlo (ISO-8 «dont waste gold») o la Ideal CTP List lo ponga en «Not worth». | La guía de armado tiene una fila por personaje y la completa para la mayoría [Comprobado]; la pestaña Armado la muestra. |
| Tier lists | Su lugar en la tier list General de thanosvibs; la función en PvP y en PvE va como dato. | La General ubica a todo el roster [Comprobado]. Estar o no en Arena (PvP) o en Alianza y World Boss Legend (PvE) es la función en el contexto, que dice la lista: no estar no es un faltante. |
| Retrato e íconos | Su retrato y los íconos de su clase, bando, raza, género, habilidades y habilidad de World Boss, publicados en datos.json. | La app baja lo que publica datos.json [Comprobado]. |
| Rotación | Una rotación de thanosvibs para la variante, o la de la guía de armado si la guía es de ese uniforme. | Toda variante usa sus activas en algún orden, y las skills cambian con cada uniforme [Probable]. thanosvibs publica las rotaciones por uniforme. |
| Perfil y roles | Con qué pega (ataque, tipos de daño, elementos) y sus roles. | Los calcula el build de sus skills [Comprobado]; la sinergia los usa. |
| Datos del uniforme | Costo, materiales y las cinco opciones de uniforme (retratos del roster). | thanosvibs los publica para cada uniforme [Comprobado]. |

## Resumen

177 de 888 variantes completas (20%); 34 de 290 personajes con todas sus variantes completas.

Lo que falta, de lo que deja incompletas más variantes a lo que deja menos (lo que falta en el personaje cuenta en todas sus variantes):

| Faltante | Variantes | Personajes | Casos | De dónde podría salir |
|---|---|---|---|---|
| [Strikers](#strikers) | 356 | 122 | 122 | la wiki (pestaña Striker), el juego o foros |
| [Rotación](#rotación) | 189 | 109 | 189 | thanosvibs (rotaciones), la guía de armado o foros |
| [Duración sin publicar ($TIME)](#duración-sin-publicar-time) | 131 | 75 | 155 | thanosvibs (Leads & Supports), la wiki o foros |
| [Código en lugar de un nombre](#código-en-lugar-de-un-nombre) | 83 | 30 | 119 | thanosvibs (ids de la API de skills), la wiki o foros |
| [Fila vacía en la guía de armado](#fila-vacía-en-la-guía-de-armado) | 73 | 32 | 32 | la guía de armado o foros |
| [Facción, tipo, raza o habilidad sin resolver ($HEROSUBTYPE1)](#facción-tipo-raza-o-habilidad-sin-resolver-herosubtype1) | 70 | 33 | 96 | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| [«Give Power» sin lo que otorga](#give-power-sin-lo-que-otorga) | 68 | 27 | 79 | thanosvibs (Leads & Supports), la wiki o foros |
| [Instinto desconocido](#instinto-desconocido) | 50 | 15 | 15 | la wiki (infobox o categoría de la página), el juego o foros |
| [Skill sin efectos](#skill-sin-efectos) | 48 | 31 | 48 | la wiki (en la pasiva de uniforme, el «Bonus» del uniforme) o foros |
| [Liderazgo sin completar](#liderazgo-sin-completar) | 35 | 12 | 35 | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| [Bonos de equipo que faltan](#bonos-de-equipo-que-faltan) | 33 | 32 | 32 | la wiki (sección Team Bonus), capturas del juego o foros |
| [Sin el C.T.P. de su contexto en la guía de armado](#sin-el-ctp-de-su-contexto-en-la-guía-de-armado) | 29 | 27 | 31 | la guía de armado o foros |
| [ISO-8 u obelisco sin dato en la guía de armado](#iso-8-u-obelisco-sin-dato-en-la-guía-de-armado) | 23 | 6 | 6 | la guía de armado o foros |
| [Soporte que Leads & Supports no publica](#soporte-que-leads--supports-no-publica) | 21 | 15 | 21 | thanosvibs (Leads & Supports) o a mano desde la skill |
| [Nombre en Leads & Supports distinto del de la skill](#nombre-en-leads--supports-distinto-del-de-la-skill) | 16 | 15 | 17 | el juego o foros |
| [Objetivo sin nombre (Target ID)](#objetivo-sin-nombre-target-id) | 16 | 12 | 16 | thanosvibs (Leads & Supports) o foros |
| [Valores del artefacto incompletos](#valores-del-artefacto-incompletos) | 12 | 5 | 5 | la wiki (página Artifact) o el juego |
| [Skill que falta](#skill-que-falta) | 7 | 3 | 11 | thanosvibs (API de skills), la wiki o foros |
| [Activa sin recarga](#activa-sin-recarga) | 4 | 2 | 4 | la wiki o el juego |
| [Bono de equipo sin nombre](#bono-de-equipo-sin-nombre) | 4 | 2 | 2 | capturas del juego o foros |
| [Retrato o ícono](#retrato-o-ícono) | 3 | 1 | 3 | thanosvibs (imágenes) |
| [Sin C.T.P. en la guía de armado](#sin-ctp-en-la-guía-de-armado) | 3 | 2 | 2 | la guía de armado o foros |

Sin casos: Dato de identidad vacío; Stats; Efecto que el catálogo no clasifica; Artefacto que falta; Sin fila en la Ideal CTP List; Sin lugar en la tier list General; Perfil de combate o roles; Datos del uniforme.

### Lo que ya se sabía que no cierra

- **Marcadores sin resolver:** 96 efectos en 70 variantes. docs/AUDITORIA.md (sección 8) los cuenta por id de la API, que se repite en los uniformes que comparten la skill.
- **Liderazgos:** Leads & Supports publica el de 411 variantes, y el build deriva el de 443 más de su Leader Skill (461 slots, con "src": "api"; docs/AUDITORIA.md, sección 12). 35 slots de 35 variantes no se pudieron derivar (efecto sin stat, 35; «Give Power», 1; un slot puede tener más de un motivo).
- **Strikers:** 119 personajes sin la pestaña Striker en la wiki y 3 con la pestaña sin filas que se puedan leer.
- **Bonos de equipo por confirmar:** los que se vieron en capturas del juego y esperan confirmación no están en data.js, así que este informe no los ve. Sí ve 30 personajes sin ningún bono y 2 solo con los del juego (Annihilus y Galactus). Los 49 bonos con versiones empatadas entre páginas de la wiki son diferencias entre fuentes (docs/AUDITORIA.md, sección 10): van en «Lo que no cuenta».
- **Nombres de Leads & Supports que no son los de la API de skills:** 17 en 16 variantes; 6 con el nombre de otra skill de la variante, entre ellos Jeff the Land Shark y Polaris — Uncanny X-Men.

### Lo que no cuenta como faltante

- **Sin artefacto:** 21 personajes, y ninguna fuente dice que tengan uno: Black Dwarf, Blue Marvel, Corvus Glaive, Darkhawk, Deathlok, Dormammu, Elsa Bloodstone, Iron Fist, Jessica Jones, Luke Cage, Molecule Man, Moonstone, Morbius, Nightcrawler, Proxima Midnight, Quasar (Avril Kincaid), Silk, Singularity, Songbird, Supergiant, Viper.
- **Guía de armado sin C.T.P., ISO-8 u obelisco para quien no vale la pena armar:** 63 personajes: la guía dice «dont waste gold» como ISO-8 o la Ideal CTP List los pone en «Not worth».
- **Bonos con versiones empatadas entre páginas de la wiki:** 49 (docs/AUDITORIA.md, sección 10). La app muestra todas las versiones.
- **Función en el contexto:** 60 variantes tienen función en PvP y 119 en PvE (están en las tier lists de ese contexto). Las demás no la tienen: la lista lo dice al no ponerlas.
- **Lo que este chequeo no mira:** las diferencias entre fuentes (docs/AUDITORIA.md), las traducciones, cómo se consigue cada artefacto, los stats de cada uniforme (data.js trae solo los del personaje) y el Set Striker, que la app no tiene.

## Por tipo de faltante

Las variantes de un personaje con el mismo faltante van en una fila.

### Instinto desconocido

15 casos en 15 personajes. thanosvibs no publica el instinto y la app lo toma del infobox de la wiki, que no lo da para estos personajes. Que todos tengan uno en el juego es [Probable].

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Aero (sus 2 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Agent 13 (sus 2 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Black Knight | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Blue Marvel (sus 2 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Captain Marvel (sus 8 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Daredevil (sus 5 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Falcon (sus 7 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Gorgon | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Human Torch (sus 5 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Invisible Woman (sus 5 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Mysterio (sus 3 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Stryfe (sus 3 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Supergiant (sus 2 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Vulture (sus 2 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |
| Wave (sus 2 variantes) | la app no sabe su instinto: thanosvibs no lo publica y la wiki no lo da | la wiki (infobox o categoría de la página), el juego o foros |

### Skill que falta

11 casos en 3 personajes y 7 variantes. La API de skills no trae una skill que la variante tiene en el juego por su tier o por ser uniforme (docs/AUDITORIA.md, sección 4, lista las de Tier-4 sin Striker y las de skill 6 sin Definitiva).

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Black Swan | Pasiva: la API de skills no la trae; Pasiva T2: la API de skills no la trae; Activa 4: la API de skills no la trae; Activa 5: la API de skills no la trae; Definitiva: la API de skills no la trae (es Tier-3 o Trascendido) | thanosvibs (API de skills), la wiki o foros |
| Red Skull (base, Secret Wars: Red Skull, Hydra Armor) | Striker: la API de skills no la trae (es Tier-4) | thanosvibs (API de skills), la wiki o foros |
| Sister Grimm (base, All-New, All-Different, Runaways) | Striker: la API de skills no la trae (es Tier-4) | thanosvibs (API de skills), la wiki o foros |

### Skill sin efectos

48 casos en 31 personajes y 48 variantes. La skill está en la API, sin ningún efecto. Que el juego le dé uno es [Probable]: de la pasiva de uniforme, la wiki publica el «Bonus» de cada uniforme.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Beast — Age of Apocalypse | Pasiva de uniforme «Age of Apocalypse»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Beast — Uncanny X-Men | Pasiva de uniforme «Uncanny X-Men»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Black Panther — Marvel Studios' Captain America: Civil War | Pasiva de uniforme «Marvel Studios' Captain America: Civil War»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Blade — 70's Classic | Pasiva de uniforme «70's Classic»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Captain Marvel — Secret Wars: Captain Marvel & The Carol Corps | Pasiva de uniforme «Secret Wars: Captain Marvel & The Carol Corps»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Captain Marvel — Ms. Marvel | Pasiva de uniforme «Ms. Marvel»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Captain Marvel — Marvel Studios' Captain Marvel | Pasiva de uniforme «Marvel Studios' Captain Marvel»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Crystal — Royal Suit | Pasiva de uniforme «Royal Suit»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Crystal — Fantastic Four | Pasiva de uniforme «Fantastic Four»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Cyclops — Age of Apocalypse | Pasiva de uniforme «Age of Apocalypse»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Cyclops — Marvel NOW! | Pasiva de uniforme «Marvel NOW!»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Daisy Johnson — Marvel Studios' Agents of S.H.I.E.L.D. (Quake) | Pasiva de uniforme «Marvel Studios' Agents of S.H.I.E.L.D. (Quake)»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Gamora — All-New, All-Different | Pasiva de uniforme «All-New, All-Different»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Ghost — Marvel Studios' Ant-Man and the Wasp | Pasiva de uniforme «Marvel Studios' Ant-Man and the Wasp»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Ghost Rider — King of Hell | Pasiva de uniforme «King of Hell»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Gwenpool — Gwen Poole | Pasiva de uniforme «Gwen Poole»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Hulk — Marvel Studios' Thor: Ragnarok | Pasiva de uniforme «Marvel Studios' Thor: Ragnarok»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Hulk — Marvel Studios' Avengers: Endgame | Pasiva de uniforme «Marvel Studios' Avengers: Endgame»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Hulk — Team Suit | Pasiva de uniforme «Team Suit»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Iron Man — Secret Wars: 2099 | Pasiva de uniforme «Secret Wars: 2099»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Iron Man — Marvel Studios' Captain America: Civil War | Pasiva de uniforme «Marvel Studios' Captain America: Civil War»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Loki — Lady Loki | Pasiva de uniforme «Lady Loki»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Loki — Marvel Studios' Thor: Ragnarok | Pasiva de uniforme «Marvel Studios' Thor: Ragnarok»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Loki — Classic | Pasiva de uniforme «Classic»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Luke Cage — All-New, All-Different | Pasiva de uniforme «All-New, All-Different»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Luke Cage — Marvel Studios' Luke Cage | Pasiva de uniforme «Marvel Studios' Luke Cage»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| M.O.D.O.K. — SPIDOC | Pasiva de uniforme «SPIDOC»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Magik — Phoenix Five | Pasiva de uniforme «Phoenix Five»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Medusa — Monsters Unleashed! (MFF Variant) | Pasiva de uniforme «Monsters Unleashed! (MFF Variant)»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Medusa — Inhumans vs X-Men | Pasiva de uniforme «Inhumans vs X-Men»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Moon Knight — Armored | Pasiva de uniforme «Armored»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Nebula — Classic | Pasiva de uniforme «Classic»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Nick Fury — Marvel Studios' Captain Marvel | Pasiva de uniforme «Marvel Studios' Captain Marvel»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Proxima Midnight — Marvel Studios' Avengers: Infinity War | Pasiva de uniforme «Marvel Studios' Avengers: Infinity War»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Rocket Raccoon — All-New, All-Different | Pasiva de uniforme «All-New, All-Different»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Rogue — Age of Apocalypse | Pasiva de uniforme «Age of Apocalypse»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Rogue — Uncanny Avengers | Pasiva de uniforme «Uncanny Avengers»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Ronan — Annihilation | Pasiva de uniforme «Annihilation»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Satana — Marvel Legacy | Pasiva de uniforme «Marvel Legacy»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Sister Grimm — All-New, All-Different | Pasiva de uniforme «All-New, All-Different»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Spider-Man — Secret Wars: Renew Your Vows | Pasiva de uniforme «Secret Wars: Renew Your Vows»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Spider-Man — All-New, All-Different | Pasiva de uniforme «All-New, All-Different»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Storm — X-Men Red | Pasiva de uniforme «X-Men Red»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| War Machine — Iron Patriot | Pasiva de uniforme «Iron Patriot»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| War Machine — Avengers: The Initiative | Pasiva de uniforme «Avengers: The Initiative»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| War Machine — Marvel Studios' Captain America: Civil War | Pasiva de uniforme «Marvel Studios' Captain America: Civil War»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Winter Soldier — Marvel Studios' Captain America: Civil War | Pasiva de uniforme «Marvel Studios' Captain America: Civil War»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |
| Winter Soldier — Marvel Studios' Avengers: Infinity War | Pasiva de uniforme «Marvel Studios' Avengers: Infinity War»: la API la publica sin ningún efecto | la wiki (el «Bonus» del uniforme) o foros |

### Facción, tipo, raza o habilidad sin resolver ($HEROSUBTYPE1)

96 casos en 33 personajes y 70 variantes. El efecto nombra una facción, un tipo, una raza o una habilidad con un marcador que ni la tabla a mano, ni Leads & Supports, ni la wiki resolvieron: la app lo muestra «sin especificar». Son los de docs/AUDITORIA.md, sección 8, que los cuenta por id de la API (un id se repite en los uniformes que comparten la skill); acá va cada variante.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Agent Venom — Agent Anti-Venom | Pasiva de uniforme «Agent Anti-Venom»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Angela — Secret Wars: 1602 Witch Hunter Angela | Pasiva de uniforme «Secret Wars: 1602 Witch Hunter Angela»: «Increases basic damage dealt to $HEROCLASS1 types by 20%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Captain Marvel — Marvel Studios' Avengers: Endgame | Pasiva de uniforme «Marvel Studios' Avengers: Endgame»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.»; Pasiva de uniforme «Marvel Studios' Avengers: Endgame»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 10%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Captain Marvel — Marvel Studios' The Marvels | Pasiva de uniforme «Marvel Studios' The Marvels»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.»; Pasiva de uniforme «Marvel Studios' The Marvels»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 50%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Captain Marvel — Marvel Animation's Marvel Zombies | Pasiva de uniforme «Marvel Animation's Marvel Zombies»: «Increases basic damage by 55% when attacking characters without $HEROSUBTYPE1 Ability.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Deathlok (sus 2 variantes) | Pasiva «Centipede Serum»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 50%.»; Pasiva «Centipede Serum»: «Decreases basic damage received from enemies with $HEROSUBTYPE1 ability by 50%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Drax — Annihilation | Pasiva de uniforme «Annihilation»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 60%.» (2 veces) | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ebony Maw (Dark Obsidian Armor, General's Hand) | Pasiva T2 «Evil Persuasion»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.»; Pasiva T2 «Evil Persuasion»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Electro — Spider-Man: No Way Home | Pasiva «Electric Battlefield»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.»; Pasiva «Electric Battlefield»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Falcon (base, All-New Captain America, Marvel Studios' Captain America: Civil War, Marvel Legacy, Marvel Studios' The Falcon and the Winter Soldier (Captain America (Sam Wilson)), What If... Zombies?!) | Definitiva «Hero's Rise»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 70%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Falcon — Marvel Studios' Captain America: Brave New World (Captain America (Sam Wilson)) | Pasiva «New Captain America»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.»; Definitiva «Hero's Rise»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 70%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Falcon (Joaquin Torres) | Pasiva T2 «Captain's Wingman»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Gamora (Requiem, Marvel Studios' Guardians of the Galaxy 3, Wastelanders) | Pasiva T2 «Cosmic Enforcer»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.» (2 veces) | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ghost Rider (base, 70's Classic, Inhumans: Attilan Rising, King of Hell) | Pasiva T2 «Repentance»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ghost Rider (Rage Returned, Savage Avengers) | Pasiva T2 «Hell's Wrath»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ghost Rider (Robbie Reyes) — Lord of Vengeance | Pasiva de uniforme «Lord of Vengeance»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.»; Pasiva de uniforme «Lord of Vengeance»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 70%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Gorgon | Activa 3 «War Cry»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Green Goblin — Gold Goblin | Pasiva T2 «OZ Formula»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.» (2 veces) | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Iron Man (Marvel Studios' Avengers: Endgame, Team Suit) | Activa 3 «Overdrive Beam»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Magneto — Marvel NOW! | Pasiva de uniforme «Marvel NOW!»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 45%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Malekith (base, All-New, All-Different) | Pasiva T2 «Malicious Manipulation»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.»; Pasiva T2 «Malicious Manipulation»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Malekith — War of the Realms | Pasiva T2 «Dark Blessing»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Maximus | Pasiva «Mad Scientist»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 50%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Mephisto (sus 2 variantes) | Pasiva T2 «Rage of the Pit»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%. Effect cannot be removed.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Molten Man | Pasiva «Fire Eater»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Punisher — Cosmic Ghost Rider | Pasiva de uniforme «Cosmic Ghost Rider»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.» (2 veces) | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Punisher — Fist of the Beast | Pasiva de uniforme «Fist of the Beast»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Punisher — Marvel Television's Daredevil: Born Again | Pasiva de uniforme «Marvel Television's Daredevil: Born Again»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Red Skull (base, Secret Wars: Red Skull, Hydra Armor) | Pasiva T2 «Hero Hunter»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.»; Pasiva T2 «Hero Hunter»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Red Skull — The Crimson Fall | Pasiva T2 «Age of Malice»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.» (2 veces) | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ronan — Marvel Studios' Captain Marvel | Pasiva de uniforme «Marvel Studios' Captain Marvel»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Sentinel — Stark Sentinels Mk II | Pasiva «Mutant Suppressor»: «Increases basic damage dealt to $HEROSUBTYPE1 characters by 100%.»; Pasiva «Mutant Suppressor»: «Decreases basic damage received from $HEROSUBTYPE1 characters by 60%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Spider-Man (Miles Morales) (base, Into the Spider-Verse, Absolute Carnage) | Pasiva T2 «Ultimate Spider-Man»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Spider-Man (Miles Morales) — Spider-Man: Across the Spider-Verse | Pasiva de uniforme «Spider-Man: Across the Spider-Verse»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Spider-Man (Miles Morales) — Ancient Curse | Pasiva de uniforme «Ancient Curse»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Spider-Man 2099 — All-New, All-Different | Pasiva de uniforme «All-New, All-Different»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 10%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Thanos — Obsidian King | Pasiva «Mad Titan»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Thanos — Wise Harvester | Pasiva «True Peace»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.»; Pasiva «True Peace»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 20%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Thanos (Thanos Wins, Annihilation) | Pasiva «Hero Slayer»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Thor (Jane Foster) — Marvel Studios' Thor: Love and Thunder | Pasiva de uniforme «Marvel Studios' Thor: Love and Thunder»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 35%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ulik | Activa 3 «Troll's Roar»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ultron (Avengers: Age of Ultron (Ultron Prime), Avengers: Age of Ultron (Ultron Mark 1), Avengers: Age of Ultron (Ultron Mark 3)) | Pasiva de uniforme «Avengers: Age of Ultron»: «Decreases basic damage received from $HEROCLASS1 types by 10%.»; Pasiva de uniforme «Avengers: Age of Ultron»: «Increases basic damage dealt to $HEROCLASS1 types by 10%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ultron — Marvel Studios' What If...? (Infinity Ultron) | Pasiva de uniforme «Marvel Studios' What If...?»: «Increases basic damage by 40% when attacking characters without $HEROSUBTYPE1 Ability.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ultron — All-Father Ultron | Pasiva de uniforme «All-Father Ultron»: «Increases basic damage by 40% when attacking characters without $HEROSUBTYPE1 Ability.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Vulture — Spider-Man: Homecoming | Pasiva de uniforme «Spider-Man: Homecoming»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Whiplash | Pasiva «Mechanical Engineering»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 80%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Yellowjacket — Marvel NOW! | Pasiva de uniforme «Marvel NOW!»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |

### Duración sin publicar ($TIME)

155 casos en 75 personajes y 131 variantes. La API publica «$TIME» sin la duración del efecto: la app lo muestra «sin especificar». Si Leads & Supports publica el mismo slot con una duración, se dice; si no, y lo que otorga trae la suya, también: que sea la misma no está comprobado.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Agent Venom (Classic, Guardians of the Galaxy) | Pasiva «Emergency Escape»: «Acquires the following effect for $TIME sec.» (2 veces) | la wiki o foros |
| Ant-Man — Ant-Man and the Wasp: Quantumania | Pasiva T2 «Elusive Hero»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 20 s, que podría ser la misma), la wiki o foros |
| Ares | Pasiva T2 «God of Battle»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 10 s, que podría ser la misma), la wiki o foros |
| Ares — Punisher | Pasiva T2 «God of Battle»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Beta Ray Bill (sus 2 variantes) | Pasiva «Korbinite Strength»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Black Swan | Activa 3 «Brutal Incursion»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros |
| Black Widow — Venomous | Pasiva de uniforme «Venomous»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros |
| Blue Dragon | Liderazgo «Sky Serpent»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 5 s) |
| Blue Dragon — Moon Temple Defenders | Liderazgo «Sky Serpent»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 10 s) |
| Captain America — Hydra Supreme | Pasiva de uniforme «Hydra Supreme»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 3 s y 6 s, que podría ser la misma), la wiki o foros |
| Captain America — Enter the Phoenix | Pasiva de uniforme «Enter the Phoenix»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 3 s y 6 s, que podría ser la misma), la wiki o foros |
| Captain America — Back to Basics | Pasiva de uniforme «Back to Basics»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 4 s y 10 s, que podría ser la misma), la wiki o foros |
| Captain America — What If... Zombies?! | Pasiva de uniforme «What If... Zombies?!»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 5 s, que podría ser la misma), la wiki o foros |
| Captain America — Galactic Talon | Pasiva de uniforme «Galactic Talon»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 5 s, que podría ser la misma), la wiki o foros |
| Cassandra Nova | Pasiva «Evil Spirit»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 3 s, que podría ser la misma), la wiki o foros |
| Daken — Dark Wolverine | Pasiva «Undying Spirit»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Daredevil — Marvel Television's Daredevil: Born Again | Pasiva de uniforme «Marvel Television's Daredevil: Born Again»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Deadpool (X-Force, 30th Anniversary Black Version, 30th Anniversary White Version, April Pools) | Pasiva T2 «Merc With A Mouth»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Deadpool (Lady Deadpool, Holiday Party) | Pasiva T2 «Merc With A Mouth»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Deadpool — Marvel Studios' Deadpool & Wolverine | Liderazgo «Marvel's Savior»: «Acquires the following effect for $TIME sec.»; Pasiva «Healing Factor»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 10 s); thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Deadpool — Marvel Studios' Deadpool & Wolverine (Nicepool) | Pasiva «Healing Factor»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Doctor Doom — 3099 | Pasiva de uniforme «3099»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Drax — Annihilation | Pasiva «Unquenchable Vengeance»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros |
| Echo | Pasiva T2 «Hero's Promise»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Echo (Marvel Studios' Hawkeye (Maya Lopez), Marvel Studios' Echo (Maya Lopez (Echo))) | Liderazgo «Back Alley Queen»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Electro | Pasiva «Unstable Current»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Electro — Spider-Man: No Way Home | Pasiva «Electric Battlefield»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Emma Frost — Phoenix Five | Pasiva de uniforme «Phoenix Five»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 10 s, que podría ser la misma), la wiki o foros |
| Emma Frost — Hellfire Gala | Pasiva de uniforme «Hellfire Gala»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 10 s, que podría ser la misma), la wiki o foros |
| Falcon (Joaquin Torres) | Pasiva «Agile Flight»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Galactus | Pasiva «Siphon of Realms»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Gilgamesh (sus 2 variantes) | Pasiva «Eternal Resilience»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Gladiator — Thanos: The Infinity Revelation | Pasiva T2 «Confidence Regained»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Gorr (sus 2 variantes) | Liderazgo «Whispers of Darkness»: «Acquires the following effect for $TIME sec.»; Pasiva «Indigarr Anger»: «Acquires the following effect for $TIME sec.»; Pasiva T2 «Godless Prayer»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s); la wiki o foros |
| Groot (Marvel Studios' Guardians of the Galaxy 3, Planet X Palm) | Pasiva T2 «Bloom»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 1 s) |
| Hawkeye — Marvel Studios' Hawkeye (Hero Suit) | Pasiva de uniforme «Marvel Studios' Hawkeye (Hero Suit)»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros |
| Hawkeye — Wastelanders | Pasiva de uniforme «Wastelanders»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros |
| Heimdall — Asgard Invasion | Pasiva de uniforme «Asgard Invasion»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 10 s, que podría ser la misma), la wiki o foros |
| Hercules | Pasiva «Immortal Hercules»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Hulk (Immortal Hulk, Fear Itself, Titan, Marvel Studios' Spider-Man: Brand New Day) | Pasiva «Enraged»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Hulkbuster (Iron Man Mark 44) — Celestial Hulkbuster (Hulkbuster) | Pasiva de uniforme «Celestial Hulkbuster»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Ikaris (sus 2 variantes) | Pasiva «Eternal Rebirth»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Invisible Woman — Classic | Pasiva T2 «Psionic Fields»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros |
| Invisible Woman — Marvel Studios' The Fantastic Four: First Steps | Pasiva de uniforme «Marvel Studios' The Fantastic Four: First Steps»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Iron Man — Marvel Studios' Avengers: Infinity War | Pasiva de uniforme «Marvel Studios' Avengers: Infinity War»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Iron Man — Marvel Studios' Avengers: Endgame | Pasiva de uniforme «Marvel Studios' Avengers: Endgame»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Iron Man — Team Suit | Pasiva de uniforme «Team Suit»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Iron Man — Avengers 3099 | Pasiva de uniforme «Avengers 3099»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Jessica Jones — Jewel | Pasiva de uniforme «Jewel»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 1 s y 10 s) |
| Kang the Conqueror (sus 2 variantes) | Liderazgo «Kang's Readiness»: «Acquires the following effect for $TIME sec.»; Pasiva «Temporal Resurrection»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s); la wiki o foros |
| Kid Omega | Pasiva T2 «Omega Power»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 5 s, que podría ser la misma), la wiki o foros |
| Kid Omega — Uncanny X-Men | Pasiva T2 «Omega Power»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Kingpin — Winter Criminal | Pasiva de uniforme «Winter Criminal»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros |
| Kingpin — Marvel Television's Daredevil: Born Again | Pasiva de uniforme «Marvel Television's Daredevil: Born Again»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros |
| Knull (sus 2 variantes) | Pasiva T2 «Dark Domination»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 12 s, que podría ser la misma), la wiki o foros |
| Korath | Pasiva «Zero Hesitation»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s y 3 s, que podría ser la misma), la wiki o foros |
| Loki — Marvel Studios' Loki (President Loki) | Pasiva «Trickster»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 8 s y 10 s, que podría ser la misma), la wiki o foros |
| Malekith — War of the Realms | Pasiva «Dark Elf's Will»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Man-Thing | Pasiva «Force of Nature»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Mephisto | Pasiva T2 «Rage of the Pit»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Mephisto — Master of Hell | Liderazgo «Lord of Hell»: «Acquires the following effect for $TIME sec.»; Pasiva T2 «Rage of the Pit»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Mister Fantastic (base, Future Foundation) | Pasiva T2 «Elastic Skin»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 10 s, que podría ser la misma), la wiki o foros |
| Mister Fantastic — The Maker | Pasiva T2 «Elastic Skin»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 3 s y 20 s, que podría ser la misma), la wiki o foros |
| Molecule Man | Liderazgo «Material Transformation»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 6 s) |
| Molten Man | Pasiva T2 «Fiery Rage»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 5 s, que podría ser la misma), la wiki o foros |
| Moonstone | Pasiva «Master Manipulator»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 3 s, que podría ser la misma), la wiki o foros |
| Morgan le Fay | Pasiva T2 «Transcendence»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Morgan le Fay — Fallen Soul | Pasiva de uniforme «Fallen Soul»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 10 s) |
| Mysterio — Summer Mystery | Pasiva T2 «Cunning Battle»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Nightcrawler (base, X-Force) | Pasiva «Into the Shadow»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 10 s, que podría ser la misma), la wiki o foros |
| Nightcrawler — Classic | Pasiva «Into the Shadow»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 6 s y 12 s, que podría ser la misma), la wiki o foros |
| Odin (Avengers 1,000,000 BC, Lord of Asgard) | Liderazgo «Asgardian Wisdom»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Omega Red | Pasiva «Omega Sense»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Polaris (sus 2 variantes) | Pasiva «Inherited Power»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 10 s, que podría ser la misma), la wiki o foros |
| Quasar (Wendell Vaughn) | Liderazgo «Annihilators Assemble»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Rachel Summers — X-Men: Days of Future Past | Liderazgo «Phoenix's Majesty»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Red Guardian — Marvel Studios' Thunderbolts* | Pasiva de uniforme «Marvel Studios' Thunderbolts*»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Red Hulk — Marvel Studios' Captain America: Brave New World | Pasiva «President's Doctor»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Sentinel (sus 3 variantes) | Pasiva «Mutant Suppressor»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 6 s, que podría ser la misma), la wiki o foros |
| Sentry — Merged | Liderazgo «Shining Hero»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Sentry — Marvel Studios' Thunderbolts* | Liderazgo «Shining Hero»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Sleeper | Pasiva «Symbiote Heroes»: «Acquires the following effect for $TIME sec.»; Pasiva T2 «Invisible Symbiote»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s); la wiki o foros |
| Spectrum — Marvel Studios' The Marvels (Captain Monica Rambeau) | Pasiva «Inherited Will»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 5 s, que podría ser la misma), la wiki o foros |
| Spider-Man — Marvel Studios' Avengers: Infinity War | Pasiva de uniforme «Marvel Studios' Avengers: Infinity War»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 5 s, que podría ser la misma), la wiki o foros |
| Spider-Man — Spider-Man: Far From Home | Pasiva de uniforme «Spider-Man: Far From Home»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 5 s, que podría ser la misma), la wiki o foros |
| Spider-Man — Spider-Man: Far From Home (Stealth Suit) | Pasiva de uniforme «Spider-Man: Far From Home (Stealth Suit)»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 5 s, que podría ser la misma), la wiki o foros |
| Spider-Woman — Spider-Man: Across the Spider-Verse | Liderazgo «Mother of Spider»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Squirrel Girl — Nutty Titan | Pasiva de uniforme «Nutty Titan»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Stryfe — The Tyrant of Spring | Pasiva «Energy Curtain»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «The Tyrant of Spring»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 7 s, que podría ser la misma), la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Thanos — Obsidian King | Pasiva «Mad Titan»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «Obsidian King»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros; la wiki o foros |
| Thanos — Wise Harvester | Liderazgo «Enlightened Advice»: «Acquires the following effect for $TIME sec.»; Pasiva «True Peace»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «Wise Harvester»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s); thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros; la wiki o foros |
| Thanos — Thanos Wins | Liderazgo «Enlightened Advice»: «Acquires the following effect for $TIME sec.»; Pasiva «Hero Slayer»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «Thanos Wins»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s); thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros; la wiki o foros |
| Thanos — Annihilation | Liderazgo «Enlightened Advice»: «Acquires the following effect for $TIME sec.»; Pasiva «Hero Slayer»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «Annihilation»: «Acquires the following effect for $TIME sec.» | thanosvibs (Leads & Supports publica el mismo slot con 12 s); thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros; la wiki o foros |
| Titania — Fear Itself | Pasiva T2 «Advanced Musculature»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Toxin | Pasiva T2 «Anger Manifest»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| U.S. Agent | Pasiva «Agent's Shield»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Ultron — All-Father Ultron | Pasiva T2 «Suppression Order»: «Acquires the following effect for $TIME sec.» | la wiki o foros |
| Venom — King in Black | Pasiva de uniforme «King in Black»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Venom — Warstar | Pasiva de uniforme «Warstar»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Venom — Snow Symbiote | Pasiva de uniforme «Snow Symbiote»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Venus (Aphrodite) | Pasiva «The Beauty»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 2 s, que podría ser la misma), la wiki o foros |
| Viper | Pasiva T2 «Venomous Call»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 8 s, que podría ser la misma), la wiki o foros |
| Vision — Ultimate Vision | Pasiva «Manipulation of Atomic Valences»: «Acquires the following effect for $TIME sec.»; Pasiva T2 «Bug Fix»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 10 s, que podría ser la misma), la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Wasp — Ant-Man and the Wasp: Quantumania | Pasiva «The Paralyzer»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 2 s, que podría ser la misma), la wiki o foros |
| Weapon Hex | Pasiva «Witchcraft»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Weapon Hex — Infected Bioweapon | Pasiva T2 «Undead Magic»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «Infected Bioweapon»: «Acquires the following effect for $TIME sec.» | la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot con 12 s) |
| Wolverine — Enter the Phoenix | Pasiva «Regenerative Healing Factor»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «Enter the Phoenix»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Wolverine — X Deaths of Wolverine | Pasiva «Regenerative Healing Factor»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «X Deaths of Wolverine»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |
| Wolverine — Marvel Studios' Deadpool & Wolverine | Pasiva «Regenerative Healing Factor»: «Acquires the following effect for $TIME sec.»; Pasiva de uniforme «Marvel Studios' Deadpool & Wolverine»: «Acquires the following effect for $TIME sec.» | thanosvibs (lo que otorga dura 1 s, que podría ser la misma), la wiki o foros |

### Código en lugar de un nombre

119 casos en 30 personajes y 83 variantes. El texto trae un número donde va el nombre de un efecto, de un elemento o de unas ranuras, y la app lo muestra como viene (docs/AUDITORIA.md, sección 7). Los de tres cifras son ids de habilidades de la API; los de cifras sueltas parecen ranuras o elementos.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Adam Warlock (sus 3 variantes) | Striker «Light of Life», Counter Reflect: «Decreases damage received from reflected effects by 50%.Effect: 2» | la wiki o foros |
| Angel (sus 4 variantes) | Striker «Wings of Mutant Will», Counter Reflect: «Decreases damage received from reflected effects by 50%.Effect: 2» | la wiki o foros |
| Beta Ray Bill (sus 2 variantes) | Striker «Indomitable Spirit», Accumulate All True Element Damage Dealt: «Accumulates 10% of pure 12345 damage when attacking (Max 100%)» | la wiki o foros |
| Black Cat (base, Claws, All-New, All-Different) | Pasiva T2 «Bad Luck», DEBUFF EFFECT ↓: «Decreases 0 effect used by the Character by 80%.» (2 veces) | la wiki o foros |
| Black Dwarf — Marvel Studios' Avengers: Infinity War (Cull Obsidian) | Activa 3 «Wheel of Cull», SET SKILL CD: «Sets the Cooldown time of 12 skill to 1 sec» | la wiki o foros |
| Blue Marvel — Classic | Pasiva de uniforme «Classic», Natural Enemy: «Increases damage dealt to targets with 206 effect by 30%»; Pasiva de uniforme «Classic», Natural Enemy: «Increases damage dealt to targets with 401 effect by 30%» | thanosvibs (es el id de una habilidad de la API de skills) |
| Doctor Octopus (base, Superior Octopus, Spider-Man: No Way Home, Ends of the Earth) | Striker «Unmatched Intellect», SET SKILL CD: «Sets the Cooldown time of 12345 skill to 4 sec» | la wiki o foros |
| Doctor Octopus — Superior Spider-Man | Pasiva T2 «Superior Spider», DURATION INCREASE: «2s increase to the duration of 205.»; Striker «Unmatched Intellect», SET SKILL CD: «Sets the Cooldown time of 12345 skill to 4 sec» | thanosvibs (es el id de una habilidad de la API de skills); la wiki o foros |
| Doctor Strange (base, Marvel Studios' Doctor Strange, Marvel Studios' Avengers: Infinity War) | Activa 5 «Sorcerer Supreme», SET SKILL CD: «Sets the Cooldown time of 1234 skill to 1 sec» | la wiki o foros |
| Doctor Strange — Space Suit | Activa 5 «Vishanti Destruction», SET SKILL CD: «Sets the Cooldown time of 1234 skill to 1 sec» (2 veces) | la wiki o foros |
| Drax (Classic, Annihilation) | Pasiva T2 «Unstoppable Might», Natural Enemy: «Increases damage dealt to targets with 401 effect by 70%» | thanosvibs (es el id de una habilidad de la API de skills) |
| Electro — Spider-Man: No Way Home | Pasiva de uniforme «Spider-Man: No Way Home», Natural Enemy: «Increases damage dealt to targets with 108 effect by 90%» | thanosvibs (es el id de una habilidad de la API de skills) |
| Ghost — Marvel Studios' Thunderbolts* | Activa 4 «Quantum Wave», Selective Removal: «Removes the effect 206 from 0.» | la wiki o foros |
| Ghost Rider (sus 6 variantes) | Striker «Endless Burn», ELEMENT CONVERSION: «Increases 1 damage by 10% of 1 Resistance (up to 50%)» | la wiki o foros |
| Hades (Pluto) | Striker «Lord of Hades», ELEMENT CONVERSION: «Increases 1 damage by 10% of 1 Resistance (up to 50%)» | la wiki o foros |
| Hela | Activa 4 «Nightsword's Glow», DEBUFF EFFECT ↓: «Decreases 0 effect used by the Character by 50%.» (2 veces) | la wiki o foros |
| Hellstorm (sus 2 variantes) | Striker «Branding», Accumulate All True Element Damage Dealt: «Accumulates 10% of pure 12345 damage when attacking (Max 100%)» | la wiki o foros |
| Kahhori | Pasiva T2 «Hero's Decree», Natural Enemy: «Increases damage dealt to targets with 206 effect by 50%»; Pasiva T2 «Hero's Decree», Natural Enemy: «Increases damage dealt to targets with 407 effect by 50%» | thanosvibs (es el id de una habilidad de la API de skills) |
| Kang the Conqueror (sus 2 variantes) | Striker «Battle Armor Shield», REMOVE: «Removes 1 from target (Includes all debuffs)» | la wiki o foros |
| Kingo — Marvel Studios' Eternals | Pasiva de uniforme «Marvel Studios' Eternals», SET SKILL CD: «Sets the Cooldown time of 2 skill to 1 sec» | la wiki o foros |
| Knull (sus 2 variantes) | Striker «Root of Darkness», REMOVE: «Removes 1 from target (Includes all debuffs)» | la wiki o foros |
| Magik — Phoenix Five | Activa 4 «Flames of Doom», SET SKILL CD: «Sets the Cooldown time of 1 skill to 1 sec» | la wiki o foros |
| Satana (base, Marvel Legacy) | Pasiva T2 «Queen of Hell», DEBUFF EFFECT ↓: «Decreases 0 effect used by the Character by 80%.» (2 veces) | la wiki o foros |
| Shadow Shell | Activa 3 «Serpent Strike», SET SKILL CD: «Sets the Cooldown time of 12 skill to 1 sec» | la wiki o foros |
| Silk — Web Suit | Pasiva de uniforme «Web Suit», DURATION INCREASE: «2s increase to the duration of 205.» | thanosvibs (es el id de una habilidad de la API de skills) |
| Songbird | Pasiva T2 «Sonic Pitch», DURATION INCREASE: «1s increase to the duration of 204.» | thanosvibs (es el id de una habilidad de la API de skills) |
| Spider-Man (base, Secret Wars: Renew Your Vows, All-New, All-Different, Marvel Studios' Captain America: Civil War, Spider-Man: Homecoming Homemade Suit, Marvel Studios' Avengers: Infinity War, Spider-Man: Far From Home, Spider-Man: Far From Home (Stealth Suit)) | Pasiva T2 «Great Responsibility», DURATION INCREASE: «2s increase to the duration of 205.»; Striker «Hero's Responsibility», REMOVE: «Removes 1 from target (Includes all debuffs)» (2 veces) | thanosvibs (es el id de una habilidad de la API de skills); la wiki o foros |
| Spider-Man (Spider-Man: No Way Home (Integrated Suit), Spider-Man: No Way Home (Black & Gold Suit), Back to Basics, The Symbiote Suit, Marvel Studios' Spider-Man: Brand New Day) | Striker «Hero's Responsibility», REMOVE: «Removes 1 from target (Includes all debuffs)» (2 veces) | la wiki o foros |
| Storm (sus 5 variantes) | Striker «Crack the Sky», Accumulate All True Element Damage Dealt: «Accumulates 10% of pure 23 damage when attacking (Max 100%)» | la wiki o foros |
| Thanos (Obsidian King, Wise Harvester, Thanos Wins, Annihilation) | Pasiva T2 «Space Throne», Natural Enemy: «Increases damage dealt to targets with 206 effect by 80%»; Pasiva T2 «Space Throne», Natural Enemy: «Increases damage dealt to targets with 407 effect by 80%» | thanosvibs (es el id de una habilidad de la API de skills) |
| Wiccan | Pasiva T2 «Magic Field», DURATION INCREASE: «1s increase to the duration of 120.»; Pasiva T2 «Magic Field», DURATION INCREASE: «1s increase to the duration of 204.» | thanosvibs (es el id de una habilidad de la API de skills) |
| Winter Soldier (sus 7 variantes) | Striker «Assassination Weapon», Natural Enemy: «Increases damage dealt to targets with 577 effect by 70%» | thanosvibs (es el id de una habilidad de la API de skills) |
| Wong (sus 4 variantes) | Striker «Martial Artist of Kamar-Taj», REMOVE: «Removes 1 from target (Includes all debuffs)» | la wiki o foros |

### Objetivo sin nombre (Target ID)

16 casos en 12 personajes y 16 variantes. La etapa se aplica a un grupo de aliados que la API no nombra («Target ID: 72»): la app no puede decir a quiénes les llega. Si Leads & Supports restringe el mismo slot, se dice a quiénes.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Deadpool — April Pools | Liderazgo «Head Honcho»: se aplica a «Target ID: 88» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Gwenpool) |
| Falcon (Joaquin Torres) | Pasiva T2 «Captain's Wingman»: se aplica a «Target ID: 30» | foros |
| Gwenpool — April Pools | Pasiva de uniforme «April Pools»: se aplica a «Target ID: 164» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Deadpool) |
| Hope Summers | Liderazgo «Last Hope»: se aplica a «Target ID: 142» | thanosvibs (Leads & Supports restringe el mismo slot a la raza Mutante) |
| Hulkbuster (Iron Man Mark 44) (3099, Celestial Hulkbuster (Hulkbuster)) | Liderazgo «Iron Armada»: se aplica a «Target ID: 3» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Iron Man) |
| Katy | Liderazgo «Perfect Teamwork»: se aplica a «Target ID: 89» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Shang-Chi) |
| Sleeper | Liderazgo «Father And Me»: se aplica a «Target ID: 42» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Venom) |
| Spider-Man (Miles Morales) — Absolute Carnage | Liderazgo «Quick Recovery»: se aplica a «Target ID: 72» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Carnage) |
| Spider-Man (Miles Morales) — Anniversary Special | Liderazgo «Spider Party»: se aplica a «Target ID: 10» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Spider-Man) |
| Squirrel Girl — Nutty Titan | Pasiva de uniforme «Nutty Titan»: se aplica a «Target ID: 75» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Thanos) |
| Victorious | Liderazgo «For Victory!»: se aplica a «Target ID: 183» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Doctor Doom) |
| Victorious — Emperor Guarder | Liderazgo «Latverian Vanguard»: se aplica a «Target ID: 183» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Doctor Doom) |
| Vision — Marvel Studios' WandaVision | Liderazgo «Prophetic Vision»: se aplica a «Target ID: 140» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Scarlet Witch) |
| Wave (sus 2 variantes) | Liderazgo «Ride the Current»: se aplica a «Target ID: 198» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Namor) |

### «Give Power» sin lo que otorga

79 casos en 27 personajes y 68 variantes. «Give Power» («Acquires the following effect…») sin el efecto que sigue: el análisis dice «Otorga un efecto que la fuente no dice». Si Leads & Supports publica el mismo slot, se dice qué trae. El de una Leader Skill que resuelve el juego (scripts/contenido/liderazgos_api.json) no falta.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Ancient One (sus 4 variantes) | Striker «Enlightenment»: otorga un efecto que la API no dice | la wiki o foros |
| Blue Dragon | Liderazgo «Sky Serpent»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, Remove All Debuffs (5 s)) |
| Blue Dragon — Moon Temple Defenders | Liderazgo «Sky Serpent»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, Remove All Debuffs (10 s)) |
| Cable (sus 6 variantes) | Striker «Focus Enforced»: otorga un efecto que la API no dice | la wiki o foros |
| Captain America (Sharon Rogers) (sus 7 variantes) | Striker «Tireless Super Soldier»: otorga un efecto que la API no dice | la wiki o foros |
| Crystal (sus 4 variantes) | Striker «Elemental Amplification»: otorga un efecto que la API no dice | la wiki o foros |
| Deadpool — Marvel Studios' Deadpool & Wolverine | Liderazgo «Marvel's Savior»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, All Basic Defenses, All Speeds, Remove All Debuffs (10 s)) |
| Doctor Doom — 3099 | Pasiva de uniforme «3099»: otorga un efecto que la API no dice | la wiki o foros |
| Echo | Striker «Ancestor’s Spirit»: otorga un efecto que la API no dice | la wiki o foros |
| Echo (Marvel Studios' Hawkeye (Maya Lopez), Marvel Studios' Echo (Maya Lopez (Echo))) | Striker «Ancestor’s Spirit»: otorga un efecto que la API no dice; Liderazgo «Back Alley Queen»: otorga un efecto que la API no dice | la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, All Basic Defenses, Remove All Debuffs (12 s)) |
| Gorr (sus 2 variantes) | Pasiva «Indigarr Anger»: otorga un efecto que la API no dice; Pasiva T2 «Godless Prayer»: otorga un efecto que la API no dice; Liderazgo «Whispers of Darkness»: otorga un efecto que la API no dice | la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot: HP, Remove All Debuffs (12 s)) |
| Groot (Marvel Studios' Guardians of the Galaxy 3, Planet X Palm) | Pasiva T2 «Bloom»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: Basic Damage Dealt to Boss Types, Heal (1 s)) |
| Human Torch (sus 5 variantes) | Striker «Flame Resonance»: otorga un efecto que la API no dice | la wiki o foros |
| Invisible Woman — Marvel Studios' The Fantastic Four: First Steps | Pasiva de uniforme «Marvel Studios' The Fantastic Four: First Steps»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: Remove All Debuffs (12 s), Debuff Immunity (12 s)) |
| Kang the Conqueror (sus 2 variantes) | Liderazgo «Kang's Readiness»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, Remove All Debuffs (12 s)) |
| Molecule Man | Liderazgo «Material Transformation»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: Ignores Damage Increase/Decrease Effect Between Self and Opposing Faction, Chain Hit Damage Received, Remove All Debuffs (6 s)) |
| Mysterio — Summer Mystery | Pasiva T2 «Cunning Battle»: otorga un efecto que la API no dice | la wiki o foros |
| Odin (Avengers 1,000,000 BC, Lord of Asgard) | Liderazgo «Asgardian Wisdom»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: Lightning Damage, Remove All Debuffs (12 s)) |
| Quasar (Wendell Vaughn) | Liderazgo «Annihilators Assemble»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: HP, Remove All Debuffs (12 s)) |
| Rachel Summers — X-Men: Days of Future Past | Liderazgo «Phoenix's Majesty»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: Mind Resist, Remove All Debuffs (12 s)) |
| Scorpion (sus 2 variantes) | Striker «Scorpion's Hunt»: otorga un efecto que la API no dice | la wiki o foros |
| Sentry | Striker «Light and Darkness»: otorga un efecto que la API no dice | la wiki o foros |
| Sentry — Merged | Striker «Light and Darkness»: otorga un efecto que la API no dice; Liderazgo «Shining Hero»: otorga un efecto que la API no dice | la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, Remove All Debuffs (12 s)) |
| Sentry — Marvel Studios' Thunderbolts* | Striker «Light and Darkness»: otorga un efecto que la API no dice; Liderazgo «Shining Hero»: otorga un efecto que la API no dice | la wiki o foros |
| Sleeper | Pasiva T2 «Invisible Symbiote»: otorga un efecto que la API no dice | la wiki o foros |
| Spider-Woman — Spider-Man: Across the Spider-Verse | Liderazgo «Mother of Spider»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, Remove All Debuffs (12 s)) |
| Stryfe — The Tyrant of Spring | Pasiva de uniforme «The Tyrant of Spring»: otorga un efecto que la API no dice | thanosvibs (Leads & Supports publica el mismo slot: Remove All Debuffs (12 s)) |
| Taskmaster (sus 3 variantes) | Striker «Photographic Memory»: otorga un efecto que la API no dice | la wiki o foros |
| Thanos — Obsidian King | Pasiva de uniforme «Obsidian King»: otorga un efecto que la API no dice | la wiki o foros |
| Thanos — Wise Harvester | Pasiva de uniforme «Wise Harvester»: otorga un efecto que la API no dice; Liderazgo «Enlightened Advice»: otorga un efecto que la API no dice | la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, All Basic Defenses, Remove All Debuffs (12 s)) |
| Thanos — Thanos Wins | Pasiva de uniforme «Thanos Wins»: otorga un efecto que la API no dice; Liderazgo «Enlightened Advice»: otorga un efecto que la API no dice | la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, All Basic Defenses, Remove All Debuffs (12 s)) |
| Thanos — Annihilation | Pasiva de uniforme «Annihilation»: otorga un efecto que la API no dice; Liderazgo «Enlightened Advice»: otorga un efecto que la API no dice | la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, All Basic Defenses, Remove All Debuffs (12 s)) |
| Ultron (sus 6 variantes) | Striker «Organic Hatred»: otorga un efecto que la API no dice | la wiki o foros |
| Weapon Hex — Infected Bioweapon | Pasiva T2 «Undead Magic»: otorga un efecto que la API no dice | la wiki o foros |

### Activa sin recarga

4 casos en 2 personajes y 4 variantes. Las activas 1 a 5 se recargan por tiempo y la API publica 0 [Probable].

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Black Swan | Activa 3 «Brutal Incursion»: la API publica recarga 0 | la wiki o el juego |
| Destroyer (base, Prometheus) | Activa 5 «Asgardian Armament»: la API publica recarga 0 | la wiki o el juego |
| Destroyer — The Mighty Thor | Activa 5 «God of Thunder Armor»: la API publica recarga 0 | la wiki o el juego |

### Liderazgo sin completar

35 casos en 12 personajes y 35 variantes. Leads & Supports no publica el liderazgo de la variante y el build no pudo derivar ese slot de su Leader Skill (docs/AUDITORIA.md, sección 12, con el mismo motivo): un efecto sin stat o una activación sin correspondencia (ni de Leads & Supports ni a mano), un valor que la API no publica, un «Give Power» o una contradicción de Leads & Supports. La sinergia y los órdenes PvP y PvE no ven ese slot.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Blade (base, 70's Classic, Avengers) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Recovers HP equal to 8% of damage dealt to a target<br>Cannot recover more than 0.5% HP each time damage is dealt.» (HP STEAL) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Captain America (Sharon Rogers) (base, Star Light Armor, Dark Star Armor, Star Night Armor) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates an energy Shield equal to 20% of Max HP» (ENERGY SHIELD) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Captain America (Sharon Rogers) (Light Sirius Armor, Poseidon Armor, Arctic Warrior) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates an energy Shield equal to 50% of Max HP» (ENERGY SHIELD) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Daisy Johnson (sus 3 variantes) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates a physical Shield equal to 30% of Max HP» (PHYSICAL SHIELD) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Green Goblin | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Increases Poison Resist by 50%.» (POISON RESIST ↑) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Hydro-Man | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Immunity to BLEED Effect.» (RESIST); un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Immunity to Fracture Effect.» (RESIST) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Luna Snow (sus 6 variantes) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «30% chance to become immune to Cold Damage.» (COLD IMMUNITY) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Sentry — Marvel Studios' Thunderbolts* | Liderazgo (secundario): no se pudo derivar de la Leader Skill: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Silk (sus 3 variantes) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Bleed: Deals additional 10% Damage every 0.7 sec. (Removes Elasticity)» (BLEED) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Sister Grimm (base, All-New, All-Different) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates an energy Shield equal to 30% of Max HP» (ENERGY SHIELD) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Sister Grimm (Runaways, Princess Tsukimi) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates an energy Shield equal to 60% of Max HP» (ENERGY SHIELD) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| White Tiger (sus 2 variantes) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Bleed: Deals additional 10% Damage every 0.7 sec. (Removes Elasticity)» (BLEED) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Wong (Marvel Studios' Doctor Strange 2, What If... Zombies?!) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «100% chance to grant All Damage Immunity» (ALL DAMAGE IMMUNE) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Yellowjacket (sus 2 variantes) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Paralyze» (PARALYZE) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |

### Soporte que Leads & Supports no publica

21 casos en 15 personajes y 21 variantes. Según el análisis, la pasiva le da algo al equipo, y Leads & Supports no publica ese soporte (ni en su slot ni con el nombre de la skill): la sinergia no lo cuenta.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Blue Marvel — Classic | Pasiva de uniforme «Classic» le da al equipo «Daño contra ciertos rivales», «Resistencias elementales», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Deadpool (Lady Deadpool, Holiday Party) | Pasiva T2 «Merc With A Mouth» le da al equipo «Recuperación», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Ghost — Marvel Studios' Thunderbolts* | Pasiva de uniforme «Marvel Studios' Thunderbolts*» le da al equipo «Le saca todos los debuffs», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Green Goblin — Gold Goblin | Pasiva T2 «OZ Formula» le da al equipo «Daño contra ciertos rivales», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Hulkbuster (Iron Man Mark 44) — 3099 | Pasiva «Heavy Duty Exo-Frame» le da al equipo «Vida», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Invisible Woman (base, Future Foundation, Classic) | Pasiva «Invisibility Shift» le da al equipo «Barrera», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Luna Snow | Pasiva «Encore» le da al equipo «Inmune a un elemento (probabilidad)», «Todas las velocidades», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Molecule Man | Pasiva «Unbound Being» le da al equipo «Menos daño reflejado recibido», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Red Skull — The Crimson Fall | Pasiva T2 «Age of Malice» le da al equipo «Daño contra ciertos rivales», «Todos los ataques básicos», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Rhino — Uncanny Spider-Man | Pasiva de uniforme «Uncanny Spider-Man» le da al equipo «Ignora la reducción de daño del rival (no jefes)», «Menos daño de golpes en cadena», «Vida», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Sister Grimm — Princess Tsukimi | Pasiva «Healing Sound» le da al equipo «Curación», «Le saca todos los debuffs», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| The Thing — Future Foundation | Pasiva de uniforme «Future Foundation» le da al equipo «Vida», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| The Thing — Classic | Pasiva de uniforme «Classic» le da al equipo «Vida», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Venom — Anti-Venom | Pasiva de uniforme «Anti-Venom» le da al equipo «Curación», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Venom — War of the Realms | Pasiva de uniforme «War of the Realms» le da al equipo «Curación», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Venom — King in Black | Pasiva de uniforme «King in Black» le da al equipo «Curación», «Daño crítico», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Wasp (Nadia Van Dyne) | Pasiva «Winsome Wasp» le da al equipo «Todos los ataques básicos», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |
| Wenwu | Pasiva «Legendary Power» le da al equipo «Vida», y Leads & Supports no lo publica | thanosvibs (Leads & Supports) o a mano desde la skill |

### Nombre en Leads & Supports distinto del de la skill

17 casos en 15 personajes y 16 variantes. Leads & Supports nombra el soporte o el liderazgo con el nombre de otra skill de la variante o con uno que la variante no tiene. El enlace del «Por qué» busca la skill por ese nombre: con el de otra skill, cae en ella (la «Pasiva 4★ (secundaria)» de Jeff the Land Shark lleva a su Activa 5; la Tier-2 de Polaris — Uncanny X-Men, a su Activa 1).

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Apocalypse — Marvel Animation's X-Men '97 (Young Apocalypse) | Liderazgo: Leads & Supports la llama «Unavoidable Apocalypse», que es su Pasiva T2; su Liderazgo se llama «End of Days» | el juego o foros |
| Arachknight — Arachknight 2099 | Liderazgo: Leads & Supports la llama «Unstoppable», que no es ninguna de sus skills; su Liderazgo se llama «Guardian of Dimensions» | el juego o foros |
| Bullseye — Wastelanders | Liderazgo: Leads & Supports la llama «Correct Arrow», que no es ninguna de sus skills; su Liderazgo se llama «Assassin's Eye» | el juego o foros |
| Destroyer — The Mighty Thor | Pasiva 4★: Leads & Supports la llama «God of Thunder Armor», que es su Activa 5; su Pasiva se llama «Mech Thor» | el juego o foros |
| Electro — Spider-Man: No Way Home | Pasiva 4★: Leads & Supports la llama «Unstable Current», que no es ninguna de sus skills; su Pasiva se llama «Electric Battlefield» | el juego o foros |
| Falcon (Joaquin Torres) | Pasiva 4★: Leads & Supports la llama «Captain's Wingman», que es su Pasiva T2; su Pasiva se llama «Agile Flight» | el juego o foros |
| Jeff the Land Shark | Pasiva 4★ (secundaria): Leads & Supports la llama «Jeff's Cuddle Buddy», que es su Activa 5; su Pasiva se llama «Guardian of the Deep» | el juego o foros |
| Lash (sus 2 variantes) | Liderazgo: Leads & Supports la llama «Judgement of the Lord», que no es ninguna de sus skills; su Liderazgo se llama «Judgment of the Lord» | el juego o foros |
| Marvel Boy | Pasiva 4★: Leads & Supports la llama «Nanotech Core», que no es ninguna de sus skills; su Pasiva se llama «Nanotech Care» | el juego o foros |
| Polaris — Uncanny X-Men | Pasiva de Tier-2: Leads & Supports la llama «Magnetic Pulse», que es su Activa 1; su Pasiva T2 se llama «Antipolarity Effect» | el juego o foros |
| Spider-Man (Miles Morales) — Anniversary Special | Liderazgo: Leads & Supports la llama «Quick Recovery», que no es ninguna de sus skills; su Liderazgo se llama «Spider Party» | el juego o foros |
| Spider-Woman — Spider-Man: Across the Spider-Verse | Liderazgo: Leads & Supports la llama «Spider-Leader», que no es ninguna de sus skills; su Liderazgo se llama «Mother of Spider» | el juego o foros |
| Taskmaster — Marvel Studios' Thunderbolts* | Pasiva de Tier-2: Leads & Supports la llama «Flawless Strategy», que no es ninguna de sus skills; su Pasiva T2 se llama «Training Thunderbolts*» | el juego o foros |
| Toxin | Liderazgo: Leads & Supports la llama «Anger Manifest», que es su Pasiva T2; su Liderazgo se llama «Red Threat» | el juego o foros |
| Victorious — Emperor Guarder | Liderazgo: Leads & Supports la llama «For Victory!», que no es ninguna de sus skills; su Liderazgo se llama «Latverian Vanguard»; Pasiva 4★: Leads & Supports la llama «Latverian Champion», que no es ninguna de sus skills; su Pasiva se llama «Spear of Latveria» | el juego o foros |

### Valores del artefacto incompletos

5 casos en 5 personajes. El texto del artefacto usa valores que thanosvibs no publica en esos niveles de estrellas: la app los marca «sin dato» (docs/AUDITORIA.md, sección 6).

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Domino (sus 3 variantes) | Probability Power: thanosvibs no publica todos sus valores en 3★, 4★ y 5★ | la wiki (página Artifact) o el juego |
| Hulkbuster (Iron Man Mark 44) (sus 5 variantes) | Big Armor: thanosvibs no publica todos sus valores en 3★, 4★, 5★ y 6★ | la wiki (página Artifact) o el juego |
| Inferno (sus 2 variantes) | The Flames of Attilan: thanosvibs no publica todos sus valores en 3★, 4★ y 5★ | la wiki (página Artifact) o el juego |
| Sunspot | Solar: thanosvibs no publica todos sus valores en 3★, 4★ y 5★ | la wiki (página Artifact) o el juego |
| Wiccan | Future Demiurge: thanosvibs no publica todos sus valores en 3★, 4★, 5★ y 6★ | la wiki (página Artifact) o el juego |

### Strikers

122 casos en 122 personajes. La app toma los strikers de la pestaña Striker de la página de la wiki: sin ella no tiene los suyos (docs/AUDITORIA.md, sección 11). Que existan en el juego para todos es [Probable].

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Adam Warlock (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Agent Venom (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Angel (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Annihilus | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Ant-Man (sus 7 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Apocalypse (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Arachknight (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Athena | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Beast (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Bishop (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Black Bolt (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Black Knight | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Black Swan | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Black Widow (sus 12 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Captain America (sus 15 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Carnage (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Cassandra Nova | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Cassie Lang | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Colossus (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Cyclops (sus 6 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Destroyer (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Doctor Doom (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Doctor Octopus (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Doctor Voodoo (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Elektra (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Emma Frost (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Exodus | la pestaña Striker de la wiki no trae ninguna fila que se pueda leer | la wiki (pestaña Striker), el juego o foros |
| Falcon (Joaquin Torres) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Fantomex | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Franklin Richards | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Galactus | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Gambit (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Ghost Panther | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Ghost Rider (Robbie Reyes) (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Giant-Man (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Gorr (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Green Goblin (sus 6 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Gwenpool (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Hades (Pluto) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Havok | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Hercules | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Hope Summers | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Hulk (sus 10 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Iceman (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Ikon | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Iron Hammer | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Ironheart (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Jean Grey (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Jeff the Land Shark | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Jubilee (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Juggernaut (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Kahhori | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Kang the Conqueror (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Kid Omega (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Kitty Pryde (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Kraven The Hunter (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Leader | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Lizard | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| M'Baku | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Madelyne Pryor (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Magik (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Magneto (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Man-Thing | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Mantis (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Marvel Boy | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Maximus | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Moon Girl (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Morgan le Fay (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Morph | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Ms. Marvel (Kamala Khan) (sus 6 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Namor (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Nightcrawler (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Nova (Sam Alexander) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Odin (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Okoye | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Omega Red | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Polaris (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Professor X (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Psylocke (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Punisher (sus 8 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Quasar (Wendell Vaughn) | la pestaña Striker de la wiki no trae ninguna fila que se pueda leer | la wiki (pestaña Striker), el juego o foros |
| Quicksilver (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Rachel Summers (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Rhino (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Rogue (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Sabretooth (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Scarlet Spider (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Scarlet Witch (sus 8 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Scorpion (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Scream (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Shadow Shell (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| She-Hulk (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Shuri (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Silver Samurai | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Silver Surfer (Shalla-Bal) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Skurge | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Sleeper | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Songbird | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Spider-Man (sus 13 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Spider-Man (Miles Morales) (sus 6 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Spot | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Squirrel Girl (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Storm (sus 5 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Sun Bird (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Sunspot | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Sylvie | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| The Hood | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Thor (Jane Foster) (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Titania (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Toxin | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| U.S. Agent | la pestaña Striker de la wiki no trae ninguna fila que se pueda leer | la wiki (pestaña Striker), el juego o foros |
| Valeria Richards | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Valkyrie (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Venom (sus 7 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Venus (Aphrodite) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| War Tiger (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Wasp (Nadia Van Dyne) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Weapon Hex (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| White Tiger (sus 2 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Wolverine (sus 8 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| X-23 (sus 4 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Zeus | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |

### Bonos de equipo que faltan

32 casos en 32 personajes. La app toma los bonos de la sección Team Bonus de la wiki y de lo que se vio en el juego. Sin ninguno, o solo con los del juego, faltan los demás [Probable].

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Annihilus | solo tiene los 2 que se vieron en el juego: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Athena | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Black Knight | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Black Swan | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Cassandra Nova | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Exodus | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Falcon (Joaquin Torres) | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Franklin Richards | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Galactus | solo tiene los 2 que se vieron en el juego: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Hades (Pluto) | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Havok | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Hercules | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Hope Summers | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Ikon | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Jeff the Land Shark | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Kahhori | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Leader | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Madelyne Pryor (sus 2 variantes) | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Man-Thing | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Marvel Boy | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Morph | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Okoye | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Quasar (Wendell Vaughn) | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Silver Surfer (Shalla-Bal) | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Sleeper | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Sunspot | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Sylvie | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| The Hood | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| U.S. Agent | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Valeria Richards | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Venus (Aphrodite) | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
| Zeus | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |

### Bono de equipo sin nombre

2 casos en 2 personajes. Ninguna página de la wiki de sus integrantes le da nombre (docs/AUDITORIA.md, sección 10).

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Thor (Jane Foster) (sus 2 variantes) | el bono con Titania no tiene nombre en ninguna página de la wiki | capturas del juego o foros |
| Titania (sus 2 variantes) | el bono con Thor (Jane Foster) no tiene nombre en ninguna página de la wiki | capturas del juego o foros |

### Sin C.T.P. en la guía de armado

2 casos en 2 personajes. La fila del personaje en la guía de armado está hecha pero no trae ningún C.T.P., y ni la guía ni la Ideal CTP List dicen que no vale la pena: las tarjetas de equipo dicen «sin dato en la guía». La ficha muestra el de la Ideal CTP List.

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Jubilee (sus 2 variantes) | su fila en la guía de armado no trae ningún C.T.P.; la Ideal CTP List (CrisisCardio) lo pone en «Liberation» | la guía de armado o foros |
| Leader | su fila en la guía de armado no trae ningún C.T.P.; la Ideal CTP List (CrisisCardio) lo pone en «Insight» | la guía de armado o foros |

### Sin el C.T.P. de su contexto en la guía de armado

31 casos en 27 personajes y 29 variantes. La variante tiene función en el contexto (está en sus tier lists) y la fila del personaje en la guía de armado no tiene el C.T.P. meta de ese contexto: su tarjeta de equipo dice «sin dato en la guía».

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Abomination | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Ancient One (Unleashed Mystic, The Monk of Kamar-Taj) | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Ares — Punisher | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Beast — Marvel Animation's X-Men '97 | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Black Cat — Queen in Black | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Bullseye — Wastelanders | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Dazzler — X-Song | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Deadpool — Marvel Studios' Deadpool & Wolverine (Nicepool) | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Gambit — X-Men Year-End Party | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Hawkeye — Wastelanders | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Invisible Woman — The Fall of the Fantastic Four | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Invisible Woman — Marvel Studios' The Fantastic Four: First Steps | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP; tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Kid Omega — Uncanny X-Men | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| M'Baku | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Malekith — All-New, All-Different | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Mephisto — Master of Hell | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Nick Fury — Secret Avengers | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Nova (Richard Rider) — Marvel Cosmic Invasion | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP; tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Proxima Midnight — Dark Obsidian Armor | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Psylocke — Summer Vacation | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Ronan — Annihilators | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Shuri — Marvel Studios' Black Panther: Wakanda Forever (Black Panther) | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Sin — Rage Returned | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Valeria Richards | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Victorious — Emperor Guarder | tiene función en PvP y la guía de armado no le da el C.T.P. meta de PvP | la guía de armado o foros |
| Wolverine — Marvel Studios' Deadpool & Wolverine | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Wong — What If... Zombies?! | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |
| Yelena Belova — Marvel Studios' Thunderbolts* | tiene función en PvE y la guía de armado no le da el C.T.P. meta de PvE | la guía de armado o foros |

### Fila vacía en la guía de armado

32 casos en 32 personajes. La guía de armado tiene una fila por personaje y esta no tiene nada de lo que la guía completa (C.T.P., ISO-8, obelisco, lugar en su tier list, cómo se consigue): no está hecha. La ficha y las tarjetas de equipo dicen «sin dato».

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Annihilus | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Competition» |
| Apocalypse (sus 4 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Conquest» |
| Athena | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Insight» |
| Baron Mordo (sus 3 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| Black Knight | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Liberation» |
| Echo (sus 3 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Liberation» |
| Falcon (sus 7 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Energy» |
| Galactus | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Conquest» |
| Gorilla-Man | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| Hades (Pluto) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Competition» |
| Hercules | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Conquest» |
| Hulk (Amadeus Cho) (sus 4 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Insight» |
| Hulkbuster (Iron Man Mark 44) (sus 5 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Regeneration» |
| Ironheart (sus 3 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Insight» |
| Jeff the Land Shark | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Liberation» |
| Killmonger (sus 2 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| Madelyne Pryor (sus 2 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Conquest» |
| Man-Thing | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| Marvel Boy | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| Morph | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Insight» |
| Nebula (sus 5 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| Scarlet Spider (sus 3 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Insight» |
| Silver Samurai | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Liberation» |
| Silver Surfer (Shalla-Bal) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Conquest» |
| Spectrum (sus 2 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| Sun Bird (sus 2 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| The Hood | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| The Thing (sus 5 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Insight» |
| U.S. Agent | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Not worth» |
| Ultron (sus 6 variantes) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Destruction» |
| Venus (Aphrodite) | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Insight» |
| Zeus | su fila en la guía de armado está vacía: sin C.T.P., ISO-8, obelisco, lugar en su tier list ni cómo se consigue | la guía de armado o foros; la Ideal CTP List (CrisisCardio) lo pone en «Competition» |

### ISO-8 u obelisco sin dato en la guía de armado

6 casos en 6 personajes. La fila del personaje en la guía de armado está hecha pero no trae el ISO-8 o el obelisco, y la guía no dice que no valga la pena armarlo: la pestaña Armado dice «—».

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Dazzler (sus 2 variantes) | su fila en la guía de armado no trae ISO-8 ni obelisco | la guía de armado o foros |
| Deadpool (sus 9 variantes) | su fila en la guía de armado no trae ISO-8 ni obelisco | la guía de armado o foros |
| Exodus | su fila en la guía de armado no trae obelisco | la guía de armado o foros |
| Franklin Richards | su fila en la guía de armado no trae obelisco | la guía de armado o foros |
| Jubilee (sus 2 variantes) | su fila en la guía de armado no trae ISO-8 ni obelisco | la guía de armado o foros |
| Wolverine (sus 8 variantes) | su fila en la guía de armado no trae ISO-8 ni obelisco | la guía de armado o foros |

### Retrato o ícono

3 casos en 1 personaje y 3 variantes. La app baja lo que publica datos.json; sin el archivo, no muestra el retrato o el ícono. El ícono del bando Neutral no lo baja el build: que thanosvibs tenga uno es [Conjetura].

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Destroyer (sus 3 variantes) | el ícono de «Neutral» no está en datos.json | thanosvibs (imágenes) |

### Rotación

189 casos en 109 personajes y 189 variantes. thanosvibs publica rotaciones por uniforme, y la guía de armado, la del mejor uniforme de cada personaje. Se dice si otro uniforme del personaje tiene la suya.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Agent 13 (sus 2 variantes) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Annihilus | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Captain America (Sharon Rogers) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Star Light Armor, Dark Star Armor, Star Night Armor, Light Sirius Armor, Poseidon Armor y Arctic Warrior; la guía de armado tiene la de Arctic Warrior |
| Dazzler — X-Song | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
| Drax (sus 4 variantes) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Ebony Maw | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Infinity War, Dark Obsidian Armor y General's Hand |
| Echo — Marvel Studios' Hawkeye (Maya Lopez) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Marvel Studios' Echo (Maya Lopez (Echo)); la guía de armado tiene la de Marvel Studios' Echo (Maya Lopez (Echo)) |
| Electro | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Spider-Man: No Way Home; la guía de armado tiene la de Spider-Man: No Way Home |
| Elsa Bloodstone (base, Secret Wars: Marvel Zombies) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Monsters Unleashed! (MFF Variant); la guía de armado tiene la de Monsters Unleashed! (MFF Variant) |
| Emma Frost — Summer Queen | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Marvel NOW!, Phoenix Five y Hellfire Gala |
| Enchantress | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Summer Days y War of the Realms; la guía de armado tiene la de War of the Realms |
| Falcon (base, All-New Captain America, Marvel Studios' Captain America: Civil War) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Legacy, Marvel Studios' The Falcon and the Winter Soldier (Captain America (Sam Wilson)), What If... Zombies?! y Marvel Studios' Captain America: Brave New World (Captain America (Sam Wilson)); la guía de armado tiene la de Marvel Studios' Captain America: Brave New World (Captain America (Sam Wilson)) |
| Fandral | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Galactus | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Gamora (base, All-New, All-Different) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Guardians of the Galaxy 2, Requiem, Marvel Studios' Guardians of the Galaxy 3 y Wastelanders; la guía de armado tiene la de Wastelanders |
| Ghost (base, Marvel Studios' Ant-Man and the Wasp) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Thunderbolts*; la guía de armado tiene la de Marvel Studios' Thunderbolts* |
| Ghost Rider (base, 70's Classic) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Inhumans: Attilan Rising, King of Hell, Rage Returned y Savage Avengers; la guía de armado tiene la de Savage Avengers |
| Ghost Rider (Robbie Reyes) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Lord of Vengeance; la guía de armado tiene la de Lord of Vengeance |
| Giant-Man (base, Modern (Goliath)) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Ultron Pym |
| Gilgamesh | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Eternals; la guía de armado tiene la de Marvel Studios' Eternals |
| Gorgon | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Green Goblin — Ultimate | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Dark Avengers, Spider-Man: No Way Home, Red Goblin y Gold Goblin |
| Groot (base, Secret Wars: Thors, Marvel Studios' Avengers: Infinity War, Planet X Palm) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Guardians of the Galaxy 2, Snowflake Festival y Marvel Studios' Guardians of the Galaxy 3 |
| Hawkeye (base, Avengers: Age of Ultron, Marvel Studios' Captain America: Civil War, Classic) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Endgame (Ronin), Marvel Studios' Hawkeye (Hero Suit) y Wastelanders; la guía de armado tiene la de Wastelanders |
| Hawkeye (Kate Bishop) — Young Avengers | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Marvel Studios' Hawkeye |
| Hela (base, Asgard Invasion) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Thor: Ragnarok y Marvel Studios' What If...?; la guía de armado tiene la de Marvel Studios' What If...? |
| Hellstorm — TVA | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
| Hercules | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Hogun | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Hulk (base, Secret Wars: Future Imperfect (Maestro), World War Hulk, Marvel Studios' Thor: Ragnarok) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Endgame, Team Suit, Immortal Hulk, Fear Itself, Titan y Marvel Studios' Spider-Man: Brand New Day; la guía de armado tiene la de Marvel Studios' Spider-Man: Brand New Day |
| Hulkbuster (Iron Man Mark 44) (base, Heavy Duty Armor (Hulkbuster (Iron Man Mark 43))) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Infinity War (Hulkbuster 2.0), 3099 y Celestial Hulkbuster (Hulkbuster); la guía de armado tiene la de Celestial Hulkbuster (Hulkbuster) |
| Human Torch — Marvel Studios' The Fantastic Four: First Steps | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Future Foundation, Classic y The Fall of the Fantastic Four |
| Hyperion | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Classic y Enter the Phoenix; la guía de armado tiene la de Enter the Phoenix |
| Invisible Woman — Marvel Studios' The Fantastic Four: First Steps | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Future Foundation, Classic y The Fall of the Fantastic Four |
| Iron Fist (base, New Avengers, All-New, All-Different) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Iron Fist y The Living Weapon; la guía de armado tiene la de The Living Weapon |
| Iron Man (base, Avengers: Age of Ultron, Secret Wars: 2099, Marvel Studios' Captain America: Civil War, Marvel Studios' Avengers: Endgame, Team Suit) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Infinity War, Avengers 3099, Superior Iron Man, Back to Basics y Model Nil; la guía de armado tiene la de Model Nil |
| Ironheart — Marvel Television's Ironheart | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Black Panther: Wakanda Forever (Riri Williams) |
| Jeff the Land Shark | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Juggernaut — Savage Avengers | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Fear Itself |
| Kang the Conqueror — Rama-Tut | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
| Karnak (sus 2 variantes) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Kid Kaiju (sus 2 variantes) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Kid Omega — Uncanny X-Men | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
| Killmonger | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Black Panther (Erik Killmonger (Black Panther)); la guía de armado tiene la de Marvel Studios' Black Panther (Erik Killmonger (Black Panther)) |
| Kingpin (base, Secret Wars: Armor Wars, Marvel Television's Daredevil: Born Again) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Winter Criminal |
| Lash (sus 2 variantes) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Lizard | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Luke Cage (base, All-New, All-Different) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Luke Cage y Uptown Suit; la guía de armado tiene la de Uptown Suit |
| M.O.D.O.K. (base, CAPDOC) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de SPIDOC y Ant-Man and the Wasp: Quantumania; la guía de armado tiene la de Ant-Man and the Wasp: Quantumania |
| Madelyne Pryor — Winter Queen | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
| Magik — Marvel Rivals | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Phoenix Five y Krakoan Winter |
| Magneto (base, Marvel NOW!) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de House of X, Krakoan Winter y Marvel Animation's X-Men '97 |
| Makkari | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Eternals; la guía de armado tiene la de Marvel Studios' Eternals |
| Malekith (base, All-New, All-Different) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de War of the Realms; la guía de armado tiene la de War of the Realms |
| Mantis | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Guardians of the Galaxy 3; la guía de armado tiene la de Marvel Studios' Guardians of the Galaxy 3 |
| Minn-Erva | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Captain Marvel; la guía de armado tiene la de Marvel Studios' Captain Marvel |
| Mister Fantastic — Marvel Studios' The Fantastic Four: First Steps | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Future Foundation, The Maker y The Fall of the Fantastic Four |
| Mockingbird (sus 3 variantes) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Ms. Marvel (Kamala Khan) (base, Karachi Costume) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Inhumans: Attilan Rising, Marvel Studios' Ms. Marvel, Marvel Studios' The Marvels y Marvel Animation's Marvel Zombies; la guía de armado tiene la de Marvel Animation's Marvel Zombies |
| Nebula (base, Classic) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Endgame, Team Suit y Marvel Studios' What If...? (Super Nova Nebula); la guía de armado tiene la de Marvel Studios' What If...? (Super Nova Nebula) |
| Nick Fury — Secret Avengers | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Marvel Studios' Captain Marvel y Marvel Studios' The Marvels |
| Nightcrawler (X-Force, Classic) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
| Odin | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de All-Father, Avengers 1,000,000 BC y Lord of Asgard; la guía de armado tiene la de Lord of Asgard |
| Phil Coulson (base, A.O.S. Season 3) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Winter Ops; la guía de armado tiene la de Winter Ops |
| Polaris — Uncanny X-Men | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
| Punisher (base, Noir, War Journal) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Daredevil, Marvel Legacy, Cosmic Ghost Rider, Fist of the Beast y Marvel Television's Daredevil: Born Again; la guía de armado tiene la de Marvel Television's Daredevil: Born Again |
| Quicksilver (base, Marvel Legacy) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Uncanny Avengers, Summer Days y Mighty Avengers; la guía de armado tiene la de Mighty Avengers |
| Red Hulk | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel NOW!, Symbiote of Vengeance y Marvel Studios' Captain America: Brave New World; la guía de armado tiene la de Marvel Studios' Captain America: Brave New World |
| Red Skull (base, Secret Wars: Red Skull, The Crimson Fall) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Hydra Armor; la guía de armado tiene la de Hydra Armor |
| Rocket Raccoon (base, All-New, All-Different, Guardians of the Galaxy 2, Marvel Studios' Avengers: Infinity War) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Endgame, Team Suit y Marvel Studios' Guardians of the Galaxy 3; la guía de armado tiene la de Marvel Studios' Guardians of the Galaxy 3 |
| Rogue — Age of Apocalypse | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Uncanny Avengers, Excalibur y Winter Ops; la guía de armado tiene la de Winter Ops |
| Ronan | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Annihilation, Marvel Studios' Captain Marvel y Annihilators; la guía de armado tiene la de Annihilators |
| Sabretooth | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Uncanny Avengers y Ultimate; la guía de armado tiene la de Ultimate |
| Satana | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Legacy y Ascended One; la guía de armado tiene la de Ascended One |
| Scarlet Spider — Gift Deliverer | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Dark Web (Chasm) |
| Scarlet Witch (base, Marvel Studios' Avengers: Infinity War) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Uncanny Avengers, All-New, All-Different, Marvel Studios' WandaVision, Marvel Studios' Doctor Strange 2, Scarlet Witch y Marvel Animation's Marvel Zombies; la guía de armado tiene la de Marvel Animation's Marvel Zombies |
| Sentinel (base, Stark Sentinels Mk II) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Nimrod The Lesser |
| Sentry — Marvel Studios' Thunderbolts* | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Merged |
| Shang-Chi (base, Marvel Animation's Marvel Zombies) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Shang-Chi |
| She-Hulk (base, All-New) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Fantastic Four, Avengers y Marvel Studios' She-Hulk: Attorney at Law; la guía de armado tiene la de Marvel Studios' She-Hulk: Attorney at Law |
| Shuri | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Black Panther, Black Panther: Wakanda Forever y Marvel Studios' Black Panther: Wakanda Forever (Black Panther); la guía de armado tiene la de Marvel Studios' Black Panther: Wakanda Forever (Black Panther) |
| Sif | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Modern y Asgard Invasion; la guía de armado tiene la de Asgard Invasion |
| Silver Samurai | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Silver Surfer | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Black y Void Knight |
| Silver Surfer (Shalla-Bal) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| Sister Grimm — Princess Tsukimi | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, All-New, All-Different y Runaways; la guía de armado tiene la de Runaways |
| Spider-Gwen | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Gwendolyne Stacy, Gwenom y Spider-Man: Across the Spider-Verse; la guía de armado tiene la de Spider-Man: Across the Spider-Verse |
| Spider-Man (base, Secret Wars: Renew Your Vows, All-New, All-Different, Marvel Studios' Captain America: Civil War, Spider-Man: Homecoming Homemade Suit, Spider-Man: Far From Home) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Infinity War, Spider-Man: Far From Home (Stealth Suit), Spider-Man: No Way Home (Integrated Suit), Spider-Man: No Way Home (Black & Gold Suit), Back to Basics, The Symbiote Suit y Marvel Studios' Spider-Man: Brand New Day; la guía de armado tiene la de Marvel Studios' Spider-Man: Brand New Day |
| Spider-Man (Miles Morales) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Into the Spider-Verse, Absolute Carnage, Anniversary Special, Spider-Man: Across the Spider-Verse y Ancient Curse; la guía de armado tiene la de Ancient Curse |
| Star-Lord (base, Space Armor) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Guardians of the Galaxy 2, Marvel Studios' Avengers: Infinity War, Grounded, Marvel Studios' Guardians of the Galaxy 3 y Wastelanders; la guía de armado tiene la de Wastelanders |
| Storm — X-Men Red | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Inhumans vs X-Men, Krakoan Summer y Marvel Animation's X-Men '97 |
| Stryfe — The Tyrant of Spring | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Classic |
| Sun Bird — Moon Temple Defenders | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
| Taskmaster — Marvel Studios' Thunderbolts* | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Marvel Studios' Black Widow |
| Thanos (Secret Wars: Infinity, Annihilation) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Marvel Studios' Avengers: Infinity War, Marvel Studios' Avengers: Endgame, Obsidian King, Wise Harvester y Thanos Wins |
| The Thing (base, Future Foundation, Marvel Studios' The Fantastic Four: First Steps) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Classic y The Fall of the Fantastic Four |
| Thor (base, Avengers: Age of Ultron, Unworthy) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Thor: Ragnarok, Marvel Studios' Avengers: Infinity War, Marvel Studios' Avengers: Endgame, Team Suit, Herald of Thunder, Marvel Studios' Thor: Love and Thunder y All-Father Reborn; la guía de armado tiene la de All-Father Reborn |
| Ultron (base, Avengers: Age of Ultron (Ultron Prime), Avengers: Age of Ultron (Ultron Mark 1), Avengers: Age of Ultron (Ultron Mark 3)) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' What If...? (Infinity Ultron) y All-Father Ultron; la guía de armado tiene la de All-Father Ultron |
| Venom (base, Secret Wars: Marvel Zombies, Anti-Venom) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de War of the Realms, King in Black, Warstar y Snow Symbiote; la guía de armado tiene la de Snow Symbiote |
| Vision — Ultimate Vision | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Avengers: Age of Ultron, Uncanny Avengers y Marvel Studios' WandaVision |
| Volstagg | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| War Machine (base, Iron Patriot, Avengers: The Initiative, Marvel Studios' Captain America: Civil War, Marvel Studios' Avengers: Infinity War) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Endgame, Team Suit, 3099 y Invincible Iron Man; la guía de armado tiene la de Invincible Iron Man |
| Warwolf | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
| White Tiger | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Television's Daredevil: Born Again; la guía de armado tiene la de Marvel Television's Daredevil: Born Again |
| Winter Soldier (base, Marvel Studios' Captain America: Civil War, Captain America) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Avengers: Infinity War, Marvel Studios' The Falcon and the Winter Soldier, Revolution y Marvel Studios' Thunderbolts*; la guía de armado tiene la de Marvel Studios' Thunderbolts* |
| Wolverine (Age of Apocalypse, All-New Marvel NOW!) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, X-Force, House of X, Enter the Phoenix, X Deaths of Wolverine y Marvel Studios' Deadpool & Wolverine; la guía de armado tiene la de Marvel Studios' Deadpool & Wolverine |
| Wong (base, Marvel Studios' Doctor Strange) | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de Marvel Studios' Doctor Strange 2 y What If... Zombies?!; la guía de armado tiene la de What If... Zombies?! |
| Yelena Belova — Marvel Studios' Thunderbolts* | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Marvel Studios' Black Widow y Marvel Studios' Black Widow (Snow Suit) |
| Yondu — All-New, All-Different | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base, Guardians of the Galaxy 2 y Summer Vacation; la guía de armado tiene la de Summer Vacation |

## Por personaje

Los personajes con algún faltante, en orden alfabético: primero lo del personaje y después cada variante incompleta. El detalle está en las tablas de arriba.

<details><summary>Abomination: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Base:** C.T.P. de su contexto: PvE

</details>

<details><summary>Adam Warlock: 4 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** código sin nombre: Striker
- **Infinity Countdown:** código sin nombre: Striker
- **Marvel Studios' Guardians of the Galaxy 3:** código sin nombre: Striker

</details>

<details><summary>Aero: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** instinto

</details>

<details><summary>Agent 13: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** instinto
- **Base:** rotación
- **Marvel Studios' Captain America: Civil War:** rotación

</details>

<details><summary>Agent Venom: 6 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Agent Anti-Venom:** marcador sin resolver: Pasiva de uniforme
- **Classic:** $TIME sin duración: Pasiva (2)
- **Guardians of the Galaxy:** $TIME sin duración: Pasiva (2)

</details>

<details><summary>Ancient One: 6 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **Marvel Studios' Doctor Strange:** «Give Power» vacío: Striker
- **Unleashed Mystic:** «Give Power» vacío: Striker; C.T.P. de su contexto: PvE
- **The Monk of Kamar-Taj:** «Give Power» vacío: Striker; C.T.P. de su contexto: PvE

</details>

<details><summary>Angel: 5 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** código sin nombre: Striker
- **X-Force (Archangel):** código sin nombre: Striker
- **All-New X-Men:** código sin nombre: Striker
- **Fallen One:** código sin nombre: Striker

</details>

<details><summary>Angela: 1 faltante, 1 de 4 variantes incompletas</summary>

- **Secret Wars: 1602 Witch Hunter Angela:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Annihilus: 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** rotación

</details>

<details><summary>Ant-Man: 2 faltantes, 7 de 7 variantes incompletas</summary>

- **Personaje:** strikers
- **Ant-Man and the Wasp: Quantumania:** $TIME sin duración: Pasiva T2

</details>

<details><summary>Apocalypse: 3 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers; fila vacía en la guía de armado
- **Marvel Animation's X-Men '97 (Young Apocalypse):** nombre en Leads & Supports: Liderazgo

</details>

<details><summary>Arachknight: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Arachknight 2099:** nombre en Leads & Supports: Liderazgo

</details>

<details><summary>Ares: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** $TIME sin duración: Pasiva T2
- **Punisher:** $TIME sin duración: Pasiva T2; C.T.P. de su contexto: PvE

</details>

<details><summary>Athena: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Baron Mordo: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado

</details>

<details><summary>Beast: 4 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Age of Apocalypse:** skill sin efectos: Pasiva de uniforme
- **Uncanny X-Men:** skill sin efectos: Pasiva de uniforme
- **Marvel Animation's X-Men '97:** C.T.P. de su contexto: PvP

</details>

<details><summary>Beta Ray Bill: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** $TIME sin duración: Pasiva; código sin nombre: Striker
- **Beta Ray Bill:** $TIME sin duración: Pasiva; código sin nombre: Striker

</details>

<details><summary>Bishop: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Black Bolt: 1 faltante, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Black Cat: 7 faltantes, 4 de 5 variantes incompletas</summary>

- **Base:** código sin nombre: Pasiva T2 (2)
- **Claws:** código sin nombre: Pasiva T2 (2)
- **All-New, All-Different:** código sin nombre: Pasiva T2 (2)
- **Queen in Black:** C.T.P. de su contexto: PvP

</details>

<details><summary>Black Dwarf: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Marvel Studios' Avengers: Infinity War (Cull Obsidian):** código sin nombre: Activa 3

</details>

<details><summary>Black Knight: 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** instinto; strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Black Panther: 1 faltante, 1 de 5 variantes incompletas</summary>

- **Marvel Studios' Captain America: Civil War:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Black Swan: 9 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** falta la skill: Pasiva, Pasiva T2, Activa 4, Activa 5, Definitiva; sin recarga: Activa 3; $TIME sin duración: Activa 3

</details>

<details><summary>Black Widow: 2 faltantes, 12 de 12 variantes incompletas</summary>

- **Personaje:** strikers
- **Venomous:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Blade: 4 faltantes, 3 de 4 variantes incompletas</summary>

- **Base:** liderazgo sin completar: Liderazgo
- **70's Classic:** skill sin efectos: Pasiva de uniforme; liderazgo sin completar: Liderazgo
- **Avengers:** liderazgo sin completar: Liderazgo

</details>

<details><summary>Blue Dragon: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo
- **Moon Temple Defenders:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo

</details>

<details><summary>Blue Marvel: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** instinto
- **Classic:** código sin nombre: Pasiva de uniforme (2); soporte sin Leads & Supports: Pasiva de uniforme

</details>

<details><summary>Bullseye: 2 faltantes, 1 de 4 variantes incompletas</summary>

- **Wastelanders:** nombre en Leads & Supports: Liderazgo; C.T.P. de su contexto: PvE

</details>

<details><summary>Cable: 6 faltantes, 6 de 6 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **X-Force:** «Give Power» vacío: Striker
- **Cable & Deadpool:** «Give Power» vacío: Striker
- **Summer Days:** «Give Power» vacío: Striker
- **X of Swords:** «Give Power» vacío: Striker
- **Heart of Darkness:** «Give Power» vacío: Striker

</details>

<details><summary>Captain America: 6 faltantes, 15 de 15 variantes incompletas</summary>

- **Personaje:** strikers
- **Hydra Supreme:** $TIME sin duración: Pasiva de uniforme
- **Enter the Phoenix:** $TIME sin duración: Pasiva de uniforme
- **Back to Basics:** $TIME sin duración: Pasiva de uniforme
- **What If... Zombies?!:** $TIME sin duración: Pasiva de uniforme
- **Galactic Talon:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Captain America (Sharon Rogers): 15 faltantes, 7 de 7 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker; liderazgo sin completar: Liderazgo; rotación
- **Star Light Armor:** «Give Power» vacío: Striker; liderazgo sin completar: Liderazgo
- **Dark Star Armor:** «Give Power» vacío: Striker; liderazgo sin completar: Liderazgo
- **Star Night Armor:** «Give Power» vacío: Striker; liderazgo sin completar: Liderazgo
- **Light Sirius Armor:** «Give Power» vacío: Striker; liderazgo sin completar: Liderazgo
- **Poseidon Armor:** «Give Power» vacío: Striker; liderazgo sin completar: Liderazgo
- **Arctic Warrior:** «Give Power» vacío: Striker; liderazgo sin completar: Liderazgo

</details>

<details><summary>Captain Marvel: 9 faltantes, 8 de 8 variantes incompletas</summary>

- **Personaje:** instinto
- **Secret Wars: Captain Marvel & The Carol Corps:** skill sin efectos: Pasiva de uniforme
- **Ms. Marvel:** skill sin efectos: Pasiva de uniforme
- **Marvel Studios' Captain Marvel:** skill sin efectos: Pasiva de uniforme
- **Marvel Studios' Avengers: Endgame:** marcador sin resolver: Pasiva de uniforme (2)
- **Marvel Studios' The Marvels:** marcador sin resolver: Pasiva de uniforme (2)
- **Marvel Animation's Marvel Zombies:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Carnage: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Cassandra Nova: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** $TIME sin duración: Pasiva

</details>

<details><summary>Cassie Lang: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Colossus: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Crystal: 6 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **Royal Suit:** «Give Power» vacío: Striker; skill sin efectos: Pasiva de uniforme
- **Fantastic Four:** «Give Power» vacío: Striker; skill sin efectos: Pasiva de uniforme
- **Spring Lady:** «Give Power» vacío: Striker

</details>

<details><summary>Cyclops: 3 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** strikers
- **Age of Apocalypse:** skill sin efectos: Pasiva de uniforme
- **Marvel NOW!:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Daisy Johnson: 4 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** liderazgo sin completar: Liderazgo
- **Modern (Quake):** liderazgo sin completar: Liderazgo
- **Marvel Studios' Agents of S.H.I.E.L.D. (Quake):** skill sin efectos: Pasiva de uniforme; liderazgo sin completar: Liderazgo

</details>

<details><summary>Daken: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Dark Wolverine:** $TIME sin duración: Pasiva

</details>

<details><summary>Daredevil: 2 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** instinto
- **Marvel Television's Daredevil: Born Again:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Dazzler: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** ISO-8 u obelisco en la guía de armado
- **X-Song:** rotación; C.T.P. de su contexto: PvE

</details>

<details><summary>Deadpool: 15 faltantes, 9 de 9 variantes incompletas</summary>

- **Personaje:** ISO-8 u obelisco en la guía de armado
- **X-Force:** $TIME sin duración: Pasiva T2
- **Lady Deadpool:** $TIME sin duración: Pasiva T2; soporte sin Leads & Supports: Pasiva T2
- **Holiday Party:** $TIME sin duración: Pasiva T2; soporte sin Leads & Supports: Pasiva T2
- **30th Anniversary Black Version:** $TIME sin duración: Pasiva T2
- **30th Anniversary White Version:** $TIME sin duración: Pasiva T2
- **April Pools:** objetivo sin nombre: Liderazgo; $TIME sin duración: Pasiva T2
- **Marvel Studios' Deadpool & Wolverine:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo, Pasiva
- **Marvel Studios' Deadpool & Wolverine (Nicepool):** $TIME sin duración: Pasiva; C.T.P. de su contexto: PvE

</details>

<details><summary>Deathlok: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** marcador sin resolver: Pasiva (2)
- **Modern:** marcador sin resolver: Pasiva (2)

</details>

<details><summary>Destroyer: 8 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** sin recarga: Activa 5; retrato o ícono: Neutral
- **Prometheus:** sin recarga: Activa 5; retrato o ícono: Neutral
- **The Mighty Thor:** sin recarga: Activa 5; nombre en Leads & Supports: Pasiva 4★; retrato o ícono: Neutral

</details>

<details><summary>Doctor Doom: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **3099:** «Give Power» vacío: Pasiva de uniforme; $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Doctor Octopus: 7 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** código sin nombre: Striker
- **Superior Spider-Man:** código sin nombre: Pasiva T2, Striker
- **Superior Octopus:** código sin nombre: Striker
- **Spider-Man: No Way Home:** código sin nombre: Striker
- **Ends of the Earth:** código sin nombre: Striker

</details>

<details><summary>Doctor Strange: 5 faltantes, 4 de 7 variantes incompletas</summary>

- **Base:** código sin nombre: Activa 5
- **Marvel Studios' Doctor Strange:** código sin nombre: Activa 5
- **Marvel Studios' Avengers: Infinity War:** código sin nombre: Activa 5
- **Space Suit:** código sin nombre: Activa 5 (2)

</details>

<details><summary>Doctor Voodoo: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Domino: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** valores del artefacto

</details>

<details><summary>Drax: 9 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** rotación
- **Classic:** código sin nombre: Pasiva T2; rotación
- **Annihilation:** $TIME sin duración: Pasiva; código sin nombre: Pasiva T2; marcador sin resolver: Pasiva de uniforme (2); rotación

</details>

<details><summary>Ebony Maw: 5 faltantes, 3 de 4 variantes incompletas</summary>

- **Base:** rotación
- **Dark Obsidian Armor:** marcador sin resolver: Pasiva T2 (2)
- **General's Hand:** marcador sin resolver: Pasiva T2 (2)

</details>

<details><summary>Echo: 10 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** «Give Power» vacío: Striker; $TIME sin duración: Pasiva T2
- **Marvel Studios' Hawkeye (Maya Lopez):** «Give Power» vacío: Striker, Liderazgo; $TIME sin duración: Liderazgo; rotación
- **Marvel Studios' Echo (Maya Lopez (Echo)):** «Give Power» vacío: Striker, Liderazgo; $TIME sin duración: Liderazgo

</details>

<details><summary>Electro: 7 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** $TIME sin duración: Pasiva; rotación
- **Spider-Man: No Way Home:** $TIME sin duración: Pasiva; marcador sin resolver: Pasiva (2); código sin nombre: Pasiva de uniforme; nombre en Leads & Supports: Pasiva 4★

</details>

<details><summary>Elektra: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Elsa Bloodstone: 2 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Secret Wars: Marvel Zombies:** rotación

</details>

<details><summary>Emma Frost: 4 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Phoenix Five:** $TIME sin duración: Pasiva de uniforme
- **Hellfire Gala:** $TIME sin duración: Pasiva de uniforme
- **Summer Queen:** rotación

</details>

<details><summary>Enchantress: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Exodus: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; ISO-8 u obelisco en la guía de armado

</details>

<details><summary>Falcon: 13 faltantes, 7 de 7 variantes incompletas</summary>

- **Personaje:** instinto; fila vacía en la guía de armado
- **Base:** marcador sin resolver: Definitiva; rotación
- **All-New Captain America:** marcador sin resolver: Definitiva; rotación
- **Marvel Studios' Captain America: Civil War:** marcador sin resolver: Definitiva; rotación
- **Marvel Legacy:** marcador sin resolver: Definitiva
- **Marvel Studios' The Falcon and the Winter Soldier (Captain America (Sam Wilson)):** marcador sin resolver: Definitiva
- **What If... Zombies?!:** marcador sin resolver: Definitiva
- **Marvel Studios' Captain America: Brave New World (Captain America (Sam Wilson)):** marcador sin resolver: Pasiva, Definitiva

</details>

<details><summary>Falcon (Joaquin Torres): 6 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** $TIME sin duración: Pasiva; objetivo sin nombre: Pasiva T2; marcador sin resolver: Pasiva T2; nombre en Leads & Supports: Pasiva 4★

</details>

<details><summary>Fandral: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** rotación

</details>

<details><summary>Fantomex: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Franklin Richards: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; ISO-8 u obelisco en la guía de armado

</details>

<details><summary>Galactus: 5 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** $TIME sin duración: Pasiva; rotación

</details>

<details><summary>Gambit: 2 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **X-Men Year-End Party:** C.T.P. de su contexto: PvE

</details>

<details><summary>Gamora: 9 faltantes, 5 de 6 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** skill sin efectos: Pasiva de uniforme; rotación
- **Requiem:** marcador sin resolver: Pasiva T2 (2)
- **Marvel Studios' Guardians of the Galaxy 3:** marcador sin resolver: Pasiva T2 (2)
- **Wastelanders:** marcador sin resolver: Pasiva T2 (2)

</details>

<details><summary>Ghost: 5 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Studios' Ant-Man and the Wasp:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Thunderbolts*:** código sin nombre: Activa 4; soporte sin Leads & Supports: Pasiva de uniforme

</details>

<details><summary>Ghost Panther: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Ghost Rider: 15 faltantes, 6 de 6 variantes incompletas</summary>

- **Base:** marcador sin resolver: Pasiva T2; código sin nombre: Striker; rotación
- **70's Classic:** marcador sin resolver: Pasiva T2; código sin nombre: Striker; rotación
- **Inhumans: Attilan Rising:** marcador sin resolver: Pasiva T2; código sin nombre: Striker
- **King of Hell:** marcador sin resolver: Pasiva T2; skill sin efectos: Pasiva de uniforme; código sin nombre: Striker
- **Rage Returned:** marcador sin resolver: Pasiva T2; código sin nombre: Striker
- **Savage Avengers:** marcador sin resolver: Pasiva T2; código sin nombre: Striker

</details>

<details><summary>Ghost Rider (Robbie Reyes): 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Lord of Vengeance:** marcador sin resolver: Pasiva de uniforme (2)

</details>

<details><summary>Giant-Man: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Modern (Goliath):** rotación

</details>

<details><summary>Gilgamesh: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** $TIME sin duración: Pasiva; rotación
- **Marvel Studios' Eternals:** $TIME sin duración: Pasiva

</details>

<details><summary>Gladiator: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Thanos: The Infinity Revelation:** $TIME sin duración: Pasiva T2

</details>

<details><summary>Gorgon: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** instinto
- **Base:** marcador sin resolver: Activa 3; rotación

</details>

<details><summary>Gorilla-Man: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** fila vacía en la guía de armado

</details>

<details><summary>Gorr: 13 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** «Give Power» vacío: Pasiva, Pasiva T2, Liderazgo; $TIME sin duración: Liderazgo, Pasiva, Pasiva T2
- **The God Butcher:** «Give Power» vacío: Pasiva, Pasiva T2, Liderazgo; $TIME sin duración: Liderazgo, Pasiva, Pasiva T2

</details>

<details><summary>Green Goblin: 6 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** liderazgo sin completar: Liderazgo
- **Ultimate:** rotación
- **Gold Goblin:** marcador sin resolver: Pasiva T2 (2); soporte sin Leads & Supports: Pasiva T2

</details>

<details><summary>Groot: 8 faltantes, 5 de 7 variantes incompletas</summary>

- **Base:** rotación
- **Secret Wars: Thors:** rotación
- **Marvel Studios' Avengers: Infinity War:** rotación
- **Marvel Studios' Guardians of the Galaxy 3:** «Give Power» vacío: Pasiva T2; $TIME sin duración: Pasiva T2
- **Planet X Palm:** «Give Power» vacío: Pasiva T2; $TIME sin duración: Pasiva T2; rotación

</details>

<details><summary>Gwenpool: 3 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Gwen Poole:** skill sin efectos: Pasiva de uniforme
- **April Pools:** objetivo sin nombre: Pasiva de uniforme

</details>

<details><summary>Hades (Pluto): 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** código sin nombre: Striker

</details>

<details><summary>Havok: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Hawkeye: 7 faltantes, 6 de 7 variantes incompletas</summary>

- **Base:** rotación
- **Avengers: Age of Ultron:** rotación
- **Marvel Studios' Captain America: Civil War:** rotación
- **Classic:** rotación
- **Marvel Studios' Hawkeye (Hero Suit):** $TIME sin duración: Pasiva de uniforme
- **Wastelanders:** $TIME sin duración: Pasiva de uniforme; C.T.P. de su contexto: PvE

</details>

<details><summary>Hawkeye (Kate Bishop): 1 faltante, 1 de 3 variantes incompletas</summary>

- **Young Avengers:** rotación

</details>

<details><summary>Heimdall: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Asgard Invasion:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Hela: 4 faltantes, 2 de 4 variantes incompletas</summary>

- **Base:** código sin nombre: Activa 4 (2); rotación
- **Asgard Invasion:** rotación

</details>

<details><summary>Hellstorm: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** código sin nombre: Striker
- **TVA:** código sin nombre: Striker; rotación

</details>

<details><summary>Hercules: 5 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** $TIME sin duración: Pasiva; rotación

</details>

<details><summary>Hogun: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** rotación

</details>

<details><summary>Hope Summers: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** objetivo sin nombre: Liderazgo

</details>

<details><summary>Hulk: 12 faltantes, 10 de 10 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Secret Wars: Future Imperfect (Maestro):** rotación
- **World War Hulk:** rotación
- **Marvel Studios' Thor: Ragnarok:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Avengers: Endgame:** skill sin efectos: Pasiva de uniforme
- **Team Suit:** skill sin efectos: Pasiva de uniforme
- **Immortal Hulk:** $TIME sin duración: Pasiva
- **Fear Itself:** $TIME sin duración: Pasiva
- **Titan:** $TIME sin duración: Pasiva
- **Marvel Studios' Spider-Man: Brand New Day:** $TIME sin duración: Pasiva

</details>

<details><summary>Hulk (Amadeus Cho): 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado

</details>

<details><summary>Hulkbuster (Iron Man Mark 44): 8 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** valores del artefacto; fila vacía en la guía de armado
- **Base:** rotación
- **Heavy Duty Armor (Hulkbuster (Iron Man Mark 43)):** rotación
- **3099:** objetivo sin nombre: Liderazgo; soporte sin Leads & Supports: Pasiva
- **Celestial Hulkbuster (Hulkbuster):** objetivo sin nombre: Liderazgo; $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Human Torch: 7 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** instinto
- **Base:** «Give Power» vacío: Striker
- **Future Foundation:** «Give Power» vacío: Striker
- **Classic:** «Give Power» vacío: Striker
- **The Fall of the Fantastic Four:** «Give Power» vacío: Striker
- **Marvel Studios' The Fantastic Four: First Steps:** «Give Power» vacío: Striker; rotación

</details>

<details><summary>Hydro-Man: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** liderazgo sin completar: Liderazgo

</details>

<details><summary>Hyperion: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Iceman: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Ikaris: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** $TIME sin duración: Pasiva
- **Marvel Studios' Eternals:** $TIME sin duración: Pasiva

</details>

<details><summary>Ikon: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Inferno: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** valores del artefacto

</details>

<details><summary>Invisible Woman: 11 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** instinto
- **Base:** soporte sin Leads & Supports: Pasiva
- **Future Foundation:** soporte sin Leads & Supports: Pasiva
- **Classic:** $TIME sin duración: Pasiva T2; soporte sin Leads & Supports: Pasiva
- **The Fall of the Fantastic Four:** C.T.P. de su contexto: PvE
- **Marvel Studios' The Fantastic Four: First Steps:** «Give Power» vacío: Pasiva de uniforme; $TIME sin duración: Pasiva de uniforme; rotación; C.T.P. de su contexto: PvP, PvE

</details>

<details><summary>Iron Fist: 3 faltantes, 3 de 5 variantes incompletas</summary>

- **Base:** rotación
- **New Avengers:** rotación
- **All-New, All-Different:** rotación

</details>

<details><summary>Iron Hammer: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Iron Man: 14 faltantes, 8 de 11 variantes incompletas</summary>

- **Base:** rotación
- **Avengers: Age of Ultron:** rotación
- **Secret Wars: 2099:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Captain America: Civil War:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Avengers: Infinity War:** $TIME sin duración: Pasiva de uniforme
- **Marvel Studios' Avengers: Endgame:** $TIME sin duración: Pasiva de uniforme; marcador sin resolver: Activa 3; rotación
- **Team Suit:** $TIME sin duración: Pasiva de uniforme; marcador sin resolver: Activa 3; rotación
- **Avengers 3099:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Ironheart: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers; fila vacía en la guía de armado
- **Marvel Television's Ironheart:** rotación

</details>

<details><summary>Jean Grey: 1 faltante, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Jeff the Land Shark: 5 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** nombre en Leads & Supports: Pasiva 4★ (secundaria); rotación

</details>

<details><summary>Jessica Jones: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Jewel:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Jubilee: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; C.T.P. en la guía de armado; ISO-8 u obelisco en la guía de armado

</details>

<details><summary>Juggernaut: 2 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Savage Avengers:** rotación

</details>

<details><summary>Kahhori: 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** código sin nombre: Pasiva T2 (2)

</details>

<details><summary>Kang the Conqueror: 10 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo, Pasiva; código sin nombre: Striker
- **Rama-Tut:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo, Pasiva; código sin nombre: Striker; rotación

</details>

<details><summary>Karnak: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** rotación

</details>

<details><summary>Katy: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** objetivo sin nombre: Liderazgo

</details>

<details><summary>Kid Kaiju: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** rotación
- **Monsters Unleashed! (MFF Variant):** rotación

</details>

<details><summary>Kid Omega: 5 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** $TIME sin duración: Pasiva T2
- **Uncanny X-Men:** $TIME sin duración: Pasiva T2; rotación; C.T.P. de su contexto: PvE

</details>

<details><summary>Killmonger: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** rotación

</details>

<details><summary>Kingo: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Marvel Studios' Eternals:** código sin nombre: Pasiva de uniforme

</details>

<details><summary>Kingpin: 5 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** rotación
- **Secret Wars: Armor Wars:** rotación
- **Winter Criminal:** $TIME sin duración: Pasiva de uniforme
- **Marvel Television's Daredevil: Born Again:** $TIME sin duración: Pasiva de uniforme; rotación

</details>

<details><summary>Kitty Pryde: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Knull: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** $TIME sin duración: Pasiva T2; código sin nombre: Striker
- **Ancient History:** $TIME sin duración: Pasiva T2; código sin nombre: Striker

</details>

<details><summary>Korath: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** $TIME sin duración: Pasiva

</details>

<details><summary>Kraven The Hunter: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Lash: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** nombre en Leads & Supports: Liderazgo; rotación
- **Modern:** nombre en Leads & Supports: Liderazgo; rotación

</details>

<details><summary>Leader: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; C.T.P. en la guía de armado

</details>

<details><summary>Lizard: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers
- **Base:** rotación

</details>

<details><summary>Loki: 4 faltantes, 4 de 9 variantes incompletas</summary>

- **Lady Loki:** skill sin efectos: Pasiva de uniforme
- **Marvel Studios' Thor: Ragnarok:** skill sin efectos: Pasiva de uniforme
- **Classic:** skill sin efectos: Pasiva de uniforme
- **Marvel Studios' Loki (President Loki):** $TIME sin duración: Pasiva

</details>

<details><summary>Luke Cage: 4 faltantes, 3 de 4 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Luke Cage:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Luna Snow: 7 faltantes, 6 de 6 variantes incompletas</summary>

- **Base:** liderazgo sin completar: Liderazgo; soporte sin Leads & Supports: Pasiva
- **Andromeda Suit:** liderazgo sin completar: Liderazgo
- **Lifestyle Series 1:** liderazgo sin completar: Liderazgo
- **Light Sirius Armor:** liderazgo sin completar: Liderazgo
- **Summer Lilac:** liderazgo sin completar: Liderazgo
- **Mirae 2099:** liderazgo sin completar: Liderazgo

</details>

<details><summary>M'Baku: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers
- **Base:** C.T.P. de su contexto: PvP

</details>

<details><summary>M.O.D.O.K.: 3 faltantes, 3 de 4 variantes incompletas</summary>

- **Base:** rotación
- **SPIDOC:** skill sin efectos: Pasiva de uniforme
- **CAPDOC:** rotación

</details>

<details><summary>Madelyne Pryor: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Winter Queen:** rotación

</details>

<details><summary>Magik: 4 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Phoenix Five:** skill sin efectos: Pasiva de uniforme; código sin nombre: Activa 4
- **Marvel Rivals:** rotación

</details>

<details><summary>Magneto: 4 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Marvel NOW!:** marcador sin resolver: Pasiva de uniforme; rotación

</details>

<details><summary>Makkari: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Malekith: 9 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** marcador sin resolver: Pasiva T2 (2); rotación
- **All-New, All-Different:** marcador sin resolver: Pasiva T2 (2); rotación; C.T.P. de su contexto: PvP
- **War of the Realms:** $TIME sin duración: Pasiva; marcador sin resolver: Pasiva T2

</details>

<details><summary>Man-Thing: 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** $TIME sin duración: Pasiva

</details>

<details><summary>Mantis: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación

</details>

<details><summary>Marvel Boy: 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** nombre en Leads & Supports: Pasiva 4★

</details>

<details><summary>Maximus: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers
- **Base:** marcador sin resolver: Pasiva

</details>

<details><summary>Medusa: 2 faltantes, 2 de 4 variantes incompletas</summary>

- **Monsters Unleashed! (MFF Variant):** skill sin efectos: Pasiva de uniforme
- **Inhumans vs X-Men:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Mephisto: 6 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** marcador sin resolver: Pasiva T2; $TIME sin duración: Pasiva T2
- **Master of Hell:** $TIME sin duración: Liderazgo, Pasiva T2; marcador sin resolver: Pasiva T2; C.T.P. de su contexto: PvP

</details>

<details><summary>Minn-Erva: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Mister Fantastic: 4 faltantes, 4 de 5 variantes incompletas</summary>

- **Base:** $TIME sin duración: Pasiva T2
- **Future Foundation:** $TIME sin duración: Pasiva T2
- **The Maker:** $TIME sin duración: Pasiva T2
- **Marvel Studios' The Fantastic Four: First Steps:** rotación

</details>

<details><summary>Mockingbird: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Studios' Agents of S.H.I.E.L.D. (Bobbi Morse):** rotación
- **All-New, All-Different:** rotación

</details>

<details><summary>Molecule Man: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Base:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo; soporte sin Leads & Supports: Pasiva

</details>

<details><summary>Molten Man: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Base:** marcador sin resolver: Pasiva; $TIME sin duración: Pasiva T2

</details>

<details><summary>Moon Girl: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Moon Knight: 1 faltante, 1 de 5 variantes incompletas</summary>

- **Armored:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Moonstone: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** $TIME sin duración: Pasiva

</details>

<details><summary>Morgan le Fay: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** $TIME sin duración: Pasiva T2
- **Fallen Soul:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Morph: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Ms. Marvel (Kamala Khan): 3 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Karachi Costume:** rotación

</details>

<details><summary>Mysterio: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** instinto
- **Summer Mystery:** «Give Power» vacío: Pasiva T2; $TIME sin duración: Pasiva T2

</details>

<details><summary>Namor: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Nebula: 4 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** rotación
- **Classic:** skill sin efectos: Pasiva de uniforme; rotación

</details>

<details><summary>Nick Fury: 3 faltantes, 2 de 4 variantes incompletas</summary>

- **Marvel Studios' Captain Marvel:** skill sin efectos: Pasiva de uniforme
- **Secret Avengers:** rotación; C.T.P. de su contexto: PvP

</details>

<details><summary>Nightcrawler: 6 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** $TIME sin duración: Pasiva
- **X-Force:** $TIME sin duración: Pasiva; rotación
- **Classic:** $TIME sin duración: Pasiva; rotación

</details>

<details><summary>Nova (Richard Rider): 2 faltantes, 1 de 2 variantes incompletas</summary>

- **Marvel Cosmic Invasion:** C.T.P. de su contexto: PvP, PvE

</details>

<details><summary>Nova (Sam Alexander): 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Odin: 6 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Avengers 1,000,000 BC:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo
- **Lord of Asgard:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo

</details>

<details><summary>Okoye: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Omega Red: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers
- **Base:** $TIME sin duración: Pasiva

</details>

<details><summary>Phil Coulson: 2 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** rotación
- **A.O.S. Season 3:** rotación

</details>

<details><summary>Polaris: 5 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** $TIME sin duración: Pasiva
- **Uncanny X-Men:** $TIME sin duración: Pasiva; nombre en Leads & Supports: Pasiva de Tier-2; rotación

</details>

<details><summary>Professor X: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Proxima Midnight: 2 faltantes, 2 de 3 variantes incompletas</summary>

- **Marvel Studios' Avengers: Infinity War:** skill sin efectos: Pasiva de uniforme
- **Dark Obsidian Armor:** C.T.P. de su contexto: PvE

</details>

<details><summary>Psylocke: 2 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Summer Vacation:** C.T.P. de su contexto: PvE

</details>

<details><summary>Punisher: 8 faltantes, 8 de 8 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Noir:** rotación
- **War Journal:** rotación
- **Cosmic Ghost Rider:** marcador sin resolver: Pasiva de uniforme (2)
- **Fist of the Beast:** marcador sin resolver: Pasiva de uniforme
- **Marvel Television's Daredevil: Born Again:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Quasar (Wendell Vaughn): 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo

</details>

<details><summary>Quicksilver: 3 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Marvel Legacy:** rotación

</details>

<details><summary>Rachel Summers: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **X-Men: Days of Future Past:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo

</details>

<details><summary>Red Guardian: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Marvel Studios' Thunderbolts*:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Red Hulk: 2 faltantes, 2 de 4 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Studios' Captain America: Brave New World:** $TIME sin duración: Pasiva

</details>

<details><summary>Red Skull: 15 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** falta la skill: Striker; marcador sin resolver: Pasiva T2 (2); rotación
- **Secret Wars: Red Skull:** falta la skill: Striker; marcador sin resolver: Pasiva T2 (2); rotación
- **Hydra Armor:** falta la skill: Striker; marcador sin resolver: Pasiva T2 (2)
- **The Crimson Fall:** marcador sin resolver: Pasiva T2 (2); soporte sin Leads & Supports: Pasiva T2; rotación

</details>

<details><summary>Rhino: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Uncanny Spider-Man:** soporte sin Leads & Supports: Pasiva de uniforme

</details>

<details><summary>Rocket Raccoon: 5 faltantes, 4 de 7 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** skill sin efectos: Pasiva de uniforme; rotación
- **Guardians of the Galaxy 2:** rotación
- **Marvel Studios' Avengers: Infinity War:** rotación

</details>

<details><summary>Rogue: 4 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Age of Apocalypse:** skill sin efectos: Pasiva de uniforme; rotación
- **Uncanny Avengers:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Ronan: 4 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** rotación
- **Annihilation:** skill sin efectos: Pasiva de uniforme
- **Marvel Studios' Captain Marvel:** marcador sin resolver: Pasiva de uniforme
- **Annihilators:** C.T.P. de su contexto: PvP

</details>

<details><summary>Sabretooth: 2 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación

</details>

<details><summary>Satana: 6 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** código sin nombre: Pasiva T2 (2); rotación
- **Marvel Legacy:** código sin nombre: Pasiva T2 (2); skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Scarlet Spider: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers; fila vacía en la guía de armado
- **Gift Deliverer:** rotación

</details>

<details><summary>Scarlet Witch: 3 faltantes, 8 de 8 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Marvel Studios' Avengers: Infinity War:** rotación

</details>

<details><summary>Scorpion: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** «Give Power» vacío: Striker
- **Marvel Studios' Spider-Man: Brand New Day:** «Give Power» vacío: Striker

</details>

<details><summary>Scream: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Sentinel: 7 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** $TIME sin duración: Pasiva; rotación
- **Nimrod The Lesser:** $TIME sin duración: Pasiva
- **Stark Sentinels Mk II:** $TIME sin duración: Pasiva; marcador sin resolver: Pasiva (2); rotación

</details>

<details><summary>Sentry: 9 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **Merged:** «Give Power» vacío: Striker, Liderazgo; $TIME sin duración: Liderazgo
- **Marvel Studios' Thunderbolts*:** «Give Power» vacío: Striker, Liderazgo; $TIME sin duración: Liderazgo; liderazgo sin completar: Liderazgo (secundario); rotación

</details>

<details><summary>Shadow Shell: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** código sin nombre: Activa 3

</details>

<details><summary>Shang-Chi: 2 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Animation's Marvel Zombies:** rotación

</details>

<details><summary>She-Hulk: 3 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **All-New:** rotación

</details>

<details><summary>Shuri: 3 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Marvel Studios' Black Panther: Wakanda Forever (Black Panther):** C.T.P. de su contexto: PvP

</details>

<details><summary>Sif: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Silk: 4 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** liderazgo sin completar: Liderazgo
- **Web Suit:** código sin nombre: Pasiva de uniforme; liderazgo sin completar: Liderazgo
- **Summer Days:** liderazgo sin completar: Liderazgo

</details>

<details><summary>Silver Samurai: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; fila vacía en la guía de armado
- **Base:** rotación

</details>

<details><summary>Silver Surfer: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Silver Surfer (Shalla-Bal): 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** rotación

</details>

<details><summary>Sin: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Rage Returned:** C.T.P. de su contexto: PvE

</details>

<details><summary>Sister Grimm: 10 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** falta la skill: Striker; liderazgo sin completar: Liderazgo
- **All-New, All-Different:** falta la skill: Striker; skill sin efectos: Pasiva de uniforme; liderazgo sin completar: Liderazgo
- **Runaways:** falta la skill: Striker; liderazgo sin completar: Liderazgo
- **Princess Tsukimi:** liderazgo sin completar: Liderazgo; soporte sin Leads & Supports: Pasiva; rotación

</details>

<details><summary>Skurge: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Sleeper: 6 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** «Give Power» vacío: Pasiva T2; objetivo sin nombre: Liderazgo; $TIME sin duración: Pasiva, Pasiva T2

</details>

<details><summary>Songbird: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers
- **Base:** código sin nombre: Pasiva T2

</details>

<details><summary>Spectrum: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Marvel Studios' The Marvels (Captain Monica Rambeau):** $TIME sin duración: Pasiva

</details>

<details><summary>Spider-Gwen: 1 faltante, 1 de 4 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Spider-Man: 46 faltantes, 13 de 13 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** código sin nombre: Pasiva T2, Striker (2); rotación
- **Secret Wars: Renew Your Vows:** código sin nombre: Pasiva T2, Striker (2); skill sin efectos: Pasiva de uniforme; rotación
- **All-New, All-Different:** código sin nombre: Pasiva T2, Striker (2); skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Captain America: Civil War:** código sin nombre: Pasiva T2, Striker (2); rotación
- **Spider-Man: Homecoming Homemade Suit:** código sin nombre: Pasiva T2, Striker (2); rotación
- **Marvel Studios' Avengers: Infinity War:** código sin nombre: Pasiva T2, Striker (2); $TIME sin duración: Pasiva de uniforme
- **Spider-Man: Far From Home:** código sin nombre: Pasiva T2, Striker (2); $TIME sin duración: Pasiva de uniforme; rotación
- **Spider-Man: Far From Home (Stealth Suit):** código sin nombre: Pasiva T2, Striker (2); $TIME sin duración: Pasiva de uniforme
- **Spider-Man: No Way Home (Integrated Suit):** código sin nombre: Striker (2)
- **Spider-Man: No Way Home (Black & Gold Suit):** código sin nombre: Striker (2)
- **Back to Basics:** código sin nombre: Striker (2)
- **The Symbiote Suit:** código sin nombre: Striker (2)
- **Marvel Studios' Spider-Man: Brand New Day:** código sin nombre: Striker (2)

</details>

<details><summary>Spider-Man (Miles Morales): 10 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** marcador sin resolver: Pasiva T2; rotación
- **Into the Spider-Verse:** marcador sin resolver: Pasiva T2
- **Absolute Carnage:** objetivo sin nombre: Liderazgo; marcador sin resolver: Pasiva T2
- **Anniversary Special:** objetivo sin nombre: Liderazgo; nombre en Leads & Supports: Liderazgo
- **Spider-Man: Across the Spider-Verse:** marcador sin resolver: Pasiva de uniforme
- **Ancient Curse:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Spider-Man 2099: 1 faltante, 1 de 3 variantes incompletas</summary>

- **All-New, All-Different:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Spider-Woman: 3 faltantes, 1 de 2 variantes incompletas</summary>

- **Spider-Man: Across the Spider-Verse:** «Give Power» vacío: Liderazgo; $TIME sin duración: Liderazgo; nombre en Leads & Supports: Liderazgo

</details>

<details><summary>Spot: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Squirrel Girl: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Nutty Titan:** objetivo sin nombre: Pasiva de uniforme; $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Star-Lord: 2 faltantes, 2 de 7 variantes incompletas</summary>

- **Base:** rotación
- **Space Armor:** rotación

</details>

<details><summary>Storm: 8 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** código sin nombre: Striker
- **X-Men Red:** skill sin efectos: Pasiva de uniforme; código sin nombre: Striker; rotación
- **Inhumans vs X-Men:** código sin nombre: Striker
- **Krakoan Summer:** código sin nombre: Striker
- **Marvel Animation's X-Men '97:** código sin nombre: Striker

</details>

<details><summary>Stryfe: 5 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** instinto
- **The Tyrant of Spring:** «Give Power» vacío: Pasiva de uniforme; $TIME sin duración: Pasiva, Pasiva de uniforme; rotación

</details>

<details><summary>Sun Bird: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; fila vacía en la guía de armado
- **Moon Temple Defenders:** rotación

</details>

<details><summary>Sunspot: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** valores del artefacto; strikers; bonos de equipo

</details>

<details><summary>Supergiant: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** instinto

</details>

<details><summary>Sylvie: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Taskmaster: 5 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **Marvel Studios' Black Widow:** «Give Power» vacío: Striker
- **Marvel Studios' Thunderbolts*:** «Give Power» vacío: Striker; nombre en Leads & Supports: Pasiva de Tier-2; rotación

</details>

<details><summary>Thanos: 33 faltantes, 5 de 8 variantes incompletas</summary>

- **Secret Wars: Infinity:** rotación
- **Obsidian King:** «Give Power» vacío: Pasiva de uniforme; marcador sin resolver: Pasiva; $TIME sin duración: Pasiva, Pasiva de uniforme; código sin nombre: Pasiva T2 (2)
- **Wise Harvester:** «Give Power» vacío: Pasiva de uniforme, Liderazgo; $TIME sin duración: Liderazgo, Pasiva, Pasiva de uniforme; marcador sin resolver: Pasiva (2); código sin nombre: Pasiva T2 (2)
- **Thanos Wins:** «Give Power» vacío: Pasiva de uniforme, Liderazgo; $TIME sin duración: Liderazgo, Pasiva, Pasiva de uniforme; marcador sin resolver: Pasiva; código sin nombre: Pasiva T2 (2)
- **Annihilation:** «Give Power» vacío: Pasiva de uniforme, Liderazgo; $TIME sin duración: Liderazgo, Pasiva, Pasiva de uniforme; marcador sin resolver: Pasiva; código sin nombre: Pasiva T2 (2); rotación

</details>

<details><summary>The Hood: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>The Thing: 6 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** rotación
- **Future Foundation:** soporte sin Leads & Supports: Pasiva de uniforme; rotación
- **Classic:** soporte sin Leads & Supports: Pasiva de uniforme
- **Marvel Studios' The Fantastic Four: First Steps:** rotación

</details>

<details><summary>Thor: 3 faltantes, 3 de 10 variantes incompletas</summary>

- **Base:** rotación
- **Avengers: Age of Ultron:** rotación
- **Unworthy:** rotación

</details>

<details><summary>Thor (Jane Foster): 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; bono sin nombre
- **Marvel Studios' Thor: Love and Thunder:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Titania: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; bono sin nombre
- **Fear Itself:** $TIME sin duración: Pasiva T2

</details>

<details><summary>Toxin: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers
- **Base:** $TIME sin duración: Pasiva T2; nombre en Leads & Supports: Liderazgo

</details>

<details><summary>U.S. Agent: 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** $TIME sin duración: Pasiva

</details>

<details><summary>Ulik: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** marcador sin resolver: Activa 3

</details>

<details><summary>Ultron: 20 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** «Give Power» vacío: Striker; rotación
- **Avengers: Age of Ultron (Ultron Prime):** «Give Power» vacío: Striker; marcador sin resolver: Pasiva de uniforme (2); rotación
- **Avengers: Age of Ultron (Ultron Mark 1):** «Give Power» vacío: Striker; marcador sin resolver: Pasiva de uniforme (2); rotación
- **Avengers: Age of Ultron (Ultron Mark 3):** «Give Power» vacío: Striker; marcador sin resolver: Pasiva de uniforme (2); rotación
- **Marvel Studios' What If...? (Infinity Ultron):** «Give Power» vacío: Striker; marcador sin resolver: Pasiva de uniforme
- **All-Father Ultron:** «Give Power» vacío: Striker; $TIME sin duración: Pasiva T2; marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Valeria Richards: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** C.T.P. de su contexto: PvE

</details>

<details><summary>Valkyrie: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Venom: 10 faltantes, 7 de 7 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Secret Wars: Marvel Zombies:** rotación
- **Anti-Venom:** soporte sin Leads & Supports: Pasiva de uniforme; rotación
- **War of the Realms:** soporte sin Leads & Supports: Pasiva de uniforme
- **King in Black:** $TIME sin duración: Pasiva de uniforme; soporte sin Leads & Supports: Pasiva de uniforme
- **Warstar:** $TIME sin duración: Pasiva de uniforme
- **Snow Symbiote:** $TIME sin duración: Pasiva de uniforme

</details>

<details><summary>Venus (Aphrodite): 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** $TIME sin duración: Pasiva

</details>

<details><summary>Victorious: 5 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** objetivo sin nombre: Liderazgo
- **Emperor Guarder:** objetivo sin nombre: Liderazgo; nombre en Leads & Supports: Liderazgo, Pasiva 4★; C.T.P. de su contexto: PvP

</details>

<details><summary>Viper: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** $TIME sin duración: Pasiva T2

</details>

<details><summary>Vision: 4 faltantes, 2 de 5 variantes incompletas</summary>

- **Marvel Studios' WandaVision:** objetivo sin nombre: Liderazgo
- **Ultimate Vision:** $TIME sin duración: Pasiva, Pasiva T2; rotación

</details>

<details><summary>Volstagg: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** rotación

</details>

<details><summary>Vulture: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** instinto
- **Spider-Man: Homecoming:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>War Machine: 8 faltantes, 5 de 9 variantes incompletas</summary>

- **Base:** rotación
- **Iron Patriot:** skill sin efectos: Pasiva de uniforme; rotación
- **Avengers: The Initiative:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Captain America: Civil War:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Avengers: Infinity War:** rotación

</details>

<details><summary>War Tiger: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Warwolf: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** rotación

</details>

<details><summary>Wasp: 1 faltante, 1 de 4 variantes incompletas</summary>

- **Ant-Man and the Wasp: Quantumania:** $TIME sin duración: Pasiva

</details>

<details><summary>Wasp (Nadia Van Dyne): 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers
- **Base:** soporte sin Leads & Supports: Pasiva

</details>

<details><summary>Wave: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** instinto
- **Base:** objetivo sin nombre: Liderazgo
- **Classic:** objetivo sin nombre: Liderazgo

</details>

<details><summary>Weapon Hex: 5 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** $TIME sin duración: Pasiva
- **Infected Bioweapon:** «Give Power» vacío: Pasiva T2; $TIME sin duración: Pasiva T2, Pasiva de uniforme

</details>

<details><summary>Wenwu: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Base:** soporte sin Leads & Supports: Pasiva

</details>

<details><summary>Whiplash: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** marcador sin resolver: Pasiva

</details>

<details><summary>White Tiger: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** liderazgo sin completar: Liderazgo; rotación
- **Marvel Television's Daredevil: Born Again:** liderazgo sin completar: Liderazgo

</details>

<details><summary>Wiccan: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** valores del artefacto
- **Base:** código sin nombre: Pasiva T2 (2)

</details>

<details><summary>Winter Soldier: 12 faltantes, 7 de 7 variantes incompletas</summary>

- **Base:** código sin nombre: Striker; rotación
- **Marvel Studios' Captain America: Civil War:** skill sin efectos: Pasiva de uniforme; código sin nombre: Striker; rotación
- **Captain America:** código sin nombre: Striker; rotación
- **Marvel Studios' Avengers: Infinity War:** skill sin efectos: Pasiva de uniforme; código sin nombre: Striker
- **Marvel Studios' The Falcon and the Winter Soldier:** código sin nombre: Striker
- **Revolution:** código sin nombre: Striker
- **Marvel Studios' Thunderbolts*:** código sin nombre: Striker

</details>

<details><summary>Wolverine: 11 faltantes, 8 de 8 variantes incompletas</summary>

- **Personaje:** strikers; ISO-8 u obelisco en la guía de armado
- **Age of Apocalypse:** rotación
- **All-New Marvel NOW!:** rotación
- **Enter the Phoenix:** $TIME sin duración: Pasiva, Pasiva de uniforme
- **X Deaths of Wolverine:** $TIME sin duración: Pasiva, Pasiva de uniforme
- **Marvel Studios' Deadpool & Wolverine:** $TIME sin duración: Pasiva, Pasiva de uniforme; C.T.P. de su contexto: PvE

</details>

<details><summary>Wong: 9 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** código sin nombre: Striker; rotación
- **Marvel Studios' Doctor Strange:** código sin nombre: Striker; rotación
- **Marvel Studios' Doctor Strange 2:** código sin nombre: Striker; liderazgo sin completar: Liderazgo
- **What If... Zombies?!:** código sin nombre: Striker; liderazgo sin completar: Liderazgo; C.T.P. de su contexto: PvE

</details>

<details><summary>X-23: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Yelena Belova: 2 faltantes, 1 de 4 variantes incompletas</summary>

- **Marvel Studios' Thunderbolts*:** rotación; C.T.P. de su contexto: PvE

</details>

<details><summary>Yellowjacket: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** liderazgo sin completar: Liderazgo
- **Marvel NOW!:** marcador sin resolver: Pasiva de uniforme; liderazgo sin completar: Liderazgo

</details>

<details><summary>Yondu: 1 faltante, 1 de 4 variantes incompletas</summary>

- **All-New, All-Different:** rotación

</details>

<details><summary>Zeus: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>
