import Game
import Level
import mods.API_Universal.APIs.API_Boss.API_Boss as API_Boss
import mods.API_Universal.APIs.API_WinCondition.API_WinCondition as API_WinCondition

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


__check_triggers_old = Game.Game.check_triggers
def check_triggers(self):
	API_Boss.check_triggers_pre(self)
	API_WinCondition.check_triggers_pre(self)

	if API_Multiplayer:
		API_Multiplayer.check_triggers(self)
	else:
		__check_triggers_old(self)

	API_WinCondition.check_triggers_post(self)
	API_Boss.check_triggers_post(self)
Game.Game.check_triggers = check_triggers


if API_Multiplayer:
	print('overriding stuff')
	Game.Game.buy_upgrade = API_Multiplayer.Game_buy_upgrade
	Game.Game.can_buy_upgrade = API_Multiplayer.Game_can_buy_upgrade
	Game.Game.can_shop = API_Multiplayer.Game_can_shop
	Game.Game.enter_portal = API_Multiplayer.enter_portal
	Game.Game.get_upgrade_cost = API_Multiplayer.Game_get_upgrade_cost
	Game.Game.has_upgrade = API_Multiplayer.Game_has_upgrade
	Game.Game.is_awaiting_input = API_Multiplayer.Game_is_awaiting_input
	Game.Game.save_game = API_Multiplayer.save_game_wrapper
	Game.Game.try_cast = API_Multiplayer.Game_try_cast
	Game.Game.try_deploy = API_Multiplayer.try_deploy
	Game.Game.try_move = API_Multiplayer.Game_try_move
	Game.Game.try_shop = API_Multiplayer.Game_try_shop

