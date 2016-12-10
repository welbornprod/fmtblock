# FmtBlock

Formats text into "blocks" that do not exceed the maximum length for each line.
This can be used as a command-line tool or imported for the `FormatBlock`
class. There are various features like prepending, appending,
expanding space between words, splitting on characters or spaces, and
preserving newlines.

_______________________________________________________________________________

## Command-line help:

```
Usage:
    fmtblock -h | -v
    fmtblock [WORDS...] [-D] [-w num]
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
                            Default: 79
```

_______________________________________________________________________________

## Dependencies:

* **Python 3.3+** - This project uses `yield from`. Porting to older python
versions would be trivial, but I don't plan on doing it (just use `for-loops`
and `yield` instead of `yield from`).

## Python Dependencies:

These are installable with `pip`.

* **Colr** - Used for colorized output.
* **Docopt** - Used to handle command-line argument parsing.

_______________________________________________________________________________

## Installation:

Install the module with pip:
```
# You may have to use pip3 here.
pip install formatblock
```

Then you can run it like this:
```
fmtblock --help
```

Or like this:
```
python3 -m fmtblock --help
```

## Imports

All of the functionality for `fmtblock` is contained in a class called
`FormatBlock`, which is importable for use in your project.

```python
from fmtblock import FormatBlock

print(FormatBlock('This is a test okay.').format(width=5))
```

Output:
```
This
is a
test
okay.
```
______________________________________________________________________________

## Examples:

### Input:

These three methods for sending input to `fmtblock` are the same:
```bash
echo "Test String" | fmtblock -w 5
fmtblock "Test String" -w 5
fmtblock Test String -w 5
```

### Space splitting:
```bash
fmtblock -w 30 "This is a fairly long string, though I've seen bigger."
```

Output:
```
This is a fairly long string,
though I've seen bigger.
```

### Character splitting:
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

### Newlines:
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

### Enumeration:
```bash
echo {a..c} | fmtblock -e -w 1
```

Output:
```
1: a
2: b
3: c
```

### Indents:
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

### Prepended Text:
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

Also see `-P`, to prepend text without it affecting width calculations.

### Appended Text:
```bash
seq 1 3 | fmtblock -n -a ") Test"
```

Output:
```
1) Test
2) Test
3) Test
```

Also see `-A`, to append text without it affecting width calculations.

### Strip first/last:
When using `-p` or `-P`, you can skip the first line with `-s`.

When using `-a` or `-A`, you can also skip the last line with `-S`.
```bash
seq 200000 200010 | fmtblock -w 30 -p "    " -s -a " \\" -S
```

Output:
```
200000 200001 200002 \
    200003 200004 200005 \
    200006 200007 200008 \
    200009 200010
```

### Fill:
```bash
echo "this is a test of the word fill feature for fmtblock" | fmtblock -w 20 -f
```

Output:
```
this  is  a  test of
the     word    fill
feature for fmtblock
```
