#!/usr/bin/env python

import sys
import logging
import argparse

A_START = 289
B_START = 629

# SAMPLE DATA
# A_START = 65
# B_START = 8921

A_FACTOR = 16807
B_FACTOR = 48271

A_MULTIPLE = 4
B_MULTIPLE = 8

MODULO = 0x7fffffff

PART1_ITERATIONS = 40000000
PART2_ITERATIONS = 5000000

class Generator:
    def __init__(self, start, factor, multiple=1):
        self._start = start
        self._factor = factor
        self._multiple = multiple
        self._generator = self.__generator()

    def __generator(self):
        prev = self._start
        while True:
            prev = (prev * self._factor) % MODULO
            if prev % self._multiple != 0:
                continue

            yield prev

    def __next__(self):
        return next(self._generator)

def main(args):

    if args.part in (None, 1):
        part1()

    if args.part in (None, 2):
        part2()

    return 0

def part1():
    genA = Generator(A_START, A_FACTOR)
    genB = Generator(B_START, B_FACTOR)
    match = 0
    for i in range(PART1_ITERATIONS):
        a = next(genA)
        b = next(genB)

        logging.debug('A: %d, B: %d', a, b)

        if (a & 0xffff) == (b & 0xffff):
            match += 1

    print('Part 1:', match)

def part2():
    genA = Generator(A_START, A_FACTOR, A_MULTIPLE)
    genB = Generator(B_START, B_FACTOR, B_MULTIPLE)
    match = 0
    for i in range(PART2_ITERATIONS):
        a = next(genA)
        b = next(genB)

        logging.debug('A: %d, B: %d', a, b)

        if (a & 0xffff) == (b & 0xffff):
            match += 1

    print('Part 2:', match)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    # parser.add_argument('file', help='Input file', type=open)

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
