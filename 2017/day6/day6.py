#!/usr/bin/env python

import sys
import copy
import logging
import argparse
import itertools

def main(args):
    buckets = []
    data = args.file.read()
    data = data.strip()
    data = data.split()
    buckets = list(map(int, data))

    if args.part in (None, 1):
        buckets = part1(copy.copy(buckets))

    if args.part in (None, 2):
        part2(copy.copy(buckets))

    return 0

def part1(buckets):
    count = 0
    seen = []
    blen = len(buckets)
    while buckets not in seen:
        count += 1
        seen.append(copy.copy(buckets))

        logging.debug('buckets: %r', buckets)

        hi = max(buckets)
        idx = buckets.index(hi)
        logging.debug('hi %d, idx %d', hi, idx)

        buckets[idx] = 0
        for i in range(hi):
            buckets[(idx + 1 + i) % blen] += 1

        logging.debug('buckets: %r', buckets)

    print('Part 1:', count)
    return buckets

def part2(buckets):
    count = 0
    seen = []
    blen = len(buckets)
    start = copy.copy(buckets)
    while start not in seen:

        logging.debug('buckets: %r', buckets)

        hi = max(buckets)
        idx = buckets.index(hi)
        logging.debug('hi %d, idx %d', hi, idx)

        buckets[idx] = 0
        for i in range(hi):
            buckets[(idx + 1 + i) % blen] += 1

        logging.debug('buckets: %r', buckets)

        count += 1
        seen.append(copy.copy(buckets))

    print('Part 2:', count)

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
t
