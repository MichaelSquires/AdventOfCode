import pprint
import logging
import itertools
import collections

from pyparsing import *

COLON = Literal(':').suppress()
COMMA = Literal(',').suppress()
OCOMMA = Optional(COMMA)
NAMETOK = Word(alphas + nums + ' ')
INTTOK = Word(nums).setParseAction(lambda s,l,t: [int(t[0])])
CHILDREN = (
    OCOMMA +
    Literal('children:').suppress() +
    INTTOK.setResultsName('children')

)
CATS = (
    OCOMMA +
    Literal('cats:').suppress() +
    INTTOK.setResultsName('cats') 
)
SAMOYEDS = (
    OCOMMA +
    Literal('samoyeds:').suppress() +
    INTTOK.setResultsName('samoyeds') 
)
POMERANIANS = (
    OCOMMA +
    Literal('pomeranians:').suppress() +
    INTTOK.setResultsName('pomeranians') 
)
AKITAS = (
    OCOMMA +
    Literal('akitas:').suppress() +
    INTTOK.setResultsName('akitas') 
)
VIZSLAS = (
    OCOMMA +
    Literal('vizslas:').suppress() +
    INTTOK.setResultsName('vizslas') 
)
GOLDFISH = (
    OCOMMA +
    Literal('goldfish:').suppress() +
    INTTOK.setResultsName('goldfish') 
)
TREES = (
    OCOMMA +
    Literal('trees:').suppress() +
    INTTOK.setResultsName('trees') 
)
CARS = (
    OCOMMA +
    Literal('cars:').suppress() +
    INTTOK.setResultsName('cars') 
)
PERFUMES = (
    OCOMMA +
    Literal('perfumes:').suppress() +
    INTTOK.setResultsName('perfumes')
)

INPUT = Group(
    NAMETOK.setResultsName('name') +  
    COLON +

    OneOrMore(
        CHILDREN | CATS | SAMOYEDS | 
        POMERANIANS | AKITAS | VIZSLAS | 
        GOLDFISH | TREES | CARS | PERFUMES
    )
)
INPUTS = OneOrMore(INPUT)

Aunt = collections.namedtuple('Aunt', [
    'children', 
    'cats',
    'samoyeds',
    'pomeranians',
    'akitas',
    'vizslas',
    'goldfish',
    'trees',
    'cars',
    'perfumes'
])

CLUES = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}

MYSTERY = Aunt(3, 7, 2, 3, 0, 0, 5, 3, 2, 1)

def part1(data):
    # Narrow down the list with values that we know
    aunts = [k for k in data.values() if k.akitas <= MYSTERY.akitas]
    aunts = [k for k in aunts if k.vizslas <= MYSTERY.vizslas]
    aunts = [k for k in aunts if k.perfumes <= MYSTERY.perfumes]
    aunts = [k for k in aunts if k.cars <= MYSTERY.cars]
    aunts = [k for k in aunts if k.samoyeds <= MYSTERY.samoyeds]
    aunts = [k for k in aunts if k.children <= MYSTERY.children]
    aunts = [k for k in aunts if k.pomeranians <= MYSTERY.pomeranians]
    aunts = [k for k in aunts if k.trees <= MYSTERY.trees]
    aunts = [k for k in aunts if k.goldfish <= MYSTERY.goldfish]
    aunts = [k for k in aunts if k.cats <= MYSTERY.cats]

    pprint.pprint(aunts)

    best = 0
    bestMatches = 0

    for k in aunts:
        matches = 0
        for i in range(len(MYSTERY)):
            if MYSTERY[i] == -1:
                continue

            if MYSTERY[i] == k[i]:
                matches += 1

        if matches > bestMatches:
            best = k

    answer = [k for k,v in data.items() if v == best]
    return answer[0]

def part2(data):
    # Narrow down the list with values that we know
    aunts = [k for k in data.values() if k.akitas <= MYSTERY.akitas]
    aunts = [k for k in aunts if k.vizslas <= MYSTERY.vizslas]
    aunts = [k for k in aunts if k.perfumes <= MYSTERY.perfumes]
    aunts = [k for k in aunts if k.samoyeds <= MYSTERY.samoyeds]
    aunts = [k for k in aunts if k.children <= MYSTERY.children]
    aunts = [k for k in aunts if k.cats <= MYSTERY.cats]

    aunts = [k for k in aunts if k.cars > MYSTERY.cars or k.cars == -1]
    aunts = [k for k in aunts if k.trees > MYSTERY.trees or k.trees == -1]

    aunts = [k for k in aunts if k.pomeranians < MYSTERY.pomeranians or k.pomeranians == -1]
    aunts = [k for k in aunts if k.goldfish < MYSTERY.goldfish or k.goldfish == -1]

    pprint.pprint(aunts)

    best = 0
    bestMatches = 0
    x = []

    for k in aunts:
        matches = 0

        if MYSTERY.akitas == k.akitas:
            matches += 1
        if MYSTERY.vizslas == k.vizslas:
            matches += 1
        if MYSTERY.perfumes == k.perfumes:
            matches += 1
        if MYSTERY.samoyeds == k.samoyeds:
            matches += 1
        if MYSTERY.children == k.children:
            matches += 1
        if MYSTERY.cats == k.cats:
            matches += 1
        if MYSTERY.cars < k.cars:
            matches += 1

        if MYSTERY.trees < k.trees:
            matches += 1

        if MYSTERY.pomeranians > k.pomeranians:
            matches += 1

        if MYSTERY.goldfish > k.goldfish:
            matches += 1

        if matches:
            x.append((matches, k))
            logging.info('k', matches, k)

        if matches > bestMatches:
            best = k

    for m,n in x:
        logging.info([(k,m) for k,v in data.items() if v == n])

    answer = [k for k,v in data.items() if v == best]
    return answer[0]

def parse(data):
    data = INPUTS.parseString(data)

    return {k.name: Aunt(
            k.children or -1,
            k.cats or -1,
            k.samoyeds or -1,
            k.pomeranians or -1,
            k.akitas or -1,
            k.vizslas or -1,
            k.goldfish or -1,
            k.trees or -1,
            k.cars or -1,
            k.perfumes or -1
        ) for k in data
    }