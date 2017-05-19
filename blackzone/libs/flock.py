import fcntl
import os
import struct


# maybe block when file is busy
def open_l(name, mode='r', buffering=-1):
    fp = file(name, mode, buffering)
    flag = fcntl.F_RDLCK
    if 'w' in fp.mode or 'a' in fp.mode or '+' in fp.mode:
        flag = fcntl.F_WRLCK
    fmt = 'hhiii'
    wlock_all = struct.pack(fmt, flag, os.SEEK_SET, 0, 0, 0)
    fcntl.fcntl(fp, fcntl.F_SETLKW, wlock_all)
    return fp
