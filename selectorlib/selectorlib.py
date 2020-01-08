# -*- coding: utf-8 -*-
import parsel
import yaml
import inspect


def extract_field(element, item_type, attribute=None, formatter=None):
    if item_type == 'Text':
        texts = [i.strip() for i in element.xpath('.//text()').getall() if i.strip()]
        content = " ".join(texts)
    elif item_type == 'Link':
        content = element.xpath('.//@href').get()
    elif item_type == 'HTML':
        content = element.get()
    elif item_type == 'Attribute':
        content = element.attrib.get(attribute)
    elif item_type == 'Image':
        content = element.attrib.get('src')
    if formatter:
        content = formatter.format(content)
    return content


class Extractor:
    """selector class"""
    def __init__(self, config, formatters=None):
        self.config = config
        if formatters:
            formatters = [i() if inspect.isclass(i) else i for i in formatters]
            self.formatters = {i.name: i for i in formatters}
        else:
            self.formatters = {}

    @classmethod
    def from_yaml_string(cls, yaml_string: str, formatters=None):
        """create `Extractor` object from yaml string

        >>> yaml_string = '''
            title:
                css: "h1"
                type: Text
            '''
        >>> extractor = Extractor.from_yaml_string(yaml_string)
        """
        config = yaml.safe_load(yaml_string)
        return cls(config, formatters=formatters)

    @classmethod
    def from_yaml_file(cls, yaml_filename: str, formatters=None):
        """create `Extractor` object from yaml file

        >>> extractor = Extractor.from_yaml_string('selectors.yaml')
        """
        with open(yaml_filename) as yaml_fileobj:
            config = yaml.safe_load(yaml_fileobj.read())
        return cls(config, formatters=formatters)

    def extract(self, html: str, base_url: str = None):
        """
        Args:
            html: html string
            base_url (str, optional): specifying the base_url will make all extracted Links absolute
        Returns:
            dict: extracted data from given html string

        >>> response = requests.get(url)
        >>> extractor.extract(response.text, base_url=response.url)
        """
        sel = parsel.Selector(html, base_url=base_url)
        if base_url:
            sel.root.make_links_absolute()
        fields_data = {}
        for selector_name, selector_config in self.config.items():
            fields_data[selector_name] = self._extract_selector(selector_config, sel)
        return fields_data

    def _extract_selector(self, field_config, parent_parser):
        if field_config.get("xpath") is not None:
            elements = parent_parser.xpath(field_config['xpath'])
        else:
            css = field_config['css']
            if css == '':
                elements = [parent_parser]
            else:
                elements = parent_parser.css(field_config['css'])
        item_type = field_config.get('type', 'Text')
        if not elements:
            return None
        values = []

        for element in elements:
            if 'children' in field_config:
                value = self._get_child_item(field_config, element)
            else:
                kwargs = {'attribute': field_config.get('attribute')}
                if 'attribute' in field_config:
                    kwargs['attribute'] = field_config['attribute']
                if 'format' in field_config:
                    kwargs['formatter'] = self.formatters[field_config['format']]
                value = extract_field(element, item_type, **kwargs)

            if field_config.get('multiple') is not True:
                return value
            else:
                values.append(value)

        return values

    def _get_child_item(self, field_config, element):
        children_config = field_config['children']
        child_item = {}
        for field in children_config:
            child_value = self._extract_selector(children_config[field], element)
            child_item[field] = child_value
        return child_item
