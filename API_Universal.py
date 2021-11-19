

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
            break #                                |
	 #                                             |
    return f #                                     |
#                                                  |
RiftWizard = get_RiftWizard() #                    |
#                                                  |
#                                                  |
####################################################

