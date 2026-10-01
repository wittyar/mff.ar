# Catálogo de efectos

Generado por `scripts/catalogo.py` el 2026-10-01, sobre los datos del juego 12.2.5, desde `scripts/contenido/catalogo.json` (contenido curado: se edita ahí, no acá).

thanosvibs publica el mismo efecto de dos lados que no se cruzan: las skills lo traen como una etiqueta (`ALL BASIC ATTACKS INCREASE`) y Leads & Supports como un stat (`All Basic Attacks`). Acá los dos apuntan al mismo efecto, y cada efecto dice qué es, a quién le sirve y cómo se lee en PvE y en PvP. Cuándo se activa y a quién le llega no es del efecto sino de cada skill o soporte (su activación, su objetivo, su restricción): eso lo muestra la ficha.

## Cómo se lee

- **Se aplica:** a su lado (él o los aliados que diga el objetivo de la skill) o al rival.
- **Le sirve:** a quién le aporta algo, según con qué pega cada variante (docs/MODELO.md, perfil de combate).
- **PvE / PvP:** la lectura de cada modo. Si el efecto no trae una propia, vale la de su grupo.
- **Certeza:**
  - [Comprobado] Lo dice una fuente (citada).
  - [Probable] Se deduce del texto del efecto.
  - [Conjetura] Suposición sin fuente.
- **Skills:** las etiquetas que apuntan al efecto, de la más usada a la menos, con cuántos retratos la usan.
- **Leads & Supports:** los stats que apuntan al efecto, con cuántos retratos lo dan.

16 grupos, 124 efectos, 228 etiquetas de skills y 72 stats de Leads & Supports. Todo lo que traen los datos está clasificado.

## Golpe

El daño de la skill: lo que todo lo demás potencia.

- **PvE:** Es el daño del personaje. [Probable]
- **PvP:** Es el daño del personaje. [Probable]

### Daño de la skill

`golpe` · Skill hit · Se aplica al rival · Le sirve: a él (es parte de su kit).

- **Skills:**
  - `PHYSICAL ATK DAMAGE` (501 retratos)
  - `ENERGY ATK DAMAGE` (389 retratos)
  - `HP DAMAGE` (6 retratos)

## Ataque

Sube un ataque, el stat del que sale el daño.

- **PvE:** Sube el daño de quien escala con ese ataque. Cada personaje escala con uno solo. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Sube el daño de quien escala con ese ataque. Cada personaje escala con uno solo. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))

### Ataque físico

`ataque_fisico` · Physical Attack · Se aplica a su lado · Le sirve: a quien escala con el ataque físico.

- **Skills:**
  - `PHYSICAL ATTACK ↑` (114 retratos)
  - `Explosion`, con `Physical Attack increases by #% every # sec (up to #%)` (26 retratos) — varía: crece cada unos segundos
- **Leads & Supports:**
  - `Physical Attack` (57 retratos)

### Ataque de energía

`ataque_energia` · Energy Attack · Se aplica a su lado · Le sirve: a quien escala con el ataque de energía.

- **Skills:**
  - `ENERGY ATTACK ↑` (139 retratos)
  - `Explosion`, con `Energy Attack increases by #% every # sec (up to #%)` (26 retratos) — varía: crece cada unos segundos
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of Energy Attack each #% of pure damage accumulated` (2 retratos) — varía: crece con el daño puro acumulado
- **Leads & Supports:**
  - `Energy Attack` (81 retratos)

### Todos los ataques básicos

`ataques_todos` · All Basic Attacks · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Le rinde a cualquiera igual que su propio ataque. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Le rinde a cualquiera igual que su propio ataque. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `FRENZY` (491 retratos)
  - `ALL BASIC ATTACKS INCREASE` (411 retratos)
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of All Basic Attacks each #% of pure damage accumulated` (321 retratos) — varía: crece con el daño puro acumulado
  - `Increases all Basic Attacks` (266 retratos)
  - `Increases all Basic Attacks and Defenses` (220 retratos)
  - `Increases all basic stats` (220 retratos)
  - `INCREASES ALL BASIC ATTACKS PER HP LOST` (77 retratos) — varía: crece con el daño recibido
  - `ENLARGE`, con `Increases character size by #%, all Basic Attacks by #%^, all Basic Defenses by #%.` (35 retratos)
  - `ATK PER SUPER HIT SHIELD INCREASE` (12 retratos) — varía: según su escudo
  - `Misdirection` (9 retratos) — varía: crece cada vez que recibe un golpe
  - `Camouflage` (8 retratos)
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of All Basic Attacks, Critical Rate each #% of pure damage accumulated` (7 retratos) — varía: crece con el daño puro acumulado
  - `Increases all Attacks, Defense and Speed relative to HP` (6 retratos) — varía: según su vida
  - `MINIATURIZE`, con `Decreases character size by #%, increases all Basic Attacks by #%^, all Basic Defenses by #%.` (6 retratos) — Nota: Achica al personaje (y le sube ataques y defensas) o al rival (y le baja los suyos): lo distingue el texto. Que el segundo vaya al rival lo dicen el texto y la activación «When attacking an enemy with MINIATURIZE effect applied».
  - `Attack per Recharge Shield (Consumption) Increase` (5 retratos) — varía: crece con el escudo que gasta
  - `Absorb` (4 retratos) — varía: el ataque crece con cada absorción
  - `ENLARGE`, con `Increases character size by #% and all Speeds, all Basic Attacks by #%.` (4 retratos)
  - `Mockery` (4 retratos)
  - `Increases all Basic Attacks per summoned character` (2 retratos) — varía: por cada invocación viva
  - `Condensed Power` (1 retrato) — varía: se acumula
  - `Demonization (Darkchylde)` (1 retrato)
  - `Increases Accumulative ATK` (1 retrato) — varía: se acumula
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of All Basic Attacks, Critical Damage each #% of pure damage accumulated` (1 retrato) — varía: crece con el daño puro acumulado
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of All Basic Attacks, Critical Rate, Critical Damage each #% of pure damage accumulated` (1 retrato) — varía: crece con el daño puro acumulado
- **Leads & Supports:**
  - `All Basic Attacks` (180 retratos)
  - `All Basic Attacks (Stackable)` (5 retratos) — varía: se acumula

## Daño

Sube el daño que hace, aparte del ataque.

- **PvE:** Sube el daño. Un buff de daño multiplica al de elemento en vez de sumarse (el ejemplo de la guía). [Probable] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Sube el daño. [Probable]

### Daño básico

`dano_basico` · Basic damage · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Sube el daño. Es el efecto del proc de los obeliscos («Increases basic damage by x% for 1 attack(s)»), que según la guía sube mucho el daño. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Sube el daño. Es el efecto del proc de los obeliscos («Increases basic damage by x% for 1 attack(s)»), que según la guía sube mucho el daño. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `SKILL DAMAGE ↑` (475 retratos) — dura unos ataques
  - `Basic Damage Increase (Influence)` (49 retratos) — varía: baja con el tiempo
  - `Evasion Reload` (26 retratos)
  - `Increases a stack of basic damage` (21 retratos) — varía: se acumula
  - `Increases skill damage relative to HP` (3 retratos) — varía: crece con la vida que gana
  - `Damage Increase with Fewer Enemies` (2 retratos) — con pocos enemigos cerca
  - `Body Enhancement` (1 retrato) — varía: el daño crece con cada golpe que ignora

### Daño de skill

`dano_skill` · Skill damage · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** La guía llama «Skill Damage» a la parte del golpe que sale del ataque y «Additional Damage» al daño fijo extra; no aclara si «Bonus Damage» es ese daño fijo.
- **Skills:**
  - `SKILL AND BONUS DAMAGE ↑` (627 retratos)
- **Leads & Supports:**
  - `Skill Damage` (6 retratos)

### Daño extra (Bonus)

`dano_extra` · Bonus damage · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** La guía llama «Skill Damage» a la parte del golpe que sale del ataque y «Additional Damage» al daño fijo extra; no aclara si «Bonus Damage» es ese daño fijo.
- **Skills:**
  - `SKILL AND BONUS DAMAGE ↑` (627 retratos)
- **Leads & Supports:**
  - `Bonus Damage` (6 retratos)

### Daño final

`dano_final` · Final damage · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Valor` (10 retratos) — según la vida máxima del rival frente a la suya
  - `Increases Final Damage` (5 retratos)

### Daño contra ciertos rivales

`dano_contra` · Damage against some foes · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Sube el daño solo contra esos rivales. [Probable]
- **PvP:** Sube el daño solo contra esos rivales. [Probable]
- **Skills:**
  - `Increases basic damage based on character's faction` (139 retratos) — contra una facción (cada skill dice cuál)
  - `Vigor` (28 retratos) — contra rivales con la vida baja
  - `Increases basic damage when attacking boss types` (25 retratos) — contra jefes
  - `Bravery` (23 retratos) — según la vida máxima del rival frente a la suya
  - `Natural Enemy` (16 retratos) — contra rivales con un efecto dado; Nota: La fuente publica el efecto como un código; en Leads & Supports el mismo efecto aparece con nombre («Removes All Debuffs»).
  - `Strength` (16 retratos) — contra rivales con la vida alta
  - `Increases basic damage based on character's type` (10 retratos) — contra un tipo (cada skill dice cuál)
  - `Increases basic damage based on character's race` (9 retratos) — contra una raza (cada skill dice cuál)
  - `INCREASES BASIC DAMAGE WHEN ATTACKING CHARACTERS WITH ABILITIES` (7 retratos) — contra quien tiene una habilidad (cada skill dice cuál)
  - `INCREASES BASIC DAMAGE BASED ON CHARACTER'S GENDER` (6 retratos) — contra un género (cada skill dice cuál)
  - `Increases basic damage when attacking characters without abilities.` (3 retratos) — contra quien no tiene una habilidad (cada skill dice cuál)
  - `Demonize` (2 retratos) — contra una facción (cada skill dice cuál)
  - `All Basic Damage Increased Except Specific Species` (1 retrato) — contra todos menos una raza (cada skill dice cuál)
  - `Luck` (1 retrato) — contra todos menos los jefes
- **Leads & Supports:**
  - `Basic Damage Dealt to Villains` (85 retratos) — contra una facción: Supervillano
  - `Basic Damage Dealt to Boss Types` (44 retratos) — contra jefes
  - `Basic Damage Dealt to Heroes` (41 retratos) — contra una facción: Superhéroe
  - `Basic Damage Dealt to Males` (6 retratos) — contra un género: Masculino
  - `Basic Damage Dealt to Enemies with 25% HP or Higher` (4 retratos) — contra rivales con la vida alta
  - `Basic Damage Dealt to Universals` (3 retratos) — contra un tipo: Universal
  - `Basic Damage Dealt to Enemies except Mutant Characters` (1 retrato) — contra todos menos una raza: Mutante
  - `Basic Damage Dealt to Enemies with "Debuff Removal (Instinct)" Effect` (1 retrato) — contra rivales con un efecto dado
  - `Basic Damage Dealt to Enemies with "Removes All Debuffs" Effect` (1 retrato) — contra rivales con un efecto dado
  - `Basic Damage Dealt to Females` (1 retrato) — contra un género: Femenino

### Probabilidad de crítico

`critico` · Critical rate · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Más golpes críticos. En pelea se reduce según el nivel del rival: la guía dice contar la mitad. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Más golpes críticos, con la misma reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `FRENZY` (491 retratos)
  - `CRITICAL RATE ↑` (311 retratos)
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of All Basic Attacks, Critical Rate each #% of pure damage accumulated` (7 retratos) — varía: crece con el daño puro acumulado
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of All Basic Attacks, Critical Rate, Critical Damage each #% of pure damage accumulated` (1 retrato) — varía: crece con el daño puro acumulado
- **Leads & Supports:**
  - `Critical Rate` (7 retratos)

### Crítico garantizado

`critico_garantizado` · Guaranteed critical rate · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Críticos sin la reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Críticos sin la reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `GUARANTEED CRITICAL RATE ↑` (209 retratos)
  - `Precision` (15 retratos)
- **Leads & Supports:**
  - `Guaranteed Critical Rate` (10 retratos)

### Daño crítico

`dano_critico` · Critical damage · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Multiplica el golpe crítico. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Multiplica el golpe crítico. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `CRITICAL DAMAGE ↑` (346 retratos)
  - `DOUBLE CRITICAL` (47 retratos)
  - `Precision` (15 retratos)
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of All Basic Attacks, Critical Damage each #% of pure damage accumulated` (1 retrato) — varía: crece con el daño puro acumulado
  - `STAT ↑ PROPORTIONAL TO TOTAL DMG`, con `#% Increase of All Basic Attacks, Critical Rate, Critical Damage each #% of pure damage accumulated` (1 retrato) — varía: crece con el daño puro acumulado
- **Leads & Supports:**
  - `Critical Damage` (10 retratos)

### Ignorar defensa

`ignorar_defensa` · Ignore defense · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Sube el daño. La guía no sabe bien cómo funciona, pero recomienda llevarla al tope y la pone primera en las prioridades del equipo 4. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Sube el daño. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `IGNORE DEFENSE` (139 retratos)
- **Leads & Supports:**
  - `Ignore Defense` (1 retrato)

### Daño de golpe en cadena

`golpes_encadenados` · Chain hit damage · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** Rinde con las skills de golpes en cadena; la fuente no marca cuáles lo son.
- **Skills:**
  - `CHAIN HIT DMG DEALT ↑` (239 retratos)
- **Leads & Supports:**
  - `Chain Hit Damage` (5 retratos)

### Ignora la reducción de daño del rival (no jefes)

`ignorar_reduccion` · Ignores the foe's damage reduction (not bosses) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Contra enemigos comunes, no contra jefes. [Probable]
- **PvP:** Contra rivales que se protegen con reducción de daño. [Probable]
- **Skills:**
  - `Excluding bosses, ignores enemy's damage decrease` (24 retratos)
- **Leads & Supports:**
  - `Ignore Non-Boss Damage Decrease` (3 retratos)

### Ignora los aumentos y reducciones entre facciones

`ignorar_faccion` · Ignores damage modifiers between factions · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Ignores Damage Increase effect between factions` (1 retrato)
- **Leads & Supports:**
  - `Ignores Damage Increase/Decrease Effect Between Self and Opposing Faction` (1 retrato)

### Acumula daño

`acumula_dano` · Damage accumulation · Se aplica a su lado · Le sirve: a él (es parte de su kit).

- **Nota:** Parte de su propio kit: carga una reserva de daño que otro efecto suyo convierte en ataque o en daño.
- **Skills:**
  - `ACCUMULATE PURE DMG DEALT` (332 retratos)
  - `ACCUMULATE PURE DMG` (78 retratos)
  - `Charge Rate Increase` (35 retratos)
  - `Accumulate All True Element Damage Dealt` (9 retratos)
  - `ACCUMULATE TRUE ENERGY DMG` (4 retratos)
  - `ACCUMULATE ENERGY DMG` (2 retratos)

### Efecto de los debuffs

`efecto_debuffs` · Debuff effect · Se aplica a su lado · Le sirve: a quien aplica debuffs.

- **Skills:**
  - `DEBUFF EFFECT ↑` (34 retratos)
- **Leads & Supports:**
  - `All Debuffs Effect` (12 retratos)

### Efecto de los buffs

`efecto_buffs` · Buff effect · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `BUFF EFFECT INCREASE` (33 retratos)
  - `BUFF EFFECT ↑` (20 retratos)

### Daño de perforación

`dano_perforacion` · Pierce damage · Se aplica a su lado · Le sirve: a quien tiene Perforación.

- **Nota:** Sube el daño adicional que hace al perforar.
- **Skills:**
  - `ADDITIONAL PIERCE DAMAGE INCREASE` (36 retratos)
- **Leads & Supports:**
  - `Additional Pierce Damage` (1 retrato)

## Elemento

Sube el daño de un elemento.

- **PvE:** Solo le sirve a quien tiene ese elemento en sus skills. Los buffs del mismo elemento se suman entre sí, así que rinden menos que un buff de daño, que multiplica. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Igual que en PvE. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))

### Daño de fuego

`dano_fuego` · Fire damage · Se aplica a su lado · Le sirve: a quien hace daño de fuego.

- **Skills:**
  - `FLAME DAMAGE ↑` (43 retratos)
- **Leads & Supports:**
  - `Fire Damage` (18 retratos)
  - `Fire Damage by % Fire Resist` (2 retratos) — varía: según su resistencia al fuego

### Daño de frío

`dano_frio` · Cold damage · Se aplica a su lado · Le sirve: a quien hace daño de frío.

- **Skills:**
  - `COLD DAMAGE ↑` (14 retratos)
- **Leads & Supports:**
  - `Cold Damage` (1 retrato)

### Daño de rayo

`dano_rayo` · Lightning damage · Se aplica a su lado · Le sirve: a quien hace daño de rayo.

- **Skills:**
  - `LIGHTNING DAMAGE ↑` (43 retratos)
- **Leads & Supports:**
  - `Lightning Damage` (11 retratos)

### Daño de veneno

`dano_veneno` · Poison damage · Se aplica a su lado · Le sirve: a quien hace daño de veneno.

- **Skills:**
  - `POISON DAMAGE ↑` (8 retratos)
- **Leads & Supports:**
  - `Poison Damage` (1 retrato)

### Daño mental

`dano_mente` · Mind damage · Se aplica a su lado · Le sirve: a quien hace daño mental.

- **Skills:**
  - `MIND DAMAGE ↑` (31 retratos)
- **Leads & Supports:**
  - `Mind Damage` (4 retratos)

### Daño de todos los elementos

`dano_elementos` · All element damage · Se aplica a su lado · Le sirve: a quien hace daño de algún elemento.

- **Skills:**
  - `ALL ELEMENT DAMAGE INCREASE` (14 retratos)
  - `ALL ELEMENT DAMAGE ↑` (13 retratos)
- **Leads & Supports:**
  - `All Element Damage` (9 retratos)

### Daño de su elemento

`dano_elemento_propio` · Damage of its element · Se aplica a su lado · Le sirve: a él (es parte de su kit).

- **Nota:** La fuente publica el elemento como un código; es el de sus propias skills.
- **Skills:**
  - `Element Damage ↑ Proportional to Accumulated Element Damage` (9 retratos) — varía: crece con el daño elemental acumulado
  - `ELEMENT CONVERSION` (7 retratos) — varía: según su resistencia a ese elemento

## Precisión

Que el golpe entre o atraviese protecciones.

- **PvE:** Sirve contra rivales que esquivan o se protegen. [Probable]
- **PvP:** Sirve contra rivales que esquivan o se protegen. [Probable]

### Ignorar evasión

`ignorar_evasion` · Ignore dodge · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Si el rival iba a esquivar, el golpe entra igual con esa probabilidad. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Si el rival iba a esquivar, el golpe entra igual con esa probabilidad. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `IGNORE DODGE` (631 retratos)
- **Leads & Supports:**
  - `Ignore Dodge` (92 retratos)

### Perforación

`perforar` · Pierce · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** Atraviesa, con una probabilidad, la invencibilidad, la inmunidad a todo daño, los escudos, las barreras o la superarmadura del rival (cada skill dice cuáles).
- **Skills:**
  - `PIERCE` (663 retratos)

### Apunta a quien no se deja apuntar

`apuntado` · Guaranteed targeting · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** Le pega a los rivales con el efecto «Ignore Targeting».
- **Skills:**
  - `Guaranteed Targeting` (13 retratos)

### Atraviesa una resistencia elemental

`penetrar_resistencia` · Goes through an elemental resist · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `TYPE PENETRATION` (13 retratos)

### Rompe la guardia

`romper_guardia` · Guard break · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `ACTIVATES GUARD BREAK` (6 retratos) — dura unos ataques

## Daño continuo

Daño que sigue unos segundos después del golpe.

- **PvE:** La guía lo llama inútil como daño. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** La guía lo llama inútil como daño. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))

### Quemadura

`continuo_quemadura` · Burn · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Poco daño, pero corta el ataque especial de los jefes de Alliance Battle Extreme. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), [THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **Skills:**
  - `BURN` (412 retratos)

### Sangrado

`continuo_sangrado` · Bleed · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Nota:** Además le saca la Elasticidad al rival.
- **Skills:**
  - `BLEED` (335 retratos)

### Electrochoque

`continuo_electrochoque` · Shock · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Poco daño, pero corta el ataque especial de los jefes de Alliance Battle Legend. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), [THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **Skills:**
  - `SHOCK` (162 retratos)

### Veneno

`continuo_veneno` · Poison · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `POISON` (23 retratos)

### Helada

`continuo_helada` · Chill · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `CHILL` (40 retratos)

### Encanto

`continuo_encanto` · Charm · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Nota:** Además cura a quien lo aplica con parte de ese daño; la recuperación no sube esa curación (guía, parte 3).
- **Skills:**
  - `CHARM` (24 retratos)

### Maldición

`continuo_maldicion` · Curse · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Nota:** Además cura a quien la aplica con parte de ese daño.
- **Skills:**
  - `CURSE` (3 retratos)

### Pérdida

`continuo_perdida` · Loss · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Loss` (5 retratos)

### Plasmoide de energía

`continuo_plasmoide` · Energy Plasmoid · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Energy Plasmoid` (4 retratos)

## Control

Inmoviliza o domina al rival.

- **PvE:** Frena a los enemigos. [Probable]
- **PvP:** Frena al rival. [Probable]

### Aturdir

`aturdir` · Stun · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `STUN` (762 retratos)

### Parálisis

`paralizar` · Paralyze · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Frena a los enemigos y corta el ataque especial de los jefes de Alliance Battle Extreme. [Comprobado] ([THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **Skills:**
  - `Paralysis (Ignores immunity)` (474 retratos)
  - `PARALYZE` (85 retratos)

### Silencio

`silenciar` · Silence · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Frena a los enemigos y corta el ataque especial de los jefes de Alliance Battle Extreme. [Comprobado] ([THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **Skills:**
  - `SILENCE` (345 retratos)

### Atrapar

`atrapar` · Snare · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Frena a los enemigos y corta el ataque especial de los jefes de Alliance Battle Legend. [Comprobado] ([THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **Skills:**
  - `SNARE` (310 retratos)

### Fractura

`fracturar` · Fracture · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Corta el ataque especial de los jefes de Alliance Battle Legend. [Comprobado] ([THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **PvP:** Si es un control, frena al rival. [Conjetura]
- **Nota:** Ninguna fuente dice qué hace; se aplica al rival. Que sea un control es una suposición.
- **Skills:**
  - `Fracture` (218 retratos)

### Congelar

`congelar` · Freeze · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `FREEZE` (61 retratos)

### Telaraña

`telarana` · Web · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `WEB` (38 retratos)
  - `Web (ignores immunity)` (14 retratos)

### Miedo

`miedo` · Fear · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `FEAR` (110 retratos)

### Control mental

`control_mental` · Mind control · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Mind Control` (65 retratos)

### Detención del tiempo

`detener_tiempo` · Time freezing · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `TIME FREEZING` (26 retratos)

### Sepultar

`sepultar` · Entomb · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `ENTOMB` (5 retratos)

### Ámbar

`ambar` · Amberize · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Amberize` (2 retratos)

### Pánico

`panico` · Panic · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Panic` (23 retratos)

### Seducir

`seducir` · Entice · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Entice` (9 retratos)

### Provocar

`provocar` · Provoke · Se aplica a su lado o al rival, según la etiqueta · Le sirve: a cualquiera del equipo.

- **Nota:** Obliga a los rivales a atacarlo a él: protege al resto del equipo.
- **Skills:**
  - `Mockery` (4 retratos)
  - `PROVOKE` (4 retratos) — al rival

## Debilitar

Le baja algo al rival o le quita buffs.

- **PvE:** Contra ese rival, el equipo pega más o recibe menos. [Probable]
- **PvP:** Contra ese rival, el equipo pega más o recibe menos. [Probable]

### Baja las defensas del rival

`defensas_rival` · Lowers the foe's defenses · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Decreases all Basic Defenses (Can stack, ignores immunity)` (544 retratos)
  - `ALL BASIC DEFENSES DECREASE` (58 retratos)
  - `DECREASES ALL BASIC DEFENSES (CAN STACK)` (58 retratos)
  - `PHYSICAL DEFENSE ↓` (17 retratos)
  - `MINIATURIZE`, con `Decreases character size by #%, all Basic Attacks by #%^, all Basic Defenses by #%.` (15 retratos) — Nota: Achica al personaje (y le sube ataques y defensas) o al rival (y le baja los suyos): lo distingue el texto. Que el segundo vaya al rival lo dicen el texto y la activación «When attacking an enemy with MINIATURIZE effect applied».
  - `All Basic Defenses Decrease` (13 retratos)
  - `VULNERABILITY` (4 retratos)
  - `ENERGY DEFENSE ↓` (3 retratos)

### Baja los ataques del rival

`ataques_rival` · Lowers the foe's attacks · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Ese rival pega menos. [Probable]
- **PvP:** Ese rival pega menos. [Probable]
- **Skills:**
  - `ALL BASIC ATTACKS DECREASE` (26 retratos)
  - `MINIATURIZE`, con `Decreases character size by #%, all Basic Attacks by #%^, all Basic Defenses by #%.` (15 retratos) — Nota: Achica al personaje (y le sube ataques y defensas) o al rival (y le baja los suyos): lo distingue el texto. Que el segundo vaya al rival lo dicen el texto y la activación «When attacking an enemy with MINIATURIZE effect applied».
  - `DECREASES ALL BASIC ATTACKS (CAN STACK)` (11 retratos)
  - `VULNERABILITY` (4 retratos)

### Baja la velocidad del rival

`velocidad_rival` · Lowers the foe's speed · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `ALL SPEED ↓` (115 retratos)
  - `MOVEMENT SPEED ↓` (19 retratos)
  - `VULNERABILITY` (4 retratos)
  - `ALL SPEED ↓ (can stack)` (2 retratos)

### El rival recibe más daño

`vulnerable_rival` · The foe takes more damage · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Contra ese rival, el equipo pega más. [Probable]
- **PvP:** Contra ese rival, el equipo pega más. [Probable]
- **Skills:**
  - `Mind Control` (65 retratos)
  - `Panic` (23 retratos)

### Baja la resistencia al fuego del rival

`resistencia_rival_fuego` · Lowers the foe's fire resist · Se aplica al rival · Le sirve: a quien hace daño de fuego.

- **Skills:**
  - `Flame Resist Decrease (Can stack, ignores immunity)` (30 retratos)
  - `FLAME RESIST ↓` (9 retratos)

### Baja la resistencia al frío del rival

`resistencia_rival_frio` · Lowers the foe's cold resist · Se aplica al rival · Le sirve: a quien hace daño de frío.

- **Skills:**
  - `Cold Resist Decrease (Can stack, ignores immunity)` (9 retratos)

### Baja la resistencia al rayo del rival

`resistencia_rival_rayo` · Lowers the foe's lightning resist · Se aplica al rival · Le sirve: a quien hace daño de rayo.

- **Skills:**
  - `Lightning Resist Decrease (Can stack, ignores immunity)` (23 retratos)
  - `LIGHTNING RESIST ↓` (16 retratos)

### Baja la resistencia al veneno del rival

`resistencia_rival_veneno` · Lowers the foe's poison resist · Se aplica al rival · Le sirve: a quien hace daño de veneno.

- **Skills:**
  - `Poison Resist Decrease (Can stack, ignores immunity)` (1 retrato)

### Baja la resistencia mental del rival

`resistencia_rival_mente` · Lowers the foe's mind resist · Se aplica al rival · Le sirve: a quien hace daño mental.

- **Skills:**
  - `Mind Resist Decrease (Can stack, ignores immunity)` (34 retratos)
  - `MIND RESIST ↓` (15 retratos)
  - `MIND BLAST` (9 retratos)

### Baja todas las resistencias del rival

`resistencias_rival` · Lowers all the foe's resists · Se aplica al rival · Le sirve: a quien hace daño de algún elemento.

- **Skills:**
  - `ALL RESISTANCE ↓` (18 retratos)
  - `All Resist Decrease (Can stack, ignores immunity)` (2 retratos)

### Le quita los buffs al rival

`quitar_buffs` · Strips the foe's buffs · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Incapacitation` (303 retratos)
  - `CANCEL` (103 retratos)
  - `REMOVE` (21 retratos) — Nota: La fuente publica qué quita como un código; la wiki (Spider-Man, «Hero's Responsibility») dice que le quita los buffs activos al rival.
  - `Loss` (5 retratos)
  - `Selective Removal` (1 retrato) — Nota: Le quita al rival un efecto que la fuente publica como código.

### Baja el efecto de los buffs del rival

`buffs_rival` · Lowers the effect of the foe's buffs · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `BUFF EFFECT ↓` (9 retratos)

### Baja el efecto de los debuffs del rival

`debuffs_rival` · Lowers the effect of the foe's debuffs · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Nota:** La fuente publica el efecto afectado como un código.
- **Skills:**
  - `DEBUFF EFFECT ↓` (6 retratos)

### Quita las zonas del rival

`quitar_zonas` · Removes the foe's zones · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `AREA DISABLED` (15 retratos)

### Alarga la recarga del rival

`recarga_rival` · Lengthens the foe's cooldown · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `SKILL COOLDOWN ↑` (1 retrato)

### Ceguera

`cegar` · Blind · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Nota:** El rival falla golpes con esa probabilidad.
- **Skills:**
  - `BLIND` (89 retratos)
  - `Darkness` (5 retratos)

## Defensa

Sube las defensas.

- **PvE:** La guía la da por casi inútil. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Tampoco es lo que pesa en PvP: la guía pone al frente la reducción de daño, la vida y la evasión. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))

### Todas las defensas

`defensas_todas` · All defenses · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `FRENZY` (491 retratos)
  - `SUPER ARMOR` (329 retratos)
  - `Increases all Basic Attacks and Defenses` (220 retratos)
  - `Increases all basic stats` (220 retratos)
  - `ALL BASIC DEFENSES INCREASE` (91 retratos)
  - `ENLARGE`, con `Increases character size by #%, all Basic Attacks by #%^, all Basic Defenses by #%.` (35 retratos)
  - `Increases all Attacks, Defense and Speed relative to HP` (6 retratos) — varía: según su vida
  - `MINIATURIZE`, con `Decreases character size by #%, increases all Basic Attacks by #%^, all Basic Defenses by #%.` (6 retratos) — Nota: Achica al personaje (y le sube ataques y defensas) o al rival (y le baja los suyos): lo distingue el texto. Que el segundo vaya al rival lo dicen el texto y la activación «When attacking an enemy with MINIATURIZE effect applied».
  - `Condensed Power` (1 retrato) — varía: se acumula
- **Leads & Supports:**
  - `All Basic Defenses` (49 retratos)
  - `Super Armor, All Basic Defenses` (9 retratos)

### Defensa física

`defensa_fisica` · Physical defense · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `PHYSICAL DEFENSE ↑` (37 retratos)

### Defensa de energía

`defensa_energia` · Energy defense · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `ENERGY DEFENSE ↑` (14 retratos)
- **Leads & Supports:**
  - `Energy Defense` (5 retratos)

### Superarmadura

`superarmadura` · Super armor · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Los golpes no lo interrumpen. [Probable]
- **PvP:** Los golpes no lo interrumpen. [Probable]
- **Skills:**
  - `SUPER ARMOR` (329 retratos)
- **Leads & Supports:**
  - `Super Armor, All Basic Defenses` (9 retratos)

## Vida

Vida, curación, escudos y revivir.

- **PvE:** Lo mantiene vivo. [Probable]
- **PvP:** La guía pone la vida entre lo que pesa en PvP. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))

### Vida

`vida_max` · HP · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Lo mantiene vivo; sube el daño solo de los pocos que escalan con la vida. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Importante en PvP. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), [THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))
- **Skills:**
  - `MAX HP ↑` (167 retratos)
  - `Demonization (Darkchylde)` (1 retrato)
- **Leads & Supports:**
  - `HP` (62 retratos)

### Curación

`curacion` · Healing · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `HP RECOVERY` (553 retratos)
  - `Misdirection` (9 retratos) — varía: crece cada vez que recibe un golpe
  - `Accumulate Damage HP Recovery` (7 retratos)
  - `FORTITUDE` (6 retratos)
  - `Recovers HP per summoned character.` (2 retratos)
- **Leads & Supports:**
  - `Heal` (17 retratos)
  - `Immortality + Heal` (1 retrato)

### Recuperación

`recuperacion` · Recovery rate · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Multiplica sus curaciones. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Multiplica sus curaciones. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `RECOVERY RATE ↑` (24 retratos)
- **Leads & Supports:**
  - `Recovery Rate` (9 retratos)

### Robo de vida

`robo_vida` · HP steal · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `HP Steal` (12 retratos)
  - `HP STEAL` (7 retratos)

### Escudo

`escudo` · Shield · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Recharge Shield` (14 retratos)
  - `SHIELD` (14 retratos)
  - `ENERGY SHIELD` (12 retratos)
  - `SUPER HIT SHIELD` (12 retratos)
  - `PHYSICAL SHIELD` (4 retratos)
- **Leads & Supports:**
  - `Max HP Shield` (2 retratos)

### Barrera

`barrera` · Barrier · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** Bloquea una cantidad de golpes.
- **Skills:**
  - `BARRIER` (251 retratos)
- **Leads & Supports:**
  - `Barrier` (2 retratos)

### Revivir

`revivir` · Revive · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvP:** Muy importante en PvP (la guía lo dice del de Sersi). [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `REVIVE` (38 retratos)
  - `Appearance` (3 retratos)
- **Leads & Supports:**
  - `Revive with % HP` (2 retratos)

### No muere por un tiempo

`inmortalidad` · Cannot die for a while · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `FORTITUDE` (6 retratos)
  - `Death Throes` (3 retratos)
- **Leads & Supports:**
  - `Immortality + Death` (1 retrato)
  - `Immortality + Heal` (1 retrato)

## Reducción de daño

Recibe menos daño o lo evita.

- **PvE:** Lo mantiene vivo. [Probable]
- **PvP:** Clave: la guía pone la reducción de daño y la evasión al frente del PvP. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))

### Invencible

`invencible` · Invincible · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvP:** Valiosa en PvP: la guía la sugiere en vez del proc de daño en el equipo de PvP. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `INVINCIBLE` (817 retratos)
  - `Body Enhancement` (1 retrato) — varía: el daño crece con cada golpe que ignora

### Inmune a todo daño (probabilidad)

`inmune_todo` · All damage immunity (chance) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `ALL DAMAGE IMMUNE` (555 retratos)
  - `Parry` (2 retratos)

### Menos daño recibido

`dano_recibido` · Less damage taken · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Decreases all basic damage` (378 retratos)
  - `Body Enhancement` (1 retrato) — varía: el daño crece con cada golpe que ignora
- **Leads & Supports:**
  - `Basic Damage Received` (15 retratos)

### Menos daño recibido de ciertos rivales

`dano_recibido_de` · Less damage taken from some foes · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Solo contra esos rivales. [Probable]
- **PvP:** Solo contra esos rivales. [Probable]
- **Skills:**
  - `Decreases basic damage based on character's faction` (55 retratos) — contra una facción (cada skill dice cuál)
  - `Bravery` (23 retratos) — según la vida máxima del rival frente a la suya
  - `Valor` (10 retratos) — según la vida máxima del rival frente a la suya
  - `Decreases basic damage based on character's type` (6 retratos) — contra un tipo (cada skill dice cuál)
  - `Decreases basic damage based on character's race` (3 retratos) — contra una raza (cada skill dice cuál)
  - `DECREASES BASIC DAMAGE WHEN ATTACKED BY CHARACTERS WITH ABILITIES` (2 retratos) — contra quien tiene una habilidad (cada skill dice cuál)
  - `Luck` (1 retrato) — contra todos menos los jefes
- **Leads & Supports:**
  - `Basic Damage Received from Villains` (34 retratos) — contra una facción: Supervillano; Nota: Leads & Supports publica esta reducción a veces con signo positivo; la skill dice siempre que reduce.
  - `Basic Damage Received from Heroes` (7 retratos) — contra una facción: Superhéroe
  - `Basic Damage Received from Universals` (3 retratos) — contra un tipo: Universal

### Menos daño físico recibido

`dano_fisico_recibido` · Less physical damage taken · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `PHYSICAL DAMAGE ↓` (20 retratos)
  - `Elasticity` (5 retratos)

### Menos daño de energía recibido

`dano_energia_recibido` · Less energy damage taken · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `ENERGY DAMAGE ↓` (19 retratos)

### Inmune al daño físico (probabilidad)

`inmune_fisico` · Physical damage immunity (chance) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `PHYSICAL IMMUNITY` (27 retratos)
- **Leads & Supports:**
  - `Physical Immunity Chance` (1 retrato)

### Inmune al daño de energía (probabilidad)

`inmune_energia` · Energy damage immunity (chance) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Absorb` (4 retratos) — varía: el ataque crece con cada absorción
  - `ENERGY IMMUNITY` (3 retratos)

### Inmune a un elemento (probabilidad)

`inmune_elemento` · Element immunity (chance) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `FLAME IMMUNITY` (28 retratos)
  - `MIND IMMUNITY` (16 retratos)
  - `COLD IMMUNITY` (9 retratos)
  - `LIGHTNING IMMUNITY` (5 retratos)
  - `POISON IMMUNITY` (4 retratos)
- **Leads & Supports:**
  - `Lightning Immunity Chance` (2 retratos)
  - `Fire Immunity Chance` (1 retrato)
  - `Mind Immunity Chance` (1 retrato)

### Ignora el daño que pase de un % de su vida

`tope_golpe` · Ignores damage above a % of its HP · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Lo protege de los golpes muy grandes. [Probable]
- **PvP:** Lo protege de los golpes muy grandes. [Probable]
- **Skills:**
  - `Stubbornness` (31 retratos)

### Inmune al mayor daño recibido (probabilidad)

`inmune_mayor_dano` · Immune to the greatest damage taken (chance) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** La fuente no aclara si es el golpe más fuerte o el tipo de daño que más recibe.
- **Skills:**
  - `Adaptation` (3 retratos)

### Menos daño de golpes en cadena

`encadenados_recibidos` · Less chain hit damage taken · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `CHAIN HIT DMG RECEIVED ↓` (23 retratos)
- **Leads & Supports:**
  - `Chain Hit Damage Received` (10 retratos)

### Menos daño de perforación recibido

`perforacion_recibida` · Less pierce damage taken · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvP:** Bueno en PvP (la guía lo dice de los artefactos con este efecto). [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `Additional Pierce Damage Decrease` (5 retratos)

### Menos daño reflejado recibido

`reflejo_recibido` · Less reflected damage taken · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** Le sirve a quien le pega a rivales que reflejan.
- **Skills:**
  - `Counter Reflect`, con `Decreases damage received from reflected effects by #%.Effect: Reflect All Attacks` (17 retratos) — Nota: El texto dice de qué reflejo protege; en un caso la fuente lo publica como código.
  - `Counter Reflect`, con `Decreases damage received from reflected effects by #%.Effect: #` (7 retratos) — Nota: El texto dice de qué reflejo protege; en un caso la fuente lo publica como código.
- **Leads & Supports:**
  - `All Reflect Damage Received` (5 retratos)

### Menos daño reflejado de un golpe físico

`reflejo_fisico_recibido` · Less reflected physical damage taken · Se aplica a su lado · Le sirve: a quien hace daño físico.

- **Skills:**
  - `Counter Reflect`, con `Decreases damage received from reflected effects by #%.Effect: Physical Reflect` (12 retratos) — Nota: El texto dice de qué reflejo protege; en un caso la fuente lo publica como código.
- **Leads & Supports:**
  - `Physical Reflect Damage Received` (9 retratos) — Nota: Leads & Supports publica esta reducción a veces con signo positivo; la skill dice siempre que reduce.

### Evasión

`evasion` · Dodge · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Esquiva golpes; se reduce según el nivel del rival. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Pesa en PvP; se reduce según el nivel del rival. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), [THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))
- **Skills:**
  - `DODGE ↑` (154 retratos)
  - `INVISIBILITY` (36 retratos)
  - `Camouflage` (8 retratos)
- **Leads & Supports:**
  - `Dodge` (6 retratos)

### Evasión garantizada

`evasion_garantizada` · Guaranteed dodge · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Esquiva sin la reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Esquiva sin la reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), [THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))
- **Skills:**
  - `GUARANTEED DODGE RATE ↑` (273 retratos)

### Invisibilidad

`invisibilidad` · Invisibility · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `INVISIBILITY` (36 retratos)
  - `Camouflage` (8 retratos)

### Esquiva una cantidad de golpes

`esquivar_golpes` · Dodges a number of hits · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** Según la skill, incluso los que ignoran la evasión.
- **Skills:**
  - `Evasion Reload` (26 retratos)
  - `Dodges certain attacks.` (2 retratos)

### Resistencias elementales

`resistencias` · Elemental resists · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Poco importante. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Poco importante. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `MIND RESIST ↑` (32 retratos)
  - `ALL RESISTANCE ↑` (26 retratos)
  - `FLAME RESIST ↑` (18 retratos)
  - `LIGHTNING RESIST ↑` (14 retratos)
  - `COLD RESIST ↑` (3 retratos)
  - `POISON RESIST ↑` (1 retrato)
- **Leads & Supports:**
  - `All Resistances` (5 retratos)
  - `Mind Resist` (5 retratos)
  - `Fire Resist` (2 retratos)

## Contra debuffs

Le saca los debuffs o lo hace inmune a ellos.

- **PvE:** Sirve donde el rival aplica debuffs. [Probable]
- **PvP:** Clave: la guía dice que la inmunidad a debuffs es crucial en PvP. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))

### Le saca todos los debuffs

`quita_debuffs` · Removes all debuffs · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvP:** Muy útil en Timeline (la guía lo dice del soporte de Wasp). [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 1](https://thanosvibs.money/beginners/1))
- **Nota:** La API de skills a veces publica «Give Power» sin decir qué otorga; Leads & Supports trae que es esto (docs/AUDITORIA.md, sección 7).
- **Skills:**
  - `Removes all Debuffs. ` (409 retratos)
  - `Parry` (2 retratos)
- **Leads & Supports:**
  - `Remove All Debuffs` (81 retratos)

### Inmunidad a debuffs

`inmune_debuffs` · Debuff immunity · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvP:** Crucial en PvP: si el principal no la tiene, se lleva un líder o un soporte que la dé. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))
- **Skills:**
  - `IMMUNE` (13 retratos)
- **Leads & Supports:**
  - `Debuff Immunity` (3 retratos)

### Inmune a un debuff

`inmune_efecto` · Immune to a debuff · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `RESIST` (94 retratos)
- **Leads & Supports:**
  - `Burn Immunity` (4 retratos)
  - `Incapacitation Immunity` (2 retratos)
  - `Fear Immunity` (1 retrato)
  - `Stun Immunity` (1 retrato)

### Inmune a que le rompan la guardia

`inmune_romper_guardia` · Guard break immunity · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `GUARD BREAK IMMUNE` (38 retratos)
  - `FORTITUDE` (6 retratos)
- **Leads & Supports:**
  - `Guard Break Immunity` (1 retrato)

### Debuffs más cortos

`debuffs_cortos` · Shorter debuffs · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Poco importante. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Poco importante. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `CROWD CONTROL TIME ↓` (75 retratos)
- **Leads & Supports:**
  - `Debuff Duration` (10 retratos)

## Velocidad y recarga

Velocidades, recarga de skills y cargas.

- **PvE:** Depende del stat. [Probable]
- **PvP:** Depende del stat. [Probable]

### Todas las velocidades

`velocidades` · All speeds · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Incluye la velocidad de ataque, que importa; la de movimiento no. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Incluye la velocidad de ataque, que importa; la de movimiento no. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `FRENZY` (491 retratos)
  - `Increases all basic stats` (220 retratos)
  - `ALL SPEED ↑` (148 retratos)
  - `Increases all Attacks, Defense and Speed relative to HP` (6 retratos) — varía: según su vida
  - `ENLARGE`, con `Increases character size by #% and all Speeds, all Basic Attacks by #%.` (4 retratos)
  - `ALL SPEED ↑(Can Stack)` (1 retrato)
- **Leads & Supports:**
  - `All Speeds` (25 retratos)

### Velocidad de ataque

`velocidad_ataque` · Attack speed · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Importante: acelera las animaciones de las skills. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Importante: acelera las animaciones de las skills. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `ATTACK SPEED ↑` (12 retratos)

### Velocidad de movimiento

`velocidad_movimiento` · Movement speed · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** No importa. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** No importa. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `MOVEMENT SPEED ↑` (4 retratos)

### Recarga de skills

`enfriamiento` · Skill cooldown · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Crucial: los personajes están pensados con el tope de 50%. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **PvP:** Crucial: los personajes están pensados con el tope de 50%. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Skills:**
  - `COOLDOWN DURATION ↓` (61 retratos)
- **Leads & Supports:**
  - `Skill Cooldown` (1 retrato)

### Reinicia o fija la recarga de una skill

`reinicia_recarga` · Resets or sets a skill's cooldown · Se aplica a su lado · Le sirve: a él (es parte de su kit).

- **Skills:**
  - `COOLDOWN RESET` (17 retratos)
  - `SET SKILL CD` (13 retratos)

### Carga de la definitiva

`carga_definitiva` · Ultimate gauge · Se aplica a su lado · Le sirve: a quien tiene la definitiva de Tier-3 (la que se carga con la barra).

- **Skills:**
  - `Ultimate Skill Gauge Recharge` (13 retratos)
  - `Ultimate Skill Gauge Recovery` (1 retrato)

### Striker más seguido

`striker` · More frequent striker · Se aplica a su lado · Le sirve: a quien tiene Striker (Tier-4).

- **Skills:**
  - `STRIKER COOLDOWN ↓` (2 retratos)
  - `STRIKER RATE ↑` (2 retratos)

### Efectos más largos

`duracion_efectos` · Longer effects · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Nota:** La fuente publica el efecto que dura más como un código.
- **Skills:**
  - `DURATION INCREASE` (12 retratos)
- **Leads & Supports:**
  - `1s Pierce Duration Increase` (1 retrato)
  - `1s Snare Duration Increase` (1 retrato)

## Reflejo

Le devuelve al que pega parte del daño recibido.

- **PvE:** Castiga al que le pega. [Probable]
- **PvP:** Castiga al que le pega. [Probable]

### Refleja daño

`reflejo` · Reflects damage · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `PHYSICAL REFLECT` (21 retratos)
  - `REFLECT ALL ATTACKS ` (19 retratos)
  - `ENERGY REFLECT` (16 retratos)
  - `Always Reflect All Damage` (5 retratos)
  - `MIND REFLECT` (2 retratos)

## Invocación

Pone unidades a pelear.

- **PvE:** Suma unidades que pegan o distraen. [Conjetura]
- **PvP:** Suma unidades que pegan o distraen. [Conjetura]

### Invoca

`invocar` · Summons · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `SUMMON` (84 retratos)
  - `Target Duplication` (5 retratos)
- **Leads & Supports:**
  - `Summon` (1 retrato)

### Mejora sus invocaciones

`invocaciones_stats` · Boosts its summons · Se aplica a su lado · Le sirve: a quien invoca.

- **Skills:**
  - `SUMMONED CHARACTER STATS ↑` (41 retratos)

## Otros

Mecánicas propias de un personaje.

- **PvE:** Depende del personaje. [Probable]
- **PvP:** Depende del personaje. [Probable]

### Otorga los efectos que siguen

`otorga` · Grants the following effects · Se aplica a su lado · Le sirve: a él (es parte de su kit).

- **Nota:** Envoltorio: lo que da son los efectos que vienen después. A veces la API de skills no los trae y Leads & Supports sí.
- **Skills:**
  - `Give Power` (224 retratos)

### Mecánica propia

`mecanica_propia` · Own mechanic · Se aplica a su lado · Le sirve: a él (es parte de su kit).

- **Skills:**
  - `ADDS EFFECT ON USE` (3 retratos)
  - `ACCUMULATE MOVEMENT RANGE` (1 retrato)
  - `EFFECT CHANGES BASED ON TARGET` (1 retrato)
  - `Reality Manipulation` (1 retrato)
  - `STAT ↑ PROPORTIONAL TO MOVEMENT DISTANCE` (1 retrato)

### Alcance

`alcance` · Range · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `RANGE ↑` (4 retratos)

### Tamaño

`tamano` · Size · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `ENLARGE`, con `Increases character size by #%, all Basic Attacks by #%^, all Basic Defenses by #%.` (35 retratos)
  - `MINIATURIZE`, con `Decreases character size by #%, increases all Basic Attacks by #%^, all Basic Defenses by #%.` (6 retratos) — Nota: Achica al personaje (y le sube ataques y defensas) o al rival (y le baja los suyos): lo distingue el texto. Que el segundo vaya al rival lo dicen el texto y la activación «When attacking an enemy with MINIATURIZE effect applied».
  - `ENLARGE`, con `Increases character size by #% and all Speeds, all Basic Attacks by #%.` (4 retratos)

## Fuentes

- [THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl)
- [THANO$VIB$ Beginner's Guide, parte 1](https://thanosvibs.money/beginners/1)
- [THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3)
- [THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4)
