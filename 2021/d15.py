import copy
import queue
import logging
import collections

import utils
import pyrust

sample = '''\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''

INFINITY = 2**32

class Grid(utils.Grid):
    def adjacent(self, x, y):
        up = utils.up(x, y)
        down = utils.down(x, y)
        left = utils.left(x, y)
        right = utils.right(x, y)

        ret = []

        for x, y in (up, down, left, right):
            if x < 0 or x > self.width - 1:
                continue

            if y < 0 or y > self.height - 1:
                continue

            ret.append((x,y))

        return ret


    def cost(self, coords):
        return sum([self[xy] for xy in coords])

    def dijkstra(self):
        return pyrust.dijkstra(self._grid, self.height, self.width)

    def pydijkstra(self):
        '''
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        '''
        source = (0, 0)
        target = (self.height - 1, self.width - 1)

        Q = queue.PriorityQueue()

        dist = collections.defaultdict(lambda: INFINITY)
        dist[source] = 0

        prev = collections.defaultdict(lambda: None)

        Q.put((0, source))

        while not Q.empty():
            d, u = Q.get()

            for v in self.adjacent(*u):
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

def lowest(dict_):
    ret = ((0,0), INFINITY)
    for xy, val in dict_.items():
        _, m = ret
        if val < m:
            ret = (xy, val)

    return ret[0]


def parse(data):
    data1 = [list(map(int, k)) for k in data.splitlines()]
    grid1 = Grid.init_with_data(data1)

    data2 = [list(map(int, k)) for k in data.splitlines()]
    data3 = copy.deepcopy(data2)

    overflow = list(range(10))
    overflow.extend(range(1, 10))

    for row in range(len(data2)):

        for ii in range(1, 5):
            data3[row].extend([overflow[k+ii] for k in data2[row]])

    for ii in range(1, 5):
        for row in range(len(data2)):
            data3.append([overflow[k+ii] for k in data3[row]])

    grid2 = Grid.init_with_data(data3)

    return grid1, grid2

def part1(data):
    grid = data[0]
    grid[0,0] = 0

    path = grid.dijkstra()
    return grid.cost(path)

def part2(data):
    grid = data[1]
    grid[0,0] = 0

    path = grid.dijkstra()
    return grid.cost(path)