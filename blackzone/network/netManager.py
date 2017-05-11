from pyroute2 import IPDB
from pyroute2 import IPRoute
from pyroute2 import netns
from ..context import context
import os
import ConfigParser


class NetManager(object):
    def __init__(self):
        main_conf_path = os.path.join(context.cwd, "netconf", "main.config")
        conf = ConfigParser.SafeConfigParser()
        conf.read(main_conf_path)
        self.bridge_name = conf.get('bridge', 'name')
        self.bridge_ip = conf.get('bridge', 'ip')

    # it should be find to use contain_id as net namespace name.
    def create_ns(self, ns_name):
        self.ns_name = ns_name
        netns.create(self.ns_name)

    def get_ns(self):
        pass