#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = [i.strip() for i in requirements_file]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="scrapehero",
    author_email='pypi@scrapehero.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A library to read a YML file with Xpath or CSS Selectors and extract data from HTML pages using them",
    entry_points={
        'console_scripts': [
            'selectorlib=selectorlib.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='selectorlib',
    name='selectorlib',
    packages=find_packages(include=['selectorlib']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/scrapehero/selectorlib',
    version='0.8.0',
    zip_safe=False,
)
