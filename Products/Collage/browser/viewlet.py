from zope.viewlet import viewlet
from zope.component import getUtility, getMultiAdapter
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.interface import directlyProvidedBy, directlyProvides, alsoProvides

from Products.CMFCore.utils import getToolByName

from Products.Collage.interfaces import ICollageBrowserLayer
from Products.Collage.interfaces import IDynamicViewManager
from Products.Collage.interfaces import ICollageAlias

class SimpleContentMenuViewlet(object):
    def portal_url(self):
        return getToolByName(self.context, 'portal_url')()

    def test(self):
        return lambda a, b, c: a and b or c

    def getTargetURL(self):
        alias = getattr(self.__parent__, '__alias__', None)
        if alias:
            return alias.absolute_url()

        return self.context.absolute_url()        

class LayoutViewlet(SimpleContentMenuViewlet):
    def getLayouts(self):
        manager = getUtility(IDynamicViewManager)
        context = self.context

        # add marker interfaces to request
        alsoProvides(self.request, ICollageBrowserLayer)
        
        # save list of interfaces
        provides = list(directlyProvidedBy(self.request))

        # remove default layer from request
        provides.remove(IDefaultBrowserLayer)
        directlyProvides(self.request, provides)

        # handle aliased objects
        alias = getattr(self.__parent__, '__alias__', None)
        if alias: context = alias
            
        # lookup active layout
        active = manager.getLayout(context)

        if not active:
            active = manager.getDefaultLayout(context, self.request)
        
        # compile list of layouts
        views = manager.getViews(context, self.request)

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

class IconViewlet(SimpleContentMenuViewlet):
    def getIcon(self):
        tt = getToolByName(self.context, 'portal_types')
        obj_typeinfo = tt.getTypeInfo(self.context.portal_type)

        return obj_typeinfo.getIcon()

class ActionsViewlet(SimpleContentMenuViewlet):
    def isAlias(self):
        return getattr(self.__parent__, '__alias__', None) and True
