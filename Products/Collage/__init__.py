from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

from Products.CMFCore.DirectoryView import registerDirectory
import Products.CMFPlone.interfaces

# Make the skins available as DirectoryViews                                                        
registerDirectory( 'skins', globals() )

def initialize(context):
    from Products.Collage import content
    from Products.CMFCore import utils as cmfutils
    from Products.Archetypes import atapi

    all_content_types, \
    all_constructors, \
    all_ftis = atapi.process_types(atapi.listTypes('Collage'),
                                   'Collage')
    
    cmfutils.ContentInit('Collage Content',
                         content_types = all_content_types,
                         permission = 'Add Collage content',
                         extra_constructors = all_constructors,
                         fti = all_ftis,
                         ).initialize(context)
    
    profile_registry.registerProfile(
        name='default',
        title='Collage profile',
        description='Profile for Collage',
        path='profiles/default',
        product='Collage',
        profile_type=EXTENSION,
        for_=Products.CMFPlone.interfaces.IPloneSiteRoot)
    
