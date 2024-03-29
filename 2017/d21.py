import re
import logging

import numpy as np

START = '.#./..#/###'

class Grid:
    def __init__(self, grid):
        self.grid = np.array(
            [list(k) for k in grid.split('/')]
        )

    @classmethod
    def fromNpArray(cls, array):
        inst = cls('')
        inst.grid = array
        return inst

    @property
    def size(self):
        return len(self.grid)

    def like(self, other):
        assert isinstance(other, Grid)

        if other.size != self.size:
            return False

        us = self.grid
        them = other.grid

        if np.array_equal(them, us):
            return True

        for i in range(4):
            us = np.rot90(us)
            if np.array_equal(them, us):
                return True

            if np.array_equal(them, np.flipud(us)):
                return True

            if np.array_equal(them, np.fliplr(us)):
                return True

#            if np.array_equal(them, np.fliplr(np.flipud(us))):
#                return True

        return False

class Image:
    def __init__(self, rules):
        self._rules = rules
        self._image = Grid(START)

    def __repr__(self):
        return '\n'.join(''.join(k) for k in self._image.grid.tolist())

    @property
    def on(self):
        return ''.join(self._image.grid.flatten().tolist()).count('#')

    def iterate(self):

        logging.debug('SIZE: %d', self._image.size)

        if self._image.size % 2 == 0:
            height = self._image.size / 2
            width = self._image.size / 2
            mult = 2

        elif self._image.size % 3 == 0:
            width = self._image.size / 3
            height = self._image.size / 3
            mult = 3

        assert width.is_integer()
        assert height.is_integer()

        rows = []
        for h in range(int(height)):
            cols = []
            for w in range(int(width)):

                logging.debug('VIEW: %d:%d | %d:%d', h*mult, (h+1)*mult, w*mult, (w+1)*mult)
                view = self._image.grid[h*mult:(h+1)*mult, w*mult:(w+1)*mult]
                col = Grid.fromNpArray(view)

                match = None
                for src, dst in self._rules:
                    if col.like(src):
                        match = dst

                if match is None:
                    cols.append(col.grid)
                else:
                    cols.append(match.grid)

            rows.append(np.concatenate(cols, axis=1))

        self._image.grid = np.concatenate(rows, axis=0)

def parse(data):
    rules = []

    for line in data.splitlines():

        src, dst = line.split(' => ')
        src = Grid(src)
        dst = Grid(dst)

        rules.append((src, dst))

    return rules

def part1(rules):
    image = Image(rules)
    for i in range(5):
        image.iterate()
        logging.info('ON: %d', image.on)
        logging.info('IMAGE:\n%r', image)

    return image.on

def part2(rules):
    image = Image(rules)
    for i in range(18):
        image.iterate()
        logging.info('ON: %d', image.on)
        logging.info('IMAGE:\n%r', image)

    print('Part 2:', image.on)
    return image.on