from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.Collage.content.common import LayoutContainer,CommonCollageSchema
from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.Collage.interfaces import ICollageRow

from zope.interface import implements

# CMFDynamicViewFTI imports
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.Collage.utilities import findFirstAvailableInteger, isNumber

CollageRowSchema = atapi.BaseContent.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='title',
        accessor='Title',
        required=False,
        widget=atapi.StringWidget(
            label='Title',
            label_msgid='Collage_label_title',
            description='You may optionally supply a title for this content row.',
            description_msgid='Collage_description_title',
            i18n_domain='Collage',
        )
    ),
))

CollageRowSchema = CollageRowSchema + CommonCollageSchema.copy()


# move description to main edit page
CollageRowSchema['description'].schemata = 'default'

#never show row in navigation, also when its selected
CollageRowSchema['excludeFromNav'].default = True

# support show in navigation feature and at marshalling
finalizeATCTSchema(CollageRowSchema, folderish=True, moveDiscussion=False)


class CollageRow(BrowserDefaultMixin, LayoutContainer, atapi.OrderedBaseFolder):
    __implements__ = (getattr(atapi.OrderedBaseFolder,'__implements__',()), \
                      getattr(BrowserDefaultMixin,'__implements__',()))

    meta_type = 'CollageRow'

    schema = CollageRowSchema
    
    _at_rename_after_creation = True

    implements(ICollageRow)

    security = ClassSecurityInfo()

    def generateNewId(self):
        parent_contents = self.aq_parent.objectValues()
        contentIDs = map(lambda x: x.getId(), parent_contents)
        numericalIDs = filter(isNumber.match, contentIDs)
        return str(findFirstAvailableInteger(numericalIDs))

    security.declareProtected(ModifyPortalContent, 'reorderObject')
    def reorderObject(self, id, position, REQUEST=None):
        "Move a collagerow up or down the page"

        if position.lower()=='up':
            self.moveObjectsUp(id)

        if position.lower()=='down':
            self.moveObjectsDown(id)

        if position.lower()=='top':
            self.moveObjectsToTop(id)

        if position.lower()=='bottom':
            self.moveObjectsToBottom(id)

        # order folder by field
        # id in this case is the field
        if position.lower()=='ordered':
            self.orderObjects(id)

        self.plone_utils.reindexOnReorder(self)

        if REQUEST.get('simple'):
            return 1
        
        if not REQUEST is None:
            REQUEST.RESPONSE.redirect(self.aq_parent.absolute_url() + '/manage_page')

    def SearchableText(self):
        return self.aggregateSearchableText()

    ##Based on RichDocument/content/richdocument.py
    # This method, from ISelectableBrowserDefault, is used to check whether
    # the "Choose content item to use as deafult view" option will be
    # presented. This makes sense for folders, but not for RichDocument, so
    # always disallow
    def canSetDefaultPage(self):
        return False

    security.declareProtected(View, 'getColumnBatches')
    def getColumnBatches(self, bsize):
        columns = self.getFolderContents()
        if not columns:
            return []

        # calculate number of batches
        count = (len(columns)-1)/3+1
        
        batches = []
        for c in range(count):
            batch = []
            for i in range(bsize):
                index = c*bsize+i

                # pad with null-columns
                column = None

                if index < len(columns):
                    column = columns[index]

                # do not pad first row
                if column or c > 0:
                    batch += [column]
                
            batches += [batch]
        
        return batches
    
atapi.registerType(CollageRow, 'Collage')
