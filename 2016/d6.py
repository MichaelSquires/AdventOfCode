import hashlib
import logging
import itertools

def parse(data):
    return data.splitlines()

def decode(messages, reverse=True):
    message = []

    for i in range(len(messages[0])):
        d = {}
        letters = [k[i] for k in messages]

        for letter in letters:
            if letter not in d:
                d[letter] = 0
            d[letter] += 1

        def keyfunc(x):
            return x[1]

        letters = sorted(d.items(), key=keyfunc, reverse=reverse)
        groups = []
        for k, g in itertools.groupby(letters, key=keyfunc):
            groups.append(sorted(g))

        letter = list(itertools.chain.from_iterable(groups))[0]

        message += letter[0]

    return ''.join(message)

def part1(messages):

    message = decode(messages)
    return message

def part2(messages):
    message = decode(messages, False)
    return message