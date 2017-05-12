from pyroute2 import IPDB
from pyroute2 import IPRoute
from ..context import context
import ConfigParser
import os


# TODO need iptables
def net_init(bridge_name="blackzone0", ip_addr="172.20.0.1/16"):
    pid = os.getuid()
    if pid != 0:
        raise OSError("Permission denied: please use root")

    ipdb = IPDB()
    ipr = IPRoute()

    # delete old bridge
    main_conf_path = os.path.join(context.cwd, "netconf", "main.config")
    ns_conf_path = os.path.join(context.cwd, "netconf", "namespace.config")
    # TODO need clean ns

    main_conf = ConfigParser.SafeConfigParser()
    main_conf.read(main_conf_path)
    if main_conf.has_section('bridge'):
        if main_conf.has_option('bridge', 'name'):
            old_name = main_conf.get('bridge', 'name')
            dev = ipr.link_lookup(ifname=old_name)
            if len(dev) > 0:
                dev = dev[0]
                ipr.link('del', index=dev)

    main_bridge = ipr.link_lookup(ifname=bridge_name)

    # has contention between check and create. but not have good idea to solve
    if len(main_bridge) == 0:
        ipdb.create(kind="bridge", ifname=bridge_name)
        ipdb.commit()

    # contention two
    ipdb.commit()  # reload info
    try:
        if ipdb.interfaces[bridge_name].kind != "bridge":
            raise OSError("the bridge name is exist", bridge_name)
    except KeyError:
        raise OSError("This should not happen except contention, just retry")

    # set bridge ip and up. The route should be add automatic
    with ipdb.interfaces[bridge_name] as br:
        br.down()

    with ipdb.interfaces[bridge_name] as br:
        br.add_ip(ip_addr)
        br.up()

    conf_dir = os.path.join(context.cwd, "netconf")

    if not os.path.exists(conf_dir):
        os.mkdir(conf_dir)
    elif not os.path.isdir(conf_dir):
        raise OSError("netconf is not exists", conf_dir)

    main_conf = ConfigParser.SafeConfigParser()
    main_conf.add_section("bridge")
    main_conf.set("bridge", "name", bridge_name)
    main_conf.set("bridge", "ip", ip_addr)
    main_conf_fp = file(main_conf_path, 'w')
    main_conf.write(main_conf_fp)
    main_conf_fp.close()

    ns_conf = ConfigParser.SafeConfigParser({"bridge name": bridge_name, "bridge ip": ip_addr})
    nc_conf_fp = file(ns_conf_path, 'w')
    ns_conf.write(nc_conf_fp)
    nc_conf_fp.close()
