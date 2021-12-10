import logging
import itertools

from pyparsing import *

NAMETOK = Word(alphas)
INTTOK = Word(nums).setParseAction(lambda s,l,t: [int(t[0])])

INPUT = Group(
    NAMETOK.setResultsName('name') +
    Literal('can fly').suppress() +
    INTTOK.setResultsName('speed') +
    Literal('km/s for').suppress() +
    INTTOK.setResultsName('flytime') +
    Literal('seconds, but then must rest for').suppress() +
    INTTOK.setResultsName('resttime') +
    Literal('seconds.').suppress()
)

INPUTS = OneOrMore(INPUT)

verbose = False

TIMELIMIT = 2503

class Reindeer:
    def __init__(self, name, speed, flytime, resttime):
        self.name = name
        self.speed = speed
        self.flytime = flytime
        self.resttime = resttime

        self.points = 0

    def __repr__(self):
        return '<Reindeer: {}, {:d} km/s, {:d} flying, {:d} resting, {:d} pts>'.format(
            self.name,
            self.speed,
            self.flytime,
            self.resttime,
            self.points
        )

    def getDistance(self, time):
        div, mod = divmod(time, self.flytime + self.resttime)
        distance = div * self.speed * self.flytime
        distance += min(mod, self.flytime) * self.speed

        return distance

def part1(reindeer):

    farthest = 0
    for r in reindeer:

        distance = r.getDistance(TIMELIMIT)
        if distance > farthest:
            farthest = distance
        
    return farthest

def part2(reindeer):
    # Iterate over each second in the race
    for i in range(1,TIMELIMIT+1):
        # Calculate the distance for each reindeer
        times = {k:k.getDistance(i) for k in reindeer}

        if verbose:
            pprint.pprint(times)

        # Figure out who's in the lead
        first = 0
        for k,v in times.items():
            if v > first:
                first = v

        # If a reindeer is in the lead (or tied), give a point
        for k,v in times.items():
            if v == first:
                k.points += 1

    # Get the highest number of points
    best = 0
    for k in reindeer:
        if k.points > best:
            best = k.points

    return best

def parse(data):
    data = INPUTS.parseString(data)

    reindeer = []
    for line in data:

        r = Reindeer(line.name, line.speed, line.flytime, line.resttime)
        reindeer.append(r)

    return reindeer