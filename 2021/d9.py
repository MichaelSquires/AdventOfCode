'''
## --- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active;
small hydrothermal vents release smoke into the caves that slowly settles like
rain.

If you can model how the smoke flows through the caves, you might be able to
avoid it and be that much safer. The submarine generates a heightmap of the
floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the
following heightmap:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

Each number corresponds to the height of a particular location, where 9 is the
highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than
any of its adjacent locations. Most locations have four adjacent locations (up,
down, left, and right); locations on the edge or corner of the map have three or
two adjacent locations, respectively. (Diagonal locations do not count as
adjacent.)

In the above example, there are four low points, all highlighted: two are in the
first row (a 1 and a 0), one is in the third row (a 5), and one is in the bottom
row (also a 5). All other locations on the heightmap have some lower adjacent
location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the
risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels of
all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels
of all low points on your heightmap?

## --- Part Two ---

Next, you need to find the largest basins so you know what areas are most
important to avoid.

A basin is all locations that eventually flow downward to a single low point.
Therefore, every low point has a basin, although some basins are very small.
Locations of height 9 do not count as being in any basin, and all other
locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the
low point. The example above has four basins.

The top-left basin, size 3:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

The top-right basin, size 9:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

The middle basin, size 14:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

The bottom-right basin, size 9:

```
2199943210
3987894921
9856789892
8767896789
9899965678
```

Find the three largest basins and multiply their sizes together. In the above
example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?

'''
import math
import logging

from utils import *

SAMPLE = '''\
2199943210
3987894921
9856789892
8767896789
9899965678
'''

class Day9Grid(Grid):
    def adjacent(self, x, y):
        ret = []

        ret.append(self.up(x, y))
        ret.append(self.down(x, y))
        ret.append(self.left(x, y))
        ret.append(self.right(x, y))

        return ret


def parse(data):
    data = [list(map(int, k)) for k in data.splitlines()]
    return Day9Grid.init_with_data(data, default=None)

def part1(data):
    if data.width < 80:
        data.print()

    lows = []
    for x in range(data.width):
        for y in range(data.height):
            logging.debug('X: %s, Y: %s', x, y)
            val = data[x, y]
            adj = [k for k in data.adjacent(x, y) if k is not None]

            logging.info('ADJ: %s, %s -> %s', x, y, adj)

            if val < min(adj):
                logging.info('VAL: %s -> %s, %s', val, x, y)
                lows.append(val)

    logging.info('LOWS: %s', lows)
    return sum(lows) + len(lows)

def part2(data):
    basins = []
    seen = []

    for x, y in data.foreach():
        if data[x, y] == 9:
            continue

        if (x, y) in seen:
            continue

        basin = []
        todo = [(x, y)]

        while len(todo):
            x, y = todo.pop()

            seen.append((x, y))
            basin.append((x, y))

            u, d, l, r = data.adjacent(x, y)

            if u not in (None, 9) and (xy := up(x, y)) not in seen:
                todo.append(xy)

            if d not in (None, 9) and (xy := down(x, y)) not in seen:
                todo.append(xy)

            if l not in (None, 9) and (xy := left(x, y)) not in seen:
                todo.append(xy)

            if r not in (None, 9) and (xy := right(x, y)) not in seen:
                todo.append(xy)

        logging.debug('BASIN: %s', basin)
        basins.append(basin)

    lengths = [len(k) for k in basins]
    lengths.sort()

    return math.prod(lengths[-3:])