from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.Collage.content.common import LayoutContainer,CommonCollageSchema
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.Collage.interfaces import ICollageColumn

from zope.interface import implements

# CMFDynamicViewFTI imports
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Collage.utilities import findFirstAvailableInteger, isNumber

CollageColumnSchema = atapi.BaseContent.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='title',
        accessor='Title',
        required=False,
        widget=atapi.StringWidget(
            label='Title',
            label_msgid='Collage_label_title',
            description='You may optionally supply a title for this column.',
            i18n_domain='Collage',
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

class CollageColumn(BrowserDefaultMixin, LayoutContainer, atapi.OrderedBaseFolder):
    __implements__ = (getattr(atapi.OrderedBaseFolder,'__implements__',()), \
                      getattr(BrowserDefaultMixin,'__implements__',()))

    schema = CollageColumnSchema
    
    _at_rename_after_creation = True

    implements(ICollageColumn)

    security = ClassSecurityInfo()

    def generateNewId(self):
        parent_contents = self.aq_parent.objectValues()
        contentIDs = map(lambda x: x.getId(), parent_contents)
        numericalIDs = filter(isNumber.match, contentIDs)
        return str(findFirstAvailableInteger(numericalIDs))

    def SearchableText(self):
        return self.aggregateSearchableText()

atapi.registerType(CollageColumn, 'Collage')
