#!/usr/bin/python3

import subprocess as sp


def run_cmd(cmd):
    return sp.check_output(cmd.split()).decode('utf-8').split('\n')


if __name__ == '__main__':
    devices = run_cmd('xinput')
    dev_id = int([d.split('id=')[-1].split()[0] for d in devices if 'TouchPad' in d][0])
    props = run_cmd(f'xinput list-props {dev_id}')
    line_to_id = lambda s: s.split('(')[-1].split(')')[0]
    tap_id = int([line_to_id(p) for p in props if 'Tapping Enabled' in p and 'Default' not in p][0])
    scroll_id = int([line_to_id(p) for p in props if 'Natural Scrolling Enabled' in p and 'Default' not in p][0])
    print(run_cmd(f'xinput set-prop {dev_id} {tap_id} 1'))
    print(run_cmd(f'xinput set-prop {dev_id} {scroll_id} 1'))

