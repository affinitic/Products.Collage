# -*- coding: utf-8 -*-
from persistent.dict import PersistentDict
from Products.CMFCore.utils import getToolByName
from Products.Collage.interfaces import ICollageAlias
from Products.Collage.interfaces import ICollageBrowserLayer
from Products.Collage.interfaces import ICollageBrowserLayerType
from Products.Collage.interfaces import IDynamicViewManager
from Products.Five import BrowserView
from zope.annotation.interfaces import IAnnotations
from zope.component import ComponentLookupError
from zope.component import getMultiAdapter
from zope.component import getSiteManager
from zope.component import getUtilitiesFor
from zope.component import queryUtility
from zope.interface import directlyProvidedBy
from zope.interface import directlyProvides
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import providedBy

ANNOTATIONS_KEY = u'Collage'


@implementer(IDynamicViewManager)
class DynamicViewManager(object):

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
        request = context.REQUEST

        if ICollageAlias.providedBy(self.context):
            target = self.context.get_target()
            if target is not None:
                context = target

        ifaces = mark_request(context, request)

        sm = getSiteManager()
        layouts = sm.adapters.lookupAll(
            required=(providedBy(context), providedBy(request)),
            provided=Interface
        )

        directlyProvides(request, *ifaces)
        layouts = [(name, getattr(layout, 'title', name))
                   for (name, layout) in layouts
                   if isinstance(layout, type) and
                   issubclass(layout, BrowserView) and
                   not getattr(layout, 'hide', False)]
        layouts.sort(lambda a, b: cmp(a[1], b[1]))
        return layouts

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

            ifaces = mark_request(self.context, request)

            target = self.context
            if ICollageAlias.providedBy(target):
                target = target.get_target()
                if not target:
                    target = self.context

            try:
                view = getMultiAdapter((target, request), name=layout)
                skinInterfaces = getattr(view, 'skinInterfaces', ())
            except ComponentLookupError:
                skinInterfaces = ()

            for si in skinInterfaces:
                for name, utility in getUtilitiesFor(si):
                    skins.append((name, utility.title))

            # restore interfaces
            directlyProvides(request, ifaces)

        skins.sort(lambda x, y: cmp(x[0], y[0]))
        return skins


def mark_request(context, request):
    """ Marks the request with general and theme-specific Collage browser layers.

        Returns the initial set of request marker interfaces so that you can
        restore them using directlyProvides(request, ifaces).
    """
    initial_ifaces = directlyProvidedBy(request)

    # general Collage layer
    directlyProvides(request, ICollageBrowserLayer)

    # theme-specific Collage layer
    portal_skins = getToolByName(context, 'portal_skins', None)
    if portal_skins is not None:
        skin_name = portal_skins.getCurrentSkinName()
        layer_iface = queryUtility(ICollageBrowserLayerType, name=skin_name)
        if layer_iface is not None:
            directlyProvides(request, layer_iface, ICollageBrowserLayer)

    return initial_ifaces
