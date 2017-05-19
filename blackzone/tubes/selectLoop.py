import select
import threading
import os


# TODO thread security
class SelectLoop(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.stdin_dict = {}
        self.stderr_dict = {}
        for tube in args:
            self.stdin_dict[tube.stdout] = tube

    def run(self):
        # TODO epoll or poll is a better choose
        while True:
            if len(self.stdin_dict) == 0:
                break
            try:
                rlist, wlist, xlist = select.select(self.stdin_dict.keys(), [], [], 1)
            except IOError, e:
                if e.errno == os.errno.EBADF:
                    for fp in self.stdin_dict.keys():
                        if self.stdin_dict[fp].poll() is not None:
                            del self.stdin_dict[fp]
                else:
                    raise IOError(e)
                continue

            for fp in rlist:
                tube = self.stdin_dict[fp]
                data = tube.read()
                if data == "":
                    tube.other.close()          # TODO it seem's bad to close
                    del self.stdin_dict[fp]
                    continue
                result = tube.other.write(data)
                if result != 0:
                    tube.close()
                    del self.stdin_dict[fp]
                    continue
