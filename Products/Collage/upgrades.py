# $Id$
"""Misc GenericSetup upgrade steps"""

# Warning, the various upgrade handlers here must be coded in
# a defensive way. This means that the changes each handler does
# may have already done. The handler must behave accoringly.


from Products.Collage.utilities import getPortal

def runTypesStepOnly(setuptool):
    """We upgrade our types only"""

    setuptool.runImportStepFromProfile('profile-Products.Collage:default', 'typeinfo',
                                       run_dependencies=True)
    return


def updateJSRegistry(setuptool):
    """Javascript moved from skins to resources"""

    OLDID = 'collage.js'
    NEWID = '++resource++collage-resources/collage.js'
    jstool = getPortal().portal_javascripts
    all_rscids = jstool.getResourceIds()
    if (OLDID in all_rscids) and (NEWID not in all_rscids):
        jstool.renameResource(OLDID, NEWID)
    return


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
