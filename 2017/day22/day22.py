#!/usr/bin/env python

import re
import sys
import copy
import math
import logging
import argparse

CLEAN = '.'
INFECTED = '#'
WEAKENED = 'W'
FLAGGED = 'F'

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRMOD = 4

def main(args):

    data = [list(k.strip()) for k in args.file.readlines()]

    nodes = {}
    for y in range(len(data)):
        for x in range(len(data[y])):
            nodes[(x,y)] = data[y][x]

    if args.part in (None, 1):
        part1(nodes)

    if args.part in (None, 2):
        part2(nodes)

    return 0

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

    print('Part 1:', infected)

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

    print('Part 2:', infected)

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
