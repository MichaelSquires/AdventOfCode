#!/usr/bin/env python

import sys
import hashlib
import logging
import argparse
import itertools

def main(args):
    messages = args.file.readlines()

    if args.part in (None, 1):
        part1(messages)

    if args.part in (None, 2):
        part2(messages)

    return 0

def decode(messages, reverse=True):
    message = []

    for i in range(len(messages[0])):
        d = {}
        letters = [k[i] for k in messages]

        for letter in letters:
            if letter not in d:
                d[letter] = 0
            d[letter] += 1

        def keyfunc(x):
            return x[1]

        letters = sorted(d.items(), key=keyfunc, reverse=reverse)
        groups = []
        for k, g in itertools.groupby(letters, key=keyfunc):
            groups.append(sorted(g))

        letter = list(itertools.chain.from_iterable(groups))[0]

        message += letter[0]

    return ''.join(message)

def part1(messages):

    message = decode(messages)
    print('Part 1:', message)

def part2(messages):
    message = decode(messages, False)
    print('Part 2:', message)

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
