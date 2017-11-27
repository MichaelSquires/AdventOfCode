#!/usr/bin/env python

import sys
import hashlib
import logging
import argparse

def main(args):
    doorid = args.id.strip()
    print ('Using door ID: %r' % (doorid))

    if args.part in (None, 1):
        part1(doorid)

    if args.part in (None, 2):
        part2(doorid)

    return 0

def part1(doorid):
    index = 0
    digest = ''
    password = ''

    while len(password) < 8:
        while not digest.startswith('00000'):
            index += 1
            if index % 1000000 == 0:
                print('-->', index)
            digest = hashlib.md5('{:s}{:d}'.format(doorid, index).encode()).hexdigest()

        print('INDEX:', index, digest)
        password += digest[5]
        digest = ''

    print('Part 1:', password)

def part2(doorid):
    index = 0
    digest = ''
    password = [None]*8
    hexvals = '0123456789abcdef'

    while None in password:
        digest = ''
        while not digest.startswith('00000'):
            index += 1
            if index % 1000000 == 0:
                print('-->', index)
            digest = hashlib.md5('{:s}{:d}'.format(doorid, index).encode()).hexdigest()

        print('INDEX:', index, digest)

        position = hexvals.index(digest[5])
        print('POSITION:', position)
        if position >= len(password):
            continue

        value = digest[6]
        print('VALUE:', value)

        if password[position] is None:
            password[position] = value

    print('Part 2:', ''.join(password))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('id', help='Door ID')

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
