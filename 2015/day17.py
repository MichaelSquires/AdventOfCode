#!/usr/bin/env python

import sys
import pprint
import argparse
import itertools
import traceback

verbose = False

TOTAL_VOLUME = 150

def part1(data):
    ret = 0
    
    for i in range(2, len(data)):
        for k in itertools.combinations(data, i):
            if sum(k) == TOTAL_VOLUME:
                ret += 1
    return ret

def part2(data):
    ret = len(data)
    for i in range(2, len(data)):
        for k in itertools.combinations(data, i):
            if sum(k) != TOTAL_VOLUME:
                continue

            length = len(k)
            if length < ret:
                if verbose:
                    print k, length
                ret = length

    return ret

def main(args):

    data = args.file.readlines()

    data = [int(k) for k in data]

    if verbose:
        pprint.pprint(data)

    print 'Part1: {:d}'.format(part1(data))
    print 'Part2: {:d}'.format(part2(data))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-i', '--interact', help='Show verbose messages', action='store_true')
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=file)

    args = parser.parse_args()
    verbose = args.verbose

    try:
        sys.exit(main(args))
    except Exception as exc:
        print 'ERROR: %s' % (exc)
        if verbose:
            traceback.print_exc()
        sys.exit(-1)
