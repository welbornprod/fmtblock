#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" runtests.py
    Glorified shortcut to `green -vv -q ARGS...`.
    Provides some sane defaults and extra output.
    -Christopher Welborn 03-19-2017
"""

import os
import subprocess
import sys
import unittest
from importlib import import_module

from green import __version__ as green_version
from colr import (
    __version__ as colr_version,
    auto_disable as colr_auto_disable,
    docopt,
    Colr as C,
)
from fmtblock import __version__ as fmtblock_version
colr_auto_disable()

APPNAME = 'FormatBlock'
APPVERSION = fmtblock_version
NAME = '{} Test Runner'.format(APPNAME)
VERSION = '0.0.1'
VERSIONSTR = '{} v. {}'.format(NAME, VERSION)
SCRIPT = os.path.split(os.path.abspath(sys.argv[0]))[1]
SCRIPTDIR = os.path.abspath(sys.path[0])

USAGESTR = """{versionstr}
    Runs tests using `green` and provides a little more info.

    Usage:
        {script} [-h | -l | -L | -v]
        {script} [-d] [-s] TESTS...

    Options:
        TESTS         : Test names for `green`.
        -d,--dryrun   : Just show test names.
        -h,--help     : Show this help message.
        -L,--listall  : List all test names with their full name.
        -l,--list     : List all test cases/names.
        -s,--stdout   : Allow stdout (removes -q from green args).
        -v,--version  : Show version.
""".format(script=SCRIPT, versionstr=VERSIONSTR)


def main(argd):
    """ Main entry point, expects doctopt arg dict as argd. """
    # Use the test directory when no args are given.
    green_exe = get_green_exe()
    if argd['--list'] or argd['--listall']:
        return list_tests(full=argd['--listall'])
    green_args = parse_test_names(argd['TESTS']) or ['test']
    if argd['--dryrun']:
        return print_test_names(green_args)
    cmd = [green_exe, '-vv']
    if not argd['--stdout']:
        cmd.append('-q')
    cmd.extend(green_args)
    print_header(cmd)

    return subprocess.run(cmd).returncode


def get_green_exe():
    """ Get the green executable for this Python version. """
    paths = set(
        s for s in os.environ.get('PATH', '').split(':')
        if s and os.path.isdir(s)
    )
    pyver = '{v.major}.{v.minor}'.format(v=sys.version_info)
    greenmajorexe = 'green{}'.format(sys.version_info.major)
    greenexe = 'green{}'.format(pyver)
    for trypath in paths:
        greenpath = os.path.join(trypath, greenexe)
        greenmajorpath = os.path.join(trypath, greenmajorexe)
        if os.path.exists(greenpath):
            return greenpath
        elif os.path.exists(greenmajorpath):
            return greenmajorpath
    raise MissingDependency('cannot find an executable for `green`.')


def get_test_cases(modulename, package='test'):
    """ Load all TestCase classes by module name. """
    modl = get_test_module(modulename, package=package)
    cases = []
    for attr in dir(modl):
        try:
            val = getattr(modl, attr, None)
        except AttributeError:
            # This can happen in weird cases.
            continue
        if type(val).__name__ != 'type':
            continue
        if issubclass(val, unittest.TestCase):
            cases.append(val())
    return cases


def get_test_files(package='test'):
    """ Load all test_XX.py module names from the test dir. """
    try:
        files = [s for s in os.listdir(package) if s.startswith('test_')]
    except EnvironmentError as ex:
        raise EnvironmentError(
            'Unable to list "test" dir: {}'.format(os.getcwd())
        )
    return [os.path.splitext(s)[0] for s in files]


def get_test_methods(testcase):
    """ Retrieve a list of test method names from a TestCase instance. """
    return [s for s in dir(testcase) if s.startswith('test_')]


def get_test_module(modulename, package='test'):
    """ Load a module object by name. """
    # thispath = sys.path.pop(0)
    cwd = os.getcwd()
    testpath = os.path.join(cwd, package)
    if not os.path.isdir(testpath):
        raise EnvironmentError('Test package not found: {}'.format(testpath))
    if testpath not in sys.path:
        sys.path.insert(0, testpath)
    if cwd not in sys.path:
        sys.path.insert(0, cwd)
    root = os.path.split(cwd)[-1]
    try:
        import_module(package, package=root)
    except ImportError as ex:
        raise ImportError('Cannot import test module: {}'.format(ex))
    try:
        modl = import_module('{}.{}'.format(package, modulename))
    except ImportError as ex:
        raise ImportError('Cannot import module: {}'.format(ex))

    return modl


def get_test_names(package='test'):
    """ Get a flat list of all test modules/cases/names, with their full path.
    """
    yield package
    for modulename, cases in load_test_info(package=package).items():
        yield '.'.join((package, modulename))
        casenames = {type(c).__name__: c for c in cases}
        for casename in sorted(casenames):
            yield '.'.join((package, modulename, casename))
            case = cases[casenames[casename]]
            for methodname in sorted(case):
                yield '.'.join((package, modulename, casename, methodname))


def list_tests(package='test', full=False):
    """ List all discoverable tests. """
    for modulename, cases in load_test_info(package=package).items():
        modulefmt = C(modulename, 'blue', style='bright')
        if not full:
            print(modulefmt(':'))
        casenames = {type(c).__name__: c for c in cases}
        for casename in sorted(casenames):
            case = cases[casenames[casename]]
            casefmt = C(casename, 'cyan')
            if not full:
                print('  {}'.format(casefmt))
            for methodname in sorted(case):
                methodfmt = C(methodname, 'green')
                if full:
                    print(C('.').join(modulefmt, casefmt, methodfmt))
                else:
                    print('    {}'.format(methodfmt))

    return 0


def load_test_info(package='test'):
    """ Return a dict of {file: {testcase: [test_names...]}} """
    if not os.path.isdir(package):
        print_err('Cannot find test package (\'{}\') dir in: {}'.format(
            package,
            os.getcwd(),
        ))
        return {}
    testinfo = {}
    for modulename in get_test_files(package=package):
        testinfo[modulename] = {}
        for case in get_test_cases(modulename):
            testmethods = get_test_methods(case)
            if not testmethods:
                continue
            testinfo[modulename][case] = testmethods
    return testinfo


def parse_test_names(names):
    """ Prepend 'test.' to test names without it.
        Return a list of test names.
    """
    fixed = set()
    for testname in TESTNAMES:

        for i, name in enumerate(names):
            if not name:
                # Already done.
                continue
            if (name == testname) or (testname.endswith(name)):
                fixed.add(testname)
                names[i] = ''
    return sorted(fixed)


def print_err(*args, **kwargs):
    """ A wrapper for print() that uses stderr by default. """
    if kwargs.get('file', None) is None:
        kwargs['file'] = sys.stderr
    print(*args, **kwargs)


def print_header(cmd):
    """ Print some info about the Colr and Green versions being used. """
    textcolors = {'fore': 'cyan'}
    libcolors = {'fore': 'blue', 'style': 'bright'}
    vercolors = {'fore': 'blue'}
    execolors = {'fore': 'green', 'style': 'bright'}
    argcolors = {'fore': 'green'}

    def fmt_app_info(name, ver):
        """ Colorize a library and version number. """
        return C(' v. ', **textcolors).join(
            C(name, **libcolors),
            C(ver, **vercolors)
        )

    def fmt_cmd_args(cmdargs):
        """ Colorize a command and argument list. """
        return C(' ').join(
            C(cmdargs[0], **execolors),
            C(' ').join(C(s, **argcolors) for s in cmdargs[1:]),
        ).join('(', ')', style='bright')

    print('{}\n'.format(
        C(' ').join(
            C('Testing', **textcolors),
            fmt_app_info(APPNAME, APPVERSION),
            C('using', **textcolors),
            fmt_app_info('Green', green_version),
            fmt_cmd_args(cmd),
        )
    ))
    print(
        C(': ').join(
            C('Running from', 'cyan'),
            C(os.getcwd(), 'blue', style='bright'),
        ),
    )


def print_test_names(names):
    """ Print formatted test names. """
    print(C(':').join(
        C('Parsed test names', 'cyan'),
        C(len(names), 'blue', style='bright'),
    ))
    for name in names:
        print(C(name, 'blue'))

    return 0 if names else 1


class InvalidArg(ValueError):
    """ Raised when the user has used an invalid argument. """
    def __init__(self, msg=None):
        self.msg = msg or ''

    def __str__(self):
        if self.msg:
            return 'Invalid argument, {}'.format(self.msg)
        return 'Invalid argument!'


class MissingDependency(EnvironmentError):
    def __init__(self, msg=None):
        self.msg = msg or ''

    def __str__(self):
        if self.msg:
            return 'Missing dependency, {}'.format(self.msg)
        return 'Missing a dependency!'


TESTNAMES = reversed(list(get_test_names()))

if __name__ == '__main__':
    try:
        mainret = main(docopt(USAGESTR, version=VERSIONSTR, script=SCRIPT))
    except (InvalidArg, MissingDependency) as ex:
        print_err(ex)
        mainret = 1
    except (EOFError, KeyboardInterrupt):
        print_err('\nUser cancelled.\n')
        mainret = 2
    except BrokenPipeError:
        print_err('\nBroken pipe, input/output was interrupted.\n')
        mainret = 3
    sys.exit(mainret)
