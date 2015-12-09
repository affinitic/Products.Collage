# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.Collage.browser.renderer import SimpleContainerRenderer
from Products.Collage.browser.renderer import WithPublishDateRenderer
from Products.Collage.testing import COLLAGE_INTEGRATION_TESTING
import time
import unittest


class SimpleContainerRendererTestCase(unittest.TestCase):
    """We test utilities for testcases"""

    layer = COLLAGE_INTEGRATION_TESTING

    def setUp(self):
        self.folder = self.layer['portal'].folder
        _ = self.folder.invokeFactory(id='collage', type_name='Collage')
        self.collage = self.folder[_]

        _ = self.collage.invokeFactory(id='row', type_name='CollageRow')
        self.row = self.collage[_]

        _ = self.row.invokeFactory(id='column', type_name='CollageColumn')
        self.column = self.row[_]

        _ = self.folder.invokeFactory(id='doc', type_name='Document')
        self.doc = self.folder[_]

        _ = self.column.invokeFactory(id='alias', type_name='CollageAlias')
        self.alias = self.column[_]
        self.alias.set_target(self.doc.UID())

    def _makeOne(self, context):
        return SimpleContainerRenderer(context, self.layer['request'])

    def test_getItemsCollage(self):
        view = self._makeOne(self.collage)
        items = view.getItems()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].__name__, 'standard')

    def test_getItemsRow(self):
        view = self._makeOne(self.row)
        items = view.getItems()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].__name__, 'standard')

    def test_getItemsColumn(self):
        view = self._makeOne(self.column)
        items = view.getItems()
        self.assertEqual(items[0].__name__, 'standard')


class WithPublishDateRendererTestCase(unittest.TestCase):

    layer = COLLAGE_INTEGRATION_TESTING

    def setUp(self):
        self.folder = self.layer['portal'].folder
        _ = self.folder.invokeFactory(id='collage', type_name='Collage')
        self.collage = self.folder[_]

        _ = self.collage.invokeFactory(id='row', type_name='CollageRow')
        self.row = self.collage[_]

        _ = self.row.invokeFactory(id='column', type_name='CollageColumn')
        self.column = self.row[_]

        _ = self.folder.invokeFactory(id='doc', type_name='Document')
        self.doc = self.folder[_]

        _ = self.column.invokeFactory(id='alias', type_name='CollageAlias')
        self.alias = self.column[_]
        self.alias.set_target(self.doc.UID())
        # By default this permission is also given to Owner, but that
        # defeats our test purpose.  Alternatively, we could make sure
        # Anonymous can view the collage, maybe simply by doing a
        # workflow transition, but that may depend on the workflow.
        self.layer['portal'].manage_permission(
            'Access inactive portal content',
            ['Manager']
        )

    def _makeOne(self, context):
        return WithPublishDateRenderer(context, self.layer['request'])

    def test_rowfilter(self):
        view = self._makeOne(self.collage)
        items = view.getItems()
        self.assertEqual(len(items), 1)

        tomorrow = DateTime() + 1

        self.row.setEffectiveDate(tomorrow)
        items = view.getItems()
        self.assertEqual(len(items), 0)

    def test_columnfilter(self):
        view = self._makeOne(self.row)
        items = view.getItems()
        self.assertEqual(len(items), 1)

        yesterday = DateTime() - 1

        self.column.setExpirationDate(yesterday)
        items = view.getItems()
        self.assertEqual(len(items), 0)

    def test_itemfilter(self):
        now = DateTime()
        nearfuture = now + 1 / 86400.0 * 2  # 2 seconds ahead of now
        self.doc.setEffectiveDate(nearfuture)
        view = self._makeOne(self.column)
        items = view.getItems()
        self.assertEqual(len(items), 0)

        time.sleep(2)  # wait for the document to appear

        items = view.getItems()
        self.assertEqual(len(items), 1)
