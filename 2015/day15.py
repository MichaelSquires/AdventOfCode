#!/usr/bin/env python

import sys
import pprint
import argparse
import itertools
import traceback

from pyparsing import *

COLON = Literal(':').suppress()
COMMA = Literal(',').suppress()
NAMETOK = Word(alphas)
INTTOK = Word(nums + '-').setParseAction(lambda s,l,t: [int(t[0])])

INPUT = Group(
    NAMETOK.setResultsName('name') +  
    COLON +
    Literal('capacity').suppress() +
    INTTOK.setResultsName('capacity') + 
    COMMA +
    Literal('durability').suppress() +
    INTTOK.setResultsName('durability') + 
    COMMA +
    Literal('flavor').suppress() +
    INTTOK.setResultsName('flavor') + 
    COMMA +
    Literal('texture').suppress() +
    INTTOK.setResultsName('texture') + 
    COMMA +
    Literal('calories').suppress() +
    INTTOK.setResultsName('calories')
)
INPUTS = OneOrMore(INPUT)

verbose = False

TOTAL_WEIGHT = 100

class Ingredient:
    def __init__(self, name, capacity, durability, flavor, texture, calories):
        self.name = name
        self.capacity = capacity
        self.durability = durability
        self.flavor = flavor
        self.texture = texture
        self.calories = calories

    def __repr__(self):
        return '<Ingredient: {}: capacity {:d}, durability {:d}, flavor {:d}, texture {:d}, calories {:d}, weight {:d}>'.format(
            self.name,
            self.capacity,
            self.durability,
            self.flavor,
            self.texture,
            self.calories,
            self.weight
        )

    def __mul__(self, other):
        if not isinstance(other, (int, long)):
            raise Exception('Invalid type')

        return Ingredient(
            self.name,
            self.capacity * other,
            self.durability * other,
            self.flavor * other,
            self.texture * other,
            self.calories * other
        )

    def __add__(self, other):
        if not isinstance(other, Ingredient):
            raise Exception('Invalid type: {}'.format(type(other)))

        capacity = max(0, self.capacity + other.capacity)
        durability = max(0, self.durability + other.durability)
        flavor = max(0, self.flavor + other.flavor)
        texture = max(0, self.texture + other.texture)
        calories = self.calories + other.calories

        return Ingredient(
            self.name+other.name,
            capacity,
            durability,
            flavor,
            texture,
            calories
        )

    @property
    def weight(self):
        return self.capacity * self.durability * self.flavor * self.texture 

def isum(ilist):
    # Special sum function just for adding lists of ingredients
    ret = ilist[0]
    for i in ilist[1:]:
        ret += i
    return ret

# itertools.permutations and itertools.combinations doesn't do what I need
# I expected it to give me tuples that are in ascending order such as:
#
#    (0, 0, 0, 0)
#    (0, 0, 0, 1)
#    (0, 0, 0, 2)
#    ...
#    (99, 99, 99, 0)
#    (99, 99, 99, 1)
#    (99, 99, 99, 2)
#
# Instead, they each have their own quirks. These really messed me up when trying
# to solve this challenge because I thought I was getting a sequence but instead,
# there are gaps. This function gives a sequence
def sequence(maxval, width=1):

    endval = (maxval ** width)

    _sequence = [0] * width

    for i in xrange(endval):
        index = width - 1

        div, mod = divmod(i, maxval)
        _sequence[index] = mod

        index -= 1

        while div >= maxval:
            div, mod = divmod(div, maxval)

            _sequence[index] = mod

            index -= 1

        _sequence[index] = div

        yield _sequence

def part1(data):
    
    best = 0

    for ratio in sequence(TOTAL_WEIGHT, len(data)):

        # If the ratio doesn't add up to TOTAL_WEIGHT, it's an invalid combination
        if sum(ratio) != TOTAL_WEIGHT:
            continue

        # Multiple the ingredients times their ratios
        ingredients = [k*j for k,j in zip(data, ratio)]

        # Add up all the weights and get their weight
        cookie = isum(ingredients)
        if 0 == cookie.weight:
            continue

        # IF this is the best weight we've seen, record it
        if cookie.weight > best:
            if verbose:
                print 'weight:', cookie, ratio
            best = cookie.weight

    return best

def part2(data):
    best = 0

    for ratio in sequence(TOTAL_WEIGHT, len(data)):

        # If the ratio doesn't add up to TOTAL_WEIGHT, it's an invalid combination
        if sum(ratio) != TOTAL_WEIGHT:
            continue

        # Multiple the ingredients times their ratios
        ingredients = [k*j for k,j in zip(data, ratio)]

        # Add up all the weights and get their weight
        cookie = isum(ingredients)
        if 0 == cookie.weight or 500 != cookie.calories:
            continue

        # IF this is the best weight we've seen, record it
        if cookie.weight > best:
            if verbose:
                print 'weight:', cookie, ratio
            best = cookie.weight

    return best

def main(args):

    data = INPUTS.parseFile(args.file)

    data = [Ingredient(k.name, k.capacity, k.durability, k.flavor, k.texture, k.calories) for k in data]

    if verbose:
        pprint.pprint(data)

    print 'Part1: {:d}'.format(part1(data))
    print 'Part2: {:d}'.format(part2(data))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-i', '--interact', help='Show verbose messages', action='store_true')
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=file)

    args = parser.parse_args()
    verbose = args.verbose

    try:
        sys.exit(main(args))
    except Exception as exc:
        print 'ERROR: %s' % (exc)
        if verbose:
            traceback.print_exc()
        sys.exit(-1)
