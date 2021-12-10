import logging

A_START = 289
B_START = 629

# SAMPLE DATA
# A_START = 65
# B_START = 8921

A_FACTOR = 16807
B_FACTOR = 48271

A_MULTIPLE = 4
B_MULTIPLE = 8

MODULO = 0x7fffffff

PART1_ITERATIONS = 40000000
PART2_ITERATIONS = 5000000

class Generator:
    def __init__(self, start, factor, multiple=1):
        self._start = start
        self._factor = factor
        self._multiple = multiple
        self._generator = self.__generator()

    def __generator(self):
        prev = self._start
        while True:
            prev = (prev * self._factor) % MODULO
            if prev % self._multiple != 0:
                continue

            yield prev

    def __next__(self):
        return next(self._generator)

def part1(data):
    genA = Generator(A_START, A_FACTOR)
    genB = Generator(B_START, B_FACTOR)
    match = 0
    for i in range(PART1_ITERATIONS):
        a = next(genA)
        b = next(genB)

        logging.debug('A: %d, B: %d', a, b)

        if (a & 0xffff) == (b & 0xffff):
            match += 1

    return match

def part2(data):
    genA = Generator(A_START, A_FACTOR, A_MULTIPLE)
    genB = Generator(B_START, B_FACTOR, B_MULTIPLE)
    match = 0
    for i in range(PART2_ITERATIONS):
        a = next(genA)
        b = next(genB)

        logging.debug('A: %d, B: %d', a, b)

        if (a & 0xffff) == (b & 0xffff):
            match += 1

    return match