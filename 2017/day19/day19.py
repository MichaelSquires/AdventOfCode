#!/usr/bin/env python

import sys
import string
import logging
import argparse

NORTH = 0
EAST = 1
WEST = 2
SOUTH = 3

def main(args):

    ret = ''
    steps = 0

    data = args.file.readlines()

    x = data[0].index('|')
    y = 0
    direction = SOUTH

    while True:
        steps += 1
        assert direction in (NORTH, EAST, WEST, SOUTH)

        if direction == NORTH:
            y -= 1
        elif direction == EAST:
            x += 1
        elif direction == WEST:
            x -= 1
        elif direction == SOUTH:
            y += 1

        c = data[y][x]
        logging.debug('C: (%d, %d) %s', x, y, c)

        if c in string.ascii_uppercase:
            ret += c

        # Change direction
        elif c == '+':
            if direction in (NORTH, SOUTH):
                if data[y][x-1] != ' ':
                    direction = WEST
                    logging.debug('WEST')
                elif data[y][x+1] != ' ':
                    direction = EAST
                    logging.debug('EAST')
                else:
                    logging.error('Unknown direction: %d %d', x, y)
                    raise Exception('Unknown direction')

            elif direction in (EAST, WEST):
                if data[y+1][x] != ' ':
                    direction = SOUTH
                    logging.debug('SOUTH')
                elif data[y-1][x] != ' ':
                    direction = NORTH
                    logging.debug('NORTH')
                else:
                    logging.error('Unknown direction: %d %d', x, y)
                    raise Exception('Unknown direction')

        elif c == ' ':
            break

    print('Part 1:', ret)
    print('Part 2:', steps)

    return 0

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
