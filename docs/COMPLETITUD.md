# Completitud de los datos

Generado por `scripts/completitud.py` sobre `data.js` (juego 12.3, datos del 2026-10-16, formato 18) y `datos.json`.

Qué le falta a cada variante (un personaje con un uniforme) para tener la información que la app muestra y usa, y de dónde podría salir. Lo que dos fuentes dicen distinto está en `docs/AUDITORIA.md`; esto es lo que no está. Lo que no existe en el juego no es un faltante (un personaje sin artefacto, si ninguna fuente dice que tenga uno), y lo que una fuente dice a propósito va aparte.

## Qué es «completo»

Una variante está completa si no le falta nada de esto. Lo del personaje (instinto, stats, artefacto, strikers, bonos, Ideal CTP List, guía de armado, tier list General) vale para todas sus variantes.

| Pieza | Qué se pide | Por qué es esperable que esté |
|---|---|---|
| Identidad | Clase, bando, género, raza, habilidades, habilidad de World Boss, instinto y tipo de ataque. | thanosvibs los publica para todos [Comprobado]; el instinto, con lo visto en el juego encima. El tipo de ataque se deduce del daño de las activas. |
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

261 de 891 variantes completas (29%); 56 de 291 personajes con todas sus variantes completas.

Lo que falta, de lo que deja incompletas más variantes a lo que deja menos (lo que falta en el personaje cuenta en todas sus variantes):

| Faltante | Variantes | Personajes | Casos | De dónde podría salir |
|---|---|---|---|---|
| [Strikers](#strikers) | 358 | 123 | 123 | la wiki (pestaña Striker), el juego o foros |
| [Rotación](#rotación) | 192 | 112 | 192 | thanosvibs (rotaciones), la guía de armado o foros |
| [Fila vacía en la guía de armado](#fila-vacía-en-la-guía-de-armado) | 74 | 33 | 33 | la guía de armado o foros |
| [«Give Power» sin lo que otorga](#give-power-sin-lo-que-otorga) | 68 | 27 | 78 | thanosvibs (Leads & Supports), la wiki o foros |
| [Skill sin efectos](#skill-sin-efectos) | 48 | 31 | 48 | la wiki (en la pasiva de uniforme, el «Bonus» del uniforme) o foros |
| [Bonos de equipo que faltan](#bonos-de-equipo-que-faltan) | 34 | 33 | 33 | la wiki (sección Team Bonus), capturas del juego o foros |
| [Facción, tipo, raza o habilidad sin resolver ($HEROSUBTYPE1)](#facción-tipo-raza-o-habilidad-sin-resolver-herosubtype1) | 31 | 18 | 42 | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| [Sin el C.T.P. de su contexto en la guía de armado](#sin-el-ctp-de-su-contexto-en-la-guía-de-armado) | 29 | 27 | 31 | la guía de armado o foros |
| [Efecto que el catálogo no clasifica](#efecto-que-el-catálogo-no-clasifica) | 24 | 16 | 25 | a mano (scripts/contenido/catalogo.json) |
| [ISO-8 u obelisco sin dato en la guía de armado](#iso-8-u-obelisco-sin-dato-en-la-guía-de-armado) | 23 | 6 | 6 | la guía de armado o foros |
| [Valores del artefacto incompletos](#valores-del-artefacto-incompletos) | 17 | 7 | 7 | la wiki (página Artifact) o el juego |
| [Nombre en Leads & Supports distinto del de la skill](#nombre-en-leads--supports-distinto-del-de-la-skill) | 15 | 14 | 16 | el juego o foros |
| [Liderazgo sin completar](#liderazgo-sin-completar) | 10 | 4 | 10 | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| [Soporte que Leads & Supports no publica](#soporte-que-leads--supports-no-publica) | 5 | 3 | 5 | thanosvibs (Leads & Supports) o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| [Activa sin recarga](#activa-sin-recarga) | 4 | 2 | 4 | la wiki o el juego |
| [Retrato o ícono](#retrato-o-ícono) | 4 | 2 | 4 | thanosvibs (imágenes) |
| [Bono de equipo sin nombre](#bono-de-equipo-sin-nombre) | 4 | 2 | 2 | capturas del juego o foros |
| [Objetivo sin nombre (Target ID)](#objetivo-sin-nombre-target-id) | 3 | 3 | 3 | thanosvibs (Leads & Supports) o foros |
| [Sin C.T.P. en la guía de armado](#sin-ctp-en-la-guía-de-armado) | 3 | 2 | 2 | la guía de armado o foros |
| [Skill que falta](#skill-que-falta) | 1 | 1 | 5 | thanosvibs (API de skills), la wiki o foros |
| [Stats](#stats) | 1 | 1 | 1 | thanosvibs |
| [Sin fila en la Ideal CTP List](#sin-fila-en-la-ideal-ctp-list) | 1 | 1 | 1 | thanosvibs (Ideal CTP List) |
| [Sin lugar en la tier list General](#sin-lugar-en-la-tier-list-general) | 1 | 1 | 1 | thanosvibs (tier list General) |

Sin casos: Dato de identidad vacío; Duración sin publicar ($TIME); Código en lugar de un nombre; Artefacto que falta; Perfil de combate o roles; Datos del uniforme.

### Lo que ya se sabía que no cierra

- **Marcadores sin resolver:** 42 efectos en 31 variantes. docs/AUDITORIA.md (sección 8) los cuenta por id de la API, que se repite en los uniformes que comparten la skill.
- **Liderazgos:** Leads & Supports publica el de 415 variantes, y el build deriva el de 466 más de su Leader Skill (484 slots, con "src": "api"; docs/AUDITORIA.md, sección 12) y 12 soportes de las pasivas. 10 slots de 10 variantes no se pudieron derivar (efecto sin stat, 10; un slot puede tener más de un motivo).
- **Strikers:** 120 personajes sin la pestaña Striker en la wiki y 3 con la pestaña sin filas que se puedan leer.
- **Bonos de equipo por confirmar:** los que se vieron en capturas del juego y esperan confirmación no están en data.js, así que este informe no los ve. Sí ve 31 personajes sin ningún bono y 2 solo con los del juego (Annihilus y Galactus). Los 49 bonos con versiones empatadas entre páginas de la wiki son diferencias entre fuentes (docs/AUDITORIA.md, sección 10): van en «Lo que no cuenta».
- **Nombres de Leads & Supports que no son los de la API de skills:** 16 en 15 variantes; 5 con el nombre de otra skill de la variante, entre ellos Jeff the Land Shark y Polaris — Uncanny X-Men.

### Lo que no cuenta como faltante

- **Sin artefacto:** 21 personajes, y ninguna fuente dice que tengan uno: Black Dwarf, Blue Marvel, Corvus Glaive, Darkhawk, Deathlok, Dormammu, Elsa Bloodstone, Iron Fist, Jessica Jones, Luke Cage, Molecule Man, Moonstone, Morbius, Nightcrawler, Proxima Midnight, Quasar (Avril Kincaid), Silk, Singularity, Songbird, Supergiant, Viper.
- **Guía de armado sin C.T.P., ISO-8 u obelisco para quien no vale la pena armar:** 63 personajes: la guía dice «dont waste gold» como ISO-8 o la Ideal CTP List los pone en «Not worth».
- **Bonos con versiones empatadas entre páginas de la wiki:** 49 (docs/AUDITORIA.md, sección 10). La app muestra todas las versiones.
- **Función en el contexto:** 60 variantes tienen función en PvP y 119 en PvE (están en las tier lists de ese contexto). Las demás no la tienen: la lista lo dice al no ponerlas.
- **Lo que este chequeo no mira:** las diferencias entre fuentes (docs/AUDITORIA.md), las traducciones, cómo se consigue cada artefacto, los stats de cada uniforme (data.js trae solo los del personaje) y el Set Striker, que la app no tiene.

## Por tipo de faltante

Las variantes de un personaje con el mismo faltante van en una fila.

### Stats

1 caso en 1 personaje. thanosvibs publica recuperación y resistencias de todos los personajes.

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Agatha Harkness | faltan recovery_rate, fire_resist, cold_resist, lightning_resist, poison_resist, mind_resist | thanosvibs |

### Skill que falta

5 casos en 1 personaje y 1 variante. La API de skills no trae una skill que la variante tiene en el juego por su tier o por ser uniforme (docs/AUDITORIA.md, sección 4, lista las de Tier-4 sin Striker y las de skill 6 sin Definitiva).

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Black Swan | Pasiva: la API de skills no la trae; Pasiva T2: la API de skills no la trae; Activa 4: la API de skills no la trae; Activa 5: la API de skills no la trae; Definitiva: la API de skills no la trae (es Tier-3 o Trascendido) | thanosvibs (API de skills), la wiki o foros |

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

### Efecto que el catálogo no clasifica

25 casos en 16 personajes y 24 variantes. Una etiqueta de efecto que el catálogo no clasifica (docs/AUDITORIA.md, sección 9).

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Adam Warlock — Marvel Studios' Guardians of the Galaxy 3 | Pasiva T2: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Beast (All-New X-Men, Marvel Animation's X-Men '97) | Pasiva T2: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Echo — Marvel Studios' Echo (Maya Lopez (Echo)) | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Electro — Spider-Man: No Way Home | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Galactus | Activa 2: «Excluding bosses, ignores enemy's basic damage decrease» (2 veces) | a mano (scripts/contenido/catalogo.json) |
| Gorr — The God Butcher | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Jeff the Land Shark | Pasiva: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Jubilee — Marvel Animation's X-Men '97 | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Kang the Conqueror — Rama-Tut | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Knull — Ancient History | Activa 2: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Madelyne Pryor — Winter Queen | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Red Guardian — Marvel Studios' Thunderbolts* | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Rhino — Uncanny Spider-Man | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Sentry (Merged, Marvel Studios' Thunderbolts*) | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Spider-Man (Spider-Man: No Way Home (Integrated Suit), Back to Basics, The Symbiote Suit, Marvel Studios' Spider-Man: Brand New Day) | Pasiva de uniforme: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Thanos (Obsidian King, Wise Harvester, Thanos Wins) | Activa 5: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |
| Thanos — Annihilation | Activa 4: «Excluding bosses, ignores enemy's basic damage decrease» | a mano (scripts/contenido/catalogo.json) |

### Facción, tipo, raza o habilidad sin resolver ($HEROSUBTYPE1)

42 casos en 18 personajes y 31 variantes. El efecto nombra una facción, un tipo, una raza o una habilidad con un marcador que ni la tabla a mano, ni Leads & Supports, ni la wiki resolvieron: la app lo muestra «sin especificar». Son los de docs/AUDITORIA.md, sección 8, que los cuenta por id de la API (un id se repite en los uniformes que comparten la skill); acá va cada variante.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Agent Venom — Agent Anti-Venom | Pasiva de uniforme «Agent Anti-Venom»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Angela — Secret Wars: 1602 Witch Hunter Angela | Pasiva de uniforme «Secret Wars: 1602 Witch Hunter Angela»: «Increases basic damage dealt to $HEROCLASS1 types by 20%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Captain Marvel — Marvel Studios' Avengers: Endgame | Pasiva de uniforme «Marvel Studios' Avengers: Endgame»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.»; Pasiva de uniforme «Marvel Studios' Avengers: Endgame»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 10%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Deathlok (sus 2 variantes) | Pasiva «Centipede Serum»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 50%.»; Pasiva «Centipede Serum»: «Decreases basic damage received from enemies with $HEROSUBTYPE1 ability by 50%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ghost Rider (base, 70's Classic, Inhumans: Attilan Rising, King of Hell) | Pasiva T2 «Repentance»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Gorgon | Activa 3 «War Cry»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Iron Man (Marvel Studios' Avengers: Endgame, Team Suit) | Activa 3 «Overdrive Beam»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Magneto — Marvel NOW! | Pasiva de uniforme «Marvel NOW!»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 45%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Malekith (base, All-New, All-Different) | Pasiva T2 «Malicious Manipulation»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.»; Pasiva T2 «Malicious Manipulation»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Maximus | Pasiva «Mad Scientist»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 50%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Mephisto (sus 2 variantes) | Pasiva T2 «Rage of the Pit»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%. Effect cannot be removed.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Molten Man | Pasiva «Fire Eater»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Red Skull (base, Secret Wars: Red Skull, Hydra Armor) | Pasiva T2 «Hero Hunter»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.»; Pasiva T2 «Hero Hunter»: «Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ronan — Marvel Studios' Captain Marvel | Pasiva de uniforme «Marvel Studios' Captain Marvel»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Spider-Man (Miles Morales) (base, Into the Spider-Verse, Absolute Carnage) | Pasiva T2 «Ultimate Spider-Man»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ulik | Activa 3 «Troll's Roar»: «Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Ultron (Avengers: Age of Ultron (Ultron Prime), Avengers: Age of Ultron (Ultron Mark 1), Avengers: Age of Ultron (Ultron Mark 3)) | Pasiva de uniforme «Avengers: Age of Ultron»: «Decreases basic damage received from $HEROCLASS1 types by 10%.»; Pasiva de uniforme «Avengers: Age of Ultron»: «Increases basic damage dealt to $HEROCLASS1 types by 10%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |
| Whiplash | Pasiva «Mechanical Engineering»: «Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 80%.» | el juego o foros, y a mano en scripts/contenido/marcadores.csv |

### Objetivo sin nombre (Target ID)

3 casos en 3 personajes y 3 variantes. La etapa se aplica a un grupo de aliados que la API no nombra («Target ID: 72»): la app no puede decir a quiénes les llega. Si Leads & Supports restringe el mismo slot, se dice a quiénes.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Spider-Man (Miles Morales) — Absolute Carnage | Liderazgo «Quick Recovery»: se aplica a «Target ID: 72» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Carnage) |
| Victorious | Liderazgo «For Victory!»: se aplica a «Target ID: 183» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Doctor Doom) |
| Wave | Liderazgo «Ride the Current»: se aplica a «Target ID: 198» | thanosvibs (Leads & Supports restringe el mismo slot al personaje Namor) |

### «Give Power» sin lo que otorga

78 casos en 27 personajes y 68 variantes. «Give Power» («Acquires the following effect…») sin el efecto que sigue: el análisis dice «Otorga un efecto que la fuente no dice». Si Leads & Supports publica el mismo slot, se dice qué trae. El de una Leader Skill que resuelve el juego (scripts/contenido/liderazgos_api.json) no falta.

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
| Sentry (base, Marvel Studios' Thunderbolts*) | Striker «Light and Darkness»: otorga un efecto que la API no dice | la wiki o foros |
| Sentry — Merged | Striker «Light and Darkness»: otorga un efecto que la API no dice; Liderazgo «Shining Hero»: otorga un efecto que la API no dice | la wiki o foros; thanosvibs (Leads & Supports publica el mismo slot: All Basic Attacks, Remove All Debuffs (12 s)) |
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

10 casos en 4 personajes y 10 variantes. Leads & Supports no publica el liderazgo de la variante y el build no pudo derivar ese slot de su Leader Skill (docs/AUDITORIA.md, sección 12, con el mismo motivo): un efecto sin stat o una activación sin correspondencia (ni de Leads & Supports ni a mano), un valor que la API no publica, un «Give Power» o una contradicción de Leads & Supports. La sinergia y los órdenes PvP y PvE no ven ese slot.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Blade (base, 70's Classic, Avengers) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Recovers HP equal to 8% of damage dealt to a target<br>Cannot recover more than 0.5% HP each time damage is dealt.» (HP STEAL) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Silk (sus 3 variantes) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Bleed: Deals additional 10% Damage every 0.7 sec. (Removes Elasticity)» (BLEED) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| White Tiger (sus 2 variantes) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Bleed: Deals additional 10% Damage every 0.7 sec. (Removes Elasticity)» (BLEED) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Yellowjacket (sus 2 variantes) | Liderazgo: no se pudo derivar de la Leader Skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Paralyze» (PARALYZE) | thanosvibs (Leads & Supports), el juego o a mano con su fuente (scripts/contenido/liderazgos_api.json) |

### Soporte que Leads & Supports no publica

5 casos en 3 personajes y 5 variantes. Según el análisis, la pasiva le da algo al equipo, Leads & Supports no publica ese soporte (ni en su slot ni con el nombre de la skill) y el build no lo pudo derivar de la skill de la API (docs/AUDITORIA.md, sección 12, con el mismo motivo): la sinergia no lo cuenta.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Blue Marvel — Classic | Pasiva de uniforme «Classic» le da al equipo «Daño contra ciertos rivales», «Resistencias elementales», Leads & Supports no lo publica y no se pudo derivar de la skill: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Increases damage dealt to targets with 206 effect by 30%» (Natural Enemy); un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Increases damage dealt to targets with 401 effect by 30%» (Natural Enemy) | thanosvibs (Leads & Supports) o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Invisible Woman (base, Future Foundation, Classic) | Pasiva «Invisibility Shift» le da al equipo «Barrera», Leads & Supports no lo publica y no se pudo derivar de la skill: una activación sin correspondencia (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «when hit»; un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Barrier 1 time(s)» (BARRIER) | thanosvibs (Leads & Supports) o a mano con su fuente (scripts/contenido/liderazgos_api.json) |
| Venom — King in Black | Pasiva de uniforme «King in Black» le da al equipo «Curación», «Daño crítico», Leads & Supports no lo publica y no se pudo derivar de la skill: la API no dice a quiénes llega («All Allies y All Allies: a quiénes otorga el «Give Power»») | thanosvibs (Leads & Supports) o a mano con su fuente (scripts/contenido/liderazgos_api.json) |

### Nombre en Leads & Supports distinto del de la skill

16 casos en 14 personajes y 15 variantes. Leads & Supports nombra el soporte o el liderazgo con el nombre de otra skill de la variante o con uno que la variante no tiene. El enlace del «Por qué» busca la skill por ese nombre: con el de otra skill, cae en ella (la «Pasiva 4★ (secundaria)» de Jeff the Land Shark lleva a su Activa 5; la Tier-2 de Polaris — Uncanny X-Men, a su Activa 1).

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Apocalypse — Marvel Animation's X-Men '97 (Young Apocalypse) | Liderazgo: Leads & Supports la llama «Unavoidable Apocalypse», que es su Pasiva T2; su Liderazgo se llama «End of Days» | el juego o foros |
| Arachknight — Arachknight 2099 | Liderazgo: Leads & Supports la llama «Unstoppable», que no es ninguna de sus skills; su Liderazgo se llama «Guardian of Dimensions» | el juego o foros |
| Bullseye — Wastelanders | Liderazgo: Leads & Supports la llama «Correct Arrow», que no es ninguna de sus skills; su Liderazgo se llama «Assassin's Eye» | el juego o foros |
| Destroyer — The Mighty Thor | Pasiva 4★: Leads & Supports la llama «God of Thunder Armor», que es su Activa 5; su Pasiva se llama «Mech Thor» | el juego o foros |
| Electro — Spider-Man: No Way Home | Pasiva 4★: Leads & Supports la llama «Unstable Current», que no es ninguna de sus skills; su Pasiva se llama «Electric Battlefield» | el juego o foros |
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

7 casos en 7 personajes. El texto del artefacto usa valores que thanosvibs no publica en esos niveles de estrellas: la app los marca «sin dato» (docs/AUDITORIA.md, sección 6).

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Agatha Harkness | The Vishanti's Sorcerer Supreme: thanosvibs no publica todos sus valores en 3★, 4★ y 5★ | la wiki (página Artifact) o el juego |
| Domino (sus 3 variantes) | Probability Power: thanosvibs no publica todos sus valores en 3★, 4★ y 5★ | la wiki (página Artifact) o el juego |
| Hulkbuster (Iron Man Mark 44) (sus 5 variantes) | Big Armor: thanosvibs no publica todos sus valores en 3★, 4★, 5★ y 6★ | la wiki (página Artifact) o el juego |
| Inferno (sus 2 variantes) | The Flames of Attilan: thanosvibs no publica todos sus valores en 3★, 4★ y 5★ | la wiki (página Artifact) o el juego |
| Morgan le Fay (sus 3 variantes) | Dark Knowledge: thanosvibs no publica todos sus valores en 3★, 4★ y 5★ | la wiki (página Artifact) o el juego |
| Sunspot | Solar: thanosvibs no publica todos sus valores en 3★, 4★ y 5★ | la wiki (página Artifact) o el juego |
| Wiccan (sus 2 variantes) | Future Demiurge: thanosvibs no publica todos sus valores en 3★, 4★, 5★ y 6★ | la wiki (página Artifact) o el juego |

### Strikers

123 casos en 123 personajes. La app toma los strikers de la pestaña Striker de la página de la wiki: sin ella no tiene los suyos (docs/AUDITORIA.md, sección 11). Que existan en el juego para todos es [Probable].

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Adam Warlock (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
| Agatha Harkness | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
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
| Morgan le Fay (sus 3 variantes) | la wiki no tiene la pestaña Striker de su página | la wiki (pestaña Striker), el juego o foros |
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

33 casos en 33 personajes. La app toma los bonos de la sección Team Bonus de la wiki y de lo que se vio en el juego. Sin ninguno, o solo con los del juego, faltan los demás [Probable].

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Agatha Harkness | no tiene ningún bono de equipo: la wiki no lista ninguno con él | la wiki (sección Team Bonus), capturas del juego o foros |
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

### Sin fila en la Ideal CTP List

1 caso en 1 personaje. La Ideal CTP List ubica a cada personaje en la fila de su C.T.P.

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Agatha Harkness | no está en la Ideal CTP List (CrisisCardio) | thanosvibs (Ideal CTP List) |

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

33 casos en 33 personajes. La guía de armado tiene una fila por personaje y esta no tiene nada de lo que la guía completa (C.T.P., ISO-8, obelisco, lugar en su tier list, cómo se consigue): no está hecha. La ficha y las tarjetas de equipo dicen «sin dato».

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Agatha Harkness | la guía de armado no tiene su fila | la guía de armado o foros |
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

### Sin lugar en la tier list General

1 caso en 1 personaje. La tier list General de thanosvibs ubica a todo el roster.

| Personaje | Qué falta | De dónde podría salir |
|---|---|---|
| Agatha Harkness | no está en la tier list General | thanosvibs (tier list General) |

### Retrato o ícono

4 casos en 2 personajes y 4 variantes. La app baja lo que publica datos.json; sin el archivo, no muestra el retrato o el ícono. El ícono del bando Neutral no lo baja el build: que thanosvibs tenga uno es [Conjetura].

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Agatha Harkness | el ícono de «Neutral» no está en datos.json | thanosvibs (imágenes) |
| Destroyer (sus 3 variantes) | el ícono de «Neutral» no está en datos.json | thanosvibs (imágenes) |

### Rotación

192 casos en 112 personajes y 192 variantes. thanosvibs publica rotaciones por uniforme, y la guía de armado, la del mejor uniforme de cada personaje. Se dice si otro uniforme del personaje tiene la suya.

| Variante | Qué falta | De dónde podría salir |
|---|---|---|
| Agatha Harkness | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros |
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
| Morgan le Fay — Classic | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base y Fallen Soul; la guía de armado tiene la de Fallen Soul |
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
| Wiccan — Young Avengers | ni thanosvibs ni la guía de armado le dan rotación | thanosvibs (rotaciones), la guía de armado o foros; thanosvibs publica la de la base |
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

<details><summary>Adam Warlock: 2 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Marvel Studios' Guardians of the Galaxy 3:** efecto sin clasificar: Pasiva T2

</details>

<details><summary>Agatha Harkness: 9 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** stats; valores del artefacto; strikers; bonos de equipo; Ideal CTP List; fila vacía en la guía de armado; tier list General
- **Base:** retrato o ícono: Neutral; rotación

</details>

<details><summary>Agent 13: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Studios' Captain America: Civil War:** rotación

</details>

<details><summary>Agent Venom: 2 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Agent Anti-Venom:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Ancient One: 6 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **Marvel Studios' Doctor Strange:** «Give Power» vacío: Striker
- **Unleashed Mystic:** «Give Power» vacío: Striker; C.T.P. de su contexto: PvE
- **The Monk of Kamar-Taj:** «Give Power» vacío: Striker; C.T.P. de su contexto: PvE

</details>

<details><summary>Angel: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Angela: 1 faltante, 1 de 4 variantes incompletas</summary>

- **Secret Wars: 1602 Witch Hunter Angela:** marcador sin resolver: Pasiva de uniforme

</details>

<details><summary>Annihilus: 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** rotación

</details>

<details><summary>Ant-Man: 1 faltante, 7 de 7 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Apocalypse: 3 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers; fila vacía en la guía de armado
- **Marvel Animation's X-Men '97 (Young Apocalypse):** nombre en Leads & Supports: Liderazgo

</details>

<details><summary>Arachknight: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Arachknight 2099:** nombre en Leads & Supports: Liderazgo

</details>

<details><summary>Ares: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Punisher:** C.T.P. de su contexto: PvE

</details>

<details><summary>Athena: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Baron Mordo: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado

</details>

<details><summary>Beast: 6 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Age of Apocalypse:** skill sin efectos: Pasiva de uniforme
- **Uncanny X-Men:** skill sin efectos: Pasiva de uniforme
- **All-New X-Men:** efecto sin clasificar: Pasiva T2
- **Marvel Animation's X-Men '97:** efecto sin clasificar: Pasiva T2; C.T.P. de su contexto: PvP

</details>

<details><summary>Bishop: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Black Bolt: 1 faltante, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Black Cat: 1 faltante, 1 de 5 variantes incompletas</summary>

- **Queen in Black:** C.T.P. de su contexto: PvP

</details>

<details><summary>Black Knight: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Black Panther: 1 faltante, 1 de 5 variantes incompletas</summary>

- **Marvel Studios' Captain America: Civil War:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Black Swan: 8 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** falta la skill: Pasiva, Pasiva T2, Activa 4, Activa 5, Definitiva; sin recarga: Activa 3

</details>

<details><summary>Black Widow: 1 faltante, 12 de 12 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Blade: 4 faltantes, 3 de 4 variantes incompletas</summary>

- **Base:** liderazgo sin completar: Liderazgo
- **70's Classic:** skill sin efectos: Pasiva de uniforme; liderazgo sin completar: Liderazgo
- **Avengers:** liderazgo sin completar: Liderazgo

</details>

<details><summary>Blue Dragon: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Liderazgo
- **Moon Temple Defenders:** «Give Power» vacío: Liderazgo

</details>

<details><summary>Blue Marvel: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Classic:** soporte sin Leads & Supports: Pasiva de uniforme

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

<details><summary>Captain America: 1 faltante, 15 de 15 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Captain America (Sharon Rogers): 8 faltantes, 7 de 7 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker; rotación
- **Star Light Armor:** «Give Power» vacío: Striker
- **Dark Star Armor:** «Give Power» vacío: Striker
- **Star Night Armor:** «Give Power» vacío: Striker
- **Light Sirius Armor:** «Give Power» vacío: Striker
- **Poseidon Armor:** «Give Power» vacío: Striker
- **Arctic Warrior:** «Give Power» vacío: Striker

</details>

<details><summary>Captain Marvel: 5 faltantes, 4 de 8 variantes incompletas</summary>

- **Secret Wars: Captain Marvel & The Carol Corps:** skill sin efectos: Pasiva de uniforme
- **Ms. Marvel:** skill sin efectos: Pasiva de uniforme
- **Marvel Studios' Captain Marvel:** skill sin efectos: Pasiva de uniforme
- **Marvel Studios' Avengers: Endgame:** marcador sin resolver: Pasiva de uniforme (2)

</details>

<details><summary>Carnage: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Cassandra Nova: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

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

<details><summary>Daisy Johnson: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Marvel Studios' Agents of S.H.I.E.L.D. (Quake):** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Dazzler: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** ISO-8 u obelisco en la guía de armado
- **X-Song:** rotación; C.T.P. de su contexto: PvE

</details>

<details><summary>Deadpool: 3 faltantes, 9 de 9 variantes incompletas</summary>

- **Personaje:** ISO-8 u obelisco en la guía de armado
- **Marvel Studios' Deadpool & Wolverine:** «Give Power» vacío: Liderazgo
- **Marvel Studios' Deadpool & Wolverine (Nicepool):** C.T.P. de su contexto: PvE

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

<details><summary>Doctor Doom: 2 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **3099:** «Give Power» vacío: Pasiva de uniforme

</details>

<details><summary>Doctor Octopus: 1 faltante, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Doctor Voodoo: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Domino: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** valores del artefacto

</details>

<details><summary>Drax: 4 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** rotación
- **Classic:** rotación
- **Annihilation:** rotación

</details>

<details><summary>Ebony Maw: 1 faltante, 1 de 4 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Echo: 8 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** «Give Power» vacío: Striker
- **Marvel Studios' Hawkeye (Maya Lopez):** «Give Power» vacío: Striker, Liderazgo; rotación
- **Marvel Studios' Echo (Maya Lopez (Echo)):** efecto sin clasificar: Pasiva de uniforme; «Give Power» vacío: Striker, Liderazgo

</details>

<details><summary>Electro: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** rotación
- **Spider-Man: No Way Home:** efecto sin clasificar: Pasiva de uniforme; nombre en Leads & Supports: Pasiva 4★

</details>

<details><summary>Elektra: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Elsa Bloodstone: 2 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Secret Wars: Marvel Zombies:** rotación

</details>

<details><summary>Emma Frost: 2 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Summer Queen:** rotación

</details>

<details><summary>Enchantress: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Exodus: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; ISO-8 u obelisco en la guía de armado

</details>

<details><summary>Falcon: 4 faltantes, 7 de 7 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** rotación
- **All-New Captain America:** rotación
- **Marvel Studios' Captain America: Civil War:** rotación

</details>

<details><summary>Falcon (Joaquin Torres): 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

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

<details><summary>Galactus: 6 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** efecto sin clasificar: Activa 2 (2); rotación

</details>

<details><summary>Gambit: 2 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **X-Men Year-End Party:** C.T.P. de su contexto: PvE

</details>

<details><summary>Gamora: 3 faltantes, 2 de 6 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** skill sin efectos: Pasiva de uniforme; rotación

</details>

<details><summary>Ghost: 3 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Studios' Ant-Man and the Wasp:** skill sin efectos: Pasiva de uniforme; rotación

</details>

<details><summary>Ghost Panther: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Ghost Rider: 7 faltantes, 4 de 6 variantes incompletas</summary>

- **Base:** marcador sin resolver: Pasiva T2; rotación
- **70's Classic:** marcador sin resolver: Pasiva T2; rotación
- **Inhumans: Attilan Rising:** marcador sin resolver: Pasiva T2
- **King of Hell:** marcador sin resolver: Pasiva T2; skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Ghost Rider (Robbie Reyes): 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación

</details>

<details><summary>Giant-Man: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Modern (Goliath):** rotación

</details>

<details><summary>Gilgamesh: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Gorgon: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Base:** marcador sin resolver: Activa 3; rotación

</details>

<details><summary>Gorilla-Man: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** fila vacía en la guía de armado

</details>

<details><summary>Gorr: 8 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** «Give Power» vacío: Pasiva, Pasiva T2, Liderazgo
- **The God Butcher:** efecto sin clasificar: Pasiva de uniforme; «Give Power» vacío: Pasiva, Pasiva T2, Liderazgo

</details>

<details><summary>Green Goblin: 2 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** strikers
- **Ultimate:** rotación

</details>

<details><summary>Groot: 6 faltantes, 5 de 7 variantes incompletas</summary>

- **Base:** rotación
- **Secret Wars: Thors:** rotación
- **Marvel Studios' Avengers: Infinity War:** rotación
- **Marvel Studios' Guardians of the Galaxy 3:** «Give Power» vacío: Pasiva T2
- **Planet X Palm:** «Give Power» vacío: Pasiva T2; rotación

</details>

<details><summary>Gwenpool: 2 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Gwen Poole:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Hades (Pluto): 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Havok: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Hawkeye: 5 faltantes, 5 de 7 variantes incompletas</summary>

- **Base:** rotación
- **Avengers: Age of Ultron:** rotación
- **Marvel Studios' Captain America: Civil War:** rotación
- **Classic:** rotación
- **Wastelanders:** C.T.P. de su contexto: PvE

</details>

<details><summary>Hawkeye (Kate Bishop): 1 faltante, 1 de 3 variantes incompletas</summary>

- **Young Avengers:** rotación

</details>

<details><summary>Hela: 2 faltantes, 2 de 4 variantes incompletas</summary>

- **Base:** rotación
- **Asgard Invasion:** rotación

</details>

<details><summary>Hellstorm: 1 faltante, 1 de 2 variantes incompletas</summary>

- **TVA:** rotación

</details>

<details><summary>Hercules: 4 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** rotación

</details>

<details><summary>Hogun: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** rotación

</details>

<details><summary>Hope Summers: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Hulk: 8 faltantes, 10 de 10 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Secret Wars: Future Imperfect (Maestro):** rotación
- **World War Hulk:** rotación
- **Marvel Studios' Thor: Ragnarok:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Avengers: Endgame:** skill sin efectos: Pasiva de uniforme
- **Team Suit:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Hulk (Amadeus Cho): 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado

</details>

<details><summary>Hulkbuster (Iron Man Mark 44): 4 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** valores del artefacto; fila vacía en la guía de armado
- **Base:** rotación
- **Heavy Duty Armor (Hulkbuster (Iron Man Mark 43)):** rotación

</details>

<details><summary>Human Torch: 6 faltantes, 5 de 5 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **Future Foundation:** «Give Power» vacío: Striker
- **Classic:** «Give Power» vacío: Striker
- **The Fall of the Fantastic Four:** «Give Power» vacío: Striker
- **Marvel Studios' The Fantastic Four: First Steps:** «Give Power» vacío: Striker; rotación

</details>

<details><summary>Hyperion: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Iceman: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Ikon: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Inferno: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** valores del artefacto

</details>

<details><summary>Invisible Woman: 8 faltantes, 5 de 5 variantes incompletas</summary>

- **Base:** soporte sin Leads & Supports: Pasiva
- **Future Foundation:** soporte sin Leads & Supports: Pasiva
- **Classic:** soporte sin Leads & Supports: Pasiva
- **The Fall of the Fantastic Four:** C.T.P. de su contexto: PvE
- **Marvel Studios' The Fantastic Four: First Steps:** «Give Power» vacío: Pasiva de uniforme; rotación; C.T.P. de su contexto: PvP, PvE

</details>

<details><summary>Iron Fist: 3 faltantes, 3 de 5 variantes incompletas</summary>

- **Base:** rotación
- **New Avengers:** rotación
- **All-New, All-Different:** rotación

</details>

<details><summary>Iron Hammer: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Iron Man: 10 faltantes, 6 de 11 variantes incompletas</summary>

- **Base:** rotación
- **Avengers: Age of Ultron:** rotación
- **Secret Wars: 2099:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Captain America: Civil War:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Avengers: Endgame:** marcador sin resolver: Activa 3; rotación
- **Team Suit:** marcador sin resolver: Activa 3; rotación

</details>

<details><summary>Ironheart: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers; fila vacía en la guía de armado
- **Marvel Television's Ironheart:** rotación

</details>

<details><summary>Jean Grey: 1 faltante, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Jeff the Land Shark: 6 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Base:** efecto sin clasificar: Pasiva; nombre en Leads & Supports: Pasiva 4★ (secundaria); rotación

</details>

<details><summary>Jubilee: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; C.T.P. en la guía de armado; ISO-8 u obelisco en la guía de armado
- **Marvel Animation's X-Men '97:** efecto sin clasificar: Pasiva de uniforme

</details>

<details><summary>Juggernaut: 2 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **Savage Avengers:** rotación

</details>

<details><summary>Kahhori: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Kang the Conqueror: 5 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** «Give Power» vacío: Liderazgo
- **Rama-Tut:** efecto sin clasificar: Pasiva de uniforme; «Give Power» vacío: Liderazgo; rotación

</details>

<details><summary>Karnak: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** rotación

</details>

<details><summary>Kid Kaiju: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** rotación
- **Monsters Unleashed! (MFF Variant):** rotación

</details>

<details><summary>Kid Omega: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Uncanny X-Men:** rotación; C.T.P. de su contexto: PvE

</details>

<details><summary>Killmonger: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** rotación

</details>

<details><summary>Kingpin: 3 faltantes, 3 de 4 variantes incompletas</summary>

- **Base:** rotación
- **Secret Wars: Armor Wars:** rotación
- **Marvel Television's Daredevil: Born Again:** rotación

</details>

<details><summary>Kitty Pryde: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Knull: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Ancient History:** efecto sin clasificar: Activa 2

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

<details><summary>Loki: 3 faltantes, 3 de 9 variantes incompletas</summary>

- **Lady Loki:** skill sin efectos: Pasiva de uniforme
- **Marvel Studios' Thor: Ragnarok:** skill sin efectos: Pasiva de uniforme
- **Classic:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Luke Cage: 4 faltantes, 3 de 4 variantes incompletas</summary>

- **Base:** rotación
- **All-New, All-Different:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Luke Cage:** skill sin efectos: Pasiva de uniforme

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

<details><summary>Madelyne Pryor: 5 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado
- **Winter Queen:** efecto sin clasificar: Pasiva de uniforme; rotación

</details>

<details><summary>Magik: 3 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Phoenix Five:** skill sin efectos: Pasiva de uniforme
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

<details><summary>Malekith: 7 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** marcador sin resolver: Pasiva T2 (2); rotación
- **All-New, All-Different:** marcador sin resolver: Pasiva T2 (2); rotación; C.T.P. de su contexto: PvP

</details>

<details><summary>Man-Thing: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

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

<details><summary>Mephisto: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** marcador sin resolver: Pasiva T2
- **Master of Hell:** marcador sin resolver: Pasiva T2; C.T.P. de su contexto: PvP

</details>

<details><summary>Minn-Erva: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Mister Fantastic: 1 faltante, 1 de 5 variantes incompletas</summary>

- **Marvel Studios' The Fantastic Four: First Steps:** rotación

</details>

<details><summary>Mockingbird: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Studios' Agents of S.H.I.E.L.D. (Bobbi Morse):** rotación
- **All-New, All-Different:** rotación

</details>

<details><summary>Molecule Man: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** «Give Power» vacío: Liderazgo

</details>

<details><summary>Molten Man: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** marcador sin resolver: Pasiva

</details>

<details><summary>Moon Girl: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Moon Knight: 1 faltante, 1 de 5 variantes incompletas</summary>

- **Armored:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Morgan le Fay: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** valores del artefacto; strikers
- **Classic:** rotación

</details>

<details><summary>Morph: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Ms. Marvel (Kamala Khan): 3 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Karachi Costume:** rotación

</details>

<details><summary>Mysterio: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Summer Mystery:** «Give Power» vacío: Pasiva T2

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

<details><summary>Nightcrawler: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers
- **X-Force:** rotación
- **Classic:** rotación

</details>

<details><summary>Nova (Richard Rider): 2 faltantes, 1 de 2 variantes incompletas</summary>

- **Marvel Cosmic Invasion:** C.T.P. de su contexto: PvP, PvE

</details>

<details><summary>Nova (Sam Alexander): 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Odin: 4 faltantes, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Avengers 1,000,000 BC:** «Give Power» vacío: Liderazgo
- **Lord of Asgard:** «Give Power» vacío: Liderazgo

</details>

<details><summary>Okoye: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Omega Red: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Phil Coulson: 2 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** rotación
- **A.O.S. Season 3:** rotación

</details>

<details><summary>Polaris: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Uncanny X-Men:** nombre en Leads & Supports: Pasiva de Tier-2; rotación

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

<details><summary>Punisher: 4 faltantes, 8 de 8 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Noir:** rotación
- **War Journal:** rotación

</details>

<details><summary>Quasar (Wendell Vaughn): 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** «Give Power» vacío: Liderazgo

</details>

<details><summary>Quicksilver: 3 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Marvel Legacy:** rotación

</details>

<details><summary>Rachel Summers: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **X-Men: Days of Future Past:** «Give Power» vacío: Liderazgo

</details>

<details><summary>Red Guardian: 1 faltante, 1 de 3 variantes incompletas</summary>

- **Marvel Studios' Thunderbolts*:** efecto sin clasificar: Pasiva de uniforme

</details>

<details><summary>Red Hulk: 1 faltante, 1 de 4 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Red Skull: 9 faltantes, 4 de 4 variantes incompletas</summary>

- **Base:** marcador sin resolver: Pasiva T2 (2); rotación
- **Secret Wars: Red Skull:** marcador sin resolver: Pasiva T2 (2); rotación
- **Hydra Armor:** marcador sin resolver: Pasiva T2 (2)
- **The Crimson Fall:** rotación

</details>

<details><summary>Rhino: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Uncanny Spider-Man:** efecto sin clasificar: Pasiva de uniforme

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

<details><summary>Satana: 2 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Legacy:** skill sin efectos: Pasiva de uniforme

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

<details><summary>Sentinel: 2 faltantes, 2 de 3 variantes incompletas</summary>

- **Base:** rotación
- **Stark Sentinels Mk II:** rotación

</details>

<details><summary>Sentry: 7 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **Merged:** efecto sin clasificar: Pasiva de uniforme; «Give Power» vacío: Striker, Liderazgo
- **Marvel Studios' Thunderbolts*:** efecto sin clasificar: Pasiva de uniforme; «Give Power» vacío: Striker; rotación

</details>

<details><summary>Shadow Shell: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers

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

<details><summary>Silk: 3 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** liderazgo sin completar: Liderazgo
- **Web Suit:** liderazgo sin completar: Liderazgo
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

<details><summary>Sister Grimm: 2 faltantes, 2 de 4 variantes incompletas</summary>

- **All-New, All-Different:** skill sin efectos: Pasiva de uniforme
- **Princess Tsukimi:** rotación

</details>

<details><summary>Skurge: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Sleeper: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** «Give Power» vacío: Pasiva T2

</details>

<details><summary>Songbird: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Spectrum: 1 faltante, 2 de 2 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado

</details>

<details><summary>Spider-Gwen: 1 faltante, 1 de 4 variantes incompletas</summary>

- **Base:** rotación

</details>

<details><summary>Spider-Man: 13 faltantes, 13 de 13 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Secret Wars: Renew Your Vows:** skill sin efectos: Pasiva de uniforme; rotación
- **All-New, All-Different:** skill sin efectos: Pasiva de uniforme; rotación
- **Marvel Studios' Captain America: Civil War:** rotación
- **Spider-Man: Homecoming Homemade Suit:** rotación
- **Spider-Man: Far From Home:** rotación
- **Spider-Man: No Way Home (Integrated Suit):** efecto sin clasificar: Pasiva de uniforme
- **Back to Basics:** efecto sin clasificar: Pasiva de uniforme
- **The Symbiote Suit:** efecto sin clasificar: Pasiva de uniforme
- **Marvel Studios' Spider-Man: Brand New Day:** efecto sin clasificar: Pasiva de uniforme

</details>

<details><summary>Spider-Man (Miles Morales): 7 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** marcador sin resolver: Pasiva T2; rotación
- **Into the Spider-Verse:** marcador sin resolver: Pasiva T2
- **Absolute Carnage:** objetivo sin nombre: Liderazgo; marcador sin resolver: Pasiva T2
- **Anniversary Special:** nombre en Leads & Supports: Liderazgo

</details>

<details><summary>Spider-Woman: 2 faltantes, 1 de 2 variantes incompletas</summary>

- **Spider-Man: Across the Spider-Verse:** «Give Power» vacío: Liderazgo; nombre en Leads & Supports: Liderazgo

</details>

<details><summary>Spot: 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Squirrel Girl: 1 faltante, 3 de 3 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Star-Lord: 2 faltantes, 2 de 7 variantes incompletas</summary>

- **Base:** rotación
- **Space Armor:** rotación

</details>

<details><summary>Storm: 3 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** strikers
- **X-Men Red:** skill sin efectos: Pasiva de uniforme; rotación

</details>

<details><summary>Stryfe: 2 faltantes, 1 de 3 variantes incompletas</summary>

- **The Tyrant of Spring:** «Give Power» vacío: Pasiva de uniforme; rotación

</details>

<details><summary>Sun Bird: 3 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; fila vacía en la guía de armado
- **Moon Temple Defenders:** rotación

</details>

<details><summary>Sunspot: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** valores del artefacto; strikers; bonos de equipo

</details>

<details><summary>Sylvie: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo

</details>

<details><summary>Taskmaster: 5 faltantes, 3 de 3 variantes incompletas</summary>

- **Base:** «Give Power» vacío: Striker
- **Marvel Studios' Black Widow:** «Give Power» vacío: Striker
- **Marvel Studios' Thunderbolts*:** «Give Power» vacío: Striker; nombre en Leads & Supports: Pasiva de Tier-2; rotación

</details>

<details><summary>Thanos: 13 faltantes, 5 de 8 variantes incompletas</summary>

- **Secret Wars: Infinity:** rotación
- **Obsidian King:** efecto sin clasificar: Activa 5; «Give Power» vacío: Pasiva de uniforme
- **Wise Harvester:** efecto sin clasificar: Activa 5; «Give Power» vacío: Pasiva de uniforme, Liderazgo
- **Thanos Wins:** efecto sin clasificar: Activa 5; «Give Power» vacío: Pasiva de uniforme, Liderazgo
- **Annihilation:** efecto sin clasificar: Activa 4; «Give Power» vacío: Pasiva de uniforme, Liderazgo; rotación

</details>

<details><summary>The Hood: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>The Thing: 4 faltantes, 5 de 5 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** rotación
- **Future Foundation:** rotación
- **Marvel Studios' The Fantastic Four: First Steps:** rotación

</details>

<details><summary>Thor: 3 faltantes, 3 de 10 variantes incompletas</summary>

- **Base:** rotación
- **Avengers: Age of Ultron:** rotación
- **Unworthy:** rotación

</details>

<details><summary>Thor (Jane Foster): 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; bono sin nombre

</details>

<details><summary>Titania: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers; bono sin nombre

</details>

<details><summary>Toxin: 2 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers
- **Base:** nombre en Leads & Supports: Liderazgo

</details>

<details><summary>U.S. Agent: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Ulik: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** marcador sin resolver: Activa 3

</details>

<details><summary>Ultron: 17 faltantes, 6 de 6 variantes incompletas</summary>

- **Personaje:** fila vacía en la guía de armado
- **Base:** «Give Power» vacío: Striker; rotación
- **Avengers: Age of Ultron (Ultron Prime):** «Give Power» vacío: Striker; marcador sin resolver: Pasiva de uniforme (2); rotación
- **Avengers: Age of Ultron (Ultron Mark 1):** «Give Power» vacío: Striker; marcador sin resolver: Pasiva de uniforme (2); rotación
- **Avengers: Age of Ultron (Ultron Mark 3):** «Give Power» vacío: Striker; marcador sin resolver: Pasiva de uniforme (2); rotación
- **Marvel Studios' What If...? (Infinity Ultron):** «Give Power» vacío: Striker
- **All-Father Ultron:** «Give Power» vacío: Striker

</details>

<details><summary>Valeria Richards: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo
- **Base:** C.T.P. de su contexto: PvE

</details>

<details><summary>Valkyrie: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Venom: 5 faltantes, 7 de 7 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** rotación
- **Secret Wars: Marvel Zombies:** rotación
- **Anti-Venom:** rotación
- **King in Black:** soporte sin Leads & Supports: Pasiva de uniforme

</details>

<details><summary>Venus (Aphrodite): 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>

<details><summary>Victorious: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** objetivo sin nombre: Liderazgo
- **Emperor Guarder:** nombre en Leads & Supports: Liderazgo, Pasiva 4★; C.T.P. de su contexto: PvP

</details>

<details><summary>Vision: 1 faltante, 1 de 5 variantes incompletas</summary>

- **Ultimate Vision:** rotación

</details>

<details><summary>Volstagg: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** rotación

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

<details><summary>Wasp (Nadia Van Dyne): 1 faltante, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers

</details>

<details><summary>Wave: 1 faltante, 1 de 2 variantes incompletas</summary>

- **Base:** objetivo sin nombre: Liderazgo

</details>

<details><summary>Weapon Hex: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Infected Bioweapon:** «Give Power» vacío: Pasiva T2

</details>

<details><summary>Whiplash: 1 faltante, 1 de 1 variante incompleta</summary>

- **Base:** marcador sin resolver: Pasiva

</details>

<details><summary>White Tiger: 4 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** strikers
- **Base:** liderazgo sin completar: Liderazgo; rotación
- **Marvel Television's Daredevil: Born Again:** liderazgo sin completar: Liderazgo

</details>

<details><summary>Wiccan: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Personaje:** valores del artefacto
- **Young Avengers:** rotación

</details>

<details><summary>Winter Soldier: 5 faltantes, 4 de 7 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Studios' Captain America: Civil War:** skill sin efectos: Pasiva de uniforme; rotación
- **Captain America:** rotación
- **Marvel Studios' Avengers: Infinity War:** skill sin efectos: Pasiva de uniforme

</details>

<details><summary>Wolverine: 5 faltantes, 8 de 8 variantes incompletas</summary>

- **Personaje:** strikers; ISO-8 u obelisco en la guía de armado
- **Age of Apocalypse:** rotación
- **All-New Marvel NOW!:** rotación
- **Marvel Studios' Deadpool & Wolverine:** C.T.P. de su contexto: PvE

</details>

<details><summary>Wong: 3 faltantes, 3 de 4 variantes incompletas</summary>

- **Base:** rotación
- **Marvel Studios' Doctor Strange:** rotación
- **What If... Zombies?!:** C.T.P. de su contexto: PvE

</details>

<details><summary>X-23: 1 faltante, 4 de 4 variantes incompletas</summary>

- **Personaje:** strikers

</details>

<details><summary>Yelena Belova: 2 faltantes, 1 de 4 variantes incompletas</summary>

- **Marvel Studios' Thunderbolts*:** rotación; C.T.P. de su contexto: PvE

</details>

<details><summary>Yellowjacket: 2 faltantes, 2 de 2 variantes incompletas</summary>

- **Base:** liderazgo sin completar: Liderazgo
- **Marvel NOW!:** liderazgo sin completar: Liderazgo

</details>

<details><summary>Yondu: 1 faltante, 1 de 4 variantes incompletas</summary>

- **All-New, All-Different:** rotación

</details>

<details><summary>Zeus: 3 faltantes, 1 de 1 variante incompleta</summary>

- **Personaje:** strikers; bonos de equipo; fila vacía en la guía de armado

</details>
