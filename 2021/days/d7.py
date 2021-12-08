import math
import logging
import statistics

def parse(data):
    return list(map(int, data.split(',')))

def diff(a, b):
    return max(a, b) - min(a, b)

def fact(a, b):
    return sum(range(diff(a,b) + 1))

def fuel(func, center, data):
    return sum(map(func, data, [center] * len(data)))

def part1(data):
    median = statistics.median(data)
    return fuel(diff, median, data)

def part2(data):
    mean = statistics.mean(data)

    return min(
        fuel(fact, math.floor(mean), data),
        fuel(fact, math.ceil(mean), data)
    )