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
  con la historia de cada uno). Los datos publicados salen de main. Con un formato nuevo, primero va el
  push de main, después se corre a mano el workflow de datos y, cuando termina bien, la etiqueta `vX.Y.Z`
  va sobre ese commit de datos: así la release ya sale con los datos que pide (con la 1.0.17, la etiqueta
  salió antes y la app quedó esperando). El workflow arma la release con la etiqueta.
- Build: `python3 scripts/build.py`, sobre lo bajado en `work/` (sin red). Regenera `data.js`,
  `datos.json`, `docs/AUDITORIA.md`, `docs/CATALOGO.md` y `docs/COMPLETITUD.md`; para con un mensaje
  si el contenido curado (`scripts/contenido/`) no cierra con los datos. El contenido curado llega a
  los datos recién cuando corre el build: sin `work/`, se valida con `catalogo.validar` (con
  `contenido/guia.json`, por los topes), `catalogo.validar_glosario`, `catalogo.validar_valor` (la
  tabla de valor de los equipos) y `fuentes.validar_contenido`;
  `scripts/contenido/liderazgos_api.json` lo valida `liderazgos.validar` contra las tablas de la API
  (sin `work/`, con el `MFF_TABLAS` de data.js: `liderazgos_api/prueba.py`).
- Pruebas: no están en el repo. Son scripts de Playwright contra la app servida por
  `desktop/lanzador.py`, con modelos de la sinergia y del puntaje escritos aparte de `app.js`. La
  copia más reciente va en un zip junto al último bundle (`pruebas-mff-*.zip`); su `LEEME.txt` dice
  qué rutas adaptar. `images/` y `work/` no están en el repo: las imágenes se bajan con
  `bajar_imagenes.py`, y sin `work/` no corren verif_guia_ficha, verif_marcadores ni verif_opciones.
  Las que leen el contenido curado del repo (verif_glosario) fallan contra un data.js viejo:
  `armar_datos_contenido.py` arma datos de prueba con el contenido nuevo, y `armar_datos_build.py`, con
  lo que el próximo build cambia en data.js (hoy, el formato 8: el catálogo con la regla de cada stat,
  si se acumula y su tope, la tabla de valor `MFF_VALOR`, `SEED.SKILL_TAGS` y el análisis recalculado
  con `scripts/modelo.py`).
  `armar_datos_build.py` recalcula también los roles. `armar_datos_lideres.py` les suma los liderazgos
  que el build deriva de la Leader Skill (`scripts/liderazgos.py`, con las correspondencias a mano de
  `scripts/contenido/liderazgos_api.json`, sus traducciones en `MFF_TXT` y la sección 12 de
  `docs/AUDITORIA.md` y `docs/COMPLETITUD.md` rehechas), y `liderazgos_api/prueba.py` prueba esa función
  y `liderazgos.validar` sin `work/`. `verif_otorga.py` prueba el aviso del «Give Power» que ninguna
  fuente publica, y que no va donde lo dice el juego. `armar_datos_cierre.py` les suma lo que el build
  corrige de thanosvibs con el juego (`fuentes.nombre_ctp` y `fuentes.linea_artefacto`, con la sección 5
  de `docs/AUDITORIA.md`), y `verif_cierre.py` lo prueba en la app.
  `verif_consistencia.py` compara, para las 888 variantes, lo que contesta cada pantalla a la misma
  pregunta (formato de los soportes, verificación, recarga, filas de las listas, habilidades del
  filtro, efectos de la comparativa, strikers; y, con las reglas del 4 de octubre, el C.T.P.
  recomendado, el líder del trío, los strikers que desempatan, «le sirve», lo propio y los
  anti-mermas, y la fuente de cada liderazgo; con las del 5 de octubre, el filtro «Solo el último
  uniforme», la habilidad que cuenta una vez y si cada stat se acumula y su tope) y lista como
  pendiente la de los recomendados de Modos. `verif_ultimo_uniforme.py`, `verif_solapado.py` y
  `verif_acumula.py` prueban esas cosas en pantalla y contra modelos aparte, y `medir_solapado.py`
  mide, contra otro app.js, cuánto cambian las listas. `verif_historico.py` prueba el histórico (datos, la pestaña, los
  filtros, la ficha, los links, inglés y celular) contra un modelo con `MFF_HISTORICO`. `verif_trabada.py` prueba la pantalla de datos
  cuando lo publicado es de otro formato (más nuevo con y sin versión nueva de la app, más viejo, igual, inglés). Con datos de una versión más
  nueva que la publicada, `MFF_DATOS` apunta a datos armados con el build sobre lo bajado ese día (sin `work/` en la
  carpeta de Ezequiel: se baja con `fetch_all.py --no-portraits` en el contenedor). verif_consistencia tarda más de 25
  min y su página llega a unos 5,5 GB: en un contenedor de 8 GB va sola (con otra prueba al lado, el OOM mata la página y
  la prueba queda colgada).

## Estado (5 de octubre de 2026)

- Publicadas: de la 1.0.14 a la 1.0.23. La 1.0.13 no se publicó; las notas de la 1.0.14 anuncian su Glosario.
- La 1.0.23 (etiqueta en 39852b8, «Datos actualizados 2026-10-05», datos de formato 10) trajo el histórico de los
  personajes y lo de la 1.0.22. Su build dio lo esperado: 64 stats que se suman, 19 que cuentan una vez y 16 con tope;
  `docs/HISTORICO.md` con 213 versiones (181 con nota) y 191 notas.
- La 1.0.22 salió mal: Ezequiel empujó los dos bundles juntos y la etiqueta `v1.0.22` fue sobre 4a14974 (el commit de la
  versión, con datos de formato 8), mientras el workflow publicaba desde main los de formato 10. Los de formato 9 nunca
  se publicaron, y la 1.0.22 instalada quedó trabada en la pantalla de datos («actualizá la app»), que no ofrecía el
  parche: se arregla con el instalador de la 1.0.23. De ahí la 1.0.24 (abajo).
- La 1.0.21 trajo los datos de formato 8; la 1.0.20, los de formato 7. La 1.0.17 trajo los de formato 6: su etiqueta salió
  antes que los datos y la app actualizada quedó esperando hasta «Datos actualizados 2026-10-03».
- Entregada sin publicar: la 1.0.24, solo programa (datos de formato 10, sin cambio): la pantalla de datos ofrece la
  versión de la app que lee los datos publicados si son de un formato más nuevo, y publicar.yml no publica una versión si
  los datos del commit etiquetado o los de main no son del formato que pide `version.json`.

## Pendiente

Al publicar la 1.0.24 (pantalla de datos y publicar.yml):
- Sin formato nuevo: push de main y la etiqueta `v1.0.24` sobre el commit «Versión 1.0.24» (sus datos son los de 39852b8,
  de formato 10, como los publicados), sin correr el workflow de datos. publicar.yml chequea los dos formatos antes de
  armar nada.
- Una versión por vez: con un formato nuevo, primero los datos y la etiqueta de esa versión, y recién después la
  siguiente (lo que salió mal con la 1.0.22).
- Guaranteed Critical Rate cuenta una vez y lo dan 10 soportes: la de mayor valor puede cambiar algún trío (sin medir).
- Las listas de PvE bajan con el vínculo del líder del contexto (Knull — Ancient History, de 15.102 a 9.997): que
  Ezequiel mire una con los datos nuevos («Equipos por contexto» de `docs/MODELO.md`).

Histórico (1.0.23):
- Cómo se arma (`scripts/historico.py`): cada nota va a la versión de thanosvibs de fecha más cercana, a 4 días o menos;
  cada llegada de `/api/updates` (personaje, uniforme, T3, TP, T4) lleva el texto de esa nota que nombra al personaje
  (por nombre o alias); cada sección de skills o de balance (título con balanc, rework, adjust, skill, improve...) da un
  hecho «balance» por personaje nombrado. Por ahora solo personajes y el texto en inglés.
- Tareas futuras del histórico (Ezequiel, 5 de octubre): revisar las notas del foro coreano (si la traducción inglesa
  está bien y si completa cosas) y sumar los modos de juego. Las 207 llegadas sin nota (162 en versiones sin nota, casi
  todas parches de mitad de mes de 2020 y 2021, que es probable estén en otro tablero; el resto, nombres distintos o
  detalles en imágenes) están en `docs/HISTORICO.md`.

Preguntas para Ezequiel (de los carriles del 4 y 5 de octubre):
- Liderazgos: los 34 slots sin stat (escudo de energía y físico, inmunidad al frío, robo de vida, inmunidad a todo
  daño, resistencia al veneno, inmunidad al sangrado y a la fractura; el sangrado y la parálisis son para el rival):
  ¿se agregan stats al catálogo? «When enemies are below 30% HP,» (Warwolf) va con la coma de la API.
- ¿Un aviso de Insight o Liberation repetidos en un equipo? (Los stats dudosos de `acumula` los confirmó el 5 de
  octubre.)
- De las habilidades que cuentan una vez (carril filtro2), lo que decidió Claude y falta confirmar: entre dos
  soportes de los que no lideran, va primero el de clave menor (un orden fijo, para que el trío dé lo mismo desde la
  lista de cualquiera: el juego no dice cuál; cambia el puntaje si solo uno de los dos trae además otra cosa que se
  aplica: con el orden al revés, en 20.000 tríos con algo sin valor cambian 3 sinergias y 2 puntajes de PvP y de
  PvE, medido con la primera parte); la regla vale también para el liderazgo en la sinergia sin contexto (un
  liderazgo que solo le da a los demás lo que ya tienen propio no suma ni vincula); y en PvP y PvE el vínculo por un
  soporte se cuenta con el líder del contexto. Los topes se muestran con lo que suman liderazgos, soportes y
  artefactos, sin lo que el personaje ya tiene ni los bonos de equipo, y no cambian los puntos.
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
  PvP otro tanto. Con *Efectos iguales* (5 de octubre), las listas de PvP y PvE más pesadas con una habilidad
  tardan más. Con el arreglo de la segunda parte del carril filtro2 (elegir la fuente sin ordenar el equipo y no
  recontar el vínculo cuando no hace falta), consulta + orden: Silver Surfer (Shalla-Bal) en PvP, 1,7 + 2,3 s
  (antes de la regla, 1,3 + 1,6; con la primera parte, 2,0 + 3,0); Invisible Woman — The Fall of the Fantastic
  Four en PvE, 2,4 + 3,3 s (1,7 + 1,8; 2,5 + 3,7). Lo que queda es la regla misma: qué fuente se le aplica a cada
  uno y el vínculo por un soporte con el líder del contexto (`vinculosSoporte`, una sinergia entera, hasta 195.000
  veces en esas listas). Bajarlo más pediría contar ese vínculo sin la sinergia entera: otra ruta [Probable].
- Si las pruebas pasan al repo.
