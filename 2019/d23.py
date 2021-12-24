import sys
import time
import logging
import functools
import collections

from . import intcode

parse = intcode.parse

class Packet:
    dst = None
    x = None
    y = None
    
    def __repr__(self):
        return f'<Packet dst {self.dst}, x {self.x}, y {self.y}>'
    
class Network:
    def __init__(self):
        self.wire = collections.defaultdict(list)
        self.machines = {}
        
    def recv(self, machid):
        queue = self.wire.get(machid)
        if not queue:
            time.sleep(0.1)
            return -1

        packet = queue.pop(0)

        mach = self.machines.get(machid)
        mach.infunc = functools.partial(self.recv2, machid, packet)

        return packet.x
    
    def recv2(self, machid, packet):
        mach = self.machines.get(machid)
        mach.infunc = functools.partial(self.recv, machid)
        logging.debug('RECV: %s', packet)
        return packet.y

    def send(self, machid, val):
        packet = Packet()
        packet.dst = val
        mach = self.machines.get(machid)
        mach.outfunc = functools.partial(self.send2, machid, packet)
        
    def send2(self, machid, packet, val):
        packet.x = val
        
        mach = self.machines.get(machid)
        mach.outfunc = functools.partial(self.send3, machid, packet)
        
    def send3(self, machid, packet, val):
        packet.y = val
        self.wire[packet.dst].append(packet)

        mach = self.machines.get(machid)
        mach.outfunc = functools.partial(self.send, machid)
        
        logging.debug('SEND: %s', packet)

def newmach(prog, network, machid):
    mach = intcode.ThreadedComputer()
    mach.load(prog)
    
#    def bootstrap(network, mach, machid):
#        mach.infunc = functools.partial(network.recv, mach, machid)
#        return machid

    def bootstrap():
        mach.infunc = functools.partial(network.recv, machid)
        return machid

    mach.infunc = bootstrap
    mach.outfunc = functools.partial(network.send, machid)
    
    return mach

def part1(data):
    network = Network()

    for ii in range(50):
        network.machines[ii] = newmach(data, network, ii)
        
    [k.start() for k in network.machines.values()]
    
    while not network.wire.get(255):
        time.sleep(0.1)
        
    [k.stop() for k in network.machines.values()]
    [k.join() for k in network.machines.values()]
        
    packet = network.wire.get(255).pop(0)
    return packet.y

class Nat:
    packet = None
    last = None

def part2(data):
    nat = Nat()
    network = Network()

    for ii in range(50):
        network.machines[ii] = newmach(data, network, ii)
        
    [k.start() for k in network.machines.values()]
    
    while True:
        if (last := network.wire.get(255)):
            nat.packet = last.pop(0)
            
        if any(network.wire.values()):
            #time.sleep(0.1)
            continue
        
        # The any(...) check is racy. Sleep and check again to reduce chance of race
        time.sleep(0.05)

        if any(network.wire.values()):
            #time.sleep(0.1)
            continue

        if not nat.packet:
            time.sleep(0.1)
            continue
            
        packet = Packet()

        packet.dst = 0
        packet.x = nat.packet.x
        packet.y = nat.packet.y
        
        if nat.last == nat.packet.y:
            break
        
        nat.last = nat.packet.y

        network.wire[0].append(packet)
        
    [k.stop() for k in network.machines.values()]
    [k.join() for k in network.machines.values()]
        
    return nat.last