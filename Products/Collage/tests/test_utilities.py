# -*- coding: utf-8 -*-
from Products.Collage import utilities as cu
from Products.Collage.testing import COLLAGE_INTEGRATION_TESTING
import unittest


class UtilitiesTestCase(unittest.TestCase):

    layer = COLLAGE_INTEGRATION_TESTING

    def _makeCollage(self, newid, title):
        effectiveid = self.layer['portal'].invokeFactory(
            id=newid,
            type_name='Collage',
            title=title,
        )
        return self.layer['portal'][effectiveid]

    def testGenerateNewId(self):
        self.layer['request'].environ['REQUEST_METHOD'] = 'POST'
        foo_collage = self._makeCollage('foo', 'Foo')

        new_id = cu.generateNewId(foo_collage)
        self.failUnlessEqual(new_id, '1')

        foo_collage.restrictedTraverse('insert-row').insertRow()
        new_id = cu.generateNewId(foo_collage)
        self.failUnlessEqual(new_id, '2')

        foo_collage.restrictedTraverse('insert-row').insertRow()
        self.failUnlessEqual(foo_collage.objectIds()[-1], '2')

        foo_collage._delObject(foo_collage.objectIds()[0])
        new_id = cu.generateNewId(foo_collage)
        self.failUnlessEqual(new_id, '1')
        return

    def testIsTranslatable(self):
        self.layer['portal'].invokeFactory('Document', 'doc', title="Doc")
        doc = getattr(self.layer['portal'], 'doc')
        if cu.HAS_LINGUAPLONE:
            self.failUnless(cu.isTranslatable(doc))
        else:
            self.failIf(cu.isTranslatable(doc))
        return
