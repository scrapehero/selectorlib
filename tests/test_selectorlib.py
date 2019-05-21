#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `selectorlib` package."""

import pytest
import os
import yaml

from click.testing import CliRunner

from selectorlib import selectorlib
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
def input_yaml():
    return read_file_content("input.yml")

@pytest.fixture
def output_yaml():
    return read_file_content("output.yml")


def test_content(html, input_yaml, output_yaml):
    base_url = "https://scrapeme.live/shop/Bulbasaur/"
    selector = selectorlib.Selector.from_yaml_string(input_yaml)
    output = selector.extract(html, base_url=base_url)
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
