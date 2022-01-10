from collections import defaultdict, namedtuple, OrderedDict
import sys
import Game
import Level
import Monsters
import LevelGen
import Mutators
import RareMonsters
import random

#This part patches final boss killing
# __check_triggers_old = Game.Game.check_triggers

UNIT_FAKE_MORDRED = Monsters.Mordred()

#Prevents victory with a pretend mordred in the last level only
#Effectively changes the victory condition to last level + all is_final_boss units need to be killed
def check_triggers_pre(self):
	if(self.level_num == Level.LAST_LEVEL):
		self.cur_level.units.append(UNIT_FAKE_MORDRED)

def check_triggers_post(self):
	if(self.level_num == Level.LAST_LEVEL):
		self.cur_level.units.pop()
	
	if self.level_num == Level.LAST_LEVEL and not self.victory and not any(getattr(u,'is_final_boss',False) for u in self.cur_level.units):
		self.victory = True
		self.victory_evt = True
		self.finalize_save(victory=True)
	
# Game.Game.check_triggers = check_triggers

# __levelgenerator_init_old = LevelGen.LevelGenerator.__init__

#Marks all bosses on the final level as final bosses
def levelgenerator_init(self, *args, **kwargs):
	# __levelgenerator_init_old(self, *args, **kwargs)

	if(self.difficulty == Level.LAST_LEVEL):
		finalboss = random.choice(default_finalbosses)
		finalboss.generator(self)
		
		if self.game:
			for m in self.game.mutators:
				if(hasattr(m, 'on_levelgen_finalboss')):
					m.on_levelgen_finalboss(self)
		
		for boss in self.bosses:
			boss.is_final_boss = True
	
# LevelGen.LevelGenerator.__init__ = levelgenerator_init

FinalBoss = namedtuple('FinalBoss', 'name generator')

def generator_empty(levelgen):
	pass

default_finalbosses = [FinalBoss('Mordred', generator_empty)] # We leave the default as is
bestiary_additions = []

DIFF_SECRET = 9999

print("API_Boss Loaded")

###########
### API ###
###########

# Adds a monster to the bestiary is a "final boss".
# All bosses added this way will appear before Mordred in the Bestiary.
# 
# spawner - A monster spawner function
def add_finalboss_bestiary(spawner):
	if not spawner in bestiary_additions:
		bestiary_additions.append(spawner)
		RareMonsters.rare_monsters.append((spawner, DIFF_SECRET, 1, 1, None))

# Adds a final boss generator.
#
# name - Name of the boss for easier removal/editing
# generator - A function that accepts a LevelGenerator as parameter
def add_finalboss_generator(name, generator):
	default_finalbosses.append(FinalBoss(name, generator))

# Adds a final boss monster.
#
# name - Name of the boss for easier removal/editing
# spawner - A monster spawner function
# add_bestiary - whether the monster is added to the bestiary
def add_finalboss(name, spawner, add_bestiary = True):
	def generator(levelgen):
		unit = spawner()
		levelgen.bosses = [unit]

	add_finalboss_generator(name, generator)
	add_finalboss_bestiary(spawner)

# Adds a group of final bosses.
#
# name - Name of the boss for easier removal/editing
# spawners - A list of monster spawner functions
# add_bestiary - whether the monsters are added to the bestiary
def add_finalboss_group(name, spawners, add_bestiary = True):
	def generator(levelgen):
		levelgen.bosses = []
		# could be simplified
		for spawner in spawners:
			unit = spawner()
			levelgen.bosses.append(unit)

	add_finalboss_generator(name, generator)
	for spawner in spawners:
		add_finalboss_bestiary(spawner)
		


