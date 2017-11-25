#!/usr/bin/env python

import sys
import argparse
import traceback

verbose = False

def part1(data):
    return len(data.replace(')', '')) - len(data.replace('(', ''))

def part2(data):
    floor = 0
    position = 0

    for position in range(len(data)):
        if data[position] == '(':
            floor += 1
        else:
            floor -= 1

        if floor == -1:
            return position + 1

        position += 1

    raise Exception('Does not enter basement')

def main(args):

    data = args.file.read()

    print 'Part1: {:d}'.format(part1(data))
    print 'Part2: {:d}'.format(part2(data))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
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
