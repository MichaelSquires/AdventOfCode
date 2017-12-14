#!/usr/bin/env python

import sys
import logging
import argparse

import networkx as nx

class KnotHash:
    def __init__(self, size=256):
        self._size = size
        self._state = list(range(0, size))

        self._skip = 0
        self._pos = 0

    @property
    def result(self):
        return self._state[0] * self._state[1]

    @property
    def digest(self):
        dense = []
        for i in range(16):
            block = self._state[16*i:16*i+16]

            xor = 0
            for k in block:
                xor ^= k

            dense.append(xor)

        logging.debug('DENSE: %r', dense)
        return bytes(dense)

    @property
    def hexdigest(self):
        return self.digest.hex()

    @property
    def bindigest(self):
        ret = ''
        digest = self.digest
        for d in digest:
            binform = bin(d)[2:]
            ret += '0' * (8-len(binform)) + binform
        return ret

    def incpos(self, val):
        self._pos = (self._pos + val) % self._size

    def updateLength(self, length):
        logging.debug('LENGTH: %d', length)
        logging.debug('POS: %d', self._pos)

        if length > self._size:
            logging.error('Invalid length: %d', length)
            raise Exception('Invalid length')

        overflow = length + self._pos > self._size

        if overflow:
            select = self._state[self._pos:] + self._state[:length - (self._size - self._pos)]
        else:
            select = self._state[self._pos:self._pos+length]

        select.reverse()

        if overflow:
            self._state[self._pos:] = select[:self._size - self._pos]
            self._state[:length - (self._size - self._pos)] = select[self._size - self._pos:]

        else:
            self._state[self._pos:self._pos+length] = select

        logging.debug('STATE: %r', self._state)

        self.incpos(length + self._skip)
        self._skip += 1


def main(args):

    data = args.file.read().strip()

    grid = []
    for i in range(128):
        kh = knothash('%s-%d' % (data, i))
        row = [int(k) for k in kh.bindigest]
        grid.append(row)

    if args.part in (None, 1):
        part1(grid)

    if args.part in (None, 2):
        part2(grid)

    return 0

def knothash(data):

    data = data.encode()
    data += b'\x11\x1f\x49\x2f\x17'

    logging.info('DATA: %r', data)

    kh = KnotHash()
    for i in range(64):
        logging.debug('ROUND: %d', i)
        for length in data:
            kh.updateLength(length)

    return kh

def part1(grid):
    used = 0
    for row in grid:
        used += row.count(1)

    print('Part 1:', used)

def part2(grid):

    graph = nx.Graph()

    # Build graph
    for x in range(128):
        for y in range(128):
            if grid[x][y]:
                graph.add_node((x,y))

    # Iterate over graph and add edges between adjacent nodes
    for x in range(128):
        for y in range(128):
            if not graph.has_node((x,y)):
                continue

            up = (x, y-1)
            down = (x, y+1)
            left = (x-1, y)
            right = (x+1, y)

            if graph.has_node(up):
                graph.add_edge((x,y), up)

            if graph.has_node(down):
                graph.add_edge((x,y), down)

            if graph.has_node(left):
                graph.add_edge((x,y), left)

            if graph.has_node(right):
                graph.add_edge((x,y), right)

    # Find the islands
    subgraphs = list(nx.k_edge_subgraphs(graph, 1))
    print('Part 2:', len(subgraphs))

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
