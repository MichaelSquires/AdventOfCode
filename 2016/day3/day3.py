#!/usr/bin/env python

import re
import sys
import logging
import argparse

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @property
    def possible(self):
        return (
            self.a + self.b > self.c and
            self.b + self.c > self.a and
            self.a + self.c > self.b
        )

regex = re.compile(r'^\s+(\d+)\s+(\d+)\s+(\d+)$')

def main(args):
    dimensions = []
    for line in args.input.readlines():
        m = regex.match(line)

        dimensions.append((
            int(m.group(1)),
            int(m.group(2)),
            int(m.group(3))
        ))

    part1(dimensions)
    part2(dimensions)

    return 0

def part1(dimensions):
    possible = 0

    for a,b,c in dimensions:
        triangle = Triangle(a, b, c)
        if triangle.possible:
            possible += 1

    print('Part 1:', possible)

def part2(dimensions):
    possible = 0

    for y in range(0, len(dimensions) - 2, 3):
        for x in range(3):
            a = dimensions[y+0][x]
            b = dimensions[y+1][x]
            c = dimensions[y+2][x]
            triangle = Triangle(a, b, c)
            if triangle.possible:
                possible += 1

    print('Part 2:', possible)

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
