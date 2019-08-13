Selectorlib lets you use a YML styled file to specify the selectors for
the elements or data that you need to extract from a website. You can
use both CSS Selectors, XPaths or both.

YML Structure
-------------

Lets take a look at this fictional store that sells Pokemon -
https://scrapeme.live/shop/

Lets extract Here is a sample YML that SelectorLib accepts as Input

.. code:: yaml

    pokemon:
        css: li.product
        multiple: true
        type: Text
        children:
            name:
                css: h2.woocommerce-loop-product__title
                type: Text
            price:
                css: span.woocommerce-Price-amount
                type: Text
            image:
                css: img.attachment-woocommerce_thumbnail
                type: Attribute
                attribute: src
            url:
                css: a.woocommerce-LoopProduct-link
                type: Link

Here ``pokemon`` is the main element and the elements - name, price,
image and url are inside it and are called the children of the pokemon
element.

Every element starts with its name and can have these properties

-  css
-  xpath
-  type
-  children
-  formatter

css (default: Blank)
~~~~~~~~~~~~~~~~~~~~

The css selector for the element. In our example the element called
pokemon is in an li with a class product. So its ``li.product``.

xpath (default: Blank)
~~~~~~~~~~~~~~~~~~~~~~

The xpath selector for the element. If we were to use xpaths instead of
css selectors for the element pokemon above. It would be
``//li[contains(@class,'pokemon')]``. Every element needs either css or
xpath selectors.

Every element needs either css or xpath selectors. If both xpath and css
are defined, xpath takes preference.

type (default: Text)
~~~~~~~~~~~~~~~~~~~~

The type defines what kind of extraction needs to happen on the selected
element. Here are accepted types

Text
^^^^

This type of extraction just extracts all the text content from the
selected elements. If you have not specifed a type, Text would be used
as default.

Attribute
^^^^^^^^^

This type of extraction lets you extract a particular attribute,
specified using the ``attribute`` property for the element. This is not
usually required when you are selecting using xpaths as you define that
easily in an expression as compared to css selectors. eg.
``//img[@src]``

Here is an example that extracts the src attribute of an img element

.. code:: yaml

    image:
        css: img.attachment-woocommerce_thumbnail
        type: Attribute
        attribute: src

Link
^^^^

This type is a shortcut for getting the href attribute from any links in
the html defined using an ``<a>`` tag

Example,

.. code:: yaml

    url:
        css: a.woocommerce-LoopProduct-link
        type: Link

HTML
^^^^

HTML type, just gives you the full HTML content of the element. This is
useful when you need the html as is for some custom extraction or
checking a few conditions.

multiple (default: False)
~~~~~~~~~~~~~~~~~~~~~~~~~

If you need multiple matches on the selector of an element use multiple
as true. If you only need to get the first match, use multiple as false
or leave it blank. For example, the element pokemon has multiple matches
on the same page, so we have set multiple:true in it to get all of them.

children (default: Blank)
~~~~~~~~~~~~~~~~~~~~~~~~~

An element can have multiple child elements. In the example above the
parent element ``pokemon`` has these "children" -
``name``,\ ``price``,\ ``image``,\ ``url``. Each child element could
also more children and can be nested. If an element has children, it's
``type`` property is ignored.

format
~~~~~~

You can define custom formatters, and can be used for minor
transformations on the extracted data. In Python, these formatters are
defined as

::

    from selectorlib.formatter import Formattter

    class Price(Formattter):
        def format(self, text):
            return text.replace('\\n','').strip()

Used in the YAML as

.. code:: yaml

    price:
        css: span.woocommerce-Price-amount
        type: Text
        format: Price

And passed to the Extractor while its initialized

.. code:: python

    formatters = Formatter.get_all()
    Extractor.from_yaml_file('a.yaml', formatters=formatters)

Python Example
--------------

``scrapeme_listing_page.yml``

.. code:: yaml

    pokemon:
        css: li.product
        multiple: true
        type: Text
        children:
            name:
                css: h2.woocommerce-loop-product__title
                type: Text
            price:
                css: span.woocommerce-Price-amount
                type: Text
            image:
                css: img.attachment-woocommerce_thumbnail
                type: Attribute
                attribute: src
            url:
                css: a.woocommerce-LoopProduct-link
                type: Link

``extract.py``

.. code:: python

    import requests 
    from selectorlib import Extractor, Formatter
    from pprint import pprint
    import re 

    # Define a formatter for Price 
    class Price(Formatter):
        def format(self, text):
            price = re.findall(r'\d+\.\d+',text)
            if price:
                return price[0]
            return None
    formatters = Formatter.get_all()
    extractor = Extractor.from_yaml_file('./scrapeme_listing_page.yml',formatters=formatters)

    #Download the HTML and use Extractor 
    r = requests.get('https://scrapeme.live/shop/')
    data = extractor.extract(r.text)
    pprint(data)

::

    >>> python extract.py

::

    {'pokemon': [{'image': 'https://scrapeme.live/wp-content/uploads/2018/08/001-350x350.png',
                  'name': 'Bulbasaur',
                  'price': '63.00',
                  'url': 'https://scrapeme.live/shop/Bulbasaur/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/002-350x350.png',
                  'name': 'Ivysaur',
                  'price': '87.00',
                  'url': 'https://scrapeme.live/shop/Ivysaur/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/003-350x350.png',
                  'name': 'Venusaur',
                  'price': '105.00',
                  'url': 'https://scrapeme.live/shop/Venusaur/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/004-350x350.png',
                  'name': 'Charmander',
                  'price': '48.00',
                  'url': 'https://scrapeme.live/shop/Charmander/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/005-350x350.png',
                  'name': 'Charmeleon',
                  'price': '165.00',
                  'url': 'https://scrapeme.live/shop/Charmeleon/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/006-350x350.png',
                  'name': 'Charizard',
                  'price': '156.00',
                  'url': 'https://scrapeme.live/shop/Charizard/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/007-350x350.png',
                  'name': 'Squirtle',
                  'price': '130.00',
                  'url': 'https://scrapeme.live/shop/Squirtle/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/008-350x350.png',
                  'name': 'Wartortle',
                  'price': '123.00',
                  'url': 'https://scrapeme.live/shop/Wartortle/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/009-350x350.png',
                  'name': 'Blastoise',
                  'price': '76.00',
                  'url': 'https://scrapeme.live/shop/Blastoise/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/010-350x350.png',
                  'name': 'Caterpie',
                  'price': '73.00',
                  'url': 'https://scrapeme.live/shop/Caterpie/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/011-350x350.png',
                  'name': 'Metapod',
                  'price': '148.00',
                  'url': 'https://scrapeme.live/shop/Kakuna/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/015-350x350.png',
                  'name': 'Beedrill',
                  'price': '168.00',
                  'url': 'https://scrapeme.live/shop/Beedrill/'},
                 {'image': 'https://scrapeme.live/wp-content/uploads/2018/08/016-350x350.png',
                  'name': 'Pidgey',
                  'price': '159.00',
                  'url': 'https://scrapeme.live/shop/Pidgey/'}]}

