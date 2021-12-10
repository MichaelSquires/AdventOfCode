import re
import logging
import itertools

class Stream:
    def __init__(self, data):
        self._data = data

        self.score = 0

        self._group = 0
        self._garbage = False
        self._escaped = False

        self.gscore = 0

    def run(self):
        for char in self._data:
            logging.debug('CHAR: %s', char)
            # Open group
            if char == '{' and not self._garbage:
                self._group += 1
                logging.debug('GROUP: %d', self._group)

            # Close group
            elif char == '}' and not self._garbage:
                self.score += self._group
                self._group -= 1
                logging.debug('SCORE: %d', self.score)
                logging.debug('GROUP: %d', self._group)

            # Escape character
            elif char == '!':
                self._escaped = not self._escaped
                logging.debug('ESCAPE: %s', self._escaped)

            # Open garbage
            elif char == '<' and not self._garbage:
                self._garbage = True
                logging.debug('GARBAGE: %s', self._garbage)

            # Close garbage
            elif char == '>' and not self._escaped:
                self._garbage = False
                logging.debug('GARBAGE: %s', self._garbage)

            # Only escape one character
            elif self._escaped:
                self._escaped = False
                logging.debug('ESCAPE: %s', self._escaped)

            # All others
            else:
                if self._garbage:
                    self.gscore += 1

def parse(data):
    stream = Stream(data)
    stream.run()

    return stream

def part1(stream):
    return stream.score

def part2(stream):
    return stream.gscore