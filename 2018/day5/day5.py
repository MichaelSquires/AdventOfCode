#!/usr/bin/env python

import re
import sys
import string
import logging
import argparse

def react(polymer, combinations):
    while True:
        size = len(polymer)

        for ptype in combinations:
            polymer = polymer.replace(ptype, '')

        if len(polymer) == size:
            break

    return polymer

def part1(data):
    combinations = []
    for letter in string.ascii_lowercase:
        combinations.append('%s%s' % (letter, letter.upper()))
        combinations.append('%s%s' % (letter.upper(), letter))

    polymer = react(data, combinations)

    logging.debug('DATA: %r', polymer)
    print('Part 1:', len(polymer))

def part2(data):
    combinations = []
    for letter in string.ascii_lowercase:
        combinations.append('%s%s' % (letter, letter.upper()))
        combinations.append('%s%s' % (letter.upper(), letter))

    shortest = len(data)

    for letter in string.ascii_lowercase:
        polymer = react(data.replace(letter, '').replace(letter.upper(), ''), combinations)
        if len(polymer) < shortest:
            shortest = len(polymer)

    print('Part 2:', shortest)

def main(args):

    data = open(args.file, 'rb').read().decode('utf8').strip()

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
    parser.add_argument('file', help='Input file', nargs='?', default='input.txt')

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
