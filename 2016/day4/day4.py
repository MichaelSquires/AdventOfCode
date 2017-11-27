#!/usr/bin/env python

import re
import sys
import string
import logging
import argparse
import itertools

class Room:
    def __init__(self, room, sector, checksum):
        self.room = room
        self.sector = sector
        self.checksum = checksum

    def __repr__(self):
        return '<Room %s [%s] %d>' % (self.room, self.checksum, self.sector)

    def computeChecksum(self):
        d = {}

        letters = self.room.replace('-', '')
        for letter in letters:
            if letter not in d:
                d[letter] = 0
            d[letter] += 1

        def keyfunc(x):
            return x[1]

        letters = sorted(d.items(), key=keyfunc, reverse=True)
        groups = []
        for k, g in itertools.groupby(letters, key=keyfunc):
            groups.append(sorted(g))

        checksum = ''
        for val in itertools.chain.from_iterable(groups):
            checksum += val[0]

            if len(checksum) == 5:
                break

        return checksum

    def _shift(self, letter):
        amount = self.sector % 26
        table = string.ascii_lowercase + string.ascii_lowercase

        return table[table.index(letter) + amount]

    def decrypt(self):
        plaintext = ''

        for letter in self.room:
            if letter == '-':
                plaintext += ' '
                continue

            plaintext += self._shift(letter)

        return plaintext

regex = re.compile(r'^([a-z-]+)-(\d+)\[([a-z]+)\]$')

def main(args):
    rooms = []
    for line in args.input.readlines():
        m = regex.match(line)

        rooms.append(
            Room(
                m.group(1),
                int(m.group(2)),
                m.group(3)
            )
        )

    part1(rooms)
    part2(rooms)

    return 0

def part1(rooms):
    total = 0

    for room in rooms:
        if room.checksum == room.computeChecksum():
            total += room.sector

    print('Part 1:', total)

def part2(rooms):

    sector = 0
    for room in rooms:
        name = room.decrypt()
        if 'north' in name:
            sector = room.sector
            break

    print('Part 2:', sector)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('input', help='Input file', type=open)

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
