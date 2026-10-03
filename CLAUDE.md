# MFF.ar: notas para Claude

Comparador personal de MARVEL Future Fight de Ezequiel, como app de escritorio (README.md). El
modelo del juego, con las reglas y decisiones de Ezequiel y de dónde sale cada dato, está en
`docs/MODELO.md`; lo que no cierra entre fuentes, en `docs/AUDITORIA.md`.

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
  `datos.json`, `docs/AUDITORIA.md` y `docs/CATALOGO.md`; para con un mensaje si el contenido curado
  (`scripts/contenido/`) no cierra con los datos.
- Pruebas: no están en el repo. Son scripts de Playwright contra la app servida por
  `desktop/lanzador.py`, con modelos de la sinergia y del puntaje escritos aparte de `app.js`. La
  copia más reciente va en un zip junto al último bundle (`pruebas-mff-*.zip`); su `LEEME.txt` dice
  qué rutas adaptar. `images/` y `work/` no están en el repo: las imágenes se bajan con
  `bajar_imagenes.py`, y sin `work/` no corren verif_guia_ficha, verif_marcadores ni verif_opciones.

## Estado (3 de octubre de 2026)

- Publicadas: la 1.0.14, la 1.0.15 y la 1.0.16 (datos de formato 5). La 1.0.13 no se publicó; las
  notas de la 1.0.14 anuncian su Glosario.
- Entregada sin publicar: la 1.0.17 (los marcadores también se completan con Leads & Supports;
  datos de formato 6). El data.js de main sigue en formato 5 hasta que corra el workflow
  «Actualizar datos MFF», que ya arma con la regla nueva y con los liderazgos completados por
  Leader Skill idéntica. El orden es este:
  1. Push.
  2. Workflow a mano.
  3. Confirmar el commit «Datos actualizados» con `datos.json` en formato 6.
  4. Etiqueta `v1.0.17` sobre ese commit, así el instalador lleva datos de formato 6. Si la
     etiqueta sale antes que los datos, el parche deja a la app esperando la próxima publicación.
  `MFF.bat` comparte la carpeta de datos con la app instalada: abrir la del repo con datos de
  formato 6 deja a la 1.0.16 instalada en la pantalla de datos. Primero se actualiza la instalada.

## Pendiente

- Doctor Voodoo — Savage Avengers entra a la lista de PvP de Adam Warlock por el Ignore Dodge +30%
  a todos los aliados de su Tier-2 (así lo publican la API de skills y Leads & Supports). Ezequiel
  dice que no les da nada a los demás: falta mirarlo en el juego y, si thanosvibs está mal, cargar
  una corrección a mano. Las «permutaciones» de los mismos integrantes que vio en su lista no
  aparecen en las listas de combinaciones; falta ver dónde estaban.
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
  cuentan. Los pesos se revisaron con casos y quedaron igual (ver «Casos de referencia» en
  `docs/MODELO.md`).
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
