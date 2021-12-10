import logging
import collections


def parse(data):
    return data.splitlines()

def points(char):
    logging.debug('PT: %s', char)
    return {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }.get(char)

def part1(data):
    queue = collections.deque()

    score = 0
    for line in data:
        logging.info('LINE: %s', line)
        for char in line:
            logging.debug('CHAR: %s', char)
            match char:
                case '(' | '[' | '{' | '<':
                    queue.append(char)
                case ')':
                    old = queue.pop()
                    if old != '(':
                        score += points(char)
                        break

                case ']':
                    old = queue.pop()
                    if old != '[':
                        score += points(char)
                        break

                case '}':
                    old = queue.pop()
                    if old != '{':
                        score += points(char)
                        break

                case '>':
                    old = queue.pop()
                    if old != '<':
                        score += points(char)
                        break

    return score


def part2(data):

    incomplete = []

    for line in data:
        queue = collections.deque()
        corrupt = False
        for char in line:
            logging.debug('CHAR: %s', char)
            match char:
                case '(' | '[' | '{' | '<':
                    queue.append(char)
                case ')':
                    old = queue.pop()
                    if old != '(':
                        corrupt = True
                        break

                case ']':
                    old = queue.pop()
                    if old != '[':
                        corrupt = True
                        break

                case '}':
                    old = queue.pop()
                    if old != '{':
                        corrupt = True
                        break

                case '>':
                    old = queue.pop()
                    if old != '<':
                        corrupt = True
                        break

        if not corrupt:
            incomplete.append(line)

    scores = []
    logging.info('INCOMPLETE: %s', incomplete)

    for line in incomplete:
        score = 0
        queue = collections.deque()
        for char in line:
            match char:
                case '(' | '[' | '{' | '<':
                    queue.append(char)
                case ')' | ']' | '}' | '>':
                    queue.pop()

        while len(queue):
            old = queue.pop()
            score *= 5
            match old:
                case '(':
                    score += 1
                case '[':
                    score += 2
                case '{':
                    score += 3
                case '<':
                    score += 4

        scores.append(score)

    scores.sort()
    return scores[int(len(scores)/2)]