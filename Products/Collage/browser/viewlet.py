from zope.viewlet import viewlet
from zope.component import getMultiAdapter
from zope.interface import directlyProvidedBy, directlyProvides

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
        context = self.context

        # handle aliased objects
        alias = getattr(self.__parent__, '__alias__', None)
        if alias: context = alias

        manager = IDynamicViewManager(context)

        # lookup active layout
        active = manager.getLayout()

        if not active:
            active, title = manager.getDefaultLayout()
        
        # compile list of registered layouts
        layouts = manager.getLayouts()

        # filter out fallback view
        layouts = filter(lambda (name, title): name != u'fallback', layouts)

        return [{'id': name,
                 'name': title,
                 'active': name == active} for (name, title) in layouts]

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
