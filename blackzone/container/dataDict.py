# coding=utf-8
from collections import MutableMapping


class DataDict(MutableMapping):
    """
    内部存放config元数据的类
    """
    def __init__(self, **kw):
        self.__dict__ = kw

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __setitem__(self, key, value):
        #TODO 需要对添加对象的检查
        self.__dict__[key] = value

    def keys(self):
        return self.__dict__.keys()

    def __len__(self):
        return len(self.__dict__)

    def __contains__(self, value):
        return value in self.__dict__

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__dict__ == other.__dict__

    def copy(self):
        return self.__class__(**self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, repr(self.__dict__))

    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.__dict__))