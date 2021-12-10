import re
import logging
import collections

FABRIC_SIZE = 1009

class Fabric:
    def __init__(self):
        self._fabric = [[0] * FABRIC_SIZE for k in range(FABRIC_SIZE)]
        self._claims = [[0] * FABRIC_SIZE for k in range(FABRIC_SIZE)]
        self._start = (0, 0)

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        if not isinstance(value, tuple):
            raise TypeError('Value must be a tuple')

        if len(value) != 2:
            raise ValueError('Value must be a tuple with two elements')

        if not isinstance(value[0], int):
            raise TypeError('Elements must be integers')

        if not isinstance(value[1], int):
            raise TypeError('Elements must be integers')

        self._start = value

    def cut(self, width, height, cid=None):
        x,y = self._start
        for i in range(height):
            for k in range(width):
                logging.info('%d,%d', x+i, y+k)
                self._fabric[y + i][x + k] += 1
                if self._claims[y + i][x + k] == 0:
                    self._claims[y+i][x+k] = list()
                self._claims[y + i][x + k].append(cid)

    @property
    def overlap(self):
        ret = 0
        for i in range(FABRIC_SIZE):
            for k in range(FABRIC_SIZE):
                if self._fabric[i][k] > 1:
                    ret += 1

        return ret

    @property
    def noverlap(self):
        single = set()
        multi = set()
        for i in range(FABRIC_SIZE):
            for k in range(FABRIC_SIZE):
                cid = self._claims[i][k]
                if not cid:
                    continue

                if len(cid) == 1:
                    single.add(cid[0])

                else:
                    [multi.add(k) for k in cid]

        return single - multi

def part1(claims):
    fabric = Fabric()

    for claim in claims:
        fabric.start = (claim.x, claim.y)
        fabric.cut(claim.width, claim.height)

    print('Part 1:', fabric.overlap)
    return fabric.overlap

def part2(claims):
    fabric = Fabric()

    for claim in claims:
        fabric.start = (claim.x, claim.y)
        fabric.cut(claim.width, claim.height, cid=claim.id)

    return fabric.noverlap

Claim = collections.namedtuple('Claim', ('id', 'x', 'y', 'width', 'height'))

def parse(data):
    parsed = re.findall('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', data)
    claims = []
    for k in parsed:
        claims.append(
            Claim(
                int(k[0]),
                int(k[1]),
                int(k[2]),
                int(k[3]),
                int(k[4]),
            )
        )

    return claims