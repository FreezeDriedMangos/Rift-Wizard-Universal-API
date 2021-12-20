from collections import defaultdict, namedtuple, OrderedDict
import sys
import inspect 
import os
import pygame
import random

import Level

frm = inspect.stack()[-1]
RiftWizard = inspect.getmodule(frm[0])

#TagEffect = namedtuple("TagEffect", "tag path")

tag_effects = {}

## Patch load_effect_images 
#__load_effect_images_old = RiftWizard.PyGameView.load_effect_images
#
#def load_effect_images(self):
#	__load_effect_images_old(self)
#	
#	for tag_effect in tag_effects:
#		path = tag_effect.path+'.png'
#		minor_path = tag_effect.path+'_0.png'
#		if os.path.exists(path):
#			self.effect_images[tag.color.to_tup()] = pygame.image.load(path)
#		if os.path.exists(minor_path):
#			self.minor_effect_images[tag.color.to_tup()] = pygame.image.load(minor_path)
#	
#RiftWizard.PyGameView.load_effect_images = load_effect_images

## Patch get_effect 
# __get_effect_old = RiftWizard.PyGameView.get_effect

def get_effect(self, effect, color=None, *args, **kvargs):
	if(effect.color in tag_effects):
		function = tag_effects[effect.color]
		return function(effect, color)
	# return __get_effect_old(self, effect, color, *args, **kvargs)
	return None
	
# RiftWizard.PyGameView.get_effect = get_effect

class ColorUnique(Level.Color):
	def __init__(self):
		Level.Color.__init__(self)

	def __hash__(self):
		return object.__hash__(self)

	def __eq__(self, other):
		return object.__eq__(self, other)

	def __str__(self):
		return "<ColorUnique>"

###########
### API ###
###########


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
def add_tag_effect(tag, function):
	if(isinstance(tag, str)): #we got a name instead, make a new tag
		tag = Level.Tag(tag, ColorUnique())
		Level.Tags.elements.append(tag)
	
	tag_effects[tag.color] = function
	
# Adds an effect to a tag
# tag - a Level.Tag. Your tag's color will be used as a key, so it should be unique. If a string is passed instead, it will create the tag for you.
# path - the path to your effect png, excluding the file extension. You should use os.path.join to create your path.
# 
# there is also a minor effect automatically created for you for projectiles, if you have a <name>_0.png.
#
# example usage:
#     add_tag_effect(Level.Tags.BlueFire, os.path.join('mods','ExampleMod','fireball_blue.png'))
def add_tag_effect_simple(tag, path_base):
	path = path_base + '.png'
	path_minor = path_base + '_0.png'
	if os.path.exists(path):
		image = pygame.image.load(path)
	if os.path.exists(path_minor):
		image_minor = pygame.image.load(path_minor)
		
	def func(effect, color):
		if effect.minor and image_minor:
			return RiftWizard.SimpleSprite(effect.x, effect.y, image_minor, speed=1)
		else:
			return RiftWizard.SimpleSprite(effect.x, effect.y, image, speed=1)
	
	add_tag_effect(tag, func)
	


