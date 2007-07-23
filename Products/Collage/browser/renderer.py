from zope.interface import Interface
from zope.interface import directlyProvidedBy, directlyProvides, alsoProvides
from zope.component import getUtility, getMultiAdapter
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from Products.Five.browser import BrowserView

from Products.Collage.interfaces import ICollageBrowserLayer, IDynamicViewManager
from Products.Collage.interfaces import ICollageAlias

class SimpleContainerRenderer(BrowserView):
    def getItems(self, contents=None):
        # needed to circumvent bug :-(
        self.request.debug = False
        
        # add marker interfaces to request
        alsoProvides(self.request, ICollageBrowserLayer)
        
        # save list of interfaces
        provides = list(directlyProvidedBy(self.request))

        # remove default layer from request if present
        if IDefaultBrowserLayer in provides:
            provides.remove(IDefaultBrowserLayer)

        directlyProvides(self.request, provides)        
        
        views = []

        if not contents:
            contents = self.context.getFolderContents()

        for item in contents:
            target = context = item.getObject()
            manager = getUtility(IDynamicViewManager)
            layout = manager.getLayout(context)

            if not layout:
                layout = manager.getDefaultLayout(context, self.request)

            if ICollageAlias.providedBy(context):
                target = context.get_target()

                # if not set, revert to context
                if not target: target = context

            # assume that a layout is always available
            view = getMultiAdapter((target, self.request), name=layout)

            # store reference to alias if applicable
            if ICollageAlias.providedBy(context):
                view.__alias__ = context
            
            views.append(view)

        # restore interfaces
        provides.remove(ICollageBrowserLayer)
        provides.append(IDefaultBrowserLayer)
        directlyProvides(self.request, *provides)

        return views

