# ======================================================================================================================
# SERVICE LIB
# Dependencies: psutil
# ======================================================================================================================
from subprocess import PIPE, Popen, TimeoutExpired, STDOUT


__all__ = [
    "as_dict", "stop_service", "service_up", "can_shutdown", "can_pause", "can_stop", "set_startup"
]


def __sys_exec(command, timeout=None, work_dir=None) -> int:
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


def __ps_exec(cmd):
    output = Popen(cmd, stderr=STDOUT, stdout=PIPE)
    output_collected = output.communicate()[0], output.returncode
    command_out = output_collected[0].decode('utf-8').strip()
    return command_out


def __ps_bool(cmd):
    if 'False' in __ps_exec(cmd):
        return False
    elif 'True' in __ps_exec(cmd):
        return True


def __status(cmd):
    if 'Running' in __ps_exec(cmd):
        return True
    elif 'Stopped' in __ps_exec(cmd):
        return False


def as_dict(service) -> dict:
    """Return service info as dictionary"""
    data = dict()
    status = __sys_exec(f"powershell Stop-Service -Name {service} -Force -Confirm:$false") == 0
    shutdown = __ps_bool(f"powershell Get-Service -Name {service} | Select-Object -ExpandProperty CanShutdown")
    stoppable = __ps_bool(f"powershell Get-Service -Name {service} | Select-Object -ExpandProperty CanStop")
    pausable = __ps_bool(f"powershell Get-Service -Name {service} | Select-Object -ExpandProperty CanPauseAndContinue")

    if status:
        state = 'running'
    else:
        state = 'stopped'

    data['status'] = state
    data['can_shutdown'] = shutdown
    data['can_stop'] = stoppable
    data['can_pause'] = pausable

    return data


def stop_service(service) -> bool:
    """Terminate Service"""
    return __sys_exec(f"powershell Stop-Service -Name {service} -Force -Confirm:$false") == 0


def service_up(service) -> bool:
    """Return is service running"""
    return as_dict(service)['status'] == 'running'


def can_shutdown(service) -> bool:
    """Get property for a service: CanShutDown"""
    return as_dict(service)['can_shutdown']


def can_pause(service) -> bool:
    """Get property for a service: CanPauseAndContinue"""
    return as_dict(service)['can_pause']


def can_stop(service) -> bool:
    """Get property for a service: CanStop"""
    return as_dict(service)['can_stop']


def set_startup(service, option="manual") -> bool:
    """Change service startup type"""
    if option == "manual":
        type_ = "Manual"
    if option == "auto":
        type_ = "Automatic"
    if option == "disable":
        type_ = "Disable"

    return __sys_exec(f"powershell Set-Service -Name {service} -StartupType {type_}") == 0
