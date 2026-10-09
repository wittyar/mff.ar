# Transcribir capturas de MARVEL Future Fight en coreano (álbum 2)

Ezequiel sacó 386 capturas del juego en coreano (2712x1220, Android, 4 de octubre de 2026, de 19:33 a
19:52). Son fuente primaria para el comparador mff.ar. Tu carril transcribe un rango de capturas,
literal, a un archivo. No interpretás ni traducís: eso lo hace después quien integra.

Carpeta: `/tmp/claude-0/-home-claude/edce997e-7225-50a2-90b7-128832dd7122/scratchpad/ko3` (abajo, `$K`).

- `$K/indice.json`: una fila por captura, en el orden en que se sacaron: `n` (1 a 386), `f` (archivo,
  relativo a `$K`) y `cap` (hora de captura).
- `$K/hojas/hNN.jpg`: hojas de miniaturas numeradas, 24 por hoja (h01 = 1 a 24, h02 = 25 a 48...). Sirven
  para ver de un vistazo qué hay en tu rango; no se leen.
- `$K/recortar.py`: `python3 $K/recortar.py N PRESET [ZOOM]` o `python3 $K/recortar.py N x0,y0,x1,y1 [ZOOM]`
  deja un recorte en `$K/recortes/` e imprime su ruta; leelo con Read. Presets: `entera`, `guia` (lista de
  la izquierda + panel), `panel` (solo el panel de la derecha), `lista`, `popup` (ventana centrada),
  `striker` (mitad derecha de la ficha de personaje), `bonos`. La primera vez que aparece un tipo de
  pantalla nuevo, mirá la captura `entera` una vez y elegí el recorte que tenga todo el texto. Si algo se
  lee chico, recortá más ajustado y ampliá (ZOOM 1.5 o 2) antes de darlo por ilegible.

## Qué hay en el álbum

Por las miniaturas, tres bloques (los límites exactos no se conocen):
- **Guía del juego** (가이드, botón 가이드 홈): un dibujo arriba y un texto que explica un sistema (호출,
  상성 효과, 유니폼, 팀 효과, 전성, 진영, 장비 강화, ISO-8, 코믹스 카드, 아티팩트, 소드, 특수 장비, C.T.P. 재련, 우루,
  J.A.R.V.I.S.…). Lista a la izquierda con el ítem elegido resaltado.
- **Diccionario de términos** (…어 사전): lista de términos a la izquierda, algunos con una pastilla naranja
  (전투 가이드), y el texto del término en el panel. Botones 전투 가이드 y 가이드 홈.
- **Ficha de un personaje** (영웅 정보), Mephisto (메피스토): ventanas de skills, tipo, ISO-8, artefacto,
  equipo especial (C.T.P., con 적용 콘텐츠 PVP / PVE), uniforme, opciones de uniforme (유니폼 옵션),
  pestaña de strikers (스트라이커, solo retratos) y otras.

## Qué escribir

Un archivo `$K/salida/<carril>.jsonl`: un objeto JSON por renglón, uno por captura, en orden de `n`.
**Escribí (append) el renglón apenas terminás cada captura**, no al final: si el contexto pierde imágenes
viejas, lo escrito queda. Lo más seguro: un script chico que reciba el objeto en un heredoc con comillas
simples y haga `json.dumps(..., ensure_ascii=False)`.

Campos de cada renglón:

```
{
  "n": 131, "archivo": "img/131.jpg",
  "pantalla": "용어 사전",                   // título arriba a la izquierda, tal cual se ve (puede estar cortado: lo visible)
  "tipo": "guia | glosario | personaje | ctp | striker | equipo | bonos | otro",
  "lista": ["매혹", "타겟팅 무시", ...],       // ítems visibles en la lista de la izquierda, en orden (null si no hay)
  "seleccionado": "정신 지배",                // el ítem resaltado de la lista
  "insignias": {"타겟팅 무시": "전투 가이드"},  // pastillas junto a ítems de la lista
  "titulo": "정신 지배",                      // título del panel o de la ventana
  "texto": "정신 지배 능력은 …\n정신 지배에 걸린 적은 …\n\nTip: …",  // literal; \n entre renglones de párrafo distintos y \n\n entre párrafos
  "resaltados": [{"texto": "정신 지배", "color": "naranja", "subrayado": false}],
  "botones": ["가이드 홈"],
  "datos": {},                               // campos propios del tipo, abajo
  "legibilidad": "completa | parcial",
  "dudas": ""                                // qué no se pudo leer y por qué
}
```

Un párrafo que el juego corta en dos renglones solo por el ancho va en un solo renglón (sin \n); \n solo
donde el texto empieza un renglón nuevo a propósito (frase nueva alineada a la izquierda, viñeta, «Tip:»,
«▶»). Si la misma pantalla aparece dos veces seguidas sin cambios (captura repetida), igual va su renglón,
con `"dudas": "igual a la n anterior"` y el texto completo.

`datos` según el tipo:

- `guia`: `{"rotulos": ["생체 데이터", "영웅 획득"]}`: los rótulos bajo los dibujos de arriba, en orden.
- `personaje`: `{"personaje": "메피스토", "uniforme": "…", "pestana": "스킬 | 타입 | ISO-8 | 아티팩트 | 특수 장비 | 유니폼 | 기본 정보 | 유니폼 효과 | 변경 스킬 | 능력치 | 소개 | 스트라이커 | …", "ventana": {"titulo": "…", "subtitulo": "액티브 스킬 Lv.10", "lineas": ["…"], "pie": ["재사용 대기시간 14초"]}, "lista": [{"nombre": "…", "nivel": "액티브 스킬 Lv.10"}], "pares": {"상태이상 지속시간 감소": "+1589"}}`.
  Cada línea de una ventana de skill, literal, con sus números, paréntesis y viñetas (`-`, `▶`, `※`). Las
  skills de la lista de la derecha, con su nivel. Opciones de uniforme, ISO-8, tipo, artefacto y equipo
  especial: todos los textos y valores visibles, en `pares` o `lineas`.
- `ctp`: `{"nombre": "…", "estrellas": 6, "aplica": "PVP", "secciones": [{"titulo": "…", "lineas": ["…"]}], "pie": ["…"]}`.
- `striker`: `{"personaje": "메피스토", "pestana": "스트라이커", "cabecera": "…", "retratos": 12, "tooltip": {"nombre": "…", "texto": "…"}}`.
  Los integrantes solo se ven por retrato: contá los retratos y no nombres a nadie. Si hay un globo con un
  nombre escrito, transcribilo.
- `equipo` / `bonos`: `{"pestanas": [...], "pestana_activa": "…", "bonos": [{"nombre": "…", "lineas": ["…"], "boton": "…"}], "ventana": {"titulo": "…", "lineas": [...]}}`.

## Reglas

- Literal: coreano tal cual, con su espaciado, más todo lo que esté en letras latinas (Tip:, C.T.P.,
  ISO-8, PVP, Lv.10), puntuación, %, 초, decimales, todo como se ve. No traduzcas, no corrijas erratas del
  juego (anotalas en `dudas`), no completes. Lo cortado por el borde o el scroll: lo visible y
  `[cortado]`. Lo ilegible después de ampliar: `[ilegible]`. Nunca adivines una sílaba: si dudás entre
  dos, `[?]` y la duda en `dudas`.
- Personajes: solo por texto visible (nombres). Nunca identifiques a nadie por el retrato.
- Privacidad: no transcribas notificaciones del teléfono, mensajes del chat del juego, nombres de otros
  jugadores ni de la cuenta, ni la barra de recursos de arriba (energía, oro, cristales). Si una
  notificación tapa contenido, poné en `dudas` «tapado por una notificación», sin su contenido.
- Colores que importan: naranja (término con link al glosario), amarillo (efecto clave), rojo o rosa
  («Tip:»), verde (nota de enfriamiento o de duración), azul o celeste (link, subrayado). Anotalos en
  `resaltados`.
- No uses la web. No toques nada fuera de `$K/salida/` y `$K/recortes/`. No leas la salida de otros
  carriles.
- Al terminar: validá el archivo con python (cada renglón con `json.loads`, sin `n` repetidos, todos los
  `n` de tu rango presentes) y escribí `$K/salida/<carril>-resumen.json` con: rango, cuántas por tipo, la
  lista de ítems o términos cubiertos (el `seleccionado` o el `titulo` de cada una, sin repetir) y las `n`
  con legibilidad parcial.

## Respuesta final

Menos de 300 palabras: cuántas capturas, qué tipos de pantalla, la lista de ítems o términos cubiertos
(solo los nombres, en coreano), qué quedó ilegible, y cualquier regla del juego que el texto diga
explícitamente y te haya llamado la atención (con el `n`, y una traducción tuya entre corchetes marcada
como tal). Nada de transcripciones completas: están en el archivo.
