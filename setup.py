# coding='utf-8'
""" @brief distutils setup script for 'hanzi_basics'.
    @author jivan
    @since Jan 18, 2012
"""
from __future__ import unicode_literals, print_function, division
from setuptools import setup, find_packages

setup(
    name='hanzi_basics',
    version='0.2',
    packages=find_packages(),
    # why aren't these found by find_packages?
    scripts=['models.py', 'pinyin_nums_to_markers.py', ],

    author = "Jivan Amara",
    author_email = "Development@JivanAmara.net",
    description = "A couple of models for handling Hanzi and their Pinyin",
#    license = "Undecided",
#    keywords = "hello world example examples",
#    url = "http://unavailable",   # project home page, if any
)
