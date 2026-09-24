"""Vocabulario del dominio: los valores cerrados de la API de thanosvibs (clase, raza,
género, bando, origen, instinto, habilidad) y su nombre en la app. Un solo lugar: lo
usan _core.py (personajes) y fuentes.py (restricciones de Alliance Battle, soportes)."""
TYPE = {'Combat':'Combate','Blast':'Detonación','Speed':'Velocidad','Universal':'Universal'}
ALLIES = {'Alien':'Alienígena','Creature':'Criatura','Human':'Humano','Inhuman':'Inhumano','Mutant':'Mutante','Other':'Otro'}
GENDER = {'Male':'Masculino','Female':'Femenino','Neutral':'Neutro'}
SIDE = {'Super Hero':'Superhéroe','Super Villain':'Supervillano','Neutral':'Neutral'}
ORIGIN = {'MCU':'MCU','Comic':'Cómic','Animation':'Animación','TV':'TV','Sony':'Sony','Collab':'Colaboración','Original':'Original MFF'}
INSTINCT = {'Justice':'Justicia','Order':'Orden','Destruction':'Destrucción','Cruelty':'Crueldad'}
ABIL = {
 'Agent':'Agente','Agility':'Agilidad','Annihilators':'Aniquiladores','Black Order':'Orden Negra',
 'Chaos Magic':'Magia del Caos','Chill':'Congelación','Cold Blooded':'Sangre Fría','Command':'Mando',
 'Cosmic Cube':'Cubo Cósmico','Dark Avengers':'Vengadores Oscuros','Defenders':'Defensores','Durability':'Durabilidad',
 'Energy Projection':'Proyección de Energía','Eternals':'Eternos','Fantastic Four':'Los 4 Fantásticos',
 'Fast Movement':'Movimiento Rápido','Flame':'Llama','Gamma Radiation':'Radiación Gamma',
 'Guardians of the Galaxy':'Guardianes de la Galaxia','Healing':'Curación','Heightened Senses':'Sentidos Agudizados',
 'Hellfire':'Fuego Infernal','Infinity Warps':'Infinity Warps','Leadership':'Liderazgo','Machine':'Máquina',
 'Magic':'Magia','Mind':'Mente','Mind Resist':'Resistencia Mental','Olympus':'Olimpo','Phoenix Force':'Fuerza Fénix',
 'Poison':'Veneno','Power Cosmic':'Poder Cósmico','Pure Evil':'Maldad Pura','Shock':'Electrochoque',
 'Sinister Six':'Los Seis Siniestros','Spider-Sense':'Sentido Arácnido','Strong':'Fuerza','Symbiote':'Simbionte',
 'Thunderbolts':'Thunderbolts','Time Freezing Immunity':'Inmunidad a Detención del Tiempo',
 'Warriors of the Sky':'Guerreros del Cielo','Weapons Master':'Maestro de Armas','Young Avengers':'Jóvenes Vengadores','Zombie':'Zombi'}
