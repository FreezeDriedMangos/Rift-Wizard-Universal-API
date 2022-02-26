import LevelGen
import mods.API_Universal.APIs.API_Boss.API_Boss as API_Boss
import mods.API_Universal.APIs.API_LevelGenProps.API_LevelGenProps as API_LevelGenProps
import mods.API_Universal.APIs.API_LevelGen.API_LevelGen as API_LevelGen


__levelgenerator_init_old = LevelGen.LevelGenerator.__init__

#Marks all bosses on the final level as final bosses
def levelgenerator_init(self, *args, **kwargs):
	__levelgenerator_init_old(self, *args, **kwargs)
	API_Boss.levelgenerator_init(self, *args, **kwargs)

LevelGen.LevelGenerator.__init__ = levelgenerator_init



__populate_level_old = LevelGen.LevelGenerator.populate_level
def populate_level(self):
	API_LevelGenProps.pre_populate_level(self)
	
	__populate_level_old(self)
	
	API_LevelGenProps.place_extra_props(self)

LevelGen.LevelGenerator.populate_level = populate_level


# allows trials to define fully custom level gen
LevelGen.LevelGenerator.make_level = API_LevelGen.make_level