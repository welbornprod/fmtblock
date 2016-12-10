#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FormatBlock Setup

-Christopher Welborn 12-09-2016
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Try using the latest DESC.txt.
shortdesc = ' '.join((
    'Format blocks of characters for display,',
    'split by words, characters, or newlines.',
))
try:
    with open('DESC.txt', 'r') as f:
        shortdesc = f.read()
except FileNotFoundError:
    pass

# Default README files to use for the longdesc, if pypandoc fails.
readmefiles = ('docs/README.txt', 'README.txt', 'docs/README.rst')
for readmefile in readmefiles:
    try:
        with open(readmefile, 'r') as f:
            # Use previously converted README.
            longdesc = f.read()
        break
    except EnvironmentError:
        # File not found or failed to read.
        pass
else:
    # No readme file found.
    # If a README.md exists, and pypandoc is installed, generate a new readme.
    try:
        import pypandoc
    except ImportError:
        print('Pypandoc not installed, using default description.')
        longdesc = shortdesc
    else:
        # Convert using pypandoc.
        try:
            longdesc = pypandoc.convert('README.md', 'rst')
        except EnvironmentError:
            # No readme file, no fresh conversion.
            print('Pypandoc readme conversion failed, using default desc.')
            longdesc = shortdesc

setup(
    name='FormatBlock',
    version='0.3.5',
    author='Christopher Welborn',
    author_email='cj@welbornprod.com',
    packages=['fmtblock'],
    url='https://github.com/welbornprod/fmtblock',
    description=shortdesc,
    long_description=longdesc,
    keywords=('python module library 3 format block characters chars text'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'docopt',
        'colr >= 0.5.1',
    ],
    entry_points={
        'console_scripts': [
            'fmtblock = fmtblock.__main__:main',
        ]
    }
)
