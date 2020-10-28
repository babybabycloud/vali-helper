# encoding: utf-8

import collections

from abc import ABC
from functools import wraps
from inspect import getcallargs
from typing import Any, Dict, Generic, List, NewType, Tuple, TypeVar


__all__ = [
    'ValidationItem',
    'Vali',
    'validator',
    'ValiProp',
    'ValiFailError'
]

T = TypeVar('T')

class ValiResult:
    result: bool = False
    message: str = None

    def __init__(self, result: bool, message: str):
        if not result:
            self.message = message
        self.result = result


class ValidationMeta(type):
    """
    metaclasss for ValidationItem.
    Checking if the subclass of ValidationItem implements test method and ERROR_MESSAGE attribute.
    """
    def __new__(mcls, *args, **kwargs):
        cls = super().__new__(mcls, *args, **kwargs)
        keys_ = cls.__dict__.keys()
        if cls.__name__ != 'ValidationItem' and \
                any(('ERROR_MESSAGE' not in keys_, 'test' not in keys_, not callable(cls.test))):
            raise NotImplementedError('Subclass of ValidationItem')
        return cls


class ValidationItem(metaclass=ValidationMeta):
    """
    Validation item is the validation base class. 
    The subclass should implement the actual validate logic.
    """
    ERROR_MESSAGE_TEMPLATE = "The validation value must {} {}, but provided {}"
    ERROR_MESSAGE = None


    def __init__(self, *, name: str, value: Generic[T]):
        """
        :param name: The name of the argument needed to be validated
        :param value: The value used to be compared 
        """
        self._name = name
        self.value = value

    
    def validate(self, vali_value: Generic[T]) -> ValiResult:
        """
        Do validation.
        :param vali_value: The value needed to be validated
        :return: ValiResult
        """
        result = self.test(vali_value)
        return ValiResult(result, self.ERROR_MESSAGE_TEMPLATE.format(self.ERROR_MESSAGE, self.value, vali_value))


    def test(self, vali_value: Generic[T]) -> bool:
        """
        :param vali_value: The value needed to be validated
        :return: bool
        """
        pass


ValiItems = NewType('ValiItems', List[ValidationItem])


class Vali:
    """
        Validation framework base class
    """
    def __init__(self, func, valis: ValiItems):
        """
        :param func: The wrapped function
        :param valis: A list contains the main validation class instance
        """
        self.__func = func
        self.__valis = valis if isinstance(valis, collections.Iterable) else (valis,)

    def __call__(self, *args: Any, **kwargs: Any):
        self._validate(getcallargs(self.__func, *args, **kwargs))
        return self.__func(*args, **kwargs)

    def _validate(self, call_args: Dict[str, Any]):
        for vali_item in self.__valis:
            vali_result = vali_item.validate(call_args.get(vali_item._name))
            if vali_result.result == False:
                raise ValiFailError(vali_result.message)


def validator(cls=Vali, *, valis: ValiItems):
    """
    The validation decorator, can be used to decorate a function
    
    :param cls: Vali or subclass of Vali.
    :param valis: A list contains the main validation class instance
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
        :param valis: A list contains the main validation class instance
        """
        self._name = str(id(self))
        self.__valis = valis

    def __get__(self, instance: Any, owner: Any):
        if instance is None:
            return self
        return instance.__dict__.get(self._name)

    def __set__(self, instance: Any, value: Any):
        for vali in self.__valis:
            vali_result= vali.validate(value) 
            if vali_result.result == False:
                raise ValiFailError(vali_result.message)

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
