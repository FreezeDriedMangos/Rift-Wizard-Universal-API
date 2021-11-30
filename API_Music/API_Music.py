
###########################################################################
##  Example usage:
# -------------------------------------------------------------------------
# def level_has_shrine(pygameview):
# 	shrines = [prop for prop in pygameview.game.cur_level.props if isinstance(prop, Level.ShrineShop)]
# 	return len(shrines) > 0
# 
# API_Music.add_track(API_Music.TRACK_TYPE_LEVEL, API_Music.PRIORITY_NORMAL, os.path.join('mods', 'ShougsMusic', 'shrine' + '.wav'), level_has_shrine)
# 
###########################################################################


####################################################
# Importing RiftWizard.py                          |
# Credit to trung on discord                       |
#                                                  |
#----------------------------------------------    |
import inspect #                                   |
def get_RiftWizard(): #                            |
    # Returns the RiftWizard.py module object      |
    for f in inspect.stack()[::-1]: #              |
        if "file 'RiftWizard.py'" in str(f): #     |
            return inspect.getmodule(f[0]) #       |
	 #                                             |
    return inspect.getmodule(f[0]) #               |
#                                                  |
RiftWizard = get_RiftWizard() #                    |
#                                                  |
#                                                  |
####################################################

import pygame
from collections import defaultdict, namedtuple, OrderedDict
import random
import os


Track = namedtuple("Track", "condition_func priority path")

boss_tracks = []
level_tracks = []
title_tracks = []
gameover_tracks = []
victory_tracks = []


current_track = None


PRIORITY_FALLBACK = 0
PRIORITY_NORMAL = 1
PRIORITY_SPECIAL_TRACK = 2


TRACK_TYPE_BOSS = 'boss'
TRACK_TYPE_LEVEL = 'level'
TRACK_TYPE_TITLE = 'title'
TRACK_TYPE_GAMEOVER = 'gameover'
TRACK_TYPE_VICTORY = 'victory'



def add_track(track_type, priority, path, condition_func):
	new_track = Track(condition_func, priority, path)

	if track_type == TRACK_TYPE_BOSS:
		boss_tracks.append(new_track)
		boss_tracks.sort(key=lambda t: t.priority)
	if track_type == TRACK_TYPE_LEVEL:
		level_tracks.append(new_track)
		level_tracks.sort(key=lambda t: t.priority)
	if track_type == TRACK_TYPE_TITLE:
		title_tracks.append(new_track)
		title_tracks.sort(key=lambda t: t.priority)
	if track_type == TRACK_TYPE_GAMEOVER:
		gameover_tracks.append(new_track)
		gameover_tracks.sort(key=lambda t: t.priority)
	if track_type == TRACK_TYPE_VICTORY:
		victory_tracks.append(new_track)
		victory_tracks.sort(key=lambda t: t.priority)


add_track(TRACK_TYPE_BOSS, PRIORITY_FALLBACK, os.path.join('rl_data', 'music', 'mordred_theme' + '.wav'), lambda pygameview: True)
add_track(TRACK_TYPE_LEVEL, PRIORITY_FALLBACK, os.path.join('rl_data', 'music', 'battle_2' + '.wav'), lambda pygameview: True)
add_track(TRACK_TYPE_TITLE, PRIORITY_FALLBACK, os.path.join('rl_data', 'music', 'battle_1' + '.wav'), lambda pygameview: True)
add_track(TRACK_TYPE_GAMEOVER, PRIORITY_FALLBACK, os.path.join('rl_data', 'music', 'lose' + '.wav'), lambda pygameview: True)
add_track(TRACK_TYPE_VICTORY, PRIORITY_FALLBACK, os.path.join('rl_data', 'music', 'victory_theme' + '.wav'), lambda pygameview: True)


def select_track_from(self, tracks):
	possible_tracks = [t for t in tracks if t.condition_func(self)]
	highest_priority = possible_tracks[0].priority
	possible_tracks = [t for t in possible_tracks if t.priority == highest_priority]
	return random.choice(possible_tracks)


def play_music(self, track_name):
	if not self.can_play_sound:
		return

	global boss_tracks
	global level_tracks
	global title_tracks
	global gameover_tracks
	global victory_tracks

	if track_name == 'mordred_theme':
		new_track = select_track_from(self, boss_tracks)
	if track_name == 'battle_2':
		new_track = select_track_from(self, level_tracks)
	if track_name == 'battle_1':
		new_track = select_track_from(self, title_tracks)
	if track_name == 'lose':
		new_track = select_track_from(self, gameover_tracks)
	if track_name == 'victory_theme':
		new_track = select_track_from(self, victory_tracks)

	global current_track
	if new_track == current_track:
		return

	current_track = new_track
	music_path = new_track.path
	pygame.mixer.music.load(music_path)
	self.adjust_volume(0, 'music')
	pygame.mixer.music.play(-1)
