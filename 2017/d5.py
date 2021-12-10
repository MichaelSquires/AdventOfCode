import copy
import logging
import itertools

def parse(data):
    return list(map(int, data.splitlines()))

def part1(offsets):
    pc = 0
    count = 0
    while pc >= 0 and pc <= len(offsets):
        try:
            logging.debug('pc %d, offset %d', pc, offsets[pc])
            nextpc = pc + offsets[pc]
            offsets[pc] += 1
            pc = nextpc
            count += 1
        except IndexError:
            break

    return count

def part2(offsets):
    pc = 0
    count = 0
    while pc >= 0 and pc <= len(offsets):
        try:
            logging.debug('pc %d, offset %d', pc, offsets[pc])
            nextpc = pc + offsets[pc]
            curr = offsets[pc]
            if curr >= 3:
                offsets[pc] -= 1
            else:
                offsets[pc] += 1
            pc = nextpc
            count += 1
        except IndexError:
            break

    return count