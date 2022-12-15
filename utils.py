import os
import re
import ast
import copy
import logging
import pathlib
import textwrap
import functools
import itertools

import bs4
import requests

__all__ = [
    'challenge',
    'download',
    'template',
    'exectime',

    'Grid',
    'up', 'down', 'left', 'right'
]

def open_aoc(url):
    # Try to get the session ID from the environment first. If that fails, try
    # session.txt on the filesystem
    session_id = os.environ.get('AOC_SESSION')
    if session_id is None:
        session = pathlib.Path('session.txt')
        if not session.exists():
            raise FileNotFoundError('session.txt')

        session_id = session.read_text().strip()

    cookies = dict(session=session_id)

    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'github.com/MichaelSquires/AdventOfCode'})

    req = requests.get(url, cookies=cookies, headers=headers, timeout=10)
    if not req.ok:
        raise Exception(f'Error downloading AoC data: {req.reason}')

    return req

def challenge(year, day):
    req = open_aoc(f'https://adventofcode.com/{year}/day/{day}')
    soup = bs4.BeautifulSoup(req.text, 'html.parser')

    text = ''
    text += '\'\'\'\n'

    for article in soup.findAll('article'):
        for tag in article:
            match tag.name:
                case 'h2':
                    text += f'## {tag.text}\n\n'

                case 'p':
                    text += '\n'.join(textwrap.wrap(tag.text, width=80))
                    text += '\n\n'

                case 'pre':
                    text += '```\n'
                    text += tag.text
                    if not tag.text.endswith('\n'):
                        text += '\n'
                    text += '```\n\n'

                case 'ul':
                    for item in tag:
                        if item.name != 'li':
                            continue

                        text += '\n'.join(
                            textwrap.wrap(
                                item.text,
                                width=80,
                                initial_indent='  - ',
                                subsequent_indent='    '
                            )
                        )
                        text += '\n\n'

    text += '\'\'\'\n'

    outfile = pathlib.Path(f'{year}/d{day}.py')
    text += outfile.read_text()
    outfile.write_text(text)

def template(outfile):
    outdata = '''\
    SAMPLE = 'SAMPLE INPUTS GO HERE AS STRING'

    def parse(data: str):
        return data

    def part1(data):
        pass

    def part2(data):
        pass
    '''

    outfile.write_text(textwrap.dedent(outdata))

def download(year, day):
    outfile = pathlib.Path(f'inputs/{year}/d{day}.txt')
    if outfile.exists():
        return

    # Create inputs path if it doesn't exist
    pathlib.Path(f'inputs/{year}').mkdir(parents=True, exist_ok=True)

    url = f'https://adventofcode.com/{year}/day/{day}/input'
    req = open_aoc(url)

    logging.debug('Writing input data: %s', req.text)
    outfile.write_text(req.text)

# Exectime header
ET_HEADER = textwrap.dedent('''\
    ## Solution execution times
    NOTE: All times in milliseconds

    | Year | Day | Part 1 | Part 2 |
    | ---- | --- | ------ | ------ |
    ''')

# Exectime regex
# | 2022 | 1   | 2.0000 | 2.0010 |
ET_RGX = re.compile(r'\| (?P<year>\d+) \| (?P<day>\d+) \| (?P<p1time>\d+.\d+) \| (?P<p2time>\d+.\d+) \|')

def exectime(year, day, p1time, p2time):

    outfile = pathlib.Path('EXECTIMES.md')
    with outfile.open('r') as fp:
        indata = fp.read()

    matches = [list(map(ast.literal_eval, m)) for m in ET_RGX.findall(indata)]
    matches.append((year, day, p1time, p2time))

    # Deduplicate data by copying it through a dict with (year, day) as the key
    matches = {(k[0], k[1]):(k[2], k[3]) for k in matches}
    matches = [k+v for k,v in matches.items()]

    def cmp(a,b):
        ayear, aday, _, _ = a
        byear, bday, _, _ = b
        if ayear == byear:
            if aday == bday:
                return 0
            elif aday < bday:
                return -1
            else:
                return 1
        elif ayear < byear:
            return -1
        else:
            return 1

    matches.sort(key=functools.cmp_to_key(cmp), reverse=True)

    outdata = ET_HEADER
    for match in matches:
        year, day, p1time, p2time = match
        outdata += f'| {year} | {day} | {p1time:.4f} | {p2time:.4f} |\n'

    with outfile.open('w') as fp:
        fp.write(outdata)

def up(x, y): # pylint: disable=invalid-name
    '''
    Return the coordinates above the argument
    '''
    return x, y - 1

def down(x, y):
    '''
    Return the coordinates below the argument
    '''
    return x, y + 1

def left(x, y):
    '''
    Return the coordinates left of the argument
    '''
    return x - 1, y

def right(x, y):
    '''
    Return the coordinates right of the argument
    '''
    return x + 1, y

class Grid:
    def __init__(self, height, width, default=0):
        logging.info('GRID: %s x %s', height, width)
        self.height = height
        self.width = width
        self.default = default

        self._grid = [self.default] * (height * width)

    @classmethod
    def init_with_data(cls, data, default=0):
        height = len(data)
        width = len(data[0])

        grid = cls(height, width, default=default)

        grid._grid = list(itertools.chain(*data))

        return grid

    def __getitem__(self, key):
        '''
        Get the value at the provided coordinates (x, y)
        '''
        if not isinstance(key, (tuple, list)):
            raise TypeError(f'Invalid type: {type(key)}')

        x, y = key

        if x < 0 or x >= self.width:
            return self.default

        if y < 0 or y >= self.height:
            return self.default

        return self._grid[x + self.width * y]

    def __setitem__(self, key, value):
        '''
        Set the value at the provided coordinates (x, y)
        '''
        if not isinstance(key, (tuple, list)):
            raise TypeError('Invalid type: {type(key)}')

        x, y = key

        if x < 0 or x >= self.width:
            return

        if y < 0 or y >= self.height:
            return

        self._grid[x + self.width * y] = value

    def _get(self, x, y):
        return self[x, y]

    def _set(self, x, y, val):
        self[x, y] = val

    def up(self, x, y):  # pylint: disable=invalid-name
        '''
        Return the value above the provided coordinates
        '''
        if y == 0:
            return self.default

        return self._get(*up(x, y))

    def down(self, x, y):
        '''
        Return the value below the provided coordinates
        '''
        if y == self.height - 1:
            return self.default

        return self._get(*down(x, y))

    def left(self, x, y):
        '''
        Return the value left of the provided coordinates
        '''
        if x == 0:
            return self.default

        return self._get(*left(x, y))

    def right(self, x, y):
        '''
        Return the value right of the provided coordinates
        '''
        if x == self.width - 1:
            return self.default

        return self._get(*right(x, y))

    def count(self, val):
        return self._grid.count(val)

    def print(self, xoffset=0, yoffset=0):
        for yy in range(self.height):  # pylint: disable=invalid-name
            height = self.width * (yy - yoffset)
            print(self._grid[0+xoffset + height:self.width + height])

    def foreach(self, min_x=0, min_y=0, max_x=None, max_y=None):
        if max_x is None:
            max_x = self.width

        if max_y is None:
            max_y = self.height
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                yield (x, y)

    def rotate(self):
        data = copy.copy(self._grid)
        grid = []

        offset = 0
        while len(grid) < self.height:
            grid.append(data[offset:offset+self.width])
            offset += self.width

        data = [list(reversed(k)) for k in zip(*grid)]
        return self.__class__.init_with_data(data)

    def hrange(self, start, end):
        '''Get a slice of a row '''
        assert isinstance(start, (list, tuple))
        assert isinstance(end, (list, tuple))

        # A row will have the same y coord
        assert start[1] == end[1]

        row = start[1]

        start = start[0]
        end = end[0]

        return self._grid[(row * self.width) + start:(row * self.width) + end]

    def vrange(self, start, end):
        '''Get a slice of a column'''
        assert isinstance(start, (list, tuple))
        assert isinstance(end, (list, tuple))

        # A column will have the same x coord
        assert start[0] == end[0]

        col = start[0]

        start = start[1]
        end = end[1]

        ret = []
        for ii in range(start, end):
            ret.append(self._grid[col + (ii * self.width)])

        return ret

    def find(self, val):
        for xy in self.foreach():
            if self[xy] == val:
                return xy
        raise ValueError(f'Value not found in grid: {val}')

    def findall(self, val):
        ret = []
        for xy in self.foreach():
            if self[xy] == val:
                ret.append(xy)

        return ret

    def adjacent(self, x, y):
        _up = up(x, y)
        _down = down(x, y)
        _left = left(x, y)
        _right = right(x, y)

        ret = []

        for x, y in (_up, _down, _left, _right):
            if x < 0 or x > self.width - 1:
                continue

            if y < 0 or y > self.height - 1:
                continue

            ret.append((x,y))

        return ret

    def extend(self, new_height, new_width):
        assert new_height >= self.height
        assert new_width >= self.width

        grid = Grid(new_height, new_width)
        for xy in self.foreach():
            grid[xy] = self[xy]

        self.height = new_height
        self.width = new_width
        self._grid = copy.copy(grid._grid)
