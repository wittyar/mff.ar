# Auditoría de datos

Generado por `scripts/auditar.py` el 2026-10-03, sobre los datos del juego 12.2.5 (thanosvibs) y la wiki de Future Fight bajada en la misma sincronización.

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
| Bonos de equipo (las páginas de la wiki entre sí) | 1588 | 43 por mayoría, 49 empatados | 25 páginas sin la sección |
| Strikers (pestaña Striker de la wiki) | 7020 filas en 171 páginas | 2 filas que no se pudieron leer | 119 páginas sin la pestaña |
| Artefactos a 6★ (thanosvibs vs wiki) | 209 (+31 donde la wiki lista otro nivel de estrellas) | 17 | 10 sin fila en la wiki; 5 con niveles incompletos en thanosvibs |

Cobertura de la wiki: de 5887 skills (activas, Definitiva y Striker) de thanosvibs, 2270 (39%) se pudieron comparar; 1222 están en la página pero solo en la sección de otro uniforme, y el resto no aparece (sobre todo uniformes que la wiki no documenta). Infobox: 552 retratos con pestaña en la wiki, 305 sin pestaña de su uniforme y 31 de personajes sin infobox legible.

Catálogo de efectos (docs/CATALOGO.md): 228 etiquetas de skills y 72 stats de Leads & Supports en los datos; todos clasificados.

Liderazgos: 5 uniformes que Leads & Supports no lista tienen el de su base, porque su Leader Skill es idéntica; 58 retratos siguen sin liderazgo aunque una hermana lo tiene (sección 12).

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
- **C.T.P.: thanosvibs contra el juego** — En el juego, los números de los 15 C.T.P. coinciden con los de thanosvibs en 6★ y en los reforjados Mighty y Brilliant: todos los que muestra cada captura (lo que queda fuera de la parte visible no se pudo ver). El texto difiere: los escudos de Regeneration y Veteran también bloquean el daño de instinto ("Blocks instinct damage"), que thanosvibs no dice; en Judgement, thanosvibs agrega que la baja de resistencias ignora la inmunidad, y el juego no; donde el juego dice "basic damage" (Energy, Destruction, Veteran, Rage), thanosvibs dice "damage"; Ambush (Greed) ignora la reducción de daño del rival ("damage decrease", como dice también el glosario de skills del juego), y thanosvibs dice reducción de defensa; Greed tiene en el juego dos opciones, que cambian qué par de clases recibe primero el aumento de daño, y thanosvibs muestra una. Dentro del juego, el reforjado de Judgement se llama "Type Amplification" y dice subir el daño de las skills "de tipo", pero el glosario lo describe como "Element Amplification", que sube el ataque de las skills con elemento, y el glosario en coreano lo llama 속성 증폭 (amplificación de elemento): es un problema de traducción del inglés (Judgement es un C.T.P. de elemento). La app muestra el texto de thanosvibs. (MARVEL Future Fight — C.T.P. (Custom Gear, dentro del juego, octubre de 2026), MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026), [THANO$VIB$ — C.T.P.s](https://thanosvibs.money/ctps))

## 8. Facción, tipo o raza que la fuente no publica

thanosvibs publica 249 efectos con un marcador (`$HEROSUBTYPE1`, `$HEROCLASS1`) en vez de la facción, el tipo, la raza o la habilidad a la que se refieren (`Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%`). El build los completa en este orden (Ezequiel, 3 de octubre de 2026): la tabla a mano (scripts/contenido/marcadores.csv); Leads & Supports, en los slots de la misma skill (Leader Skill: `leader` y `leader2`; Passive: `passive` y `passive2`; Tier-2 Passive: `t2` y `t22`; Uniform Passive: `uniform` y `uniform2`), con «Basic Damage Dealt to …» o «Basic Damage Received from …» en el mismo sentido, el mismo porcentaje (el recibido, sin el signo) y un grupo de la clase que pide el texto, y la wiki: la misma skill con el mismo porcentaje, en el mismo sentido (daño infligido o recibido). Si la skill trae el mismo efecto varias veces, la fuente tiene que dar tantos valores distintos como efectos, y se asignan en el orden en que aparecen. En la ficha, el valor completado va subrayado y dice de dónde salió.

De los 249: 3 a mano, 131 de Leads & Supports, 38 de la wiki y 77 sin resolver (la app los muestra "sin especificar").

- **Valores de Leads & Supports distintos de la wiki (gana Leads & Supports):** 1022870012, 1022870013

Para completar uno: en scripts/contenido/marcadores.csv, la columna `valor` de su id, escrita como la muestra la app (Superhéroe, Supervillano, Neutral, Combate, Mutante...) o en inglés como la nombra el juego. `python3 scripts/marcadores.py` agrega las filas que falten.

| Personaje | Skill | Efecto | id |
|---|---|---|---|
| Agent Venom — Agent Anti-Venom | Agent Anti-Venom | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.` | 1012150011 |
| Angela — Secret Wars: 1602 Witch Hunter Angela | Secret Wars: 1602 Witch Hunter Angela | `Increases basic damage dealt to $HEROCLASS1 types by 20%.` | 1003950011 |
| Captain America (Sam Wilson) — Marvel Studios' Captain America: Brave New World | New Captain America | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1203012012 |
| Captain Marvel — Marvel Animation's Marvel Zombies | Marvel Animation's Marvel Zombies | `Increases basic damage by 55% when attacking characters without $HEROSUBTYPE1 Ability.` | 1202629012 |
| Captain Marvel — Marvel Studios' Avengers: Endgame | Marvel Studios' Avengers: Endgame | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 15%.` | 1002654012 |
| Captain Marvel — Marvel Studios' Avengers: Endgame | Marvel Studios' Avengers: Endgame | `Decreases basic damage received from $HEROSUBTYPE1 faction by 10%.` | 1002654013 |
| Captain Marvel — Marvel Studios' The Marvels | Marvel Studios' The Marvels | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.` | 1202608012 |
| Captain Marvel — Marvel Studios' The Marvels | Marvel Studios' The Marvels | `Decreases basic damage received from $HEROSUBTYPE1 faction by 50%.` | 1202608013 |
| Deathlok / Deathlok — Modern | Centipede Serum | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 50%.` | 1005804011 |
| Deathlok / Deathlok — Modern | Centipede Serum | `Decreases basic damage received from enemies with $HEROSUBTYPE1 ability by 50%.` | 1005804012 |
| Drax — Annihilation | Annihilation | `Decreases basic damage received from $HEROSUBTYPE1 faction by 60%.` | 1002239012 |
| Drax — Annihilation | Annihilation | `Decreases basic damage received from $HEROSUBTYPE1 faction by 60%.` | 1002239013 |
| Ebony Maw — Dark Obsidian Armor | Evil Persuasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1007771012 |
| Ebony Maw — Dark Obsidian Armor | Evil Persuasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1007771013 |
| Ebony Maw — General's Hand | Evil Persuasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1007760012 |
| Ebony Maw — General's Hand | Evil Persuasion | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1007760013 |
| Electro — Spider-Man: No Way Home | Electric Battlefield | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1019733011 |
| Electro — Spider-Man: No Way Home | Electric Battlefield | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1019733012 |
| Falcon / Falcon — All-New Captain America / Falcon — Marvel Studios' Captain America: Civil War / Falcon — Marvel Legacy / Captain America (Sam Wilson) — Marvel Studios' The Falcon and the Winter Soldier / Falcon — What If... Zombies?! / Captain America (Sam Wilson) — Marvel Studios' Captain America: Brave New World | Hero's Rise | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 70%.` | 1003080013 |
| Falcon (Joaquin Torres) | Captain's Wingman | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.` | 1027770011 |
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
| Green Goblin — Gold Goblin | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1201811011 |
| Green Goblin — Gold Goblin | OZ Formula | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 45%.` | 1201811012 |
| Infinity Ultron — Marvel Studios' What If...? | Marvel Studios' What If...? | `Increases basic damage by 40% when attacking characters without $HEROSUBTYPE1 Ability.` | 1001331012 |
| Iron Man — Marvel Studios' Avengers: Endgame / Iron Man — Team Suit | Overdrive Beam | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1000372102 |
| Magneto — Marvel NOW! | Marvel NOW! | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 45%.` | 1012950011 |
| Malekith / Malekith — All-New, All-Different | Malicious Manipulation | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1002008011 |
| Malekith / Malekith — All-New, All-Different | Malicious Manipulation | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1002008012 |
| Malekith — War of the Realms | Dark Blessing | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1002036011 |
| Maximus | Mad Scientist | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 50%.` | 1011504012 |
| Mephisto | Rage of the Pit | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%. Effect cannot be removed.` | 1024470012 |
| Mephisto — Master of Hell | Hell Fire | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%. Effect cannot be removed.` | 1224401102 |
| Mephisto — Master of Hell | Rage of the Pit | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%. Effect cannot be removed.` | 1024493012 |
| Molten Man | Fire Eater | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 30%.` | 1019504012 |
| Punisher — Cosmic Ghost Rider | Cosmic Ghost Rider | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1003243012 |
| Punisher — Cosmic Ghost Rider | Cosmic Ghost Rider | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1003243013 |
| Punisher — Fist of the Beast | Fist of the Beast | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1003288011 |
| Punisher — Marvel Television's Daredevil: Born Again | Marvel Television's Daredevil: Born Again | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 50%.` | 1203209011 |
| Red Skull / Red Skull — Secret Wars: Red Skull | Hero Hunter | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1001506011 |
| Red Skull / Red Skull — Secret Wars: Red Skull | Hero Hunter | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1001506012 |
| Red Skull — Hydra Armor | Hero Hunter | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1001571011 |
| Red Skull — Hydra Armor | Hero Hunter | `Decreases basic damage received from $HEROSUBTYPE1 faction by 20%.` | 1001571012 |
| Red Skull — The Crimson Fall | Age of Malice | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.` | 1001545011 |
| Red Skull — The Crimson Fall | Age of Malice | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 55%.` | 1001545012 |
| Ronan — Marvel Studios' Captain Marvel | Marvel Studios' Captain Marvel | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1004851011 |
| Sentinel — Stark Sentinels Mk II | Mutant Suppressor | `Increases basic damage dealt to $HEROSUBTYPE1 characters by 100%.` | 1017563012 |
| Sentinel — Stark Sentinels Mk II | Mutant Suppressor | `Decreases basic damage received from $HEROSUBTYPE1 characters by 60%.` | 1017563013 |
| Spider-Man (Miles Morales) / Spider-Man (Miles Morales) — Into the Spider-Verse | Ultimate Spider-Man | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1006570011 |
| Spider-Man (Miles Morales) — Absolute Carnage | Ultimate Spider-Man | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 120%.` | 1006571011 |
| Spider-Man (Miles Morales) — Ancient Curse | Ancient Curse | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1206529011 |
| Spider-Man (Miles Morales) — Spider-Man: Across the Spider-Verse | Spider-Man: Across the Spider-Verse | `Decreases basic damage received from $HEROSUBTYPE1 faction by 30%.` | 1206502011 |
| Spider-Man 2099 — All-New, All-Different | All-New, All-Different | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 10%.` | 1013635011 |
| Thanos — Obsidian King | Mad Titan | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1007590011 |
| Thanos — Thanos Wins / Thanos — Annihilation | Hero Slayer | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1207527011 |
| Thanos — Wise Harvester | True Peace | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1207502011 |
| Thanos — Wise Harvester | True Peace | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 20%.` | 1207502012 |
| Thor (Jane Foster) — Marvel Studios' Thor: Love and Thunder | Marvel Studios' Thor: Love and Thunder | `Decreases basic damage received from $HEROSUBTYPE1 faction by 35%.` | 1007150012 |
| Ulik | Troll's Roar | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%.` | 1009803062 |
| Ultron Mark 1 — Avengers: Age of Ultron | Avengers: Age of Ultron | `Decreases basic damage received from $HEROCLASS1 types by 10%.` | 1001351011 |
| Ultron Mark 1 — Avengers: Age of Ultron | Avengers: Age of Ultron | `Increases basic damage dealt to $HEROCLASS1 types by 10%.` | 1001351012 |
| Ultron Mark 3 — Avengers: Age of Ultron | Avengers: Age of Ultron | `Decreases basic damage received from $HEROCLASS1 types by 10%.` | 1001352011 |
| Ultron Mark 3 — Avengers: Age of Ultron | Avengers: Age of Ultron | `Increases basic damage dealt to $HEROCLASS1 types by 10%.` | 1001352012 |
| Ultron Prime — Avengers: Age of Ultron | Avengers: Age of Ultron | `Decreases basic damage received from $HEROCLASS1 types by 10%.` | 1001350011 |
| Ultron Prime — Avengers: Age of Ultron | Avengers: Age of Ultron | `Increases basic damage dealt to $HEROCLASS1 types by 10%.` | 1001350012 |
| Ultron — All-Father Ultron | All-Father Ultron | `Increases basic damage by 40% when attacking characters without $HEROSUBTYPE1 Ability.` | 1001363012 |
| Vulture — Spider-Man: Homecoming | Spider-Man: Homecoming | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1013550011 |
| Whiplash | Mechanical Engineering | `Increases basic damage dealt to enemies with $HEROSUBTYPE1 ability by 80%.` | 1012204011 |
| Yellowjacket — Marvel NOW! | Marvel NOW! | `Increases basic damage dealt to $HEROSUBTYPE1 faction by 25%.` | 1005250011 |

## 9. Efectos que el catálogo no clasifica

Cada etiqueta de efecto de las skills y cada stat de Leads & Supports apunta a efectos del catálogo (scripts/contenido/catalogo.json; docs/CATALOGO.md lo muestra entero). Lo que thanosvibs agregue y el catálogo no tenga se lista acá hasta que se clasifique a mano.

Ninguno: todo lo que traen los datos está clasificado.

## 10. Bonos de equipo: la wiki contra sí misma

thanosvibs no publica los bonos de equipo. La app los toma de la sección Team Bonus de la página de cada personaje en la wiki (265 páginas la tienen) y de lo que se vio en el juego (scripts/contenido/bonos.json), que manda sobre la wiki. Un bono aparece en la página de cada integrante: valen el nombre y los stats que dice la mayoría de sus páginas, y si empatan la app muestra todas las versiones empatadas. La wiki redondea los valores a un decimal (scripts/bonos.py).

1683 bonos: 938 de dos integrantes y 745 de tres; 3 del juego (MARVEL Future Fight — Team Bonus (dentro del juego, octubre de 2026)).

Personajes sin la sección en su página (25): Absorbing Man, Annihilus, Athena, Black Knight, Black Swan, Cassandra Nova, Falcon (Joaquin Torres), Galactus, Havok, Hope Summers, Ikon, Kahhori, Leader, Madelyne Pryor, Man-Thing, Marvel Boy, Morph, Okoye, Omega Red, Silver Surfer (Shalla-Bal), Sleeper, Sunspot, Sylvie, The Hood, Valeria Richards. Sus bonos están solo si la página de otro integrante los lista.

### Del juego (3)

| Bono | Integrantes | La wiki decía |
|---|---|---|
| Galactus Abducted | Annihilus, Galactus, Thanos | no lo tiene |
| Battle for the Cosmic Control Rod #2 | Annihilus, Human Torch, The Thing | no lo tiene |
| Invasion of the Devourer #2 | Galactus, Human Torch, The Thing | no lo tiene |

### Versiones empatadas (49)

Ninguna versión tiene más páginas: la app las muestra todas.

| Integrantes | Versiones (páginas que dicen cada una) |
|---|---|
| Ancient One, Baron Mordo | Energy Attack +5.3%, Skill Cooldown −4.9% (Ancient One) — Attack Speed +4.9%, Movement Speed +4.9% (Baron Mordo) |
| Angel, Apocalypse | HP +5.4%, Critical Damage +4.8% (Angel) — All Basic Attacks +5.4%, Critical Damage +4.8% (Apocalypse) |
| Angel, X-23 | Physical Attack +5.1%, Critical Damage +4.8% (Angel) — Critical Damage +5%, Energy Defense +5% (X-23) |
| Angela, Blade | All Basic Attacks +5.4%, Attack Speed +5.1%, Critical Rate +4.3% (Angela) — All Basic Attacks +5.4%, Attack Speed +5.1%, Critical Damage +4.3% (Blade) |
| Arachknight, Moon Knight | Dodge +5%, Critical Rate +4.9% (Arachknight) — Critical Rate +5.1%, Critical Damage +4.8% (Moon Knight) |
| Arachknight, Spider-Man | Critical Rate +5.1%, Critical Damage +4.8% (Arachknight) — Dodge +5%, Critical Rate +4.9% (Spider-Man) |
| Baron Mordo, Kaecilius | HP +5.2%, Critical Rate +5% (Baron Mordo) — HP +5.2%, Critical Damage +4.8% (Kaecilius) |
| Beast, Wolverine | All Basic Attacks +5.1%, All Basic Defenses +5.3% (Beast) — All Basic Attacks +5.3%, All Basic Defenses +5.3% (Wolverine) |
| Black Bolt, Black Panther | All Basic Attacks +5%, HP +5.5% (Black Bolt) — All Basic Attacks +4.8%, HP +5.5% (Black Panther) |
| Black Bolt, Songbird | Movement Speed +5.5%, Recovery Rate +4.8% (Black Bolt) — Movement Speed +4.9%, Recovery Rate +4.8% (Songbird) |
| Black Cat, Gwenpool | All Basic Attacks +4.8%, Attack Speed +4.6% (Black Cat) — Movement Speed +4.9%, Attack Speed +4.8% (Gwenpool) |
| Black Cat, Silk | HP +4.7%, Dodge +4.6% (Black Cat) — All Basic Attacks +5.2%, Ignore Defense +4.8% (Silk) |
| Black Cat, Spider-Man | All Basic Attacks +4.8%, Critical Damage +4.7% (Black Cat) — All Basic Attacks +5.2%, Dodge +4.9% (Spider-Man) |
| Black Dwarf, Shang-Chi | Physical Defense +5.4%, Skill Cooldown −4.8% (Black Dwarf) — Attack Speed +4.9%, Physical Attack +5.1% (Shang-Chi) |
| Black Widow, Captain America | Movement Speed +4.9%, Crowd Control Time −4.8% (Black Widow) — Movement Speed +5.2%, Crowd Control Time −5.1% (Captain America) |
| Black Widow, Winter Soldier | Critical Rate +5%, HP +4.9% (Black Widow) — Critical Rate +4.9%, HP +5% (Winter Soldier) |
| Bullseye, Crossbones | Attack Speed +4.9%, Dodge +4.7% (Bullseye) — Attack Speed +4.9%, Dodge +4.8% (Crossbones) |
| Captain America, Crossbones | All Basic Defenses +5.2%, Critical Damage +4.9% (Captain America) — All Basic Defenses +5.3%, Critical Damage +4.9% (Crossbones) |
| Captain America, X-23 | Critical Rate +5%, Dodge +4.8% (Captain America) — All Basic Defenses +5.4%, Physical Attack +5.1% (X-23) |
| Corvus Glaive, Hyperion | Movement Speed +4.9%, Attack Speed +4.8% (Corvus Glaive) — All Basic Defenses +5%, HP +5% (Hyperion) |
| Crossbones, Falcon | Attack Speed +4.9%, Skill Cooldown −4.8% (Crossbones) — All Basic Attacks +4.8%, Critical Damage +4.7% (Falcon) |
| Crossbones, Sin | Physical Defense +5.2%, Physical Attack +5.1% (Crossbones) — Physical Defense +5.1%, Physical Attack +5.2% (Sin) |
| Crossbones, Ulik | Attack Speed +5%, Movement Speed +4.8% (Crossbones) — Attack Speed +5%, Movement Speed +4.9% (Ulik) |
| Daredevil, Spider-Gwen | All Basic Attacks +5.2%, Critical Rate +4.9% (Daredevil) — All Basic Attacks +4.9%, Critical Rate +4.9% (Spider-Gwen) |
| Deathlok, Rocket Raccoon | All Basic Attacks +4.8%, Critical Damage +4.5% (Deathlok) — All Basic Attacks +4.8%, Critical Rate +4.5% (Rocket Raccoon) |
| Doctor Strange, Spider-Man | Physical Defense +5.4%, Movement Speed +4.8% (Doctor Strange) — Physical Defense +4.9%, Crowd Control Time −4.8% (Spider-Man) |
| Doctor Strange, Wiccan | Energy Attack +5.2%, Movement Speed +4.8% (Doctor Strange) — Energy Attack +4.9%, Movement Speed +5.1% (Wiccan) |
| Doctor Strange, X-23 | Critical Rate +4.8%, Recovery Rate +4.9% (Doctor Strange) — Movement Speed +5%, Attack Speed +4.7% (X-23) |
| Enchantress, Hela | Attack Speed +4.9%, Movement Speed +4.9% (Enchantress) — Ignore Defense +4.9%, Critical Damage +4.9% (Hela) |
| Enchantress, Hulk (Amadeus Cho) | Attack Speed +4.9%, Movement Speed +4.9% (Enchantress) — All Basic Attacks +5.2%, Crowd Control Time −4.8% (Hulk (Amadeus Cho)) |
| Enchantress, Loki | Energy Attack +5.3%, Skill Cooldown −4.9% (Enchantress) — Dodge +4.8%, Energy Defense +5.3% (Loki) |
| Enchantress, Odin | Energy Attack +5.3%, Skill Cooldown −4.9% (Enchantress) — Energy Attack +5.1%, Critical Rate +5% (Odin) |
| Enchantress, Thor | Attack Speed +4.9%, Movement Speed +4.9% (Enchantress) — Movement Speed +4.9%, Dodge +4.8% (Thor) |
| Fantomex, Psylocke | Movement Speed +5%, Critical Damage +4.9% (Fantomex) — Critical Rate +5.1%, Critical Damage +4.8% (Psylocke) |
| Gorr, Thor | Critical Damage +5%, HP +5% (Gorr) — Critical Damage +5%, Critical Rate +4.9% (Thor) |
| Hellstorm, Sin | Critical Rate +4.9%, Critical Damage +4.8% (Hellstorm) — Critical Rate +4.9%, Skill Cooldown −4.8% (Sin) |
| Kingpin, Rhino | All Basic Defenses +5.4%, Crowd Control Time −5.2% (Kingpin) — All Basic Defenses +5.3%, Crowd Control Time −4.8% (Rhino) |
| Loki, Thor | All Basic Attacks +4.4%, Movement Speed +4.2% (Loki) — Attack Speed +4.4%, Movement Speed +4.2% (Thor) |
| Loki, Ulik | Crowd Control Time −4.9%, Critical Rate +4.8% (Loki) — Attack Speed +4.9%, Movement Speed +4.8% (Ulik) |
| Shang-Chi, Spider-Man | Physical Attack +5.1%, Crowd Control Time −4.9% (Shang-Chi) — Physical Attack +4.9%, Crowd Control Time −5.1% (Spider-Man) |
| She-Hulk, Titania | Physical Attack +5.1%, Ignore Defense +4.8% (She-Hulk) — Physical Attack +5.3%, Ignore Defense +4.8% (Titania) |
| Spider-Man, X-23 | Attack Speed +4.9%, Crowd Control Time −4.7% (Spider-Man) — Critical Damage +4.9%, HP +5.2% (X-23) |
| Squirrel Girl, X-23 | Dodge +5%, Skill Cooldown −4.8% (Squirrel Girl) — Energy Defense +5.4%, Skill Cooldown −5% (X-23) |
| Storm, X-23 | Critical Damage +5%, Energy Defense +5.1% (Storm) — HP +5.3%, Crowd Control Time −4.8% (X-23) |
| Thor, Ulik | Physical Defense +5.1%, Critical Damage +5% (Thor) — Physical Attack +5.1%, Critical Damage +5% (Ulik) |
| Wasp, X-23 | HP +5.4%, Skill Cooldown −4.8% (Wasp) — Recovery Rate +5.1%, Physical Defense +5.1% (X-23) |
| Wolverine, X-23 | All Basic Attacks +5.2%, HP +5% (Wolverine) — Skill Cooldown −4.9%, Dodge +4.8% (X-23) |
| Captain America, Punisher, Spider-Gwen | All Basic Defenses +5.5%, HP +5.4%, Skill Cooldown −4.9% (Captain America) — All Basic Attacks +5.2%, HP +5.4%, Skill Cooldown −4.9% (Punisher) — All Basic Attacks +5.5%, HP +5.4%, Skill Cooldown −4.9% (Spider-Gwen) |
| Hawkeye, Iron Fist, Wong | All Basic Attacks +4.8%, Attack Speed +5.1%, Movement Speed +4.5% (Hawkeye) — Attack Speed +4.9%, Dodge +4.8%, Critical Rate +4.7% (Iron Fist) — Attack Speed +4.9%, Dodge +4.8%, Critical Damage +4.7% (Wong) |

### Versiones en minoría (43)

Vale la primera, la de más páginas.

| Integrantes | Versiones (páginas que dicen cada una) |
|---|---|
| Agent Venom, Black Widow, Hawkeye | Physical Attack +5.3%, Energy Defense +5%, Dodge +4.7% (Agent Venom, Black Widow) — All Basic Attacks +5.4%, Critical Rate +5%, Critical Damage +5% (Hawkeye) |
| Agent Venom, Groot, Rocket Raccoon | All Basic Attacks +5.1%, Dodge +5%, Movement Speed +4.7% (Agent Venom, Groot) — All Basic Attacks +5.1%, Dodge +4.3%, Movement Speed +4.7% (Rocket Raccoon) |
| Angel, Black Widow, Ghost Rider | All Basic Attacks +4.7%, Dodge +4.8%, Critical Damage +5.4% (Black Widow, Ghost Rider) — All Basic Attacks +5.4%, Dodge +4.8%, Critical Damage +4.7% (Angel) |
| Ant-Man, Giant-Man, Shang-Chi | Energy Defense +5.2%, Crowd Control Time −4.8%, HP +5.1% (Ant-Man, Shang-Chi) — Energy Attack +5.2%, Crowd Control Time −4.8%, HP +5.1% (Giant-Man) |
| Baron Mordo, Doctor Strange, Spider-Man | All Basic Attacks +5.2%, Critical Rate +5.9%, Movement Speed +4.8% (Baron Mordo, Doctor Strange) — All Basic Attacks +5.2%, Critical Rate +4.9%, Movement Speed +4.8% (Spider-Man) |
| Black Bolt, Captain Marvel, Venom | Skill Cooldown −4.8%, HP +4.5%, Critical Damage +5.1% (Black Bolt, Captain Marvel) — All Basic Attacks +5.4%, All Basic Defenses +4.4%, Movement Speed +5% (Venom) |
| Black Bolt, Iron Man, Karnak | Dodge +5%, HP +5.1%, All Basic Attacks +5% (Black Bolt, Karnak) — All Basic Defenses +5%, HP +5.1%, All Basic Attacks +5% (Iron Man) |
| Black Cat, Black Panther, Silk | All Basic Attacks +5.4%, Attack Speed +5%, Critical Rate +5% (Black Panther, Silk) — All Basic Attacks +5.2%, Attack Speed +5.1%, Critical Rate +4.9% (Black Cat) |
| Black Cat, Elektra, Winter Soldier | Attack Speed +4.4%, Movement Speed +5.1%, Critical Rate +4.4% (Black Cat, Elektra) — All Basic Defenses +4.4%, Movement Speed +5.1%, Critical Rate +4.4% (Winter Soldier) |
| Black Panther, Captain America, Hawkeye | HP +5%, All Basic Defenses +5.4%, Movement Speed +5% (Black Panther, Captain America) — All Basic Attacks +5.4%, All Basic Defenses +4.9%, Movement Speed +4.7% (Hawkeye) |
| Black Panther, Falcon, Misty Knight | Physical Attack +5.1%, Dodge +5%, Ignore Defense +4.8% (Black Panther, Misty Knight) — Physical Defense +5.2%, Energy Defense +5.1%, Attack Speed +4.7% (Falcon) |
| Black Widow, Falcon, Misty Knight | Critical Rate +5%, Attack Speed +4.8%, Skill Cooldown −4.7% (Black Widow, Misty Knight) — All Basic Attacks +5.3%, HP +5.3%, Critical Rate +4.9% (Falcon) |
| Black Widow, Hawkeye, Mockingbird | Critical Damage +4.5%, Movement Speed +4.4%, Skill Cooldown −4.8% (Black Widow, Mockingbird) — All Basic Attacks +4.8%, Attack Speed +5.1%, Movement Speed +4.5% (Hawkeye) |
| Blade, Doctor Strange, Ghost Rider | Skill Cooldown −5.1%, Recovery Rate +4.2%, All Basic Defenses +4.6% (Blade, Doctor Strange) — All Basic Attacks +5.2%, All Basic Defenses +5.3%, HP +4.9% (Ghost Rider) |
| Bullseye, Captain America, Iron Man | All Basic Attacks +5.4%, Critical Rate +5%, Crowd Control Time −4.9% (Captain America, Iron Man) — All Basic Attacks +5.5%, Critical Rate +5%, Crowd Control Time −4.9% (Bullseye) |
| Bullseye, Hawkeye, Punisher | Attack Speed +4.9%, Critical Rate +5%, Critical Damage +4.5% (Bullseye, Punisher) — All Basic Attacks +4.8%, Attack Speed +5.1%, Movement Speed +4.5% (Hawkeye) |
| Captain America, Daisy Johnson, Daredevil | All Basic Defenses +5.1%, HP +5.1%, Ignore Defense +4.6% (Daisy Johnson, Daredevil) — Defense +5.1%, HP +5.1%, Ignore Defense +4.6% (Captain America) |
| Captain America, Deadpool, Phil Coulson | All Basic Attacks +5.4%, Crowd Control Time −4.8%, HP +5.1% (Captain America, Phil Coulson) — All Basic Attacks +5.3%, Critical Rate +4.8%, Ignore Defense +5.1% (Deadpool) |
| Captain America, Deadpool, Wolverine | Physical Attack +5.3%, HP +5%, Recovery Rate +4.9% (Captain America, Wolverine) — Critical Rate +4.7%, Critical Damage +4.7%, Ignore Defense +4.8% (Deadpool) |
| Captain America, Falcon, Wiccan | Skill Cooldown −4.9%, Crowd Control Time −4.8%, All Basic Defenses +5% (Captain America, Wiccan) — All Basic Attacks +5.4%, Critical Rate +5%, Critical Damage +4.9% (Falcon) |
| Carnage, Deadpool, Enchantress | Dodge +4.9%, Critical Rate +4.9%, HP +5.1% (Carnage, Enchantress) — All Basic Attacks +5.2%, Dodge +4.7%, Critical Damage +4.8% (Deadpool) |
| Clea, Doctor Strange, Dormammu | Physical Defense +5.2%, HP +5.1%, Movement Speed +4.7% (Clea, Doctor Strange) — Physical Defense +5.2%, HP +5.2%, Movement Speed +4.7% (Dormammu) |
| Corvus Glaive, Hulk, Proxima Midnight | All Basic Attacks +5.5%, All Basic Defenses +5.5%, Skill Cooldown −5.1% (Corvus Glaive, Hulk) — All Basic Attacks +5.5%, All Basic Defenses +5.5%, Crowd Control Time −5.1% (Proxima Midnight) |
| Crossbones, Red Skull, Sin | Skill Cooldown −4.9%, Dodge +4.8%, Movement Speed +4.7% (Red Skull, Sin) — Skill Cooldown −4.9%, Dodge +4.9%, Movement Speed +4.7% (Crossbones) |
| Daredevil, Deadpool, Spider-Man | Physical Attack +5.4%, All Basic Defenses +5.1%, Crowd Control Time −4.8% (Daredevil, Spider-Man) — Energy Defense +5.2%, Crowd Control Time −4.8%, HP +5.1% (Deadpool) |
| Daredevil, Iron Fist, Shang-Chi | Attack Speed +4.9%, Movement Speed +4.7%, Crowd Control Time −4.8% (Daredevil, Shang-Chi) — Attack Speed +5.2%, Movement Speed +4.7%, Crowd Control Time −4.8% (Iron Fist) |
| Daredevil, Punisher, Spider-Man | All Basic Defenses +4.8%, HP +5.4%, Ignore Defense +4.3% (Punisher, Spider-Man) — All Basic Defenses +4.6%, HP +5.4%, Ignore Defense +4.3% (Daredevil) |
| Deadpool, Fantomex, Wolverine | Physical Attack +5.2%, Attack Speed +4.9%, Recovery Rate +4.8% (Fantomex, Wolverine) — All Basic Attacks +5.2%, Attack Speed +4.7%, Critical Rate +5% (Deadpool) |
| Deadpool, Iron Fist, Luke Cage | All Basic Attacks +5.2%, Critical Damage +4.9%, Recovery Rate +4.8% (Iron Fist, Luke Cage) — Energy Defense +5.2%, Crowd Control Time −4.7%, HP +5.1% (Deadpool) |
| Deadpool, Spider-Man, Wong | Physical Attack +5.4%, Dodge +4.9%, Attack Speed +4.7% (Spider-Man, Wong) — Attack Speed +4.7%, Movement Speed +4.6%, Dodge +4.9% (Deadpool) |
| Doctor Octopus, Iron Man, Ultron | Movement Speed +4.4%, HP +4.7%, Attack Speed +4.8% (Iron Man, Ultron) — Movement Speed +4.4%, Max HP Defense +4.7%, Attack Speed +4.8% (Doctor Octopus) |
| Doctor Octopus, Kraven The Hunter, Sandman | Physical Attack +5.1%, Crowd Control Time −5%, Movement Speed +4.7% (Kraven The Hunter, Sandman) — Physical Attack +5.2%, Crowd Control Time −4.9%, Movement Speed +5% (Doctor Octopus) |
| Doctor Octopus, Silk, Spider-Man | All Basic Defenses +5.2%, Critical Damage +4.8%, Ignore Defense +4.9% (Silk, Spider-Man) — All Basic Defenses +5.2%, HP +5.1%, Dodge +5.3% (Doctor Octopus) |
| Falcon, Hawkeye, Mockingbird | Attack Speed +5.1%, Movement Speed +4.9%, Critical Damage +4.8% (Falcon, Mockingbird) — All Basic Attacks +5.4%, Critical Rate +5%, Critical Damage +5% (Hawkeye) |
| Falcon, Vision, War Machine | All Basic Attacks +5.5%, Attack Speed +4.4%, Dodge +4.7% (Falcon, War Machine) — All Basic Attacks +5.2%, Attack Speed +4.4%, Dodge +4.7% (Vision) |
| Giant-Man, Hawkeye, Quicksilver | Physical Attack +5.1%, Physical Defense +5.4%, Dodge +4.7% (Hawkeye, Quicksilver) — Attack +5.1%, Physical Defense +5.4%, Dodge +4.7% (Giant-Man) |
| Hawkeye, Hawkeye (Kate Bishop), Mockingbird | Physical Defense +5.2%, Energy Defense +5.2%, Movement Speed +4.7% (Hawkeye (Kate Bishop), Mockingbird) — All Basic Attacks +5.4%, All Basic Defenses +4.9%, Movement Speed +4.7% (Hawkeye) |
| Hawkeye, Hellstorm, Mockingbird | Critical Rate +5.1%, Dodge +4.9%, Attack Speed +4.7% (Hellstorm, Mockingbird) — All Basic Attacks +4.8%, Attack Speed +5.1%, Movement Speed +4.5% (Hawkeye) |
| Magneto, Nova (Sam Alexander), Spider-Man | HP +5%, Movement Speed +5%, All Basic Attacks +5.7% (Magneto, Spider-Man) — HP +5.1%, Movement Speed +5%, All Basic Attacks +5.1% (Nova (Sam Alexander)) |
| Misty Knight, Moon Knight, Punisher | Physical Attack +5.3%, Max Dodge +4.8%, Crowd Control Time −4.8% (Moon Knight, Punisher) — Physical Attack +5.3%, Dodge +4.8%, Crowd Control Time −4.8% (Misty Knight) |
| Odin, Thor, Thor (Jane Foster) | Energy Attack +5.2%, All Basic Defenses +5.2%, Critical Rate +4.7% (Odin, Thor (Jane Foster)) — Energy Attack +5.3%, All Basic Defenses +5.2%, Critical Rate +4.7% (Thor) |
| Punisher, Rocket Raccoon, Star-Lord | Attack Speed +4.9%, Critical Damage +4.9%, Ignore Defense +5.1% (Punisher, Star-Lord) — All Basic Attacks +4.9%, Attack Speed +4.9%, HP +5.1% (Rocket Raccoon) |
| Silk, Spider-Gwen, Spider-Man (Miles Morales) | Critical Rate +5%, Dodge +5.1%, Ignore Defense +5% (Spider-Gwen, Spider-Man (Miles Morales)) — All Basic Defenses +5.4%, Skill Cooldown −4.9%, Ignore Defense +5% (Silk) |

### Nombres empatados (29)

La app los muestra juntos, separados por « / ».

- Ancient One, Doctor Strange: Sorcercer's Successor / Sorcerer's Successor
- Arachknight, Moon Knight: Knights On Guard / Spider Knights
- Arachknight, Spider-Man: Knights On Guard / Spider Knights
- Black Bolt, Black Panther: Kings of Illuminati / Kings of the Illuminati
- Black Dwarf, Thanos: You Disappointed Me / You Dissapointed Me
- Black Widow, Whiplash: Straight Out Of Russia / Straight Out of Russia
- Captain America, Captain America (Sharon Rogers): Generation Justice / Generational Justice
- Captain America, Thor: Hammer & Shield / Hammer and Shield
- Captain America, Wasp: Born To Lead / Born to Lead
- Captain America (Sharon Rogers), Vision: Synthezoid Liberty / Synthezoid of Liberty
- Crystal, Quicksilver: Temporary Happiness / Tepmorary Happiness
- Cyclops, Daredevil: Shades  of Red / Shades of Red
- Daredevil, Spider-Man: Misfortune of Fate / Symbiote Shock
- Deathlok, Winter Soldier: Cybernetically Enchanced / Cybernetically Enhanced
- Doctor Strange, Iron Fist: Mediation Time / Meditation Time
- Enchantress, Hulk (Amadeus Cho): Mind Controlled Hulk / Mind-Controlled Hulk
- Hyperion, Thor: Brother in Arms / Brothers in Arms
- Magneto, Rogue: Suprising Relationship / Surprising Relationship
- Moon Girl, Wolverine: Dino Ball Special / Dinosaur Ball Special
- Nebula, Ronan: Galactic Judgement / Galactic Judgment
- Punisher, Rhino: Bad Rhino / Bad Rhino!
- Punisher, Rocket Raccoon: I Love the Smell of Gun Powder... / I love the Smell of Gun Powder...
- Red She-Hulk, She-Hulk: Woman of Power / Women of Power
- Shang-Chi, Wong: Chinese Martial Artists / Chinese Martial Arts
- Slapstick, Spider-Man: Deadpool Pal / Deadpool Pol
- Spider-Man (Miles Morales), Venom: No More / No More!
- Vision, War Machine: Need some help, Stark? / Stark Contrast
- Captain Marvel, Spider-Man, Venom: Journalistic Integirty / Journalistic Integrity / Journalistic Intergrity
- Giant-Man, Hulk (Amadeus Cho), Spider-Man: The Odessey / The Odyessey / The Odyssey

Sin nombre en ninguna de sus páginas: Thor (Jane Foster), Titania.

### Stats que la app no conoce

Van como los escribe la wiki: la sinergia los cuenta para todos y dice que no están clasificados. Si son un stat conocido con otro nombre, se agregan a STATS en scripts/bonos.py.

- `Attack`: Giant-Man
- `Attack Defense`: Captain Marvel, Dazzler, She-Hulk
- `Critical Defense`: Black Panther, Killmonger, Shuri
- `Defense`: Captain America
- `Energy Damage`: Iceman, Supergiant
- `Max Dodge`: Moon Knight, Punisher
- `Max HP Defense`: Doctor Octopus
- `Physical Damage`: Human Torch, Nick Fury, Spider-Man, White Fox

### Bonos que la página de un integrante no lista (32)

- Bishop: con Sabretooth + Silver Samurai
- Black Cat: con Winter Soldier
- Black Panther: con Mister Fantastic; con Black Bolt + Doctor Doom; con Crescent + White Fox; con Doctor Doom + Storm; con Mister Fantastic + Star-Lord; con Storm + Victorious
- Captain America (Sharon Rogers): con Luna Snow + White Fox; con War Machine + Winter Soldier
- Ghost Rider (Robbie Reyes): con Daisy Johnson
- Kang the Conqueror: con Apocalypse; con Cable; con Doctor Doom; con Doctor Strange; con Gladiator; con Iron Man; con Ant-Man + Wasp; con Captain America + Thor; con Iron Man + Mister Fantastic; con Thanos + Ultron
- Sabretooth: con Bishop + Silver Samurai
- Scorpion: con Electro + Vulture
- Sentry: con Daken + Green Goblin
- Viper: con Emma Frost + Rachel Summers; con Kitty Pryde + Sabretooth
- Vulture: con Doctor Octopus
- War Machine: con Captain America (Sharon Rogers) + Falcon
- White Fox: con Captain America (Sharon Rogers) + Luna Snow
- Winter Soldier: con Black Panther; con Captain America (Sharon Rogers) + War Machine
- Wolverine: con Jubilee + X-23

### Lo que no se pudo leer (1)

Esa página no cuenta para ese bono.

- Vulture, Creatures of Air and Sea: stat ilegible: ''Dodge ↑ +4.%''

## 11. Strikers: la pestaña Striker de la wiki

thanosvibs no publica los strikers. La app los toma de la pestaña Striker de la página de cada personaje en la wiki (171 páginas la tienen, 7020 filas): quién puede aparecer a pegar junto a él y con qué probabilidad, cuando él ataca o cuando lo atacan (scripts/strikers.py).

Personajes sin la pestaña en su página (119): Adam Warlock, Agent Venom, Angel, Annihilus, Ant-Man, Apocalypse, Arachknight, Athena, Beast, Bishop, Black Bolt, Black Knight, Black Swan, Black Widow, Captain America, Carnage, Cassandra Nova, Cassie Lang, Colossus, Cyclops, Destroyer, Doctor Doom, Doctor Octopus, Doctor Voodoo, Elektra, Emma Frost, Falcon (Joaquin Torres), Fantomex, Franklin Richards, Galactus, Gambit, Ghost Panther, Ghost Rider (Robbie Reyes), Giant-Man, Gorr, Green Goblin, Gwenpool, Hades (Pluto), Havok, Hercules, Hope Summers, Hulk, Iceman, Ikon, Iron Hammer, Ironheart, Jean Grey, Jeff the Land Shark, Jubilee, Juggernaut, Kahhori, Kang the Conqueror, Kid Omega, Kitty Pryde, Kraven The Hunter, Leader, Lizard, M'Baku, Madelyne Pryor, Magik, Magneto, Man-Thing, Mantis, Marvel Boy, Maximus, Moon Girl, Morgan le Fay, Morph, Ms. Marvel (Kamala Khan), Namor, Nightcrawler, Nova (Sam Alexander), Odin, Okoye, Omega Red, Polaris, Professor X, Psylocke, Punisher, Quicksilver, Rachel Summers, Rhino, Rogue, Sabretooth, Scarlet Spider, Scarlet Witch, Scorpion, Scream, Shadow Shell, She-Hulk, Shuri, Silver Samurai, Silver Surfer (Shalla-Bal), Skurge, Sleeper, Songbird, Spider-Man, Spider-Man (Miles Morales), Spot, Squirrel Girl, Storm, Sun Bird, Sunspot, Sylvie, The Hood, Thor (Jane Foster), Titania, Toxin, Valeria Richards, Valkyrie, Venom, Venus (Aphrodite), War Tiger, Wasp (Nadia Van Dyne), Weapon Hex, White Tiger, Wolverine, X-23, Zeus. En la app no tienen strikers propios; sí pueden ser strikers de otros.

### Lo que no se pudo leer (2)

Esa fila no cuenta.

- Rocket Raccoon: no se lee la probabilidad o cuándo aparece (`| style="text-align:left"|[[Image:LincolnCampbellIcon.png|30px]] Lincoln Campbell ||  chance to appear when attacking.`)
- Vision: no se lee la probabilidad o cuándo aparece (`| style="text-align:left"|[[Image:SpiderGwenIcon.png|30px]] Spider-Gwen || 19% chance to appear when attack.`)

## 12. Liderazgos que Leads & Supports no lista

Leads & Supports de thanosvibs publica el liderazgo de cada retrato con los uniformes que comparten su entrada, y a algunos uniformes no los lista. Si la Leader Skill de uno de ellos, en la API de skills, es idéntica a la de su base, el build le copia el liderazgo de la base (Ezequiel, 2 de octubre de 2026): solo el liderazgo (`leader` y `leader2`), no los soportes. Idéntica es igual en todo lo que la API publica de ella, salvo sus ids: el nombre, la recarga y, en cada etapa, el objetivo, la activación, el elemento y cada efecto, con su etiqueta, su texto (sin negritas ni espacios de más) con sus números, su duración y su intervalo. Una Leader Skill con un valor que la API no publica (`$TIME`, `$HEROSUBTYPE1`) no se puede comparar, así que no se completa. Si otra hermana con la misma Leader Skill tiene otro liderazgo, el build para (scripts/fuentes.py, `completar_liderazgos`).

### Completados (5)

- Ghost — Marvel Studios' Thunderbolts* (`ghost2`) ← Ghost (`ghost`)
- Knull — Ancient History (`knull1`) ← Knull (`knull`)
- Moon Girl — Monsters Unleashed! (MFF Variant) (`moongirl1`) ← Moon Girl (`moongirl`)
- Sentinel — Stark Sentinels Mk II (`sentinel2`) ← Sentinel (`sentinel`)
- Shang-Chi — Marvel Animation's Marvel Zombies (`shangchi2`) ← Shang-Chi (`shangchi`)

### Sin completar aunque una hermana tiene liderazgo (58)

En qué difiere su Leader Skill (la suya / la de la otra): si la base tiene liderazgo, de la de la base, y se nombran las hermanas que la tienen igual; si no, de la de la hermana con liderazgo más parecida. Las hermanas con la misma Leader Skill van juntas.

- Arachknight (`arachknight`): es la base, y la regla es para uniformes. Contra `arachknight1`: nombre: Spider-Totem / Guardian of Dimensions; etapa 1, objetivo: All Allies / Infinity Warps Allies\nActivates when: Infinity Warps type Ally enters; etapa 1, efecto 1: «Dodge Rate increases by 6%.» (DODGE ↑) / «Increases all Basic Attacks by 45%» (ALL BASIC ATTACKS INCREASE); etapa 1, efecto 2: «Decreases Debuff Duration by 24%.» (CROWD CONTROL TIME ↓) / «Increases all Basic Attacks by 55%» (ALL BASIC ATTACKS INCREASE); etapa 1, efecto 3: — / «Increases all Basic Attacks by 65%» (ALL BASIC ATTACKS INCREASE).
- Blade (`blade`): es la base, y la regla es para uniformes. Contra `blade3`: nombre: Daywalker / Master Hunter; recarga: 25 s / 0 s; etapa 1, objetivo: All Allies / Weapon Master Allies; etapa 1, activación: 25% chance when attacking / —; etapa 1, efecto 1: «Recovers HP equal to 8% of damage dealt to a target<br>Cannot recover more than 0.5% HP each time damage is dealt.» (HP STEAL), 10 s / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Blade — 70's Classic (`blade1`): su base no tiene liderazgo en Leads & Supports. Contra `blade3`: nombre: Daywalker / Master Hunter; recarga: 25 s / 0 s; etapa 1, objetivo: All Allies / Weapon Master Allies; etapa 1, activación: 25% chance when attacking / —; etapa 1, efecto 1: «Recovers HP equal to 8% of damage dealt to a target<br>Cannot recover more than 0.5% HP each time damage is dealt.» (HP STEAL), 10 s / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Blade — Avengers (`blade2`): su base no tiene liderazgo en Leads & Supports. Contra `blade3`: nombre: Daywalker / Master Hunter; recarga: 25 s / 0 s; etapa 1, objetivo: All Allies / Weapon Master Allies; etapa 1, activación: 25% chance when attacking / —; etapa 1, efecto 1: «Recovers HP equal to 8% of damage dealt to a target<br>Cannot recover more than 0.5% HP each time damage is dealt.» (HP STEAL), 10 s / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Captain America (`captainamerica`): es la base, y la regla es para uniformes. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Avengers 3099 (`captainamerica10`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Avengers: Age of Ultron (`captainamerica1`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Enter the Phoenix (`captainamerica12`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Galactic Talon (`captainamerica15`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: idéntica.
- Captain America — Hydra Supreme (`captainamerica11`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Marvel NOW! (`captainamerica5`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Marvel Studios' Avengers: Endgame (`captainamerica9`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Marvel Studios' Avengers: Infinity War (`captainamerica6`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Marvel Studios' Captain America: Civil War (`captainamerica4`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Marvel Studios' Captain America: The Winter Soldier (`captainamerica3`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Secret Wars: 2099 (`captainamerica2`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Captain America — Team Suit (`captainamerica8`): su base no tiene liderazgo en Leads & Supports. Contra `captainamerica13`, `captainamerica14`: etapa 1, efecto 1: «30% increase of HP.» (MAX HP ↑) / «45% increase of HP.» (MAX HP ↑).
- Deadpool (`deadpool`): es la base, y la regla es para uniformes. Contra `deadpool8`: nombre: Natural Born Leader?! / Marvel's Savior; etapa 1, efecto 1: «6% increase of Recovery Rate.» (RECOVERY RATE ↑) / «Increases all Basic Attacks by 40%, all Basic Defenses by 40%, and all Speeds by 15%.» (Increases all basic stats); etapa 1, efecto 2: «Increases all Basic Attacks by 35%, all Basic Defenses by 35%, and all Speeds by 10%.» (Increases all basic stats) / «Acquires the following effect for $TIME sec.» (Give Power).
- Deadpool — 30th Anniversary Black Version (`deadpool4`): su base no tiene liderazgo en Leads & Supports. Contra `deadpool8`: nombre: Natural Born Leader?! / Marvel's Savior; etapa 1, efecto 1: «6% increase of Recovery Rate.» (RECOVERY RATE ↑) / «Increases all Basic Attacks by 40%, all Basic Defenses by 40%, and all Speeds by 15%.» (Increases all basic stats); etapa 1, efecto 2: «Increases all Basic Attacks by 35%, all Basic Defenses by 35%, and all Speeds by 10%.» (Increases all basic stats) / «Acquires the following effect for $TIME sec.» (Give Power).
- Deadpool — 30th Anniversary White Version (`deadpool5`): su base no tiene liderazgo en Leads & Supports. Contra `deadpool8`: nombre: Natural Born Leader?! / Marvel's Savior; etapa 1, efecto 1: «6% increase of Recovery Rate.» (RECOVERY RATE ↑) / «Increases all Basic Attacks by 40%, all Basic Defenses by 40%, and all Speeds by 15%.» (Increases all basic stats); etapa 1, efecto 2: «Increases all Basic Attacks by 35%, all Basic Defenses by 35%, and all Speeds by 10%.» (Increases all basic stats) / «Acquires the following effect for $TIME sec.» (Give Power).
- Deadpool — Holiday Party (`deadpool3`): su base no tiene liderazgo en Leads & Supports. Contra `deadpool8`: nombre: Natural Born Leader?! / Marvel's Savior; etapa 1, efecto 1: «6% increase of Recovery Rate.» (RECOVERY RATE ↑) / «Increases all Basic Attacks by 40%, all Basic Defenses by 40%, and all Speeds by 15%.» (Increases all basic stats); etapa 1, efecto 2: «Increases all Basic Attacks by 35%, all Basic Defenses by 35%, and all Speeds by 10%.» (Increases all basic stats) / «Acquires the following effect for $TIME sec.» (Give Power).
- Deadpool — Lady Deadpool (`deadpool2`): su base no tiene liderazgo en Leads & Supports. Contra `deadpool8`: nombre: Natural Born Leader?! / Marvel's Savior; etapa 1, efecto 1: «6% increase of Recovery Rate.» (RECOVERY RATE ↑) / «Increases all Basic Attacks by 40%, all Basic Defenses by 40%, and all Speeds by 15%.» (Increases all basic stats); etapa 1, efecto 2: «Increases all Basic Attacks by 35%, all Basic Defenses by 35%, and all Speeds by 10%.» (Increases all basic stats) / «Acquires the following effect for $TIME sec.» (Give Power).
- Deadpool — X-Force (`deadpool1`): su base no tiene liderazgo en Leads & Supports. Contra `deadpool8`: nombre: Natural Born Leader?! / Marvel's Savior; etapa 1, efecto 1: «6% increase of Recovery Rate.» (RECOVERY RATE ↑) / «Increases all Basic Attacks by 40%, all Basic Defenses by 40%, and all Speeds by 15%.» (Increases all basic stats); etapa 1, efecto 2: «Increases all Basic Attacks by 35%, all Basic Defenses by 35%, and all Speeds by 10%.» (Increases all basic stats) / «Acquires the following effect for $TIME sec.» (Give Power).
- Dormammu (`dormammu`): es la base, y la regla es para uniformes. Contra `dormammu1`: etapa 1, objetivo: All Allies / Super Villain Allies; etapa 1, efecto 1: «Increases all Basic Defenses by 24%.» (ALL BASIC DEFENSES INCREASE) / «Increases basic damage dealt to $HEROSUBTYPE1 faction by 60%.» (Increases basic damage based on character's faction).
- Gamora (`gamora`): es la base, y la regla es para uniformes. Contra `gamora3`: nombre: Most Dangerous Woman / Assassination Technique; etapa 1, efecto 1: «Attack Speed increases by 13.5%.» (ATTACK SPEED ↑) / «55% increase of Physical Attack.» (PHYSICAL ATTACK ↑); etapa 1, efecto 2: — / «Increases All Speeds by 6%.» (ALL SPEED ↑).
- Gamora — All-New, All-Different (`gamora1`): su base no tiene liderazgo en Leads & Supports. Contra `gamora3`: nombre: Most Dangerous Woman / Assassination Technique; etapa 1, efecto 1: «Attack Speed increases by 13.5%.» (ATTACK SPEED ↑) / «55% increase of Physical Attack.» (PHYSICAL ATTACK ↑); etapa 1, efecto 2: — / «Increases All Speeds by 6%.» (ALL SPEED ↑).
- Gamora — Guardians of the Galaxy 2 (`gamora2`): su base no tiene liderazgo en Leads & Supports. Contra `gamora3`: nombre: Most Dangerous Woman / Assassination Technique; etapa 1, efecto 1: «Attack Speed increases by 13.5%.» (ATTACK SPEED ↑) / «55% increase of Physical Attack.» (PHYSICAL ATTACK ↑); etapa 1, efecto 2: — / «Increases All Speeds by 6%.» (ALL SPEED ↑).
- Green Goblin (`greengoblin`): es la base, y la regla es para uniformes. Contra `greengoblin2`: etapa 1, objetivo: All Allies / Dark Avengers Allies; etapa 1, efecto 1: «Increases Poison Resist by 50%.» (POISON RESIST ↑) / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Green Goblin — Gold Goblin (`greengoblin5`): su base no tiene liderazgo en Leads & Supports. Contra `greengoblin3`, `greengoblin4`: idéntica.
- Green Goblin — Ultimate (`greengoblin1`): su base no tiene liderazgo en Leads & Supports. Contra `greengoblin2`: etapa 1, objetivo: All Allies / Dark Avengers Allies; etapa 1, efecto 1: «Increases Flame Resist by 50%.» (FLAME RESIST ↑) / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Heimdall (`heimdall`): es la base, y la regla es para uniformes. Contra `heimdall1`: etapa 1, efecto 1: «Increases all Basic Defenses by 36%.» (ALL BASIC DEFENSES INCREASE) / «Increases all Basic Defenses by 40%.» (ALL BASIC DEFENSES INCREASE); etapa 1, efecto 2: — / «Ignores target's Dodge Rate by 30%.» (IGNORE DODGE).
- Hulk — Fear Itself (`hulk7`): su Leader Skill no es idéntica a la de su base. Contra `hulk`, `hulk1`, `hulk2`, `hulk3`, `hulk4`, `hulk5`: etapa 1, efecto 1: «Increases all Basic Defenses by 24%.» (ALL BASIC DEFENSES INCREASE) / «30% increase of Physical Attack.» (PHYSICAL ATTACK ↑).
- Hulk — Immortal Hulk (`hulk6`): su Leader Skill no es idéntica a la de su base. Contra `hulk`, `hulk1`, `hulk2`, `hulk3`, `hulk4`, `hulk5`: etapa 1, efecto 1: «Increases all Basic Defenses by 24%.» (ALL BASIC DEFENSES INCREASE) / «30% increase of Physical Attack.» (PHYSICAL ATTACK ↑).
- Hulk — Marvel Studios' Spider-Man: Brand New Day (`hulk9`): su Leader Skill no es idéntica a la de su base. Contra `hulk`, `hulk1`, `hulk2`, `hulk3`, `hulk4`, `hulk5`: nombre: Banner's Biotech / Hulk Roar; etapa 1, objetivo: All Allies for the first effect, Self for the second effect / All Allies; etapa 1, efecto 1: «Increases all Basic Defenses by 24%.» (ALL BASIC DEFENSES INCREASE) / «30% increase of Physical Attack.» (PHYSICAL ATTACK ↑); etapa 1, efecto 2: «30% increase of HP.» (MAX HP ↑) / —.
- Hulk — Titan (`hulk8`): su Leader Skill no es idéntica a la de su base. Contra `hulk`, `hulk1`, `hulk2`, `hulk3`, `hulk4`, `hulk5`: nombre: Titan's Vigor / Hulk Roar; etapa 1, objetivo: All Allies for the first effect, Self for the second effect / All Allies; etapa 1, efecto 1: «Increases all Basic Defenses by 24%.» (ALL BASIC DEFENSES INCREASE) / «30% increase of Physical Attack.» (PHYSICAL ATTACK ↑); etapa 1, efecto 2: «30% increase of HP.» (MAX HP ↑) / —.
- Human Torch — Classic (`humantorch2`): su Leader Skill no es idéntica a la de su base. Contra `humantorch`, `humantorch1`: etapa 1, efecto 1: «Increases Flame Resist by 50%.» (FLAME RESIST ↑) / «Increases Flame Damage by 25%.» (FLAME DAMAGE ↑).
- Human Torch — Marvel Studios' The Fantastic Four: First Steps (`humantorch4`): su Leader Skill no es idéntica a la de su base. Contra `humantorch`, `humantorch1`: etapa 1, efecto 1: «Increases Flame Resist by 50%.» (FLAME RESIST ↑) / «Increases Flame Damage by 25%.» (FLAME DAMAGE ↑).
- Human Torch — The Fall of the Fantastic Four (`humantorch3`): su Leader Skill no es idéntica a la de su base. Contra `humantorch`, `humantorch1`: etapa 1, efecto 1: «Increases Flame Resist by 50%.» (FLAME RESIST ↑) / «Increases Flame Damage by 25%.» (FLAME DAMAGE ↑).
- Invisible Woman (`invisiblewoman`): es la base, y la regla es para uniformes. Contra `invisiblewoman3`, `invisiblewoman4`: nombre: Strong Willpower / Motherly Guidance; etapa 1, efecto 1: «Increases Mind Resist by 50%.» (MIND RESIST ↑) / «45% increase of Energy Attack.» (ENERGY ATTACK ↑).
- Invisible Woman — Future Foundation (`invisiblewoman1`): su base no tiene liderazgo en Leads & Supports. Contra `invisiblewoman3`, `invisiblewoman4`: nombre: Strong Willpower / Motherly Guidance; etapa 1, efecto 1: «Increases Mind Resist by 50%.» (MIND RESIST ↑) / «45% increase of Energy Attack.» (ENERGY ATTACK ↑).
- Iron Fist (`ironfist`): es la base, y la regla es para uniformes. Contra `ironfist4`: recarga: 40 s / 0 s; etapa 1, objetivo: All Allies / Defenders Allies; etapa 1, activación: 25% chance when attacking / —; etapa 1, efecto 1: «Attack Speed increases by 12%.» (ATTACK SPEED ↑), 30 s / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Iron Fist — All-New, All-Different (`ironfist2`): su base no tiene liderazgo en Leads & Supports. Contra `ironfist4`: recarga: 40 s / 0 s; etapa 1, objetivo: All Allies / Defenders Allies; etapa 1, activación: 25% chance when attacking / —; etapa 1, efecto 1: «Attack Speed increases by 12%.» (ATTACK SPEED ↑), 30 s / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Iron Fist — Marvel Studios' Iron Fist (`ironfist3`): su base no tiene liderazgo en Leads & Supports. Contra `ironfist4`: recarga: 40 s / 0 s; etapa 1, objetivo: All Allies / Defenders Allies; etapa 1, activación: 25% chance when attacking / —; etapa 1, efecto 1: «Attack Speed increases by 12%.» (ATTACK SPEED ↑), 30 s / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Iron Fist — New Avengers (`ironfist1`): su base no tiene liderazgo en Leads & Supports. Contra `ironfist4`: recarga: 40 s / 0 s; etapa 1, objetivo: All Allies / Defenders Allies; etapa 1, activación: 25% chance when attacking / —; etapa 1, efecto 1: «Attack Speed increases by 12%.» (ATTACK SPEED ↑), 30 s / «Increases all Basic Attacks by 60%» (ALL BASIC ATTACKS INCREASE).
- Luke Cage (`lukecage`): es la base, y la regla es para uniformes. Contra `lukecage3`: recarga: 50 s / 20 s; etapa 1, objetivo: All Allies / Defenders Allies; etapa 1, activación: 25% rate when hit / when debuffed; etapa 1, efecto 1: «100% chance to become immune to Physical Damage.» (PHYSICAL IMMUNITY), 11 s / «100% chance to become immune to Physical Damage.» (PHYSICAL IMMUNITY), 6 s; etapa 1, efecto 2: — / «Removes all Debuffs.» (Removes all Debuffs.), 12 s.
- Luke Cage — All-New, All-Different (`lukecage1`): su base no tiene liderazgo en Leads & Supports. Contra `lukecage3`: recarga: 40 s / 20 s; etapa 1, objetivo: All Allies / Defenders Allies; etapa 1, activación: 25% rate when hit / when debuffed; etapa 1, efecto 1: «100% chance to become immune to Physical Damage.» (PHYSICAL IMMUNITY), 12 s / «100% chance to become immune to Physical Damage.» (PHYSICAL IMMUNITY), 6 s; etapa 1, efecto 2: — / «Removes all Debuffs.» (Removes all Debuffs.), 12 s.
- Luke Cage — Marvel Studios' Luke Cage (`lukecage2`): su base no tiene liderazgo en Leads & Supports. Contra `lukecage3`: recarga: 40 s / 20 s; etapa 1, objetivo: All Allies / Defenders Allies; etapa 1, activación: 25% rate when hit / when debuffed; etapa 1, efecto 1: «100% chance to become immune to Physical Damage.» (PHYSICAL IMMUNITY), 12 s / «100% chance to become immune to Physical Damage.» (PHYSICAL IMMUNITY), 6 s; etapa 1, efecto 2: — / «Removes all Debuffs.» (Removes all Debuffs.), 12 s.
- Magik (`magik`): es la base, y la regla es para uniformes. Contra `magik2`, `magik3`: nombre: Darkchylde / Limbo Leader; etapa 1, objetivo: All Allies / Mutant Allies; etapa 1, efecto 1: «Critical Rate increases by 13%.» (CRITICAL RATE ↑) / «Increases all Basic Attacks by 40%» (ALL BASIC ATTACKS INCREASE).
- Magik — Phoenix Five (`magik1`): su base no tiene liderazgo en Leads & Supports. Contra `magik2`, `magik3`: nombre: Darkchylde / Limbo Leader; etapa 1, objetivo: All Allies / Mutant Allies; etapa 1, efecto 1: «Critical Rate increases by 13%.» (CRITICAL RATE ↑) / «Increases all Basic Attacks by 40%» (ALL BASIC ATTACKS INCREASE).
- Mephisto — Master of Hell (`mephisto1`): su Leader Skill no es idéntica a la de su base. Contra `mephisto`: nombre: Lord of Hell / Soul Contract; recarga: 0 s / 20 s; etapa 1, activación: — / when debuffed; etapa 1, efecto 1: «Increases Flame Damage by 30%.» (FLAME DAMAGE ↑) / «Removes all Debuffs.» (Removes all Debuffs.), 11 s; etapa 1, efecto 2: «Acquires the following effect for $TIME sec.» (Give Power) / «Increases Flame Damage by 30%.» (FLAME DAMAGE ↑), 15 s.
- Rachel Summers (`rachelsummers`): es la base, y la regla es para uniformes. Contra `rachelsummers1`: nombre: Mental Enhancement / Phoenix's Majesty; etapa 1, objetivo: All Allies / Phoenix Force Allies; etapa 1, efecto 2: — / «Acquires the following effect for $TIME sec.» (Give Power).
- Rescue (`rescue`): es la base, y la regla es para uniformes. Contra `rescue1`, `rescue2`: etapa 1, activación: when HP is below 30% / when HP is below 99%; etapa 1, efecto 1: «Creates a Shield equal to 20% of Max HP» (SHIELD), 10 s / «Creates a Shield equal to 50% of Max HP» (SHIELD), 5 s.
- Sentry — Marvel Studios' Thunderbolts* (`sentry2`): su Leader Skill no es idéntica a la de su base. Contra `sentry`: recarga: 0 s / 20 s; etapa 1, activación: — / when debuffed; etapa 1, efecto 1: «Increases all Basic Attacks by 30%» (ALL BASIC ATTACKS INCREASE) / «Removes all Debuffs.» (Removes all Debuffs.), 12 s; etapa 1, efecto 2: «Acquires the following effect for $TIME sec.» (Give Power) / «Increases all Basic Attacks by 30%.» (Increases all Basic Attacks), 12 s. Contra `sentry1`: el mismo texto, con valores que la API no publica.
- Spider-Man (Miles Morales) (`milesmorales`): es la base, y la regla es para uniformes. Contra `milesmorales2`: etapa 1, objetivo: All Allies / Target ID: 72; etapa 1, efecto 2: — / «Increases all Basic Attacks by 70%» (ALL BASIC ATTACKS INCREASE); etapa 1, efecto 3: — / «Decreases basic damage received by 20%.» (Decreases all basic damage).
- Spider-Man (Miles Morales) — Into the Spider-Verse (`milesmorales1`): su base no tiene liderazgo en Leads & Supports. Contra `milesmorales2`: etapa 1, objetivo: All Allies / Target ID: 72; etapa 1, efecto 2: — / «Increases all Basic Attacks by 70%» (ALL BASIC ATTACKS INCREASE); etapa 1, efecto 3: — / «Decreases basic damage received by 20%.» (Decreases all basic damage).
- Sword Master (`swordmaster`): es la base, y la regla es para uniformes. Contra `swordmaster1`: etapa 1, efecto 1: «Increases all Basic Defenses by 35%.» (ALL BASIC DEFENSES INCREASE) / «Increases all Basic Defenses by 50%.» (ALL BASIC DEFENSES INCREASE); etapa 1, efecto 2: — / «30% increase of HP.» (MAX HP ↑).
- Thane — Phoenix Force (`thane1`): su Leader Skill no es idéntica a la de su base. Contra `thane`: recarga: 20 s / 25 s.
- Winter Soldier — Marvel Studios' Thunderbolts* (`wintersoldier6`): su Leader Skill no es idéntica a la de su base. Contra `wintersoldier`, `wintersoldier1`, `wintersoldier2`, `wintersoldier3`, `wintersoldier4`: etapa 1, efecto 1: «45% increase of Physical Attack.» (PHYSICAL ATTACK ↑) / «30% increase of Physical Attack.» (PHYSICAL ATTACK ↑). Contra `wintersoldier5`: idéntica.
