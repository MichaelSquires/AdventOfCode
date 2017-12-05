#!/usr/bin/env python

import sys
import logging
import argparse
import itertools

def main(args):
    passwords = []
    for password in args.file.readlines():
        password = password.strip()

        words = password.split()

        passwords.append(words)

    if args.part in (None, 1):
        passwords = part1(passwords)

    if args.part in (None, 2):
        part2(passwords)

    return 0

def part1(passwords):
    valid = []
    for password in passwords:

        wordset = set(password)

        if len(wordset) == len(password):
            valid.append(password)

        logging.debug('Invalid password: %s', password)

    print('Part 1:', len(valid))
    return valid

def part2(passwords):
    valid = 0
    for password in passwords:

        anagrams = []
        for word in password:
            # Get all permutations
            p = list(itertools.permutations(word))

            # Reduce to unique permutations
            p = list(set(p))

            # Extend list
            anagrams.extend(p)

        wordset = set(anagrams)

        if len(wordset) == len(anagrams):
            valid += 1
            continue

        logging.debug('Invalid password: %s', password)

    print('Part 2:', valid)

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
