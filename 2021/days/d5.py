import logging
import collections

import utils

Point = collections.namedtuple('Point', ['x', 'y'])
Line = collections.namedtuple('Line', ['start', 'end'])

def parse(data):
    ret = []
    lines = data.splitlines()
    for line in lines:
        start, end = line.split('->')

        start = Point(*[int(k) for k in start.split(',')])
        end = Point(*[int(k) for k in end.split(',')])
        ret.append(Line(start, end))

    return ret


class Grid(utils.Grid):
    def inc(self, x, y):
        logging.debug('X: %s, Y: %s (%d)', x, y, x + self.width * y)
        self[x, y] += 1

    def print(self):
        for yy in range(self.height):
            height = self.width * yy
            print(self._grid[0 + height:self.width + height])

    def do_horizontal(self, line):
        start = min(line.start.y, line.end.y)
        end = max(line.start.y, line.end.y)
        for ii in range(start, end + 1):
            self.inc(line.start.x, ii)

    def do_vertical(self, line):
        start = min(line.start.x, line.end.x)
        end = max(line.start.x, line.end.x)
        for ii in range(start, end + 1):
            self.inc(ii, line.start.y)

    def do_diagonal(self, line):
        stepx = 1
        startx = line.start.x
        endx = line.end.x
        if line.start.x > line.end.x:
            stepx = -1

        stepy = 1
        starty = line.start.y
        endy = line.end.y
        if line.start.y > line.end.y:
            stepy = -1

        while startx != endx + stepx and starty != endy + stepy:
            logging.debug('STARTX %s, STARTY %s', startx, starty)
            self.inc(startx, starty)
            startx += stepx
            starty += stepy

    def do_line(self, line):
        logging.info('LINE: %s', line)

        if line.start.x != line.end.x and line.start.y != line.end.y:
            self.do_diagonal(line)
        elif line.start.x == line.end.x:
            self.do_horizontal(line)
        else:
            self.do_vertical(line)


def gridsize(lines):
    all_x = []
    all_x.extend([line.start.x for line in lines])
    all_x.extend([line.end.x for line in lines])

    all_y = []
    all_y.extend([line.start.y for line in lines])
    all_y.extend([line.end.y for line in lines])

    width = max(all_x)
    height = max(all_y)

    return height, width

def part1(data):
    height, width = gridsize(data)
    grid = Grid(height + 1, width + 1)

    for line in data:
        # Skip diagonal lines
        if line.start.x != line.end.x and line.start.y != line.end.y:
            logging.info('SKIP: %s', line)
            continue

        grid.do_line(line)

    if grid.width < 80:
        grid.print()

    return len([k for k in grid._grid if k > 1])

def part2(data):
    height, width = gridsize(data)
    grid = Grid(height + 1, width + 1)

    for line in data:
        grid.do_line(line)

    if grid.width < 80:
        grid.print()

    return len([k for k in grid._grid if k > 1])
