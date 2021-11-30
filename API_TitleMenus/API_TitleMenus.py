

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


Menu = namedtuple('Menu', 'id draw_function process_input blocks_char_sheet_and_examine')
menus = [
	Menu(RiftWizard.STATE_TITLE, RiftWizard.PyGameView.draw_title, RiftWizard.PyGameView.process_title_input, True),
	Menu(RiftWizard.STATE_PICK_MODE, RiftWizard.PyGameView.draw_pick_mode, RiftWizard.PyGameView.process_pick_mode_input, True),
	Menu(RiftWizard.STATE_PICK_TRIAL, RiftWizard.PyGameView.draw_pick_trial, RiftWizard.PyGameView.process_pick_trial_input, True),
	Menu(RiftWizard.STATE_OPTIONS, RiftWizard.PyGameView.draw_options_menu, RiftWizard.PyGameView.process_options_input, True),
	Menu(RiftWizard.STATE_REBIND, RiftWizard.PyGameView.draw_key_rebind, RiftWizard.PyGameView.process_key_rebind, True),
	Menu(RiftWizard.STATE_MESSAGE, RiftWizard.PyGameView.draw_message, RiftWizard.PyGameView.process_message_input, True),
	Menu(RiftWizard.STATE_REMINISCE, RiftWizard.PyGameView.draw_reminisce, RiftWizard.PyGameView.process_reminisce_input, True),
	Menu(RiftWizard.STATE_LEVEL, RiftWizard.PyGameView.draw_level, lambda pygameview: None, False),
	Menu(RiftWizard.STATE_CHAR_SHEET, RiftWizard.PyGameView.draw_char_sheet, RiftWizard.PyGameView.process_char_sheet_input, False),
	Menu(RiftWizard.STATE_SHOP, RiftWizard.PyGameView.draw_shop, RiftWizard.PyGameView.process_shop_input, False),
	Menu(RiftWizard.STATE_CONFIRM, RiftWizard.PyGameView.draw_confirm, RiftWizard.PyGameView.process_confirm_input, False),
	Menu(RiftWizard.STATE_COMBAT_LOG, RiftWizard.PyGameView.draw_combat_log, RiftWizard.PyGameView.process_combat_log_input, False),
]
menu_transition_overrides = []

id_counter = 99

def on_run_draw(self):
	global menus
	cur_menu = [menu for menu in menus if menu.id == self.state][0]

	cur_menu.draw_function(self)

	if not cur_menu.blocks_char_sheet_and_examine:
		if self.game:
			RiftWizard.PyGameView.draw_character(self)
		if self.game or self.state == RiftWizard.STATE_SHOP:
			RiftWizard.PyGameView.draw_examine(self)

def on_run_process_input(self):
	global menus
	cur_menu = [menu for menu in menus if menu.id == self.state][0]

	prev_state = self.state
	cur_menu.process_input(self)
	new_state = self.state

	global menu_transition_overrides
	state_transition_overrides = [override for (fro, to, override, condition) in menu_transition_overrides if condition(self) and fro == prev_state and to == new_state]
	if len(state_transition_overrides) > 0:
		self.state = state_transition_overrides[0]




# api
def add_menu(draw_function, process_input_function, blocks_char_sheet_and_examine=True):
	global menus
	global id_counter
	id_counter += 1

	menus.append(Menu(id_counter, draw_function, process_input_function, blocks_char_sheet_and_examine))

	return id_counter


def override_menu(menu_id, draw_function, process_input_function):
	global menus
	menu = [menu for menu in menus if menu.id == menu_id][0]
	menu_index = menus.index(menu)

	menus[menu_index] = Menu(menu_id, draw_function, process_input_function, menu.blocks_char_sheet_and_examine)


def override_menu_transition(menu_from, menu_to, override, condition = (lambda pygameview: True)):
	global menu_transition_overrides
	menu_transition_overrides.append((menu_from, menu_to, override, condition))