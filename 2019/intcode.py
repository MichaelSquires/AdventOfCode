import copy
import enum
import logging
import collections

class InvalidInstruction(Exception):
    pass

class Opcode(enum.IntEnum):
    Add     = 1
    Mult    = 2
    Input   = 3
    Output  = 4
    Jt      = 5
    Jf      = 6
    Lt      = 7
    Eq      = 8
    Halt    = 99
    
INSTRUCTIONS = {}
def instruction(opcode, opcount):
    oplist = [f'op{k}' for k in range(1, opcount+1)]
    ret = collections.namedtuple(opcode.name, oplist)
    INSTRUCTIONS[opcode] = ret
    return ret
    
# 0-opcode instructions
Halt = instruction(Opcode.Halt, 0)

# 1-opcode instructions
Input = instruction(Opcode.Input, 1)
Output = instruction(Opcode.Output, 1)

# 2-opcode instructions
Jt = instruction(Opcode.Jt, 2)
Jf = instruction(Opcode.Jf, 2)

# 3-opcode instructions
Lt = instruction(Opcode.Lt, 3)
Eq = instruction(Opcode.Eq, 3)
Add = instruction(Opcode.Add, 3)
Mult = instruction(Opcode.Mult, 3)


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

def infunc():
    return int(input('Enter value: '))

def outfunc(val):
    print(f'OUTPUT: {val}')
    assert val == 0

class Computer:
    def __init__(self):
        super().__init__()
        self.pc = 0
        self.mem = []

        self.running = False

        self.infunc = infunc
        self.outfunc = outfunc

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
        
        inscls = INSTRUCTIONS.get(opval, None)
        if inscls is None:
            raise InvalidInstruction(f'Invalid opcode: {opcode}')
            
        _, oplist = opmode(opcode, self.mem[self.pc+1:self.pc+1+len(inscls._fields)])
        
        instruction = inscls(*oplist)

        logging.debug('Decoded (pc %d) %s -> %s', self.pc, self.mem[self.pc: self.pc + len(instruction) + 1], instruction)
        self.pc += len(instruction) + 1

        return instruction

    def _run(self):
        instruction = self._decode()

        ### Execute instruction
        match instruction:
            case Halt():
                self.running = False

            case Input(op1):
                val = self.infunc()
                self.mem[op1] = val

            case Output(op1):
                val = self._opval(op1)
                self.outfunc(val)

            case Jt(op1, op2):
                val = self._opval(op1)
                if val != 0:
                    self.pc = self._opval(op2)

            case Jf(op1, op2):
                val = self._opval(op1)
                if val == 0:
                    self.pc = self._opval(op2)

            case Lt(op1, op2, op3):
                val1 = self._opval(op1)
                val2 = self._opval(op2)
                self.mem[op3] = int(val1 < val2)

            case Eq(op1, op2, op3):
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


def parse(data):
    return list(map(int, data.split(',')))
