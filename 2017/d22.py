import re
import copy
import math
import logging

CLEAN = '.'
INFECTED = '#'
WEAKENED = 'W'
FLAGGED = 'F'

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRMOD = 4

def parse(data):
    data = data.splitlines()

    nodes = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            nodes[(x,y)] = data[y][x]

    return nodes

def part1(nodes):
    vx = 12
    vy = 12
    vd = UP

    infected = 0
    for i in range(10000):
        logging.debug('V: %d,%d %d', vx, vy, vd)

        curr = nodes.get((vx,vy))
        if curr is None:
            nodes[(vx,vy)] = CLEAN
            curr = nodes[(vx,vy)]

        if curr == INFECTED:
            vd = (vd + 1) % DIRMOD
            nodes[(vx, vy)] = CLEAN

        elif curr == CLEAN:
            vd = (vd - 1) % DIRMOD
            nodes[(vx, vy)] = INFECTED
            infected += 1

        if vd == UP:
            vy -= 1

        elif vd == RIGHT:
            vx += 1

        elif vd == DOWN:
            vy += 1

        elif vd == LEFT:
            vx -= 1

        else:
            logging.error('Invalid direction: %d', vd)
            raise Exception('Invalid direction')

    return infected

def part2(nodes):
    vx = 12
    vy = 12
    vd = UP

    infected = 0
    for i in range(10000000):
        logging.debug('V: %d,%d %d', vx, vy, vd)

        curr = nodes.get((vx,vy))
        if curr is None:
            nodes[(vx,vy)] = CLEAN
            curr = nodes[(vx,vy)]

        if curr == INFECTED:
            vd = (vd + 1) % DIRMOD
            nodes[(vx, vy)] = FLAGGED

        elif curr == CLEAN:
            vd = (vd - 1) % DIRMOD
            nodes[(vx, vy)] = WEAKENED

        elif curr == WEAKENED:
            nodes[(vx,vy)] = INFECTED
            infected += 1

        elif curr == FLAGGED:
            nodes[(vx,vy)] = CLEAN
            vd = (vd + 2) % DIRMOD

        else:
            logging.error('Invalid state: %s', curr)
            raise Exception('Invalid state')

        if vd == UP:
            vy -= 1

        elif vd == RIGHT:
            vx += 1

        elif vd == DOWN:
            vy += 1

        elif vd == LEFT:
            vx -= 1

        else:
            logging.error('Invalid direction: %d', vd)
            raise Exception('Invalid direction')

    return infected