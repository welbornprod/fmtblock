#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" fmtblock.py
    ...Formats long text into terminal-friendly blocks of text.
    Christopher Welborn 02-03-2015
"""

from docopt import docopt
import os
import sys

NAME = 'Format Block'
VERSION = '0.2.0'
VERSIONSTR = '{} v. {}'.format(NAME, VERSION)
SCRIPT = os.path.split(os.path.abspath(sys.argv[0]))[1]
SCRIPTDIR = os.path.abspath(sys.path[0])

# Maximum width for lines, unless -w is used.
DEFAULT_WIDTH = 79

USAGESTR = """{versionstr}

    Formats text, files, or stdin, into blocks of text with a maximum width.
    Output is printed to stdout.

    Usage:
        {script} -h | -v
        {script} [WORDS...] [-c] [-e] ([-i num] | [-I num]) [-l] [-n] [-w num]

    Options:
        WORDS                : Words to format into a block.
                               File names can be passed to read from a file.
                               If not given, stdin is used instead.
        -c,--chars           : Wrap on characters instead of spaces.
        -e,--enumerate       : Print line numbers before each line.
        -h,--help            : Show this help message.
        -i num,--indent num  : Indention level. Each indent level is 4 spaces.
                               Maximum width includes any indention.
                               Default: 0
        -I num,--INDENT num  : Same as --indent, except maximum width is
                               calculated after indention.
                               Default: 0
        -l,--lstrip          : Remove leading spaces for each line, before
                               indention.
        -n,--newlines        : Preserve newlines.
        -v,--version         : Show version.
        -w num,--width num   : Maximum width for the block.
                               Default: {defaultwidth}

        By default words are wrapped on spaces, so lines may be longer than the
        specified width. To force a hard limit use --chars.
""".format(
    script=SCRIPT,
    versionstr=VERSIONSTR,
    defaultwidth=DEFAULT_WIDTH)


def main(argd):
    """ Main entry point, expects doctopt arg dict as argd. """
    width = parse_int(argd['--width'] or DEFAULT_WIDTH)
    indent = parse_int(argd['--indent'] or (argd['--INDENT'] or 0))
    prepend = ' ' * (indent * 4)
    if prepend and argd['--indent']:
        # Smart indent, change max width based on indention.
        width -= len(prepend)

    if argd['WORDS']:
        # Try each argument as a file name.
        # TODO: Just remove the WORDS feature and use stdin or FILE.
        argd['WORDS'] = (
            (try_read_file(w) if len(w) < 256 else w)
            for w in argd['WORDS']
        )
        words = ' '.join((w for w in argd['WORDS'] if w))
    else:
        words = read_stdin()

    block = FormatBlock().iter_format_block(
        words,
        chars=argd['--chars'],
        prepend=prepend,
        width=width,
        newlines=argd['--newlines'],
        lstrip=argd['--lstrip']
    )

    for i, line in enumerate(block):
        if argd['--enumerate']:
            # Current line number format supports up to 999 lines before
            # messing up. Who would format 1000 lines like this anyway?
            print('{: >3}: {}'.format(i, line))
        else:
            print(line)

    return 0


class FormatBlock(object):

    """ Class to format text into a block, with or without indention.
        Able to break on characters or words, and preserve newlines when
        wanted.
        This used to be purely procedural, but I decided it would be easier
        to 'contain' this functionality and copy/paste this class where
        needed.
    """
    __slots__ = ('text',)

    def __init__(self, text=None):
        self.text = text or ''

    def format(
            self, text=None,
            width=60, chars=False, newlines=False,
            prepend=None, strip_first=False, lstrip=False):
        """ Format a long string into a block of newline seperated text.
            Arguments:
                See iter_format_block().
        """
        # Basic usage of iter_format_block(), for convenience.
        return '\n'.join(
            self.iter_format_block(
                text or self.text,
                prepend=prepend,
                strip_first=strip_first,
                width=width,
                chars=chars,
                newlines=newlines,
                lstrip=lstrip
            )
        )

    def iter_block(
            self, text=None,
            width=60, chars=False, newlines=False, lstrip=False):
        """ Iterator that turns a long string into lines no greater than
            'width' in length.
            It can wrap on spaces or characters. It only does basic blocks.
            For prepending see `iter_format_block()`.

            Arguments:
                text       : String to format.
                width  : Maximum width for each line.
                             Default: 60
                chars      : Wrap on characters if true, otherwise on spaces.
                             Default: False
                newlines   : Preserve newlines when True.
                             Default: False
                lstrip     : Whether to remove leading spaces from each line.
                             Default: False
        """
        text = text or self.text
        if lstrip:
            # Remove leading spaces from each line.
            fmtline = str.lstrip
        else:
            # Yield the line as-is.
            fmtline = lambda s: s

        if chars and (not newlines):
            # Simple block by chars, newlines are treated as a space.
            text = ' '.join(text.splitlines())
            yield from (
                fmtline(text[i:i + width])
                for i in range(0, len(text), width)
            )
        elif newlines:
            # Preserve newlines
            for line in text.splitlines():
                yield from self.iter_block(
                    line,
                    width=width,
                    chars=chars,
                    lstrip=lstrip)
        else:
            # Wrap on spaces (ignores newlines)..
            curline = ''
            for word in text.split():
                possibleline = ' '.join((curline, word)) if curline else word

                if len(possibleline) > width:
                    # This word would exceed the limit, start a new line with
                    # it.
                    yield fmtline(curline)
                    curline = word
                else:
                    curline = possibleline
            if curline:
                yield fmtline(curline)

    def iter_format_block(
            self, text=None,
            width=60, chars=False, newlines=False,
            prepend=None, strip_first=False, lstrip=False):
        """ Iterate over lines in a formatted block of text.
            This iterator allows you to prepend to each line.
            For basic blocks see iter_block().


            Arguments:
                text         : String to format.

                width        : Maximum width for each line. The prepend string
                               is not included in this calculation.
                               Default: 60

                chars        : Whether to wrap on characters instead of spaces.
                               Default: False

                newlines     : Whether to preserve newlines in the original
                               string.
                               Default: False

                prepend      : String to prepend before each line.

                strip_first  : Whether to omit the prepend string for the first
                               line.
                               Default: False

                               Example (when using prepend='$'):
                                Without strip_first -> '$this', '$that'
                                   With strip_first -> 'this', '$that'

                lstrip       : Whether to remove leading spaces from each line.
                               This doesn't include any spaces in `prepend`.
                               Default: False
        """
        iterlines = self.iter_block(
            text or self.text,
            width=width,
            chars=chars,
            newlines=newlines,
            lstrip=lstrip)
        if prepend is None:
            yield from iterlines
        else:
            # Prepend text to each line.
            for i, l in enumerate(iterlines):
                if (i == 0) and strip_first:
                    yield l
                else:
                    yield '{}{}'.format(prepend, l)


def parse_int(s):
    """ Parse a string as an integer.
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
    if sys.stdin.isatty() and sys.stdout.isatty():
        print('\nReading from stdin until EOF (Ctrl + D)...\n')
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
