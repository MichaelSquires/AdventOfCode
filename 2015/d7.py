import pprint
import string
import logging
import functools

def AND(x,y):
    return (x & y) & 0xffff

def LSHIFT(x,y):
    return (x << y) & 0xffff

def RSHIFT(x,y):
    return (x >> y) & 0xffff

def OR(x,y):
    return (x | y) & 0xffff

def NOT(x,y):
    return (~x) & 0xffff

# EQ is for the following types of wires:
#   <wire|signal> -> <wire>
def EQ(x,y):
    return x

GATES = {
    'AND': AND,
    'LSHIFT': LSHIFT,
    'RSHIFT': RSHIFT,
    'OR': OR,
    'NOT': NOT,
}

for k,v in list(GATES.items()):
    GATES[v] = k


class Wire:
    def __init__(self, x, y, op):
        self._x = x
        self._y = y
        self._op = op

    def __repr__(self):
        return '<Wire: {} {} {}>'.format(self._x, GATES.get(self._op), self._y)

    def compute(self, circuit):

        # Handle int/long types specially
        if isinstance(self._x, int):
            x = self._x

        # Otherwise, get the wire
        else:
            x = circuit.getWire(self._x)

        # Handle int/long types specially
        if isinstance(self._y, int):
            y = self._y

        # Otherwise, get the wire
        else:
            y = circuit.getWire(self._y)

        # Run the operation
        ret = self._op(x, y)

        logging.debug('{}({}) {} {}({}) -> {}'.format(self._x, x, GATES.get(self._op), self._y, y, ret))

        return ret

# We need a caching layer because the same wires get run over and over
# Adding a cache sped this up from <too long> run-time to sub-second run-time
def cached(func):
    @functools.wraps(func)
    def wrapped(self, name):
        cache = self.__cache__.get(name)
        if None is cache:
            cache = func(self, name)
            self.__cache__[name] = cache
            
        return cache

    return wrapped

class Circuit:
    __cache__ = {}
    def __init__(self):
        self._wires = {}

    def __repr__(self):
        return pprint.pformat(self._wires)

    def clearCache(self):
        self.__cache__ = {}

    def addWire(self, name, wire):
        logging.debug('addWire: {} -> {}'.format(wire, name))
        self._wires[name] = wire

    # Don't believe me that the cache is required? Comment 
    # out the following line and see for yourself
    @cached
    def getWire(self, name):
        logging.debug('getWire: {}'.format(name))
        return self._wires[name].compute(self)

def isNumber(token):
    for k in token:
        if k not in string.digits:
            return False
    return True

def isLower(token):
    for k in token:
        if k not in string.ascii_lowercase:
            return False
    return True

def isGate(token):
    return token in GATES.keys()

def parse(data):
    data = data.splitlines()

    circuit = Circuit()

    for line in data:
        logging.debug(line)
        inputs, output = line.split(' -> ')

        inputs = inputs.split(' ')

        # This case wasn't covered in the docs
        # it's just a straight assignment
        #   1. <signal> -> <wire>
        #   2. <wire> -> <wire>
        if len(inputs) == 1:
            x = inputs[0]
            if isNumber(x):
                x = int(x)

            w = Wire(x, 0, EQ)

        # This can (should) only ever be the NOT wire
        #   NOT <wire> -> <wire>
        elif len(inputs) == 2:
            tok, x = inputs

            if tok != 'NOT':
                raise Exception('Unexpected gate: {}'.format(tok))

            w = Wire(x, 0, NOT)

        # This case includes all the remaining wires
        #   <wire|signal> LSHIFT <wire|signal> -> <wire>
        #   <wire|signal> RSHIFT <wire|signal> -> <wire>
        #   <wire|signal> AND    <wire|signal> -> <wire>
        #   <wire|signal> OR     <wire|signal> -> <wire>
        elif len(inputs) == 3:
            x, tok, y = inputs

            if not isGate(tok):
                raise Exception('Unexpected gate: {}'.format(tok))

            if isNumber(x):
                x = int(x)

            if isNumber(y):
                y = int(y)

            w = Wire(x, y, GATES.get(tok))

        # Add the new wire to the circuit
        circuit.addWire(output, w)

    return circuit

def part1(circuit):
    return circuit.getWire('a')

def part2(circuit):
    # <value of a wire> -> b
    circuit.addWire('b', Wire(circuit.getWire('a'), 0, EQ))

    # Clear the cache to reset all the computed values
    circuit.clearCache()

    return circuit.getWire('a')