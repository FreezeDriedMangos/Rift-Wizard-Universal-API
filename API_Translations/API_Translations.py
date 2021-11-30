

import mods.API_Universal.API_OptionsMenu.API_OptionsMenu as API_OptionsMenu
import os

NO_TRANSLATION = 'English (default)'

translations = [NO_TRANSLATION]
def initialize():
	global translations
	if not os.path.exists(os.path.join('mods','API_Universal','translations')):
		return

	for f in os.listdir(os.path.join('mods','API_Universal','translations')):
		if os.path.isdir(os.path.join('mods','API_Universal','translations', f)):
			continue
		
		translations.append(f.split('.')[0])

initialize()



def translation_changed(self, cur_value):
	self.options['translation'] = cur_value
	load_translation(self)


translation = None
def load_translation(self):
	if self.options['translation'] == NO_TRANSLATION:
		return

	global translation
	translation = dict()
	translation_filename = self.options['translation'] + '.txt'

	with open(os.path.join('mods','API_Universal','translations', translation_filename)) as f:
		for line in f:
			split_line = line.split('\t')
			if len(split_line) <= 1:
				print('WARNING: translation file ' + translation_filename + ' - no tab character found on line: ' + line)
				continue
			(english, translated) = split_line
			translation[english] = translated


untranslated_strings = set()
def translate(string):
	if translation == None:
		return string

	if not string in translation:
		global untranslated_strings
		if string not in untranslated_strings:
			print(string)
			untranslated_strings.add(string)
		return string

	return translation[string]






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
