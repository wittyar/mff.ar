"""Vocabulario del dominio: los valores cerrados de la API de thanosvibs (clase, raza,
género, bando, origen, instinto, habilidad) y su nombre en la app. Un solo lugar: lo
usan _core.py (personajes), fuentes.py (restricciones de Alliance Battle, soportes) y
skills_api.py (objetivos de las skills que son un grupo de aliados)."""
import re

TYPE ={'Combat':'Combate','Blast':'Detonación','Speed':'Velocidad','Universal':'Universal'}
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

# Objetivos de skill (el texto de la API de skills) que son un grupo de aliados -> la
# restricción que lo define, con la forma de las de líder y soporte de /api/supports
# (r en MFF_SOPORTES). La app la usa para listar quiénes lo cumplen. Cada una está
# contrastada con esas restricciones en los retratos que traen las dos cosas: la pasiva
# de Wong que apunta a "Magic Allies" restringe por la habilidad Magic en su soporte, y
# la de Jane Foster que apunta a "Electrokinetic Allies", por Shock.
OBJETIVO_GRUPO = {
    'Combat Type Allies': ('Type', TYPE['Combat']),
    'Blast Type Allies': ('Type', TYPE['Blast']),
    'Speed Type Allies': ('Type', TYPE['Speed']),
    'Universal Type Allies': ('Type', TYPE['Universal']),
    'Super Hero Allies': ('Side', SIDE['Super Hero']),
    'Super Villain Allies': ('Side', SIDE['Super Villain']),
    'Mutant Allies': ('Allies', ALLIES['Mutant']),
    'Alien Allies': ('Allies', ALLIES['Alien']),
    'Inhuman Allies': ('Allies', ALLIES['Inhuman']),
    'Allies with Leadership': ('Ability', ABIL['Leadership']),
    'Allies with Spider-Sense': ('Ability', ABIL['Spider-Sense']),
    'Annihilator Allies Only': ('Ability', ABIL['Annihilators']),
    'Black Order Allies': ('Ability', ABIL['Black Order']),
    'Dark Avengers Allies': ('Ability', ABIL['Dark Avengers']),
    'Defenders Allies': ('Ability', ABIL['Defenders']),
    'Electrokinetic Allies': ('Ability', ABIL['Shock']),
    'Eternals Allies': ('Ability', ABIL['Eternals']),
    'Fantastic Four Allies': ('Ability', ABIL['Fantastic Four']),
    'Flame Allies': ('Ability', ABIL['Flame']),
    'Gamma Radiation Allies': ('Ability', ABIL['Gamma Radiation']),
    'Guardians of the Galaxy Allies': ('Ability', ABIL['Guardians of the Galaxy']),
    'Machine Allies': ('Ability', ABIL['Machine']),
    'Magic Allies': ('Ability', ABIL['Magic']),
    'Olympus Allies Only': ('Ability', ABIL['Olympus']),
    'Phoenix Force Allies': ('Ability', ABIL['Phoenix Force']),
    'Sinister Six Allies': ('Ability', ABIL['Sinister Six']),
    'Strong Allies': ('Ability', ABIL['Strong']),
    'Symbiote Allies': ('Ability', ABIL['Symbiote']),
    'Thunderbolts Allies Only': ('Ability', ABIL['Thunderbolts']),
    'Warriors of the Sky Allies': ('Ability', ABIL['Warriors of the Sky']),
    'Weapon Master Allies': ('Ability', ABIL['Weapons Master']),
    'Young Avengers Allies Only': ('Ability', ABIL['Young Avengers']),
    'Zombie Allies': ('Ability', ABIL['Zombie']),
}
# Objetivos que no son un grupo: todos, uno mismo, el invocado. "Infinity Warps Allies"
# con condición de entrada queda afuera a propósito: el soporte de Arachknight, el único
# que lo usa, no restringe a nadie, así que no se sabe si alcanza solo a los Infinity
# Warps. (Los "\n" son literales: la fuente mete la condición dentro del objetivo.)
OBJETIVO_SIN_GRUPO = {
    'All Allies', 'Self', 'Summoned Character',
    'All Allies for the first effect, Self for the second effect',
    'All Allies\\nActivates when: Combat Type Ally enters',
    'Self\\nActivates when: Mutant Ally enters',
    'Infinity Warps Allies\\nActivates when: Infinity Warps type Ally enters',
}
# Objetivos que la fuente no nombra: solo trae el número ("Target ID: 88").
OBJETIVO_SIN_NOMBRE = re.compile(r'^Target ID: \d+$')
