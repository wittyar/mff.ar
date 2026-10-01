# Modelo del juego

La app arma un modelo por **variante** (un personaje con un uniforme) a partir de las fuentes, en
vez de mostrar cada fuente por separado. Cada dato dice de dónde sale y lo que se deduce dice con
qué regla. La ficha, el roster, la sinergia y las combinaciones leen del modelo.

Este documento es el mapa de ese modelo y se completa por etapas. Lo que no está comprobado va
marcado como probable o como duda.

## Decisiones (Ezequiel, 1 de octubre de 2026)

- PvE y PvP se evalúan a la par, cada uno con su lectura.
- Sin topes: un efecto cuenta por lo que da, aunque ese stat ya esté al tope.
- Sin números: el modelo dice qué da cada cosa, a quién le llega y si le sirve; no estima el daño.
- La «mesa» es la tabla de datos del modelo. Se define al final, con lo aprendido en las etapas
  anteriores.

## Etapas

1. **Personajes y características**: qué es cada variante (identidad y perfil de combate).
2. **Skills**: qué hace cada efecto (las 228 etiquetas tipadas de thanosvibs), a quién apunta y
   cómo se lee en PvE y en PvP. Los roles se rehacen acá.
3. **Pasivas, liderazgos y soportes**: su efecto sobre los stats y para quién sirven. Junta las
   skills con Leads & Supports de thanosvibs, que son el mismo efecto visto de dos lados (de ahí
   sale, por ejemplo, que el efecto de uniforme de General's Hand es contra Universales).
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

## Fuentes

- thanosvibs: API de personajes, de skills y de [Leads & Supports](https://thanosvibs.money/supports);
  Beginner's Guide, [parte 3](https://thanosvibs.money/beginners/3) y
  [parte 4](https://thanosvibs.money/beginners/4) (versión 12.1.5).
- Future Fight Wiki: infobox de cada personaje; páginas
  [Combat](https://future-fight.fandom.com/wiki/Combat), [Blast](https://future-fight.fandom.com/wiki/Blast),
  [Speed](https://future-fight.fandom.com/wiki/Speed) y [Universal](https://future-fight.fandom.com/wiki/Universal).
