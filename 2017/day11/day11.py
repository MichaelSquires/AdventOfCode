#!/usr/bin/env python

import re
import sys
import math
import logging
import argparse

# See the following URL for coordinate system
# http://3dmdesign.com/development/hexmap-coordinates-the-easy-way

class Grid:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.farthest = 0

    @property
    def distance(self):
        x = 0 - self.x
        y = 0 - self.y
        d = x - y
        return max(abs(x), abs(y), abs(d))

    def north(self):
        self.y += 1
        self.farthest = max(self.farthest, self.distance)

    def south(self):
        self.y -= 1
        self.farthest = max(self.farthest, self.distance)

    def northwest(self):
        self.x -= 1
        self.farthest = max(self.farthest, self.distance)

    def northeast(self):
        self.y += 1
        self.x += 1
        self.farthest = max(self.farthest, self.distance)

    def southwest(self):
        self.y -= 1
        self.x -= 1
        self.farthest = max(self.farthest, self.distance)

    def southeast(self):
        self.x += 1
        self.farthest = max(self.farthest, self.distance)

def main(args):

    directions = args.file.read().strip().split(',')

    grid = Grid()
    for direction in directions:
        logging.debug('DIRECTION: %s', direction)
        {
            'n': grid.north,
            's': grid.south,
            'nw': grid.northwest,
            'ne': grid.northeast,
            'sw': grid.southwest,
            'se': grid.southeast,
        }.get(direction)()


    if args.part in (None, 1):
        part1(grid)

    if args.part in (None, 2):
        part2(grid)

    return 0

def part1(grid):
    print('Part 1:', grid.distance)

def part2(grid):
    print('Part 2:', grid.farthest)

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
