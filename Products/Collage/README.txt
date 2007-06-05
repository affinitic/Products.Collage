Collage
=======

:: compatibility

   Plone 2.5

:: about

Collage is a product for aggregating and displaying multiple content items on
a single page.

It provides the following content-types:

  * Collage
  * Row
  * Column
  * Alias

The Collage and Row-objects are structural containers that allow spreading
content in rows and columns.

To support various use-cases, the Column and Alias types are provided.

Columns extend the functionality of a standard page by providing a field to
select a number of existing items. These items are rendered as a list with
an option to show only a subset of possible fields (title, description etc.)

The Alias type allows displaying an existing item with a view template that
is available for that type.

CMFDynamicViewFTI is used throughout the product to provide options to change
the view templates. This is also integrated in the user interface.

:: Javascript-functionality

We use the jquery-library to facilitate easy scripting. Ajax is used to move
columns and rows without reloading the page.

:: information for integrators and developers

You'll want to customize pagecolumn_default_view.pt to specify correct image scales.
In the default template, no scaling is used; images are loaded with the width set
to 100% so the layout should be preserved at any rate.

:: credits

Malthe Borch <mborch@gmail.com>
Pelle Kroegholt <pelle@headnet.dk>
Sune Toft <sune@headnet.dk>

This product is based on ideas in the PageBuilder product by Max M. Rasmussen.

:: sponsors

Work on this product has been sponsored by Headnet (http://www.headnet.dk).
