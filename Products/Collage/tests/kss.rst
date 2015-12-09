KSS support
===========

  >>> helper = layer['portal']['folder'].restrictedTraverse('@@collage_kss_helper')

We use the UID provided by Archetypes as unique identifier:

  >>> helper.getUniqueIdentifier() == layer['portal']['folder'].UID()
  True
