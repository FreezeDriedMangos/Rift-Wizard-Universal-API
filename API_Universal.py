
import mods.API_Universal.ConsumablesOverrides
import mods.API_Universal.GameOverrides
import mods.API_Universal.LevelGenOverrides
import mods.API_Universal.LevelOverrides
import mods.API_Universal.RiftWizardOverrides
import mods.API_Universal.ShrinesOverrides

import mods.API_Universal.Modred


#
# Example usage: 
# import mods.API_Universal.Modred as Modred
# Modred.add_tag_tooltip(MyCustomTag)

# TODO: RiftWizard.idle_frame = RiftWizard.idle_frame % 100000

# TODO: add a function here block_steam_adapter(modname) and unblock_steam_adapter(modname)
# block all steam adapter stuff if len(blocklist) > 0

# TODO: also add a way to block all but the bestiary

# TODO: add hashes of rift wizard source files, throw warning if stored hashes don't match current computed hashes (and display warning on title screen)


# TODO: API_Boss doesn't work - Universal results in an instant win when fighting Mordred


# ######################################### 
#
# Disable Steam stats during multiplayer
#
# #########################################
		
def should_block_steam_adapter():
	return False

def should_block_steam_adapter_bestiary():
	return False

import SteamAdapter as SteamAdapter

old_SteamAdapter_set_stat = SteamAdapter.set_stat
def SteamAdapter_set_stat(stat, val):
	if should_block_steam_adapter():
		return
	old_SteamAdapter_set_stat(stat, val)
SteamAdapter.set_stat = SteamAdapter_set_stat

old_SteamAdapter_set_presence_level = SteamAdapter.set_presence_level
def SteamAdapter_set_presence_level(level):
	if should_block_steam_adapter():
		return
	old_SteamAdapter_set_presence_level(level)
SteamAdapter.set_presence_level = SteamAdapter_set_presence_level

old_SteamAdapter_set_trial_complete = SteamAdapter.set_trial_complete
def SteamAdapter_set_trial_complete(trial_name):
	if should_block_steam_adapter():
		return
	old_SteamAdapter_set_trial_complete(trial_name)
SteamAdapter.set_trial_complete = SteamAdapter_set_trial_complete


old_SteamAdapter_unlock_bestiary = SteamAdapter.unlock_bestiary
def SteamAdapter_unlock_bestiary(monster_name):
	if should_block_steam_adapter_bestiary():
		return
	old_SteamAdapter_unlock_bestiary(monster_name)
SteamAdapter.unlock_bestiary = SteamAdapter_unlock_bestiary
