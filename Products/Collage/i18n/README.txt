Translations for Collage
========================

The updatei18n.py script rebuilds the collage.pot file and synchronizes the .po
files.

Requirements
------------

Of course, we assume that you know basics about Plone internationalisation and
localisation, as well as the gettext standard (.po files, ...) otherwise, ask
Google.

You need i18ndude (from the cheeseshop) to run this script. As
installing i18ndude makes a huge mess in the standard Python
"site-packages" that may conflict with the Zope bundle, it is strongly
recommanded to install i18ndude in a dedicated virtualenv::

  $ easy_install virtualenv
    ...
  $ cd /where/you/want
  $ virtualenv --no-site-packages i18ndude
  $ cd i18ndude
  $ . bin/activate
  (i18ndude)$ easy_install i18ndude
    ...

You're done. In the future, you'll need to activate that virtualenv
before running i18ndude or updatei18n.py. After you're done, you might
run::

  $ deactivate

...to leave the virtual Python environment for i18ndude

Updating the catalogs
---------------------

After changing translatable labels in Python code or templates, you may need to
run::

  $ . /where/you/want/i18ndude/bin/activate
  (i18ndude)$ cd .../Products.Collage/Products/Collage/i18n # Here ;)
  (i18ndude)$ python updatei18n.py

If some msgids are missing from the synched ".po" files, you may need to add
these msgid to "collage-manual.pot" (for 'collage' domain). Then re-run the
above commands.

After commiting your changes, please notify the translators of Collage of the
changes you made and checked in (see the "Credits" section of the main
README.txt).

If you added a new translation language to Collage, please add your
language/name/mail in the "Credits" section of the main README.txt.

More information
----------------

* http://pypi.python.org/pypi/virtualenv
* http://pypi.python.org/pypi/i18ndude
