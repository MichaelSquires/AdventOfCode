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
    AdjRel  = 9
    Halt    = 99
    
INSTRUCTIONS = {}
def make_instruction(opcode, opcount):
    oplist = [f'op{k}' for k in range(1, opcount+1)]
    ret = collections.namedtuple(opcode.name, oplist)
    INSTRUCTIONS[opcode] = ret
    return ret
    
# 0-opcode instructions
Halt = make_instruction(Opcode.Halt, 0)

# 1-opcode instructions
Input = make_instruction(Opcode.Input, 1)
Output = make_instruction(Opcode.Output, 1)
AdjRel = make_instruction(Opcode.AdjRel, 1)

# 2-opcode instructions
Jt = make_instruction(Opcode.Jt, 2)
Jf = make_instruction(Opcode.Jf, 2)

# 3-opcode instructions
Lt = make_instruction(Opcode.Lt, 3)
Eq = make_instruction(Opcode.Eq, 3)
Add = make_instruction(Opcode.Add, 3)
Mult = make_instruction(Opcode.Mult, 3)

class InvalidOperand(Exception):
    pass

class Position(int):
    def __repr__(self):
        return f'{int.__repr__(self)}_P'

class Immediate(int):
    def __repr__(self):
        return f'{int.__repr__(self)}_I'

class Relative(int):
    def __repr__(self):
        return f'{int.__repr__(self)}_R'
        
MODES = {
    0: Position,
    1: Immediate,
    2: Relative,
}

def opmode(opcode, oplist):
    # Reverse opcode string into integers
    opmap = list(map(int, str(opcode)[::-1]))

    # Pad opmap with zeroes if needed
    while len(opmap) - 2 < len(oplist):
        opmap.append(0)

    opret = []
    for idx, opval in enumerate(oplist):
        mode = opmap[idx + 2]
        
        if mode not in MODES:
            raise InvalidOperand('Unsupported mode %s', mode)
            
        opret.append(MODES.get(mode)(opval))

    return opcode % 100, opret

def infunc():
    return int(input('Enter value: '))

def outfunc(val):
    print(f'OUTPUT: {val}')

class Computer:
    def __init__(self):
        super().__init__()
        self.pc = 0
        self.mem = []
        self.base = 0

        self.running = False

        self.last_in = None
        self.last_out = None

        self.infunc = infunc
        self.outfunc = outfunc

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
        
    def _check_addr(self, addr):
        if addr < 0:
            raise Exception(f'Invalid address: {addr}')

        if addr > len(self.mem) - 1:
            diff = addr - (len(self.mem) - 1)
            logging.debug('Extending memory by %d', diff)
            self.mem += ([0] * diff)

    def _rval(self, op):
        match op:
            case Position(addr):
                addr = int(addr)
            case Immediate(val):
                return int(val)
            case Relative(addr):
                addr = int(self.base + addr)
            case _:
                raise InvalidOperand(op)

        self._check_addr(addr)
        return int(self.mem[addr])

    def _wval(self, op, val):
        match op:
            case Position(addr):
                addr = int(addr)
            case Relative(addr):
                addr = int(self.base + addr)
            case _:
                raise InvalidOperand(op)

        self._check_addr(addr)
        self.mem[addr] = val

    def _run(self):
        instruction = self._decode()

        ### Execute instruction
        match instruction:
            case Halt():
                self.running = False

            case Input(op1):
                val = self.infunc()
                self.last_in = val
                self._wval(op1, val)

            case Output(op1):
                val = self._rval(op1)
                self.last_out = val
                self.outfunc(val)
                
            case AdjRel(op1):
                val = self._rval(op1)
                self.base += val

            case Jt(op1, op2):
                val = self._rval(op1)
                if val != 0:
                    self.pc = self._rval(op2)

            case Jf(op1, op2):
                val = self._rval(op1)
                if val == 0:
                    self.pc = self._rval(op2)

            case Lt(op1, op2, op3):
                val1 = self._rval(op1)
                val2 = self._rval(op2)
                self._wval(op3, int(val1 < val2))

            case Eq(op1, op2, op3):
                val1 = self._rval(op1)
                val2 = self._rval(op2)
                self._wval(op3, int(val1 == val2))

            case Add(op1, op2, op3):
                val1 = self._rval(op1)
                val2 = self._rval(op2)
                self._wval(op3, val1 + val2)

            case Mult(op1, op2, op3):
                val1 = self._rval(op1)
                val2 = self._rval(op2)
                self._wval(op3, val1 * val2)

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
