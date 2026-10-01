# Modelo del juego

## Para qué

La meta de la app (Ezequiel): unificar la información de todos los lugares posibles para poder
razonar cómo funciona el juego. thanosvibs tiene muchísima información, pero suelta: cada página es
un módulo aparte y los mismos datos se repiten de un lado a otro sin unirse (lo que una skill
publica con un marcador sin resolver, Leads & Supports lo publica resuelto). La wiki, las guías y
las planillas de la comunidad agregan otras piezas.

Por eso la app arma un modelo por **variante** (un personaje con un uniforme) que junta las
fuentes, en vez de mostrar cada una por separado. Cada dato dice de dónde sale y lo que se deduce
dice con qué regla. Sobre ese modelo va el análisis: qué hace cada cosa, cuándo, a quién le llega,
a quién le sirve y cómo se lee en PvE y en PvP. La ficha, el roster, la sinergia y las combinaciones
leen del modelo.

Este documento es el mapa de ese modelo y se completa por etapas. Lo que no está comprobado va
marcado como probable o como duda.

## Decisiones (Ezequiel, 1 de octubre de 2026)

- La meta es unificar las fuentes para razonar el juego, no copiar lo que muestra cada una.
- PvE y PvP se evalúan a la par, cada uno con su lectura.
- Sin topes: un efecto cuenta por lo que da, aunque ese stat ya esté al tope.
- Sin números: el modelo dice qué da cada cosa, a quién le llega y si le sirve; no estima el daño.
- La «mesa» es la tabla de datos del modelo. Se define al final, con lo aprendido en las etapas
  anteriores.

## Etapas

1. **Personajes y características**: qué es cada variante (identidad y perfil de combate).
2. **Skills**: qué hace cada efecto (las 228 etiquetas tipadas de thanosvibs), a quién apunta y
   cómo se lee en PvE y en PvP. Los roles se rehacen acá. En curso: el catálogo de efectos.
3. **Pasivas, liderazgos y soportes**: su efecto sobre los stats y para quién sirven. Junta las
   skills con Leads & Supports de thanosvibs, que son el mismo efecto visto de dos lados (de ahí
   sale, por ejemplo, que el efecto de uniforme de General's Hand es contra Universales). En curso:
   el mismo catálogo clasifica los 72 stats de Leads & Supports.
4. **La tabla del modelo**: la definición final.

## Etapa 1: personajes y características

### La unidad es la variante

Un uniforme puede cambiar casi todo. En los datos actuales, 46 uniformes cambian la clase, 66 el
bando, 84 las habilidades, 11 el género y 2 la raza, y cada uno tiene sus propias skills y sus
propios liderazgos y soportes. Ebony Maw, por ejemplo, es Universal con su base y con Infinity War,
y Detonación con Dark Obsidian Armor y con General's Hand. Todo lo que sigue es por variante.

### Identidad

| Característica | Valores | Qué hace en el juego | Fuente |
|---|---|---|---|
| Clase | Combate, Detonación, Velocidad, Universal | Ventaja de tipo: más daño contra la clase a la que le gana y menos daño recibido de ella. Combate le gana a Velocidad, Velocidad a Detonación y Detonación a Combate. Universal le gana a las otras tres con una ventaja menor y no tiene debilidad. Restringe liderazgos y soportes. | thanosvibs (`type`); wiki (páginas de cada clase); guía de thanosvibs, parte 3 (Type Enhancement); la ventaja de Universal, confirmada por Ezequiel |
| Bando | Superhéroe, Supervillano, Neutral | Restringe liderazgos y soportes; hay efectos de daño contra héroes o villanos. | thanosvibs (`side`) |
| Raza | Humano, Mutante, Inhumano, Alienígena, Criatura, Otro | Restringe liderazgos y soportes; hay efectos contra una raza («excepto mutantes»). | thanosvibs (`allies`) |
| Género | Masculino, Femenino, Neutro | Hay efectos de daño contra un género. | thanosvibs (`gender`) |
| Habilidades | 44 etiquetas (Agente, Orden Negra, Simbionte...), de 1 a 3 por variante | Restringen liderazgos, soportes y skills de artefacto («Restricted by Ability: Black Order»). | thanosvibs (`ability`) |
| Habilidad de World Boss | una de sus habilidades | Ver *Dudas*. | thanosvibs (`world_boss_ability`) |
| Instinto | Justicia, Orden, Destrucción, Crueldad | Capa de daño de instinto, la de los artefactos; la guía la da por irrelevante por ahora. | wiki (infobox): thanosvibs no lo publica; 15 de 290 personajes sin dato |
| Origen | MCU, Cómic, Animación... | Sin efecto conocido en combate. | thanosvibs (`original`) |
| Progresión | Tier (T2, T3, T4); skill 6 (Tier-3 o Trascendido); Striker (T4) | La skill 6 de un Trascendido se recarga aunque no esté en pantalla (guía, parte 4). | thanosvibs (`skill6`, `tier-4`, `striker_skill`) |
| Stats propios | recuperación y resistencias elementales | Los únicos stats que la fuente publica por variante. | thanosvibs (`stats`) |

La auditoría contrasta clase, bando, género, raza y tipo de ataque con el infobox de la wiki
(`docs/AUDITORIA.md`, sección 2): difieren 5, 11, 3, 13 y 21 de unos 540 retratos con pestaña en
la wiki. La app usa thanosvibs.

### Perfil de combate (deducido)

Regla única (`scripts/modelo.py`), sobre el daño de las skills activas (las cinco y la skill 6; la
Striker no):

- **Escala con**: de qué ataque sale el % de daño (ataque físico, de energía o la vida), con su
  parte del total. Según la guía (parte 3), cada personaje escala con un solo ataque, que es el que
  se construye; el tipo de daño de cada skill no lo cambia.
- **Tipos de daño**: físico y/o de energía. Importa contra los reflejos y en las etapas que solo
  reciben uno (la guía cita el World Boss Ultimate de Ebony Maw).
- **Elementos**: fuego, frío, rayo, veneno, mente. Son un modificador del daño, no un tipo aparte:
  un buff de un elemento solo sirve si sus skills lo tienen, y los buffs del mismo elemento se
  suman entre sí (guía, parte 3).

Se calcula una vez, en el build, y viaja en `data.js` (`MFF_PERFIL`, por retrato). Antes la app lo
deducía en el navegador con dos funciones distintas; el resultado es el mismo en los 888 retratos.

### Lo que se corrigió en esta etapa

- **Género por uniforme**: 11 uniformes cambian el género (Lady Loki, Lady Deadpool, Ancient One
  del MCU, Ghost del MCU, entre otros) y la ficha mostraba el de la base.
- **Ventaja de Universal**: la app no le daba ninguna (la wiki solo dice que no tiene debilidad).
  Le gana a las otras tres con ventaja menor, como dice la guía de thanosvibs. En la sinergia, un
  Universal cubre la debilidad de un compañero y suma igual que una ventaja normal; la razón lo
  aclara. Pesarla menos es una decisión abierta.

### Dudas abiertas

- **Habilidad de World Boss.** Cada variante tiene una, siempre una de sus habilidades. Falta saber
  para qué se usa en el juego.
- **Roles.** Salen de juntar las skills de todos los uniformes del personaje, no de cada variante.
  Se rehacen en la etapa 2.

## Etapas 2 y 3: el catálogo de efectos

thanosvibs publica el mismo efecto de dos lados: la API de skills como una etiqueta tipada (228
distintas, como `ALL BASIC ATTACKS INCREASE`) y Leads & Supports como un stat (72, como
`All Basic Attacks`). El catálogo (`scripts/contenido/catalogo.json`, contenido curado) hace que
las dos apunten a los mismos efectos (124, en 16 grupos) y responde una sola vez, por efecto, lo
que después la ficha va a decir de cada variante:

| Pregunta | Dónde está la respuesta |
|---|---|
| Qué es | El efecto y su grupo (ataque, daño, elemento, control, reducción de daño...). |
| Cuándo aplica | Lo propio del efecto, en su condición: solo contra ciertos rivales (una facción, los jefes, los que tienen más vida...), crece o baja (se acumula, según la vida...) o dura unos ataques. Lo demás es de cada skill o soporte: su activación y su duración. |
| A quién le llega | Si lo recibe su lado o el rival, en la etiqueta. A qué aliados, el objetivo de la skill o la restricción del soporte. |
| A quién le sirve | Una regla por efecto: a cualquiera del equipo, a quien escala con un ataque, a quien tiene un elemento, a quien hace daño físico, aplica debuffs, invoca, perfora, tiene definitiva de Tier-3 o Striker, o solo a él. Se compara con el perfil de combate de la etapa 1 y con sus skills. |
| PvE y PvP | Una lectura por modo, del grupo o propia del efecto. |
| Fuente y certeza | Cada lectura dice su certeza: comprobado (lo dice una fuente, que se cita), probable (se deduce del texto del efecto) o conjetura. |

Las etiquetas que la fuente usa para dos cosas se clasifican por el texto (el patrón): `MINIATURIZE`
achica al personaje y le sube ataques y defensas, o achica al rival y le baja los suyos;
`Counter Reflect` protege de todo reflejo o solo del físico.

`scripts/catalogo.py` lo valida en cada build. Un error del contenido (un efecto que no existe, una
lectura «comprobada» sin fuente) corta el build. Una etiqueta, un patrón o un stat nuevo que el
catálogo no tiene se avisa y queda en la sección 9 de `docs/AUDITORIA.md` hasta clasificarlo, sin
frenar la actualización semanal. El catálogo entero, para leerlo, está en `docs/CATALOGO.md`.

### Lo que dejó el primer cruce

Con el catálogo, cada soporte de Leads & Supports se puede comparar con la skill de la que sale
(por su nombre): de 1.020 efectos de soporte (sin los de artefacto, que no tienen skill), 986 están
entre las etiquetas de su skill. Lo que dejó el cruce está en `docs/AUDITORIA.md` (sección 7):

- **«Give Power» sin contenido.** En 27 retratos (29 efectos) la skill dice que otorga un efecto y no
  dice cuál; Leads & Supports sí (casi siempre «Remove All Debuffs»).
- **Signo.** Leads & Supports publica algunas reducciones de daño recibido con signo positivo; la
  skill dice siempre que reduce.
- **Códigos.** Algunas descripciones traen un número donde va el nombre de un efecto o de un elemento
  (`206`, que Leads & Supports nombra «Removes All Debuffs»).

Quedan 5 efectos, en 4 retratos, que no aparecen en la skill del mismo nombre; se revisan cuando el
cruce sea parte del build.

### Dudas abiertas del catálogo

- **Fractura.** Ninguna fuente dice qué hace. Se sabe que se aplica al rival y que corta el ataque
  especial de los jefes de Alliance Battle Legend; que sea un control es una suposición.
- **«Bonus Damage».** La guía llama «Skill Damage» a la parte del golpe que sale del ataque y
  «Additional Damage» al daño fijo extra; no dice si «Bonus Damage» es ese daño fijo.
- **«Adaptation».** «Inmune al mayor daño recibido»: no está claro si es el golpe más fuerte o el
  tipo de daño que más recibe.
- **Códigos sin nombre.** 401, 577 y 108 en «Natural Enemy», y los de otras etiquetas; ninguna
  fuente los nombra.

### Lo que sigue

1. La ficha muestra, por variante, lo que da cada skill, liderazgo y soporte según el catálogo: qué
   es, cuándo, a quién le llega, a quién le sirve y cómo se lee en PvE y en PvP.
2. Los marcadores (`$HEROSUBTYPE1`) se completan también con Leads & Supports, que publica el mismo
   efecto con la facción, el tipo o la raza escritos.
3. La regla de «a quién le sirve» del catálogo reemplaza a la que hoy tiene la app para la
   sinergia y el índice de equipos.

## Fuentes

- thanosvibs: API de personajes, de skills y de [Leads & Supports](https://thanosvibs.money/supports);
  Beginner's Guide, [parte 1](https://thanosvibs.money/beginners/1),
  [parte 3](https://thanosvibs.money/beginners/3) y [parte 4](https://thanosvibs.money/beginners/4)
  (versión 12.1.5); [Alliance Battle](https://thanosvibs.money/abxl) (qué controles cortan el ataque
  especial de los jefes).
- Future Fight Wiki: infobox de cada personaje; páginas
  [Combat](https://future-fight.fandom.com/wiki/Combat), [Blast](https://future-fight.fandom.com/wiki/Blast),
  [Speed](https://future-fight.fandom.com/wiki/Speed) y [Universal](https://future-fight.fandom.com/wiki/Universal).
