#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" format_block.py
    ...Formats long text into terminal-friendly blocks of text.
    Christopher Welborn 02-03-2015
"""

from docopt import docopt
import os
import sys

NAME = 'Format Block'
VERSION = '0.1.1'
VERSIONSTR = '{} v. {}'.format(NAME, VERSION)
SCRIPT = os.path.split(os.path.abspath(sys.argv[0]))[1]
SCRIPTDIR = os.path.abspath(sys.path[0])

# Maximum width for lines, unless -w is used.
DEFAULT_WIDTH = 79

USAGESTR = """{versionstr}
    Usage:
        {script} -h | -v
        {script} [WORDS...] [-c] [-i num] [-n] [-s] [-w num]

    Options:
        WORDS                : Words to format into a block.
                               File names can be passed to read from a file.
                               If not given, stdin is used instead.
        -c,--chars           : Wrap on characters instead of spaces.
        -h,--help            : Show this help message.
        -i num,--indent num  : Indention level.
                               Default: 0
        -n,--newlines        : Preserve newlines.
        -v,--version         : Show version.
        -w num,--width num   : Maximum width for the block.
                               Default: {defaultwidth}
""".format(
    script=SCRIPT,
    versionstr=VERSIONSTR,
    defaultwidth=DEFAULT_WIDTH)


def main(argd):
    """ Main entry point, expects doctopt arg dict as argd. """
    width = parse_int(argd['--width'] or DEFAULT_WIDTH)
    indent = parse_int(argd['--indent'] or 0)
    prepend = ' ' * (indent * 4)

    if argd['WORDS']:
        # Try each argument as a file name.
        argd['WORDS'] = (
            (try_read_file(w) if len(w) < 256 else w)
            for w in argd['WORDS']
        )
        words = ' '.join((w for w in argd['WORDS'] if w))
    else:
        words = read_stdin()

    if len(words) < 256:
        words = try_read_file(words)
        if words is None:
            return 1

    print('\n{}'.format(
        format_block(
            words,
            chars=argd['--chars'],
            prepend=prepend,
            blocksize=width,
            newlines=argd['--newlines']
        )
    ))

    return 0


def format_block(
        text,
        prepend=None, lstrip=False, blocksize=60,
        chars=False, newlines=False):
    """ Format a long string into a block of newline seperated text. """
    iterlines = make_block(
        text,
        blocksize=blocksize,
        chars=chars,
        newlines=newlines)
    if prepend is None:
        return '\n'.join(iterlines)
    if lstrip:
        # Add 'prepend' before each line, except the first.
        return '\n{}'.format(prepend).join(iterlines)
    # Add 'prepend' before each line.
    return '{}{}'.format(prepend, '\n{}'.format(prepend).join(iterlines))

# TODO: Possible `iter_format_block`, which would allow:
#       for line in iter_format_block(s):
#           f.write(line)


def make_block(text, blocksize=60, chars=False, newlines=False):
    """ Iterator that turns a long string into lines no greater than
        'blocksize' in length.
        This can wrap on spaces, instead of characters if 'chars' is falsey.

        Arguments:
            text       : String to format.
            blocksize  : Maximum width for each line.
                         Default: 60
            chars      : Wrap on characters if true, otherwise on spaces.
                         Default: False
            newlines   : Preserve newlines when True.
                         Default: False
    """
    if chars and (not newlines):
        # Simple block by chars, newlines are treated as a space.
        text = ' '.join(text.splitlines())
        yield from (
            text[i:i + blocksize] for i in range(0, len(text), blocksize)
        )
    elif newlines:
        # Preserve newlines
        for line in text.splitlines():
            yield from make_block(line, blocksize=blocksize, chars=chars)
    else:
        # Wrap on spaces (ignores newlines)..
        # lines = []
        curline = ''
        for word in text.split():
            possibleline = ' '.join((curline, word)) if curline else word

            if len(possibleline) > blocksize:
                yield curline
                curline = word
            else:
                curline = possibleline
        if curline:
            yield curline


def parse_int(s):
    """ Parse a string into an integer.
        Exit with a message on failure.
    """
    try:
        val = int(s)
    except ValueError:
        print('\nInvalid integer: {}'.format(s))
        sys.exit(1)
    return val


def read_stdin():
    """ Read from stdin, but print a helpful message if it's a tty. """
    if sys.stdin.isatty():
        print('\nReading from stdin until EOF (Ctrl + D)\n')
    return sys.stdin.read()


def try_read_file(s):
    """ If `s` is a file name, read the file and return it's content.
        Otherwise, return the original string.
        Returns None if the file was opened, but errored during reading.
    """
    try:
        with open(s, 'r') as f:
            data = f.read()
    except FileNotFoundError:
        # Not a file name.
        return s
    except EnvironmentError as ex:
        print('\nFailed to read file: {}\n  {}'.format(s, ex))
        return None
    return data

if __name__ == '__main__':
    mainret = main(docopt(USAGESTR, version=VERSIONSTR))
    sys.exit(mainret)
