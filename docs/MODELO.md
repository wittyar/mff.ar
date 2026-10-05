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
- Roles (2 de octubre de 2026): no existen en el juego y dicen qué le aporta cada variante al
  equipo (ver *Etapa 2*).

## Etapas

1. **Personajes y características**: qué es cada variante (identidad y perfil de combate).
2. **Skills**: qué hace cada efecto (las 228 etiquetas tipadas de thanosvibs), a quién apunta y
   cómo se lee en PvE y en PvP. Los roles se rehacen acá. Hecha: el catálogo de efectos y el
   análisis de cada variante, que la ficha muestra en la pestaña *Análisis*.
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
| Clase | Combate, Detonación, Velocidad, Universal | Ventaja de tipo: más daño contra la clase a la que le gana y menos daño recibido de ella. Combate le gana a Velocidad, Velocidad a Detonación y Detonación a Combate. Universal le gana a las otras tres con una ventaja menor y no tiene debilidad. La fuerza depende de la mejora de tipo de cada personaje (ver *Lo que muestran las pantallas del juego*). Restringe liderazgos y soportes. | thanosvibs (`type`); wiki (páginas de cada clase); guía de thanosvibs, parte 3 (Type Enhancement); la ventaja de Universal, confirmada por Ezequiel; el ciclo, también la guía del juego (Type Affinity) |
| Bando | Superhéroe, Supervillano, Neutral | Restringe liderazgos y soportes; hay efectos de daño contra héroes o villanos. Dentro de una etapa, los Super Villains (jefes) y los Villains son facciones distintas (ver *Dudas*). | thanosvibs (`side`); guía del juego (Side) |
| Raza | Humano, Mutante, Inhumano, Alienígena, Criatura, Otro | Restringe liderazgos y soportes; hay efectos contra una raza («excepto mutantes»). | thanosvibs (`allies`) |
| Género | Masculino, Femenino, Neutro | Hay efectos de daño contra un género. | thanosvibs (`gender`) |
| Habilidades | 44 etiquetas (Agente, Orden Negra, Simbionte...), de 1 a 3 por variante | Restringen liderazgos, soportes y skills de artefacto («Restricted by Ability: Black Order»). | thanosvibs (`ability`) |
| Habilidad de World Boss | una de sus habilidades | Ver *Dudas*. | thanosvibs (`world_boss_ability`) |
| Instinto | Justicia, Orden, Destrucción, Crueldad | Capa de daño de instinto, la de los artefactos; la guía de thanosvibs la da por irrelevante por ahora. Según la guía del juego, los ataques básicos suman daño de instinto según los stats de instinto, que crecen con el rango y el nivel; ese daño solo se defiende con habilidades de instinto, y los buffs y debuffs de stats básicos no lo tocan. Sus porcentajes (crítico, evasión) rinden más contra quien tiene menos instinto total. Los escudos de los C.T.P. Regeneration y Veteran también lo bloquean. | wiki (infobox): thanosvibs no lo publica; 15 de 290 personajes sin dato; guía del juego (Instinct); C.T.P. en el juego |
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
- **Daño según la resistencia**: los elementos cuya resistencia le sube el daño. Según Ezequiel,
  un liderazgo o un soporte de resistencias solo le sirve a quien tiene esa mejora. Sale del
  artefacto exclusivo, cuando es para él («Increases Cold Damage by [P1]% of Cold Resist»: Luna
  Snow, Thor, Iceman, Iron Hammer, Ghost Panther, Professor X, Enchantress, Lincoln Campbell,
  Hellstorm y Misty Knight), y de la Element Conversion de la Striker de Ghost Rider y de Hades,
  que la fuente publica con el elemento sin resolver («Increases 1 damage by 10% of 1
  Resistance»): vale el elemento de su daño, fuego en los dos. El artefacto de Robbie Reyes da
  esa mejora a los aliados con la habilidad Llama: depende de que él esté en el equipo, así que no
  entra en el perfil de nadie. 38 de los 888 retratos la tienen.

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

- **Habilidad de World Boss.** Cada variante tiene una, siempre una de sus habilidades. Según
  NamuWiki (4 de octubre de 2026), en World Boss se eligen, además del equipo de tres, cinco
  strikers: cada uno le da al equipo el bono de su habilidad de World Boss (Liderazgo, 영웅심: +10%
  de daño a los Supervillanos; Agente: ignora la evasión del objetivo con 20% de probabilidad;
  Fuerza, 괴력: ataque físico +8%, entre otras) y todos aparecen a pegar con la skill cooperativa.
  En Legend tienen que ser de Tier-2, 6★, maestría 6 y Nv. 60, y el que se usó en una victoria no
  se repite ese día. Los de Liderazgo y Agente coinciden con thanosvibs; en Fuerza, NamuWiki pone
  además a cinco que thanosvibs ubica en otra (hallazgo `world-boss-habilidad`). La app no usa
  todavía la habilidad de World Boss.
- **Villains en las etapas.** El juego llama «SUPER VILLAIN faction» al bando Supervillano (C.T.P.
  Insight; los artefactos de thanosvibs, igual) y Leads & Supports lo llama «Villains». La guía del
  juego dice que dentro de una etapa los Super Villains, que son jefes, y los Villains son facciones
  distintas; la línea siguiente quedó cortada en la captura. Los World Bosses cuentan como
  Supervillanos (NamuWiki). Falta saber si un efecto contra el bando Supervillano les pega a los
  Villains comunes de una etapa.
- **Roles.** Salían de juntar las skills de todos los uniformes del personaje. Se rehicieron en la
  etapa 2, por variante.

## Etapas 2 y 3: el catálogo de efectos

thanosvibs publica el mismo efecto de dos lados: la API de skills como una etiqueta tipada (228
distintas, como `ALL BASIC ATTACKS INCREASE`) y Leads & Supports como un stat (72, como
`All Basic Attacks`). El catálogo (`scripts/contenido/catalogo.json`, contenido curado) hace que
las dos apunten a los mismos efectos (126, en 16 grupos) y responde una sola vez, por efecto, lo
que después la ficha va a decir de cada variante:

| Pregunta | Dónde está la respuesta |
|---|---|
| Qué es | El efecto y su grupo (ataque, daño, elemento, control, reducción de daño...). |
| Cuándo aplica | Lo propio del efecto, en su condición: solo contra ciertos rivales (una facción, los jefes, los que tienen más vida...), crece o baja (se acumula, según la vida...) o dura unos ataques. Lo demás es de cada skill o soporte: su activación y su duración. |
| A quién le llega | Si lo recibe su lado o el rival, en la etiqueta. A qué aliados, el objetivo de la skill o la restricción del soporte. |
| A quién le sirve | Una regla por efecto, la de sus skills: a cualquiera del equipo, a quien escala con un ataque, a quien tiene un elemento, a quien hace daño físico, aplica debuffs, invoca, tiene definitiva de Tier-3 o Striker, o solo a él. Se compara con el perfil de combate de la etapa 1 y con sus skills. Y una por stat de Leads & Supports y de bonos de equipo, la de los liderazgos, soportes y bonos, que es la que usa la app en los equipos (ver abajo). |
| PvE y PvP | Una lectura por modo, del grupo o propia del efecto. |
| Fuente y certeza | Cada lectura dice su certeza: comprobado (lo dice una fuente, que se cita), probable (se deduce del texto del efecto) o conjetura. |

A quién le sirve un liderazgo, un soporte o un bono de equipo es una sola regla, en el catálogo
(`soporte`: cada stat con sus efectos y su `sirve`; Ezequiel, 4 de octubre de 2026). La app no tiene
reglas propias: la sinergia, las combinaciones, el índice, las casillas, el «Por qué» y PvP y PvE leen
la del stat, y el Glosario y el «Cómo funciona» la muestran en su efecto. La app sabe evaluar las que
miran el perfil de combate de quien lo recibe (a todos, a nadie, según con qué escala, sus elementos,
su tipo de daño o su resistencia); el build no deja pasar otra. Casi siempre es la regla del efecto;
difieren, por decisión de Ezequiel:
- Todas las velocidades: a nadie como liderazgo, soporte o bono; en las skills (el frenesí) siguen
  contando.
- Las resistencias: como liderazgo, soporte o bono, solo a quien tiene una mejora de daño según esa
  resistencia (*Daño según la resistencia*); en las skills, a cualquiera.
- El efecto de los debuffs (All Debuffs Effect): como liderazgo, soporte o bono, a cualquiera («es
  útil»); en las skills, a quien aplica debuffs.
Un stat que el catálogo no tiene (uno nuevo de Leads & Supports, o uno de un bono de la wiki) cuenta
para todos y la app lo dice; el build lo avisa y la auditoría lo lista (sección 9).

Las etiquetas que la fuente usa para dos cosas se clasifican por el texto (el patrón): `MINIATURIZE`
achica al personaje y le sube ataques y defensas, o achica al rival y le baja los suyos;
`Counter Reflect` protege de todo reflejo o solo del físico.

`scripts/catalogo.py` lo valida en cada build. Un error del contenido (un efecto que no existe, una
lectura «comprobada» sin fuente) corta el build. Una etiqueta, un patrón o un stat nuevo que el
catálogo no tiene se avisa y queda en la sección 9 de `docs/AUDITORIA.md` hasta clasificarlo, sin
frenar la actualización semanal. El catálogo entero, para leerlo, está en `docs/CATALOGO.md`.

### Lo que dejó el primer cruce

Con el catálogo, cada soporte de Leads & Supports se puede comparar con la skill de la que sale
(por su nombre): de 1.025 efectos de soporte (sin los de artefacto, que no tienen skill), 991 están
entre las etiquetas de su skill. Lo que dejó el cruce está en `docs/AUDITORIA.md` (sección 7):

- **«Give Power» sin contenido.** En 27 retratos (29 efectos) la skill dice que otorga un efecto y no
  dice cuál; Leads & Supports sí (casi siempre «Remove All Debuffs»).
- **Signo.** Leads & Supports publica algunas reducciones de daño recibido con signo positivo; la
  skill dice siempre que reduce.
- **Códigos.** Algunas descripciones traen un número donde va el nombre de un efecto o de un elemento.
  Los de tres cifras son ids de habilidades de la propia API (`206` es «Removes all Debuffs»).

Quedan 5 efectos, en 4 retratos, que no aparecen en la skill del mismo nombre; se revisan cuando el
cruce sea parte del build.

### Liderazgos que Leads & Supports no publica

Leads & Supports no publica el liderazgo de todas las variantes: con los datos de formato 7, lo tienen
411 de 888, y a 135 personajes no les publica ninguno. Los que faltan los deriva el build de la Leader
Skill de la API de skills (Ezequiel, 4 de octubre de 2026: «¿Tomamos los liderazgos que Leads &
Supports no publica de la Leader Skill de la API?», «si, tomalos de ahí»; `scripts/liderazgos.py`).
Llegan en `MFF_SOPORTES` como los demás, con `"src": "api"`, y la app dice su fuente donde muestra un
liderazgo: «según la skill del juego» en el Resumen (y su cita suma las skills de thanosvibs), el
«Cómo funciona», el detalle de PvP y PvE, el «Por qué», la comparativa y el índice del roster; los de
Leads & Supports, como siempre. Una fuente desconocida corta el arranque.

Es la única ruta: reemplaza a la regla del 2 de octubre, que les copiaba el liderazgo de la base a los
uniformes con la Leader Skill idéntica. Los cinco que copiaba (Knull — Ancient History, Shang-Chi —
Marvel Zombies, Moon Girl — Monsters Unleashed!, Ghost — Thunderbolts* y Sentinel — Stark Sentinels
Mk II) salen iguales derivados, salvo «Notable», que es una marca de thanosvibs y la API no la tiene:
Knull — Ancient History y Ghost — Thunderbolts* la pierden, y en la sinergia su liderazgo pasa de 3
puntos a 2 [Comprobado].

Cómo se derivan:

1. **Partes.** La Leader Skill tiene una etapa (las 888), con un objetivo, una activación y sus
   efectos, y se parte en los dos slots de liderazgo de Leads & Supports. El objetivo da la
   restricción: la de un grupo de aliados (`OBJETIVO_GRUPO` en `scripts/dominio.py`), ninguna con
   «All Allies» y el personaje con «Self». «All Allies for the first effect, Self for the second
   effect» da dos slots: el primer efecto para todos y el segundo para él. «Give Power» («Acquires
   the following effect for $TIME sec.») va en un slot aparte, al final: es lo que Leads & Supports
   publica como segundo liderazgo, en los 19 casos quitar los debuffs al recibir uno, con una duración
   y una recarga que la API no trae. Ese slot no se deriva, salvo que el juego diga qué otorga (punto 2).
2. **Correspondencia.** Se aprende en cada build de las variantes que tienen las dos cosas. Cada slot
   de Leads & Supports va con la parte de su Leader Skill del mismo lugar, y los efectos en orden.
   Cada número del texto de la API da un stat de Leads & Supports con ese valor, con su signo
   («Decreases Debuff Duration by 30%» es Debuff Duration −30), y la duración es la del efecto.

   Así salen 34 efectos (de «Increases all Basic Attacks by #%», en 117 variantes, a los que se ven
   una sola vez), dos activaciones («when debuffed» → «When Debuffed», «when HP is below 99%» → «When
   HP is below 99%») y la condición de cada efecto de dos objetivos «Activates when». Exodus lleva
   «when 1 Mutant»…; Drax y Nebula, «when 1 Combat»…: la condición va porque el texto de la API la
   trae, y su texto sale de las variantes en que Leads & Supports la publica. Que Drax — Classic y
   Drax — Annihilation no la tengan en Leads & Supports es una diferencia de la verificación. Lo que
   dos variantes dicen distinto no se usa.

   Lo que Leads & Supports no publica en ningún liderazgo va a mano (decisión del 5 de octubre de
   2026; `scripts/contenido/liderazgos_api.json`):
   - un efecto, con su texto de la API citado literal, da un stat que ya está en el catálogo (con su
     «le sirve»), con el número del texto. Son defensa física, resistencia al fuego y eléctrica,
     velocidad de ataque, superarmadura y perforación de defensa. Tres de ellos Leads & Supports los
     publica igual en pasivas: Fire Resist en Robbie Reyes — Hellfire Charge, Ignore Defense en Mantis,
     Super Armor en Nick Fury — Director of S.H.I.E.L.D.;
   - una activación («25% rate when hit», «when tagging», «when dealing Critical Attack»…) va con el
     texto de la API y su traducción;
   - lo que otorga un «Give Power», si lo dice el juego (decisión del 5 de octubre): sus efectos, su
     activación (un texto de la API, que pasa como las demás) y su recarga, con la fuente y el texto
     del juego; la restricción es la del objetivo de la API, y el slot lleva la fuente (`otorga`), que
     la app cita. Hoy, Mephisto — Master of Hell: la ficha en coreano dice que su liderazgo, al recibir
     un debuff, les quita todos los debuffs a los del bando Villano (12 s), con recarga de 20 s
     (capturas 253, 269 y 286 del 4 de octubre). Son, valor por valor, los dos liderazgos que Leads &
     Supports publica para la base, cuya Leader Skill en la API es otra: es probable que Leads &
     Supports le haya puesto a la base el de Master of Hell (hallazgo `mephisto-base-leads-supports`;
     los datos de la base no se tocan).

   El build valida el archivo (texto de la API, stat del catálogo, la misma clasificación, las fuentes)
   y para si Leads & Supports dice otra cosa. Lo que no tiene stat no se inventa: queda sin derivar y
   listado.
3. **Todo o nada por slot.** Un slot se deriva si cierra entero: el objetivo con restricción
   conocida, la activación y cada efecto con su correspondencia, y cada valor publicado (sin $TIME ni
   $HEROSUBTYPE1 sin resolver). Si no, no se deriva, y la sección 12 de `docs/AUDITORIA.md` y
   `docs/COMPLETITUD.md` («Liderazgo sin completar») lo listan con sus motivos. Lo derivado lleva el
   nombre de la Leader Skill y los textos de Leads & Supports, que ya tienen traducción; no lleva
   «Notable» (decisión del 5 de octubre).
4. **Verificación.** La misma regla, sobre las variantes con liderazgo de Leads & Supports. De sus 448
   slots, 394 dan igual derivados (stats, valores, duración, condición, restricción, activación y
   recarga). 47 no se pueden derivar:
   - 19 por el «Give Power»;
   - 27 por un objetivo que la API no nombra («Target ID: 183») o que no es un grupo (Arachknight 2099);
   - Invisible Woman — Classic, con «Immunity to all Debuffs», que Leads & Supports parte en dos slots.

   Cinco dan distinto:
   - Black Swan: recarga de 25 s en la API, 20 s en Leads & Supports;
   - The Hood: la API lo da a los supervillanos y Leads & Supports a todos;
   - Mephisto: Leads & Supports parte en dos slots lo que la API da junto al recibir un debuff;
   - Drax — Classic y Drax — Annihilation: sin la condición en Leads & Supports.

   Y 2 están solo en Leads & Supports.

Lo que dio con los datos de formato 7 (`armar_datos_lideres.py`, en las pruebas; sin `work/` el build
no se pudo correr) [Comprobado]:

- **Derivados:** 443 variantes (461 slots).
  - Tienen liderazgo 854 de 888 variantes, y los personajes sin ninguno bajan de 135 a 8 (Captain
    America (Sharon Rogers), Daisy Johnson, Hydro-Man, Luna Snow, Silk, Sister Grimm, White Tiger y
    Yellowjacket).
  - Casi todos son liderazgos chicos: todas las velocidades (88 slots), evasión (69), duración de los
    debuffs (54), todas las defensas (48), recarga de skills (42), crítico (40).
  - Lo de a mano deriva 111 slots, de 111 variantes: defensa física (23), inmunidad física al recibir
    un golpe (14), resistencia al fuego (14) y eléctrica (13), recarga de skills al asestar un crítico
    o al esquivar, todas las velocidades al cambiar de personaje (12)… y el «Give Power» de Mephisto —
    Master of Hell.
  - Cinco traen anti-mermas, al recibir un debuff: Carnage — Fallen Soul y Superior Carnage (para los
    Simbiontes), Thane — Phoenix Force, Sentinel — Stark Sentinels Mk II y Mephisto — Master of Hell
    (para los Supervillanos, según el juego).
- **Sin derivar:** 35 slots de 35 variantes de 12 personajes.
  - 34 por un efecto sin stat en el catálogo: escudo de energía (11) y físico (3), contra los que «Max
    HP Shield» diría más que la skill; inmunidad al frío (6); sangrado (5) y parálisis (2), que son
    para el rival; robo de vida (3); inmunidad a todo daño (2); resistencia al veneno (1); inmunidad al
    sangrado y a la fractura (Hydro-Man).
  - 1 por el «Give Power» de Sentry — Thunderbolts*, que tiene derivado el otro slot y del que ninguna
    fuente dice qué otorga.

La app avisa, donde muestra el liderazgo, que la Leader Skill da un poder que ninguna fuente publica:
en Sentry — Thunderbolts* y en los 19 pares con Leads & Supports. En los pares no se deduce de lo que
publica Leads & Supports (decisión del 5 de octubre).

### Lo que corrigió el glosario del juego

El juego trae un glosario de skills (Skill Name Glossary; capturas de Ezequiel, octubre de 2026).
Corrigió el catálogo en cinco puntos:

- **Fractura** no es un control: le baja todos los ataques básicos al rival (se acumula), cada
  curación le saca una carga y lo cura menos, y «quitar todos los debuffs» no la saca. Pasó a
  *Debilitar* y dejó de contar para el rol Control.
- **Mockery** es un debuff sobre los rivales: los obliga a atacarlo a él, pero a ellos les sube el
  ataque. El catálogo lo leía como un aumento de su propio ataque.
- **Encanto** y **Pérdida** frenan al rival (no se mueve ni usa skills); thanosvibs publica solo su
  daño continuo. Cada uno suma un control, con certeza probable: el nombre es el mismo, pero ninguna
  fuente dice las dos cosas juntas.
- **Daño perforante adicional** (Additional Pierce Damage) es daño extra que ignora la defensa,
  sobre el daño de la skill. No depende de la Perforación (atravesar invencibilidad, escudos o
  barreras), así que le sirve a cualquiera; el catálogo lo daba solo a quien perfora.
- **Incapacitación**, además de quitar los buffs, baja todas las defensas (se acumula).

También dio la lectura comprobada de lo que frena cada protección (invencible, superarmadura,
barrera, escudo, inmunidad al daño) y de los controles (miedo, atrapar, detención del tiempo,
seducir, control mental, pánico).

### Lo que agrega el glosario en coreano

El mismo glosario en coreano (스킬 용어 사전, 44 términos; capturas de Ezequiel, 2 de octubre de
2026) dice lo mismo que el inglés casi siempre. Donde no, el inglés traduce mal:

- **피격 모션**, la reacción al recibir un golpe, sale en inglés como «basic attacks» o «basic attack
  motions» en invencible, superarmadura, escudo, inmunidad al daño y contraataque. La invencibilidad
  no tiene que ver con el stat de ataque básico: los golpes no lo interrumpen ni lo mueven; por eso
  el contraataque, que reemplaza esa reacción, no se activa mientras es invencible. La rotura de
  guardia, según el coreano, corta la skill forzando esa reacción. El catálogo corrigió la lectura
  de invencible (y el inglés de la del escudo); las otras ya hablaban del movimiento de los golpes.
- **Barrera:** dura un tiempo y una cantidad de golpes, y no frena la rotura de guardia ni los
  debuffs. El inglés dice solo el tiempo, y las skills cuentan los golpes («# time(s)»): las dos
  cosas son ciertas.
- **Escudo:** frena una cantidad fija de daño.
- **Jefes inmunes.** En detención del tiempo, encanto, seducción y control mental, el inglés dice
  que sirven contra rivales «sin debuffs»; el coreano, contra los jefes y rivales a los que no se
  les aplican debuffs: los inmunes. El catálogo corrigió las cuatro lecturas.
- **Crítico y evasión garantizados** le suman un valor fijo a la probabilidad; el inglés dice «a una
  tasa fija».
- **«Type» es elemento.** El inglés traduce 속성 (elemento) como «Type»: el daño puro no pasa por la
  defensa ni por las resistencias elementales (el inglés dice «Type Resistance»), y la etiqueta
  «TYPE PENETRATION» de las skills atraviesa una resistencia elemental. **Type Amplification** es 속성
  증폭, amplificación de elemento: el reforjado de Judgment que en inglés se llama así es un problema
  de traducción (el hallazgo de los C.T.P., en `docs/AUDITORIA.md`).
- **Penetration** es 간파, «ver a través»: no es la Perforación. Corta el ataque del rival con una
  rotura de guardia, como dice la guía de thanosvibs. Es una de las dos opciones de reforjado de
  Regeneration y de Transcendence (la otra de Transcendence es Beatdown): un C.T.P. reforjado lleva,
  probablemente, una sola (los que se ven equipados traen una).

Confirma lo que el catálogo ya decía del encanto (frena también los ataques que se activan solos),
la elasticidad (la saca el sangrado; la cancelación y la incapacitación, no), la fractura y lo que
no se le aplica a quien quita todos los debuffs (la marca, en cambio, sí). Y dice cosas de efectos
que el catálogo todavía no tiene: el contraataque no se activa mientras el personaje es invencible,
el muro (Wall) no se usa junto con la barrera ni se suma a la reducción de daño, Enraged (reforjado
de Rage) ignora el tope de daño crítico y Vitality (reforjado de Refinement) da inmunidad a la
rotura y a la superrotura de guardia, y vida por segundo. Las capturas en inglés de Enraged,
Vitality y Wall llegaron el 4 de octubre y dicen lo mismo.

NamuWiki (4 de octubre de 2026) agrega nombres que el glosario no tiene: Liderazgo es 영웅심
(«heroísmo»), el instinto es 천성 («naturaleza») y Destrucción y Crueldad son 파멸 («ruina») y 냉혹
(«despiadado»); Justicia (정의) y Orden (질서) son literales. La comunidad coreana llama 상태이상 면역
(«inmunidad a estados alterados») a «quitar todos los debuffs» con duración, y 추가 피해량 al daño
fijo extra («Additional # Damage»).

Los 44 términos, con estas diferencias y los efectos del catálogo que les corresponden, están en
`scripts/contenido/glosario.json`, y la app los muestra en la solapa **Glosario**.

### Lo que aclaró NamuWiki

Páginas generales de NamuWiki en coreano (World Boss, Legend, héroes, Timeline, Giant Boss Raid),
leídas el 4 de octubre de 2026; las fichas de personaje no se pudieron leer.

- **Quitar todos los debuffs con duración.** En los liderazgos y soportes, «Removes all Debuffs»
  dura un tiempo desde que el personaje recibe un debuff (casi siempre 12 s), y mientras dura
  protege: NamuWiki dice que el liderazgo de Malekith le da a todo el equipo 20 s de inmunidad a los
  estados alterados, y la guía de thanosvibs llama «Debuff Immunity» a la Tier-2 de Wasp (20 s).
  Para los de 12 s es lo probable. No es lo mismo que la inmunidad: según el glosario del juego, la
  detención del tiempo, el encanto, la seducción, el control mental y el pánico alcanzan a los
  inmunes, pero no a quien tiene un efecto que quita todos los debuffs.
- **El «buffer» de Timeline.** Un equipo de Timeline suele llevar un líder con anti-mermas, un DPS
  y un tercero con aumentos o bajas de daño entre facciones, como Colossus. Es un dato para la
  decisión abierta de cómo cuenta en PvP el daño contra una facción. Molecule Man, que ignora esos
  aumentos y bajas, lo neutralizaría (probable).
- **World Boss Legend.** Los jefes ignoran incluso los controles que ignoran la inmunidad
  («Paralysis (Ignores immunity)», «Web (ignores immunity)»); el daño perforante adicional de las
  cartas sí les entra.

### Dudas abiertas del catálogo

- **«Bonus Damage».** La guía llama «Skill Damage» a la parte del golpe que sale del ataque y
  «Additional Damage» al daño fijo extra, el único que sube con el nivel de la skill (NamuWiki dice
  lo mismo del 추가 피해량); no dice si «Bonus Damage» es ese daño fijo. En inglés, «Bonus damage»
  nombra también el daño continuo de la maldición y de la pérdida. Falta el texto en coreano de la
  pasiva de Tier-2.
- **«Adaptation».** «Inmune al mayor daño recibido»: no está claro si es el golpe más fuerte o el
  tipo de daño que más recibe. Ninguna fuente que se pudo leer lo dice.
- **Códigos sin nombre.** En «Natural Enemy», 401 es Mockery y 108 Shock (ids de la API); 407 y 577
  no son el id de ninguna habilidad de las skills (Leads & Supports nombra 407 «Debuff Removal
  (Instinct)»). 407 es probablemente el efecto de cinco artefactos (Aero, Punisher, Scarlet Spider,
  Domino y Yelena Belova: ignorar los debuffs según el instinto); 577 sigue sin fuente. La app
  todavía muestra los números: podría mostrar el nombre de los que tienen id.
- **Efectos para todo el equipo que se repiten.** Los C.T.P. Insight y Liberation dicen en el juego
  que su efecto para todo el equipo no se aplica dos veces si lo llevan dos. Falta saber si pasa lo
  mismo con los soportes de los personajes; la sinergia hoy cuenta cada uno por quien lo da. Una
  respuesta de GameFAQs de 2016 dice que dos bonos de equipo iguales se acumulan: habla de bonos,
  no de soportes, y es vieja (conjetura).

## Etapa 2: lo que hace cada variante con sus skills

`scripts/modelo.py` (`analisis`) recorre cada efecto de cada skill de la variante y, con el
catálogo, anota:

- **Qué efecto es.** Las etiquetas que la fuente usa para dos cosas se resuelven por el texto.
- **A quién le llega.** Lo que el catálogo dice que se aplica al rival va al rival. Lo demás va al
  objetivo de la etapa: a él si no tiene (las de liderazgo siempre lo traen) o si es «Self»; al
  equipo, con qué aliados, si es un grupo; a sus invocaciones. La etapa «All Allies for the first
  effect, Self for the second effect» manda el primer efecto al equipo y el resto a él.
- **De qué skills sale y cuándo:** la skill y la activación de la etapa. Las apariciones de un mismo
  efecto se juntan si comparten destino, aliados y condición.
- **Si le sirve**, cuando es para él: la regla «le sirve» del catálogo contra su perfil de combate y
  sus skills (un buff de Striker sin Striker, o de un elemento que no usa, no le sirve).
- **Lo que la fuente no dice.** «Give Power» («Acquires the following effect») es un envoltorio:
  lo que otorga viene después, en la misma etapa o en las que siguen. En una etapa con un objetivo
  para cada efecto, lo que le sigue va a otro objetivo y no es lo que otorga (el «Give Power» de Kang
  the Conqueror es para todos y la suba de ataque, para él). Si no le sigue nada, la fuente no dice
  qué otorga, y el análisis lo muestra así (80 casos, en 69 variantes, con los datos de formato 7). Lo
  que el catálogo no clasifica también se ve, como lo publica la fuente.

El daño de los golpes no va en el análisis: es el perfil de combate de la etapa 1. Viaja en
`data.js` (`MFF_ANALISIS`, por retrato, con el catálogo en `MFF_CATALOGO`; formato 3) y la ficha lo
muestra en la pestaña *Análisis*: un resumen y, por destino y por grupo de efecto, cada efecto con
sus fuentes, su condición y sus lecturas de PvE y de PvP.

### Roles

No existen en el juego. Dicen qué le aporta la variante al equipo (Ezequiel, 2 de octubre de 2026),
y cada uniforme tiene los suyos:

| Rol | Regla | Variantes que lo tienen |
|---|---|---|
| Soporte | Le da algo a sus aliados fuera del liderazgo. | 239 de 888 (27%) |
| Tanque | Provoca, o le baja al equipo el daño que recibe. | 230 (26%) |
| Control | Le aplica al rival 3 o más controles distintos. | 469 (53%) |
| Daño | Todos. | 888 |

Antes salían de juntar los uniformes del personaje, con una lista de etiquetas por rol (curación,
escudo o barrera para Soporte; superarmadura o defensas para Tanque; 2 controles para Control): por
variante, eso daba Soporte al 88%, Tanque al 85% y Control al 82%, y no distinguía a nadie. Pesan en
el filtro de rol del roster y en los «roles cubiertos» de la sinergia.

### Lo que sigue

1. Etapa 3: los liderazgos y soportes de Leads & Supports en el mismo análisis, con el efecto
   que la skill no dice (los «Give Power» vacíos). Los marcadores (`$HEROSUBTYPE1`) ya se completan
   con la facción, el tipo o la raza que escribe Leads & Supports, después de la tabla a mano y
   antes que la wiki (Ezequiel, 3 de octubre de 2026; `scripts/marcadores.py`): Angela — Asgard's
   Assassin quedaba «sin especificar» y Leads & Supports dice Villains.

## Lo que muestran las pantallas del juego

Capturas de Ezequiel (octubre de 2026), de su cuenta.

- **Mejora de tipo (Type Enhancement).** Cada personaje la sube por niveles. En el máximo (6), una
  clase hace 60% más de daño normal a la clase a la que le gana y recibe 45% menos de ella (Thanos,
  Adam Warlock y un Velocidad, uno de cada clase). Universal solo sube el daño, igual contra las
  otras tres: 17,5% en el nivel 5 (Gorr), sin reducción del daño recibido. El juego muestra además
  un valor entre paréntesis (+30%, +15%, +12,5%) que esa pantalla no explica. Según NamuWiki, la
  ventaja base es 30% más de daño y 30% menos de daño recibido, y la de Universal, 5% más de daño
  contra las otras tres: 60 = 30 + 30, 45 = 30 + 15 y 17,5 = 5 + 12,5, así que el paréntesis es lo
  que suma la mejora sobre la base (probable). En PvE casi no pesa, según la misma página.
- **Strikers.** Solo personajes de 6★ o más; el buff del striker rinde más cuanto más alto es su
  tier, y el striker suma un bonus de instinto (Destrucción +Nv. 2 en el ejemplo).
- **Pasivas de equipo.** El panel del equipo lista las pasivas que les llegan a todos aunque su
  dueño no sea el líder (el glosario las llama Team Passive: «Applies to: All Team members»), como
  la de Cyclops con el uniforme de X-Men '97 o la de Jeff the Land Shark. Es lo que el análisis ya
  manda al equipo.
- **Todos los efectos del equipo.** El panel «All Effects» suma los efectos iguales de distintas
  fuentes (todos los ataques básicos +58,36%) y muestra aparte los que son contra ciertos rivales
  (30% y 45% contra SUPER VILLAIN). Que el combate los sume igual es probable, no comprobado.
- **Bonos de equipo (Team Bonus).** Llevar ciertos personajes juntos da stats («Afflicted Lovers»,
  Cyclops y Jean Grey: ataques +5,24% y vida +4,97%), y también llevar tres de 6★ (ataques, defensas
  y vida +3,12%). El panel del equipo los suma con el liderazgo. La wiki publica los de personajes
  en la página de cada integrante (265 de 290 páginas, unos 1.680 bonos de dos y de tres),
  redondeados a un decimal. Le faltan los de los personajes más nuevos (Galactus, Annihilus,
  Kahhori, entre otros) y los de estrellas. namu.wiki tiene solo seis de ejemplo. Las capturas del
  2 de octubre muestran 20 bonos con dos decimales, 13 de ellos de Galactus, pero sus integrantes se
  ven solo por retrato. Ver *Bonos de equipo* más abajo.
- **Lo que suma la cuenta.** El nivel de agente, las cartas de cómic (5, en dos mazos que se asignan
  por contenido), las espadas (X of Swords) y el S.H.I.E.L.D. Archive (stats de instinto) valen
  para todos los personajes; los emblemas, solo en ciertos contenidos; las colecciones de equipo
  (Team-Up), para los de un tema o una raza. Suben los stats de todos por igual o de un grupo: no
  cambian la comparación entre variantes, salvo las colecciones de equipo.
- **C.T.P. por contenido.** Cada personaje lleva un C.T.P. desde el Nv. 30. La guía del juego dice
  «uno por personaje», pero la ficha tiene ranuras, y cada una dice en qué contenido vale su C.T.P.
  (적용 콘텐츠, «Applied Content»): con una sola ranura, en PVE y en PVP (Gorr, 2 de octubre); con
  dos, una para cada uno (Mephisto, 4 de octubre: Conquest Mighty en PVP y Competition Mighty en
  PVE). Al lado hay un botón para editarlo: lo elige el jugador (probable). Qué modos son PVP y
  cuáles PVE no se ve. Un C.T.P. reforjado (Mighty o Brilliant) conserva la opción fija y suma una
  opción de reforjado: la ficha lista dos, y los tres reforjados que se ven equipados traen una sola
  (probable: una de las dos). La ficha muestra el valor máximo de cada opción, y los equipados pueden
  tener menos, también en la opción fija (hallazgos de los C.T.P., en `docs/AUDITORIA.md`).
- **Elite Gear.** Los Tier-4 con Nv. 80 y gear +30 pueden desbloquearlo: otra progresión, con
  puntos para elegir stats, que la app todavía no tiene.

## Bonos de equipo

`scripts/bonos.py` lee la sección Team Bonus de la página de cada personaje en la wiki y la junta
con lo que se vio en el juego (`scripts/contenido/bonos.json`), que manda. Un bono es un conjunto de
integrantes, porque los nombres tienen erratas entre páginas. Vale lo que dice la mayoría de sus
páginas; si empatan (medio centenar), la app muestra todas las versiones empatadas. Los stats se
escriben como los efectos de soporte de thanosvibs («All Attack» de la wiki es «All Basic Attacks»,
como lo llama el juego), así que la sinergia les aplica la misma regla de «le sirve». La recarga y
la duración de control siempre bajan, aunque la página ponga la flecha al revés. Lo que no cierra va
a `docs/AUDITORIA.md` (sección 10).

En la sinergia (Ezequiel pidió sumarlos, 2 de octubre de 2026), cada bono con todos sus integrantes
en el equipo suma 1 si le sirve a alguien. Con foco en un integrante, suma si él está en el bono o si
le sirve a él. Los integrantes de un bono quedan vinculados entre sí, porque están juntos por el
bono. A los demás del equipo les llega igual, así que no los vincula. Todos los bonos de los datos
traen algún stat que le sirve a cualquiera, así que en la práctica cada bono activo suma. La ficha
los muestra en la pestaña *Equipos*.

Dudas:
- **«X 2 Bonuses».** La wiki anota, debajo de un bono de tres, qué parejas del trío tienen su
  propio bono de dos. Sugiere que se activan todos a la vez (probable); la app suma cada uno.
- **Stats con nombres sueltos.** Seis bonos traen stats que no usa ningún otro bono ni Leads &
  Supports («Physical Damage», «Critical Defense» y otros). Van como los escribe la wiki y cuentan
  para todos. Falta verlos en el juego.

## Strikers

`scripts/strikers.py` lee la pestaña Striker de la página de cada personaje en la wiki: quién puede
aparecer a pegar junto a él y con qué probabilidad, cuando él ataca o cuando lo atacan («12% chance
to appear when attacking»). Según Ezequiel, el striker tiene que estar en el mismo equipo. La tienen
171 de 290 páginas (unas 7.000 filas). En el juego (capturas de Ezequiel, 2 de octubre de 2026),
los 37 strikers de Kingpin que se ven coinciden con la wiki en nombre, probabilidad, condición y
orden, con un uniforme que no es el base: que la lista no dependa del uniforme es probable. Les
falta a 119 personajes, casi todos recientes (Galactus, Annihilus, Apocalypse, entre otros): en la
app no tienen strikers propios, aunque pueden ser strikers de otros. Galactus tiene 16 en el juego.
Lo que no se pudo leer va a `docs/AUDITORIA.md` (sección 11).

En los equipos (Ezequiel, 4 de octubre de 2026: «suman, MUY poco... sería un sistema de desempate»),
los strikers no dan puntos en ningún lado, ni en la sinergia ni en PvP y PvE: a igual puntaje,
desempatan. Las combinaciones van por puntaje y, a igual puntaje, por cuántos strikers tiene el trío
(en PvP y PvE, todos; en los puntos para él, los que lo involucran), y cada tarjeta lo dice
(«desempate: 2 strikers»). «Cómo entraría» elige el lugar igual.

Dudas:
- **Set Striker.** El juego tiene además un striker que se elige para cada personaje (solo de 6★ o
  más), que aparece con su Striker Skill y cuyo efecto crece con el tier (captura de Gorr con Silver
  Surfer (Shalla-Bal)). Es otro sistema: la app no lo tiene.
- **Strikers vistos en el juego.** Cargarlos (Galactus, y confirmar los de Kingpin) pide un archivo
  de contenido, una fuente y código nuevos, con el juego por encima de la wiki fila por fila, y
  probablemente un formato de datos nuevo. Falta decidir.

## Equipos por contexto

Reglas de Ezequiel para armar equipos (2 de octubre de 2026):

- **PvP:** los tres tienen que tener anti-mermas (quitar todos los debuffs), del liderazgo del
  líder, del soporte de alguno o propio (4 de octubre de 2026: «hay muy pocos casos... Knull,
  Captain America, alguno más»); un equipo de PvP sin anti-mermas es un mal equipo. Si viene de un
  soporte, el lugar de líder queda para otro liderazgo. En PvE no hace falta.
- **Liderazgos:** los más útiles en general son todos los ataques, PG (vida) e ignorar esquiva; en
  PvP, también todas las defensas: Thanos — Annihilation es el mejor líder por todo lo que suma
  (anti-mermas, ataques y defensas), y gana a Black Cat — Queen in Black, que da ataques e ignorar
  esquiva (Ezequiel, 2 de octubre de 2026; ver *Casos de referencia*). En PvE pesan los de daño:
  ataque, daño elemental y daño a jefes, cada uno a quien pega con eso. Un liderazgo de todas las
  velocidades es inútil, y uno de resistencias solo le sirve a quien tiene una mejora de daño según
  su resistencia (ver *Daño según la resistencia*).
- **DPS:** no todos pegan bien, y sin quien pegue un equipo no es relevante. Agent 13 no le aporta
  nada a ningún equipo (relleno); Black Cat sirve de soporte o de líder, no de DPS; hay quien es
  las tres cosas, como Apocalypse.
- **Sinergia y strikers:** relevantes, no definitorios. El striker tiene que estar en el mismo equipo y
  solo desempata (4 de octubre de 2026).
- **Líder:** un trío tiene un solo líder, el mismo en las listas de los tres: el orden solo cambia
  cuando hay un peso real distinto entre las opciones. Un liderazgo que se activa con una condición
  (al recibir un debuff, por ejemplo) pesa la mitad, sin mirar los porcentajes (Ezequiel, 2 de
  octubre de 2026: «único + condicional a la mitad»; ver *Casos de referencia*). La misma regla vale
  para todo, también sin contexto (Ezequiel, 4 de octubre de 2026). Y donde se ve un equipo, el líder
  va siempre primero, a la izquierda como en el juego, con una marca en el retrato, para reconocer
  quién lidera sin leer el texto.
- **Ataque contra daño a una facción:** para hacer daño hay que tener ataque suficiente para
  superar la defensa o la esquiva del rival, y eso pesa al armar un equipo. Lo dudoso es comparar
  un porcentaje de ataque con un daño agregado contra una facción: no está claro cuál aporta más,
  siempre que haya anti-mermas. La excepción rara es el liderazgo de Molecule Man.
- **Prioridad en PvP** (Ezequiel, 4 de octubre de 2026): quitar los debuffs (anti-mermas), vida,
  todos los ataques, todas las defensas, ignorar esquiva y el efecto de los debuffs («es útil, está
  por debajo de todas las defensas»; lo traen dos o tres liderazgos).

### Tabla de valor

Cuánto vale un equipo según el modo de juego está en `scripts/contenido/valor_equipos.json`
(Ezequiel, 4 de octubre de 2026), una fila por contexto; cada modo de juego usa la de su tipo
(`tipo` en `modos.json`), sin pesos propios por ahora. La app no tiene ningún peso escrito: lee la
tabla (`MFF_VALOR`) y arma con ella el puntaje, el detalle y la nota de cada orden. El build para si
un stat de la tabla no está en el catálogo de efectos (no tendría regla de «le sirve»), si un modo
no tiene la fila de su tipo o si falta un dato de una fila.

| Fila | PvP | PvE |
|---|---|---|
| Requisito | Anti-mermas para los tres | Ninguno |
| Liderazgo, por integrante al que le llega y le sirve | Vida 2,5; todos los ataques 2 (también la acumulable); todas las defensas 1,5; ignorar evasión 1; efecto de los debuffs 0,5 | Cada uno de daño 2: todos los ataques, ataque físico y de energía, daño de cada elemento y de todos, daño a jefes |
| Liderazgo condicional | La mitad | La mitad |
| Cada nivel de fila de cada DPS | 2 | 2 |
| Cada soporte que le llega a otro y le sirve | 1 | 1 |
| Cada bono de equipo activo | 1 | 1 |
| Strikers | Desempatan | Desempatan |

Anti-mermas: Remove All Debuffs y Debuff Immunity. Los pesos son una propuesta (la tabla lo dice, y
la nota de cada orden también) y se ajustan con los *Casos de referencia*.

Cómo lo aplica la app, en las combinaciones de 3 de la pestaña *Equipos* (órdenes PvP y PvE):

- Quién es DPS, soporte o líder en cada contexto sale de las filas de las tier lists de thanosvibs:
  Arena de Equipos para PvP; Batalla de Alianza y World Boss Legend para PvE
  (`scripts/contenido/roles_listas.json`, con el rótulo de cada fila; el build para si una cambia).
  Así quedan los ejemplos: Agent 13 no está en ninguna, Black Cat es soporte y Apocalypse es DPS.
- Sin función en el contexto, no hay lista: si el personaje no figura en las tier lists del
  contexto, o solo como «Not for wbl», el orden de ese contexto no arma combinaciones y la pestaña
  lo dice (Ezequiel, 2 de octubre de 2026: Thor base no tiene función en PvP ni en PvE). Con los
  datos actuales tienen función 60 de las 888 variantes en PvP y 119 en PvE.
- Un trío entra si alguno es DPS de ese contexto y cumple el requisito de la tabla: en PvP, que con
  algún líder los tres tengan anti-mermas. Cada compañero tiene vínculo con él o es DPS de ese
  contexto.
- Anti-mermas (Ezequiel, 4 de octubre de 2026): son los stats de la tabla de valor (Remove All
  Debuffs y Debuff Immunity), los mismos en el filtro de PvP, su detalle, la casilla de las
  combinaciones y el índice. A cada uno se los da el liderazgo del líder, un soporte de alguno o
  algo propio: su soporte, si le aplica, o sus skills, lo que le dan a él mismo (el análisis: los
  efectos de esos stats con destino «él», de sus pasivas). Con los datos actuales, 31 variantes los
  tienen de sus skills (Knull, por su pasiva de Tier-2, al recibir un debuff), y Leads & Supports no
  los publica porque no son para el equipo. Uno que se activa con una probabilidad no cubre: el
  detalle y el «Por qué» lo muestran con su probabilidad y dicen que no cuenta. Son 19 variantes:
  Captain America (la base y 13 uniformes; 50% al recibir un debuff, o 60% en Back to Basics, Enter the
  Phoenix, Hydra Supreme y What If... Zombies?!), Hulkling (25% al recibir un golpe), Dormammu y
  Dormammu — Damnation (25% al atacar), Karnak — All-New, All-Different (35% al recibir un debuff) y
  Baron Mordo — Doctor Strange 2 (80% al recibir un golpe). Lo propio cuenta para su dueño también
  en lo que le llega (la casilla y el «Por qué»), pero no en la sinergia: ahí un soporte suma solo
  si le llega a otro integrante.
- Puntaje, con la tabla de valor: cada stat del liderazgo del líder suma su peso por cada
  integrante al que le llega y le sirve (cada stat una vez, aunque el liderazgo lo traiga en varias
  líneas; la parte del condicional si solo le llega por un liderazgo que se activa con una condición,
  el slot con `ac`); cada nivel de fila de cada DPS (3 la más alta), cada soporte que le llega a otro
  y le sirve y cada bono de equipo activo, lo suyo. Los strikers del trío no suman: a igual puntaje,
  desempatan. Con pesos con decimales, el orden de las listas usa el puntaje en centésimas. El líder es el que más suma de los que cumplen y no depende
  del orden del trío: a igual puntaje, el mejor ubicado en las tier lists del contexto (la suma de
  su puesto en cada una) y después la clave. Hasta la 1.0.15, a igual puntaje ganaba el primero del
  trío, que es siempre el personaje de la ficha, así que el mismo trío salía con otro líder en cada
  lista (con los datos de la 1.0.14, en 44.583 tríos de PvP). Cada combinación muestra de dónde sale
  cada punto (cada línea del liderazgo, con lo que suma), y el liderazgo condicional dice qué parte
  cuenta. Los pesos se revisan con casos (ver *Casos de referencia*).
- Sin contexto (los puntos para él, las tier lists, tus equipos, los favoritos, la comparativa y
  «cómo entraría»), el líder sale de la misma función: el que más suma con su liderazgo en la
  sinergia (cada slot que le llega y le sirve a otro: 3 si es Notable, 2 si no); a igual puntaje, el
  mejor ubicado en la General de thanosvibs, y después la clave. Antes era el que más le sumaba al
  personaje de la ficha y, a igual puntaje, el primero: el mismo trío salía con otro líder según
  desde qué lista se lo mirara, y la tarjeta de PvP decía un líder y contaba los puntos «para él»
  con otro. En una tarjeta de PvP o PvE, esos puntos se cuentan con el líder del contexto. Tus
  equipos se guardan en un orden fijo: el mismo equipo, guardado desde dos listas, es uno.
- Con los datos actuales, la lista de PvP de Knull — Ancient History tiene 1.956 equipos. Las de
  Galactus y de Jean Grey — Summer Flare Phoenix tienen unos 36.500 (36.488 y 36.219): sus
  liderazgos dan anti-mermas a cualquiera, así que con ellos de líder cualquier trío con un DPS
  cumple. Con el líder único bajaron (Galactus tenía 37.514, Jean Grey 37.089 y Knull 1.979): un
  compañero que se vinculaba con él solo por su liderazgo ya no se vincula si no es el líder del
  equipo. Con lo propio, la de Knull subió de 1.915 a 1.956, porque su pasiva de Tier-2 le da
  anti-mermas.
- Con los liderazgos de la Leader Skill (medido sobre los datos de formato 7 con lo que va a derivar el
  próximo build; *Liderazgos que Leads & Supports no publica*), las variantes con función siguen
  siendo 60 en PvP y 119 en PvE, y todas tienen lista. Las listas de PvP suman 479.581 combinaciones
  en vez de 460.726 (crecen 46 y se achican 7), y las de PvE 2.502.520 en vez de 2.066.097 (crecen 77
  y se achican 10). La de PvP de Knull — Ancient History pasa de 1.956 a 2.178, la de Galactus de
  36.488 a 36.499, la de Jean Grey — Summer Flare Phoenix de 36.219 a 36.235 y la de Thanos —
  Annihilation de 8.787 a 8.907 [Comprobado]. Crecen porque un compañero con un liderazgo derivado
  se vincula cuando lidera, y casi todos los derivados le sirven a cualquiera. Se achican porque el
  vínculo de cada compañero sale de la consulta, que lo calcula con el líder sin contexto: en la lista
  de PvP de Malekith — All-New, All-Different (de 4.826 a 3.631), el trío con Silver Surfer
  (Shalla-Bal) y Vision — Ultimate Vision tenía a Vision de líder sin contexto; ahora Silver Surfer
  (Shalla-Bal) tiene un liderazgo derivado (Debuff Duration −24%), empata en puntos con el de Vision y
  lidera por la General, así que Vision ya no se vincula con Malekith y el trío sale de la lista,
  aunque en PvP el líder sería Vision (15,5 puntos) [Comprobado]. Falta decidir si en PvP y PvE el
  vínculo tiene que salir del líder del contexto.

### Casos de referencia

Los pesos se revisaron con cuatro pares reales que Ezequiel comparó (2 de octubre de 2026). Quedaron
como estaban; lo que cambió es que en PvP cuentan las defensas del liderazgo. Con el líder único y
el condicional a la mitad solo cambia el de Thor en PvP, que ahora gana por puntaje. Sin los strikers
en el puntaje (4 de octubre de 2026), los cuatro siguen ganando por puntaje. Con la tabla de valor
(4 de octubre de 2026: en PvP, vida 2,5, ataques 2, defensas 1,5, ignorar evasión 1 y efecto de los
debuffs 0,5) también: Thanos — Annihilation le sigue ganando a Black Cat — Queen in Black (su
liderazgo suma 10,5 contra 9), y en el par de Galactus lidera Wasp, cuyo liderazgo suma 10,5.

| Contexto y foco | Mejor, según Ezequiel | Contra | Puntos: antes → con defensas | Con líder único | Sin strikers | Con la tabla de valor |
|---|---|---|---|---|---|---|
| PvP, Galactus | Thanos — Annihilation (líder) + Kang — Rama-Tut: tres DPS | Black Cat — Queen in Black (líder; con la tabla, Wasp) + Wasp — Quantumania: un DPS | 21 a 22 → 27 a 22 | 27 a 22 | 26 a 20 | 24,5 a 18,5 |
| PvE, Thor | Phil Coulson — Winter Ops + Invisible Woman — The Fall of the Fantastic Four (líder): un DPS | Crystal — Spring Lady (líder) + Mephisto — Master of Hell: dos DPS | 25 a 24, igual | 25 a 24 | 19 a 18 | 19 a 18 |
| PvP, Thor | Wasp — Quantumania (líder) + Sentry — Thunderbolts*: un DPS | Silver Surfer — Void Knight (líder) + Gorr: dos DPS | 21 a 21 → 27 a 27 | 27 a 21 | 21 a 18 | 19,5 a 17,25 |
| PvP, Jean Grey — Summer Flare Phoenix | Black Cat — Queen in Black (líder) + Invisible Woman — First Steps: un DPS | Knull + Gorr: tres DPS GOd | 26 a 21, igual | 26 a 21 | 23 a 19 | 20 a 19 |

- **Galactus.** «Thanos es el mejor líder por el agregado de las mermas y mejoras de daños y
  defensa, y los 3 son DPS»; Black Cat + Wasp «es una opción depositando todo el peso en que
  Galactus haga el trabajo». El liderazgo de Thanos trae Remove All Debuffs, todos los ataques +50%
  y todas las defensas +40%; con los stats de antes solo contaban los ataques (6), y a Black Cat
  (ataques +65%, ignorar evasión +35%) le contaban los dos (12). Con el líder único, Black Cat y
  Wasp empatan en puntos y en puesto, y lidera Black Cat por la clave. Con la tabla de valor, el de
  Thanos suma 10,5 (ataques 6, defensas 4,5) y el de Black Cat 9 (ataques 6, ignorar evasión 3); en
  su par lidera Wasp, con 10,5.
- **Thor.** No tiene función en PvP ni en PvE (Ezequiel): los pares valen por los otros dos. En PvP
  eligió el primero «en caso de que haya que sumarlo». Con la 1.0.15 empataban y desempataba la tier
  list, que ponía primero al segundo; con los strikers a 2 ganaba el primero, pero decidían listas
  enteras (con Apocalypse — Heralds of Apocalypse, Deadpool + Stryfe quedaba arriba de Jean Grey +
  Wolverine solo por cuatro strikers), contra la regla de que no son definitorios. Con el
  condicional a la mitad gana el primero, 27 a 21: los ataques y las defensas de Silver Surfer —
  Void Knight se activan al recibir un debuff, y su liderazgo baja de 12 a 6.
- **Jean Grey.** Knull y Gorr no pueden liderar: solo Jean Grey, con su liderazgo, les da
  anti-mermas a los tres, y ese liderazgo no trae nada que valga en PvP. El liderazgo de Black Cat
  no trae anti-mermas, así que solo sirve si un soporte se los da a los tres (Ezequiel): acá, el de
  Invisible Woman; con Galactus, el de Wasp.
- **Silver Surfer — Void Knight, Knull — Ancient History y Gorr — The God Butcher (PvP).** Ezequiel:
  «Gorr es notoriamente mejor liderazgo para villanos», y no tiene sentido contar como dos equipos el
  mismo trío con otro orden. Los dos dan el mismo anti-mermas (al recibir un debuff, 12 s, recarga
  20 s). Gorr da PG +35% permanente a los supervillanos, y el uniforme Void Knight lo es: 6. Silver
  Surfer da ataques y defensas +30% solo al recibir un debuff: 12 con la 1.0.15, 6 a la mitad.
  Empataban y lideraba Gorr por la tier list de Arena (GOd contra Niche), con 26 puntos en las listas
  de los tres (24 sin los strikers): ganaba por desempate, no por peso. Con la tabla de valor gana
  por peso: la vida de Gorr suma 7,5 y el liderazgo condicional de Silver Surfer, 5,25; el trío, 25,5.
  Antes lideraba Silver Surfer: con la 1.0.14, en su lista y en la de Knull; con la 1.0.15, en las
  tres, con 32.
- **Doctor Voodoo — Savage Avengers en la lista de PvP de Adam Warlock**, con Wasp — Quantumania de
  líder. Su pasiva de uniforme es solo para Universales, pero entra por la Tier-2, «Voodoo Shield»:
  ignora la evasión del objetivo 30% para todos los aliados (así lo publican la API de skills, «All
  Allies for the first effect, Self for the second effect», y Leads & Supports). Ezequiel lo
  confirmó (3 de octubre de 2026): el equipo está bien armado.

Lo que todavía no está:
- El artefacto de Robbie Reyes (fuego según la resistencia, para los aliados Llama) depende de que
  él esté en el equipo, y la regla de «le sirve» no ve el equipo.
- Las filas de soporte y de líder (rigged leaders de Arena) no suman por sí mismas: un soporte vale
  por lo que les da a los otros.
- Los efectos de artefacto cuentan como si lo llevara.
- El daño contra una facción no cuenta en el liderazgo de PvP: es la comparación dudosa de las
  reglas. Con los datos actuales lo trae un solo liderazgo, el de Dormammu — Damnation (daño a
  héroes +60%).
- Molecule Man, «la excepción rara» (Ezequiel). Su liderazgo ignora los aumentos y las bajas de
  daño entre facciones («Ignores Damage Increase/Decrease Effect Between Self and Opposing
  Faction») y baja 15% el daño recibido de golpes en cadena, y el segundo les quita todos los
  debuffs a todos. En PvP no le suma nada fuera de los anti-mermas, y no está en la tier list de
  Arena, así que tampoco tiene lista de PvP. Falta decidir cómo cuenta.
- Los compañeros sin función en el contexto entran igual si tienen vínculo con él: con Knull —
  Ancient History en PvP, Thor — All-Father Reborn queda en el puesto 18. Ezequiel decidió que el
  personaje de la ficha sin función no tiene lista; para los compañeros, falta decidir.

## Fuentes

- thanosvibs: API de personajes, de skills y de [Leads & Supports](https://thanosvibs.money/supports);
  Beginner's Guide, [parte 1](https://thanosvibs.money/beginners/1),
  [parte 3](https://thanosvibs.money/beginners/3) y [parte 4](https://thanosvibs.money/beginners/4)
  (versión 12.1.5); [Alliance Battle](https://thanosvibs.money/abxl) (qué controles cortan el ataque
  especial de los jefes).
- Future Fight Wiki: infobox de cada personaje; páginas
  [Combat](https://future-fight.fandom.com/wiki/Combat), [Blast](https://future-fight.fandom.com/wiki/Blast),
  [Speed](https://future-fight.fandom.com/wiki/Speed) y [Universal](https://future-fight.fandom.com/wiki/Universal).
- El juego (capturas de Ezequiel, octubre de 2026): la guía (Type Affinity, Side, Instinct, los
  glosarios de contenidos, de crecimiento, de ítems y de skills), la ficha de cada C.T.P. y las
  pantallas de personaje y de equipo.
- NamuWiki, en coreano: [World Boss](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%EC%9B%94%EB%93%9C%20%EB%B3%B4%EC%8A%A4),
  [sus strikers](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%EC%9B%94%EB%93%9C%20%EB%B3%B4%EC%8A%A4/%EC%8A%A4%ED%8A%B8%EB%9D%BC%EC%9D%B4%EC%BB%A4),
  [Legend](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%EC%9B%94%EB%93%9C%20%EB%B3%B4%EC%8A%A4/%EB%A0%88%EC%A0%84%EB%93%9C),
  [héroes](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%EC%98%81%EC%9B%85)
  y [Timeline](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%20%EB%B0%B0%ED%8B%80)
  (4 de octubre de 2026). No se pudieron leer las fichas de personaje de NamuWiki, Reddit, DC
  Inside ni el foro de Netmarble.
