#!/usr/bin/env python

import sys
import logging
import argparse

def main(args):
    data = args.file.read().strip()

    if args.part in (None, 1):
        part1(data)

    if args.part in (None, 2):
        part2(data)

    return 0

def part1(data):
    total = 0
    for i in range(len(data) - 1):
        if data[i] != data[i+1]:
            continue

        logging.debug('%s == %s', data[i], data[i+1])
        total += int(data[i])

    if data[-1] == data[0]:
        total += int(data[-1])

    print('Part 1:', total)

def part2(data):
    total = 0
    dlen = len(data)
    half = dlen/2
    for i in range(dlen):
        idx = int((i+half)%dlen)
        if data[i] != data[idx]:
            continue

        logging.debug('%s == %s', data[i], data[idx])
        total += int(data[i])

    print('Part 2:', total)

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
