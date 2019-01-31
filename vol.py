#!/usr/bin/python3

from os import system
from sys import argv


def consume_args(to_consume, args=argv):
    consumed = []
    for arg in to_consume:
        if arg in args:
            consumed.append(args[args.index(arg) + 1])
            args.remove(arg)
            args.remove(consumed[-1])
    return consumed


def main():
    card = consume_args(['--card', '-c'])
    card = card[0] if card else 1
    output = consume_args(['--output', '-o'])[0]
    amt = argv[-1] if argv[-1].endswith(('-', '+')) else '5+'
    tmute = 'tmute' in argv
    if tmute:
        system(f'amixer -c {card} sset {output} toggle')
    system(f'amixer sset -c {card} {output} {amt}')

if __name__ == '__main__':
    main()

