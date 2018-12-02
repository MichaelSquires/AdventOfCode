#!/usr/bin/env python

import sys
import logging
import argparse
import itertools

def count(line):
    d = {}
    for k in line:
        if k not in d:
            d[k] = 0
        d[k] += 1

    twos = False
    threes = False

    values = d.values()
    logging.debug('D: %s', d)
    logging.debug('VALUES: %s', values)

    if 2 in values:
        twos = True

    if 3 in values:
        threes = True

    return (twos, threes)

def part1(data):

    twos = 0
    threes = 0

    for line in data:
        _twos, _threes = count(line)
        if _twos:
            twos += 1

        if _threes:
            threes += 1

    logging.info('TWOS: %d', twos)
    logging.info('THREES: %d', threes)

    print('Part 1:', twos * threes)

def part2(data):

    while True:
        curr = list(data.pop())

        found = None

        for k in data:
            k = list(k)
            diff = []
            for i in range(len(curr)):
                diff.append(curr[i] - k[i])

            if diff.count(0) == len(curr) - 1:
                logging.info('FOUND', bytes(curr), bytes(k))
                found = (curr, k)
                break

        if found:
            a,b = found
            answer = []
            for k in range(len(a)):
                if a[k] == b[k]:
                    answer.append(a[k])

            break

    print('Part 2:', bytes(answer).decode('utf-8'))

def main(args):

    lines = open(args.file, 'rb').readlines()
    data = [k.strip() for k in lines]

    if args.part in (None, 1):
        part1(data)

    if args.part in (None, 2):
        part2(data)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[0, 1, 2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    parser.add_argument('file', help='Input file')

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
