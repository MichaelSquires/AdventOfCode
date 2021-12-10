import logging
import itertools

def count(line):
    d = {}
    for k in line:
        if k not in d:
            d[k] = 0
        d[k] += 1

    twos = False
    threes = False

    values = d.values()
    logging.debug('D: %s', d)
    logging.debug('VALUES: %s', values)

    if 2 in values:
        twos = True

    if 3 in values:
        threes = True

    return (twos, threes)

def part1(data):

    twos = 0
    threes = 0

    for line in data:
        _twos, _threes = count(line)
        if _twos:
            twos += 1

        if _threes:
            threes += 1

    logging.info('TWOS: %d', twos)
    logging.info('THREES: %d', threes)

    print('Part 1:', twos * threes)
    return twos * threes

def part2(data):

    while True:
        curr = list(data.pop())

        found = None

        for k in data:
            k = list(k)
            diff = []
            for i in range(len(curr)):
                diff.append(curr[i] - k[i])

            if diff.count(0) == len(curr) - 1:
                logging.info('FOUND', bytes(curr), bytes(k))
                found = (curr, k)
                break

        if found:
            a,b = found
            answer = []
            for k in range(len(a)):
                if a[k] == b[k]:
                    answer.append(a[k])

            break

    print('Part 2:', bytes(answer).decode('utf-8'))

def parse(data):
    return data.splitlines()