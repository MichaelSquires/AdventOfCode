#!/usr/bin/env python

import sys
import code
import copy
import inspect
import logging
import argparse
import importlib

import days

MODULES = {}

for ii in range(1,26):
    try:
        MODULES[ii] = importlib.import_module(f'days.d{ii}')
    except ModuleNotFoundError:
        MODULES[ii] = None

def main(args):

    # Retrieve module for given day
    mod = MODULES.get(args.day)
    if mod is None:
        raise NotImplemented(f'Day {args.day}')

    # Get functions from module and validate them
    parse = getattr(mod, 'parse', None)
    part1 = getattr(mod, 'part1')
    part2 = getattr(mod, 'part2')

    if ((parse is not None and not inspect.isfunction(parse)) or
        not inspect.isfunction(part1) or
        not inspect.isfunction(part2)):
        raise Exception('Invalid day module')

    # Read data from input file
    data = open(args.file, 'rb').read().decode('utf8')

    # Optionally parse data into a different format
    if parse is not None:
        data = parse(data)
        logging.debug('DATA: %s', data)

    if args.interact:
        code.interact(local=locals())

    # Optionally run part 1
    if args.part in (None, 1):
        ret = part1(copy.copy(data))
        print(f'PART1: {ret}')

    # Optionally run part 2
    if args.part in (None, 2):
        ret = part2(copy.copy(data))
        print(f'PART2: {ret}')

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-i', '--interact', help='Interact with data', action='store_true')
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[0, 1, 2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    parser.add_argument('day', help='Day to solve', type=int, choices=range(1,26))
    parser.add_argument('file', help='Input file', nargs='?', default='input.txt')

    args = parser.parse_args()
    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
