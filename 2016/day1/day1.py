#!/usr/bin/env python

import sys
import logging
import argparse

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Grid:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = NORTH
        self._seen = []
        self.first = None

    @property
    def seen(self):
        return self._seen

    @seen.setter
    def seen(self, coord):
        if coord in self._seen:
            if self.first is None:
                self.first = coord
        self._seen.append(coord)

    def doDirection(self, direction, distance):
        if direction == 'R':
            self.direction += 1
            if self.direction > WEST:
                self.direction = NORTH

        if direction == 'L':
            self.direction -= 1
            if self.direction < NORTH:
                self.direction = WEST

        if self.direction == NORTH:
            for y in range(self.y, self.y + distance):
                self.seen = (self.x, y)
            self.y += distance

        if self.direction == EAST:
            for x in range(self.x, self.x + distance):
                self.seen = (x, self.y)
            self.x += distance

        if self.direction == SOUTH:
            for y in range(self.y, self.y - distance, -1):
                self.seen = (self.x, y)
            self.y -= distance

        if self.direction == WEST:
            for x in range(self.x, self.x - distance, -1):
                self.seen = (x, self.y)
            self.x -= distance

    def doInstruction(self, instruction):
        direction = instruction[0]
        distance = int(instruction[1:])

        if direction not in ('R', 'L'):
            raise Exception('Invalid direction: %s' % (direction))

        self.doDirection(direction, distance)

def main(args):
    # Read and normalize input
    data = args.input.read()
    data = data.replace('\n', '')
    data = data.replace(' ', '')

    instructions = data.split(',')

    part1(instructions)
    part2(instructions)

    return 0

def part1(instructions):
    grid = Grid()

    for instruction in instructions:
        grid.doInstruction(instruction)

    print('Part 1:', (grid.x, grid.y))
    print('Part 1:', grid.x + grid.y)

def part2(instructions):
    grid = Grid()

    for instruction in instructions:
        grid.doInstruction(instruction)

    print('Part 2:', grid.first)
    print('Part 2:', grid.first[0] + grid.first[1])

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
