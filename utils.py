import logging
import pathlib

import requests

__all__ = [
    'download',
    'Grid',
    'up', 'down', 'left', 'right'
]

def download(year, day):
    outfile = pathlib.Path(f'inputs/{year}/d{day}.txt')
    if outfile.exists():
        return

    session = pathlib.Path('session.txt')
    if not session.exists():
        logging.warning('session.txt not found - not downloading input')
        return

    # Create inputs path if it doesn't exist
    pathlib.Path(f'inputs/{year}').mkdir(parents=True, exist_ok=True)

    session_id = session.read_text().strip()
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    cookies = dict(session=session_id)

    req = requests.get(url, cookies=cookies)
    if req.status_code != 200:
        raise Exception(f'Error downloading input data: {req.reason}')

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
    def __init__(self, height, width):
        logging.info('GRID: %s x %s', height, width)
        self.height = height
        self.width = width

        self._grid = [0] * (height * width)

    @classmethod
    def init_with_data(cls, data):
        height = len(data)
        width = len(data[0])

        grid = cls(height, width)

        flat = []
        for line in data:
            flat.extend(line)
        grid._grid = flat

        return grid

    def __getitem__(self, key):
        '''
        Get the value at the provided coordinates (x, y)
        '''
        if not isinstance(key, (tuple, list)):
            raise TypeError('Invalid type: %s' % type(key))

        x, y = key

        return self._grid[x + self.width * y]

    def __setitem__(self, key, value):
        '''
        Set the value at the provided coordinates (x, y)
        '''
        if not isinstance(key, (tuple, list)):
            raise TypeError('Invalid type: %s' % type(key))

        x, y = key

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

    def foreach(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y)