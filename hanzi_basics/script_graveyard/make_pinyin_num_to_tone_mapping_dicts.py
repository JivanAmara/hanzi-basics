# coding='utf8'
""" @brief 
    @author jivan
    @since Nov 19, 2011
"""
from __future__ import unicode_literals, print_function, division
import csv
import os

f = open(os.path.join(os.path.dirname(__file__), 'pinyin_numbers_to_markers.csv'))
csv_reader = csv.reader(f)

pinyin_num_to_tone_marker = dict()
pinyin_tone_marker_to_num = dict()

for row in csv_reader:
    for i, col in enumerate(row):
        col = col.decode('utf-8').strip()
        if i==0:
            key = col
        elif i==1:
            value = col
        
    pinyin_num_to_tone_marker[key] = value
    pinyin_tone_marker_to_num[value] = key

file_base = """# coding='utf-8'
\"\"\" @brief contains a dictionary 'pinyin_nums_to_markers' keying pinyin with
        numerical tones to pinyin with tone markers (utf-8).
    @author jivan
    @since Nov 19, 2011
\"\"\"
from __future__ import unicode_literals, print_function, division
"""

print(file_base)
print("pinyin_num_to_tone_marker = ", end="")
print(pinyin_num_to_tone_marker)
print()
print("pinyin_tone_marker_to_num = ", end="")
print(pinyin_tone_marker_to_num)
