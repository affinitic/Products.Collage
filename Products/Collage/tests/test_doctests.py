# -*- coding: utf-8 -*-
"""
Running doctests

Ploneboard functional doctests.  This module collects all *.txt
files in the tests directory and runs them. (stolen from Plone)
"""
from Products.ATContentTypes.config import HAS_LINGUA_PLONE
from Products.Collage.tests.base import CollageFunctionalTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite
import doctest
import unittest


OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

doc_tests = [
    'collage_helper.rst',
    'controlpanel.rst',
    'indexing.rst',
    'kss.rst',
    'orphanaliaslayout.rst',
    'viewlets.rst',
]
if HAS_LINGUA_PLONE:
    doc_tests += 'multilingual_support.rst'


def test_suite():
    return unittest.TestSuite(
        [
            Suite(
                filename,
                optionflags=OPTIONFLAGS,
                package='Products.Collage.tests',
                test_class=CollageFunctionalTestCase
            )
            for filename in doc_tests
        ]
    )
