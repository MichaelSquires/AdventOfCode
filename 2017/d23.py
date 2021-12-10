import queue
import string
import logging
import threading

import primesieve

VALID_COMMANDS = [
    'set', 'sub', 'mul', 'jnz',
]

VALID_REGISTERS = list('abcdefgh')

def logexec(instruction):
    if len(instruction) == 1:
        logging.info(
            '%s: %s',
            instruction.__class__.__name__,
            instruction.operands[0],
        )
    elif len(instruction) == 2:
        logging.info(
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
            'set': Set,
            'sub': Sub,
            'mul': Mul,
            'jnz': Jnz,
        }.get(cmd)(*operands, machine=machine)

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

class Sub(Instruction):
    '''
    `sub X Y` decreases register X by the value of Y.
    '''
    def __init__(self, *operands, machine):
        super().__init__('sub', *operands, machine=machine)

    def exec(self):
        logexec(self)
        self.pc += 1
        self.machine.registers[self.operands[0]] -= self.rm1

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

class Jnz(Instruction):
    '''
    `jnz X Y` jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the
    next instruction, an offset of -1 jumps to the previous instruction, and so on.)
    '''
    def __init__(self, *operands, machine):
        super().__init__('jnz', *operands, machine=machine)

    def exec(self):
        logexec(self)
        offset = self.rm1
        if self.rm0 == 0:
            offset = 1

        self.pc += offset

class VirtualMachine(threading.Thread):
    def __init__(self, program):
        super(VirtualMachine, self).__init__()
        self.daemon = True

        self.instructions = [Instruction.decode(i, self) for i in program]

        self.pc = 0
        self.registers = dict()
        for reg in VALID_REGISTERS:
            self.registers[reg] = 0

        self.mul = 0

    def __repr__(self):
        return '<VirtualMachine: [%d] %s>' % (self.pc, ' '.join('%s:%d' % (k,v) for k,v in self.registers.items()))

    def run(self):
        while self.pc < len(self.instructions) and self.pc >= 0:
            try:
                logging.debug('VM: %r', self)
                instruction = self.instructions[self.pc]
                if isinstance(instruction, Mul):
                    self.mul += 1
                instruction.exec()

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

def parse(data):
    return data.splitlines()

def part1(program):
    vm = VirtualMachine(program)
    vm.run()

    return vm.mul

def part2(program):
    b = 105700
    c = 122700
    step = 17

    primes = primesieve.primes(b, c)
    comps = [k for k in range(b, c+1, step) if k not in primes]

    return len(comps)