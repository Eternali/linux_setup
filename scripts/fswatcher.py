#!/usr/bin/python3

import inotify.adapters
from os import system
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


def startWatcher(path, cmd):
    print(f'Watching {path} and running "{cmd}" on change.')
    watcher = inotify.adapters.InotifyTree(path)

    for event in watcher.event_gen(yield_nones=False):
        if 'IN_CLOSE_WRITE' in event[1]:
            system(cmd)


def manualReload(cmd):
    print('[**] Press ENTER to reload.')
    while True:
        input('')
        print('[!!] Reloading...')
        system(cmd)


def main():
    [_, *cmd], [auto], [path] = parse_args(argv, flags=['-a'], named=['-p'])
    if cmd[0] in ['-h', '--help']:
        usage()
    cmd = ' '.join(cmd)

    watcherThread = None
    try:
        system(cmd)
        if auto:
            watcherThread = Thread(target=startWatcher, args=(path, cmd))
            watcherThread.daemon = True
            watcherThread.start()
        manualReload(cmd)
    except KeyboardInterrupt:
        print('[!!] Exiting.')
        exit(0)


if __name__ == '__main__':
    main()

