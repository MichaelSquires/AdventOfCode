import copy
import logging
import itertools

START = 'CRnSiRnCaPTiMgYCaPTiRnFArSiThFArCaSiThSiThPBCaCaSiRnSiRnTiTiMgArPBCaPMgYPTiRnFArFArCaSiRnBPMgArPRnCaPTiRnFArCaSiThCaCaFArPBCaCaPTiTiRnFArCaSiRnSiAlYSiThRnFArArCaSiRnBFArCaCaSiRnSiThCaCaCaFYCaPTiBCaSiThCaSiThPMgArSiRnCaPBFYCaCaFArCaCaCaCaSiThCaSiRnPRnFArPBSiThPRnFArSiRnMgArCaFYFArCaSiRnSiAlArTiTiTiTiTiTiTiRnPMgArPTiTiTiBSiRnSiAlArTiTiRnPMgArCaFYBPBPTiRnSiRnMgArSiThCaFArCaSiThFArPRnFArCaSiRnTiBSiThSiRnSiAlYCaFArPRnFArSiThCaFArCaCaSiThCaCaCaSiRnPRnCaFArFYPMgArCaPBCaPBSiRnFYPBCaFArCaSiAl'
#START = 'HOH'

def part1(data):
    molecules = []

    for key,values in data.items():
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

def parse(data):
    replacements = {}
    data = [k.split(' ') for k in data.splitlines()[:-2]]

    # Split from '<input> => <output>' and make dictionary
    for key, _, value in data:
        if key not in replacements:
            replacements[key] = []

        replacements[key].append(value)

    logging.debug(replacements)

    return replacements