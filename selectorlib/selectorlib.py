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
    if formatter:
        content = formatter.format(content)
    return content


class Selector:
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
        """create selector object from yaml string"""
        config = yaml.safe_load(yaml_string)
        return cls(config, formatters=formatters)

    @classmethod
    def from_yaml_file(cls, yaml_filename: str, formatters=None):
        """create selector object from yaml file"""
        with open(yaml_filename) as yaml_fileobj:
            config = yaml.safe_load(yaml_fileobj.read())
        return cls(config, formatters=formatters)

    def extract(self, html: str, base_url: str = None):
        """returns extracted dict"""
        sel = parsel.Selector(html, base_url=base_url)
        if base_url:
            sel.root.make_links_absolute()
        fields_data = {}
        for selector_name, selector_config in self.config.items():
            fields_data[selector_name] = self.extract_selector(selector_config, sel)
        return fields_data

    def extract_selector(self, field_config, parent_parser):
        if 'xpath' in field_config:
            elements = parent_parser.xpath(field_config['xpath'])
        else:
            elements = parent_parser.css(field_config['selector'])
        item_type = field_config.get('type', 'Text')
        values = []

        for element in elements:
            if 'children' in field_config:
                value = self.get_child_item(field_config, element)
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

    def get_child_item(self, field_config, element):
        children_config = field_config['children']
        child_item = {}
        for field in children_config:
            child_value = self.extract_selector(children_config[field], element)
            child_item[field] = child_value
        return child_item
