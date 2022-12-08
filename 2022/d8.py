import math
import logging

import utils

SAMPLE = '''\
30373
25512
65332
33549
35390
'''

def parse(data: str):
    data = [list(map(int, k)) for k in data.splitlines()]
    grid = utils.Grid.init_with_data(data)

    assert grid.height == grid.width
    return grid

def part1(grid: utils.Grid):
    visible = 0

    for x,y in grid.foreach():
        if x == 0 or x == grid.width - 1:
            visible += 1
            continue

        if y == 0 or y == grid.height - 1:
            visible += 1
            continue

        val = grid[(x,y)]

        left = grid.hrange((0,y), (x,y))
        right = grid.hrange((x+1,y), (grid.width,y))

        below = grid.vrange((x,y+1), (x,grid.height))
        above = grid.vrange((x,0), (x,y))

        logging.debug('%s -> %s', (x,y), val)
        logging.debug('LEFT: %s', left)
        logging.debug('RIGHT: %s', right)
        logging.debug('ABOVE: %s', above)
        logging.debug('BELOW: %s', below)

        if all([
            any(map(lambda x: x >= val, left)),
            any(map(lambda x: x >= val, right)),
            any(map(lambda x: x >= val, above)),
            any(map(lambda x: x >= val, below)),
        ]):
            continue

        logging.debug('VISIBLE')

        visible += 1

    return visible


def takeuntil(pred, iterable):
    ret = []
    idx = 0
    for val in iterable:
        ret.append(val)
        if pred(val):
            break

    return ret


def part2(grid: utils.Grid):
    best = 0

    for x,y in grid.foreach():
        if x == 0 or x == grid.width - 1:
            continue

        if y == 0 or y == grid.height - 1:
            continue

        val = grid[(x,y)]

        left = grid.hrange((0,y), (x,y))
        right = grid.hrange((x+1,y), (grid.width,y))

        below = grid.vrange((x,y+1), (x,grid.height))
        above = grid.vrange((x,0), (x,y))

        logging.debug('%s -> %s', (x,y), val)
        logging.debug('LEFT: %s', left)
        logging.debug('RIGHT: %s', right)
        logging.debug('ABOVE: %s', above)
        logging.debug('BELOW: %s', below)

        left.reverse()
        above.reverse()

        lval = len(takeuntil(lambda x: x >= val, left))
        rval = len(takeuntil(lambda x: x >= val, right))
        aval = len(takeuntil(lambda x: x >= val, above))
        bval = len(takeuntil(lambda x: x >= val, below))

        logging.debug('LVAL: %s', lval)
        logging.debug('RVAL: %s', rval)
        logging.debug('AVAL: %s', aval)
        logging.debug('BVAL: %s', bval)

        score = math.prod([lval, rval, aval, bval])

        logging.debug('SCORE: %s', score)

        if score > best:
            best = score

    return best
