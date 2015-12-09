# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.utils import versionTupleFromString
from Products.Collage.config import I18N_DOMAIN
from Products.Collage.config import PACKAGE_HOME
from Products.Collage.config import PROJECTNAME
from Products.Collage.interfaces import ICollageSiteOptions
from zope.component import getAdapter
from zope.i18nmessageid import MessageFactory
import logging
import re
import warnings

try:
    from Products.LinguaPlone.interfaces import ITranslatable
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

logger = logging.getLogger(PROJECTNAME)
CollageMessageFactory = MessageFactory(I18N_DOMAIN)


def findFirstAvailableInteger(ids):
    i = 1
    while True:
        if str(i) not in ids:
            return i
        i += 1


_isNumber = re.compile(r"^\d+$")


def generateNewId(container):
    parent_contents = container.objectValues()
    contentIDs = map(lambda x: x.getId(), parent_contents)
    numericalIDs = filter(_isNumber.match, contentIDs)
    return str(findFirstAvailableInteger(numericalIDs))


def isTranslatable(content):
    """Detects translatable objects when LP installed"""
    # FIXME: Should we check that LP is installed in this site too ?
    if HAS_LINGUAPLONE:
        return ITranslatable.providedBy(content)


def getPortal():
    """Get the portal object without context/request"""
    warnings.warn(
        "getPortal is deprecated, use plone.api.portal.get instead",
        DeprecationWarning
    )
    return api.portal.get()


def getCollageSiteOptions():
    """Collage site options from contol panel"""
    return getAdapter(api.portal.get(), ICollageSiteOptions)


def getFSVersionTuple():
    """Reads version.txt and returns version tuple"""
    vfile = "%s/version.txt" % PACKAGE_HOME
    v_str = open(vfile, 'r').read().lower().strip()
    return versionTupleFromString(v_str)

###
# Upgrade steps decorator
###

# Background: GenericSetup shows upgrade steps for components that are
# *not* installed in the site, and let the Manager execute these
# upgrade steps. This is somehow harmful. While this bug is not fixed,
# this safety belt will prevent managers executing the exposed upgrade
# steps.
# See https://dev.plone.org/plone/ticket/8507
# Usage:
#
#  @IfInstalled('Collage')
#  def someUpgradeScript(setuptool):
#      # Usual upgrade script


class NotInstalledComponent(LookupError):

    def __init__(self, cpt_name):
        self.cpt_name = cpt_name
        return

    def __str__(self):
        msg = ("Component '%s' is not installed in this site."
               " You can't run its upgrade steps."
               % self.cpt_name)
        return msg


class IfInstalled(object):

    def __init__(self, prod_name=PROJECTNAME):
        """@param prod_name: as shown in quick installer"""
        self.prod_name = prod_name

    def __call__(self, func):
        """@param func: the decorated function"""
        def wrapper(setuptool):
            qi = getPortal().portal_quickinstaller
            installed_ids = [p['id'] for p in qi.listInstalledProducts()]
            if self.prod_name not in installed_ids:
                raise NotInstalledComponent(self.prod_name)
            return func(setuptool)
        wrapper.__name__ = func.__name__
        wrapper.__dict__.update(func.__dict__)
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        return wrapper
