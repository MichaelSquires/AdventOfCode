import re
import logging

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @property
    def possible(self):
        return (
            self.a + self.b > self.c and
            self.b + self.c > self.a and
            self.a + self.c > self.b
        )

regex = re.compile(r'^\s+(\d+)\s+(\d+)\s+(\d+)$')

def parse(data):
    dimensions = []
    for line in data.splitlines():
        m = regex.match(line)

        dimensions.append((
            int(m.group(1)),
            int(m.group(2)),
            int(m.group(3))
        ))

    return dimensions

def part1(dimensions):
    possible = 0

    for a,b,c in dimensions:
        triangle = Triangle(a, b, c)
        if triangle.possible:
            possible += 1

    return possible

def part2(dimensions):
    possible = 0

    for y in range(0, len(dimensions) - 2, 3):
        for x in range(3):
            a = dimensions[y+0][x]
            b = dimensions[y+1][x]
            c = dimensions[y+2][x]
            triangle = Triangle(a, b, c)
            if triangle.possible:
                possible += 1

    return possible