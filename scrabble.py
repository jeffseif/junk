#! /usr/bin/env python3
'''
Find the Scrabble words which can be built from prompt
'''

# Imports

import itertools

# Constants

SCRABBLE_FILE = './scrabble.txt'

# Functions

def FindWords(prompt):

    # Build dictionary of sorted letter combinations mapped to words they can create

    with open(SCRABBLE_FILE, 'r') as f:
        words = set(tuple(f.read().split('\n')))

    sortedLetters2Words = {}
    for word in words:
        sortedLetters = tuple(sorted(word))
        if sortedLetters not in sortedLetters2Words:
            sortedLetters2Words[sortedLetters] = set()
        sortedLetters2Words[sortedLetters].add(word)

    # Return words that prompt can form

    prompt = tuple(sorted(prompt))

    return sorted(
        {word for length in range(len(prompt)) for combination in itertools.combinations(prompt, length + 1) for word in sortedLetters2Words.get(combination, [])},
        key = lambda string: (len(string), string),
    )

def Report(prompt, words):

    # Report results

    if prompt.lower() in words:
        print('> \'{:s}\' is a word'.format(prompt))

    if words:
        print('> \'{:s}\' can form {:d} words:'.format(prompt, len(words)))
        print(*words, sep = '\n')

def main(prompt):

    words = FindWords(prompt)
    Report(prompt, words)

# Script

if __name__ == '__main__':

    # Interpret arguments

    from sys import argv
    argv.pop(0)
    if argv:
        prompt = argv.pop(0)
    else:
        exit('word/letters were not input ... exiting')

    main(prompt)
