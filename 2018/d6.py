import string
import logging

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

    return grid

def part2(data):
    return data

def parse(data):
    data = data.splitlines()

    def f(x):
        parts = x.split(',')
        return (int(parts[0]), int(parts[1]))

    # Turn list of coordinates into a dictionary with
    # the key (uppercase letter) as the name
    coords = {}
    for idx, coord in enumerate(list(map(f, data))):
        coords[string.ascii_uppercase[idx]] = coord

    return coords