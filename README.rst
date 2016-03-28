============
hanzi-basics
============

Provides basic models:

PinyinSyllable - Stores sound, tone, display string, and verified status
Hanzi - Maps hanzi to their pronunciation via foreign key to PinyinSyllable

After installing and running migrations run django management command
"populate_hanzi_basics" to populate tables.  (Faster than a fixture).


Developers:

Use 'runtests.py' to run tests outside of a django project.
These tests expect the packages in tests/requirements_testing to be installed
in the active python enviornment.
