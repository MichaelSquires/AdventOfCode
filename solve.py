#!/usr/bin/env python

import sys
import code
import copy
import time
import pstats
import logging
import pathlib
import argparse
import cProfile
import datetime
import importlib

import utils

NOW = datetime.datetime.now()

def runpart(func, data, profile=False):
    copied = copy.deepcopy(data)

    if profile:
        profiler = cProfile.Profile()
        profiler.enable()

    start = time.time()

    try:
        ret = func(copied)
    except KeyboardInterrupt:
        logging.warning('Caught Ctrl-C')

    end = time.time()

    if args.profile:
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('tottime')
        stats.print_stats()

    exectime = (end - start) * 1000

    if ret is not None:
        print(f'{func.__name__}: ({exectime:.04f}ms) {ret}')

    if ret is None:
        exectime = 0.0

    return exectime

def main(args):  # pylint: disable=redefined-outer-name

    year = args.year
    if year == 0:
        year = NOW.year

    if not (yeardir := pathlib.Path(str(year))).exists():
        yeardir.mkdir()

    if not (modfile := pathlib.Path(f'{year}/d{args.day}.py')).exists():
        logging.error('Module %s not found. Creating template', modfile)
        utils.template(modfile)
        return -1

    try:
        # Retrieve module for given year and day
        mod = importlib.import_module(f'{year}.d{args.day}')
        if mod is None:
            raise NotImplementedError(f'{year}.d{args.day}')

    except ModuleNotFoundError as exc:
        logging.error('Error importing module: %s/%s.py: %s', year, args.day, exc)
        return -1

    if args.challenge:
        if mod.__doc__ is not None:
            raise Exception(f'Challenge text already retrieved: {mod.__doc__}')
        utils.challenge(year, args.day)
        return

    # Get functions from module and validate them
    parse = getattr(mod, 'parse', None)
    sample = getattr(mod, 'SAMPLE', None)
    part1 = getattr(mod, 'part1')
    part2 = getattr(mod, 'part2')

    if ((parse is not None and not callable(parse)) or
        not callable(part1) or
        not callable(part2)):
        raise Exception('Invalid day module')

    if not args.no_download:
        utils.download(year, args.day)

    filename = args.file
    if not filename:
        filename = pathlib.Path(f'inputs/{year}/d{args.day}.txt')

    # Read data from input file. Wrap it in a list because the samples imported
    # from a module could be a list that we want to iterate over. This just
    # makes the code easier since it can just iterate over the single element in
    # the list
    data = [filename.read_text()]

    # If the module has sample data, and we're in the debugger
    if sample is not None and (sys.gettrace() is not None or args.sample):
        if not isinstance(sample, list):
            sample = [sample]
        data = sample

    if not args.sample:
        assert len(data) == 1

    p1time = None
    p2time = None

    for datum in data:
        # Optionally parse data into a different format
        if parse is not None:
            datum = parse(datum)
            logging.debug('DATA: %s', datum)

        if args.interact:
            code.interact(local=locals())

        # Optionally run part 1
        if args.part in (None, 1):
            p1time = runpart(part1, datum, profile=args.profile)

        # Optionally run part 2
        if args.part in (None, 2):
            p2time = runpart(part2, datum, profile=args.profile)

    if not args.sample and not args.no_exectime:
        utils.exectime(args.year, args.day, p1time, p2time)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-c', '--challenge', help='Download challenge text', action='store_true')
    parser.add_argument('-e', '--no-exectime', help='Do not record execution time', action='store_true')
    parser.add_argument('-i', '--interact', help='Interact with data', action='store_true')
    parser.add_argument('-n', '--no-download', help='Do not check and download input data', action='store_true')
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[0, 1, 2])
    parser.add_argument('-P', '--profile', help='Profile parts', action='store_true')
    parser.add_argument('-s', '--sample', help='Use the sample data if available', action='store_true')
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)
    parser.add_argument('-y', '--year', help='Specify year to play', type=int, default=NOW.year)

    # Positional arguments
    parser.add_argument('day', help='Day to solve', type=int, choices=range(1,26))
    parser.add_argument('file', help='Input file. Defaults to inputs/$YEAR/d$DAY.txt', nargs='?', type=pathlib.Path)

    args = parser.parse_args()
    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose == 2 or sys.gettrace() is not None:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as fatal:  # pylint: disable=broad-except
        logging.exception('ERROR in main: %s', fatal)
        sys.exit(-1)
