#coding=utf-8
""" @brief Scrapes the descending frequency hanzi list from 
        http://www.zein.se/patrick/3000char.html
    @author jivan
    @since Sep 4, 2011
"""
from __future__ import unicode_literals, print_function, division
from collections import defaultdict
from tonerecorder.models import Hanzi, PinyinSyllable
import codecs
import os
import re
import sys

def check_args(argc, argv):
    usage = "{} <filename>".format(argv[0])
    ok = True
    
    if argc != 2 or not os.path.exists(argv[1]):
        ok = False

    if not ok:
        print(usage)
        exit(1)
        
def main(argc, argv):
    check_args(argc, argv)

    filename = argv[1]
    html_file = codecs.open(filename, 'r', 'utf-8')
    
    html = html_file.read()
    
    # --- Remove the content except for the table rows.
    preceding = re.compile(r'<b>Pronunciations and explanations</b></td></tr>')
    following = re.compile(r'<tr></tr></tbody></table></blockquote></body></html>')
    pm = preceding.search(html)
    fm = following.search(html)
    table_rows = html[pm.end():fm.start()]

    # --- Collect the raw html content of each row.
    rowpattern = re.compile(r'\s*<tr>(?P<row>.*?)</tr>', re.DOTALL)
    
    rows = list()
    rowiter = rowpattern.finditer(table_rows)
    for rowmatch in rowiter:
        rows.append(rowmatch.group('row'))
    
    # --- Collect the raw html content of each column
    colpattern = re.compile(
                     '''
                         <td.*?>(?P<rank>.*?)</td>        # Get frequency rank
                         <td.*?>(?P<hanzi>.*?)</td>       # Get hanzi
                         <td.*?>(?P<details>.*?)</td>     # Get Details
                     '''
                     , re.VERBOSE | re.DOTALL
                 )

    pinyin_set = set()
    all_pinyin = ""
    hanzi_sounds = defaultdict(list)

    for row in rows:
        m = colpattern.search(row)
        if m is None:
            print("Pattern failed for:\n{}".format(row))
        else:
            rankcol = m.group('rank')
            # No cleanup needed for rank
            rank = rankcol
            
            # The hanzi is wrapped with a <font> tag.
            hanzicol = m.group('hanzi')
            hanzimatch = re.search(r'<font.*?>(?P<char>.*?)</font>', hanzicol)
            hanzi = hanzimatch.group('char')

            # --- Add hanzi to database
            # Add the hanzi itself.
            nh = Hanzi.get_or_create(char=hanzi, use_rank=rank)
            
            # Get the pinyin for the char from the details column
            detailscol = m.group('details')
            pinyinmatches = re.finditer(r'\[(.*?)\]', detailscol)
            pinyin = [ pm.group(1) for pm in pinyinmatches]
            for p in pinyin:
                # Use all lowercase
                p=p.lower()
                # If alternatives are presented, only take the first
                if '/' in p:
                    p = p[:p.index('/')]
                pinyin_set.add(p)
                sound, tone = sound_and_tone(p)
                if len(sound) == 2 and sound[1] == 'g':
                    print
                    print("{} {} {} {}".format(p, sound, tone, row))
                    print
                    
                syllable = PinyinSyllable.get_or_create(sound, tone)
                
                nh.syllables.add(syllable)

            nh.save()
            print("{}".format(hanzi), end="")
            sys.stdout.flush()

            pinyin_string = ' '.join(pinyin)

            all_pinyin = ' '.join([all_pinyin, pinyin_string])

    print()

#            print("{} {} {}".format(rank, hanzi, pinyin_string).encode('utf-8'))
#        
#    print("Count of pinyin sounds: {}".format(len(pinyin_set)).encode('utf-8'))
#    print("{}".format(all_pinyin).encode('utf-8'))
        
def sound_and_tone(syllable):
    """ @brief Takes pinyin syllables with a tone indicator, like 'dí', and returns
            a 2-tuple of the sound and tone, like ('di', 2).
    """
    # List of 3-tuples containing (<marked_letter>, <int_tone>, <unmarked_letter>
    #    marked_letter is the letter with the tone marking
    #    int_tone is the integer representation of the tone
    #    unmarked_letter is the letter without a tone marking
    tone_replacement = [
        ('ā', 1, 'a'),
        ('á', 2, 'a'),
        ('ǎ', 3, 'a'),
        ('à', 4, 'a'),
        ('ē', 1, 'e'),
        ('é', 2, 'e'),
        ('ě', 3, 'e'),
        ('è', 4, 'e'),
        ('ī', 1, 'i'),
        ('í', 2, 'i'),
        ('ǐ', 3, 'i'),
        ('ì', 4, 'i'),
        ('ō', 1, 'o'),
        ('ó', 2, 'o'),
        ('ǒ', 3, 'o'),
        ('ò', 4, 'o'),
        ('ū', 1, 'u'),
        ('ú', 2, 'u'),
        ('ǔ', 3, 'u'),
        ('ù', 4, 'u'),
        ('ǚ', 3, 'ü'),
        ('ǜ', 4, 'ü'),
    ]
    
    found = False

    for repl in tone_replacement:
        if repl[0] in syllable:
            sound = syllable.replace(repl[0], repl[2])
            tone = repl[1]
            found = True
            break

    if not found:
        sound = syllable
        tone = 5
    
    return (sound, tone)

if __name__=='__main__':
    argc = len(sys.argv)
    main(argc, sys.argv)
