# Auditoría de datos

Generado por `scripts/auditar.py` el 2026-10-05, sobre los datos del juego 12.2.5 (thanosvibs) y la wiki de Future Fight bajada en la misma sincronización.

La app muestra thanosvibs, salvo lo que el build corrige con aviso (sección 5). Esto marca dónde otra fuente dice otra cosa, con los dos valores; no corrige nada. La wiki la edita la comunidad y muchas páginas quedaron viejas (uniformes sin sección, valores de antes de un rebalanceo), así que una diferencia es algo para revisar en el juego, no un error confirmado de ninguna de las dos.

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
| Strikers (pestaña Striker de la wiki) | 7020 filas en 171 páginas | 2 filas que no se pudieron leer; 2 con más de 100% | 119 páginas sin la pestaña |
| Artefactos a 6★ (thanosvibs vs wiki) | 209 (+31 donde la wiki lista otro nivel de estrellas) | 17 | 10 sin fila en la wiki; 5 con niveles incompletos en thanosvibs |

Cobertura de la wiki: de 5887 skills (activas, Definitiva y Striker) de thanosvibs, 2270 (39%) se pudieron comparar; 1222 están en la página pero solo en la sección de otro uniforme, y el resto no aparece (sobre todo uniformes que la wiki no documenta). Infobox: 552 retratos con pestaña en la wiki, 305 sin pestaña de su uniforme y 31 de personajes sin infobox legible.

Catálogo de efectos (docs/CATALOGO.md): 228 etiquetas de skills y 72 stats de Leads & Supports y 26 de bonos de equipo en los datos; todos clasificados.

Liderazgos: el build deriva de la Leader Skill de la API el de 443 variantes que Leads & Supports no publica; 35 slots no se pudieron derivar (sección 12).

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

## 5. Lo que el build corrige de thanosvibs

El build corrige estos datos de thanosvibs con aviso, y la app usa el corregido.

### Restricciones de liderazgos y soportes

La fuente las clasifica mal; la ficha muestra la original.

- `thing3` (uniform): la fuente dice Allies "Fantastic Four"; se usa Ability "Los 4 Fantásticos".
- `thing4` (uniform): la fuente dice Allies "Fantastic Four"; se usa Ability "Los 4 Fantásticos".
- `weaponhex1` (uniform2): la fuente dice Type "Zombie"; se usa Ability "Zombi".
- `kang` (leader): la fuente dice Character "Kang"; se usa Character "Kang the Conqueror".
- `kang1` (leader): la fuente dice Character "Kang"; se usa Character "Kang the Conqueror".

### Nombres de C.T.P.

Va el nombre que escribe la ficha del C.T.P. en el juego. El id sigue siendo el de thanosvibs: es la clave del ícono, de la guía de armado y de lo que guarda la capa.

- `judgement`: thanosvibs dice «Judgement»; se usa «Judgment», como lo escribe el juego (MARVEL Future Fight — C.T.P. (Custom Gear, dentro del juego, octubre de 2026)).

### Texto de los artefactos

Va lo que dice la ficha del artefacto en el juego; la app marca la línea y dice lo que publica thanosvibs.

- `galactus` (Planet Eater): thanosvibs dice «Applies to: Self»; se usa «Applies to: Allies with Power Cosmic Ability», como dice el juego (MARVEL Future Fight — 아티팩트 도감 (los artefactos dentro del juego, en coreano; octubre de 2026)).

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
- **Nivel de skills para Tier-4: la guía de thanosvibs dice 12; el juego, 10** — La guía de thanosvibs pone "skills en Nv. 12" en el paso previo al Tier-4. Las skills llegan hasta el Nv. 10: la guía del juego dice que su nivel máximo sube con el del personaje hasta el 10 y pide todas en Nv. 10 para el Tier-4, como la wiki, y Ezequiel lo confirma. La hoja de ruta dice Nv. 10. ([THANO$VIB$ Beginner's Guide, parte 1](https://thanosvibs.money/beginners/1), [Future Fight Wiki — Tier-4](https://future-fight.fandom.com/wiki/Tier-4), MARVEL Future Fight — guía dentro del juego (contenidos, crecimiento e ítems, octubre de 2026))
- **Tabla de efectos del artefacto en el sitio de thanosvibs** — En la sección Leads & Supports, el sitio muestra el tercer número de cada efecto de artefacto como duración ("0.2s"), con la columna "Instinct" corrida. Por la página Artifact de la wiki (Robbie Reyes, She-Hulk) ese número es el % adicional del instinto total, la duración va al final y, si el efecto acumula, el tope va antes de la duración. La app los muestra con ese significado. ([THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports), [THANO$VIB$ — Artifacts](https://thanosvibs.money/artifacts))
- **Leads & Supports: reducciones de daño con signo positivo** — En 17 soportes, Leads & Supports publica la reducción de daño recibido con valor positivo: 16 «Basic Damage Received from Villains» y un «Physical Reflect Damage Received» (Black Dwarf, Dwarf Charge). La skill del mismo personaje dice siempre que reduce (Shuri, Panther God's Protection: +40 en Leads & Supports; «Decreases basic damage received from … faction by 40%» en la skill), y en otros soportes el mismo stat viene negativo. El catálogo de efectos los lee siempre como reducción. ([THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **API de skills: «Give Power» sin lo que otorga** — En 27 retratos, la skill trae «Give Power» («Acquires the following effect for … sec.») sin el efecto que sigue, y Leads & Supports dice cuál es: casi siempre «Remove All Debuffs» (Deadpool en Marvel's Savior, Odin, Thanos, Sentry, Blue Dragon, Gorr, Kang, entre otros), y también inmunidad a debuffs (Invisible Woman, First Steps), curación y reducción de daño (Jessica Jones, Jewel), curación (Groot, Bloom) o ataque físico (Toxin). La ficha muestra la skill como viene y el soporte con su efecto. ([THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters), [THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports))
- **API de skills: códigos en lugar de nombres** — Algunas descripciones traen un número donde va el nombre de un efecto o de un elemento, y la app los muestra como vienen: «Natural Enemy» («Increases damage dealt to targets with 206 effect by 50%»), «DURATION INCREASE», «ELEMENT CONVERSION», «Accumulate All True Element Damage Dealt», «REMOVE», «Selective Removal», «DEBUFF EFFECT ↓», «Counter Reflect» y «SET SKILL CD». Los de tres cifras son el id de una habilidad de la misma API (abilityId): 206 es «Removes all Debuffs», 401 «Mockery», 108 «SHOCK», 205 «WEB», 204 «SNARE» y 120 «PIERCE». 407 y 577 no son el id de ninguna habilidad de las skills; Leads & Supports nombra 407 «Debuff Removal (Instinct)» en el soporte de Kahhori (Hero's Decree). Los de cifras sueltas («1234 skill», «pure 23 damage») parecen listas de ranuras o de elementos. La wiki nombra otro: el «REMOVE» del Striker de Spider-Man le quita al rival sus buffs activos. Es probable que 407 sea el efecto de cinco artefactos, los de Aero, Punisher, Scarlet Spider, Domino y Yelena Belova («[P1]% chance to ignore all debuffs received, and an additional [P2]% of total Instinct»): es lo único de los datos que deja de lado los debuffs según el instinto. 577, del Striker de Winter Soldier, no tiene nombre en ninguna fuente que se pudo leer. ([THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters), [THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports), [THANO$VIB$ — Artifacts](https://thanosvibs.money/artifacts))
- **C.T.P.: thanosvibs contra el juego** — En el juego (la ficha de cada C.T.P., en inglés y en coreano), los números de los 15 C.T.P. coinciden con los de thanosvibs en 6★ y en los reforjados Mighty y Brilliant, en lo que se ve de cada ficha, salvo donde thanosvibs escribe un número fijo en vez de uno por rango, que en Brilliant cambia: Steel (Authority) dura 6 s, no 5; Beatdown dura 6 s, no 5 (Energy), y se recarga en 9 s, no en 10 (Energy y Transcendence); Penetration se recarga en 7 s, no en 8 (Regeneration y Transcendence). En Transcendence, thanosvibs no da la duración de Beatdown (5 s en Mighty, 6 s en Brilliant). thanosvibs redondea además 51,75% a 51,8% (Authority, Destruction, Energy y Transcendence) y 44,85% a 44,9% (Insight). La ficha en coreano deja ver más de la opción fija de los Brilliant, y coincide: Competition ignora el 65% de la reducción de daño de los jefes, Energy y Veteran suben 50% el daño de los golpes en cadena, Patience baja 90% el daño recibido por reflejo, Judgment baja 50% las resistencias, Insight sube 30% el daño básico del equipo a los Supervillanos, y Liberation da +32,2% a los ataques y defensas básicos y se activa con 15% al atacar. El texto difiere: los escudos de Regeneration y Veteran también bloquean el daño de instinto ("Blocks instinct damage"), que thanosvibs no dice; en Judgment, thanosvibs dice en los tres grados que la baja de resistencias ignora la inmunidad, y el juego no lo dice en 6★ ni en Mighty, y en Brilliant sí, donde agrega que se acumula hasta −50% (la línea se lee por su mitad de arriba); donde el juego dice "basic damage" (Energy, Destruction, Veteran, Rage, Greed e Insight), thanosvibs dice "damage"; Ambush (Greed) ignora la reducción de daño del rival ("damage decrease", como dice también el glosario de skills del juego), y thanosvibs dice reducción de defensa; Greed tiene en el juego dos opciones, que cambian qué par de clases recibe primero el aumento de daño, y thanosvibs muestra una; Greed vuelve a activarse 12 s después de que se termina su efecto ("Effect reactivates in 12 sec after removed"), y thanosvibs lo pone como una recarga de 12 s; Liberation sube el daño contra todos los instintos ("All damage dealt to all Instincts"), y thanosvibs lo parte en dos pares de instintos. Dentro del juego, el reforjado de Judgment se llama "Type Amplification" y dice subir el daño de las skills "de tipo", pero el glosario lo describe como "Element Amplification", que sube el ataque de las skills con elemento, y en coreano la ficha y el glosario dicen 속성 증폭 y 속성 스킬 (elemento): es un problema de traducción del inglés (Judgment es un C.T.P. de elemento). La app muestra el texto de thanosvibs. (MARVEL Future Fight — C.T.P. (Custom Gear, dentro del juego, octubre de 2026), MARVEL Future Fight — 특수 장비 도감 (los C.T.P. dentro del juego, en coreano, octubre de 2026), MARVEL Future Fight — Skill Name Glossary (guía dentro del juego, octubre de 2026), MARVEL Future Fight — 스킬 용어 사전 (el mismo glosario de skills, en coreano; dentro del juego, octubre de 2026), [THANO$VIB$ — C.T.P.s](https://thanosvibs.money/ctps))
- **C.T.P. reforjados: una de las dos opciones de reforjado (probable), y valores por debajo de los de la ficha** — La ficha de cada C.T.P. reforjado (Mighty y Brilliant) lista dos opciones de reforjado: un efecto con barra propia (Fury, Steel, Clash…) y, en la mayoría, +20% (Mighty) o +32% (Brilliant) a todos los ataques y defensas básicos; en Transcendence, Penetration y Beatdown, y en Insight y Liberation, dos efectos para todo el equipo. thanosvibs las publica como "special" y "generic". Los tres reforjados que se ven equipados traen una sola, seguida de la opción fija: Mephisto lleva un Conquest Mighty con Clash y un Competition Mighty con Fury, y Gorr, un Conquest Brilliant con Clash; y las notas del 4 de octubre de 2023 hablan de dos C.T.P. of Insight "with different reforge options". Es probable que cada C.T.P. reforjado lleve una de las dos. Las fichas aclaran además que muestran el valor más alto que se puede obtener ("Greatest Option Value Displayed"), y los equipados pueden tener menos, también en la opción fija: el Competition Mighty de Mephisto tiene Fury 40% y 40% (la ficha dice 60% y 60%), crítico y crítico de instinto +20,55% (34%) y daño crítico de instinto 31,63% (45%); el Conquest Brilliant de Gorr, Clash 70% y 60% con recarga de 8 s (90%, 80% y 7 s). La app muestra el texto de thanosvibs, sin números. (MARVEL Future Fight — C.T.P. (Custom Gear, dentro del juego, octubre de 2026), MARVEL Future Fight — 특수 장비 도감 (los C.T.P. dentro del juego, en coreano, octubre de 2026), MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026), [Foro oficial de MARVEL Future Fight — 10/4 Update Details (notas del 4 de octubre de 2023)](https://forum.netmarble.com/futurefight_en/view/2196/1799063), [THANO$VIB$ — C.T.P.s](https://thanosvibs.money/ctps))
- **C.T.P. por contenido: la guía del juego dice uno por personaje, y la ficha tiene una ranura para PvP y otra para PvE** — La guía del juego dice que cada personaje puede equipar como máximo un C.T.P. ("A max of 1 Custom Gear can be equipped per character"; en coreano, lo mismo). La ficha del personaje tiene ranuras numeradas, y cada una dice en qué contenido se aplica su C.T.P. ("Applied Content", 적용 콘텐츠): Gorr, con una sola ranura y un "+" al lado, lleva su Conquest Brilliant en PVE y en PVP; Mephisto, con dos, lleva un Conquest Mighty en PVP y un Competition Mighty en PVE, y el detalle de sus stats se ve por ranura. Al lado del contenido hay un botón para editarlo: es probable que el contenido de cada ranura lo elija el jugador. Las fichas de los C.T.P. no nombran contenidos, así que no es un dato del C.T.P. Qué modos cuentan como PVP y cuáles como PVE no se ve. La app recomienda un C.T.P. para PvP y otro para PvE y, en cada modo, usa el del tipo del modo (modos.json). (MARVEL Future Fight — guía dentro del juego (contenidos, crecimiento e ítems, octubre de 2026), MARVEL Future Fight — 가이드, 콘텐츠 사전 y 아이템 사전 (la guía dentro del juego, en coreano: contenidos, crecimiento e ítems; octubre de 2026), MARVEL Future Fight — C.T.P. (Custom Gear, dentro del juego, octubre de 2026), MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026))
- **Instinto: la regla de NamuWiki contra el infobox de la wiki** — Según NamuWiki, el instinto (en coreano 천성) depende de si el personaje es humano y de si es héroe o villano, y no cambia con el uniforme: humano y héroe, Justicia (정의); humano y villano, Crueldad (냉혹); no humano y héroe, Orden (질서); no humano y villano, Destrucción (파멸). Con la raza y el bando de la base que publica thanosvibs, la regla da el instinto del infobox en 268 de los 274 personajes que lo tienen y son héroes o villanos (Destroyer, Neutral, queda afuera). No lo da en Quicksilver, Scarlet Witch, Shadow Shell, Kahhori y Quasar (Wendell Vaughn), que tienen Orden, ni en Agent Venom, que tiene Crueldad. En Quicksilver y Scarlet Witch lo explica Netmarble: en las notas del 4 de noviembre de 2025 pasaron a «Human» y «Their Instinct remains as Order», así que el instinto no sigue a un cambio de raza.De los cuatro personajes cuya página contradice al infobox (sección 3), la regla da la categoría de la página en Agent Venom, Kahhori y Quasar (Justicia) y el infobox en Marvel Boy (Orden; es alienígena). A los 15 sin instinto, la regla les daría Justicia a Aero, Agent 13, Black Knight, Blue Marvel, Captain Marvel, Daredevil, Falcon, Human Torch, Invisible Woman y Wave; Orden a Gorgon; Crueldad a Mysterio y Vulture, y Destrucción a Stryfe y Supergiant. Por las seis excepciones, la regla no alcanza para afirmarlo, y la app no los completa. Desde el 15 de octubre de 2024 el juego filtra los personajes por instinto: ahí se pueden ver. ([NamuWiki — MARVEL 퓨처파이트/영웅 (en coreano)](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%EC%98%81%EC%9B%85), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters), [Foro oficial de MARVEL Future Fight — 11/4 Update Details (notas del 4 de noviembre de 2025)](https://forum.netmarble.com/futurefight_en/view/2196/1861240), [Foro oficial de MARVEL Future Fight — 10/15 Update Details (notas del 15 de octubre de 2024)](https://forum.netmarble.com/futurefight_en/view/2196/1825274))
- **Habilidad de World Boss: para qué sirve, y NamuWiki contra thanosvibs** — En World Boss, además de los tres del equipo se eligen cinco strikers, que suben stats del equipo, bajan los del rival y aparecen a pegar cuando se usa la skill cooperativa (NamuWiki). El bono de cada uno depende de su habilidad: Liderazgo (en coreano 영웅심, «heroísmo») sube 10% el daño a los Supervillanos, Agente ignora la evasión del objetivo con 20% de probabilidad y Fuerza (괴력) sube 8% el ataque físico, entre otras. Los personajes que NamuWiki pone en Liderazgo y en Agente tienen esa habilidad de World Boss en thanosvibs, incluida Daisy Johnson solo con el uniforme Modern (Quake): es la habilidad de World Boss de cada variante. En Fuerza, NamuWiki pone además a Luke Cage, She-Hulk, Hulk, Hulk (Amadeus Cho) y Thanos, que en thanosvibs tienen otra (Defensores, Radiación Gamma o Poder Cósmico); la sección de Radiación Gamma de NamuWiki está vacía. ([NamuWiki — MARVEL 퓨처파이트/월드 보스/스트라이커 (en coreano)](https://namu.wiki/w/MARVEL%20%ED%93%A8%EC%B2%98%ED%8C%8C%EC%9D%B4%ED%8A%B8/%EC%9B%94%EB%93%9C%20%EB%B3%B4%EC%8A%A4/%EC%8A%A4%ED%8A%B8%EB%9D%BC%EC%9D%B4%EC%BB%A4), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **Adaptation (Sentinel): el texto dejó de decir «element»** — La pasiva «Mutant Suppressor» de Sentinel (etiqueta Adaptation, 3 retratos) dice en thanosvibs «#% chance to become immune to the greatest damage received.», y no se sabía si era el golpe más fuerte o un tipo de daño. Las notas oficiales del 15 de septiembre de 2020 cambiaron ese texto («Previous: become immune to the greatest element damage received by a certain rate of chance») y aclararon «The Skill Info has been changed, and the skill effect is applied as previously». La inmunidad es al elemento del mayor daño recibido, y el catálogo lo dice así. ([Foro oficial de MARVEL Future Fight — 9/15 Update Details (notas del 15 de septiembre de 2020)](https://forum.netmarble.com/futurefight_en/view/2196/1645272), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **«Bonus Damage» de las pasivas de Tier-2: el daño adicional (probable)** — Las pasivas de Tier-2 con la etiqueta «SKILL AND BONUS DAMAGE ↑» dicen «Increases Skill damage by #%, increases Bonus Damage by #%.», y las skills no usan ese término: dicen, por ejemplo, «Physical Damage: #% of Physical Attack. Additional # Physical Damage.». Una guía de mecánicas de un jugador en el foro oficial (DarkGamer0, diciembre de 2018) los une: «The first part is the Skill Damage, the second part is the Bonus Damage; both of which get boosted by certain T2 passives.». No es oficial ni trae pruebas, pero coincide con la guía de thanosvibs, que llama «Additional Damage» a la segunda parte y dice que es la única que sube con el nivel de la skill. En inglés, «Bonus damage» nombra además el daño continuo de la maldición y de la pérdida. En el juego en coreano, la pasiva de Tier-2 de Mephisto — Master of Hell dice «스킬 피해량 40% 상승, 추가 피해량 40% 상승» (los valores de la API), y sus skills escriben la segunda parte del golpe «추가 화염 피해 672»: el coreano usa la misma palabra, 추가 (adicional), para las dos (capturas 255, 261 y 285 del 4 de octubre de 2026). Sigue siendo lo probable. ([Foro oficial de MARVEL Future Fight — «An explanation to some of the mechanics found in-game» (guía de un jugador, DarkGamer0, diciembre de 2018)](https://forum.netmarble.com/futurefight_en/view/85/1317588), [THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters), MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026))
- **Efectos repetidos en el equipo: en los C.T.P. vale el mayor; de los soportes no hay nada oficial** — Lo que dice Netmarble es de los C.T.P.: las notas del 7 de abril de 2026 arreglan que «the highest value was not applied when multiple identical C.T.P. effects were active simultaneously», y las del 4 de octubre de 2023, que si dos o más llevan C.T.P. of Insight con distinto reforjado se aplican los dos; el juego dice en Insight y en Liberation que su efecto para todo el equipo no se aplica dos veces. En las colecciones de equipo, de un personaje que está en varios temas vale solo la opción de colección más alta, y las opciones de equipo de todos los temas (enero de 2026). De los soportes no dice nada: una guía de un jugador de 2018 afirma, sin pruebas, que si dos compañeros tienen el mismo buff de equipo (crítico garantizado, reducción de daño) cada uno usa el suyo y el tercero el del líder, y que los aumentos del daño contra una facción y las bajas del daño recibido de ella sí se suman. La sinergia de la app cuenta cada soporte por quien lo da. ([Foro oficial de MARVEL Future Fight — 4/7 Update Details (notas del 7 de abril de 2026)](https://forum.netmarble.com/futurefight_en/view/2196/1867762), [Foro oficial de MARVEL Future Fight — 10/4 Update Details (notas del 4 de octubre de 2023)](https://forum.netmarble.com/futurefight_en/view/2196/1799063), MARVEL Future Fight — C.T.P. (Custom Gear, dentro del juego, octubre de 2026), [Foro oficial de MARVEL Future Fight — 1/20 Update Details (notas del 20 de enero de 2026)](https://forum.netmarble.com/futurefight_en/view/2196/1864090), [Foro oficial de MARVEL Future Fight — «An explanation to some of the mechanics found in-game» (guía de un jugador, DarkGamer0, diciembre de 2018)](https://forum.netmarble.com/futurefight_en/view/85/1317588))
- **Alliance Conquest: la guía en coreano y la inglesa dan reglas distintas de las defensas** — En el paso «2. 전투» (batalla) de Alliance Conquest, justo después de decir que los que conquistan una región quedan defendiéndola, la guía en coreano dice «연합원과 전투 중인 방어 병력은 공격할 수 없습니다» (traducción de Claude: no se puede atacar a una defensa que está peleando con alguien de la alianza), y la inglesa, en el mismo renglón, «Characters that are defending a region cannot be used to attack other regions». Son reglas distintas. El juego es de un estudio coreano (Netmarble), así que lo probable es que la inglesa sea una mala traducción; lo que dice, además, ya se sigue de la frase anterior: un personaje usado no vuelve hasta el reinicio. El coreano agrega que la región conquistada queda protegida «일정 시간동안» (por un tiempo; el inglés no lo dice). La app muestra la regla del coreano y aclara que la inglesa dice otra cosa. (MARVEL Future Fight — 가이드, 콘텐츠 사전 y 아이템 사전 (la guía dentro del juego, en coreano: contenidos, crecimiento e ítems; octubre de 2026), MARVEL Future Fight — guía dentro del juego (contenidos, crecimiento e ítems, octubre de 2026))
- **Amplificación de urus: la guía del juego habla de urus; el foro y thanosvibs, de ranuras** — La guía del juego, en inglés y en coreano, describe la amplificación sobre los urus equipados: «Uru Amplification can be used to increase the stats of equipped Uru» y «all equipped Uru will attempt amplification»; en coreano, «장착된 모든 강화 우루의 증폭을 시도» (traducción de Claude: se intenta amplificar todos los urus equipados), y el dibujo rotula el resultado «증폭된 강화 우루» (uru amplificado). Lo que se cargó del foro oficial (las notas de la 4.0, de abril de 2018, y la guía de urus de diciembre de 2021) dice que lo que se amplifica es la ranura y que se puede amplificar sin urus, y la guía de thanosvibs también habla de ranuras. Que repetir pueda quitarle la amplificación a un uru («has a chance of losing its amplification»; «증폭이 해제될 수도 있습니다») no contradice al foro: cada intento vuelve a sortear qué ranuras quedan amplificadas. Se resuelve en el juego, amplificando una pieza en +20 sin urus. La app dice lo del foro y que la guía del juego habla de urus. (MARVEL Future Fight — guía dentro del juego (contenidos, crecimiento e ítems, octubre de 2026), MARVEL Future Fight — 가이드, 콘텐츠 사전 y 아이템 사전 (la guía dentro del juego, en coreano: contenidos, crecimiento e ítems; octubre de 2026), [Foro oficial de MARVEL Future Fight — 4.0 Update Details (notas de abril de 2018)](https://forum.netmarble.com/futurefight_en/view/2196/1118083), [Foro oficial de MARVEL Future Fight — Enchanted Uru Guide (guía oficial, diciembre de 2021)](https://forum.netmarble.com/futurefight_en/view/2524/1735745), [THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **La guía del juego: lo que el coreano dice distinto del inglés** — Además de lo de Alliance Conquest (hallazgo aparte), la guía del juego en coreano y la inglesa difieren en cinco cosas que la app no muestra. Mejora de uniforme: el inglés dice «You must have a Specific Uniform of another character to do this»; el coreano, «다른 영웅의 특정 유니폼을 가지고 있지 않으면 강화해도 추가 옵션을 획득할 수 없습니다» (traducción de Claude: si no tenés el uniforme de otro personaje, mejorarlo no da la opción adicional), que es lo que dice la guía de thanosvibs de las opciones de uniforme. Epic Quest: en inglés, el protagonista se recibe al empezarla («When you begin an Epic Quest»); en coreano, al completarla («에픽 퀘스트를 완료하면»). Combinar ISO-8: el inglés pide una piedra en +5 («If a specific ISO-8 has been enhanced to +5, you may combine 2»), el coreano dos («최대 단계(+5)까지 강화한 ISO-8 두 개»), y el dibujo, en los dos idiomas, muestra las dos en +5; lo curado en guia.json (iso.mejora, que la app no muestra) dice «con la primera en +5». Piedras de invocación de Dimension Rift: el glosario de ítems en inglés dice que salen de Story («Summon Stones can be acquired in Story»); el coreano, de Dimension Rift (획득처: 차원의 틈), como el diccionario de contenidos en los dos idiomas. Trascender el Potencial: el inglés dice «can Awaken their Potential» donde el coreano dice 잠재력 초월 (trascender). (MARVEL Future Fight — guía dentro del juego (contenidos, crecimiento e ítems, octubre de 2026), MARVEL Future Fight — 가이드, 콘텐츠 사전 y 아이템 사전 (la guía dentro del juego, en coreano: contenidos, crecimiento e ítems; octubre de 2026), [THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **C.T.P. of Judgment: el juego y thanosvibs lo escriben distinto, y la app usa el del juego** — El juego escribe «C.T.P. of Judgment» en la ficha de los tres grados (6★, Mighty y Brilliant); thanosvibs, «Judgement». La app usa el del juego (Ezequiel, 5 de octubre de 2026): el build corrige el nombre de thanosvibs con aviso, y la sección 5 lo lista. El id (judgement) sigue siendo el de thanosvibs, porque es la clave del ícono, de la guía de armado y de lo que guarda la capa. Los textos de las fuentes que lo nombran van como los escriben: las descripciones y las rotaciones de thanosvibs, y la leyenda de la guía de armado de Cynicalex («Elemental characters: Judgement»). En coreano es 심판의 C.T.P. (심판, «juicio»), así que la captura en coreano no decide la ortografía inglesa. (MARVEL Future Fight — C.T.P. (Custom Gear, dentro del juego, octubre de 2026), MARVEL Future Fight — 특수 장비 도감 (los C.T.P. dentro del juego, en coreano, octubre de 2026), [THANO$VIB$ — C.T.P.s](https://thanosvibs.money/ctps), [Cynicalex Mega Guides — Character Building Guide](https://docs.google.com/spreadsheets/d/1H0Hcl9oVZV9gA266xkJAqPv5bD1qwqhC5NeVbLj_-FE/edit?gid=190850363#gid=190850363))
- **Mephisto: Leads & Supports publica para la base el liderazgo de Master of Hell (probable)** — En el juego, el liderazgo de Mephisto con el uniforme Master of Hell (지옥 군주, Lord of Hell) tiene dos partes para los aliados del bando Supervillano: fuego +30%, sin activación, y, al recibir un debuff, quitar todos los debuffs (12 s), con recarga de 20 s. La segunda es el «Give Power» que la API no publica, y la app la toma del juego. Son, valor por valor, los dos liderazgos que Leads & Supports publica para la base (Soul Contract), cuya Leader Skill en la API es otra: una sola parte, al recibir un debuff, con quitar los debuffs 11 s y fuego +30% 15 s, y recarga de 20 s (la verificación de la sección 12 la lista como distinta). Además, el efecto de uniforme de Master of Hell dice que cambia el efecto de Soul Contract («영혼의 계약 스킬의 효과 변경»): en el juego, la base no tiene el liderazgo del uniforme. Es probable que Leads & Supports le haya puesto a la base el liderazgo de Master of Hell. Ninguna captura muestra Soul Contract en el juego, que lo confirmaría. La app muestra para la base lo que publica Leads & Supports. (MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters), [THANO$VIB$ — Leads & Supports](https://thanosvibs.money/supports))
- **Armageddon (Young Apocalypse): en el juego, su quemadura también baja las defensas** — La Definitiva de Apocalypse con el uniforme Marvel Animation's X-Men '97 (Young Apocalypse), Armageddon, aplica en el juego una quemadura que además baja todas las defensas básicas: «화상 : 1초마다 30% 추가 화염 피해, 10%만큼 모든 일반 방어력을 감소(5 초)» (traducción de Claude: quemadura, 30% de daño de fuego adicional por segundo y todas las defensas básicas −10%, por 5 s; captura 295 del 4 de octubre de 2026). La API de skills dice solo «Burn: Deals additional 30% Flame Damage every 1 sec.» (5 s), así que la app no cuenta la baja de defensas. (MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **Las habilidades dan un efecto propio, según el juego** — En el detalle de stats del personaje (영웅 상세 정보), cada ícono de habilidad abre un globo con un efecto para él (capturas del 4 de octubre de 2026; las 301 a 303, que se habían tomado por bonos de equipo, son estos globos): Durabilidad (내구력), todas las defensas básicas +5%; Maldad Pura (사악), daño básico a la facción SUPER HERO (영웅 진영) +4%; Movimiento Rápido (고속 이동), velocidad de movimiento +3%, en Apocalypse — Marvel Animation's X-Men '97 (Young Apocalypse); Magia (마법), ataque de energía +4%; Fuego Infernal (지옥불), daño de fuego +10%, y Maldad Pura, en Mephisto — Master of Hell. Las tres de cada uno son sus habilidades en la app. thanosvibs no lo publica y la app no lo tiene: las habilidades solo restringen liderazgos, soportes y artefactos. No se sabe en qué contenidos vale ni qué dan las demás habilidades. (MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026), [THANO$VIB$ — Characters (skills de cada personaje)](https://thanosvibs.money/characters))
- **Strikers de Mephisto: el juego tiene al menos 91; la app, 90** — La pestaña Striker de la ficha de Mephisto en el juego (capturas 379 a 386 del 4 de octubre de 2026) muestra al menos 91 strikers distintos: son ocho capturas, siete de 12 retratos y una de 11, y la última fila de la séptima se repite como primera de la octava (comparadas por píxeles). La grilla, de a cuatro, termina en una fila de tres; si el desplazamiento salteó filas, hay más. No pueden ser los 90 que la app toma de la pestaña Striker de la wiki (41 cuando él ataca y 49 cuando lo atacan): a la app le falta al menos uno. Las capturas muestran solo retratos, así que no se sabe cuál. La cabecera de la pestaña confirma que el striker tiene que ir en el mismo equipo: «같은 팀으로 편성할 경우 특수 조건에서 발동되며» (traducción de Claude: si se lo arma en el mismo equipo, se activa en condiciones especiales). (MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026), Future Fight Wiki — pestaña Striker de cada personaje)
- **Opciones de uniforme: en Mítico, el juego muestra ataques y defensas +40%** — Con el uniforme Master of Hell de Mephisto en el grado más alto (신화, Mítico: «최고 등급»), la pantalla de opciones del uniforme muestra, arriba de las cinco opciones, «모든 일반 공격력 상승 +40%» y «모든 일반 방어력 상승 +40%»: todos los ataques y todas las defensas básicas +40% (captura 277 del 4 de octubre de 2026). La nota de la app sobre la mejora del uniforme, de la guía de thanosvibs, dice +2% por mejora (+3% en los de costo doble). La app no lo explica. (MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026), [THANO$VIB$ Beginner's Guide, parte 3](https://thanosvibs.money/beginners/3))
- **Artefacto de Annihilus: el juego dice que se recarga en 300 s, y la app no lo tiene** — La ficha del artefacto de Annihilus en el códice de artefactos del juego (아티팩트 도감: 네거티브 존의 지배자, Lord of the Negative Zone; captura 211 del 4 de octubre de 2026) termina con «재사용 대기시간 300초»: se recarga en 300 s. Antes dice lo mismo que thanosvibs (al morir, revive con 80% de la vida, más 0,5% del instinto total, hasta 100%). thanosvibs no publica la recarga, así que la app no la muestra. La página Artifact de la wiki trae un 300 que thanosvibs no tiene (sección 6): es probable que sea esta recarga. (MARVEL Future Fight — 아티팩트 도감 (los artefactos dentro del juego, en coreano; octubre de 2026), [THANO$VIB$ — Artifacts](https://thanosvibs.money/artifacts))
- **Red Skull — The Crimson Fall y Sister Grimm — Princess Tsukimi: la versión sale de /api/updates, y la fecha difiere en uno o dos días** — /api/uniforms de thanosvibs no trae la versión de estos dos uniformes (el 5 de octubre de 2026); /api/updates los pone en la 12.2.5 («2026 Welcome Autumn»), y en los otros 596 uniformes coincide con /api/uniforms. El build toma la versión de /api/updates para todos. Las notas oficiales dicen que los dos uniformes llegan con el parche del 21 de septiembre de 2026 (20:00 PDT; el 22 a las 3:00 UTC); thanosvibs le pone a la 12.2.5 el 23 de septiembre. Las notas no dan número de versión. La app no usa fechas: con «Solo el último uniforme», son el último uniforme de su personaje. ([THANO$VIB$ — Updates (la versión del juego en que salió cada personaje y uniforme)](https://thanosvibs.money/updates), [THANO$VIB$ — Uniforms](https://thanosvibs.money/uniforms), [Foro oficial de MARVEL Future Fight — 9/21 Patch Details (notas del 21 de septiembre de 2026)](https://forum.netmarble.com/futurefight_en/view/2196/1896518))

## 8. Facción, tipo o raza que la fuente no publica

thanosvibs publica 249 efectos con un marcador (`$HEROSUBTYPE1`, `$HEROCLASS1`) en vez de la facción, el tipo, la raza o la habilidad a la que se refieren (`Increases basic damage dealt to $HEROSUBTYPE1 faction by 30%`). El build los completa en este orden (Ezequiel, 3 de octubre de 2026): la tabla a mano (scripts/contenido/marcadores.csv); Leads & Supports, en los slots de la misma skill (Leader Skill: `leader` y `leader2`; Passive: `passive` y `passive2`; Tier-2 Passive: `t2` y `t22`; Uniform Passive: `uniform` y `uniform2`), con «Basic Damage Dealt to …» o «Basic Damage Received from …» en el mismo sentido, el mismo porcentaje (el recibido, sin el signo) y un grupo de la clase que pide el texto, y la wiki: la misma skill con el mismo porcentaje, en el mismo sentido (daño infligido o recibido). Si la skill trae el mismo efecto varias veces, la fuente tiene que dar tantos valores distintos como efectos, y se asignan en el orden en que aparecen. En la ficha, el valor completado va subrayado y dice de dónde salió.

De los 249: 4 a mano, 131 de Leads & Supports, 38 de la wiki y 76 sin resolver (la app los muestra "sin especificar").

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

Cada etiqueta de efecto de las skills y cada stat de Leads & Supports y de los bonos de equipo apunta a efectos del catálogo (scripts/contenido/catalogo.json; docs/CATALOGO.md lo muestra entero). Lo que thanosvibs o la wiki agreguen y el catálogo no tenga se lista acá hasta que se clasifique a mano; mientras tanto, la app lo cuenta para todos y lo dice.

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

### Probabilidades imposibles (2)

Más de 100%: un error de la wiki. No se corrige ni se topea: la app la muestra tal cual, marcada como dato imposible de la fuente. Hay que verla en el juego.

- Daken: Doctor Octopus, 219% cuando lo atacan
- Molecule Man: Morgan le Fay, 120% cuando él ataca

## 12. Liderazgos que Leads & Supports no publica

Leads & Supports de thanosvibs no publica el liderazgo de todas las variantes. Los que no publica los deriva el build de la Leader Skill de la API de skills (Ezequiel, 4 de octubre de 2026; scripts/liderazgos.py, explicado en docs/MODELO.md) y van en los datos con `"src": "api"`: la app dice «según la skill del juego». La Leader Skill se parte en los dos slots de liderazgo de Leads & Supports, y cada efecto, cada activación y la condición de cada efecto pasan a lo que publica Leads & Supports según las variantes que tienen las dos cosas (la correspondencia aprendida, abajo) o, lo que Leads & Supports no publica en ningún liderazgo, según scripts/contenido/liderazgos_api.json (la correspondencia a mano: un stat del catálogo para cada efecto, y la activación con el texto de la API). Todo o nada por slot: si algo no cierra, ese slot no se deriva y va abajo con su motivo. Lo derivado no lleva «Notable», que es una marca de thanosvibs que la API no tiene.

411 variantes tienen liderazgo de Leads & Supports y 477 no. El build deriva el de 443 (461 slots); 35 slots, de 35 variantes, no se pudieron derivar.

### Correspondencia aprendida

De las variantes con liderazgo de Leads & Supports, efecto por efecto: lo que da cada uno de los 34 efectos de la API (el número del texto, con su signo) y en cuántas variantes se ve.

| Efecto de la API | Leads & Supports | Variantes |
|---|---|---|
| «Increases all Basic Attacks by #%» (ALL BASIC ATTACKS INCREASE) | All Basic Attacks +n1 | 117 |
| «#% increase of Energy Attack.» (ENERGY ATTACK ↑) | Energy Attack +n1 | 70 |
| «#% increase of Physical Attack.» (PHYSICAL ATTACK ↑) | Physical Attack +n1 | 57 |
| «Ignores target's Dodge Rate by #%.» (IGNORE DODGE) | Ignore Dodge +n1 | 39 |
| «Removes all Debuffs.» (Removes all Debuffs. ) | Remove All Debuffs | 37 |
| «#% increase of HP.» (MAX HP ↑) | HP +n1 | 36 |
| «Increases all Basic Defenses by #%.» (ALL BASIC DEFENSES INCREASE) | All Basic Defenses +n1 | 27 |
| «Increases all Basic Attacks by #%, all Basic Defenses by #%, and all Speeds by #%.» (Increases all basic stats) | All Basic Attacks +n1, All Basic Defenses +n2, All Speeds +n3 | 16 |
| «Increases Flame Damage by #%.» (FLAME DAMAGE ↑) | Fire Damage +n1 | 14 |
| «Increases All Debuffs effect by #%.» (DEBUFF EFFECT ↑) | All Debuffs Effect +n1 | 10 |
| «Decreases Debuff Duration by #%.» (CROWD CONTROL TIME ↓) | Debuff Duration −n1 | 9 |
| «Increases all Basic Attacks by #%.» (Increases all Basic Attacks) | All Basic Attacks +n1 | 7 |
| «Critical Damage increases by #%.» (CRITICAL DAMAGE ↑) | Critical Damage +n1 | 6 |
| «Critical Rate increases by #%.» (CRITICAL RATE ↑) | Critical Rate +n1 | 6 |
| «Increases Lightning Damage by #%.» (LIGHTNING DAMAGE ↑) | Lightning Damage +n1 | 6 |
| «#% increase of Energy Defense.» (ENERGY DEFENSE ↑) | Energy Defense +n1 | 5 |
| «Dodge Rate increases by #%.» (DODGE ↑) | Dodge +n1 | 5 |
| «Increases All Speeds by #%.» (ALL SPEED ↑) | All Speeds +n1 | 5 |
| «Increases basic damage dealt to $HEROSUBTYPE# types by #%.» (INCREASES BASIC DAMAGE BASED ON CHARACTER'S GENDER), con Masculino | Basic Damage Dealt to Males +n2 | 5 |
| «Immunity to BURN Effect.» (RESIST) | Burn Immunity | 4 |
| «Increases Mind Resist by #%.» (MIND RESIST ↑) | Mind Resist +n1 | 4 |
| «Creates a Shield equal to #% of Max HP» (SHIELD) | Max HP Shield +n1 | 2 |
| «Increases All Resistances by #%.» (ALL RESISTANCE ↑) | All Resistances +n1 | 2 |
| «Increases Mind Damage by #%.» (MIND DAMAGE ↑) | Mind Damage +n1 | 2 |
| «Recovers #% of HP.» (HP RECOVERY) | Heal +n1 | 2 |
| «#% chance to become immune to Physical Damage.» (PHYSICAL IMMUNITY) | Physical Immunity Chance +n1 | 1 |
| «#% increase of Recovery Rate.» (RECOVERY RATE ↑) | Recovery Rate +n1 | 1 |
| «Decreases Chain Hit damage by #% when attacked.» (CHAIN HIT DMG RECEIVED ↓) | Chain Hit Damage Received −n1 | 1 |
| «Decreases Skill Cooldown by #%.» (COOLDOWN DURATION ↓) | Skill Cooldown −n1 | 1 |
| «Ignores Damage Increase/Decrease effect between self and opposing faction» (Ignores Damage Increase effect between factions) | Ignores Damage Increase/Decrease Effect Between Self and Opposing Faction | 1 |
| «Increases Cold Damage by #%.» (COLD DAMAGE ↑) | Cold Damage +n1 | 1 |
| «Increases Poison Damage by #%.» (POISON DAMAGE ↑) | Poison Damage +n1 | 1 |
| «Increases basic damage dealt to $HEROSUBTYPE# faction by #%.» (Increases basic damage based on character's faction), con Superhéroe | Basic Damage Dealt to Heroes +n2 | 1 |
| «Increases basic damage dealt to boss types by #%.» (Increases basic damage when attacking boss types) | Basic Damage Dealt to Boss Types +n1 | 1 |

`n1`, `n2`...: el primer número del texto, el segundo... La duración es la del efecto, si la publica.

Activaciones: «when HP is below 99%» → «When HP is below 99%» (2 variantes); «when debuffed» → «When Debuffed» (37 variantes).

Condición de cada efecto: «All Allies\nActivates when: Combat Type Ally enters» → when 1 Combat, when 2 Combats, when 3 Combats (2 variantes); «Self\nActivates when: Mutant Ally enters» → when 1 Mutant, when 2 Mutants, when 3 Mutants (1 variante).

### Correspondencia a mano

De scripts/contenido/liderazgos_api.json: lo que Leads & Supports no publica en ningún liderazgo. Cada efecto, con su texto de la API, da un stat del catálogo con el número del texto, y cada activación va con el texto de la API. Variantes: las que lo tienen en la Leader Skill.

| Efecto de la API | Stat | Variantes |
|---|---|---|
| «Attack Speed increases by #%.» (ATTACK SPEED ↑) | Attack Speed +n1 | 8 |
| «Increases Flame Resist by #%.» (FLAME RESIST ↑) | Fire Resist +n1 | 14 |
| «#% Ignore Defense» (IGNORE DEFENSE) | Ignore Defense +n1 | 2 |
| «Increases Lightning Resist by #%.» (LIGHTNING RESIST ↑) | Lightning Resist +n1 | 13 |
| «#% increase of Physical Defense.» (PHYSICAL DEFENSE ↑) | Physical Defense +n1 | 24 |
| «Super Armor, increases all Basic Defenses by #%.» (SUPER ARMOR) | Super Armor, All Basic Defenses +n1 | 3 |

Activaciones: «#% chance when attacking» (12 variantes); «#% rate when dodging» (5 variantes); «#% rate when hit» (27 variantes); «When enemies are below #% HP,» (1 variante); «when dealing Critical Attack» (15 variantes); «when dodging» (4 variantes); «when HP is below #%» (3 variantes); «when tagging» (15 variantes).

«Give Power» que dice el juego: la API no publica qué otorga la Leader Skill, y la ficha del juego sí. El slot lleva la restricción del objetivo de la API y, de lo que dice el juego, los efectos, la activación y la recarga; la app cita su fuente.

- Mephisto — Master of Hell (`mephisto1`), Lord of Hell: `leader2` Remove All Debuffs (12 s) — para Side: Supervillano, When Debuffed, recarga 20 s. MARVEL Future Fight — 영웅 정보 (la ficha de personaje dentro del juego, en coreano: skills, uniforme, C.T.P., artefacto y strikers; octubre de 2026): La ficha de Mephisto con el uniforme Master of Hell, 지옥 군주 (리더 스킬 Lv.6), renglón por renglón: «적용 대상: 빌런 진영인 팀원만 / · 화염 피해량 +30% 상승 / 발동 확률: 상태 이상에 걸렸을 때 / 적용 대상: 빌런 진영인 팀원만 / · 모든 상태 이상 제거(12 초) / 재사용 대기시간 20초» (traducción de Claude: para los integrantes del bando Villano, daño de fuego +30%; y, al recibir un debuff, para los mismos, quitar todos los debuffs por 12 s, con recarga de 20 s). Capturas 253, 269 y 286 del 4 de octubre de 2026.

### Verificación contra Leads & Supports

Cada slot de liderazgo de Leads & Supports contra el que la misma regla deriva de su Leader Skill, en stats, valores, duración, condición, restricción, activación y recarga (no en el nombre ni en «Notable»): de 448 slots, 394 iguales, 5 distintos, 47 que no se pueden derivar, 2 que la Leader Skill no da aparte.

Distintos (lo derivado / Leads & Supports):

- Black Swan (`blackswan`), `leader`: recarga: 25 s / 20 s.
- Drax (`drax3`, `drax2`), `leader`: efectos: HP +45% (when 1 Combat), HP +55% (when 2 Combats), HP +65% (when 3 Combats) / HP +45%, HP +55%, HP +65%.
- Mephisto (`mephisto`), `leader`: activación: When Debuffed / ninguna; recarga: 20 s / ninguna; efectos: Remove All Debuffs (11 s), Fire Damage +30% (15 s) / Fire Damage +30%.
- The Hood (`thehood`), `leader`: restricción: Side: Supervillano / ninguna.

No se pueden derivar:

- Arachknight — Arachknight 2099 (`arachknight1`), `leader`: la API no dice a quiénes llega («Infinity Warps Allies\nActivates when: Infinity Warps type Ally enters»).
- Blue Dragon (`bluedragon`, `bluedragon1`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Deadpool — April Pools (`deadpool6`), `leader`: la API no dice a quiénes llega («Target ID: 88»).
- Deadpool — April Pools (`deadpool6`), `leader2`: la API no dice a quiénes llega («Target ID: 88»).
- Deadpool — Marvel Studios' Deadpool & Wolverine (`deadpool8`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Gorr (`gorr1`, `gorr2`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Hope Summers (`hopesummers`), `leader`: la API no dice a quiénes llega («Target ID: 142»).
- Hope Summers (`hopesummers`), `leader2`: la API no dice a quiénes llega («Target ID: 142»).
- Hulkbuster — Celestial Hulkbuster (`hulkbuster4`), `leader`: la API no dice a quiénes llega («Target ID: 3»).
- Hulkbuster — Celestial Hulkbuster (`hulkbuster4`), `leader2`: la API no dice a quiénes llega («Target ID: 3»).
- Hulkbuster (Iron Man Mark 44) — 3099 (`hulkbuster3`), `leader`: la API no dice a quiénes llega («Target ID: 3»).
- Hulkbuster (Iron Man Mark 44) — 3099 (`hulkbuster3`), `leader2`: la API no dice a quiénes llega («Target ID: 3»).
- Invisible Woman — Classic (`invisiblewoman2`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Immunity to all Debuffs.» (IMMUNE).
- Kang the Conqueror (`kang`, `kang1`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Katy (`katy`), `leader`: la API no dice a quiénes llega («Target ID: 89»).
- Katy (`katy`), `leader2`: la API no dice a quiénes llega («Target ID: 89»).
- Maya Lopez — Marvel Studios' Hawkeye (`echo1`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Maya Lopez (Echo) — Marvel Studios' Echo (`echo2`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Molecule Man (`moleculeman`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Odin (`odin2`, `odin3`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Quasar (Wendell Vaughn) (`wendellvaughn`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Rachel Summers — X-Men: Days of Future Past (`rachelsummers1`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Sentry — Merged (`sentry1`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Sleeper (`sleeper`), `leader`: la API no dice a quiénes llega («Target ID: 42»).
- Sleeper (`sleeper`), `leader2`: la API no dice a quiénes llega («Target ID: 42»).
- Spider-Man (Miles Morales) — Absolute Carnage (`milesmorales2`), `leader`: la API no dice a quiénes llega («Target ID: 72»).
- Spider-Man (Miles Morales) — Anniversary Special (`milesmorales3`), `leader`: la API no dice a quiénes llega («Target ID: 10»).
- Spider-Man (Miles Morales) — Absolute Carnage (`milesmorales2`), `leader2`: la API no dice a quiénes llega («Target ID: 72»).
- Spider-Man (Miles Morales) — Anniversary Special (`milesmorales3`), `leader2`: la API no dice a quiénes llega («Target ID: 10»).
- Spider-Woman — Spider-Man: Across the Spider-Verse (`spiderwoman1`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Thanos (`thanos7`, `thanos6`, `thanos5`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Victorious (`victorious`, `victorious1`), `leader`: la API no dice a quiénes llega («Target ID: 183»).
- Victorious (`victorious`, `victorious1`), `leader2`: la API no dice a quiénes llega («Target ID: 183»).
- Vision — Marvel Studios' WandaVision (`vision3`), `leader`: la API no dice a quiénes llega («Target ID: 140»).
- Vision — Marvel Studios' WandaVision (`vision3`), `leader2`: la API no dice a quiénes llega («Target ID: 140»).
- Wave (`wave`, `wave1`), `leader`: la API no dice a quiénes llega («Target ID: 198»).
- Wave (`wave`, `wave1`), `leader2`: la API no dice a quiénes llega («Target ID: 198»).

Solo en Leads & Supports:

- Invisible Woman — Classic (`invisiblewoman2`), `leader2`.
- Mephisto (`mephisto`), `leader2`.

### Sin derivar (35 slots en 35 variantes)

Variantes sin liderazgo de Leads & Supports con un slot de su Leader Skill que no se pudo derivar, con todos sus motivos. En docs/COMPLETITUD.md son el faltante «Liderazgo sin completar».

Por motivo (un slot puede tener más de uno): efecto sin stat, 35; «Give Power», 1. Van juntas las variantes de un personaje con los mismos motivos.

Efectos sin stat (no están en el catálogo o falta cargarlos a mano), con los slots que dejan sin derivar: «30% chance to become immune to Cold Damage.» (COLD IMMUNITY), 6; «Bleed: Deals additional 10% Damage every 0.7 sec. (Removes Elasticity)» (BLEED), 5; «Creates an energy Shield equal to 20% of Max HP» (ENERGY SHIELD), 4; «Creates a physical Shield equal to 30% of Max HP» (PHYSICAL SHIELD), 3; «Creates an energy Shield equal to 50% of Max HP» (ENERGY SHIELD), 3; «Recovers HP equal to 8% of damage dealt to a target<br>Cannot recover more than 0.5% HP each time damage is dealt.» (HP STEAL), 3; «100% chance to grant All Damage Immunity» (ALL DAMAGE IMMUNE), 2; «Creates an energy Shield equal to 30% of Max HP» (ENERGY SHIELD), 2; «Creates an energy Shield equal to 60% of Max HP» (ENERGY SHIELD), 2; «Paralyze» (PARALYZE), 2; «Immunity to BLEED Effect.» (RESIST), 1; «Immunity to Fracture Effect.» (RESIST), 1; «Increases Poison Resist by 50%.» (POISON RESIST ↑), 1.

- Blade (`blade`, `blade1`, `blade2`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Recovers HP equal to 8% of damage dealt to a target<br>Cannot recover more than 0.5% HP each time damage is dealt.» (HP STEAL).
- Captain America (Sharon Rogers) (`sharonrogers`, `sharonrogers2`, `sharonrogers1`, `sharonrogers3`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates an energy Shield equal to 20% of Max HP» (ENERGY SHIELD).
- Captain America (Sharon Rogers) (`sharonrogers6`, `sharonrogers4`, `sharonrogers5`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates an energy Shield equal to 50% of Max HP» (ENERGY SHIELD).
- Daisy Johnson (`daisyjohnson`, `daisyjohnson2`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates a physical Shield equal to 30% of Max HP» (PHYSICAL SHIELD).
- Green Goblin (`greengoblin`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Increases Poison Resist by 50%.» (POISON RESIST ↑).
- Hydro-Man (`hydroman`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Immunity to BLEED Effect.» (RESIST); un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Immunity to Fracture Effect.» (RESIST).
- Luna Snow (`lunasnow`, `lunasnow1`, `lunasnow2`, `lunasnow3`, `lunasnow5`, `lunasnow4`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «30% chance to become immune to Cold Damage.» (COLD IMMUNITY).
- Quake — Modern (`daisyjohnson1`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates a physical Shield equal to 30% of Max HP» (PHYSICAL SHIELD).
- Sentry — Marvel Studios' Thunderbolts* (`sentry2`), `leader2`: otorga un efecto que la API no dice, por un tiempo que no publica («Give Power», $TIME).
- Silk (`silk`, `silk2`, `silk1`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Bleed: Deals additional 10% Damage every 0.7 sec. (Removes Elasticity)» (BLEED).
- Sister Grimm (`sistergrimm`, `sistergrimm1`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates an energy Shield equal to 30% of Max HP» (ENERGY SHIELD).
- Sister Grimm (`sistergrimm3`, `sistergrimm2`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Creates an energy Shield equal to 60% of Max HP» (ENERGY SHIELD).
- White Tiger (`whitetiger`, `whitetiger1`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Bleed: Deals additional 10% Damage every 0.7 sec. (Removes Elasticity)» (BLEED).
- Wong (`wong2`, `wong3`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «100% chance to grant All Damage Immunity» (ALL DAMAGE IMMUNE).
- Yellowjacket (`yellowjacket`, `yellowjacket1`), `leader`: un efecto sin stat (no se aprende de Leads & Supports ni está en scripts/contenido/liderazgos_api.json): «Paralyze» (PARALYZE).

### Derivados (443 variantes)

Van juntas las variantes de un personaje con el mismo liderazgo derivado.

- Absorbing Man (`absorbingman`, `absorbingman1`): `leader` Physical Defense +45%.
- Adam Warlock (`adamwarlock`, `adamwarlock1`, `adamwarlock2`): `leader` Energy Defense +60%.
- Aero (`aero`, `aero1`): `leader` All Speeds +6%.
- Agent 13 (`sharoncarter`, `sharoncarter1`): `leader` Skill Cooldown −24%.
- Amadeus Cho — Heroic Age (`amadeuscho3`): `leader` Critical Rate +6%, Critical Damage +6%.
- Angela (`angela`, `angela2`, `angela3`, `angela1`): `leader` Physical Defense +30%.
- Annihilus (`annihilus`): `leader` All Speeds +6%; `leader2` Poison Damage +60% — para Character: Annihilus.
- Ant-Man (`antman`, `antman6`, `antman1`, `antman3`, `antman4`, `antman2`, `antman5`): `leader` All Speeds +9%.
- Arachknight (`arachknight`): `leader` Dodge +6%, Debuff Duration −24%.
- Athena (`athena`): `leader` All Basic Defenses +24%.
- Baron Mordo (`baronmordo`): `leader` Dodge +6%.
- Black Cat (`blackcat`, `blackcat2`, `blackcat1`): `leader` All Speeds +6%.
- Black Dwarf (`blackdwarf`): `leader` Physical Immunity Chance +100% (8 s) — 30% rate when hit, recarga 15 s.
- Black Dwarf — Dark Obsidian Armor (`blackdwarf2`): `leader` Physical Immunity Chance +100% (10 s) — 50% rate when hit, recarga 15 s.
- Black Knight (`blackknight`): `leader` Debuff Duration −24%.
- Black Panther (`blackpanther`, `blackpanther3`, `blackpanther4`, `blackpanther2`, `blackpanther1`): `leader` Critical Rate +15%.
- Black Widow (`blackwidow`, `blackwidow7`, `blackwidow1`, `blackwidow10`, `blackwidow5`, `blackwidow4`, `blackwidow8`, `blackwidow9`, `blackwidow3`, `blackwidow2`, `blackwidow6`, `blackwidow11`): `leader` All Speeds +9% (10 s) — when tagging.
- Blue Marvel (`bluemarvel`, `bluemarvel1`): `leader` All Basic Defenses +50%.
- Bobbi Morse — Marvel Studios' Agents of S.H.I.E.L.D. (`mockingbird1`): `leader` Dodge +6%.
- Captain America (`captainamerica`, `captainamerica10`, `captainamerica1`, `captainamerica12`, `captainamerica11`, `captainamerica5`, `captainamerica9`, `captainamerica6`, `captainamerica4`, `captainamerica3`, `captainamerica2`, `captainamerica8`): `leader` HP +30%.
- Captain America — Galactic Talon (`captainamerica15`): `leader` HP +45%.
- Captain America (Sam Wilson) (`falcon6`, `falcon4`): `leader` Dodge +15%.
- Captain Britain — Hellfire Gala (`psylocke3`): `leader` Mind Resist +50%.
- Carnage (`carnage`, `carnage1`): `leader` Critical Rate +6%, Critical Damage +18%.
- Carnage (`carnage2`, `carnage3`): `leader` Remove All Debuffs (12 s), All Basic Defenses +30% (12 s) — para Ability: Simbionte, When Debuffed, recarga 20 s.
- Cassie Lang (`cassielang`): `leader` Critical Rate +18%.
- Chasm — Dark Web (`scarletspider1`): `leader` Dodge +6%.
- Clea (`clea`): `leader` Skill Cooldown −24%.
- Colossus (`colossus`, `colossus3`, `colossus2`, `colossus1`): `leader` Physical Immunity Chance +100% (11 s) — 25% rate when hit, recarga 40 s.
- Corvus Glaive (`corvusglaive`, `corvusglaive2`, `corvusglaive1`): `leader` Skill Cooldown −24%.
- Cull Obsidian — Marvel Studios' Avengers: Infinity War (`blackdwarf1`): `leader` Physical Immunity Chance +100% (8 s) — 30% rate when hit, recarga 15 s.
- Daken (`daken`, `daken1`): `leader` Debuff Duration −30%.
- Daredevil (`daredevil`, `daredevil2`, `daredevil1`, `daredevil3`, `daredevil4`): `leader` Critical Rate +12% (18 s), Critical Damage +12% (18 s) — 30% rate when dodging, recarga 30 s.
- Darkhawk (`darkhawk`): `leader` All Speeds +6%.
- Dazzler (`dazzler`, `dazzler1`): `leader` Critical Rate +6%.
- Deadpool (`deadpool`, `deadpool4`, `deadpool5`, `deadpool3`, `deadpool2`, `deadpool1`): `leader` Recovery Rate +6%; `leader2` All Basic Attacks +35%, All Basic Defenses +35%, All Speeds +10% — para Character: Deadpool.
- Destroyer (`destroyer`, `destroyer1`, `destroyer2`): `leader` Energy Defense +30%.
- Dormammu (`dormammu`): `leader` All Basic Defenses +24%.
- Elektra (`elektra`, `elektra3`, `elektra1`, `elektra2`): `leader` All Speeds +6%.
- Emma Frost (`emmafrost`, `emmafrost3`, `emmafrost1`, `emmafrost2`, `emmafrost4`): `leader` Debuff Duration −24%.
- Erik Killmonger (Black Panther) — Marvel Studios' Black Panther (`killmonger1`): `leader` Physical Defense +50%.
- Falcon (`falcon`, `falcon1`, `falcon3`, `falcon2`): `leader` Dodge +6%.
- Falcon — What If... Zombies?! (`falcon5`): `leader` Dodge +15%.
- Falcon (Joaquin Torres) (`joaquintorres`): `leader` All Speeds +6%.
- Fandral (`fandral`): `leader` All Speeds +9%.
- Fantomex (`fantomex`): `leader` All Speeds +6%.
- Franklin Richards (`franklinrichards`): `leader` Debuff Duration −24%.
- Gamora (`gamora`, `gamora1`, `gamora2`): `leader` Attack Speed +13.5% — para Type: Velocidad.
- Ghost — Marvel Studios' Thunderbolts* (`ghost2`): `leader` All Basic Attacks +50% — para Ability: Máquina.
- Ghost Rider (`ghostrider`, `ghostrider1`, `ghostrider2`, `ghostrider3`, `ghostrider4`, `ghostrider5`): `leader` Fire Resist +50%.
- Gilgamesh (`gilgamesh`, `gilgamesh1`): `leader` All Basic Defenses +50%.
- Gorilla-Man (`gorillaman`): `leader` All Speeds +6%.
- Green Goblin — Gold Goblin (`greengoblin5`): `leader` All Basic Attacks +40%, Ignore Dodge +40%.
- Green Goblin — Ultimate (`greengoblin1`): `leader` Fire Resist +50%.
- Groot (`groot`, `groot3`, `groot5`, `groot6`): `leader` Physical Defense +45% — para Type: Combate.
- Groot (`groot2`, `groot4`): `leader` Physical Defense +45% — para Type: Velocidad.
- Groot — Secret Wars: Thors (`groot1`): `leader` Physical Defense +45% — para Type: Universal.
- Gwenpool (`gwenpool`, `gwenpool3`, `gwenpool4`, `gwenpool1`, `gwenpool2`): `leader` All Speeds +6%.
- Hawkeye (`hawkeye`, `hawkeye1`, `hawkeye3`, `hawkeye2`, `hawkeye5`, `hawkeye6`): `leader` Critical Damage +12%.
- Hawkeye (Kate Bishop) (`katebishop`, `katebishop1`, `katebishop2`): `leader` Critical Rate +15%.
- Heimdall (`heimdall`): `leader` All Basic Defenses +36%.
- Hellcat (`hellcat`): `leader` All Speeds +9%.
- Hellstorm (`hellstorm`, `hellstorm1`): `leader` Fire Resist +50%.
- Hulk (`hulk7`, `hulk6`): `leader` All Basic Defenses +24%.
- Hulk (`hulk9`, `hulk8`): `leader` All Basic Defenses +24%; `leader2` HP +30% — para Character: Hulk.
- Hulk (Amadeus Cho) (`amadeuscho`, `amadeuscho2`, `amadeuscho1`): `leader` Critical Rate +6%, Critical Damage +6%.
- Hulkling (`hulkling`): `leader` Physical Defense +30%.
- Human Torch (`humantorch2`, `humantorch4`, `humantorch3`): `leader` Fire Resist +50%.
- Iceman (`iceman`, `iceman2`, `iceman1`): `leader` Skill Cooldown −24%.
- Ikon (`ikon`): `leader` Critical Rate +8%.
- Inferno (`inferno`, `inferno1`): `leader` Fire Resist +50%.
- Invisible Woman (`invisiblewoman`, `invisiblewoman1`): `leader` Mind Resist +50%.
- Iron Fist (`ironfist`, `ironfist2`, `ironfist3`, `ironfist1`): `leader` Attack Speed +12% (30 s) — 25% chance when attacking, recarga 40 s.
- Iron Man (`ironman`, `ironman7`, `ironman1`, `ironman9`, `ironman5`, `ironman4`, `ironman3`, `ironman10`, `ironman2`, `ironman8`, `ironman6`): `leader` Skill Cooldown −24%.
- Jeff the Land Shark (`jeffthelandshark`): `leader` Debuff Duration −24%.
- Jessica Jones (`jessicajones`, `jessicajones1`): `leader` Physical Immunity Chance +100% (10 s) — 25% rate when hit, recarga 45 s.
- Jubilee (`jubilee`, `jubilee1`): `leader` Mind Resist +50%.
- Juggernaut (`juggernaut`, `juggernaut1`, `juggernaut2`): `leader` All Basic Defenses +50%.
- Kaecilius (`kaecilius`): `leader` Physical Defense +45%.
- Kahhori (`kahhori`): `leader` Energy Defense +45%.
- Karnak (`karnak`, `karnak1`): `leader` All Speeds +9%.
- Killmonger (`killmonger`): `leader` Physical Defense +50%.
- Kingo (`kingo`, `kingo1`): `leader` Dodge +15%.
- Knull — Ancient History (`knull1`): `leader` All Basic Attacks +60% — para Ability: Simbionte.
- Korath (`korath`): `leader` All Speeds +10%.
- Kraven The Hunter (`kraventhehunter`, `kraventhehunter1`): `leader` Critical Damage +12%.
- Loki (`loki`, `loki4`, `loki3`, `loki1`, `loki7`, `loki6`, `loki5`, `loki2`, `loki8`): `leader` Mind Resist +50%.
- Luke Cage (`lukecage`): `leader` Physical Immunity Chance +100% (11 s) — 25% rate when hit, recarga 50 s.
- Luke Cage (`lukecage1`, `lukecage2`): `leader` Physical Immunity Chance +100% (12 s) — 25% rate when hit, recarga 40 s.
- Magik (`magik`, `magik1`): `leader` Critical Rate +13%.
- Makkari (`makkari`, `makkari1`): `leader` All Speeds +6%.
- Mantis (`mantis`, `mantis1`): `leader` Debuff Duration −24%.
- Maximus (`maximus`): `leader` Debuff Duration −24%.
- Mephisto — Master of Hell (`mephisto1`): `leader` Fire Damage +30% — para Side: Supervillano; `leader2` Remove All Debuffs (12 s) — para Side: Supervillano, When Debuffed, recarga 20 s.
- Minn-Erva (`minn-erva`, `minn-erva1`): `leader` Debuff Duration −24%.
- Mister Sinister (`mistersinister`, `mistersinister1`): `leader` Mind Resist +50%; `leader2` All Basic Attacks +35%, All Basic Defenses +35%, All Speeds +10% — para Character: Mister Sinister.
- Mockingbird (`mockingbird`, `mockingbird2`): `leader` Dodge +6%.
- Molten Man (`moltenman`): `leader` All Basic Defenses +45%.
- Moon Girl — Monsters Unleashed! (MFF Variant) (`moongirl1`): `leader` All Basic Attacks +36%.
- Moon Knight (`moonknight`, `moonknight1`, `moonknight4`, `moonknight3`, `moonknight2`): `leader` Debuff Duration −24%.
- Moonstone (`moonstone`): `leader` Dodge +6%.
- Mordo (`baronmordo1`, `baronmordo2`): `leader` Dodge +6%.
- Morgan le Fay (`morganlefay`, `morganlefay1`): `leader` Debuff Duration −24%.
- Morph (`morph`): `leader` Debuff Duration −24%.
- Ms. Marvel (Kamala Khan) (`kamalakhan`, `kamalakhan2`, `kamalakhan1`, `kamalakhan5`, `kamalakhan3`, `kamalakhan4`): `leader` Physical Defense +45%.
- Mysterio (`mysterio`, `mysterio1`, `mysterio2`): `leader` Skill Cooldown −24%.
- Mystique (`mystique`, `mystique1`): `leader` All Speeds +6%; `leader2` All Basic Attacks +45% — para Character: Mystique.
- Namor (`namor`, `namor2`, `namor1`): `leader` Critical Rate +24%.
- Nebula (`nebula`, `nebula1`, `nebula4`, `nebula5`): `leader` Dodge +4.2% (when 1 Combat), Dodge +6% (when 2 Combats), Dodge +7.8% (when 3 Combats).
- Negasonic Teenage Warhead (`negasonicteenagewarhead`): `leader` Debuff Duration −30%.
- Nightcrawler (`nightcrawler`, `nightcrawler2`, `nightcrawler1`): `leader` All Speeds +6%.
- Nova (Sam Alexander) (`samalexander`): `leader` All Speeds +6%.
- Okoye (`okoye`): `leader` All Speeds +9%.
- Omega Red (`omegared`): `leader` All Speeds +6%; `leader2` Physical Attack +30% — para Character: Omega Red.
- Phil Coulson (`philcoulson`, `philcoulson1`, `philcoulson2`): `leader` Skill Cooldown −30% (10 s) — para Side: Superhéroe, when dealing Critical Attack, recarga 15 s.
- Phyla-Vell (`phylavell`, `phylavell1`): `leader` Energy Defense +50%.
- Psylocke (`psylocke`, `psylocke2`, `psylocke4`): `leader` Mind Resist +50%.
- Quasar (Avril Kincaid) (`quasar`, `quasar1`): `leader` Skill Cooldown −24%.
- Quicksilver (`quicksilver`, `quicksilver1`, `quicksilver4`, `quicksilver3`, `quicksilver2`): `leader` All Speeds +6%, Dodge +6%.
- Rachel Summers (`rachelsummers`): `leader` Mind Resist +40%.
- Red Skull (`redskull`, `redskull2`, `redskull1`, `redskull3`): `leader` All Basic Defenses +24%.
- Rescue (`rescue`): `leader` Max HP Shield +20% (10 s) — when HP is below 30%, recarga 10 s.
- Rhino (`rhino`, `rhino1`): `leader` Ignore Defense +20%.
- Rocket Raccoon (`rocketraccoon`, `rocketraccoon1`, `rocketraccoon2`, `rocketraccoon4`, `rocketraccoon3`, `rocketraccoon6`, `rocketraccoon5`): `leader` Skill Cooldown −30% (10 s) — when dealing Critical Attack, recarga 10 s.
- Rogue (`rogue`, `rogue1`, `rogue3`, `rogue2`, `rogue4`): `leader` All Basic Defenses +36%.
- Ronin — Marvel Studios' Avengers: Endgame (`hawkeye4`): `leader` Critical Damage +12%.
- Sabretooth (`sabretooth`, `sabretooth2`, `sabretooth1`): `leader` Debuff Duration −24%.
- Sandman (`sandman`, `sandman1`): `leader` All Basic Defenses +24%.
- Scarlet Spider (`scarletspider`, `scarletspider2`): `leader` Dodge +6%.
- Scorpion (`scorpion`, `scorpion1`): `leader` All Basic Defenses +50%.
- Scream (`scream`, `scream1`): `leader` Critical Rate +12%.
- Sentinel — Stark Sentinels Mk II (`sentinel2`): `leader` Remove All Debuffs (12 s) — When Debuffed, recarga 20 s.
- Sentry — Marvel Studios' Thunderbolts* (`sentry2`): `leader` All Basic Attacks +30%.
- Sersi (`sersi`, `sersi1`): `leader` All Speeds +6%.
- Shadow Shell (`shadowshell`, `shadowshell1`): `leader` Debuff Duration −24%.
- Shang-Chi — Marvel Animation's Marvel Zombies (`shangchi2`): `leader` All Basic Attacks +24%.
- Shuri (`shuri`, `shuri2`, `shuri1`): `leader` All Speeds +6%.
- Silver Surfer (Shalla-Bal) (`shallabal`): `leader` Debuff Duration −24%.
- Skurge (`skurge`): `leader` Critical Rate +9%, Attack Speed +9%.
- Slapstick (`slapstick`): `leader` Lightning Resist +50%.
- Songbird (`songbird`): `leader` All Speeds +9%.
- Spider-Gwen (`spidergwen`, `spidergwen1`, `spidergwen2`, `spidergwen3`): `leader` Skill Cooldown −30% (10 s) — when dodging, recarga 10 s.
- Spider-Man (`spiderman`, `spiderman2`, `spiderman10`, `spiderman5`, `spiderman3`, `spiderman12`, `spiderman1`, `spiderman6`, `spiderman7`, `spiderman4`, `spiderman9`, `spiderman8`, `spiderman11`): `leader` Dodge +6%.
- Spider-Man (Miles Morales) (`milesmorales`, `milesmorales1`): `leader` Debuff Duration −24%.
- Spot (`spot`): `leader` Dodge +6%, Critical Rate +12%.
- Squirrel Girl (`squirrelgirl`, `squirrelgirl1`, `squirrelgirl2`): `leader` Dodge +6%.
- Storm (`storm`, `storm3`, `storm4`, `storm5`, `storm1`): `leader` All Speeds +6%.
- Sun Bird (`sunbird`, `sunbird1`): `leader` All Speeds +6%.
- Sunspot (`sunspot`): `leader` All Speeds +6%.
- Super Nova Nebula — Marvel Studios' What If...? (`nebula6`): `leader` Dodge +4.2% (when 1 Combat), Dodge +6% (when 2 Combats), Dodge +7.8% (when 3 Combats).
- Sword Master (`swordmaster`): `leader` All Basic Defenses +35% — para Side: Superhéroe.
- Sylvie (`sylvie`): `leader` Mind Resist +50%.
- Taskmaster (`taskmaster`, `taskmaster1`, `taskmaster2`): `leader` Dodge +6%; `leader2` All Basic Attacks +35%, All Basic Defenses +35%, All Speeds +10% — para Character: Taskmaster.
- Thane — Phoenix Force (`thane1`): `leader` Remove All Debuffs (12 s), All Basic Attacks +25% (12 s) — When Debuffed, recarga 20 s.
- The Thing (`thing`, `thing2`, `thing1`, `thing4`, `thing3`): `leader` All Basic Defenses +50%.
- Thor (`thor`, `thor10`, `thor7`, `thor8`, `thor5`, `thor4`, `thor9`, `thor3`, `thor6`, `thor2`): `leader` Lightning Resist +50%.
- Thor (Jane Foster) (`janefoster`, `janefoster1`): `leader` Lightning Resist +50%, Critical Damage +6%.
- Ulysses Klaue (`ulyssesklaue`): `leader` Critical Rate +13%.
- Valkyrie (`valkyrie`, `valkyrie3`, `valkyrie1`, `valkyrie2`): `leader` Dodge +11%.
- Venom (`venom`, `venom2`, `venom4`, `venom1`, `venom6`, `venom3`, `venom5`): `leader` Debuff Duration −24%.
- Vision (`vision`, `vision1`, `vision2`): `leader` Super Armor, All Basic Defenses +30% (10 s) — when tagging, recarga 30 s.
- Volstagg (`volstagg`): `leader` All Basic Defenses +24%.
- Vulture (`vulture`, `vulture1`): `leader` Dodge +6%, Critical Rate +9%.
- War Tiger (`wartiger`, `wartiger1`): `leader` Skill Cooldown −24%.
- Warpath (`warpath`): `leader` All Speeds +6%.
- Warwolf (`warwolf`): `leader` Critical Rate +18% (5 s), Critical Damage +18% (5 s) — When enemies are below 30% HP,, recarga 1 s.
- Wasp (Nadia Van Dyne) (`nadiavandyne`): `leader` Dodge +11%.
- Weapon Hex (`weaponhex`, `weaponhex1`): `leader` Dodge +6%, Debuff Duration −24%.
- Whiplash (`whiplash`): `leader` Skill Cooldown −24%.
- Winter Soldier — Marvel Studios' Thunderbolts* (`wintersoldier6`): `leader` Physical Attack +45%.
- Wolverine (`wolverine`, `wolverine1`, `wolverine2`, `wolverine5`, `wolverine4`, `wolverine7`, `wolverine6`, `wolverine3`): `leader` Debuff Duration −30%.
- Wong (`wong`, `wong1`): `leader` Physical Immunity Chance +100% (12 s) — 25% rate when hit, recarga 60 s.
- X-23 (`x-23`, `x-232`, `x-233`, `x-231`): `leader` Debuff Duration −24%.
- Yelena Belova (`yelenabelova`, `yelenabelova1`, `yelenabelova2`, `yelenabelova3`): `leader` All Speeds +6%.
- Yondu (`yondu`, `yondu1`, `yondu2`, `yondu3`): `leader` Critical Rate +7.8%.
