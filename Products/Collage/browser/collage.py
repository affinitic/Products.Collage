from Products.Five.browser import BrowserView

from zope.interface import alsoProvides
from zope.interface import Interface

from Products.Collage.interfaces import ICollageEditLayer

class ICollageView(Interface):
    def isStructuralFolder():
        """Copied from CMFPlone/browser/plone.py."""

    def edit_mode():
        pass
    
class CollageView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
        url = request.get('ACTUAL_URL', request.get('URL', None))
        if url.endswith('manage_page'):
            # add marker interfaces to request
            alsoProvides(self.request, ICollageEditLayer)

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
        elif z2INonStructuralFolder.isImplementedBy(context):
            # BBB: for z2 interface compat
            return False
        else:
            return folderish
    
