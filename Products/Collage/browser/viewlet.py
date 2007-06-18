from zope.viewlet import viewlet
from zope.component import getUtility, getMultiAdapter
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import directlyProvidedBy, directlyProvides, alsoProvides

from Products.CMFCore.utils import getToolByName

from Products.Collage.interfaces import ICollageBrowserLayer, IDynamicViewManager

class SimpleContentMenuViewlet(object):
    def portal_url(self):
        return getToolByName(self.context, 'portal_url')()

    def test(self):
        return lambda a, b, c: a and b or c
        
class LayoutViewlet(object):
    def getLayouts(self):
        manager = getUtility(IDynamicViewManager)

        # add marker interfaces to request
        alsoProvides(self.request, ICollageBrowserLayer)
        
        # save list of interfaces
        provides = list(directlyProvidedBy(self.request))

        # remove default layer from request
        provides.remove(IDefaultBrowserLayer)
        directlyProvides(self.request, provides)        

        # lookup active layout
        active = manager.getLayout(self.context)

        if not active:
            active = manager.getDefaultLayout(self.context, self.request)
        
        # compile list of layouts
        views = manager.getViews(self.context, self.request)

        # filter out fallback
        views = [v for v in views if v[0] != u'fallback']
        
        layouts = [{'id': view[0],
                    'name': getattr(view[1], 'title', view[1].__name__),
                    'active': view[0] == active} for view in views]

        # restore interfaces
        provides.remove(ICollageBrowserLayer)
        provides.append(IDefaultBrowserLayer)
        directlyProvides(self.request, *provides)

        return layouts
    
class InsertNewItemViewlet(object):
    pass

class SplitColumnViewlet(object):
    pass
