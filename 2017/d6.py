import copy
import logging
import itertools

def parse(data):
    return list(map(int, data.splitlines()[0].split()))

def part1(buckets):
    count = 0
    seen = []
    blen = len(buckets)
    while buckets not in seen:
        count += 1
        seen.append(copy.copy(buckets))

        logging.debug('buckets: %r', buckets)

        hi = max(buckets)
        idx = buckets.index(hi)
        logging.debug('hi %d, idx %d', hi, idx)

        buckets[idx] = 0
        for i in range(hi):
            buckets[(idx + 1 + i) % blen] += 1

        logging.debug('buckets: %r', buckets)

    return count

def part2(buckets):
    count = 0
    seen = []
    blen = len(buckets)
    start = copy.copy(buckets)
    while start not in seen:

        logging.debug('buckets: %r', buckets)

        hi = max(buckets)
        idx = buckets.index(hi)
        logging.debug('hi %d, idx %d', hi, idx)

        buckets[idx] = 0
        for i in range(hi):
            buckets[(idx + 1 + i) % blen] += 1

        logging.debug('buckets: %r', buckets)

        count += 1
        seen.append(copy.copy(buckets))

    return count