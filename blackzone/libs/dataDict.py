# coding=utf-8
from collections import MutableMapping
from json import dumps
import dataList


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
            self.__dict__[key] = dataList.DataList(value)
        else:
            self.__dict__[key] = value

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if isinstance(value, self.__class__):
                d[key] = value.to_dict()
            elif isinstance(value, dataList.DataList):
                d[key] = value.to_list()
            else:
                d[key] = value
        return d

    def to_json(self):
        return dumps(self.to_dict())

    def _check(self, key, value):
        # TODO 需要对添加对象的检查
        pass
