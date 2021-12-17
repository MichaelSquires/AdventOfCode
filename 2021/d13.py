'''
## --- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you
could do some kind of thermal imaging so you could tell ahead of time which
caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you
activate it, you are greeted with:

```
Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.
```

Apparently, the Elves have never used this feature. To your surprise, you manage
to find the manual; as you go to open it, page 1 falls out. It's a large sheet
of transparent paper! The transparent paper is marked with random dots and
includes instructions on how to fold it up (your puzzle input). For example:

```
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
```

The first section is a list of dots on the transparent paper. 0,0 represents the
top-left coordinate.  The first value, x, increases to the right.  The second
value, y, increases downward.  So, the coordinate 3,0 is to the right of 0,0,
and the coordinate 0,7 is below 0,0. The coordinates in this example form the
following pattern, where # is a dot on the paper and . is an empty, unmarked
position:

```
...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
```

Then, there is a list of fold instructions. Each instruction indicates a line on
the transparent paper and wants you to fold the paper up (for horizontal y=...
lines) or left (for vertical x=... lines). In this example, the first fold
instruction is fold along y=7, which designates the line formed by all of the
positions where y is 7 (marked here with -):

```
...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........
```

Because this is a horizontal line, fold the bottom half up. Some of the dots
might end up overlapping after the fold is complete, but dots will never appear
exactly on a fold line. The result of doing this fold looks like this:

```
#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........
```

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the
transparent paper is folded; after the fold is complete, those dots appear in
the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot
just below them in the result (at 0,3) remains visible, as it can be seen
through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge
together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

```
#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....
```

Because this is a vertical line, fold left:

```
#####
#...#
#...#
#...#
#####
.....
.....
```

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the
first fold. After the first fold in the example above, 17 dots are visible -
dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on
your transparent paper?

## --- Part Two ---

Finish folding the transparent paper according to the instructions. The manual
says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?

'''
import logging
import collections

import utils

SAMPLE = '''\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'''

class Grid(utils.Grid):
    #DEFAULT = '.'
    def foldup(self, val):
        new = Grid(val, self.width)

        # Copy old data
        for x,y in self.foreach(max_y=val):
            if y >= val:
                continue

            new[x, y] = self[x, y]

        # Copy folded data
        for x,y in self.foreach(min_y=val+1):
            if self[x, y] != 1:
                continue

            y = val - (y - val)

            new[x, y] = 1

        return new

    def foldleft(self, val):
        new = Grid(self.height, val)

        # Copy old data
        for x,y in self.foreach(max_x=val):
            new[x, y] = self[x, y]

        # Copy folded data
        for x,y in self.foreach(min_x=val+1):
            if self[x, y] != 1:
                continue

            x = val - (x - val)

            new[x, y] = 1

        return new

    def fold(self, instruction):
        axis, val = instruction
        if axis == 'y':
            return self.foldup(val)

        return self.foldleft(val)

    def count(self, val):
        return self._grid.count(val)

    def __str__(self):
        ret = '\n'
        for yy in range(self.height):
            height = self.width * yy
            row = self._grid[0 + height:self.width + height]
            ret += ''.join(str(k) for k in row)
            ret += '\n'

        ret = ret.replace('0', ' ')
        ret = ret.replace('1', '#')

        return ret


Instruction = collections.namedtuple('Instruction', ['axis', 'line'])
Data = collections.namedtuple('Data', ['grid', 'instructions'])

def parse(data):
    # Split input into coord and fold parts
    coords, folds = data.split('\n\n')

    # Parse out coordinates
    data = []
    for line in coords.splitlines():
        x,y = line.split(',')
        data.append((int(x), int(y)))

    width = max([x for x,y in data]) + 1
    height = max([y for x,y in data]) + 1

    # Create and build grid
    grid = Grid(height, width)

    for xy in data:
        grid[xy] = 1

    # Parse out folds
    data = [k.split('along')[1].strip() for k in folds.splitlines()]

    def fx(val):
        axis, val = val.split('=')
        assert axis in ('x', 'y')
        return (axis, int(val))

    instructions = list(map(fx, data))

    return Data(grid, instructions)

def part1(data):
    grid = data.grid.fold(data.instructions[0])
    return grid.count(1)

def part2(data):
    grid = data.grid
    for instruction in data.instructions:
        grid = grid.fold(instruction)

    return grid