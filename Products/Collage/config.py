# -*- coding: utf-8 -*-
"""Collage config constants"""
from Products.CMFCore.permissions import setDefaultRoles
import os

PROJECTNAME = "Collage"
I18N_DOMAIN = PROJECTNAME.lower()
PROPERTYSHEETNAME = 'collage_properties'
COLLAGE_TYPES = ('Collage', 'CollageRow', 'CollageColumn', 'CollageAlias')


DEFAULT_ADD_CONTENT_PERMISSION = "Add Collage content"
setDefaultRoles(
    DEFAULT_ADD_CONTENT_PERMISSION,
    ('Manager', 'Owner', 'Site Administrator', 'Contributor')
)

PACKAGE_HOME = os.path.dirname(os.path.abspath(__file__))
del os
