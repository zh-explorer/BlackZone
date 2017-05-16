import multiprocessing
import types


class ProcessSynClass(object):
    class_object = None

    def __init__(self, *args, **kwargs):
        class_object = object.__getattribute__(self, "class_object")
        if class_object is None:
            raise SyntaxError("This class shouldn't be use direct")

        parent_conn, child_conn = multiprocessing.Pipe()
        object.__setattr__(self, "parent_conn", parent_conn)
        object.__setattr__(self, "child_conn", child_conn)

        do_syn = object.__getattribute__(self, "do_syn")
        p = multiprocessing.Process(target=do_syn, args=args, kwargs=kwargs)
        p.start()
        object.__setattr__(self, "p", p)

    def do_syn(self, *args, **kwargs):
        class_object = object.__getattribute__(self, "class_object")
        peer = object.__getattribute__(self, "child_conn")
        instance = class_object(*args, **kwargs)
        while True:
            cmd = peer.recv()
            print cmd
            if cmd == "end":
                break
            if cmd["func"] == "get":
                ret = instance.__getattribute__(cmd["item"])
                if isinstance(ret, types.MethodType):
                    peer.send("a func")
                    peer.send("true")
                else:
                    peer.send(ret)
                    if ret == "a func":
                        peer.send("false")
            elif cmd["func"] == "set":
                instance.__setattr__(cmd["key"], cmd["value"])
            elif cmd["func"] == "call":
                ret = getattr(instance, cmd["name"])(*cmd["args"], **cmd["kwargs"])
                if isinstance(ret, types.MethodType):
                    peer.send("a func")
                    peer.send("true")
                else:
                    peer.send(ret)
                    if ret == "a func":
                        peer.send("false")
            else:
                raise OSError("shouldn't be here")

    def __getattribute__(self, item):
        if item == "kill_the_subprocess":
            return object.__getattribute__(self, "kill_the_subprocess")
        parent = object.__getattribute__(self, "parent_conn")
        parent.send({"func": "get", "item": item})
        ret = parent.recv()
        if ret == "a func":
            flag = parent.recv()
            if flag == "true":
                def func(*args, **kwargs):
                    name = item
                    parent.send({"func": "call", "name": name, "args": args, "kwargs": kwargs})
                    return parent.recv()
                ret = func
        return ret

    def __setattr__(self, key, value):
        parent = object.__getattribute__(self, "parent_conn")
        parent.send({"func": "set", "key": key, "value": value})

    def kill_the_subprocess(self):
        parent = object.__getattribute__(self, "parent_conn")
        parent.send("end")

def get_process_syn(c):
    return type(c.__name__, (ProcessSynClass,), {"class_object": c})
