# -*- coding: utf-8 -*-
# $Id$

from types import UnicodeType
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from plone.memoize.view import memoize_contextless
from Products.CMFPlone.utils import getSiteEncoding
from Products.CMFPlone import utils as cmfutils
from Products.CMFPlone import PloneMessageFactory as p_
from Products.Collage.utilities import getCollageSiteOptions
from utils import escape_to_entities


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

        content = self.index()
        if not isinstance(content, UnicodeType):
            content = content.decode(encoding)

        # convert special characters to HTML entities since we're recoding
        # to latin-1
        return escape_to_entities(content).encode('latin-1')

    @property
    def catalog(self):
        return cmfutils.getToolByName(self.context,
                                      'portal_catalog')

    def portal_url(self):
        return cmfutils.getToolByName(self.context, 'portal_url')()

    def normalizeString(self, str):
        return self.context.plone_utils.normalizeString(str)

    @memoize_contextless
    def listEnabledTypes(self):
        """Enabled types in a Collage as list of dicts"""

        actual_portal_type = self.request.get('portal_type', None)
        collage_options = getCollageSiteOptions()
        return [{'id': pt.getId(),
                 'title': p_(pt.Title()),
                 'selected': pt.getId() == actual_portal_type and 'selected' or None}
                for pt in self.context.getAllowedTypes()
                if collage_options.enabledType(pt.getId())]

    def getItems(self):
        """Found items"""

        portal_types = self.request.get('portal_type', None)
        if not portal_types:
            portal_types = [pt['id'] for pt in self.listEnabledTypes()]
        limit = self.request.get('count', 50)
        items = self.catalog(SearchableText=self.request.get('SearchableText', ''),
                             portal_type=portal_types,
                             sort_order='reverse',
                             sort_on='modified',
                             sort_limit=limit)

        # setup description cropping
        cropText = self.context.restrictedTraverse('@@plone').cropText
        props = cmfutils.getToolByName(self.context, 'portal_properties')
        site_properties = props.site_properties
        desc_length = getattr(site_properties, 'search_results_description_length', 25)
        desc_ellipsis = getattr(site_properties, 'ellipsis', '...')
        portal_url = self.portal_url()

        return [{'UID': obj.UID(),
                 'icon' : result.getIcon,
                 'title': result.Title,
                 'description': cropText(result.Description, desc_length, desc_ellipsis),
                 'type': result.Type,
                 'portal_type':  self.normalizeString(result.portal_type),
                 'modified': result.ModificationDate,
                 'published': result.EffectiveDate or ''} for (result, obj) in
                map(lambda result: (result, result.getObject()), items)]

