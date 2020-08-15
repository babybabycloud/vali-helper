# encoding: utf-8

import collections

from abc import ABC
from functools import wraps
from inspect import getcallargs
from typing import Any, Dict, Generic, Iterable, List, NewType, Tuple, TypeVar


__all__ = [
    'ValidationItem',
    'Vali',
    'validator',
    'ValiProp',
    'ValiFailError'
]

T = TypeVar('T')


class ValidationItem(ABC):
    """
    Validation item is the validation base class. 
    The subclass should implement the actual validate logic.
    """
    ERROR_MESSAGE_TEMPLATE = "The validation value must {} {}, but provided {}"
    def __init__(self, *, name: str, value: Generic[T]):
        """
        @param name: The name of the argument needed to be validated
        @param value: The value used to be compared 
        """
        self._name = name
        self.value = value

    def validate(self, vali_value: Generic[T]) -> Tuple[bool, str]:
        """
        @param vali_value: The value needed to be validated
        @return: A tuple
            The bool value indicates the result of the validation
            The string value is the error message for why validation failed.
        """
        pass


ValiItems = NewType('ValiItems', List[ValidationItem])


class Vali:
    """
        Validation framework base class
    """
    def __init__(self, func, valis: ValiItems):
        """
        @param func: The wrapped function
        @param valis: A list contains the main validation class instance
        """
        self.__func = func
        self.__valis = valis if isinstance(valis, collections.Iterable) else (valis,)

    def __call__(self, *args: Any, **kwargs: Any):
        self._validate(getcallargs(self.__func, *args, **kwargs))
        return self.__func(*args, **kwargs)

    def _validate(self, call_args: Dict[str, Any]):
        for vali_item in self.__valis:
            result, message = vali_item.validate(call_args.get(vali_item._name))
            if result == False:
                raise ValiFailError(message)


def validator(cls=Vali, *, valis: ValiItems):
    """
    The validation decorator, can be used to decorate a function
    
    @param cls: Vali or subclass of Vali.
    @param valis: A list contains the main validation class instance
    """
    def outer(f):
        c = cls(f, valis)
        @wraps(f)
        def wrappers(*args, **kwargs):
            return c(*args, **kwargs)
        return wrappers
    return outer


class ValiProp:
    """
        A descriptor for validating the class attribute
    """
    def __init__(self, valis: ValiItems):
        """
        @param valis: A list contains the main validation class instance
        """
        self._name = str(id(self))
        self.__valis = valis

    def __get__(self, instance: Any, owner: Any):
        if instance is None:
            return self
        return instance.__dict__.get(self._name)

    def __set__(self, instance: Any, value: Any):
        for vali in self.__valis:
            result, message = vali.validate(value) 
            if result == False:
                raise ValiFailError(message)

        if instance is None:
            type(instance).__dict__[self._name] = value
        else:
            instance.__dict__[self._name] = value


class ValiFailError(Exception):
    """
    The Exception would be raised when validation failed.
    """
    def __init__(self, message):
        self.message = message
