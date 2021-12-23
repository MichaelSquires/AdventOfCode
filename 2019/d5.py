import logging
import functools

from . import intcode

#SAMPLE = '1101,100,-1,4,0'
#SAMPLE = '1002,4,3,4,33'
#SAMPLE = '3,0,4,0,99'

parse = intcode.parse

class OutData:
    val = None

def stop(out, val):
    out.val = val

def part1(data):
    mach = intcode.Computer()
    mach.load(data)

    out = OutData()

    mach.infunc = lambda: 1
    mach.outfunc = functools.partial(stop, out)

    mach.run()

    return out.val

def part2(data):
    mach = intcode.Computer()
    mach.load(data)

    out = OutData()

    mach.infunc = lambda: 5
    mach.outfunc = functools.partial(stop, out)

    mach.run()

    return out.val
