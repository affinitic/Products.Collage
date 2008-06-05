from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable

from zope.interface import Interface
from zope.interface import \
     implements, alsoProvides, providedBy

from zope.component import getUtility, getAdapters
from zope.app.publisher.interfaces.browser import IBrowserMenu

from interfaces import IDynamicViewManager
from interfaces import ICollageAlias

from persistent.dict import PersistentDict

ANNOTATIONS_KEY = u'Collage'

class DynamicViewManager(object):
    implements(IDynamicViewManager)

    def __init__(self, context):
        self.context = context
        
    def getStorage(self):
        annotations = IAnnotations(self.context)
        return annotations.setdefault(ANNOTATIONS_KEY, PersistentDict())

    def getLayout(self):
        storage = self.getStorage()
        return storage.get('layout', None)

    def setLayout(self, layout):
        storage = self.getStorage()
        storage['layout'] = layout

    def getDefaultLayout(self):
        layouts = self.getLayouts()

        if layouts:
            # look for a standard view (by naming convention)
            for name, title in layouts:
                if name == u'standard':
                    return (name, title)
            
            # otherwise return first view factory
            return layouts[0]

        raise ValueError
    
    def getLayouts(self):
        context = self.context
        
        if ICollageAlias.providedBy(self.context):
            # use target as self.context
            
            target = self.context.get_target()
            if target: context = target
            
        if not context:
            context = self.context
        
        menu = getUtility(IBrowserMenu, u'collage-views')
        layouts = list(getAdapters((context, context.REQUEST), menu.getMenuItemType()))
        return [(item.action.lstrip(u'@'), name) for (name, item) in layouts]
