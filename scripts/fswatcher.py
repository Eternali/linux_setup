#!/usr/bin/python3

import inotify.adapters
import shlex
from subprocess import PIPE, Popen
from sys import argv
from threading import Thread

from util import parse_args


def usage():
    print('Usage: ./fswatcher [-h, --help] [-a] [-p /path/to/dir] CMD')
    print()
    print('-h, --help Shows this usage')
    print('-a         Reruns command when a change is detected in the specified path')
    print('-p         Path to directory to watch')
    print('CMD        Command to run on reload')
    exit(0)


proc = None

def start_watcher(path, cmd):
    global proc
    print(f'Watching {path} and running "{cmd}" on change.')
    watcher = inotify.adapters.InotifyTree(path)

    for event in watcher.event_gen(yield_nones=False):
        if 'IN_CLOSE_WRITE' in event[1]:
            proc.kill()
            proc = Popen(shlex.split(cmd))


def manual_reload(cmd):
    global proc
    print('[**] Press ENTER to reload.')
    while True:
        input('')
        print('[!!] Reloading...')
        proc.kill()
        proc = Popen(shlex.split(cmd))


def main():
    global proc
    [_, *cmd], [auto], [path] = parse_args(argv, flags=['-a'], named=['-p'])
    if cmd[0] in ['-h', '--help']:
        usage()
    cmd = ' '.join(cmd)

    watcher_thread = None
    try:
        proc = Popen(shlex.split(cmd))
        if auto:
            watcher_thread = Thread(target=start_watcher, args=(path, cmd))
            watcher_thread.daemon = True
            watcher_thread.start()
        manual_reload(cmd)
    except KeyboardInterrupt:
        print('[!!] Exiting.')
        exit(0)


if __name__ == '__main__':
    main()

