#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `selectorlib` package."""

import pytest
import os
import yaml
import json
from click.testing import CliRunner

from selectorlib import selectorlib
from selectorlib import formatter
from selectorlib import cli


def read_file_content(filename):
    cur_dir = os.path.dirname(__file__)
    with open(os.path.join(cur_dir, "data", filename)) as fileobj:
        content = fileobj.read()
    return content


@pytest.fixture
def html():
    return read_file_content("Bulbasaur-ScrapeMe.html")

@pytest.fixture
def amazon_nike_product_page_output():
    return read_file_content('amazon_nike_product_output.json')

@pytest.fixture
def amazon_nike_product_page_html():
    return read_file_content("amazon_nike_shoes_product.html")

@pytest.fixture
def input_yaml():
    return read_file_content("input.yml")

@pytest.fixture
def empty_selector_yaml():
    return read_file_content("empty_selector_input.yml")

@pytest.fixture
def output_yaml():
    return read_file_content("output.yml")


def test_content(html, input_yaml, output_yaml):
    base_url = "https://scrapeme.live/shop/Bulbasaur/"
    formatters = formatter.Formatter.get_all()
    extractor = selectorlib.Extractor.from_yaml_string(input_yaml, formatters=formatters)
    output = extractor.extract(html, base_url=base_url)
    assert output == yaml.safe_load(output_yaml)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'selectorlib.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

def test_empty_selector_in_children(amazon_nike_product_page_html, empty_selector_yaml, amazon_nike_product_page_output):
    base_url = "https://www.amazon.com/NIKE-Monarch-Cross-Trainer-Regular/dp/B004K4CIKC/ref=sr_1_3?qid=1563864262&refinements=p_89:NIKE&s=apparel&sr=1-3"
    formatters = formatter.Formatter.get_all()
    extractor = selectorlib.Extractor.from_yaml_string(empty_selector_yaml, formatters=formatters)
    output = extractor.extract(amazon_nike_product_page_html, base_url=base_url)
    assert output == json.loads(amazon_nike_product_page_output)
