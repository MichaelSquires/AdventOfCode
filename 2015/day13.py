#!/usr/bin/env python

import sys
import argparse
import itertools
import traceback

from pyparsing import *

NAMETOK = Word(alphas)
DIRTOK = oneOf('gain lose').setResultsName('direction')
INTTOK = Word(nums).setParseAction(lambda s,l,t: [int(t[0])]).setResultsName('value')

INPUT = Group(
    NAMETOK.setResultsName('src') +
    Literal('would').suppress() +
    DIRTOK +
    INTTOK +
    Literal('happiness units by sitting next to').suppress() +
    NAMETOK.setResultsName('dst') +
    Literal('.').suppress()
)

INPUTS = OneOrMore(INPUT)

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
        #self.edges[(dst,src)] = distance

    def getEdge(self, src, dst):
        return self.edges.get((src, dst))

def parse_input(data):
    graph = Graph()

    for line in data:

        direction = 1
        if line.direction == 'lose':
            direction = -1

        if verbose:
            print 'src: {}, dst: {}, distance: {}'.format(line.src, line.dst, line.value * direction)
        graph.addEdge(line.src, line.dst, line.value * direction)

    return graph

def part1(graph):
    minlen = 0
    count = 0
    best = None
    for circuit in itertools.permutations(graph.vertices):

        # Add the first person to the end of the list to complete the loop
        circuit = list(circuit)
        circuit.append(circuit[0])

        distance = 0
        for i in range(len(circuit) - 1):
            count += 1

            # Count the happiness count in both directions
            distance += graph.getEdge(circuit[i], circuit[i+1])
            distance += graph.getEdge(circuit[i+1], circuit[i])

        if distance > minlen:
            minlen = distance
            best = circuit

    if verbose:
        print 'Part2 iterations: {:d}'.format(count)

    print 'best',best
    for i in range(len(circuit) - 1):
        print '{} -> {}: {:d}'.format(circuit[i], circuit[i+1], graph.getEdge(circuit[i], circuit[i+1]))
    return minlen

def main(args):

    data = INPUTS.parseFile(args.file)
    graph = parse_input(data)

    if verbose:
        print 'Vertices: {}'.format(graph.vertices)
        print 'Edges: {}'.format(graph.edges)

    print 'Part1: {:d}'.format(part1(graph))

    # Add edges for the host. The host has a happiness rating of 0 for everyone
    for vertex in graph.vertices:
        graph.addEdge('host', vertex, 0)
        graph.addEdge(vertex, 'host', 0)

    # Re-run part1 with the host included
    print 'Part2: {:d}'.format(part1(graph))

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
