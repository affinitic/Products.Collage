import unittest
from zope.testing import doctest
from Testing.ZopeTestCase import ZopeDocTestSuite
from Products.PloneTestCase import PloneTestCase

PloneTestCase.installProduct('Collage')
PloneTestCase.setupPloneSite(products=['Collage'])

from Products.PloneTestCase import PloneTestCase

optionflags =  (doctest.ELLIPSIS |
                doctest.NORMALIZE_WHITESPACE |
                doctest.REPORT_ONLY_FIRST_FAILURE)

def test_suite():
    return unittest.TestSuite(
        [ZopeDocTestSuite(module,
                          test_class=PloneTestCase.PloneTestCase,
                          optionflags=optionflags)
         for module in []]
        )
