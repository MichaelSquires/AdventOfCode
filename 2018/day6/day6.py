#!/usr/bin/env python

import sys
import pprint
import string
import logging
import argparse

class Location:
    def __init__(self):
        self.name = '-'
        self.distances = {}

    def set(self, node, distance):
        self.distances[node] = distance

    def __repr__(self):
        return '%s' % (self.name)
#        return '%s' % (len(self.bar))

class Grid:
    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._grid = [[None for i in range(width)] for i in range(height)]


def part1(coords):
    # Find bounds of grid
    lo_x = 1000
    lo_y = 1000
    hi_x = 0
    hi_y = 0
    for x,y in coords.values():
        if x < lo_x:
            lo_x = x

        if x > hi_x:
            hi_x = x

        if y < lo_y:
            lo_y = y

        if y > hi_y:
            hi_y = y

    logging.info('LOW: %d,%d, HI: %d,%d', lo_x, lo_y, hi_x, hi_y)

    grid = [[Location() for i in range(hi_x + 2)] for i in range(hi_y + 2)]

    for name,(x,y) in coords.items():
        print(name, x, y)
        grid[y][x].name = name

    print('Part 1:')
    pprint.pprint(grid)

def part2(data):
    print('Part 2:', data)

def main(args):

    data = open(args.file, 'r').read().splitlines()

    def f(x):
        parts = x.split(',')
        return (int(parts[0]), int(parts[1]))

    # Turn list of coordinates into a dictionary with
    # the key (uppercase letter) as the name
    coords = {}
    name_idx = 0
    for coord in list(map(f, data)):
        coords[string.ascii_uppercase[name_idx]] = coord
        name_idx += 1

    if args.part in (None, 1):
        part1(coords)

    if args.part in (None, 2):
        part2(coords)

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
