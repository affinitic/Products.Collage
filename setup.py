# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os


def _textOfModuleFile(filename):
    return open(filename, 'r').read().strip()

setup(
    name='Products.Collage',
    version='1.4.0',
    description=("A product to create page compositions in Plone."),
    long_description='\n\n'.join([
        _textOfModuleFile(name)
        for name in (
            'README.rst',
            os.path.join('docs', 'DEVELOPERS.txt'),
            'CHANGES.rst'
        )
    ]),
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_
    # classifiers
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords='plone layout composition',
    author='Malthe Borch',
    author_email='mborch@gmail.com',
    url='http://www.plone.org/products/collage',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.api',
        'Products.Archetypes',
        'setuptools',
    ],
    extras_require={
        'test': [
            'interlude',
            'ipdb',
            'plone.app.testing',
        ],
    },    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
