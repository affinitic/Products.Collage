# $Id$
"""Misc utilities"""

import re

isNumber = re.compile(r"^\d+$")

def findFirstAvailableInteger(ids):
    i = 1
    while True:
        if str(i) not in ids:
            return i
        i += 1

def generateNewId(container):
    parent_contents = container.objectValues()
    contentIDs = map(lambda x: x.getId(), parent_contents)
    numericalIDs = filter(isNumber.match, contentIDs)
    return str(findFirstAvailableInteger(numericalIDs))

###
## i18ndude helper
###

# FIXME: It seems we could use directly a real MessageFactory object.
# as in ATCT schemas.

def faketranslate(text, default=""):
    """A fake translator to be used in AT schemas as i18ndude marker like this
    from Products.Collage.utils import faketranslate as _
    ...
    widget = FooWidget('foo', label_msgid=_('label_foo', default="Foo"), ...)
    """
    return text

###
## Detects translatable objects when LP installed
###

# FIXME: Should we check that LP is installed in this site too ?
try:
    from Products.LinguaPlone.interfaces import ITranslatable
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

def isTranslatable(content):
    if HAS_LINGUAPLONE:
        return ITranslatable.providedBy(content)
    return False

###
## Logging utility
###

from Products.Collage.config import PROJECTNAME
import logging
logger = logging.getLogger(PROJECTNAME)

###
## Get the portal object without context/request
###

from zope.component import getUtility
from Products.CMFCore.interfaces import ISiteRoot

def getPortal():
    return getUtility(ISiteRoot)

###
## Our i18n message factory
###

from zope.i18nmessageid import MessageFactory
from Products.Collage.config import I18N_DOMAIN

CollageMessageFactory = MessageFactory(I18N_DOMAIN)


