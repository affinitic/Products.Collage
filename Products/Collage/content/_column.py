from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.Collage.content.common import LayoutContainer

from Products.ATContentTypes.content.document import ATDocument
from Products.Archetypes.utils import DisplayList

# CMFDynamicViewFTI imports
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

# define list of dynamic types
DYNAMIC_TYPES = ('Topic', 'Folder')

# define list of possible fields with friendly name
FIELDS = (('title','Title',),
          ('description','Description',),
          ('text','Text',),
          ('date','Date',),
          ('author','Author',),
          ('email','Email',),
          ('image','Image',),
          ('images','Images',),
          ('link','Link',),
          ('icon','Icon',),
         )

CollageColumnSchema = ATDocument.schema.copy() + atapi.Schema((
    atapi.ReferenceField(
        name='items',
        mutator='set_items',
        accessor='get_items',
        relationship='Collage_staticItems',
        multiValued = 1,
        allowed_types = (),
        widget=ReferenceBrowserWidget(
            label='Selected items',
            label_msgid='Collage_label_static_list',
            i18n_domain='Collage',
            startup_directory='/',
        ),
    ),

    atapi.LinesField(
        name='visible_fields',
        mutator='set_visible_fields',
        accessor='get_visible_fields',
        multiValued=True,
        vocabulary='visible_fields_vocabulary',
        default = ('title', 'description', 'date', 'author', 'email', 'image', 'images', 'link',),
        widget=atapi.MultiSelectionWidget(
            size = 10,
            label='Visible fields for selected items',
            label_msgid='Collage_label_topic_visible_fields',
            i18n_domain='Collage',
        ),
    ),
))

# move description to main edit page
CollageColumnSchema['description'].schemata = 'default'

# we don't require any fields to be filled out
CollageColumnSchema['title'].required = False
CollageColumnSchema['text'].required = False

# never show row in navigation, also when its selected
CollageColumnSchema['excludeFromNav'].default = True

# don't show related items field
CollageColumnSchema['relatedItems'].widget.visible['edit'] = 'invisible'

#since its a subclassed atdocument, no need for finalizeATCTSchema


class CollageColumn(BrowserDefaultMixin, LayoutContainer, ATDocument):
    __implements__ = (getattr(atapi.OrderedBaseFolder,'__implements__',()), \
                      getattr(BrowserDefaultMixin,'__implements__',()))

    meta_type = 'CollageColumn'

    schema = CollageColumnSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    security.declarePublic('visible_fields_vocabulary')
    def visible_fields_vocabulary(self):
        """Returns displaylist of possible fields."""

        return DisplayList(FIELDS)

    security.declarePublic('getDynamicItems')
    def getDynamicItems(self):
        dynamic_items = [i for i in self.get_items() if i.portal_type in DYNAMIC_TYPES]

        items = []
        for item in dynamic_items:
            contents = [i.getObject() for i in item.queryCatalog()]
            items += list(contents)
            
        return self.getItemsAsDict(items)
    
    security.declarePublic('getStaticItems')
    def getStaticItems(self):
        items = [i for i in self.get_items() if i.portal_type not in DYNAMIC_TYPES]
        return self.getItemsAsDict(items)
    
    def getItemsAsDict(self, selected_items):
        """
        Pairs selected items' visible fields with content (using
        accessor-function).

        Add a Collage-object, with a row and a column

        >>> self.setRoles(['Manager'])
        >>> _ = self.folder.invokeFactory('Collage', 'p0')
        >>> _ = self.folder.p0.invokeFactory('CollageRow', 'r0')
        >>> _ = self.folder.p0.r0.invokeFactory('CollageColumn', 'c0')
        >>> column = self.folder.p0.r0.c0

        Now add three documents and attach them to the column for display.

        >>> for i in range(3):
        ...     _ = self.folder.invokeFactory('Document', 'd%s' % i)
        >>> self.folder.d0.setTitle("A Title")
        >>> self.folder.d1.setDescription("A Description")
        >>> self.folder.d2.setText("A body text")
        >>> references = self.folder.d0, self.folder.d1, self.folder.d2
        >>> column.set_items(references)
        >>> column.set_visible_fields(('title', 'description'))
        
        Confirm that we get a list of dictionary pairing IDs to fields

        >>> column.getItemsAsDict(column.get_items())
        [{'url': 'http://nohost/plone/Members/test_user_1_/d0', 'object': \
        <ATDocument at /plone/Members/test_user_1_/d0>, 'description': '', \
        'title': 'A Title'}, {'url': 'http://nohost/plone/Members/test_user_1_/d1', \
        'object': <ATDocument at /plone/Members/test_user_1_/d1>, 'description': \
        'A Description', 'title': ''}, \
        {'url': 'http://nohost/plone/Members/test_user_1_/d2', 'object': \
        <ATDocument at /plone/Members/test_user_1_/d2>, 'description': '', 'title': ''}]
        
        Now, add text to list of visible fields and try again

        >>> column.set_visible_fields(('title', 'description', 'text'))
        >>> column.getItemsAsDict(column.get_items())
        [{'url': 'http://nohost/plone/Members/test_user_1_/d0', 'text': '', \
        'object': <ATDocument at /plone/Members/test_user_1_/d0>, 'description': '', \
        'title': 'A Title'}, {'url': 'http://nohost/plone/Members/test_user_1_/d1', \
        'text': '', 'object': <ATDocument at /plone/Members/test_user_1_/d1>, \
        'description': 'A Description', 'title': ''}, \
        {'url': 'http://nohost/plone/Members/test_user_1_/d2', 'text': \
        '<p>A body text</p>', 'object': <ATDocument at /plone/Members/test_user_1_/d2>, \
        'description': '', 'title': ''}]
        
        """

        items = []
        for item in selected_items:
            fields = {}
            allowed_fields = self.get_visible_fields()

            visible_fields = [f for f in item.schema.fields() if f.getName() in allowed_fields]
            for field in visible_fields:
                accessor = field.getAccessor(item)
                fields[field.getName()] = accessor()

            # add attributes
            fields['url'] = item.absolute_url();
            fields['object'] = item
            
            items.append(fields)

        return items

atapi.registerType(CollageColumn, 'Collage')
