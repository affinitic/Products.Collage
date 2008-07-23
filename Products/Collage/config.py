PROJECTNAME = "Collage"

from Products.CMFCore.permissions import setDefaultRoles

DEFAULT_ADD_CONTENT_PERMISSION = "Add Collage content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner',))
