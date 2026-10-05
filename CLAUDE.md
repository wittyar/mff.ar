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

- Formato 7 (carril de consistencia, segunda parte): `scripts/build.py` ya escribe datos de formato 7
  (el catálogo trae a quién le sirve cada stat de liderazgo, soporte y bono, y `MFF_VALOR` los pesos
  de PvP y PvE), pero `version.json`
  sigue pidiendo el 6 (el carril no lo tocó). Subirlo a 7 en el push que publica, con la etiqueta.
- Con el próximo build (carril de consistencia, sin `work/` no se pudo correr): `SEED.SKILL_TAGS` con
  las habilidades de todas las variantes (el filtro del roster suma Zombi y Guardianes de la
  Galaxia) y la sección 11 de `docs/AUDITORIA.md` con las dos probabilidades de striker de más de
  100% (Daken: Doctor Octopus, 219%; Molecule Man: Morgan le Fay, 120%), contadas en el resumen.
  Después, verif_consistencia tiene que pasar con los datos del repo.
- Consistencia entre pantallas: queda la pregunta de los recomendados de Modos contra la función en
  PvP y PvE (verif_consistencia la tiene listada como pendiente).
- Anti-mermas propios con probabilidad: no cuentan (Hulkling). Ezequiel nombró a Captain America entre
  los que tienen anti-mermas propio, pero en la API el suyo es de 50% o 60% al recibir un debuff, así
  que hoy no cuenta. Falta que lo confirme (lista en «Equipos por contexto» de `docs/MODELO.md`).

- Capturas del 2 de octubre (380, transcriptas el 4 de octubre):
  - Strikers del juego: Galactus tiene 16 y la app ninguno; los 37 visibles de Kingpin coinciden
    con la wiki. Cargarlos pide un archivo de contenido, una fuente y código nuevos (el juego por
    encima de la wiki, fila por fila) y probablemente formato 7. Falta decidir.
  - Bonos de equipo: las capturas no resuelven el pendiente de más abajo, porque los integrantes
    solo se ven por retrato. Para eso, capturar «TEAM BONUS PER CHARACTER» de cada candidato (la
    barra muestra el nombre) y la lista de Galactus hasta el final (Heralds #3).
  - Urus: el juego habla de urus amplificados y thanosvibs de ranuras amplificadas. Verlo en el
    juego.
- Completitud: falta decidir si los que la guía de armado marca «dont waste gold» cuentan como
  faltantes y si el informe (unos 220 KB) se achica.
- Propuesta, sin decidir: que publicar.yml no publique una versión si el `datos.json` de main no es
  del formato de `version.json`. Evita lo que pasó con la 1.0.17.
- Las «permutaciones» de los mismos integrantes que Ezequiel vio en la lista de Adam Warlock no
  aparecen en las listas de combinaciones; si vuelven, falta una captura.
- Equipos (1.0.18):
  - Las casillas siguen marcadas al cambiar de orden, de uniforme o de personaje, como «Sin».
    Falta decidir.
  - Alliance Battle muestra los C.T.P. de PvE, pero la leyenda de la guía dice «ABX: Rage». Falta
    decidir. Los equipos recomendados de Alliance Battle y los descartados no muestran C.T.P.
  - El link de un soporte busca la skill por el nombre que le da Leads & Supports. La «Pasiva 4★
    (secundaria)» de Jeff es su Activa 5, y en Polaris — Uncanny X-Men el nombre de la Tier-2 está
    mal, así que el link cae en la Activa 1.
- Marcadores:
  - El mismo par de valores en otro orden cuenta como diferencia entre fuentes. En Abomination
    base, Fists of the World Ravager, Leads & Supports dice Villains y después Heroes, y la wiki
    al revés: queda listado y la ficha invierte las dos líneas.
  - Falcon (Joaquin Torres): Leads & Supports pone su Tier-2 en `passive`, así que no se cruza.
  - Las filas vacías de `marcadores.csv` que ahora resuelve Leads & Supports siguen en la tabla.
  - Con el primer build, verif_marcadores (necesita `work/`) tiene que actualizar sus cuentas.
  - Los avisos de `soportes()` salen dos veces en el log del build (fuentes.py y marcadores.py).

- Tabla de valor (`scripts/contenido/valor_equipos.json`): los pesos son la propuesta del 4 de
  octubre (en PvP, vida 2,5, ataques 2, defensas 1,5, ignorar evasión 1, efecto de los debuffs 0,5).
  Falta que Ezequiel la confirme con los «Casos de referencia» de `docs/MODELO.md`: los cuatro pares
  siguen ganando por puntaje, y en el trío Silver Surfer — Void Knight + Knull + Gorr ahora lidera
  Gorr por peso (7,5 a 5,25), no por la tier list.
- Volumen de las listas (medido el 2 de octubre sobre la 1.0.14, antes de las listas solo con
  función; hay que volver a medirlo). Exigir en PvP un liderazgo que valga saca el 59% de las
  tarjetas (Galactus, de 37.514 a 1.699; Silver Surfer — Void Knight sigue en 37.452). Una lista por
  personaje en vez de una por uniforme deja 290 listas en vez de 888 y saca el 54%, con cada lista
  casi igual. Las dos juntas sacan el 80%. Falta decidir.
- El filtro de PvP acepta anti-mermas condicionales (al recibir un debuff). Falta decidir.
- Liderazgos de la Leader Skill (carril Q, 5 de octubre de 2026; regla de Ezequiel del 4 de octubre):
  `scripts/liderazgos.py` reemplaza a la copia del liderazgo de la base. Sin `work/` el build no se pudo
  correr; con los datos de formato 7 (`armar_datos_lideres.py`), el próximo build tiene que dar: 328
  variantes con liderazgo derivado (345 slots, con `"src": "api"`), 151 slots sin derivar, 34 efectos, 2
  activaciones y 1 condición aprendidos, una contradicción (la condición de Drax) y, en la verificación,
  392 de 448 slots de Leads & Supports iguales, 3 distintos (Black Swan, The Hood y Mephisto) y 51 que no
  se pueden derivar; en `docs/COMPLETITUD.md`, «Liderazgo sin completar» en 151 variantes y 144 de 888
  completas. Si thanosvibs cambió algo, las cifras se mueven: lo que no puede pasar es un slot sin
  derivar ni listar. Después tienen que pasar con los datos del repo verif_consistencia (la fuente de
  cada liderazgo, ahora también sobre los datos) y la regresión (verif_combos ya espera «No mejoran con
  él: Arena», porque Captain America e Iron Man tienen liderazgo derivado). Hasta ese build,
  `scripts/completitud.py` sobre el data.js del repo para con «data.js no trae los liderazgos que
  scripts/liderazgos.py deriva de sus datos»: es lo esperado.
- Falta decidir, sobre los liderazgos derivados (lista en «Liderazgos que Leads & Supports no publica» de
  `docs/MODELO.md` y en la sección 12 de `docs/AUDITORIA.md`):
  - «Notable»: lo derivado no lo lleva (es una marca de thanosvibs). Knull — Ancient History y Ghost —
    Thunderbolts* lo tenían copiado de la base y lo pierden: su liderazgo suma 2 en la sinergia, no 3.
  - 80 slots no se derivan por la activación (Leads & Supports solo publica liderazgos al recibir un
    debuff o con la vida baja; las otras son «25% rate when hit», «when tagging»...) y 99 por un efecto
    que Leads & Supports no publica en ningún liderazgo (defensa física, resistencias, escudos, velocidad
    de ataque). Cargarlos pide una correspondencia a mano en `scripts/contenido/`, con su fuente.
  - Drax: Leads & Supports pone la condición «when 1 Combat»... en dos de sus cuatro variantes, así que no
    se usa, y Nebula (5 variantes, el mismo objetivo) queda sin liderazgo.
  - Sentry — Thunderbolts* y Mephisto — Master of Hell tienen un slot derivado y el del «Give Power» no: la
    app muestra un liderazgo sin el anti-mermas que probablemente tienen [Probable: en los 19 pares, el
    «Give Power» es quitar los debuffs al recibir uno].
  - Las listas de PvP y PvE toman el vínculo de cada compañero de la consulta, que usa el líder sin
    contexto: con los derivados, la de Malekith — All-New, All-Different baja de 4.826 a 3.631 (ejemplo en
    «Equipos por contexto» de `docs/MODELO.md`). Falta decidir si el vínculo sale del líder del contexto.

- Liderazgo en PvP: Molecule Man es «la excepción rara» (Ezequiel) y hoy no suma nada fuera de los
  anti-mermas, ni tiene lista de PvP; el daño contra una facción no cuenta. Falta decidir cómo
  cuentan. Según NamuWiki, el tercero de un equipo de Timeline suele ser un «buffer» de daño entre
  facciones (Colossus), y Molecule Man ignora justamente eso. Los pesos están en la tabla de valor
  (ver «Casos de referencia» en `docs/MODELO.md`).
- Compañeros sin función en el contexto: entran igual si tienen vínculo con él. Falta decidir si
  quedan fuera, como el personaje de la ficha.
- Bonos de equipo del juego por confirmar con capturas. Quedaron anotados así: W, D, R y SW; con
  duda, Sersi, Beta Ray Bill, Amadeus Cho, Doom y Kang; el segundo stat de Heralds #3; la lista de
  Annihilus.
- El artefacto de Robbie Reyes da daño según la resistencia a los aliados Llama: depende de que él
  esté en el equipo y «le sirve» no ve el equipo.
- Set Striker (el striker que se elige para cada personaje, de 6★ o más): es otro sistema y la app
  no lo tiene. A 119 personajes la wiki no les tiene la pestaña Striker.
- Rendimiento: con quien da algo a todos (Galactus), la consulta de combinaciones tarda cerca de
  1,5 s y el orden PvP otro tanto.
- Decidir si las pruebas pasan al repo.
