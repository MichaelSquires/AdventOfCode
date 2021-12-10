import hashlib
import logging

def part1(key):
    nonce = 0

    while True:
        digest = hashlib.md5(f'{key}{nonce}'.encode()).hexdigest()
        if digest.startswith('00000'):
            return nonce

        nonce += 1

        if nonce % 100000 == 0:
            logging.debug('Nonce: {:d}'.format(nonce))

def part2(key):
    nonce = 0

    while True:
        digest = hashlib.md5(f'{key}{nonce}'.encode()).hexdigest()
        if digest.startswith('000000'):
            return nonce

        nonce += 1

        if nonce % 100000 == 0:
            logging.debug('Nonce: {:d}'.format(nonce))

def parse(data):
    return data.splitlines()[0]