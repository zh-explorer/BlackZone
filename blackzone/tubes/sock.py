import socket
from os import errno
from tube import Tube


class Sock(Tube):
    def __init__(self, s):
        Tube.__init__(self)
        self.sock = s
        self.stdin = s
        self.stdout = s
        self.stderr = s
        self.unblock_tube()

    def read(self):
        data = ''
        if self.poll() is not None:
            return data
        while True:
            try:
                d = self.stdout.recv(1024)
                if d == '':
                    break
                data += d
            except IOError, e:
                if e.errno == errno.EAGAIN:
                    break
                else:
                    raise IOError(e)
        if data == '':
            self.sock.close()
            self.poll_code = 0
        return data

    def write(self, data):
        if self.poll() is not None:
            return -1
        try:
            self.stdin.send(data)
        except IOError, e:
            if e.errno == errno.EPIPE:
                self.sock.close()
                self.poll_code = 0
                return -1
            else:
                raise IOError(e)
        return 0

    def close(self):
        self.poll_code = 0
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except IOError, e:
            if e.errno != socket.EBADF:
                raise IOError(e)
        self.sock.close()

