#!/usr/bin/env python

import sys
import string
import argparse
import traceback

verbose = False

VOWELS = ['a', 'e', 'i', 'o', 'u']
BADSEQS = ['ab', 'cd', 'pq', 'xy']
DOUBLES = [k*2 for k in string.ascii_lowercase]

def check_vowels(data):
    # returns:
    #   True: >= 3 vowels
    #   False: < 3 vowels
    vowels = [k for k in data if k in VOWELS]
    if len(vowels) >= 3:
        return True

    return False

def check_badseqs(data):
    # returns:
    #   True: Bad sequences found
    #   False: No bad sequences found
    badseqs = [k for k in BADSEQS if k in data]
    if len(badseqs):
        return True

    return False

def check_doubles(data):
    # returns:
    #   True: Contains double letters
    #   False: Does no contain double letters
    doubles = [k for k in DOUBLES if k in data]
    if doubles:
        return True

    return False

def part1(data):
    nice = 0
    for line in data:
        vowels = check_vowels(line)
        badseqs = check_badseqs(line)
        doubles = check_doubles(line)
        if verbose:
            print '{}: v {}, b {}, d {}'.format(line, vowels, badseqs, doubles)

        if vowels and doubles and not badseqs:
            nice += 1

    return nice

def get_xgrams(data, length):
    ret = []
    count = 0

    while count < len(data) - (length - 1):
        ret.append(data[count:count+length])
        count += 1

    return ret

def check_digrams(data):
    digrams = get_xgrams(data, 2)

    for d in digrams:
        if len(data) - len(data.replace(d, '')) > 2:
            return True

    return False

def check_trigrams(data):
    # returns:
    #   True: Contains at least one trigram where the first and last letter are the same
    #   False: Does not contain at least one trigram where the first and last letter are the same
    trigrams = get_xgrams(data, 3)

    for trigram in trigrams:
        if trigram[0] == trigram[2]:
            if verbose: print 'Tri: {}'.format(trigram)
            return True

    return False


def part2(data):

    nice = 0
    for line in data:
        digrams = check_digrams(line)
        trigrams = check_trigrams(line)

        if verbose:
            print '{}: d {}, t {}'.format(line, digrams, trigrams)

        if digrams and trigrams:
            nice += 1

    return nice

    return 0

def main(args):
    
    data = args.file.readlines()

    # Strip newlines
    data = [k.strip() for k in data]

    print 'Part 1: {:d}'.format(part1(data))
    print 'Part 2: {:d}'.format(part2(data))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
    #parser.add_argument('-i', '--interact', help='Interact', action='store_true')
    parser.add_argument('-v', '--verbose', help='Show verbose messages', action='store_true')

    # Positional arguments
    parser.add_argument('file', help='Input file', type=file)

    args = parser.parse_args()
    verbose = args.verbose

    try:
        sys.exit(main(args))
    except Exception as exc:
        print 'ERROR: %s' % (exc)
        if verbose:
            traceback.print_exc()
        sys.exit(-1)
