from collections import defaultdict, namedtuple, OrderedDict
import Level
import inspect 
import Game
import os

frm = inspect.stack()[-1]
RiftWizard = inspect.getmodule(frm[0])

tag_keybinds = []
tag_tooltips = []

__pygameview_init_old = RiftWizard.PyGameView.__init__

def pygameview_init(self, *args, **kwargs):
	__pygameview_init_old(self, *args, **kwargs)
	
	for tag, keybind in tag_keybinds: #setup keybinds
		self.tag_keys[keybind.lower()] = tag
		self.reverse_tag_keys[tag] = keybind.upper()
		
	for tag in tag_tooltips: #setup tag tooltip colors
		RiftWizard.tooltip_colors[tag.name.lower()] = tag.color
	
RiftWizard.PyGameView.__init__ = pygameview_init

###########################
### Multi-Target Spells ###
###########################

def has_enough_targets(self):
	return True

Level.Spell.has_enough_targets = has_enough_targets

__spell_init_old = Level.Spell.__init__

def spell_init(self, *args, **kwargs):
	__spell_init_old(self, *args, **kwargs)
	
	self.multi_targets = []

Level.Spell.__init__ = spell_init

__game_try_cast_old = Game.Game.try_cast

def try_cast(self, spell, x, y, *args, **kwargs):
	if spell.can_cast(x, y):
		spell.multi_targets.append(Level.Point(x, y)) #Append a target
		if(spell.has_enough_targets()):
			return __game_try_cast_old(self, spell, x, y, *args, **kwargs)
		else:
			return True
	else:
		return False
	
Game.Game.try_cast = try_cast
	
def cast_cur_spell(self):
	success = self.game.try_cast(self.cur_spell, self.cur_spell_target.x, self.cur_spell_target.y)
	has_enough_targets = self.cur_spell.has_enough_targets()
	if not success:
		self.play_sound('menu_abort')
	elif not has_enough_targets:
		self.play_sound('menu_confirm')
	#if self.examine_target == self.cur_spell:
		#self.examine_target = None
	if not success or has_enough_targets:
		self.cur_spell = None
		unit = self.game.cur_level.get_unit_at(self.cur_spell_target.x, self.cur_spell_target.y)
		if unit:
			self.cur_spell_target = unit
	
RiftWizard.PyGameView.cast_cur_spell = cast_cur_spell #override completely
	
__pygameview_choose_spell_old = RiftWizard.PyGameView.choose_spell

def choose_spell(self, spell):
	__pygameview_choose_spell_old(self, spell)
	spell.multi_targets = [] #reset targets

RiftWizard.PyGameView.choose_spell = choose_spell

###########
### API ###
###########

# Adds a tag to the spell/skill shop.
# 
# tag - The tag to add
# keybind - A keybind, as a string, can be either lowercase or uppercase
def add_tag_keybind(tag, keybind):
	tag_keybinds.append((tag, keybind))
		
# Adds a tag to the tooltip colors.
# 
# tag - The tag to add, the color will be taken from the tag
def add_tag_tooltip(tag):
	tag_tooltips.append(tag)