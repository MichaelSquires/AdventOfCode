import string
import logging
import itertools

sample = '''\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''

xsample = '''\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
'''

def parse(data):
    return [k.split('-') for k in data.splitlines()]

def part1(data):
    pass

def part2(data):
    pass