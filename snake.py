#! /usr/bin/env python3
'''
Snake!

Make sure your terminal is at least 40 rows high.
'''

# Imports

import curses
import random

# Classes

class Vector:
    def __init__(self, container):
        self.i = container[0]
        self.j = container[1]
        return

    def __add__(self, other):
        if isinstance(other, int):
            i = self.i + other
            j = self.j + other
        elif isinstance(other, type(self)):
            i = self.i + other.i
            j = self.j + other.j
        return Vector((i, j))

    def __mul__(self, other):
        if isinstance(other, int):
            i = self.i * other
            j = self.j * other
        return Vector((i, j))

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    __radd__ = __add__

    __rmul__ = __mul__

    def __neg__(self): return -1 * self

    def __sub__(self, other): return self.__add__(-other)

    def __rsub__(self, other): return -self.__add__(other)

class Snake:
    
    size = 40
    snakeDirection = Vector((0, +1))
    snakeLength = 8
    period = 300
    snakeSpeed = 1
    score = 0

    def __init__(self):
        self.snakeDirection = Vector(self.snakeDirection)

        self.Initialize()
        self.Go()
        return

    def Increment(self):

        # Push snake head

        self.snakeHead += self.snakeDirection
        self.snake.insert(0, self.snakeHead)

        # Check for snake/border collision

        if self.snakeHead.i == 0 or self.snakeHead.j == 0 or self.snakeHead.i == self.size - 1 or self.snakeHead.j == self.size - 1 or any(segment == self.snakeHead for segment in self.snake[1 : ]):
            self.alive = False
            self.PrePaint(self.snakeHead, 'X')
        else:
            self.PrePaint(self.snakeHead, 'O')

        # Check for snake/fruit collision

        if self.snakeHead == self.fruit:
            self.NewFruit()

            self.score += 10 * self.snakeSpeed
            self.UpdateScore()
            self.snakeSpeed += 2
            self.pad.timeout(self.period // self.snakeSpeed)
            self.snakeLength += self.snakeSpeed

        # Pull snake tail?

        if len(self.snake) >= self.snakeLength:
            self.PrePaint(self.snake.pop(), ' ')

        # Paint

        curses.doupdate()
        return

    def Initialize(self):
        self.snakeHead = Vector([self.size // 2] * 2)
        self.snake = [self.snakeHead - (self.snakeDirection * index) for index in range(self.snakeLength)]

        stdscr = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        self.pad = curses.newpad(self.size, self.size)
        self.pad.border('|', '|', '-', '-')
        for segment in self.snake:
            self.pad.addch(segment.i, segment.j, 'O')
        self.NewFruit()

        self.pad.keypad(1)
        self.pad.nodelay(1)
        self.pad.timeout(self.period // self.snakeSpeed)
        self.UpdateScore()
        self.pad.addstr(self.size - 1, self.size // 2 - 5, '(q to quit)')
        self.pad.refresh(0, 0, 0, 0, self.size, self.size)

        return

    def Go(self):
        key2Direction = {\
            curses.KEY_UP    : Vector((-1, 0)),\
            curses.KEY_LEFT  : Vector(( 0,-1)),\
            curses.KEY_DOWN  : Vector((+1, 0)),\
            curses.KEY_RIGHT : Vector(( 0,+1)),\
        }
        null = Vector((0, 0))
        self.alive = True
        while self.alive:

            # Wait a little for keypress

            key = self.pad.getch()
            if key in key2Direction:
                if null != self.snakeDirection + key2Direction[key]:
                    self.snakeDirection = key2Direction[key]
            elif ord('q') == key:
                self.alive = False
                break
            self.Increment()

        # Nuke curses

        self.pad.keypad(0)
        curses.curs_set(1)
        curses.echo()
        curses.endwin()
        return

    def NewFruit(self):
        self.fruit = self.snakeHead
        while any(segment == self.fruit for segment in self.snake):
            self.fruit = Vector((random.choice(range(1, self.size - 1)), random.choice(range(1, self.size - 1))))
        self.PrePaint(self.fruit, '@')
        return

    def PrePaint(self, vector, character):
        i, j = vector.i, vector.j
        self.pad.addch(i, j, character)
        self.pad.noutrefresh(i, j, i, j, i, j)
        return

    def UpdateScore(self):
        self.pad.addstr(0, self.size // 2 - 7, '| Score: {:3d} |'.format(self.score))
        self.pad.noutrefresh(0, 0, 0, 0, 0, self.size - 1)
        return

# Script

if __name__ == '__main__':
    snake = Snake()
