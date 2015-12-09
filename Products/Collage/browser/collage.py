# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Collage.interfaces import ICollageEditLayer
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.interface import noLongerProvides


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
        alsoProvides(self.request, ICollageEditLayer)
        result = super(CollageComposeView, self).__call__()
        noLongerProvides(self.request, ICollageEditLayer)
        return result
