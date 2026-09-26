# TA GUIANAEL MFF

App de escritorio para Windows (HTML/JS sin dependencias ni build, servida por un proceso Python
local) para consultar y comparar personajes de MARVEL Future Fight, ver para qué se usa cada uno y
cómo armarlo, armar equipos y trabajar sobre tier lists. 290 personajes, 598 uniformes, 9.147 skills con efectos estructurados por objetivo.
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
  (hace falta actualizar la app).
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
`data.js` cambia de una forma que una versión anterior de la app no entiende.

## Datos del juego (pipeline)
El pipeline corre en GitHub: el workflow **Actualizar datos MFF** (los lunes, o a mano desde
Actions → Run workflow) baja todo de thanosvibs y la wiki, regenera `data.js`, `datos.json`,
`docs/AUDITORIA.md` y el import, y los commitea. La app instalada baja ese resultado.

A mano (Linux o macOS; en Windows ver Limitaciones):
```
python scripts/fetch_all.py        # datos, tier lists e imágenes (images/ no se versiona)
python scripts/parse_instinto.py
python scripts/build.py            # data.js, datos.json, mff-thanosvibs-import.json, docs/AUDITORIA.md
```
`datos.json` lleva el sha256 y el tamaño de cada archivo que baja la app y la lista de imágenes con
su origen (`scripts/imagenes.py`). `.gitattributes` evita que git cambie los finales de línea de
esos archivos: el hash publicado tiene que ser el de lo que se descarga.

La versión de juego del snapshot sale de `/api/updates` de thanosvibs (la última publicada con
fecha pasada), no de una tier list: las listas se actualizan a su propio ritmo.

## Dónde viven los datos
- `data.js` es la **única** fuente de personajes, uniformes, skills, imágenes, tier lists importadas
  y del resto de lo que viene de las fuentes. La app nunca lo copia a la capa: actualizarlo se ve
  al recargar, sin borrar nada.
- `capa.json` (carpeta de datos) guarda **solo la capa del usuario**: personajes propios o
  editados, equipos, tier lists propias, cambios sobre las importadas, imágenes subidas, atributos
  marcados, hojas de ruta, topes cargados y preferencias. Se guarda a través del servidor local
  en cada cambio; si un guardado falla, la app lo dice y ofrece reintentar. Un `capa.json`
  ilegible frena el arranque en vez de pisarlo. Se exporta e importa desde **Ajustes**, y las
  capas viejas (una sola fila por entrada, modos de ejemplo) se convierten al cargarlas.
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
- `index.html` / `app.js` / `styles.css` — la app (la página).
- `version.json` — versión de la app, formato de datos que entiende, versión de Python y notas.
- `data.js` / `datos.json` — snapshot generado de los datos y su manifiesto.
- `scripts/` — pipeline: `fetch_all` → `parse_instinto` → `build`, que llama a `skills_api.py`,
  `fuentes.py`, `auditar.py` y `_core.py`. `dominio.py` tiene el vocabulario cerrado del juego,
  `traducir.py` las tablas de las skills y `version_juego.py` la versión del snapshot.
- `scripts/traducciones/` — las tablas de traducción, editables a mano.
- `scripts/contenido/` — lo curado a mano, con fuentes.
- `docs/AUDITORIA.md` — el informe de la auditoría entre fuentes (se regenera en cada build).
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
