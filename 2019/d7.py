import queue
import logging
import functools
import itertools
import threading

from . import intcode

#SAMPLE = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
#SAMPLE = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
#SAMPLE = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
#SAMPLE = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
SAMPLE = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'

parse = intcode.parse

class State:
    high = 0

def infunc(q):
    return q.get()

def outfunc(q, state, val):
    q.put(val)

    if val > state.high:
        state.high = val

class ThreadedComputer(intcode.Computer, threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

def solve(prog, data):

    A = ThreadedComputer()
    B = ThreadedComputer()
    C = ThreadedComputer()
    D = ThreadedComputer()
    E = ThreadedComputer()

    A.load(prog)
    B.load(prog)
    C.load(prog)
    D.load(prog)
    E.load(prog)

    state = State()

    EA = queue.SimpleQueue()
    AB = queue.SimpleQueue()
    BC = queue.SimpleQueue()
    CD = queue.SimpleQueue()
    DE = queue.SimpleQueue()

    EA.put(data.pop(0))
    EA.put(0)

    AB.put(data.pop(0))
    BC.put(data.pop(0))
    CD.put(data.pop(0))
    DE.put(data.pop(0))

    A.infunc = functools.partial(infunc, EA)
    A.outfunc = functools.partial(outfunc, AB, state)

    B.infunc = functools.partial(infunc, AB)
    B.outfunc = functools.partial(outfunc, BC, state)

    C.infunc = functools.partial(infunc, BC)
    C.outfunc = functools.partial(outfunc, CD, state)

    D.infunc = functools.partial(infunc, CD)
    D.outfunc = functools.partial(outfunc, DE, state)

    E.infunc = functools.partial(infunc, DE)
    E.outfunc = functools.partial(outfunc, EA, state)

    [k.start() for k in [A, B, C, D, E]]
    [k.join() for k in [A, B, C, D, E]]

    return state.high

def permute(prog, phases):
    high = 0
    for data in itertools.permutations(phases):
        data = list(data)
        new = solve(prog, data)
        if new > high:
            high = new
            logging.info('New High: %s', new)

    return high

def part1(prog):
    return permute(prog, range(5))

def part2(prog):
    return permute(prog, range(5, 10))
