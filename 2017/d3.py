import pprint
import logging
import collections

import requests

Range = collections.namedtuple('Range', ['start', 'stop'])
Point = collections.namedtuple('Point', ['x', 'y'])
Ring = collections.namedtuple('Ring', [
    'range',    # Range (inclusive) of ring
    'number',   # Ring number
    'right',    # Range (inclusive) of right side of ring
    'top',      # Range (inclusive) of top side of ring
    'left',     # Range (inclusive) of left side of ring
    'bottom',   # Range (inclusive) of bottom side of ring
])

class Spiral:
    def __init__(self, minnum):
        self._minnum = minnum
        self._rings = [
            Ring(
                Range(1, 1),
                0,
                Range(1, 1),
                Range(1, 1),
                Range(1, 1),
                Range(1, 1),
            ),
        ]
        self._maxnum = 1

        while self._maxnum < self._minnum:
            ringsize = len(self._rings) * 8
            start = self._maxnum + 1
            stop = self._maxnum + ringsize
            sidelen = ringsize / 4

            start = start
            end = start + sidelen - 1
            right = Range(start, end)

            start = end + 1
            end = start + sidelen - 1
            top = Range(start, end)

            start = end + 1
            end = start + sidelen - 1
            left = Range(start, end)

            start = end + 1
            end = start + sidelen - 1
            bottom = Range(start, end)

            ring = Ring(
                Range(self._maxnum + 1, self._maxnum + ringsize),
                len(self._rings),
                right,
                top,
                left,
                bottom,
            )
            self._rings.append(ring)
            self._maxnum += ringsize

        logging.debug('RINGS: %s', pprint.pformat(self._rings))

    def coords(self, number):
        ring = None
        for r in self._rings:
            if number >= r.range.start and number <= r.range.stop:
                ring = r
                break

        assert ring is not None

        # Find the side the number is on
        side = None
        if number >= ring.right.start and number <= ring.right.stop:
            side = ring.right

            half = side.start + ((side.stop + 1 - side.start) / 2 - 1)
            x = ring.number
            y = number - half

        elif number >= ring.top.start and number <= ring.top.stop:
            side = ring.top

            half = side.start + ((side.stop + 1 - side.start) / 2 - 1)
            y = ring.number
            x = number - half

        elif number >= ring.left.start and number <= ring.left.stop:
            side = ring.left

            half = side.start + ((side.stop + 1 - side.start) / 2 - 1)
            x = ring.number * -1
            y = number - half

        elif number >= ring.bottom.start and number <= ring.bottom.stop:
            side = ring.bottom

            half = side.start + ((side.stop + 1 - side.start) / 2 - 1)
            y = ring.number * -1
            x = number - half

        return (x, y)


def parse(data):
    return int(data.strip())


def part1(number):
    spiral = Spiral(number)
    x,y = spiral.coords(number)
    return abs(x) + abs(y)

def part2(number):
    req = requests.get('https://oeis.org/A141481/b141481.txt')
    data = []
    for line in req.text.split('\n'):
        if line.startswith('#'):
            continue

        if not line:
            continue

        _, num = line.split()
        data.append(int(num))

    data = [k for k in data if k > number]
    data.sort()

    return data[0]