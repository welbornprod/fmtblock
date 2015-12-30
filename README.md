FmtBlock
========

Formats text into "blocks" that do not exceed the maximum length for each line.
This can be used as a command-line tool or imported for the `FormatBlock`
class.

_______________________________________________________________________________

Command-line help:
==================

```
Formats text, files, or stdin, into blocks of text with a maximum width.
Output is printed to stdout.

Usage:
    fmtblock -h | -v
    fmtblock [WORDS...] [-w num]
             [-c] [-e] ([-i num] | [-I num])
             [-l] [-n] ([-p txt] | [-P txt])

Options:
    WORDS                 : Words to format into a block.
                            File names can be passed to read from a file.
                            If not given, stdin is used instead.
    -c,--chars            : Wrap on characters instead of spaces.
    -e,--enumerate        : Print line numbers before each line.
    -h,--help             : Show this help message.
    -i num,--indent num   : Indention level. Each indent level is 4 spaces.
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
    -v,--version          : Show version.
    -w num,--width num    : Maximum width for the block.
                            Default: 79

    By default words are wrapped on spaces, so lines may be longer than the
    specified width. To force a hard limit use --chars.
```

_______________________________________________________________________________

Dependencies:
=============

* **Python 3.3+** - This project uses `yield from`. Porting to older python
versions would be trivial, but I don't plan on doing it (just use `for-loops`
and `yield` instead of `yield from`).

_______________________________________________________________________________

Installation:
=============

* Download `fmtblock.py` or clone this repo:
```
git clone https://github.com/welbornprod/fmtblock.git
```

* Change to the fmtblock directory (containing `fmtblock.py`):
```
cd fmtblock
```

* Symlink the script into a directory in your `$PATH`:
```
ln -s "$PWD/fmtblock.py" ~/bin/fmtblock
```

Now you can run `fmtblock` instead of `./fmtblock.py`.

_______________________________________________________________________________

Examples:
=========

###Input:

These three methods for sending input to `fmtblock` are the same:
```bash
echo "Test String" | fmtblock -w 5
fmtblock "Test String" -w 5
fmtblock Test String -w 5
```

###Space splitting:
```bash
fmtblock -w 30 "This is a fairly long string, though I've seen bigger."
```

Output:
```
This is a fairly long string,
though I've seen bigger.
```

###Character splitting:
```bash
fmtblock -c -w 10 "This is a fairly long string, though I've seen bigger."
```

Output:
```
This is a
fairly lon
g string,
though I'v
e seen big
ger.
```

###Newlines:
```bash
echo "This is a string
that contains newlines
and they will be preserved." | fmtblock -w 20 -n
```

Output:
```
This is a string
that contains
newlines
and they will be
preserved.
```

###Enumeration:
```bash
echo {a..c} | fmtblock -e -w 1
```

Output:
```
  1: a
  2: b
  3: c
```

###Indents:
```bash
# Preserving newlines with -n, instead of using -w.
seq 1 3 | fmtblock -i 1 -n
```

Output:
```
    1
    2
    3
```

###Prepended Text:
```bash
# Preserving newlines with -n, instead of using -w.
seq 1 3 | fmtblock -n -p "Test "
```

Output:
```
Test 1
Test 2
Test 3
```
