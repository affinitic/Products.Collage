# -*- coding: utf-8 -*-
# $Id$

from zope.component import getMultiAdapter
from plone.memoize.view import memoize_contextless
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Collage.interfaces import IDynamicViewManager, IPortletSkin

def doTest(condition, value_true, value_false):
    if condition:
        return value_true
    else:
        return value_false

class BaseView(BrowserView):

    def test(self):
        # return lambda a, b, c: a and b or c
        return doTest

    @memoize_contextless
    def isAnon(self):
        return self.mtool().isAnonymousUser()

    @memoize_contextless
    def normalizeString(self):

        return getToolByName(self.context, 'plone_utils').normalizeString

    @memoize_contextless
    def mtool(self):

        plone_tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        return plone_tools.membership()

    @memoize_contextless
    def portal_url(self):

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        return portal_state.portal_url()

    @memoize_contextless
    def site_properties(self):

        plone_tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        return plone_tools.properties().site_properties

    @memoize_contextless
    def friendlyTypes(self):

        return getToolByName(self.context, 'plone_utils').getUserFriendlyTypes()

    @property
    def collage_context(self):
        alias = getattr(self, '__alias__', None)

        if alias:
            return alias

        return self.__parent__

    def getSkin(self):
        manager = IDynamicViewManager(self.collage_context)
        return manager.getSkin()


class RowView(BaseView):
    def getColumnBatches(self, bsize=3):
        columns = self.context.folderlistingFolderContents()
        if not columns:
            return []

        # calculate number of batches
        count = (len(columns)-1)/3+1

        batches = []
        for c in range(count):
            batch = []
            for i in range(bsize):
                index = c*bsize+i

                # pad with null-columns
                column = None

                if index < len(columns):
                    column = columns[index]

                # do not pad first row
                if column or c > 0:
                    batch += [column]

            batches += [batch]

        return batches

class AutomaticRowView(RowView):
    title = u'Automatic'

class LargeLeftRowView(RowView):
    title = u'Large left'

class LargeRightRowView(RowView):
    title = u'Large right'

class StandardView(BaseView):
    title = u'Standard'

class TextView(BaseView):
    title = u'Text'

class FeaturedView(BaseView):
    title = u'Featured'

class PortletView(BaseView):
    title = u'Portlet'
    skinInterfaces = (IPortletSkin,)

class AlbumTopicView(BaseView):
    title = u'Album'

class ClickableView(BaseView):
    title = u'Clickable'

class StandardDocumentView(StandardView):
    """Includes for BBB."""
