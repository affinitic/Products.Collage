from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from zope.interface import alsoProvides

from zope import event
from zope.app.event import objectevent

from Products.Five.browser import BrowserView

from Acquisition import aq_base, aq_inner, aq_parent

from Products.CMFPlone import utils as cmfutils
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.CMFPlone.utils import getSiteEncoding
from Products.CMFPlone.interfaces.NonStructuralFolder import \
     INonStructuralFolder as z2INonStructuralFolder

from Products.Collage.utilities import generateNewId

from Products.Collage.interfaces import ICollage
from Products.Collage.interfaces import IDynamicViewManager
from Products.Collage.interfaces import ICollageEditLayer

from Products.CMFPlone import PloneMessageFactory as _

from Acquisition import aq_inner, aq_parent

class SelectDynamicViewView(BrowserView):
    def setDynamicView(self):
        layout = self.request['layout']

        manager = getUtility(IDynamicViewManager)
        manager.setLayout(self.context, layout)

        self.context.plone_utils.addPortalMessage(_(u'View changed.'))
        self.request.response.redirect(self.context.REQUEST['HTTP_REFERER'])

class ReorderObjectView(BrowserView):
    def __call__(self):
        object_id = self.request['id']
        position = self.request['position']

        if position.lower()=='up':
            self.context.moveObjectsUp(object_id)

        if position.lower()=='down':
            self.context.moveObjectsDown(object_id)

        if position.lower()=='top':
            self.context.moveObjectsToTop(object_id)

        if position.lower()=='bottom':
            self.context.moveObjectsToBottom(object_id)

        # order folder by field
        # id in this case is the field
        if position.lower()=='ordered':
            self.context.orderObjects(object_id)

        cmfutils.getToolByName(self.context, 'plone_utils').reindexOnReorder(self.context)

        return 1

class InsertRowView(BrowserView):
    def __call__(self):
        # create row
        desired_id = generateNewId(self.context)
        row_id = self.context.invokeFactory(id=desired_id, type_name='CollageRow')
        row = getattr(self.context, row_id, None)
        row.setTitle('')
        
        # create column
        desired_id = generateNewId(row)
        col_id = row.invokeFactory(id=desired_id, type_name='CollageColumn')
        col = getattr(row, col_id, None)
        col.setTitle('')
        
        self.context.plone_utils.addPortalMessage(_(u'Row added.'))
        self.request.response.redirect(self.context.REQUEST['HTTP_REFERER'])    

class SplitColumnView(BrowserView):
    def __call__(self):
        container = aq_parent(aq_inner(self.context))
        desired_id = generateNewId(container)

        container.invokeFactory(id=desired_id, type_name='CollageColumn')
        
        self.context.plone_utils.addPortalMessage(_(u'Column inserted.'))
        self.request.response.redirect(self.context.REQUEST['HTTP_REFERER'])    

class InsertAliasView(BrowserView):
    def __call__(self):
        uid_catalog = cmfutils.getToolByName(self.context,
                                             'uid_catalog')

        uid = self.request.get('uid')

        # check that target object exists
        brains = uid_catalog(UID=uid)
        if brains:
            target_id = brains[0].id
            self.context.invokeFactory('CollageAlias', id=target_id)
            alias = self.context[target_id]
            alias.set_target(uid)
            event.notify(objectevent.ObjectModifiedEvent(alias))
            
            msg = 'Alias inserted.'
        else:
            msg = 'Target object not found.'
            
        referer = self.request.get('HTTP_REFERER', self.context.absolute_url())
        return self.request.RESPONSE.redirect('%s?portal_status_message=%s' % (referer, msg))

class ExistingItemsView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
        # beware of url-encoded spaces
        if 'portal_type' in self.request:
            self.request['portal_type'] = self.request['portal_type'].replace('%20', ' ')

    def __call__(self):
        """There are browser-issues in sending out content in UTF-8.
        We'll encode it in latin-1."""
        
        self.request.RESPONSE.setHeader("Content-Type",
                                        "text/html; charset=ISO-8859-1")

        encoding = getSiteEncoding(self.context.context)        
        return self.index().decode(encoding).encode('latin-1')
    
    @property
    def catalog(self):
        return cmfutils.getToolByName(self.context,
                                      'portal_catalog')

    def normalizeString(self, str):
        return self.context.plone_utils.normalizeString(str)
        
    def getItems(self):
        items = self.catalog(self.request,
                             sort_on='modified')[:self.request.get('count', 20)]

        return [{'UID': obj.UID(),
                 'title': result.Title,
                 'type': result.Type,
                 'portal_type':  self.normalizeString(result.portal_type),
                 'modified': result.ModificationDate,
                 'published': result.EffectiveDate or ''} for (result, obj) in
                map(lambda result: (result, result.getObject()), items)]

class ICollageView(Interface):
    def getTemplate():
        """Fetch template macro for a given brain taking the current
        object layout into account."""

    def isStructuralFolder():
        """Copied from CMFPlone/browser/plone.py."""
        
class CollageView(BrowserView):
    def getTemplate(self, brain):
        layout = self.context.getTargetObjectLayout(brain.getObject());
        return getattr(brain, layout, 'base_view')

    def isStructuralFolder(self, instance):
        context = instance
        folderish = bool(getattr(aq_base(context), 'isPrincipiaFolderish',
                                 False))
        if not folderish:
            return False
        elif INonStructuralFolder.providedBy(context):
            return False
        elif z2INonStructuralFolder.isImplementedBy(context):
            # BBB: for z2 interface compat
            return False
        else:
            return folderish
        
class ICollageUtility(Interface):
    def loadCollageJS(self):
        """Determine if we need to load JS."""
        
    def isCollageContent():
        """Search object tree for a Collage-object."""
        pass

    def getCollageObjectURL():
        """Search object tree for a Collage-object and return URL."""
        pass

class CollageUtility(object):
    implements(ICollageUtility)
    adapts(Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

        url = request.get('ACTUAL_URL', request.get('URL', None))
        if url.endswith('manage_page'):
            # add marker interfaces to request
            alsoProvides(self.request, ICollageEditLayer)

    def loadCollageJS(self):
        if ICollageEditLayer.providedBy(self.request):
            return True
        
    def isCollageContent(self, parent=None):
        return self.getCollageObjectURL() is not None

    def getCollageObjectURL(self, parent=None):
        if not parent:
            parent = aq_parent(aq_inner(self.context))

        if parent:
            if ICollage.providedBy(parent):
                return parent.absolute_url()

            parent = aq_parent(parent)
            if parent:
                if ICollage.providedBy(parent):
                    return parent.absolute_url()

        return None
