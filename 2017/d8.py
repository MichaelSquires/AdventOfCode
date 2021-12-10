import re
import logging
import itertools

regex = re.compile(r'([a-z]+) (inc|dec) ([-\d]+) if ([a-z]+) ([<>!=]{1,2}) ([-\d]+)$')

class Instruction:
    __registers__ = {}
    __maxseen__ = 0
    def __init__(self, register, action, amount, left, condition, right):
        self.register = register
        self.action = action
        self.amount = amount
        self.left = left
        self.condition = condition
        self.right = right

    @classmethod
    def getRegister(cls, regname):
        return cls.__registers__.get(regname, 0)

    @classmethod
    def setRegister(cls, regname, value):
        if value > cls.__maxseen__:
            cls.__maxseen__ = value
        cls.__registers__[regname] = value

    @classmethod
    def getRegisters(cls):
        return cls.__registers__

    @classmethod
    def getMaxSeen(cls):
        return cls.__maxseen__

def parse(data):
    instructions = []
    for line in data.splitlines():
        line = line.strip()

        match = regex.match(line)
        if match is None:
            logging.error('Match failed: %s', line)
            raise Exception('Match failed')

        groups = match.groups()

        logging.debug('GROUPS: %r', groups)

        instruction = Instruction(
            groups[0],
            groups[1],
            int(groups[2]),
            groups[3],
            groups[4],
            int(groups[5]),
        )

        instructions.append(instruction)

    runProgram(instructions)

    return instructions

def runProgram(instructions):
    for instruction in instructions:
        left = Instruction.getRegister(instruction.left)
        result = {
            '>': lambda a, b: a > b,
            '<': lambda a, b: a < b,
            '>=': lambda a, b: a >= b,
            '<=': lambda a, b: a <= b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
        }.get(instruction.condition)(left, instruction.right)

        if not result:
            continue

        regval = Instruction.getRegister(instruction.register)

        if instruction.action == 'inc':
            Instruction.setRegister(instruction.register, regval + instruction.amount)
        elif instruction.action == 'dec':
            Instruction.setRegister(instruction.register, regval - instruction.amount)
        else:
            logger.error('Invalid action: %r', action)
            raise Exception('Invalid action')

def part1(instructions):
    registers = Instruction.getRegisters()
    return max(registers.values())

def part2(instructions):
    return Instruction.getMaxSeen()