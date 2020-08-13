# encoding: utf-8

from abc import ABC
from functools import wraps
from inspect import getcallargs
from typing import Any, List, Dict


class ValidationItem(ABC):
    def __init__(self, *, name: str, message: str):
        self._name = name
        self._message = message

    def validate(self) -> bool:
        pass


class Vali:
    def __init__(self, func, vali_list: List[ValidationItem]):
        self.__func = func
        self.__vali_list = vali_list

    def __call__(self, *args: Any, **kwargs: Any):
        self._validate(getcallargs(self.__func, *args, **kwargs))
        return self.__func(*args, **kwargs)

    def _validate(self, call_args: Dict[str, Any]):
        for vali_item in self.__vali_list:
            if vali_item.validate(call_args.get(vali_item._name)) == False:
                raise ValiFailError(vali_item._message)

def validator(cls=Vali, *, vali_list: List[ValidationItem]):
    def outer(f):
        c = cls(f, vali_list)
        @wraps(f)
        def wrappers(*args, **kwargs):
            return c(*args, **kwargs)
        return wrappers
    return outer

class ValiFailError(Exception):
    def __init__(self, message):
        self.message = message