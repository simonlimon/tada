#!/usr/bin/env python

import cursor
import argparse
from random import randint
from termcolor import cprint
from time import sleep


class Network():

    STATE_TO_COLOR = {
        '.': 'grey',
        '*': 'cyan',
        'r': 'magenta',
        'g': 'green',
        'G': 'green',
        '>': 'white',
        '<': 'white',
        '!': 'red',
        '(': 'yellow',
        '[': 'yellow',
        '{': 'yellow',
        ')': 'yellow',
        '}': 'yellow',
        ']': 'yellow'
    }

    def __init__(self, k):
        self.states = []
        # init = ['x', 'y']
        for _ in range(0, 2**k - 1):
            # self.states += [init[randint(0,1)]]
            self.states += ['.']

    def update(self):
        # update logic for first state
        next_states = [None] * len(self.states)
        for i in range(1, len(self.states)-1):
            s = self.states[i]
            neighbors = (self.states[i-1], self.states[i+1])

            if s == '*':
                if neighbors == ('*', '*'):
                    s = '!'

            elif s == 'g':
                if neighbors == ('*', '*'):
                    s = '*'
                else:
                    s = 'G'

            elif s == 'G':
                s = '.'

            elif s == 'r':
                s = '*'

            elif s == ']':
                if neighbors[1] == '<':
                    s = 'r'
                else:
                    s = ')'

            elif s == '[':
                if neighbors[0] == '>':
                    s = 'r'
                else:
                    s = '('

            elif s == '}':
                if neighbors[1] == '<':
                    s = 'r'
                elif neighbors[1] == 'g':
                    s = '*'
                else:
                    s = ']'

            elif s == '{':
                if neighbors[0] == '>':
                    s = 'r'
                elif neighbors[0] == 'g':
                    s = '*'
                else:
                    s = '['

            elif s == ')' or s == '(':
                s = '.'

            elif s == '<':
                if neighbors[1] in ['G']:
                    s = '{'
                elif neighbors[0] in ['*']:
                    s = '>'
                else:
                    s = '.'

            elif s == '>':
                if neighbors[0] in ['G']:
                    s = '}'
                elif neighbors[1] in ['*']:
                    s = '<'
                else:
                    s = '.'

            elif s == '.':
                if 'r' in neighbors:
                    s = 'g'
                elif neighbors == ('.', 'g'):
                    s = '<'
                elif neighbors == ('g', '.'):
                    s = '>'
                elif neighbors[0] == '>':
                    s = '>'
                elif neighbors[1] == '<':
                    s = '<'
                elif neighbors[0] == ')':
                    s = '}'
                elif neighbors[1] == '(':
                    s = '{'

            next_states[i] = s

        # update logic for first state
        s = self.states[0]
        if s == '*':
            if self.states[1] == '*':
                s = '!'
        elif s == '.':
            if self.states[1] == '<':
                s = '<'
            elif self.states[1] == '*':
                s = '*'
        elif s == '<':
            s = '>'
        elif s == '>':
            s = '.'
        next_states[0] = s

        # update logic for last state
        s = self.states[-1]
        if s == '*':
            if self.states[-2] == '*':
                s = '!'
        elif s == '.':
            if self.states[-2] == '>':
                s = '>'
            elif self.states[-2] == '*':
                s = '*'
        elif s == '>':
            s = '<'
        elif s == '<':
            s = '.'
        elif s == 'g':
            s = 'G'
        elif s == 'G':
            s = '.'

        next_states[-1] = s

        self.states = next_states

    def print_states(self, leave_trace=False):
        for s in self.states:
            cprint(s, color=self.STATE_TO_COLOR[s], attrs=['bold'], end='')
        print('\n' if leave_trace else '\r', end='')


def animate_network(k=2, leave_trace=False, speed=10):
    cursor.hide()

    n = Network(k)
    n.print_states()
    n.states[-1] = 'g'
    while n.states[0] != '!':
        sleep(1.0/speed)
        n.print_states(leave_trace)
        n.update()
    n.print_states()

    cursor.show()


def main():
    parser = argparse.ArgumentParser(description='Animate a tada! network')
    parser.add_argument('k', type=int, help='network size')
    parser.add_argument('-s', '--speed', default=10, type=int,
                        help='animation speed, defaults to 3', metavar='N')
    parser.add_argument('-t', '--trace', action='store_true',
                        help='leave trace of animation')
    args = parser.parse_args()
    animate_network(args.k, args.trace, args.speed)


if __name__ == '__main__':
    main()
