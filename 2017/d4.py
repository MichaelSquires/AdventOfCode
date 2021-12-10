import logging
import itertools

def parse(data):
    passwords = []
    for password in data.splitlines():
        password = password.strip()

        words = password.split()

        passwords.append(words)

    return passwords

def part1(passwords):
    valid = []
    for password in passwords:

        wordset = set(password)

        if len(wordset) == len(password):
            valid.append(password)

        logging.debug('Invalid password: %s', password)

    return len(valid)

def part2(passwords):
    valid = 0
    for password in passwords:

        anagrams = []
        for word in password:
            # Get all permutations
            p = list(itertools.permutations(word))

            # Reduce to unique permutations
            p = list(set(p))

            # Extend list
            anagrams.extend(p)

        wordset = set(anagrams)

        if len(wordset) == len(anagrams):
            valid += 1
            continue

        logging.debug('Invalid password: %s', password)

    return valid