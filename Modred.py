
import mods.API_Universal.API_Boss.API_Boss as API_Boss
import mods.API_Universal.API_Effect.API_Effect as API_Effect
import mods.API_Universal.API_Spells.API_Spells as API_Spells
import mods.API_Universal.API_OptionsMenu.API_OptionsMenu as API_OptionsMenu
import mods.API_Universal.API_TitleMenus.API_TitleMenus as API_TitleMenus
import mods.API_Universal.API_Music.API_Music as API_Music
import mods.API_Universal.EventSystem as EventSystem

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