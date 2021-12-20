import pygame
import math

class TextInput():
	def __init__(self):
		self.font = None
		self.text = ""
		self.has_focus = False
		self.confirmed = False

		self.comfirm_callback = None
		self.abort_callback = None

		self.blink_count = 0
		self.blink_freq = 10

		self.selection_highlight_width = 30

	def draw(self, pygameview, x, y, draw_panel, center=False):
		if self.font == None:
			self.font = pygameview.font

		if center:
			x -= self.font.size(self.text)[0]//2
	
		text = self.text +'|' if self.blink_count//2 == 1 and self.has_focus else self.text
		text = " "*math.floor(self.selection_highlight_width/2) + self.text + " "*math.ceil(self.selection_highlight_width/2) if center else self.text + " "*self.selection_highlight_width
		self.draw_string(text, draw_panel, x, y, font=self.font, mouse_content=self)

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

			if evt.key in pygame.key_binds[KEY_BIND_CONFIRM]:
				self.remove_focus()
				self.confirmed = True
				if self.confirm_callback:
					self.confirm_callback(self.text)
			elif evt.key in self.key_binds[KEY_BIND_ABORT]:
				self.remove_focus()
				if self.abort_callback:
					self.abort_callback(self.text)
			elif evt.key == pygame.K_BACKSPACE:
				self.text = self.text[:-1]
			elif hasattr(evt, 'unicode'):
				self.text += evt.unicode