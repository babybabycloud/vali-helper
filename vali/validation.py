# encoding: utf-8

from abc import ABC
from functools import wraps
from inspect import getcallargs
from typing import Any, Dict, Generic, List, NewType, TypeVar


T = TypeVar('T')


class ValidationItem(ABC):
    def __init__(self, *, name: str, message: str, value: Generic[T]):
        self._name = name
        self._message = message
        self.value = value

    def validate(self, vali_value: Generic[T]) -> bool:
        pass


ValiItems = NewType('ValiItems', List[ValidationItem])


class Vali:
    def __init__(self, func, vali_list: ValiItems):
        self.__func = func
        self.__vali_list = vali_list

    def __call__(self, *args: Any, **kwargs: Any):
        self._validate(getcallargs(self.__func, *args, **kwargs))
        return self.__func(*args, **kwargs)

    def _validate(self, call_args: Dict[str, Any]):
        for vali_item in self.__vali_list:
            if vali_item.validate(call_args.get(vali_item._name)) == False:
                raise ValiFailError(vali_item._message.format(vali_item.value))


def validator(cls=Vali, *, vali_list: ValiItems):
    def outer(f):
        c = cls(f, vali_list)
        @wraps(f)
        def wrappers(*args, **kwargs):
            return c(*args, **kwargs)
        return wrappers
    return outer


class ValiProp:
    def __init__(self, vali_list: ValiItems):
        self._name = str(id(self))
        self.__vali_list = vali_list

    def __get__(self, instance: Any, owner: Any):
        if instance is None:
            return self
        return instance.__dict__.get(self._name)

    def __set__(self, instance: Any, value: Any):
        for vali in self.__vali_list:
            if vali.validate(value) == False:
                raise ValiFailError(vali._message.format(vali.value))

        if instance is None:
            type(instance).__dict__[self._name] = value
        else:
            instance.__dict__[self._name] = value


class ValiFailError(Exception):
    def __init__(self, message):
        self.message = message
