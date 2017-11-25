#!/usr/bin/env python

import sys
import argparse
import traceback

verbose = False

def part1(data):
    paper = 0

    data = [k.split('x') for k in data]

    for l, w, h in data:
        l = int(l)
        w = int(w)
        h = int(h)
        small = min(l*w, w*h, h*l)
        paper += 2*l*w + 2*w*h + 2*h*l + small

    return paper

def part2(data):
    ribbon = 0

    data = [k.split('x') for k in data]

    for l, w, h in data:
        l = int(l)
        w = int(w)
        h = int(h)
        large = max(l, w, h)
        ribbon += (2*l + 2*w + 2*h - 2*large) + (l * w * h)

    return ribbon

def main(args):

    data = args.file.readlines()

    print 'Part1: {:d}'.format(part1(data))
    print 'Part2: {:d}'.format(part2(data))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
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
