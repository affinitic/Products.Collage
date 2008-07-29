from Products.Five.browser import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.Collage.interfaces import IDynamicViewManager, IPortletSkin

class BaseView(BrowserView):
    def test(self):
        return lambda a, b, c: a and b or c

    def isAnon(self):
        return getToolByName(self.context, 'portal_membership').isAnonymousUser()

    def normalizeString(self):
        return getToolByName(self.context, 'plone_utils').normalizeString

    def mtool(self):
        return getToolByName(self.context, 'portal_membership')

    def portal_url(self):
        return getToolByName(self.context, 'portal_url')()

    def site_properties(self):
        props = getToolByName(self.context, 'portal_properties')
        return props.site_properties

    def friendlyTypes(self):
        return getToolByName(self.context, 'plone_utils').getUserFriendlyTypes()

    def getSkin(self):
        alias = getattr(self, '__alias__', None)

        if alias:
            context = alias
        else:
            context = self.__parent__

        manager = IDynamicViewManager(context)
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
