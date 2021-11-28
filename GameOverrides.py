import Game
import mods.API_Universal.API_Boss.API_Boss as API_Boss

def check_triggers(self):
	API_Boss.check_triggers(self)
Game.Game.check_triggers = check_triggers