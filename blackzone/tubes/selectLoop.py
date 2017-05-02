import select
import threading


# TODO thread security
class SelectLoop(threading.Thread):
    def __init__(self, *args):
        threading.Thread.__init__(self)
        self.stdin_dict = {}
        self.stderr_dict = {}
        for tube in args:
            self.stdin_dict[tube.stdout] = tube

    def run(self):
        while True:
            if len(self.stdin_dict) == 0:
                break
            rlist, wlist, xlist = select.select(self.stdin_dict.keys(), [], [], 1)
            for fp in rlist:
                tube = self.stdin_dict[fp]
                data = tube.read()
                if data == "":
                    del self.stdin_dict[fp]
                result = tube.other.write(data)
                if result != 0:
                    tube.close()
                    del self.stdin_dict[fp]