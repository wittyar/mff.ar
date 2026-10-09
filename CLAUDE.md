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
  `publicar.yml` corta si los datos del commit etiquetado o los de main en `datos/<formato>/` no son del formato de
  `version.json`. Desde la 1.0.30 (#1) la app baja los datos de `datos/<formato>/` (los copia ahí
  `scripts/carpeta_formato.py`, que corre el build); la raíz se sigue publicando para las versiones hasta la 1.0.29.
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
  sirve: `.gitignore` no tapa un enlace, que no se commitea). `verif_trabada.py` prueba que la app baja los datos de
  la carpeta de su formato aunque la raíz publique uno más nuevo, y la pantalla de datos sin su carpeta (1.0.30);
  `verif_rescate.py`, la pantalla de rescate (1.0.31). Con datos de una versión más
  nueva que la publicada, `MFF_DATOS` apunta a datos armados con el build sobre lo bajado ese día (sin `work/` en la
  carpeta de Ezequiel: se baja con `fetch_all.py --no-portraits` en el contenedor). verif_consistencia tarda más de 25
  min y su página llega a unos 5,5 GB: en un contenedor de 8 GB va sola (con otra prueba al lado, el OOM mata la página y
  la prueba queda colgada).

## Capturas del juego

Ezequiel sacó capturas de todo el juego en dos idiomas (álbumes de Google Fotos; el número de captura es el orden en el
álbum, desde 0). No volver a pedírselas:
- Español (267): https://photos.app.goo.gl/EK155akXC5fjtSV7A — transcriptas en `fuentes/juego-es/`.
- Coreano (386): https://photos.app.goo.gl/iuuBUAvSZc3qHzx96 — transcriptas en `fuentes/juego-ko/`.
- Progresión de Galactus (84, del nivel 1 con 1★ al 80 con T4): https://photos.app.goo.gl/Q5hQWtXeubx9k85EA —
  transcriptas en `fuentes/progresion/galactus.csv` (#8). La de Mephisto, en `fuentes/progresion/mephisto.csv`.
**Índice:** `fuentes/capturas/INDICE.md` (e `indice.json`) dice qué muestra cada captura de los tres álbumes y de las
380 en inglés del 4 de octubre (que no quedaron guardadas como imagen), y dónde está su transcripción; las transcripciones
literales captura por captura del álbum coreano y de las de inglés, en `fuentes/capturas/crudo/`. Leer el índice antes de
abrir imágenes. Las imágenes (737) están en el zip `capturas-mff-*.zip` de la carpeta de Ezequiel (no en el repo):
`es/NNN.jpg`, `ko/NNN.jpg`, `galactus/NNN.jpg`, con el número desde 0.
Para bajarlas: la página del álbum trae las primeras 300 (`["AF1Qip…",["https://lh3…",ancho,alto`); el resto, con el
token `AH_uQ4…` de la página, por `photos.google.com/_/PhotosUi/data/batchexecute` (rpc `snAcKc`, `[álbum, token, null,
key]`). Cada foto en tamaño original: `<url>=w<ancho>-h<alto>`.

## Estado (9 de octubre de 2026)

- Publicadas: de la 1.0.14 a la 1.0.36 (la 1.0.13 no se publicó; las notas de la 1.0.14 anuncian su Glosario). La
  1.0.26 (a65f7c4): la lista de la izquierda con la búsqueda y los filtros del roster, también en Equipos. La 1.0.27
  (3aa6beb), primera parte de #24 (la ficha): el Resumen con dónde rinde, qué le da al equipo y qué necesita arriba;
  cinco pestañas (Análisis fuera hasta #33, Progreso dentro de Armado, Más → Fuentes); las explicaciones a un «?»
  (`ayudaHtml`); strikers en una tabla con los dos sentidos.
  La 1.0.28 (4a0510f, pedido de Ezequiel sobre la 1.0.27): en Skills, cada etapa junta con su daño y sus efectos; en
  Armado, los bloques en dos columnas que se reparten la altura.
  La 1.0.29 (1f5b904, #24, Glosario e Histórico): el Glosario en dos pestañas (`ui.glTab`: los términos del juego y
  los efectos de la app), cada entrada plegada en una línea (`details.glitem`); los enlaces internos cambian de pestaña
  y abren los `details` hasta el destino. El Histórico con cada versión plegada (la primera abierta), sus notas una vez
  y una fila por personaje (`.hifila`). Sigue de #24: Modos, Tier lists, la barra de 5 secciones, avisos como estado y
  direcciones estables.
  La 1.0.30 (7281b39, #1): la app baja los datos de `datos/<formato>/`, que el build llena con
  `scripts/carpeta_formato.py`. #1 se puede cerrar.
  La 1.0.31 (15b25ec, #2): la pantalla de rescate (`/rescate`, `desktop/rescate.py`, sin app.js ni
  data.js). La página avisa el arranque (`POST /api/arranque`); el lanzador abre `/rescate` con un error o sin aviso en
  `--espera-arranque` s; desde ahí, parche, instalador, volver al programa anterior (`actualizador.volver_al_anterior`)
  y volver a bajar los datos. Prueba: `verif_rescate.py`. #1 y #2 se pueden cerrar.
- La 1.0.32 (cf45353, #32, primera tanda): las capturas del juego en español en `fuentes/juego-es/`, la tabla
  `scripts/contenido/terminos_es.json` y su validación en el build (`scripts/terminos_es.py`); el glosario, los stats de
  la guía, etiquetas de skills y efectos del catálogo con los términos del juego. #3 (notas del foro coreano) fue sin
  versión. Issues cerrados el 6 de octubre: #1, #2, #3, #24 y #32 (lo que quedó, en #41 a #45).
- La 1.0.33 (etiqueta en e7811c4, «Datos actualizados 2026-10-07»; formato 11, #32 segunda tanda, #43, #44, parte de #45): las capturas en coreano
  (`fuentes/juego-ko/`) y el resto de las de español; el vocabulario del juego en todos los textos en español (sección
  vocabulario de `terminos_es.json`, que `terminos_es.py` valida contra traducciones, contenido curado y app.js: PG,
  merma, potenciador, esquiva…; los nombres de las skills siguen siendo propios, por decisión de Ezequiel); los C.T.P. y
  los modos con su nombre del juego en español (`MFF_CTPS[].es`, `nombre_es` en modos.json); la información dudosa
  entre coreano, inglés y español en un «≠» (`scripts/contenido/dudas.json`, `scripts/dudas.py`, `MFF_DUDAS`, prueba
  `verif_dudas.py`). La primera etiqueta fue sobre el commit de la versión y publicar.yml cortó (bien): se borró y se
  puso sobre el de datos.
- La 1.0.34 (etiqueta en 816d288; formato 12, #4): el histórico con los modos de juego. `scripts/historico.py` saca de
  cada sección de las notas cuyo título nombra un modo de `modos.json` (tabla `MODOS`, expresiones sobre el título en
  inglés) un hecho «modo» con clave `modo:<id>`; las secciones de otros modos (Danger Room, Villain Siege, Legendary
  Battle…) van a `docs/HISTORICO.md`. En la app: el filtro «Personaje o modo», el tipo «Modo de juego», el nombre del
  modo lleva a Modos, y cada modo de Modos tiene su «Historial» (las 5 versiones más recientes y el botón al Histórico).
  Prueba: `verif_historico.py` (sección 7).
- La 1.0.35 (etiqueta en 4ebcc49, formato 13, #6, cerrado): la comparativa por efecto, a prueba (Ezequiel, 7 de octubre: «probemos a ver
  como queda»), según la maqueta del canvas «Rediseño MFF.ar» (artboards «Comparativa · por efecto», escritorio y celular). El número de cada efecto en los textos de
  las skills: `modelo.valores` (sin «#», ninguno; un solo «#%», ese) y los patrones sin una sola respuesta a mano en
  `catalogo.json` (`valores`); viaja en `MFF_CATALOGO.valor`. En la app, `cmpPorEfecto` (`ui.cmpVista`, por defecto
  'efecto'; la tabla de antes es «Ficha»). Prueba: `verif_cmp_efecto.py`; verif_mesa, verif_aliados y verif_consistencia
  usan la vista «Ficha» donde miran la tabla.
- La 1.0.36 (etiqueta en 02c808e, formato 14, #33 con #7): «Qué hace con sus skills». Ezequiel, 8 y 9 de octubre:
  #7 va dentro de #33; con números; medir todo (tiempo activo, daño de cada skill, PvE/PvP, rareza); en el Resumen y en
  cada skill; cortes raro ≤ 15% del roster y alto ≥ percentil 90 (con 20 o más para comparar). Lo que más vale en PvP
  (supervivencia y lo que la atraviesa) en `catalogo.json` (`pvp`), `MFF_CATALOGO.pvp`. En la app, `filasAn`,
  `analisisResumenHtml` (el bloque del Resumen) y `lecturaSkillHtml` (la línea de cada skill). «Solo en PvE/PvP»: el
  efecto tiene lectura de un modo y no del otro. Prueba: `verif_que_hace.py`. Maqueta: canvas «Rediseño MFF.ar»,
  artboards «Análisis (#33)». Sin mapear de lo que dijo Ezequiel: «penetración» y «daño que aumenta según el daño
  recibido» (no hay un efecto del catálogo que sea solo eso).
- Entregado sin versión (solo datos), 9 de octubre: la progresión de stats de Mephisto y Galactus
  (`fuentes/progresion/`, #8, en pausa hasta que Ezequiel pueda sacar capturas: lo que falta está en el issue) y 25 de
  los 35 slots de liderazgo derivados que no tenían stat (#10): stats nuevos en el catálogo (escudos de energía y físico,
  inmunidades a frío, a todo el daño, a sangrado y a fractura, resistencia a veneno) con su correspondencia en
  `liderazgos_api.json`, que ahora acepta textos sin número (stat sin valor); quedan el sangrado y la parálisis (van al
  rival) y el robo de PG (dos números).
- Entregado sin versión (solo datos, #5): `scripts/foro.py` baja también del tablero de avisos (2213: los parches de mitad
  de mes de 2020 y 2021 y algunas notas viejas); `historico.version_de_nota` asigna cada nota por la versión de su título
  o por las llegadas que nombra (thanosvibs tiene mal algunas fechas: 4.0, 5.5); los nombres se buscan sin tildes, sin
  apóstrofos curvos y, los de varias palabras, sin mirar mayúsculas. Llegadas sin su nota: de 207 a 121 (36 de la 1.0).
  Llega a la app con el workflow de datos.
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
  #22, #27, #29, #30) se cerraron el 9 de octubre (lo que puede servir está en un comentario de #34).
- Análisis (#33): la primera parte va en la 1.0.36; falta completar las lecturas de PvE y PvP del catálogo (46 y 47 de 131 efectos).
- Antes de cualquier cambio visual, la propuesta de arquitectura de la información y de navegación (#24, con los
  casos de strikers y Glosario en sus comentarios); después el rediseño visual (#6) y el tooltip de las habilidades
  (#39).
- Español del juego (#45, lo que queda): los nombres de objetos donde la app los nombra, «striker» → «pegador»,
  «Tier-N» → «categoría N» y «skill» → «habilidad» (Ezequiel no lo decidió: los nombres de las skills no importan, las
  características sí), los textos de los modos (Tier, WBL…). Las capturas: sección «Capturas del juego».
- Apartados nuevos: Cromos de cómic (#35), Espadas (#36), Jarvis (#37, falta el alcance); atributos de las skills
  (#38).
- Histórico: el texto coreano de las notas en la app (#42; las notas en `fuentes/cafe/`, el cotejo en
  `docs/NOTAS_COREANO.md`, la revisión en `docs/REVISION_COREANO.md`; desde la 1.0.33 los casos dudosos llevan «≠»),
  las llegadas que siguen sin su nota (lista en `docs/HISTORICO.md`: de 2015, notas con imágenes y parches); los modos
  que las notas nombran y `modos.json` no tiene (#46). Rediseño de la información, segunda parte (#41). Preguntas abiertas: #11 a #20 y #23. Bugs: #25, #26.
  Pruebas en el repo: #31.
