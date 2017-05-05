# coding=utf-8
from collections import MutableMapping, MutableSequence
from json import dumps


class DataDict(MutableMapping):
    """
    内部存放config元数据的类
    类似字典,可以和字典混用。但是可以使用点调用取值与赋值的字典.并且可以嵌套赋值。
    >>> a = DataDict()
    >>> a.a = 3
    >>> a.b = {"a":1,"b":2}
    >>> a.b.c = 123
    >>> a
    {'a': 3, 'b': {'a': 1, 'c': 123, 'b': 2}}
    """

    def __init__(self, *args, **kwargs):
        for d in args:
            if not isinstance(d, dict):
                raise KeyError
            for key, value in d.items():
                self._check_set(key, value)
        for key, value in kwargs.items():
            self._check_set(key, value)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __setitem__(self, key, value):
        self._check_set(key, value)

    def __setattr__(self, key, value):
        self[key] = value

    def keys(self):
        return self.__dict__.keys()

    def __len__(self):
        return len(self.__dict__)

    def update(self, other):
        if isinstance(other, self.__class__):
            raise ValueError
        self.__dict__.update(other)

    def __contains__(self, value):
        return value in self.__dict__

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self == other

    def copy(self):
        return self.__class__(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

        # def to_json(self):
        #     dumps(self.to_dict())

    def _check_set(self, key, value):
        self._check(key, value)
        if isinstance(value, dict):
            self.__dict__[key] = self.__class__(value)
        elif isinstance(value, list):
            self.__dict__[key] = DataList(value)
        else:
            self.__dict__[key] = value

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if isinstance(value, self.__class__):
                d[key] = value.to_dict()
            elif isinstance(value, DataList):
                d[key] = value.to_list()
            else:
                d[key] = value
        return d

    def to_json(self):
        return dumps(self.to_dict())

    def _check(self, key, value):
        check_type_dict = {
            "ociVersion":str,
            "prestart":list,
            "poststart":list,
            "poststop":list,
            "annotations":dict,
            "hostname":str,
            "mounts":list,
            "arch":str,
            "os":str,
            "path":str,
            "readonly":bool,
            "args":list,
            "height":long,
            "width":long,
            "cwd":str,
            "env":list,
            "terminal":bool,
            "uid":int,
            "gid":int,
            "additionalGids":list,
            "bounding": list,
            "permitted":list,
            "effective":list,
            "inheritable":list,
            "ambient":list,
            "apparmorProfile":str,
            "selinuxLabel":str,
            "noNewPrivileges":bool,
            "rlimits":list,
            "hard":long,
            "soft":long,
            "type":str,
            "devices":list,
            "uidMappings":list,
            "gidMappings":list,
            "namespaces":list,
            "devices":list,
            "oomScoreAdj":int,
            "limit":long,
            "blkioWeight":int,
            "blkioLeafWeight":int,
            "blkioThrottleReadBpsDevice":list,
            "blkioThrottleWriteBpsDevice":list,
            "blkioThrottleReadIopsDevice":list,
            "blkioThrottleWriteIopsDevice":list,
            "blkioWeightDevice":list,
            "cpus":str,
            "mems":str,
            "period":long,
            "quota":long,
            "realtimePeriod":long,
            "realtimeRuntime":long,
            "shares":long,
            "disableOOMKiller":bool,
            "hugepageLimits":list,
            "pageSize":str,
            "kernel":long,
            "kernelTCP":long,
            "reservation":long,
            "swap":long,
            "swappiness":long,
            "classID":int,
            "priorities":list,
            "cgroupsPath":str,
            "rootfsPropagation":str,
            "defaultAction":str,
            "architectures":list,
            "syscalls":list,
            "sysctl":dict,
            "maskedPaths":list,
            "readonlyPaths":list,
            "mountLabel":str
        }
        return isinstance(self.value,check_type_dict[self.key])


class DataList(MutableSequence):
    def __init__(self, iter=[]):
        self.__list__ = list()
        for value in iter:
            self._check_add(value)

    def __getitem__(self, item):
        return self.__list__[item]

    def __delitem__(self, key):
        del self.__list__[key]

    def __setitem__(self, key, value):
        self._check_set(key, value)

    def __add__(self, other):
        new_list = self.__class__(self)
        new_list += other
        return new_list

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        # change to a iter?
        if isinstance(other, list) or isinstance(other, self.__class__):
            for i in other:
                self._check_add(i)
        else:
            self._check_add(other)
        return self

    def __len__(self):
        return len(self.__list__)

    def insert(self, index, value):
        self.__list__.insert(index, None)
        self._check_set(index, value)

    def __eq__(self, other):
        if (not isinstance(other, list)) or (not isinstance(other, self.__class__)):
            return True
        if len(self) != len(other):
            return False
        for i, j in zip(self, other):
            if i != j:
                return False
        return True

    def __repr__(self):
        return repr(self.__list__)

    def __str__(self):
        return str(self.__list__)

    def __ne__(self, other):
        return not self == other

    def _check_set(self, key, value):
        self._check(value)
        if isinstance(value, list):
            self.__list__[key] = self.__class__(value)
        elif isinstance(value, dict):
            self.__list__[key] = DataDict(value)
        else:
            self.__list__[key] = value

    def _check_add(self, value):
        self._check(value)
        if isinstance(value, list):
            self.__list__.append(self.__class__(value))
        elif isinstance(value, dict):
            self.__list__.append(DataDict(value))
        else:
            self.__list__.append(value)

    def to_list(self):
        d = []
        for i in self:
            if isinstance(i, DataDict):
                d.append(i.to_dict())
            elif isinstance(i, self.__class__):
                d.append(i.to_list())
            else:
                d.append(i)
        return d

    def _check(self, value):
        # TODO 需要对添加对象的检查
        pass
