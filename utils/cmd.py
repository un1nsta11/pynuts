# ======================================================================================================================
# COMMAND EXECUTOR
# ======================================================================================================================
from subprocess import Popen, PIPE, TimeoutExpired


def cmd(command, timeout=None, work_dir=None) -> int:
    """
    Execute command and return exit code
    :param command: command <- str()
    :param timeout: seconds <- int()
    :param work_dir: path <- str()
    :return: error_level <- int()
    """
    proc = Popen(command, stdout=PIPE, stderr=PIPE, cwd=work_dir)
    error_level = 0
    try:
        proc.communicate(timeout=timeout)
        error_level = proc.returncode
    except TimeoutExpired:
        error_level = 5
    return error_level
