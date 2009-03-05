# -*- coding: utf-8 -*-
# $Id$
"""Collage site wide options"""

from zope.interface import Interface
from zope.component import adapts
from zope.interface import implements
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import Tuple
from zope.schema import Int
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.app.vocabularies.types import BAD_TYPES
from zope.formlib.form import FormFields
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import MultiCheckBoxThreeColumnWidget
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Collage.config import PROPERTYSHEETNAME
from Products.Collage.config import COLLAGE_TYPES
from Products.Collage.utilities import getPortal
from Products.Collage.utilities import CollageMessageFactory as _

class ICollageSiteOptions(Interface):

    use_whitelist = Bool(
        title=_(u'label_use_whitelist', default=u"Use types whitelist"),
        description=_(u'help_use_whitelist',
                      default=u"Only types in below whitelist can be added in a Collage."),
        default=False,
        required=True)

    types_whitelist = Tuple(
        title=_(u'label_types_whitelist', default=u"Types whitelist"),
        description=_(u'help_types_whitelist',
                      default=u"Select item types that can be added in a Collage object."),
        required=False,
        missing_value=tuple(),
        value_type=Choice(vocabulary='collage.vocabularies.CollageUserFriendlyTypes'))

    alias_whitelist = Tuple(
        title=_(u'label_alias_whitelist', default=u"Alias whitelist"),
        description=_(u'help_alias_whitelist',
                      default=u"Select item types that can be aliased in a Collage object."),
        required=False,
        missing_value=tuple(),
        value_type=Choice(vocabulary='collage.vocabularies.CollageUserFriendlyTypes'))

    alias_search_limit = Int(
        title=_(u'label_alias_search_limit', default=u"Alias search limit"),
        description=_(u'help_alias_search_limit',
                      default=u"Alias target search maximum results. '0' or negative means unlimited."),
        required=False,
        default=50)
    
    def enabledType(portal_type):
        """True if portal type is enabled for adding in a Collage."""

    def enabledAlias(portal_type):
        """True if portal type is enabled for alias in a Collage"""


class CollageSiteOptions(SchemaAdapterBase):

    implements(ICollageSiteOptions)
    adapts(IPloneSiteRoot)

    use_whitelist = ProxyFieldProperty(ICollageSiteOptions['use_whitelist'])
    types_whitelist = ProxyFieldProperty(ICollageSiteOptions['types_whitelist'])
    alias_whitelist = ProxyFieldProperty(ICollageSiteOptions['alias_whitelist'])
    alias_search_limit = ProxyFieldProperty(ICollageSiteOptions['alias_search_limit'])

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
    form_fields['types_whitelist'].custom_widget = MultiCheckBoxThreeColumnWidget
    form_fields['alias_whitelist'].custom_widget = MultiCheckBoxThreeColumnWidget

    label = form_name = _(u'title_collage_controlpanel', default=u"Collage control panel")
    description = _(u'help_collage_controlpanel', default=u"Site wide options for Collage")


class CollageUserFriendlyTypesVocabulary(object):
    """Vocabulary"""
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ttool = getToolByName(context, 'portal_types', None)
        if ttool is None:
            return None
        items = [(t, t, ttool[t].Title())
                  for t in ttool.listContentTypes()
                  if t not in BAD_TYPES + COLLAGE_TYPES]
        items = [SimpleTerm(*v) for v in items]
        return SimpleVocabulary(items)

CollageUserFriendlyTypesVocabularyFactory = CollageUserFriendlyTypesVocabulary()
