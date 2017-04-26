from ..libs.dataDict import DataDict


class ContainerConfig(object):
    config = DataDict()

    def __init__(self):
        self.config.ociVersion = "1.0.0-rc5"
        self.set_platform()

    def set_platform(self):
        self.config.platform = {}

        platform = self.config.platform
        platform.os = "linux"
        platform.arch = "amd64"

    def set_process(self):
        self.config.process = {}
        process = self.config.process

        process.terminal = True
        process.consoleSize = {"height": 0, "width": 0}
        process.user = {"uid": 0, "gid": 0}
        process.args = []