#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" fmtblock.py
    ...Formats long text into terminal-friendly blocks of text.
    Christopher Welborn 02-03-2015
"""

import inspect
import os
import sys
from contextlib import suppress

from colr import (
    auto_disable as colr_auto_disable,
    Colr as C,
    docopt
)

from .formatters import (
    __version__,
    FormatBlock,
)

colr_auto_disable()

NAME = 'Format Block'
VERSIONSTR = '{} v. {}'.format(NAME, __version__)
SCRIPT = 'fmtblock'
SCRIPTDIR = os.path.abspath(sys.path[0])

# Maximum width for lines, unless -w is used.
DEFAULT_WIDTH = 79

USAGESTR = """{versionstr}

    Formats text, files, or stdin, into blocks of text with a maximum width.
    Output is printed to stdout.

    Usage:
        {script} -h | -v
        {script} [WORDS...] [-D] [-w num]
                 [-c | -f] [-e] ([-i num] | [-I num]) [-l] [-n]
                 ([-s] [-p txt | -P txt]) ([-S] [-a txt | -A txt])

    Options:
        WORDS                 : Words to format into a block.
                                File names can be passed to read from a file.
                                If not given, stdin is used instead.
        -a txt,--append txt   : Append this text before each line, after any
                                indents.
        -A txt,--APPEND txt   : Same as --append, except the appended text
                                is not included when calculating the width.
        -c,--chars            : Wrap on characters instead of spaces.
        -D,--debug            : Show some debugging info.
        -e,--enumerate        : Print line numbers before each line.
        -f,--fill             : Insert spaces between words so that each line
                                is the same width.
        -h,--help             : Show this help message.
        -i num,--indent num   : Indention level, where 4 spaces is 1 indent.
                                Maximum width includes any indention.
                                Default: 0
        -I num,--INDENT num   : Same as --indent, except the indention is not
                                included when calculating the width.
                                Default: 0
        -l,--lstrip           : Remove leading spaces for each line, before
                                indention.
        -n,--newlines         : Preserve newlines.
        -p txt,--prepend txt  : Prepend this text before each line, after any
                                indents.
        -P txt,--PREPEND txt  : Same as --prepend, except the prepended text
                                is not included when calculating the width.
        -s,--stripfirst       : Strip first --prepend.
        -S,--striplast        : Strip last --append.
        -v,--version          : Show version.
        -w num,--width num    : Maximum width for the block.
                                Default: {defaultwidth}
""".format(
    script=SCRIPT,
    versionstr=VERSIONSTR,
    defaultwidth=DEFAULT_WIDTH)

DEBUG = False


def main():
    """ Main entry point, expects doctopt arg dict as argd. """
    global DEBUG
    argd = docopt(USAGESTR, version=VERSIONSTR, script=SCRIPT)
    DEBUG = argd['--debug']

    width = parse_int(argd['--width'] or DEFAULT_WIDTH) or 1
    indent = parse_int(argd['--indent'] or (argd['--INDENT'] or 0))
    prepend = ' ' * (indent * 4)
    if prepend and argd['--indent']:
        # Smart indent, change max width based on indention.
        width -= len(prepend)

    userprepend = argd['--prepend'] or (argd['--PREPEND'] or '')
    prepend = ''.join((prepend, userprepend))
    if argd['--prepend']:
        # Smart indent, change max width based on prepended text.
        width -= len(userprepend)
    userappend = argd['--append'] or (argd['--APPEND'] or '')
    if argd['--append']:
        width -= len(userappend)

    if argd['WORDS']:
        # Try each argument as a file name.
        argd['WORDS'] = (
            (try_read_file(w) if len(w) < 256 else w)
            for w in argd['WORDS']
        )
        words = ' '.join((w for w in argd['WORDS'] if w))
    else:
        # No text/filenames provided, use stdin for input.
        words = read_stdin()

    block = FormatBlock(words).iter_format_block(
        chars=argd['--chars'],
        fill=argd['--fill'],
        prepend=prepend,
        strip_first=argd['--stripfirst'],
        append=userappend,
        strip_last=argd['--striplast'],
        width=width,
        newlines=argd['--newlines'],
        lstrip=argd['--lstrip'],
    )

    for i, line in enumerate(block):
        if argd['--enumerate']:
            # Current line number format supports up to 999 lines before
            # messing up. Who would format 1000 lines like this anyway?
            print('{: >3}: {}'.format(i + 1, line))
        else:
            print(line)

    return 0


def debug(*args, **kwargs):
    """ Print a message only if DEBUG is truthy. """
    if not (DEBUG and args):
        return None

    # Include parent class name when given.
    parent = kwargs.get('parent', None)
    with suppress(KeyError):
        kwargs.pop('parent')

    # Go back more than once when given.
    backlevel = kwargs.get('back', 1)
    with suppress(KeyError):
        kwargs.pop('back')

    frame = inspect.currentframe()
    # Go back a number of frames (usually 1).
    while backlevel > 0:
        frame = frame.f_back
        backlevel -= 1
    fname = os.path.split(frame.f_code.co_filename)[-1]
    lineno = frame.f_lineno
    if parent:
        func = '{}.{}'.format(parent.__class__.__name__, frame.f_code.co_name)
    else:
        func = frame.f_code.co_name

    lineinfo = '{}:{} {}: '.format(
        C(fname, 'yellow'),
        C(str(lineno).ljust(4), 'blue'),
        C().join(C(func, 'magenta'), '()').ljust(20)
    )
    # Patch args to stay compatible with print().
    pargs = list(C(a, 'green').str() for a in args)
    pargs[0] = ''.join((lineinfo, pargs[0]))
    print_err(*pargs, **kwargs)


def parse_int(s):
    """ Parse a string as an integer.
        Exit with a message on failure.
    """
    try:
        val = int(s)
    except ValueError:
        print_err('\nInvalid integer: {}'.format(s))
        sys.exit(1)
    return val


def print_err(*args, **kwargs):
    """ Print to stderr by default. """
    if kwargs.get('file', None) is None:
        kwargs['file'] = sys.stderr
    print(*args, **kwargs)


def read_stdin():
    """ Read from stdin, but print a helpful message if it's a tty. """
    if sys.stdin.isatty() and sys.stdout.isatty():
        print('\nReading from stdin until end of file (Ctrl + D)...\n')
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
        print_err('\nFailed to read file: {}\n  {}'.format(s, ex))
        return None
    return data

if __name__ == '__main__':
    sys.exit(main())
