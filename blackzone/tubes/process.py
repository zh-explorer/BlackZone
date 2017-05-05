import pty

from tube import Tube
import subprocess
import os


class PTY(object): pass


PTY = PTY()


class Process(Tube):
    def __init__(self, args, bufsize=0, executable=None, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None,
                 universal_newlines=False, startupinfo=None, creationflags=0):
        Tube.__init__(self)

        self.proc = subprocess.Popen(args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds,
                                     shell, cwd, env, universal_newlines, startupinfo, creationflags)

        self.stdin = self.proc.stdin
        self.stdout = self.proc.stdout
        self.stderr = self.stdout if stderr == subprocess.STDOUT else self.proc.stderr
        self.unblock_tube()

    # TODO is a big problem of term, I will do it later
    # def __init__(self, args, bufsize=0, executable=None, stdin=subprocess.PIPE, stdout=PTY,
    #              stderr=subprocess.STDOUT, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None,
    #              universal_newlines=False, startupinfo=None, creationflags=0):
    #     Tube.__init__(self)
    #     self.user_preexec_fn = preexec_fn
    #     handles = (stdin, stdout, stderr)
    #     self.pty = handles.index(PTY) if PTY in handles else None
    #
    #     master, slave = pty.openpty()
    #     self.slave = slave
    #     if self.pty is not None:
    #         if stdin == PTY:
    #             stdin = slave
    #         if stdout == PTY:
    #             stdout = slave
    #         if stderr == PTY:
    #             stderr = slave
    #
    #     self.proc = subprocess.Popen(args, bufsize, executable, stdin, stdout, stderr, self.__preexec_fn, close_fds,
    #                                  shell, cwd, env, universal_newlines, startupinfo, creationflags)
    #
    #     if self.pty is not None:
    #         if stdin is slave:
    #             self.stdin = os.fdopen(os.dup(master), 'r+')
    #         else:
    #             self.stdin = self.proc.stdin
    #         if stdout is slave:
    #             self.stdout = os.fdopen(os.dup(master), 'r+')
    #         else:
    #             self.stdout = self.proc.stdout
    #         if stderr is slave:
    #             self.stderr = os.fdopen(os.dup(master), 'r+')
    #         else:
    #             # set stderr to stdout if necessary
    #             self.stderr = self.stdout if stderr == subprocess.STDOUT else self.proc.stderr
    #     os.close(master)
    #     os.close(slave)
    #     self.unblock_tube()
    #
    # def __preexec_fn(self):
    #     if self.pty is not None:
    #         self.__pty_make_controlling_tty(self.pty)
    #     if self.user_preexec_fn is not None:
    #         self.user_preexec_fn()

    def poll(self):
        return self.proc.poll()

    def read(self):
        data = ''
        if self.poll() is not None:
            return data
        while True:
            try:
                d = self.stdout.read()
                if d == '':
                    break
                data += d
            except IOError, e:
                if e.errno == os.errno.EAGAIN:
                    break
                else:
                    raise IOError(e)
        if data == '':
            self.close()
        return data

    def write(self, data):
        if self.poll() is not None:
            return -1
        try:
            self.stdin.write(data)
            self.stdin.flush()
        except IOError, e:
            if e.errno == os.errno.EPIPE:
                self.close()
                return -1
            else:
                raise IOError(e)
        return 0

    def close(self):
        try:
            self.proc.kill()
        except OSError, e:
            if e.errno != os.errno.ESRCH:
                raise OSError(e)
        self.proc.wait()

    # def __pty_make_controlling_tty(self, tty_fd):  # come from pwntools :)
    #     '''This makes the pseudo-terminal the controlling tty. This should be
    #             more portable than the pty.fork() function. Specifically, this should
    #             work on Solaris. '''
    #
    #     child_name = os.ttyname(tty_fd)
    #
    #     # Disconnect from controlling tty. Harmless if not already connected.
    #     try:
    #         fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
    #         if fd >= 0:
    #             os.close(fd)
    #     # which exception, shouldnt' we catch explicitly .. ?
    #     except OSError:
    #         # Already disconnected. This happens if running inside cron.
    #         pass
    #
    #     os.setsid()
    #
    #     # Verify we are disconnected from controlling tty
    #     # by attempting to open it again.
    #     try:
    #         fd = os.open("/dev/tty", os.O_RDWR | os.O_NOCTTY)
    #         if fd >= 0:
    #             os.close(fd)
    #             raise Exception('Failed to disconnect from ' +
    #                             'controlling tty. It is still possible to open /dev/tty.')
    #     # which exception, shouldnt' we catch explicitly .. ?
    #     except OSError:
    #         # Good! We are disconnected from a controlling tty.
    #         pass
    #
    #     # Verify we can open child pty.
    #     fd = os.open(child_name, os.O_RDWR)
    #     if fd < 0:
    #         raise Exception("Could not open child pty, " + child_name)
    #     else:
    #         os.close(fd)
    #
    #     # Verify we now have a controlling tty.
    #     fd = os.open("/dev/tty", os.O_WRONLY)
    #     if fd < 0:
    #         raise Exception("Could not open controlling tty, /dev/tty")
    #     else:
    #         os.close(fd)
    #     pass
