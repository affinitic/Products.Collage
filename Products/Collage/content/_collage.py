from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.Collage.content.common import LayoutContainer, CommonCollageSchema

# from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.CMFPlone.interfaces import INonStructuralFolder

# CMFDynamicViewFTI imports
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Collage.interfaces import ICollage

from zope.interface import implements

CollageSchema = atapi.BaseContent.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='title',
        searchable=True,
        widget=atapi.StringWidget(
            label='Title',
            label_msgid='Collage_label_title',
            i18n_domain='Collage',
        )
    ),

    atapi.TextField(
        name='description',
        searchable=True,
        widget=atapi.TextAreaWidget(
            label='Description',
            label_msgid='Collage_label_description',
            i18n_domain='Collage',
        )
    ),
    atapi.BooleanField('show_title',
        accessor='getShowTitle',
        widget=atapi.BooleanWidget(label='Show title',
                                   label_msgid='label_show_title',
                                   i18n_domain='Collage'
                                   ),
                       default=1
                       ),

    atapi.BooleanField('show_description',
        accessor='getShowDescription',
        widget=atapi.BooleanWidget(label='Show description',
                                   label_msgid='label_show_description',
                                   i18n_domain='Collage'
                                   ),
                       default=1
                       ),

    
))

CollageSchema = CollageSchema + CommonCollageSchema.copy()

# move description to main edit page
CollageSchema['description'].schemata = 'default'

# support show in navigation feature and at marshalling
# speciel case set folderish to False since we want related items to be used
finalizeATCTSchema(CollageSchema, folderish=False, moveDiscussion=False)

class Collage(LayoutContainer, BrowserDefaultMixin, atapi.OrderedBaseFolder):
    __implements__ = (getattr(atapi.OrderedBaseFolder,'__implements__',()), \
                      getattr(BrowserDefaultMixin,'__implements__',()))

    schema = CollageSchema

    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    implements(ICollage, INonStructuralFolder)

    def SearchableText(self):
        return self.aggregateSearchableText()

atapi.registerType(Collage, 'Collage')
