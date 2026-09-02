# Comparador MFF

App standalone (HTML/JS sin dependencias) para comparar personajes de MARVEL Future Fight,
armar equipos y crear tier lists. 288 personajes, 594 uniformes, ~2.900 skills con efectos
estructurados por objetivo. **Material de consulta de uso interno/personal, sin fin comercial.**

**Fuentes de datos** (crédito correspondiente):
- [THANO$VIB$](https://thanosvibs.money) — personajes, uniformes, retratos, íconos y tier list general.
- [Future Fight Wiki (Fandom)](https://future-fight.fandom.com) — skills e instintos.

## Uso
Las **imágenes no están en el repo** (58 MB de PNGs de terceros, gitignoreadas). Tras clonar:
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

## Estructura
- `index.html` / `app.js` / `styles.css` — la app (roster, comparación, equipos, tier lists).
- `data.js` — snapshot generado de los datos (autosuficiente; la app no necesita importar nada).
- `scripts/` — pipeline de regeneración (`fetch_all` → `parse_skills` → `build`; `_core.py` es el transformador común).
- `mff-thanosvibs-import.json` — export del estado completo (backup / re-import manual desde Ajustes).

## Limitaciones conocidas
- 33 personajes sin skills: sus páginas de la wiki son stubs (personajes recientes en su mayoría).
- Roles derivados por reglas documentadas (el juego no tiene roles); `modes` sin fuente real.
- Tier list de THANO$VIB$ aplastada de sus 8 niveles a los rangos S–D de la app.
- Los números de skills reflejan la wiki, que puede atrasarse respecto a rebalanceos del juego.
