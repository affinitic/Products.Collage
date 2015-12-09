# -*- coding: utf-8 -*-
"""Collage site wide options"""
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import MultiCheckBoxThreeColumnWidget
from plone.app.vocabularies.types import BAD_TYPES
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Collage.config import COLLAGE_TYPES
from Products.Collage.config import PROPERTYSHEETNAME
from Products.Collage.interfaces import ICollageSiteOptions
from Products.Collage.utilities import CollageMessageFactory as _
from Products.Collage.utilities import getPortal
from zope.component import adapter
from zope.formlib.form import FormFields
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    from zope.app.schema.vocabulary import IVocabularyFactory


@implementer(ICollageSiteOptions)
@adapter(IPloneSiteRoot)
class CollageSiteOptions(SchemaAdapterBase):

    ref_browser_empty = \
        ProxyFieldProperty(ICollageSiteOptions['ref_browser_empty'])
    ref_browser_types = \
        ProxyFieldProperty(ICollageSiteOptions['ref_browser_types'])
    use_whitelist = ProxyFieldProperty(ICollageSiteOptions['use_whitelist'])
    types_whitelist = ProxyFieldProperty(
        ICollageSiteOptions['types_whitelist'])
    alias_whitelist = ProxyFieldProperty(
        ICollageSiteOptions['alias_whitelist'])
    batch_size = ProxyFieldProperty(ICollageSiteOptions['batch_size'])

    def __init__(self, context):
        super(CollageSiteOptions, self).__init__(context)
        properties = getPortal().portal_properties
        self.context = properties.restrictedTraverse(PROPERTYSHEETNAME)

    def enabledType(self, portal_type):
        if portal_type in COLLAGE_TYPES:
            return False
        if self.use_whitelist:
            return portal_type in self.types_whitelist
        return True

    def enabledAlias(self, portal_type):
        if portal_type in COLLAGE_TYPES:
            return False
        if self.use_whitelist:
            return portal_type in self.alias_whitelist
        return True


class CollageControlPanel(ControlPanelForm):

    form_fields = FormFields(ICollageSiteOptions)
    form_fields['types_whitelist'].custom_widget = MultiCheckBoxThreeColumnWidget  # noqa
    form_fields['alias_whitelist'].custom_widget = MultiCheckBoxThreeColumnWidget  # noqa

    label = form_name = _(u'title_collage_controlpanel',
                          default=u"Collage control panel")
    description = _(u'help_collage_controlpanel',
                    default=u"Site wide options for Collage")


@implementer(IVocabularyFactory)
class CollageUserFriendlyTypesVocabulary(object):
    """Vocabulary"""

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ttool = getToolByName(context, 'portal_types', None)
        if ttool is None:
            return None
        CHECK_TYPES = list(BAD_TYPES) + list(COLLAGE_TYPES)
        items = [
            (t, t, ttool[t].Title())
            for t in ttool.listContentTypes()
            if t not in CHECK_TYPES
        ]
        items = [SimpleTerm(*v) for v in items]
        return SimpleVocabulary(items)

CollageUserFriendlyTypesVocabularyFactory = CollageUserFriendlyTypesVocabulary()  # noqa
