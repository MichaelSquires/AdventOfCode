import re
import copy
import logging
import collections

SCREEN_HEIGHT = 6
SCREEN_WIDTH = 50

#SCREEN_HEIGHT = 3
#SCREEN_WIDTH = 7

V_RECT = 0
V_ROTCOL = 1
V_ROTROW = 2

Instruction = collections.namedtuple('Instruction', ['verb', 'a', 'b'])

class Screen:
    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._pixels = []
        # This is convoluted but the easy way is where dragons live
        # This way:
        # self._pixels = [[0] * self._width] * self._height
        # the inner lists (rows) are all the same object. Sometimes:
        # ugh, python...
        for x in range(self._height):
            row = []
            for y in range(self._width):
                row.append(0)
            self._pixels.append(row)

        # Looks like this
        # self._pixels[height][width]

    @property
    def on(self):
        ret = 0
        for h in range(self._height):
            for w in range(self._width):
                if self._pixels[h][w]:
                    ret += 1

        return ret

    def exec(self, instruction):
        assert isinstance(instruction, Instruction)
        logging.debug('Processing instruction: %r', instruction)

        return {
            V_RECT: self.rect,
            V_ROTCOL: self.rotcol,
            V_ROTROW: self.rotrow,
        }.get(instruction.verb)(instruction)

    def rect(self, instruction):
        width = instruction.a
        height = instruction.b

        for h in range(height):
            for w in range(width):
                logging.debug('RECT: %d %d', h, w)
                self._pixels[h][w] = 1

        print(self)

    def rotcol(self, instruction):
        logging.debug('ROTCOL: %r', instruction)
        x = instruction.a
        by = instruction.b

        pixels = copy.deepcopy(self._pixels)
        for i in range(self._height):
            logging.debug('ROTCOL: %d %d = %d %d', (i+by) % self._height, x, (i+self._height) % self._height, x)
            pixels[(i+by) % self._height][x] = self._pixels[(i+self._height) % self._height][x]

        self._pixels = pixels

        print(self)

    def rotrow(self, instruction):
        logging.debug('ROTROW: %r', instruction)
        y = instruction.a
        by = instruction.b

        pixels = copy.deepcopy(self._pixels)
        for i in range(self._width):
            logging.debug('ROTROW: %d %d = %d %d', y, (i+by) % self._width, y, (i+self._width) % self._width)
            pixels[y][(i+by) % self._width] = self._pixels[y][(i+self._width) % self._width]

        self._pixels = pixels

        print(self)

    def __repr__(self):
        ret = '\n'

        for h in range(self._height):
            for w in range(self._width):
                pixel = self._pixels[h][w]
                ret += {
                    0: '.',
                    1: '#',
                }.get(pixel)

            ret += '\n'

        return ret

# rect 3x2
rect_re = re.compile('^rect (?P<a>\d+)x(?P<b>\d+)$')

# rotate column x=1 by 1
rotcol_re = re.compile('^rotate column x=(?P<a>\d+) by (?P<b>\d+)$')

# rotate row y=0 by 4
rotrow_re = re.compile('^rotate row y=(?P<a>\d+) by (?P<b>\d+)$')

def parse(data):
    instructions = []
    for line in data.splitlines():
        if line.startswith('rect'):
            match = rect_re.match(line)
            if match is None:
                raise Exception('Invalid rect instruction: %s' % (line))

            verb = V_RECT

        elif line.startswith('rotate column'):
            match = rotcol_re.match(line)
            if match is None:
                raise Exception('Invalid rotcol instruction: %s' % (line))

            verb = V_ROTCOL

        elif line.startswith('rotate row'):
            match = rotrow_re.match(line)
            if match is None:
                raise Exception('Invalid rotrow instruction: %s' % (line))

            verb = V_ROTROW

        instructions.append(Instruction(
            verb, int(match.group('a')), int(match.group('b'))
        ))

    return instructions

def part1(instructions):
    screen = Screen(SCREEN_HEIGHT, SCREEN_WIDTH)
    for instruction in instructions:
        screen.exec(instruction)

    return screen.on

def part2(instructions):
    screen = Screen(SCREEN_HEIGHT, SCREEN_WIDTH)
    return screen