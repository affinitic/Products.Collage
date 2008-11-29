# -*- coding: utf-8 -*-
# $Id$

import sys
from urllib import unquote_plus
from types import UnicodeType
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from plone.memoize.view import memoize_contextless
from Products.CMFPlone.utils import getSiteEncoding
from Products.CMFPlone import PloneMessageFactory as p_
from Products.Collage.utilities import getCollageSiteOptions
from utils import escape_to_entities


class ExistingItemsView(BrowserView):

    def __init__(self, *args, **kw):
        """We must recode the Unicode quoted request from javascript"""

        super(ExistingItemsView, self).__init__(*args, **kw)
        for param, value in self.request.form.items():
            value = unquote_plus(value)
            self.request.form[param] = value
        return


    def __call__(self):
        """There are browser-issues in sending out content in UTF-8.
        We'll encode it in latin-1."""

        # IE6 encoding bug workaround (IE6 sucks but...)
        if self.request.get('USER_AGENT', '').find('MSIE 6.0') > 0:
            self.request.RESPONSE.setHeader("Content-Type", "text/html; charset=ISO-8859-1")
            encoding = getSiteEncoding(self.context.context)
            content = self.index()
            if not isinstance(content, UnicodeType):
                content = content.decode(encoding)

            # Convert special characters to HTML entities since we're recoding
            # to latin-1
            return escape_to_entities(content).encode('latin-1')
        else:
            return self.index()


    @property
    def catalog(self):
        return getMultiAdapter((self.context, self.request),
                               name=u'plone_tools').catalog()


    def portal_url(self):
        return getMultiAdapter((self.context, self.request),
                               name=u'plone_portal_state').portal_url()


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

        limit = getCollageSiteOptions().alias_search_limit
        if limit <= 0:
            limit = sys.maxint
        items = self.catalog(SearchableText=self.request.get('SearchableText', ''),
                             portal_type=portal_types,
                             sort_order='reverse',
                             sort_on='modified',
                             sort_limit=limit)

        # setup description cropping
        cropText = self.context.restrictedTraverse('@@plone').cropText
        croptext = getMultiAdapter((self.context, self.request),
                                   name=u'plone').cropText
        props = getMultiAdapter((self.context, self.request),
                                name=u'plone_tools').properties()
        site_properties = props.site_properties
        desc_length = getattr(site_properties, 'search_results_description_length', 25)
        desc_ellipsis = getattr(site_properties, 'ellipsis', '...')
        portal_url = self.portal_url()

        return [{'UID': result.UID,
                 'icon' : result.getIcon,
                 'title': result.Title,
                 'description': cropText(result.Description, desc_length, desc_ellipsis),
                 'type': result.Type,
                 'target_url': result.getURL(),
                 'link_css_class': 'state-%s' % result.review_state
                 }
                for result in items]

