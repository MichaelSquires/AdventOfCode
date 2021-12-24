'''
## --- Day 13: Care Package ---

As you ponder the solitude of space and the ever-increasing three-hour roundtrip
for messages between you and Earth, you notice that the Space Mail Indicator
Light is blinking.  To help keep you sane, the Elves have sent you a care
package.

It's a new game for the ship's arcade cabinet! Unfortunately, the arcade is all
the way on the other end of the ship. Surely, it won't be hard to build your own
- the care package even comes with schematics.

The arcade cabinet runs Intcode software like the game the Elves sent (your
puzzle input). It has a primitive screen capable of drawing square tiles on a
grid.  The software draws tiles to the screen with output instructions: every
three output instructions specify the x position (distance from the left), y
position (distance from the top), and tile id. The tile id is interpreted as
follows:

  - 0 is an empty tile.  No game object appears in this tile.

  - 1 is a wall tile.  Walls are indestructible barriers.

  - 2 is a block tile.  Blocks can be broken by the ball.

  - 3 is a horizontal paddle tile.  The paddle is indestructible.

  - 4 is a ball tile.  The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a
horizontal paddle tile (1 tile from the left and 2 tiles from the top) and a
ball tile (6 tiles from the left and 5 tiles from the top).

Start the game. How many block tiles are on the screen when the game exits?

## --- Part Two ---

The game didn't run because you didn't put in any quarters. Unfortunately, you
did not bring any quarters. Memory address 0 represents the number of quarters
that have been inserted; set it to 2 to play for free.

The arcade cabinet has a joystick that can move left and right.  The software
reads the position of the joystick with input instructions:

  - If the joystick is in the neutral position, provide 0.

  - If the joystick is tilted to the left, provide -1.

  - If the joystick is tilted to the right, provide 1.

The arcade cabinet also has a segment display capable of showing a single number
that represents the player's current score. When three output instructions
specify X=-1, Y=0, the third output instruction is not a tile; the value instead
specifies the new score to show in the segment display.  For example, a sequence
of output values like -1,0,12345 would show 12345 as the player's current score.

Beat the game by breaking all the blocks. What is your score after the last
block is broken?

'''
import enum

import utils

from . import intcode

parse = intcode.parse

class Grid(utils.Grid):
    def __str__(self):
        ret = '\n'
        for yy in range(self.height):
            height = self.width * yy
            row = self._grid[0 + height:self.width + height]
            ret += ''.join(str(k) for k in row)
            ret += '\n'

        ret = ret.replace('0', ' ')
        ret = ret.replace('1', 'X')
        ret = ret.replace('2', '#')
        ret = ret.replace('3', '-')
        ret = ret.replace('4', 'o')

        return ret

class State(enum.IntEnum):
    X = 0
    Y = 1
    TILE = 2
    
class Tile(enum.IntEnum):
    Empty = 0
    Wall = 1
    Block = 2
    HPaddle = 3
    Ball = 4

class Arcade:
    def __init__(self):
        self.screen = Grid(30, 50)
        self.state = State.X
        self.x = None
        self.y = None
        
    def input(self, val):
        match self.state:
            case State.X:
                self.x = val
                self.state = State.Y

            case State.Y:
                self.y = val
                self.state = State.TILE

            case State.TILE:
                if (self.x, self.y) == (-1, 0):
                    print(f'SCORE: {val}')
                else:
                    self.screen[(self.x, self.y)] = val

                self.state = State.X
                self.x = None
                self.y = None
                
    def joystick(self):
        print(self.screen)
        val = input('Enter value: ')
        match val:
            case '\x1b[D': return -1
            case '\x1b[C': return 1
            case _: return 0
        
def part1(data):
    arcade = Arcade()
    
    mach = intcode.Computer()
    mach.load(data)
    
    mach.outfunc = arcade.input
    
    mach.run()

    return arcade.screen.count(Tile.Block)

def part2(data):
    arcade = Arcade()
    
    mach = intcode.Computer()
    mach.load(data)
    mach.mem[0] = 2
    
    mach.infunc = arcade.joystick
    mach.outfunc = arcade.input
    
    mach.run()

    return 