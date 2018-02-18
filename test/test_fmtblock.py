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

    def test_expand_words(self):
        """ expand_words() should insert spaces to make words fit. """
        s = 'This is a test and only a test. I really like this test.'
        expected = {
            25: """
This is a test and only a
test.  I really like this
test.
""".strip(),
            30: """
This  is  a  test  and  only a
test. I really like this test.
""".strip(),
            15: """
This  is a test
and    only   a
test.  I really
like this test.
""".strip(),
        }
        for width, expectedstr in expected.items():
            result = FormatBlock(s).format(fill=True, width=width)
            self.assertEqual(
                result,
                expectedstr,
                msg='\n'.join((
                    'Failed to expand words correctly. Width: {}'.format(
                        width
                    ),
                    'Result:\n{}'.format(result),
                    'Expected:\n{}'.format(expectedstr),
                ))
            )

    def test_expand_words_colr(self):
        """ expand_words() should ignore escape codes. """
        s = ''.join((
            '\x1b[38;5;57mT\x1b[0m\x1b[38;5;63mh\x1b[0m\x1b[38;5;63mi',
            '\x1b[0m\x1b[38;5;63ms\x1b[0m\x1b[38;5;63m \x1b[0m\x1b[38;5;63mi',
            '\x1b[0m\x1b[38;5;63ms\x1b[0m\x1b[38;5;63m \x1b[0m\x1b[38;5;63ma',
            '\x1b[0m\x1b[38;5;63m \x1b[0m\x1b[38;5;27mt\x1b[0m\x1b[38;5;27me',
            '\x1b[0m\x1b[38;5;27ms\x1b[0m\x1b[38;5;27mt\x1b[0m\x1b[38;5;27m ',
            '\x1b[0m\x1b[38;5;27ma\x1b[0m\x1b[38;5;27mn\x1b[0m\x1b[38;5;27md',
            '\x1b[0m\x1b[38;5;33m \x1b[0m\x1b[38;5;33mo\x1b[0m\x1b[38;5;33mn',
            '\x1b[0m\x1b[38;5;33ml\x1b[0m\x1b[38;5;33my\x1b[0m\x1b[38;5;32m ',
            '\x1b[0m\x1b[38;5;32ma\x1b[0m\x1b[38;5;32m \x1b[0m\x1b[38;5;32mt',
            '\x1b[0m\x1b[38;5;32me\x1b[0m\x1b[38;5;38ms\x1b[0m\x1b[38;5;38mt',
            '\x1b[0m\x1b[38;5;38m.\x1b[0m',
        ))

        expected = {
            10: ''.join((
                '\x1b[38;5;57mT\x1b[0m\x1b[38;5;63mh\x1b[0m\x1b[38;5;63mi',
                '\x1b[0m\x1b[38;5;63ms \x1b[0m\x1b[38;5;63m \x1b[0m',
                '\x1b[38;5;63mi\x1b[0m\x1b[38;5;63ms\x1b[0m\x1b[38;5;63m ',
                '\x1b[0m\x1b[38;5;63ma\x1b[0m\x1b[38;5;63m\n\x1b[0m',
                '\x1b[38;5;27mt\x1b[0m\x1b[38;5;27me\x1b[0m\x1b[38;5;27ms',
                '\x1b[0m\x1b[38;5;27mt  \x1b[0m\x1b[38;5;27m \x1b[0m',
                '\x1b[38;5;27ma\x1b[0m\x1b[38;5;27mn\x1b[0m\x1b[38;5;27md',
                '\x1b[0m\x1b[38;5;33m\n\x1b[0m\x1b[38;5;33mo\x1b[0m',
                '\x1b[38;5;33mn\x1b[0m\x1b[38;5;33ml\x1b[0m',
                '\x1b[38;5;33my  \x1b[0m\x1b[38;5;32m \x1b[0m',
                '\x1b[38;5;32ma  \x1b[0m\x1b[38;5;32m\n\x1b[0m',
                '\x1b[38;5;32mt\x1b[0m\x1b[38;5;32me\x1b[0m\x1b[38;5;38ms',
                '\x1b[0m\x1b[38;5;38mt\x1b[0m\x1b[38;5;38m.\x1b[0m',
            )),
            15: ''.join((
                '\x1b[38;5;57mT\x1b[0m\x1b[38;5;63mh\x1b[0m\x1b[38;5;63mi',
                '\x1b[0m\x1b[38;5;63ms \x1b[0m\x1b[38;5;63m \x1b[0m',
                '\x1b[38;5;63mi\x1b[0m\x1b[38;5;63ms\x1b[0m',
                '\x1b[38;5;63m \x1b[0m\x1b[38;5;63ma\x1b[0m',
                '\x1b[38;5;63m \x1b[0m\x1b[38;5;27mt\x1b[0m\x1b[38;5;27me',
                '\x1b[0m\x1b[38;5;27ms\x1b[0m\x1b[38;5;27mt\x1b[0m',
                '\x1b[38;5;27m\n\x1b[0m\x1b[38;5;27ma\x1b[0m\x1b[38;5;27mn',
                '\x1b[0m\x1b[38;5;27md  \x1b[0m\x1b[38;5;33m \x1b[0m',
                '\x1b[38;5;33mo\x1b[0m\x1b[38;5;33mn\x1b[0m\x1b[38;5;33ml',
                '\x1b[0m\x1b[38;5;33my  \x1b[0m\x1b[38;5;32m \x1b[0m',
                '\x1b[38;5;32ma \x1b[0m\x1b[38;5;32m\n\x1b[0m',
                '\x1b[38;5;32mt\x1b[0m\x1b[38;5;32me\x1b[0m\x1b[38;5;38ms',
                '\x1b[0m\x1b[38;5;38mt\x1b[0m\x1b[38;5;38m.\x1b[0m',
            )),
            20: ''.join((
                '\x1b[38;5;57mT\x1b[0m\x1b[38;5;63mh\x1b[0m\x1b[38;5;63mi',
                '\x1b[0m\x1b[38;5;63ms  \x1b[0m\x1b[38;5;63m \x1b[0m',
                '\x1b[38;5;63mi\x1b[0m\x1b[38;5;63ms\x1b[0m',
                '\x1b[38;5;63m \x1b[0m\x1b[38;5;63ma\x1b[0m',
                '\x1b[38;5;63m \x1b[0m\x1b[38;5;27mt\x1b[0m\x1b[38;5;27me',
                '\x1b[0m\x1b[38;5;27ms\x1b[0m\x1b[38;5;27mt\x1b[0m',
                '\x1b[38;5;27m \x1b[0m\x1b[38;5;27ma\x1b[0m\x1b[38;5;27mn',
                '\x1b[0m\x1b[38;5;27md\x1b[0m\x1b[38;5;33m\n\x1b[0m',
                '\x1b[38;5;33mo\x1b[0m\x1b[38;5;33mn\x1b[0m\x1b[38;5;33ml',
                '\x1b[0m\x1b[38;5;33my  \x1b[0m\x1b[38;5;32m \x1b[0m',
                '\x1b[38;5;32ma  \x1b[0m\x1b[38;5;32m \x1b[0m',
                '\x1b[38;5;32mt\x1b[0m\x1b[38;5;32me\x1b[0m\x1b[38;5;38ms',
                '\x1b[0m\x1b[38;5;38mt\x1b[0m\x1b[38;5;38m.    \x1b[0m',
            )),
        }
        for width, expectedstr in expected.items():
            result = FormatBlock(s).format(fill=True, width=width)
            self.assertEqual(
                result,
                expectedstr,
                msg='\n'.join((
                    'Failed to expand words correctly. Width: {}'.format(
                        width
                    ),
                    'Result:\n{}'.format(result),
                    'Expected:\n{}'.format(expectedstr),
                ))
            )

    def test_find_word_end(self):
        """ find_word_end() should correctly find the end of words. """
        words = 'this is a test and only a test. not a problem.'.split()
        s = ' '.join(words)
        for cnt in range(1, len(words)):
            i = FormatBlock().find_word_end(s, count=cnt)
            result = '-'.join((s[:i], s[i:]))
            self.assertEqual(
                result,
                '{}- {}'.format(' '.join(words[:cnt]), ' '.join(words[cnt:])),
                msg='Failed to find word end. Count: {}'.format(cnt)
            )

        # No words, should return -1.
        self.assertEqual(
            FormatBlock().find_word_end('', count=1),
            -1,
            msg='No words to find. Should\'ve returned -1.',
        )
        self.assertEqual(
            FormatBlock().find_word_end('      ', count=1),
            -1,
            msg='No words to find. Should\'ve returned -1.',
        )
        # Single word.
        self.assertEqual(
            FormatBlock().find_word_end('test', count=1),
            0,
            msg='Single word, should\'ve returned 0.',
        )

    def test_find_word_end_colr(self):
        """ find_word_end() should ignore escape codes. """
        s = '\x1b[31mtest\x1b[0m \x1b[34mthis\x1b[0m \x1b[32mout\x1b[0m'
        i = FormatBlock().find_word_end(s, count=1)
        result = '-'.join((s[:i], s[i:]))
        self.assertEqual(
            result,
            '\x1b[31mtest-\x1b[0m \x1b[34mthis\x1b[0m \x1b[32mout\x1b[0m',
            msg='Failed to find word end with escape codes.'
        )
        i = FormatBlock().find_word_end(s, count=2)
        result = '-'.join((s[:i], s[i:]))
        self.assertEqual(
            result,
            '\x1b[31mtest\x1b[0m \x1b[34mthis-\x1b[0m \x1b[32mout\x1b[0m',
            msg='Failed to find word end with escape codes.'
        )
        i = FormatBlock().find_word_end(s, count=3)
        result = '-'.join((s[:i], s[i:]))
        self.assertEqual(
            result,
            '\x1b[31mtest\x1b[0m \x1b[34mthis\x1b[0m \x1b[32mout-\x1b[0m',
            msg='Failed to find word end with escape codes.'
        )

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
