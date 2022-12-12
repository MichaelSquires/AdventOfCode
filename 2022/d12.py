import queue
import string
import logging
import collections

import utils
import pyrust

SAMPLE = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''

INDICES = 'S' + string.ascii_lowercase + 'E'
START = INDICES.index('S')
END = INDICES.index('E')

INFINITY = 2**32

class Grid(utils.Grid):
    def dijkstra(self, source, target):
        return pyrust.y22d12(self, source, target)

    def pydijkstra(self, source, target):
        '''
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        '''
        Q = queue.PriorityQueue()

        dist = collections.defaultdict(lambda: INFINITY)
        dist[source] = 0

        prev = collections.defaultdict(lambda: None)

        Q.put((0, source))

        while not Q.empty():
            _, u = Q.get()

            here = self[u]

            for v in self.adjacent(*u):
                # NOTE: This is non-standard for dijkstra. Do not copy this to
                # future days
                if self[v] > here + 1:
                    continue

                alt = dist[u] + self[v]
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    Q.put((alt, v))

        S = []
        u = target
        while u is not None:
            S.insert(0, u)
            u = prev[u]

        return S

def parse(data: str):
    values = []

    for line in data.splitlines():
        values.append([INDICES.index(k) for k in line])

    return Grid.init_with_data(values)


def part1(grid: Grid):
    start = grid.find(START)
    end = grid.find(END)
    
    path = grid.dijkstra(start, end)
    return len(path) - 1

def part2(grid: Grid):
    start = grid.find(START)
    end = grid.find(END)

    grid[start] = INDICES.index('a')

    best = INFINITY
    
    for xy in grid.findall(INDICES.index('a')):
        path = grid.dijkstra(xy, end)

        attempt = len(path) - 1
        if attempt <= 0:
            continue

        if attempt < best and attempt != 0:
            best = attempt

    return best
