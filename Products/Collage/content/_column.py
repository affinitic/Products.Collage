# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.Collage.content.common import CommonCollageSchema
from Products.Collage.content.common import LayoutContainer
from Products.Collage.interfaces import ICollageColumn
from Products.Collage.utilities import CollageMessageFactory as _
from zope.interface import implementer

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi

CollageColumnSchema = atapi.BaseContent.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='title',
        accessor='Title',
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'label_optional_column_title', default=u"Title"),
            description=_(
                u'help_optional_column_title',
                default=u"You may optionally supply a title for this column."
            ),
        )
    ),
))

CollageColumnSchema = CollageColumnSchema + CommonCollageSchema.copy()

# move description to main edit page
CollageColumnSchema['description'].schemata = 'default'

# never show row in navigation, also when its selected
CollageColumnSchema['excludeFromNav'].default = True

# support show in navigation feature and at marshalling
finalizeATCTSchema(CollageColumnSchema, folderish=True, moveDiscussion=False)


@implementer(ICollageColumn)
class CollageColumn(
    BrowserDefaultMixin,
    LayoutContainer,
    atapi.OrderedBaseFolder
):

    schema = CollageColumnSchema

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    def SearchableText(self):
        return self.aggregateSearchableText()

    def indexObject(self):
        pass

    def reindexObject(self, idxs=[]):
        pass

    def unindexObject(self):
        pass

atapi.registerType(CollageColumn, 'Collage')
