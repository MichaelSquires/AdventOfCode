import sys
import copy
import enum
import logging
import collections

class InvalidInstruction(Exception):
    pass

class Opcode(enum.IntEnum):
    ADD     = 1
    MULT    = 2
    INPUT   = 3
    OUTPUT  = 4
    JT      = 5
    JF      = 6
    LT      = 7
    EQ      = 8
    HALT    = 99

# 0-opcode instructions
Halt = collections.namedtuple('Halt', [])

# 1-opcode instructions
Input = collections.namedtuple('Input', ['op1'])
Output = collections.namedtuple('Output', ['op1'])

# 2-opcode instructions
JumpTrue = collections.namedtuple('JumpTrue', ['op1', 'op2'])
JumpFalse = collections.namedtuple('JumpFalse', ['op1', 'op2'])

# 3-opcode instructions
LessThan = collections.namedtuple('LessThan', ['op1', 'op2', 'op3'])
Equal = collections.namedtuple('Equal', ['op1', 'op2', 'op3'])
Add = collections.namedtuple('Add', ['op1', 'op2', 'op3'])
Mult = collections.namedtuple('Mult', ['op1', 'op2', 'op3'])

class InvalidOperand(Exception):
    pass

class Position(int):
    def __repr__(self):
        return f'{int.__repr__(self)}_P'

class Immediate(int):
    def __repr__(self):
        return f'{int.__repr__(self)}_I'

def opmode(opcode, oplist):
    # Reverse opcode string into integers
    opmap = list(map(int, str(opcode)[::-1]))

    # Pad opmap with zeroes if needed
    while len(opmap) - 2 < len(oplist):
        opmap.append(0)

    opret = []
    for idx, opval in enumerate(oplist):
        mode = opmap[idx + 2]
        assert mode in (0, 1)

        match mode:
            case 0:
                opret.append(Position(opval))
            case 1:
                opret.append(Immediate(opval))

    return opcode % 100, opret

class Computer:
    def __init__(self):
        self.pc = 0
        self.mem = []

        self.running = False

        self.infunc = None
        self.outfunc = None

    def _opval(self, op):
        match op:
            case Position(addr):
                return int(self.mem[addr])

            case Immediate(val):
                return int(val)

            case _:
                raise InvalidOperand(op)

    def _decode(self):

        ### Read a full instruction
        opcode = self.mem[self.pc]
        opval, _ = opmode(opcode, ())

        match opval:
            # One-byte opcodes
            case Opcode.HALT:   instruction = Halt()
            case _:
                op1 = self.mem[self.pc + 1]
                opval, (op1,) = opmode(opcode, (op1,))

                match opval:
                    # Two-byte opcodes
                    case Opcode.INPUT:  instruction = Input(op1)
                    case Opcode.OUTPUT: instruction = Output(op1)
                    case _:
                        op2 = self.mem[self.pc + 2]
                        opval, (op1, op2) = opmode(opcode, (op1, op2))

                        match opval:
                            # Three-byte opcodes
                            case Opcode.JT: instruction = JumpTrue(op1, op2)
                            case Opcode.JF: instruction = JumpFalse(op1, op2)
                            case _:
                                op3 = self.mem[self.pc + 3]
                                opval, (op1, op2, op3) = opmode(opcode, (op1, op2, op3))

                                match opval:
                                    # Four-byte opcodes
                                    case Opcode.LT:     instruction = LessThan(op1, op2, op3)
                                    case Opcode.EQ:     instruction = Equal(op1, op2, op3)
                                    case Opcode.ADD:    instruction = Add(op1, op2, op3)
                                    case Opcode.MULT:   instruction = Mult(op1, op2, op3)
                                    case _:
                                        raise InvalidInstruction(f'Invalid opcode: {opcode}')

        logging.debug('Decoded %s -> %s', self.mem[self.pc: self.pc + len(instruction) + 1], instruction)
        self.pc += len(instruction) + 1

        return instruction

    def _run(self):
        instruction = self._decode()

        ### Execute instruction
        match instruction:
            case Halt():
                self.running = False

            case Input(op1):
                val = self.input()
                self.mem[op1] = val

            case Output(op1):
                val = self._opval(op1)
                self.output(val)

            case JumpTrue(op1, op2):
                val = self._opval(op1)
                if val != 0:
                    self.pc = self._opval(op2)

            case JumpFalse(op1, op2):
                val = self._opval(op1)
                if val == 0:
                    self.pc = self._opval(op2)

            case LessThan(op1, op2, op3):
                val1 = self._opval(op1)
                val2 = self._opval(op2)
                self.mem[op3] = int(val1 < val2)

            case Equal(op1, op2, op3):
                val1 = self._opval(op1)
                val2 = self._opval(op2)
                self.mem[op3] = int(val1 == val2)

            case Add(op1, op2, op3):
                val1 = self._opval(op1)
                val2 = self._opval(op2)
                self.mem[op3] = val1 + val2

            case Mult(op1, op2, op3):
                val1 = self._opval(op1)
                val2 = self._opval(op2)
                self.mem[op3] = val1 * val2

            case _:
                raise InvalidInstruction(f'Invalid instruction: f{instruction}')

    def load(self, data):
        assert isinstance(data, list)
        assert all(isinstance(k, int) for k in data)

        self.mem = copy.copy(data)
        self.pc = 0

    def run(self):
        try:
            self.running = True
            while self.running:
                self._run()
        finally:
            self.running = False

    def input(self):
        if self.infunc and callable(self.infunc):
            return self.infunc()  # pylint: disable=not-callable

        return int(input('Enter value: '))

    def output(self, val):
        self.out = val

        if self.outfunc and callable(self.outfunc):
            return self.outfunc(val)  # pylint: disable=not-callable

        print(f'OUTPUT: {val}')
        assert val == 0


def parse(data):
    return list(map(int, data.split(',')))
