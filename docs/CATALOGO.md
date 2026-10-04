# Catálogo de efectos

Generado por `scripts/catalogo.py` el 2026-10-04, sobre los datos del juego 12.2.5, desde `scripts/contenido/catalogo.json` (contenido curado: se edita ahí, no acá).

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

16 grupos, 126 efectos, 228 etiquetas de skills y 72 stats de Leads & Supports. Todo lo que traen los datos está clasificado.

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

- **Nota:** La guía llama «Skill Damage» a la parte del golpe que sale del ataque y «Additional Damage» al daño fijo extra, el único que sube con el nivel de la skill (NamuWiki dice lo mismo del 추가 피해량, «daño adicional»); no aclara si «Bonus Damage» es ese daño fijo. Falta ver si el texto en coreano de la pasiva de Tier-2 lo llama 추가 피해량. En inglés, «Bonus damage» nombra también el daño continuo de la maldición y de la pérdida.
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
- **PvP:** Sube el daño solo contra esos rivales. Contra una facción, es lo que suele aportar el tercero del equipo en Timeline, el «buffer»: según NamuWiki, un personaje con aumentos o bajas de daño entre facciones en su pasiva o su uniforme, como Colossus. [Comprobado] ([NamuWiki — MARVEL 퓨처파이트/타임라인 배틀 (en coreano)](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%20%EB%B0%B0%ED%8B%80))
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

- **PvE:** Suma un valor fijo a la probabilidad de crítico, sin la reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** Suma un valor fijo a la probabilidad de crítico, sin la reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **Nota:** El glosario en inglés dice que hace crítico «a una tasa fija» (at a set rate); el coreano, que le suma un valor fijo a la probabilidad de crítico.
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

- **PvP:** Anula los aumentos y las bajas de daño entre su facción y la del rival. En Timeline, eso es lo que suele aportar el «buffer» del equipo (Colossus, según NamuWiki), así que lo neutraliza. [Probable] ([NamuWiki — MARVEL 퓨처파이트/타임라인 배틀 (en coreano)](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%20%EB%B0%B0%ED%8B%80))
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

### Daño perforante adicional

`dano_perforacion` · Additional Pierce Damage · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Daño extra que ignora del todo la defensa; sale del daño de la skill. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **PvP:** Daño extra que ignora del todo la defensa; sale del daño de la skill. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **Nota:** No es la Perforación (atravesar invencibilidad, escudos o barreras): el glosario del juego no lo ata a ella, y las colecciones de equipo se lo dan a todos sus integrantes. Por eso le sirve a cualquiera.
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

### Rotura de guardia (cancela la skill del rival)

`romper_guardia` · Guard Break (cancels the foe's skill) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Cancela la skill que está usando el rival y abre un contraataque. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **PvP:** Cancela la skill que está usando el rival y abre un contraataque. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
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

### Daño mental del encanto

`continuo_encanto` · Charm mind damage · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Nota:** Además cura a quien lo aplica con parte de ese daño; la recuperación no sube esa curación (guía, parte 3).
- **Skills:**
  - `CHARM` (24 retratos)

### Maldición

`continuo_maldicion` · Curse · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Nota:** Además cura a quien la aplica con parte de ese daño.
- **Skills:**
  - `CURSE` (3 retratos)

### Daño de la pérdida

`continuo_perdida` · Loss damage · Se aplica al rival · Le sirve: a cualquiera del equipo.

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
  - `Paralysis (Ignores immunity)` (474 retratos) — Nota: La etiqueta dice que ignora la inmunidad. Según NamuWiki (World Boss Legend), los jefes de World Boss Legend ignoran incluso los controles que ignoran la inmunidad.
  - `PARALYZE` (85 retratos)

### Silencio

`silenciar` · Silence · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Frena a los enemigos y corta el ataque especial de los jefes de Alliance Battle Extreme. [Comprobado] ([THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **Skills:**
  - `SILENCE` (345 retratos)

### Atrapar

`atrapar` · Snare · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** No puede moverse, atacar ni usar skills por un rato. Corta el ataque especial de los jefes de Alliance Battle Legend. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), [THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **PvP:** No puede moverse, atacar ni usar skills por un rato. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **Skills:**
  - `SNARE` (310 retratos)

### Congelar

`congelar` · Freeze · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `FREEZE` (61 retratos)

### Telaraña

`telarana` · Web · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `WEB` (38 retratos)
  - `Web (ignores immunity)` (14 retratos) — Nota: La etiqueta dice que ignora la inmunidad. Según NamuWiki (World Boss Legend), los jefes de World Boss Legend ignoran incluso los controles que ignoran la inmunidad.

### Miedo

`miedo` · Fear · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Huye de quien se lo aplicó y no puede atacar ni usar skills. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **PvP:** Huye de quien se lo aplicó y no puede atacar ni usar skills. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **Skills:**
  - `FEAR` (110 retratos)

### Control mental

`control_mental` · Mind control · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Pasa a pelear del lado propio y recibe más daño. Sirve contra World Bosses y rivales a los que no se les aplican debuffs, pero no contra quien quita todos los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** Pasa a pelear del lado propio y recibe más daño. Sirve contra World Bosses y rivales a los que no se les aplican debuffs, pero no contra quien quita todos los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **Nota:** El glosario en inglés dice «enemies that don't have debuffs» (rivales sin debuffs encima); el coreano, rivales a los que no se les aplican debuffs: los inmunes.
- **Skills:**
  - `Mind Control` (65 retratos)

### Detención del tiempo

`detener_tiempo` · Time freezing · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** No puede moverse ni atacar por un rato. Atrapa también a los jefes grandes a los que no se les aplican debuffs, pero no a quien tiene un efecto que quita todos los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** No puede moverse ni atacar por un rato. Atrapa también a los jefes grandes a los que no se les aplican debuffs, pero no a quien tiene un efecto que quita todos los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **Nota:** El glosario en inglés dice que atrapa a «epic monsters that have no debuffs» (monstruos sin debuffs encima); el coreano, a los jefes grandes a los que no se les aplican debuffs: los inmunes.
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

- **PvE:** Le aplica miedo y recibe más daño. Se puede aplicar a World Bosses y a rivales que no reciben debuffs, pero no a quien quita todos los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **PvP:** Le aplica miedo y recibe más daño. Se puede aplicar a World Bosses y a rivales que no reciben debuffs, pero no a quien quita todos los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **Skills:**
  - `Panic` (23 retratos)

### Seducir

`seducir` · Entice · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** No puede moverse ni usar skills y camina despacio hacia quien lo aplicó. Sirve contra World Bosses y rivales a los que no se les aplican debuffs, pero no contra quien quita todos los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** No puede moverse ni usar skills y camina despacio hacia quien lo aplicó. Sirve contra World Bosses y rivales a los que no se les aplican debuffs, pero no contra quien quita todos los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **Nota:** El glosario en inglés dice «enemies that don't have debuffs» (rivales sin debuffs encima); el coreano, rivales a los que no se les aplican debuffs: los inmunes.
- **Skills:**
  - `Entice` (9 retratos)

### Provocar

`provocar` · Provoke · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Nota:** Obliga a los rivales a atacarlo a él: protege al resto del equipo.
- **Skills:**
  - `Mockery` (4 retratos) — Nota: Obliga a los rivales a atacarlo a él y «quitar todos los debuffs» no lo saca. Según el glosario del juego, al rival le sube el ataque y puede que no se le apliquen algunos buffs: si anula un Invencible, no se le aplica mientras dure.
  - `PROVOKE` (4 retratos)

### Encanto

`encantar` · Charm · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** No se mueve ni usa skills, ni siquiera los ataques que se activan solos. Alcanza también a los jefes grandes a los que no se les aplican debuffs, pero no a quien tiene un efecto que quita todos los debuffs. [Probable] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** No se mueve ni usa skills, ni siquiera los ataques que se activan solos. [Probable] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **Nota:** El glosario del juego define el encanto como un control; thanosvibs publica solo su daño mental continuo («Charm: Deals #% Mind Damage…»). Que sean el mismo efecto es probable: tienen el mismo nombre. Sobre los jefes, el inglés dice «epic monsters that have no debuffs» (monstruos sin debuffs encima); el coreano, jefes grandes a los que no se les aplican debuffs: los inmunes.
- **Skills:**
  - `CHARM` (24 retratos)

### Pérdida

`perdida` · Loss · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** No se mueve ni usa skills por un rato, pierde sus buffs y recibe más daño. No se le aplica a quien tiene un efecto que quita todos los debuffs. [Probable] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **PvP:** No se mueve ni usa skills por un rato, pierde sus buffs y recibe más daño. [Probable] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **Nota:** El glosario del juego dice que la pérdida frena al rival; thanosvibs publica su daño continuo y que le quita los buffs («Loss: Deals #% Bonus damage every # sec, removes Active Buffs»). Que sean el mismo efecto es probable: tienen el mismo nombre.
- **Skills:**
  - `Loss` (5 retratos)

## Debilitar

Le baja algo al rival o le quita buffs.

- **PvE:** Contra ese rival, el equipo pega más o recibe menos. [Probable]
- **PvP:** Contra ese rival, el equipo pega más o recibe menos. [Probable]

### Fractura

`fracturar` · Fracture · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **PvE:** Le baja todos los ataques básicos al rival (se acumula). Cada curación del rival le saca una carga y lo cura menos; «quitar todos los debuffs» no la saca. Además corta el ataque especial de los jefes de Alliance Battle Legend. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), [THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl))
- **PvP:** Le baja todos los ataques básicos al rival (se acumula). Cada curación del rival le saca una carga y lo cura menos; «quitar todos los debuffs» no la saca. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **Skills:**
  - `Fracture` (218 retratos)

### Baja las defensas del rival

`defensas_rival` · Lowers the foe's defenses · Se aplica al rival · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `Decreases all Basic Defenses (Can stack, ignores immunity)` (544 retratos)
  - `Incapacitation` (303 retratos) — Nota: La skill dice que le quita los buffs; el glosario del juego agrega que después le baja todas las defensas (se acumula) y que no sirve contra quien quita todos los debuffs.
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
  - `Incapacitation` (303 retratos) — Nota: La skill dice que le quita los buffs; el glosario del juego agrega que después le baja todas las defensas (se acumula) y que no sirve contra quien quita todos los debuffs.
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

- **PvE:** Los golpes no lo interrumpen ni le rompen la guardia, pero recibe el daño. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** Los golpes no lo interrumpen ni le rompen la guardia, pero recibe el daño. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
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

- **PvE:** Frena una cantidad fija de daño (las skills la dan como un porcentaje de la vida máxima), pero no frena el movimiento de los golpes, la rotura de guardia ni los debuffs. Hay escudos contra todo daño, solo contra el físico o solo contra el de energía. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **PvP:** Frena una cantidad fija de daño (las skills la dan como un porcentaje de la vida máxima), pero no frena el movimiento de los golpes, la rotura de guardia ni los debuffs. Hay escudos contra todo daño, solo contra el físico o solo contra el de energía. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **Skills:**
  - `Recharge Shield` (14 retratos) — Nota: Se recarga solo. Un escudo del mismo tipo se absorbe y lo hace más fuerte; uno de otro tipo se suma aparte (glosario del juego).
  - `SHIELD` (14 retratos)
  - `ENERGY SHIELD` (12 retratos)
  - `SUPER HIT SHIELD` (12 retratos) — Nota: Se recarga cada vez que su ataque le pega a un rival; no se puede quitar con «quitar buffs» y la perforación no lo afecta (glosario del juego).
  - `PHYSICAL SHIELD` (4 retratos)
- **Leads & Supports:**
  - `Max HP Shield` (2 retratos)

### Barrera

`barrera` · Barrier · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** No recibe daño por un tiempo y una cantidad de golpes (las skills dicen cuántos: «Barrier # time(s)»), pero no frena la rotura de guardia ni los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **PvP:** No recibe daño por un tiempo y una cantidad de golpes (las skills dicen cuántos: «Barrier # time(s)»), pero no frena la rotura de guardia ni los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **Nota:** El glosario en inglés dice solo «por un tiempo»; el coreano, por un tiempo y una cantidad de golpes, como la cuentan las skills.
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
  - `Death Throes` (3 retratos) — Nota: Al terminar, muere. La rotura de guardia lo afecta igual y el efecto no se puede quitar (glosario del juego).
- **Leads & Supports:**
  - `Immortality + Death` (1 retrato)
  - `Immortality + Heal` (1 retrato)

## Reducción de daño

Recibe menos daño o lo evita.

- **PvE:** Lo mantiene vivo. [Probable]
- **PvP:** Clave: la guía pone la reducción de daño y la evasión al frente del PvP. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))

### Invencible

`invencible` · Invincible · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Los golpes no lo interrumpen ni lo mueven, y no lo afectan la rotura de guardia, el daño ni los debuffs. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** Los golpes no lo interrumpen ni lo mueven, y no lo afectan la rotura de guardia, el daño ni los debuffs. Valiosa en PvP: la guía la sugiere en vez del proc de daño en el equipo de PvP. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026), [THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Nota:** El glosario en inglés dice que es inmune a los «basic attacks»; el coreano dice 피격 모션, la reacción al recibir un golpe. No tiene que ver con el stat de ataque básico.
- **Skills:**
  - `INVINCIBLE` (817 retratos)
  - `Body Enhancement` (1 retrato) — varía: el daño crece con cada golpe que ignora

### Inmune a todo daño (probabilidad)

`inmune_todo` · All damage immunity (chance) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Mientras dura no recibe daño ni debuffs, pero los golpes lo mueven igual y la rotura de guardia lo afecta. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** Mientras dura no recibe daño ni debuffs, pero los golpes lo mueven igual y la rotura de guardia lo afecta. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
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
- **PvP:** Solo contra esos rivales. Contra una facción, es lo que suele aportar el tercero del equipo en Timeline, el «buffer»: según NamuWiki, un personaje con aumentos o bajas de daño entre facciones en su pasiva o su uniforme, como Colossus. [Comprobado] ([NamuWiki — MARVEL 퓨처파이트/타임라인 배틀 (en coreano)](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%20%EB%B0%B0%ED%8B%80))
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
  - `Elasticity` (5 retratos) — Nota: Se suma a la reducción de daño físico; no la sacan la cancelación ni la incapacitación, pero sí el sangrado (glosario del juego).

### Menos daño de energía recibido

`dano_energia_recibido` · Less energy damage taken · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **Skills:**
  - `ENERGY DAMAGE ↓` (19 retratos)

### Inmune al daño físico (probabilidad)

`inmune_fisico` · Physical damage immunity (chance) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Mientras dura no recibe daño físico ni los debuffs de ese daño, pero los golpes lo mueven igual y la rotura de guardia lo afecta. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** Mientras dura no recibe daño físico ni los debuffs de ese daño, pero los golpes lo mueven igual y la rotura de guardia lo afecta. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **Skills:**
  - `PHYSICAL IMMUNITY` (27 retratos)
- **Leads & Supports:**
  - `Physical Immunity Chance` (1 retrato)

### Inmune al daño de energía (probabilidad)

`inmune_energia` · Energy damage immunity (chance) · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** Mientras dura no recibe daño de energía ni los debuffs de ese daño, pero los golpes lo mueven igual y la rotura de guardia lo afecta. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** Mientras dura no recibe daño de energía ni los debuffs de ese daño, pero los golpes lo mueven igual y la rotura de guardia lo afecta. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
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

- **PvE:** Suma un valor fijo a la evasión, sin la reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **PvP:** Suma un valor fijo a la evasión, sin la reducción por nivel. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), [THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4), MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026))
- **Nota:** El glosario en inglés dice que esquiva «a una tasa fija» (at a set rate); el coreano, que le suma un valor fijo a la evasión.
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
- **Nota:** Como liderazgo o soporte, según Ezequiel, solo le sirven a quien tiene una mejora de daño según su resistencia (diez artefactos y la Striker de Ghost Rider y de Hades): la app las cuenta solo para ellos.
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

- **PvP:** Muy útil en Timeline (la guía lo dice del soporte de Wasp). Cuando dura un tiempo, protege mientras dura: NamuWiki dice que el liderazgo de Malekith le da a todo el equipo 20 s de inmunidad a los estados alterados, y la guía de thanosvibs llama «Debuff Immunity» a la pasiva de Tier-2 de Wasp, que la API publica como «Removes all Debuffs» por 20 s. En los liderazgos y soportes casi siempre dura 12 s desde que recibe un debuff: que esos protejan igual es lo probable, pero ninguna fuente lo dice. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 1](https://thanosvibs.money/beginners/1), [THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4), [NamuWiki — MARVEL 퓨처파이트/타임라인 배틀 (en coreano)](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%20%EB%B0%B0%ED%8B%80))
- **Nota:** La API de skills a veces publica «Give Power» sin decir qué otorga; Leads & Supports trae que es esto (docs/AUDITORIA.md, sección 7).
- **Skills:**
  - `Removes all Debuffs. ` (409 retratos)
  - `Parry` (2 retratos)
- **Leads & Supports:**
  - `Remove All Debuffs` (81 retratos)

### Inmunidad a debuffs

`inmune_debuffs` · Debuff immunity · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvP:** Crucial en PvP: si el principal no la tiene, se lleva un líder o un soporte que la dé. [Comprobado] ([THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4))
- **Nota:** La guía de thanosvibs llama «Debuff Immunity» también a «quitar todos los debuffs» con duración (la Tier-2 de Wasp). No son lo mismo: según el glosario del juego, la detención del tiempo, el encanto, la seducción, el control mental y el pánico alcanzan a los jefes y rivales a los que no se les aplican debuffs, pero no a quien tiene un efecto que quita todos los debuffs.
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

### Inmune a la rotura de guardia

`inmune_romper_guardia` · Guard Break immunity · Se aplica a su lado · Le sirve: a cualquiera del equipo.

- **PvE:** La rotura de guardia no le cancela la skill; la superrotura de guardia, sí. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
- **PvP:** La rotura de guardia no le cancela la skill; la superrotura de guardia, sí. [Comprobado] (MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026))
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
- **Nota:** Como liderazgo o soporte, según Ezequiel, no sirve: la app no lo cuenta para nadie. Como efecto de las skills (frenesí) sigue contando.
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

## Glosario del juego

El glosario de skills del juego (Skill Name Glossary en inglés, 스킬 용어 사전 en coreano), desde `scripts/contenido/glosario.json`: 44 términos, en el orden del juego. El coreano es el original: donde el inglés no dice lo mismo, se aclara.

### Errores que se repiten

- **«Basic attacks» donde el coreano dice «reacción al golpe»** (Invencible, Superarmadura, Escudo, Inmunidad al daño, Contraataque). 피격 모션 es la reacción al recibir un golpe: el personaje se frena y se le corta lo que estaba haciendo. El inglés lo traduce como «basic attacks» o «basic attack motions», que no tiene nada que ver con el stat de ataque básico. Con la traducción correcta todo cierra: la rotura de guardia corta la skill forzando esa reacción, la superarmadura es inmune a ella (y por eso a la rotura de guardia), y el contraataque reemplaza esa reacción, así que no se activa mientras es invencible.
- **«Sin debuffs» donde el coreano dice «inmunes a los debuffs»** (Congelación del tiempo, Encanto, Seducción, Control mental). El coreano dice que estos controles alcanzan también a los jefes y rivales a los que no se les aplican debuffs, es decir, a los inmunes. El inglés dice «that have no debuffs» o «that don't have debuffs», que se lee como rivales sin debuffs encima. En los cuatro, lo que no los deja entrar es tener un efecto que quita todos los debuffs.
- **«Type» donde el coreano dice «elemento»** (Daño puro, Type Amplification). 속성 es el elemento (fuego, frío, rayo, veneno, mente). El inglés lo traduce a veces como «Type», que en el juego también es la clase (Combate, Detonación, Velocidad, Universal). El daño puro no pasa por las resistencias elementales (el inglés dice «Type Resistance»), Type Amplification sube el daño de las skills con elemento, y la etiqueta «TYPE PENETRATION» de las skills atraviesa una resistencia elemental.

### Términos

- **Rotura de guardia** (Guard Break) · 가드 브레이크: Corta la skill que está usando el rival y abre un contraataque. La superrotura de guardia atraviesa además la inmunidad a la rotura de guardia.
  - **El inglés y el coreano:** El coreano dice cómo la corta: fuerza la reacción al golpe (피격 모션). El inglés solo dice que la cancela.
  - **En el catálogo:** Rotura de guardia (cancela la skill del rival), Inmune a la rotura de guardia.
- **Evasión garantizada** (Guaranteed Dodge Rate) · 무조건 회피율: La evasión depende de la diferencia de nivel con el rival. La garantizada no pasa por esa cuenta: le suma un valor fijo a la evasión.
  - **El inglés y el coreano:** El inglés dice que esquiva «a una tasa fija»; el coreano, que le suma un valor fijo a la evasión.
  - **En el catálogo:** Evasión garantizada.
- **Crítico garantizado** (Guaranteed Critical Rate) · 무조건 치명타율: La probabilidad de crítico depende de la diferencia de nivel con el rival. La garantizada no pasa por esa cuenta: le suma un valor fijo a la probabilidad de crítico.
  - **El inglés y el coreano:** El inglés dice que hace crítico «a una tasa fija»; el coreano, que le suma un valor fijo a la probabilidad de crítico.
  - **En el catálogo:** Crítico garantizado.
- **Daño puro** (Pure Damage) · 순수 피해량: El daño que recibe un personaje sale del ataque del rival, reducido por su defensa y sus resistencias elementales. El daño puro no pasa por la defensa ni por las resistencias.
  - **El inglés y el coreano:** El inglés dice «Character Type Resistance»; el coreano, resistencias elementales (속성 저항).
  - **En el catálogo:** Acumula daño.
- **Pasiva de equipo** (Team Passive) · 팀 패시브: Una pasiva que les llega a todos los del equipo aunque su dueño no sea el líder: las que dicen «Applies to: All Team members». El análisis de la app ya las manda al equipo.
- **Invencible** (Invincible) · 무적: Inmune a todo lo que lo puede afectar: la reacción a los golpes, la rotura de guardia, el daño y los debuffs.
  - **El inglés y el coreano:** El inglés dice que es inmune a los «basic attacks»; el coreano, a la reacción al golpe (피격 모션).
  - **En el catálogo:** Invencible.
- **Superarmadura** (Super Armor) · 슈퍼 아머: Inmune a la reacción a los golpes y a la rotura de guardia: los ataques del rival no le cortan lo que está haciendo, pero recibe el daño.
  - **El inglés y el coreano:** El inglés dice «basic attack motions»; el coreano, la reacción al golpe (피격 모션).
  - **En el catálogo:** Superarmadura.
- **Barrera** (Barrier) · 배리어: Frena el daño por un tiempo y una cantidad de golpes. No frena la rotura de guardia ni los debuffs.
  - **El inglés y el coreano:** El inglés dice solo «por un tiempo» y que no frena la rotura de guardia; el coreano agrega la cantidad de golpes (como la cuentan las skills: «Barrier # time(s)») y que tampoco frena los debuffs.
  - **En el catálogo:** Barrera.
- **Escudo** (Shield) · 쉴드: Frena una cantidad fija de daño por un tiempo. No frena la reacción a los golpes, la rotura de guardia ni los debuffs. Hay escudos contra todo daño, solo contra el físico o solo contra el de energía.
  - **El inglés y el coreano:** El inglés no dice que la cantidad de daño es fija («stops damage for a set amount of time») y llama «basic attack motions» a la reacción al golpe (피격 모션).
  - **En el catálogo:** Escudo.
- **Inmunidad al daño** (Damage Immunity) · 피해 면역: Frena el daño y los debuffs por un tiempo, pero no la reacción a los golpes ni la rotura de guardia. Puede ser contra todo daño, solo el físico o solo el de energía, con sus debuffs.
  - **El inglés y el coreano:** El inglés dice «basic attack motions»; el coreano, la reacción al golpe (피격 모션).
  - **En el catálogo:** Inmune a todo daño (probabilidad), Inmune al daño físico (probabilidad), Inmune al daño de energía (probabilidad).
- **Miedo** (Fear) · 공포: El rival huye de quien se lo aplicó y no puede atacar ni usar skills.
  - **En el catálogo:** Miedo.
- **Trampa** (Snare) · 속박: Ata al rival a un lugar: no puede moverse, atacar ni usar skills.
  - **En el catálogo:** Atrapar.
- **Congelación del tiempo** (Time Freezing) · 타임 프리징: Encierra al rival en el tiempo: no se mueve ni ataca. Alcanza también a los jefes grandes a los que no se les aplican debuffs, pero no a quien tiene un efecto que quita todos los debuffs.
  - **El inglés y el coreano:** El inglés dice «epic monsters that have no debuffs»; el coreano, jefes grandes a los que no se les aplican debuffs.
  - **En el catálogo:** Detención del tiempo.
- **Encanto** (Charm) · 매혹: El rival no se mueve ni usa skills, ni siquiera los ataques que se activan solos. Alcanza también a los jefes grandes a los que no se les aplican debuffs, pero no a quien tiene un efecto que quita todos los debuffs.
  - **El inglés y el coreano:** El inglés dice «epic monsters that have no debuffs»; el coreano, jefes grandes a los que no se les aplican debuffs.
  - **En el catálogo:** Encanto, Daño mental del encanto.
- **No se deja apuntar** (Ignore Targeting) · 타겟팅 무시: Queda fuera de la mira del rival: las skills que apuntan a un objetivo lo ignoran y no recibe daño aunque lo ataquen. Usado justo cuando el rival ataca, esquiva el ataque entero y deja seguir con el propio.
- **Seducción** (Entice) · 유혹: El rival no se mueve ni usa skills y camina despacio hacia quien lo sedujo. Sirve contra World Bosses y rivales a los que no se les aplican debuffs, pero no contra quien tiene un efecto que quita todos los debuffs.
  - **El inglés y el coreano:** El inglés dice «enemies that don't have debuffs»; el coreano, rivales a los que no se les aplican debuffs.
  - **En el catálogo:** Seducir.
- **Control mental** (Mind Control) · 정신 지배: El rival pasa a pelear del lado propio y recibe más daño. Sirve contra World Bosses y rivales a los que no se les aplican debuffs, pero no contra quien tiene un efecto que quita todos los debuffs.
  - **El inglés y el coreano:** El inglés dice «enemies that don't have debuffs»; el coreano, rivales a los que no se les aplican debuffs.
  - **En el catálogo:** Control mental.
- **Escudo recargable** (Recharge Shield) · 리차지 쉴드: Un escudo que se recarga solo. Si recibe otro escudo del mismo tipo, lo absorbe y crece; uno del otro tipo (físico o de energía) no lo agranda: cada uno funciona aparte.
  - **En el catálogo:** Escudo.
- **Fractura** (Fracture) · 골절: Le baja todos los ataques básicos al rival y se acumula. Cada curación del rival le saca una carga y lo cura menos. «Quitar todos los debuffs» no la saca.
  - **En el catálogo:** Fractura.
- **Incapacitación** (Incapacitation) · 무력화: Le saca los buffs al rival y le baja todas las defensas (se acumula). No se le aplica a quien tiene un efecto que quita todos los debuffs.
  - **En el catálogo:** Le quita los buffs al rival, Baja las defensas del rival.
- **Contraataque** (Counterattack) · 반격기: Al recibir un golpe, en vez de la reacción al golpe hace un contraataque. Como necesita esa reacción, no se activa mientras es invencible.
  - **El inglés y el coreano:** El inglés dice que reemplaza los «basic attack motions» y explica mal por qué no se activa siendo invencible; el coreano: reemplaza la reacción al golpe (피격 모션), que el invencible no tiene.
- **Elasticidad** (Elasticity) · 탄성: Acumula reducción del daño físico recibido. No la sacan la cancelación (Cancel) ni la incapacitación; el sangrado, sí.
  - **En el catálogo:** Menos daño físico recibido.
- **Concentración** (Concentration) · 집중: Un stat que mejora lo que rinden algunas skills y algunos efectos de los C.T.P.: los efectos de barra propia de los reforjados crecen con ella.
- **Daño perforante adicional** (Additional Pierce Damage) · 추가 관통 피해: Daño extra que ignora del todo la defensa; sale del daño de la skill.
  - **En el catálogo:** Daño perforante adicional.
- **Penetration** · 간파: Cuando lo atacan, tiene una probabilidad de cortar el ataque del rival: sube si su Concentración es mayor que la del rival y baja si es menor. Barra propia que se carga al recibir golpes; después de usarse, no carga por 5 s.
  - **El inglés y el coreano:** 간파 quiere decir «ver venir» (leer el ataque), no perforar: no tiene que ver con la Perforación (Pierce) ni con la etiqueta «TYPE PENETRATION» de las skills. El inglés dice que corta la skill del rival; el coreano, su ataque.
  - **Lo da:** Regeneration reforjado, Transcendence reforjado.
  - **Nota:** Transcendence reforjado da Penetration y Beatdown juntos.
- **Beatdown** · 압도: Al usar una skill, sube el daño perforante adicional (sin el tope máximo) y da inmunidad a la rotura de guardia; la suba crece con la Concentración. Barra propia que se carga al moverse; después de usarse, no carga por 7 s.
  - **Lo da:** Energy reforjado, Transcendence reforjado.
- **Type Amplification** · 속성 증폭: Al usar una skill, sube el ataque de las skills con elemento y da inmunidad a la rotura de guardia; la suba crece con la Concentración. Barra propia que se carga al moverse; después de usarse, no carga por 7 s.
  - **El inglés y el coreano:** El menú en inglés dice «Type Amplification» y el texto, «Element Amplification»; el coreano, 속성 증폭: amplificación de elemento. El C.T.P. Judgement reforjado dice en inglés que sube el daño de las skills «de tipo».
  - **Lo da:** Judgement reforjado.
- **Steel** · 강철: Da inmunidad a la rotura y a la superrotura de guardia y baja el daño recibido; la baja crece con la Concentración. Barra propia que se carga al recibir golpes; se activa sola y después no carga por 6 s.
  - **Lo da:** Authority reforjado.
- **Burla** (Mockery) · 조롱: Un debuff que obliga a los rivales a atacarlo a él. A los afectados les sube el ataque, pero con cierta probabilidad no les entra un buff determinado: si la burla anula la invencibilidad, por ejemplo, no pueden volverse invencibles mientras dure.
  - **En el catálogo:** Provocar.
- **Strike** · 강타: Al usar una skill, ignora la evasión del rival y sube el daño a los jefes; la suba crece con la Concentración. Barra propia que se carga al moverse; después de usarse, no carga por 7 s.
  - **Lo da:** Destruction reforjado.
- **Ambush** · 맹공: Da inmunidad a la rotura y a la superrotura de guardia y al daño reflejado, e ignora una parte de la reducción de daño del rival; esa parte crece con la Concentración. Barra propia que se carga al recibir golpes; se activa sola y después no carga por 6 s.
  - **Lo da:** Greed reforjado.
  - **Nota:** thanosvibs dice que ignora la reducción de defensa del rival; el juego, la reducción de daño (el hallazgo de los C.T.P., en la auditoría).
- **Fortaleza** (Fortitude) · 불굴: Por un tiempo la vida no baja de 1 y, al terminar, se cura. Se activa sola cuando la vida baja de cierto valor; mientras dura, da inmunidad a la rotura de guardia y no se puede quitar con efectos que quitan buffs.
  - **En el catálogo:** No muere por un tiempo, Inmune a la rotura de guardia, Curación.
- **Blade** · 칼날: Al usar una skill, atraviesa los efectos defensivos del rival y sube el daño; la suba crece con la Concentración. Barra propia que se carga al usar skills (no los ataques básicos); se activa sola y después no carga por 7 s.
  - **Lo da:** Veteran reforjado.
- **Defend** · 방호: Da inmunidad a la rotura y a la superrotura de guardia y una barrera que ignora la cancelación y la perforación y frena una cantidad de golpes; además cura según la Concentración. Barra propia que se carga al recibir golpes; se activa sola y después no carga por 7 s.
  - **Lo da:** Patience reforjado.
- **Escudo de supergolpe** (Super Hit Shield) · 슈퍼 히트 쉴드: Un escudo que se recarga cada vez que su ataque le pega al rival. Si se activan varios escudos a la vez, ignora los demás y queda solo este. No lo quitan los efectos que quitan buffs ni lo atraviesa la perforación.
  - **En el catálogo:** Escudo.
- **Enraged** · 격노: Al usar una skill, sube el daño crítico aunque pase el tope y da inmunidad a la rotura de guardia; la suba crece con la Concentración. Barra propia que se carga al usar skills (no los ataques básicos); después de usarse, no carga por 7 s.
  - **Lo da:** Rage reforjado.
- **Vitality** · 활력: Da inmunidad a la rotura y a la superrotura de guardia y cura vida cada segundo; la cura crece con la Concentración. Barra propia que se carga al recibir golpes; se activa sola y después no carga por 7 s.
  - **Lo da:** Refinement reforjado.
- **Wall** · 방벽: Una barrera propia que baja el daño recibido; cada golpe le resta reducción hasta un mínimo, que dura hasta que se termina. No se usa junto con la Barrera y no se suma a otras reducciones de daño: va aparte.
  - **Lo da:** Conquest sin reforjar.
  - **Nota:** En Conquest sin reforjar se activa con la vida por debajo del 50%.
- **Clash** · 격돌: Da inmunidad a la rotura y a la superrotura de guardia y al daño reflejado, y sube el daño básico; la suba crece con la Concentración. Barra propia que se carga al recibir golpes; se activa sola y después no carga por 6 s.
  - **Lo da:** Conquest reforjado.
- **Pánico** (Panic) · 공황: Le aplica miedo al rival y lo hace recibir más daño. Se le puede aplicar a World Bosses y a rivales que no reciben debuffs, pero no a quien tiene un efecto que quita todos los debuffs.
  - **En el catálogo:** Pánico.
  - Sin la captura en coreano.
- **Pérdida** (Loss) · 상실: Absorbe las habilidades del rival por un rato: no se mueve ni usa skills, pierde sus buffs y recibe más daño. No se le aplica a quien tiene un efecto que quita todos los debuffs.
  - **En el catálogo:** Pérdida, Daño de la pérdida.
- **Agonía** (Death Throes) · 최후의 발악: Por un tiempo la vida no baja de 1 y, al terminar, muere en el acto. Se activa sola cuando la vida baja de cierto valor; la rotura de guardia lo afecta, pero no se puede quitar con efectos que quitan buffs.
  - **En el catálogo:** No muere por un tiempo.
- **Marca** (Mark) · 표식: Le pone una marca al rival: las skills que le aplican efectos al marcado hacen más daño. Alcanza a World Bosses, a jefes grandes a los que no se les aplican debuffs y a quien quita todos los debuffs, y no la cambian los aumentos ni las bajas del efecto de los debuffs.
- **Fury** · 맹렬: Al usar una skill, sube todo el daño y da inmunidad a la rotura de guardia; la suba crece con la Concentración. Barra propia que se carga al usar skills (no los ataques básicos); después de usarse, no carga por 7 s.
  - **Lo da:** Competition reforjado.

## Fuentes

- MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026)
- MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026)
- [NamuWiki — MARVEL 퓨처파이트/타임라인 배틀 (en coreano)](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%ED%83%80%EC%9E%84%EB%9D%BC%EC%9D%B8%20%EB%B0%B0%ED%8B%80)
- [THANO$VIB$ — Alliance Battle (ABX/ABL)](https://thanosvibs.money/abxl)
- [THANO$VIB$ — C.T.P.s](https://thanosvibs.money/ctps)
- [THANO$VIB$ Beginner's Guide, parte 1](https://thanosvibs.money/beginners/1)
- [THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3)
- [THANO$VIB$ Beginner's Guide, parte 4](https://thanosvibs.money/beginners/4)
- [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters)
