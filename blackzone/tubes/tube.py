import fcntl
import os
from abc import abstractmethod
from selectLoop import SelectLoop


# TODO The tube is not well design. need rewrite
class Tube(object):
    def __init__(self):
        self.stdin = None
        self.stdout = None
        self.stderr = None
        self.other = None
        self.poll_code = None
        self.log = None

    def connect_to(self, other):
        self.other = other
        s = SelectLoop(self)
        s.start()

    def poll(self):
        return self.poll_code

    def connect_both(self, other):
        self.connect_to(other)
        other.connect_to(self)

    def set_log(self, log):
        # TODO need default
        self.log = log

    @abstractmethod
    def read(self):
        raise NameError("call abstractmethod: ", self.__class__)

    @abstractmethod
    def write(self, data):
        raise NameError("call abstractmethod: ", self.__class__)

    @abstractmethod
    def close(self):
        raise NameError("call abstractmethod: ", self.__class__)

    def unblock_tube(self):
        self.set_unblock(self.stdin)
        self.set_unblock(self.stdout)
        self.set_unblock(self.stderr)

    def set_unblock(self, fp):
        flag = fcntl.fcntl(fp, fcntl.F_GETFL)
        result = fcntl.fcntl(fp, fcntl.F_SETFL, flag | os.O_NONBLOCK)
        if result != 0:
            raise IOError("cat not set unblock pipe", fp)
