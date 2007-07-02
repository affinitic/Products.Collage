from Products.Five.browser import BrowserView

from Products.CMFPlone.utils import getSiteEncoding
from Products.CMFPlone import utils as cmfutils

class ExistingItemsView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        
        # beware of url-encoded spaces
        if 'portal_type' in self.request:
            self.request['portal_type'] = self.request['portal_type'].replace('%20', ' ')

    def __call__(self):
        """There are browser-issues in sending out content in UTF-8.
        We'll encode it in latin-1."""
        
        self.request.RESPONSE.setHeader("Content-Type",
                                        "text/html; charset=ISO-8859-1")

        encoding = getSiteEncoding(self.context.context)        
        return self.index().decode(encoding).encode('latin-1')
    
    @property
    def catalog(self):
        return cmfutils.getToolByName(self.context,
                                      'portal_catalog')

    def normalizeString(self, str):
        return self.context.plone_utils.normalizeString(str)
        
    def getItems(self):
        items = self.catalog(self.request,
                             sort_on='modified')[:self.request.get('count', 20)]

        return [{'UID': obj.UID(),
                 'title': result.Title,
                 'type': result.Type,
                 'portal_type':  self.normalizeString(result.portal_type),
                 'modified': result.ModificationDate,
                 'published': result.EffectiveDate or ''} for (result, obj) in
                map(lambda result: (result, result.getObject()), items)]
