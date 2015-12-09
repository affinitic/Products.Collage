# -*- coding: utf-8 -*-
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2
import Products.Collage

try:
    import Products.LinguaPlone
    HAS_LINGUA_PLONE = True
except ImportError:
    HAS_LINGUA_PLONE = False


class CollageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=Products.Collage)

        if HAS_LINGUA_PLONE:
            self.loadZCML(package=Products.LinguaPlone)
            z2.installProduct(app, 'Products.LinguaPlone')

        z2.installProduct(app, 'Products.Collage')

    def setUpPloneSite(self, portal):
        if HAS_LINGUA_PLONE:
            applyProfile(portal, 'Products.LinguaPlone:LinguaPlone')
        applyProfile(portal, 'Products.Collage:default')
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Site Administrator'])
        portal.invokeFactory(id='folder', type_name='Folder')
        setRoles(portal, TEST_USER_ID, ['Contributor', 'Editor'])


COLLAGE_FIXTURE = CollageLayer()


COLLAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLAGE_FIXTURE,),
    name='CollageLayer:IntegrationTesting'
)


COLLAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLAGE_FIXTURE,),
    name='CollageLayer:FunctionalTesting'
)
