#!/usr/bin/python3

import inotify.adapters
from subprocess import Popen
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


def start_watcher(proc, path, cmd):
    print(f'Watching {path} and running "{cmd}" on change.')
    watcher = inotify.adapters.InotifyTree(path)

    for event in watcher.event_gen(yield_nones=False):
        if 'IN_CLOSE_WRITE' in event[1]:
            proc.terminate()
            proc = Popen([cmd], shell=True)


def manual_reload(proc, cmd):
    print('[**] Press ENTER to reload.')
    while True:
        input('')
        print('[!!] Reloading...')
        proc.terminate()
        proc = Popen([cmd], shell=True)


def main():
    [_, *cmd], [auto], [path] = parse_args(argv, flags=['-a'], named=['-p'])
    if cmd[0] in ['-h', '--help']:
        usage()
    cmd = ' '.join(cmd)

    watcher_thread = None
    running_proc = None
    try:
        running_proc = Popen([cmd], shell=True)
        if auto:
            watcher_thread = Thread(target=start_watcher, args=(running_proc, path, cmd))
            watcher_thread.daemon = True
            watcher_thread.start()
        manual_reload(running_proc, cmd)
    except KeyboardInterrupt:
        print('[!!] Exiting.')
        exit(0)


if __name__ == '__main__':
    main()

