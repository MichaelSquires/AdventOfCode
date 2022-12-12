import queue
import string
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

VALUES = 'S' + string.ascii_lowercase + 'E'
START = VALUES.index('S')
END = VALUES.index('E')

INFINITY = 2**32

class Grid(utils.Grid):
    def dijkstra(self, source, target):
        return pyrust.y22d12(self, source, target)  # pylint: disable=no-member

    def dijkstra_find(self, source, target_val):
        '''
        Dijkstra search for target_val of cell instead of coordinates

        NOTE: This is a non-standard dijkstra algorithm. Do not copy this to
        future days
        '''
        Q = queue.PriorityQueue()

        dist = collections.defaultdict(lambda: INFINITY)
        dist[source] = 0

        prev = collections.defaultdict(lambda: None)

        Q.put((0, source))

        target = None

        while not Q.empty():
            _, u = Q.get()

            here = self[u]

            # Break if we find a coord that has the target value
            if here == target_val:
                target = u
                break

            for v in self.adjacent(*u):
                # For this challenge, we can't step up more than one at a time.
                # Since we're searching backward, that means we can't step down
                # more than one at a time.
                if self[v] < here - 1:
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
    data = [list(map(VALUES.index, k)) for k in data.splitlines()]
    return Grid.init_with_data(data)

def part1(grid: Grid):
    start = grid.find(START)
    end = grid.find(END)
    
    path = grid.dijkstra(start, end)
    # Path includes the source coordinates so sub 1
    return len(path) - 1

def part2(grid: Grid):
    end = grid.find(END)

    path = grid.dijkstra_find(end, VALUES.index('a'))
    # Path includes the source coordinates so sub 1
    return len(path) - 1
