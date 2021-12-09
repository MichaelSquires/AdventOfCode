import math
import logging

from utils import *


class Day9Grid(Grid):
    def adjacent(self, x, y):
        ret = []

        ret.append(self.up(x, y))
        ret.append(self.down(x, y))
        ret.append(self.left(x, y))
        ret.append(self.right(x, y))

        return ret


def parse(data):
    data = [list(map(int, k)) for k in data.splitlines()]
    return Day9Grid.init_with_data(data)

def part1(data):
    if data.width < 80:
        data.print()

    lows = []
    for x in range(data.width):
        for y in range(data.height):
            logging.debug('X: %s, Y: %s', x, y)
            val = data[x, y]
            adj = [k for k in data.adjacent(x, y) if k is not None]

            logging.info('ADJ: %s, %s -> %s', x, y, adj)

            if val < min(adj):
                logging.info('VAL: %s -> %s, %s', val, x, y)
                lows.append(val)

    logging.info('LOWS: %s', lows)
    return sum(lows) + len(lows)

def part2(data):
    basins = []
    seen = []

    for x, y in data.foreach():
        if data[x, y] == 9:
            continue

        if (x, y) in seen:
            continue

        basin = []
        todo = [(x, y)]

        while len(todo):
            x, y = todo.pop()

            seen.append((x, y))
            basin.append((x, y))

            u, d, l, r = data.adjacent(x, y)

            if u not in (None, 9) and (xy := up(x, y)) not in seen:
                todo.append(xy)

            if d not in (None, 9) and (xy := down(x, y)) not in seen:
                todo.append(xy)

            if l not in (None, 9) and (xy := left(x, y)) not in seen:
                todo.append(xy)

            if r not in (None, 9) and (xy := right(x, y)) not in seen:
                todo.append(xy)

        logging.debug('BASIN: %s', basin)
        basins.append(basin)

    lengths = [len(k) for k in basins]
    lengths.sort()

    return math.prod(lengths[-3:])