#!/usr/bin/env python

import sys
import string
import argparse
import traceback

verbose = False

TOGGLE  = 0
TURNON  = 1
TURNOFF = 2

def parse_input(data):
    # returns:
    #   List of commands as tuples
    #   Sample tuple:
    #       (TOGGLE, x1, y1, x2, y2)
    ret = []

    # Get rid of the word "turn"
    data = [k.replace('turn ', '') for k in data]

    for line in data:
        cmd, start, _junk, end = line.split(' ')

        cmd = {
            'off': TURNOFF,
            'on': TURNON,
            'toggle': TOGGLE
        }.get(cmd)

        x1,y1 = start.split(',')
        x1 = int(x1)
        y1 = int(y1)

        x2,y2 = end.split(',')
        x2 = int(x2)
        y2 = int(y2)

        ret.append((cmd, x1, y1, x2, y2))

    return ret

def part1(data):
    # Create lights 2d array (1000 x 1000)
    lights = []
    for i in range(1000):
        lights.append([0]*1000)

    for cmd, x1, y1, x2, y2 in data:
        if verbose: 
            print 'Cmd: {}, x1: {:d}, y1: {:d}, x2: {:d}, y2: {:d}'.format(cmd, x1, y1, x2, y2)

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                if cmd == TOGGLE:
                    lights[x][y] = lights[x][y] ^ 1

                elif cmd == TURNON:
                    lights[x][y] = 1

                elif cmd == TURNOFF:
                    lights[x][y] = 0

    ret = 0
    for x in range(1000):
        for y in range(1000):
            if lights[x][y] == 1:
                ret += 1
            
    return ret

def part2(data):
    # Create lights 2d array (1000 x 1000)
    lights = []
    for i in range(1000):
        lights.append([0]*1000)

    for cmd, x1, y1, x2, y2 in data:
        if verbose: 
            print 'Cmd: {}, x1: {:d}, y1: {:d}, x2: {:d}, y2: {:d}'.format(cmd, x1, y1, x2, y2)

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                if cmd == TOGGLE:
                    lights[x][y] += 2

                elif cmd == TURNON:
                    lights[x][y] += 1

                elif cmd == TURNOFF:
                    lights[x][y] = max(0, lights[x][y] - 1)

    ret = 0
    for x in range(1000):
        for y in range(1000):
            ret += lights[x][y]
            
    return ret
        
def main(args):
    
    data = args.file.readlines()

    # Strip newlines
    data = [k.strip() for k in data]

    data = parse_input(data)

    print 'Part 1: {:d}'.format(part1(data))
    print 'Part 2: {:d}'.format(part2(data))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    #parser.add_argument('-i', '--interact', help='Interact', action='store_true')
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=file)

    args = parser.parse_args()
    verbose = args.verbose

    try:
        sys.exit(main(args))
    except Exception as exc:
        print 'ERROR: %s' % (exc)
        if verbose:
            traceback.print_exc()
        sys.exit(-1)
