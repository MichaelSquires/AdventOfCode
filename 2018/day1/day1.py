#!/usr/bin/env python

import sys
import logging
import pathlib
import argparse

def part1(data):
    return sum(data)

def part2(data):
    freq = 0
    # I originally had a list here that I would append seen frequencies
    # to but that turned out to slow enough that I wasn't patient enough
    # to let it finish. The dictionary wound up being incredibly fast -
    # less than one second.
    seen = {}

    while True:
        for k in data:
            freq += k
            if freq in seen:
                return freq

            seen[freq] = 0

def main(args):
    lines = pathlib.Path(args.file).read_text().split('\n')

    data = [int(k) for k in lines if k]

    print('PART1: %d' % (part1(data)))
    print('PART2: %d' % (part2(data)))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file')

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s' % (exc))
        sys.exit(-1)
