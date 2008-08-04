# $Id$

def runTypesStepOnly(setuptool):
    """We upgrade our types only"""

    setuptool.runImportStepFromProfile('profile-Products.Collage:default', 'typeinfo',
                                       run_dependencies=True)
    return
