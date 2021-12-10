import copy
import logging

def parse(data):
    lines = data.splitlines()
    return [[int(j) for j in k] for k in lines]

def common(data, col):
    vals = [k[col] for k in data]
    ones = vals.count(1)
    zeroes = vals.count(0)

    if ones == zeroes:
        return None

    if ones > zeroes:
        return 1

    return 0

def most(data, col):
    return common(data, col)

def least(data, col):
    return {
        None: None,
        0: 1,
        1: 0,
    }.get(common(data, col))

def part1(data):
    gamma = ''
    epsilon = ''

    for idx in range(len(data[0])):
        match common(data, idx):
            case 0:
                gamma += '0'
                epsilon += '1'

            case 1:
                gamma += '1'
                epsilon += '0'

    logging.info('GAMMA: %s', gamma)
    logging.info('EPSILON: %s', epsilon)

    g = int(gamma, 2)
    e = int(epsilon, 2)

    return g * e

def reduce_(data, col, val):
    return [k for k in data if k[col] == val]

def part2(data):
    oxy = copy.copy(data)
    co2 = copy.copy(data)

    length = len(data[0])

    for idx in range(length):
        if len(oxy) == 1:
            break
        cmn = most(oxy, idx)
        if cmn is None:
            cmn = 1

        oxy = reduce_(oxy, idx, cmn)

        logging.debug('OXY: (%d) %r', len(oxy), oxy)

    for idx in range(length):
        if len(co2) == 1:
            break
        cmn = least(co2, idx)
        logging.debug('CMN: %s', cmn)
        if cmn is None:
            cmn = 0

        co2 = reduce_(co2, idx, cmn)

        logging.debug('CO2: (%d) %r', len(co2), co2)

    logging.info('OXY: %r', oxy)
    logging.info('CO2: %r', co2)

    oxy = int(''.join([str(k) for k in oxy[0]]), 2)
    co2 = int(''.join([str(k) for k in co2[0]]), 2)

    return oxy * co2
