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
  salió antes y la app quedó esperando). Sin formato nuevo, la etiqueta va sobre el commit de la versión. Una
  versión por vez: con un formato nuevo, los datos y la etiqueta de esa versión van antes de entregar o empujar la
  siguiente (con la 1.0.22, dos bundles empujados juntos dejaron la etiqueta sobre datos de otro formato). Publicar
  es solo empujar la etiqueta: el workflow «Publicar versión» arma la release con ella y no se corre a mano.
  `publicar.yml` corta si los datos del commit etiquetado o los de main no son del formato de `version.json`.
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
  filtros, la ficha, los links, inglés y celular) contra un modelo con `MFF_HISTORICO`. `verif_mesa.py` prueba la mesa de trabajo (1.0.25: tres
  paneles, poner y quitar, líder, restricción de Alliance Battle contra un modelo, bonos activos, guardar, la capa, comparar,
  ventana angosta); desde la 1.0.25 las que usaban el armador viejo de Equipos o la barra de comparar del roster usan la mesa.
  `verif_filas` y `verif_export_viejo` comparan contra versiones viejas (worktrees que ya no están) y no corren solas; las
  que miran retratos (`verif_paginador`, `verif_servidor_caido`) necesitan `images/` en el repo (un enlace a las bajadas
  sirve: `.gitignore` no tapa un enlace, que no se commitea). `verif_trabada.py` prueba la pantalla de datos
  cuando lo publicado es de otro formato (más nuevo con y sin versión nueva de la app, más viejo, igual, inglés). Con datos de una versión más
  nueva que la publicada, `MFF_DATOS` apunta a datos armados con el build sobre lo bajado ese día (sin `work/` en la
  carpeta de Ezequiel: se baja con `fetch_all.py --no-portraits` en el contenedor). verif_consistencia tarda más de 25
  min y su página llega a unos 5,5 GB: en un contenedor de 8 GB va sola (con otra prueba al lado, el OOM mata la página y
  la prueba queda colgada).

## Estado (6 de octubre de 2026)

- Publicadas: de la 1.0.14 a la 1.0.25 (la 1.0.13 no se publicó; las notas de la 1.0.14 anuncian su Glosario).
- Entregada sin publicar: la 1.0.26 (la lista de la izquierda con la búsqueda y los filtros del roster, también en
  Equipos; Ezequiel: sin filtros era inutilizable). Etiqueta sobre «Versión 1.0.26», sin workflow de datos.
- La 1.0.25 (etiqueta en 676f50a), solo programa (datos de formato 10, sin cambio), la *mesa de trabajo* a prueba
  (Ezequiel, 6 de octubre: «me gusta... no estoy 100% convencido... lo podemos probar a ver si realmente mejora»): el
  aspecto de la maqueta B (grafito, ámbar, Chakra Petch / Instrument Sans / JetBrains Mono; el rojo, solo para errores) y
  tres paneles: la lista del roster a la izquierda en la ficha, la mesa a la derecha en todas las secciones (`U.mesa` en la
  capa). La mesa reemplaza al armador de Equipos. Maquetas: «Arquitectura MFF.ar» (#24) y «MFF.ar · dos direcciones».
  Cada equipo guardado lleva su líder declarado (`lider`, Ezequiel: «necesita estar declarado como tal para el cálculo de
  estadísticas»); los de antes reciben el de la sinergia al cargar la capa, con aviso en Equipos.
  Ezequiel (6 de octubre), sobre la 1.0.25: la mesa puede quedar, pero #24 no está hecho: la meta es mejorar cómo se
  ve y se prioriza la información, y la 1.0.25 solo agregó la mesa encima de lo que había (las pantallas siguen igual).
- La 1.0.24 (etiqueta en ae17e4e, «Versión 1.0.24», solo programa, datos de formato 10 sin cambio): la pantalla de
  datos ofrece la versión de la app que lee los datos publicados si son de un formato más nuevo, y publicar.yml no
  publica una versión con datos de otro formato. Release con sus tres archivos (instalador, parche y `latest.json`).
  Después, main recibió «Datos actualizados 2026-10-05» (e26fee1).
- La 1.0.23 (etiqueta en 39852b8, datos de formato 10) trajo el histórico de los personajes y lo de la 1.0.22.
- La 1.0.22 salió mal: la etiqueta fue sobre 4a14974 (el commit de la versión, con datos de formato 8) mientras el
  workflow publicaba los de formato 10; los de formato 9 nunca se publicaron y la 1.0.22 instalada quedó trabada en
  la pantalla de datos hasta reinstalar. De ahí la 1.0.24 y la regla de una versión por vez.

## Pendiente

Todo lo pendiente está en los issues de GitHub (wittyar/mff.ar), ordenado por tema; antes de empezar, leer los
abiertos. Decisiones de Ezequiel del 6 de octubre de 2026:
- Equipos (#34): la construcción se rehace completa como consulta sobre tags curados por personaje, armada en
  pasos y sin puntajes calculados que no se ven. Reemplaza la sinergia, la tabla de valor y las listas actuales (el
  liderazgo de Hulk — Amadeus Cho sale primero en varias listas). Los issues de las reglas actuales (#9, #12, #21,
  #22, #27, #29, #30) se revisan contra eso.
- Análisis (#33): no sirve como está; falta revisar el «sin números» del 1 de octubre.
- Antes de cualquier cambio visual, la propuesta de arquitectura de la información y de navegación (#24, con los
  casos de strikers y Glosario en sus comentarios); después el rediseño visual (#6) y el tooltip de las habilidades
  (#39).
- Español de la app con los términos del juego en español (#32), con capturas que va a pasar Ezequiel.
- Robustez: datos por formato (#1) y pantalla de rescate (#2).
- Apartados nuevos: Cromos de cómic (#35), Espadas (#36), Jarvis (#37, falta el alcance); atributos de las skills
  (#38).
- Histórico: foro coreano (#3), modos (#4), llegadas sin nota (#5). Preguntas abiertas: #10 a #23. Bugs: #25, #26.
  Pruebas en el repo: #31.
