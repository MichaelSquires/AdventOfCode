import logging

def parse(data):
    return data.strip()

def part1(data):
    total = 0
    for i in range(len(data) - 1):
        if data[i] != data[i+1]:
            continue

        logging.debug('%s == %s', data[i], data[i+1])
        total += int(data[i])

    if data[-1] == data[0]:
        total += int(data[-1])

    return total

def part2(data):
    total = 0
    dlen = len(data)
    half = dlen/2
    for i in range(dlen):
        idx = int((i+half)%dlen)
        if data[i] != data[idx]:
            continue

        logging.debug('%s == %s', data[i], data[idx])
        total += int(data[i])

    return total