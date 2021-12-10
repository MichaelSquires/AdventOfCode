import copy
import logging
import collections

def parse(data):
    return int(data.strip())

def part1(steps):
    spins = 2017
    buf = collections.deque([0])
    curpos = 0

    adj = 0
    for i in range(1,spins+1):
        index = (curpos + steps) % i
        buf.insert(index, i)
        curpos = index + 1

    n = buf.index(2017)

    return buf[n+1]

def part2(steps):
    spins = 50000000
    curpos = 0

    adj = 0
    for i in range(1,spins+1):
        index = (curpos + steps) % i
        curpos = index + 1
        if curpos == 1:
            adj = i

    return adj