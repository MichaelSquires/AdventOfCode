import logging
import itertools

TOTAL_VOLUME = 150

def part1(data):
    ret = 0
    
    for i in range(2, len(data)):
        for k in itertools.combinations(data, i):
            if sum(k) == TOTAL_VOLUME:
                ret += 1
    return ret

def part2(data):
    ret = len(data)
    for i in range(2, len(data)):
        for k in itertools.combinations(data, i):
            if sum(k) != TOTAL_VOLUME:
                continue

            length = len(k)
            if length < ret:
                logging.debug(k, length)
                ret = length

    return ret

def parse(data):
    return list(map(int, data.splitlines()))