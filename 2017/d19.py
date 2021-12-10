import string
import logging

NORTH = 0
EAST = 1
WEST = 2
SOUTH = 3

def parse(data):

    ret = ''
    steps = 0

    data = data.splitlines()

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

    return ret, steps

def part1(data):
    return data[0]

def part2(data):
    return data[1]