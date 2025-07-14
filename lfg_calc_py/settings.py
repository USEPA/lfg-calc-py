"""
Settings to import datapath
"""

import os
import subprocess
from importlib.metadata import version
from pathlib import Path
from esupy.processed_data_mgmt import Paths, mkdir_if_missing
from esupy.util import get_git_hash


DEFAULT_DOWNLOAD_IF_MISSING = False

MODULEPATH = Path(__file__).resolve().parent
methodpath = MODULEPATH / 'methods'
datapath = MODULEPATH / 'data'

# "Paths()" are a class defined in esupy
paths = Paths()
paths.local_path = paths.local_path / 'lfg-calc-py'
outputpath = paths.local_path
lfgoutputpath = outputpath / 'MethodOutput'
logoutputpath = outputpath / 'Logs'

# ensure directories exist
mkdir_if_missing(lfgoutputpath)
mkdir_if_missing(logoutputpath)



def return_pkg_version():
    # return version with git describe
    try:
        # set path to flowsa repository, necessary if running method files
        # outside the flowsa repo
        tags = subprocess.check_output(
            ["git", "describe", "--tags", "--always", "--match", "v[0-9]*"],
            cwd=MODULEPATH).decode().strip()
        pkg_version = tags.split("-", 1)[0].replace('v', "")
    except subprocess.CalledProcessError:
        pkg_version = version('lfg-calc-py')

    return pkg_version


# https://stackoverflow.com/a/41125461
def memory_limit(percentage=.93):
    # Placed here because older versions of Python do not have this
    import resource
    # noinspection PyBroadException
    try:
        max_memory = get_memory()
        print(f"Max Memory: {max_memory}")
    except Exception:
        print("Could not determine max memory")
    else:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        resource.setrlimit(resource.RLIMIT_AS, (int(max_memory * 1024 * percentage), hard))


def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:', 'SwapFree:'):
                free_memory += int(sline[1])
    return free_memory


# metadata
PKG = "lfg-calc-py"
PKG_VERSION_NUMBER = return_pkg_version()
GIT_HASH_LONG = os.environ.get('GITHUB_SHA') or get_git_hash('long')
if GIT_HASH_LONG:
    GIT_HASH = GIT_HASH_LONG[0:7]
else:
    GIT_HASH = None

# Common declaration of write format for package data products
WRITE_FORMAT = "parquet"


