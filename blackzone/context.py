import random


class context(object):
    def __init__(self):
        pass
    cwd = "/home/explorer/mycontainer/"
    runc = "/home/explorer/project/blackzone/runc"

    @staticmethod
    def get_noise():
        return str(random.random())
