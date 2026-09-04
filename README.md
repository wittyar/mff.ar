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
- `scripts/` — pipeline de regeneración (`fetch_all` → `parse_skills` → `build`; `_core.py` es el transformador común).
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
- La fuente ubica tres entradas en dos filas a la vez; `build.py` avisa y se queda con la primera.
