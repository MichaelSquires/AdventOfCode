#!/usr/bin/env python

import sys
import copy
import logging
import argparse
import collections

def main(args):

    steps = int(args.file.read().strip())

    if args.part in (None, 1):
        part1(steps)

    if args.part in (None, 2):
        part2(steps)

    return 0

def part1(steps):
    spins = 2017
    buf = collections.deque([0])
    curpos = 0

    adj = 0
    for i in range(1,spins+1):
        index = (curpos + steps) % i
        buf.insert(index, i)
        curpos = index + 1

    n = buf.index(2017)

    print('Part 1:', buf[n+1])

def part2(steps):
    spins = 50000000
    curpos = 0

    adj = 0
    for i in range(1,spins+1):
        index = (curpos + steps) % i
        curpos = index + 1
        if curpos == 1:
            adj = i

    print('Part 2:', adj)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    parser.add_argument('file', help='Input file', type=open)

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
