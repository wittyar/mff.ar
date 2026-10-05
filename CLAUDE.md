# MFF.ar: notas para Claude

Comparador personal de MARVEL Future Fight de Ezequiel, como app de escritorio (README.md). El
modelo del juego, con las reglas y decisiones de Ezequiel y de dónde sale cada dato, está en
`docs/MODELO.md`; lo que no cierra entre fuentes, en `docs/AUDITORIA.md`; lo que le falta a cada
variante, en `docs/COMPLETITUD.md`.

## Cómo trabajamos

- En español, directo y sin halagos. Lo que no es trivial va marcado [Comprobado], [Probable] o
  [Conjetura]; las respuestas importantes cierran con «Verificá por tu cuenta:». Antes de
  preguntar, se usa lo que hay (el repo, los datos, la web). Las prioridades las decide Ezequiel.
- Código: una sola ruta (sin caminos alternativos ni capas de compatibilidad), nada silencioso
  (nada se degrada ni cambia sin error o aviso), simple antes que defensivo, commits atómicos (una
  intención por commit; el que cambia una firma lleva sus llamadas), la causa y no el síntoma.
- Entregas: el push desde el contenedor de Claude está bloqueado por el proxy, y no se esquiva. Se
  commitea en un clon y se entrega un `git bundle` (`origin/main..main`, después de `git fetch`) con
  un nombre nuevo cada vez (fecha y hora UTC) en la carpeta del repo, con el comando de pull. El push
  y las etiquetas los hace Ezequiel. No se reescribe historia ya entregada. En su carpeta, solo git
  de lectura.
- Versiones: `version.json` (versión, notas para el usuario, formato de datos). El formato sube
  cuando la app nueva necesita algo que los datos viejos no traen (`FORMATO` en `scripts/build.py`,
  con la historia de cada uno). Los datos publicados salen de main: con un formato nuevo, el push y
  la etiqueta `vX.Y.Z` van juntos. El workflow arma la release con la etiqueta.
- Build: `python3 scripts/build.py`, sobre lo bajado en `work/` (sin red). Regenera `data.js`,
  `datos.json`, `docs/AUDITORIA.md`, `docs/CATALOGO.md` y `docs/COMPLETITUD.md`; para con un mensaje
  si el contenido curado (`scripts/contenido/`) no cierra con los datos. El contenido curado llega a
  los datos recién cuando corre el build: sin `work/`, se valida con `catalogo.validar`,
  `catalogo.validar_glosario`, `catalogo.validar_valor` (la tabla de valor de los equipos) y
  `fuentes.validar_contenido`; `scripts/contenido/liderazgos_api.json` lo valida `liderazgos.validar`
  contra las tablas de la API (sin `work/`, con el `MFF_TABLAS` de data.js: `liderazgos_api/prueba.py`).
- Pruebas: no están en el repo. Son scripts de Playwright contra la app servida por
  `desktop/lanzador.py`, con modelos de la sinergia y del puntaje escritos aparte de `app.js`. La
  copia más reciente va en un zip junto al último bundle (`pruebas-mff-*.zip`); su `LEEME.txt` dice
  qué rutas adaptar. `images/` y `work/` no están en el repo: las imágenes se bajan con
  `bajar_imagenes.py`, y sin `work/` no corren verif_guia_ficha, verif_marcadores ni verif_opciones.
  Las que leen el contenido curado del repo (verif_glosario) fallan contra un data.js viejo:
  `armar_datos_contenido.py` arma datos de prueba con el contenido nuevo, y `armar_datos_build.py`, con
  lo que el próximo build cambia en data.js (hoy, el formato 7: el catálogo con la regla de cada stat,
  la tabla de valor `MFF_VALOR`, `SEED.SKILL_TAGS` y el análisis recalculado con `scripts/modelo.py`).
  `armar_datos_build.py` recalcula también los roles. `armar_datos_lideres.py` les suma los liderazgos
  que el build deriva de la Leader Skill (`scripts/liderazgos.py`, con las correspondencias a mano de
  `scripts/contenido/liderazgos_api.json`, sus traducciones en `MFF_TXT` y la sección 12 de
  `docs/AUDITORIA.md` y `docs/COMPLETITUD.md` rehechas), y `liderazgos_api/prueba.py` prueba esa función
  y `liderazgos.validar` sin `work/`. `verif_otorga.py` prueba el aviso del «Give Power» que ninguna
  fuente publica, y que no va donde lo dice el juego.
  `verif_consistencia.py` compara, para las 888 variantes, lo que contesta cada pantalla a la misma
  pregunta (formato de los soportes, verificación, recarga, filas de las listas, habilidades del
  filtro, efectos de la comparativa, strikers; y, con las reglas del 4 de octubre, el C.T.P.
  recomendado, el líder del trío, los strikers que desempatan, «le sirve», lo propio y los
  anti-mermas, y la fuente de cada liderazgo) y lista como pendiente la de los recomendados de Modos.

## Estado (4 de octubre de 2026)

- Publicadas: de la 1.0.14 a la 1.0.17. La 1.0.13 no se publicó; las notas de la 1.0.14 anuncian
  su Glosario.
- La 1.0.17 trajo los datos de formato 6. Su etiqueta salió antes que los datos, y la app
  actualizada quedó esperando hasta que el workflow publicó «Datos actualizados 2026-10-03». En la
  sección 8 de AUDITORIA.md, los marcadores quedaron así: 3 a mano, 131 de Leads & Supports, 38 de
  la wiki y 77 sin resolver.
- Entregadas sin publicar, las dos con datos de formato 6 (el push y la etiqueta pueden ir juntos):
  - La 1.0.18: casillas por cobertura en las combinaciones, los C.T.P. de la guía de armado en cada
    tarjeta, y el «Por qué» y el detalle de PvP y PvE rehechos para que se lean (suma de lo que le
    llega, desglose por origen con link a cada habilidad).
  - La 1.0.19: el «Cómo funciona» de cada skill (cinco secciones, al tocarla en la pestaña Skills),
    `docs/COMPLETITUD.md` y el contenido curado revisado con NamuWiki y con las 380 capturas del
    juego del 2 de octubre. Ese contenido llega a los datos cuando corre el workflow: conviene
    correrlo a mano después del push.

## Pendiente

Al publicar (lo del 4 y 5 de octubre: las reglas de los equipos, los liderazgos de la Leader Skill y lo que
dejaron el foro y las capturas en coreano):
- `version.json` pide el formato 6 y `scripts/build.py` escribe el 7: subir `formato_datos` a 7 en el commit que
  publica, con la etiqueta, y correr el workflow de datos después del push.
- Lo que tiene que dar el próximo build (sin `work/` no se pudo correr; las cifras son de los datos de prueba de
  formato 7 del 5 de octubre y se mueven si thanosvibs cambió algo; lo que no puede pasar es algo sin listar):
  - `SEED.SKILL_TAGS` con Zombi y Guardianes de la Galaxia, y en la sección 11 de `docs/AUDITORIA.md` las dos
    probabilidades de striker de más de 100% (Daken: Doctor Octopus, 219%; Molecule Man: Morgan le Fay, 120%).
  - Liderazgos de la Leader Skill: 443 variantes (461 slots, con `"src": "api"`) derivadas y 35 slots sin derivar
    (34 por un efecto sin stat en el catálogo y el «Give Power» de Sentry — Thunderbolts*); en la verificación, de
    448 slots, 394 iguales, 5 distintos, 47 que no se pueden derivar y 2 solo en Leads & Supports; en
    `docs/COMPLETITUD.md`, «Liderazgo sin completar» en 35 variantes y 177 de 888 completas. Hasta ese build,
    `scripts/completitud.py` sobre el data.js del repo para con «data.js no trae los liderazgos…»: es lo esperado.
  - Con aviso en el log y en la sección 5 de `docs/AUDITORIA.md`: «Judgment» y Planet Eater. En la sección 8, un
    marcador más a mano (Hell Fire de Mephisto — Master of Hell). En el análisis, 80 «Give Power» sin lo que
    otorgan, en 69 variantes, y Stryfe — The Tyrant of Spring con el rol Soporte.
  - Después, verif_consistencia y la regresión tienen que pasar con los datos del repo, y verif_marcadores (con
    `work/`) tiene que actualizar sus cuentas.
- Las listas de PvE bajan con el vínculo del líder del contexto (Knull — Ancient History, de 15.102 a 9.997): que
  Ezequiel mire una antes de publicar («Equipos por contexto» de `docs/MODELO.md`).

Preguntas para Ezequiel (de los carriles del 4 y 5 de octubre):
- La tabla de valor (`scripts/contenido/valor_equipos.json`) es la propuesta del 4 de octubre: ¿la confirma con los
  «Casos de referencia» de `docs/MODELO.md`?
- Captain America tiene anti-mermas propio con probabilidad (50% o 60% al recibir un debuff), y hoy no cuenta. ¿Está
  bien?
- Cinco stats de bonos de la wiki no tienen efecto en el catálogo (Attack Defense, Critical Defense, Energy Damage,
  Max Dodge y Physical Damage; el próximo build los avisa en la sección 9): ¿cómo se clasifican?
- Liderazgos: los 34 slots sin stat (escudo de energía y físico, inmunidad al frío, robo de vida, inmunidad a todo
  daño, resistencia al veneno, inmunidad al sangrado y a la fractura; el sangrado y la parálisis son para el rival):
  ¿se agregan stats al catálogo? «When enemies are below 30% HP,» (Warwolf) va con la coma de la API.
- Efectos repetidos en el equipo: lo oficial de los C.T.P. apunta a contar el mayor y no la suma, y la sinergia
  suma cada soporte (`docs/MODELO.md`). ¿Se cambia? ¿Y un aviso de Insight o Liberation repetidos en un equipo?
- C.T.P.: ¿la app muestra los números del juego por grado (un archivo de contenido nuevo y formato)?
- Las opciones de uniforme en Mítico muestran ataques y defensas +40% (hallazgo `opciones-uniforme-mitico`): ¿a
  qué se debe?
- Strikers vistos en el juego (Galactus, 16; Mephisto, al menos 91 contra 90 de la wiki; Kingpin coincide): ¿se
  cargan, con el juego por encima de la wiki? Pide un archivo de contenido, una fuente y código.
- ¿Se cargan los efectos propios de las habilidades (hallazgo `habilidades-efecto-propio`)? Y, del carril ko-u:
  ¿van a Modos la recompensa de ocupación y las fases de Alliance Conquest (sus pantallas no tienen fuente
  todavía), el equipo de élite a la hoja de ruta y la regla del instinto a Armado? ¿Los efectos de alianza de Nv.
  30 aparecen en la pantalla de stats del personaje?
- Para ver en el juego: amplificar una pieza en +20 sin urus (urus contra ranuras: hallazgo
  `uru-amplificacion-guia`); si entran dos Odin's Blessing de distinto tipo en una pieza; en Alliance Conquest, si
  se puede atacar una defensa que ya pelea alguien de la alianza (hallazgo `conquista-defensas-coreano`); el
  instinto de los 15 sin dato, con el filtro por instinto.
- Capturas que faltan: Soul Contract de Mephisto base en el 도감 (decide si Leads & Supports tiene mal la base:
  hallazgo `mephisto-base-leads-supports`); en el 특수 장비 도감, el «?» de 재련 옵션, la opción fija de las 30
  fichas reforjadas con el scroll abajo (Wall y los valores de Brilliant), la sección de Greed debajo de 옵션1 y el
  lápiz de 적용 콘텐츠 (qué modos son PVP y PVE); el panel de 진영 / SIDE hasta abajo (la nota de los Villains); la
  pestaña Striker de Mephisto con superposición entre capturas; «TEAM BONUS PER CHARACTER» de cada candidato a
  bono (la barra muestra el nombre; 301 a 303 del 4 de octubre no son bonos) y la lista de Galactus hasta Heralds
  #3. Sentry — Thunderbolts* no tiene fuente para su «Give Power».

Sin decidir, de antes:
- Consistencia entre pantallas: los recomendados de Modos contra la función en PvP y PvE (verif_consistencia la
  tiene como pendiente).
- Volumen de las listas (medido el 2 de octubre sobre la 1.0.14; hay que volver a medirlo). Exigir en PvP un
  liderazgo que valga saca el 59% de las tarjetas; una lista por personaje en vez de una por uniforme, el 54%; las
  dos juntas, el 80%.
- El filtro de PvP acepta anti-mermas condicionales (al recibir un debuff).
- Liderazgo en PvP: Molecule Man es «la excepción rara» (Ezequiel) y hoy no suma nada fuera de los anti-mermas, ni
  tiene lista de PvP; el daño contra una facción no cuenta (NamuWiki: el tercero de un equipo de Timeline suele ser
  un «buffer» de daño entre facciones, y Molecule Man ignora justamente eso).
- Compañeros sin función en el contexto: entran igual si tienen vínculo con él. ¿Quedan fuera, como el personaje
  de la ficha?
- Completitud: si los que la guía de armado marca «dont waste gold» cuentan como faltantes y si el informe (unos
  220 KB) se achica.
- Que publicar.yml no publique una versión si el `datos.json` de main no es del formato de `version.json` (evita lo
  que pasó con la 1.0.17).
- Equipos (1.0.18): las casillas siguen marcadas al cambiar de orden, de uniforme o de personaje, como «Sin»;
  Alliance Battle muestra los C.T.P. de PvE, pero la leyenda de la guía dice «ABX: Rage», y sus equipos
  recomendados y los descartados no muestran C.T.P.; el link de un soporte busca la skill por el nombre que le da
  Leads & Supports (la «Pasiva 4★ (secundaria)» de Jeff es su Activa 5; en Polaris — Uncanny X-Men el nombre de la
  Tier-2 está mal y el link cae en la Activa 1).
- Marcadores: el mismo par de valores en otro orden cuenta como diferencia entre fuentes (Abomination base, Fists
  of the World Ravager); Falcon (Joaquin Torres) tiene la Tier-2 en `passive` en Leads & Supports y no se cruza;
  las filas vacías de `marcadores.csv` que ahora resuelve Leads & Supports siguen en la tabla; los avisos de
  `soportes()` salen dos veces en el log del build.
- Bonos de equipo del juego por confirmar con capturas: W, D, R y SW; con duda, Sersi, Beta Ray Bill, Amadeus Cho,
  Doom y Kang; el segundo stat de Heralds #3; la lista de Annihilus.
- El artefacto de Robbie Reyes da daño según la resistencia a los aliados Llama: depende de que él esté en el
  equipo, y «le sirve» no ve el equipo.
- Set Striker: es otro sistema y la app no lo tiene. A 119 personajes la wiki no les tiene la pestaña Striker.
- Las «permutaciones» de los mismos integrantes que Ezequiel vio en la lista de Adam Warlock no aparecen en las
  listas; si vuelven, falta una captura.
- Rendimiento: con quien da algo a todos (Galactus), la consulta de combinaciones tarda cerca de 1,5 s y el orden
  PvP otro tanto.
- Si las pruebas pasan al repo.
