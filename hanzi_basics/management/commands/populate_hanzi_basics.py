# encoding=utf-8
'''
Created on Mar 18, 2016

@author: jivan
'''
from __future__ import print_function

from _collections import defaultdict
import encodings
import re, os
import sys

from django.core.management import BaseCommand
from django.db import transaction

from hanzi_basics.models import PinyinSyllable, Hanzi
from hanzi_basics.pinyin_nums_to_markers import num_to_tone, UnsupportedVowelCombination


class Command(BaseCommand):
    # Show this when the user types help
    help = "Populate the tables of hanzi-basics"

    # A command must define handle()
    def handle(self, *args, **options):
        populate()


def populate():
    """
        The file 'hanzi_frequency.html' was downloaded from:
            http://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO
        on 2016-03-18.
    """
    file_dir = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))
    file_path = os.path.join(file_dir, 'hanzi_frequency.html')
    with open(file_path) as freq_file:
        freq_html = freq_file.read()

    # Drop all of the html outside the <pre> tags
    just_data_regex = r'.*<pre>(.*)</pre>'
    just_data_match = re.search(just_data_regex, freq_html)
    just_data_html = just_data_match.groups()[0]
    # Split each line into a single list entry
    line_regex = r'(.*?)<br>'
    matches = re.findall(line_regex, just_data_html)
    # Number of top characters to index
    include_linecount = 6000

    # --- These two need to be dictionaries so duplication can be detected using the string
    #    The objects can't be hashed until they have a primary key (after they're saved).
    # new PinyinSyllable objects
    pinyin_syllables_by_string = {}
    # new Hanzi objects
    hanzis_by_string = {}

    # Pinyin string list keyed by Hanzi string (Ex: {'土': ['tu3']})
    #    The Pinyin strings are the pronunciations of the Hanzi.
    pinyins_for_hanzi = defaultdict(list)

    # List of pinyin strings that couldn't be converted to tone representations for display.
    no_display_text = []

    for i, line in enumerate(matches, 1):
        if i > include_linecount: break
        line_parse_regex = r'(\d+)\s+(.+?)\s+(.*?)\s+([\d.]+)\s+([\w/]+)'
        line_data_match = re.match(line_parse_regex, line)
        if not line_data_match:
            print("Regex doesn't match:\n{}\n{}\n{}".format(matches[i - 2], line, matches[i]))
        else:
            # rank, hanzi, frequency, percentile, pinyin pronunciation separated by '/'
            rank, hanzi_string_gbk, freq, perc, pronunciation_string_gbk = line_data_match.groups()
            pronunciation_string_utf8 = pronunciation_string_gbk.decode('gbk').encode('utf-8')
            hanzi_string_utf8 = hanzi_string_gbk.decode('gbk').encode('utf-8')

            if hanzi_string_utf8 not in hanzis_by_string:
                h = Hanzi(char=hanzi_string_utf8, use_count=freq)
                hanzis_by_string[hanzi_string_utf8] = h
            pinyin_strings = pronunciation_string_utf8.split('/')
            for pstring in pinyin_strings:
                # Use tone number 5 for syllables with no tone.
                tone = pstring[-1] if pstring[-1] in '1234' else 5
                sound = pstring[:-1] if tone != 5 else pstring
                # Set the display text as a syllable with tone marker
                #    as opposed to sound-tonenum format.
                display_text = num_to_tone('{}{}'.format(sound, tone))
                if display_text == '{}{}'.format(sound, tone):
                    no_display_text.append('{}{}'.format(sound, tone))
                    display_text = '{}{}'.format(sound, tone)

                ps = PinyinSyllable(sound=sound, tone=tone, display=display_text)
                if '{}{}'.format(sound, tone) not in pinyin_syllables_by_string:
                    pinyin_syllables_by_string['{}{}'.format(sound, tone)] = ps
                pinyins_for_hanzi[hanzi_string_utf8].append('{}{}'.format(sound, tone))
                print('.', end='')
    print()

    print('Creating model instances for new data:')
    print(' PinyinSyllable')
    PinyinSyllable.objects.bulk_create(pinyin_syllables_by_string.values())
    pinyin_syllables_by_string = {}
    for ps in PinyinSyllable.objects.all():
        pinyin_syllables_by_string['{}{}'.format(ps.sound, ps.tone)] = ps

    print(' Hanzi')
    Hanzi.objects.bulk_create(hanzis_by_string.values())
    hanzis_by_string = {}
    for hanzi in Hanzi.objects.all():
        hanzis_by_string[hanzi.char.encode('utf-8')] = hanzi

    print(' Connecting Hanzi to pronunciation as PinyinSyllable')
    with transaction.atomic():
        for hanzi_string, pinyin_strings in pinyins_for_hanzi.items():
            hanzi = hanzis_by_string[hanzi_string]
            print('{}'.format(hanzi_string), end='')
            sys.stdout.flush()
            pinyins = [pinyin_syllables_by_string[ps] for ps in pinyin_strings]
            hanzi.syllables.add(*pinyins)

    print('Syllables without tone marker representation (This should be empty):')
    print(no_display_text)
