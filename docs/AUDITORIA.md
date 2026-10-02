# Auditoría de datos

Generado por `scripts/auditar.py` el 2026-10-02, sobre los datos del juego 12.2.5 (thanosvibs) y la wiki de Future Fight bajada en la misma sincronización.

La app muestra thanosvibs. Esto marca dónde otra fuente dice otra cosa, con los dos valores; no corrige nada. La wiki la edita la comunidad y muchas páginas quedaron viejas (uniformes sin sección, valores de antes de un rebalanceo), así que una diferencia es algo para revisar en el juego, no un error confirmado de ninguna de las dos.

En la app, cada ficha muestra lo que le toca en "Verificación entre fuentes".

## Resumen

| Chequeo | Coinciden | Difieren | Sin dato para comparar |
|---|---|---|---|
| Daño de skills (thanosvibs vs wiki) | 1122 (+849 donde la wiki lista menos etapas) | 57 | 57 |
| Recarga de skills | 1777 | 40 | 86 |
| Clase (infobox de la wiki) | 541 | 5 | — |
| Bando (infobox de la wiki) | 528 | 11 | — |
| Género (infobox de la wiki) | 541 | 3 | — |
| Raza (infobox de la wiki) | 535 | 13 | — |
| Tipo de ataque (infobox de la wiki) | 531 | 21 | — |
| Instinto (campo vs categoría de la wiki) | 77 | 4 | — |
| Artefactos a 6★ (thanosvibs vs wiki) | 208 (+31 donde la wiki lista otro nivel de estrellas) | 18 | 10 sin fila en la wiki; 5 con niveles incompletos en thanosvibs |

Cobertura de la wiki: de 5887 skills (activas, Definitiva y Striker) de thanosvibs, 2270 (39%) se pudieron comparar; 1222 están en la página pero solo en la sección de otro uniforme, y el resto no aparece (sobre todo uniformes que la wiki no documenta). Infobox: 552 retratos con pestaña en la wiki, 305 sin pestaña de su uniforme y 31 de personajes sin infobox legible.

Catálogo de efectos (docs/CATALOGO.md): 228 etiquetas de skills y 72 stats de Leads & Supports en los datos; todos clasificados.

## 1. Skills: daño y recarga

Método: cada skill de thanosvibs se busca por nombre en la página de la wiki del personaje, en la sección de su uniforme o en la general (la de "All Uniforms"; en las páginas viejas, sin secciones por uniforme, la general solo vale para el uniforme base). Nombres parecidos al 85% cuentan, porque la wiki tiene erratas como "Turque Chain". Se comparan los % de daño distintos de la skill (de ataque físico, de energía o de vida) y la recarga. "Menos etapas" = la wiki lista solo algunos de los % que trae thanosvibs: no es una contradicción. La Definitiva de Tier-3 y la Striker no tienen recarga (se cargan con su barra), así que solo se compara su daño.

### Daño distinto (57)

| Personaje | Uniforme | Slot | Skill | thanosvibs | wiki |
|---|---|---|---|---|---|
| Adam Warlock | Infinity Countdown | Active Ult | Fate's End | 97 | 87 |
| Adam Warlock | Marvel Studios' Guardians of the Galaxy 3 | Active Ult | Fate's End | 97 | 87 |
| Adam Warlock | Modern | Active 4 | Cosmic Master | 128 | 97 |
| Adam Warlock | Modern | Active Ult | Fate's End | 97 | 87 |
| Agent Venom | Agent Anti-Venom | Active 2 | Venom Lash | 128 | 60 |
| America Chavez | Ultimates | Active 1 | Stars and Stripes | 112 | 115 |
| America Chavez | Ultimates | Active 2 | Smash Kick | 124 | 126 |
| America Chavez | Ultimates | Active 4 | Dimension Drop | 98 | 88 |
| America Chavez | Ultimates | Active 5 | Star Shower | 124, 195 | 78 |
| Arachknight | Arachknight 2099 | Active 4 | Shuriken Storm | 120 | 10 |
| Black Cat | Modern | Active 2 | Acrobatic Kick | 158 | 156 |
| Blade | Avengers | Active 2 | Blood Dance | 58, 108 | 56 |
| Cable | Modern | Active 5 | Plasma Shower | 127 | 45 |
| Captain America | Back to Basics | Active Ult | Heroic Charge | 95, 120, 200 | 100 |
| Captain America | Galactic Talon | Active Ult | Heroic Charge | 95, 120, 200 | 100 |
| Captain America | What If... Zombies?! | Active Ult | Heroic Charge | 95, 120, 200 | 100 |
| Clea | Modern | Active Ult | Mystic Storm | 100, 120, 130 | 64 |
| Deadpool | Modern | Active 3 | Cool Finale | 85, 93, 103 | 44 |
| Destroyer | Prometheus | Active 4 | Obliteration Wave | 172 | 112 |
| Doctor Doom | 3099 | Active 1 | Devil's Grab | 130, 150, 185 | 183 |
| Doctor Doom | God Emperor | Active 1 | Emperor's Fist | 55, 65, 70 | 183 |
| Doctor Octopus | Ends of the Earth | Active 2 | Crusher | 70 | 68 |
| Doctor Strange | All-New, All-Different | Active 5 | Sorcerer Supreme |  | 161 |
| Giant-Man | Modern | Active 5 | Giant Jackhammer | 245 | 102 |
| Green Goblin | Ultimate | Active Ult | Goblin Unleashed | 95, 120 | 90 |
| Hela | Modern | Active 1 | Fires of Hel | 96 | 48, 96 |
| Hela | Modern | Active 2 | Nightsword Stab | 112 | 96, 112 |
| Hela | Modern | Active 4 | Nightsword's Glow | 90 | 30, 90 |
| Hela | Modern | Active 5 | Goddess of Death | 140 | 140, 163 |
| Hulk | Fear Itself | Active Ult | Worldbreaker Smash | 106 | 150 |
| Hulk | Immortal Hulk | Active Ult | Worldbreaker Smash | 53 | 150 |
| Hulk | Marvel Studios' Spider-Man: Brand New Day | Active Ult | Worldbreaker Smash | 106 | 150 |
| Hulk | The Avengers | Active 3 | Hulk Smash | 120 | 193 |
| Hulk | Titan | Active Ult | Worldbreaker Smash | 106 | 150 |
| Hulk (Amadeus Cho) | Totally Awesome Hulk | Active 1 | Tornado Punch | 124 | 124, 160 |
| Hulkbuster (Iron Man Mark 44) | Avengers: Age of Ultron | Active Ult | Buster Blast | 85, 108, 111 | 66 |
| Ikaris | Modern | Active Ult | Fated Precision | 200, 240 | 65 |
| Jean Grey | Dark Phoenix | Active Ult | Revelation | 146, 155, 180 | 62 |
| Jessica Jones | Modern | Active 5 | Collateral Damage | 148 | 141 |
| Kaecilius | Marvel Studios' Doctor Strange | Active 5 | Mystical Avalanche | 153 | 152 |
| Moon Knight | Marvel Studios' Moon Knight | Active 3 | Mercenary Bombing | 77 | 200 |
| Namor | Black Panther: Wakanda Forever | Active Ult | King of Atlantis' Command | 153 | 180 |
| Nova (Richard Rider) | Modern | Active 2 | Light Speed Strike | 30, 49 | 19 |
| Professor X | Classic | Active Ult | Cerebro Scan | 155, 200 | 100 |
| Professor X | Modern | Active Ult | Cerebro Scan | 155, 200 | 100 |
| Rogue | Classic | Active Ult | Ultimate Absorption | 90 | 190 |
| Spider-Man | Classic | Active 5 | Wrecking Web | 346 | 345 |
| Spot | Spider-Man: Across the Spider-Verse | Active 4 | Punching Bag | 40, 80, 118 | 89 |
| Squirrel Girl | Marvel NOW! | Active 4 | Squirrel Army | 166 | 116 |
| Storm | Modern | Active 5 | Elemental Goddess | 50 | 90 |
| Thor | The Avengers | Active Ult | Thunder Blow | 53, 385 | 72 |
| Thor | The Avengers | Striker Skill | King of the Realms |  | 72 |
| Viper | Modern | Active 1 | Whip Strike | 103, 120 | 46 |
| Viper | Modern | Active 2 | Toxic Throw | 45, 107 | 95 |
| Wiccan | New Avengers | Active 1 | Spell Bomb | 80 | 115 |
| Wolverine | House of X | Active 4 | Berserker Slice | 125 | 103 |
| Yondu | Guardians of the Galaxy | Active 5 | Ravager Strike | 93 | 98 |

### Recarga distinta (40)

| Personaje | Uniforme | Slot | Skill | thanosvibs (s) | wiki (s) |
|---|---|---|---|---|---|
| Arachknight | Infinity Warps | Active 1 | Web Shuriken | 6 | 16 |
| Captain America | Marvel NOW! | Active 2 | Valor | 7 | 6 |
| Clea | Modern | Active Ult | Mystic Storm | 60 | 9 |
| Doctor Doom | 3099 | Active 1 | Devil's Grab | 8 | 6 |
| Doctor Doom | God Emperor | Active 1 | Emperor's Fist | 7 | 6 |
| Doctor Doom | God Emperor | Active 2 | Power of Destruction | 8 | 7 |
| Doctor Octopus | Superior Octopus | Active 2 | Spinning Elimination | 8 | 6 |
| Doctor Octopus | Superior Spider-Man | Active 2 | Final Embrace | 8 | 6 |
| Doctor Voodoo | Modern | Active 4 | Soul Magic Eruption | 15 | 13 |
| Echo | Enter the Phoenix | Active 5 | Phoenix Swarm | 15 | 25 |
| Elektra | Classic | Active 2 | Harsh Strike | 6 | 8 |
| Elektra | Classic | Active 4 | Silent Ambush | 10 | 11 |
| Elektra | Marvel Studios' Daredevil | Active 2 | Harsh Strike | 6 | 8 |
| Elektra | Marvel Studios' Daredevil | Active 4 | Silent Ambush | 10 | 11 |
| Elektra | Woman Without Fear | Active 1 | Acrobatic Attack | 9 | 7 |
| Elektra | Woman Without Fear | Active 2 | Threat Detection | 9 | 7 |
| Elektra | Woman Without Fear | Active 4 | Ruthless Sweep | 14 | 11 |
| Fantomex | X-Force | Active 2 | Acrobatic Fire | 8 | 7 |
| Gambit | Modern | Active 2 | Scatter Card | 6 | 8 |
| Lizard | Classic | Active 5 | Reptile Instinct | 30 | 14 |
| Magneto | Classic | Active 4 | Magnetic Storm | 14 | 13 |
| Magneto | Marvel NOW! | Active 4 | Magnetic Storm | 14 | 13 |
| Misty Knight | All-New, All-Different | Active 4 | Cold Shoulder | 12 | 13 |
| Phyla-Vell | Modern | Active 4 | Energy Eruption | 12 | 71 |
| Polaris | Uncanny X-Men | Active 4 | Magnetic Resonance Explosion | 15 | 16 |
| Professor X | Classic | Active 2 | Mental Disruption | 7 | 11 |
| Punisher | Noir | Active 3 | Killer Instinct | 10 | 30 |
| Scorpion | Modern | Active 4 | Prey Piercer | 16 | 10 |
| Scorpion | Modern | Active 5 | Scorpion Slam | 15 | 14 |
| Spider-Man | All-New, All-Different | Active 5 | Wrecking Web | 11 | 9 |
| Spider-Man | Back to Basics | Active 2 | Perfect Dodge | 9 | 12 |
| Spider-Man | Classic | Active 5 | Wrecking Web | 11 | 9 |
| Squirrel Girl | Marvel NOW! | Active 4 | Squirrel Army | 12 | 13 |
| Squirrel Girl | New Avengers | Active 4 | Squirrel Army | 12 | 13 |
| Storm | Inhumans vs X-Men | Active 3 | Ice Whirlwind | 14 | 13 |
| Storm | Modern | Active 3 | Wind Shear | 14 | 13 |
| Storm | X-Men Red | Active 3 | Wind Shear | 14 | 13 |
| Thor (Jane Foster) | All-New, All-Different | Active 5 | Goddess of Thunder | 15 | 16 |
| Valkyrie | Fearless Defenders | Active 4 | Rage of the Valkyrie | 14 | 10 |
| Viper | Modern | Active 2 | Toxic Throw | 10 | 7 |

## 2. Infobox: clase, bando, género, raza y tipo de ataque

El tipo de ataque de thanosvibs no es un campo: se deriva de con qué escalan los % de daño de sus skills activas (igual que en la ficha). Cuando la wiki dice otra cosa, sus propias skills suelen darle la razón a thanosvibs (Ghost Rider Robbie Reyes: infobox "Physical", skills "% of Energy Attack").

### Clase (5)

| Personaje | Uniforme | thanosvibs | wiki |
|---|---|---|---|
| Cassie Lang | Ant-Man and the Wasp: Quantumania | Speed | Blast |
| Green Goblin | Dark Avengers | Blast | Speed |
| Green Goblin | Ultimate | Combat | Speed |
| Jean Grey | X-Men Red | Blast | Universal |
| X-23 | All-New Wolverine | Combat | Speed |

### Bando (11)

| Personaje | Uniforme | thanosvibs | wiki |
|---|---|---|---|
| Agent Venom | Agent Anti-Venom | Super Hero | Super Villain |
| Agent Venom | All-New, All-Different | Super Hero | Super Villain |
| Agent Venom | Classic | Super Hero | Super Villain |
| Agent Venom | Guardians of the Galaxy | Super Hero | Super Villain |
| Captain Marvel | Marvel Studios' The Marvels | Super Hero | Super Villain |
| Kraven The Hunter | Modern | Super Villain | Super Hero |
| Polaris | Uncanny X-Men | Super Villain | Super Hero |
| Ronan | Annihilators | Super Hero | Super Villain |
| Scream | Silence | Super Hero | Super Villain |
| Spider-Gwen | Gwenom | Super Villain | Super Hero |
| Vision | Modern | Super Hero | Super Villain |

### Género (3)

| Personaje | Uniforme | thanosvibs | wiki |
|---|---|---|---|
| Deadpool | Holiday Party | Female | Male |
| Deadpool | Lady Deadpool | Female | Male |
| Shadow Shell | Modern | Female | Male |

### Raza (13)

| Personaje | Uniforme | thanosvibs | wiki |
|---|---|---|---|
| Clea | Modern | Alien | Human |
| Karnak | All-New, All-Different | Inhuman | Human |
| Karnak | War of Kings | Inhuman | Human |
| Quasar (Wendell Vaughn) | Modern | Human | Alien |
| Quicksilver | Classic | Human | Other |
| Quicksilver | Marvel Legacy | Human | Other |
| Quicksilver | Summer Days | Human | Other |
| Quicksilver | Uncanny Avengers | Human | Other |
| Scarlet Witch | All-New, All-Different | Human | Other |
| Scarlet Witch | Classic | Human | Other |
| Scarlet Witch | Marvel Studios' Avengers: Infinity War | Human | Other |
| Scarlet Witch | Marvel Studios' WandaVision | Human | Other |
| Scarlet Witch | Uncanny Avengers | Human | Other |

### Tipo de ataque (21)

| Personaje | Uniforme | thanosvibs | wiki |
|---|---|---|---|
| Ant-Man | Modern | Physical | Energy |
| Athena | Incredible Hercules | Physical | Energy |
| Ghost Rider (Robbie Reyes) | Marvel NOW! | Energy | Physical |
| Giant-Man | Modern | Physical | Energy |
| Green Goblin | Classic | Energy | Physical |
| Green Goblin | Dark Avengers | Energy | Physical |
| Green Goblin | Red Goblin | Energy | Physical |
| Green Goblin | Ultimate | Energy | Physical |
| Hercules | Modern | Physical | Energy |
| Hope Summers | Modern | Physical | Energy |
| Hulk | The Avengers | Physical | Energy |
| Lincoln Campbell | Marvel Studios' Agents of S.H.I.E.L.D. | Energy | Physical |
| Mantis | Guardians of the Galaxy 2 | Energy | Physical |
| Moon Girl | Marvel NOW! | Physical | Energy |
| Rhino | Classic | Physical | Energy |
| Rocket Raccoon | Guardians of the Galaxy | Energy | Physical |
| Scorpion | Modern | Physical | Energy |
| Thane | Modern | Physical | Energy |
| Victorious | Modern | HP | Energy |
| Vulture | Classic | Physical | Energy |
| Vulture | Spider-Man: Homecoming | Physical | Energy |

## 3. Instinto

thanosvibs no publica el instinto: la app lo toma del infobox de la wiki. Acá, los personajes cuya página lo contradice en sus categorías.

| Personaje | Infobox (lo que usa la app) | Categoría de la página |
|---|---|---|
| Agent Venom | Cruelty | Justice |
| Kahhori | Order | Justice |
| Marvel Boy | Order | Justice |
| Quasar (Wendell Vaughn) | Order | Justice |

## 4. thanosvibs contra sí mismo

- Retratos marcados Tier-4 sin Striker Skill en sus skills: 6: Red Skull (Captain America: The First Avenger); Red Skull (Hydra Armor); Red Skull (Secret Wars: Red Skull); Sister Grimm (All-New, All-Different); Sister Grimm (Runaways); Sister Grimm (Secret Wars: A-Force)
- Retratos con skill 6 (Tier-3 o Trascendido) sin Definitiva en sus skills: 1: Black Swan (Modern, Tier-3)
- Textos de efecto con marcadores de plantilla sin resolver (`$HEROSUBTYPE`, `$HEROCLASS`, `$TIME`...): 18 patrones, usados por 320 retratos. La facción, el tipo o la raza se completan como dice la sección 8; lo que no, la app lo muestra "sin especificar" en vez de inventar el valor.

## 5. Efectos de líder y soporte: restricciones corregidas

La fuente clasifica mal estas restricciones; el build las corrige con aviso y la ficha muestra la original.

- `thing3` (uniform): la fuente dice Allies "Fantastic Four"; se usa Ability "Los 4 Fantásticos".
- `thing4` (uniform): la fuente dice Allies "Fantastic Four"; se usa Ability "Los 4 Fantásticos".
- `weaponhex1` (uniform2): la fuente dice Type "Zombie"; se usa Ability "Zombi".
- `kang` (leader): la fuente dice Character "Kang"; se usa Character "Kang the Conqueror".
- `kang1` (leader): la fuente dice Character "Kang"; se usa Character "Kang the Conqueror".

## 6. Artefactos

Los números del texto a 6★ de thanosvibs contra la tabla de la página Artifact de la wiki (que los lista a 6★, "Lv.4"). Se listan los números que están en una sola de las dos.

| Personaje | Artefacto | Solo en thanosvibs | Solo en la wiki |
|---|---|---|---|
| Annihilus | Lord of the Negative Zone |  | 300 |
| Captain America (Sharon Rogers) | Spear of Justice | 15, 16 | 50 |
| Captain Marvel | Leader's Flight | 50 |  |
| Daisy Johnson | Skye | 0.2 | 0.5 |
| Daken | Cruel Claws | 50 |  |
| Dazzler | Disco Queen |  | 0.2 |
| Domino | Probability Power | 25 |  |
| Franklin Richards | Pocket Universe | 5, 180 |  |
| Goliath | Giant-Man II |  | 0.1 |
| Morgan le Fay | Dark Knowledge |  | 0.2, 10 |
| Red Skull | Captain Hydra | 0.25, 15, 200 |  |
| Rhino | Charging Horn | 1, 15, 40, 70 | 20 |
| Satana | Painful Temptation | 0.25 | 0.3 |
| Shuri | Blossoming Talent | 25 | 16 |
| Sleeper | Symbiote of Justice | 40 |  |
| Valeria Richards | Inherited Intellect | 0.25 | 0.3, 60 |
| Warpath | Ancestral Rage | 0.5 | 0, 5 |
| Whiplash | Whip of Vengeance |  | 25 |

En 31 la wiki dice listar 6★ pero sus números son exactamente los de otro nivel de estrellas de thanosvibs (no es una contradicción de valores): Ant-Man (Size Shift): 3★; Beta Ray Bill (Champion of Korbin): 3★; Doctor Doom (The Great Destroyer): 3★; Doctor Strange (Multiversal Magic): 3★; Giant-Man (Advances in Science): 3★; Gladiator (Shi'Ar Confidence): 3★; Groot (Strong Roots): 3★; Ikon (Galadorian Gallantry): 3★; Kang the Conqueror (Infinite Identity): 3★; Kraven The Hunter (Hunter's Spear): 3★; Lizard (Reptile Scales): 3★; M.O.D.O.K. (Broken Mind): 3★; Mantis (Power of Emotion): 3★; Mister Sinister (Genetic Mastermind): 3★; Moon Girl (Transcendent Friendship): 3★; Moon Knight (Lunar Fist): 3★; Mysterio (Master Illusionist): 3★; Professor X (Mutant Utopia): 3★; Quasar (Wendell Vaughn) (Quantum Protector): 3★; Quicksilver (Speed Star): 3★; Rocket Raccoon (Bounty Hunter): 3★; Sabretooth (Devil Teeth): 3★; Scorpion (Ever-Changing): 3★; Spider-Man 2099 (Future Warrior): 3★; Spider-Woman (Maternal Love): 3★; Spot (Black and White): 3★; Squirrel Girl (Fated Victory): 3★; Star-Lord (Legendary Hero): 3★; Storm (Regent of Mars): 3★; Victorious (Latverian Loyalist): 3★; Wasp (Rapid Wings): 3★.

Incompletos en thanosvibs (faltan valores en esos niveles de estrellas; la app marca "sin dato"):

- Domino, Probability Power: 3★, 4★, 5★
- Hulkbuster (Iron Man Mark 44), Big Armor: 3★, 4★, 5★, 6★
- Inferno, The Flames of Attilan: 3★, 4★, 5★
- Sunspot, Solar: 3★, 4★, 5★
- Wiccan, Future Demiurge: 3★, 4★, 5★, 6★

## 7. Hallazgos revisados a mano

Lo que no se puede detectar con un chequeo automático (scripts/contenido/hallazgos.json).

- **Rotación de Mr. Knight que nombra a Elsa** — La rotación "Awakened Ready (Hard)" de Moon Knight (uniforme Mr. Knight) dice "cancelá en la rotación normal cuando Elsa hace la voltereta hacia atrás": parece copiada de la de Elsa Bloodstone. Se muestra como viene. ([THANO$VIB$ — Rotations](https://thanosvibs.money/rotations))
- **ISO: "equipables seguros" de la guía** — La guía (parte 3) muestra como piedras que se pueden equipar antes de rolear el set dos Powerful, dos Amplifying, dos Impregnable, dos Absorbing y dos Chaotic. Según la composición de los tres sets de ataque (tabla de la wiki, que coincide con la imagen de la guía), lo que comparten los tres es una de cada una de las cuatro primeras, una Fierce y dos Chaotic: Power of Angry Hulk y Hawk's Eye llevan una sola Powerful y una sola Amplifying, y los tres llevan una Fierce. La app no repite esa lista. ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), [Future Fight Wiki — ISO-8](https://future-fight.fandom.com/wiki/ISO-8))
- **Opción de uniforme Heroic con evasión (PvP)** — Para PvP la guía sugiere evasión en la opción Heroic, pero su propia lista del pool de Heroic no tiene evasión (sí Advanced y Legendary). La app lo muestra con esa advertencia. ([THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Nivel de skills para Tier-4: la guía de thanosvibs dice 12; el juego, 10** — La guía de thanosvibs pone "skills en Nv. 12" en el paso previo al Tier-4. Las skills llegan hasta el Nv. 10: la guía del juego dice que su nivel máximo sube con el del personaje hasta el 10 y pide todas en Nv. 10 para el Tier-4, como la wiki, y Ezequiel lo confirma. La hoja de ruta dice Nv. 10. ([THANO$VIB$ Beginner's Guide, parte 1](https://thanosvibs.money/beginners/1), [Future Fight Wiki — Tier-4](https://future-fight.fandom.com/wiki/Tier-4), MARVEL Future Fight — guía dentro del juego (contenidos y crecimiento, octubre de 2026))
- **Tabla de efectos del artefacto en el sitio de thanosvibs** — En la sección Leads & Supports, el sitio muestra el tercer número de cada efecto de artefacto como duración ("0.2s"), con la columna "Instinct" corrida. Por la página Artifact de la wiki (Robbie Reyes, She-Hulk) ese número es el % adicional del instinto total, la duración va al final y, si el efecto acumula, el tope va antes de la duración. La app los muestra con ese significado. ([THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports), [THANO$VIB$ — Artifacts](https://thanosvibs.money/artifacts))
- **Leads & Supports: reducciones de daño con signo positivo** — En 17 soportes, Leads & Supports publica la reducción de daño recibido con valor positivo: 16 «Basic Damage Received from Villains» y un «Physical Reflect Damage Received» (Black Dwarf, Dwarf Charge). La skill del mismo personaje dice siempre que reduce (Shuri, Panther God's Protection: +40 en Leads & Supports; «Decreases basic damage received from … faction by 40%» en la skill), y en otros soportes el mismo stat viene negativo. El catálogo de efectos los lee siempre como reducción. ([THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **API de skills: «Give Power» sin lo que otorga** — En 27 retratos, la skill trae «Give Power» («Acquires the following effect for … sec.») sin el efecto que sigue, y Leads & Supports dice cuál es: casi siempre «Remove All Debuffs» (Deadpool en Marvel's Savior, Odin, Thanos, Sentry, Blue Dragon, Gorr, Kang, entre otros), y también inmunidad a debuffs (Invisible Woman, First Steps), curación y reducción de daño (Jessica Jones, Jewel), curación (Groot, Bloom) o ataque físico (Toxin). La ficha muestra la skill como viene y el soporte con su efecto. ([THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters), [THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports))
- **API de skills: códigos en lugar de nombres** — Algunas descripciones traen un número donde va el nombre de un efecto o de un elemento, y la app los muestra como vienen: «Natural Enemy» («Increases damage dealt to targets with 206 effect by 50%»), «DURATION INCREASE», «ELEMENT CONVERSION», «Accumulate All True Element Damage Dealt», «REMOVE», «Selective Removal», «DEBUFF EFFECT ↓», «Counter Reflect» y «SET SKILL CD». Los de tres cifras son el id de una habilidad de la misma API (abilityId): 206 es «Removes all Debuffs», 401 «Mockery», 108 «SHOCK», 205 «WEB», 204 «SNARE» y 120 «PIERCE». 407 y 577 no son el id de ninguna habilidad de las skills; Leads & Supports nombra 407 «Debuff Removal (Instinct)» en el soporte de Kahhori (Hero's Decree). Los de cifras sueltas («1234 skill», «pure 23 damage») parecen listas de ranuras o de elementos. La wiki nombra otro: el «REMOVE» del Striker de Spider-Man le quita al rival sus buffs activos. ([THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters), [THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports))
- **C.T.P.: thanosvibs contra el juego** — En el juego, los números de los 15 C.T.P. coinciden con los de thanosvibs en 6★ y en los reforjados Mighty y Brilliant: todos los que muestra cada captura (lo que queda fuera de la parte visible no se pudo ver). El texto difiere: los escudos de Regeneration y Veteran también bloquean el daño de instinto ("Blocks instinct damage"), que thanosvibs no dice; en Judgement, thanosvibs agrega que la baja de resistencias ignora la inmunidad, y el juego no; donde el juego dice "basic damage" (Energy, Destruction, Veteran, Rage), thanosvibs dice "damage"; Ambush (Greed) ignora la reducción de daño del rival ("damage decrease", como dice también el glosario de skills del juego), y thanosvibs dice reducción de defensa; Greed tiene en el juego dos opciones, que cambian qué par de clases recibe primero el aumento de daño, y thanosvibs muestra una. Dentro del juego, el reforjado de Judgement se llama "Type Amplification" y dice subir el daño de las skills "de tipo", pero el glosario lo describe como "Element Amplification", que sube el ataque de las skills con elemento: probablemente un problema de traducción (Judgement es un C.T.P. de elemento). La app muestra el texto de thanosvibs. (MARVEL Future Fight — C.T.P. (Custom Gear, dentro del juego, octubre de 2026), MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), [THANO$VIB$ — C.T.P.s](https://thanosvibs.money/ctps))

## 8. Facción, tipo o raza que la fuente no publica

thanosvibs publica 249 efectos con un marcador (`$HEROSUBTYPE1`, `$HEROCLASS1`) en vez de la facción, el tipo, la raza o la habilidad a la que se refieren (`Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%`). El build los completa con la tabla a mano (scripts/contenido/marcadores.csv) y, lo que no está ahí, con la wiki: la misma skill con el mismo porcentaje, en el mismo sentido (daño infligido o recibido). En la ficha, el valor completado va subrayado y dice de dónde salió.

De los 249: 78 de la wiki, 3 a mano y 168 sin resolver (la app los muestra "sin especificar").

Para completar uno: en scripts/contenido/marcadores.csv, la columna `valor` de su id, escrita como la muestra la app (Superhéroe, Supervillano, Neutral, Combate, Mutante...) o en inglés como la nombra el juego. `python3 scripts/marcadores.py` agrega las filas que falten.

| Personaje | Skill | Efecto | id |
|---|---|---|---|
| Abomination — Infected Bioweapon | Fists of the World Ravager | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1022830012 |
| Abomination — Infected Bioweapon | Fists of the World Ravager | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1022830013 |
| Agent Venom — Agent Anti-Venom | Agent Anti-Venom | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.` | 1012150011 |
| Amadeus Cho — Heroic Age | Heroic Age | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1006857011 |
| Angela — Asgard's Assassin | Asgard's Assassin | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1003928011 |
| Angela — Secret Wars: 1602 Witch Hunter Angela | Secret Wars: 1602 Witch Hunter Angela | `Increases basic damage dealt to $HEROCLASS1 types by 20%.` | 1003950011 |
| Athena | Righteous Wisdom | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1028604011 |
| Beta Ray Bill — Beta Ray Bill | Beta Ray Bill | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 35%.` | 1022247011 |
| Captain America (Sam Wilson) — Marvel Studios' Captain America: Brave New World | New Captain America | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1203012012 |
| Captain Marvel — Marvel Animation's Marvel Zombies | Marvel Animation's Marvel Zombies | `Increases basic damage by 55% when attacking characters without $HEROSUBTYPE1 Ability.` | 1202629012 |
| Captain Marvel — Marvel Studios' Avengers: Endgame | Marvel Studios' Avengers: Endgame | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.` | 1002654012 |
| Captain Marvel — Marvel Studios' Avengers: Endgame | Marvel Studios' Avengers: Endgame | `Decreases basic damage received from $HEROSUBTYPE1 faction by 10%.` | 1002654013 |
| Captain Marvel — Marvel Studios' The Marvels | Marvel Studios' The Marvels | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.` | 1202608012 |
| Captain Marvel — Marvel Studios' The Marvels | Marvel Studios' The Marvels | `Decreases basic damage received from $HEROSUBTYPE1 faction by 50%.` | 1202608013 |
| Colossus / Colossus — X-Force | Piotr’s Will | `Decreases basic damage received from $HEROSUBTYPE1 faction by 50%.` | 1015814011 |
| Colossus — Hellfire Gala | Piotr’s Will | `Decreases basic damage received from $HEROSUBTYPE1 faction by 50%.` | 1015883011 |
| Colossus — Hellfire Gala | Piotr’s Will | `Decreases basic damage received from $HEROSUBTYPE1 faction by 50%.` | 1015883013 |
| Colossus — Phoenix Five | Piotr’s Will | `Decreases basic damage received from $HEROSUBTYPE1 faction by 50%.` | 1015834011 |
| Colossus — Phoenix Five | Piotr’s Will | `Decreases basic damage received from $HEROSUBTYPE1 faction by 50%.` | 1015834013 |
| Deathlok / Deathlok — Modern | Centipede Serum | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 50%.` | 1005804011 |
| Deathlok / Deathlok — Modern | Centipede Serum | `Decreases basic damage received from enemies with $HEROSUBTYPE1 ability by 50%.` | 1005804012 |
| Doctor Voodoo — Savage Avengers | Savage Avengers | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1020441011 |
| Doctor Voodoo — Savage Avengers | Savage Avengers | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1020441012 |
| Dormammu — Damnation | Dread One | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1011631061 |
| Drax — Annihilation | Annihilation | `Decreases basic damage received from $HEROSUBTYPE1 faction by 60%.` | 1002239012 |
| Drax — Annihilation | Annihilation | `Decreases basic damage received from $HEROSUBTYPE1 faction by 60%.` | 1002239013 |
| Ebony Maw — Dark Obsidian Armor | Evil Persuasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1007771012 |
| Ebony Maw — Dark Obsidian Armor | Evil Persuasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1007771013 |
| Ebony Maw — General's Hand | Evil Persuasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1007760012 |
| Ebony Maw — General's Hand | Evil Persuasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1007760013 |
| Ebony Maw — General's Hand | General's Hand | `Increases basic damage dealt to $HEROCLASS1 types by 40%.` | 1007761011 |
| Ebony Maw — General's Hand | General's Hand | `Decreases basic damage received from $HEROCLASS1 types by 35%.` | 1007761012 |
| Electro — Spider-Man: No Way Home | Electric Battlefield | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1019733011 |
| Electro — Spider-Man: No Way Home | Electric Battlefield | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1019733012 |
| Falcon / Falcon — All-New Captain America / Falcon — Marvel Studios' Captain America: Civil War / Falcon — Marvel Legacy / Captain America (Sam Wilson) — Marvel Studios' The Falcon and the Winter Soldier / Falcon — What If... Zombies?! / Captain America (Sam Wilson) — Marvel Studios' Captain America: Brave New World | Hero's Rise | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 70%.` | 1003080013 |
| Falcon (Joaquin Torres) | Captain's Wingman | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1027770011 |
| Falcon — What If... Zombies?! | Hero Meat.. Villain Meat.. | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1003091011 |
| Falcon — What If... Zombies?! | Hero Meat.. Villain Meat.. | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1003091012 |
| Gamora — Requiem / Gamora — Marvel Studios' Guardians of the Galaxy 3 | Cosmic Enforcer | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1001247012 |
| Gamora — Requiem / Gamora — Marvel Studios' Guardians of the Galaxy 3 | Cosmic Enforcer | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1001247013 |
| Gamora — Wastelanders | Cosmic Enforcer | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1001297012 |
| Gamora — Wastelanders | Cosmic Enforcer | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1001297013 |
| Ghost Rider / Ghost Rider — 70's Classic / Ghost Rider — Inhumans: Attilan Rising | Repentance | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1000470011 |
| Ghost Rider (Robbie Reyes) — Lord of Vengeance | Lord of Vengeance | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1011750012 |
| Ghost Rider (Robbie Reyes) — Lord of Vengeance | Lord of Vengeance | `Decreases basic damage received from $HEROSUBTYPE1 faction by 70%.` | 1011750013 |
| Ghost Rider — King of Hell | Repentance | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1000471011 |
| Ghost Rider — Rage Returned / Ghost Rider — Savage Avengers | Hell's Wrath | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1000443011 |
| Gorgon | War Cry | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.` | 1011203062 |
| Green Goblin — Dark Avengers | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1001844011 |
| Green Goblin — Dark Avengers | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1001844012 |
| Green Goblin — Gold Goblin | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1201811011 |
| Green Goblin — Gold Goblin | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1201811012 |
| Green Goblin — Red Goblin | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1001886011 |
| Green Goblin — Red Goblin | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1001886012 |
| Green Goblin — Spider-Man: No Way Home | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1001864011 |
| Green Goblin — Spider-Man: No Way Home | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1001864012 |
| Hela — Asgard Invasion | Asgard Invasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1010639011 |
| Hela — Asgard Invasion | Asgard Invasion | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1010639012 |
| Hela — Marvel Studios' Thor: Ragnarok | Marvel Studios' Thor: Ragnarok | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.` | 1010650011 |
| Hela — Marvel Studios' Thor: Ragnarok | Marvel Studios' Thor: Ragnarok | `Decreases basic damage received from $HEROSUBTYPE1 faction by 15%.` | 1010650012 |
| Hela — Marvel Studios' What If...? | Marvel Studios' What If...? | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1010676011 |
| Hela — Marvel Studios' What If...? | Marvel Studios' What If...? | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1010676012 |
| Infinity Ultron — Marvel Studios' What If...? | Marvel Studios' What If...? | `Increases basic damage by 40% when attacking characters without $HEROSUBTYPE1 Ability.` | 1001331012 |
| Iron Man — Marvel Studios' Avengers: Endgame / Iron Man — Team Suit | Overdrive Beam | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1000372102 |
| Jubilee — Marvel Animation's X-Men '97 | The Light of the X-Men | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 35%.` | 1019417011 |
| Jubilee — Marvel Animation's X-Men '97 | The Light of the X-Men | `Decreases basic damage received from $HEROSUBTYPE1 faction by 45%.` | 1019417012 |
| Jubilee — Marvel Animation's X-Men '97 | The Light of the X-Men | `Decreases basic damage received from $HEROSUBTYPE1 faction by 45%.` | 1019417013 |
| Kraven The Hunter — Interdimensional Hunter | Interdimensional Hunter | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 35%.` | 1013233011 |
| Kraven The Hunter — Interdimensional Hunter | Interdimensional Hunter | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 35%.` | 1013233012 |
| Leader | Evil Leadership | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1027604011 |
| Leader | Evil Leadership | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1027604012 |
| Loki — Young Avengers | The Young Avengers' Clever One | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1201424011 |
| Magneto — Marvel NOW! | Marvel NOW! | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 45%.` | 1012950011 |
| Malekith / Malekith — All-New, All-Different | Malicious Manipulation | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1002008011 |
| Malekith / Malekith — All-New, All-Different | Malicious Manipulation | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1002008012 |
| Malekith — War of the Realms | Dark Blessing | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1002036011 |
| Maximus | Mad Scientist | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 50%.` | 1011504012 |
| Medusa — Ancient Curse | Ancient Curse | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1010942011 |
| Medusa — Inhumans vs X-Men | Queenly Gaze | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1010940011 |
| Mephisto | Rage of the Pit | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%. Effect cannot be removed.` | 1024470012 |
| Mephisto — Master of Hell | Hell Fire | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%. Effect cannot be removed.` | 1224401102 |
| Mephisto — Master of Hell | Rage of the Pit | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%. Effect cannot be removed.` | 1024493012 |
| Molten Man | Fire Eater | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 30%.` | 1019504012 |
| Morph | Gender Equality | `Increases basic damage dealt to $HEROSUBTYPE1 types by 40%.` | 1029170011 |
| Morph | Gender Equality | `Increases basic damage dealt to $HEROSUBTYPE1 types by 40%.` | 1029170012 |
| Mystique | Perfect Deception | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1021870011 |
| Mystique | Perfect Deception | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1021870012 |
| Mystique — Hellfire Gala | Perfect Deception | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1021844011 |
| Mystique — Hellfire Gala | Perfect Deception | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1021844012 |
| Nick Fury — Marvel Studios' Captain Marvel / Nick Fury — Marvel Studios' The Marvels | Director of S.H.I.E.L.D. | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.` | 1018571011 |
| Nick Fury — Secret Avengers | Director of S.H.I.E.L.D. | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1018563011 |
| Nova (Richard Rider) — Marvel Cosmic Invasion | Worldmind Knowledge | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1022550011 |
| Phil Coulson — Winter Ops | Director's Orders | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1006114012 |
| Phil Coulson — Winter Ops | Director's Orders | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1006114013 |
| Proxima Midnight — Dark Obsidian Armor | Dark Obsidian Armor | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1006951012 |
| Punisher — Cosmic Ghost Rider | Cosmic Ghost Rider | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1003243012 |
| Punisher — Cosmic Ghost Rider | Cosmic Ghost Rider | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1003243013 |
| Punisher — Fist of the Beast | Fist of the Beast | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1003288011 |
| Punisher — Marvel Television's Daredevil: Born Again | Marvel Television's Daredevil: Born Again | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1203209011 |
| Red Hulk — Marvel Studios' Captain America: Brave New World | Marvel Studios' Captain America: Brave New World | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1002558012 |
| Red Skull / Red Skull — Secret Wars: Red Skull | Hero Hunter | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1001506011 |
| Red Skull / Red Skull — Secret Wars: Red Skull | Hero Hunter | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1001506012 |
| Red Skull — Hydra Armor | Hero Hunter | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1001571011 |
| Red Skull — Hydra Armor | Hero Hunter | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1001571012 |
| Red Skull — The Crimson Fall | Age of Malice | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.` | 1001545011 |
| Red Skull — The Crimson Fall | Age of Malice | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.` | 1001545012 |
| Ronan — Annihilators | Annihilators | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1004861011 |
| Ronan — Annihilators | Annihilators | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1004861012 |
| Ronan — Marvel Studios' Captain Marvel | Marvel Studios' Captain Marvel | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1004851011 |
| Scarlet Spider — Gift Deliverer | Good Guy, Bad Guy | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1023167012 |
| Scarlet Spider — Gift Deliverer | Good Guy, Bad Guy | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 35%.` | 1023167013 |
| Sentinel — Stark Sentinels Mk II | Mutant Suppressor | `Increases basic damage dealt to $HEROSUBTYPE1 characters by 100%.` | 1017563012 |
| Sentinel — Stark Sentinels Mk II | Mutant Suppressor | `Decreases basic damage received from $HEROSUBTYPE1 characters by 60%.` | 1017563013 |
| Sersi — Marvel Studios' Eternals | Cosmic Focus | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1024324012 |
| Sersi — Marvel Studios' Eternals | Cosmic Focus | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1024324013 |
| Sleeper | Symbiote Heroes | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 35%.` | 1027522011 |
| Sleeper | Symbiote Heroes | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1027522012 |
| Spider-Man (Miles Morales) / Spider-Man (Miles Morales) — Into the Spider-Verse | Ultimate Spider-Man | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1006570011 |
| Spider-Man (Miles Morales) — Absolute Carnage | Ultimate Spider-Man | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1006571011 |
| Spider-Man (Miles Morales) — Ancient Curse | Ancient Curse | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1206529011 |
| Spider-Man (Miles Morales) — Spider-Man: Across the Spider-Verse | Spider-Man: Across the Spider-Verse | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1206502011 |
| Spider-Man 2099 — All-New, All-Different | All-New, All-Different | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 10%.` | 1013635011 |
| Taskmaster — Marvel Studios' Black Widow | Marvel Studios' Black Widow | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1021650011 |
| Taskmaster — Marvel Studios' Black Widow | Marvel Studios' Black Widow | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1021650012 |
| Taskmaster — Marvel Studios' Thunderbolts* | Marvel Studios' Thunderbolts* | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1021691011 |
| Taskmaster — Marvel Studios' Thunderbolts* | Marvel Studios' Thunderbolts* | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1021691012 |
| Thanos — Obsidian King | Mad Titan | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1007590011 |
| Thanos — Thanos Wins / Thanos — Annihilation | Hero Slayer | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1207527011 |
| Thanos — Wise Harvester | True Peace | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1207502011 |
| Thanos — Wise Harvester | True Peace | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 20%.` | 1207502012 |
| The Thing — Marvel Studios' The Fantastic Four: First Steps | Family Man | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 35%.` | 201820901 |
| Thor (Jane Foster) — Marvel Studios' Thor: Love and Thunder | Marvel Studios' Thor: Love and Thunder | `Decreases basic damage received from $HEROSUBTYPE1 faction by 35%.` | 1007150012 |
| Ulik | Troll's Roar | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1009803062 |
| Ultron Mark 1 — Avengers: Age of Ultron | Avengers: Age of Ultron | `Decreases basic damage received from $HEROCLASS1 types by 10%.` | 1001351011 |
| Ultron Mark 1 — Avengers: Age of Ultron | Avengers: Age of Ultron | `Increases basic damage dealt to $HEROCLASS1 types by 10%.` | 1001351012 |
| Ultron Mark 3 — Avengers: Age of Ultron | Avengers: Age of Ultron | `Decreases basic damage received from $HEROCLASS1 types by 10%.` | 1001352011 |
| Ultron Mark 3 — Avengers: Age of Ultron | Avengers: Age of Ultron | `Increases basic damage dealt to $HEROCLASS1 types by 10%.` | 1001352012 |
| Ultron Prime — Avengers: Age of Ultron | Avengers: Age of Ultron | `Decreases basic damage received from $HEROCLASS1 types by 10%.` | 1001350011 |
| Ultron Prime — Avengers: Age of Ultron | Avengers: Age of Ultron | `Increases basic damage dealt to $HEROCLASS1 types by 10%.` | 1001350012 |
| Ultron — All-Father Ultron | All-Father Ultron | `Increases basic damage by 40% when attacking characters without $HEROSUBTYPE1 Ability.` | 1001363012 |
| Valkyrie | Shield Maiden of Asgard | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1014470011 |
| Valkyrie | Shield Maiden of Asgard | `Decreases basic damage received from $HEROSUBTYPE1 faction by 15%.` | 1014470012 |
| Valkyrie — Asgardians of the Galaxy | Shield Maiden of Asgard | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1014486011 |
| Valkyrie — Asgardians of the Galaxy | Shield Maiden of Asgard | `Decreases basic damage received from $HEROSUBTYPE1 faction by 25%.` | 1014486012 |
| Valkyrie — Fearless Defenders | Shield Maiden of Asgard | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1014446011 |
| Valkyrie — Fearless Defenders | Shield Maiden of Asgard | `Decreases basic damage received from $HEROSUBTYPE1 faction by 25%.` | 1014446012 |
| Valkyrie — Marvel Studios' Thor: Love and Thunder | Shield Maiden of Asgard | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.` | 1014448011 |
| Valkyrie — Marvel Studios' Thor: Love and Thunder | Shield Maiden of Asgard | `Decreases basic damage received from $HEROSUBTYPE1 faction by 25%.` | 1014448012 |
| Venus (Aphrodite) | Olympian Hymn | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1028770011 |
| Venus (Aphrodite) | Olympian Hymn | `Decreases basic damage received from $HEROSUBTYPE1 faction by 35%.` | 1028770012 |
| Vulture — Spider-Man: Homecoming | Spider-Man: Homecoming | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1013550011 |
| War Machine — Invincible Iron Man | Machine Army | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1002794011 |
| War Machine — Invincible Iron Man | Machine Army | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 40%.` | 1002794012 |
| Wave — Classic | Wrath of the Waves | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1020071011 |
| Weapon Hex — Infected Bioweapon | Infected Bioweapon | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1017248011 |
| Weapon Hex — Infected Bioweapon | Infected Bioweapon | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1017248012 |
| Whiplash | Mechanical Engineering | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 80%.` | 1012204011 |
| White Fox / White Fox — Lifestyle Series 1 | Kumiho Stance | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1017870011 |
| White Fox — Agent F-One | Villain Specialist | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 65%.` | 1017854011 |
| White Fox — Agent F-One | Villain Specialist | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1017854012 |
| White Fox — Lifestyle Series 2 | Kumiho Stance | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 65%.` | 1017871011 |
| White Fox — Lifestyle Series 2 | Kumiho Stance | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1017871012 |
| Wong — Marvel Studios' Doctor Strange 2 | Mystic Advancement | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 53%.` | 1009222011 |
| Wong — Marvel Studios' Doctor Strange 2 | Mystic Advancement | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 53%.` | 1009222012 |
| Wong — What If... Zombies?! | Mystic Advancement | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 53%.` | 1009279011 |
| Wong — What If... Zombies?! | Mystic Advancement | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 53%.` | 1009279012 |
| Yellowjacket — Marvel NOW! | Marvel NOW! | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1005250011 |
| Yondu — Summer Vacation | Exploit | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1004652011 |

## 9. Efectos que el catálogo no clasifica

Cada etiqueta de efecto de las skills y cada stat de Leads & Supports apunta a efectos del catálogo (scripts/contenido/catalogo.json; docs/CATALOGO.md lo muestra entero). Lo que thanosvibs agregue y el catálogo no tenga se lista acá hasta que se clasifique a mano.

Ninguno: todo lo que traen los datos está clasificado.
