# coding=utf-8
from collections import MutableSequence
import dataDict


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
            self.__list__[key] = dataDict.DataDict(value)
        else:
            self.__list__[key] = value

    def _check_add(self, value):
        self._check(value)
        if isinstance(value, list):
            self.__list__.append(self.__class__(value))
        elif isinstance(value, dict):
            self.__list__.append(dataDict.DataDict(value))
        else:
            self.__list__.append(value)

    def to_list(self):
        d = []
        for i in self:
            if isinstance(i, dataDict.DataDict):
                d.append(i.to_dict())
            elif isinstance(i, self.__class__):
                d.append(i.to_list())
            else:
                d.append(i)

    def _check(self, value):
        # TODO 需要对添加对象的检查
        pass
