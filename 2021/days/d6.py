import logging
import collections

def parse(data):
    timers = list(map(int, data.split(',')))
    fish = collections.deque([0] * 9)

    for ii in timers:
        fish[ii] += 1

    return fish

def count(fish, iterations):
    for ii in range(iterations):
        zero = fish[0]
        fish.rotate(-1)
        fish[6] += zero
        logging.debug('FISH: %s', fish)

    return sum(fish)

def part1(fish):
    return count(fish, 80)

def part2(fish):
    return count(fish, 256)