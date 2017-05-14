from pyroute2 import IPDB
from pyroute2 import IPRoute
from pyroute2 import NetNS
from ..context import context
import os
import ConfigParser
from ..libs import open_l
from hashlib import sha256
import time


# TODO port forward
class NetManager(object):
    def __init__(self):
        main_conf_path = os.path.join(context.cwd, "netconf", "main.config")
        self.ns_conf_path = os.path.join(context.cwd, "netconf", "namespace.config")

        conf = ConfigParser.SafeConfigParser()
        conf.read(main_conf_path)
        self.bridge_name = conf.get('bridge', 'name')
        self.bridge_ip = conf.get('bridge', 'ip')

        # must lock free conf first
        ns_fp = open_l(self.ns_conf_path, 'r+')
        conf = ConfigParser.SafeConfigParser()
        conf.readfp(ns_fp)
        self.get_ns(conf)

        ns_fp.seek(0)
        ns_fp.truncate()
        conf.write(ns_fp)
        ns_fp.close()

    def get_ns(self, conf):
        self.ns_name = self.get_exists_ns(conf)
        if self.ns_name is None:
            self.create_new_ns(conf)

    def create_new_ns(self, conf):
        # TODO need recheck
        self.veth_name = self.random_ns_name()
        self.ns_name = self.veth_name
        ipdb = IPDB()
        ipdb2 = IPDB(nl=NetNS(self.ns_name))
        ipdb.commit()
        ipdb2.commit()


        # create veth part
        ipdb.create(ifname=self.veth_name, kind='veth', peer='veth0').commit()

        # add veth to bridge and up
        with ipdb.interfaces[self.bridge_name] as br:
            br.add_port(self.veth_name)

        with ipdb.interfaces[self.veth_name] as i:
            i.up()

        # add to peer to ns
        with ipdb.interfaces['veth0'] as i:
            i.net_ns_fd = self.ns_name

        # set peer address and up
        self.veth_ip = self.get_ip(conf)

        ipdb2 = IPDB(nl=NetNS(self.ns_name))
        ipdb2.commit()
        with ipdb2.interfaces['veth0'] as i:
            i.add_ip(self.veth_ip)
            i.up()

        with ipdb2.interfaces['lo'] as i:
            i.up()

        # add route
        # ipdb2.routes.add(dst='0.0.0.0/0', gateway=self.bridge_ip.split('/')[0],
        #                 oif=ipdb2.interfaces['veth0'].index).commit()
        ns = NetNS(self.ns_name)
        ns.route("add", dst='0.0.0.0', mask=0, gateway =self.bridge_ip.split('/')[0], oif=ns.link_lookup(ifname='veth0'))

        conf.add_section(self.veth_ip)
        conf.set(self.veth_ip, "veth name", self.veth_name)
        conf.set(self.veth_ip, "ns name", self.ns_name)
        conf.set(self.veth_ip, "in use", "true")

    def release(self):
        # TODO need clean when has too much free ns
        # just set in use to false
        ns_fp = open_l(self.ns_conf_path, "r+")
        conf = ConfigParser.SafeConfigParser()
        conf.readfp(ns_fp)
        conf.set(self.veth_ip, 'in use', 'false')

        ns_fp.seek(0)
        ns_fp.truncate()
        conf.write(ns_fp)

    def get_exists_ns(self, conf):
        # find a free ns
        for section in conf.sections():
            if not conf.getboolean(section, "in use"):
                self.veth_ip = section
                self.veth_name = conf.get(section, 'veth name')
                conf.set(section, "in use", "true")
                return conf.get(section, "ns name")
        # not find
        return None

    def random_ns_name(self):
        name = str(time.time()) + context.get_noise()
        return sha256(name).hexdigest()[:10]

    def get_ip(self, conf):
        sections = conf.sections()
        for i in xrange(0, 256):
            for j in xrange(2, 256):
                ip_zone = self.bridge_ip.split('.')[:2]
                ip = ip_zone[0] + '.' + ip_zone[1] + '.' + str(i) + '.' + str(j) + '/16'
                if ip not in sections:
                    return ip
