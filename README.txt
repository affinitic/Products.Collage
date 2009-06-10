Collage
=======

Compatibility
-------------

* Plone 3.1-3.3
* Five 1.5

About
-----

Collage is a product for aggregating and displaying multiple content items on a
single page.

It provides the following content-types:

  * Collage
  * Row
  * Column
  * Alias

The first three are structural containers that provide basic layouting
functionality. The premise is that a column fits inside a row which again fits
inside a collage.

The Alias-type is provided to allow displaying existing objects from the site
inside the collage.

Upgrading
---------

If you upgraded Products.Collage in the file system, open in ZMI
/your/plone/site/portal_setup and click the "Upgrades" tab.

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

Support for third party content types are available with your subversion
client from https://svn.plone.org/svn/collective/Products.Collage/addons/

See DEVELOPER.txt to add support for custom content types and themings.

Issue tracker
-------------

http://www.plone.org/products/collage/issues

Credits
-------

Development:

* `Malthe Borch (main developer) <mborch@gmail.com>`_
* `David Glick <davidglick@onenw.org>`_
* `Pelle Kroegholt <pelle@headnet.dk>`_
* `Gilles Lenfant <gilles.lenfant@gmail.com>`_
* `Sune Toft <sune@headnet.dk>`_
* `Jens Klein <jens@bluedynamics.com>`_

Translations:

* Bulgarian (bg): `Vladimir Iliev <vladimir.iliev@gmail.com>`_
* Danish (da): `Jacob Vestergaard <jacobv@headnet.dk>`_
* German (de): `Roland Fasching <rof@sterngasse.at>`_, `Jens Klein <jens@bluedynamics.com>`_
* English (en): `Kevin Deldycke <kevin@deldycke.com>`_
* Spanish (es): `Mikel Larreategi <mlarreategi@codesyntax.com>`_
* Basque (eu): `Mikel Larreategi <mlarreategi@codesyntax.com>`_
* French (fr): `Kevin Deldycke <kevin@deldycke.com>`_
* Italian (it): `Yuri Carrer <yurj@alfa.it>`_
* Brazilian Portuguese (pt-br): `Danilo G. Botelho <danilogbotelho@yahoo.com>`_
* Catalan (ca): `Pilar Marinas <pilar.marinas@upcnet.es>`_
* Portuguese (pt): `Ricardo Alves <rsa@eurotux.com>`_
* Dutch (nl): `Reinout van Rees <reinout@vanrees.org>`_

Sponsors
--------

Work on this product has been sponsored by Headnet (http://www.headnet.dk) and
EDF (http://www.edf.fr)
