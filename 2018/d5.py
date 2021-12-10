import re
import string
import logging

def react(polymer, combinations):
    while True:
        size = len(polymer)

        for ptype in combinations:
            polymer = polymer.replace(ptype, '')

        if len(polymer) == size:
            break

    return polymer

def part1(data):
    combinations = []
    for letter in string.ascii_lowercase:
        combinations.append('%s%s' % (letter, letter.upper()))
        combinations.append('%s%s' % (letter.upper(), letter))

    polymer = react(data, combinations)

    logging.debug('DATA: %r', polymer)
    return len(polymer)

def part2(data):
    combinations = []
    for letter in string.ascii_lowercase:
        combinations.append('%s%s' % (letter, letter.upper()))
        combinations.append('%s%s' % (letter.upper(), letter))

    shortest = len(data)

    for letter in string.ascii_lowercase:
        polymer = react(data.replace(letter, '').replace(letter.upper(), ''), combinations)
        if len(polymer) < shortest:
            shortest = len(polymer)

    return shortest

def parse(data):
    return data.strip()