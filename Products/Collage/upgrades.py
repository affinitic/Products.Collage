# -*- coding: utf-8 -*-
# $Id$
"""Misc GenericSetup upgrade steps"""

# Warning, the various upgrade handlers here must be coded in
# a defensive way. This means that the changes each handler does
# may have already done. The handler must behave accordingly.

from Products.Collage.utilities import getPortal, IfInstalled


@IfInstalled()
def runTypesStepOnly(setuptool):
    """We upgrade our types only"""

    setuptool.runImportStepFromProfile('profile-Products.Collage:default', 'typeinfo',
                                       run_dependencies=True)
    return


@IfInstalled()
def updateJSRegistry(setuptool):
    """Javascript moved from skins to resources"""

    OLDID = 'collage.js'
    NEWID = '++resource++collage-resources/collage.js'
    jstool = getPortal().portal_javascripts
    all_rscids = jstool.getResourceIds()
    if (OLDID in all_rscids) and (NEWID not in all_rscids):
        jstool.renameResource(OLDID, NEWID)
    return


@IfInstalled()
def removeSkinsLayer(setuptool):
    """Collage doesn't require a CMF skins layer anymore"""

    LAYERNAME = 'Collage'
    skinstool = getPortal().portal_skins
    # Unfortunately, there's no easy way to remove a layer from all skins

    skinnames = skinstool.selections.keys()
    for name in skinnames:
        layers = skinstool.selections[name]
        layers = [l.strip() for l in layers.split(',')
                  if l.strip() != LAYERNAME]
        layers = ','.join(layers)
        skinstool.selections[name] = layers
    if LAYERNAME in skinstool.objectIds():
        skinstool._delObject(LAYERNAME)
    return


@IfInstalled()
def addControlPanel(setuptool):
    """Add Collage control panel resources"""

    for step in ('propertiestool', 'controlpanel', 'action-icons'):
        setuptool.runImportStepFromProfile('profile-Products.Collage:default', step, run_dependencies=False)
    return


@IfInstalled()
def addAliasWhitelistProperty(setuptool):
    """Add Alias whitelist control panel property"""

    propsheet = getPortal().portal_properties.collage_properties
    # Default: same value as types whitelist
    default_value = propsheet.getProperty('types_whitelist')
    propsheet.manage_addProperty('alias_whitelist', default_value, 'lines')
    return
