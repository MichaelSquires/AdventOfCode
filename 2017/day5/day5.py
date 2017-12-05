#!/usr/bin/env python

import sys
import copy
import logging
import argparse
import itertools

def main(args):
    offsets = []
    for offset in args.file.readlines():
        offset = int(offset.strip())
        offsets.append(offset)

    if args.part in (None, 1):
        part1(copy.copy(offsets))

    if args.part in (None, 2):
        part2(copy.copy(offsets))

    return 0

def part1(offsets):
    pc = 0
    count = 0
    while pc >= 0 and pc <= len(offsets):
        try:
            logging.debug('pc %d, offset %d', pc, offsets[pc])
            nextpc = pc + offsets[pc]
            offsets[pc] += 1
            pc = nextpc
            count += 1
        except IndexError:
            break

    print('Part 1:', count)

def part2(offsets):
    pc = 0
    count = 0
    while pc >= 0 and pc <= len(offsets):
        try:
            logging.debug('pc %d, offset %d', pc, offsets[pc])
            nextpc = pc + offsets[pc]
            curr = offsets[pc]
            if curr >= 3:
                offsets[pc] -= 1
            else:
                offsets[pc] += 1
            pc = nextpc
            count += 1
        except IndexError:
            break

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
