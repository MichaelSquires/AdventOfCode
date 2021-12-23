from . import intcode

#SAMPLE = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
#SAMPLE = '1102,34915192,34915192,7,4,7,99,0'
#SAMPLE = '104,1125899906842624,99'

parse = intcode.parse

def part1(data):
    mach = intcode.Computer()
    mach.load(data)

    mach.infunc = lambda: 1

    mach.run()

    return mach.last_out

def part2(data):
    mach = intcode.Computer()
    mach.load(data)

    mach.infunc = lambda: 2

    mach.run()
    
    return mach.last_out