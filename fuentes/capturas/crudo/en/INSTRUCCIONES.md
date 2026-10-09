# Transcribir capturas de MARVEL Future Fight

Ezequiel mandó 380 capturas del juego (2712x1220, Android). Sirven como fuente primaria para el
comparador mff.ar: textos del juego en inglés y coreano, C.T.P., strikers, bonos de equipo. Tu
carril transcribe un rango de capturas, literal, a un archivo. No interpretás ni traducís: eso lo
hace después quien integra.

Carpeta: `/tmp/claude-0/-home-claude/edce997e-7225-50a2-90b7-128832dd7122/scratchpad/capturas`
(abajo, `$C`).

- `$C/indice.json`: una fila por captura, en el orden en que se sacaron: `n` (1 a 380), `f`
  (archivo en `/root/.claude/uploads/edce997e-7225-50a2-90b7-128832dd7122/`), `cap` (hora de
  captura), `titulo` (OCR aproximado del título de la pantalla; puede tener errores).
- `$C/recortar.py`: `python3 $C/recortar.py N PRESET [ZOOM]` o `python3 $C/recortar.py N x0,y0,x1,y1 [ZOOM]`
  deja un recorte en `$C/recortes/` e imprime su ruta; leelo con Read. Presets: `entera`, `guia`
  (lista de la izquierda + panel; se lee bien), `panel`, `lista`, `popup` (ventana centrada),
  `striker` (mitad derecha de la ficha de personaje), `bonos`. La primera vez que aparece un tipo
  de pantalla nuevo, mirá la captura `entera` una vez y elegí el recorte que tenga todo el texto.
  Si algo se lee chico, recortá más ajustado y ampliá (ZOOM 1.5 o 2) antes de darlo por ilegible.

## Qué escribir

Un archivo `$C/salida/<carril>.jsonl`: un objeto JSON por renglón, uno por captura, en orden de
`n`. **Escribí (append) el renglón apenas terminás cada captura**, no al final: si el contexto
pierde imágenes viejas, lo escrito queda. Usá python o `cat >>` con cuidado del escape (lo más
seguro: un script chico que reciba el objeto en un heredoc con comillas simples y haga
`json.dumps(..., ensure_ascii=False)`).

Campos de cada renglón:

```
{
  "n": 140, "archivo": "xxxxxxxx-image.jpg",
  "pantalla": "SKILL NAME GLOSSARY",      // título arriba a la izquierda, tal cual se ve
  "tipo": "glosario | guia | ctp | striker | equipo | bonos | coleccion | otro",
  "lista": ["ENTICE", "MIND CONTROL", ...], // ítems visibles en la lista de la izquierda, en orden (null si no hay)
  "seleccionado": "COUNTERATTACK",         // el ítem resaltado de la lista
  "insignias": {"COUNTERATTACK": "BATTLE GUIDE"},  // pastillas junto a ítems de la lista
  "titulo": "COUNTERATTACK",               // título del panel o de la ventana
  "texto": "When hit by an enemy, ...\nBecause Counterattack ...",  // literal, \n entre renglones de párrafo distintos y \n\n entre párrafos
  "resaltados": [{"texto": "Counterattack", "color": "naranja", "subrayado": false}],
  "botones": ["BATTLE GUIDE", "GUIDE HOME"],
  "datos": {},                              // campos propios del tipo, abajo
  "legibilidad": "completa | parcial",
  "dudas": ""                               // qué no se pudo leer y por qué
}
```

Un párrafo que el juego corta en dos renglones solo por el ancho va en un solo renglón (sin \n);
\n solo donde el texto empieza un renglón nuevo a propósito (frase nueva alineada a la izquierda,
viñeta, «Tip:»).

`datos` según el tipo:

- `ctp`: `{"nombre": "...", "estrellas": 6, "secciones": [{"titulo": "Locked Option", "lineas": ["Applies to: Self", ...]}, {"titulo": "Reforge Option", "lineas": [...]}], "pie": ["Greatest Option Value Displayed", "Can be acquired from the Custom Gear Chest"]}`. Cada línea literal, con sus números y paréntesis.
- `striker`: `{"personaje": "KINGPIN", "uniforme": "MARVEL TELEVISION'S DAREDEVIL: BORN AGAIN", "pestana": "STRIKER", "cabecera": "Strikers will assist you ...", "tooltip": {"nombre": "RED SKULL", "texto": "20% Chance to appear when attacking."}}`. En las pestañas STATS o INFO, transcribí lo que muestren en `texto` y en `datos` como pares.
- `equipo` / `bonos`: `{"pestanas": [...], "pestana_activa": "...", "bonos": [{"nombre": "...", "lineas": ["ENERGY ATTACK +5.13%", ...], "boton": "SET TEAM"}], "ventana": {"titulo": "...", "lineas": [...]}}` (la ventana, si hay un globo o popup abierto, como el de una pasiva de equipo).
- `coleccion`: lo que muestre, en pares nombre → líneas.

## Reglas

- Literal: mayúsculas, puntuación, %, «sec.», decimales, todo como se ve. No traduzcas, no
  corrijas erratas del juego (anotalas en `dudas`), no completes. Lo cortado por el borde o el
  scroll: lo visible y `[cortado]`. Lo ilegible después de ampliar: `[ilegible]`. Nunca adivines.
- Personajes: solo por texto visible (nombres). Nunca identifiques a nadie por el retrato.
- Privacidad: no transcribas notificaciones del teléfono (Instagram, WhatsApp, etc.), mensajes del
  chat del juego, nombres de otros jugadores ni de la cuenta, ni la barra de recursos de arriba
  (energía, oro, cristales). Si una notificación tapa contenido, poné en `dudas` «tapado por una
  notificación», sin su contenido.
- Colores que importan: naranja (término con link al glosario), amarillo (efecto clave), rojo
  («Tip:»), verde (nota de enfriamiento), azul o celeste (link). Anotalos en `resaltados`.
- No uses la web. No toques nada fuera de `$C/salida/` y `$C/recortes/`. No leas la salida de
  otros carriles.
- Al terminar: validá el archivo con python (cada renglón con `json.loads`, sin `n` repetidos,
  todos los `n` de tu rango presentes) y escribí el resumen que pide tu carril.

## Respuesta final

Menos de 300 palabras: cuántas capturas, qué tipos de pantalla, la lista de ítems o términos
cubiertos (solo los nombres), qué quedó ilegible, y cualquier regla del juego que el texto diga
explícitamente y te haya llamado la atención (con el `n`). Nada de transcripciones completas:
están en el archivo.
