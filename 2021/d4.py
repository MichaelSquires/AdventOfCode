import logging

class BingoCard:
    def __init__(self, grid):
        # Initial data a 5x5 array of numbers
        self._grid = grid

        # Called numbers
        self._seen = []

        # Winning sequences on this card
        self._winning_sequences = []

        # Each row is a winning sequence
        for row in self._grid:
            self._winning_sequences.append(row)

        # Each column is a winning sequence
        for col in range(5):
            self._winning_sequences.append([k[col] for k in self._grid])

    @property
    def score(self):
        allnums = []
        for line in self._grid:
            allnums.extend(line)

        unmarked = set(allnums) - set(self._seen)
        return sum(unmarked) * self._seen[-1]

    def check(self):
        for seq in self._winning_sequences:
            seq = set(seq)
            if seq & set(self._seen) == seq:
                return self

        return None

    def mark(self, number):
        self._seen.append(number)

    def unmarked(self):
        nums = []
        for line in self._grid:
            nums.extend(line)

        return set(nums) - set(self._seen)

    def __repr__(self):
        return str(self._grid)


class Data:
    numbers = []
    boards = []


def parse(data):
    ret = Data()

    lines = data.splitlines()
    ret.numbers = [int(k) for k in lines[0].split(',')]

    grid = []
    ii = 1
    while ii < len(lines):
        grid = lines[ii+1:ii+6]
        grid = [[int(num) for num in line.split()] for line in grid]
        ret.boards.append(BingoCard(grid))
        ii += 6

    return ret

def part1(data):
    winner = None
    for num in data.numbers:
        for board in data.boards:
            board.mark(num)
            if board.check():
                winner = board
                break

        if winner:
            break

    return winner.score

def part2(data):
    winners = []
    for num in data.numbers:
        for board in data.boards:
            board.mark(num)
            if board.check() and board not in winners:
                winners.append(board)

        if set(winners) == set(data.boards):
            break

    import code
    code.interact(local=locals())
    return winners[-1].score