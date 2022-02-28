
import mods.API_Universal.APIs.API_Boss.API_Boss as API_Boss
import mods.API_Universal.APIs.API_Effect.API_Effect as API_Effect
import mods.API_Universal.APIs.API_Spells.API_Spells as API_Spells
import mods.API_Universal.APIs.API_OptionsMenu.API_OptionsMenu as API_OptionsMenu
import mods.API_Universal.APIs.API_TitleMenus.API_TitleMenus as API_TitleMenus
import mods.API_Universal.APIs.API_Music.API_Music as API_Music
import mods.API_Universal.APIs.API_LevelGenProps.API_LevelGenProps as API_LevelGenProps
import mods.API_Universal.APIs.API_LevelGen.API_LevelGen as API_LevelGen
import mods.API_Universal.APIs.API_WinCondition.API_WinCondition as API_WinCondition
import mods.API_Universal.EventSystem as EventSystem

import mods.API_Universal.Libraries.Library_TextInput.Library_TextInput as Library_TextInput
import mods.API_Universal.Libraries.Library_Menus.Library_Menus as Library_Menus

# regex find: /def (.*)\(.*/
# regex replace: /#\n# $&\n$1 = API_Boss.$1/



###################
### EventSystem ###
###################

# Adds an event listener to the event system. 
# listener - a function that takes parameters according to the event name passed
#
# EVENT NAMES:
# 'PyGameView.on_frame'
#     called at the start of every frame after animation timers are updated - even on the title screen
#     listener takes (pygameview)
# 
# 'PyGameView.on_exit'
#     called when the game window is closed
#     listener takes (pygameview)
# 
#  
# def register_listener(event_name, listener):
register_listener = EventSystem.register_listener

########################
### API_Translations ###
########################

# no exports


###################
### API_Disrupt ###
###################

# no exports


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

# Adds an attribute (eg 'construct') to the tooltip colors.
#
# attr - string. The name of the attribute
# color - (int, int, int) color. The color of the attribute
# 
# def add_attr_color(attr, color):
add_attr_color = API_Spells.add_attr_color

# Adds an tag to the shrine options.
#
# tag - Tag. Level.Tag() Object
# magnitude - int. 1 = uncommon Tag (eg elements), 2 = common Tag (eg sorcery/conjuration), rest = rare Tag (eg dragon/chaos),
#
# def add_shrine_option(tag, magnitude):
add_shrine_option = API_Spells.add_shrine_option


#######################
### API_OptionsMenu ###
#######################


# Adds a blank line to the (current) bottom of the options menu.
#
# def add_blank_option_line():
add_blank_option_line = API_OptionsMenu.add_blank_option_line

# Adds a title line to the (current) bottom of the options menu.
# 
# title_string - the string to be rendered as the title
#
# def add_tile_option_line(title_string):
add_tile_option_line = API_OptionsMenu.add_tile_option_line


# Adds a new option to the (current) bottom of the options menu.
# See API_Universal/API_OptionsMenu/API_OptionsMenu.py for an example (in comments at the top of the file).
# 
# get_option_string - a function that takes (pygameview, cur_value_of_option). Return None to hide this option.
# get_cur_value - a function that takes (pygameview). Returns the current value of this option. You may wish to access pygameview.options['your_option_name'].
# possible_values - a list of possible values for this option. values may be of any type, but strings or numbers are recommened.
# mouse_content - a unique string or number for your option. A string like "my_option_name" is recommended to avoid conflicts between mods.
# trigger_on_select - a function that takes (pygameview, new_value). Called whenever the option has its value updated or enter is pressed while the option is highlighted.
# option_wraps - boolean. If True, when the user hits 'right' while the option is selected and the last value of possible_values is the current value, possible_values[0] will become the new value
# initialize_option - a function that takes (pygameview). Called when the game is launched
# 
# def add_option(get_option_string, get_cur_value, possible_values, mouse_content, trigger_on_select=None, option_wraps=False, initialize_option=None):
add_option = API_OptionsMenu.add_option


######################
### API_TitleMenus ###
######################

# Adds a new title menu. Returns the menu's id.
# See API_Universal/API_OptionsMenu/API_OptionsMenu.py for an example.
# 
# draw_function - a function that takes (pygameview). called every frame when the menu is active
# process_input_function - a function that takes (pygameview). called every frame when the menu is active
# blocks_char_sheet_and_examine - boolean. If False, the character pane and examine pane will be drawn when this menu is active
# 
# def add_menu(draw_function, process_input_function, blocks_char_sheet_and_examine=True):
add_menu = API_TitleMenus.add_menu

# Overrides the draw_function and process_input_function of an existing menu. Typically used to patch menus from the base game.
#
# menu_id - the id of the menu to be overriden (eg RiftWizard.STATE_PICK_MODE)
# draw_function - a function that takes (pygameview). called every frame when the menu is active
# process_input_function - a function that takes (pygameview). called every frame when the menu is active
#
# def override_menu(menu_id, draw_function, process_input_function):
override_menu = API_TitleMenus.override_menu

# Redirects a transition between menus.
# eg override_menu_transition(RiftWizard.STATE_PICK_MODE, RiftWizard.STATE_LEVEL, STATE_LOBBY_MENU, lambda pygameview: pygameview.in_online_multiplayer_mode))
# 
# menu_from - id of the menu the transition starts at
# menu_to - id of the menu the transition ends at
# override - id of the menu the transition will be redirected to
# condition - a function that takes (pygameview). If this function returns False, the transition will not be overriden
# 
# def override_menu_transition(menu_from, menu_to, override, condition = (lambda pygameview: True)):
override_menu_transition = API_TitleMenus.override_menu_transition




#################
### API_Music ###
#################

class ConstantsPackage(object):
    pass

API_Music_Constants = ConstantsPackage()
API_Music_Constants.PRIORITY_FALLBACK = API_Music.PRIORITY_FALLBACK
API_Music_Constants.PRIORITY_NORMAL = API_Music.PRIORITY_NORMAL
API_Music_Constants.PRIORITY_SPECIAL_TRACK = API_Music.PRIORITY_SPECIAL_TRACK

API_Music_Constants.TRACK_TYPE_BOSS = API_Music.TRACK_TYPE_BOSS
API_Music_Constants.TRACK_TYPE_LEVEL = API_Music.TRACK_TYPE_LEVEL
API_Music_Constants.TRACK_TYPE_TITLE = API_Music.TRACK_TYPE_TITLE
API_Music_Constants.TRACK_TYPE_GAMEOVER = API_Music.TRACK_TYPE_GAMEOVER
API_Music_Constants.TRACK_TYPE_VICTORY = API_Music.TRACK_TYPE_VICTORY

# Adds a track to play in-game. When a new track event occurs, tracks with equal priority whose condition_func retuns 'True' will be chosen from at random.
# ex:
# def level_has_shrine(pygameview):
# 	shrines = [prop for prop in pygameview.game.cur_level.props if isinstance(prop, Level.ShrineShop)]
# 	return len(shrines) > 0
# 
# Modred.add_track(Modred.API_Music_Constants.TRACK_TYPE_LEVEL, Modred.API_Music_Constants.PRIORITY_NORMAL, os.path.join('mods', 'ShougsMusic', 'shrine' + '.wav'), level_has_shrine) 
#
#
# track_type - API_Music_Constants constant. the type of track this is
# priority - API_Music_Constants constant. the priority this track takes over other tracks of the same type
# path - string. the path to the mp3 file for this track
# condition_func - a function that takes (pygameview). Return True if this track is valid to play under the current conditions (eg a certain enemy is present in the current level)
# 
# def add_track(track_type, priority, path, condition_func):
add_track = API_Music.add_track


# Forces a new music track to be selected from existing added tracks, tracks with equal priority whose condition_func retuns 'True' will be chosen from at random.
# track_type - API_Music_Constants constant. the type of track this is
# 
# def play_music(track_type):
play_music = API_Music.play_music


#########################
### API_LevelGenProps ###
#########################
# allows you to customize the primary reward for rifts (eg shrines/circles/ruby hearts)

API_LevelGenProps_Constants = ConstantsPackage()


# Add a new shrine to the level gen pool
#
# shrine - a class that inherits from Shrine, eg Shrines.RedFlameShrine
# rarity - one of the rarity constants. I don't think this actually effects anything
#
# def add_shrine(shrine, rarity = API_LevelGenProps_Constants.COMMON):
add_shrine = API_LevelGenProps.add_shrine

API_LevelGenProps_Constants.SHRINE_COMMON = API_LevelGenProps.SHRINE_COMMON
API_LevelGenProps_Constants.SHRINE_UNCOMMON = API_LevelGenProps.SHRINE_UNCOMMON
API_LevelGenProps_Constants.SHRINE_RARE = API_LevelGenProps.SHRINE_RARE


# Add a primary reward for a rift (something that will generate instead of shrines/circles/ruby hearts)
#
# prop_generator - a function that takes (player) and returns an object that inherits from the Prop class
# weight - a number. the higher it is the more likely this prop will generate
# condition -  a function that takes the rift level (int) and returns True or False (should this prop be able to generate on this level)
#
# def add_primary_prop_type(prop_generator, weight, condition=lambda level: True):
add_primary_prop_type = API_LevelGenProps.add_primary_prop_type

API_LevelGenProps_Constants.RUBY_HEART_WEIGHT = API_LevelGenProps.RUBY_HEART_WEIGHT
API_LevelGenProps_Constants.SPELL_CIRCLE_WEIGHT = API_LevelGenProps.SPELL_CIRCLE_WEIGHT
API_LevelGenProps_Constants.SHRINE_WEIGHT = API_LevelGenProps.SHRINE_WEIGHT


# Add a secondary reward for a rift (something that will generate alongside shrines/circles/ruby hearts)
#
# prop_generator - a function that takes (player) and returns an object that inherits from the Prop class
# weight - a number. the higher it is the more likely this prop will generate
# condition -  a function that takes the rift level (int) and returns True or False (should this prop be able to generate on this level)
#
# def add_secondary_prop_type(prop_generator, weight, condition=lambda level: True):
add_secondary_prop_type = API_LevelGenProps.add_secondary_prop_type
	

# Define chances for how many secondary props are generated in a level 
# eg, "I want there to be a 50% chance for a level to generate 3 secondary props past level 5": 
#       add_num_secondary_props_random_option(3, .5, lambda level: level > 5)
#
# num - int. how many secondary props will be generated if this option is randomly selected
# weight - a number. the higher it is the more likely this prop will generate
# condition -  a function that takes the rift level (int) and returns True or False (should this option be able to be selected on this level)
# 
# def add_num_secondary_props_random_option(num, weight, condition = lambda level: True):
add_num_secondary_props_random_option = API_LevelGenProps.add_num_secondary_props_random_option


# Add a new kind of item that can generate in rifts
#  
# item_generator - a function that takes no params and returns an Item object (eg Consumables.heal_potion) 
# weight - an API_LevelGenProps_Constants Item rarity constant (see below)
#
# def add_item_type(item_generator, weight):
add_item_type = API_LevelGenProps.add_item_type

API_LevelGenProps_Constants.ITEM_COMMON = API_LevelGenProps.ITEM_COMMON
API_LevelGenProps_Constants.ITEM_UNCOMMON = API_LevelGenProps.ITEM_UNCOMMON
API_LevelGenProps_Constants.ITEM_RARE = API_LevelGenProps.ITEM_RARE
API_LevelGenProps_Constants.ITEM_SUPER_RARE = API_LevelGenProps.ITEM_SUPER_RARE



# example: adding a new shop:
#
# def item_with_cost(item, cost):
#   item.cost = cost
#   return item
# def gen_shop():
# 	shop = Level.Shop()
# 	shop.items = [item_with_cost(Consumables.teleporter(), 5), item_with_cost(Consumables.heal_potion(), 10)]
# 	shop.currency = Level.CURRENCY_GOLD
#   shop.description = "An example shop."
# 	shop.asset = ["MyMod", "shop_sprite"]
# 	return shop
# Modred.add_primary_prop_type(gen_shop, Modred.API_LevelGenProps_Constants.SHRINE_WEIGHT, lambda level: level > 4)


# example: adding a "pick one free spell" shop as a free bonus to every level
#
# def gen_shop_2_spells():
# 	shop = Level.Shop()
# 	shop.items = [Spells.FireballSpell(), Spells.FlameTongue()]
# 	shop.currency = Level.CURRENCY_PICK
#   shop.description = "Pick one spell."
# 	shop.asset = ["MyMod", "shop_sprite"]
# 	return shop
# def gen_shop_3_spells():
# 	shop = gen_shop_2_spells()
# 	shop.items = [Spells.FireballSpell(), Spells.FlameTongue(), LightningBoltSpell()]
# 	return shop
# Modred.add_secondary_prop_type(gen_shop_2_spells, Modred.API_LevelGenProps_Constants.SHRINE_WEIGHT)
# Modred.add_secondary_prop_type(gen_shop_3_spells, Modred.API_LevelGenProps_Constants.SHRINE_WEIGHT, lambda level: level > 5) # after level 5, have an equal chance to generate a shop with 3 spells instead of 2
# Modred.add_num_secondary_props_random_option(1, 1, lambda level: level > 3) # only generate bonus props after level 3


# Note: Check out Level.ShiftingShop too. It's very useful for dynamically generating shop items.



####################
### API_LevelGen ###
####################

# Overrides the level generation with a new level generation function
#
# level_maker - a function that takes (level_generator) as an argument and returns a level object
# 
# def set_level_maker(level_maker):
set_level_maker = API_LevelGen.set_level_maker

# Undo's the last call to set_level_maker
# 
# def restore_level_maker():
restore_level_maker = API_LevelGen.restore_level_maker

# Resets the level maker to the vanilla one. Called on loading the title screen.
#
# def clear_level_makers():
clear_level_makers = API_LevelGen.clear_level_makers



API_LevelGen_Constants = ConstantsPackage()
API_LevelGen_Constants.LEVEL_SIZE = API_LevelGen.LEVEL_SIZE




########################
### API_WinCondition ###
########################

# adds a new required win condition
#
# condition - a function that takes a game object and returns True if the condition is satisfied, otherwise False
#
# def add_win_condition(condition):
add_win_condition = API_WinCondition.add_win_condition

# Removes all custom win conditions from the list of required conditions
#
# def reset_win_conditions():
reset_win_conditions = API_WinCondition.reset_win_conditions

# removes the base game's win condition (no units on a team other than TEAM_PLAYER present on the level) from the list of win conditions
#
# def remove_default_win_condition():
remove_default_win_condition = API_WinCondition.remove_default_win_condition


##################################################
##################################################
###   LIBRARIES
##################################################
##################################################




#########################
### Library_TextInput ###
#########################

TextInput = Library_TextInput.TextInput



#####################
### Library_Menus ###
#####################

make_menu_from_rows = Library_Menus.make_menu_from_rows
make_single_page_menu_from_rows = Library_Menus.make_single_page_menu_from_rows
make_menu_from_pages = Library_Menus.make_menu_from_rows



# 
# 
# def row_from_size(width, height):
row_from_size = Library_Menus.row_from_size

# 
# 
# def row_from_text(text, font, linesize, width=None, height=0):
row_from_text = Library_Menus.row_from_text

# 
# 
# def row_from_text_and_icon(text, font, linesize, icon_asset, width=None, height=0):
row_from_text_and_icon = Library_Menus.row_from_text_and_icon

# 
# also works for items
# 
# def row_from_text_and_spell(text, font, linesize, spell, width=None, height=0):
row_from_text_and_spell = Library_Menus.row_from_text_and_spell

# 
# also works for items
# 
# def row_from_spell(spell, font, linesize, width=None, height=0):
row_from_spell = Library_Menus.row_from_spell

# 
# 
# def make_multirow(*rows):
make_multirow = Library_Menus.MultiRow
