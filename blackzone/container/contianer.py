# coding=utf-8
import os
import time
# import subprocess
# import select
from hashlib import sha256
from ..tubes.process import Process

from ..context import context
from .containerConf import ContainerConfig
from .fsManager import FsManager


class Container(object):
    def __init__(self, image_id, container_id, ns=None):
        # TODO 持久化保存
        self.image_id = image_id
        self.ns = ns

        # not make container_id by itself, the sha method may be useless
        # self.container_id = self.sha(str(time.time()) + context.get_noise())
        self.container_id = container_id

        self.fs = FsManager(self.image_id, self.container_id)
        self.config = ContainerConfig(ns_name=self.ns)
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
        return Process([context.runc, "run", "-b", self.fs.container_dir, self.container_id])

    def clean(self):
        os.chdir('/')
        self.fs.clean_container()

    @staticmethod
    def sha(data):
        return sha256(data).hexdigest()
