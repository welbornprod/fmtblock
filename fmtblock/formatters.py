__version__ = '0.3.6'


class FormatBlock(object):

    """ Class to format text into a block, with or without indention.
        Able to break on characters or words, and preserve newlines when
        wanted.
        Initialize with some text, and then call the provided format()
        methods.
    """
    __slots__ = ('text',)

    def __init__(self, text=None):
        self.text = text or ''

    def expand_words(self, line, width=60):
        """ Insert spaces between words until it is wide enough for `width`.
        """
        if not line.strip():
            return line
        # Word index, which word to insert on (cycles between 1->len(words))
        wordi = 1
        while len(line) < width:
            wordendi = self.find_word_end(line, wordi)
            if wordendi < 0:
                # Reached the end?, try starting at the front again.
                wordi = 1
                wordendi = self.find_word_end(line, wordi)
            if wordendi < 0:
                # There are no spaces to expand, just prepend one.
                line = ''.join((' ', line))
            else:
                line = ' '.join((line[:wordendi], line[wordendi:]))
                wordi += 1

        return line

    @staticmethod
    def find_word_end(text, count=1):
        """ This is a helper method for self.expand_words().
            Finds the index of word endings (default is first word).
            The last word doesn't count.
            If there are no words, or there are no spaces in the word, it
            returns -1.
            Example:
                s = 'this is a test'
                i = find_word_end(s, count=1)
                print('-'.join((s[:i], s[i:])))
                # 'this- is a test'
                i = find_word_end(s, count=2)
                print('-'.join((s[:i], s[i:])))
                # 'this is- a test'
        """
        count = count or 1
        found = 0
        foundindex = -1
        inword = False
        for i, c in enumerate(text):
            if inword and c.isspace():
                # Found space.
                inword = False
                foundindex = i
                found += 1
                if found == count:
                    return foundindex
            elif not c.isspace():
                inword = True
        # We ended in a word, or there were no words.
        return -1 if inword else foundindex

    def format(
            self, text=None,
            width=60, chars=False, fill=False, newlines=False,
            prepend=None, append=None, strip_first=False, strip_last=False,
            lstrip=False):
        """ Format a long string into a block of newline seperated text.
            Arguments:
                See iter_format_block().
        """
        # Basic usage of iter_format_block(), for convenience.
        return '\n'.join(
            self.iter_format_block(
                (self.text if text is None else text) or '',
                prepend=prepend,
                append=append,
                strip_first=strip_first,
                strip_last=strip_last,
                width=width,
                chars=chars,
                fill=fill,
                newlines=newlines,
                lstrip=lstrip
            )
        )

    def iter_add_text(self, lines, prepend=None, append=None):
        """ Prepend or append text to lines. Yields each line. """
        if (prepend is None) and (append is None):
            yield from lines
        else:
            # Build up a format string, with optional {prepend}/{append}
            fmtpcs = ['{prepend}'] if prepend else []
            fmtpcs.append('{line}')
            if append:
                fmtpcs.append('{append}')
            fmtstr = ''.join(fmtpcs)
            yield from (
                fmtstr.format(prepend=prepend, line=line, append=append)
                for line in lines
            )

    def iter_block(
            self, text=None,
            width=60, chars=False, newlines=False, lstrip=False):
        """ Iterator that turns a long string into lines no greater than
            'width' in length.
            It can wrap on spaces or characters. It only does basic blocks.
            For prepending see `iter_format_block()`.

            Arguments:
                text     : String to format.
                width    : Maximum width for each line.
                           Default: 60
                chars    : Wrap on characters if true, otherwise on spaces.
                           Default: False
                newlines : Preserve newlines when True.
                           Default: False
                lstrip   : Whether to remove leading spaces from each line.
                           Default: False
        """
        text = (self.text if text is None else text) or ''
        if width < 1:
            width = 1
        fmtline = str.lstrip if lstrip else str

        if chars and (not newlines):
            # Simple block by chars, newlines are treated as a space.
            yield from self.iter_char_block(
                text,
                width=width,
                fmtfunc=fmtline
            )
        elif newlines:
            # Preserve newlines
            for line in text.split('\n'):
                yield from self.iter_block(
                    line,
                    width=width,
                    chars=chars,
                    lstrip=lstrip,
                    newlines=False,
                )
        else:
            # Wrap on spaces (ignores newlines)..
            yield from self.iter_space_block(
                text,
                width=width,
                fmtfunc=fmtline,
            )

    def iter_char_block(self, text=None, width=60, fmtfunc=str):
        """ Format block by splitting on individual characters. """
        if width < 1:
            width = 1
        text = (self.text if text is None else text) or ''
        text = ' '.join(text.split('\n'))
        yield from (
            fmtfunc(text[i:i + width])
            for i in range(0, len(text), width)
        )

    def iter_format_block(
            self, text=None,
            width=60, chars=False, fill=False, newlines=False,
            append=None, prepend=None, strip_first=False, strip_last=False,
            lstrip=False):
        """ Iterate over lines in a formatted block of text.
            This iterator allows you to prepend to each line.
            For basic blocks see iter_block().


            Arguments:
                text        : String to format.

                width       : Maximum width for each line. The prepend string
                              is not included in this calculation.
                              Default: 60

                chars       : Whether to wrap on characters instead of spaces.
                              Default: False
                fill        : Insert spaces between words so that each line is
                              the same width. This overrides `chars`.
                              Default: False

                newlines    : Whether to preserve newlines in the original
                              string.
                              Default: False

                append      : String to append after each line.

                prepend     : String to prepend before each line.

                strip_first : Whether to omit the prepend string for the first
                              line.
                              Default: False

                              Example (when using prepend='$'):
                               Without strip_first -> '$this', '$that'
                               With strip_first -> 'this', '$that'

                strip_last  : Whether to omit the append string for the last
                              line (like strip_first does for prepend).
                              Default: False

                lstrip      : Whether to remove leading spaces from each line.
                              This doesn't include any spaces in `prepend`.
                              Default: False
        """
        if fill:
            chars = False

        iterlines = self.iter_block(
            (self.text if text is None else text) or '',
            width=width,
            chars=chars,
            newlines=newlines,
            lstrip=lstrip,
        )

        if not (prepend or append):
            # Shortcut some of the logic below when not prepending/appending.
            if fill:
                yield from (
                    self.expand_words(l, width=width) for l in iterlines
                )
            else:
                yield from iterlines
        else:
            # Prepend, append, or both prepend/append to each line.
            if prepend:
                prependlen = len(prepend)
            else:
                # No prepend, stripping not necessary and shouldn't be tried.
                strip_first = False
                prependlen = 0
            if append:
                # Unfortunately appending mean exhausting the generator.
                # I don't know where the last line is if I don't.
                lines = list(iterlines)
                lasti = len(lines) - 1
                iterlines = (l for l in lines)
                appendlen = len(append)
            else:
                # No append, stripping not necessary and shouldn't be tried.
                strip_last = False
                appendlen = 0
                lasti = -1
            for i, l in enumerate(self.iter_add_text(
                    iterlines,
                    prepend=prepend,
                    append=append)):
                if strip_first and (i == 0):
                    # Strip the prepend that iter_add_text() added.
                    l = l[prependlen:]
                elif strip_last and (i == lasti):
                    # Strip the append that iter_add_text() added.
                    l = l[:-appendlen]
                if fill:
                    yield self.expand_words(l, width=width)
                else:
                    yield l

    def iter_space_block(self, text=None, width=60, fmtfunc=str):
        """ Format block by wrapping on spaces. """
        if width < 1:
            width = 1
        curline = ''
        text = (self.text if text is None else text) or ''
        for word in text.split():
            possibleline = ' '.join((curline, word)) if curline else word

            if len(possibleline) > width:
                # This word would exceed the limit, start a new line with
                # it.
                yield fmtfunc(curline)
                curline = word
            else:
                curline = possibleline
        # yield the last line.
        if curline:
            yield fmtfunc(curline)

    @staticmethod
    def squeeze_words(line, width=60):
        """ Remove spaces in between words until it is small enough for
            `width`.
            This will always leave at least one space between words,
            so it may not be able to get below `width` characters.
        """
        # Start removing spaces to "squeeze" the text, leaving at least one.
        while ('  ' in line) and (len(line) > width):
            # Remove two spaces from the end, replace with one.
            head, _, tail = line.rpartition('  ')
            line = ' '.join((head, tail))
        return line
