# $Id$

from zope.interface import Interface, alsoProvides

from Acquisition import aq_base

from Products.Five.browser import BrowserView
from Products.CMFPlone.interfaces import INonStructuralFolder

from Products.Collage.interfaces import ICollageEditLayer

class ICollageView(Interface):
    def isStructuralFolder():
        """Copied from CMFPlone/browser/plone.py."""

    def edit_mode():
        pass

class CollageView(BrowserView):
    def edit_mode(self):
        return ICollageEditLayer.providedBy(self.request)

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

    def render_manage_view(self):
        """Set the edit layer on the request and return the
        standard view as returned by CMFDynamicViewFTI."""

        alsoProvides(self.request, ICollageEditLayer)

        fti = self.context.getTypeInfo()
        method = fti.getViewMethod(self.context)

        view = self.context.restrictedTraverse(method)
        return view()
