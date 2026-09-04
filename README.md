# TA GUIANAEL MFF

App standalone (HTML/JS sin dependencias, sin build) para consultar y comparar personajes de
MARVEL Future Fight, armar equipos y trabajar sobre tier lists. 290 personajes, 596 uniformes,
~3.000 skills con efectos estructurados por objetivo. **Material de consulta de uso interno/personal,
sin fin comercial.**

**Fuentes de datos** (crédito correspondiente):
- [THANO$VIB$](https://thanosvibs.money) — personajes, uniformes, retratos, íconos y cinco tier lists.
- [Future Fight Wiki (Fandom)](https://future-fight.fandom.com) — skills e instintos.

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
python scripts/parse_skills.py
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

Cobertura actual: 13.151 de 13.151 líneas de efecto y 2.651 de 2.651 nombres de skill.

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
- `scripts/` — pipeline de regeneración (`fetch_all` → `parse_skills` → `build`; `_core.py` es el transformador común, `traducir.py` la capa de traducción).
- `scripts/traducciones/` — las tablas de traducción (`efectos.json`, `skills.json`), editables a mano.
- `mff-thanosvibs-import.json` — export del estado completo (backup / re-import manual).

## Limitaciones conocidas
- 35 personajes sin skills: sus páginas de la wiki son stubs (personajes recientes en su mayoría).
- 3 grupos de skills por uniforme quedan afuera porque la wiki los rotula distinto que THANO$VIB$
  (Groot «GotG 2», Squirrel Girl «Nutty Tyrant», Shuri «Wakanda Forever (Black Panther)»);
  `build.py` los avisa por consola en cada corrida.
- Roles derivados por reglas documentadas (el juego no tiene roles).
- La sinergia de equipos es una heurística propia (bando, cobertura de roles, ventaja de clase),
  no un cálculo del juego.
- Los números de skills reflejan la wiki, que puede atrasarse respecto de rebalanceos del juego.
- La traducción es propia, no oficial: MFF no tiene cliente en español, así que no hay término
  establecido contra el cual contrastarla. El original en inglés siempre queda a la vista.
- La fuente ubica tres entradas en dos filas a la vez; `build.py` avisa y se queda con la primera.
