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
    return read_file_content("Amazon.in_listing_page.html")

@pytest.fixture
def input_yaml():
    return read_file_content("input.yml")

@pytest.fixture
def output_yaml():
    return read_file_content("output.yml")


def test_content(html, input_yaml, output_yaml):
    base_url = "https://www.amazon.in/s?bbn=1350387031&rh=n%3A1350387031%2Cp_36%3A-49900\
&pd_rd_r=7946767e-1145-47e3-b524-6645805407f5&pd_rd_w=Ww8Y2&pd_rd_wg=Wpv7t&pf_rd_p=68986\
e27-9447-4ba1-b222-fe7b14a47960&pf_rd_r=5FTG3J2X453KM0HS2CFR&ref=pd_gw_unk"
    output = selectorlib.extract_from_yaml(html, input_yaml, base_url=base_url)
    assert output == yaml.load(output_yaml)


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'selectorlib.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
