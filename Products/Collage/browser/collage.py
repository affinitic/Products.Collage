# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Collage.interfaces import ICollageEditLayer
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

from Acquisition import aq_inner
from Products.Collage.interfaces import ICollage
from zope.component import queryMultiAdapter


class CollageView(BrowserView):

    def isStructuralFolder(self, instance):
        context = instance
        folderish = bool(getattr(aq_base(context), 'isPrincipiaFolderish',
                                 False))
        if not folderish:
            return False
        elif INonStructuralFolder.providedBy(context):
            return False
        else:
            return folderish


class CollageComposeView(CollageView):

    def __call__(self):
        if ICollage.providedBy(self.context) is False:
            default_page = self.get_default_page()
            if ICollage.providedBy(default_page):
                url = '{0}/compose'.format(default_page.absolute_url())
                self.request.response.redirect(url)
                return None
        alsoProvides(self.request, ICollageEditLayer)
        result = super(CollageComposeView, self).__call__()
        noLongerProvides(self.request, ICollageEditLayer)
        return result

    def get_default_page(self):
        default_page_helper = queryMultiAdapter(
            (self.context, self.request),
            name='default_page',
        )
        if not default_page_helper:
            return None
        object_name = default_page_helper.getDefaultPage()
        return getattr(aq_inner(self.context), object_name, None)
