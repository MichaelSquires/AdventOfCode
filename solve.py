#!/usr/bin/env python

import sys
import code
import copy
import inspect
import logging
import argparse
import datetime
import importlib

import utils

NOW = datetime.datetime.now()

def main(args):

    year = args.year
    if year == 0:
        year = NOW.year

    try:
        # Retrieve module for given year and day
        mod = importlib.import_module(f'{year}.d{args.day}')
        if mod is None:
            raise NotImplemented(f'{year}.d{args.day}')

    except ModuleNotFoundError:
        logging.error(f'Module {year}/d{args.day}.py not found. Creating template')
        utils.template(year, args.day)
        return -1

    # Get functions from module and validate them
    parse = getattr(mod, 'parse', None)
    part1 = getattr(mod, 'part1')
    part2 = getattr(mod, 'part2')

    if ((parse is not None and not inspect.isfunction(parse)) or
        not inspect.isfunction(part1) or
        not inspect.isfunction(part2)):
        raise Exception('Invalid day module')

    if not args.no_download:
        utils.download(year, args.day)

    filename = args.file
    if not filename:
        filename = f'inputs/{year}/d{args.day}.txt'

    # Read data from input file
    data = open(filename, 'rb').read().decode('utf8')

    # Optionally parse data into a different format
    if parse is not None:
        data = parse(data)
        logging.debug('DATA: %s', data)

    if args.interact:
        code.interact(local=locals())

    # Optionally run part 1
    if args.part in (None, 1):
        ret = part1(copy.deepcopy(data))
        print(f'PART1: {ret}')

    # Optionally run part 2
    if args.part in (None, 2):
        ret = part2(copy.deepcopy(data))
        print(f'PART2: {ret}')

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-i', '--interact', help='Interact with data', action='store_true')
    parser.add_argument('-n', '--no-download', help='Do not check and download input data', action='store_true')
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[0, 1, 2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)
    parser.add_argument('-y', '--year', help='Specify year to play', type=int, default=NOW.year)

    # Positional arguments
    parser.add_argument('day', help='Day to solve', type=int, choices=range(1,26))
    parser.add_argument('file', help='Input file', nargs='?')

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
