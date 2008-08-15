Collage
=======

Compatibility
-------------

   Plone 3.1
   Five 1.5

About
-----

Collage is a product for aggregating and displaying multiple content items on
a single page.

It provides the following content-types:

  * Collage
  * Row
  * Column
  * Alias

The first three are structural containers that provide basic layouting
functionality. The premise is that a column fits inside a row which again
fits inside a collage.

The Alias-type is provided to allow displaying existing objects from the site
inside the collage.

Upgrading
---------

Open in ZMI .../your-site/portal_setup and click the "Upgrades" tab.
Select the "Products.Collage:default" profile and see if upgrades are
available. Run them :D

Javascript functionality
------------------------

We use the jquery-library to facilitate easy scripting. Ajax is used to move
content items, columns and rows around without reloading the page.

Status
------

Used in production.

Support for add-on packages
---------------------------

These should be added to the collective.collage package:

* https://svn.plone.org/svn/collective/collective.collage

under ./browser/addons/<package name>

Make sure collective.collage is in your python path if you want these views
registered for use in Collage.

Issue tracker
-------------

http://www.plone.org/products/collage/issues

Credits
-------

* Malthe Borch (main developer) <mborch@gmail.com>
* Pelle Kroegholt <pelle@headnet.dk>
* Sune Toft <sune@headnet.dk>
* Gilles Lenfant <gilles.lenfant@ingeniweb.com>
* David Glick <davidglick@onenw.org>

Sponsors
--------

Work on this product has been sponsored by Headnet (http://www.headnet.dk).
