#!/usr/bin/env python

import re
import sys
import logging
import argparse

import networkx as nx

def part1(data):
    graph = nx.DiGraph()
    for src,dst in data:
        graph.add_edge(src, dst)

    print('Part 1:', ''.join(nx.lexicographical_topological_sort(graph)))

def part2(data):
    print('Part 2:', data)

def main(args):

    data = open(args.file, 'rb').read().decode('utf8')
    data = re.findall('Step ([A-Z]) must be finished before step ([A-Z]) can begin.', data)

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
