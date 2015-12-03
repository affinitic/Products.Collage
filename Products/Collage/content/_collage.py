# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTMixin
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Collage.content.common import CommonCollageSchema
from Products.Collage.content.common import LayoutContainer
from Products.Collage.interfaces import ICollage
from Products.Collage.utilities import CollageMessageFactory as _
from zope.interface import implementer

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi

CollageSchema = atapi.BaseContent.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='title',
        searchable=True,
        widget=atapi.StringWidget(
            label='Title',
            label_msgid='label_title',
            i18n_domain='plone',
        )
    ),

    atapi.TextField(
        name='description',
        searchable=True,
        widget=atapi.TextAreaWidget(
            label='Description',
            label_msgid='label_description',
            i18n_domain='plone',
        )
    ),
    atapi.BooleanField(
        'show_title',
        accessor='getShowTitle',
        widget=atapi.BooleanWidget(
            label=_(u'label_show_title', default=u"Show title"),
            description=_(
                u'help_show_title',
                default=u"Show title in page composition."
            )
        ),
        default=1,
        languageIndependent=True,
        schemata="settings"),

    atapi.BooleanField(
        'show_description',
        accessor='getShowDescription',
        widget=atapi.BooleanWidget(
            label=_(u'label_show_description',
                    default='Show description'),
            description=_(
                u'help_show_description',
                default=u"Show description in page composition."
            )
        ),
        default=1,
        languageIndependent=True,
        schemata="settings"),

    atapi.BooleanField(
        'index_subobjects',
        accessor='mustIndexSubobjects',
        default=False,
        languageIndependent=True,
        schemata="settings",
        widget=atapi.BooleanWidget(
            label=_(u'label_index_subobjects',
                    default=u"Add collage contents in searchable text?"),
            description=_(
                u'help_index_subobjects',
                default=u"Show this collage in results when searching for "
                        u"terms appearing in a contained item. "
                        u"Note: Checking this option may slow down the system "
                        u"while editing the collage."
            )
        )
    )


))

CollageSchema = CollageSchema + CommonCollageSchema.copy()

# move description to main edit page
CollageSchema['description'].schemata = 'default'

# support show in navigation feature and at marshalling
# speciel case set folderish to False since we want related items to be used
finalizeATCTSchema(CollageSchema, folderish=False, moveDiscussion=False)


@implementer(ICollage, INonStructuralFolder)
class Collage(LayoutContainer, ATCTMixin, atapi.OrderedBaseFolder):

    schema = CollageSchema

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    def SearchableText(self):
        return self.aggregateSearchableText()

atapi.registerType(Collage, 'Collage')
