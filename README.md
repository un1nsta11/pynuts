# PyNuts Framework

Convenient Python library to work with system commands, actions etc.

## Table of content

1. [Fast Start](#fast-start)
2. [Requirements](#requirements)
3. [cmd](#cmd) - system commands
4. [fops](#fops) - file operations
5. [proc](#proc) - processes 
6. [pyftp](#pyftp) - ftp (alternative for ftplib)
7. [regedit](#regedit) - registry (alternative for winreg)
8. [smb](#smb) - control drivers
9. [svc](#svc) - control Windows services
10. [tsch](#tsch) - work with Windows Task Scheduler

## Fast Start

1. Clone to any location: `git clone git@github.com:un1nsta11/pynuts.git`
2. Copy **utils** folder to your project
3. Install requirements into your project: `pip install -r requirements.txt`
4. Import necessary methods into your project: `from utils import cmd`
5. Use and enjoy

## Requirements

* Supported OS: Windows 7, 8, 10, 11 (x86 and x64)
* python v.3.8 and above
* python libs: psutil
* powershell v.5.0 and above


## Documentation

### cmd

Executes system commands and returns exit code

```python
from utils import cmd

error_level = cmd("net use", timeout=5, work_dir="")

if error_level != 0:
    exit()
```

### fops

Execute file operations in system

```python
from utils import fops

# returns version of a file
if not fops.version("C:\\Windows\\System32\\drivers\\my_driver.sys") == "1.0.1":
    assert False
    
# returns hash of a file (md5, sha1)
md5 = fops.file_hash("C:\\Windows\\System32\\drivers\\my_driver.sys", hash_type='md5')
sha1 = fops.file_hash("C:\\Windows\\System32\\drivers\\my_driver.sys", hash_type='sha1')
```

### proc

Library to work with processes

```python
from utils import proc

# returns is process running or not
proc.process_up("my_process.exe")

# returns list of processes which are running
proc.processes_up(["my_process", "another_proc.exe"])

# returns list or processes which are not running
proc.processes_down(["my_process", "another_proc.exe"])

# returns list of process pid`s
proc.processes_pid("my_process")

# returns num of process instances which are not running
proc.down_instances("my_process")

# returns num of process instances which are running
proc.up_instances("my_process")

# stop process
proc.stop_proc("my_process")

# returns true if pid exists
proc.pid_used(1234)
```

### pyftp


Good alternative for built-in python ftplib

```python
# NOTE: 
# supported following path formats for FTP destination:
# path/to/dir/on/ftp
# path\\to\\dir\\on\\ftp

from utils import PyFtp

# init connection
ftp = PyFtp(address="10.10.10.10", user="anonymous", password="anonymous")

# returns true if specified path exists
ftp.path_exists("path/to/folder/without/address")

# returns list of items in directory
ftp.dir_list("path/to/dir")

# returns true if path is actually a file
ftp.isfile("path/to/my/file/or/folder")

# downloads file to a location and create destination dir if it does not exist
ftp.download_file("path/to/my/file.txt", "C:\\temp")

# downloads directory content if it is a file and create destination dir if it does not exist
ftp.download_content("path/to/dir/on/ftp", "C:\\temp")

# upload a file on ftp, does not create destination path
ftp.upload_file("C:\\temp\\my_file.txt", "path/to/dir/on/ftp")

# creates directory tree if it does not exist or partially exists
ftp.mk_tree("path/would/like/to/have")
```

### regedit 

Library to work with Windows OS registry - alternative for python winreg

```python
"""
NOTE: ROOT key formats have to be expanded:
"HKEY_CLASSES_ROOT", 
"HKEY_CURRENT_USER", 
"HKEY_LOCAL_MACHINE", 
"HKEY_USERS", 
"HKEY_CURRENT_CONFIG"
"""
from utils import regedit

# returns list of sub-keys in specified key, recursively by default
regedit.key_list("HKEY_LOCAL_MACHINE\\Wow6432Node\\SOFTWARE", recurse=True)

# returns list of values in specified key 
regedit.values_list("HKEY_LOCAL_MACHINE\\Wow6432Node\\SOFTWARE\\MyOwnKey")

# returns data content for specified key and value as string 
regedit.value_data("HKEY_LOCAL_MACHINE\\Wow6432Node\\SOFTWARE\\MyOwnKey", "myOwnValue")

# delete key and returns true if success else false
regedit.del_key("HKEY_LOCAL_MACHINE\\Wow6432Node\\SOFTWARE\\MyOwnKey")

# delete value in a key and returns true if success else false 
regedit.del_value("HKEY_LOCAL_MACHINE\\Wow6432Node\\SOFTWARE\\MyOwnKey", "valueToDelete")

# create value with data in specified key then returns true if success else false
regedit.set_value("HKEY_LOCAL_MACHINE\\Wow6432Node\\SOFTWARE\\myNewKey", "myNewValue", "myData", reg_type=None)

# returns true if key exists else false
regedit.key_exists("HKEY_LOCAL_MACHINE\\Wow6432Node\\SOFTWARE\\myNewKey")
```

### smb

Library to connect PC to a SMB file share (Windows)

```python
from utils import smb

# mount network drive and return true if success
smb.mount("\\computer\\shared_folder", local_path='', login=None, password=None, attempts=3)

# unmount all mounted drives and return true if success
smb.unmount()
```

### svc

Library to work with Windows services - stop, change startup type, request service property

```python
from utils import svc

service = "MyService"

# returns service property in dictionary format
svc.as_dict(service)

# stop service, return true if success else false
svc.stop_service(service)

# returns true if service property is 'CanShutDown'
svc.can_shutdown(service)

# returns true if service property is 'CanPauseAndContinue' (PAUSABLE)
svc.can_pause(service)

# returns true if service property is 'CanStop' (STOPPABLE)
svc.can_stop(service)

# set startup type: if manual=True -> change to manual else automatic
svc.set_startup(service, option="manual") # allowed: "auto" and "disable"
```

### tsch

Task Scheduler wrapper for Windows OS

```python
from utils import tsch

task = "MyNewTask"

# returns true if task exists in Task Scheduler
tsch.exists(task)

# crate task and returns true if task was created successful
tsch.create(task, "ping 8.8.8.8", args='', work_dir='', privileges=True)

# run task and returns true if task was created successful
tsch.run(task)

# end task and returns true if task was created successful
tsch.end(task)

# disable task and returns true if task was created successful
tsch.disable(task)

# enable task and returns true if task was created successful
tsch.enable(task)
```