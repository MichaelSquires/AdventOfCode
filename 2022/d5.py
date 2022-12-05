import re
import collections

SAMPLE = '''\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''

PATTERN = re.compile(r'move (\d+) from (\d+) to (\d+)')

def parse(data: str):
    crates, instructions = data.split('\n\n')

    # Figure out how many stacks there are
    last = crates.splitlines()[-1]
    count = int((len(last) + 1) / 4)

    stacks = {}
    for ii in range(1, count+1):
        # Stacks are 1-indexed
        stacks[ii] = collections.deque()

    for line in crates.splitlines()[:-1]:
        for index in range(count):
            curr = line[1+(index*4)]
            if curr == ' ':
                continue

            stacks[index + 1].append(curr)

    for ii in range(1, count+1):
        stacks[ii].reverse()

    moves = []
    for line in instructions.splitlines():
        moves.append(tuple(map(int, PATTERN.match(line).groups())))

    return stacks, moves


def part1(data):
    stacks, moves = data

    for count, src, dst in moves:
        for _ in range(count):
            stacks[dst].append(stacks[src].pop())

    ret = []
    for ii in range(1, len(stacks)+1):
        ret.append(stacks[ii].pop())

    return ''.join(ret)


def part2(data):
    stacks, moves = data

    for count, src, dst in moves:
        lift = []
        for _ in range(count):
            lift.append(stacks[src].pop())
        lift.reverse()
        stacks[dst].extend(lift)

    ret = []
    for ii in range(1, len(stacks)+1):
        ret.append(stacks[ii].pop())

    return ''.join(ret)
