import re
import string
import logging
import itertools

class Room:
    def __init__(self, room, sector, checksum):
        self.room = room
        self.sector = sector
        self.checksum = checksum

    def __repr__(self):
        return '<Room %s [%s] %d>' % (self.room, self.checksum, self.sector)

    def computeChecksum(self):
        d = {}

        letters = self.room.replace('-', '')
        for letter in letters:
            if letter not in d:
                d[letter] = 0
            d[letter] += 1

        def keyfunc(x):
            return x[1]

        letters = sorted(d.items(), key=keyfunc, reverse=True)
        groups = []
        for k, g in itertools.groupby(letters, key=keyfunc):
            groups.append(sorted(g))

        checksum = ''
        for val in itertools.chain.from_iterable(groups):
            checksum += val[0]

            if len(checksum) == 5:
                break

        return checksum

    def _shift(self, letter):
        amount = self.sector % 26
        table = string.ascii_lowercase + string.ascii_lowercase

        return table[table.index(letter) + amount]

    def decrypt(self):
        plaintext = ''

        for letter in self.room:
            if letter == '-':
                plaintext += ' '
                continue

            plaintext += self._shift(letter)

        return plaintext

regex = re.compile(r'^([a-z-]+)-(\d+)\[([a-z]+)\]$')

def parse(data):
    rooms = []
    for line in data.splitlines():
        m = regex.match(line)

        rooms.append(
            Room(
                m.group(1),
                int(m.group(2)),
                m.group(3)
            )
        )

    return rooms

def part1(rooms):
    total = 0

    for room in rooms:
        if room.checksum == room.computeChecksum():
            total += room.sector

    return total

def part2(rooms):

    sector = 0
    for room in rooms:
        name = room.decrypt()
        if 'north' in name:
            sector = room.sector
            break

    return sector