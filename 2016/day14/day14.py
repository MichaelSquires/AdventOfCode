#!/usr/bin/env python

import sys
import hashlib
import logging
import argparse

def main(args):
    data = args.file.read().strip()

    if args.part in (None, 1):
        part1(data)

    if args.part in (None, 2):
        part2(data)

    return 0

TRIPLES = {
    k*3 for k in '0123456789abcdef'
}

def hashfunc(data, rounds=1):
    digest = data
    for i in range(rounds):
        digest = hashlib.md5(digest.encode()).hexdigest()

    return digest

def check_three(digest):
    threes = [triple for triple in TRIPLES if triple in digest]
    lowest = 99
    three = None
    for k in threes:
        index = digest.index(k)
        if index < lowest:
            three = k
        lowest = index

    return three

def check_fives(salt, index, three, rounds=1):
    five = three[0]*5

    found_five = False
    subindex = 0
    while subindex <= 1000:
        subindex += 1
        digest = hashfunc('{}{}'.format(salt, index+subindex), rounds)

        if five not in digest:
            continue

        logging.info('FIVE: %s, digest:%s, index:%d, subindex:%d', five, digest, index, subindex)
        found_five = True

    return found_five

def getkey(salt, rounds=1):
    index = -1
    key = 0
    while key < 64:
        index += 1
        if index % 1000 == 0:
            logging.info('INDEX: %d', index)

        digest = hashfunc('{}{}'.format(salt, index), rounds)
        logging.debug('digest: %s', digest)

        three = check_three(digest)
        if not three:
            continue

        logging.info('THREE:%s, digest:%s, index:%d', three, digest, index)
        if not check_fives(salt, index, three, rounds):
            continue

        logging.info('FOUND KEY %d', key)
        key += 1

    return index

def part1(salt):
    index = getkey(salt)
    print('Part 1:', index)

def part2(salt):
    index = getkey(salt, 2017)
    print('Part 2:', index)

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
    else:
        logging.getLogger().setLevel(logging.INFO)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
