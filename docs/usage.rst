Usage
======

Using selectorlib with requests
--------------------------------

>>> import requests
>>> from selectorlib import Extractor
>>> selector_yaml = """
name:
    css: h1.product_title
price:
    css: p.price
stock:
    css: p.stock
tags:
    css: span.tagged_as a
short_description:
    css: .woocommerce-product-details__short-description > p
description:
    css: div#tab-description p
attributes:
    css: table.shop_attributes
    multiple: True
    children:
        name:
            css: th
        value:
            css: td
related_products:
    css: li.product
    multiple: True
    children:
        name:
            css: h2
        url:
            css: a[href]
        price:
            css: .price
"""
>>> extractor = Extractor.from_yaml_string(selector_yaml)
>>> url = 'https://scrapeme.live/shop/Bulbasaur/'
>>> response = requests.get(url)
>>> extractor.extract(response.text, base_url=response.url)
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


Using formatter with selectors
-------------------------------

>>> from selectorlib import Extractor, Formatter
>>> class Number(Formatter):
        def format(self, text):
            return int(text)
>>> yaml_string = """
    title:
        css: "h1"
        type: Text
    num:
        css: "h2 span"
        format: Number
    """
>>> formatters = Formatter.get_all()
>>> extractor = Extractor.from_yaml_string(yaml_string, formatters=formatters)
>>> html = """
    <h1>Title</h1>
    <h2>
        <span>123</span>
    </h2>
    """
>>> extractor.extract(html)
