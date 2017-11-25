#!/usr/bin/env python

import sys
import argparse
import itertools
import traceback

verbose = False

class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = {}

    def addEdge(self, src, dst, distance):
        if src not in self.vertices:
            self.vertices.append(src)

        if dst not in self.vertices:
            self.vertices.append(dst)

        # This is a symmetric TSP so add edges in both directions
        self.edges[(src,dst)] = distance
        self.edges[(dst,src)] = distance

    def getEdge(self, src, dst):
        return self.edges.get((src, dst))

def parse_input(data):
    graph = Graph()

    for line in data:
        src, _, dst, _, distance = line.split(' ')

        graph.addEdge(src, dst, int(distance))

    return graph

def part1(graph):
    maxlen = 9999
    count = 0
    for circuit in itertools.permutations(graph.vertices):

        distance = 0
        for i in range(len(circuit) - 1):
            count += 1
            distance += graph.getEdge(circuit[i], circuit[i+1])

            if distance > maxlen:
                break

        if distance < maxlen:
            maxlen = distance

    if verbose:
        print 'Part1 iterations: {:d}'.format(count)

    return maxlen

def part2(graph):
    minlen = 0
    count = 0
    for circuit in itertools.permutations(graph.vertices):

        distance = 0
        for i in range(len(circuit) - 1):
            count += 1
            distance += graph.getEdge(circuit[i], circuit[i+1])

        if distance > minlen:
            minlen = distance

    if verbose:
        print 'Part2 iterations: {:d}'.format(count)

    return minlen

def main(args):

    data = args.file.readlines()

    # Strip newlines
    data = [k.strip() for k in data]

    graph = parse_input(data)

    if verbose:
        print 'Vertices: {}'.format(graph.vertices)
        print 'Edges: {}'.format(graph.edges)

    print 'Part1: {:d}'.format(part1(graph))
    print 'Part2: {:d}'.format(part2(graph))

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
