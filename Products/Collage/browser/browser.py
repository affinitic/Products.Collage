from zope import event
from zope.app.event import objectevent
from zope.component import getUtility

from Products.Five.browser import BrowserView

from Products.CMFPlone import utils as cmfutils
from Products.CMFPlone import PloneMessageFactory as _

from Products.Collage.utilities import generateNewId
from Products.Collage.interfaces import IDynamicViewManager

from Acquisition import aq_inner, aq_parent

class CollageActionsView(BrowserView):
    def setDynamicView(self):
        layout = self.request['layout']

        manager = getUtility(IDynamicViewManager)
        manager.setLayout(self.context, layout)

        self.context.plone_utils.addPortalMessage(_(u'View changed.'))
        self.request.response.redirect(self.context.REQUEST['HTTP_REFERER'])

    def reorderObjects(self):
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

    def insertRow(self):
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

    def splitColumn(self):
        container = aq_parent(aq_inner(self.context))
        desired_id = generateNewId(container)

        container.invokeFactory(id=desired_id, type_name='CollageColumn')
        
        self.context.plone_utils.addPortalMessage(_(u'Column inserted.'))
        self.request.response.redirect(self.context.REQUEST['HTTP_REFERER'])    

    def insertAlias(self):
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


