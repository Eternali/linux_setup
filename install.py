#!/usr/bin/python3

## Copyright (C) 2018 Conrad Heidebrecht

from fullcolor.colors import Color
from fullcolor.common import CommonColors as cc
from os import getcwd, getlogin, system
import subprocess as sp
from sys import argv


COLORS = {
    'purple': Color('885ead')
}


class Config:

    def __init__(
        self,
        debug=False,
        dry_run=False,
        user='',
        homedir='',
        curdir='',
        silent=False,
        fail_hard=False
    ):
        self.debug = debug
        self.dry_run = dry_run
        self.user = user
        self.homedir = homedir
        self.curdir = curdir
        self.silent = silent
        self.fail_hard = fail_hard

    def pretty_print(self):
        if not self.silent:
            print(cc.GREEN.fg, end='')
            print( '\n------------------------------------')
            print( '[##] RUN CONFIGURATION:\n')
            print(f'[##] Debug:            {self.debug}')
            print(f'[##] Dry run:          {self.dry_run}')
            print(f'[##] User:             {self.user}')
            print(f'[##] Home Directory:   {self.homedir}')
            print(f'[##] Source Directory: {self.curdir}')
            print(f'[##] Fail Hard:        {self.fail_hard}')
            print( '-----------------------------------\n')
            print(cc.RT, end='')

    def log(self, msg, level=0):
        """Log message according to log level:
        0 = not set (everything)
        1 = debug (if debug is set)
        2 = info (same as debug but PURPLE)
        3 = critical (same as debug but RED)

        If the silent flag has been set, nothing will be logged regardless of the level
        
        Arguments:
            msg {String} -- message to print

        Keyword Arguments:
            level {int} -- level to log at (default: {0})
        """

        if self.silent:
            return

        if level == 0:
            print(msg)
        elif level == 1 and self.debug:
            print(cc.BLUE.fg + msg + cc.RT)
        elif level == 2 and self.debug:
            print(COLORS['purple'].fg + msg + cc.RT)
        elif level == 3 and self.debug:
            print(cc.RED.fg + msg + cc.RT)


class Installable:

    def __init__(self, dependancies, installs):
        self.gen_dependancies = dependancies if callable(dependancies) else None
        self.dependancies = [] if callable(dependancies) else dependancies
        self.gen_installs = installs if callable(installs) else None
        self.installs = [] if callable(installs) else installs
        self.config = None

    def generate(self, config):
        self.config = config
        if self.gen_dependancies:
            self.dependancies = self.gen_dependancies(config)
        if self.gen_installs:
            self.installs = self.gen_installs(config)

    def _call_cmd(self, cmd, sh_cmd):
        if callable(cmd):
            return cmd(self.config)
        elif self.config.dry_run:
            self.config.log('$ ' + cmd if isinstance(cmd, str) else ' '.join(cmd))
            return
        elif self.config.fail_hard:
            return sh_cmd(' '.join(cmd) if isinstance(cmd, list) else cmd)
        try:
            return sh_cmd(' '.join(cmd) if isinstance(cmd, list) else cmd)
        except Exception as e:
            return e.message

    def install(self, sh_cmd=system, with_deps=True):
        results = []
        if with_deps:
            for dep in self.dependancies:
                results.append(self._call_cmd(dep, sh_cmd))
        for inst in self.installs:
            results.append(self._call_cmd(inst, sh_cmd))
        
        return results


def distro_install(packs='', distro='debian', fix=False, update=False):
    cmd = ''
    if distro == 'debian':
        if update:
            cmd += 'sudo apt update'
        if packs:
            cmd += f"{' && ' if cmd else ''}sudo apt install -y {packs if isinstance(packs, str) else ' '.join(packs)}"
        if fix:
            cmd += f"{' && ' if cmd else ''}sudo apt install -f -y"
    
    return cmd


INSTALLABLES = {
    'zsh': Installable(
        lambda config: [
            distro_install(['git', 'build-essential', 'curl'])
        ],
        lambda config: [
            f'rm {config.homedir}/.zshrc',
            f'rm {config.homedir}/.zsh_aliases',
            distro_install('zsh'),
            ['sh -c',
            '"$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"'],
            'git clone https://github.com/bhilburn/powerlevel9k.git ' +
            f'{config.homedir}/.oh-my-zsh/custom/themes/powerlevel9k',
            f'ln -s {config.curdir}/.zshrc {config.homedir}/.zshrc',
            f'ln -s {config.curdir}/.zsh_aliases {config.homedir}/.zsh_aliases'
        ]
    ),
    'tmux': Installable(
        lambda config: [

        ],
        lambda config: [
            f'rm {config.homedir}/.tmux.conf',
            distro_install('tmux'),
            f'ln -s {config.curdir}/.tmux.conf {config.homedir}/.tmux.conf'
        ]
    ),
    'i3': Installable(
        lambda config: [
            distro_install([
                'libpth-dev',
                'libx11-dev',
                'libx11-xcb-dev',
                'libcairo2-dev',
                'libxcb-xkb-dev',
                'libxcb-xinerama0-dev',
                'libxcb-randr0-dev',
                'libxinerama-dev',
                'libxft-dev'
            ], fix=True),
            f'mkdir -p {config.homedir}/applications'
        ],
        lambda config: [
            f'rm -rf {config.homedir}/.config/i3',
            f'rm -rf {config.homedir}/.config/i3blocks',
            f'mkdir -p {config.homedir}/.config/i3',
            f'rm -r {config.homedir}/.screenlayout',
            distro_install([
                'i3',
                'i3blocks',
                'arandr',
                'pm-utils',
                'xbacklight',
                'blueman',
                'xautolock',
                'scratchpad'
            ]),
            f'ln -s {config.curdir}/.config/i3/config {config.homedir}/.config/i3/config',
            f'ln -s {config.curdir}/.config/i3/startup {config.homedir}/.config/i3/startup'
            f'ln -s {config.curdir}/.config/i3blocks {config.homedir}/.config/i3blocks',
            f'ln -s {config.curdir}/.screenlayout {config.homedir}/.screenlayout',
            f'cd {config.homedir}/Downloads && git clone https://github.com/guimeira/i3lock-fancy-multimonitor.git',
            f'cd {config.homedir}/Downloads && cp -r i3lock-fancy-multimonitor ' +
            f'{config.homedir}/.config/i3',
            f'chmod +x {config.homedir}/.config/i3/i3lock-fancy-multimonitor/lock',
            f'git clone https://github.com/sbstnc/dmenu-ee {config.homedir}/applications/dmenu-ee',
            f'cd {config.homedir}/applications/dmenu-ee && sudo make clean install',
            'sudo mv /usr/bin/dmenu /usr/bin/dmenu_bak',
            'sudo ln -s /usr/local/bin/dmenu /usr/bin/dmenu'
        ]
    ),
    'nvim': Installable(
        lambda config: [
            distro_install('python3-pip')
        ],
        lambda config: [
            distro_install(['neovim']),
            f'rm -rf {config.homedir}/.config/nvim',
            f'mkdir -p {config.homedir}/.config/nvim',
            f'ln -s {config.curdir}/.config/nvim/init.vim {config.homedir}/.config/nvim/init.vim',
            f'ln -s {config.homedir}/.config/nvim/colors {config.homedir}/.config/nvim/colors',
            'sudo pip3 install neovim'
        ]
    ),
    'nodejs': Installable(
        lambda config: [

        ],
        lambda config: [
            'curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -',
            distro_install('nodejs'),
            'sudo npm i -g standard eslint'
        ]
    ),
    'yarn': Installable(
        lambda config: [

        ],
        lambda config: [
            'curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -',
            'echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee ' +
            '/etc/apt/sources.list.d/yarn.list',
            distro_install('yarn')
        ]
    ),
    'kotlin': Installable(
        lambda config: [
            distro_install(['snapd', 'snapd-xdg-open'])
        ],
        lambda config: [
            distro_install(['default-jdk', 'gradle']),
            'sudo snap install kotlin --classic'
        ]
    ),
    'docker': Installable(
        lambda config: [

        ],
        lambda config: [
            'curl -fsSL https://download.docker.com/linux/ubuntu/gpg' +
            '| sudo apt-key add -',
            'sudo add-apt-repository "deb [arch=amd64] ' +
            'https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"',
            distro_install('docker-ce', update=True),
            'sudo groupadd docker',
            f'sudo usermod -aG docker {config.user}'
        ]
    ),
    'essentials': Installable(
        lambda config: [

        ],
        lambda config: [
            distro_install([
                'mongodb',
                'xclip',
                'python3-pip',
                'nitrogen',
                'apt-transport-https',
                'whois',
                'screenfetch'
            ]),
            'git config --global user.email "conrad.heidebrecht@gmail.com"',
            'git config --global user.name "Conrad"'
        ]
    ),
    'typescript': Installable(
        lambda config: [

        ],
        lambda config: [
            'sudo npm i -g typescript typings'
        ]
    ),
    'fonts': Installable(
        lambda config: [

        ],
        lambda config: [
            f'mkdir -p {config.homedir}/.fonts',
            f'cp {config.curdir}/.fonts/* {config.homedir}/.fonts/',
            distro_install('fonts-firacode')
        ]
    ),
    'flutter': Installable(
        lambda config: [
            f'mkdir -p {config.homedir}/applications',
            f'mkdir -p {config.homedir}/FlutterProjects'
        ],
        lambda config: [
            'git clone https://github.com/flutter/flutter.git -b beta ' +
            f'{config.homedir}/applications/flutter',
            f'. {config.homedir}/.zshrc',
            'flutter doctor',
            'git clone https://github.com/eternali/watoplan_flut -b dev ' +
            f'{config.homedir}/FlutterProjects/watoplan_flut',
            'git clone https://github.com/eternali/custom_radio ' +
            f'{config.homedir}/FlutterProjects/custom_radio',
            'git clone https://github.com/eternali/mldemos ' + 
            f'{config.homedir}/FlutterProjects/mldemos',
            'git clone https://github.com/eternali/flutter_calendar ' +
            f'{config.homedir}/FlutterProjects/flutter_calendar',
            'git clone https://github.com/eternali/date_utils ' +
            f'{config.homedir}/FlutterProjects/date_utils',
            'git clone https://github.com/eternali/tictacthrow ' +
            f'{config.homedir}/FlutterProjects/tictacthrow'
        ]
    ),
    'debs': Installable(
        lambda config: [

        ],
        lambda config: [
            f'cd {config.homedir}/Downloads && sudo dpkg -i skypeforlinux-64.deb ' +
            'google-chrome-stable_current_amd64.deb',
            distro_install(fix=True)
        ]
    ),
    'vue': Installable(
        lambda config: [
            f'mkdir -p {config.homedir}/VueProjects'
        ],
        lambda config: [
            'sudo npm i -g @vue/cli',
            'git clone https://github.com/eternali/conradheidebrecht.com ' +
            f'{config.homedir}/VueProjects/conradheidebrecht.com'
        ]
    ),
    'spotify': Installable(
        lambda config: [

        ],
        lambda config: [
            'sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys ' +
            '931FF8E79F0876134EDDBDCCA87FF9DF48BF1C90',
            'echo deb http://repository.spotify.com stable non-free | sudo tee ' +
            '/etc/apt/sources.list.d/spotify.list',
            distro_install('spotify-client')
        ]
    ),
    'signal': Installable(
        lambda config: [

        ],
        lambda config: [
            'curl -s https://updates.signal.org/desktop/apt/keys.asc | sudo apt-key add -',
            'echo "deb [arch=amd64] https://updates.signal.org/desktop/apt xenial main" ' +
            '| sudo tee -a /etc/apt/sources.list.d/signal-xenial.list',
            distro_install('signal-desktop', update=True)
        ]
    ),
    'brave': Installable(
        lambda config: [

        ],
        lambda config: [
            'curl https://brave-browser-apt-release.s3.brave.com/brave-core.asc | sudo apt-key add -',
            'echo "deb [arch=amd64] https://brave-browser-apt-release.s3.brave.com/ `lsb_release -sc` ' +
            'main" | sudo tee -a /etc/apt/sources.list.d/brave-browser-release-`lsb_release -sc`.list',
            distro_install('brave-browser', update=True)
        ]
    )
}


def help():
    print('')
    print('./install.py [options] [installables | \'all\']')
    print('\t [--debug, -d]   Run in debug mode with extra logging.')
    print('\t [--dry-run, -r] Only print operations to terminal, does not actually run anything.')
    print('\t [--silent, -s]  Do not display anything.')
    print('\t [--user, -u]    Specify which user to run as, defaults to the current user.')
    print('\t [--fail-hard, -f]   If specified will exit as soon as any error is encountered.')
    print('')
    print('\t [installables]  A space separated list of features to install.')
    print('\t                 \'all\' will install all possible features.')
    print('')
    print('Example: ./install.py --debug --dry-run --user bob zsh i3 kotlin')
    print('')

    exit(0)


def parse_args(args):
    has_arg = lambda to_find: any(a in args for a in to_find)
    def consume_args(to_consume):
        consumed = []
        for arg in to_consume:
            if arg in args:
                consumed.append(args[args.index(arg) + 1])
                args.remove(consumed[-1])
        return consumed

    if has_arg(['--help', '-h']):
        help()

    debug = has_arg(['--debug', '-d'])
    dry_run = has_arg(['--dry-run', '-r'])
    silent = has_arg(['--silent', '-s'])
    user = consume_args(['--user', '-u'])
    user = user[0] if len(user) else None
    to_install = [arg.lower() for arg in args if not arg.startswith('-')]
    fail_hard = has_arg(['--fail-hard', '-f'])

    return debug, dry_run, silent, user, to_install, fail_hard


def main():
    debug, dry_run, silent, user, to_install, fail_hard = parse_args(argv[1:])

    config = Config(
        debug=debug,
        dry_run=dry_run,
        user=user or getlogin(),
        homedir=f'/home/{user or getlogin()}',
        curdir=getcwd(),
        silent = silent,
        fail_hard = fail_hard
    )

    config.pretty_print()

    if len(to_install) and to_install[0] == 'all':
        to_install = INSTALLABLES.keys()
    for name in to_install:
        if name not in INSTALLABLES.keys():
            continue
        installable = INSTALLABLES[name]
        config.log(f'Generating installation commands for {name}.', 2)
        installable.generate(config)
        config.log(f'Installing {name}.', 2)
        installable.install()
        config.log(f'Finished installing {name}.' + '\n', 2)


if __name__ == '__main__':
    main()
