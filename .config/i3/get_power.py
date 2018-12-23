#!/usr/bin/python3

import subprocess as sp
from sys import argv


def run_cmd(cmd):
    return sp.check_output(cmd.split()).decode('utf-8').strip().split('\n')


def main():
    # usually the files are either prefixed with "charge" or "energy"
    mode = argv[-1] if len(argv) == 2 else 'charge'
    bat_dir = '/sys/class/power_supply'
    batteries = [bat for bat in run_cmd(f'ls {bat_dir}') if 'BAT' in bat]
    fulls = [int(run_cmd(f'cat {bat_dir}/{b}/{mode}_full')[0]) for b in batteries]
    currents = [int(run_cmd(f'cat {bat_dir}/{b}/{mode}_now')[0]) for b in batteries]
    adjusted_pct = round(sum(currents) / sum(fulls) * 100.0, )
    print(adjusted_pct, end='')


if __name__ == '__main__':
    main()

