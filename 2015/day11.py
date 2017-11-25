#!/usr/bin/env python

import sys
import string
import argparse
import traceback

verbose = False

class Base26:
    __alphabet__ = string.ascii_lowercase

    def __init__(self, b10value):
        # The underlying value is stored as an integer
        self.__value__ = b10value

    def __repr__(self):
        return '<Base{}: {} ({:d})>'.format(len(self.__alphabet__), self.toString(), self.__value__)

    def __str__(self):
        return self.toString()

    def __add__(self, other):
        self.__value__ += other
        return self

    def __radd__(self, other):
        self.__value__ += other
        return self

    def __iadd__(self, other):
        self.__value__ += other
        return self

    def __sub__(self, other):
        self.__value__ -= other
        return self

    def __rsub__(self, other):
        self.__value__ -= other
        return self

    def __isub__(self, other):
        self.__value__ -= other
        return self

    def toString(self):
        ret = []
        div = self.__value__
        mod = 0
        alphalen = len(self.__alphabet__)
        while div > alphalen:
            div, mod = divmod(div, alphalen)
            ret.append(self.__alphabet__[mod])

        ret.append(self.__alphabet__[div])
        ret.reverse()

        return ''.join(ret)

    @classmethod
    def b26decode(cls, value):
        intval = 0
        exponent = 0

        # Validate input
        for digit in value:
            if digit not in cls.__alphabet__:
                raise Exception('Invalid alphabet specified: {}'.format(digit))

        # Iterate over value in reverse order
        for digit in value[::-1]:
            intval += cls.__alphabet__.index(digit) * (len(cls.__alphabet__)**exponent)
            exponent += 1
            
        return cls(intval)

def get_xgrams(data, length):
    ret = []
    count = 0

    while count < len(data) - (length - 1):
        ret.append(data[count:count+length])
        count += 1

    return ret

BADLETTERS = ['i', 'o', 'l']
DIGRAMS = [k*2 for k in string.ascii_lowercase]
TRI_ALPHABET = string.ascii_lowercase
for letter in BADLETTERS:
    TRI_ALPHABET = TRI_ALPHABET.replace(letter, '')
TRIGRAMS = get_xgrams(string.ascii_lowercase, 3)

def isValidPassword(data):
    # Check that there are at least two double characters
    doubles = [k for k in DIGRAMS if k in data]
    if len(doubles) < 2:
        return False

    # Check that there is at least one consecutive sequence of three
    if not [k for k in TRIGRAMS if k in data]:
        return False

    # Check that we don't have any bad letters
    if [k for k in BADLETTERS if k in data]:
        return False

    return True

def part1(data):
    b26 = Base26.b26decode(data)

    while not isValidPassword(b26.toString()):
        b26 += 1

    return b26.toString()

def part2(data):
    b26 = Base26.b26decode(data)

    # The input from part1 is valid so increment by one
    b26 += 1

    while not isValidPassword(b26.toString()):
        b26 += 1

    return b26.toString()

def main(args):

    p1 = part1(args.input)
    print 'Part1: {}'.format(p1)
    print 'Part2: {}'.format(part2(p1))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('input', help='Input', type=str)

    args = parser.parse_args()
    verbose = args.verbose

    try:
        sys.exit(main(args))
    except Exception as exc:
        print 'ERROR: %s' % (exc)
        if verbose:
            traceback.print_exc()
        sys.exit(-1)
