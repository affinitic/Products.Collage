# -*- coding: utf-8 -*-
# $Id$

from zope.component import getMultiAdapter
from plone.memoize.view import memoize_contextless
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Collage.interfaces import IDynamicViewManager, IPortletSkin

def test(condition, value_true, value_false):
    if condition:
        return value_true
    else:
        return value_false

class BaseView(BrowserView):
    hide = False

    def test(self):
        return test

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

class ErrorViewNotFoundView(BaseView):
    title = u'View not Found'
    hide = True    

class RowView(BaseView):

    def getColumnBatches(self, bsize=3):
        """Rows with more than *bsize* columns are split.
        
        @param bsize: number of max. allowed columns per row. 0 for no batching.
                
        @return: list of columns, each containing a list of rows.
        """   
        columns = self.context.folderlistingFolderContents()
        if not columns:
            return []
        if bsize == 0:
            return [columns,]
        numbatches = (len(columns) - 1) / bsize + 1
        batches = []
        for numbatch in range(numbatches):
            batch = []
            for bidx in range(bsize):
                index = numbatch * bsize + bidx
                column = None
                if index < len(columns):
                    column = columns[index]
                # pad with null-columns, but do not pad first row
                if column or numbatch > 0:
                    batch.append(column)
            batches.append(batch)
        return batches

class AutomaticRowView(RowView):
    title = u'Automatic'

class LargeLeftRowView(RowView):
    title = u'Large left'

class LargeRightRowView(RowView):
    title = u'Large right'

class UnbatchedRowView(RowView):
    title = u'Unbatched'

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

class FileMinimalView(StandardView):
    """File for download in one line."""

    title = u'minimal'

    def getBUFile(self):
        acc = self.context.Schema()['file'].getAccessor(self.context)()
        return acc
