# -*- coding: utf-8 -*-
# $Id$

from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component import ComponentLookupError
from zope.interface import providedBy
from zope.interface import Interface
from plone.memoize.view import memoize_contextless
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Collage.interfaces import IDynamicViewManager, IPortletSkin
from Products.Collage.interfaces import ICollageBrowserLayer
from Products.Collage.utilities import CollageMessageFactory as _

def test(condition, value_true, value_false):
    if condition:
        return value_true
    else:
        return value_false

class BaseView(BrowserView):
    hide = False
    __alias__ = None

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
    notfoundlayoutname = None

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
    title = _(u'Automatic')

class LargeLeftRowView(RowView):
    title = _(u'Large left')

class LargeRightRowView(RowView):
    title = _(u'Large right')

class UnbatchedRowView(RowView):
    title = _(u'Unbatched')

class StandardView(BaseView):
    title = _(u'Standard')

class TextView(BaseView):
    title = _(u'Text')

class FeaturedView(BaseView):
    title = _(u'Featured')

class PortletView(BaseView):
    title = _(u'Portlet')
    skinInterfaces = (IPortletSkin,)

class AlbumTopicView(BaseView):
    title = _(u'Album')

class SummaryTopicView(BaseView):
    title = _(u'Summary')

class TabularTopicView(BaseView):
    title = _(u'Tabular')

class InheritTopicView(BaseView):
    """Inherits view from topic's display setting."""

    title = _(u'Inherit')

    mapping = {
        'folder_listing': 'standard',
        'folder_summary_view': 'summary',
        'folder_tabular_view': 'tabular',
        'atct_album_view': 'album',
        'atct_topic_view': 'standard',
        }

    error_view_name = "error_collage-view-not-found"
    fallback_view_name = "fallback"

    def __call__(self):
        """Determine inherited view and attempt to find suitable
        collage view.

        If a view can't be determined, render fallback view. If the
        view does not exist, render an error message.
        """

        layout = self.context.getLayout()
        name = self.mapping.get(layout, self.fallback_view_name)
        spec = providedBy(self.context), ICollageBrowserLayer
        lookup = getSiteManager().adapters.lookup
        factory = lookup(spec, Interface, name=name)
        if factory is None:
            name = None
            factory = lookup(spec, Interface, name=self.error_view_name)
            if factory is None:
                raise ComponentLookupError(
                    "Layout not found: %s (and unable to render error view)." % \
                    layout)
        view = factory(self.context, self.request)
        if name is None:
            view.notfoundlayoutname = layout

        view.__alias__ = self.__alias__
        return view()

class ClickableView(BaseView):
    title = _(u'Clickable')

class StandardDocumentView(StandardView):
    """Includes for BBB."""

class FileMinimalView(StandardView):
    """File for download in one line."""

    title = _(u'minimal')

    def getBUFile(self):
        acc = self.context.Schema()['file'].getAccessor(self.context)()
        return acc
