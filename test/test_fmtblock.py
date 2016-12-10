#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" test_fmtblock.py
    Unit tests for fmtblock.py

    -Christopher Welborn 12-09-2016
"""

import sys
import unittest

from fmtblock import FormatBlock


class FmtBlockTests(unittest.TestCase):

    def test_format_append(self):
        """ format() should append text after wrapping. """
        s = 'A AA AAA B BB BBB C CC CCC'
        expected = '\n'.join((
            'A AA <',
            'AAA <',
            'B BB <',
            'BBB <',
            'C CC <',
            'CCC <',

        ))
        self.assertEqual(
            FormatBlock(s).format(width=4, append=' <'),
            expected,
            msg='Failed to append text properly!'
        )

    def test_format_append_strip_last(self):
        """ format() should append text after wrapping, except the last line.
        """
        s = 'A AA AAA B BB BBB C CC CCC'
        expected = '\n'.join((
            'A AA <',
            'AAA <',
            'B BB <',
            'BBB <',
            'C CC <',
            'CCC',

        ))
        self.assertEqual(
            FormatBlock(s).format(width=4, append=' <', strip_last=True),
            expected,
            msg='Failed to append text, stripping the last line!'
        )

    def test_format_chars(self):
        """ format() should split on characters correctly. """
        s = 'AAABBBCCC'
        expected = '\n'.join((
            'AAA',
            'BBB',
            'CCC'
        ))
        self.assertEqual(
            FormatBlock(s).format(chars=True, width=3),
            expected,
            msg='Failed to wrap on characters!'
        )

    def test_format_fill(self):
        """ format() should fill lines to the correct width. """
        s = 'A AA AAA B BB BBB C CC CCC'
        result = FormatBlock(s).format(width=9, fill=True)
        self.assertTrue(
            all((len(line) == 9) for line in result.split('\n')),
            msg='Failed to fill text to width!'
        )

        s = 'This is a convoluted test to see if fmtblock fills.'
        result = FormatBlock(s).format(width=20, fill=True)
        self.assertTrue(
            all((len(line) == 20) for line in result.split('\n')),
            msg='Failed to fill text to width.'
        )

    def test_format_newlines(self):
        """ format() should preserve newlines when asked. """
        s = '\n'.join((
            'This',
            'is a',
            'test with some',
            'newlines',
            'in',
            'it, to split on.',
        ))
        expected = '\n'.join((
            'This',
            'is a',
            'test with',
            'some',
            'newlines',
            'in',
            'it, to',
            'split on.',
        ))
        self.assertEqual(
            FormatBlock(s).format(width=10, newlines=True),
            expected,
            msg='Failed to preserve newlines when splitting!'
        )

    def test_format_prepend(self):
        """ format() should prepend text after wrapping. """
        s = 'A AA AAA B BB BBB C CC CCC'
        expected = '\n'.join((
            '> A AA',
            '> AAA',
            '> B BB',
            '> BBB',
            '> C CC',
            '> CCC',
        ))
        self.assertEqual(
            FormatBlock(s).format(width=4, prepend='> '),
            expected,
            msg='Failed to prepend text properly!'
        )

    def test_format_prepend_strip_first(self):
        """ format() should prepend text after wrapping, except the first line
        """
        s = 'A AA AAA B BB BBB C CC CCC'
        expected = '\n'.join((
            'A AA',
            '> AAA',
            '> B BB',
            '> BBB',
            '> C CC',
            '> CCC',
        ))
        self.assertEqual(
            FormatBlock(s).format(width=4, prepend='> ', strip_first=True),
            expected,
            msg='Failed to prepend text, stripping the first line!'
        )

    def test_format_spaces(self):
        """ format() should wrap on spaces. """
        s = 'AAA BBB CCC DDD'
        expected = '\n'.join((
            'AAA',
            'BBB',
            'CCC',
            'DDD',
        ))
        self.assertEqual(
            FormatBlock(s).format(width=3),
            expected,
            msg='Failed to wrap on spaces!'
        )


if __name__ == '__main__':
    sys.exit(unittest.main(argv=sys.argv))
