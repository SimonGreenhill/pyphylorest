# coding=utf-8
"""
Main command line interface of the phlorest package.

Like programs such as git, this cli splits its functionality into sub-commands
(see e.g. https://docs.python.org/2/library/argparse.html#sub-commands).

The rationale behind this is that while a lot of different tasks may be
triggered using this cli, most of them require common configuration.
The basic invocation looks like
    phlorest [OPTIONS] <command> [args]
"""
import sys
from clldutils.clilib import ArgumentParserWithLogging

import phlorest
from phlorest import commands
assert commands


def main():  # pragma: no cover
    parser = ArgumentParserWithLogging(phlorest.__name__)
    parser.add_argument(
        '--repos',
        type=phlorest.Repos,
        default=phlorest.Repos('phlorest'),
        help='Location of clone of phlorest data (defaults to ./phlorest)')
    sys.exit(parser.main())
