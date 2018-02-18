#!/usr/bin/env python3
""" FormatBlock - Escape Codes
    Functions to test against/strip terminal escape codes from strings.
    -Christopher Welborn 2-17-18
"""

import re
from typing import (
    Any,
    Dict,
    List,
)

_codepats = (
    # Colors.
    r'(([\d;]+)?m{1})',
    # Cursor show/hide.
    r'(\?25l)',
    r'(\?25h)',
    # Move position.
    r'(([\d]+[;])?([\d]+[Hf]))',
    # Save/restore position.
    r'([su])',
    # Others (move, erase).
    r'([\d]+[ABCDEFGHJKST])',
)

# Used to strip escape codes from a string.
codepat = re.compile(
    '\033\[({})'.format('|'.join(_codepats))
)
# Used to grab codes from a string.
codegrabpat = re.compile('\033\[[\d;]+?m{1}')


def get_codes(s: Any) -> List[str]:
    """ Grab all escape codes from a string.
        Returns a list of all escape codes.
    """
    return codegrabpat.findall(str(s))


def get_code_indices(s: Any) -> Dict[int, str]:
    """ Retrieve a dict of {index: escape_code} for a given string.
        If no escape codes are found, an empty dict is returned.
    """
    indices = {}
    i = 0
    codes = get_codes(s)
    for code in codes:
        codeindex = s.index(code)
        realindex = i + codeindex
        indices[realindex] = code
        codelen = len(code)
        i = realindex + codelen
        s = s[codeindex + codelen:]
    return indices


def get_indices(s: Any) -> Dict[int, str]:
    """ Retrieve a dict of characters and escape codes with their real index
        into the string as the key.
    """
    codes = get_code_indices(s)
    if not codes:
        # This function is not for non-escape-code stuff, but okay.
        return {i: c for i, c in enumerate(s)}

    indices = {}
    for codeindex in sorted(codes):
        code = codes[codeindex]
        if codeindex == 0:
            indices[codeindex] = code
            continue
        # Grab characters before codeindex.
        start = max(indices or {0: ''}, key=int)
        startcode = indices.get(start, '')
        startlen = start + len(startcode)
        indices.update({i: s[i] for i in range(startlen, codeindex)})
        indices[codeindex] = code

    if not indices:
        return {i: c for i, c in enumerate(s)}
    lastindex = max(indices, key=int)
    lastitem = indices[lastindex]
    start = lastindex + len(lastitem)
    textlen = len(s)
    if start < (textlen - 1):
        # Grab chars after last code.
        indices.update({i: s[i] for i in range(start, textlen)})
    return indices


def get_indices_list(s: Any) -> List[str]:
    """ Retrieve a list of characters and escape codes where each escape
        code uses only one index. The indexes will not match up with the
        indexes in the original string.
    """
    indices = get_indices(s)
    return [
        indices[i] for i in sorted(indices, key=int)
    ]


def is_escape_code(s: Any) -> bool:
    """ Returns True if `s` appears to be any kind of escape code. """
    return codepat.match(str(s)) is not None


def strip_codes(s: Any) -> str:
    """ Strip all color codes from a string.
        Returns empty string for "falsey" inputs.
    """
    return codepat.sub('', str(s) if (s or (s == 0)) else '')
