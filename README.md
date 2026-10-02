# TA GUIANAEL MFF

App de escritorio para Windows (HTML/JS sin dependencias ni build, servida por un proceso Python
local) para consultar y comparar personajes de MARVEL Future Fight, ver para qué se usa cada uno y
cómo armarlo, armar equipos y trabajar sobre tier lists. 290 personajes, 598 uniformes, 9.147 skills con efectos estructurados por objetivo.
**Material de consulta de uso interno/personal, sin fin comercial.**

**Fuentes de datos** (crédito correspondiente):
- [THANO$VIB$](https://thanosvibs.money) — personajes, uniformes, **skills**, costos de mejora,
  tier lists públicas, C.T.P., artefactos, efectos de líder y de soporte, rotaciones, Alliance
  Battle (restricciones y equipos), la Beginner's Guide, retratos e íconos.
- [Future Fight Wiki (Fandom)](https://future-fight.fandom.com) — el instinto y los bonos de equipo
  (thanosvibs no los publica), los requisitos de Tier-3/Trascendencia/Tier-4, las reglas de ISO,
  urus y gear, y el contraste de `docs/AUDITORIA.md`.
- [Cynicalex Mega Guides](https://docs.google.com/spreadsheets/d/1H0Hcl9oVZV9gA266xkJAqPv5bD1qwqhC5NeVbLj_-FE)
  (planilla de Google) — la **guía de armado** por personaje (pestaña CHAMP BUILDING) y la
  leyenda de los emojis de su tier list (pestaña TIER LIST).
- MARVEL Future Fight, el juego (capturas de Ezequiel, octubre de 2026) — su glosario de skills,
  en inglés y en coreano (qué hace cada efecto, en el catálogo), su guía de contenidos y de crecimiento, la ficha de cada
  C.T.P. (contrastada con thanosvibs en `docs/AUDITORIA.md`) y los bonos de equipo de los personajes
  que la wiki todavía no tiene.

## Qué hay en la app
- **Roster** con filtros (clase, rol, tier, bando, instinto, raza, habilidad, efecto, objetivo,
  atributos marcados, y lo que da su liderazgo o su soporte: ver *Índice para armar equipos*) y
  orden por la tier list que elijas.
- **Ficha** de cada personaje y uniforme, en pestañas. Arriba, fijos, la foto, el nombre, las
  flechas ‹ › para pasar al anterior o al siguiente del listado del roster tal como está
  filtrado y ordenado (también con ← y →; la pestaña se conserva) y el selector de uniforme (el
  uniforme cambia casi todo lo de abajo). Si se llegó desde otro personaje (por ejemplo, desde
  sus combinaciones), «← Nombre» vuelve a él tal como estaba: pestaña, página y posición; también
  con Alt+← o el botón de volver del mouse. «← Roster» vuelve al roster donde se lo dejó:
  - *Resumen*: los datos del uniforme puesto, lo que **le sirve** de un liderazgo o un soporte
    (con atajos al roster: «Líderes que se lo dan», «Soportes que se lo dan») y *para qué se
    usa*: su fila en cada tier list, lo que le da al equipo (liderazgo, pasivas, efecto de
    uniforme y artefacto, con a quién se aplican y sus categorías del índice), dónde lo recomienda la guía, en qué equipos de Alliance Battle aparece, qué
    controles aplica para cortar a los jefes y lo que dice la **guía de armado de Cynicalex**:
    su mejor uniforme, su lugar en la tier list de la guía con los emojis explicados, cómo se
    consigue y la nota.
  - *Skills*: cargas de ult y striker, buffs clave, las **rotaciones** de thanosvibs con la
    leyenda de la notación, las de la guía de armado (de proc, con su mejor C.T.P. y la skill de
    proc / frenesí, con su propia notación) y cada skill, con tabla de daño por etapa.
  - *Análisis*: lo que hace con sus skills según el catálogo de efectos (ver *Modelo del juego*):
    un resumen (qué da para él, para el equipo y contra el rival, con qué pega y sus roles) y,
    por grupo de efecto, cada efecto con a quién le llega (él, el equipo y qué aliados, el rival
    o sus invocaciones), de qué skill sale y cuándo, su condición (contra jefes, contra una
    facción...), si no le sirve (un buff de algo que él no usa) y cómo se lee en PvE y en PvP,
    con su certeza y su fuente. Marca lo que la fuente no dice: el «Give Power» que no trae qué
    otorga y lo que el catálogo todavía no clasifica.
  - *Armado*: su C.T.P. según la Ideal CTP List, la guía de principiantes y la guía de armado
    (esta dice en qué lugar lo pone —mejor, segundo, meta y fuera del meta de PvE y de PvP— y
    si va reforjado); su artefacto con los valores por nivel de estrellas y si lo necesita
    según la guía de armado; el ISO-8 (cada categoría con sus sets) y el obelisco de la guía de
    armado; las **opciones del uniforme** abierto (qué uniforme habilita cada una y qué stat
    conviene elegir); plegadas, las reglas generales de ISO y urus para su tipo de ataque
    (derivado de sus skills). Lo de la guía de armado es de su mejor uniforme: si está abierto
    otro, lo dice.
  - *Equipos*: con el uniforme elegido, tus equipos donde ya está; cómo entraría en los otros
    (el mejor cambio según la sinergia de la app: a quién reemplaza o si se suma, el puntaje
    antes y después, y qué se gana y qué se pierde; tiene que quedar con *vínculo* con alguien
    del equipo: le da un soporte o el liderazgo, o recibe uno suyo, y le sirve (un efecto que sube
    un ataque o un daño elemental solo cuenta para quien pega con eso según sus skills, así que un
    liderazgo de daño de fuego no vincula a uno que pega físico), o forman juntos un bono de
    equipo); sus **bonos de equipo**, plegados: con quiénes, qué suben y de dónde sale cada uno
    (valen con cualquier uniforme); sus **strikers** y de quiénes es striker, plegados, con la
    probabilidad de aparecer y cuándo (de la pestaña Striker de la wiki); y **todas las
    combinaciones de 3 con él**, una consulta sobre los datos: cada pareja de compañeros con vínculo
    con él, una por trío de personajes, de a 20 por página. Se ordenan por *puntos para él* (la
    sinergia contando solo lo que lo involucra), por cualquier tier list, también las tuyas, o por
    **contexto**: PvP o PvE, con las reglas de Ezequiel (ver *Equipos por contexto* en
    `docs/MODELO.md`). Si él no figura en las tier lists del contexto (Arena; Alianza y WBL), o solo
    como «Not for wbl», no tiene función ahí y ese orden no arma combinaciones. En un contexto entran
    solo los tríos con algún DPS de sus tier lists y, en PvP, con anti-mermas para los tres; un DPS
    entra aunque no tenga vínculo con él, y el puntaje de equipo (liderazgo, DPS, sinergia y
    strikers) dice de dónde sale cada punto. Se
    filtran con «Con» y «Sin»; cada una dice su líder y su **cobertura** (lo que recibe él en
    ese equipo, por categoría del índice), se marca con ★ como favorita, se arma
    para tu cuenta o se *descarta*: el trío se oculta en las combinaciones de sus tres
    personajes, con cualquier uniforme, y «Ver descartados» los muestra para restaurarlos.
  - *Progreso*: la hoja de ruta de progresión y la calculadora de topes de stats, que se guardan
    en tu capa.
  - *Más*: la verificación entre fuentes y el retrato propio.
- **Comparar** hasta 4 variantes lado a lado, con la sinergia estimada.
- **Tier lists**: todas las listas públicas de thanosvibs, con sus filas originales; listas
  propias de personajes, de C.T.P., de artefactos o de tus equipos, con filas a medida. Una entrada
  puede estar en varias filas de la misma lista.
- **Modos**: los 14 modos que la guía marca como importantes, con qué dan, cómo armar el equipo,
  personajes y C.T.P. recomendados, y el armado general (ISO, urus, 4.º gear, opciones de
  uniforme, obelisco) para PvE y PvP.
- **Equipos**: los equipos de tu cuenta, con el modo y su tamaño según la fuente (Alliance
  Conquest: dos escuadras de 3); los favoritos (★), y los descartados, plegados, para
  restaurarlos. Al armar uno, avisa si un personaje ya está en otro equipo tuyo del mismo modo.
- **Glosario**: los 44 términos del glosario de skills del juego, en inglés, coreano y español,
  con lo que el inglés traduce distinto del coreano (los tres errores que se repiten van aparte)
  y qué C.T.P. da cada efecto de la barra de Concentración; y los 126 efectos del catálogo por
  grupo, con sus lecturas de PvE y de PvP, a quién le sirven y con qué etiquetas aparecen en las
  skills. Se busca en los tres idiomas y los enlaces llevan de un término a sus efectos y al revés.

Todo lo que viene de una fuente la cita; lo derivado se dice derivado; lo que falta en la fuente
se marca como faltante en vez de inventarse.

## Instalar y usar
1. Bajar `TA-GUIANAEL-MFF-X.Y.Z.exe` de la [última release](https://github.com/wittyar/mff.ar/releases/latest).
2. Abrirlo. El instalador no está firmado, así que Windows muestra *"Windows protegió su PC"*:
   **Más información → Ejecutar de todas formas**. No pide permisos de administrador.
3. Queda un acceso directo en el menú Inicio (y, si lo marcaste, en el escritorio).

La app abre en su propia ventana (Microsoft Edge en modo app, con un perfil aparte que no toca el
navegador de todos los días) y se cierra sola unos minutos después de cerrar la ventana: no hay
consola ni servidor que cerrar por separado. Abrirla dos veces abre otra ventana contra la misma
instancia.

- **Programa**: `%LOCALAPPDATA%\Programs\TA GUIANAEL MFF`.
- **Datos**: `%LOCALAPPDATA%\TA GUIANAEL MFF` — `capa.json` (lo tuyo), `respaldos/` (una copia de
  la capa por día, quedan 7), `data.js` y `datos.json` (datos del juego), `images/` y `registro.txt`
  (qué pasó en cada arranque). Ajustes muestra la ruta. Desinstalar borra el programa, no los datos.

La primera vez la app abre con los datos que trae el instalador y baja en segundo plano los
retratos e íconos (77 MB de thanosvibs), con el avance a la vista.

### Actualizaciones
Al abrir, la app consulta GitHub:
- **Datos del juego**: `datos.json` (publicado por el workflow semanal, ver abajo) dice qué hay.
  Si hay datos nuevos del formato que entiende esta versión, se bajan solos, se verifican contra
  su sha256 y un botón recarga la ventana para usarlos. Si son de un formato más nuevo, se avisa
  (hace falta actualizar la app). La guía de armado llega con los datos; Ajustes dice qué versión
  de la planilla se usa, cuándo se revisó y, si la última no se pudo usar, por qué.
- **Versión de la app**: cada release publica `latest.json`. Si hay una versión nueva con el mismo
  Python, un aviso muestra las novedades y, confirmado, baja el parche (solo los archivos del
  programa, unos 100 KB), lo verifica, guarda el programa anterior en `programa-anterior/` y se
  reinicia sola en la misma ventana. Si cambia Python, ofrece el instalador completo.
- **Retratos e íconos** que falten: se bajan solos. Los que thanosvibs no publica se cuentan en
  Ajustes y la app muestra el nombre sin ícono.

Sin conexión, la app anda igual con lo que tiene y lo dice en un aviso.

### Pasar lo que tenías en el navegador
Hasta la versión anterior, la capa (listas, equipos, rutas, topes, marcas) vivía en el navegador.
Se pasa una vez: en la versión vieja, **Ajustes → Exportar mi capa**; en la nueva, **Ajustes →
Importar**.

### Desde el repo
`MFF.bat` (Windows, con Python instalado) o `MFF.sh` (Linux/macOS) corren el mismo lanzador sobre
la copia del repo, con **la misma carpeta de datos** que la app instalada. Desde el repo no se
aplican parches: la app avisa que hay versión nueva y se actualiza con `git pull`. No pueden estar
abiertas a la vez la del repo y la instalada (la segunda lo dice y no arranca).

### Publicar una versión
1. En `version.json`: subir `version`, escribir `notas` (es lo que ve el usuario antes de
   actualizar). Si cambia `python`, agregar su sha256 en `PYTHON_SHA256` de
   `desktop/construir.py`: esa versión ya no se puede parchar y pide el instalador completo.
2. Commit, etiqueta `vX.Y.Z` y push de la etiqueta:
   ```
   git tag v1.0.1
   git push origin v1.0.1
   ```
3. El workflow **Publicar versión** arma en Windows el programa, el parche y el instalador (Inno
   Setup) y publica la release con `latest.json`. Si la etiqueta no coincide con `version.json`,
   falla sin publicar.

`formato_datos` (en `version.json`) y `FORMATO` (en `scripts/build.py`) van juntos: se suben cuando
una app y unos datos de versiones distintas ya no se entienden (a la app nueva le falta algo que los
datos viejos no traen, o la anterior leería mal los nuevos). La app solo usa datos de su formato: con
otros, los baja al arrancar o avisa que hay que actualizarla. Formato 2: el perfil de combate viene
calculado en `data.js` (ver *Modelo del juego*). Formato 3: también el análisis de cada variante y el
catálogo de efectos para mostrarlo, y cada uniforme trae sus roles.

## Modelo del juego
`docs/MODELO.md` es el mapa del modelo que arma la app por variante (un personaje con un uniforme):
qué características tiene, qué hacen en el juego, de dónde sale cada una y lo que se deduce, con su
regla. Se construye por etapas (personajes y características, skills, pasivas y soportes, la tabla
final) y lista las dudas abiertas. La etapa 1 ya está: la identidad de cada variante (incluido el
género, que 11 uniformes cambian) y su **perfil de combate** (con qué ataque escala, tipos de daño y
elementos), que calcula `scripts/modelo.py` en el build y la app lee de `data.js`.

Las etapas 2 y 3 arrancan con el **catálogo de efectos** (`scripts/contenido/catalogo.json`): cada
etiqueta de efecto de las skills de thanosvibs y cada stat de Leads & Supports, que son el mismo
efecto visto de dos lados, apuntan a efectos únicos, y cada efecto dice qué es, a quién le sirve y
cómo se lee en PvE y en PvP, con su certeza y su fuente. `scripts/catalogo.py` lo valida en el build
(un error del contenido corta; una etiqueta o un stat nuevo que no está se avisa y va a la sección 9
de la auditoría) y genera `docs/CATALOGO.md`, el catálogo entero para leerlo y revisarlo.

Con el catálogo, `scripts/modelo.py` arma el **análisis** de cada variante: cada efecto de cada
skill con su destino (él, el equipo y qué aliados, el rival o sus invocaciones), sus fuentes y su
condición, y si le sirve a él. La ficha lo muestra en la pestaña *Análisis*. De ahí salen también
los **roles**, que no existen en el juego y dicen qué le aporta cada variante al equipo: Soporte,
le da algo a sus aliados fuera del liderazgo; Tanque, provoca o le baja al equipo el daño que
recibe; Control, le aplica al rival 3 o más controles distintos; Daño, todos. Cada uniforme tiene
los suyos.

## Índice para armar equipos
Lo que da cada liderazgo y cada soporte de thanosvibs (Leads & Supports), en las categorías con
las que se arman los equipos:

| Categoría | Stats de thanosvibs | Le sirve a |
|---|---|---|
| Ataque físico | Physical Attack | quien pega con ataque físico |
| Ataque de energía | Energy Attack | quien pega con ataque de energía |
| Todos los ataques | All Basic Attacks (también la acumulable) | cualquiera |
| Daño de fuego, hielo, eléctrico, veneno, mental | Fire Damage (y Fire Damage by % Fire Resist), Cold, Lightning, Poison, Mind Damage | quien hace daño de ese elemento |
| Daño de todos los elementos | All Element Damage | quien hace daño de algún elemento |
| Ignorar evasión | Ignore Dodge | cualquiera |
| Todas las defensas | All Basic Defenses, Super Armor + All Basic Defenses | cualquiera |
| Vida | HP | cualquiera |
| Quita todos los debuffs | Remove All Debuffs | cualquiera |

«Le sirve» es la misma regla de la sinergia: según el daño de sus skills activas (con qué ataque
escala y qué elementos lleva). Se usa en tres lugares:
- **Ficha**: cada liderazgo y soporte muestra sus categorías; el Resumen dice cuáles le sirven.
- **Roster**: «Su liderazgo da» y «Su soporte da» (dentro de cada grupo, cualquiera de las
  categorías elegidas; entre los dos, ambos), «Liderazgo o soporte solo para» (una clase, bando,
  raza, habilidad o personaje) y «Que le llegue y le sirva a», que se elige desde la ficha del
  personaje: cuenta solo lo que le llega (la restricción del liderazgo o soporte) y le sirve.
  Cada tarjeta dice qué encontró.
- **Combinaciones de 3**: lo que recibe el personaje en cada equipo: los soportes de sus
  compañeros y el liderazgo del líder elegido, también si el líder es él, en cinco grupos
  (ataque, ignorar evasión, defensas, vida, quita debuffs), con * si solo llega con el artefacto
  del compañero.

No cambia los puntos de la sinergia. Lo que no está en ninguna categoría (velocidad, crítico,
daño a héroes o villanos...) sigue a la vista en la ficha, sin categoría.

## Datos del juego (pipeline)
El pipeline corre en GitHub: el workflow **Actualizar datos MFF** (los lunes, o a mano desde
Actions → Run workflow) baja todo de thanosvibs, la wiki y la guía de armado de Cynicalex,
regenera `data.js`, `datos.json`, `docs/AUDITORIA.md`, `docs/CATALOGO.md` y el import, y los
commitea junto con la copia en uso de la guía de armado (ver abajo). La app instalada baja ese
resultado.

A mano (Linux o macOS; en Windows ver Limitaciones):
```
python scripts/fetch_all.py        # datos, tier lists e imágenes (images/ no se versiona)
python scripts/parse_instinto.py
python scripts/build.py            # data.js, datos.json, mff-thanosvibs-import.json, docs/AUDITORIA.md, docs/CATALOGO.md
```
`datos.json` lleva el sha256 y el tamaño de cada archivo que baja la app y la lista de imágenes con
su origen (`scripts/imagenes.py`). `.gitattributes` evita que git cambie los finales de línea de
esos archivos: el hash publicado tiene que ser el de lo que se descarga.

La versión de juego del snapshot sale de `/api/updates` de thanosvibs (la última publicada con
fecha pasada), no de una tier list: las listas se actualizan a su propio ritmo.

### La guía de armado de Cynicalex
La planilla se edita a mano, seguido, y su formato es libre, así que no se lee directo:
`fetch_all.py` baja las dos pestañas como CSV y `scripts/guia_armado.py` decide si se usan. Se
aceptan solo si este lector las entiende:
- la fila de encabezados (la que empieza con «PK») tiene todas las columnas que se usan (se
  ubican por nombre: una columna nueva no rompe nada) y arriba está la versión («V12.2.0»);
- siguen estando, textuales, las líneas de la leyenda cuyo significado usa la app (las siglas de
  cómo se consigue, los códigos de artefacto, la notación de rotaciones, «CTP+ = Reforged
  required», las categorías de ISO-8 y sus sets): si cambian, lo que diría la app podría no ser
  lo que dice la planilla;
- la pestaña TIER LIST tiene la línea de leyenda de los emojis;
- hay al menos 200 filas y se entiende el 80% o más de los nombres (personaje + mejor uniforme,
  contra thanosvibs) y de cada columna que se interpreta (C.T.P., ISO-8, obelisco, artefacto,
  emojis).

Si se acepta, pasa a ser la **copia en uso**, `fuentes/guia-armado/` (versionada; el workflow
semanal la commitea con los datos). Si no se acepta, o no se pudo bajar, la copia en uso queda
como está y `estado.json` anota la fecha y los motivos; la app lo muestra en **Ajustes** y
sigue con la última versión compatible. Un valor suelto que no se entiende (un C.T.P. nuevo, un
emoji sin leyenda) no la rechaza: viaja tal cual, la app lo marca y Ajustes lo lista.

`fuentes.py` lee siempre la copia en uso. La planilla da una fila por personaje, con su mejor
uniforme; los nombres se cruzan con los de thanosvibs fila por fila (un uniforme puede cambiar
el nombre: «Amadeus Cho» con Heroic Age). Las columnas que repiten lo que ya trae thanosvibs
(tier, tipo de ataque, aliados, bando, instinto, opciones de uniforme) no se usan, y «Story
Mode» no tiene leyenda. Las opciones de uniforme salen de thanosvibs, que las da para los 598
uniformes y coincide con la planilla en sus 213 filas.

## Dónde viven los datos
- `data.js` es la **única** fuente de personajes, uniformes, skills, imágenes, tier lists importadas
  y del resto de lo que viene de las fuentes. La app nunca lo copia a la capa: actualizarlo se ve
  al recargar, sin borrar nada.
- `capa.json` (carpeta de datos) guarda **solo la capa del usuario**: personajes propios o
  editados, equipos, favoritos, descartados, tier lists propias, cambios sobre las
  importadas, imágenes subidas, atributos marcados, hojas de ruta, topes cargados y
  preferencias. Se guarda a través del servidor local en cada cambio; si un guardado falla,
  la app lo dice y ofrece reintentar. Un `capa.json` ilegible frena el arranque en vez de
  pisarlo. Se exporta e importa desde **Ajustes**, y las capas viejas (una sola fila por
  entrada, modos de ejemplo) se convierten al cargarlas.
- `scripts/contenido/` — lo curado a mano, cada bloque con su fuente: `guia.json` (armado,
  progresión, topes, ranking de C.T.P., reglas de ISO y urus), `modos.json`, `hallazgos.json`,
  `marcadores.csv` (la facción, el tipo o la raza que la fuente no publica en algunos efectos) y
  `catalogo.json` (el catálogo de efectos del modelo).
- `fuentes/guia-armado/` — la copia en uso de la guía de armado (los dos CSV tal como se bajaron)
  y `estado.json` (versión, cuándo se tomó, la última revisión y, si se rechazó, por qué).

## De dónde salen las skills
De `/api/characters/<retrato>/skills`, que es el modelo de datos del juego. Cada retrato (el base y
el de cada uniforme) tiene su propio set completo: 9.147 skills y ningún personaje sin skills.

Lo que trae:
- Cooldown, y el porcentaje de carga de ult y de striker por skill (y sus totales combinados). La
  fuente pone recarga 1 a la Definitiva de Tier-3 y a la Striker, que se cargan con su barra: la
  app las muestra así ("se carga con la barra") en vez de "CD 1s".
- *Uniform Passive* y *Striker Skill*, que la wiki no publica.
- Etapas: cada skill puede tener varias, cada una con su elemento, su objetivo y su condición de activación.
- Efectos tipados: cada efecto trae `abilityId` + etiqueta de un vocabulario cerrado de 228 valores,
  más duración y tick. El análisis, los roles y los filtros por efecto salen de ahí, no de un regex
  sobre texto libre.
- **A quién le pega cada skill**: 53 grupos de objetivo (todos los aliados, aliados mutantes,
  aliados de tipo Velocidad...). Se muestra como insignia en el encabezado de la skill, se compara
  en la fila «Beneficia a» y se puede filtrar el roster por grupo. Los 33 que son un tipo de
  aliado (clase, bando, raza o habilidad) se tocan y muestran los personajes que lo cumplen, con
  el uniforme que haga falta: `OBJETIVO_GRUPO` en `scripts/dominio.py` dice qué campo define cada
  uno, contrastado con las restricciones de líder y soporte de `/api/supports`.
- Qué controles aplica cada skill para cortar a los jefes de Alliance Battle (`cancels`).
- De `/api/uniforms`, el costo de mejora de cada uniforme.

**Lo que no trae**: la geometría del golpe (cantidad de hits, melee/ranged, área, empuje) y los
atributos de la skill (*Ignore Targeting*, *Ignore All Targeting*, *Guard Break*, *Super Guard
Break*). Por eso **esos cuatro atributos se marcan a mano**: en la ficha, el botón «Marcar
atributos» muestra un checkbox por skill. Las marcas viven en la capa del usuario, indexadas por
retrato y tipo de skill (`thanos7::Active 1`), así que sobreviven a las sincronizaciones.

**Marcadores sin resolver**: algunas descripciones de la fuente traen plantillas como
`$HEROSUBTYPE1` o `$TIME` sin reemplazar. Cuando hay un campo real detrás (`duration`, `tick`) la
app lo usa. La facción, el tipo, la raza o la habilidad (`$HEROSUBTYPE1`, `$HEROCLASS1`: 249
efectos) no vienen en ningún campo, y `scripts/marcadores.py` los completa en el build:
1. **A mano**, en `scripts/contenido/marcadores.csv`: el id del efecto y el valor, como lo muestra
   la app (Superhéroe, Supervillano, Neutral, Combate, Mutante...) o en inglés como lo nombra el
   juego. Gana sobre la wiki. Un valor que no corresponde al efecto (una raza donde el texto
   dice «faction») corta el build con los valores posibles.
2. **De la wiki**: la misma skill (la pasiva de uniforme, en el «Bonus» de ese uniforme) con el
   mismo porcentaje, en el mismo sentido (daño infligido o recibido). Si la skill tiene varios
   efectos así, la wiki tiene que nombrar la misma cantidad de valores; si no, no se usa.

En la ficha, el valor completado va subrayado y el tooltip dice de dónde salió; lo que no se
completó sigue «sin especificar», con la explicación. Hoy: 78 de la wiki y 171 pendientes. La
tabla trae una fila vacía por cada pendiente (personaje, skill y texto) y `docs/AUDITORIA.md`
los lista en su sección 8; `python3 scripts/marcadores.py` agrega a la tabla los que falten.

### Formato en data.js
Los ~41.000 efectos usan solo 299 descripciones distintas. Cada efecto guarda el índice de su
patrón y sus números (`{"a":12,"p":3,"v":[152,1067]}`) y el texto se arma en el navegador desde
`MFF_TABLAS`, en el idioma activo.

## Auditoría entre fuentes
`scripts/auditar.py` corre en cada build y contrasta thanosvibs con la wiki y consigo mismo: % de
daño y recarga de cada skill (contra la sección de su uniforme en la wiki), clase, bando, género,
raza y tipo de ataque del infobox, instinto, valores de los artefactos y coherencia interna (Tier-4
sin Striker, skill 6 sin Definitiva). **No corrige nada**: la app sigue mostrando thanosvibs, y
una diferencia es algo para revisar en el juego (la wiki suele estar vieja), no un error
confirmado. El informe completo queda en `docs/AUDITORIA.md`; cada ficha muestra lo suyo en
«Verificación entre fuentes». Los hallazgos que no se detectan solos están en
`scripts/contenido/hallazgos.json`.

## Idioma
La app tiene un botón **ES / EN** en la barra superior. Cambia la interfaz completa y también
el contenido: efectos y nombres de skill, textos de C.T.P., de la guía, de Alliance Battle, de
soportes, de artefactos y de rotaciones.

Cómo funciona la traducción:
- Skills (`scripts/skills_api.py` con las tablas de `scripts/traducir.py`): cada descripción se
  normaliza reemplazando los números por `#`; ese patrón se busca en
  `scripts/traducciones/efectos.json` (patrón inglés → patrón español) y la app reinyecta los
  números en orden. Una traducción cubre todas las variantes numéricas. Nombres de skill,
  etiquetas, elementos, objetivos y activaciones tienen su propia tabla.
- Resto de las fuentes (`scripts/fuentes.py`): por texto exacto (`ctps`, `abx`, `guia`,
  `soportes`, `rotaciones`, `armado`, `bonos`), y las líneas de artefacto por patrón (`artefactos.json`,
  con `#` por número). Las rotaciones que son solo notación no se traducen.
- Un patrón con otra cantidad de `#` que el original corta el build. Lo que no tiene traducción
  viaja en inglés, la app lo marca y el build lo lista en `work/sin_traducir_*.json`. **Nunca se
  emite una traducción aproximada.**
- El vocabulario de dominio (clases, roles, slots, razas, orígenes, habilidades) viaja en `data.js`
  como `MFF_VOCAB_EN`, generado invirtiendo los mismos mapas de `scripts/dominio.py`.

Cobertura actual, sin nada pendiente: 299 patrones de descripción, 228 etiquetas, 85
activaciones, 53 objetivos, 13 elementos, 5.025 nombres de skill y 1.347 textos de las demás
fuentes (entre ellos 681 descripciones, 70 nombres de rotación y las 41 notas de la guía de
armado).

**Los nombres de personaje, uniforme, C.T.P., artefacto y modo quedan en inglés a propósito**: son
el identificador con el que se cruza la app con el juego, con la wiki y con thanosvibs. Los
rótulos de las filas de las tier lists tampoco se traducen.

## Tier lists
Se importan **todas las listas públicas de thanosvibs** (20 hoy) con **las filas y los rótulos que
les puso su autor**, no convertidas a S–D: muchas filas no son un ranking (`strikers`, `best
support`, una fila por C.T.P.). Se agrupan en *Principales* (las cinco de la guía: General,
Alliance Battle, Arena, World Boss Legend y Soportes), *Comunidad* y *Mías*.

| Lista | Autor | Versión de juego | Ubicados |
|---|---|---|---|
| General | Gummy Steve 2129 | 12.2 | 293 |
| Batalla de Alianza | Shiruishi | 12.1.5 | 68 |
| Arena de Equipos | Shiruishi | 12.2 | 60 |
| World Boss Legend (+) | Shiruishi | 12.1.5 | 136 |
| Soportes | Gummy Steve 2129 | 12.1.5 | 57 |

Son listas de autor, no rankings oficiales del juego. Una entrada puede estar en varias filas de
la misma lista (así las publica la fuente). Las listas propias arrancan de una plantilla (rango
S–D, rango con SS, uso: líder/principal/soporte/striker, una fila por C.T.P., o vacía) y pueden
ser de personajes, de C.T.P., de artefactos o de tus equipos.

## Estructura
- `index.html` / `app.js` / `styles.css` — la app (la página).
- `version.json` — versión de la app, formato de datos que entiende, versión de Python y notas.
- `data.js` / `datos.json` — snapshot generado de los datos y su manifiesto.
- `scripts/` — pipeline: `fetch_all` → `parse_instinto` → `build`, que llama a `skills_api.py`,
  `fuentes.py`, `catalogo.py`, `auditar.py` y `_core.py`. `dominio.py` tiene el vocabulario cerrado del juego,
  `traducir.py` las tablas de las skills, `version_juego.py` la versión del snapshot,
  `guia_armado.py` el lector de la guía de armado (y si se acepta), `marcadores.py` lo que
  completa los marcadores de facción, tipo o raza, `modelo.py` lo que se deduce de cada variante
  (el perfil de combate) y `bonos.py` los bonos de equipo (de la wiki y de lo que se vio en el
  juego).
- `fuentes/guia-armado/` — la copia en uso de la guía de armado y su estado.
- `scripts/traducciones/` — las tablas de traducción, editables a mano.
- `scripts/contenido/` — lo curado a mano, con fuentes.
- `docs/AUDITORIA.md` — el informe de la auditoría entre fuentes (se regenera en cada build).
- `docs/MODELO.md` — el modelo del juego: características de cada variante, reglas y dudas.
- `docs/CATALOGO.md` — el catálogo de efectos entero (se regenera en cada build desde
  `scripts/contenido/catalogo.json`).
- `desktop/` — `lanzador.py` (entrada: instancia única, ventana, apagado, reinicio tras un parche),
  `servidor.py` (sirve la app y la API local), `actualizador.py` (datos, imágenes y parches, todo
  verificado), `construir.py` + `instalador.iss` (lo que publica cada versión) y el ícono.
- `.github/workflows/` — `actualizar.yml` (datos, semanal) y `publicar.yml` (release al etiquetar).
- `MFF.bat` / `MFF.sh` — lanzadores desde el repo.
- `mff-thanosvibs-import.json` — export del estado completo (backup / re-import manual).

## Limitaciones conocidas
- El pipeline de datos no corre en Windows: los scripts leen y escriben texto con la codificación
  del sistema (cp1252) y los datos traen caracteres que no entran (★, ↑). Corre en GitHub (Linux);
  la app instalada ya no lo necesita.
- Probado en Linux y bajo Wine (instalador compilado con Inno Setup, Python embebido de Windows):
  instalación, arranque, carpeta de datos, instancia única, capa, apagado y desinstalación. **No
  probado en un Windows real**: la ventana de Edge en modo app, el cuadro de error y el aviso de
  SmartScreen.
- No hay cantidad de hits ni melee/ranged/área/empuje: la API de skills no lo publica.
- Roles derivados por reglas documentadas (el juego no tiene roles), a partir del análisis de
  cada variante (ver *Modelo del juego*).
- 15 de 290 personajes sin instinto: sus páginas de la wiki no lo declaran.
- Los personajes que agregues a mano no llevan skills: las skills vienen tipadas de la API.
- La sinergia se apoya en los efectos de líder y de soporte de thanosvibs y en los bonos de
  equipo (de la wiki, o del juego si se cargaron): cada bono con todos sus integrantes en el equipo
  suma 1. Roles y ventaja de clase son lecturas propias (la ventaja: Combate > Velocidad >
  Detonación > Combate, y Universal le gana a las tres con ventaja menor, que en la sinergia suma
  igual y se dice). No es un cálculo del juego. Cada efecto cuenta solo para quien le sirve: los
  que suben el ataque físico o el de energía, para quien pega con ese ataque; los de un elemento
  (fuego, frío, rayo, veneno, mente, o todos), para quien hace daño de ese elemento; la reducción
  del reflejo físico, para quien hace daño físico; todo según el daño de sus skills activas. Los
  demás (daño básico, crítico, ignorar evasión, defensas, vida, inmunidades) cuentan para todos,
  también los que dependen de qué debuffs aplica o de si tiene golpes en cadena, que las skills no
  marcan de forma legible. Un efecto nuevo que la app no conoce cuenta para todos y la sinergia lo
  dice. Cada efecto vale lo mismo, sin importar cuánto sube.
- Los bonos de equipo de la wiki están redondeados a un decimal y sus páginas no siempre
  coinciden: vale lo que dice la mayoría y, si empatan, la app muestra las dos versiones
  (`docs/AUDITORIA.md`, sección 10). Faltan los de los personajes que la wiki todavía no tiene,
  salvo los que se cargaron del juego (`scripts/contenido/bonos.json`), y el de llevar tres de 6★.
- La cobertura de las combinaciones cuenta el liderazgo del líder también para el líder mismo:
  no hay una fuente a mano que diga si el juego se lo aplica (se ve en el juego, con el
  personaje de líder y sus stats en el equipo).
- Los números reflejan lo que publica thanosvibs, que puede atrasarse respecto de un rebalanceo.
- La guía curada está escrita sobre la versión 12.1.5 de la Beginner's Guide: si thanosvibs
  publica otra, el build avisa y la sección Modos lo muestra.
- La traducción es propia, no oficial: MFF no tiene cliente en español, así que no hay término
  establecido contra el cual contrastarla. El original en inglés siempre queda a la vista.
