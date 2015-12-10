# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from plone import api
from Products.Archetypes.ReferenceEngine import Reference
from Products.ATContentTypes.content.base import ATCTContent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.Collage.content.common import LayoutContainer
from Products.Collage.interfaces import ICollageAlias
from Products.Collage.interfaces import IDynamicViewManager
from Products.Collage.utilities import CollageMessageFactory as _
from Products.Collage.utilities import isTranslatable
from zope.interface import implementer

try:
    from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
except ImportError:
    from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
        ReferenceBrowserWidget

try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi


class CollageAliasReference(Reference):
    """We need our own reference class to have a custom target deletion hook
    that resets the alias layout.
    """

    def delHook(self, tool, sourceObject=None, targetObject=None):
        """Override standard delHook
        """
        manager = IDynamicViewManager(sourceObject)
        manager.setLayout(None)
        return


CollageAliasSchema = ATCTContent.schema.copy() + atapi.Schema((
    atapi.ReferenceField(
        name='target',
        mutator='set_target',
        accessor='get_target',
        referenceClass=CollageAliasReference,
        relationship='Collage_aliasedItem',
        multiValued=0,
        allowed_types=(),
        widget=ReferenceBrowserWidget(
            label=_(u'label_alias_target', default="Selected target object"),
            startup_directory='/',
        ),
        keepReferencesOnCopy=True,
    ),
))

# we don't require any fields to be filled out
CollageAliasSchema['title'].required = False

# never show in navigation, also when its selected
CollageAliasSchema['excludeFromNav'].default = True

CollageAliasSchema['relatedItems'].widget.visible = {
    'edit': 'invisible',
    'view': 'invisible'
}


@implementer(ICollageAlias)
class CollageAlias(BrowserDefaultMixin, LayoutContainer, ATCTContent):

    meta_type = 'CollageAlias'

    schema = CollageAliasSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    def indexObject(self):
        pass

    def reindexObject(self, idxs=[]):
        pass

    def unindexObject(self):
        pass

    def get_target(self):
        res = self.getRefs(self.getField('target').relationship)
        if not res:
            if not isTranslatable(self):
                return
            # fall back to canonicals target
            canonical = self.getCanonical()
            res = canonical.getRefs(self.getField('target').relationship)
            if not res:
                return
        res = res[0]
        if isTranslatable(res):
            lt = api.portal.get_tool('portal_languages')
            res = res.getTranslation(lt.getPreferredLanguage()) or res
        return res

atapi.registerType(CollageAlias, 'Collage')
