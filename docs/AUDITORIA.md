# Auditoría de datos

Generado por `scripts/auditar.py` el 2026-09-24, sobre los datos del juego 12.2.5 (thanosvibs) y la wiki de Future Fight bajada en la misma sincronización.

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
- Textos de efecto con marcadores de plantilla sin resolver ($HEROSUBTYPE, $HEROCLASS...): 18 patrones, usados por 320 retratos. La app los muestra como "sin especificar en la fuente" en vez de inventar el valor.

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
- **Nivel de skills para Tier-4: guía 12 y wiki 10** — La guía pone "skills en Nv. 12" en el paso previo al Tier-4; la wiki pide Nv. 10 como requisito. No hay una fuente que diga cuál es el requisito vigente: puede que la guía recomiende más del mínimo. La hoja de ruta muestra los dos. ([THANO$VIB$ Beginner's Guide, parte 1](https://thanosvibs.money/beginners/1), [Future Fight Wiki — Tier-4](https://future-fight.fandom.com/wiki/Tier-4))
- **Tabla de efectos del artefacto en el sitio de thanosvibs** — En la sección Leads & Supports, el sitio muestra el tercer número de cada efecto de artefacto como duración ("0.2s"), con la columna "Instinct" corrida. Por la página Artifact de la wiki (Robbie Reyes, She-Hulk) ese número es el % adicional del instinto total, la duración va al final y, si el efecto acumula, el tope va antes de la duración. La app los muestra con ese significado. ([THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports), [THANO$VIB$ — Artifacts](https://thanosvibs.money/artifacts))
