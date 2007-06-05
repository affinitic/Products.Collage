from StringIO import StringIO
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import getToolByName
from Products import Collage
from Products.Collage.config import PROJECTNAME

def setup_gs_profile(self, portal, out):
    setup_tool = cmfutils.getToolByName(portal, 'portal_setup', None)

    if setup_tool:
        current_context = setup_tool.getImportContextID()

        # set import profile
        setup_tool.setImportContext('profile-Collage:default')

        # run the profile
        setup_tool.runAllImportSteps()

        # Restore import context again
        setup_tool.setImportContext(current_context)

        out.write("portal_setup is runned with the '%s' profile\n\n" % ('profile-Collage:default'))

    else:
        out.write("setup_tool is not available\n\n")

def install(self):
    out = StringIO()

    portal=getToolByName(self,'portal_url').getPortalObject()

    setup_gs_profile(self, portal, out)

    out.write("Successfully installed %s.\n\n" % PROJECTNAME)
    return out.getvalue()
