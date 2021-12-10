import hashlib
import logging
import itertools

class VirtualMachine:
    def __init__(self, instructions):
        self.instructions = instructions

        self.pc = 0
        self.registers = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0,
        }

    def run(self):
        while self.pc < len(self.instructions):
            self.execute(self.instructions[self.pc].strip())

    @property
    def a(self):
        return self.registers['a']

    @a.setter
    def a(self, value):
        self.registers['a'] = value

    @property
    def b(self):
        return self.registers['b']

    @b.setter
    def b(self, value):
        self.registers['b'] = value

    @property
    def c(self):
        return self.registers['c']

    @c.setter
    def c(self, value):
        self.registers['c'] = value

    @property
    def d(self):
        return self.registers['d']

    @d.setter
    def d(self, value):
        self.registers['d'] = value

    def cpy(self, src, dst):
        if src in ('a', 'b', 'c', 'd'):
            srcval = self.registers[src]
        else:
            srcval = int(src)

        if dst not in ('a', 'b', 'c', 'd'):
            raise Exception('Invalid register specified: %s' % (dst))

        self.registers[dst] = srcval

        return 1

    def inc(self, register):
        if register not in ('a', 'b', 'c', 'd'):
            raise Exception('Invalid register specified: %s' % (register))

        self.registers[register] += 1

        return 1

    def dec(self, register):
        if register not in ('a', 'b', 'c', 'd'):
            raise Exception('Invalid register specified: %s' % (register))

        self.registers[register] -= 1

        return 1

    def jnz(self, src, offset):
        if src in ('a', 'b', 'c', 'd'):
            if self.registers[src] != 0:
                return int(offset)
            return 1

        if int(src) != 0:
            return int(offset)
        return 1

    def execute(self, instruction):
        inst = instruction.split(' ')
        if inst[0] == 'cpy':
            self.pc += self.cpy(inst[1], inst[2])

        elif inst[0] == 'inc':
            self.pc += self.inc(inst[1])

        elif inst[0] == 'dec':
            self.pc += self.dec(inst[1])

        elif inst[0] == 'jnz':
            self.pc += self.jnz(inst[1], inst[2])

        else:
            raise Exception('Illegal instruction: %s' % (inst[0]))

def parse(data):
    return data.splitlines()

def part1(instructions):
    vm = VirtualMachine(instructions)
    vm.run()
    return vm.a

def part2(instructions):
    vm = VirtualMachine(instructions)
    vm.c = 1
    vm.run()
    return vm.a