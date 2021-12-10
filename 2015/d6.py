import string
import logging

TOGGLE  = 0
TURNON  = 1
TURNOFF = 2

def parse(data):
    # returns:
    #   List of commands as tuples
    #   Sample tuple:
    #       (TOGGLE, x1, y1, x2, y2)
    ret = []

    data = data.splitlines()

    # Get rid of the word "turn"
    data = [k.replace('turn ', '') for k in data]

    for line in data:
        cmd, start, _junk, end = line.split(' ')

        cmd = {
            'off': TURNOFF,
            'on': TURNON,
            'toggle': TOGGLE
        }.get(cmd)

        x1,y1 = start.split(',')
        x1 = int(x1)
        y1 = int(y1)

        x2,y2 = end.split(',')
        x2 = int(x2)
        y2 = int(y2)

        ret.append((cmd, x1, y1, x2, y2))

    return ret

def part1(data):
    # Create lights 2d array (1000 x 1000)
    lights = []
    for i in range(1000):
        lights.append([0]*1000)

    for cmd, x1, y1, x2, y2 in data:
        logging.debug('Cmd: {}, x1: {:d}, y1: {:d}, x2: {:d}, y2: {:d}'.format(cmd, x1, y1, x2, y2))

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                if cmd == TOGGLE:
                    lights[x][y] = lights[x][y] ^ 1

                elif cmd == TURNON:
                    lights[x][y] = 1

                elif cmd == TURNOFF:
                    lights[x][y] = 0

    ret = 0
    for x in range(1000):
        for y in range(1000):
            if lights[x][y] == 1:
                ret += 1
            
    return ret

def part2(data):
    # Create lights 2d array (1000 x 1000)
    lights = []
    for i in range(1000):
        lights.append([0]*1000)

    for cmd, x1, y1, x2, y2 in data:
        logging.debug('Cmd: {}, x1: {:d}, y1: {:d}, x2: {:d}, y2: {:d}'.format(cmd, x1, y1, x2, y2))

        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                if cmd == TOGGLE:
                    lights[x][y] += 2

                elif cmd == TURNON:
                    lights[x][y] += 1

                elif cmd == TURNOFF:
                    lights[x][y] = max(0, lights[x][y] - 1)

    ret = 0
    for x in range(1000):
        for y in range(1000):
            ret += lights[x][y]
            
    return ret