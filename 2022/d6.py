import logging

SAMPLE = [
    'mjqjpqmgbljsphdztnvjfqwrcgsmlb',
    'bvwbjplbgvbhsrlpgdmjqwftvncz',
    'nppdvjthqldpwncqszvftbrmjlhg',
    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
    'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw',
]

def find_marker(data, size):
    index = None

    for ii in range(len(data) - 3):
        curr = set(data[ii:ii+size])
        logging.debug('CURR: %s', curr)
        if len(curr) == size:
            index = ii + size
            break

    return index

def part1(data):
    return find_marker(data, 4)

def part2(data):
    return find_marker(data, 14)