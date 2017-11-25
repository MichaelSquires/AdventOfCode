#!/usr/bin/env python

import sys
import copy
import pprint
import argparse
import itertools
import traceback

verbose = False

TOTAL_STEPS = 100

class GameOfLife:
    def __init__(self, grid):
        self._grid = copy.deepcopy(grid)

    def __str__(self):
        ret = ''
        for row in self._grid:
            for col in row:
                if col:
                    ret += '#'
                else:
                    ret += '.'
            ret += '\n'

        return ret
                    

    def step(self):
        shadow = copy.deepcopy(self._grid)

        rows = len(shadow)
        cols = len(shadow[0])

        for row in range(rows):
            for col in range(cols):
                ul = -1
                up = -1
                ur = -1
                lt = -1
                rt = -1
                dl = -1
                dn = -1
                dr = -1
                
                if row == 0:
                    ul = 0
                    up = 0
                    ur = 0

                if col == 0:
                    ul = 0
                    lt = 0
                    dl = 0

                if row == rows - 1:
                    dl = 0
                    dn = 0
                    dr = 0

                if col == cols - 1:
                    ur = 0
                    rt = 0
                    dr = 0

                if ul == -1:
                    ul = shadow[row-1][col-1]

                if up == -1:
                    up = shadow[row-1][col]

                if ur == -1:
                    ur = shadow[row-1][col+1]

                if lt == -1:
                    lt = shadow[row][col-1]

                if rt == -1:
                    rt = shadow[row][col+1]

                if dl == -1:
                    dl = shadow[row+1][col-1]

                if dn == -1:
                    dn = shadow[row+1][col]

                if dr == -1:
                    dr = shadow[row+1][col+1]

                neighbors = [ul, up, ur, lt, rt, dl, dn, dr]

                # If on and 2 or 3 neighbors are not on, turn off
                if shadow[row][col] and not sum(neighbors) in (2, 3):
                    self._grid[row][col] = 0

                # If off and 3 neighbors are on, turn on
                if not shadow[row][col] and sum(neighbors) == 3:
                    self._grid[row][col] = 1

    def step2(self):
        shadow = copy.deepcopy(self._grid)

        rows = len(shadow)
        cols = len(shadow[0])
        corners = ((0,0), (0, cols-1), (rows-1, 0), (rows-1, cols-1))

        for row in range(rows):
            for col in range(cols):
                ul = -1
                up = -1
                ur = -1
                lt = -1
                rt = -1
                dl = -1
                dn = -1
                dr = -1
                
                if (row,col) in corners:
                    continue

                if row == 0:
                    ul = 0
                    up = 0
                    ur = 0

                if col == 0:
                    ul = 0
                    lt = 0
                    dl = 0

                if row == rows - 1:
                    dl = 0
                    dn = 0
                    dr = 0

                if col == cols - 1:
                    ur = 0
                    rt = 0
                    dr = 0

                if ul == -1:
                    ul = shadow[row-1][col-1]

                if up == -1:
                    up = shadow[row-1][col]

                if ur == -1:
                    ur = shadow[row-1][col+1]

                if lt == -1:
                    lt = shadow[row][col-1]

                if rt == -1:
                    rt = shadow[row][col+1]

                if dl == -1:
                    dl = shadow[row+1][col-1]

                if dn == -1:
                    dn = shadow[row+1][col]

                if dr == -1:
                    dr = shadow[row+1][col+1]

                neighbors = [ul, up, ur, lt, rt, dl, dn, dr]

                # If on and 2 or 3 neighbors are not on, turn off
                if shadow[row][col] and not sum(neighbors) in (2, 3):
                    self._grid[row][col] = 0

                # If off and 3 neighbors are on, turn on
                if not shadow[row][col] and sum(neighbors) == 3:
                    self._grid[row][col] = 1

    @property
    def on(self):
        ret = 0
        for row in self._grid:
            ret += sum(row)

        return ret

def part1(grid):
    game = GameOfLife(grid)
    if verbose:
        print game

    for i in range(TOTAL_STEPS):
        game.step()

    if verbose:
        print game

    return game.on

def part2(grid):
    game = GameOfLife(grid)
    game._grid[0][0] = 1
    game._grid[0][-1] = 1
    game._grid[-1][0] = 1
    game._grid[-1][-1] = 1

    if verbose:
        print '----- START -----'
        print game
        print '-----------------'

    for i in range(TOTAL_STEPS):
        game.step2()
        if verbose:
            print game

    if verbose:
        print '-----  END  -----'
        print game
        print '-----------------'

    return game.on

def main(args):

    data = args.file.readlines()

    # Strip newlines
    data = [k.strip() for k in data]

    grid = []
    for line in data:
        row = []
        for x in line.strip():
            if x == '#':
                row.append(1)
            elif x == '.':
                row.append(0)
            else:
                raise Exception('Invalid input: {}'.format(x))

        grid.append(row)
                
    print 'Part1: {:d}'.format(part1(grid))
    print 'Part2: {:d}'.format(part2(grid))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-s', '--steps', help='Specify number of steps', type=int, default=TOTAL_STEPS)
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=file)

    args = parser.parse_args()
    verbose = args.verbose
    TOTAL_STEPS = args.steps

    try:
        sys.exit(main(args))
    except Exception as exc:
        print 'ERROR: %s' % (exc)
        if verbose:
            traceback.print_exc()
        sys.exit(-1)
