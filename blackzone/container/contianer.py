# coding=utf-8
import os
import time
# import subprocess
# import select
from hashlib import sha256
from ..tubes.process import Process
import socket
from ..context import context
from .containerConf import ContainerConfig
from .fsManager import FsManager
from ..network import NetManager
from ..tubes import Sock


class Container(object):
    def __init__(self, image_id, ns=None):
        # TODO 持久化保存
        self.image_id = image_id
        self.ns = ns

        # not make container_id by itself, the sha method may be useless
        self.container_id = self.sha(str(time.time()) + context.get_noise())
        # self.container_id = container_id

        self.fs = FsManager(self.image_id, self.container_id)
        if isinstance(self.ns, NetManager):
            name = self.ns.ns_name
        else:
            name = self.ns
        self.config = ContainerConfig(ns_name=name)
        self.create_config_file()

    def create_config_file(self):
        config = self.config.to_json()
        self.config_path = os.path.join(self.fs.container_dir, 'config.json')
        fp = open(self.config_path, 'w')
        fp.write(config)
        fp.close()

    def start(self):
        self.fs.mount_aufs()
        os.chdir(self.fs.container_dir)
        # TODO new branch
        # os.system('%s run -b %s %s'%(context.runc, self.fs.container_dir, self.container_id))
        # os.execv(context.runc, ["runc", "run", "-b", self.fs.container_dir, self.container_id])
        self.process =  Process([context.runc, "run", "-b", self.fs.container_dir, self.container_id])

    def clean(self):
        os.chdir('/')
        self.fs.clean_container()

    def connect_sock(self):
        s = socket.socket()
        s.connect(('121.42.25.113', 20000))
        s = Sock(s)
        self.process.connect_both(s)

    @staticmethod
    def sha(data):
        return sha256(data).hexdigest()
