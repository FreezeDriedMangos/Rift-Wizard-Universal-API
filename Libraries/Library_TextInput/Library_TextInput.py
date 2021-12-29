import pygame
import math

class TextInput():
	def __init__(self):
		self.font = None
		self.linesize = None

		self.text = ""
		self.has_focus = False
		self.confirmed = False

		self.confirm_callback = None
		self.abort_callback = None

		self.blink_count = 15
		self.blink_freq = 15

		self.selection_highlight_width = 30

		self.placeholder_text = "type here"

	def draw(self, pygameview, x, y, draw_panel, center=False):
		if self.font == None:
			self.font = pygameview.font
		if self.linesize == None:
			self.linesize = pygameview.linesize
	
		draw_placeholder = bool(self.text == '') and not self.has_focus
		text = self.placeholder_text if draw_placeholder else self.text

		if self.has_focus:
			text = ' '+text +'|' if self.blink_count//self.blink_freq == 1 else ' '+text+' '
		else:
			text = text

		if center:
			text = " "*math.floor(self.selection_highlight_width/2) + text + " "*math.ceil(self.selection_highlight_width/2)
		else:
			text = text + " "*self.selection_highlight_width
		
		if center:
			x -= self.font.size(text)[0]//2

		old_linesize = pygameview.linesize
		pygameview.linesize = self.linesize # :(
		pygameview.draw_string(text, draw_panel, x, y, font=self.font, mouse_content=self, color=(50, 50, 50) if draw_placeholder else (255, 255, 255))
		pygameview.linesize = old_linesize

		self.blink_count += 1
		self.blink_count %= self.blink_freq*2

	def give_focus(self):
		self.has_focus = True
		self.confirmed = False
	
	def remove_focus(self):
		self.has_focus = False

	def process_input(self, pygameview, KEY_BIND_ABORT, KEY_BIND_CONFIRM):
		for evt in pygameview.events:
			if evt.type != pygame.KEYDOWN:
				continue
			
			if not self.has_focus:
				return

			if evt.key in pygameview.key_binds[KEY_BIND_CONFIRM]:
				self.remove_focus()
				self.confirmed = True
				pygameview.play_sound('menu_confirm')
				if hasattr(self, 'confirm_callback') and self.confirm_callback:
					self.confirm_callback(self.text)
			elif evt.key in pygameview.key_binds[KEY_BIND_ABORT]:
				self.remove_focus()
				pygameview.play_sound('menu_abort')
				if self.abort_callback:
					self.abort_callback(self.text)
			elif evt.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]
			elif hasattr(evt, 'unicode'):
				self.text += evt.unicode