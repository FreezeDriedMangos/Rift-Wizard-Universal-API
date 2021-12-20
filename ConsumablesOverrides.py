import Consumables
import mods.API_Universal.APIs.API_Disrupt.API_Disrupt as API_Disrupt

def disrupt_portals_cast_instant(self, x, y):
	API_Disrupt.disrupt_portals_cast_instant(self, x, y)

Consumables.DisruptPortalsSpell.cast_instant = disrupt_portals_cast_instant