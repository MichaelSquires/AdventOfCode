#!/usr/bin/env python

import sys
import logging
import argparse

def main(args):

    firewall = {}
    for line in args.file.readlines():
        line = line.strip()

        depth, range_ = line.split(': ')
        depth = int(depth)
        range_ = int(range_)

        firewall[depth] = range_

    if args.part in (None, 1):
        part1(firewall)

    if args.part in (None, 2):
        part2(firewall)

    return 0

def scanner(depth, range_, delay=0):
    return (depth + delay) % (2 * range_ - 2)

def part1(firewall):
    caught = []

    for depth in range(max(firewall)+1):
        range_ = firewall.get(depth)
        if range_ is None:
            continue

        scan = scanner(depth, range_)
        logging.debug('SCAN: %d', scan)
        if scan == 0:
            caught.append(depth)

    severity = 0
    for depth in caught:
        severity += depth * firewall[depth]

    print('Part 1:', severity)

def part2(firewall):
    for delay in range(2**32):
        passed = True
        for depth in range(max(firewall)+1):
            range_ = firewall.get(depth)
            if range_ is None:
                continue

            if scanner(depth, range_, delay) == 0:
                passed = False
                break

        if passed:
            break

    print('Part 2:', delay)

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
