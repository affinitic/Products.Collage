from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable

from zope.interface import Interface
from zope.interface import \
     implements, alsoProvides, providedBy

from zope.component import getSiteManager
from zope.component.interfaces import ComponentLookupError

from interfaces import IDynamicViewManager
from interfaces import ICollageAlias
from interfaces import ICollageBrowserLayer

from persistent.dict import PersistentDict

ANNOTATIONS_KEY = u'Collage'

def getViewFactoryInfo(context, layer):
    """Return view factory info for this context and browser layer."""
    
    sm = getSiteManager(context)

    context_ifaces = providedBy(context)

    lookupAll = sm.adapters.lookupAll
    
    collage_aware = lookupAll((context_ifaces, layer), Interface)
    collage_agnostic = lookupAll((context_ifaces, Interface), Interface)

    return [(name, getattr(factory, 'title', name)) \
            for (name, factory) in collage_aware if (name, factory) not in collage_agnostic]

class DynamicViewManager(object):
    implements(IDynamicViewManager)

    def getStorage(self, context):
        try:
            annotations = IAnnotations(context)
        except:
            alsoProvides(context, IAttributeAnnotatable)
            annotations = IAnnotations(context)

        return annotations.setdefault(ANNOTATIONS_KEY, PersistentDict())

    def getLayout(self, context):
        storage = self.getStorage(context)
        return storage.get('layout', None)

    def setLayout(self, context, layout):
        storage = self.getStorage(context)
        storage['layout'] = layout

    def getDefaultLayout(self, context):
        layouts = self.getLayouts(context)

        if layouts:
            # look for a standard view (by naming convention)
            for name, title in layouts:
                if name == u'standard':
                    return (name, title)
            
            # otherwise return first view factory
            return layouts[0]

        raise ValueError
    
    def getLayouts(self, context):
        if ICollageAlias.providedBy(context):
            # use target as context
            target = context.get_target()
            if target: context = target
            
        return getViewFactoryInfo(context, ICollageBrowserLayer)
