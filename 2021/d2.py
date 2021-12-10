#!/usr/bin/env python

import logging
import collections

def part1(data):
    pos = 0
    depth = 0

    for command in data:
        match command.direction:
            case 'up':
                depth -= command.distance
            case 'down':
                depth += command.distance
            case 'forward':
                pos += command.distance

    logging.debug('POS: %s', pos)
    logging.debug('DEPTH: %s', depth)

    print(f'ANS: {pos * depth}')


def part2(data):
    aim = 0
    pos = 0
    depth = 0

    for command in data:
        match command.direction:
            case 'up':
                aim -= command.distance
            case 'down':
                aim += command.distance
            case 'forward':
                pos += command.distance
                depth += aim * command.distance

    logging.debug('POS: %s', pos)
    logging.debug('DEPTH: %s', depth)

    print(f'ANS: {pos * depth}')

Command = collections.namedtuple('Command', ('direction', 'distance'))
def make(t):
    return Command(t[0], int(t[1]))

def parse(data):
    return [make(k.split()) for k in data.splitlines()]
