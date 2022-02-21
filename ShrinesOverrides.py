
import Shrines as Shrines
import LevelGen as LevelGen
import mods.API_Universal.APIs.API_LevelGenProps.API_LevelGenProps as API_LevelGenProps
import mods.API_Universal.APIs.API_Spells.API_Spells as API_Spells

Shrines.roll_shrine = API_LevelGenProps.roll_shrine
Shrines.random_spell_tag = API_Spells.random_spell_tag
LevelGen.roll_shrine = API_LevelGenProps.roll_shrine
LevelGen.random_spell_tag = API_Spells.random_spell_tag