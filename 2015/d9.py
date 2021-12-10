import logging
import itertools


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

def parse(data):
    data = data.splitlines()

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

    logging.debug('Part1 iterations: {:d}'.format(count))

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

    logging.debug('Part2 iterations: {:d}'.format(count))

    return minlen