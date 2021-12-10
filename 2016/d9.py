import re
import copy
import logging
import collections

regex = re.compile(r'([A-Z]*)\((\d+)x(\d+)\)')

def parse(data):
    return data.strip()

def decompress(data):
    ret = ''
    while data:
        #logging.debug('RET: %d', len(ret))
        match = regex.match(data)
        if match is None:
            ret += data
            break
            #raise Exception('Invalid marker: %r' % (data))

        end = match.end()
        chars = int(match.group(2))
        times = int(match.group(3))

        ret += data[end:end + chars] * times

        data = data[end+chars:]

    return ret

def part1(data):
    data = decompress(data)
    return len(data)

def part2(data):
#    decomp=decompress
#    rgx=regex
#    import code
#    code.interact(local=locals())
    match = True
    while True:
        data = decompress(data)
        logging.debug('DATA: %d', len(data))
        if '(' not in data:
            break

    return len(data)