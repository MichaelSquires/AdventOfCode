import hashlib
import logging

def parse(data):
    return data.strip()
TRIPLES = {
    k*3 for k in '0123456789abcdef'
}

def hashfunc(data, rounds=1):
    digest = data
    for i in range(rounds):
        digest = hashlib.md5(digest.encode()).hexdigest()

    return digest

def check_three(digest):
    threes = [triple for triple in TRIPLES if triple in digest]
    lowest = 99
    three = None
    for k in threes:
        index = digest.index(k)
        if index < lowest:
            three = k
        lowest = index

    return three

def check_fives(salt, index, three, rounds=1):
    five = three[0]*5

    found_five = False
    subindex = 0
    while subindex <= 1000:
        subindex += 1
        digest = hashfunc('{}{}'.format(salt, index+subindex), rounds)

        if five not in digest:
            continue

        logging.info('FIVE: %s, digest:%s, index:%d, subindex:%d', five, digest, index, subindex)
        found_five = True

    return found_five

def getkey(salt, rounds=1):
    index = -1
    key = 0
    while key < 64:
        index += 1
        if index % 1000 == 0:
            logging.info('INDEX: %d', index)

        digest = hashfunc('{}{}'.format(salt, index), rounds)
        logging.debug('digest: %s', digest)

        three = check_three(digest)
        if not three:
            continue

        logging.info('THREE:%s, digest:%s, index:%d', three, digest, index)
        if not check_fives(salt, index, three, rounds):
            continue

        logging.info('FOUND KEY %d', key)
        key += 1

    return index

def part1(salt):
    return getkey(salt)

def part2(salt):
    return getkey(salt, 2017)