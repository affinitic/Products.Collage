from setuptools import setup, find_packages
import os

version = '1.2b3'

setup(name='Products.Collage',
      version=version,
      description="A product to create page compositions in Plone. Content can be created directly inside the object or existing items can be pulled in for display.",
      long_description=open(os.path.join('Products', 'Collage', "README.txt")).read() + "\n" +
                       open(os.path.join('Products', 'Collage', "DEVELOPERS.txt")).read() + "\n" +
                       open(os.path.join('Products', 'Collage', "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Development Status :: 5 - Production/Stable",
        ],
      keywords='plone layout composition themeing',
      author='Malthe Borch',
      author_email='mborch@gmail.com',
      url='http://www.plone.org/products/collage',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
