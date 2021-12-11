'''
## --- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents
constantly produce large, opaque clouds, so it would be best to avoid them if
possible.

They tend to form in lines; the submarine helpfully produces a list of nearby
lines of vents (your puzzle input) for you to review. For example:

```
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
```

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where
x1,y1 are the coordinates of one end the line segment and x2,y2 are the
coordinates of the other end. These line segments include the points at both
ends. In other words:

  - An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.

  - An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2
or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the
following diagram:

```
.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
```

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
Each position is shown as the number of lines which cover that point or . if no
line covers that point. The top-left pair of 1s, for example, comes from 2,2 ->
2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9
-> 2,9.

To avoid the most dangerous areas, you need to determine the number of points
where at least two lines overlap. In the above example, this is anywhere in the
diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two
lines overlap?

## --- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you
the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your
list will only ever be horizontal, vertical, or a diagonal line at exactly 45
degrees. In other words:

  - An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.

  - An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

Considering all lines from the above example would now produce the following
diagram:

```
1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
```

You still need to determine the number of points where at least two lines
overlap. In the above example, this is still anywhere in the diagram with a 2 or
larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?

'''
import logging
import collections

import utils

Point = collections.namedtuple('Point', ['x', 'y'])
Line = collections.namedtuple('Line', ['start', 'end'])

def parse(data):
    ret = []
    lines = data.splitlines()
    for line in lines:
        start, end = line.split('->')

        start = Point(*[int(k) for k in start.split(',')])
        end = Point(*[int(k) for k in end.split(',')])
        ret.append(Line(start, end))

    return ret


class Grid(utils.Grid):
    def inc(self, x, y):
        logging.debug('X: %s, Y: %s (%d)', x, y, x + self.width * y)
        self[x, y] += 1

    def print(self):
        for yy in range(self.height):
            height = self.width * yy
            print(self._grid[0 + height:self.width + height])

    def do_horizontal(self, line):
        start = min(line.start.y, line.end.y)
        end = max(line.start.y, line.end.y)
        for ii in range(start, end + 1):
            self.inc(line.start.x, ii)

    def do_vertical(self, line):
        start = min(line.start.x, line.end.x)
        end = max(line.start.x, line.end.x)
        for ii in range(start, end + 1):
            self.inc(ii, line.start.y)

    def do_diagonal(self, line):
        stepx = 1
        startx = line.start.x
        endx = line.end.x
        if line.start.x > line.end.x:
            stepx = -1

        stepy = 1
        starty = line.start.y
        endy = line.end.y
        if line.start.y > line.end.y:
            stepy = -1

        while startx != endx + stepx and starty != endy + stepy:
            logging.debug('STARTX %s, STARTY %s', startx, starty)
            self.inc(startx, starty)
            startx += stepx
            starty += stepy

    def do_line(self, line):
        logging.info('LINE: %s', line)

        if line.start.x != line.end.x and line.start.y != line.end.y:
            self.do_diagonal(line)
        elif line.start.x == line.end.x:
            self.do_horizontal(line)
        else:
            self.do_vertical(line)


def gridsize(lines):
    all_x = []
    all_x.extend([line.start.x for line in lines])
    all_x.extend([line.end.x for line in lines])

    all_y = []
    all_y.extend([line.start.y for line in lines])
    all_y.extend([line.end.y for line in lines])

    width = max(all_x)
    height = max(all_y)

    return height, width

def part1(data):
    height, width = gridsize(data)
    grid = Grid(height + 1, width + 1)

    for line in data:
        # Skip diagonal lines
        if line.start.x != line.end.x and line.start.y != line.end.y:
            logging.info('SKIP: %s', line)
            continue

        grid.do_line(line)

    if grid.width < 80:
        grid.print()

    return len([k for k in grid._grid if k > 1])

def part2(data):
    height, width = gridsize(data)
    grid = Grid(height + 1, width + 1)

    for line in data:
        grid.do_line(line)

    if grid.width < 80:
        grid.print()

    return len([k for k in grid._grid if k > 1])
