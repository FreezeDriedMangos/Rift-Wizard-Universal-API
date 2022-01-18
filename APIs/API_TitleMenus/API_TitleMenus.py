

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
import mods.API_Universal.APIs.API_DrawPanel.API_DrawPanel as API_DrawPanel


Menu = namedtuple('Menu', 'id draw_function process_input blocks_char_sheet_and_examine')
menus = [
	Menu(RiftWizard.STATE_TITLE, lambda self: RiftWizard.PyGameView.draw_title(self), lambda self: RiftWizard.PyGameView.process_title_input(self), True),
	Menu(RiftWizard.STATE_PICK_MODE, lambda self: RiftWizard.PyGameView.draw_pick_mode(self), lambda self: RiftWizard.PyGameView.process_pick_mode_input(self), True),
	Menu(RiftWizard.STATE_PICK_TRIAL, lambda self: RiftWizard.PyGameView.draw_pick_trial(self), lambda self: RiftWizard.PyGameView.process_pick_trial_input(self), True),
	Menu(RiftWizard.STATE_OPTIONS, lambda self: RiftWizard.PyGameView.draw_options_menu(self), lambda self: RiftWizard.PyGameView.process_options_input(self), True),
	Menu(RiftWizard.STATE_REBIND, lambda self: RiftWizard.PyGameView.draw_key_rebind(self), lambda self: RiftWizard.PyGameView.process_key_rebind(self), True),
	Menu(RiftWizard.STATE_MESSAGE, lambda self: RiftWizard.PyGameView.draw_message(self), lambda self: RiftWizard.PyGameView.process_message_input(self), True),
	Menu(RiftWizard.STATE_REMINISCE, lambda self: RiftWizard.PyGameView.draw_reminisce(self), lambda self: RiftWizard.PyGameView.process_reminisce_input(self), True),
	Menu(RiftWizard.STATE_LEVEL, lambda self: RiftWizard.PyGameView.draw_level(self), lambda self: None, False),
	Menu(RiftWizard.STATE_CHAR_SHEET, lambda self: RiftWizard.PyGameView.draw_char_sheet(self), lambda self: RiftWizard.PyGameView.process_char_sheet_input(self), False),
	Menu(RiftWizard.STATE_SHOP, lambda self: RiftWizard.PyGameView.draw_shop(self), lambda self: RiftWizard.PyGameView.process_shop_input(self), False),
	Menu(RiftWizard.STATE_CONFIRM, lambda self: RiftWizard.PyGameView.draw_confirm(self), lambda self: RiftWizard.PyGameView.process_confirm_input(self), False),
	Menu(RiftWizard.STATE_COMBAT_LOG, lambda self: RiftWizard.PyGameView.draw_combat_log(self), lambda self: RiftWizard.PyGameView.process_combat_log_input(self), False),
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

	if new_state == prev_state and not cur_menu.blocks_char_sheet_and_examine:
		API_DrawPanel.process_input_character(self)

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