"""Python API wrapper for the Crawlbase API."""

import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

readme = open('README.md').read()

setup(
    name = 'crawlbase',
    license = 'Apache-2.0',
    version = '3.2.0',
    description = 'A Python class that acts as wrapper for Crawlbase scraping and crawling API',
    long_description = readme,
    long_description_content_type = 'text/markdown',
    author = 'Crawlbase',
    author_email = 'info@crawlbase.com',
    url = 'https://github.com/crawlbase/crawlbase-python',
    keywords = 'scraping scraper crawler crawling crawlbase api',
    include_package_data = True,
    packages = find_packages(),
    classifiers = (
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ),
)
