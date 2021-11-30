import Level
import mods.API_Universal.API_Disrupt.API_Disrupt as API_Disrupt

def portal_disrupt(self, caster):
	API_Disrupt.disrupt_default(self, caster)
Level.Portal.disrupt = portal_disrupt