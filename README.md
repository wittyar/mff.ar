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
- De `/api/uniforms`, el costo de mejora de cada uniforme: cristales, oro, kits, XP y materiales por nivel.

**Lo que se perdió al cambiar de fuente**: la geometría del golpe (cantidad de hits, melee/ranged,
área, empuje). Eso solo estaba en la wiki y la API de thanosvibs no lo publica.

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
