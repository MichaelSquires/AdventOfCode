#!/usr/bin/env python

import re
import sys
import logging
import argparse
import itertools

class Stream:
    def __init__(self, data):
        self._data = data

        self.score = 0

        self._group = 0
        self._garbage = False
        self._escaped = False

        self.gscore = 0

    def run(self):
        for char in self._data:
            logging.debug('CHAR: %s', char)
            # Open group
            if char == '{' and not self._garbage:
                self._group += 1
                logging.debug('GROUP: %d', self._group)

            # Close group
            elif char == '}' and not self._garbage:
                self.score += self._group
                self._group -= 1
                logging.debug('SCORE: %d', self.score)
                logging.debug('GROUP: %d', self._group)

            # Escape character
            elif char == '!':
                self._escaped = not self._escaped
                logging.debug('ESCAPE: %s', self._escaped)

            # Open garbage
            elif char == '<' and not self._garbage:
                self._garbage = True
                logging.debug('GARBAGE: %s', self._garbage)

            # Close garbage
            elif char == '>' and not self._escaped:
                self._garbage = False
                logging.debug('GARBAGE: %s', self._garbage)

            # Only escape one character
            elif self._escaped:
                self._escaped = False
                logging.debug('ESCAPE: %s', self._escaped)

            # All others
            else:
                if self._garbage:
                    self.gscore += 1

def main(args):

    stream = Stream(args.file.read())
    stream.run()

    if args.part in (None, 1):
        part1(stream)

    if args.part in (None, 2):
        part2(stream)

    return 0

def part1(stream):
    print('Part 1:', stream.score)

def part2(stream):
    print('Part 2:', stream.gscore)

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
