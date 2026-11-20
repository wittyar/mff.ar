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
- **GitHub Actions: no usar** (Ezequiel, 20 de noviembre de 2026), literal:
  > ## GitHub Actions: no usar
  > - No crees, edites ni actives workflows de GitHub Actions (`.github/workflows/*`): ni jobs nuevos, ni triggers
  >   (`push`, `pull_request`, `schedule`, `workflow_dispatch`), ni matrices.
  > - No dispares workflows: nada de «Run workflow», `gh workflow run`, re-runs ni llamadas de dispatch por API.
  > - No uses el CI de GitHub para validar. Corré tests, lint, typecheck y build dentro de la sesión y reportá el resultado.
  > - No hagas push "para ver si pasa CI". Juntá los cambios en pocos commits y pocos pushes.
  > - Si una tarea parece necesitar Actions (cron, deploy, respaldo, chequeos programados), PARÁ y proponé una alternativa
  >   sin Actions, con trade-offs […]. La decisión es mía.
  > - Si encontrás workflows que se disparan solos, no los borres ni los edites: listalos (archivo, nombre, triggers) y avisame.

  Claude no toca `.github/`. **Siguen activos** (20 de noviembre de 2026) los dos workflows de antes:
  `.github/workflows/actualizar.yml` («Actualizar datos MFF»: `schedule` lunes 06:00 UTC y `workflow_dispatch`; commitea
  datos como mff-bot en main) y `.github/workflows/publicar.yml` («Publicar versión»: `push` de etiquetas `v*`). Mientras
  sigan activos, `actualizar.yml` sigue corriendo solo cada lunes, y **crear la release crea la etiqueta `vX.Y.Z` y
  dispara `publicar.yml`** [Probable: una etiqueta creada con la credencial de Ezequiel dispara `push`], que arma todo de
  nuevo en Windows (gasta minutos) y corta al crear una release que ya existe [Probable]. Qué hacer con
  ellos lo decide Ezequiel: desactivarlos (en GitHub, Actions → cada workflow → «Disable workflow», o Settings → Actions →
  General → «Disable actions») o borrarlos él del repo.
- Entregas: el push desde el contenedor de Claude está bloqueado (el proxy no le da credencial porque el repo no
  está entre los autorizados de la sesión), y no se esquiva; tampoco hay credencial para crear releases. Se commitea en
  un clon y se entrega un `git bundle` (`origin/main..main`, después de `git fetch`) en la carpeta del repo, con un nombre
  nuevo cada vez: `mff-AAAAMMDD-HHMM-<tema>-<versión>.bundle` (fecha y hora UTC). Cada entrega lleva versión, para no
  perder el rastro (Ezequiel, 16 de octubre de 2026): el último commit del bundle es el de la versión. Con el bundle van
  los cuatro archivos de la release que Claude arma en la sesión (`python3 desktop/construir.py release vX.Y.Z`, ver
  «Release»), para `dist\` de la carpeta del repo (git no la sigue): `TA-GUIANAEL-MFF-X.Y.Z.exe`, `mff-parche-X.Y.Z.zip`,
  `latest.json` y `notas.md`, y el commit sobre el que se armó. Los archivos de `dist/` no se commitean. El push, los datos
  y la release los hace Ezequiel. No se reescribe historia ya entregada. En su carpeta, solo git de lectura. Los pasos de
  cada entrega van con esta sintaxis (Ezequiel, 10 de octubre de 2026), en PowerShell:
  «1. Código» (`cd C:\Users\ezequ\dev\MFF.ar`, `git pull --ff-only`, `git pull --ff-only .\<bundle> main`, `git push`);
  «2. Datos» (`python scripts\actualizar_datos.py`, o doble clic en `ActualizarDatos.bat`; termina con «Listo: «Datos
  actualizados AAAA-MM-DD» empujado a origin/main.» o «Sin cambios»); «3. Release» (los cuatro archivos en `dist\`,
  `python desktop\construir.py subir vX.Y.Z <commit>`, con el commit que dio Claude: verifica y crea la release con `gh`,
  con la etiqueta sobre ese commit; ya no hay `git tag`). Los tres pasos van siempre. Sin formato nuevo, van en ese orden
  en una sola entrega: la release se arma sobre el commit de la versión y no espera al de datos. Con formato nuevo, ver
  «Versiones».
- Datos: los arma y los publica `scripts/actualizar_datos.py` en la PC de Ezequiel (Windows), con la secuencia del
  workflow `actualizar.yml`: `fetch_all.py --no-portraits`, `parse_instinto.py`, `foro.py`, `cafe.py` y `build.py`, el
  `git add` de las mismas rutas y, si hay cambios, commit «Datos actualizados AAAA-MM-DD» (fecha UTC) con su identidad
  git y `git push`. Antes exige la rama main sin cambios en archivos seguidos ni archivos sin seguir en esas rutas (irían
  al commit), que siga a origin/main y que quede igual después de `git pull --ff-only`; los archivos sin seguir de otras
  partes (el bundle de la entrega en la raíz, por ejemplo) no lo frenan: los lista en un aviso y no los toca. Corta con
  el motivo ante el primer error, sin commitear, y también si el build toca algo fuera de esas rutas; para volver atrás
  dice el comando (`git reset --hard HEAD` y `git clean -fd` solo sobre esas rutas). Lo que muestra queda también en `work\actualizar_datos.log`. Necesita Python 3.12 o más (de
  python.org, con el lanzador `py`; los scripts usan solo la biblioteca estándar), Git para Windows con la credencial
  para empujar a GitHub y red; los scripts corren en modo UTF-8 (`PYTHONUTF8=1`, que pone el script: sin él se caen en
  cp1252). **Deuda**: los pasos y las rutas están copiados de `actualizar.yml`, que no se toca; si cambia uno, se cambia
  el otro, hasta que Ezequiel decida qué hacer con el workflow. El build no es determinista entre corridas (el orden de
  algunas listas depende de `PYTHONHASHSEED`): cada corrida cambia `data.js` aunque las fuentes no cambien, y hay commit.
  Semanal (no registrada; la crea Ezequiel si quiere), en PowerShell, los lunes a las 3:00 de Buenos Aires (las 6:00 UTC
  del workflow):
  ```
  $accion = New-ScheduledTaskAction -Execute (Get-Command py).Source -Argument '-3 scripts\actualizar_datos.py' -WorkingDirectory 'C:\Users\ezequ\dev\MFF.ar'
  $cuando = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 3:00
  Register-ScheduledTask -TaskName 'MFF actualizar datos' -Action $accion -Trigger $cuando -Settings (New-ScheduledTaskSettingsSet -StartWhenAvailable)
  ```
  No probado en Windows. Trade-offs: corre solo con la PC prendida y la sesión de Ezequiel iniciada (así se registra; con
  `StartWhenAvailable`, si a esa hora estaba apagada, corre apenas se pueda); abre una ventana de consola mientras dura;
  el push usa la credencial guardada de Git para Windows (Git Credential Manager), que anda en su sesión: «correr aunque
  el usuario no haya iniciado sesión» pide su contraseña de Windows y puede dejar a git sin credencial; si sus commits van
  firmados con una clave con frase, la tarea se queda esperándola. Si la carpeta tiene cambios sin commitear, corta y no
  toca nada. Una falla se ve en la ventana, en `work\actualizar_datos.log` y en el Programador de tareas (último
  resultado 0x1). Si la tarea commitea entre que Claude arma un bundle y Ezequiel lo aplica, `git pull --ff-only
  .\<bundle> main` no puede avanzar (main y el bundle se separaron) y hace falta otro bundle sobre el main nuevo.
  Quitarla: `Unregister-ScheduledTask -TaskName 'MFF actualizar datos'`.
- Release: `python3 desktop/construir.py release vX.Y.Z` en la sesión de Claude (Linux) hace lo que hacía
  `publicar.yml`: la etiqueta coincide con `version.json`; los datos del commit (`datos.json`) y los de
  `datos/<formato>/` son del formato que pide; el programa y el parche (con el Python embebido de python.org, verificado);
  Inno Setup 6.7.3 de su release oficial, verificado por sha256 antes de ejecutarlo, en el prefijo de Wine
  `/tmp/wine64pfx`, y el instalador compilado con ISCC bajo Wine; `latest.json` y `notas.md`. Se arma sobre la punta de
  main, sin cambios y con origin/main adentro (después de `git fetch`): es lo que Ezequiel empuja antes de subirla, así
  que los datos publicados de su formato van a ser los de ese commit. Al final imprime el sha256 y el tamaño de cada
  archivo y el comando de «3. Release». En el contenedor hace falta Wine con soporte de 32 bits (el instalador de Inno
  Setup lo es) y una pantalla virtual: `dpkg --add-architecture i386`, `apt-get update`, `apt-get install wine64
  wine32:i386 xvfb` (Wine 9.0 de Ubuntu 24.04). Wine se corre sin `TMPDIR` (Wine 9.0 se cae al arrancar con ella). Frente a
  lo que armaba Actions en Windows (comparado con la v1.0.57 publicada el 20 de noviembre de 2026): los mismos 51
  archivos instalados y el mismo `latest.json` salvo sha256 y tamaños; los archivos de texto del programa van con LF
  (Actions, con el git de Windows, los ponía con CRLF; mismo contenido), y el `.exe` (y su desinstalador) guarda además
  los íconos por defecto de Inno Setup (el `UpdateResource` de Wine no los borra; unos 86 KB más): el que se ve es el
  mismo, el nuestro. `latest.json` no depende del commit: depende del instalador, del parche y de `version.json`; la
  etiqueta la pone `subir` sobre el commit que se le da, que tiene que estar en origin/main.
- Versiones: `version.json` (versión, notas para el usuario, formato de datos). El formato sube
  cuando la app nueva necesita algo que los datos viejos no traen (`FORMATO` en `scripts/build.py`,
  con la historia de cada uno). Los datos publicados salen de main. Con un formato nuevo, la release tiene que armarse
  sobre un commit «Datos actualizados» de ese formato que ya esté en main, así que la entrega va en dos vueltas:
  «1. Código» (el push de main, con el commit de la versión) y «2. Datos» (`actualizar_datos.py` commitea y empuja los
  datos del formato nuevo, en `datos/<formato>/`); recién entonces Claude, con `git fetch`, arma la release sobre ese
  commit de datos y Ezequiel corre «3. Release» con lo que le deja: así la release ya sale con los datos que pide (con la
  1.0.17, la etiqueta salió antes y la app quedó esperando). `construir.py release` corta si los datos del commit o los
  de `datos/<formato>/` no son del formato de `version.json`. Sin formato nuevo, la release va sobre el commit de la
  versión. Una versión por vez: con un formato nuevo, los datos y la release de esa versión van antes de entregar o
  empujar la siguiente (con la 1.0.22, dos bundles empujados juntos dejaron la etiqueta sobre datos de otro formato).
  Desde la 1.0.30 (#1) la app baja los datos de `datos/<formato>/` (los copia ahí
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

## Estado (20 de noviembre de 2026)

- Publicadas: de la 1.0.14 a la 1.0.40 (la 1.0.13 no se publicó; las notas de la 1.0.14 anuncian su Glosario; tampoco la
  1.0.56: las notas de la 1.0.57 anuncian sus Objetos). La
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
- La 1.0.50 (sin cambio de formato, 18; la etiqueta va sobre el commit de versión), 28 de octubre: comparar desde la
  ficha pone primero las versiones de ese personaje (Ezequiel: «cuando estoy en Dormammu, para comparar prefiero no
  tener que buscarlo»): `ui.pickDe`, `pickPrimero` en `rosterData`, con aviso arriba de la lista; no filtra, y sin otras
  versiones la lista queda igual. Prueba: `verif_comparar_ficha.py`.
- La 1.0.51 (sin cambio de formato, 18; la etiqueta va sobre el commit de versión), 2 de noviembre: revisión del código.
  Fuera lo que no se usaba (tres funciones y tres textos de app.js, imports de scripts que pyflakes marca), Dormammu
  <The Living Dark Planet> y Clea <Death of Doctor Strange> con el retrato de thanosvibs (ya los publica; salen de
  `fuentes/propio/retratos/`), y pruebas al día: `verif_consistencia` (una skill constante no dice recarga en ningún
  lado) y las de la guía de armado (leen la versión y la fecha de la copia en uso). Corridas todas con los datos del 2
  de noviembre: fallan lo mismo que con la 1.0.47 (datos o entorno: cierre, contexto, ctp_equipos, dudas,
  filtros_cobertura, glosario, guia_ficha y guia_ajustes (el bloque de Cynicalex ya no está en el Resumen), historico
  en celular, marcadores (la tabla vacía de A0), mesa, otorga, porque, programa, ultimo_uniforme, y guia_aceptar 15: la
  guía tiene 290 de 291 personajes), más formato e imagenes, por la carpeta de datos armada a mano. La investigación de
  cómo calcula el juego el daño (lo que se sabe, lo que no y cómo medirlo en LDPlayer), en el doc del proyecto de
  Claude «claude/mff-modelo-combate.md».
- La 1.0.52 (sin cambio de formato, 18; la etiqueta va sobre el commit de versión), 12 de noviembre, **a prueba**: pedido
  de Ezequiel («decime cómo podemos mejorar la interfaz... una mejor visual de las habilidades... formas de comparar en
  un mismo personaje entre uniformes... que me proponga metodologías de comparación... Valida la lógica de navegación
  de toda la aplicación, es necesario que tenga sentido cada botón y su funcionalidad... Separa el armado de mi propia
  cuenta de lo demás del juego»). Es parte de #41 (la barra con «Mi cuenta»); de #41 quedan agrupar Tier lists,
  Glosario e Histórico en «Referencia» (no se hizo: suma un clic), los avisos como estado y las direcciones estables.
  - **Mi cuenta aparte.** La barra en dos grupos (`renderNav`: `VISTAS_ROSTER`, `VISTAS_CUENTA`): el juego y, con su
    color (`--cuenta`), «Mi cuenta» y «Mesa». La mesa se ve solo abierta (`U.prefs.mesa`, `mesaVisible()`) o en Mi
    cuenta › Equipos; cerrada no hay «Poner en la mesa» ni «+» en la lista (`.trabajo.sin-mesa`). La bandeja de comparar
    va aparte (`bandejaVisible()`, `bandejaHtml()`), en el roster y en la ficha; elegir para comparar (`ui.pickMode`) se
    apaga al pasar a otra sección (en `render`), y lo elegido queda. Vista `cuenta` (`ui.cuentaTab`, `CUENTA_TABS`; Equipos y el editor
    son vistas propias con la misma sub-barra, `cuentaCabHtml`): resumen, progreso, personajes propios, atributos
    marcados y Mi capa (exportar, importar y borrar salieron de Ajustes). «Mi cuenta» de la barra abre siempre el
    resumen. La ficha tiene la pestaña `cuenta` (`fichaCuenta`): tus equipos y «cómo entraría» (`equiposTuyosHtml`,
    antes en Equipos), tu progreso (antes en Armado), atributos marcados y tus cambios, con «Marcar atributos» y
    «Editar» (que salieron de la cabecera de la ficha). El «Por qué» de «cómo entraría» (`t|…`) es vigente en esa pestaña.
  - **Skills: el kit de un vistazo** (`kitDe`, `difSkill`, `kitVistazoHtml`): una fila por skill con su daño, su parte
    del total, cada cuánto y sus efectos por destino, con «Comparar con» otra versión (`ui.kitCon`: suma, cambia, pierde).
    La etiqueta de cada efecto del detalle lleva el color de su destino.
  - **Comparativa: «Cómo compararlos»** (`metodosCmp`, `cmpMetodosHtml`): `ui.cmpVista` es el método (kit, efecto, pot,
    pvp, listas, ficha; null = el sugerido, que se fija al pintar); `goCompare` lo vuelve a null. Nuevos: skill por skill
    (`cmpPorKit`, con referencia `ui.cmpRef` y «Solo lo que cambia» entre versiones de un mismo personaje), en las listas
    (`cmpEnListas`, con el rol de `rolEn`) y para PvP (`pesaEnPvp`). «Comparar sus versiones» en la ficha
    (`cmpVersiones`) y el desplegable de versión en cada columna (`cmpCabHtml`, `cmpVersion`).
  - **Tier lists de lectura** hasta «Editar listas» (`ui.tlEditar`): sin editar, una entrada abre su ficha.
  - **Arreglos** encontrados al revisar: la ficha de un personaje creado a mano no abría desde #33 (`analisisDe`: sin
    retrato, análisis vacío); «MAYOR» de la comparativa trataba lo de una pasiva sin condición como «sin duración»;
    «Ult 0%» sin dato de carga (`cargas` da null); la tabla de topes se salía en el celular (`.stagewrap` sin regla); y la
    traducción del efecto del striker de Dormammu.
  - Pruebas nuevas: `verif_cuenta.py`, `verif_kit.py`, `verif_cmp_metodos.py`, `verif_tl_editar.py`. En el arnés,
    `ir_a_equipos(pg)` y `abrir_mesa(pg)`. `verif_filas.py` y `verif_export_viejo.py` corren una app vieja y quedan como
    estaban. Corridas todas (85) con los datos del 2 de noviembre: 54 sin fallas; las demás fallan lo mismo que con la
    1.0.51 (datos o entorno: cierre, contexto, ctp_equipos, dudas, filtros_cobertura, formato, glosario, guia_aceptar,
    guia_ajustes, guia_ficha, historico en celular, marcadores, otorga, porque, programa, ultimo_uniforme, y las que
    piden otro armado: actualizacion_real, export_viejo, filas, parche_1xx, wine). `verif_mesa` vuelve a pasar (tenía
    escrito «de 888»). `verif_tooltip_todas` recorre también los efectos del kit: 77.138 tooltips por idioma, sin errores.
  - Visto y sin tocar (a decidir): entre el roster y la comparativa, «Comparando» sigue encendido después de abrir la
    comparación (de vuelta en el roster, tocar una tarjeta la elige en vez de abrirla hasta apagarlo); la activación «al
    tener menos de un {0}% de PG» sale así de la fuente; «Refleja daño» de Dormammu (Activa 4) figura como «para el
    equipo» en el análisis; y el tiempo activo de «Qué hace» sigue dividiendo por la recarga base (ver el doc del modelo).
  - El relevamiento de tier lists y opiniones de otras comunidades (inglés, coreano, chino, japonés y más: qué hay, con
    qué criterios comparan y qué dicen de cómo funciona el juego, con lo que choca con nuestro modelo), en el doc del
    proyecto de Claude «claude/mff-tier-lists.md». Lo más útil: la planilla coreana «정보 공유», que se puede leer por
    programa (prioridad de C.T.P. y de artefacto por personaje, corredores de Alliance Battle).
- La 1.0.53 (formato 19; la etiqueta va sobre el commit de datos), 17 de noviembre de 2026:
  - **La actualización War of Kings (12.4) como contenido propio** (notas foro-1897819 y cafe-3190031, que se suman a
    `fuentes/foro` y `fuentes/cafe`): Vulcan <War of Kings> (nativo de Tier-3), Lilandra <Majestrix Lilandra> (nativa de
    Tier-2) y Deathbird <Uncanny X-Men>, personajes nuevos con sus fichas, la definitiva de Tier-3, el striker de Tier-4 (Lv.6)
    y sus artefactos (Lv.4). La ficha de Deathbird no llegó con las imágenes pegadas, pero está en la nota del foro: va
    completa (sin confirmar, como los otros dos, retrato, id, origen, habilidad de jefe mundial, striker y resistencias; y su
    categoría nativa, Tier-1). La 12.4 («War of Kings»; el número, sin confirmar) entra como versión. Sin retrato: un propio
    que thanosvibs no publica va sin imagen («SIN RETRATO»; antes pedía una de thanosvibs que daba 404). En notas de lo
    propio: el requisito de Vulcan («False Emperor»), el nivel 90 de Hulk y Vulcan y los stats básicos máximos de Lilandra
    (2848/1893/1802/6951; ni la app ni la fila de la API tienen dónde). El sangrado de Lilandra que también baja el índice de
    recuperación va como un solo efecto (la API no tiene uno para bajarle la recuperación al rival). Vulcan: su liderazgo
    tiene dos partes (aliados al estar mermados; él) y no se deriva (docs/AUDITORIA.md lo lista).
  - **Cromos de cómic** (#35; Ezequiel: «Arma un modulo sobre cromos donde pongas todos los cromos con sus caractaristicas y
    en lo que respecta la cuenta personal poder anotar los cromos que tengo en sus dos sets»). `fetch_all.py` baja
    `/api/cards` (112) y sus imágenes; `scripts/cromos.py` arma `MFF_CROMOS` (fijas, cinco opciones por grado, activaciones,
    tipos, colecciones) con `scripts/contenido/cromos.json` (cómo se lee cada texto; lo que no está corta el build). «Rare?»
    va como Raro marcado dudoso. Los cinco de War of Kings, propios (`fuentes/propio/cromos.json`, por nombre), con los
    valores de la nota a la máxima calidad y grado (solo ellos tienen valores), la colección (los 5 en Mítico, +3% de índice
    de recuperación) y que el #1 no acumula su activación de ataque de energía. La sección «Cromos» (en el grupo del juego):
    «Da este stat» (fijo, posible o cualquiera), tipo, activación y búsqueda; cada cromo dice en qué mazo tuyo está. Mi
    cuenta › Cromos: los dos mazos («Mazo de cromos» en el juego) de 5 lugares (`U.cromos.mazos`, {id, op}; la capa los
    valida al cargar e importar), la opción de cada grado y qué cubre cada mazo, sin sumar porcentajes. Un cromo va una vez
    por mazo: la guía del juego en inglés (captura 57: «Only one of a card type can be equipped at a time») y en coreano.
    Arreglo de paso: importar otra vez el mismo archivo después de que no entró.
  - Pendiente: el cromo Premium Fantastic Four (1961) #49 (la nota lo nombra sin opciones); el tipo de los War of Kings #3 a
    #6; «CROWD CONTROL TIME» de los cromos nuevos y «DEBUFF DURATION» de los de thanosvibs son probablemente el mismo stat
    (van aparte); los valores de los demás cromos; cómo pesan los cromos en los equipos (#34). Los cinco cromos y los tres
    personajes, hasta que thanosvibs los publique (la auditoría compara).
  - Pruebas nuevas: `verif_cromos.py`, `verif_cuenta_cromos.py`; `verif_propio` con los tres personajes; `verif_cuenta` con
    la pestaña y la barra nuevas; `verif_historico` espera el desplazamiento suave (con la 12.4, el modo más reciente es Epic
    Quests). Corridas con los datos armados el 17 de noviembre (formato 19): sin fallas propio, cuenta, cuenta_cromos,
    cromos, analisis, atras, capa, datos, ficha, kit, artefacto, cmp_pot, que_hace, modos_juego, mesa, ayuda, humo y
    tooltip_todas (77.416 tooltips, sin errores). Fallan igual que sin estos cambios (la 1.0.52 con sus datos del mismo
    `work/`): historico en celular, tooltip_skill (Angela — Asgard's Assassin, «abrir no mueve la página») y dudas; glosario
    falla a veces por un 409 de la bajada de imágenes (los íconos de artefacto que thanosvibs no publica). formato e imagenes
    piden los datos del repo, que siguen en el formato 18 hasta correr el workflow.
- La 1.0.54 (sin cambio de formato, 19; la etiqueta va sobre el commit de versión), 17 de noviembre de 2026: **el recorrido
  guiado** (Ezequiel: «Ok, ahora empiezo a necesitar una opcion para poder enseñar a utilizar la aplicacion... Es decir, la
  primera vez que lo abris y, si presionas el boton, te aparece un tutorial de cada area de la aplicacion explicando que
  cosas ver y como verlas.»). Hasta ahora la usaba solo él: es para mostrársela a alguien que no la conoce.
  - **El botón.** «Recorrido», en la barra junto a «Ayuda», arranca el tramo del área en la que se está, con lo que se tiene
    abierto (el personaje de la ficha, los comparados); «Otras áreas» ofrece cada una y el recorrido completo, que navega
    solo de un área a otra (fuera de su área, la ficha de Thor y la comparación de Hulk y Wolverine: `RECORRIDO_EJEMPLO`).
    Ajustes cuenta como la barra; Equipos y el editor, como Mi cuenta.
  - **Los pasos.** Una sola tabla, `RECORRIDO`: once tramos y 49 pasos (barra 6, Roster 5, Ficha 9, Comparativa 3, Tier
    lists 3, Modos 3, Cromos 3, Glosario 3, Histórico 3, Mi cuenta 8, Mesa 3), cada uno con el selector de lo que señala
    (`data-rec` donde no había una clase estable), la clave de sus textos (`rc_<área>_<paso>_t` y `_x`, es y en) y la
    pantalla que pide (`ui`). Cada paso resalta su elemento (`#rc-luz`) con la tarjeta al lado (`ubicarFlotante`; en el
    celular, la hoja de abajo, y la página deja lugar abajo para subir lo que está al final): título, qué mirar y cómo
    llegar, «Paso n de m», Anterior, Siguiente, ← y →, Esc y tocar afuera para salir (como el «Cómo funciona»); el foco
    queda en la tarjeta (`atraparFoco` recibe la ventana) y vuelve a «Recorrido» al salir. Si el elemento de un paso no está
    en la pantalla (el roster sin resultados), la tarjeta lo dice, al centro y sin resaltar, y se sigue.
  - **No toca nada tuyo.** Lo que abre es estado de pantalla (`ui`): cada paso parte de cómo estaba la pantalla al empezar
    (`restaurarUi`) y al salir vuelve a eso, a la misma altura; no guarda la capa, ni la mesa, ni la bandeja de comparar.
    Mientras está abierto no se anota el historial (`anotarLugar`, `sincronizarLugar`): «Atrás» del navegador lo cierra y va
    al lugar anterior, como siempre. El fondo tapa la página: el tooltip de la ayuda no se abre debajo, y con el «Cómo
    funciona» abierto no se llega al botón (tocar afuera solo lo cierra). Cambiar de idioma no es parte del recorrido.
  - **La primera vez.** Sin capa guardada (`/api/capa` sin archivo) sale una bienvenida: «Empezar el recorrido» (el
    completo) o «Ahora no» (también Esc o tocar afuera); las dos guardan la capa, y con capa no vuelve a salir. Una capa ya
    guardada (la de Ezequiel) no la ve al actualizar, sin marca nueva ni compatibilidad. No sale en la pantalla de datos ni
    en la de error (ahí no se pinta la app). Las pruebas arrancan con una capa vacía guardada (`carpeta_datos()`;
    `primer_uso=True` es sin capa) y las que arman su carpeta también (verif_datos, verif_imagenes, verif_paginador,
    verif_servidor_caido).
  - **Arreglos de paso**, que encontró el recorrido en el celular: tres cosas desbordaban el ancho de la página (las
    casillas de cobertura de las combinaciones, la activación larga de una skill y el selector del Histórico) y, con eso, el
    navegador agrandaba la página y la hoja de abajo (del recorrido y del «Cómo funciona») quedaba fuera de la vista.
  - Pruebas: `verif_recorrido.py` (primer uso, capa existente, el botón en cada área, el completo en escritorio y celular
    con cada paso a la vista, volver como estaba, teclas, un paso sin su elemento, «Atrás», convivencia, inglés). Corridas
    con los datos armados el 17 de noviembre: sin fallas recorrido, humo, ayuda, atras, capa, cuenta, cromos, cuenta_cromos,
    ficha, mesa, datos, historico (vuelve a pasar en celular), modal, cmp_metodos y servidor_caido. Fallan igual que sin
    estos cambios: tooltip_skill (Angela, «abrir no mueve la página») y kit (Cyclops, Definitiva: «63%» contra 62 del
    modelo, con estos datos). paginador falló 1 de 3 veces por un 409 de la bajada de imágenes ya en curso (el de glosario:
    la segunda página la pide mientras sigue la de la primera); sin estos cambios pasó las 5 veces que se corrió.
  - Pendiente / a decidir: los textos de los pasos los corrige Ezequiel (están en `T`, `rc_*`). En el celular, un elemento
    más alto que el lugar sobre la hoja (el primer bloque del Resumen) queda con su comienzo a la vista y el resto debajo
    de la hoja. Otra cosa que desborde el ancho en el celular vuelve a sacar la hoja de la vista (se encontraron tres; no se
    revisaron todas las variantes). Los personajes de ejemplo se nombran en `RECORRIDO_EJEMPLO`: si faltan en los datos, el
    recorrido de otra área corta con un error.
- La 1.0.55 (sin cambio de formato, 19; la etiqueta va sobre el commit de versión), 18 de noviembre de 2026: **retratos
  temporales** de Vulcan, Lilandra y Deathbird (Ezequiel: «Podes poner lso retratos temporales? Mientras esperamos lso de
  Thanso Vibs?»; thanosvibs sigue sin publicarlos). `fuentes/propio/retratos/{vulcan,lilandra,deathbird}.png`: la celda
  «Hero Image» de la ficha de cada uno en la nota foro-1897819 (155 px, la más grande de la nota; la ruta sin «thumbnail»
  da 403), agrandada a 256x256 y con el fondo blanco transparente (relleno desde los bordes, los huecos encerrados
  elegidos a mano, alfa del borde por mezcla con el blanco y color descontaminado). Más blandos que los de thanosvibs
  por el agrandamiento. Sin código nuevo: el mecanismo de la 1.0.40 (`_core.retrato`, `propio.py`, `imagenes.origen`).
  Son temporales: cuando thanosvibs publique los suyos, se sacan de `fuentes/propio/retratos/` (a mano, como en la 1.0.44
  y la 1.0.51: mientras el archivo esté, manda el propio). Llegan a la app con el workflow de datos. Pruebas:
  `verif_propio` (los tres con su retrato, que carga sin 404) y `verif_imagenes` (los retratos propios desde el origen
  falso, no desde GitHub). Corridas con los datos armados el 18 de noviembre: sin fallas propio, imagenes, humo, ficha,
  recorrido y ayuda. Pendiente: los íconos de los tres artefactos (la nota los trae, pero lo propio no tiene dónde
  ponerlos: haría falta código, como `images/propio/` para los retratos).
- La 1.0.56 (formato 20; **no se publicó**: su workflow de datos falló el 19 de noviembre y no tiene etiqueta; sale con la
  1.0.57, que la lleva en sus notas), 18 de noviembre de 2026: **Objetos** (Ezequiel: «Por otro
  lado, ademas de la parte de cormos... Arma un modulo para * CTPs, donde este el detalle. * Bendiciones de Odin * Javis *
  Emblemas * Sets de Iso e ISOs»). Como Cromos: una sección de consulta por sistema, con todo el detalle que dan las fuentes.
  - **La entrada.** «Objetos» reemplaza a «Cromos» en el grupo del juego (decisión de quien coordinó: cinco entradas más no
    entran). El nombre es el del glosario de objetos del juego en español (capturas 116 a 162), el único que nombra a todos
    (ISO-8, cromos, equipo personalizado, uru encantado, datos de emblema y de JARVIS); «Crecimiento de equipo», la sección de
    la guía, no tiene los emblemas y «equipo» ya es otra cosa en la app. Sub-pestañas, con la sub-barra de Mi cuenta
    (`subBarraHtml`, ahora de las dos; la de Objetos con el color del juego): C.T.P., ISO-8, Bendiciones de Odín, Emblemas,
    J.A.R.V.I.S. y Cromos (la vista de la 1.0.53, adentro tal cual; Mi cuenta › Cromos no cambia). `ui.objTab` va en el
    historial (`fotoLugar`/`popstate`); cada elemento es un `details.glitem.objitem` (las entradas del Glosario) y lo abierto
    sigue abierto al repintar.
  - **Las fuentes.** C.T.P.: `/api/ctps`, lo que ya se bajaba y el build tiraba (`MFF_CTPS[].op`: opción bloqueada y las dos de
    reforja con los valores de normal, poderoso y brillante; `.obt`: de dónde se consigue cada grado), traducido por patrón
    con el vocabulario de las fichas del juego (`traducciones/ctp_opciones.json`; los patrones que ya tenían los artefactos
    valen los de ellos: un texto, una traducción, y si no el build corta). Bendiciones de Odín: `/api/odins-blessings` (17,
    con valor, bono de amplificación y total por stat, como su página; color, forma, de dónde caen). Emblemas: `/api/emblems`
    (63), `/api/emblems/static` (el modo de cada colección, cómo se consiguen: así los lee su página) y `/api/emblems/levels`
    (estrellas y costo de cada nivel); los íconos, de `/_game-assets/ui_item/` (`images/emblemas/`). Sets de ISO-8: la tabla
    «ISO SET BONUS» de la página ISO-8 de la wiki (`work/wiki_iso.json`; thanosvibs no tiene API de ISO-8), 26 sets; las
    piedras, las de `guia.json`; los sets de la guía y de la leyenda de la guía de armado tienen que estar en la wiki y cerrar.
    J.A.R.V.I.S. (#37: el alcance de esta versión es de consulta): `fuentes/objetos/jarvis.json`, de la nota del 2 de
    septiembre de 2026 que lo introdujo (foro-1895951; la lista de los 27 chips es una imagen de la nota, transcripta tal
    cual), la del 14 de octubre (foro-1896956) y la guía del juego. `scripts/objetos.py` arma `MFF_OBJETOS` con
    `scripts/contenido/objetos.json` (cómo se lee cada texto; lo que no está corta el build) y las notas de cada sistema con su
    fuente. El nombre en español de seis piedras y de Fuerza del Hulk cabreado, de las capturas 246 y 247.
  - **Lo dudoso.** «Advanced» de thanosvibs va como «De lujo» marcado dudoso (la guía del juego dice «Luxury», y en español
    «de lujo», en ese lugar de la lista). Healing Factor: la wiki escribe «Crowd Control Time ↑», y «↓» en los demás. Los
    valores de los sets son los de la wiki, que no dice a qué rango ni despertar corresponden (la página lo dice). El C.T.P. de
    Ascenso sigue propio, ahora marcado y sin ícono (thanosvibs no lo publica: pedía uno que daba 404).
  - **Enlaces.** El nombre de un C.T.P. (`ctpDetalle`, `ctpCorto`, `ctpFilaIdeal`: la ficha, Modos, Alliance Battle, las
    tarjetas de equipo) y el de un set de ISO-8 (la ficha › Armado, Modos › Armado) llevan a su detalle (`verObj`), con
    «Atrás». Los de los emblemas y J.A.R.V.I.S. a sus modos (`modoLink`, también el del histórico). Todos son `button.objlink`.
  - **Recorrido.** El tramo «Objetos» reemplaza al de Cromos: un paso por pestaña y los tres de Cromos (55 pasos en 11 tramos).
  - Pendiente: los valores de los chips de J.A.R.V.I.S. (ninguna fuente los da: harían falta capturas del juego, chip por
    chip) y sus nombres en español; los nombres en español de las bendiciones, de los sets de ISO-8 (salvo uno) y de las
    piedras Vital y Nimble; qué piedra es de qué color en el juego (los colores son los de la guía); a qué rango o despertar
    corresponden los valores de la wiki; las recompensas de las colecciones de emblemas (`/api/emblems/collections`, sin
    bajar); los nombres por grado de los C.T.P. en inglés. Fuera de alcance, por pedido: anotar en Mi cuenta lo que uno tiene
    de cada sistema, cómo pesan en los equipos (#34) y las espadas (#36).
  - Pruebas: `verif_objetos.py` (nueva: las seis pestañas, todos los de cada fuente, filtros, detalle, valores, lo dudoso y
    lo propio, los enlaces con «Atrás», el historial, inglés y celular); `verif_cromos` y `verif_cuenta_cromos` entran por
    Objetos; `verif_cuenta` y `verif_recorrido`, con la barra y el tramo nuevos; `verif_imagenes`, los íconos de los emblemas.
    Corridas con los datos armados el 18 de noviembre (formato 20): sin fallas objetos, cromos, cuenta_cromos, cuenta,
    recorrido, atras, humo, ayuda, propio, ctp_abx, ficha, modos_juego, historico, glosario, capa, datos y artefacto; imagenes y
    formato, con esos datos puestos en el repo. Fallan igual que la 1.0.55 con datos de su formato del mismo `work/`:
    ctp_equipos (404 de consola), guia_aceptar 15, guia_ajustes y guia_ficha (el bloque de Cynicalex).
- La 1.0.57 (sin cambio de formato, 20, pero el 20 nunca se publicó: la etiqueta va sobre el commit de datos), 19 de
  noviembre de 2026: **el build de datos de la 1.0.56 falló y se arregla**; quien actualiza pasa de la 1.0.55 a esta, y
  las notas cuentan Objetos.
  - **La falla.** El workflow cortó en `completitud.py` («data.js no trae los liderazgos que scripts/liderazgos.py deriva
    de sus datos»). thanosvibs publicó dos filas de la 12.4.5 («War of Kings (Part 2)», 3 de diciembre) con el uniforme
    «???»: `blackbolt5` (`uniformed` False, sin `uniform_id` ni fila en `/api/uniforms`, y la fila y las skills iguales a
    las de la base) y `karnak2` (uniforme con `uniform_id`, skills nuevas y una pasiva de uniforme «???»). blackbolt5
    entraba a medias: `_core.py` tomaba la primera fila sin uniforme de cada personaje y salteaba la otra sin decir nada,
    pero sus skills, su perfil, su análisis y el liderazgo que `liderazgos.py` deriva (fuentes.py le pasa todos los
    retratos de `work/characters.json`) iban a data.js.
  - **El criterio** (quien coordinó prefería dejarlos fuera hasta que tengan nombre; los datos lo confirman: blackbolt5
    es una copia de la base y entrarlo daba dos Black Bolt iguales): una fila cuyo uniforme o personaje es solo «?» es un
    **adelanto** y no entra a los datos. `fetch_all.py` la deja fuera de `work/characters.json` (y con eso de sus skills,
    su retrato y todo lo que sale de ahí) y la anota en `work/adelantos.json`; borra las skills de los retratos que ya no
    están, como las tier lists. El build pide `work/adelantos.json` y `auditar.py` da un AVISO por cada adelanto y su
    línea en `docs/AUDITORIA.md` (sección 4). karnak2 también queda fuera (el mismo criterio; tampoco estaba en los datos
    publicados). Sus llegadas de `/api/updates` quedan en `docs/HISTORICO.md` como llegadas sin retrato. Cuando thanosvibs
    les ponga nombre, entran solos.
  - **Lo que lo habría detectado** (`completitud.py` lo notó solo porque derivaba un liderazgo): `_core.py` corta si un
    personaje tiene más de una fila sin uniforme, y `build.py`, si una tabla por retrato (MFF_SKILLS, MFF_BUFFS,
    MFF_PERFIL, MFF_ANALISIS, MFF_CANCELS, MFF_SOPORTES, MFF_ROTACIONES, MFF_GUIA_PJ, la guía de armado, MFF_VERIFICACION)
    trae un retrato que el roster no tiene. Probados los dos con el `work/` de la falla.
  - **Retratos.** thanosvibs ya publica los de Vulcan, Lilandra y Deathbird (256x256, fondo transparente): los temporales
    de la 1.0.55 salen de `fuentes/propio/retratos/` (hoy no queda ninguno); `verif_propio` espera los de thanosvibs.
  - **War of Kings en thanosvibs.** Publica a Vulcan (id 297), Lilandra (295) y Deathbird (296), con sus skills y la 12.4
    («War of Kings», con fecha 19 de noviembre; la nota es del 17). Lo propio sigue mandando y no se tocó: las
    diferencias (id, habilidad de jefe mundial, stats, striker, valores de skills, golpes, cargas y recargas), en
    `docs/AUDITORIA.md` sección 13, para que Ezequiel decida qué manda en cada campo. Todavía no publica sus artefactos,
    los cromos de War of Kings ni el C.T.P. de Ascenso (siguen propios, sin ícono).
  - Pendiente / a decidir: las diferencias de lo propio contra thanosvibs de los tres (y las de Agatha, Wiccan, Morgan,
    Dormammu y Clea, que siguen desde octubre). El id propio (9001 de Agatha contra el 294 de thanosvibs) hace que las
    tier lists de thanosvibs no la crucen (AVISO «entradas sin personaje: Agatha Harkness / Modern» en seis listas); con
    los ids propios 9002 a 9004 pasará lo mismo con Vulcan, Lilandra y Deathbird cuando entren a una lista.
    Visto y sin tocar: thanosvibs ya marca a Karnak (base y All-New, All-Different) como Tier-4, la de la 12.4.5, sin su
    Striker Skill (docs/AUDITORIA.md, sección 4): la app lo muestra T4 desde hoy.
  - Corridas: la secuencia del workflow, de punta a punta, termina con 0 con Python 3.13 (en el clon) y con 3.12 (en un clon
    nuevo, sin `work/`, como Actions); `git add` del paso «Commitear» y `construir.py formato` sobre `datos/20/` pasan.
    Con los datos armados el 19 de noviembre (`MFF_DATOS`): sin fallas propio, humo, ficha, objetos, cromos, recorrido,
    historico y analisis; imagenes y formato, con esos datos puestos en el repo.
- La 1.0.58 (sin cambio de formato, 20; la release va sobre el commit de versión), 20 de noviembre de 2026: **sin GitHub
  Actions** (Ezequiel: «GitHub Actions: no usar», la regla literal en «Cómo trabajamos»). Sin cambios a la vista en la
  app: cambia cómo se publican los datos y las versiones.
  - **Datos, desde la PC de Ezequiel**: `scripts/actualizar_datos.py` (con doble clic, `ActualizarDatos.bat`) hace lo de
    `actualizar.yml` y empuja; la tarea semanal queda escrita, sin registrar (ver «Datos»). Para Windows: los scripts
    corren en modo UTF-8, y los archivos que se commitean y se escribían en modo texto sin `newline`
    (`mff-thanosvibs-import.json`, las notas de `fuentes/foro` y `fuentes/cafe`) van con LF.
  - **Release, en la sesión**: `construir.py release vX.Y.Z` (con Inno Setup bajo Wine) y `construir.py subir vX.Y.Z
    <commit>` para Ezequiel (ver «Release»).
  - Corridas: `actualizar_datos.py` de punta a punta con Python 3.12 en un clon nuevo sin `work/` (3 min 35 s; el commit y
    el push, a un repo local), y otra vez con un bundle sin seguir en la raíz (aviso, no va al commit), y sus cortes:
    un cambio o un borrado en un archivo seguido, un archivo sin seguir en `fuentes/foro`, otra rama, sin upstream, main
    adelantado, main y origin/main separados, sin red en el primer paso, el build roto después de traer origin/main, un
    archivo nuevo fuera de las rutas después del build, y «Sin cambios». `build.py` con el Python 3.14.7 de Windows bajo Wine: con la misma `PYTHONHASHSEED`, `data.js` igual
    byte a byte al de Linux; sin `PYTHONUTF8`, se cae en `skills_api.py` (cp1252). Con Wine 9.0 (Ubuntu
    9.0~repack-4build3, con wine32:i386) e Inno Setup 6.7.3, la v1.0.57 armada así frente a la publicada: lo de
    «Release» (mismos 51 archivos; LF en lugar de CRLF; los íconos de más). Con la 1.0.58: `verif_wine` y
    `verif_programa` sin fallas (las dos al día: la mesa, `datos/<formato>/`, la capa guardada, el respaldo del día y
    `TMPDIR`); la 1.0.57 publicada (el programa que instaló el instalador de Actions) se actualiza con el parche 1.0.58
    y queda con los archivos del commit (prueba suelta fuera del repo, con el Python de Linux: el parche usa
    `shutil.copy2`, que Wine 9 no tiene); el instalador 1.0.58 se instala encima de la 1.0.57 publicada y desinstala
    dejando la carpeta de datos (bajo Wine). `verif_actualizacion_real` y `verif_parche_1xx` son de la 1.0.1 a la 1.0.19
    y no corren con la versión de hoy. **No probado en un Windows real**: el script de datos (git, la bajada de las
    fuentes, el Programador de tareas), `subir` y el instalador.
  - Pendiente / a decidir (Ezequiel): qué hacer con `actualizar.yml` y `publicar.yml`, que siguen activos; registrar o no
    la tarea semanal; la lista de pasos y rutas duplicada con `actualizar.yml`. Ajustes sigue diciendo que los datos «se
    arman cada lunes»: vale si se registra la tarea. El build no es determinista entre corridas (`PYTHONHASHSEED`).
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
- Apartados nuevos: Cromos de cómic (#35: la sección y los mazos, en la 1.0.53; falta cómo pesan en los equipos, con #34),
  Espadas (#36), Jarvis (#37: la consulta, en Objetos de la 1.0.56; faltan los valores de los chips); atributos de las skills
  (#38). Objetos (1.0.56): lo pendiente de cada sistema, en su entrada de «Estado»; anotar lo que uno tiene, con #34.
- Histórico: el texto coreano de las notas en la app (#42; las notas en `fuentes/cafe/`, el cotejo en
  `docs/NOTAS_COREANO.md`, la revisión en `docs/REVISION_COREANO.md`; desde la 1.0.33 los casos dudosos llevan «≠»),
  las llegadas que siguen sin su nota (lista en `docs/HISTORICO.md`: de 2015, notas con imágenes y parches); los modos
  que las notas nombran y `modos.json` no tiene (#46). Rediseño de la información, segunda parte (#41; la 1.0.52 hizo «Mi
  cuenta» aparte: falta «Referencia», los avisos como estado y las direcciones estables). Preguntas abiertas: #11 a #20 y #23. Bugs: ninguno abierto (#25 y #26 cerrados).
