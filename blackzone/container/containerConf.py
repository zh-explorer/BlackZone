# coding=utf-8
from ..libs import DataDict


class ContainerConfig(object):
    """
    保存配置文件元数据
    """
    config = DataDict()

    def __init__(self):
        self.config.ociVersion = "1.0.0-rc5"
        self.config.hostname = "runc"
        self.set_platform()
        self.set_process()
        self.set_root()
        self.set_mounts()
        self.set_linux()

    def set_platform(self):
        self.config.platform = {}

        platform = self.config.platform
        platform.os = "linux"
        platform.arch = "amd64"

    def set_process(self):
        self.config.process = {}
        process = self.config.process

        process.terminal = False
        process.consoleSize = {"height": 0, "width": 0}
        process.user = {"uid": 0, "gid": 0}
        process.args = ["sh"]
        process.env = ["PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", "TERM=xterm"]
        process.cwd = "/"
        process.capabilities = {}

        capabilities = process.capabilities
        capabilities.bounding = ["CAP_AUDIT_WRITE",
                                 "CAP_KILL",
                                 "CAP_NET_BIND_SERVICE"]
        capabilities.effective = ["CAP_AUDIT_WRITE",
                                  "CAP_KILL",
                                  "CAP_NET_BIND_SERVICE"]
        capabilities.inheritable = ["CAP_AUDIT_WRITE",
                                    "CAP_KILL",
                                    "CAP_NET_BIND_SERVICE"]
        capabilities.permitted = ["CAP_AUDIT_WRITE",
                                  "CAP_KILL",
                                  "CAP_NET_BIND_SERVICE"]
        capabilities.ambient = ["CAP_AUDIT_WRITE",
                                "CAP_KILL",
                                "CAP_NET_BIND_SERVICE"]

        process.rlimits = []
        process.rlimits += {
            "type": "RLIMIT_NOFILE",
            "hard": 1024,
            "soft": 1024
        }

        process.noNewPrivileges = True

    def set_root(self):
        self.config.root = {}
        root = self.config.root

        root.path = "rootfs"
        # use aufs to instead
        # root.readonly = True

    def set_mounts(self):
        self.config.mounts = []
        mounts = self.config.mounts

        mounts += {
            "destination": "/proc",
            "type": "proc",
            "source": "proc"
        }
        mounts += {
            "destination": "/dev",
            "type": "tmpfs",
            "source": "tmpfs",
            "options": [
                "nosuid",
                "strictatime",
                "mode=755",
                "size=65536k"
            ]
        }
        mounts += {
            "destination": "/dev/pts",
            "type": "devpts",
            "source": "devpts",
            "options": [
                "nosuid",
                "noexec",
                "newinstance",
                "ptmxmode=0666",
                "mode=0620",
                "gid=5"
            ]
        }
        mounts += {
            "destination": "/dev/shm",
            "type": "tmpfs",
            "source": "shm",
            "options": [
                "nosuid",
                "noexec",
                "nodev",
                "mode=1777",
                "size=65536k"
            ]
        }
        mounts += {
            "destination": "/dev/mqueue",
            "type": "mqueue",
            "source": "mqueue",
            "options": [
                "nosuid",
                "noexec",
                "nodev"
            ]
        }
        mounts += {
            "destination": "/sys",
            "type": "sysfs",
            "source": "sysfs",
            "options": [
                "nosuid",
                "noexec",
                "nodev",
                "ro"
            ]
        }
        mounts += {
            "destination": "/sys/fs/cgroup",
            "type": "cgroup",
            "source": "cgroup",
            "options": [
                "nosuid",
                "noexec",
                "nodev",
                "relatime",
                "ro"
            ]
        }

    def set_linux(self):
        self.config.linux = {}
        linux = self.config.linux

        linux.resources = {}
        linux.resources.devices = []
        linux.resources.devices += {
            "allow": False,
            "access": "rwm"
        }

        linux.namespaces = []
        linux.namespaces += {
            "type": "pid"
        }
        linux.namespaces += {
            "type": "network"
        }
        linux.namespaces += {
            "type": "ipc"
        }
        linux.namespaces += {
            "type": "uts"
        }
        linux.namespaces += {
            "type": "mount"
        }

        linux.maskedPaths = [
            "/proc/kcore",
            "/proc/latency_stats",
            "/proc/timer_list",
            "/proc/timer_stats",
            "/proc/sched_debug",
            "/sys/firmware"
        ]

        linux.readonlyPaths = [
            "/proc/asound",
            "/proc/bus",
            "/proc/fs",
            "/proc/irq",
            "/proc/sys",
            "/proc/sysrq-trigger"
        ]

    def to_json(self):
        return self.config.to_json()