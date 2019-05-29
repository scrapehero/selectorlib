selectorlib package
===================

Module contents
---------------

.. automodule:: selectorlib
    :members: Extractor



Usage
-----

To use selectorlib with requests:

>>> import requests
>>> from selectorlib import Extractor
>>> selector_yaml = """
name:
    selector: h1.product_title
price:
    selector: p.price
stock:
    selector: p.stock
tags:
    selector: span.tagged_as a
short_description:
    selector: .woocommerce-product-details__short-description > p
description:
    selector: div#tab-description p
attributes:
    selector: table.shop_attributes
    multiple: True
    children:
        name:
            selector: th
        value:
            selector: td
related_products:
    selector: li.product
    multiple: True
    children:
        name:
            selector: h2
        url:
            selector: a[href]
        price:
            selector: .price
"""
>>> extractor = Extractor.from_yaml_string(selector_yaml)
>>> url = 'https://scrapeme.live/shop/Bulbasaur/'
>>> response = requests.get(url)
>>> selector.extract(response.text, base_url=response.url)
{'attributes': [{'name': 'Weight', 'value': '15.2 kg'}],
 'description': 'Bulbasaur can be seen napping in bright sunlight. There is a '
                'seed on its back. By soaking up the sun’s rays, the seed '
                'grows progressively larger.',
 'name': 'Bulbasaur',
 'price': '£ 63.00',
 'related_products': [{'name': 'Pidgeot',
                       'price': '£ 185.00',
                       'url': 'Pidgeot £ 185.00'},
                      {'name': 'Ekans',
                       'price': '£ 55.00',
                       'url': 'Ekans £ 55.00'},
                      {'name': 'Charizard',
                       'price': '£ 156.00',
                       'url': 'Charizard £ 156.00'}],
 'short_description': 'Bulbasaur can be seen napping in bright sunlight. There '
                      'is a seed on its back. By soaking up the sun’s rays, '
                      'the seed grows progressively larger.',
 'stock': '45 in stock',
 'tags': 'bulbasaur'}
