# -*- coding: utf-8 -*-
from config import DEFAULT_ADD_CONTENT_PERMISSION
from config import PROJECTNAME
from Products.Archetypes.atapi import listTypes
from Products.Archetypes.atapi import process_types

GLOBALS = globals()


def initialize(context):
    from Products.Collage import content
    from Products.CMFCore import utils as cmfutils

    content  # Keep pyflakes silent
    # initialize the content, including types and add permissions
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit('%s Content' % PROJECTNAME,
                         content_types=content_types,
                         permission=DEFAULT_ADD_CONTENT_PERMISSION,
                         extra_constructors=constructors,
                         fti=ftis,
                         ).initialize(context)
