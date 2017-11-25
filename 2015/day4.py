#!/usr/bin/env python

import sys
import hashlib
import argparse
import traceback

verbose = False

# my key was: ckczppom

def part1(key):
    nonce = 0

    while True:
        digest = hashlib.md5('{}{:d}'.format(key, nonce)).hexdigest()
        if digest.startswith('00000'):
            return nonce

        nonce += 1

        if verbose and nonce % 100000 == 0:
            print 'Nonce: {:d}'.format(nonce)

def part2(key):
    nonce = 0

    while True:
        digest = hashlib.md5('{}{:d}'.format(key, nonce)).hexdigest()
        if digest.startswith('000000'):
            return nonce

        nonce += 1

        if verbose and nonce % 100000 == 0:
            print 'Nonce: {:d}'.format(nonce)

def main(args):
    
    print 'Part 1: {:d}'.format(part1(args.key))
    print 'Part 2: {:d}'.format(part2(args.key))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    #parser.add_argument('-i', '--interact', help='Interact', action='store_true')
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('key', help='Secret key', type=str)

    args = parser.parse_args()
    verbose = args.verbose

    try:
        sys.exit(main(args))
    except Exception as exc:
        print 'ERROR: %s' % (exc)
        if verbose:
            traceback.print_exc()
        sys.exit(-1)
