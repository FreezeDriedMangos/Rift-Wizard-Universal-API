import Level
import Monsters


default_win_condition = lambda game: all([u.team == Level.TEAM_PLAYER for u in game.cur_level.units])

win_conditions = [
	default_win_condition
]

cur_level_units_holder = []
win_preventer = Level.Unit()

# "overrides"
def check_triggers_pre(game):
	global cur_level_units_holder
	cur_level_units_holder = game.cur_level.units

	if all(condition(game) for condition in win_conditions):
		game.cur_level.units = []
	else:
		game.cur_level.units.append(win_preventer)
	

def check_triggers_post(game):
	game.cur_level.units = cur_level_units_holder
	
	if win_preventer in game.cur_level.units:
		game.cur_level.units.remove(win_preventer)

# api
def add_win_condition(condition):
	win_conditions.append(condition)

def reset_win_conditions():
	win_conditions = [
		default_win_condition
	]

def remove_default_win_condition():
	win_conditions.remove(default_win_condition)


