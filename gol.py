#! /usr/bin/env python3
'''
An implementation of the 2-D Conway's game of life: http://www-inst.eecs.berkeley.edu/~selfpace/cs9honline/P1/
'''

# Constants

RULE = 30
ROWS = 10

# Functions

def BinaryString(number, bits):
    binary = bin(number)[2 : ]
    return '0' * (bits - len(binary)) + binary

def main(rule, rows, bits = 3):
  
    ruleString = BinaryString(rule, 2 ** bits)[ : : -1]

    bitMask = dict((BinaryString(index, bits), ruleString[index]) for index in range(2 ** bits))

    columns = rows * 2 + 1
    yield 'P1 {:d} {:d}'.format(columns, rows)

    columns -= 2
    line = '0' * rows + '1' + '0' * rows
    for row in range(rows):
        yield line
        line = ''.join(bitMask[line[column : column + bits]] for column in range(columns))
        line = '0' + line + '0'

# Script

if __name__ == '__main__':
    from sys import argv

    argv.pop(0)
    rule = (bool(argv) and int(argv.pop(0))) or RULE
    rows = (bool(argv) and int(argv.pop(0))) or ROWS

    print(*main(rule, rows), sep='\n')
