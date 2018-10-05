#!/usr/bin/python3

import subprocess as sp


def run_cmd(cmd):
    return sp.check_output(cmd.split()).decode('utf-8').split('\n')


if __name__ == '__main__':
    devices = run_cmd('xinput')
    dev_id = int([d.split('id=')[-1].split()[0] for d in devices if 'TouchPad' in d][0])
    props = run_cmd(f'xinput list-props {dev_id}')
    prop_id = int([p.split('(')[-1].split(')')[0] for p in props if 'Tapping Enabled' in p and 'Default' not in p][0])
    print(run_cmd(f'xinput set-prop {dev_id} {prop_id} 1'))

