import re
import logging

import networkx as nx

def part1(data):
    graph = nx.DiGraph()
    for src,dst in data:
        graph.add_edge(src, dst)

    print('Part 1:', ''.join(nx.lexicographical_topological_sort(graph)))

def part2(data):
    print('Part 2:', data)

def parse(data):
    return re.findall('Step ([A-Z]) must be finished before step ([A-Z]) can begin.', data)