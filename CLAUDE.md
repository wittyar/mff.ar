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
  copia más reciente va en un zip junto al bundle de la 1.0.14 (`pruebas-mff-*.zip`).

## Estado (2 de octubre de 2026)

- Publicada: la 1.0.12 (datos de formato 3).
- Entregadas sin publicar: la 1.0.13 (solapa Glosario, formato 4) y la 1.0.14 (equipos por
  contexto PvP y PvE, strikers, velocidades y resistencias en «le sirve»; formato 5). Se publica solo
  la 1.0.14: sus notas ya anuncian el Glosario.

## Pendiente

- Ajustar los pesos del puntaje de contexto mirando casos (hoy: liderazgo 2 y DPS 2 por nivel;
  sinergia y strikers, 1). Ver «Equipos por contexto» en `docs/MODELO.md`.
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
