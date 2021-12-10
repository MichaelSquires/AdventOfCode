def part1(data):
    return len(data.replace(')', '')) - len(data.replace('(', ''))

def part2(data):
    floor = 0
    position = 0

    for position in range(len(data)):
        if data[position] == '(':
            floor += 1
        else:
            floor -= 1

        if floor == -1:
            return position + 1

        position += 1

    raise Exception('Does not enter basement')