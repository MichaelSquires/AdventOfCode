#!/usr/bin/env python

import re
import sys
import copy
import logging
import argparse
import collections

regex = re.compile(r'([A-Z]*)\((\d+)x(\d+)\)')

def main(args):
    data = args.file.read().strip()

    if args.part in (None, 1):
        part1(data)

    if args.part in (None, 2):
        part2(data)

    return 0

def decompress(data):
    ret = ''
    while data:
        #logging.debug('RET: %d', len(ret))
        match = regex.match(data)
        if match is None:
            ret += data
            break
            #raise Exception('Invalid marker: %r' % (data))

        end = match.end()
        chars = int(match.group(2))
        times = int(match.group(3))

        ret += data[end:end + chars] * times

        data = data[end+chars:]

    return ret

def part1(data):
    data = decompress(data)
    print('Part 1:', len(data))

def part2(data):
#    decomp=decompress
#    rgx=regex
#    import code
#    code.interact(local=locals())
    match = True
    while True:
        data = decompress(data)
        logging.debug('DATA: %d', len(data))
        if '(' not in data:
            break

    print('Part 2:', len(data))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=open)

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
