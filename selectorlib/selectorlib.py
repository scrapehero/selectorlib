# -*- coding: utf-8 -*-
import parsel
import yaml


def extract_field(element, item_type, attribute=None):
    if item_type == 'Text':
        texts = [i.strip() for i in element.xpath('.//text()').getall() if i.strip()]
        content = " ".join(texts)
    elif item_type == 'Link':
        content = element.xpath('.//@href').get()
    elif item_type == 'HTML':
        content = element.get()
    elif item_type == 'Attribute':
        content = element.attrib.get(attribute)
    return content


def get_child_item(field_config, element):
    children_config = field_config['children']
    child_item = {}
    for field in children_config:
        child_value = extract_selector(children_config[field], element)
        child_item[field] = child_value
    return child_item


def extract_selector(field_config, parent_parser):
    if 'xpath' in field_config:
        elements = parent_parser.xpath(field_config['xpath'])
    else:
        elements = parent_parser.css(field_config['selector'])
    item_type = field_config.get('type', 'Text')
    values = []

    for element in elements:
        if 'children' in field_config:
            value = get_child_item(field_config, element)
        else:
            value = extract_field(element, item_type,
                                  field_config.get('attribute'))

        if field_config.get('multiple') is not True:
            return value
        else:
            values.append(value)

    return values


def extract(html, config, base_url=None):
    sel = parsel.Selector(html, base_url=base_url)
    if base_url:
        sel.root.make_links_absolute()
    fields_data = {}
    for selector_name in config:
        fields_data[selector_name] = extract_selector(config[selector_name], sel)
    return fields_data


def extract_with_yaml(html, yaml_string, **kwargs):
    config = yaml.safe_load(yaml_string)
    return extract(html, config, **kwargs)
