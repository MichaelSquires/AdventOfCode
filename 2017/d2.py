import io
import csv
import logging
import itertools

def parse(data):
    ret = []
    data = io.StringIO(data)
    for line in csv.reader(data, delimiter='\t'):
        ret.append([int(k) for k in line])

    return ret

def part1(data):
    checksum = 0
    for row in data:
        lo = min(row)
        hi = max(row)
        diff = hi - lo
        logging.debug('hi %d, lo %d, diff %d, csum %d', hi, lo, diff, checksum)
        checksum += diff

    return checksum

def part2(data):
    checksum = 0
    def div(a):
        return a[0]/a[1]

    for row in data:
        logging.debug('row %r', row)
        combinations = itertools.permutations(row, 2)
        results = map(div, combinations)
        result = None
        for r in results:
            logging.debug('r %r', r)
            if r.is_integer():
                result = r
                break

        if result is None:
            raise Exception('Result not found for row: %r' % (row))

        checksum += result

    return checksum