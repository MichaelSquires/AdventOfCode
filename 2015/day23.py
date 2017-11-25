#!/usr/bin/env python

import sys
import copy
import pprint
import argparse
import itertools
import traceback

verbose = False

INS_HALF    = 'hlf'
INS_TRIPLE  = 'tpl'
INS_INCR    = 'inc'
INS_JUMP    = 'jmp'
INS_JEVEN   = 'jie'
INS_JONE    = 'jio'


class VirtualMachine:
    def __init__(self, instructions):
        self.pc = 0

        self.registers = {
            'a': 0,
            'b': 0,
        }

        self.instructions = instructions

    def step(self):
        instruction = self.instructions[self.pc]

        func = {
            INS_HALF:   self.do_HALF,
            INS_TRIPLE: self.do_TRIPLE,
            INS_INCR:   self.do_INCR,
            INS_JUMP:   self.do_JUMP,
            INS_JEVEN:  self.do_JEVEN,
            INS_JONE:   self.do_JONE,
        }.get(instruction[0])

        self.pc += func(instruction)

    def run(self):
        while self.pc < len(self.instructions):
            self.step()

    def do_HALF(self, instruction):
        reg = instruction[1]
        self.registers[reg] /= 2

        return 1

    def do_TRIPLE(self, instruction):
        reg = instruction[1]
        self.registers[reg] *= 3

        return 1

    def do_INCR(self, instruction):
        reg = instruction[1]
        self.registers[reg] += 1

        return 1

    def do_JUMP(self, instruction):
        offset = int(instruction[1])

        return offset

    def do_JEVEN(self, instruction):
        reg = instruction[1]
        offset = int(instruction[2])

        if 0 == self.registers[reg] % 2:
            return offset
        else:
            return 1

    def do_JONE(self, instruction):
        reg = instruction[1]
        offset = int(instruction[2])

        if 1 == self.registers[reg]:
            return offset
        else:
            return 1

def part1(data):
    vm = VirtualMachine(data)
    vm.run()
    return vm.registers['b']

def part2(data):
    vm = VirtualMachine(data)
    vm.registers['a'] = 1
    vm.run()
    return vm.registers['b']

def main(args):

    data = [k.strip().replace(',', '').split(' ') for k in args.file.readlines()]

    if verbose:
        pprint.pprint(data)

    print 'Part1: {:d}'.format(part1(data))
    print 'Part2: {:d}'.format(part2(data))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=file)

    args = parser.parse_args()
    verbose = args.verbose

    try:
        sys.exit(main(args))
    except Exception as exc:
        print 'ERROR: %s' % (exc)
        if verbose:
            traceback.print_exc()
        sys.exit(-1)
