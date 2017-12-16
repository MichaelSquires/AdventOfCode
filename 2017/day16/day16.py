#!/usr/bin/env python

import sys
import copy
import logging
import argparse

def spin(programs, count):
    return programs[count*-1:] + programs[:count*-1]

def exchange(programs, a, b):
    logging.debug('A: %d, B: %d', a, b)
    aval = programs[a]
    bval = programs[b]
    logging.debug('AVAL: %s, BVAL: %s', aval, bval)
    programs[a] = bval
    programs[b] = aval
    return programs

def partner(programs, a, b):
    aidx = programs.index(a)
    bidx = programs.index(b)
    logging.debug('AIDX: %d, BIDX: %d', aidx, bidx)

    aval = programs[aidx]
    bval = programs[bidx]
    logging.debug('AVAL: %s, BVAL: %s', aval, bval)

    programs[aidx] = bval
    programs[bidx] = aval
    return programs

def main(args):

    data = args.file.read().strip().split(',')

    if args.part in (None, 1):
        part1(data)

    if args.part in (None, 2):
        part2(data)

    return 0

def dance(programs, data):
    for move in data:
        logging.debug('MOVE: %s', move)
        logging.debug('PROGRAMS: %r', programs)
        if move[0] == 's':
            programs = spin(programs, int(move[1:]))

        elif move[0] == 'x':
            a, b = move[1:].split('/')
            a = int(a)
            b = int(b)
            programs = exchange(programs, a, b)

        elif move[0] == 'p':
            a, b = move[1:].split('/')
            programs = partner(programs, a, b)

    return programs

def part1(data):
    programs = dance(list('abcdefghijklmnop'), data)

    print('Part 1:', ''.join(programs))

def part2(data):
    programs = list('abcdefghijklmnop')

    combinations = [copy.copy(programs)]
    for i in range(1000000000):
        programs = dance(programs, data)
        combinations.append(copy.copy(programs))

        if i == 0:
            first = copy.copy(programs)
            continue

        if programs == first:
            break

    idx = 1000000000 % i

    print('Part 2:', ''.join(combinations[idx]))

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
