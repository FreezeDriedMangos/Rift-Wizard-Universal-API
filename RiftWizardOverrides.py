


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

import mods.API_Universal.API_Effect.API_Effect as API_Effect


__get_effect_old = RiftWizard.PyGameView.get_effect

def get_effect(self, effect, color=None, *args, **kvargs):
	val = API_Effect.get_effect(self, effect, color=None, *args, **kvargs)
	if val:
		return val
	return __get_effect_old(self, effect, color, *args, **kvargs)
	
RiftWizard.PyGameView.get_effect = get_effect