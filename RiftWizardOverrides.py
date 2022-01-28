


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

import Level

import mods.API_Universal.APIs.API_Effect.API_Effect as API_Effect
import mods.API_Universal.APIs.API_Translations.API_Translations as API_Translations
import mods.API_Universal.APIs.API_OptionsMenu.API_OptionsMenu as API_OptionsMenu
import mods.API_Universal.APIs.API_TitleMenus.API_TitleMenus as API_TitleMenus
import mods.API_Universal.APIs.API_Music.API_Music as API_Music
import mods.API_Universal.APIs.API_Spells.API_Spells as API_Spells
import mods.API_Universal.APIs.API_DrawLevel.API_DrawLevel as API_DrawLevel
import mods.API_Universal.APIs.API_DrawPanel.API_DrawPanel as API_DrawPanel
import mods.API_Universal.EventSystem as EventSystem

# ----------------------------------------------------------------------------------------+
# try to import API_Multiplayer from either the mods/ folder or the API_Univerasl/ folder |
# -------------------------------                                                         |
try:                                                 
	import mods.API_Multiplayer.API_Multiplayer as API_Multiplayer
except:
	try:
		import mods.API_Universal.API_Multiplayer.API_Multiplayer as API_Multiplayer
	except:
		API_Multiplayer = False
		pass                                            
#                                                                                         |
#                                                                                         |
# ----------------------------------------------------------------------------------------+

EventSystem.__add_event('PyGameView.on_frame')
EventSystem.__add_event('PyGameView.on_exit')

__get_effect_old = RiftWizard.PyGameView.get_effect

def get_effect(self, effect, color=None, *args, **kvargs):
	val = API_Effect.get_effect(self, effect, color=None, *args, **kvargs)
	if val:
		return val
	return __get_effect_old(self, effect, color, *args, **kvargs)
	
RiftWizard.PyGameView.get_effect = get_effect


# I'm lazy
if API_Multiplayer:
	def draw_string(self, string, surface, x, y, color=(255, 255, 255), mouse_content=None, content_width=None, center=False, char_panel=False, font=None, player=None):
		string = API_Translations.translate(string)
		translation_font = API_Translations.get_language_font(self)
		font = font if translation_font == None else translation_font

		API_Multiplayer.draw_string(self, string, surface, x, y, color=color, mouse_content=mouse_content, content_width=content_width, center=center, char_panel=char_panel, font=font, player=player)
	RiftWizard.PyGameView.draw_string = draw_string
else:
	__draw_string_old = RiftWizard.PyGameView.draw_string
	def draw_string(self, string, surface, x, y, color=(255, 255, 255), mouse_content=None, content_width=None, center=False, char_panel=False, font=None):
		string = API_Translations.translate(string)
		translation_font = API_Translations.get_language_font(self)
		font = font if translation_font == None else translation_font

		__draw_string_old(self, string, surface, x, y, color=color, mouse_content=mouse_content, content_width=content_width, center=center, char_panel=char_panel, font=font)
	RiftWizard.PyGameView.draw_string = draw_string



__draw_wrapped_string_old = RiftWizard.PyGameView.draw_wrapped_string
def draw_wrapped_string(self, string, surface, x, y, width, color=(255, 255, 255), center=False, indent=False, extra_space=False):
	string = API_Translations.translate(string)
	translation_font = API_Translations.get_language_font(self)
	font = self.font if translation_font == None else translation_font

	old_font = self.font
	self.font = font # because draw_wrapped_string doesn't take a font argument :(
	retval = __draw_wrapped_string_old(self, string, surface, x, y, width, color=color, center=center, indent=indent, extra_space=extra_space)
	self.font = old_font

	return retval
RiftWizard.PyGameView.draw_wrapped_string = draw_wrapped_string


__pygameview_init_old = RiftWizard.PyGameView.__init__
def pygameview_init(self, *args, **kwargs):
	__pygameview_init_old(self, *args, **kwargs)
	API_OptionsMenu.try_initialize_options(self)
	API_Spells.pygameview_init(self)
RiftWizard.PyGameView.__init__ = pygameview_init


API_TitleMenus.override_menu(RiftWizard.STATE_OPTIONS, API_OptionsMenu.draw_options_menu, API_OptionsMenu.process_options_input)





__deploy_old = RiftWizard.PyGameView.deploy
def deploy(self, p):
	if API_Multiplayer:
		API_Multiplayer.deploy(self, p)
	else:
		__deploy_old(self, p)
	API_Music.play_music(self, 'battle_2')
RiftWizard.PyGameView.deploy = deploy


def play_music(self, track_name):
	API_Music.play_music(self, track_name)
RiftWizard.PyGameView.play_music = play_music





def get_repeatable_keys(self):
	if API_Multiplayer:
		return API_Multiplayer.get_repeatable_keys(self)

	repeatable_keybinds = [
		RiftWizard.KEY_BIND_UP,
		RiftWizard.KEY_BIND_DOWN,
		RiftWizard.KEY_BIND_LEFT,
		RiftWizard.KEY_BIND_RIGHT,
		RiftWizard.KEY_BIND_UP_RIGHT,
		RiftWizard.KEY_BIND_UP_LEFT,
		RiftWizard.KEY_BIND_DOWN_RIGHT,
		RiftWizard.KEY_BIND_DOWN_LEFT,
		RiftWizard.KEY_BIND_PASS
	]
	
	return [key for kb in repeatable_keybinds for key in self.key_binds[kb]]
		
RiftWizard.PyGameView.get_repeatable_keys = get_repeatable_keys

RiftWizard.PyGameView.draw_level = API_DrawLevel.draw_level

RiftWizard.PyGameView.draw_character = API_DrawPanel.draw_character

import gc
import time
import pygame
# Add support for API_TitleMenus
# future: Add support for idle animations up to 100000 frames long
	# TODO: adding the above breaks tile overlays
# Add support for holding down movement keys after rebinding them
# future: support for online multiplayer
def run(self):

	self.running = True
	profile = False

	# Disable garbage collection, manually collect at start of each level
	# Cause the game takes ~40mb of RAM and the occasionall hiccup is not worth it
	gc.disable()
	frame_time = 0
	while self.running:
		if API_Multiplayer:
			API_Multiplayer.on_run_frame_start(self)

		RiftWizard.cloud_frame_clock += 1
		RiftWizard.cloud_frame_clock %= 100000 

		RiftWizard.idle_subframe += 1
		if RiftWizard.idle_subframe >= RiftWizard.SUB_FRAMES[RiftWizard.ANIM_IDLE]:
			RiftWizard.idle_subframe = 0
			RiftWizard.idle_frame += 1
			# RiftWizard.idle_frame = RiftWizard.idle_frame % 100000 # changed this from 2 to 100000 so that idle animations can have up to 100000 frames in them
			RiftWizard.idle_frame = RiftWizard.idle_frame % 2 
			
		self.clock.tick(30)
		
		EventSystem.__trigger_listeners('PyGameView.on_frame', self)

		self.events = pygame.event.get()

		keys = pygame.key.get_pressed()
		for repeat_key, repeat_time in list(self.repeat_keys.items()):

			if keys[repeat_key] and time.time() > repeat_time:
				self.events.append(pygame.event.Event(pygame.KEYDOWN, key=repeat_key))
				self.repeat_keys[repeat_key] = time.time() + RiftWizard.REPEAT_INTERVAL

			if not keys[repeat_key]:
				del self.repeat_keys[repeat_key]

		for event in self.events:
			if event.type == pygame.QUIT:
				if self.game and (self.game.p1.is_alive() or self.game.p2.is_alive()):
					self.game.save_game()
				self.running = False
				EventSystem.__trigger_listeners('PyGameView.on_exit', self)

			# Allow repeating of directional keys (but no other keys)
			if event.type == pygame.KEYDOWN and event.key not in self.repeat_keys:
				if event.key in self.get_repeatable_keys(): # I added this function call in to allow repeatable keys to work with new keybinds (and also p2 movement keys)
					self.repeat_keys[event.key] = time.time() + RiftWizard.REPEAT_DELAY

			if event.type == pygame.VIDEORESIZE:
				self.resize_window(event)

		if profile:
			import cProfile
			import pstats
			pr = cProfile.Profile()

			start = time.time()
			
			pr.enable()

		self.ui_rects = []

		self.mouse_dx, self.mouse_dy = pygame.mouse.get_rel()
		
		# Reset examine target if mouse was moved and not in any ui rects
		if self.mouse_dy or self.mouse_dx:
			mx, my = self.get_mouse_pos()
			if self.state == RiftWizard.STATE_TITLE:
				pass
			elif self.state == RiftWizard.STATE_LEVEL and mx > self.h_margin:
				pass
			elif self.state == RiftWizard.STATE_REBIND:
				pass
			else:
				self.examine_target = None

		self.frameno += 1
		
		if self.gameover_frames < 8:
			self.screen.fill((0, 0, 0))
		elif self.game:
			self.draw_gameover()


		# here's where I add the code for drawing custom menus
		API_TitleMenus.on_run_draw(self)


		if self.game and profile and frame_time > (1.0 / 60.0):
			pygame.draw.rect(self.screen, (255, 0, 0), (0, 0, 5, 5))
		self.draw_screen()

		if self.state in [RiftWizard.STATE_LEVEL, RiftWizard.STATE_CHAR_SHEET, RiftWizard.STATE_SHOP]:
			self.process_examine_panel_input()

		advanced = False
		delay_menu_process = False
		if self.game and self.state == RiftWizard.STATE_LEVEL:
			level = self.get_display_level()
			# If any creatuers are doing a cast anim, do not process effects or spells or later moves
			#if any(u.Anim.anim == ANIM_ATTACK for u in level.units):
			#	continue

			if self.game.gameover or self.game.victory:
				self.gameover_frames += 1

			if self.gameover_frames == 4:
				# Redo the level end screenshot so that it has the red mordred (or wizard) flash frame
				self.make_level_end_screenshot()
				self.make_game_end_screenshot()

				# Force level finish on victory- the level might not be finished but we are done
				if self.game.victory:
					self.play_music('victory_theme')

			if self.game and self.game.deploying and not self.deploy_target:
				self.deploy_target = Level.Point(self.game.p1.x, self.game.p1.y)
				self.tab_targets = [t for t in self.game.next_level.iter_tiles() if isinstance(t.prop, Level.Portal)]

			prev_state = self.state
			self.process_level_input()
			if prev_state != self.state: # If we're opening a menu from the Level, delay menu process for one tick, fixes ESC and charsheet processing
				delay_menu_process = True

			if self.game and self.game.victory_evt:
				self.game.victory_evt = False
				self.on_level_finish()

			if self.game and not self.game.is_awaiting_input() and not self.gameover_frames:
				self.threat_zone = None
				advanced = True

				top_spell = self.game.cur_level.active_spells[0] if self.game.cur_level.active_spells else None
				self.game.advance()
				# Do another spell advance on speed 1
				if self.options['spell_speed'] == 1:
					if self.game.cur_level.active_spells and top_spell and top_spell == self.game.cur_level.active_spells[0]:
						self.game.advance()
				# Continually spell advance on speed 2 until the top spell is finished
				if self.options['spell_speed'] == 2:
					while self.game.cur_level.active_spells and top_spell == self.game.cur_level.active_spells[0]:
						self.game.advance()
				# Continually advance everything in super turbo, attemptng to do full turn in 1 go
				if self.options['spell_speed'] == 3:
					while not self.game.is_awaiting_input() and not self.game.gameover and not self.game.victory:
						self.game.advance()

				# Check triggers
				if level.cur_shop:
					if API_Multiplayer:
						self.open_shop(RiftWizard.SHOP_TYPE_SHOP, player = self.game.p1 if level.cur_shop.x == self.game.p1.x and level.cur_shop.y == self.game.p1.y else self.game.p2)
					else:
						self.open_shop(RiftWizard.SHOP_TYPE_SHOP)

		if not delay_menu_process:
			# here's wehre I add code for input for custom menus
			API_TitleMenus.on_run_process_input(self)
		
		# If not examining anything- examine cur spell if possible
		if not self.examine_target and self.cur_spell and self.cur_spell.show_tt:
			self.examine_target = self.cur_spell

		if self.game and profile:
			pr.disable()

			finish = time.time()
			frame_time = finish - start

			if frame_time > 1 / 10.0:
				print("draw time ms: %f" % (frame_time * 1000))
				stats = pstats.Stats(pr)
				stats.sort_stats("cumtime")
				stats.dump_stats("draw_profile.stats")
				stats.print_stats()
RiftWizard.PyGameView.run = run


if API_Multiplayer:
	RiftWizard.PyGameView.abort_buy = API_Multiplayer.abort_buy
	RiftWizard.PyGameView.abort_cur_spell = API_Multiplayer.abort_cur_spell
	RiftWizard.PyGameView.adjust_char_sheet_selection = API_Multiplayer.adjust_char_sheet_selection
	RiftWizard.PyGameView.autopickup = API_Multiplayer.autopickup
	RiftWizard.PyGameView.cast_cur_spell = API_Multiplayer.cast_cur_spell
	RiftWizard.PyGameView.choose_spell = API_Multiplayer.choose_spell
	RiftWizard.PyGameView.close_shop = API_Multiplayer.close_shop
	RiftWizard.PyGameView.confirm_buy = API_Multiplayer.confirm_buy
	RiftWizard.PyGameView.cycle_tab_targets = API_Multiplayer.cycle_tab_targets
	# RiftWizard.PyGameView.deploy = API_Multiplayer.deploy                  
	RiftWizard.PyGameView.draw_char_sheet = API_Multiplayer.draw_char_sheet  # TODO: integrate with API_Menus
	RiftWizard.PyGameView.draw_character = API_Multiplayer.draw_character    # TODO: integrate with API_Menus
	RiftWizard.PyGameView.draw_key_rebind = API_Multiplayer.draw_key_rebind  # TODO: integrate with API_Menus
	RiftWizard.PyGameView.draw_level = API_Multiplayer.draw_level            # TODO: integrate with API_Menus
	RiftWizard.PyGameView.draw_shop = API_Multiplayer.draw_shop              # TODO: integrate with API_Menus
	# RiftWizard.PyGameView.draw_string = API_Multiplayer.draw_string        
	RiftWizard.PyGameView.draw_title = API_Multiplayer.draw_title            # TODO: integrate with API_Menus
	# RiftWizard.PyGameView.get_repeatable_keys = API_Multiplayer.get_repeatable_keys
	RiftWizard.PyGameView.get_shop_options = API_Multiplayer.get_shop_options
	RiftWizard.PyGameView.get_surface_pos = API_Multiplayer.get_surface_pos
	RiftWizard.PyGameView.key_bind_select_option = API_Multiplayer.key_bind_select_option
	RiftWizard.PyGameView.load_game = API_Multiplayer.load_game
	RiftWizard.PyGameView.new_game = API_Multiplayer.new_game
	RiftWizard.PyGameView.open_buy_prompt = API_Multiplayer.open_buy_prompt
	RiftWizard.PyGameView.open_shop = API_Multiplayer.open_shop
	RiftWizard.PyGameView.process_char_sheet_input = API_Multiplayer.process_char_sheet_input   # TODO: integrate with API_Menus
	RiftWizard.PyGameView.process_click_character = API_Multiplayer.process_click_character  # TODO: integrate with API_Menus
	RiftWizard.PyGameView.process_combat_log_input = API_Multiplayer.process_combat_log_input  # TODO: integrate with API_Menus
	RiftWizard.PyGameView.process_confirm_input = API_Multiplayer.process_confirm_input  # TODO: integrate with API_Menus
	RiftWizard.PyGameView.process_key_rebind = API_Multiplayer.process_key_rebind  # TODO: integrate with API_Menus
	RiftWizard.PyGameView.process_level_input = API_Multiplayer.process_level_input  # TODO: integrate with API_Menus
	RiftWizard.PyGameView.process_shop_input = API_Multiplayer.process_shop_input  # TODO: integrate with API_Menus
	RiftWizard.PyGameView.process_title_input = API_Multiplayer.process_title_input  # TODO: integrate with API_Menus
	# RiftWizard.PyGameView.run = run
	RiftWizard.PyGameView.try_buy_shop_selection = API_Multiplayer.try_buy_shop_selection
	RiftWizard.PyGameView.try_move = API_Multiplayer.PyGameView_try_move


	# TODO: move all API_TitleMenu calls from API_Multiplayer into a function I can call from here