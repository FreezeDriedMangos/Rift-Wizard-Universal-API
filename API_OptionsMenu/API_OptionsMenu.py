#####################################################
# Example usage: 
#####################################################


# API_OptionsMenu.add_tile_option_line('Multiplayer Settings:')

# def sp_distribution_strategy_string(self, cur_value):
# 	if cur_value == SP_DISTRIBUTION_STRATEGY_DEFAULT:
# 		sp_dist_fmt = 'Default'
# 	elif cur_value == SP_DISTRIBUTION_STRATEGY_ONE_FOR_ALL:
# 		sp_dist_fmt = 'One for All'
# 	elif cur_value == SP_DISTRIBUTION_STRATEGY_ROUND_ROBIN:
# 		sp_dist_fmt = 'Round Robin'
# 	elif cur_value == SP_DISTRIBUTION_STRATEGY_HALF_FOR_ALL:
# 		sp_dist_fmt = 'Half for All'

# 	return ("SP Distribution: %6s" % sp_dist_fmt)

# def set_sp_distribution_strategy(self, new_value):
# 	self.options['sp_distribution_strategy'] = new_value
#   # other stuff that you may want to do when your option gets updated should go here

# def initialize_sp_distribution_strategy(self):
# 	if not 'sp_distribution_strategy' in self.options:
# 		self.options['sp_distribution_strategy'] = SP_DISTRIBUTION_STRATEGY_HALF_FOR_ALL
# 	# other stuff you may want to do when you initialize your option

# API_OptionsMenu.add_option( \
# 	sp_distribution_strategy_string, \
# 	lambda self: self.options['sp_distribution_strategy'], \
# 	[
# 		SP_DISTRIBUTION_STRATEGY_HALF_FOR_ALL,
# 		SP_DISTRIBUTION_STRATEGY_ONE_FOR_ALL,
# 		SP_DISTRIBUTION_STRATEGY_DEFAULT,
# 		SP_DISTRIBUTION_STRATEGY_ROUND_ROBIN,
# 	], \
# 	'sp_distribution_strategy_option'
# 	set_sp_distribution_strategy, \
# 	option_wraps=True, \
#	initialize_option=initialize_sp_distribution_strategy
# )

# API_OptionsMenu.add_blank_option_line()


#####################################################




####################################################
# Importing RiftWizard.py                          |
# Credit to trung on discord                       |
#                                                  |
#----------------------------------------------    |
import inspect #                                   |
def get_RiftWizard(): #                            |
    # Returns the RiftWizard.py module object      |
    for f in inspect.stack()[::-1]: #              |
        if "file 'RiftWizard.py'" in str(f): #     |
            return inspect.getmodule(f[0]) #       |
	 #                                             |
    return inspect.getmodule(f[0]) #               |
#                                                  |
RiftWizard = get_RiftWizard() #                    |
#                                                  |
#                                                  |
####################################################

from collections import namedtuple
import pygame

# get_cur_value takes one param, the pygameview
# get_option_stirng takes two params, the pygameview and the option's current value
# trigger_on_select takes two params, the pygameview and the option's new value
Option = namedtuple('Option', 'get_option_string get_cur_value possible_values mouse_content trigger_on_select option_wraps initialize_option')
options = []
selected_option_index = 0
options_have_been_initialized = False

def try_initialize_options(self):
	global options_have_been_initialized
	if not options_have_been_initialized:
		for option in options:
			if option.initialize_option:
				option.initialize_option(self)
		options_have_been_initialized = True


def draw_options_menu(self):
	global options

	option_strings = [(option.get_option_string(self, option.get_cur_value(self)), option) for option in options]
	option_strings = [(string, option) for (string, option) in option_strings if string]

	cur_largest_option = max(self.font.size("  " + option_string)[0] for (option_string, option) in option_strings)

	cur_x = self.screen.get_width() // 2 - self.font.size("Sound Volume")[0]
	cur_y = int(self.screen.get_height() // 2 - self.linesize * len(option_strings)/2)
	rect_w = cur_largest_option

	for (option_string, option) in option_strings:
		if option.mouse_content not in [None, RiftWizard.OPTION_RETURN, RiftWizard.OPTION_EXIT]:
			option_string = "  " + option_string
		self.draw_string(option_string, self.screen, int(cur_x), int(cur_y), mouse_content=option.mouse_content, content_width=rect_w)
		cur_y += self.linesize
# RiftWizard.PyGameView.draw_options_menu = draw_options_menu


def option_change(self, valid_options, selected_option_index, delta):
	self.play_sound("menu_confirm")
	option = valid_options[selected_option_index]

	if not option.possible_values or len(option.possible_values) == 0:
		option.trigger_on_select(self, None)
		return

	cur_value = option.get_cur_value(self)
	if cur_value in option.possible_values:
		cur_value_index = option.possible_values.index(cur_value)
		cur_value_index += delta
	else:
		cur_value_index = 0

	if option.option_wraps:
		cur_value_index += len(option.possible_values)
		cur_value_index %= len(option.possible_values)
	else:
		cur_value_index = max(0, cur_value_index)
		cur_value_index = min(cur_value_index, len(option.possible_values)-1)
	
	option.trigger_on_select(self, option.possible_values[cur_value_index])



def process_options_input(self):
	global options
	global selected_option_index

	option_strings = [(option.get_option_string(self, option.get_cur_value(self)), option) for option in options]
	valid_options = [option for (string, option) in option_strings if string and option.mouse_content != None]

	try:
		existing_selected_option = [option for option in valid_options if option.mouse_content == self.examine_target][0]
		if existing_selected_option:
			selected_option_index = valid_options.index(existing_selected_option)
	except:
		# no existing selected option
		pass

	for evt in [e for e in self.events if e.type == pygame.KEYDOWN]:

		if evt.key in self.key_binds[RiftWizard.KEY_BIND_UP]:
			if self.examine_target is None:
				self.examine_target = valid_options[0].mouse_content
				selected_option_index = 0
			else:
				selected_option_index -= 1
				selected_option_index = max(0, selected_option_index)
				self.examine_target = valid_options[selected_option_index].mouse_content
				
				self.play_sound("menu_confirm")
		if evt.key in self.key_binds[RiftWizard.KEY_BIND_DOWN]:
			if self.examine_target is None:
				self.examine_target = valid_options[0].mouse_content
				selected_option_index = 0
			else:
				selected_option_index += 1
				selected_option_index = min(selected_option_index, len(valid_options)-1)
				self.examine_target = valid_options[selected_option_index].mouse_content
				
				self.play_sound("menu_confirm")

		if evt.key in self.key_binds[RiftWizard.KEY_BIND_LEFT]:
			self.play_sound("menu_confirm")
			option_change(self, valid_options, selected_option_index, -1)

		if evt.key in self.key_binds[RiftWizard.KEY_BIND_RIGHT]:
			self.play_sound("menu_confirm")
			option_change(self, valid_options, selected_option_index, 1)

		if evt.key in self.key_binds[RiftWizard.KEY_BIND_CONFIRM]:
			self.play_sound("menu_confirm")
			option = valid_options[selected_option_index]
			option.trigger_on_select(self, option.get_cur_value(self))


		if evt.key in self.key_binds[RiftWizard.KEY_BIND_ABORT]:
			self.state = RiftWizard.STATE_LEVEL if self.game else RiftWizard.STATE_TITLE
			if self.state == RiftWizard.STATE_TITLE:
				self.examine_target = RiftWizard.TITLE_SELECTION_LOAD if RiftWizard.can_continue_game() else RiftWizard.TITLE_SELECTION_NEW
			self.play_sound("menu_confirm")


	m_loc = self.get_mouse_pos()
	for evt in [e for e in self.events if e.type == pygame.MOUSEBUTTONDOWN]:
		mouse_content = None

		for r, o in self.ui_rects:
			if r.collidepoint(m_loc):
				mouse_content = o
				break
		
		self.examine_target = mouse_content
		try:
			existing_selected_option = [option for option in valid_options if option.mouse_content == self.examine_target][0]
			if existing_selected_option:
				selected_option_index = valid_options.index(existing_selected_option)
		except:
			# no existing selected option
			continue

		if evt.button == pygame.BUTTON_LEFT:
			self.play_sound("menu_confirm")
			option_change(self, valid_options, selected_option_index, 1)

		if evt.button == pygame.BUTTON_RIGHT:
			self.play_sound("menu_confirm")
			option_change(self, valid_options, selected_option_index, -1)
# RiftWizard.PyGameView.process_options_input = process_options_input



def add_option(get_option_string, get_cur_value, possible_values, mouse_content, trigger_on_select=None, option_wraps=False, initialize_option=None):
	global options
	
	if len(options) >= 10:
		index = len(options)-3
	else:
		index = max(0, len(options))

	new_option = Option(get_option_string, get_cur_value, possible_values, mouse_content, trigger_on_select, option_wraps, initialize_option)
	options.insert(index, new_option)

def no_action(self, new_value):
	pass
def add_blank_option_line():
	add_option(lambda self,cur_value:" ", lambda self:None, None, None, no_action)
def add_tile_option_line(title_string):
	add_option(lambda self,cur_value:title_string, lambda self:None, None, None, no_action)


add_tile_option_line('Base Game Settings:')
add_option(lambda self,cur_value:"How to Play", lambda self:None, None, RiftWizard.OPTION_HELP, lambda self, new_value: self.show_help())
add_option(lambda self,cur_value:"Sound Volume:  %3d" % cur_value, \
		   lambda self: self.options['sound_volume'], \
		   list(range(0,101)), \
		   RiftWizard.OPTION_SOUND_VOLUME, \
		   lambda self, new_value:self.adjust_volume(new_value-self.options['sound_volume'], 'sound') \
)
add_option(lambda self,cur_value:"Music Volume:  %3d" % cur_value, \
		   lambda self: self.options['music_volume'], \
		   list(range(0,101)), \
		   RiftWizard.OPTION_MUSIC_VOLUME, \
		   lambda self, new_value:self.adjust_volume(new_value-self.options['music_volume'], 'music') \
)


def anim_speed_string(self, cur_value):
	if self.options['spell_speed'] == 0:
		speed_fmt = "normal"
	elif self.options['spell_speed'] == 1:
		speed_fmt = "fast"
	elif self.options['spell_speed'] == 2:
		speed_fmt = "turbo"
	elif self.options['spell_speed'] == 3:
		speed_fmt = "Xturbo"

	return ("Anim Speed: %6s" % speed_fmt)
def set_spell_speed(self, new_value):
	self.options['spell_speed'] = new_value
add_option(anim_speed_string, \
		   lambda self: self.options['spell_speed'], \
		   [0, 1, 2, 3], \
		   RiftWizard.OPTION_SPELL_SPEED, \
		   set_spell_speed, \
		   option_wraps=True \
)

add_option(lambda self,cur_value:"Rebind Controls", lambda self:None, None, RiftWizard.OPTION_CONTROLS, \
	lambda self, value: self.open_key_rebind() \
)


add_blank_option_line()


def set_state_level(self, value):
	self.state = RiftWizard.STATE_LEVEL
add_option(lambda self,cur_value:"Return to Game" if self.game else None, lambda self:None, None, RiftWizard.OPTION_RETURN, set_state_level)

def save_and_return_to_title(self, new_value):
	if self.game:
		self.game.save_game()
	self.return_to_title()
add_option(lambda self,cur_value:"Save and Exit" if self.game else None, lambda self:None, None, RiftWizard.OPTION_EXIT, save_and_return_to_title)
add_option(lambda self,cur_value:None if self.game else "Back to Title", lambda self:None, None, RiftWizard.OPTION_EXIT, save_and_return_to_title)

print("API Options Menu Loaded")