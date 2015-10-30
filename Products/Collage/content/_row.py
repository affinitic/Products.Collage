# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.Collage.content.common import CommonCollageSchema
from Products.Collage.content.common import LayoutContainer
from Products.Collage.interfaces import ICollageRow
from Products.Collage.utilities import CollageMessageFactory as _
from zope.interface import implementer

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi


CollageRowSchema = atapi.BaseContent.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='title',
        accessor='Title',
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            label=_(u'label_optional_row_title', default='Title'),
            description=_(
                u'help_optional_row_title',
                default=u"You may optionally supply a title for this row."
            ),
        )
    ),
))

CollageRowSchema = CollageRowSchema + CommonCollageSchema.copy()

# move description to main edit page
CollageRowSchema['description'].schemata = 'default'

# never show row in navigation, also when its selected
CollageRowSchema['excludeFromNav'].default = True

# support show in navigation feature and at marshalling
finalizeATCTSchema(CollageRowSchema, folderish=True, moveDiscussion=False)


@implementer(ICollageRow)
class CollageRow(
    BrowserDefaultMixin,
    LayoutContainer,
    atapi.OrderedBaseFolder
):

    schema = CollageRowSchema

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


atapi.registerType(CollageRow, 'Collage')
