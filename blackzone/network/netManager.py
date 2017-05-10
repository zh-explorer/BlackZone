from pyroute2 import IPDB
from pyroute2 import IPRoute
import os


class NetManager(object):
    def __init__(self, bridge_name="blackzone0", ip="172.20.0.1", mask=16):
        pid = os.getpid()
        if pid != 0:
            raise OSError("Permission denied: please use root")
        ipdb = IPDB()
        ip = IPRoute()
        main_bridge = ip.lonk_lookup(ifname=bridge_name)

        # has contention between check and create. but not have good idea to solve
        if len(main_bridge) == 0:
            ipdb.create(kind="bridge", ifname=bridge_name)
            ipdb.commit()

        # contention two
        ipdb.commit()     # reload info
        try:
            if ipdb[bridge_name].kind == "bridge":
                raise OSError("the bridge name is exist", bridge_name)
        except KeyError:
            raise OSError("This should not happen except contention, just retry")
