import re
import math
import logging

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

def parse(data):
    directions = data.strip().split(',')

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

    return grid

def part1(grid):
    return grid.distance

def part2(grid):
    return grid.farthest