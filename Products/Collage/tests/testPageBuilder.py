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

#interfaces
from Products.Collage.interfaces import ICollage
from Products.CMFPlone.interfaces import IBrowserDefault
from Products.CMFDynamicViewFTI.interface import ISelectableBrowserDefault

# z3 imports
from zope.interface.verify import verifyObject as Z3verifyObject
from zope.component import getMultiAdapter



PloneTestCase.installProduct('Collage')
PloneTestCase.setupPloneSite(products=['Collage'])


class TestCollage(PloneTestCase.PloneTestCase):
    """
    Basic unit / integration test  for the page builder product

    """

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



    #set up a lot of content - can be reused in each (sub)test
    def populateSite(self):
        self.setRoles(['Manager'])
        self.portal.invokeFactory('Collage', 'collage1', title='Collage 1', description='This is a description 1.')
        self.portal.invokeFactory('Collage', 'collage2', title='Collage 2', description='This is a description 2.')

        #collage as default page
        self.portal.invokeFactory('Folder', 'folder1', title='Folder 1',)
        self.folder1 = getattr(self.portal,"folder1")
        self.folder1.invokeFactory('Collage', 'collage', title='Collage front page', description='This is a description 2.')
        self.collage = getattr(self.folder1, "collage")
        self.collage_id = self.collage.getId()
        #set collage as default page of the folder
        self.folder1.setDefaultPage(self.collage_id)

        #add som epgae rows
        self.collage.invokeFactory('CollageRow', 'collagerow1', title='CollageRow 1', description='This is a description 1.')
        self.collage.invokeFactory('CollageRow', 'collagerow2', title='CollageRow 2', description='This is a description 1.')

        self.setRoles(['Member'])


    def testSetupProfile(self):

        #if default setup profile aren't executed rigth # collage isnet a contentype and not addable
        collage1 = getattr(self.portal, 'collage1')
        self.failUnless(collage1)

        #setup more tests for the setup profile installation


    def testDontShowInNavigation(self):
        pp = getToolByName(self.portal, 'portal_properties')

        CollageNonNavItems = ['CollageRow', 'CollageColumn']
        metaTypesNotToList = pp.navtree_properties.metaTypesNotToList

        for item in CollageNonNavItems:
            self.failUnless(item in metaTypesNotToList)



    def test_collageAsFrontPageByPlone(self):
        """Pagebuilder as front-page of a folder"""

        #just a basic test that proves collage is set as default page
        self.assertEqual(self.collage_id, self.folder1.getDefaultPage())

        #lets see how plone treats collage as front page
        view = Plone(self.collage, self.request)

        is_folder_or_default_page = view.isFolderOrFolderDefaultPage()
        self.failUnless(is_folder_or_default_page)

        is_portal_or_portal_default_page = view.isPortalOrPortalDefaultPage()
        self.failIf(is_portal_or_portal_default_page)

        is_default_page_in_folder = view.isDefaultPageInFolder()
        self.failUnless(is_default_page_in_folder)

        # getCurrentFolder() is the one that fails in plone wit collage
        get_current_folder = view.getCurrentFolder()

        # current folder should be collage itself
        # note: this 'bug' is fixed using javascript
        # self.assertEqual(get_current_folder, self.collage)

    def test_collageAsFrontPageByPloneAtPortal(self):
        """Pagebuilder as front-page of a plone portal"""

        #def collage
        front_portal_collage = getattr(self.portal,"collage1")
        front_portal_collage_id = front_portal_collage.getId()

        self.setRoles(['Manager'])
        #set default page of portal
        self.portal.setDefaultPage(front_portal_collage_id)
        self.setRoles(['Member'])


        #just a basic test that proves collage is set as default page
        self.assertEqual(front_portal_collage_id, self.portal.getDefaultPage())


        #lets see how plone treats collage as front page
        view = Plone(front_portal_collage, self.request)
        is_folder_or_default_page = view.isFolderOrFolderDefaultPage()
        self.failUnless(is_folder_or_default_page)

        #is portal default page
        is_portal_or_portal_default_page = view.isPortalOrPortalDefaultPage()
        self.failUnless(is_portal_or_portal_default_page)

        is_default_page_in_folder = view.isDefaultPageInFolder()
        self.failUnless(is_default_page_in_folder)

        #getCurrentFolder()
        get_current_folder = view.getCurrentFolder()

        # current folder should be collage itself
        # note: this 'bug' is fixed using javascript
        # self.assertEqual(get_current_folder, front_portal_collage)






    def test_ploneUtilIsFrontPage(self):
        #try out the plone util, its possible to pass a context or not
        is_default_page = plone_utils.isDefaultPage(self.collage, self.request, self.folder1)
        self.failUnless(is_default_page)

        is_default_page_no_context = plone_utils.isDefaultPage(self.collage, self.request)
        self.failUnless(is_default_page_no_context)

    def test_collageInterfaces(self):

        iface = ICollage
        self.failUnless(iface.providedBy(self.collage))
        self.failUnless(Z3verifyObject(iface, self.collage))


        #required interface if it should work in navigation
        iface = IBrowserDefault
        self.failUnless(iface.providedBy(self.collage))
        self.failUnless(Z3verifyObject(iface, self.collage))

#        iface = INonStructuralFolder
#        self.failUnless(iface.providedBy(self.collage))
#        self.failUnless(Z3verifyObject(iface, self.collage))



    def test_canSetDefaultPagePagebuilder(self):

        iface = ISelectableBrowserDefault
        self.failUnless(iface.providedBy(self.collage))
        self.failUnless(Z3verifyObject(iface, self.collage))

        #should not be possible to select default page
        self.failIf(self.collage.canSetDefaultPage())

        #test an page row as well
        page_row = getattr(self.collage, "collagerow1")

        iface = ISelectableBrowserDefault
        self.failUnless(iface.providedBy(page_row))
        self.failUnless(Z3verifyObject(iface, page_row))

        #should not be possible to select default page
        self.failIf(page_row.canSetDefaultPage())



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCollage))
    return suite

if __name__ == '__main__':
    framework()
