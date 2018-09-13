import os
import paramiko

from config import debug_mode

class FileGetter:

    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp = None

    def connect(self, host, port, uname):
        if debug_mode:
            print(f'connecting to {uname}@{host}:{port}')
        else:
            self.ssh.connect(hostname=host, port=port, username=uname)
            self.sftp = ssh.open_sftp()

    def disconnect(self):
        if debug_mode:
            print('disconnecting')
        else:
            self.sftp.close()

    def close(self):
        if self.sftp.isOpen():
            self.sftp.close()
        self.ssh.close()

    # files is an array of tuples with the format (remote_path, local_path)
    def get(self, files):
        for f in files:
            if debug_mode:
                print(f'getting remote:{f[0]}, local:{f[1]}')
            else:
                self.sftp.get(f[0], f[1])


class Setuper:

    def __init__(self, local, remote, get_first=False, is_script=False, recursive=False):
        self.local = local
        self.remote = remote
        self.get_first = get_first
        self.is_script = is_script

    @property
    def isRemote(self):
        return len(self.remote.split('@')) > 1 or len(self.remote.split('://')) > 1

    @property
    def host(self):
        return self.remote.split('@', 1)[-1].split(':', 1)[0]

    @property
    def port(self):
        return self.remote.split(':', 1)[-1].split('/', 1)[0]

    @property
    def username(self):
        return self.remote.split('@', 1)[0]

    @property
    def local_path(self):
        return '/' + self.local.split('/', 1)[-1]

    @property
    def remote_path(self):
        return '/' + self.remote.split('/', 1)[-1]


class Installable:

    def __init__(self, name, install_cmds, setup_files):
        self.name = name
        self.install_cmds = install_cmds
        self.setup_files = setup_files


def enforce_permissions():
    if os.getuid() != 0:
        raise Exception('Must be run as root!')

def distro_install(pkg_name, update_before=False):
    return f'apt update && apt install -y {pkg_name}'

def get_downloadables(files):
    all_remotes = [ ((f.host, f.port, f.username), (f.remote_path, f.local_path)) for f in [ fi for fi in files if fi.isRemote ] ]
    return [ (*r, [ ar[1] for ar in all_remotes if ar[0] == r ]) for r in set([ a[0] for a in all_remotes ]) ]

def download_before(installables):
    return get_downloadables([ f for inst in installables for f in inst.setup_files if f.get_first ])

def download_after(installables):
    return get_downloadables([ f for inst in installables for f in inst.setup_files if not f.get_first ])
