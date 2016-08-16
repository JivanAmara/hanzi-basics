import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    author="Jivan Amara",
    author_email="Development@JivanAmara.net",
    license="Undecided",
    name="hanzi-basics",
    version="1.1.2",
    packages=['hanzi_basics', 'hanzi_basics.migrations',
              'hanzi_basics.management',
              'hanzi_basics.management.commands'
    ],
    package_data={
        'hanzi_basics': [
            'management/commands/hanzi_frequency.html',
            'management/commands/hanzi_frequency_files/school.css',
        ],
    },
    description='Python package to provide basic models for Chinese language processing',
    long_description=README,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
    ]
)

