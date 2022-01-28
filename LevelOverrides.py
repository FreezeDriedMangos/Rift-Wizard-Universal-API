import Level
import mods.API_Universal.APIs.API_Disrupt.API_Disrupt as API_Disrupt
import mods.API_Universal.APIs.API_Turns.API_Turns as API_Turns


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


def portal_disrupt(self, caster):
	API_Disrupt.disrupt_default(self, caster)
Level.Portal.disrupt = portal_disrupt

Level.Level.iter_frame = API_Turns.iter_frame

if API_Multiplayer:
	Level.Level.iter_frame = API_Multiplayer.Level_iter_frame
	Level.ItemPickup.on_player_enter = API_Multiplayer.on_player_enter
	Level.Unit.advance = API_Multiplayer.Unit_advance