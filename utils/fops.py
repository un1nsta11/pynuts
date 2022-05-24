# ======================================================================================================================
# FILE OPERATIONS IN SYSTEM
# ======================================================================================================================

__all__ = [
    "version", "file_hash",
]

from subprocess import Popen, PIPE
from hashlib import sha1, md5


def __sys_req(query):
    """Execute system command"""
    data = None
    proc_ = Popen(query, stdout=PIPE, stderr=PIPE)
    outs, errs = proc_.communicate()
    if proc_.returncode == 0:
        if outs:
            data = outs.decode()
        else:
            pass
    else:
        raise BaseException
    return data


def version(file_path) -> str:
    """Get version of a file"""
    return __sys_req(f'powershell (Get-Item "{file_path}" ).VersionInfo.FileVersion').replace(",", ".").strip()


def file_hash(filepath, hash_type='md5') -> str:
    """Get file hash"""
    if hash_type == 'md5':
        hash_func = md5()
    elif hash_type == 'sha1':
        hash_func = sha1()
    else:
        raise Exception('Unknown hash type')

    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return str(hash_func.hexdigest())
