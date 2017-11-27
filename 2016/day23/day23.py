#!/usr/bin/env python

import sys
import logging
import argparse
import functools

VALID_COMMANDS = [
    'cpy', 'inc', 'dec', 'jnz', 'tgl',
]

VALID_REGISTERS = [
    'a', 'b', 'c', 'd',
]

class Halt(Exception): pass

def logexec(instruction):
    if len(instruction) == 1:
        logging.debug(
            '%s: %s',
            instruction.__class__.__name__,
            instruction.operands[0],
        )
    elif len(instruction) == 2:
        logging.debug(
            '%s: %s %s',
            instruction.__class__.__name__,
            instruction.operands[0],
            instruction.operands[1]
        )

class Instruction:
    def __init__(self, cmd, *args, machine):
        if cmd not in VALID_COMMANDS:
            raise Exception('Invalid command: %s' % (cmd))

        self.cmd = cmd
        self.operands = args
        self.machine = machine

    def __len__(self):
        return len(self.operands)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, ' '.join(self.operands))

    @property
    def pc(self):
        return self.machine.pc

    @pc.setter
    def pc(self, value):
        self.machine.pc = value

    @property
    def rm0(self):
        return self.machine._regOrInt(self.operands[0])

    @property
    def rm1(self):
        return self.machine._regOrInt(self.operands[1])

    @property
    def r0(self):
        register = self.operands[0]
        if register not in ('a', 'b', 'c', 'd'):
            raise Exception('Invalid register specified: %s' % (register))
        return register

    @property
    def r1(self):
        register = self.operands[1]
        if register not in ('a', 'b', 'c', 'd'):
            raise Exception('Invalid register specified: %s' % (register))
        return register

    def exec(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, instruction, machine):
        cmd, *operands = instruction.split(' ')
        return {
            'cpy': Cpy,
            'inc': Inc,
            'dec': Dec,
            'jnz': Jnz,
            'tgl': Tgl,
        }.get(cmd)(*operands, machine=machine)

class Cpy(Instruction):
    def __init__(self, *operands, machine):
        super().__init__('cpy', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.machine.registers[self.r1] = self.rm0
        self.pc += 1

class Inc(Instruction):
    def __init__(self, *operands, machine):
        super().__init__('inc', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.machine.registers[self.r0] += 1
        self.pc += 1

class Dec(Instruction):
    def __init__(self, *operands, machine):
        super().__init__('dec', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.machine.registers[self.r0] -= 1
        self.pc += 1

class Jnz(Instruction):
    def __init__(self, *operands, machine):
        super().__init__('jnz', *operands, machine=machine)

    def optimize2(self):
        i2 = self.machine.instructions[self.pc - 2]
        i1 = self.machine.instructions[self.pc - 1]

        if isinstance(i2, Dec) and isinstance(i1, Inc):
            inc = i1
            dec = i2

        if isinstance(i1, Dec) and isinstance(i2, Inc):
            inc = i2
            dec = i1

        assert isinstance(inc, Inc)
        assert isinstance(dec, Dec)

        self.machine.registers[inc.r0] += self.rm0
        self.machine.registers[self.r0] = 0
        self.pc += 1

    def optimize5(self):
        i2 = self.machine.instructions[self.pc - 2]
        i1 = self.machine.instructions[self.pc - 1]

        if isinstance(i2, Dec) and isinstance(i1, Inc):
            inc = i1
            dec = i2

        if isinstance(i1, Dec) and isinstance(i2, Inc):
            inc = i2
            dec = i1

        assert isinstance(inc, Inc)
        assert isinstance(dec, Dec)

        self.machine.registers[inc.r0] += self.rm0
        self.machine.registers[self.r0] = 0
        self.pc += 1


    def exec(self):
        logexec(self)
        src = self.rm0

        if self.rm1 == -2:
            return self.optimize2()

#        if self.rm1 == -5:
#            return self.optimize5()

        if src != 0:
            self.pc += self.rm1
            return

        self.pc += 1

class Tgl(Instruction):
    def __init__(self, *operands, machine):
        super().__init__('tgl', *operands, machine=machine)

    def exec(self):
        logexec(self)
        index = self.pc + self.rm0
        instruction = self.machine.instructions[index]
        if len(instruction) == 1:
            if instruction.cmd == 'inc':
                self.machine.instructions[index] = Dec(*instruction.operands, machine=self.machine)
            else:
                self.machine.instructions[index] = Inc(*instruction.operands, machine=self.machine)

        elif len(instruction) == 2:
            if instruction.cmd == 'jnz':
                self.machine.instructions[index] = Cpy(*instruction.operands, machine=self.machine)
            else:
                self.machine.instructions[index] = Jnz(*instruction.operands, machine=self.machine)

        self.pc += 1

class VirtualMachine:
    def __init__(self, instructions):
        self.instructions = [Instruction.decode(i, self) for i in instructions]

        self.pc = 0
        self.registers = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0,
        }

    def __repr__(self):
        return '<VirtualMachine: [%d] %s %s %s %s>' % (self.pc, self.a, self.b, self.c, self.d)

    def run(self):
        while self.pc < len(self.instructions):
            try:
                logging.debug('VM: %r', self)
                self.instructions[self.pc].exec()

            except Halt:
                logging.debug('VM: %r', self)
                logging.debug('VM: %r', self.instructions)
                break

            except AssertionError:
                print('VM: [%d] %s %r' % (self.pc, self.instructions[self.pc], self.instructions))
                logging.exception('Failed assertion')
                raise

            except Exception as exc:
                logging.error('ERROR: %s [%d] %s', exc, self.pc, self.instructions[self.pc])
                self.pc += 1

    def _regOrInt(self, val):
        if val in VALID_REGISTERS:
            return self.registers[val]
        return int(val)

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

def main(args):
    instructions = [k.strip() for k in args.file.readlines()]

    if args.part in (None, 1):
        part1(instructions)

    if args.part in (None, 2):
        part2(instructions)

    return 0

def part1(instructions):
    vm = VirtualMachine(instructions)
    vm.a = 7
    vm.run()
    print('Part 1:', vm.a)

def part2(instructions):
    vm = VirtualMachine(instructions)
    vm.a = 12
    vm.run()
    print('Part 2:', vm.a)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=open)

    args = parser.parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
