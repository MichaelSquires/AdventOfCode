import logging
import pathlib
import textwrap
import itertools

import bs4
import requests

__all__ = [
    'challenge',
    'download',
    'template',

    'Grid',
    'up', 'down', 'left', 'right'
]

def open_aoc(url):
    session = pathlib.Path('session.txt')
    if not session.exists():
        raise FileNotFoundError('session.txt')

    session_id = session.read_text().strip()
    cookies = dict(session=session_id)

    req = requests.get(url, cookies=cookies)
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

                        text += '\n'.join(textwrap.wrap(item.text, width=80, initial_indent='  - ', subsequent_indent='    '))
                        text += '\n\n'

    text += '\'\'\'\n'

    outfile = pathlib.Path(f'{year}/d{day}.py')
    text += outfile.read_text()
    outfile.write_text(text)

def template(year, day):
    template = ''
    template += 'def parse(data):\n'
    template += '    return data\n'
    template += '\n'

    template += 'def part1(data):\n'
    template += '    pass\n'
    template += '\n'

    template += 'def part2(data):\n'
    template += '    pass'

    outfile = pathlib.Path(f'{year}/d{day}.py')
    outfile.write_text(template)

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

def up(x, y):
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
    DEFAULT = 0

    def __init__(self, height, width):
        logging.info('GRID: %s x %s', height, width)
        self.height = height
        self.width = width

        self._grid = [self.__class__.DEFAULT] * (height * width)

    @classmethod
    def init_with_data(cls, data):
        height = len(data)
        width = len(data[0])

        grid = cls(height, width)

        grid._grid = list(itertools.chain(*data))

        return grid

    def __getitem__(self, key):
        '''
        Get the value at the provided coordinates (x, y)
        '''
        if not isinstance(key, (tuple, list)):
            raise TypeError('Invalid type: %s' % type(key))

        x, y = key

        if x < 0 or x >= self.width:
            return 0

        if y < 0 or y >= self.height:
            return 0

        return self._grid[x + self.width * y]

    def __setitem__(self, key, value):
        '''
        Set the value at the provided coordinates (x, y)
        '''
        if not isinstance(key, (tuple, list)):
            raise TypeError('Invalid type: %s' % type(key))

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

    def up(self, x, y):
        '''
        Return the value above the provided coordinates
        '''
        if y == 0:
            return None

        return self._get(*up(x, y))

    def down(self, x, y):
        '''
        Return the value below the provided coordinates
        '''
        if y == self.height - 1:
            return None

        return self._get(*down(x, y))

    def left(self, x, y):
        '''
        Return the value left of the provided coordinates
        '''
        if x == 0:
            return None

        return self._get(*left(x, y))

    def right(self, x, y):
        '''
        Return the value right of the provided coordinates
        '''
        if x == self.width - 1:
            return None

        return self._get(*right(x, y))

    def print(self):
        for yy in range(self.height):
            height = self.width * yy
            print(self._grid[0 + height:self.width + height])

    def foreach(self, min_x=0, min_y=0, max_x=None, max_y=None):
        if max_x is None:
            max_x = self.width

        if max_y is None:
            max_y = self.height
        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                yield (x, y)