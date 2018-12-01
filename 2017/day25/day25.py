#!/usr/bin/env python

import sys
import logging
import argparse
import itertools

LEFT = 0
RIGHT = 1

class TuringMachine:
    def __init__(self, state):
        self.tape = [0]
        self.cursor = 0
        self.state = state

    def __repr__(self):
        return '<Turing (%d)/%d %r>' % (self.cursor, len(self.tape), self.state)

    def step(self):
        logging.debug('STEP: %r', self)
        state = self.state(self)
        currval = self.tape[self.cursor]
        state.step(currval)

    def write(self, value):
        logging.debug('WRITE: (%d) %d', self.cursor, value)
        self.tape[self.cursor] = value

    def move(self, direction):
        assert direction in (LEFT, RIGHT)
        if direction == LEFT:
            if self.cursor == 0:
                self.tape.insert(0, 0)
            else:
                self.cursor -= 1

            logging.debug('MOVE: L %d', self.cursor)

        if direction == RIGHT:
            if self.cursor + 1 == len(self.tape):
                self.tape.append(0)

            self.cursor += 1

            logging.debug('MOVE: R %d', self.cursor)

    def cont(self, state):
        logging.debug('CONT: %r', state)
        self.state = state

    @property
    def checksum(self):
        return self.tape.count(1)

class State:
    def __init__(self, machine):
        self.machine = machine

    def __repr__(self):
        return '%s' % (self.__class__.__name__)

    def step(self, currval):
        assert currval in (0, 1)

        if currval == 0:
            self.curr0()
        else:
            self.curr1()

    def curr0(self):
        raise NotImplementedError

    def curr1(self):
        raise NotImplementedError

    def write(self, value):
        self.machine.write(value)

    def move(self, direction):
        self.machine.move(direction)

    def cont(self, state):
        self.machine.cont(state)

class StateA(State):
    '''
    In state A:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state B.
      If the current value is 1:
        - Write the value 0.
        - Move one slot to the left.
        - Continue with state C.
    '''
    def curr0(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(StateB)

    def curr1(self):
        self.write(0)
        self.move(LEFT)
        self.cont(StateC)

class StateB(State):
    '''
    In state B:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the left.
        - Continue with state A.
      If the current value is 1:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state C.
    '''
    def curr0(self):
        self.write(1)
        self.move(LEFT)
        self.cont(StateA)

    def curr1(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(StateC)

class StateC(State):
    '''
    In state C:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state A.
      If the current value is 1:
        - Write the value 0.
        - Move one slot to the left.
        - Continue with state D.
    '''
    def curr0(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(StateA)

    def curr1(self):
        self.write(0)
        self.move(LEFT)
        self.cont(StateD)

class StateD(State):
    '''
    In state D:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the left.
        - Continue with state E.
      If the current value is 1:
        - Write the value 1.
        - Move one slot to the left.
        - Continue with state C.
    '''
    def curr0(self):
        self.write(1)
        self.move(LEFT)
        self.cont(StateE)

    def curr1(self):
        self.write(1)
        self.move(LEFT)
        self.cont(StateC)

class StateE(State):
    '''
    In state E:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state F.
      If the current value is 1:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state A.
    '''
    def curr0(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(StateF)

    def curr1(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(StateA)

class StateF(State):
    '''
    In state F:
      If the current value is 0:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state A.
      If the current value is 1:
        - Write the value 1.
        - Move one slot to the right.
        - Continue with state E.
    '''
    def curr0(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(StateA)

    def curr1(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(StateE)

class SampleA(State):
    def curr0(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(SampleB)

    def curr1(self):
        self.write(0)
        self.move(LEFT)
        self.cont(SampleB)

class SampleB(State):
    def curr0(self):
        self.write(1)
        self.move(LEFT)
        self.cont(SampleA)

    def curr1(self):
        self.write(1)
        self.move(RIGHT)
        self.cont(SampleA)

def main(args):

    if args.part == 0:
        sample()

    if args.part in (None, 1):
        part1()

    return 0

def sample():
    machine = TuringMachine(SampleA)
    for i in range(6):
        machine.step()

    print('Sample:', machine.checksum)

def part1():
    '''
    Begin in state A.
    Perform a diagnostic checksum after 12134527 steps.
    '''

    machine = TuringMachine(StateA)
    for i in range(12134527):
        machine.step()

    print('Part 1:', machine.checksum)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[0, 1])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    # parser.add_argument('file', help='Input file', type=open)

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
