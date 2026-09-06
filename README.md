# TA GUIANAEL MFF

App standalone (HTML/JS sin dependencias, sin build) para consultar y comparar personajes de
MARVEL Future Fight, armar equipos y trabajar sobre tier lists. 290 personajes, 596 uniformes,
~3.000 skills con efectos estructurados por objetivo. **Material de consulta de uso interno/personal,
sin fin comercial.**

**Fuentes de datos** (crédito correspondiente):
- [THANO$VIB$](https://thanosvibs.money) — personajes, uniformes, **skills**, costos de mejora,
  retratos, íconos y cinco tier lists.
- [Future Fight Wiki (Fandom)](https://future-fight.fandom.com) — solo el instinto, que thanosvibs
  no publica en ninguna de sus APIs.

## App de escritorio (Windows)
`MFF.bat` levanta un servidor local en 127.0.0.1 y abre la app en el navegador por defecto.
Sirve para tener **botones de sincronización dentro de Ajustes**: la API de thanosvibs no manda
`Access-Control-Allow-Origin`, así que el navegador no puede bajar los datos por su cuenta — hace
falta un proceso afuera del sandbox, y ese proceso es `desktop/servidor.py`.

Tres botones, cada uno actualiza solo lo suyo y muestra el progreso en vivo:
- **Datos del juego** — `fetch_all --datos` + `parse_instinto` + `build`. Regenera `data.js`.
- **Tier lists** — `fetch_all --tierlists` + `build`. Rápido. Necesita que ya se hayan bajado los
  datos alguna vez (el botón se deshabilita solo y lo explica si no).
- **Retratos** — `fetch_all --imagenes`. Solo baja los PNG que falten.

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
el paquete sale en 25 MB y los retratos se bajan después desde Ajustes; con imágenes son ~81 MB.

Se eligió el Python embebido y no un `.exe` de PyInstaller a propósito: un ejecutable sin firmar
dispara el aviso de SmartScreen y es un falso positivo habitual de varios antivirus. El `.bat`, en
cambio, no dispara nada.

**Sin verificar**: el paquete se probó entero en Linux (servidor, endpoints, botones, regeneración
de `data.js`, arranque desde la carpeta armada). Lo que **no** se pudo probar desde acá es el
`python\python.exe` embebido corriendo en Windows real.

## Uso
Las **imágenes no están en el repo** (59 MB de PNGs de terceros, gitignoreadas). Tras clonar:
```
python scripts/fetch_all.py    # baja datos + imágenes a images/
```
y abrir `index.html`. Si ya tenés la carpeta `images/` de una copia anterior, alcanza con copiarla al lado del HTML.

## Actualizar datos (cuando el juego cambia de versión)
Local:
```
python scripts/fetch_all.py
python scripts/parse_instinto.py
python scripts/build.py        # regenera data.js y mff-thanosvibs-import.json
```
O desde GitHub: pestaña **Actions → "Actualizar datos MFF" → Run workflow** (regenera y commitea
`data.js` si cambió; las imágenes nuevas se bajan localmente con `fetch_all.py`).

## Dónde viven los datos
- `data.js` es la **única** fuente de personajes, uniformes, skills, imágenes y tier lists importadas.
  La app nunca lo copia a `localStorage`: regenerarlo se ve al recargar, sin borrar nada.
- `localStorage` guarda **solo la capa del usuario** (clave `mff_user_v1`): personajes propios o
  editados, equipos, tier lists propias, cambios sobre las importadas, imágenes subidas y preferencias.
  Se exporta e importa desde **Ajustes**.

## De dónde salen las skills
De `/api/characters/<retrato>/skills`, que es el modelo de datos del juego. Cada retrato (el base y
el de cada uniforme) tiene su propio set completo. Por eso hay **9.125 skills** y no las 3.008 que
salían de parsear la wiki, y no queda ningún personaje sin skills.

Lo que trae y antes no había:
- Cooldown, y el porcentaje de carga de ult y de striker por skill (y sus totales combinados).
- *Uniform Passive* y *Striker Skill*, que la wiki no publica.
- Etapas: cada skill puede tener varias, cada una con su elemento, su objetivo y su condición de activación.
- Efectos tipados: cada efecto trae `abilityId` + etiqueta de un vocabulario cerrado de 228 valores,
  más duración y tick. Los roles y los filtros por efecto salen de ahí, no de un regex sobre texto libre.
- **A quién le pega cada skill**: 1.188 de las 9.125 skills declaran un objetivo que no es uno mismo
  (los 886 liderazgos más 302 pasivas y activas), sobre 53 grupos: todos los aliados, aliados mutantes,
  aliados de tipo Velocidad, aliados con Sentido Arácnido, etc. Se muestra como insignia en el
  encabezado de la skill, se compara en la fila «Beneficia a» y se puede filtrar el roster por grupo.
  Tres valores de la fuente traen la condición de activación metida adentro del objetivo con un `\n`
  literal; se muestra como separador.
- De `/api/uniforms`, el costo de mejora de cada uniforme: cristales, oro, kits, XP y materiales por nivel.

**Lo que se perdió al cambiar de fuente**: la geometría del golpe (cantidad de hits, melee/ranged,
área, empuje) y los atributos de la skill (*Ignore Targeting*, *Ignore All Targeting*, *Guard Break*,
*Super Guard Break*). Eso solo estaba en la wiki. Verificado sobre el texto crudo de las 886
respuestas: la API menciona `Ignore Targeting` 24 veces, todas dentro de la descripción de la skill
*Guaranteed Targeting* (que apunta a enemigos que lo tienen), y `Guard Break` 94, todas de la
etiqueta `GUARD BREAK IMMUNE`, que es un buff distinto. El atributo de la skill no está en ningún
campo.

Por eso **esos cuatro atributos se marcan a mano**: en la ficha, el botón «Marcar atributos» muestra
un checkbox por skill. Las marcas viven en la capa del usuario, indexadas por retrato y tipo de
skill (`thanos7::Active 1`), así que sobreviven a las sincronizaciones; se ven como insignia en la
ficha y en la comparativa, suman la fila «Atributos marcados» y se puede filtrar el roster por ellas.
Cruzar la wiki para precargarlas cubriría solo el 11% de las 9.125 skills (medido), y una skill sin
insignia pasaría a significar dos cosas distintas, así que no se hace.

**Marcadores sin resolver**: 269 descripciones de la fuente traen plantillas como `$HEROSUBTYPE1` o
`$TIME` sin reemplazar (a veces incluso duplicadas, como en la pasiva T2 de Abomination). Cuando hay
un campo real detrás (`duration`, `tick`) la app lo usa; cuando no, muestra «sin especificar» con la
explicación en el tooltip, en vez de inventar un valor o dejar el marcador crudo.

### Formato en data.js
Los 41.152 efectos usan solo 299 descripciones distintas. Guardar el texto en cada efecto, y encima
en dos idiomas, daba 11 MB. En vez de eso cada efecto guarda el índice de su patrón y sus números
(`{"a":12,"p":3,"v":[152,1067]}`) y el texto se arma en el navegador desde `MFF_TABLAS`, en el
idioma activo. Con eso `data.js` queda en 3,4 MB llevando el triple de contenido que antes.

## Idioma
La app tiene un botón **ES / EN** en la barra superior. Cambia la interfaz completa y también
el contenido: los efectos de las skills y los nombres de skill están traducidos al español, con
el nombre original en inglés siempre a la vista al lado.

Cómo funciona la traducción:
- `scripts/parse_skills.py` **no traduce**: decide la estructura de cada skill (qué línea le pega a
  quién) y guarda el inglés de la wiki tal cual, en `fx`.
- `scripts/traducir.py` aplica la traducción y produce `fxEs`. Cada línea se normaliza reemplazando
  los números por `#`; ese patrón se busca en `scripts/traducciones/efectos.json`, que mapea patrón
  inglés → patrón español, y los números se reinyectan en orden. Una traducción cubre así todas las
  variantes numéricas, incluidas las de futuras versiones del juego.
- `scripts/traducciones/skills.json` traduce los nombres de skill.
- Si aparece un patrón sin traducción cargada, `traducir_linea` devuelve `None`, el build lo reporta
  y lo lista en `work/sin_traducir.json`, y la app muestra esa línea en inglés y marcada. **Nunca se
  emite una traducción aproximada.**
- El vocabulario de dominio (clases, roles, slots, etiquetas, razas, orígenes) viaja en `data.js`
  como `MFF_VOCAB_EN`, generado por `_core.py` invirtiendo los mismos mapas con los que se tradujo.

Cobertura actual, con el build fallando en voz alta si aparece algo nuevo sin traducir:
299 patrones de descripción, 228 etiquetas de efecto, 85 activaciones, 53 objetivos, 13 elementos y
5.008 nombres de skill. Cero sin traducir.

**Los nombres de personaje y de uniforme quedan en inglés a propósito**: son el identificador con el
que se cruza la app con el juego, con la wiki y con thanosvibs. Los rótulos de las filas de las tier
lists tampoco se traducen, por la misma razón que se conservan tal cual (ver abajo).

## Tier lists
Se importan cinco listas de thanosvibs con **las filas y los rótulos que les puso su autor**, no
convertidas a S–D: en la general las filas son `Meta / niche meta / T4 s / T4 a / T4 b / T3tp A /
t3tp b / Poo`, y en Alliance Battle `strikers` y `best support` son filas propias, no un ranking.
Aplastarlas a S–D renombraba un striker top como "D". Las listas que crees dentro de la app sí
arrancan con S/A/B/C/D.

| Lista | Autor | Versión de juego | Ubicados |
|---|---|---|---|
| General | Gummy Steve 2129 | 12.2 | 293 |
| Batalla de Alianza | Shiruishi | 12.1.5 | 68 |
| Arena de Equipos | Shiruishi | 12.1.5 | 70 |
| World Boss Legend (+) | Shiruishi | 12.1.5 | 136 |
| Soportes | Gummy Steve 2129 | 12.1.5 | 57 |

Son listas de autor publicadas en thanosvibs, no rankings oficiales del juego; las cuatro de modo
van una versión atrás de la general.

## Estructura
- `index.html` / `app.js` / `styles.css` — la app (roster, ficha, comparación, tier lists, equipos, editor).
- `data.js` — snapshot generado de los datos (autosuficiente; la app no necesita importar nada).
- `scripts/` — pipeline de regeneración (`fetch_all` → `parse_instinto` → `build`, que llama a
  `skills_api.py` y `_core.py`; `traducir.py` es la capa de traducción).
- `scripts/traducciones/` — las tablas de traducción (`efectos.json`, `skills.json`), editables a mano.
- `desktop/` — servidor local (`servidor.py`) y armador del paquete (`preparar_paquete.py`).
- `MFF.bat` / `MFF.sh` — lanzadores.
- `mff-thanosvibs-import.json` — export del estado completo (backup / re-import manual).

## Limitaciones conocidas
- No hay cantidad de hits ni melee/ranged/área/empuje: la API de skills no lo publica y la wiki
  dejó de ser fuente de skills.
- Roles derivados por reglas documentadas (el juego no tiene roles); ahora salen de las etiquetas
  tipadas de la API en vez de un regex sobre texto libre.
- 61 de 290 personajes sin instinto: sus páginas de la wiki no lo declaran.
- Los personajes que agregues a mano no llevan skills: las skills vienen tipadas de la API.
- La sinergia de equipos es una heurística propia (bando, cobertura de roles, ventaja de clase),
  no un cálculo del juego.
- Los números reflejan lo que publica thanosvibs, que puede atrasarse respecto de un rebalanceo.
- La traducción es propia, no oficial: MFF no tiene cliente en español, así que no hay término
  establecido contra el cual contrastarla. El original en inglés siempre queda a la vista.
- La fuente ubica tres entradas en dos filas a la vez; `build.py` avisa y se queda con la primera.
