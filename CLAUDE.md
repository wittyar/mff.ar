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
  `catalogo.validar_glosario` y `fuentes.validar_contenido`.
- Pruebas: no están en el repo. Son scripts de Playwright contra la app servida por
  `desktop/lanzador.py`, con modelos de la sinergia y del puntaje escritos aparte de `app.js`. La
  copia más reciente va en un zip junto al último bundle (`pruebas-mff-*.zip`); su `LEEME.txt` dice
  qué rutas adaptar. `images/` y `work/` no están en el repo: las imágenes se bajan con
  `bajar_imagenes.py`, y sin `work/` no corren verif_guia_ficha, verif_marcadores ni verif_opciones.
  Las que leen el contenido curado del repo (verif_glosario) fallan contra un data.js viejo:
  `armar_datos_contenido.py` arma datos de prueba con el contenido nuevo, y `armar_datos_build.py`, con
  lo que el próximo build cambia en data.js sin tocar el esquema (hoy, `SEED.SKILL_TAGS`).
  `verif_consistencia.py` compara, para las 888 variantes, lo que contesta cada pantalla a la misma
  pregunta (formato de los soportes, verificación, recarga, filas de las listas, habilidades del
  filtro, efectos de la comparativa, strikers) y lista como pendientes las de las reglas sin decidir.

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

- Con el próximo build (carril de consistencia, sin `work/` no se pudo correr): `SEED.SKILL_TAGS` con
  las habilidades de todas las variantes (el filtro del roster suma Zombi y Guardianes de la
  Galaxia) y la sección 11 de `docs/AUDITORIA.md` con las dos probabilidades de striker de más de
  100% (Daken: Doctor Octopus, 219%; Molecule Man: Morgan le Fay, 120%), contadas en el resumen.
  Después, verif_consistencia tiene que pasar con los datos del repo.
- Consistencia entre pantallas: quedan las preguntas que dependen de reglas sin decidir (líder del
  trío, «le sirve», los liderazgos que Leads & Supports no publica, si el soporte propio cuenta para
  su dueño y qué es anti-mermas, los strikers fuera de PvP y PvE, y los recomendados de Modos contra
  la función en PvP y PvE). verif_consistencia las tiene listadas.

- Capturas del 2 de octubre (380, transcriptas el 4 de octubre):
  - El glosario cita la captura en coreano de Mind Control, Recharge Shield, Fracture e
    Incapacitation, pero en las 380 que llegaron a esta conversación la lista coreana nunca los abre.
    Si salen de otra tanda, está bien; si no, hay que sacarles esa cita y a Mind Control su
    diferencia y el error «inmunes». Pánico en coreano sigue sin captura.
  - Strikers del juego: Galactus tiene 16 y la app ninguno; los 37 visibles de Kingpin coinciden
    con la wiki. Cargarlos pide un archivo de contenido, una fuente y código nuevos (el juego por
    encima de la wiki, fila por fila) y probablemente formato 7. Falta decidir.
  - Wall: el glosario dice «Lo da: Conquest sin reforjar», pero va en la opción fija, que el C.T.P.
    conserva al reforjarlo. Arreglarlo pide cambiar `reforjado` o cómo lo escriben catalogo.py y
    app.js.
  - Bonos de equipo: las capturas no resuelven el pendiente de más abajo, porque los integrantes
    solo se ven por retrato. Para eso, capturar «TEAM BONUS PER CHARACTER» de cada candidato (la
    barra muestra el nombre) y la lista de Galactus hasta el final (Heralds #3).
  - Urus: el juego habla de urus amplificados y thanosvibs de ranuras amplificadas. Verlo en el
    juego.
  - Sin cargar, de la guía del juego: los Boost Points de Giant Boss Raid, quién juega Alliance
    Battle y su requisito del día, las temporadas de 8 semanas de Otherworld; el juego escribe
    «Judgment» y thanosvibs «Judgement».
- Completitud: falta decidir si los que la guía de armado marca «dont waste gold» cuentan como
  faltantes y si el informe (unos 220 KB) se achica.
- Propuesta, sin decidir: que publicar.yml no publique una versión si el `datos.json` de main no es
  del formato de `version.json`. Evita lo que pasó con la 1.0.17.
- Las «permutaciones» de los mismos integrantes que Ezequiel vio en la lista de Adam Warlock no
  aparecen en las listas de combinaciones; si vuelven, falta una captura.
- Equipos (1.0.18):
  - En PvP y PvE, el «X para él» usa el líder de la sinergia y la tarjeta, el del contexto. En Adam
    Warlock + Wasp + Doctor Voodoo, la tarjeta dice Wasp y la sinergia usa a Doctor Voodoo.
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

- El caso Silver Surfer — Void Knight + Knull — Ancient History + Gorr: con las defensas de la
  1.0.15 y el condicional a la mitad empatan 6 a 6, y lidera Gorr por la tier list, no por peso (ver
  «Casos de referencia» en `docs/MODELO.md`). Falta decidir si así está bien.
- Volumen de las listas (medido el 2 de octubre sobre la 1.0.14, antes de las listas solo con
  función; hay que volver a medirlo). Exigir en PvP un liderazgo que valga saca el 59% de las
  tarjetas (Galactus, de 37.514 a 1.699; Silver Surfer — Void Knight sigue en 37.452). Una lista por
  personaje en vez de una por uniforme deja 290 listas en vez de 888 y saca el 54%, con cada lista
  casi igual. Las dos juntas sacan el 80%. Falta decidir.
- Fuera de los órdenes PvP y PvE, el líder sigue siendo el de la sinergia, el que más le suma al
  personaje de la ficha: «puntos para él», las tier lists sin contexto, Favoritos y Mis equipos. Mis
  equipos guarda dos veces el mismo trío si se guarda desde dos listas. Falta decidir.
- El filtro de PvP acepta anti-mermas condicionales (al recibir un debuff). Falta decidir.
- Liderazgos completados por Leader Skill idéntica a la de la base (sección 12 de AUDITORIA.md):
  según la prueba, knull1, shangchi2, moongirl1, ghost2 y sentinel2. Falta decidir si se extiende a
  una hermana (sumaría captainamerica15, greengoblin5 y wintersoldier6), si el build tiene que parar
  cuando solo difiere `sig` y si la ficha dice que el liderazgo es heredado.

- Liderazgo en PvP: Molecule Man es «la excepción rara» (Ezequiel) y hoy no suma nada fuera de los
  anti-mermas, ni tiene lista de PvP; el daño contra una facción no cuenta. Falta decidir cómo
  cuentan. Según NamuWiki, el tercero de un equipo de Timeline suele ser un «buffer» de daño entre
  facciones (Colossus), y Molecule Man ignora justamente eso. Los pesos se revisaron con casos y
  quedaron igual (ver «Casos de referencia» en `docs/MODELO.md`).
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
