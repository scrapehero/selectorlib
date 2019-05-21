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