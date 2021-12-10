import logging
import itertools

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

def parse(data):
    graph = Graph()

    data = INPUTS.parseString(data)
    for line in data:

        direction = 1
        if line.direction == 'lose':
            direction = -1

        logging.debug('src: {}, dst: {}, distance: {}'.format(line.src, line.dst, line.value * direction))
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

    for i in range(len(circuit) - 1):
        logging.info('{} -> {}: {:d}'.format(circuit[i], circuit[i+1], graph.getEdge(circuit[i], circuit[i+1])))

    return minlen

def part2(graph):
    # Add edges for the host. The host has a happiness rating of 0 for everyone
    for vertex in graph.vertices:
        graph.addEdge('host', vertex, 0)
        graph.addEdge(vertex, 'host', 0)

    # Re-run part1 with the host included
    return part1(graph)