"""
Running doctests
"""

"""Ploneboard functional doctests.  This module collects all *.txt
files in the tests directory and runs them. (stolen from Plone)
"""

import os, sys

import glob
import doctest
import unittest
from Globals import package_home
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

from Products.Collage.tests.base import CollageFunctionalTestCase

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

def list_doctests():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    return [filename for filename in
            glob.glob(os.path.sep.join([this_dir, '*.txt']))]

def test_suite():
    return unittest.TestSuite(
        [Suite(os.path.basename(filename),
               optionflags=OPTIONFLAGS,
               package='Products.Collage.tests',
               test_class=CollageFunctionalTestCase)
         for filename in list_doctests()]
        )
