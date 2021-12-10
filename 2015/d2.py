def part1(data):
    paper = 0

    data = [k.split('x') for k in data]

    for l, w, h in data:
        l = int(l)
        w = int(w)
        h = int(h)
        small = min(l*w, w*h, h*l)
        paper += 2*l*w + 2*w*h + 2*h*l + small

    return paper

def part2(data):
    ribbon = 0

    data = [k.split('x') for k in data]

    for l, w, h in data:
        l = int(l)
        w = int(w)
        h = int(h)
        large = max(l, w, h)
        ribbon += (2*l + 2*w + 2*h - 2*large) + (l * w * h)

    return ribbon

def parse(data):
    return data.splitlines()