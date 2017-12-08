#!/usr/bin/env python

import re
import sys
import logging
import argparse
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

def main(args):
    instructions = []
    for line in args.file.readlines():
        line = line.strip()

        match = regex.match(line)
        if match is None:
            logger.error('Match failed: %s', line)
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

    if args.part in (None, 1):
        part1(instructions)

    if args.part in (None, 2):
        part2(instructions)

    return 0

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
    print('Part 1:', max(registers.values()))

def part2(instructions):
    maxseen = Instruction.getMaxSeen()
    print('Part 2:', maxseen)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    parser.add_argument('file', help='Input file', type=open)

    args = parser.parse_args()
    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
