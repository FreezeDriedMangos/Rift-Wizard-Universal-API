

# TODO: API_Music, API_OptionsMenu


import mods.API_Universal.API_Boss.API_Boss as API_Boss
import mods.API_Universal.API_Effect.API_Effect as API_Effect
import mods.API_Universal.API_Spells.API_Spells as API_Spells

# regex find: /def (.*)\(.*/
# regex replace: /#\n# $&\n$1 = API_Boss.$1/



################
### API_BOSS ###
################

# Adds a monster to the bestiary is a "final boss".
# All bosses added this way will appear before Mordred in the Bestiary.
# 
# spawner - A monster spawner function
#
# def add_finalboss_bestiary(spawner):
add_finalboss_bestiary = API_Boss.add_finalboss_bestiary

# Adds a final boss generator.
#
# name - Name of the boss for easier removal/editing
# generator - A function that accepts a LevelGenerator as parameter
#
# def add_finalboss_generator(name, generator):
add_finalboss_generator = API_Boss.add_finalboss_generator

# Adds a final boss monster.
#
# name - Name of the boss for easier removal/editing
# spawner - A monster spawner function
# add_bestiary - whether the monster is added to the bestiary
#
# def add_finalboss(name, spawner, add_bestiary = True):
add_finalboss = API_Boss.add_finalboss


# Adds a group of final bosses.
#
# name - Name of the boss for easier removal/editing
# spawners - A list of monster spawner functions
# add_bestiary - whether the monsters are added to the bestiary
# 
# def add_finalboss_group(name, spawners, add_bestiary = True):
add_finalboss_group = API_Boss.add_finalboss_group



##################
### API_Effect ###
##################


# Adds an effect to a tag
# tag - a Level.Tag. Your tag's color will be used as a key, so it should be unique. If a string is passed instead, it will create the tag for you.
# function - a function that accepts an effect and a color and generates an effect object
# 
# effect objects must implement:
# - advance(self) - updates the effect every tick
# - draw(self, surface) - draws the effect to the screen
#
# Examine RiftWizard.py for more information.
#
# example usage:
#     add_tag_effect(Level.Tags.BlueFire, lambda effect,color: RiftWizard.EffectRect(effect.x, effect.y, effect.color, effect.frames))
#
# def add_tag_effect(tag, function):
add_tag_effect = API_Effect.add_tag_effect

	
# Adds an effect to a tag
# tag - a Level.Tag. Your tag's color will be used as a key, so it should be unique. If a string is passed instead, it will create the tag for you.
# path - the path to your effect png, excluding the file extension. You should use os.path.join to create your path.
# 
# there is also a minor effect automatically created for you for projectiles, if you have a <name>_0.png.
#
# example usage:
#     add_tag_effect(Level.Tags.BlueFire, os.path.join('mods','ExampleMod','fireball_blue.png'))
#
# def add_tag_effect_simple(tag, path_base):
add_tag_effect_simple = API_Effect.add_tag_effect_simple

	



##################
### API_Spells ###
##################


# Adds a tag to the spell/skill shop.
# 
# tag - The tag to add
# keybind - A keybind, as a string, can be either lowercase or uppercase
#
# def add_tag_keybind(tag, keybind):
add_tag_keybind = API_Spells.add_tag_keybind
		
# Adds a tag to the tooltip colors.
# 
# tag - The tag to add, the color will be taken from the tag
#
# def add_tag_tooltip(tag):
add_tag_tooltip = API_Spells.add_tag_tooltip