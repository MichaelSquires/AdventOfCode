import hashlib
import logging

def parse(data):
    return data.splitlines()[0]

def part1(doorid):
    index = 0
    digest = ''
    password = ''

    while len(password) < 8:
        while not digest.startswith('00000'):
            index += 1
            if index % 1000000 == 0:
                print('-->', index)
            digest = hashlib.md5('{:s}{:d}'.format(doorid, index).encode()).hexdigest()

        print('INDEX:', index, digest)
        password += digest[5]
        digest = ''

    return password

def part2(doorid):
    index = 0
    digest = ''
    password = [None]*8
    hexvals = '0123456789abcdef'

    while None in password:
        digest = ''
        while not digest.startswith('00000'):
            index += 1
            if index % 1000000 == 0:
                print('-->', index)
            digest = hashlib.md5('{:s}{:d}'.format(doorid, index).encode()).hexdigest()

        print('INDEX:', index, digest)

        position = hexvals.index(digest[5])
        print('POSITION:', position)
        if position >= len(password):
            continue

        value = digest[6]
        print('VALUE:', value)

        if password[position] is None:
            password[position] = value

    return ''.join(password)