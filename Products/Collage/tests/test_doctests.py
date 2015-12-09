# -*- coding: utf-8 -*-
"""
Running doctests

Ploneboard functional doctests.  This module collects all *.txt
files in the tests directory and runs them. (stolen from Plone)
"""
from interlude import interact
from plone.testing import layered
from Products.Collage.testing import COLLAGE_INTEGRATION_TESTING
from Products.Collage.testing import HAS_LINGUA_PLONE
import doctest
import pprint
import unittest

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

TESTFILES = [
    ('collage_helper.rst', COLLAGE_INTEGRATION_TESTING),
    ('controlpanel.rst', COLLAGE_INTEGRATION_TESTING),
    ('indexing.rst', COLLAGE_INTEGRATION_TESTING),
    ('kss.rst', COLLAGE_INTEGRATION_TESTING),
    ('orphanaliaslayout.rst', COLLAGE_INTEGRATION_TESTING),
    ('viewlets.rst', COLLAGE_INTEGRATION_TESTING),
]
if HAS_LINGUA_PLONE:
    TESTFILES += [('multilingual_support.rst', COLLAGE_INTEGRATION_TESTING)]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                docfile,
                globs={
                    'pprint': pprint.pprint,
                    'interact': interact,
                },
                optionflags=OPTIONFLAGS,
            ),
            layer=COLLAGE_INTEGRATION_TESTING,
        ) for docfile, layer in TESTFILES
    ])
    return suite
