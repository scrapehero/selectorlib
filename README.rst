===========
selectorlib
===========


.. image:: https://img.shields.io/pypi/v/selectorlib.svg
        :target: https://pypi.python.org/pypi/selectorlib

.. image:: https://img.shields.io/travis/scrapehero/selectorlib.svg
        :target: https://travis-ci.org/scrapehero/selectorlib

.. image:: https://readthedocs.org/projects/selectorlib/badge/?version=latest
        :target: https://selectorlib.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/scrapehero/selectorlib/shield.svg
     :target: https://pyup.io/repos/github/scrapehero/selectorlib/
     :alt: Updates



A library to read a YML file with Xpath or CSS Selectors and extract data from HTML pages using them

* Free software: MIT license
* Documentation: https://selectorlib.readthedocs.io.


Example
--------

>>> from selectorlib import Extractor
>>> yaml_string = """
    title:
        css: "h1"
        type: Text
    link:
        css: "h2 a"
        type: Link
    """
>>> extractor = Extractor.from_yaml_string(yaml_string)
>>> html = """
    <h1>Title</h1>
    <h2>Usage
        <a class="headerlink" href="http://test">¶</a>
    </h2>
    """
>>> extractor.extract(html)
{'title': 'Title', 'link': 'http://test'}
