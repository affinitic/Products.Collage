# -*- coding: utf-8 -*-
# $Id$

from zope import interface
from zope import schema
from zope.viewlet.interfaces import IViewletManager
from zope.i18nmessageid import MessageFactory
from Products.Collage.config import I18N_DOMAIN

_ = MessageFactory(I18N_DOMAIN)

class ICollage(interface.Interface):
    pass

class ICollageRow(interface.Interface):
    pass

class ICollageColumn(interface.Interface):
    pass

class ICollageAlias(interface.Interface):
    pass

class IDynamicViewManager(interface.Interface):
    pass

class ICollageBrowserLayer(interface.Interface):
    """Collage browser layer. Views registered with this layer
    are available to objects inside a collage."""
    pass
    
class ICollageBrowserLayerType(interface.interfaces.IInterface):
    """Marker interface for Collage theme-specific layers
    """
    pass

class ICollageEditLayer(interface.Interface):
    """Collage edit layer."""
    pass

class IContentMenu(IViewletManager):
    """Interface for the content-menu viewlet manager."""
    pass

class IBelowItemsMenu(IViewletManager):
    """Interface for the menu below items viewlet manager."""
    pass

class IPortletSkin(interface.Interface):
    """Interface for skinable portlets views."""
    pass

class ICollageSiteOptions(interface.Interface):

    use_whitelist = schema.Bool(
        title=_(u'label_use_whitelist', default=u"Use types whitelist"),
        description=_(u'help_use_whitelist',
                      default=u"Only types in below whitelist can be added in "
                            u"a Collage."),
        default=False,
        required=True)

    types_whitelist = schema.Tuple(
        title=_(u'label_types_whitelist', default=u"Types whitelist"),
        description=_(u'help_types_whitelist',
                      default=u"Select item types that can be added in a "
                              u"Collage object."),
        required=False,
        missing_value=tuple(),
        value_type=schema.Choice(
            vocabulary='collage.vocabularies.CollageUserFriendlyTypes')
        )

    alias_whitelist = schema.Tuple(
        title=_(u'label_alias_whitelist', default=u"Alias whitelist"),
        description=_(u'help_alias_whitelist',
                      default=u"Select item types that can be aliased in a "
                            u"Collage object."),
        required=False,
        missing_value=tuple(),
        value_type=schema.Choice(
            vocabulary='collage.vocabularies.CollageUserFriendlyTypes')
        )

    alias_search_limit = schema.Int(
        title=_(u'label_alias_search_limit', default=u"Alias search limit"),
        description=_(u'help_alias_search_limit',
                      default=u"Alias target search maximum results. '0' or "
                              u"negative means unlimited."),
        required=False,
        default=50)
    
    def enabledType(portal_type):
        """True if portal type is enabled for adding in a Collage."""

    def enabledAlias(portal_type):
        """True if portal type is enabled for alias in a Collage"""