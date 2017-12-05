#!/usr/bin/env python

import csv
import sys
import logging
import argparse
import itertools

def main(args):
    data = []
    for line in csv.reader(args.file, delimiter='\t'):
        data.append([int(k) for k in line])

    for row in data:
        logging.debug(row)

    if args.part in (None, 1):
        part1(data)

    if args.part in (None, 2):
        part2(data)

    return 0

def part1(data):
    checksum = 0
    for row in data:
        lo = min(row)
        hi = max(row)
        diff = hi - lo
        logging.debug('hi %d, lo %d, diff %d, csum %d', hi, lo, diff, checksum)
        checksum += diff

    print('Part 1:', checksum)

def part2(data):
    checksum = 0
    def div(a):
        return a[0]/a[1]

    for row in data:
        logging.debug('row %r', row)
        combinations = itertools.permutations(row, 2)
        results = map(div, combinations)
        result = None
        for r in results:
            logging.debug('r %r', r)
            if r.is_integer():
                result = r
                break

        if result is None:
            raise Exception('Result not found for row: %r' % (row))

        checksum += result

    print('Part 2:', checksum)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=open)

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
