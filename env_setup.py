#!/usr/bin/python3

import subprocess as sp

from config import *
from helpers import *

fgetter = FileGetter()
to_install = [
    Installable(
        'common_packages',
        [
            distro_install('git'),
            distro_install('build-essential')
            distro_install('docker'),
        ],
        []
    ),
    Installable(
        'general_config',
        [],
        [ Setuper(f'{local_home}/.config', f'{remote_root}/.config', recursive=True) ]
    ),
    Installable(
        'zsh',
        [
            distro_install('zsh'),
            'sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"',
            f'git clone https://github.com/bhilburn/powerlevel9k.git {local_home}/.oh-my-zsh/custom/themes/powerlevel9k',
            f'cd {tmp_dir} && git clone https://github.com/gabrielelana/awesome-terminal-fonts'
        ],
        [
            Setuper(f'{local_home}/.zshrc', f'{remote_root}/.zshrc'),
            Setuper(f'{tmp_dir}/install_fonts.sh', f'{remote_root}/install_fonts.sh')
        ]
    ),
    Installable(
        'nvim',
        [
            'add-apt-repository ppa:neovim-ppa/unstable',
            distro_install('neovim', update_before=True)
        ],
        []
    ),
    Installable(
        'yarn',
        [
            'curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -',
            'echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list',
            distro_install('yarn', update_before=True)
        ],
        []
    ),
    Installable(
        'i3',
        [
            distro_install('i3'),
            distro_install('nitrogen')
        ],
        [ Setuper(f'{local_home}/.screenlayout', f'{remote_root}/.screenlayout', recursive=True) ]
    ),
    Installable(
        'nodejs',
        [
            'curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -',
            distro_install('nodejs')
        ],
        []
    ),
    Installable(
        'code',
        [
            'curl -sL https://go.microsoft.com/fwlink/?LinkID=760868 | sudo dpkg -i -'
        ],
        []
    ),
    Installable(
        'chrome',
        [ f'dpkg -i {tmp_dir}/google-chrome.deb' ],
        [ Setuper(f'{tmp_dir}/google-chrome.deb', f'{remote_root}/google-chrome-stable_current_amd64.deb', get_first=True) ]
    ),
    Installable(
        'flutter',
        [
            f'curl -o {local_home}/flutter.zip https://github.com/flutter/flutter/archive/master.zip',
            f'unzip {local_home}/flutter.zip'
        ]
    )
]

def main():
    enforce_permissions()
    for (host, port, uname, files) in download_before(to_install):
        fgetter.connect(host, port, uname)
        fgetter.get(files)
        fgetter.disconnect()
    for inst in to_install:
        for cmd in inst.install_cmds:
            if debug_mode:
                print(cmd)
            else:
                sp.check_call(cmd.split(' '))
    for (host, port, uname, files) in download_after(to_install):
        fgetter.connect(host, port, uname)
        fgetter.get(files)
        fgetter.disconnect()


if __name__ == '__main__':
    main()
