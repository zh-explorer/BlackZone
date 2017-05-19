from tube import Tube
from sys import stdin,stdout,stderr
from os import errno


class Stdio(Tube):
    def __init__(self):
        Tube.__init__(self)
        self.stdin = stdout
        self.stdout = stdin
        self.stderr = stderr
        self.unblock_tube()
        self.other = None

    def read(self):
        data = ''
        while True:
            try:
                d = self.stdout.read()
                if d == '':
                    break
                data += d
            except IOError, e:
                if e.errno == errno.EAGAIN:
                    break
                else:
                    raise IOError(e)
        if data == '':
            self.poll_code = 0
        return data

    def write(self, data):
        try:
            self.stdin.write(data)
            self.stdin.flush()
        except IOError, e:
            if e.errno == errno.EPIPE:
                self.poll_code = 0
                return -1
            else:
                raise IOError(e)
        return 0

    def set_log(self, log):
        # TODO
        pass

    def close(self):
        self.poll_code = 0
        self.stdin.close()
        self.stdout.close()
        self.stderr.close()
