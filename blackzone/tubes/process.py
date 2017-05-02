from tube import Tube
import subprocess
from os import errno


class Process(Tube):
    def __init__(self, args, bufsize=0, executable=None, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT, preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None,
                 universal_newlines=False, startupinfo=None, creationflags=0):
        Tube.__init__(self)
        self.proc = subprocess.Popen(args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell,
                                     cwd, env, universal_newlines, startupinfo, creationflags)
        self.stdin = self.proc.stdin
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stdout
        self.unblock_tube()

    def poll(self):
        return self.proc.poll()

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
            self.proc.kill()
        return data

    def read_err(self):
        data = ''
        while True:
            try:
                d = self.stderr.read()
                if d == '':
                    break
                data += d
            except IOError, e:
                if e.errno == errno.EAGAIN:
                    break
                else:
                    raise IOError(e)
        if data == '':
            self.proc.kill()
        return data

    def write(self, data):
        try:
            self.stdin.write(data)
            self.stdin.flush()
        except IOError, e:
            if e.errno == errno.EPIPE:
                self.proc.kill()
                return -1
            else:
                raise IOError(e)
        return 0

    def close(self):
        self.proc.kill()
