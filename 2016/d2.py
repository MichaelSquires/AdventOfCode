import logging

class Keypad:
    _keypad = {
        (-1, +1): 1,
        ( 0, +1): 2,
        (+1, +1): 3,

        (-1,  0): 4,
        ( 0,  0): 5,
        (+1,  0): 6,

        (-1, -1): 7,
        ( 0, -1): 8,
        (+1, -1): 9,
    }

    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def button(self):
        return '%x' % (self._keypad[self.x, self.y])

    def doInstruction(self, instruction):
        for direction in instruction:
            x = self.x
            y = self.y
            if direction == 'U':
                y += 1

            if direction == 'D':
                y -= 1

            if direction == 'R':
                x += 1

            if direction == 'L':
                x -= 1

            new = (x, y)
            if new not in self._keypad:
                continue

            self.x, self.y = new

class Keypad2(Keypad):
    _keypad = {
        ( 0, +2): 1,

        (-1, +1): 2,
        ( 0, +1): 3,
        (+1, +1): 4,

        (-2,  0): 5,
        (-1,  0): 6,
        ( 0,  0): 7,
        (+1,  0): 8,
        (+2,  0): 9,

        (-1, -1): 10, # A
        ( 0, -1): 11, # B
        (+1, -1): 12, # C
        ( 0, -2): 13, # D
    }

    def __init__(self):
        self.x = -2
        self.y = 0

def parse(data):
    return data.splitlines()

def part1(instructions):
    code = []
    keypad = Keypad()

    for instruction in instructions:
        keypad.doInstruction(instruction)
        code.append(keypad.button)

    return ''.join(code)

def part2(instructions):
    code = []
    keypad = Keypad2()

    for instruction in instructions:
        keypad.doInstruction(instruction)
        code.append(keypad.button)

    return ''.join(code)