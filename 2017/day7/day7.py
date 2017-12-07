#!/usr/bin/env python

import re
import sys
import logging
import argparse
import itertools

regex = re.compile(r'([a-z]+) \((\d+)\)(?: -> ([a-z ,]+))?')

class Node:
    __registry__ = {}

    def __init__(self, name, weight, disc):
        self.name = name
        self.weight = weight

        if disc is None:
            disc = list()

        self.disc = disc

        self._parent = None
        self.children = list()

    def __repr__(self):
        return '<Node %s (%d)>' % (self.name, self.weight)

    @property
    def parent(self):
        return self._parent

    @property
    def siblings(self):
        return [k for k in self._parent.children if k is not self]

    @property
    def total(self):
        total = self.weight
        for child in self.children:
            total += child.total

        return total

    @parent.setter
    def parent(self, parent):
        parent.children.append(self)
        self._parent = parent

    @classmethod
    def getNode(cls, name):
        return cls.__registry__[name]

    @classmethod
    def addNode(cls, node):
        cls.__registry__[node.name] = node

    @classmethod
    def __iter__(cls):
        yield iter(cls.__registry__.values())

def main(args):
    nodes = []
    for line in args.file.readlines():
        line = line.strip()

        match = regex.match(line)
        if match is None:
            raise Exception('Could not match line: %s', line)

        name, weight, disc = match.groups()
        if disc is not None:
            disc = disc.split(',')
            disc = [k.strip() for k in disc]

        node = Node(name, int(weight), disc)
        nodes.append(node)
        Node.addNode(node)

    for node in nodes:
        for d in node.disc:
            Node.getNode(d).parent = node

    logging.debug('NODES: %r', nodes)

    root = nodes[0]
    while root.parent is not None:
        root = root.parent

    if args.part in (None, 1):
        part1(root)

    if args.part in (None, 2):
        part2(root)

    return 0

def part1(root):
    print('Part 1:', root.name)

def part2(root):
    curr = root
    while True:
        found = False
        children = curr.children

        # Check if all children have the same total
        if len({k.total for k in children}) == 1:
            # All children are the same, 'curr' is the problem node
            break

        # Sort the children by total
        totals = {}
        for child in curr.children:
            if child.total not in totals:
                totals[child.total] = []
            totals[child.total].append(child)

        # Find the unique child
        for val in totals.values():
            if len(val) == 1:
                curr = val[0]
                logging.info('CURR: %r', curr)

    # Calculate answer
    sibling = curr.siblings[0]
    if curr.total > sibling.total:
        answer = curr.weight - (curr.total - sibling.total)
    else:
        answer = curr.weight + (siblings.total - curr.total)

    print('Part 2:', answer)

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
