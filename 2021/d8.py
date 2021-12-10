import pprint
import logging
import collections

Entry = collections.namedtuple('Entry', ['signal', 'output'])

def parse(data):
    ret = []
    for line in data.splitlines():
        ins, outs = line.split('|')

        signal = list(map(set, ins.split()))
        output = outs.split()

        ret.append(Entry(signal, output))

    return ret

def part1(data):
    total = 0

    for entry in data:
        for digit in entry.output:
            match len(digit):
                case 2 | 3 | 4 | 7:
                    logging.debug('DIGIT: %s', digit)
                    total += 1

    return total


class Digits:
    DISPLAY = {
        'abcefg'    : 0,
        'cf'        : 1,
        'acdeg'     : 2,
        'acdfg'     : 3,
        'bcdf'      : 4,
        'abdfg'     : 5,
        'abdefg'    : 6,
        'acf'       : 7,
        'abcdefg'   : 8,
        'abcdfg'    : 9,
    }

    def __init__(self, scrambled_digits):
        self._data = scrambled_digits

        self.map = {}
        self._make_map()

    def _make_map(self):
        a235 = []
        a069 = []

        # Sort into buckets based on length
        for digit in self._data:
            match len(digit):
                case 2:
                    a1 = digit

                case 3:
                    a7 = digit

                case 4:
                    a4 = digit

                case 5:
                    a235.append(digit)

                case 6:
                    a069.append(digit)

                case 7:
                    a8 = digit

        # We know a235 and a069 include each of these digits
        # but we don't know which. It doesn't matter really.
        a2, a3, a5 = a235
        a0, a6, a9 = a069

        # Find each of the letters by looking for the differences in each of the digits
        a = a7 - a1
        b = (a4 - a7) & (a0 & a6 & a9)
        c = (a4 & a7) - (a0 & a6 & a9)
        d = (a4 - a7) & (a2 & a3 & a5)
        e = (a2 | a3 | a5) - a7 - a4 - (a2 & a3 & a5)
        f = (a4 & a7) & (a0 & a6 & a9)
        g = a8 - a - b - c - d - e - f

        logging.debug('%s -> A', a)
        logging.debug('%s -> B', b)
        logging.debug('%s -> C', c)
        logging.debug('%s -> D', d)
        logging.debug('%s -> E', e)
        logging.debug('%s -> F', f)
        logging.debug('%s -> G', g)

        # Map the scrambled letter back to the actual letter
        self.map = {
            a.pop(): 'a',
            b.pop(): 'b',
            c.pop(): 'c',
            d.pop(): 'd',
            e.pop(): 'e',
            f.pop(): 'f',
            g.pop(): 'g',
        }

    def to_num(self, entry, scrambled=True):
        if scrambled:
            entry = self.descramble(entry)

        return Digits.DISPLAY.get(entry)

    def descramble(self, entry):
        ret = []

        for k in entry:
            ret.append(self.map.get(k))

        ret.sort()

        logging.debug('DESCRAMBLE: %s -> %s', entry, ''.join(ret))
        return ''.join(ret)


def part2(data):
    total = 0

    for entry in data:
        digits = Digits(entry.signal)
        d = ''
        for num in entry.output:
            d += str(digits.to_num(num))

        total += int(d)

    return total