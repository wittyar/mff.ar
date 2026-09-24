# TA GUIANAEL MFF

App standalone (HTML/JS sin dependencias, sin build) para consultar y comparar personajes de
MARVEL Future Fight, ver para qué se usa cada uno y cómo armarlo, armar equipos y trabajar sobre
tier lists. 290 personajes, 598 uniformes, 9.147 skills con efectos estructurados por objetivo.
**Material de consulta de uso interno/personal, sin fin comercial.**

**Fuentes de datos** (crédito correspondiente):
- [THANO$VIB$](https://thanosvibs.money) — personajes, uniformes, **skills**, costos de mejora,
  tier lists públicas, C.T.P., artefactos, efectos de líder y de soporte, rotaciones, Alliance
  Battle (restricciones y equipos), la Beginner's Guide, retratos e íconos.
- [Future Fight Wiki (Fandom)](https://future-fight.fandom.com) — el instinto (thanosvibs no lo
  publica), los requisitos de Tier-3/Trascendencia/Tier-4, las reglas de ISO, urus y gear, y el
  contraste de `docs/AUDITORIA.md`.

## Qué hay en la app
- **Roster** con filtros (clase, rol, tier, bando, instinto, raza, habilidad, efecto, objetivo,
  atributos marcados) y orden por la tier list que elijas.
- **Ficha** de cada personaje y uniforme:
  - *Para qué se usa*: su fila en cada tier list, lo que le da al equipo (liderazgo, pasivas,
    efecto de uniforme y artefacto, con a quién se aplican), dónde lo recomienda la guía, en qué
    equipos de Alliance Battle aparece y qué controles aplica para cortar a los jefes, y la
    verificación entre fuentes.
  - *Cómo armarlo*: su C.T.P. (Ideal CTP List y guía), su artefacto con los valores por nivel de
    estrellas, ISO y urus según su tipo de ataque (derivado de sus skills), la hoja de ruta de
    progresión y la calculadora de topes de stats.
  - Skills por uniforme, con tabla de daño por etapa, y las **rotaciones** de thanosvibs con la
    leyenda de la notación.
- **Comparar** hasta 4 variantes lado a lado, con la sinergia estimada.
- **Tier lists**: todas las listas públicas de thanosvibs, con sus filas originales; listas
  propias de personajes, de C.T.P., de artefactos o de tus equipos, con filas a medida. Una entrada
  puede estar en varias filas de la misma lista.
- **Modos**: los 14 modos que la guía marca como importantes, con qué dan, cómo armar el equipo,
  personajes y C.T.P. recomendados, y el armado general (ISO, urus, 4.º gear, opciones de
  uniforme, obelisco) para PvE y PvP.
- **Equipos** con el modo y su tamaño de equipo según la fuente.

Todo lo que viene de una fuente la cita; lo derivado se dice derivado; lo que falta en la fuente
se marca como faltante en vez de inventarse.

## App de escritorio (Windows)
`MFF.bat` levanta un servidor local en 127.0.0.1 y abre la app en el navegador por defecto.
Sirve para tener **botones de sincronización dentro de Ajustes**: la API de thanosvibs no manda
`Access-Control-Allow-Origin`, así que el navegador no puede bajar los datos por su cuenta — hace
falta un proceso afuera del sandbox, y ese proceso es `desktop/servidor.py`.

Tres botones, cada uno actualiza solo lo suyo y muestra el progreso en vivo:
- **Datos del juego** — `fetch_all --datos` + `parse_instinto` + `build`. Regenera `data.js` y
  `docs/AUDITORIA.md`.
- **Tier lists** — `fetch_all --tierlists` + `build`. Rápido. Necesita que ya se hayan bajado los
  datos alguna vez (el botón se deshabilita solo y lo explica si no).
- **Retratos** — `fetch_all --imagenes`. Baja los PNG de retratos, C.T.P. y artefactos que falten.

Al terminar, la página se recarga sola y vuelve a Ajustes. Al abrir, la app compara la versión de
juego de `data.js` contra la que publica thanosvibs y avisa si hay una más nueva.

Si abrís el HTML suelto (sin `MFF.bat`), la sección de Ajustes explica por qué no hay sincronización
en vez de mostrar botones rotos.

### Pasarle la app a otra persona
```
python desktop/preparar_paquete.py
```
Deja `dist/TA-GUIANAEL-MFF/` con la app, el pipeline, el lanzador y **un Python embebido de
python.org adentro** (un ZIP sin instalador: no pide admin, no toca el PATH ni el registro).
Quien lo recibe descomprime y hace doble clic en `MFF.bat`, sin instalar nada. Con `--sin-imagenes`
el paquete sale más liviano y los retratos se bajan después desde Ajustes.

Se eligió el Python embebido y no un `.exe` de PyInstaller a propósito: un ejecutable sin firmar
dispara el aviso de SmartScreen y es un falso positivo habitual de varios antivirus. El `.bat`, en
cambio, no dispara nada.

**Sin verificar**: el paquete se probó entero en Linux (servidor, endpoints, botones, regeneración
de `data.js`, arranque desde la carpeta armada). Lo que **no** se pudo probar desde acá es el
`python\python.exe` embebido corriendo en Windows real.

## Uso
Las **imágenes no están en el repo** (PNGs de terceros, gitignoreados). Tras clonar:
```
python scripts/fetch_all.py    # baja datos + imágenes a images/
```
y abrir `index.html`. Si ya tenés la carpeta `images/` de una copia anterior, alcanza con copiarla al lado del HTML.

## Actualizar datos (cuando el juego cambia de versión)
Local:
```
python scripts/fetch_all.py
python scripts/parse_instinto.py
python scripts/build.py        # regenera data.js, mff-thanosvibs-import.json y docs/AUDITORIA.md
```
O desde GitHub: pestaña **Actions → "Actualizar datos MFF" → Run workflow** (regenera y commitea
`data.js` y el informe si cambiaron; las imágenes nuevas se bajan localmente con `fetch_all.py`).

La versión de juego del snapshot sale de `/api/updates` de thanosvibs (la última publicada con
fecha pasada), no de una tier list: las listas se actualizan a su propio ritmo.

## Dónde viven los datos
- `data.js` es la **única** fuente de personajes, uniformes, skills, imágenes, tier lists importadas
  y del resto de lo que viene de las fuentes. La app nunca lo copia a `localStorage`: regenerarlo se
  ve al recargar, sin borrar nada.
- `localStorage` guarda **solo la capa del usuario** (clave `mff_user_v1`): personajes propios o
  editados, equipos, tier lists propias, cambios sobre las importadas, imágenes subidas, atributos
  marcados, hojas de ruta, topes cargados y preferencias. Se exporta e importa desde **Ajustes**.
  Las capas viejas (una sola fila por entrada, modos de ejemplo) se migran solas al abrir.
- `scripts/contenido/` — lo curado a mano, cada bloque con su fuente: `guia.json` (armado,
  progresión, topes, ranking de C.T.P., reglas de ISO y urus), `modos.json` y `hallazgos.json`.

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
  más duración y tick. Los roles y los filtros por efecto salen de ahí, no de un regex sobre texto libre.
- **A quién le pega cada skill**: 53 grupos de objetivo (todos los aliados, aliados mutantes,
  aliados de tipo Velocidad...). Se muestra como insignia en el encabezado de la skill, se compara
  en la fila «Beneficia a» y se puede filtrar el roster por grupo.
- Qué controles aplica cada skill para cortar a los jefes de Alliance Battle (`cancels`).
- De `/api/uniforms`, el costo de mejora de cada uniforme.

**Lo que no trae**: la geometría del golpe (cantidad de hits, melee/ranged, área, empuje) y los
atributos de la skill (*Ignore Targeting*, *Ignore All Targeting*, *Guard Break*, *Super Guard
Break*). Por eso **esos cuatro atributos se marcan a mano**: en la ficha, el botón «Marcar
atributos» muestra un checkbox por skill. Las marcas viven en la capa del usuario, indexadas por
retrato y tipo de skill (`thanos7::Active 1`), así que sobreviven a las sincronizaciones.

**Marcadores sin resolver**: algunas descripciones de la fuente traen plantillas como
`$HEROSUBTYPE1` o `$TIME` sin reemplazar. Cuando hay un campo real detrás (`duration`, `tick`) la
app lo usa; cuando no, muestra «sin especificar» con la explicación en el tooltip.

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
  `soportes`, `rotaciones`), y las líneas de artefacto por patrón (`artefactos.json`, con `#` por
  número). Las rotaciones que son solo notación no se traducen.
- Un patrón con otra cantidad de `#` que el original corta el build. Lo que no tiene traducción
  viaja en inglés, la app lo marca y el build lo lista en `work/sin_traducir_*.json`. **Nunca se
  emite una traducción aproximada.**
- El vocabulario de dominio (clases, roles, slots, razas, orígenes, habilidades) viaja en `data.js`
  como `MFF_VOCAB_EN`, generado invirtiendo los mismos mapas de `scripts/dominio.py`.

Cobertura actual, sin nada pendiente: 299 patrones de descripción, 228 etiquetas, 85
activaciones, 53 objetivos, 13 elementos, 5.025 nombres de skill y 1.260 textos de las demás
fuentes (entre ellos 681 descripciones y 70 nombres de rotación).

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
- `index.html` / `app.js` / `styles.css` — la app.
- `data.js` — snapshot generado de los datos (autosuficiente; la app no necesita importar nada).
- `scripts/` — pipeline: `fetch_all` → `parse_instinto` → `build`, que llama a `skills_api.py`,
  `fuentes.py`, `auditar.py` y `_core.py`. `dominio.py` tiene el vocabulario cerrado del juego,
  `traducir.py` las tablas de las skills y `version_juego.py` la versión del snapshot.
- `scripts/traducciones/` — las tablas de traducción, editables a mano.
- `scripts/contenido/` — lo curado a mano, con fuentes.
- `docs/AUDITORIA.md` — el informe de la auditoría entre fuentes (se regenera en cada build).
- `desktop/` — servidor local (`servidor.py`) y armador del paquete (`preparar_paquete.py`).
- `MFF.bat` / `MFF.sh` — lanzadores.
- `mff-thanosvibs-import.json` — export del estado completo (backup / re-import manual).

## Limitaciones conocidas
- No hay cantidad de hits ni melee/ranged/área/empuje: la API de skills no lo publica.
- Roles derivados por reglas documentadas (el juego no tiene roles), a partir de las etiquetas
  tipadas de la API.
- 15 de 290 personajes sin instinto: sus páginas de la wiki no lo declaran.
- Los personajes que agregues a mano no llevan skills: las skills vienen tipadas de la API.
- La sinergia se apoya en los efectos de líder y de soporte de thanosvibs; roles y ventaja de
  clase son lecturas propias. No es un cálculo del juego.
- Los números reflejan lo que publica thanosvibs, que puede atrasarse respecto de un rebalanceo.
- La guía curada está escrita sobre la versión 12.1.5 de la Beginner's Guide: si thanosvibs
  publica otra, el build avisa y la sección Modos lo muestra.
- La traducción es propia, no oficial: MFF no tiene cliente en español, así que no hay término
  establecido contra el cual contrastarla. El original en inglés siempre queda a la vista.
