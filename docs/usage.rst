=====
Usage
=====

To use selectorlib in a project::

>>> import selectorlib

>>> html = """
    <h1>Title</h1>
    <h2>Usage
        <a class="headerlink" href="http:://test">¶</a>
    </h2>
    """
>>> yaml_string = """
    title:
        selector: "h1"
        type: Text
    link:
        selector: "h2 a"
        type: Link
    """
>>> selectorlib.extract_with_yaml(html, yaml_string)
{'title': 'Title', 'link': 'http:://test'}

To use selectorlib with requests

>>> import requests
>>> from selectorlib import extract_with_yaml
>>> url = 'https://scrapeme.live/shop/Bulbasaur/'
>>> response = requests.get()
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
>>> extract_with_yaml(response.text, selector_yaml, base_url=response.url)
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
