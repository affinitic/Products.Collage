PROJECTNAME = "Collage"
I18N_DOMAIN = PROJECTNAME.lower()

from Products.CMFCore.permissions import setDefaultRoles

DEFAULT_ADD_CONTENT_PERMISSION = "Add Collage content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))

import os
PACKAGE_HOME = os.path.dirname(os.path.abspath(__file__))
del os
