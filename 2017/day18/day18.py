#!/usr/bin/env python

import sys
import queue
import string
import logging
import argparse
import threading

VALID_COMMANDS = [
    'snd', 'set', 'add', 'mul',
    'mod', 'rcv', 'jgz',
]

VALID_REGISTERS = list(string.ascii_lowercase)

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
        if register not in VALID_REGISTERS:
            raise Exception('Invalid register specified: %s' % (register))
        return register

    @property
    def r1(self):
        register = self.operands[1]
        if register not in VALID_REGISTERS:
            raise Exception('Invalid register specified: %s' % (register))
        return register

    def exec(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, instruction, machine):
        cmd, *operands = instruction.split(' ')
        return {
            'snd': Snd,
            'set': Set,
            'add': Add,
            'mul': Mul,
            'mod': Mod,
            'rcv': Rcv,
            'jgz': Jgz,
        }.get(cmd)(*operands, machine=machine)

class Snd(Instruction):
    '''
    `snd X` plays a sound with a frequency equal to the value of X.
    '''
    def __init__(self, *operands, machine):
        super().__init__('snd', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.pc += 1
        logging.info('SND: %d', self.rm0)
        self.machine.remote.pipe.put(self.rm0)
        self.machine.sent += 1
        logging.info('SENT: %d -> %d', self.machine.pid, self.machine.sent)

class Set(Instruction):
    '''
    `set X Y` sets register X to the value of Y.
    '''
    def __init__(self, *operands, machine):
        super().__init__('set', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.pc += 1
        self.machine.registers[self.operands[0]] = self.rm1

class Add(Instruction):
    '''
    `add X Y` increases register X by the value of Y.
    '''
    def __init__(self, *operands, machine):
        super().__init__('add', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.pc += 1
        self.machine.registers[self.operands[0]] += self.rm1

class Mul(Instruction):
    '''
    `mul X Y` sets register X to the result of multiplying the value
    contained in register X by the value of Y.
    '''
    pass
    def __init__(self, *operands, machine):
        super().__init__('mul', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.pc += 1
        self.machine.registers[self.operands[0]] *= self.rm1

class Mod(Instruction):
    '''
    `mod X Y` sets register X to the remainder of dividing the value
    contained in register X by the value of Y (that is, it sets X
    to the result of X modulo Y).
    '''
    pass
    def __init__(self, *operands, machine):
        super().__init__('mod', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.pc += 1
        self.machine.registers[self.operands[0]] = self.rm0 % self.rm1

class Rcv(Instruction):
    '''
    `rcv X` recovers the frequency of the last sound played, but only
    when the value of X is not zero. (If it is zero, the command does
    nothing.)
    '''
    def __init__(self, *operands, machine):
        super().__init__('rcv', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.pc += 1

        self.machine.registers[self.operands[0]] = self.machine.pipe.get()

class Jgz(Instruction):
    '''
    `jgz X Y` jumps with an offset of the value of Y, but only if the value
    of X is greater than zero. (An offset of 2 skips the next instruction,
    an offset of -1 jumps to the previous instruction, and so on.)
    '''
    def __init__(self, *operands, machine):
        super().__init__('jgz', *operands, machine=machine)

    def exec(self):
        logexec(self)
        offset = self.rm1
        if self.rm0 <= 0:
            offset = 1

        self.pc += offset

class VirtualMachine(threading.Thread):
    def __init__(self, program, pid=0):
        super(VirtualMachine, self).__init__()
        self.daemon = True

        self.instructions = [Instruction.decode(i, self) for i in program]
        self.pid = pid
        self.sent = 0
        self.pipe = queue.Queue()
        self.remote = None

        self.pc = 0
        self.registers = dict()
        for reg in VALID_REGISTERS:
            self.registers[reg] = 0

        self.registers['p'] = pid

    def __repr__(self):
        return '<VirtualMachine%d: %d [%d] %s>' % (self.pid, self.pipe.qsize(), self.pc, ' '.join('%s:%d' % (k,v) for k,v in self.registers.items()))

    def run(self):
        while self.pc < len(self.instructions) and self.pc >= 0:
            try:
                logging.debug('VM: %r', self)
                self.instructions[self.pc].exec()

            except AssertionError:
                print('VM: [%d] %s %r' % (self.pc, self.instructions[self.pc], self.instructions))
                logging.exception('Failed assertion')
                raise

            except Exception as exc:
                #logging.error('ERROR: %s [%d] %s', exc, self.pc, self.instructions[self.pc])
                break

    def _regOrInt(self, val):
        if val in VALID_REGISTERS:
            return self.registers[val]
        return int(val)

def main(args):

    data = args.file.readlines()
    program = [k.strip() for k in data]

    if args.part in (None, 1):
        part1(program)

    if args.part in (None, 2):
        part2(program)

    return 0

def part1(program):
    vm = VirtualMachine(program)
    vm.run()

    print('Part 1:', vm.registers['rcv'])

def part2(program):
    vm0 = VirtualMachine(program, 0)
    vm1 = VirtualMachine(program, 1)

    vm0.remote = vm1
    vm1.remote = vm0

    vm0.start()
    vm1.start()

    [k.join() for k in (vm0, vm1)]

    print('Part 2:', len(program))

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
