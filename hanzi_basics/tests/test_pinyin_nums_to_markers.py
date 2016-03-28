# -*- coding: utf-8 -*-
"""
Created on Jul 21, 2014

@author: jivan
"""
from __future__ import unicode_literals
from django.test import TestCase

from hanzi_basics.pinyin_nums_to_markers import UnsupportedVowelCombination, \
    replace_untoned_vowel_with_toned


class TestCase_replace_untoned_vowel_with_toned(TestCase):
    def test_replace_untoned_vowel_with_toned(self):
        valid = {
            'a1': 'ā',
            'zha1': 'zhā',
            'ti1': 'tī',
            'ru2': 'rú',
            'ten3': 'těn',
            'do4': 'dò',
            'zhai1': 'zhāi',
            'zhai2': 'zhái',
            'mie3': 'miě',
            'mie4': 'miè',
            'dao1': 'dāo',
            'wei4': 'wèi',
            'nian2': 'nián',
            'xiao4': 'xiào',
            'hou4': 'hòu',
            'kuai4': 'kuài',
            'hui3': 'huǐ',
            'guo2': 'guó',
            'e4': 'è',
            'E4': 'è',
        }
        # Valid syllables not yet supported.
        unsupported = [
        ]

        # Invalid syllables
        invalid = [
            'men',  # No tone mark
            'mn3',  # No vowel
        ]

        for input, expected in valid.items():
            actual = replace_untoned_vowel_with_toned(input)
            self.assertEquals(actual, expected)

        for input in unsupported:
            self.assertRaises(UnsupportedVowelCombination, replace_untoned_vowel_with_toned, input)

        for input in invalid:
            self.assertRaises(ValueError, replace_untoned_vowel_with_toned, input)
