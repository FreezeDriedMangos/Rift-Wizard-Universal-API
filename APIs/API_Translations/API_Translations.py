

import mods.API_Universal.APIs.API_OptionsMenu.API_OptionsMenu as API_OptionsMenu
import os
import pygame

NO_TRANSLATION = 'English (default)'

translations = [NO_TRANSLATION]
def initialize():
	global translations
	if not os.path.exists(os.path.join('mods','API_Universal','translations')):
		return

	for f in os.listdir(os.path.join('mods','API_Universal','translations')):
		if os.path.isdir(os.path.join('mods','API_Universal','translations', f)):
			translations.append(f)
		

initialize()



def translation_changed(self, cur_value):
	self.options['translation'] = cur_value
	load_translation(self)


translation = None
translation_font = None
def load_translation(self):

	global translation
	global translation_font	
	translation = dict()
	translation_folder = os.path.join('mods','API_Universal','translations',self.options['translation'])
	translation_filename = None
	font_filename = None

	if self.options['translation'] == NO_TRANSLATION or not os.path.exists(translation_folder):
		translation = None
		translation_font = None
		return
	

	for f in os.listdir(translation_folder):
		if os.path.isdir(os.path.join('mods','API_Universal','translations', f)):
			continue
		
		extension = f.split('.')[-1]

		if extension == 'csv':
			translation_filename = f
		elif extension == 'ttf':
			font_filename = f


	if translation_filename == None:
		translation = None
		translation_font = None
		return


	with open(os.path.join('mods','API_Universal','translations', self.options['translation'], translation_filename), 'r', encoding='utf-8') as f:
		for line in f:
			split_line = line.split('\t')
			if len(split_line) <= 1:
				print('WARNING: translation file ' + translation_filename + ' - no tab character found on line: ' + line)
				continue
			(english, translated) = split_line
			translation[english] = translated
	
	if font_filename != None:
		font_path = os.path.join('mods','API_Universal','translations', self.options['translation'], font_filename)
		translation_font = pygame.font.Font(font_path, 16)
	else:
		translation_font = None

untranslated_strings = set()
def declare_untranslated_string(string):
	# global untranslated_strings
	# if string not in untranslated_strings:
	# 	print(string)
	# 	untranslated_strings.add(string)
	pass

import re
def translate(string):
	if translation == None:
		return string

	if string in translation:
		return translation[string]

	# attempt to translate word by word
	exp = '[\[\]:|\w\|\'|%|-]+|.| |,'
	words = re.findall(exp, string)
	words.reverse()

	translated_string = ''
	for word in words:
		if word in translation:
			translated_string += translation[word]
		elif word and word[0] == '[' and word[-1] == ']':
			translated_string += '['

			tokens = word[1:-1].split(':')
			if len(tokens) == 1:
				# ex [fire] -> [fuego:fire]
				word = tokens[0]

				if word in translation:
					translated_string += '['+translation[word]+':'+word+']'
				else:
					translated_string += '['+word+']'
					declare_untranslated_string(word)

				translated_string += word
				
			elif len(tokens) == 2:
				# ex [2_fire_damage:fire] -> [2_daños_por_fuego:fire]
				word = tokens[0].replace('_', ' ')

				if word in translation:
					translated_string += translation[w]
				else:
					word = word.split(' ')
					for (w, i) in zip(word, range(len(word))):
						
						if w in translation:
							translated_string += translation[w]
						else:
							translated_string += w
							declare_untranslated_string(w)

						if i < len(word)-1:
							translated_string += '_'

				translated_string += ":"+tokens[1]+"]" # reconstruct the original tag (the tooltip_colors dict is in english regardless of the translation loaded)
		else:
			translated_string += word
			declare_untranslated_string(word)
		
	return string

	


def get_language_font(self):
	return translation_font




def initialize_translation_option(self):
	if not 'translation' in self.options:
		self.options['translation'] = NO_TRANSLATION
	load_translation(self)

API_OptionsMenu.add_option(
	lambda self, cur_value: "Language: " + cur_value, 
	lambda self: self.options['translation'], 
	translations, 
	'translation_option', 
	trigger_on_select=translation_changed, 
	option_wraps=True, 
	initialize_option=initialize_translation_option
)
API_OptionsMenu.add_blank_option_line()
