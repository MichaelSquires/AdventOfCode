import re
import logging

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

def parse(data):
    data = data.splitlines()
    return makeParticles(data)

def part1(particles):
    for i in range(100000):
        [k.tick() for k in particles]

    lo = particles[0]

    for particle in particles:
        if particle.distance < lo.distance:
            lo = particle

    return lo

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

    return len(particles)