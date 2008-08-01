from zope.annotation.interfaces import IAnnotations

from zope.interface import (
    Interface, implements, providedBy, directlyProvidedBy,
    directlyProvides)

from zope.component import getSiteManager, getMultiAdapter, getUtilitiesFor

from interfaces import IDynamicViewManager
from interfaces import ICollageAlias
from interfaces import ICollageBrowserLayer

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

        return self._getViewFactoryInfo(ICollageBrowserLayer, context=context)

    def _getViewFactoryInfo(self, layer, context=None):
        """Return view factory info for this context and browser layer."""

        if not context:
            context = self.context

        sm = getSiteManager(context)

        context_ifaces = providedBy(context)

        lookupAll = sm.adapters.lookupAll

        collage_aware = lookupAll((context_ifaces, layer), Interface)
        collage_agnostic = list(lookupAll((context_ifaces, Interface), Interface))

        return [(name, getattr(factory, 'title', name)) \
                for (name, factory) in collage_aware if (name, factory) not in collage_agnostic]


    def getSkin(self):
        storage = self.getStorage()
        return storage.get('skin', None)


    def setSkin(self, skin):
        storage = self.getStorage()
        storage['skin'] = skin


    def getSkins(self, request=None):

        layout = self.getLayout()
        skins = []

        if layout and request:
            request.debug = False

            ifaces = directlyProvidedBy(request)
            directlyProvides(request, ICollageBrowserLayer)

            target = self.context
            if ICollageAlias.providedBy(target):
                target = target.get_target()
                if not target:
                    target = self.context

            view = getMultiAdapter((target, request), name=layout)

            skinInterfaces = getattr(view, 'skinInterfaces', ())

            for si in skinInterfaces:
                for name, utility in getUtilitiesFor(si):
                    skins.append((name, utility.title))

            # restore interfaces
            directlyProvides(request, ifaces)

        skins.sort(lambda x, y: cmp(x[0], y[0]))
        return skins



