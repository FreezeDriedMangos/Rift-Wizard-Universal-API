import LevelGen
import mods.API_Universal.API_Boss.API_Boss as API_Boss


__levelgenerator_init_old = LevelGen.LevelGenerator.__init__

#Marks all bosses on the final level as final bosses
def levelgenerator_init(self, *args, **kwargs):
	__levelgenerator_init_old(self, *args, **kwargs)

	API_Boss.levelgenerator_init(self, *args, **kwargs)

LevelGen.LevelGenerator.__init__ = levelgenerator_init