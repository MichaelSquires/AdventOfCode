#!/usr/bin/env python

import re
import sys
import string
import hashlib
import logging
import argparse
import itertools

regex = re.compile(r'\w+|\[\w+\]')

class Address:
    def __init__(self, address):
        self.address = address
        self.hypernets = []
        self.supernets = []

        for match in regex.findall(self.address):
            if match.startswith('['):
                self.hypernets.append(match)
            else:
                self.supernets.append(match)

    def __repr__(self):
        return '<Address: %s>' % (self.address)

    def hasAbba(self):
        abba = []
        perms = itertools.permutations(string.ascii_lowercase, 2)
        for perm in perms:
            val = ''.join((perm[0], perm[1], perm[1], perm[0]))
            abba.append(val)

        hasAbba = False
        supernets = ' '.join(self.supernets)
        for val in abba:
            if val in supernets:
                hasAbba = True
                break

        if hasAbba:
            hypernets = ' '.join(self.hypernets)
            for val in abba:
                if val in hypernets:
                    hasAbba = False
                    break

        return hasAbba

def main(args):
    addresses = []
    data = args.file.readlines()
    for line in data:
        addresses.append(
            Address(line.strip())
        )

    if args.part in (None, 1):
        part1(addresses)

    if args.part in (None, 2):
        part2(addresses)

    return 0

def part1(addresses):
    hastls = 0

    for address in addresses:
        if address.hasAbba():
            hastls += 1

    print('Part 1:', hastls)

def part2(addresses):
    print('Part 2:', addresses)

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
