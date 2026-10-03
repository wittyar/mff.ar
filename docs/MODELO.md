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

- **Habilidad de World Boss.** Cada variante tiene una, siempre una de sus habilidades. Falta saber
  para qué se usa en el juego.
- **Villains en las etapas.** El juego llama «SUPER VILLAIN faction» al bando Supervillano (C.T.P.
  Insight; los artefactos de thanosvibs, igual) y Leads & Supports lo llama «Villains». La guía del
  juego dice que dentro de una etapa los Super Villains, que son jefes, y los Villains son facciones
  distintas; la línea siguiente quedó cortada en la captura. Falta saber si un efecto contra el bando
  Supervillano les pega a los Villains comunes de una etapa.
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
| A quién le sirve | Una regla por efecto: a cualquiera del equipo, a quien escala con un ataque, a quien tiene un elemento, a quien hace daño físico, aplica debuffs, invoca, tiene definitiva de Tier-3 o Striker, o solo a él. Se compara con el perfil de combate de la etapa 1 y con sus skills. |
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
- **Códigos.** Algunas descripciones traen un número donde va el nombre de un efecto o de un elemento.
  Los de tres cifras son ids de habilidades de la propia API (`206` es «Removes all Debuffs»).

Quedan 5 efectos, en 4 retratos, que no aparecen en la skill del mismo nombre; se revisan cuando el
cruce sea parte del build.

A algunos uniformes Leads & Supports no los incluye en ninguna entrada, aunque su Leader Skill es la
de su base: Knull — Ancient History (`knull1`) quedaba sin liderazgo. El build les da el liderazgo de
su base (solo `leader` y `leader2`, no los soportes) cuando su Leader Skill, en la API de skills, es
idéntica a la de la base (Ezequiel, 2 de octubre de 2026; `completar_liderazgos` en
`scripts/fuentes.py`). Los completados y los que no cierran, con su diferencia, están en la sección
12 de `docs/AUDITORIA.md`.

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
  증폭, amplificación de elemento: el reforjado de Judgement que en inglés se llama así es un problema
  de traducción (el hallazgo de los C.T.P., en `docs/AUDITORIA.md`).
- **Penetration** es 간파, «ver a través»: no es la Perforación. Es el efecto del reforjado de
  Regeneration que corta el ataque del rival con una rotura de guardia, como dice la guía de
  thanosvibs.

Confirma lo que el catálogo ya decía del encanto (frena también los ataques que se activan solos),
la elasticidad (la saca el sangrado; la cancelación y la incapacitación, no), la fractura y lo que
no se le aplica a quien quita todos los debuffs (la marca, en cambio, sí). Y dice cosas de efectos
que el catálogo todavía no tiene: el contraataque no se activa mientras el personaje es invencible,
el muro (Wall) no se usa junto con la barrera ni se suma a la reducción de daño, Enraged (reforjado
de Rage) ignora el tope de daño crítico y Vitality (reforjado de Refinement) da inmunidad a la
rotura y a la superrotura de guardia, y vida por segundo.

Los 44 términos, con estas diferencias y los efectos del catálogo que les corresponden, están en
`scripts/contenido/glosario.json`, y la app los muestra en la solapa **Glosario**.

### Dudas abiertas del catálogo

- **«Bonus Damage».** La guía llama «Skill Damage» a la parte del golpe que sale del ataque y
  «Additional Damage» al daño fijo extra; no dice si «Bonus Damage» es ese daño fijo.
- **«Adaptation».** «Inmune al mayor daño recibido»: no está claro si es el golpe más fuerte o el
  tipo de daño que más recibe.
- **Códigos sin nombre.** En «Natural Enemy», 401 es Mockery y 108 Shock (ids de la API); 407 y 577
  no son el id de ninguna habilidad de las skills (Leads & Supports nombra 407 «Debuff Removal
  (Instinct)»). La app todavía muestra los números: podría mostrar el nombre de los que tienen id.
- **Efectos para todo el equipo que se repiten.** Los C.T.P. Insight y Liberation dicen en el juego
  que su efecto para todo el equipo no se aplica dos veces si lo llevan dos. Falta saber si pasa lo
  mismo con los soportes de los personajes; la sinergia hoy cuenta cada uno por quien lo da.

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
  lo que otorga viene después, en la misma etapa o en las que siguen. Si no le sigue nada, la fuente
  no dice qué otorga, y el análisis lo muestra así (74 casos en estos datos). Lo que el catálogo no
  clasifica también se ve, como lo publica la fuente.

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
2. La regla de «a quién le sirve» del catálogo reemplaza a la que hoy tiene la app para la
   sinergia y el índice de equipos.

## Lo que muestran las pantallas del juego

Capturas de Ezequiel (octubre de 2026), de su cuenta.

- **Mejora de tipo (Type Enhancement).** Cada personaje la sube por niveles. En el máximo (6), una
  clase hace 60% más de daño normal a la clase a la que le gana y recibe 45% menos de ella (Thanos,
  Adam Warlock y un Velocidad, uno de cada clase). Universal solo sube el daño, igual contra las
  otras tres: 17,5% en el nivel 5 (Gorr), sin reducción del daño recibido. El juego muestra además
  un valor entre paréntesis (+30%, +15%, +12,5%) que esa pantalla no explica.
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
  Kahhori, entre otros) y los de estrellas. namu.wiki tiene solo seis de ejemplo. Ver *Bonos de
  equipo* más abajo.
- **Lo que suma la cuenta.** El nivel de agente, las cartas de cómic (5, en dos mazos que se asignan
  por contenido), las espadas (X of Swords) y el S.H.I.E.L.D. Archive (stats de instinto) valen
  para todos los personajes; los emblemas, solo en ciertos contenidos; las colecciones de equipo
  (Team-Up), para los de un tema o una raza. Suben los stats de todos por igual o de un grupo: no
  cambian la comparación entre variantes, salvo las colecciones de equipo.
- **C.T.P. por contenido.** Cada personaje lleva un C.T.P. (desde el Nv. 30), y la pantalla deja
  elegir uno para PvE y otro para PvP.
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
171 de 290 páginas (unas 7.000 filas), y la de Kingpin coincide con la del juego (capturas de
Ezequiel, octubre de 2026). Les falta a 119 personajes, casi todos recientes (Galactus, Annihilus,
Apocalypse, entre otros): en la app no tienen strikers propios, aunque pueden ser strikers de otros.
Lo que no se pudo leer va a `docs/AUDITORIA.md` (sección 11).

Dudas:
- **Set Striker.** El juego tiene además un striker que se elige para cada personaje (solo de 6★ o
  más), que aparece con su Striker Skill y cuyo efecto crece con el tier (captura de Galactus con
  Silver Surfer). Es otro sistema: la app no lo tiene.

## Equipos por contexto

Reglas de Ezequiel para armar equipos (2 de octubre de 2026):

- **PvP:** los tres tienen que tener anti-mermas (quitar todos los debuffs), del liderazgo del
  líder o del soporte de alguno; un equipo de PvP sin anti-mermas es un mal equipo. Si viene de un
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
- **Sinergia y strikers:** relevantes, no definitorios. El striker tiene que estar en el mismo equipo.
- **Líder:** un trío tiene un solo líder, el mismo en las listas de los tres: el orden solo cambia
  cuando hay un peso real distinto entre las opciones. Un liderazgo que se activa con una condición
  (al recibir un debuff, por ejemplo) pesa la mitad, sin mirar los porcentajes (Ezequiel, 2 de
  octubre de 2026: «único + condicional a la mitad»; ver *Casos de referencia*).
- **Ataque contra daño a una facción:** para hacer daño hay que tener ataque suficiente para
  superar la defensa o la esquiva del rival, y eso pesa al armar un equipo. Lo dudoso es comparar
  un porcentaje de ataque con un daño agregado contra una facción: no está claro cuál aporta más,
  siempre que haya anti-mermas. La excepción rara es el liderazgo de Molecule Man.

Cómo lo aplica la app, en las combinaciones de 3 de la pestaña *Equipos* (órdenes PvP y PvE):

- Quién es DPS, soporte o líder en cada contexto sale de las filas de las tier lists de thanosvibs:
  Arena de Equipos para PvP; Batalla de Alianza y World Boss Legend para PvE
  (`scripts/contenido/roles_listas.json`, con el rótulo de cada fila; el build para si una cambia).
  Así quedan los ejemplos: Agent 13 no está en ninguna, Black Cat es soporte y Apocalypse es DPS.
- Sin función en el contexto, no hay lista: si el personaje no figura en las tier lists del
  contexto, o solo como «Not for wbl», el orden de ese contexto no arma combinaciones y la pestaña
  lo dice (Ezequiel, 2 de octubre de 2026: Thor base no tiene función en PvP ni en PvE). Con los
  datos actuales tienen función 60 de las 888 variantes en PvP y 119 en PvE.
- Un trío entra si alguno es DPS de ese contexto y, en PvP, si con algún líder los tres tienen
  anti-mermas (Remove All Debuffs o Debuff Immunity). Cada compañero tiene vínculo con él o es DPS
  de ese contexto.
- Puntaje: 2 por cada stat del liderazgo que vale y cada integrante al que le llega y le sirve
  (cada stat una vez, aunque el liderazgo lo traiga en varias líneas; 1 si solo le llega por un
  liderazgo que se activa con una condición, el slot con `ac`); 2 por cada nivel de fila de cada
  DPS (3 la más alta); 1 por cada soporte que le llega a otro y le sirve, por cada bono de equipo
  activo y por cada striker del trío. El líder es el que más suma de los que cumplen y no depende
  del orden del trío: a igual puntaje, el mejor ubicado en las tier lists del contexto (la suma de
  su puesto en cada una) y después la clave. Hasta la 1.0.15, a igual puntaje ganaba el primero del
  trío, que es siempre el personaje de la ficha, así que el mismo trío salía con otro líder en cada
  lista (con los datos de la 1.0.14, en 44.583 tríos de PvP). Cada combinación muestra de dónde sale
  cada punto, y el liderazgo condicional dice que cuenta la mitad. Los pesos se revisaron con casos y
  quedaron así (ver *Casos de referencia*).
- Con los datos actuales, la lista de PvP de Knull — Ancient History tiene 1.993 equipos. Las de
  Galactus y de Jean Grey — Summer Flare Phoenix tienen unos 37.000: sus liderazgos dan
  anti-mermas a cualquiera, así que con ellos de líder cualquier trío con un DPS cumple.

### Casos de referencia

Los pesos se revisaron con cuatro pares reales que Ezequiel comparó (2 de octubre de 2026). Quedaron
como estaban; lo que cambió es que en PvP cuentan las defensas del liderazgo. Con el líder único y
el condicional a la mitad solo cambia el de Thor en PvP, que ahora gana por puntaje.

| Contexto y foco | Mejor, según Ezequiel | Contra | Puntos: antes → con defensas | Con líder único |
|---|---|---|---|---|
| PvP, Galactus | Thanos — Annihilation (líder) + Kang — Rama-Tut: tres DPS | Black Cat — Queen in Black (líder) + Wasp — Quantumania: un DPS | 21 a 22 → 27 a 22 | 27 a 22 |
| PvE, Thor | Phil Coulson — Winter Ops + Invisible Woman — The Fall of the Fantastic Four (líder): un DPS | Crystal — Spring Lady (líder) + Mephisto — Master of Hell: dos DPS | 25 a 24, igual | 25 a 24 |
| PvP, Thor | Wasp — Quantumania (líder) + Sentry — Thunderbolts*: un DPS | Silver Surfer — Void Knight (líder) + Gorr: dos DPS | 21 a 21 → 27 a 27 | 27 a 21 |
| PvP, Jean Grey — Summer Flare Phoenix | Black Cat — Queen in Black (líder) + Invisible Woman — First Steps: un DPS | Knull + Gorr: tres DPS GOd | 26 a 21, igual | 26 a 21 |

- **Galactus.** «Thanos es el mejor líder por el agregado de las mermas y mejoras de daños y
  defensa, y los 3 son DPS»; Black Cat + Wasp «es una opción depositando todo el peso en que
  Galactus haga el trabajo». El liderazgo de Thanos trae Remove All Debuffs, todos los ataques +50%
  y todas las defensas +40%; con los stats de antes solo contaban los ataques (6), y a Black Cat
  (ataques +65%, ignorar evasión +35%) le contaban los dos (12). Con el líder único, Black Cat y
  Wasp empatan en puntos y en puesto, y lidera Black Cat por la clave.
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
  Empatan y lidera Gorr por la tier list de Arena (GOd contra Niche), con 26 puntos en las listas de
  los tres: gana por desempate, no por peso. Antes lideraba Silver Surfer: con la 1.0.14, en su lista
  y en la de Knull; con la 1.0.15, en las tres, con 32.
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
  glosarios de contenidos, de crecimiento y de skills), la ficha de cada C.T.P. y las pantallas de
  personaje y de equipo.
