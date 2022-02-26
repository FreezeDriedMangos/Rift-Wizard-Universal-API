import LevelGen as LevelGen


old_make_level = LevelGen.LevelGenerator.make_level

level_maker = old_make_level
level_maker_history = []

def make_level(level_generator):
	global level_maker
	global level_maker_history
	
	print('making level')
	return level_maker(level_generator)
LevelGen.LevelGenerator.make_level = make_level


def set_level_maker(new_level_maker):
	global level_maker
	global level_maker_history
	
	print('setting level maker')
	level_maker_history.append(new_level_maker)
	level_maker = new_level_maker

def restore_level_maker():
	global level_maker
	global level_maker_history
	
	if len(level_maker_history) > 0:
		level_maker = level_maker_history.pop()
	else:
		level_maker = old_make_level

# called on loading the title screen
def clear_level_makers():
	global level_maker
	global level_maker_history

	level_maker = old_make_level
	level_maker_history = []

LEVEL_SIZE = LevelGen.LEVEL_SIZE