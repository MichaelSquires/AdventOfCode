#!/usr/bin/env python

import sys
import copy
import pprint
import argparse
import itertools
import traceback

verbose = False

START = 'CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl'
#START = 'HOH'

def part1(data):
    molecules = []

    for key,values in data.iteritems():
        index = START.find(key)
        while -1 != index:
            for value in values:
                molecule = START[:index] + value + START[index+len(key):]
                if molecule not in molecules:
                    molecules.append(molecule)

            index = START.find(key, index+1)

    return len(molecules)

def part2(data):
    return 0

def main(args):

    replacements = {}
    data = [k.strip().split(' ') for k in args.file.readlines()]

    # Split from '<input> => <output>' and make dictionary
    for key, _, value in data:
        if not replacements.has_key(key):
            replacements[key] = []

        replacements[key].append(value)

    if verbose:
        pprint.pprint(replacements)

    print 'Part1: {:d}'.format(part1(replacements))
    print 'Part2: {:d}'.format(part2(replacements))

    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    # Optional arguments
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
