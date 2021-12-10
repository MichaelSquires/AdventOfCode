import re
import logging

class Circle:
    def __init__(self):
        self._data = [0]
        self._current = 0

    def insert(self, value):
        new = (current + (CW * 1)) % len(self._data)
        self._data.insert(new, value)
        self._current = new

CW = 1
CCW = -1

def part1(data):
    players, points = data
    score = [0 for k in range(players)]

    circle = [0]

    player = 1
    current = 1
    for i in range(1, points+1):
        if len(circle) == 1:
            new = 2
        else:
            new = ((current + (CW * 1)) + 1) % len(circle)
        print('CIRCLE', circle, new)
        circle.insert(new, i)

        current = new

        player += 1
        player %= players
        if player == 0:
            player = 1

        if i == 15:
            break

    return max(score)

def part2(data):
    return data

def parse(data):
    data = re.findall('(\d+) players; last marble is worth (\d+) points', data)
    return [(int(k[0]), int(k[1])) for k in data]