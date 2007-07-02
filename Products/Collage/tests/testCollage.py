#
# This file is a skeleton test suite.
# It is here for letting you add new tests to the product without having to
# modify the existing testStyleInstallation.py module.
# You may modify its name to something that describes what it tests
# (keeping its 'test' prefix).
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
from Products.CMFPlone.utils import getToolByName
from Products.CMFPlone.browser.plone import Plone
from Products.CMFPlone import utils as plone_utils

# interfaces
from Products.Collage.interfaces import ICollage
from Products.CMFPlone.interfaces import IBrowserDefault

# z3 imports
from zope.interface.verify import verifyObject as Z3verifyObject
from zope.component import getMultiAdapter

PloneTestCase.installProduct('Collage')
PloneTestCase.setupPloneSite(products=['Collage'])

class TestCollage(PloneTestCase.PloneTestCase):
    """Basic unit / integration test for the Collage product."""

    def afterSetUp(self):
        pass

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
        self.request = self.app.REQUEST
        portal = self.portal
        self.populateSite()

    # set up a lot of content - can be reused in each (sub)test
    def populateSite(self):
        portal = self.portal
        
        self.setRoles(['Manager'])
        portal.invokeFactory('Collage', 'collage1', title='Collage 1', description='This is a description 1.')
        portal.invokeFactory('Collage', 'collage2', title='Collage 2', description='This is a description 2.')

        # collage as default page
        portal.invokeFactory('Folder', 'folder1', title='Folder 1')
        self.folder1 = portal['folder1']
        self.folder1.invokeFactory('Collage', 'collage', title='Collage front page', description='This is a description 2.')
        self.collage = self.folder1['collage']
        self.collage_id = self.collage.getId()

        # set collage as default page of the folder
        self.folder1.setDefaultPage(self.collage_id)

        # add some rows
        self.collage.invokeFactory('CollageRow', 'collagerow1', title='CollageRow 1', description='This is a description 1.')
        self.collage.invokeFactory('CollageRow', 'collagerow2', title='CollageRow 2', description='This is a description 1.')

        self.setRoles(['Member'])

    def testSetupProfile(self):
        # if default setup profile isn't executed,
        # collage isn't a content-type thus not addable
        collage1 = getattr(self.portal, 'collage1')
        self.failUnless(collage1)

    def testDontShowInNavigation(self):
        pp = getToolByName(self.portal, 'portal_properties')

        CollageNonNavItems = ('CollageRow', 'CollageColumn', 'CollageAlias')
        metaTypesNotToList = pp.navtree_properties.metaTypesNotToList

        for item in CollageNonNavItems:
            self.failUnless(item in metaTypesNotToList)

    def test_collageAsFrontPageByPlone(self):
        # just a basic test that proves collage is set as default page
        self.assertEqual(self.collage_id, self.folder1.getDefaultPage())

        # let's see how plone treats collage as front page
        view = Plone(self.collage, self.request)

        is_folder_or_default_page = view.isFolderOrFolderDefaultPage()
        self.failUnless(is_folder_or_default_page)

        is_portal_or_portal_default_page = view.isPortalOrPortalDefaultPage()
        self.failIf(is_portal_or_portal_default_page)

        is_default_page_in_folder = view.isDefaultPageInFolder()
        self.failUnless(is_default_page_in_folder)

        # current folder should be parent object
        get_current_folder = view.getCurrentFolder()
        self.assertEqual(get_current_folder, self.folder1)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCollage))
    return suite

if __name__ == '__main__':
    framework()
