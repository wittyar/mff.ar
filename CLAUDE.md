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
- Entregas: el push desde el contenedor de Claude está bloqueado (el proxy no le da credencial porque el repo no
  está entre los autorizados de la sesión), y no se esquiva. Se commitea en un clon y se entrega un `git bundle`
  (`origin/main..main`, después de `git fetch`) en la carpeta del repo, con un nombre nuevo cada vez:
  `mff-AAAAMMDD-HHMM-<tema>-<versión>.bundle` (fecha y hora UTC). Cada entrega lleva versión, para no perder el
  rastro (Ezequiel, 16 de octubre de 2026): el último commit del bundle es el de la versión. El push y las
  etiquetas los hace Ezequiel. No se reescribe historia ya entregada. En su carpeta, solo git
  de lectura. Los pasos de cada entrega van con esta sintaxis (Ezequiel, 10 de octubre de 2026), en PowerShell:
  «1. Código» (`cd C:\Users\ezequ\dev\MFF.ar`, `git pull --ff-only`, `git pull --ff-only .\<bundle> main`, `git push`);
  «2. Build de datos» (Actions → «Actualizar datos MFF» → Run workflow sobre main, o `gh workflow run actualizar.yml` y
  `gh run watch`; termina con un commit «Datos actualizados» nuevo en main); «3. Etiqueta», cuando termina bien
  (`git pull --ff-only`, `git tag vX.Y.Z <commit>`, `git push origin vX.Y.Z`, con el commit explícito). Los tres
  pasos van siempre. Sin formato nuevo, la etiqueta va sobre el commit de la versión y no espera al de datos.
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
- Pruebas: en `pruebas/` desde el 9 de octubre de 2026 (#31); cómo correrlas y cuáles no corren solas, en
  `pruebas/LEEME.md` (`./pruebas/correr.sh`, `MFF_DATOS` para datos armados con el build). Son scripts de Playwright
  contra la app servida por `desktop/lanzador.py`, con modelos de la sinergia y del puntaje escritos aparte de `app.js`.
  Lo que escriben va a `pruebas/salida/`, que git no sigue. `verif_consistencia.py` compara, para las 888 variantes, lo
  que contesta cada pantalla a la misma pregunta; tarda más de 25 min y su página llega a unos 5,5 GB: en un contenedor
  de 8 GB va sola. Las pruebas viejas que armaban datos de prueba a mano (`armar_datos_*.py`) quedaron de antes de que
  el build corriera en el contenedor: hoy se arma una carpeta con el build sobre `work/`.

## Capturas del juego

Ezequiel sacó capturas de todo el juego en dos idiomas (álbumes de Google Fotos; el número de captura es el orden en el
álbum, desde 0). No volver a pedírselas:
- Español (267): https://photos.app.goo.gl/EK155akXC5fjtSV7A — transcriptas en `fuentes/juego-es/`.
- Coreano (386): https://photos.app.goo.gl/iuuBUAvSZc3qHzx96 — transcriptas en `fuentes/juego-ko/`.
- Progresión de Galactus (84, del nivel 1 con 1★ al 80 con T4): https://photos.app.goo.gl/Q5hQWtXeubx9k85EA —
  transcriptas en `fuentes/progresion/galactus.csv` (#8). La de Mephisto, en `fuentes/progresion/mephisto.csv`.
Desde el 14 de octubre de 2026 Claude también captura el juego en LDPlayer con el control de pantalla (desde el 16, los
clics llegan: maneja él y Ezequiel no toca el juego mientras tanto). «Universo Marvel» del juego muestra a todos los
personajes con rango, nivel, maestría, categoría y potencial elegibles, y sus pegadores. Cómo se hace, lo capturado y lo
pendiente, en el doc del proyecto de Claude «claude/mff-captura-ldplayer.md»; las imágenes de cada tanda, en
`capturas-ldplayer-AAAAMMDD.zip` de la carpeta de Ezequiel.
**Índice:** `fuentes/capturas/INDICE.md` (e `indice.json`) dice qué muestra cada captura de los tres álbumes y de las
380 en inglés del 4 de octubre (que no quedaron guardadas como imagen), y dónde está su transcripción; las transcripciones
literales captura por captura del álbum coreano y de las de inglés, en `fuentes/capturas/crudo/`. Leer el índice antes de
abrir imágenes. Las imágenes (737) están en el zip `capturas-mff-*.zip` de la carpeta de Ezequiel (no en el repo):
`es/NNN.jpg`, `ko/NNN.jpg`, `galactus/NNN.jpg`, con el número desde 0.
Para bajarlas: la página del álbum trae las primeras 300 (`["AF1Qip…",["https://lh3…",ancho,alto`); el resto, con el
token `AH_uQ4…` de la página, por `photos.google.com/_/PhotosUi/data/batchexecute` (rpc `snAcKc`, `[álbum, token, null,
key]`). Cada foto en tamaño original: `<url>=w<ancho>-h<alto>`.

## Estado (28 de octubre de 2026)

- Publicadas: de la 1.0.14 a la 1.0.40 (la 1.0.13 no se publicó; las notas de la 1.0.14 anuncian su Glosario). La
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
- La 1.0.37 (sin formato nuevo, 14; etiqueta en f878de4), 10 de octubre: los soportes que Leads &
  Supports no publica se derivan de la pasiva, la Tier-2 y la de uniforme de la API con la regla de los liderazgos
  (`liderazgos.partes_soporte`; Ezequiel: el caso fue la reducción del daño reflejado de Molecule Man): 13 derivados, 8
  sin derivar con su motivo; la correspondencia se aprende solo de los liderazgos, y lo de a mano acepta `signo` -1 y
  `requisitos` (el Tier que pide un soporte: Molecule Man, Tier-3, por la ficha del foro y Ezequiel). Los
  155 «Give Power» sin tiempo publicado van sin tiempo (`skills_api.SIN_TIEMPO`; Ezequiel: «son constantes... ponelas
  sin tiempo»): las fichas de las notas del foro nunca dicen ese tiempo (110 casos leídos). Mismo día, sin versión:
  #26 (marcadores: el mismo par en otro orden no difiere, la Tier-2 de Joaquin Torres a t2, la plantilla saca las filas
  vacías resueltas, los avisos de soportes una vez) y el build con los cambios de Leads & Supports del 10 de octubre
  (restricción "None", Annihilus por su retrato). #11 queda para el issue de los equipos de la cuenta (Ezequiel).
  Mismo día, con las fichas de skills de las notas de los dos foros (inglés y café coreano; Ezequiel: «Lo que puedas
  completar con esa información, completalo»): 41 marcadores a `marcadores.csv` (ahora con `fuente`), los códigos en
  lugar de nombres (`scripts/codigos.py`, `contenido/codigos.json`, el efecto lleva `cn`), los «Target ID»
  (`contenido/objetivos_juego.json`), el «Give Power» de Sentry — Thunderbolts* (`otorga`) y la pasiva de uniforme de
  Jewel (`contenido/skills_juego.json`, la skill lleva `j`, la app la marca «según el juego»). Lo que quedó, con lo que
  dicen las fichas, en la planilla `mff-faltantes-20261010.xlsx` de la carpeta de Ezequiel (fuera del repo).
- La 1.0.38 (formato 15; etiqueta en 85ec867, «Datos actualizados 2026-10-10»), 10 de octubre: la pasiva del artefacto exclusivo
  también en Skills (`skillArtefacto`; Ezequiel: «Ponelo en Skills, y no lo quites de armado») y el filtro del roster «Su
  artefacto da» (`filters.art`, `artefactoDa`) con las categorías del índice sobre los stats de cada artefacto
  (desde la 1.0.39, `MFF_ARTEFACTOS[].fx`: `contenido/artefactos_stats.json`, una regla por forma de línea;
  `fuentes.efectos_artefacto` para el build si una línea no tiene regla). Las categorías no cubren varios stats de artefactos (daño a villanos,
  héroes y jefes, crítico, esquiva, curación…): no se pueden filtrar todavía. Prueba: `verif_artefacto.py`.
- La 1.0.39 (formato 16; etiqueta en 5993ce2, «Datos actualizados 2026-10-13»), 11 de octubre: la vista «Por potenciador» de Comparar
  (`cmpPorPotenciador`, `ui.cmpVista` 'pot'; Ezequiel: emparejar el tipo de potenciador, de dónde sale en un tooltip, la
  suma si más de una fuente da lo mismo y al pie a quiénes les llega; decidió: tercera vista, las cuatro fuentes, la suma
  con la regla del catálogo y el pie con los personajes del roster). Las fuentes: el análisis de las skills (lo que va
  al equipo desde la Leader Skill es el liderazgo y desde una pasiva el soporte; no se suman además los de Leads &
  Supports, que son lo mismo) y el artefacto (`MFF_ARTEFACTOS[].fx` con el marcador de su número y `.a`, a quién se
  aplica). `acumula` en cada efecto del catálogo a favor: de los stats donde ya estaba y 29 nuevos con la regla de
  Ezequiel (estadísticas se suman, habilidades una vez), sin confirmar uno por uno. La ventana de aliados acepta un grupo
  sin objetivo de las skills (`ui.aliados` = { r, tg }, `verGrupo`). Prueba: `verif_cmp_pot.py`.
- La 1.0.40 (formato 17; etiqueta en 6ff97db, «Datos actualizados 2026-10-13»), 13 de octubre: **contenido propio** (Ezequiel: «me
  gustaría poder empezar a generar mi propio contenido y luego apoyarme en thanosvibs como confirmación»).
  `fuentes/propio/` (personajes, cambios, uniformes, versiones, instintos, skills por retrato con `desde` y `slots`,
  artefactos, C.T.P.s y retratos, en las formas de la API de thanosvibs, con `fuente` y `sin_confirmar`) y
  `scripts/propio.py`, que el build corre primero: lo pone sobre `work/` (lo propio manda; `_propio.tv` guarda lo de
  thanosvibs y se deshace al volver a correr) y compara con thanosvibs cuando lo publica (`work/propio.json`,
  `docs/AUDITORIA.md` sección 13). Los retratos propios, de `fuentes/propio/retratos/` (`images/propio/`). En la app, la
  marca «propio» (`pr`, `propioTag`). Primera carga: la actualización del 14 de octubre de 2026 de las notas de los dos
  foros (Agatha Harkness, Wiccan — Young Avengers, Morgan Le Fay — Classic, las Tier-4 de Wiccan y Morgan, el artefacto
  de Morgan cambiado, el C.T.P. de Ascenso sin nombre en español, Onslaught en modos.json). Prueba: `verif_propio.py`.
  Pendiente: los nombres en español de las skills nuevas y del C.T.P. (con el juego en español), los stats base y la
  progresión, el nivel 90 de Spider-Man y Ghost Rider (la app no tiene dónde mostrarlo) y la regla de Onslaught en los
  equipos (hoy solo está escrita en Modos). `verif_historico` falla en celular por la barra de arriba (no por esto).
- La 1.0.41 (formato 18; etiquetada en e8fccfc, el commit de datos), 13 de octubre, #25: el soporte va en la skill con el
  nombre que le da Leads & Supports solo si esa skill lo da (`skillDeSoporte`, `daSoporte`: Polaris — Uncanny X-Men;
  prueba `verif_soporte_skill.py`), y Alliance Battle tiene su contexto de C.T.P. (`ctp` «abx» en modos.json,
  `guia_armado.CTP_ABX` → `MFF_GUIA_ARMADO.leyenda.abx`, `ctpsAbxHtml`: Rage, y Judgement reforjado en su lugar; prueba
  `verif_ctp_abx.py`). Las combinaciones de la ficha siguen con sus C.T.P. en la ventana «Por qué y C.T.P.» (decisión del
  4 de octubre). El tercer punto de #25 (las casillas de las combinaciones) queda para #34 (Ezequiel). Fallan desde antes
  de esto, por los datos: `verif_mesa` (la cuenta de la lista), `verif_porque` 4a (el líder del caso) y `verif_contexto`.
- La 1.0.42 (sin cambio de formato; etiqueta en b1d069f), 14 de octubre: el anti-mermas del efecto
  de uniforme de Morgan le Fay. Fallen Soul: la API publica «Give Power» sin la etapa que se activa; va lo del juego
  (`skills_juego.json`, fuente `foro-1770940`). Classic: la recarga es solo de la parte que se activa
  (`liderazgos.partes_soporte`). «Qué hace» (`cuandoAn`): lo que se activa dice cuándo y su recarga, no «Siempre activo».
  Prueba: `verif_anti_mermas_morgan.py`. Pendiente: otras skills de la API que terminan en «Give Power» (unas 115 en
  `work/skills_api`, la mayoría con el efecto en la misma etapa) pueden tener el mismo hueco; sin revisar contra el juego.
- La 1.0.43 (sin cambio de formato, 18; etiqueta en 8b4a45e), 16 de octubre, #8: la progresión de
  Agatha Harkness (`fuentes/progresion/agatha.csv`: nivel 1 de 1★ a 6★ en categoría 1 y el máximo de las categorías 2
  a 4), de «Universo Marvel» con LDPlayer. El build no la lee: sin cambio visible en la app. Las habilidades de pegador:
  thanosvibs publica el Nv. 1 y las fichas del foro el Nv. 6 (Wiccan Nv. 6 en el juego da lo de la ficha; Agatha y Morgan
  sin pegador, lo de thanosvibs) [Probable]; Ezequiel: se usan las habilidades de mayor nivel, como lo propio. Stats de
  nivel 1 que faltan (wiki y capturas): 109 personajes, en `poder-faltan-stats-base-20261016.csv` de su carpeta.
- La 1.0.44 (sin cambio de formato, 18; etiqueta en a8c5b9f, el commit de versión de un bundle anterior que quedó
  fuera de main: mismo código que 6f0f7bb, solo cambian dos líneas de fecha de los datos), 16 de octubre: Agatha Harkness,
  Wiccan — Young Avengers y Morgan le Fay — Classic con el retrato de thanosvibs, que ya los publica con el fondo
  transparente de los demás (los de la ficha de la nota eran blancos; Ezequiel). Un retrato propio
  (`fuentes/propio/retratos/`) va solo mientras thanosvibs no publica el suyo; hoy no queda ninguno.
- La 1.0.45 (sin cambio de formato, 18; etiqueta en 4a9dc92), 16 de octubre, #17 (el instinto): la
  app toma el instinto de thanosvibs (`instinct`), que desde octubre de 2026 lo publica para los 291; la wiki queda en la
  auditoría (sección 3). En el juego (Universo Marvel) coincide en los 21 leídos salvo Destroyer (Destrucción, no Orden),
  que va como cambio propio (`fuentes/propio/personajes.json`, fuente `juego-universo-es`). Los 15 sin dato ya lo tienen.
  Visto de paso: el juego pone a Falcon (Sam Wilson) en el bando Superhéroe y thanosvibs en Supervillano; sin tocar.
- La 1.0.46 (sin cambio de formato, 18; la etiqueta va sobre el commit de versión), 27 de octubre: el parche del 27 de
  octubre de 2026 como contenido propio (notas foro-1897450 y cafe-3188979): los uniformes Dormammu <The Living Dark Planet>
  (`dormammu2`) y Clea <Death of Doctor Strange> (`clea1`), la Tier-4 de los dos (striker de Lv.6 en todos sus retratos), el
  artefacto de Dormammu (Lord of Chaos) y la 12.3.5 dentro de la 12.3 (`propio.py` acepta `dentro`: un parche de mitad de mes
  va como pote de su versión mayor, como en thanosvibs). Retratos propios de los dos uniformes, de las fichas sin el fondo
  blanco, hasta que thanosvibs publique los suyos. Pendiente: el nivel 90 de Dormammu (como el de Spider-Man y Ghost
  Rider, la app no tiene dónde mostrarlo) y los valores mínimo y medio del C.T.P. de Ascenso brillante (la app muestra los
  máximos, que no cambian).
- La 1.0.47 (sin cambio de formato, 18; la etiqueta va sobre el commit de versión), 27 de octubre: el daño se lee como en
  el juego, el elemento y de qué ataque sale (Ezequiel: «flame damage of energy attack» es daño de fuego que sale del
  ataque de energía; es un dato de todo el daño elemental). `traducciones/efectos.json`: «Daño de fuego: 65% del ataque de
  energía»; el tipo (físico o de energía) entre paréntesis solo si no es el del ataque. `traducciones/elementos.json`:
  «Fuego (energía)». Y el liderazgo de Dormammu — The Living Dark Planet es el de la ficha (Supervillanos, +60% a los
  Superhéroes, como Damnation), no el de la base (+24% de defensas a todos), con su marcador (id propio 991160201). La
  12.3.5 queda confirmada por los nombres de archivo de la nota coreana («V1235_…»).
- La 1.0.48 (sin cambio de formato, 18; la etiqueta va sobre el commit de versión), 27 de octubre: la ayuda (Ezequiel). Un
  botón «Ayuda» arriba, global y activado por defecto (`U.prefs.ayuda`): desactivada, se ocultan los «?» y el tooltip.
  Activada y con mouse, pasar por el nombre de una skill dice qué hace (sus efectos, a quién, la lectura) y por la
  etiqueta de un efecto, qué es (el término del glosario o su grupo) (`ayudaFlotanteHtml`, `#flotay`). El clic abre el
  «Cómo funciona», que ahora es una ventana modal centrada con fondo (en el celular, la hoja de abajo), también desde la
  comparativa en «Ficha» (nombre de la skill y cada efecto; `ui.tip` lleva la clave de la variante). El «?» se ubica con
  `ubicarFlotante`: antes se abría siempre hacia abajo y cerca del borde de abajo quedaba fuera de la pantalla (lo que
  vio Ezequiel en la comparativa). Y el roster se ordena por defecto por «Lanzamiento», lo más nuevo primero (la fecha
  del hecho «personaje» o «uniforme» del histórico; lo creado a mano va primero); una capa que ya guardó otro orden lo
  conserva. Las pruebas que buscan la base de un personaje con muchos uniformes eligen «Nombre». Pruebas:
  `verif_ayuda.py`, `verif_tooltip_skill.py` (la ventana modal) y `verif_tooltip_todas.py` (también los tooltips; una
  página por tanda: en una sola el renderer se queda sin memoria con 8 GB, también con la app de antes). Visto al
  correr todas con los datos de la 12.3.5 y sin relación con esto (fallan igual con la 1.0.47): `verif_analisis` (un
  texto sin clasificar en 24 variantes; resuelto en la 1.0.49), y fallas de entorno o de datos en cierre, contexto,
  ctp_equipos, dudas, filtros_cobertura, glosario, guia_*, historico, otorga, porque, programa y ultimo_uniforme.
- La 1.0.49 (sin cambio de formato, 18; la etiqueta va sobre el commit de versión), 28 de octubre: sin recarga (la fuente
  pone 0 s), la skill es constante y no se dice nada (Ezequiel: «Recarga: no tiene (la fuente pone 0 s)» sobra;
  `recargaTxt` da null). thanosvibs cambió la etiqueta de la descripción 433 a «Excluding bosses, ignores enemy's basic
  damage decrease» (como el juego desde el 27 de octubre): el catálogo la toma (`verif_analisis` vuelve a pasar) y la
  pasiva de Agatha va con ese texto. `historico.armar` corta el build si una variante no tiene su llegada con fecha (el
  orden por lanzamiento la necesita). Y lo que se escapó en la 1.0.48: el botón de la skill se busca al cerrar el «Cómo
  funciona» (`disparadorTip`, `tipAbierto`), el tooltip se va al salir de la ventana y al desplazar solo si el mouse ya
  no está encima, los «?» se reubican al cambiar el tamaño, y la letra del nombre de la skill en la comparativa.
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
  que las notas nombran y `modos.json` no tiene (#46). Rediseño de la información, segunda parte (#41). Preguntas abiertas: #11 a #20 y #23. Bugs: ninguno abierto (#25 y #26 cerrados).
