import logging

def parse(data):
    firewall = {}
    for line in data.splitlines():

        depth, range_ = line.split(': ')
        depth = int(depth)
        range_ = int(range_)

        firewall[depth] = range_

    return firewall

def scanner(depth, range_, delay=0):
    return (depth + delay) % (2 * range_ - 2)

def part1(firewall):
    caught = []

    for depth in range(max(firewall)+1):
        range_ = firewall.get(depth)
        if range_ is None:
            continue

        scan = scanner(depth, range_)
        logging.debug('SCAN: %d', scan)
        if scan == 0:
            caught.append(depth)

    severity = 0
    for depth in caught:
        severity += depth * firewall[depth]

    return severity

def part2(firewall):
    for delay in range(2**32):
        passed = True
        for depth in range(max(firewall)+1):
            range_ = firewall.get(depth)
            if range_ is None:
                continue

            if scanner(depth, range_, delay) == 0:
                passed = False
                break

        if passed:
            break

    return delay