import logging
import pathlib

def part1(data):
    return sum(data)

def part2(data):
    freq = 0
    # I originally had a list here that I would append seen frequencies
    # to but that turned out to slow enough that I wasn't patient enough
    # to let it finish. The dictionary wound up being incredibly fast -
    # less than one second.
    seen = {}

    while True:
        for k in data:
            freq += k
            if freq in seen:
                return freq

            seen[freq] = 0

def parse(data):
    return list(map(int, data.splitlines()))