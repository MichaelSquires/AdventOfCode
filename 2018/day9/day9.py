#!/usr/bin/env python

import re
import sys
import logging
import argparse

class Circle:
    def __init__(self):
        self._data = [0]
        self._current = 0

    def insert(self, value):
        new = (current + (CW * 1)) % len(self._data)
        self._data.insert(new, value)
        self._current = new

CW = 1
CCW = -1

def part1(data):
    players, points = data
    score = [0 for k in range(players)]

    circle = [0]

    player = 1
    current = 1
    for i in range(1, points+1):
        if len(circle) == 1:
            new = 2
        else:
            new = ((current + (CW * 1)) + 1) % len(circle)
        print('CIRCLE', circle, new)
        circle.insert(new, i)

        current = new

        player += 1
        player %= players
        if player == 0:
            player = 1

        if i == 15:
            break

    print(circle)

#    circle.rotate(-1)
    print(max(*score))

    print('Part 1:', data)

def part2(data):
    print('Part 2:', data)

def main(args):

    data = open(args.file, 'rb').read().decode('utf8').strip()
    data = re.findall('(\d+) players; last marble is worth (\d+) points', data)
    data = [(int(k[0]), int(k[1])) for k in data]

    if args.part in (None, 1):
        for entry in data:
            part1(entry)

    if args.part in (None, 2):
        for entry in data:
            part2(entry)

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[0, 1, 2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    parser.add_argument('file', help='Input file', nargs='?', default='input.txt')

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
