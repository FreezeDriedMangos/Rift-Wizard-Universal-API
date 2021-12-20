# Selecting a Translation In-Game

to select the translation you'd like to play with, open the options menu. there'll be an option called 'Language'

# Making a Translation

to make a translation, make a folder with the name of your translation (ex `Pirate Speak by Clay`) inside the folder `mods/API_Universal/translations`
inside that folder, make a csv file. give it the same name as your folder

on each line of that file, put the English text to be translated, a tab character, and then the text it translates into. Any text that hasn't been translated will be printed to the console (the black window RiftWizard opens in the background). Copy/paste from that window to get a head start on a list of text that needs to be translated (much easier than typing all the english text out manually)

if your language uses characters that RiftWizard's font doesn't support, add a ttf file to your translation folder. The translation API will automatically use it instead

see JP_language for an example