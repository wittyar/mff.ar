# Índice de las capturas del juego

Qué hay en cada captura que sacó Ezequiel, para no tener que mirar las imágenes: se busca acá (por tema, personaje o
término), se lee la transcripción que indica la columna «Transcripción» y, si hace falta confirmar, se abre esa sola
captura del zip. Lo mismo, en datos: `indice.json` (una fila por captura: álbum, número, archivo, pantalla, qué muestra y
fuentes).

**Las imágenes** van en el zip `capturas-mff-*.zip` que guarda Ezequiel (no están en el repo: son unos 600 MB). Dentro
del zip: `es/NNN.jpg`, `ko/NNN.jpg` y `galactus/NNN.jpg`, con NNN el número de la captura (desde 0, en el orden del
álbum), y una copia de este índice. Los álbumes originales, en CLAUDE.md («Capturas del juego»).

| Álbum | Capturas | Imágenes | Transcripción |
|---|---|---|---|
| `es`: el juego en español (6 de octubre de 2026) | 267 (0 a 266) | en el zip | `fuentes/juego-es/` (por pantalla) y `fuentes/progresion/gorr.csv` |
| `ko`: el juego en coreano (4 de octubre de 2026) | 386 (0 a 385) | en el zip | `fuentes/juego-ko/` (por pantalla), `fuentes/progresion/mephisto.csv` y, captura por captura y literal, `crudo/ko/k1.jsonl` a `k6.jsonl` |
| `galactus`: progresión de stats (9 de octubre de 2026) | 84 (0 a 83) | en el zip | `fuentes/progresion/galactus.csv` |
| `en`: el juego en inglés (380 capturas subidas al chat el 4 de octubre de 2026) | 380 (1 a 380) | **no**: se subieron a una sesión y no quedaron guardadas | captura por captura y literal, `crudo/en/*.jsonl` |

En `crudo/` el número de captura es `n`, **desde 1** (`ko`: la captura N del álbum es la `n` N+1; `en`: la `n` es el
orden en que se subieron). Cada renglón trae la pantalla, la pestaña, el título, el texto literal, los datos, lo que no se
leyó bien (`legibilidad`) y las dudas. Las instrucciones con que se transcribieron, en `crudo/*/INSTRUCCIONES.md`.


## Español

| N.º | Pantalla | Qué muestra | Transcripción |
|---|---|---|---|
| 0 | Foto ajena al juego | Caja del juego de mesa «Virus! 2 Evolution» (no es de MFF). |  |
| 1 | Artefactos | Capitán Hydra (artefacto de Cráneo Rojo, 6★): opción 1 «Aumenta uno de los siguientes: Justicia, crueldad, orden, destrucción +250»; opción 2 «Crea 1 opción al azar»; habilidad exclusiva «Yo soy Hydra» (pasiva, Nv. 4). |  |
| 2 | Artefactos | Capitán Hydra, con el globo de «Yo soy Hydra»: requisito de activación CRÁNEO ROJO; se aplica a aliados supervillanos; aumenta el daño básico infligido a los jefes en 15% y un 0,25% del instinto total (hasta un 200…, cortado). |  |
| 3 | C.T.P. | competition · C.T.P. de competición | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 4 | C.T.P. | competition · C.T.P. poderoso de Competición | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 5 | C.T.P. | C.T.P. brillante de Competición | `fuentes/juego-es/ctps_fichas.json` |
| 6 | C.T.P. | competition · C.T.P. brillante de Competición | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 7 | C.T.P. | Potenciador | `fuentes/juego-es/ctps_fichas.json` |
| 8 | C.T.P. | transcendence · C.T.P. de transcendencia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 9 | C.T.P. | authority · C.T.P. de autoridad | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 10 | C.T.P. | energy · C.T.P. de energía | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 11 | C.T.P. | destruction · C.T.P. de destrucción | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 12 | C.T.P. | patience · C.T.P. de paciencia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 13 | C.T.P. | refinement · C.T.P. de ajuste | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 14 | C.T.P. | regeneration · C.T.P. de regeneración | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 15 | C.T.P. | rage · C.T.P. de ira | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 16 | C.T.P. | veteran · C.T.P. de veterano | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 17 | C.T.P. | judgement · C.T.P. de justiciero | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 18 | C.T.P. | greed · C.T.P. de codicia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 19 | C.T.P. | insight · C.T.P. de percepción | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 20 | C.T.P. | conquest · C.T.P. de conquista | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 21 | C.T.P. | liberation · C.T.P. de liberación | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 22 | C.T.P. | transcendence · C.T.P. poderoso de trascendencia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 23 | C.T.P. | authority · C.T.P. poderoso de autoridad | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 24 | C.T.P. | energy · C.T.P. poderoso de energía | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 25 | C.T.P. | destruction · C.T.P. poderoso de destrucción | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 26 | C.T.P. | patience · C.T.P. poderoso de paciencia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 27 | C.T.P. | refinement · C.T.P. poderoso de ajuste | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 28 | C.T.P. | regeneration · C.T.P. poderoso de regeneración | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 29 | C.T.P. | rage · C.T.P. poderoso de furia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 30 | C.T.P. | veteran · C.T.P. poderoso de veterano | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 31 | C.T.P. | judgement · C.T.P. poderoso de juicio | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 32 | C.T.P. | greed · C.T.P. poderoso de codicia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 33 | C.T.P. | insight · C.T.P. poderoso de percepción | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 34 | C.T.P. | conquest · C.T.P. poderoso de conquista | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 35 | C.T.P. | liberation · C.T.P. poderoso de liberación | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 36 | C.T.P. | transcendence · C.T.P. brillante de trascendencia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 37 | C.T.P. | authority · C.T.P. brillante de autoridad | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 38 | C.T.P. | energy · C.T.P. brillante de energía | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 39 | C.T.P. | destruction · C.T.P. brillante de destrucción | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 40 | C.T.P. | patience · C.T.P. brillante de paciencia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 41 | C.T.P. | refinement · C.T.P. brillante de ajuste | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 42 | C.T.P. | regeneration · C.T.P. brillante de regeneración | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 43 | C.T.P. | rage · C.T.P. brillante de furia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 44 | C.T.P. | veteran · C.T.P. brillante de veterano | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 45 | C.T.P. | judgement · C.T.P. brillante de juicio | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 46 | C.T.P. | greed · C.T.P. brillante de codicia | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 47 | C.T.P. | insight · C.T.P. brillante de percepción | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 48 | C.T.P. | conquest · C.T.P. brillante de conquista | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 49 | C.T.P. | liberation · C.T.P. brillante de liberación | `fuentes/juego-es/ctps.json`, `fuentes/juego-es/ctps_fichas.json` |
| 50 | Ficha · características | Gorr (El Carnicero de Dioses): 1★, nivel 1/40, categoría 3, potencial 0: ataque físico 84, def. física 62, def. de energía 55, PG 410. | `fuentes/progresion/gorr.csv` |
| 51 | Ficha del héroe | Biografía (cortada; no hay captura con el resto) | `fuentes/juego-es/ficha_heroe.json` |
| 52 | Ficha del héroe | PEGADOR | `fuentes/juego-es/ficha_heroe.json` |
| 53 | Ficha del héroe | MEFISTO | `fuentes/juego-es/ficha_heroe.json` |
| 54 | Ficha · características | Gorr (El Carnicero de Dioses): 2★, nivel 1/40, categoría 3, potencial 0: ataque físico 107, def. física 76, def. de energía 68, PG 498. | `fuentes/progresion/gorr.csv` |
| 55 | Ficha · características | Gorr (El Carnicero de Dioses): 3★, nivel 1/45, categoría 3, potencial 0: ataque físico 122, def. física 90, def. de energía 81, PG 583. | `fuentes/progresion/gorr.csv` |
| 56 | Ficha · características | Gorr (El Carnicero de Dioses): 4★, nivel 1/50, categoría 3, potencial 0: ataque físico 142, def. física 104, def. de energía 91, PG 674. | `fuentes/progresion/gorr.csv` |
| 57 | Ficha · características | Gorr (El Carnicero de Dioses): 5★, nivel 1/55, categoría 3, potencial 0: ataque físico 162, def. física 118, def. de energía 104, PG 764. | `fuentes/progresion/gorr.csv` |
| 58 | Ficha · características | Gorr (El Carnicero de Dioses): 6★, nivel 1/60, categoría 3, potencial 0: ataque físico 179, def. física 128, def. de energía 114, PG 853. | `fuentes/progresion/gorr.csv` |
| 59 | Ficha · características | Gorr (El Carnicero de Dioses): 6★, nivel 2/60, categoría 3, potencial 0: ataque físico 353, def. física 252, def. de energía 228, PG 1634. | `fuentes/progresion/gorr.csv` |
| 60 | Ficha · características | Gorr (El Carnicero de Dioses): 6★, nivel 3/60, categoría 3, potencial 0: ataque físico 531, def. física 376, def. de energía 342, PG 2345. | `fuentes/progresion/gorr.csv` |
| 61 | Ficha · características | Gorr (El Carnicero de Dioses): 6★, nivel 5/60, categoría 3, potencial 0: ataque físico 879, def. física 627, def. de energía 569, PG 3553. | `fuentes/progresion/gorr.csv` |
| 62 | Ficha · características | Gorr (El Carnicero de Dioses): 6★ maestría 6, nivel 80/80, categoría 4, potencial 12: ataque físico 21367, def. física 17297, def. de energía 16162, PG 59548. | `fuentes/progresion/gorr.csv` |
| 63 | Ficha del héroe | EL CARNICERO DE DIOSES / EFECTO DEL UNIFORME | `fuentes/juego-es/ficha_heroe.json` |
| 64 | Guía / glosarios | RECLUTAR | `fuentes/juego-es/objetos.json` |
| 65 | Guía / glosarios | AFINIDAD DE CLASE | `fuentes/juego-es/objetos.json` |
| 66 | Guía / glosarios | UNIFORME | `fuentes/juego-es/objetos.json` |
| 67 | Guía / glosarios | BONIFICACIÓN DE EQUIPO | `fuentes/juego-es/objetos.json` |
| 68 | Guía / glosarios | INSTINTO | `fuentes/juego-es/objetos.json` |
| 69 | Guía / glosarios | BANDO | `fuentes/juego-es/objetos.json` |
| 70 | Guía / glosarios | BANDO | `fuentes/juego-es/objetos.json` |
| 71 | Guía / glosarios | EQUIPO | `fuentes/juego-es/objetos.json` |
| 72 | Guía / glosarios | POTENCIAR ISO-8 | `fuentes/juego-es/objetos.json` |
| 73 | Guía / glosarios | COMBINAR ISO-8 | `fuentes/juego-es/objetos.json` |
| 74 | Guía / glosarios | BONIFICACIÓN POR CONJUNTO DE ISO-8 | `fuentes/juego-es/objetos.json` |
| 75 | Guía / glosarios | DESPERTAR ISO-8 | `fuentes/juego-es/objetos.json` |
| 76 | Guía / glosarios | MEJORA DE CROMO DE CÓMIC | `fuentes/juego-es/objetos.json` |
| 77 | Guía / glosarios | CREACIÓN DE CROMOS DE CÓMIC | `fuentes/juego-es/objetos.json` |
| 78 | Guía / glosarios | MEJORAR ARTEFACTO | `fuentes/juego-es/objetos.json` |
| 79 | Guía / glosarios | TRANSFERIR MEJORA DE ARTEFACTO | `fuentes/juego-es/objetos.json` |
| 80 | Guía / glosarios | DESMONTAR ARTEFACTO | `fuentes/juego-es/objetos.json` |
| 81 | Guía / glosarios | ENCANTAR ESPADA | `fuentes/juego-es/objetos.json` |
| 82 | Guía / glosarios | DESMANTELAMIENTO DE ESPADAS | `fuentes/juego-es/objetos.json` |
| 83 | Guía / glosarios | AUMENTO DE RANGO DEL EQUIPO PERSONALIZADO | `fuentes/juego-es/objetos.json` |
| 84 | Guía / glosarios | REFORJA DE C.T.P. | `fuentes/juego-es/objetos.json` |
| 85 | Guía / glosarios | AMPLIFICACIÓN DE URU | `fuentes/juego-es/objetos.json` |
| 86 | Guía / glosarios | COMBINACIÓN DE URU | `fuentes/juego-es/objetos.json` |
| 87 | Guía / glosarios | Despertar de uru | `fuentes/juego-es/objetos.json` |
| 88 | Guía / glosarios | Mejora de JARVIS | `fuentes/juego-es/objetos.json` |
| 89 | Guía / glosarios | Cambio de opción de JARVIS | `fuentes/juego-es/objetos.json` |
| 90 | Guía / glosarios | HISTORIA | `fuentes/juego-es/objetos.json` |
| 91 | Guía / glosarios | HISTORIA | `fuentes/juego-es/objetos.json` |
| 92 | Guía / glosarios | MISIÓN ÉPICA | `fuentes/juego-es/objetos.json` |
| 93 | Guía / glosarios | MISIÓN DIMENSIONAL | `fuentes/juego-es/objetos.json` |
| 94 | Guía / glosarios | MISIÓN DE ENVÍO | `fuentes/juego-es/objetos.json` |
| 95 | Guía / glosarios | DUELO DIMENSIONAL | `fuentes/juego-es/objetos.json` |
| 96 | Guía / glosarios | BATALLA DE ALIANZA | `fuentes/juego-es/objetos.json` |
| 97 | Guía / glosarios | BATALLA DE ALIANZA | `fuentes/juego-es/objetos.json` |
| 98 | Guía / glosarios | BATALLA DE ALIANZA | `fuentes/juego-es/objetos.json` |
| 99 | Guía / glosarios | BATALLA DE OTRO MUNDO | `fuentes/juego-es/objetos.json` |
| 100 | Guía / glosarios | JEFE MUNDIAL | `fuentes/juego-es/objetos.json` |
| 101 | Guía / glosarios | JEFE MUNDIAL | `fuentes/juego-es/objetos.json` |
| 102 | Guía / glosarios | SAGA DEL MULTIVERSO | `fuentes/juego-es/objetos.json` |
| 103 | Guía / glosarios | TIERRA DE SOMBRAS | `fuentes/juego-es/objetos.json` |
| 104 | Guía / glosarios | TORNEO DE ALIANZA | `fuentes/juego-es/objetos.json` |
| 105 | Guía / glosarios | BATALLA LEGENDARIA | `fuentes/juego-es/objetos.json` |
| 106 | Guía / glosarios | CONQUISTA DE ALIANZA | `fuentes/juego-es/objetos.json` |
| 107 | Guía / glosarios | CONQUISTA DE ALIANZA | `fuentes/juego-es/objetos.json` |
| 108 | Guía / glosarios | INCURSIÓN DE JEFE GIGANTE | `fuentes/juego-es/objetos.json` |
| 109 | Guía / glosarios | EVENTO MUNDIAL | `fuentes/juego-es/objetos.json` |
| 110 | Guía / glosarios | SUPERVIVENCIA EN LA LÍNEA TEMPORAL | `fuentes/juego-es/objetos.json` |
| 111 | Guía / glosarios | BRECHA DIMENSIONAL | `fuentes/juego-es/objetos.json` |
| 112 | Guía / glosarios | BRECHA DIMENSIONAL | `fuentes/juego-es/objetos.json` |
| 113 | Guía / glosarios | SUPERVIVENCIA CONTRA ZOMBIS | `fuentes/juego-es/objetos.json` |
| 114 | Guía / glosarios | SUPERVIVENCIA CONTRA ZOMBIS | `fuentes/juego-es/objetos.json` |
| 115 | Guía / glosarios | ARENA DE BATALLA POR EQUIPOS | `fuentes/juego-es/objetos.json` |
| 116 | Guía / glosarios | BIOMETRÍAS | `fuentes/juego-es/objetos.json` |
| 117 | Guía / glosarios | ISO-8 | `fuentes/juego-es/objetos.json` |
| 118 | Guía / glosarios | PIEDRA NORN | `fuentes/juego-es/objetos.json` |
| 119 | Guía / glosarios | KIT DE EQUIPACIÓN | `fuentes/juego-es/objetos.json` |
| 120 | Guía / glosarios | RESTOS DIMENSIONALES | `fuentes/juego-es/objetos.json` |
| 121 | Guía / glosarios | CHIP DE PEX | `fuentes/juego-es/objetos.json` |
| 122 | Guía / glosarios | PAQUETE DE COMPONENTES | `fuentes/juego-es/objetos.json` |
| 123 | Guía / glosarios | PROYECTO CON LA MARCA STARK | `fuentes/juego-es/objetos.json` |
| 124 | Guía / glosarios | CROMOS DE CÓMICS | `fuentes/juego-es/objetos.json` |
| 125 | Guía / glosarios | ARTEFACTO | `fuentes/juego-es/objetos.json` |
| 126 | Guía / glosarios | ESENCIA CELESTIAL | `fuentes/juego-es/objetos.json` |
| 127 | Guía / glosarios | ESPADA | `fuentes/juego-es/objetos.json` |
| 128 | Guía / glosarios | RUNA DE ENCANTAMIENTO | `fuentes/juego-es/objetos.json` |
| 129 | Guía / glosarios | EQUIPO PERSONALIZADO | `fuentes/juego-es/objetos.json` |
| 130 | Guía / glosarios | PIEDRA NORN DE CAOS | `fuentes/juego-es/objetos.json` |
| 131 | Guía / glosarios | ANTIMATERIA NEGRA | `fuentes/juego-es/objetos.json` |
| 132 | Guía / glosarios | URU ENCANTADO | `fuentes/juego-es/objetos.json` |
| 133 | Guía / glosarios | FRAGMENTO DE M'KRAAN | `fuentes/juego-es/objetos.json` |
| 134 | Guía / glosarios | CRISTAL M'KRAAN | `fuentes/juego-es/objetos.json` |
| 135 | Guía / glosarios | PLUMA DE FÉNIX | `fuentes/juego-es/objetos.json` |
| 136 | Guía / glosarios | GEN-X | `fuentes/juego-es/objetos.json` |
| 137 | Guía / glosarios | FRAGMENTO DE CUBO CÓSMICO | `fuentes/juego-es/objetos.json` |
| 138 | Guía / glosarios | PAQUETE DE COMPONENTES DE TITÁN | `fuentes/juego-es/objetos.json` |
| 139 | Guía / glosarios | PAQUETE DE COMPONENTES DE TITÁN | `fuentes/juego-es/objetos.json` |
| 140 | Guía / glosarios | PAQUETE DE COMPONENTES DE TITÁN | `fuentes/juego-es/objetos.json` |
| 141 | Guía / glosarios | REGISTRO DE TITÁN | `fuentes/juego-es/objetos.json` |
| 142 | Guía / glosarios | REGISTRO DE TITÁN | `fuentes/juego-es/objetos.json` |
| 143 | Guía / glosarios | KIT DE POTENCIACIÓN DE TIPO | `fuentes/juego-es/objetos.json` |
| 144 | Guía / glosarios | KIT DE POTENCIACIÓN DE TIPO | `fuentes/juego-es/objetos.json` |
| 145 | Guía / glosarios | CRISTAL DEL DESPERTAR | `fuentes/juego-es/objetos.json` |
| 146 | Guía / glosarios | CRISTAL DEL DESPERTAR | `fuentes/juego-es/objetos.json` |
| 147 | Guía / glosarios | FRAGMENTO DE GEMA DE MANDALAY | `fuentes/juego-es/objetos.json` |
| 148 | Guía / glosarios | FRAGMENTO DE HISTORIA | `fuentes/juego-es/objetos.json` |
| 149 | Guía / glosarios | NÚCLEO DE REFORJA DE C.T.P. | `fuentes/juego-es/objetos.json` |
| 150 | Guía / glosarios | CUBO DE CREACIÓN DE CROMO | `fuentes/juego-es/objetos.json` |
| 151 | Guía / glosarios | PIEDRA DE INVOCACIÓN DE BRECHAS DIMENSIONALES | `fuentes/juego-es/objetos.json` |
| 152 | Guía / glosarios | LIBRO DE LOS VISHANTI | `fuentes/juego-es/objetos.json` |
| 153 | Guía / glosarios | SEMILLA DE VIDA | `fuentes/juego-es/objetos.json` |
| 154 | Guía / glosarios | CARBONADIUM | `fuentes/juego-es/objetos.json` |
| 155 | Guía / glosarios | ALMA DE LOS FALTINE | `fuentes/juego-es/objetos.json` |
| 156 | Guía / glosarios | Llama Eterna | `fuentes/juego-es/objetos.json` |
| 157 | Guía / glosarios | Poder del demiurgo | `fuentes/juego-es/objetos.json` |
| 158 | Guía / glosarios | Piedra de los dioses | `fuentes/juego-es/objetos.json` |
| 159 | Guía / glosarios | DATOS DE EMBLEMA | `fuentes/juego-es/objetos.json` |
| 160 | Guía / glosarios | KIT DE MEJORA DE EMBLEMA | `fuentes/juego-es/objetos.json` |
| 161 | Guía / glosarios | Datos de JARVIS | `fuentes/juego-es/objetos.json` |
| 162 | Guía / glosarios | Fragmento de datos de JARVIS | `fuentes/juego-es/objetos.json` |
| 163 | Glosario de habilidades | Romper guardia | `fuentes/juego-es/glosario.json` |
| 164 | Glosario de habilidades | Probabilidad de esquiva garantizada | `fuentes/juego-es/glosario.json` |
| 165 | Glosario de habilidades | Probabilidad de crítico garantizada | `fuentes/juego-es/glosario.json` |
| 166 | Glosario de habilidades | Daño puro | `fuentes/juego-es/glosario.json` |
| 167 | Glosario de habilidades | Equipo pasivo | `fuentes/juego-es/glosario.json` |
| 168 | Glosario de habilidades | Invencible | `fuentes/juego-es/glosario.json` |
| 169 | Glosario de habilidades | Superarmadura | `fuentes/juego-es/glosario.json` |
| 170 | Glosario de habilidades | Barrera | `fuentes/juego-es/glosario.json` |
| 171 | Glosario de habilidades | Escudo | `fuentes/juego-es/glosario.json` |
| 172 | Glosario de habilidades | Inmunidad al daño | `fuentes/juego-es/glosario.json` |
| 173 | Glosario de habilidades | Miedo | `fuentes/juego-es/glosario.json` |
| 174 | Glosario de habilidades | Trampa | `fuentes/juego-es/glosario.json` |
| 175 | Glosario de habilidades | Congelación temporal | `fuentes/juego-es/glosario.json` |
| 176 | Glosario de habilidades | Hechizo | `fuentes/juego-es/glosario.json` |
| 177 | Glosario de habilidades | Ignorar blanco | `fuentes/juego-es/glosario.json` |
| 178 | Glosario de habilidades | Persuasión | `fuentes/juego-es/glosario.json` |
| 179 | Glosario de habilidades | Control mental | `fuentes/juego-es/glosario.json` |
| 180 | Glosario de habilidades | Recargar escudo | `fuentes/juego-es/glosario.json` |
| 181 | Glosario de habilidades | Fractura | `fuentes/juego-es/glosario.json` |
| 182 | Glosario de habilidades | Incapacitación | `fuentes/juego-es/glosario.json` |
| 183 | Glosario de habilidades | Contrataque | `fuentes/juego-es/glosario.json` |
| 184 | Glosario de habilidades | Elasticidad | `fuentes/juego-es/glosario.json` |
| 185 | Glosario de habilidades | Concentración | `fuentes/juego-es/glosario.json` |
| 186 | Glosario de habilidades | Daño de perforación adicional | `fuentes/juego-es/glosario.json` |
| 187 | Glosario de habilidades | Penetración | `fuentes/juego-es/glosario.json` |
| 188 | Glosario de habilidades | Paliza | `fuentes/juego-es/glosario.json` |
| 189 | Glosario de habilidades | Amplificación de clase | `fuentes/juego-es/glosario.json` |
| 190 | Glosario de habilidades | Acero | `fuentes/juego-es/glosario.json` |
| 191 | Glosario de habilidades | Burla | `fuentes/juego-es/glosario.json` |
| 192 | Glosario de habilidades | Golpe | `fuentes/juego-es/glosario.json` |
| 193 | Glosario de habilidades | Emboscada | `fuentes/juego-es/glosario.json` |
| 194 | Glosario de habilidades | Fortaleza | `fuentes/juego-es/glosario.json` |
| 195 | Glosario de habilidades | Cuchilla | `fuentes/juego-es/glosario.json` |
| 196 | Glosario de habilidades | Defender | `fuentes/juego-es/glosario.json` |
| 197 | Glosario de habilidades | Escudo de superimpacto | `fuentes/juego-es/glosario.json` |
| 198 | Glosario de habilidades | Rabioso | `fuentes/juego-es/glosario.json` |
| 199 | Glosario de habilidades | Vitalidad | `fuentes/juego-es/glosario.json` |
| 200 | Glosario de habilidades | Muro | `fuentes/juego-es/glosario.json` |
| 201 | Glosario de habilidades | Choque | `fuentes/juego-es/glosario.json` |
| 202 | Glosario de habilidades | Pánico | `fuentes/juego-es/glosario.json` |
| 203 | Glosario de habilidades | Pérdida | `fuentes/juego-es/glosario.json` |
| 204 | Glosario de habilidades | Agonía letal | `fuentes/juego-es/glosario.json` |
| 205 | Glosario de habilidades | Marca | `fuentes/juego-es/glosario.json` |
| 206 | Glosario de habilidades | Furia | `fuentes/juego-es/glosario.json` |
| 207 | Ficha del héroe | Info. de bonif. de alianza | `fuentes/juego-es/ficha_heroe.json` |
| 208 | Ficha del héroe | Info. de bonif. de alianza | `fuentes/juego-es/ficha_heroe.json` |
| 209 | Ficha del héroe | INFORMACIÓN (Equipo) | `fuentes/juego-es/ficha_heroe.json` |
| 210 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 211 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 212 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 213 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 214 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 215 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 216 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 217 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 218 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 219 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 220 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 221 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 222 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 223 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 224 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 225 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 226 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 227 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 228 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 229 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 230 | Ficha del héroe | INFORMACIÓN DEL HÉROE — textos de cada pestaña | `fuentes/juego-es/ficha_heroe.json` |
| 231 | Ficha del héroe | INFORMACIÓN (Resumen de personaje) | `fuentes/juego-es/ficha_heroe.json` |
| 232 | Ficha del héroe | EQUIPO DE PERSONAJE | `fuentes/juego-es/ficha_heroe.json` |
| 233 | Ficha del héroe | EQUIPO DE PERSONAJE — Rosa de ébano | `fuentes/juego-es/ficha_heroe.json` |
| 234 | Ficha del héroe | Rosa de ébano (equipo de élite) · Gestionar estadísticas de especialización | `fuentes/juego-es/ficha_heroe.json` |
| 235 | Ficha del héroe | Poder y odio | `fuentes/juego-es/ficha_heroe.json` |
| 236 | Ficha del héroe | Sombra de la desesperación | `fuentes/juego-es/ficha_heroe.json` |
| 237 | Ficha del héroe | Rezo impío | `fuentes/juego-es/ficha_heroe.json` |
| 238 | Ficha del héroe | Detonación de berserker negro | `fuentes/juego-es/ficha_heroe.json` |
| 239 | Ficha del héroe | Venganza mortal | `fuentes/juego-es/ficha_heroe.json` |
| 240 | Ficha del héroe | Cosecha divina | `fuentes/juego-es/ficha_heroe.json` |
| 241 | Ficha del héroe | Perforación cardíaca | `fuentes/juego-es/ficha_heroe.json` |
| 242 | Ficha del héroe | Todonegra, la Matadioses | `fuentes/juego-es/ficha_heroe.json` |
| 243 | Ficha del héroe | Ira de Indigarr | `fuentes/juego-es/ficha_heroe.json` |
| 244 | Ficha del héroe | Suspiros de la oscuridad | `fuentes/juego-es/ficha_heroe.json` |
| 245 | Ficha del héroe | TIPO | `fuentes/juego-es/ficha_heroe.json` |
| 246 | Ficha del héroe | ISO-8 | `fuentes/juego-es/ficha_heroe.json` |
| 247 | Ficha del héroe | Equipa ISO-8 · Nombres y opciones de ISO-8 (recuadro de la izquierda) | `fuentes/juego-es/ficha_heroe.json` |
| 248 | Ficha del héroe | Nombres y opciones de ISO-8 (recuadro de la izquierda) | `fuentes/juego-es/ficha_heroe.json` |
| 249 | Ficha del héroe | Nombres y opciones de ISO-8 (recuadro de la izquierda) | `fuentes/juego-es/ficha_heroe.json` |
| 250 | Ficha del héroe | Nombres y opciones de ISO-8 (recuadro de la izquierda) | `fuentes/juego-es/ficha_heroe.json` |
| 251 | Ficha del héroe | Nombres y opciones de ISO-8 (recuadro de la izquierda) | `fuentes/juego-es/ficha_heroe.json` |
| 252 | Ficha del héroe | Nombres y opciones de ISO-8 (recuadro de la izquierda) | `fuentes/juego-es/ficha_heroe.json` |
| 253 | Ficha del héroe | Nombres y opciones de ISO-8 (recuadro de la izquierda) | `fuentes/juego-es/ficha_heroe.json` |
| 254 | Ficha del héroe | Nombres y opciones de ISO-8 (recuadro de la izquierda) | `fuentes/juego-es/ficha_heroe.json` |
| 255 | Ficha del héroe | ARTEFACTO | `fuentes/juego-es/ficha_heroe.json` |
| 256 | Ficha del héroe | EQUIPO PERSONALIZADO | `fuentes/juego-es/ficha_heroe.json` |
| 257 | Ficha del héroe | UNIFORME | `fuentes/juego-es/ficha_heroe.json` |
| 258 | Ficha del héroe | LISTA DE UNIFORMES — INFORMACIÓN BÁSICA | `fuentes/juego-es/ficha_heroe.json` |
| 259 | Ficha del héroe | EL CARNICERO DE DIOSES / EFECTO DEL UNIFORME · LISTA DE UNIFORMES — EFECTO DEL UNIFORME | `fuentes/juego-es/ficha_heroe.json` |
| 260 | Ficha del héroe | LISTA DE UNIFORMES — HABILIDADES CAMBIADAS | `fuentes/juego-es/ficha_heroe.json` |
| 261 | Ficha del héroe | UNIFORMES A ELEGIR | `fuentes/juego-es/ficha_heroe.json` |
| 262 | Ficha del héroe | UNIFORMES A ELEGIR — otros uniformes | `fuentes/juego-es/ficha_heroe.json` |
| 263 | Ficha del héroe | UNIFORMES A ELEGIR — otros uniformes | `fuentes/juego-es/ficha_heroe.json` |
| 264 | Ficha del héroe | UNIFORMES A ELEGIR — otros uniformes | `fuentes/juego-es/ficha_heroe.json` |
| 265 | Ficha del héroe | UNIFORMES A ELEGIR — otros uniformes | `fuentes/juego-es/ficha_heroe.json` |
| 266 | Ficha del héroe | AJUSTES | `fuentes/juego-es/ficha_heroe.json` |

## Coreano

| N.º | Pantalla | Qué muestra | Transcripción |
|---|---|---|---|
| 0 | guia | 영웅 정보 · 호출 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 1 | guia | 영웅 정보 · 상성 효과 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 2 | guia | 영웅 정보 · 유니폼 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 3 | guia | 영웅 정보 · 팀 효과 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 4 | guia | 영웅 정보 · 천성 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 5 | guia | 영웅 정보 · 진영 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 6 | guia | 장비 성장 · 장비 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 7 | guia | 장비 성장 · ISO-8 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 8 | guia | 장비 성장 · ISO-8 합성 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 9 | guia | 장비 성장 · ISO-8 세트 효과 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 10 | guia | 장비 성장 · ISO-8 각성 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 11 | guia | 장비 성장 · 코믹스 카드 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 12 | guia | 장비 성장 · 코믹스 카드 세공 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 13 | guia | 장비 성장 · 아티팩트 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 14 | guia | 장비 성장 · 아티팩트 강화 이전 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 15 | guia | 장비 성장 · 아티팩트 분해 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 16 | guia | 장비 성장 · 소드 인챈트 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 17 | guia | 장비 성장 · 소드 분해 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 18 | guia | 장비 성장 · 특수 장비 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 19 | guia | 장비 성장 · C.T.P. 재련 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 20 | guia | 장비 성장 · 우루 증폭 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 21 | guia | 장비 성장 · 우루 합성 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 22 | guia | 장비 성장 · 우루 각성 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 23 | guia | 장비 성장 · J.A.R.V.I.S. 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 24 | guia | 장비 성장 · J.A.R.V.I.S. 옵션 변경 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 25 | glosario | 콘텐츠 사전 · 이야기 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 26 | glosario | 콘텐츠 사전 · 에픽 퀘스트 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 27 | glosario | 콘텐츠 사전 · 차원 임무 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 28 | glosario | 콘텐츠 사전 · 파견 임무 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 29 | glosario | 콘텐츠 사전 · 타임라인 배틀 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 30 | glosario | 콘텐츠 사전 · 얼라이언스 배틀 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 31 | glosario | 콘텐츠 사전 · 아더월드 배틀 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 32 | glosario | 콘텐츠 사전 · 월드 보스 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 33 | glosario | 콘텐츠 사전 · 멀티버스 사가 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 34 | glosario | 콘텐츠 사전 · 섀도우랜드 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 35 | glosario | 콘텐츠 사전 · 얼라이언스 토너먼트 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 36 | glosario | 콘텐츠 사전 · 레전더리 배틀 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 37 | glosario | 콘텐츠 사전 · 연합 점령전 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 38 | glosario | 콘텐츠 사전 · 거대 보스 레이드 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 39 | glosario | 콘텐츠 사전 · 월드 이벤트 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 40 | glosario | 콘텐츠 사전 · 타임라인 서바이벌 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 41 | glosario | 콘텐츠 사전 · 차원의 틈 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 42 | glosario | 콘텐츠 사전 · 좀비 서바이벌 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 43 | glosario | 콘텐츠 사전 · 팀 배틀 아레나 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 44 | glosario | 콘텐츠 사전 · 얼라이언스 배틀 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 45 | glosario | 콘텐츠 사전 · 월드 보스 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 46 | glosario | 콘텐츠 사전 · 연합 점령전 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 47 | glosario | 콘텐츠 사전 · 좀비 서바이벌 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k1.jsonl` |
| 48 | guia | 영웅 성장 · 영웅 레벨 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 49 | guia | 영웅 성장 · 진급 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 50 | guia | 영웅 성장 · 마스터리 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 51 | guia | 영웅 성장 · 티어-2 승급 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 52 | guia | 영웅 성장 · 스킬 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 53 | guia | 영웅 성장 · ISO-8 장착 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 54 | guia | 영웅 성장 · 특수 장비 장착 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 55 | guia | 영웅 성장 · 코믹스 카드 장착 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 56 | guia | 영웅 성장 · 강화 우루 장착 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 57 | guia | 영웅 성장 · 유니폼 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 58 | guia | 영웅 성장 · 잠재력 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 59 | guia | 영웅 성장 · 잠재력 각성 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 60 | guia | 영웅 성장 · 잠재력 초월 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 61 | guia | 영웅 성장 · 티어-3 승급 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 62 | guia | 영웅 성장 · 티어-4 승급 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 63 | guia | 영웅 성장 · 레이드 레벨 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 64 | guia | 영웅 성장 · 타입 강화 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k1.jsonl` |
| 65 | guia | 영웅 성장 · 에이전트 레벨 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 66 | guia | 영웅 성장 · 쉴드 아카이브 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 67 | guia | 영웅 성장 · 팀업 컬렉션 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 68 | guia | 영웅 성장 · 엠블럼 컬렉션 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 69 | guia | 영웅 성장 · 엘리트 장비 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 70 | guia | 영웅 성장 · J.A.R.V.I.S. | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 71 | glosario | 아이템 사전 · 생체 데이터 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 72 | glosario | 아이템 사전 · ISO-8 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 73 | glosario | 아이템 사전 · 노른 스톤 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 74 | glosario | 아이템 사전 · 장비 강화 키트 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 75 | glosario | 아이템 사전 · 차원의 파편 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 76 | glosario | 아이템 사전 · 경험치 칩 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 77 | glosario | 아이템 사전 · 부품 상자 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 78 | glosario | 아이템 사전 · 스타크제 설계도 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 79 | glosario | 아이템 사전 · 코믹스 카드 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 80 | glosario | 아이템 사전 · 아티팩트 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 81 | glosario | 아이템 사전 · 천상의 정수 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 82 | glosario | 아이템 사전 · 소드 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 83 | glosario | 아이템 사전 · 인챈트 룬 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 84 | glosario | 아이템 사전 · 특수 장비 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 85 | glosario | 아이템 사전 · 혼돈의 노른 스톤 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 86 | glosario | 아이템 사전 · 암흑 반물질 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 87 | glosario | 아이템 사전 · 강화 우루 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 88 | glosario | 아이템 사전 · 엠크란 조각 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 89 | glosario | 아이템 사전 · 엠크란 크리스탈 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 90 | glosario | 아이템 사전 · 피닉스 깃털 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 91 | glosario | 아이템 사전 · X-유전자 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 92 | glosario | 아이템 사전 · 코스믹 큐브 파편 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 93 | glosario | 아이템 사전 · 차원의 정수 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 94 | glosario | 아이템 사전 · 타이탄 부품 상자 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 95 | glosario | 아이템 사전 · 타이탄의 기록 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 96 | glosario | 아이템 사전 · 타입 강화 키트 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 97 | glosario | 아이템 사전 · 각성의 크리스탈 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 98 | glosario | 아이템 사전 · 만달레이 젬 파편 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 99 | glosario | 아이템 사전 · 이야기 조각 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 100 | glosario | 아이템 사전 · C.T.P. 재련 코어 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 101 | glosario | 아이템 사전 · 카드 세공 큐브 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 102 | glosario | 아이템 사전 · 차원의 틈 소환석 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 103 | glosario | 아이템 사전 · 비샨티의 책 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 104 | glosario | 아이템 사전 · 생명의 씨앗 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 105 | glosario | 아이템 사전 · 카보나디움 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 106 | glosario | 아이템 사전 · 팔틴의 영혼 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 107 | glosario | 아이템 사전 · 영원의 불꽃 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 108 | glosario | 아이템 사전 · 데미어지의 힘 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 109 | glosario | 아이템 사전 · 갓스톤 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 110 | glosario | 아이템 사전 · 엠블럼 데이터 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 111 | glosario | 아이템 사전 · 엠블럼 강화 키트 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 112 | glosario | 아이템 사전 · J.A.R.V.I.S. 데이터 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 113 | glosario | 아이템 사전 · J.A.R.V.I.S. 데이터 조각 | `fuentes/juego-ko/objetos.json`, `crudo/ko/k2.jsonl` |
| 114 | glosario | 스킬 용어 사전 · 가드 브레이크 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 115 | glosario | 스킬 용어 사전 · 무조건 회피율 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 116 | glosario | 스킬 용어 사전 · 무조건 치명타율 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 117 | glosario | 스킬 용어 사전 · 순수 피해량 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 118 | glosario | 스킬 용어 사전 · 팀 패시브 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 119 | glosario | 스킬 용어 사전 · 무적 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 120 | glosario | 스킬 용어 사전 · 슈퍼 아머 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 121 | glosario | 스킬 용어 사전 · 배리어 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 122 | glosario | 스킬 용어 사전 · 쉴드 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 123 | glosario | 스킬 용어 사전 · 피해 면역 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 124 | glosario | 스킬 용어 사전 · 공포 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 125 | glosario | 스킬 용어 사전 · 속박 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 126 | glosario | 스킬 용어 사전 · 타임 프리징 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 127 | glosario | 스킬 용어 사전 · 매혹 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 128 | glosario | 스킬 용어 사전 · 타겟팅 무시 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 129 | glosario | 스킬 용어 사전 · 유혹 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k2.jsonl` |
| 130 | glosario | 스킬 용어 사전 · 정신 지배 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 131 | glosario | 스킬 용어 사전 · 리차지 쉴드 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 132 | glosario | 스킬 용어 사전 · 골절 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 133 | glosario | 스킬 용어 사전 · 무력화 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 134 | glosario | 스킬 용어 사전 · 반격기 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 135 | glosario | 스킬 용어 사전 · 탄성 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 136 | glosario | 스킬 용어 사전 · 집중 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 137 | glosario | 스킬 용어 사전 · 추가 관통 피해 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 138 | glosario | 스킬 용어 사전 · 간파 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 139 | glosario | 스킬 용어 사전 · 압도 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 140 | glosario | 스킬 용어 사전 · 속성 증폭 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 141 | glosario | 스킬 용어 사전 · 강철 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 142 | glosario | 스킬 용어 사전 · 조롱 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 143 | glosario | 스킬 용어 사전 · 강타 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 144 | glosario | 스킬 용어 사전 · 맹공 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 145 | glosario | 스킬 용어 사전 · 불굴 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 146 | glosario | 스킬 용어 사전 · 칼날 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 147 | glosario | 스킬 용어 사전 · 방호 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 148 | glosario | 스킬 용어 사전 · 슈퍼 히트 쉴드 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 149 | glosario | 스킬 용어 사전 · 격노 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 150 | glosario | 스킬 용어 사전 · 활력 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 151 | glosario | 스킬 용어 사전 · 방벽 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 152 | glosario | 스킬 용어 사전 · 격돌 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 153 | glosario | 스킬 용어 사전 · 공황 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 154 | glosario | 스킬 용어 사전 · 상실 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 155 | glosario | 스킬 용어 사전 · 최후의 발악 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 156 | glosario | 스킬 용어 사전 · 표식 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 157 | glosario | 스킬 용어 사전 · 맹렬 | `fuentes/juego-ko/glosario.json`, `crudo/ko/k3.jsonl` |
| 158 | otro | 영웅 도감 | `crudo/ko/k3.jsonl` |
| 159 | ctp | 특수 장비 도감 · 경쟁의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 160 | ctp | 특수 장비 도감 · 강력한 경쟁의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 161 | glosario | 스킬 용어 사전 · 맹렬 | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 162 | ctp | 특수 장비 도감 · 찬란한 경쟁의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 163 | ctp | 특수 장비 도감 · 초월의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 164 | ctp | 특수 장비 도감 · 권능의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 165 | ctp | 특수 장비 도감 · 격동의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 166 | ctp | 특수 장비 도감 · 파괴의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 167 | ctp | 특수 장비 도감 · 인내의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 168 | ctp | 특수 장비 도감 · 제련된 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 169 | ctp | 특수 장비 도감 · 재생의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 170 | ctp | 특수 장비 도감 · 분노의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 171 | ctp | 특수 장비 도감 · 역전의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 172 | ctp | 특수 장비 도감 · 심판의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 173 | ctp | 특수 장비 도감 · 탐욕의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 174 | ctp | 특수 장비 도감 · 통찰의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 175 | ctp | 특수 장비 도감 · 극복의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 176 | ctp | 특수 장비 도감 · 해방의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 177 | ctp | 특수 장비 도감 · 강력한 초월의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 178 | ctp | 특수 장비 도감 · 강력한 권능의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 179 | ctp | 특수 장비 도감 · 강력한 격동의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 180 | ctp | 특수 장비 도감 · 강력한 파괴의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 181 | ctp | 특수 장비 도감 · 강력한 인내의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 182 | ctp | 특수 장비 도감 · 강력한 제련된 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 183 | ctp | 특수 장비 도감 · 강력한 재생의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 184 | ctp | 특수 장비 도감 · 강력한 분노의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 185 | ctp | 특수 장비 도감 · 강력한 역전의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 186 | ctp | 특수 장비 도감 · 강력한 심판의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 187 | ctp | 특수 장비 도감 · 강력한 탐욕의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 188 | ctp | 특수 장비 도감 · 강력한 통찰의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 189 | ctp | 특수 장비 도감 · 강력한 극복의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 190 | ctp | 특수 장비 도감 · 강력한 해방의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 191 | ctp | 특수 장비 도감 · 찬란한 초월의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 192 | ctp | 특수 장비 도감 · 찬란한 권능의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 193 | ctp | 특수 장비 도감 · 찬란한 격동의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 194 | ctp | 특수 장비 도감 · 찬란한 파괴의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k3.jsonl` |
| 195 | ctp | 특수 장비 도감 · 찬란한 인내의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 196 | ctp | 특수 장비 도감 · 찬란한 제련된 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 197 | ctp | 특수 장비 도감 · 찬란한 재생의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 198 | ctp | 특수 장비 도감 · 찬란한 분노의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 199 | ctp | 특수 장비 도감 · 찬란한 역전의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 200 | ctp | 특수 장비 도감 · 찬란한 역전의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 201 | ctp | 특수 장비 도감 · 찬란한 심판의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 202 | ctp | 특수 장비 도감 · 찬란한 탐욕의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 203 | ctp | 특수 장비 도감 · 찬란한 통찰의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 204 | ctp | 특수 장비 도감 · 찬란한 탐욕의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 205 | ctp | 특수 장비 도감 · 찬란한 극복의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 206 | ctp | 특수 장비 도감 · 찬란한 해방의 C.T.P. | `fuentes/juego-ko/ctps.json`, `crudo/ko/k4.jsonl` |
| 207 | otro | 아티팩트 도감 · 캡틴 하이드라 | `crudo/ko/k4.jsonl` |
| 208 | otro | 아티팩트 도감 · 캡틴 하이드라 | `crudo/ko/k4.jsonl` |
| 209 | otro | 아티팩트 도감 · 네거티브 존의 지배자 | `crudo/ko/k4.jsonl` |
| 210 | otro | 아티팩트 도감 · 네거티브 존의 지배자 | `crudo/ko/k4.jsonl` |
| 211 | otro | 아티팩트 도감 · 행성 포식자 | `crudo/ko/k4.jsonl` |
| 212 | otro | 아티팩트 도감 · 행성 포식자 | `crudo/ko/k4.jsonl` |
| 213 | otro | 연합 점령전 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 214 | otro | 정비 단계 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 215 | otro | 연합 점령전 월드맵 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 216 | glosario | 콘텐츠 사전 · 연합 점령전 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 217 | otro | 연합 점령전 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 218 | otro | 연합 점령전 · 점령전 보상 목록: 챌린저 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 219 | otro | 연합 점령전 · 점령전 보상 목록: 챌린저 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 220 | otro | 연합 점령전 · 점령전 보상 목록: 챌린저 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 221 | otro | 연합 점령전 · 점령전 보상 목록: 챌린저 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 222 | otro | 연합 · 연합 효과 정보 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 223 | otro | 연합 · 연합 효과 정보 | `fuentes/juego-ko/contenidos.json`, `crudo/ko/k4.jsonl` |
| 224 | personaje | 영웅 정보 · 정보 | `crudo/ko/k4.jsonl` |
| 225 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 226 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 227 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 228 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 229 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 230 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 231 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 232 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 233 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 234 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 235 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 236 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 237 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 238 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 239 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 240 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 241 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 242 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 243 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 244 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 245 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 246 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 247 | personaje | 영웅 정보 · 영웅 상세 정보 | `crudo/ko/k4.jsonl` |
| 248 | personaje | 영웅 정보 · 영웅 상세 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 249 | personaje | 영웅 정보 · 영웅 상세 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 250 | personaje | 영웅 정보 · 영웅 상세 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 251 | personaje | 영웅 정보 · 정보 | `crudo/ko/k4.jsonl` |
| 252 | personaje | 영웅 정보 · 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 253 | personaje | 영웅 정보 · 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 254 | personaje | 영웅 정보 · 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 255 | personaje | 영웅 정보 · 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 256 | personaje | 영웅 정보 · 영웅 장비 | `crudo/ko/k4.jsonl` |
| 257 | personaje | 영웅 정보 · 영웅 장비 | `crudo/ko/k4.jsonl` |
| 258 | personaje | 영웅 정보 · 스킬 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 259 | personaje | 영웅 정보 · 스킬 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k4.jsonl` |
| 260 | personaje | 영웅 정보 · 스킬 · 헬로드 펀치 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 261 | personaje | 영웅 정보 · 스킬 · 헬로드 펀치 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 262 | personaje | 영웅 정보 · 스킬 · 지옥 불 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 263 | personaje | 영웅 정보 · 스킬 · 지옥의 폭풍 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 264 | personaje | 영웅 정보 · 스킬 · 지옥의 폭풍 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 265 | personaje | 영웅 정보 · 스킬 · 여기에 온 자, 모든 희망을 버려라 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 266 | personaje | 영웅 정보 · 스킬 · 계약의 대가 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 267 | personaje | 영웅 정보 · 스킬 · 불타는 부활 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 268 | personaje | 영웅 정보 · 스킬 · 지옥 군주 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 269 | personaje | 영웅 정보 · 타입 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 270 | personaje | 영웅 정보 · ISO-8 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 271 | personaje | 영웅 정보 · 아티팩트 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 272 | personaje | 영웅 정보 · 아티팩트 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 273 | ctp | 영웅 정보 · 특수 장비 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 274 | ctp | 영웅 정보 · 특수 장비 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 275 | personaje | 영웅 정보 · 유니폼 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 276 | personaje | 유니폼 룸 · 기본 정보 · 메피스토 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 277 | personaje | 유니폼 룸 · 상태이상 지속시간 감소 · 유니폼 옵션 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 278 | personaje | 유니폼 룸 · 에너지 공격력 상승 · 유니폼 옵션 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 279 | personaje | 유니폼 룸 · 회복률 상승 · 유니폼 옵션 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 280 | personaje | 유니폼 룸 · 모든 일반 방어력 상승 · 유니폼 옵션 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 281 | personaje | 유니폼 룸 · 치명타 피해율 상승 · 유니폼 옵션 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 282 | personaje | 유니폼 룸 · 유니폼 효과 · 메피스토 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 283 | personaje | 유니폼 룸 · 변경 스킬 · 메피스토 | `crudo/ko/k5.jsonl` |
| 284 | personaje | 유니폼 룸 · 변경 스킬 · 분노의 구덩이 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 285 | personaje | 유니폼 룸 · 변경 스킬 · 지옥 군주 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 286 | personaje | 유니폼 룸 · 변경 스킬 · 헬로드 펀치 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 287 | personaje | 유니폼 룸 · 변경 스킬 · 지옥 불 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 288 | personaje | 유니폼 룸 · 변경 스킬 · 지옥의 폭풍 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 289 | personaje | 유니폼 룸 · 변경 스킬 · 여기에 온 자, 모든 희망을 버려라 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 290 | personaje | 유니폼 룸 · 변경 스킬 · 계약의 대가 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 291 | personaje | 영웅 정보 · 영웅 장비 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 292 | equipo | 엘리트 장비 · 서펀트 크라운 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 293 | personaje | 영웅 정보 · 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 294 | personaje | 영웅 정보 · 스킬 · 아마겟돈 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 295 | personaje | 영웅 정보 · 스킬 · 막을 수 없는 종말 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 296 | personaje | 영웅 정보 · 스킬 · 뮤턴트의 제왕 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 297 | personaje | 영웅 정보 · 스킬 · 뮤턴트의 제왕 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 298 | personaje | 영웅 정보 · 스킬 · 뮤턴트의 제왕 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 299 | personaje | 영웅 정보 · 스킬 · 뮤턴트의 제왕 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 300 | bonos | 영웅 정보 · 전체 · 영웅 상세 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 301 | bonos | 영웅 정보 · 전체 · 영웅 상세 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 302 | bonos | 영웅 정보 · 전체 · 영웅 상세 정보 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k5.jsonl` |
| 303 | personaje | 도감 영웅 정보 · 능력치 · 메피스토 | `crudo/ko/k5.jsonl` |
| 304 | personaje | Mephisto: 1★, nivel 1/40, tier 3, potencial 0: ataque de energía 82, def. física 56, def. de energía 68, PG 397. | `fuentes/juego-ko/ficha.json`, `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 305 | personaje | Mephisto: 1★, nivel 1/40, tier 3, potencial 0: ataque de energía 82, def. física 56, def. de energía 68, PG 397. | `fuentes/juego-ko/ficha.json`, `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 306 | personaje | 도감 영웅 정보 · 능력치 · 메피스토 | `crudo/ko/k5.jsonl` |
| 307 | personaje | Mephisto: 2★, nivel 1/40, tier 3, potencial 0: ataque de energía 103, def. física 69, def. de energía 86, PG 483. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 308 | personaje | Mephisto: 3★, nivel 1/45, tier 3, potencial 0: ataque de energía 117, def. física 83, def. de energía 100, PG 565. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 309 | personaje | Mephisto: 4★, nivel 1/50, tier 3, potencial 0: ataque de energía 140, def. física 88, def. de energía 115, PG 653. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 310 | personaje | Mephisto: 5★, nivel 1/55, tier 3, potencial 0: ataque de energía 159, def. física 101, def. de energía 129, PG 739. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 311 | personaje | Mephisto: 6★, nivel 1/60, tier 3, potencial 0: ataque de energía 175, def. física 111, def. de energía 139, PG 824. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 312 | personaje | Mephisto: 6★, nivel 2/60, tier 3, potencial 0: ataque de energía 349, def. física 221, def. de energía 277, PG 1577. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 313 | personaje | Mephisto: 6★, nivel 2/60, tier 3, potencial 0: ataque de energía 349, def. física 221, def. de energía 277, PG 1577. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 314 | personaje | Mephisto: 6★, nivel 3/60, tier 3, potencial 0: ataque de energía 524, def. física 332, def. de energía 416, PG 2262. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 315 | personaje | Mephisto: 6★, nivel 4/60, tier 3, potencial 0: ataque de energía 699, def. física 438, def. de energía 554, PG 2881. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 316 | personaje | Mephisto: 6★, nivel 7/60, tier 3, potencial 0: ataque de energía 1218, def. física 765, def. de energía 970, PG 4319. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 317 | personaje | Mephisto: 6★, nivel 8/60, tier 3, potencial 0: ataque de energía 1393, def. física 875, def. de energía 1109, PG 4664. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 318 | personaje | Mephisto: 6★, nivel 9/60, tier 3, potencial 0: ataque de energía 1568, def. física 986, def. de energía 1247, PG 4937. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 319 | personaje | Mephisto: 6★, nivel 10/60, tier 3, potencial 0: ataque de energía 1828, def. física 1136, def. de energía 1437, PG 5403. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 320 | personaje | Mephisto: 6★, nivel 11/60, tier 3, potencial 0: ataque de energía 2002, def. física 1251, def. de energía 1580, PG 5524. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 321 | personaje | Mephisto: 6★, nivel 12/60, tier 3, potencial 0: ataque de energía 2173, def. física 1361, def. de energía 1723, PG 6003. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 322 | personaje | Mephisto: 6★, nivel 13/60, tier 3, potencial 0: ataque de energía 2347, def. física 1476, def. de energía 1866, PG 6483. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 323 | personaje | Mephisto: 6★, nivel 14/60, tier 3, potencial 0: ataque de energía 2522, def. física 1591, def. de energía 2010, PG 6962. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 324 | personaje | Mephisto: 6★, nivel 15/60, tier 3, potencial 0: ataque de energía 2782, def. física 1764, def. de energía 2231, PG 7679. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k5.jsonl` |
| 325 | personaje | Mephisto: 6★, nivel 16/60, tier 3, potencial 0: ataque de energía 2956, def. física 1883, def. de energía 2384, PG 8158. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 326 | personaje | Mephisto: 6★, nivel 17/60, tier 3, potencial 0: ataque de energía 3131, def. física 2002, def. de energía 2532, PG 8637. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 327 | personaje | Mephisto: 6★, nivel 18/60, tier 3, potencial 0: ataque de energía 3306, def. física 2117, def. de energía 2680, PG 9117. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 328 | personaje | Mephisto: 6★, nivel 19/60, tier 3, potencial 0: ataque de energía 3476, def. física 2237, def. de energía 2827, PG 9596. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 329 | personaje | Mephisto: 6★, nivel 20/60, tier 3, potencial 0: ataque de energía 3740, def. física 2435, def. de energía 3082, PG 10322. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 330 | personaje | Mephisto: 6★, nivel 21/60, tier 3, potencial 0: ataque de energía 3911, def. física 2559, def. de energía 3239, PG 10801. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 331 | personaje | Mephisto: 6★, nivel 22/60, tier 3, potencial 0: ataque de energía 4085, def. física 2683, def. de energía 3391, PG 11281. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 332 | personaje | Mephisto: 6★, nivel 23/60, tier 3, potencial 0: ataque de energía 4260, def. física 2802, def. de energía 3548, PG 11760. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 333 | personaje | Mephisto: 6★, nivel 24/60, tier 3, potencial 0: ataque de energía 4435, def. física 2926, def. de energía 3701, PG 12239. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 334 | personaje | Mephisto: 6★, nivel 25/60, tier 3, potencial 0: ataque de energía 4695, def. física 3151, def. de energía 3987, PG 12956. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 335 | personaje | Mephisto: 6★, nivel 26/60, tier 3, potencial 0: ataque de energía 4869, def. física 3275, def. de energía 4144, PG 13436. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 336 | personaje | Mephisto: 6★, nivel 27/60, tier 3, potencial 0: ataque de energía 5044, def. física 3403, def. de energía 4306, PG 13915. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 337 | personaje | Mephisto: 6★, nivel 28/60, tier 3, potencial 0: ataque de energía 5214, def. física 3527, def. de energía 4463, PG 14394. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 338 | personaje | Mephisto: 6★, nivel 29/60, tier 3, potencial 0: ataque de energía 5389, def. física 3655, def. de energía 4625, PG 14878. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 339 | personaje | Mephisto: 6★, nivel 30/60, tier 3, potencial 0: ataque de energía 5649, def. física 3907, def. de energía 4943, PG 15599. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 340 | personaje | Mephisto: 6★, nivel 31/60, tier 3, potencial 0: ataque de energía 5823, def. física 4035, def. de energía 5110, PG 16079. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 341 | personaje | Mephisto: 6★, nivel 32/60, tier 3, potencial 0: ataque de energía 5998, def. física 4168, def. de energía 5271, PG 16558. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 342 | personaje | Mephisto: 6★, nivel 33/60, tier 3, potencial 0: ataque de energía 6173, def. física 4296, def. de energía 5438, PG 17037. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 343 | personaje | Mephisto: 6★, nivel 34/60, tier 3, potencial 0: ataque de energía 6347, def. física 4429, def. de energía 5604, PG 17517. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 344 | personaje | Mephisto: 6★, nivel 35/60, tier 3, potencial 0: ataque de energía 6607, def. física 4703, def. de energía 5951, PG 18234. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 345 | personaje | Mephisto: 6★, nivel 36/60, tier 3, potencial 0: ataque de energía 6782, def. física 4840, def. de energía 6122, PG 18713. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 346 | personaje | Mephisto: 6★, nivel 36/60, tier 3, potencial 0: ataque de energía 6782, def. física 4840, def. de energía 6122, PG 18713. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 347 | personaje | Mephisto: 6★, nivel 37/60, tier 3, potencial 0: ataque de energía 6952, def. física 4973, def. de energía 6292, PG 19192. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 348 | personaje | Mephisto: 6★, nivel 38/60, tier 3, potencial 0: ataque de energía 7127, def. física 5110, def. de energía 6463, PG 19676. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 349 | personaje | Mephisto: 6★, nivel 39/60, tier 3, potencial 0: ataque de energía 7302, def. física 5242, def. de energía 6634, PG 20156. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 350 | personaje | Mephisto: 6★, nivel 40/60, tier 3, potencial 0: ataque de energía 7562, def. física 5543, def. de energía 7013, PG 20877. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 351 | personaje | Mephisto: 6★, nivel 41/60, tier 3, potencial 0: ataque de energía 7736, def. física 5684, def. de energía 7189, PG 21356. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 352 | personaje | Mephisto: 6★, nivel 42/60, tier 3, potencial 0: ataque de energía 7911, def. física 5821, def. de energía 7364, PG 21836. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 353 | personaje | Mephisto: 6★, nivel 43/60, tier 3, potencial 0: ataque de energía 8085, def. física 5963, def. de energía 7540, PG 22315. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 354 | personaje | Mephisto: 6★, nivel 44/60, tier 3, potencial 0: ataque de energía 8256, def. física 6100, def. de energía 7715, PG 22794. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 355 | personaje | Mephisto: 6★, nivel 45/60, tier 3, potencial 0: ataque de energía 8520, def. física 6427, def. de energía 8131, PG 23511. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 356 | personaje | Mephisto: 6★, nivel 46/60, tier 3, potencial 0: ataque de energía 8690, def. física 6568, def. de energía 8311, PG 23990. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 357 | personaje | Mephisto: 6★, nivel 47/60, tier 3, potencial 0: ataque de energía 8865, def. física 6714, def. de energía 8492, PG 24474. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 358 | personaje | Mephisto: 6★, nivel 48/60, tier 3, potencial 0: ataque de energía 9040, def. física 6855, def. de energía 8672, PG 24954. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 359 | personaje | Mephisto: 6★, nivel 49/60, tier 3, potencial 0: ataque de energía 9214, def. física 6997, def. de energía 8852, PG 25433. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 360 | personaje | Mephisto: 6★, nivel 50/60, tier 3, potencial 0: ataque de energía 9474, def. física 7350, def. de energía 9300, PG 26154. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 361 | personaje | Mephisto: 6★, nivel 51/60, tier 3, potencial 0: ataque de energía 9836, def. física 7496, def. de energía 9485, PG 27162. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 362 | personaje | Mephisto: 6★, nivel 52/60, tier 3, potencial 0: ataque de energía 10220, def. física 7863, def. de energía 9947, PG 28220. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 363 | personaje | Mephisto: 6★, nivel 53/60, tier 3, potencial 0: ataque de energía 10620, def. física 8013, def. de energía 10141, PG 29317. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 364 | personaje | Mephisto: 6★, nivel 54/60, tier 3, potencial 0: ataque de energía 11038, def. física 8394, def. de energía 10617, PG 30473. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 365 | personaje | Mephisto: 6★, nivel 55/60, tier 3, potencial 0: ataque de energía 11387, def. física 8548, def. de energía 10815, PG 31432. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 366 | personaje | Mephisto: 6★, nivel 56/60, tier 3, potencial 0: ataque de energía 11834, def. física 8937, def. de energía 11310, PG 32677. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 367 | personaje | Mephisto: 6★, nivel 57/60, tier 3, potencial 0: ataque de energía 12307, def. física 9096, def. de energía 11508, PG 33976. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 368 | personaje | Mephisto: 6★, nivel 58/60, tier 3, potencial 0: ataque de energía 12793, def. física 9499, def. de energía 12021, PG 35320. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 369 | personaje | Mephisto: 6★, nivel 59/60, tier 3, potencial 0: ataque de energía 13300, def. física 9662, def. de energía 12229, PG 36709. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 370 | personaje | Mephisto: 6★, nivel 60/60, tier 3, potencial 0: ataque de energía 13645, def. física 9826, def. de energía 12432, PG 37668. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 371 | personaje | Mephisto: 6★ maestría 1, nivel 60/60, tier 3, potencial 0: ataque de energía 13805, def. física 9937, def. de energía 12567, PG 38088. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 372 | personaje | Mephisto: 6★ maestría 2, nivel 60/60, tier 3, potencial 0: ataque de energía 13965, def. física 10048, def. de energía 12702, PG 38509. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 373 | personaje | Mephisto: 6★ maestría 3, nivel 60/60, tier 3, potencial 0: ataque de energía 14125, def. física 10159, def. de energía 12836, PG 38929. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 374 | personaje | Mephisto: 6★ maestría 4, nivel 60/60, tier 3, potencial 0: ataque de energía 14285, def. física 10270, def. de energía 12971, PG 39349. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 375 | personaje | Mephisto: 6★ maestría 5, nivel 60/60, tier 3, potencial 0: ataque de energía 14446, def. física 10381, def. de energía 13105, PG 39770. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 376 | personaje | Mephisto: 6★ maestría 6, nivel 60/60, tier 3, potencial 0: ataque de energía 14606, def. física 10493, def. de energía 13240, PG 40190. | `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 377 | personaje | Mephisto: 6★ maestría 6, nivel 80/80, tier 4, potencial 12: ataque de energía 23551, def. física 16065, def. de energía 19447, PG 57814. | `fuentes/juego-ko/ficha.json`, `fuentes/progresion/mephisto.csv`, `crudo/ko/k6.jsonl` |
| 378 | striker | 도감 영웅 정보 · 메피스토 | `fuentes/juego-ko/ficha.json`, `crudo/ko/k6.jsonl` |
| 379 | striker | 도감 영웅 정보 · 메피스토 | `crudo/ko/k6.jsonl` |
| 380 | striker | 도감 영웅 정보 · 메피스토 | `crudo/ko/k6.jsonl` |
| 381 | striker | 도감 영웅 정보 · 메피스토 | `crudo/ko/k6.jsonl` |
| 382 | striker | 도감 영웅 정보 · 메피스토 | `crudo/ko/k6.jsonl` |
| 383 | striker | 도감 영웅 정보 · 메피스토 | `crudo/ko/k6.jsonl` |
| 384 | striker | 도감 영웅 정보 · 메피스토 | `crudo/ko/k6.jsonl` |
| 385 | striker | 도감 영웅 정보 · 메피스토 | `crudo/ko/k6.jsonl` |

## Progresión de Galactus

| N.º | Pantalla | Qué muestra | Transcripción |
|---|---|---|---|
| 0 | ficha · stats | Galactus: 1★, nivel 1/40, tier 3, potencial 0: ataque de energía 82, def. física 56, def. de energía 62, PG 430. | `fuentes/progresion/galactus.csv` |
| 1 | ficha · stats | Galactus: 2★, nivel 1/40, tier 3, potencial 0: ataque de energía 105, def. física 70, def. de energía 76, PG 523. | `fuentes/progresion/galactus.csv` |
| 2 | ficha · stats | Galactus: 3★, nivel 1/45, tier 3, potencial 0: ataque de energía 119, def. física 83, def. de energía 90, PG 612. | `fuentes/progresion/galactus.csv` |
| 3 | ficha · stats | Galactus: 4★, nivel 1/50, tier 3, potencial 0: ataque de energía 139, def. física 93, def. de energía 104, PG 707. | `fuentes/progresion/galactus.csv` |
| 4 | ficha · stats | Galactus: 5★, nivel 2/55, tier 3, potencial 0: ataque de energía 313, def. física 209, def. de energía 228, PG 1531. | `fuentes/progresion/galactus.csv` |
| 5 | ficha · stats | Galactus: 5★, nivel 1/55, tier 3, potencial 0: ataque de energía 159, def. física 107, def. de energía 118, PG 800. | `fuentes/progresion/galactus.csv` |
| 6 | ficha · stats | Galactus: 6★, nivel 1/60, tier 3, potencial 0: ataque de energía 175, def. física 116, def. de energía 128, PG 894. | `fuentes/progresion/galactus.csv` |
| 7 | ficha · stats | Galactus: 6★, nivel 2/60, tier 3, potencial 0: ataque de energía 345, def. física 233, def. de energía 252, PG 1713. | `fuentes/progresion/galactus.csv` |
| 8 | ficha · stats | Galactus: 6★, nivel 3/60, tier 3, potencial 0: ataque de energía 520, def. física 349, def. de energía 376, PG 2457. | `fuentes/progresion/galactus.csv` |
| 9 | ficha · stats | Galactus: 6★, nivel 6/60, tier 3, potencial 0: ataque de energía 1035, def. física 699, def. de energía 751, PG 4244. | `fuentes/progresion/galactus.csv` |
| 10 | ficha · stats | Galactus: 6★, nivel 7/60, tier 3, potencial 0: ataque de energía 1205, def. física 815, def. de energía 879, PG 4691. | `fuentes/progresion/galactus.csv` |
| 11 | ficha · stats | Galactus: 6★, nivel 8/60, tier 3, potencial 0: ataque de energía 1380, def. física 932, def. de energía 1003, PG 5063. | `fuentes/progresion/galactus.csv` |
| 12 | ficha · stats | Galactus: 6★, nivel 9/60, tier 3, potencial 0: ataque de energía 1550, def. física 1048, def. de energía 1127, PG 5361. | `fuentes/progresion/galactus.csv` |
| 13 | ficha · stats | Galactus: 6★, nivel 10/60, tier 3, potencial 0: ataque de energía 1808, def. física 1210, def. de energía 1301, PG 5865. | `fuentes/progresion/galactus.csv` |
| 14 | ficha · stats | Galactus: 6★, nivel 11/60, tier 3, potencial 0: ataque de energía 1983, def. física 1331, def. de energía 1429, PG 5996. | `fuentes/progresion/galactus.csv` |
| 15 | ficha · stats | Galactus: 6★, nivel 12/60, tier 3, potencial 0: ataque de energía 2153, def. física 1452, def. de energía 1562, PG 6517. | `fuentes/progresion/galactus.csv` |
| 16 | ficha · stats | Galactus: 6★, nivel 13/60, tier 3, potencial 0: ataque de energía 2323, def. física 1572, def. de energía 1690, PG 7039. | `fuentes/progresion/galactus.csv` |
| 17 | ficha · stats | Galactus: 6★, nivel 14/60, tier 3, potencial 0: ataque de energía 2498, def. física 1693, def. de energía 1818, PG 7560. | `fuentes/progresion/galactus.csv` |
| 18 | ficha · stats | Galactus: 6★, nivel 15/60, tier 3, potencial 0: ataque de energía 2755, def. física 1882, def. de energía 2020, PG 8340. | `fuentes/progresion/galactus.csv` |
| 19 | ficha · stats | Galactus: 6★, nivel 16/60, tier 3, potencial 0: ataque de energía 2926, def. física 2007, def. de energía 2157, PG 8861. | `fuentes/progresion/galactus.csv` |
| 20 | ficha · stats | Galactus: 6★, nivel 17/60, tier 3, potencial 0: ataque de energía 3100, def. física 2132, def. de energía 2290, PG 9382. | `fuentes/progresion/galactus.csv` |
| 21 | ficha · stats | Galactus: 6★, nivel 18/60, tier 3, potencial 0: ataque de energía 3271, def. física 2258, def. de energía 2427, PG 9903. | `fuentes/progresion/galactus.csv` |
| 22 | ficha · stats | Galactus: 6★, nivel 19/60, tier 3, potencial 0: ataque de energía 3441, def. física 2383, def. de energía 2560, PG 10424. | `fuentes/progresion/galactus.csv` |
| 23 | ficha · stats | Galactus: 6★, nivel 20/60, tier 3, potencial 0: ataque de energía 3703, def. física 2598, def. de energía 2789, PG 11208. | `fuentes/progresion/galactus.csv` |
| 24 | ficha · stats | Galactus: 6★, nivel 21/60, tier 3, potencial 0: ataque de energía 3873, def. física 2728, def. de energía 2931, PG 11730. | `fuentes/progresion/galactus.csv` |
| 25 | ficha · stats | Galactus: 6★, nivel 22/60, tier 3, potencial 0: ataque de energía 4043, def. física 2858, def. de energía 3069, PG 12251. | `fuentes/progresion/galactus.csv` |
| 26 | ficha · stats | Galactus: 6★, nivel 23/60, tier 3, potencial 0: ataque de energía 4218, def. física 2988, def. de energía 3211, PG 12772. | `fuentes/progresion/galactus.csv` |
| 27 | ficha · stats | Galactus: 6★, nivel 24/60, tier 3, potencial 0: ataque de energía 4388, def. física 3118, def. de energía 3348, PG 13293. | `fuentes/progresion/galactus.csv` |
| 28 | ficha · stats | Galactus: 6★, nivel 25/60, tier 3, potencial 0: ataque de energía 4646, def. física 3360, def. de energía 3609, PG 14073. | `fuentes/progresion/galactus.csv` |
| 29 | ficha · stats | Galactus: 6★, nivel 26/60, tier 3, potencial 0: ataque de energía 4821, def. física 3494, def. de energía 3751, PG 14594. | `fuentes/progresion/galactus.csv` |
| 30 | ficha · stats | Galactus: 6★, nivel 27/60, tier 3, potencial 0: ataque de energía 4991, def. física 3629, def. de energía 3898, PG 15115. | `fuentes/progresion/galactus.csv` |
| 31 | ficha · stats | Galactus: 6★, nivel 28/60, tier 3, potencial 0: ataque de energía 5161, def. física 3763, def. de energía 4040, PG 15637. | `fuentes/progresion/galactus.csv` |
| 32 | ficha · stats | Galactus: 6★, nivel 29/60, tier 3, potencial 0: ataque de energía 5336, def. física 3898, def. de energía 4186, PG 16158. | `fuentes/progresion/galactus.csv` |
| 33 | ficha · stats | Galactus: 6★, nivel 30/60, tier 3, potencial 0: ataque de energía 5594, def. física 4166, def. de energía 4475, PG 16942. | `fuentes/progresion/galactus.csv` |
| 34 | ficha · stats | Galactus: 6★, nivel 31/60, tier 3, potencial 0: ataque de energía 5764, def. física 4305, def. de energía 4626, PG 17463. | `fuentes/progresion/galactus.csv` |
| 35 | ficha · stats | Galactus: 6★, nivel 32/60, tier 3, potencial 0: ataque de energía 5939, def. física 4444, def. de energía 4772, PG 17984. | `fuentes/progresion/galactus.csv` |
| 36 | ficha · stats | Galactus: 6★, nivel 33/60, tier 3, potencial 0: ataque de energía 6109, def. física 4583, def. de energía 4924, PG 18506. | `fuentes/progresion/galactus.csv` |
| 37 | ficha · stats | Galactus: 6★, nivel 34/60, tier 3, potencial 0: ataque de energía 6284, def. física 4722, def. de energía 5070, PG 19027. | `fuentes/progresion/galactus.csv` |
| 38 | ficha · stats | Galactus: 6★, nivel 35/60, tier 3, potencial 0: ataque de energía 6541, def. física 5018, def. de energía 5386, PG 19806. | `fuentes/progresion/galactus.csv` |
| 39 | ficha · stats | Galactus: 6★, nivel 36/60, tier 3, potencial 0: ataque de energía 6711, def. física 5161, def. de energía 5542, PG 20328. | `fuentes/progresion/galactus.csv` |
| 40 | ficha · stats | Galactus: 6★, nivel 37/60, tier 3, potencial 0: ataque de energía 6882, def. física 5304, def. de energía 5698, PG 20849. | `fuentes/progresion/galactus.csv` |
| 41 | ficha · stats | Galactus: 6★, nivel 38/60, tier 3, potencial 0: ataque de energía 7056, def. física 5448, def. de energía 5849, PG 21370. | `fuentes/progresion/galactus.csv` |
| 42 | ficha · stats | Galactus: 6★, nivel 39/60, tier 3, potencial 0: ataque de energía 7227, def. física 5591, def. de energía 6004, PG 21891. | `fuentes/progresion/galactus.csv` |
| 43 | ficha · stats | Galactus: 6★, nivel 40/60, tier 3, potencial 0: ataque de energía 7484, def. física 5914, def. de energía 6348, PG 22675. | `fuentes/progresion/galactus.csv` |
| 44 | ficha · stats | Galactus: 6★, nivel 41/60, tier 3, potencial 0: ataque de energía 7659, def. física 6061, def. de energía 6508, PG 23196. | `fuentes/progresion/galactus.csv` |
| 45 | ficha · stats | Galactus: 6★, nivel 42/60, tier 3, potencial 0: ataque de energía 7829, def. física 6209, def. de energía 6668, PG 23718. | `fuentes/progresion/galactus.csv` |
| 46 | ficha · stats | Galactus: 6★, nivel 43/60, tier 3, potencial 0: ataque de energía 8004, def. física 6357, def. de energía 6824, PG 24239. | `fuentes/progresion/galactus.csv` |
| 47 | ficha · stats | Galactus: 6★, nivel 43/60, tier 3, potencial 0: ataque de energía 8004, def. física 6357, def. de energía 6824, PG 24239. | `fuentes/progresion/galactus.csv` |
| 48 | ficha · stats | Galactus: 6★, nivel 44/60, tier 3, potencial 0: ataque de energía 8174, def. física 6505, def. de energía 6985, PG 24760. | `fuentes/progresion/galactus.csv` |
| 49 | ficha · stats | Galactus: 6★, nivel 46/60, tier 3, potencial 0: ataque de energía 8602, def. física 7007, def. de energía 7525, PG 26061. | `fuentes/progresion/galactus.csv` |
| 50 | ficha · stats | Galactus: 6★, nivel 47/60, tier 3, potencial 0: ataque de energía 8777, def. física 7159, def. de energía 7685, PG 26582. | `fuentes/progresion/galactus.csv` |
| 51 | ficha · stats | Galactus: 6★, nivel 48/60, tier 3, potencial 0: ataque de energía 8947, def. física 7311, def. de energía 7850, PG 27103. | `fuentes/progresion/galactus.csv` |
| 52 | ficha · stats | Galactus: 6★, nivel 49/60, tier 3, potencial 0: ataque de energía 9122, def. física 7464, def. de energía 8015, PG 27625. | `fuentes/progresion/galactus.csv` |
| 53 | ficha · stats | Galactus: 6★, nivel 50/60, tier 3, potencial 0: ataque de energía 9379, def. física 7840, def. de energía 8418, PG 28409. | `fuentes/progresion/galactus.csv` |
| 54 | ficha · stats | Galactus: 6★, nivel 51/60, tier 3, potencial 0: ataque de energía 9738, def. física 7997, def. de energía 8588, PG 29504. | `fuentes/progresion/galactus.csv` |
| 55 | ficha · stats | Galactus: 6★, nivel 52/60, tier 3, potencial 0: ataque de energía 10115, def. física 8387, def. de energía 9004, PG 30651. | `fuentes/progresion/galactus.csv` |
| 56 | ficha · stats | Galactus: 6★, nivel 53/60, tier 3, potencial 0: ataque de energía 10511, def. física 8548, def. de energía 9178, PG 31847. | `fuentes/progresion/galactus.csv` |
| 57 | ficha · stats | Galactus: 6★, nivel 54/60, tier 3, potencial 0: ataque de energía 10925, def. física 8951, def. de energía 9609, PG 33100. | `fuentes/progresion/galactus.csv` |
| 58 | ficha · stats | Galactus: 6★, nivel 55/60, tier 3, potencial 0: ataque de energía 11270, def. física 9117, def. de energía 9787, PG 34142. | `fuentes/progresion/galactus.csv` |
| 59 | ficha · stats | Galactus: 6★, nivel 55/60, tier 3, potencial 0: ataque de energía 11270, def. física 9117, def. de energía 9787, PG 34142. | `fuentes/progresion/galactus.csv` |
| 60 | ficha · stats | Galactus: 6★, nivel 56/60, tier 3, potencial 0: ataque de energía 11716, def. física 9533, def. de energía 10236, PG 35496. | `fuentes/progresion/galactus.csv` |
| 61 | ficha · stats | Galactus: 6★, nivel 57/60, tier 3, potencial 0: ataque de energía 12181, def. física 9704, def. de energía 10420, PG 36906. | `fuentes/progresion/galactus.csv` |
| 62 | ficha · stats | Galactus: 6★, nivel 58/60, tier 3, potencial 0: ataque de energía 12664, def. física 10134, def. de energía 10882, PG 38364. | `fuentes/progresion/galactus.csv` |
| 63 | ficha · stats | Galactus: 6★, nivel 59/60, tier 3, potencial 0: ataque de energía 13165, def. física 10308, def. de energía 11070, PG 39876. | `fuentes/progresion/galactus.csv` |
| 64 | ficha · stats | Galactus: 6★, nivel 60/60, tier 3, potencial 0: ataque de energía 13506, def. física 10483, def. de energía 11253, PG 40918. | `fuentes/progresion/galactus.csv` |
| 65 | ficha · stats | Galactus: 6★ maestría 1, nivel 60/60, tier 3, potencial 0: ataque de energía 13652, def. física 10600, def. de energía 11376, PG 41385. | `fuentes/progresion/galactus.csv` |
| 66 | ficha · stats | Galactus: 6★ maestría 2, nivel 60/60, tier 3, potencial 0: ataque de energía 13799, def. física 10717, def. de energía 11499, PG 41852. | `fuentes/progresion/galactus.csv` |
| 67 | ficha · stats | Galactus: 6★ maestría 3, nivel 60/60, tier 3, potencial 0: ataque de energía 13946, def. física 10834, def. de energía 11622, PG 42319. | `fuentes/progresion/galactus.csv` |
| 68 | ficha · stats | Galactus: 6★ maestría 4, nivel 60/60, tier 3, potencial 0: ataque de energía 14093, def. física 10951, def. de energía 11744, PG 42786. | `fuentes/progresion/galactus.csv` |
| 69 | ficha · stats | Galactus: 6★ maestría 5, nivel 60/60, tier 3, potencial 0: ataque de energía 14240, def. física 11068, def. de energía 11867, PG 43253. | `fuentes/progresion/galactus.csv` |
| 70 | ficha · stats | Galactus: 6★ maestría 6, nivel 60/60, tier 3, potencial 0: ataque de energía 14386, def. física 11185, def. de energía 11990, PG 43721. | `fuentes/progresion/galactus.csv` |
| 71 | ficha · stats | Galactus: 6★ maestría 6, nivel 60/60, tier 3, potencial 1: ataque de energía 14386, def. física 11185, def. de energía 11990, PG 43721. | `fuentes/progresion/galactus.csv` |
| 72 | ficha · stats | Galactus: 6★ maestría 6, nivel 62/62, tier 3, potencial 2: ataque de energía 14754, def. física 11558, def. de energía 12390, PG 44834. | `fuentes/progresion/galactus.csv` |
| 73 | ficha · stats | Galactus: 6★ maestría 6, nivel 64/64, tier 3, potencial 3: ataque de energía 15121, def. física 11931, def. de energía 12790, PG 45948. | `fuentes/progresion/galactus.csv` |
| 74 | ficha · stats | Galactus: 6★ maestría 6, nivel 66/66, tier 3, potencial 4: ataque de energía 15489, def. física 12304, def. de energía 13191, PG 47062. | `fuentes/progresion/galactus.csv` |
| 75 | ficha · stats | Galactus: 6★ maestría 6, nivel 68/68, tier 3, potencial 5: ataque de energía 15856, def. física 12677, def. de energía 13591, PG 48176. | `fuentes/progresion/galactus.csv` |
| 76 | ficha · stats | Galactus: 6★ maestría 6, nivel 70/70, tier 3, potencial 6: ataque de energía 16219, def. física 13049, def. de energía 13991, PG 49290. | `fuentes/progresion/galactus.csv` |
| 77 | ficha · stats | Galactus: 6★ maestría 6, nivel 70/70, tier 3, potencial 7: ataque de energía 16219, def. física 13049, def. de energía 13991, PG 49290. | `fuentes/progresion/galactus.csv` |
| 78 | ficha · stats | Galactus: 6★ maestría 6, nivel 72/72, tier 3, potencial 8: ataque de energía 16587, def. física 13422, def. de energía 14391, PG 50404. | `fuentes/progresion/galactus.csv` |
| 79 | ficha · stats | Galactus: 6★ maestría 6, nivel 74/74, tier 3, potencial 9: ataque de energía 16954, def. física 13795, def. de energía 14791, PG 51517. | `fuentes/progresion/galactus.csv` |
| 80 | ficha · stats | Galactus: 6★ maestría 6, nivel 76/76, tier 3, potencial 10: ataque de energía 17322, def. física 14168, def. de energía 15191, PG 52631. | `fuentes/progresion/galactus.csv` |
| 81 | ficha · stats | Galactus: 6★ maestría 6, nivel 78/78, tier 3, potencial 11: ataque de energía 17689, def. física 14541, def. de energía 15592, PG 53745. | `fuentes/progresion/galactus.csv` |
| 82 | ficha · stats | Galactus: 6★ maestría 6, nivel 80/80, tier 3, potencial 12: ataque de energía 18052, def. física 14914, def. de energía 15987, PG 54859. | `fuentes/progresion/galactus.csv` |
| 83 | ficha · stats | Galactus: 6★ maestría 6, nivel 80/80, tier 4, potencial 12: ataque de energía 20630, def. física 16786, def. de energía 17952, PG 65409. | `fuentes/progresion/galactus.csv` |

## Inglés (sin imágenes)

| N.º | Pantalla | Qué muestra | Transcripción |
|---|---|---|---|
| 1 | guia | TEAM · RECRUIT | `crudo/en/guias-a.jsonl` |
| 2 | guia | TEAM · TYPE AFFINITY | `crudo/en/guias-a.jsonl` |
| 3 | guia | TEAM · UNIFORM | `crudo/en/guias-a.jsonl` |
| 4 | guia | TEAM · TEAM BONUS | `crudo/en/guias-a.jsonl` |
| 5 | guia | TEAM · INSTINCT | `crudo/en/guias-a.jsonl` |
| 6 | guia | TEAM · SIDE | `crudo/en/guias-a.jsonl` |
| 7 | guia | GEAR GROWTH · GEAR | `crudo/en/guias-a.jsonl` |
| 8 | guia | GEAR GROWTH · ENHANCE ISO-8 | `crudo/en/guias-a.jsonl` |
| 9 | guia | GEAR GROWTH · COMBINE ISO-8 | `crudo/en/guias-a.jsonl` |
| 10 | guia | GEAR GROWTH · ISO-8 SET BONUS | `crudo/en/guias-a.jsonl` |
| 11 | guia | GEAR GROWTH · AWAKEN ISO-8 | `crudo/en/guias-a.jsonl` |
| 12 | guia | GEAR GROWTH · COMIC CARD UPGRADE | `crudo/en/guias-a.jsonl` |
| 13 | guia | GEAR GROWTH · COMIC CARD CRAFTING | `crudo/en/guias-a.jsonl` |
| 14 | guia | GEAR GROWTH · ENHANCE ARTIFACT | `crudo/en/guias-a.jsonl` |
| 15 | guia | GEAR GROWTH · TRANSFER ARTIFACT ENHANCE | `crudo/en/guias-a.jsonl` |
| 16 | guia | GEAR GROWTH · DISMANTLE ARTIFACT | `crudo/en/guias-a.jsonl` |
| 17 | guia | GEAR GROWTH · ENCHANT SWORD | `crudo/en/guias-a.jsonl` |
| 18 | guia | GEAR GROWTH · DISMANTLING SWORDS | `crudo/en/guias-a.jsonl` |
| 19 | guia | GEAR GROWTH · CUSTOM GEAR RANK UP | `crudo/en/guias-a.jsonl` |
| 20 | guia | GEAR GROWTH · C.T.P. REFORGING | `crudo/en/guias-a.jsonl` |
| 21 | guia | GEAR GROWTH · URU AMPLIFICATION | `crudo/en/guias-a.jsonl` |
| 22 | guia | GEAR GROWTH · URU COMBINATION | `crudo/en/guias-a.jsonl` |
| 23 | guia | GEAR GROWTH · Uru Awakening | `crudo/en/guias-a.jsonl` |
| 24 | guia | GEAR GROWTH · J.A.R.V.I.S. Enhance | `crudo/en/guias-a.jsonl` |
| 25 | guia | GEAR GROWTH · Change J.A.R.V.I.S. Option | `crudo/en/guias-a.jsonl` |
| 26 | glosario | CONTENT GLOSSARY · STORY | `crudo/en/guias-a.jsonl` |
| 27 | glosario | CONTENT GLOSSARY · EPIC QUEST | `crudo/en/guias-a.jsonl` |
| 28 | glosario | CONTENT GLOSSARY · EPIC QUEST | `crudo/en/guias-a.jsonl` |
| 29 | glosario | CONTENT GLOSSARY · DIMENSION MISSION | `crudo/en/guias-a.jsonl` |
| 30 | glosario | CONTENT GLOSSARY · DISPATCH MISSION | `crudo/en/guias-a.jsonl` |
| 31 | glosario | CONTENT GLOSSARY · TIMELINE BATTLE | `crudo/en/guias-a.jsonl` |
| 32 | glosario | CONTENT GLOSSARY · ALLIANCE BATTLE | `crudo/en/guias-a.jsonl` |
| 33 | glosario | CONTENT GLOSSARY · OTHERWORLD BATTLE | `crudo/en/guias-a.jsonl` |
| 34 | glosario | CONTENT GLOSSARY · WORLD BOSS | `crudo/en/guias-a.jsonl` |
| 35 | glosario | CONTENT GLOSSARY · WORLD BOSS | `crudo/en/guias-a.jsonl` |
| 36 | glosario | CONTENT GLOSSARY · MULTIVERSE SAGA | `crudo/en/guias-a.jsonl` |
| 37 | glosario | CONTENT GLOSSARY · SHADOWLAND | `crudo/en/guias-a.jsonl` |
| 38 | glosario | CONTENT GLOSSARY · ALLIANCE TOURNAMENT | `crudo/en/guias-a.jsonl` |
| 39 | glosario | CONTENT GLOSSARY · LEGENDARY BATTLE | `crudo/en/guias-a.jsonl` |
| 40 | glosario | CONTENT GLOSSARY · ALLIANCE CONQUEST | `crudo/en/guias-a.jsonl` |
| 41 | glosario | CONTENT GLOSSARY · ALLIANCE CONQUEST | `crudo/en/guias-a.jsonl` |
| 42 | glosario | CONTENT GLOSSARY · GIANT BOSS RAID | `crudo/en/guias-a.jsonl` |
| 43 | glosario | CONTENT GLOSSARY · WORLD EVENT | `crudo/en/guias-a.jsonl` |
| 44 | glosario | CONTENT GLOSSARY · TIMELINE SURVIVAL | `crudo/en/guias-a.jsonl` |
| 45 | glosario | CONTENT GLOSSARY · DIMENSION RIFT | `crudo/en/guias-a.jsonl` |
| 46 | glosario | CONTENT GLOSSARY · DIMENSION RIFT | `crudo/en/guias-a.jsonl` |
| 47 | glosario | CONTENT GLOSSARY · ZOMBIE SURVIVAL | `crudo/en/guias-a.jsonl` |
| 48 | glosario | CONTENT GLOSSARY · ZOMBIE SURVIVAL | `crudo/en/guias-a.jsonl` |
| 49 | glosario | CONTENT GLOSSARY · TEAM BATTLE ARENA | `crudo/en/guias-a.jsonl` |
| 50 | guia | CHARACTER GROWTH · CHARACTER LEVEL | `crudo/en/guias-b.jsonl` |
| 51 | guia | CHARACTER GROWTH · RANK UP | `crudo/en/guias-b.jsonl` |
| 52 | guia | CHARACTER GROWTH · MASTERY | `crudo/en/guias-b.jsonl` |
| 53 | guia | CHARACTER GROWTH · TIER-2 ADVANCEMENT | `crudo/en/guias-b.jsonl` |
| 54 | guia | CHARACTER GROWTH · SKILLS | `crudo/en/guias-b.jsonl` |
| 55 | guia | CHARACTER GROWTH · EQUIP ISO-8 | `crudo/en/guias-b.jsonl` |
| 56 | guia | CHARACTER GROWTH · EQUIP CUSTOM GEAR | `crudo/en/guias-b.jsonl` |
| 57 | guia | CHARACTER GROWTH · EQUIP COMIC CARD | `crudo/en/guias-b.jsonl` |
| 58 | guia | CHARACTER GROWTH · EQUIP ENCHANTED URU | `crudo/en/guias-b.jsonl` |
| 59 | guia | CHARACTER GROWTH · UNIFORM UPGRADE | `crudo/en/guias-b.jsonl` |
| 60 | guia | CHARACTER GROWTH · POTENTIAL | `crudo/en/guias-b.jsonl` |
| 61 | guia | CHARACTER GROWTH · POTENTIAL | `crudo/en/guias-b.jsonl` |
| 62 | guia | CHARACTER GROWTH · POTENTIAL AWAKENING | `crudo/en/guias-b.jsonl` |
| 63 | guia | CHARACTER GROWTH · TRANSCEND POTENTIAL | `crudo/en/guias-b.jsonl` |
| 64 | guia | CHARACTER GROWTH · TIER-3 ADVANCEMENT | `crudo/en/guias-b.jsonl` |
| 65 | guia | CHARACTER GROWTH · TIER-4 ADVANCEMENT | `crudo/en/guias-b.jsonl` |
| 66 | guia | CHARACTER GROWTH · RAID LEVEL | `crudo/en/guias-b.jsonl` |
| 67 | guia | CHARACTER GROWTH · TYPE ENHANCEMENT | `crudo/en/guias-b.jsonl` |
| 68 | guia | CHARACTER GROWTH · AGENT LEVEL | `crudo/en/guias-b.jsonl` |
| 69 | guia | CHARACTER GROWTH · AGENT LEVEL | `crudo/en/guias-b.jsonl` |
| 70 | guia | CHARACTER GROWTH · S.H.I.E.L.D. ARCHIVE | `crudo/en/guias-b.jsonl` |
| 71 | guia | CHARACTER GROWTH · TEAM-UP COLLECTION | `crudo/en/guias-b.jsonl` |
| 72 | guia | CHARACTER GROWTH · EMBLEM COLLECTION | `crudo/en/guias-b.jsonl` |
| 73 | guia | CHARACTER GROWTH · Elite Gear | `crudo/en/guias-b.jsonl` |
| 74 | guia | CHARACTER GROWTH · Elite Gear | `crudo/en/guias-b.jsonl` |
| 75 | guia | CHARACTER GROWTH · J.A.R.V.I.S. | `crudo/en/guias-b.jsonl` |
| 76 | guia | CHARACTER GROWTH · J.A.R.V.I.S. | `crudo/en/guias-b.jsonl` |
| 77 | glosario | ITEM GLOSSARY · BIOMETRICS | `crudo/en/items.jsonl` |
| 78 | glosario | ITEM GLOSSARY · ISO-8 | `crudo/en/items.jsonl` |
| 79 | glosario | ITEM GLOSSARY · NORN STONE | `crudo/en/items.jsonl` |
| 80 | glosario | ITEM GLOSSARY · GEAR UP KIT | `crudo/en/items.jsonl` |
| 81 | glosario | ITEM GLOSSARY · COMPONENT PACK | `crudo/en/items.jsonl` |
| 82 | glosario | ITEM GLOSSARY · STARK-BRANDED BLUEPRINT | `crudo/en/items.jsonl` |
| 83 | glosario | ITEM GLOSSARY · COMIC CARDS | `crudo/en/items.jsonl` |
| 84 | glosario | ITEM GLOSSARY · ARTIFACT | `crudo/en/items.jsonl` |
| 85 | glosario | ITEM GLOSSARY · CELESTIAL ESSENCE | `crudo/en/items.jsonl` |
| 86 | glosario | ITEM GLOSSARY · SWORD | `crudo/en/items.jsonl` |
| 87 | glosario | ITEM GLOSSARY · ENCHANTMENT RUNE | `crudo/en/items.jsonl` |
| 88 | glosario | ITEM GLOSSARY · CUSTOM GEAR | `crudo/en/items.jsonl` |
| 89 | glosario | ITEM GLOSSARY · NORN STONE OF CHAOS | `crudo/en/items.jsonl` |
| 90 | glosario | ITEM GLOSSARY · BLACK ANTI-MATTER | `crudo/en/items.jsonl` |
| 91 | glosario | ITEM GLOSSARY · ENCHANTED URU | `crudo/en/items.jsonl` |
| 92 | glosario | ITEM GLOSSARY · M'KRAAN SHARD | `crudo/en/items.jsonl` |
| 93 | glosario | ITEM GLOSSARY · M'KRAAN CRYSTAL | `crudo/en/items.jsonl` |
| 94 | glosario | ITEM GLOSSARY · PHOENIX FEATHER | `crudo/en/items.jsonl` |
| 95 | glosario | ITEM GLOSSARY · X-GENE | `crudo/en/items.jsonl` |
| 96 | glosario | ITEM GLOSSARY · COSMIC CUBE FRAGMENT | `crudo/en/items.jsonl` |
| 97 | glosario | ITEM GLOSSARY · ESSENCE OF DIMENSION | `crudo/en/items.jsonl` |
| 98 | glosario | ITEM GLOSSARY · TITAN COMPONENT PACK | `crudo/en/items.jsonl` |
| 99 | glosario | ITEM GLOSSARY · TITAN'S RECORD | `crudo/en/items.jsonl` |
| 100 | glosario | ITEM GLOSSARY · TYPE ENHANCEMENT KIT | `crudo/en/items.jsonl` |
| 101 | glosario | ITEM GLOSSARY · TYPE ENHANCEMENT KIT | `crudo/en/items.jsonl` |
| 102 | glosario | ITEM GLOSSARY · AWAKENING CRYSTAL | `crudo/en/items.jsonl` |
| 103 | glosario | ITEM GLOSSARY · MANDALAY GEM FRAGMENT | `crudo/en/items.jsonl` |
| 104 | glosario | ITEM GLOSSARY · STORY FRAGMENT | `crudo/en/items.jsonl` |
| 105 | glosario | ITEM GLOSSARY · C.T.P. REFORGING CORE | `crudo/en/items.jsonl` |
| 106 | glosario | ITEM GLOSSARY · CARD CRAFTING CUBE | `crudo/en/items.jsonl` |
| 107 | glosario | ITEM GLOSSARY · DIMENSION RIFT SUMMON STONE | `crudo/en/items.jsonl` |
| 108 | glosario | ITEM GLOSSARY · BOOK OF THE VISHANTI | `crudo/en/items.jsonl` |
| 109 | glosario | ITEM GLOSSARY · LIFE SEED | `crudo/en/items.jsonl` |
| 110 | glosario | ITEM GLOSSARY · CARBONADIUM | `crudo/en/items.jsonl` |
| 111 | glosario | ITEM GLOSSARY · SOUL OF THE FALTINE | `crudo/en/items.jsonl` |
| 112 | glosario | ITEM GLOSSARY · Eternal Flame | `crudo/en/items.jsonl` |
| 113 | glosario | ITEM GLOSSARY · POWER OF DEMIURGE | `crudo/en/items.jsonl` |
| 114 | glosario | ITEM GLOSSARY · GODSTONE | `crudo/en/items.jsonl` |
| 115 | glosario | ITEM GLOSSARY · EMBLEM DATA | `crudo/en/items.jsonl` |
| 116 | glosario | ITEM GLOSSARY · EMBLEM ENHANCEMENT KIT | `crudo/en/items.jsonl` |
| 117 | glosario | ITEM GLOSSARY · J.A.R.V.I.S. Data | `crudo/en/items.jsonl` |
| 118 | glosario | ITEM GLOSSARY · J.A.R.V.I.S. Data Shard | `crudo/en/items.jsonl` |
| 119 | glosario | SKILL NAME GLOSSARY · GUARD BREAK | `crudo/en/glosario-en.jsonl` |
| 120 | glosario | SKILL NAME GLOSSARY · GUARANTEED DODGE RATE | `crudo/en/glosario-en.jsonl` |
| 121 | glosario | SKILL NAME GLOSSARY · GUARANTEED CRITICAL RATE | `crudo/en/glosario-en.jsonl` |
| 122 | glosario | SKILL NAME GLOSSARY · PURE DAMAGE | `crudo/en/glosario-en.jsonl` |
| 123 | glosario | SKILL NAME GLOSSARY · TEAM PASSIVE | `crudo/en/glosario-en.jsonl` |
| 124 | glosario | SKILL NAME GLOSSARY · TEAM PASSIVE | `crudo/en/glosario-en.jsonl` |
| 125 | glosario | SKILL NAME GLOSSARY · INVINCIBLE | `crudo/en/glosario-en.jsonl` |
| 126 | glosario | SKILL NAME GLOSSARY · SUPER ARMOR | `crudo/en/glosario-en.jsonl` |
| 127 | glosario | SKILL NAME GLOSSARY · BARRIER | `crudo/en/glosario-en.jsonl` |
| 128 | glosario | SKILL NAME GLOSSARY · SHIELD | `crudo/en/glosario-en.jsonl` |
| 129 | glosario | SKILL NAME GLOSSARY · DAMAGE IMMUNITY | `crudo/en/glosario-en.jsonl` |
| 130 | glosario | SKILL NAME GLOSSARY · FEAR | `crudo/en/glosario-en.jsonl` |
| 131 | glosario | SKILL NAME GLOSSARY · SNARE | `crudo/en/glosario-en.jsonl` |
| 132 | glosario | SKILL NAME GLOSSARY · TIME FREEZING | `crudo/en/glosario-en.jsonl` |
| 133 | glosario | SKILL NAME GLOSSARY · CHARM | `crudo/en/glosario-en.jsonl` |
| 134 | glosario | SKILL NAME GLOSSARY · IGNORE TARGETING | `crudo/en/glosario-en.jsonl` |
| 135 | glosario | SKILL NAME GLOSSARY · ENTICE | `crudo/en/glosario-en.jsonl` |
| 136 | glosario | SKILL NAME GLOSSARY · MIND CONTROL | `crudo/en/glosario-en.jsonl` |
| 137 | glosario | SKILL NAME GLOSSARY · RECHARGE SHIELD | `crudo/en/glosario-en.jsonl` |
| 138 | glosario | SKILL NAME GLOSSARY · FRACTURE | `crudo/en/glosario-en.jsonl` |
| 139 | glosario | SKILL NAME GLOSSARY · INCAPACITATION | `crudo/en/glosario-en.jsonl` |
| 140 | glosario | SKILL NAME GLOSSARY · COUNTERATTACK | `crudo/en/glosario-en.jsonl` |
| 141 | glosario | SKILL NAME GLOSSARY · ELASTICITY | `crudo/en/glosario-en.jsonl` |
| 142 | glosario | SKILL NAME GLOSSARY · CONCENTRATION | `crudo/en/glosario-en.jsonl` |
| 143 | glosario | SKILL NAME GLOSSARY · ADDITIONAL PIERCE DAMAGE | `crudo/en/glosario-en.jsonl` |
| 144 | glosario | SKILL NAME GLOSSARY · PENETRATION | `crudo/en/glosario-en.jsonl` |
| 145 | glosario | SKILL NAME GLOSSARY · BEATDOWN | `crudo/en/glosario-en.jsonl` |
| 146 | glosario | SKILL NAME GLOSSARY · TYPE AMPLIFICATION | `crudo/en/glosario-en.jsonl` |
| 147 | glosario | SKILL NAME GLOSSARY · STEEL | `crudo/en/glosario-en.jsonl` |
| 148 | glosario | SKILL NAME GLOSSARY · MOCKERY | `crudo/en/glosario-en.jsonl` |
| 149 | glosario | SKILL NAME GLOSSARY · STRIKE | `crudo/en/glosario-en.jsonl` |
| 150 | glosario | SKILL NAME GLOSSARY · AMBUSH | `crudo/en/glosario-en.jsonl` |
| 151 | glosario | SKILL NAME GLOSSARY · FORTITUDE | `crudo/en/glosario-en.jsonl` |
| 152 | glosario | SKILL NAME GLOSSARY · BLADE | `crudo/en/glosario-en.jsonl` |
| 153 | glosario | SKILL NAME GLOSSARY · DEFEND | `crudo/en/glosario-en.jsonl` |
| 154 | glosario | SKILL NAME GLOSSARY · SUPER HIT SHIELD | `crudo/en/glosario-en.jsonl` |
| 155 | glosario | SKILL NAME GLOSSARY · ENRAGED | `crudo/en/glosario-en.jsonl` |
| 156 | glosario | SKILL NAME GLOSSARY · ENRAGED | `crudo/en/glosario-en.jsonl` |
| 157 | glosario | SKILL NAME GLOSSARY · VITALITY | `crudo/en/glosario-en.jsonl` |
| 158 | glosario | SKILL NAME GLOSSARY · WALL | `crudo/en/glosario-en.jsonl` |
| 159 | glosario | SKILL NAME GLOSSARY · CLASH | `crudo/en/glosario-en.jsonl` |
| 160 | glosario | SKILL NAME GLOSSARY · PANIC | `crudo/en/glosario-en.jsonl` |
| 161 | glosario | SKILL NAME GLOSSARY · Loss | `crudo/en/glosario-en.jsonl` |
| 162 | glosario | SKILL NAME GLOSSARY · Death Throes | `crudo/en/glosario-en.jsonl` |
| 163 | glosario | SKILL NAME GLOSSARY · Mark | `crudo/en/glosario-en.jsonl` |
| 164 | glosario | SKILL NAME GLOSSARY · Fury | `crudo/en/glosario-en.jsonl` |
| 165 | coleccion | MARVEL UNIVERSE | `crudo/en/ctp.jsonl` |
| 166 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Competition | `crudo/en/ctp.jsonl` |
| 167 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Competition | `crudo/en/ctp.jsonl` |
| 168 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Competition | `crudo/en/ctp.jsonl` |
| 169 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Transcendence | `crudo/en/ctp.jsonl` |
| 170 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Authority | `crudo/en/ctp.jsonl` |
| 171 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Energy | `crudo/en/ctp.jsonl` |
| 172 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Destruction | `crudo/en/ctp.jsonl` |
| 173 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Patience | `crudo/en/ctp.jsonl` |
| 174 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Refinement | `crudo/en/ctp.jsonl` |
| 175 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Regeneration | `crudo/en/ctp.jsonl` |
| 176 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Rage | `crudo/en/ctp.jsonl` |
| 177 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Veteran | `crudo/en/ctp.jsonl` |
| 178 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Judgment | `crudo/en/ctp.jsonl` |
| 179 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Greed | `crudo/en/ctp.jsonl` |
| 180 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Insight | `crudo/en/ctp.jsonl` |
| 181 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Conquest | `crudo/en/ctp.jsonl` |
| 182 | ctp | CUSTOM GEAR L[cortado] · C.T.P. of Liberation | `crudo/en/ctp.jsonl` |
| 183 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Transcendence | `crudo/en/ctp.jsonl` |
| 184 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Authority | `crudo/en/ctp.jsonl` |
| 185 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Energy | `crudo/en/ctp.jsonl` |
| 186 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Destruction | `crudo/en/ctp.jsonl` |
| 187 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Patience | `crudo/en/ctp.jsonl` |
| 188 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Refinement | `crudo/en/ctp.jsonl` |
| 189 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Regeneration | `crudo/en/ctp.jsonl` |
| 190 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Refinement | `crudo/en/ctp.jsonl` |
| 191 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Rage | `crudo/en/ctp.jsonl` |
| 192 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Veteran | `crudo/en/ctp.jsonl` |
| 193 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Judgment | `crudo/en/ctp.jsonl` |
| 194 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Greed | `crudo/en/ctp.jsonl` |
| 195 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Insight | `crudo/en/ctp.jsonl` |
| 196 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Conquest | `crudo/en/ctp.jsonl` |
| 197 | ctp | CUSTOM GEAR L[cortado] · Mighty C.T.P. of Liberation | `crudo/en/ctp.jsonl` |
| 198 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Transcendence | `crudo/en/ctp.jsonl` |
| 199 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Transcendence | `crudo/en/ctp.jsonl` |
| 200 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Authority | `crudo/en/ctp.jsonl` |
| 201 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Energy | `crudo/en/ctp.jsonl` |
| 202 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Destruction | `crudo/en/ctp.jsonl` |
| 203 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Patience | `crudo/en/ctp.jsonl` |
| 204 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Refinement | `crudo/en/ctp.jsonl` |
| 205 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Regeneration | `crudo/en/ctp.jsonl` |
| 206 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Rage | `crudo/en/ctp.jsonl` |
| 207 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Veteran | `crudo/en/ctp.jsonl` |
| 208 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Judgment | `crudo/en/ctp.jsonl` |
| 209 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Greed | `crudo/en/ctp.jsonl` |
| 210 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Insight | `crudo/en/ctp.jsonl` |
| 211 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Conquest | `crudo/en/ctp.jsonl` |
| 212 | ctp | CUSTOM GEAR L[cortado] · Brilliant C.T.P. of Liberation | `crudo/en/ctp.jsonl` |
| 213 | equipo | MY TEAM · 5 | `crudo/en/equipos.jsonl` |
| 214 | striker | TEAM · INFO | `crudo/en/equipos.jsonl` |
| 215 | striker | TEAM · CHARACTER GEAR | `crudo/en/equipos.jsonl` |
| 216 | striker | TEAM · SKILL | `crudo/en/equipos.jsonl` |
| 217 | striker | TEAM · SET STRIKER | `crudo/en/equipos.jsonl` |
| 218 | striker | TEAM · TYPE | `crudo/en/equipos.jsonl` |
| 219 | striker | TEAM · ISO-8 | `crudo/en/equipos.jsonl` |
| 220 | striker | TEAM · ARTIFACT | `crudo/en/equipos.jsonl` |
| 221 | striker | TEAM · CUSTOM GEAR | `crudo/en/equipos.jsonl` |
| 222 | striker | TEAM · UNIFORM | `crudo/en/equipos.jsonl` |
| 223 | striker | TEAM · TYPE | `crudo/en/equipos.jsonl` |
| 224 | striker | TEAM · TYPE | `crudo/en/equipos.jsonl` |
| 225 | striker | TEAM · TYPE | `crudo/en/equipos.jsonl` |
| 226 | equipo | MY TEAM · 5 · Team Passive | `crudo/en/equipos.jsonl` |
| 227 | equipo | MY TEAM · 4 · Team Passive | `crudo/en/equipos.jsonl` |
| 228 | equipo | MY TEAM · 4 · Leader of X-Men | `crudo/en/equipos.jsonl` |
| 229 | equipo | MY TEAM · 4 · Guardian of the Deep | `crudo/en/equipos.jsonl` |
| 230 | equipo | MY TEAM · 4 · Jeff's Cuddle Buddy | `crudo/en/equipos.jsonl` |
| 231 | equipo | MY TEAM · 4 · Team Gear | `crudo/en/equipos.jsonl` |
| 232 | bonos | MY TEA [cortado] | `crudo/en/equipos.jsonl` |
| 233 | bonos | MY TEA [cortado] | `crudo/en/equipos.jsonl` |
| 234 | bonos | MY TEA [cortado] | `crudo/en/equipos.jsonl` |
| 235 | equipo | MY TEAM · 4 · All Effects | `crudo/en/equipos.jsonl` |
| 236 | equipo | MY TEAM · 4 · All Effects | `crudo/en/equipos.jsonl` |
| 237 | equipo | MY TEAM · 4 · All Effects | `crudo/en/equipos.jsonl` |
| 238 | equipo | MY TEAM · 4 · All Effects | `crudo/en/equipos.jsonl` |
| 239 | otro | AGENT LEVEL · ELITE AGENT | `crudo/en/guias-b.jsonl` |
| 240 | coleccion | EMBLEM COLLECTION · Emblems | `crudo/en/guias-b.jsonl` |
| 241 | coleccion | EMBLEM COLLECTION · Emblems | `crudo/en/guias-b.jsonl` |
| 242 | coleccion | EMBLEM COLLECTION · Emblem Collection | `crudo/en/guias-b.jsonl` |
| 243 | coleccion | TEAM-UP COLLECTION | `crudo/en/guias-b.jsonl` |
| 244 | coleccion | MIDNIGHT SUNS | `crudo/en/guias-b.jsonl` |
| 245 | coleccion | SINISTER SIX | `crudo/en/guias-b.jsonl` |
| 246 | coleccion | X-FORCE | `crudo/en/guias-b.jsonl` |
| 247 | coleccion | GUARDIANS OF THE GALAXY | `crudo/en/guias-b.jsonl` |
| 248 | coleccion | AVENGERS PART 1 | `crudo/en/guias-b.jsonl` |
| 249 | coleccion | SYMBIOTE | `crudo/en/guias-b.jsonl` |
| 250 | coleccion | THE DEFENDERS | `crudo/en/guias-b.jsonl` |
| 251 | coleccion | FANTASTIC FOUR | `crudo/en/guias-b.jsonl` |
| 252 | otro | UNIFORM | `crudo/en/guias-b.jsonl` |
| 253 | otro | RECOMMENDED UNIFORMS · THANOS / ANNIHILATION · RECOMMENDED | `crudo/en/guias-b.jsonl` |
| 254 | coleccion | UNIFORM | `crudo/en/guias-b.jsonl` |
| 255 | coleccion | UNIFORM COLLECTION · ANNIHILATION | `crudo/en/guias-b.jsonl` |
| 256 | coleccion | COMIC CARDS · Card Deck 1 · EQUIPPED CARD | `crudo/en/guias-b.jsonl` |
| 257 | coleccion | COMIC CARDS · OWNED CARD | `crudo/en/guias-b.jsonl` |
| 258 | coleccion | X OF SWORDS · ELEMENT MASTERY | `crudo/en/guias-b.jsonl` |
| 259 | coleccion | X OF SWORDS · STRENGTH · ELEMENT INFO | `crudo/en/guias-b.jsonl` |
| 260 | coleccion | X OF SWORDS · STRENGTH · ELEMENT MASTERY | `crudo/en/guias-b.jsonl` |
| 261 | coleccion | X OF SWORDS · STRENGTH · VIEW ALL EFFECTS | `crudo/en/guias-b.jsonl` |
| 262 | otro | RANKING | `crudo/en/guias-b.jsonl` |
| 263 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 264 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 265 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 266 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 267 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 268 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 269 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 270 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 271 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 272 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 273 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 274 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 275 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 276 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 277 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 278 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 279 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 280 | striker | MARVEL UNIVERSE · GALACTUS | `crudo/en/strikers.jsonl` |
| 281 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 282 | striker | TEAM · SKILL · Planet Devourer | `crudo/en/equipos.jsonl` |
| 283 | striker | TEAM · SKILL · Herald My Rage! | `crudo/en/equipos.jsonl` |
| 284 | striker | TEAM · SKILL · Gesture of Ruin | `crudo/en/equipos.jsonl` |
| 285 | striker | TEAM · SKILL · Power Cosmic Bomb | `crudo/en/equipos.jsonl` |
| 286 | striker | TEAM · SKILL · Power Cosmic Blast | `crudo/en/equipos.jsonl` |
| 287 | striker | TEAM · SKILL · Black Hole Crush | `crudo/en/equipos.jsonl` |
| 288 | striker | TEAM · SKILL · Galactic Wrath | `crudo/en/equipos.jsonl` |
| 289 | striker | TEAM · SKILL · Siphon of Realms | `crudo/en/equipos.jsonl` |
| 290 | striker | TEAM · SKILL · Great Devourer | `crudo/en/equipos.jsonl` |
| 291 | striker | TEAM · SKILL | `crudo/en/equipos.jsonl` |
| 292 | striker | TEAM · SKILL | `crudo/en/equipos.jsonl` |
| 293 | striker | TEAM · SKILL | `crudo/en/equipos.jsonl` |
| 294 | striker | TEAM · SKILL | `crudo/en/equipos.jsonl` |
| 295 | striker | TEAM · SKILL | `crudo/en/equipos.jsonl` |
| 296 | striker | TEAM · SKILL | `crudo/en/equipos.jsonl` |
| 297 | bonos | MY TEA [cortado] | `crudo/en/equipos.jsonl` |
| 298 | bonos | MY TEA [cortado] | `crudo/en/equipos.jsonl` |
| 299 | bonos | MY TEA [cortado] | `crudo/en/equipos.jsonl` |
| 300 | bonos | MY TEA [cortado] | `crudo/en/equipos.jsonl` |
| 301 | bonos | MY TEA [cortado] · GALACTUS | `crudo/en/equipos.jsonl` |
| 302 | bonos | MY TEA [cortado] · GALACTUS | `crudo/en/equipos.jsonl` |
| 303 | bonos | MY TEA [cortado] · GALACTUS | `crudo/en/equipos.jsonl` |
| 304 | bonos | MY TEA [cortado] · GALACTUS | `crudo/en/equipos.jsonl` |
| 305 | glosario | 스킬 용어 사전 · 가드 브레이크 | `crudo/en/glosario-ko.jsonl` |
| 306 | glosario | 스킬 용어 사전 · 무조건 회피율 | `crudo/en/glosario-ko.jsonl` |
| 307 | glosario | 스킬 용어 사전 · 무조건 치명타율 | `crudo/en/glosario-ko.jsonl` |
| 308 | glosario | 스킬 용어 사전 · 순수 피해량 | `crudo/en/glosario-ko.jsonl` |
| 309 | glosario | 스킬 용어 사전 · 팀 패시브 | `crudo/en/glosario-ko.jsonl` |
| 310 | glosario | 스킬 용어 사전 · 무적 | `crudo/en/glosario-ko.jsonl` |
| 311 | glosario | 스킬 용어 사전 · 슈퍼 아머 | `crudo/en/glosario-ko.jsonl` |
| 312 | glosario | 스킬 용어 사전 · 배리어 | `crudo/en/glosario-ko.jsonl` |
| 313 | glosario | 스킬 용어 사전 · 쉴드 | `crudo/en/glosario-ko.jsonl` |
| 314 | glosario | 스킬 용어 사전 · 피해 면역 | `crudo/en/glosario-ko.jsonl` |
| 315 | glosario | 스킬 용어 사전 · 공포 | `crudo/en/glosario-ko.jsonl` |
| 316 | glosario | 스킬 용어 사전 · 속박 | `crudo/en/glosario-ko.jsonl` |
| 317 | glosario | 스킬 용어 사전 · 타임 프리징 | `crudo/en/glosario-ko.jsonl` |
| 318 | glosario | 스킬 용어 사전 · 매혹 | `crudo/en/glosario-ko.jsonl` |
| 319 | glosario | 스킬 용어 사전 · 타겟팅 무시 | `crudo/en/glosario-ko.jsonl` |
| 320 | glosario | 스킬 용어 사전 · 유혹 | `crudo/en/glosario-ko.jsonl` |
| 321 | glosario | 스킬 용어 사전 · 반격기 | `crudo/en/glosario-ko.jsonl` |
| 322 | glosario | 스킬 용어 사전 · 탄성 | `crudo/en/glosario-ko.jsonl` |
| 323 | glosario | 스킬 용어 사전 · 집중 | `crudo/en/glosario-ko.jsonl` |
| 324 | glosario | 스킬 용어 사전 · 추가 관통 피해 | `crudo/en/glosario-ko.jsonl` |
| 325 | glosario | 스킬 용어 사전 · 간파 | `crudo/en/glosario-ko.jsonl` |
| 326 | glosario | 스킬 용어 사전 · 압도 | `crudo/en/glosario-ko.jsonl` |
| 327 | glosario | 스킬 용어 사전 · 속성 증폭 | `crudo/en/glosario-ko.jsonl` |
| 328 | glosario | 스킬 용어 사전 · 강철 | `crudo/en/glosario-ko.jsonl` |
| 329 | glosario | 스킬 용어 사전 · 조롱 | `crudo/en/glosario-ko.jsonl` |
| 330 | glosario | 스킬 용어 사전 · 강타 | `crudo/en/glosario-ko.jsonl` |
| 331 | glosario | 스킬 용어 사전 · 맹공 | `crudo/en/glosario-ko.jsonl` |
| 332 | glosario | 스킬 용어 사전 · 불굴 | `crudo/en/glosario-ko.jsonl` |
| 333 | glosario | 스킬 용어 사전 · 칼날 | `crudo/en/glosario-ko.jsonl` |
| 334 | glosario | 스킬 용어 사전 · 방호 | `crudo/en/glosario-ko.jsonl` |
| 335 | glosario | 스킬 용어 사전 · 슈퍼 히트 쉴드 | `crudo/en/glosario-ko.jsonl` |
| 336 | glosario | 스킬 용어 사전 · 격노 | `crudo/en/glosario-ko.jsonl` |
| 337 | glosario | 스킬 용어 사전 · 활력 | `crudo/en/glosario-ko.jsonl` |
| 338 | glosario | 스킬 용어 사전 · 방벽 | `crudo/en/glosario-ko.jsonl` |
| 339 | glosario | 스킬 용어 사전 · 격돌 | `crudo/en/glosario-ko.jsonl` |
| 340 | glosario | 스킬 용어 사전 · 상실 | `crudo/en/glosario-ko.jsonl` |
| 341 | glosario | 스킬 용어 사전 · 최후의 발악 | `crudo/en/glosario-ko.jsonl` |
| 342 | glosario | 스킬 용어 사전 · 표식 | `crudo/en/glosario-ko.jsonl` |
| 343 | glosario | 스킬 용어 사전 · 맹렬 | `crudo/en/glosario-ko.jsonl` |
| 344 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 345 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 346 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 347 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 348 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 349 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 350 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 351 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 352 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 353 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 354 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 355 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 356 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 357 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 358 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 359 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 360 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 361 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 362 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 363 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 364 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 365 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 366 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 367 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 368 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 369 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 370 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 371 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 372 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 373 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 374 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 375 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 376 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 377 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 378 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 379 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
| 380 | striker | MARVEL UNIVERSE · KINGPIN | `crudo/en/strikers.jsonl` |
