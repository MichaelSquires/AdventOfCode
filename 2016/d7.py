import re
import string
import hashlib
import logging
import itertools

regex = re.compile(r'\w+|\[\w+\]')

class Address:
    def __init__(self, address):
        self.address = address
        self.hypernets = []
        self.supernets = []

        for match in regex.findall(self.address):
            if match.startswith('['):
                self.hypernets.append(match)
            else:
                self.supernets.append(match)

    def __repr__(self):
        return '<Address: %s>' % (self.address)

    def hasAbba(self):
        abba = []
        perms = itertools.permutations(string.ascii_lowercase, 2)
        for perm in perms:
            val = ''.join((perm[0], perm[1], perm[1], perm[0]))
            abba.append(val)

        hasAbba = False
        supernets = ' '.join(self.supernets)
        for val in abba:
            if val in supernets:
                hasAbba = True
                break

        if hasAbba:
            hypernets = ' '.join(self.hypernets)
            for val in abba:
                if val in hypernets:
                    hasAbba = False
                    break

        return hasAbba

def parse(data):
    addresses = []
    for line in data.splitlines():
        addresses.append(
            Address(line.strip())
        )

    return addresses

def part1(addresses):
    hastls = 0

    for address in addresses:
        if address.hasAbba():
            hastls += 1

    return hastls

def part2(addresses):
    return addresses