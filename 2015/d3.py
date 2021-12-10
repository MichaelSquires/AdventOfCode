def part1(data):
    x = 0
    y = 0

    houses = {
        (x,y): 1
    }

    for direction in data:
        if direction == '^':
            y += 1
        elif direction == 'v':
            y -= 1
        elif direction == '>':
            x += 1
        elif direction == '<':
            x -= 1

        houses[(x,y)] = True

    return len(houses)

SANTA = 0
ROBOSANTA = 1

def part2(data):

    robo_x = 0
    robo_y = 0
    santa_x = 0
    santa_y = 0

    houses = {
        (0,0): True
    }

    who = 0
    for direction in data:
        if direction == '^':
            if who % 2 == SANTA:
                santa_y += 1
            else:
                robo_y += 1

        elif direction == 'v':
            if who % 2 == SANTA:
                santa_y -= 1
            else:
                robo_y -= 1

        elif direction == '>':
            if who % 2 == SANTA:
                santa_x += 1
            else:
                robo_x += 1

        elif direction == '<':
            if who % 2 == SANTA:
                santa_x -= 1
            else:
                robo_x -= 1

        if who % 2 == SANTA:
            houses[(santa_x, santa_y)] = True
        else:
            houses[(robo_x, robo_y)] = True

        who += 1

    return len(houses)