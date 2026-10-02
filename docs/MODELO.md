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
| Clase | Combate, Detonación, Velocidad, Universal | Ventaja de tipo: más daño contra la clase a la que le gana y menos daño recibido de ella. Combate le gana a Velocidad, Velocidad a Detonación y Detonación a Combate. Universal le gana a las otras tres con una ventaja menor y no tiene debilidad. Restringe liderazgos y soportes. | thanosvibs (`type`); wiki (páginas de cada clase); guía de thanosvibs, parte 3 (Type Enhancement); la ventaja de Universal, confirmada por Ezequiel; el ciclo, también la guía del juego (Type Affinity) |
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
las dos apunten a los mismos efectos (124, en 16 grupos) y responde una sola vez, por efecto, lo
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
seducir, control mental, pánico). Dentro del mismo juego hay diferencias de traducción: el glosario
dice que la barrera frena el daño «por un tiempo» y las skills la cuentan en golpes («# time(s)»).

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
   que la skill no dice (los «Give Power» vacíos) y los marcadores (`$HEROSUBTYPE1`) completados
   con la facción, el tipo o la raza que Leads & Supports escribe.
2. La regla de «a quién le sirve» del catálogo reemplaza a la que hoy tiene la app para la
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
- El juego (capturas de Ezequiel, octubre de 2026): la guía (Type Affinity, Side, Instinct y el
  glosario de skills: Guard Break) y la ficha de cada C.T.P.
