import copy
import logging

def spin(programs, count):
    return programs[count*-1:] + programs[:count*-1]

def exchange(programs, a, b):
    logging.debug('A: %d, B: %d', a, b)
    aval = programs[a]
    bval = programs[b]
    logging.debug('AVAL: %s, BVAL: %s', aval, bval)
    programs[a] = bval
    programs[b] = aval
    return programs

def partner(programs, a, b):
    aidx = programs.index(a)
    bidx = programs.index(b)
    logging.debug('AIDX: %d, BIDX: %d', aidx, bidx)

    aval = programs[aidx]
    bval = programs[bidx]
    logging.debug('AVAL: %s, BVAL: %s', aval, bval)

    programs[aidx] = bval
    programs[bidx] = aval
    return programs

def parse(data):
    return data.strip().split(',')

def dance(programs, data):
    for move in data:
        logging.debug('MOVE: %s', move)
        logging.debug('PROGRAMS: %r', programs)
        if move[0] == 's':
            programs = spin(programs, int(move[1:]))

        elif move[0] == 'x':
            a, b = move[1:].split('/')
            a = int(a)
            b = int(b)
            programs = exchange(programs, a, b)

        elif move[0] == 'p':
            a, b = move[1:].split('/')
            programs = partner(programs, a, b)

    return programs

def part1(data):
    programs = dance(list('abcdefghijklmnop'), data)
    return ''.join(programs)

def part2(data):
    programs = list('abcdefghijklmnop')

    combinations = [copy.copy(programs)]
    for i in range(1000000000):
        programs = dance(programs, data)
        combinations.append(copy.copy(programs))

        if i == 0:
            first = copy.copy(programs)
            continue

        if programs == first:
            break

    idx = 1000000000 % i

    return ''.join(combinations[idx])