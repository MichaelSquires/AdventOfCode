#!/usr/bin/env python

import sys
import logging
import argparse

def main(args):

    ports = []
    data = args.file.readlines()
    for line in data:
        line = line.strip()
        a, b= line.split('/')
        ports.append((int(a), int(b)))

    if args.part in (None, 1):
        part1(ports)

    if args.part in (None, 2):
        part2(ports)

    return 0

def part1(ports):
    print('Part 1:', len(ports))

def part2(ports):
    print('Part 2:', len(ports))

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
