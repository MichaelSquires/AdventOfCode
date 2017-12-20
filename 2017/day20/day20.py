#!/usr/bin/env python

import re
import sys
import logging
import argparse

X = 0
Y = 1
Z = 2

# p=<-13053,-6894,1942>, v=<14,39,-11>, a=<16,7,-2>
regex = re.compile('^p=<([\d-]+),([\d-]+),([\d-]+)>, v=<([\d-]+),([\d-]+),([\d-]+)>, a=<([\d-]+),([\d-]+),([\d-]+)>$')

class Particle:
    def __init__(self, idx, position, velocity, acceleration):
        self.idx = idx

        self.x = position[X]
        self.y = position[Y]
        self.z = position[Z]

        self.vx = velocity[X]
        self.vy = velocity[Y]
        self.vz = velocity[Z]

        self.ax = acceleration[X]
        self.ay = acceleration[Y]
        self.az = acceleration[Z]

    def __repr__(self):
        return '<Particle: %d>' % (self.idx)

    @property
    def position(self):
        return (self.x, self.y, self.z)

    @property
    def distance(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def tick(self):
        self.vx += self.ax
        self.vy += self.ay
        self.vz += self.az

        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

def makeParticles(data):
    idx = 0
    particles = []
    for line in data:
        match = regex.match(line)
        if match is None:
            logging.error('Invalid input: %s', line)
            raise Exception('Invalid input')

        p = [int(k) for k in match.groups()[0:3]]
        v = [int(k) for k in match.groups()[3:6]]
        a = [int(k) for k in match.groups()[6:9]]

        particles.append(Particle(idx, p, v, a))

        idx += 1
    return particles

def main(args):

    data = [k.strip() for k in args.file.readlines()]
    particles1 = makeParticles(data)
    particles2 = makeParticles(data)

    if args.part in (None, 1):
        part1(particles1)

    if args.part in (None, 2):
        part2(particles2)

    return 0

def part1(particles):
    for i in range(100000):
        [k.tick() for k in particles]

    lo = particles[0]

    for particle in particles:
        if particle.distance < lo.distance:
            lo = particle

    print('Part 1:', lo)

def part2(particles):
    particles = set(particles)

    for i in range(10000):
        [k.tick() for k in particles]

        positions = {}
        for particle in particles:
            if particle.position not in positions:
                positions[particle.position] = set()

            positions[particle.position].add(particle)

        for key,val in positions.items():
            if len(val) > 1:
                particles = particles - val

    print('Part 2:', len(particles))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    parser.add_argument('-p', '--part', help='Specify which part to run', type=int, choices=[1,2])
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='count', default=0)

    # Positional arguments
    parser.add_argument('file', help='Input file', type=open)

    args = parser.parse_args()
    if args.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif args.verbose == 2:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        sys.exit(main(args))
    except Exception as exc:
        logging.exception('ERROR in main: %s', exc)
        sys.exit(-1)
