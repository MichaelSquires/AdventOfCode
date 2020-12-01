#!/usr/bin/env python

import sys
import string
import logging
import argparse

class Node:
    def __init__(self):
        self.children = []
        self.metadata = []

    @property
    def total(self):
        ret = sum(self.metadata)
        for child in self.children:
            ret += child.total
        return ret

    @property
    def value(self):
        if not self.children:
            return sum(self.metadata)

        ret = 0
        for index in self.metadata:
            if index == 0:
                continue

            index -= 1

            if index >= len(self.children):
                continue

            ret += self.children[index].value

        return ret

def parse(data):

    node = Node()

    children = data.pop(0)
    mdcount = data.pop(0)

    for i in range(children):
        node.children.append(parse(data))

    for i in range(mdcount):
        node.metadata.append(data.pop(0))

    return node

def part1(tree):
    print('Part 1:', tree.total)

def part2(tree):
    print('Part 2:', tree.value)

def main(args):

    data = open(args.file, 'rb').read().decode('utf8').strip()
    data = list(map(int, data.split()))
    data = parse(data)

    if args.part in (None, 1):
        part1(data)

    if args.part in (None, 2):
        part2(data)

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
