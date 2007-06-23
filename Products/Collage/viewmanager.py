from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable

from zope.interface import Interface
from zope.interface import implements, alsoProvides, providedBy

from zope.component import getSiteManager
from zope.component.interfaces import ComponentLookupError

from interfaces import IDynamicViewManager
from interfaces import ICollageAlias

from persistent.dict import PersistentDict

ANNOTATIONS_KEY = u'Collage'

def getAdapters(objects, provided, context=None):
    """Apparently it may be the case that views are registered
    with a non-callable factory which will cause the getAdapters
    method from zope.component to fail.
    """
    
    try:
        sitemanager = getSiteManager(context)
    except ComponentLookupError:
        # Oh blast, no site manager. This should *never* happen!
        return []

    result = []
    for name, factory in sitemanager.adapters.lookupAll(map(providedBy, objects),
                                                        provided):
        if callable(factory):
            adapter = factory(*objects)
            
            if adapter is not None:
                result.append((name, adapter))
        else:
            continue
        
    return result

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

    def getDefaultLayout(self, context, request):
        views = self.getViews(context, request)

        if views:
            # look for a standard view (by naming convention)
            for v in views:
                name, view = v
                if name == u'standard':
                    return name
            
            # otherwise return first view
            name, view = views[0]

            return name

        return None
    
    def getViews(self, context, request):
        if ICollageAlias.providedBy(context):
            # use target as context
            target = context.get_target()
            if target: context = target
            
        # assume desired layers are already in the request
        views = getAdapters((context, request), Interface)

        # only allow metaclasses
        views = [v for v in views if 'metaclass' in str(v)]

        return views
