============
hanzi-basics
============

Provides basic models:

PinyinSyllable - Stores sound, tone, display string, and verified status
Hanzi - Maps hanzi to their pronunciation via foreign key to PinyinSyllable

After installing and running migrations run django management command
"populate_hanzi_basics" to populate tables.  (Faster than a fixture).
