# -*- coding: utf-8 -*-
# $Id$
"""Zope 3 style event handlers"""

from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from OFS.interfaces import IObjectWillBeRemovedEvent
from zope.app.container.interfaces import IObjectRemovedEvent
from Products.Archetypes.interfaces import IReferenceable
from Products.CMFCore.interfaces import IContentish
from Products.Collage.interfaces import ICollageAlias
from Products.Collage.interfaces import IDynamicViewManager

@adapter(ICollageAlias, IObjectModifiedEvent)
def updateCollageAliasLayout(context, event):
    """Updating alias layout on alias changed"""

    target = context.get_target()
    if target:
        layout = target.getLayout()
        context.setLayout(layout)

@adapter(IContentish, IObjectModifiedEvent)
def reindexOnModify(content, event):
    """Collage subcontent change triggers Collage reindexing"""

    helper = content.restrictedTraverse('@@collage_helper')
    collage = helper.getCollageObject()
    if collage:
        # Change done in a Collage subobject
        collage.reindexObject()
    return

@adapter(IContentish, IObjectWillBeRemovedEvent)
def resetAliasLayout(content, event):
    """We must reset the layout if the alias target is deleted"""
    if not IReferenceable.providedBy(content):
        return
    aliases = content.getBRefs(relationship='Collage_aliasedItem')
    for alias in enumerate(aliases):
        # Reseting the layout
        manager = IDynamicViewManager(alias)
        manager.setLayout(u'standard')
    return
